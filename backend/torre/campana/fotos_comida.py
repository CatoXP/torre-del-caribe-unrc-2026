# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña
# Qué hace:          Descarga 24 fotos de platillos de la península de Yucatán desde Wikimedia Commons (licencias libres),
#                    las reduce para la página, las guarda en frontend/fotos/comida/ y escribe creditos.json con autor,
#                    licencia, enlace, huella SHA-256 y una descripción corta de cada platillo.
# Por qué así:       - Brandon pidió (01-oct-2026) "muchísimas fotos de toda la comida: de la vista nace el amor".
#                    - Regla de oro 4: solo fotos con licencia libre (CC BY, CC BY-SA, CC0 o dominio público) de la API
#                      oficial de Commons; nada de Google ni TripAdvisor. La licencia obliga a mostrar autor y licencia
#                      junto a cada foto, y así se hace en la página.
#                    - Cada foto se revisó A OJO en hojas de contacto (01-oct-2026). Se rechazaron, por ejemplo: "relleno
#                      negro" (la búsqueda trajo alfajores argentinos), ceviches de Perú, Israel y Brasil, escabeches de
#                      Filipinas y del País Vasco, tamales de Venezuela y Filipinas, cocos de Filipinas, elotes de
#                      Xochimilco y un supermercado peruano. También restaurantes de Estados Unidos.
#                    - Regla de oro 9: se descarta toda foto cuyo título, descripción o categorías mencionen Tulum, Cancún,
#                      Playa del Carmen, Cozumel, Holbox, Isla Mujeres, Bacalar, Mahahual, Riviera Maya o Cobá.
#                    - Las fotos son de REFERENCIA del platillo (tomadas en Mérida, Campeche, Oxkutzcab, Quintana Roo y
#                      otros lugares); no son de los negocios del DENUE que lista la página, y así se dice.
#                    - Se guardan a 1000 px de ancho en JPEG calidad 80: la galería se ve nítida y la página sigue ligera.
# Datos de entrada:  API de Wikimedia Commons (commons.wikimedia.org/w/api.php).
# Alimenta a:        La campaña: galería "La comida del sur" y antojos en "Dónde comer" (la comida como razón para ir al
#                    sur; piezas publicitarias de la Fase 8).

import hashlib
import io
import json
import re
import time

import requests
from PIL import Image

from torre.base.entorno import RAIZ

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "TorreDelCaribe/1.0 (proyecto escolar UNRC; https://commons.wikimedia.org)"}
CARPETA = RAIZ / "frontend" / "fotos" / "comida"
ANCHO = 1000
LIBRE = ("CC BY", "CC0", "Public domain", "Public Domain")
EXCLUIR = re.compile(r"tulum|canc[uú]n|playa del carmen|cozumel|holbox|isla mujeres|bacalar|mahahual|riviera maya|cob[aá]",
                     re.I)

# clave → (archivo en Commons, nombre, grupo, descripción corta)
# Grupos: "mar" (pescados y mariscos), "yucateca" (cocina yucateca), "antojitos", "bebidas" (bebidas, café y dulces).
PLATILLOS = {
    "cochinita_pibil": ("Cochinita pibil 2.jpg", "Cochinita pibil", "yucateca",
                        "Cerdo adobado en achiote y naranja agria, cocido lento en hoja de plátano."),
    "tacos_de_cochinita": ("Cochinita pibil mercado de santa ana.jpg", "Tacos de cochinita", "antojitos",
                           "La cochinita en tortilla, con cebolla morada encurtida."),
    "relleno_negro": ("PavoRellenoNegro 03.JPG", "Relleno negro", "yucateca",
                      "Pavo en recado negro, una salsa de chiles tostados."),
    "panuchos": ("Panuchos from Santa Ana Market (43438745182).jpg", "Panuchos", "antojitos",
                 "Tortilla rellena de frijol y frita, con carne, aguacate y cebolla."),
    "salbutes": ("Salbutes de pescado, Mercado Municipal, Oxkutzcab, Yucatan, Mexico.jpg", "Salbutes", "antojitos",
                 "Tortilla inflada y frita; estos llevan pescado."),
    "poc_chuc": ("Poc chuc.jpg", "Poc chuc", "yucateca", "Cerdo asado marinado en naranja agria."),
    "papadzules": ("Papadzules in Quintana Roo, Mexico.jpg", "Papadzules", "yucateca",
                   "Tortillas rellenas de huevo, bañadas en salsa de pepita de calabaza."),
    "sopa_de_lima": ("Sopa de lima yucateca en Mercado Santa Anita de Mérida 03.jpg", "Sopa de lima", "yucateca",
                     "Caldo de pollo con lima y tiras de tortilla frita."),
    "tikin_xic": ("Pescado en Tikin Xic servido en Campeche 01.jpg", "Pescado tikin xic", "mar",
                  "Pescado adobado en achiote y asado envuelto en hoja de plátano."),
    "queso_relleno": ("Queso relleno yucateco.jpg", "Queso relleno", "yucateca",
                      "Queso de bola relleno de carne molida con especias."),
    "empanadas": ("Empanadas Fritas.jpg", "Empanadas", "antojitos", "Masa de maíz rellena y frita, con salsa."),
    "tamales": ("Comidas de méxico 04.jpg", "Tamal en hoja de plátano", "antojitos",
                "Masa de maíz cocida al vapor en hoja de plátano."),
    "mucbipollo": ("Mucbipollo.jpg", "Mucbipollo", "yucateca",
                   "Tamal grande que se hornea bajo tierra para el Hanal Pixán, el día de muertos maya."),
    "marquesitas": ("Marquesitas.jpg", "Marquesitas", "bebidas", "Crepa crujiente enrollada con queso de bola."),
    "horchata": ("Horchata, my drink of choice in Mexico - Merida Yucatan 21 March 2021.jpg", "Horchata", "bebidas",
                 "Agua fresca de arroz con canela."),
    "frijol_con_puerco": ("Frijol con puerco 01.JPG", "Frijol con puerco", "yucateca",
                          "Frijol negro cocido con carne de cerdo."),
    "tacos_al_pastor": ("Al pastor tacos 2.jpg", "Tacos al pastor", "antojitos", "Cerdo adobado al trompo, con piña."),
    "agua_de_chaya": ("Agua de piña con chaya.jpg", "Agua de chaya con piña", "bebidas",
                      "Bebida de chaya, una hoja verde de la región maya."),
    "pan_de_cazon": ("Pan de Cazon Fried tortilla and shark meat Campeche Mexico.jpg", "Pan de cazón", "mar",
                     "Tortillas en capas con cazón y frijol, bañadas en salsa de tomate."),
    "coctel_de_camaron": ("Cóctel de camarones.jpg", "Cóctel de camarones", "mar",
                          "Camarón en salsa de tomate con aguacate, con tostadas."),
    "vuelve_a_la_vida": ("Un vuelve a la vida.jpg", "Vuelve a la vida", "mar", "Cóctel de mariscos variados."),
    "pescado_frito": ("Pescado recien salido de mar frito.jpg", "Pescado frito", "mar", "Pescado entero frito."),
    "cafe_de_olla": ("Café de olla .jpg", "Café de olla", "bebidas", "Café con canela y piloncillo."),
    "chile_habanero": ("Habanero chilies from Stockmann.jpg", "Chile habanero", "yucateca",
                       "El chile de la península, base de la salsa xnipec."),
}


