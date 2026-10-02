# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña
# Qué hace:          Descarga 4 a 6 fotos de cada lugar desde Wikimedia Commons y COMPRUEBA que cada una se haya tomado
#                    dentro del municipio del lugar (su coordenada GPS cae en el polígono oficial de Othón P. Blanco o
#                    Felipe Carrillo Puerto; Benito Juárez para Cancún y Solidaridad para la Riviera Maya). Las guarda en
#                    frontend/fotos/lugares/ con su crédito.
# Por qué así:       - Brandon (01-oct-2026): "que sean fotos de las zonas que sí sean de Quintana Roo" y "foto dependiendo
#                      qué escojan". La galería de comida anterior usaba fotos de Mérida y Campeche: rompía la regla de
#                      ubicación comprobada de docs/decisiones/06-pagina.md y la regla de oro 9. Esta pieza la corrige.
#                    - Solo fotos CON coordenada GPS, y la coordenada se prueba con torre.base.ubicaciones.municipio_de()
#                      (el mismo mapa municipal que validó los lugares). Si una foto no tiene coordenada o cae en otro
#                      municipio, el proceso se detiene (regla de oro 5).
#                    - Revisadas a ojo (01-oct-2026). Rechazadas, entre otras: fotos de "Kohunlich" con coordenada en
#                      Felipe Carrillo Puerto (a más de 100 km: coordenada equivocada), fotos satelitales, insectos y una
#                      serpiente en una cueva cuya coordenada no coincide con Kantemó.
#                    - En Commons no hay fotos de PLATILLOS con coordenada en los 5 lugares (se buscó: 331 fotos con
#                      coordenada y 0 de comida). Por eso la galería de platillos se retiró; se usan fotos reales de
#                      restaurantes y del malecón donde existen.
#                    - Cancún y Riviera Maya (decisión 15, 01-oct-2026): Brandon los agregó al planeador como referencia
#                      ("que aparezca"). Misma regla: coordenada dentro de su municipio. Se rechazaron a ojo las playas con
#                      sargazo (Cancún tiene varias en Commons) y cualquier foto que mencione Tulum o Cozumel.
#                    - Licencias libres (CC BY, CC BY-SA, CC0); crédito visible junto a cada foto. 1,400 px de ancho
#                      (sirven de fondo de portada), JPEG de calidad 72 o menos para quedar bajo 400 KB.
# Datos de entrada:  API de Wikimedia Commons; datos/bronze/geo (polígonos municipales, vía ubicaciones.py).
# Alimenta a:        La portada-planeador (la foto cambia con el lugar elegido) y la galería de cada lugar.

import hashlib
import io
import json
import re
import time

import requests
from PIL import Image

from torre.base.entorno import RAIZ
from torre.base.ubicaciones import MUNICIPIO_ESPERADO, municipio_de

MUNICIPIOS = {**MUNICIPIO_ESPERADO, "005": "Benito Juárez", "008": "Solidaridad"}

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "TorreDelCaribe/1.0 (proyecto escolar UNRC; https://commons.wikimedia.org)"}
CARPETA = RAIZ / "frontend" / "fotos" / "lugares"
ANCHO = 1400
LIBRE = ("CC BY", "CC0", "Public domain", "Public Domain")

