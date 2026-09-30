# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña
# Qué hace:          Descarga una foto de referencia por cada una de las 5 regiones desde Wikimedia Commons (licencias
#                    libres CC BY / CC BY-SA), la guarda en frontend/fotos/ para que la página funcione sin internet y
#                    escribe frontend/fotos/creditos.json con autor, licencia, enlace y huella SHA-256 de cada foto.
#                    Si la foto trae coordenada GPS, comprueba que caiga en el municipio esperado de Quintana Roo.
# Por qué así:       - Brandon pidió fotos de referencia para la página (28-sep-2026).
#                    - Regla de oro 4: nada de extraer imágenes de Google, TripAdvisor o sitios que lo prohíban. Commons
#                      publica fotos con licencia libre y ofrece una API oficial para descargarlas; la licencia exige
#                      citar al autor y la licencia, y eso se muestra en la página junto a cada foto.
#                    - Se descartaron (verificado el 28-sep-2026): las fotos de Tihosuco (su título dice "Yucatan") y las
#                      de "Kantemo" (son de animales y su coordenada queda a unos 40 km del pueblo).
#                    - Se baja la versión de 1200 px de ancho que genera Commons: suficiente para la página y ligera.
# Datos de entrada:  API de Wikimedia Commons (commons.wikimedia.org/w/api.php).
# Alimenta a:        La campaña (las fichas de los 5 lugares y el teléfono de la portada).

import hashlib
import json
import re

import requests

from torre.base.entorno import RAIZ
from torre.base.ubicaciones import municipio_de

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "TorreDelCaribe/1.0 (proyecto escolar UNRC; https://commons.wikimedia.org)"}
CARPETA = RAIZ / "frontend" / "fotos"

# Clave (nombre del lugar en la página, o "Portada") → (archivo en Commons, qué muestra, municipio esperado, ancho px).
# Rediseño del 28-sep-2026: fotos de alta resolución, elegidas por calidad y ubicación comprobable. La de portada se
# baja a 2400 px (ocupa toda la pantalla); las de cada lugar, a 1600 px. La iglesia de Felipe Carrillo Puerto no trae
# coordenada: se identifica por su título en Commons ("… Felipe Carrillo Puerto Municipality, Quintana Roo").
FOTOS = {
    "Portada": ("Laguna Milagros, Q. Roo. - panoramio.jpg", "La Laguna Milagros", "004", 2400),
    "Chetumal": ("Bahía de Chetumal desde el Boulevard. - panoramio.jpg", "La bahía de Chetumal desde el Boulevard", "004", 1600),
    "Calderitas y Oxtankah": ("Calderitas - panoramio.jpg", "La bahía frente a Calderitas", "004", 1600),
    "Ruta de las pirámides": ("Dzibanche1.jpg", "La gran pirámide de Dzibanché en la selva", "004", 1600),
    "Maya Ka'an": ("Church at Filipe Carrillo Puerto, Felipe Carrillo Puerto Municipality, Quintana Roo, Mexico.jpg",
                   "Iglesia en Felipe Carrillo Puerto", "002", 1600),
    "Laguna Milagros y Xul-Ha": ("En la Laguna Milagros, Chetumal, México. - panoramio.jpg", "Un muelle en la Laguna Milagros", "004", 1600),
}


def _pedir(url: str, **kw) -> requests.Response:
    """GET con reintentos: Commons limita las consultas seguidas (visto el 28-sep-2026)."""
    import time

    for intento in range(6):
        r = requests.get(url, headers=UA, timeout=120, **kw)
        if r.status_code == 200:
            return r
        time.sleep(3 * (intento + 1))
    r.raise_for_status()
    return r


def _limpiar(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def _slug(texto: str) -> str:
    texto = texto.lower().replace("'", "")
    for a, b in zip("áéíóúñ", "aeioun"):
        texto = texto.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "_", texto).strip("_")


def descargar_fotos() -> list[dict]:
    import time

    CARPETA.mkdir(parents=True, exist_ok=True)
    for viejo in CARPETA.glob("*.jpg"):  # las fotos de la versión anterior se reemplazan
        viejo.unlink()
    creditos = []
    for region, (archivo, muestra, mun, ancho) in FOTOS.items():
        time.sleep(1)
        r = _pedir(API, params={
            "action": "query", "format": "json", "titles": "File:" + archivo, "prop": "imageinfo|coordinates",
            "iiprop": "url|extmetadata", "iiurlwidth": ancho,
            "iiextmetadatafilter": "LicenseShortName|LicenseUrl|Artist"}).json()
        pagina = next(iter(r["query"]["pages"].values()))
        info = pagina["imageinfo"][0]
        md = info.get("extmetadata", {})
        licencia = md.get("LicenseShortName", {}).get("value", "")
        if not licencia.startswith(("CC BY", "CC0", "Public domain")):
            raise ValueError(f"{archivo}: licencia '{licencia}' no permite usarla; se detiene (regla de oro 4)")
        contenido = _pedir(info["thumburl"]).content
        destino = CARPETA / f"{_slug(region)}.jpg"
        destino.write_bytes(contenido)
        coord = (pagina.get("coordinates") or [{}])[0]
        verificada = None
        if coord:
            verificada = municipio_de(coord["lat"], coord["lon"]) == mun
            if not verificada:
                raise ValueError(f"{archivo}: su coordenada no cae en el municipio esperado ({mun}); se detiene")
        creditos.append({
            "region": region, "archivo_local": f"fotos/{destino.name}", "muestra": muestra,
            "autor": _limpiar(md.get("Artist", {}).get("value", "")), "licencia": licencia,
            "url_licencia": md.get("LicenseUrl", {}).get("value", ""), "url_original": info["descriptionurl"],
            "lat": coord.get("lat"), "lon": coord.get("lon"), "coordenada_en_municipio_esperado": verificada,
            "sha256": hashlib.sha256(contenido).hexdigest(), "bytes": len(contenido),
        })
        print(f"{region:26s} {licencia:13s} {creditos[-1]['autor'][:28]:28s} "
              f"{'coordenada OK' if verificada else 'sin coordenada'} · {len(contenido) / 1024:.0f} KB")
    (CARPETA / "creditos.json").write_text(json.dumps(creditos, ensure_ascii=False, indent=2), encoding="utf-8")
    return creditos


if __name__ == "__main__":
    descargar_fotos()