def _pedir(params: dict | None = None, url: str = API) -> requests.Response:
    """GET con reintentos: Commons limita las consultas seguidas."""
    for intento in range(6):
        r = requests.get(url, params=params, headers=UA, timeout=120)
        if r.status_code == 200:
            return r
        time.sleep(3 * (intento + 1))
    r.raise_for_status()
    return r


def _limpiar(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def descargar() -> list[dict]:
    CARPETA.mkdir(parents=True, exist_ok=True)
    creditos = []
    for clave, (archivo, nombre, grupo, desc) in PLATILLOS.items():
        d = _pedir({"action": "query", "titles": f"File:{archivo}", "prop": "imageinfo", "format": "json",
                    "iiprop": "url|extmetadata", "iiurlwidth": ANCHO * 2}).json()
        pagina = next(iter(d["query"]["pages"].values()))
        if "imageinfo" not in pagina:
            raise ValueError(f"{archivo}: no existe en Commons; se detiene (regla de oro 5)")
        info = pagina["imageinfo"][0]
        md = info.get("extmetadata", {})
        licencia = md.get("LicenseShortName", {}).get("value", "")
        if not licencia.startswith(LIBRE):
            raise ValueError(f"{archivo}: licencia '{licencia}' no permite usarla (regla de oro 4)")
        texto = " ".join([archivo, md.get("ImageDescription", {}).get("value", ""), md.get("Categories", {}).get("value", "")])
        if EXCLUIR.search(texto):
            raise ValueError(f"{archivo}: menciona un lugar excluido (regla de oro 9)")
        im = Image.open(io.BytesIO(_pedir(url=info["thumburl"]).content)).convert("RGB")
        im.thumbnail((ANCHO, ANCHO * 2))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=80, optimize=True, progressive=True)
        destino = CARPETA / f"{clave}.jpg"
        destino.write_bytes(buf.getvalue())
        creditos.append({
            "clave": clave, "nombre": nombre, "grupo": grupo, "descripcion": desc, "archivo": f"fotos/comida/{clave}.jpg",
            "ancho": im.width, "alto": im.height,
            "autor": _limpiar(md.get("Artist", {}).get("value", "")) or "autor sin nombre en Commons",
            "licencia": licencia, "url_licencia": md.get("LicenseUrl", {}).get("value", ""),
            "url_original": info["descriptionurl"], "sha256": hashlib.sha256(buf.getvalue()).hexdigest(),
        })
        print(f"{nombre:26s} {licencia:13s} {creditos[-1]['autor'][:30]:30s} {len(buf.getvalue()) // 1024} KB")
        time.sleep(1)
    (CARPETA / "creditos.json").write_text(json.dumps(creditos, ensure_ascii=False, indent=1), encoding="utf-8")
    return creditos


if __name__ == "__main__":
    c = descargar()
    print(f"{len(c)} fotos · {sum((CARPETA / (x['clave'] + '.jpg')).stat().st_size for x in c) / 1024 / 1024:.1f} MB")