# Lugar → municipio esperado (clave INEGI) y lista de (archivo en Commons, qué muestra).
FOTOS = {
    "Chetumal": ("004", [
        ("Monumento al Pescador al atardecer, Chetumal. - panoramio.jpg", "El Monumento al Pescador al atardecer, en la bahía"),
        ("Kiosko, Chetumal. - panoramio.jpg", "El kiosco del centro de Chetumal"),
        ("Casas típicas en el Boulevard Bahía, Chetumal, Q. Roo - panoramio.jpg", "Casas típicas de madera en el Boulevard Bahía"),
        ("Bahía Villamar, Chetumal, Q. Roo. - panoramio.jpg", "Restaurante Bahía Villamar, en una casa de madera"),
        ("Monumeto a la Bandera - panoramio.jpg", "El Monumento a la Bandera frente a la bahía"),
        ("Campana del Bicentenario, Chetumal, Q. Roo - panoramio.jpg", "La Campana del Bicentenario"),
    ]),
    "Bahía Calderitas–Oxtankah": ("004", [
        ("Bahía desde Calderitas, Q. Roo. - panoramio.jpg", "La bahía vista desde Calderitas"),
        ("Atardece en Calderitas, Q. Roo. - panoramio.jpg", "Atardecer en una calle de Calderitas"),
        ("Parque y Restaurantes en Calderitas, Q. Roo al atardecer. - panoramio.jpg", "El parque y los restaurantes de Calderitas al atardecer"),
        ("Tomb 1 pyramid, oxtankah.jpg", "Pirámide de la Tumba 1, en Oxtankah"),
        ("Structure 4, oxtankah - Maya Ruins.jpg", "Estructura 4 de Oxtankah, con pintura original"),
        ("Old chapel, oxtankah.jpg", "La capilla antigua dentro de la zona de Oxtankah"),
    ]),
    "Ruta arqueológica del sur": ("004", [
        ("Dzibanche, Building 1, Temple of the Owl (14364450242).jpg", "Dzibanché: el Templo del Búho"),
        ("Kohunlich IMG 2633.JPG", "Kohunlich: una de sus plataformas en la selva"),
        ("Kohunlich 21.JPG", "Kohunlich: los mascarones de estuco"),
        ("Dzibanche estructura 2.jpg", "Dzibanché: la Estructura 2"),
        ("Kohunlich Mask.JPG", "Kohunlich: detalle de un mascarón"),
        ("Kohunlich Ball Court Seating.JPG", "Kohunlich: el juego de pelota"),
    ]),
    "Maya Ka'an + Kantemó": ("002", [
        ("Avenida Constituyentes - panoramio.jpg", "Avenida Constituyentes, en Felipe Carrillo Puerto"),
        ("Strangler fig.JPG", "Un matapalo en la selva de Felipe Carrillo Puerto"),
        ("Papilio rogeri? (8132957950).jpg", "Mariposa en la selva cerca de Chunhuhub"),
        ("Yellow-bordered Owl (Caligo uranus) (8009828309).jpg", "Mariposa búho cerca de Chunhuhub"),
    ]),
    "Laguna Milagros–Xul-Ha": ("004", [
        ("Laguna Milagros, Q. Roo, México. - panoramio.jpg", "Nadar en la Laguna Milagros"),
        ("En Huay Pix, a orillas de la Laguna Milagros, Q. Roo - panoramio.jpg", "Palapas en Huay-Pix, a la orilla de la laguna"),
        ("Aves en el muelle, Laguna Milagros, Q. Roo. - panoramio.jpg", "Aves en un muelle de la Laguna Milagros"),
        ("En Huay Pix, Q. Roo, México. - panoramio.jpg", "La orilla de la laguna en Huay-Pix"),
        ("Laguna Milagros, Huay Pix, Q. Roo. - panoramio (1).jpg", "El agua turquesa de la Laguna Milagros"),
        ("Cenote XulHa - panoramio.jpg", "El cenote de Xul-Ha"),
    ]),
    # Referencia (no se promueve): para quien pensaba ir al norte.
    "Cancún": ("005", [
        # Primero la vista aérea: es la foto de la portada y sus sombrillas no quedan detrás del texto.
        ("Cancún - Playa Gaviota Azul - 03.jpg", "Playa Gaviota Azul, en la punta de Cancún"),
        ("Cancun Beach.jpg", "Playa de la zona hotelera de Cancún"),
        ("El Meco Site Cancun, Mexico (8950890091).jpg", "Zona arqueológica de El Meco"),
        ("Mercado 28 Cancun, Mexico Julio 2012 - 01.jpg", "El Mercado 28, en el centro de Cancún"),
        ("LAGUNA NICHUPTE DESDE EL HOTEL ELAN - panoramio.jpg", "La laguna Nichupté"),
        ("Cancun Sunset - panoramio.jpg", "Atardecer sobre la laguna de Cancún"),
    ]),
    "Riviera Maya": ("008", [
        ("Aerial of Playa del Carmen in Mexico (41787340480).jpg", "Playa del Carmen desde el aire"),
        ("Fundadores Park Playa del Carmen, Mexico (29725330708).jpg", "El Portal Maya del parque Fundadores"),
        ("Quinta Avenida (2026).jpg", "La Quinta Avenida de Playa del Carmen"),
        ("Flying Men Dance, Playa del Carmen, Mexico 1.jpg", "Los Voladores en el parque Fundadores"),
        ("Playa del Carmen church - panoramio.jpg", "La capilla de Nuestra Señora del Carmen"),
        ("Town beach of Playa del Carmen - panoramio.jpg", "La playa del pueblo, en Playa del Carmen"),
    ]),
}

# Comida (02-oct-2026, decisión 17): fotos de platillos con coordenada dentro de Benito Juárez y Solidaridad. En los lugares
# del sur no existe ninguna (decisión 14): ahí la comida llegará con los aportes del equipo.
COMIDA = {
    "Cancún": ("005", [
        ("Panuchos! Absolutely delicious - 8 pesos.jpg", "Panuchos, el antojito yucateco"),
        ("Mojitos and Guacamole (49611704466).jpg", "Guacamole y mojitos"),
        ("Seafood Lunch (13012786553).jpg", "Comida de mariscos frente al mar"),
        ("Las Quesadillas D'Luis (12990959394).jpg", "Un puesto de quesadillas"),
        ("Taqueria Coapenitos (49611957747).jpg", "Una taquería del centro"),
    ]),
    "Riviera Maya": ("008", [
        ("First meal in Playa del Carmen. Sorry -- nothing special, just chicken fajitas (= tourist food).jpg",
         "Fajitas de pollo en Playa del Carmen"),
        ("Playa del Carmen, Quintana Roo, Mexico (December 28, 2013) - Restaurant - 03.jpg", "Cocina mexicana en la Quinta Avenida"),
        ("Playa del Carmen, Quintana Roo, Mexico (December 28, 2013) - Restaurant - 02.jpg", "Cenar en la calle, de noche"),
    ]),
}


def _pedir(params: dict | None = None, url: str = API) -> requests.Response:
    for intento in range(6):
        r = requests.get(url, params=params, headers=UA, timeout=120)
        if r.status_code == 200:
            return r
        time.sleep(3 * (intento + 1))
    r.raise_for_status()
    return r


def _limpiar(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def _slug(texto: str) -> str:
    import unicodedata
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


def descargar() -> list[dict]:
    CARPETA.mkdir(parents=True, exist_ok=True)
    creditos = []
    tareas = [(lugar, mun, fotos, "lugar") for lugar, (mun, fotos) in FOTOS.items()]
    tareas += [(lugar, mun, fotos, "comida") for lugar, (mun, fotos) in COMIDA.items()]
    for lugar, mun, fotos, tipo in tareas:
        for n, (archivo, muestra) in enumerate(fotos, start=1):
            d = _pedir({"action": "query", "titles": f"File:{archivo}", "prop": "imageinfo|coordinates", "format": "json",
                        "iiprop": "url|extmetadata", "iiurlwidth": ANCHO}).json()
            p = next(iter(d["query"]["pages"].values()))
            if "imageinfo" not in p:
                raise ValueError(f"{archivo}: no existe en Commons (regla de oro 5)")
            info, md = p["imageinfo"][0], p["imageinfo"][0].get("extmetadata", {})
            licencia = md.get("LicenseShortName", {}).get("value", "")
            if not licencia.startswith(LIBRE):
                raise ValueError(f"{archivo}: licencia '{licencia}' no permitida (regla de oro 4)")
            c = (p.get("coordinates") or [None])[0]
            if not c:
                raise ValueError(f"{archivo}: sin coordenada GPS; no se puede comprobar el lugar (decisión 06)")
            if municipio_de(c["lat"], c["lon"]) != mun:
                raise ValueError(f"{archivo}: la coordenada no cae en {MUNICIPIOS[mun]} (decisión 06)")
            im = Image.open(io.BytesIO(_pedir(url=info["thumburl"]).content)).convert("RGB")
            im.thumbnail((ANCHO, ANCHO))
            # Calidad adaptable: las fotos con mucho follaje (Kohunlich) pesaban 510 KB a calidad 72; se baja de 4 en 4
            # hasta quedar bajo 400 KB, para que la página siga ligera en el celular.
            for calidad in range(72, 47, -4):
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=calidad, optimize=True, progressive=True)
                if buf.tell() < 400 * 1024:
                    break
            nombre = f"{_slug(lugar)}{'_comida' if tipo == 'comida' else ''}_{n}.jpg"
            (CARPETA / nombre).write_bytes(buf.getvalue())
            creditos.append({
                "lugar": lugar, "tipo": tipo, "orden": n, "muestra": muestra, "archivo": f"fotos/lugares/{nombre}",
                "ancho": im.width, "alto": im.height, "lat": round(c["lat"], 5), "lon": round(c["lon"], 5),
                "municipio": MUNICIPIOS[mun], "autor": _limpiar(md.get("Artist", {}).get("value", "")),
                "licencia": licencia, "url_licencia": md.get("LicenseUrl", {}).get("value", ""),
                "url_original": info["descriptionurl"], "sha256": hashlib.sha256(buf.getvalue()).hexdigest(),
            })
            print(f"{lugar[:24]:24s} {n} {MUNICIPIOS[mun]:22s} {licencia:13s} {len(buf.getvalue()) // 1024:4d} KB  {muestra}")
            time.sleep(0.8)
    (CARPETA / "creditos.json").write_text(json.dumps(creditos, ensure_ascii=False, indent=1), encoding="utf-8")
    return creditos


if __name__ == "__main__":
    c = descargar()
    print(f"{len(c)} fotos · {sum((RAIZ / 'frontend' / x['archivo']).stat().st_size for x in c) / 1024 / 1024:.1f} MB")
