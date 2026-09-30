# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Descarga de SITUR-Q (sistema estatal de información turística de Quintana Roo) los
#                    indicadores elegidos, para cada destino, zona y año 2019–2026, y los guarda crudos en
#                    datos/bronze/siturq/<fecha>/ con su registro en el manifiesto.
# Por qué así:       SITUR-Q es la única fuente oficial con datos del SUR (Chetumal, Bacalar, Mahahual, Maya Ka'an).
#                    Su tablero público consulta una API con un token que la propia página entrega a cualquier
#                    visitante. Aquí se reproduce exactamente esa consulta del navegador (verificado el
#                    27-sep-2026: Bacalar, 145 hoteles en 2025).
#                    Se guarda la respuesta COMPLETA de la API, sin tocarla: limpiar es trabajo de Silver.
#                    Alternativa descartada: exportar a mano con el botón "Exportar Excel", indicador por
#                    indicador. No es reproducible y serían cientos de clics.
# Datos de entrada:  D1 SITUR-Q (https://siturq.gob.mx/indicadores-turisticos y su API returq.siturq.gob.mx).
# Alimenta a:        A1 Radar (presión y capacidad del sur), A3 Pronóstico (series mensuales) y la selección de
#                    regiones (docs/decisiones/01-regiones.md).

import html
import json
import re
import time
from datetime import date
from pathlib import Path

import requests

from torre.base.manifiesto import BRONZE, registrar

PAGINA = "https://siturq.gob.mx/indicadores-turisticos"
API = "https://returq.siturq.gob.mx/api/charts/getCharData"
# La API rechaza peticiones que no vienen "desde" su página ("Origin not allowed"), así que se envían los mismos
# encabezados que manda el navegador.
ENCABEZADOS = {"Origin": "https://siturq.gob.mx", "Referer": PAGINA, "User-Agent": "Mozilla/5.0 (proyecto escolar UNRC)"}

# Indicadores elegidos por Brandon el 28-sep-2026 (propuesta de la Fase 1). id de SITUR-Q → nombre corto.
INDICADORES = {
    "5ff84749-c44b-48b3-934e-b11c1114afe1": "ocupacion_hotelera",
    "5a60d7fe-ec6f-45e9-87ac-f0951926ddc3": "habitaciones",
    "0cb48138-93f7-442e-a573-2b1d9d85e1a2": "centros_hospedaje",
    "c2dbcbc1-291e-4e5b-98f1-9dde4ec8b51b": "cruceristas",
    "74e66b9b-d5ec-4361-bf0f-0344b5c2a45a": "frontera_belice",
    "a0859e5e-77d8-4fd2-92b2-4d02eda16534": "tren_maya_movimiento",
    "a081b770-672c-4353-926d-23f992f65ebb": "tren_maya_descenso",
    "321012c6-7730-4651-870a-87e772ecd290": "aereos_llegadas",
    "9c95b3c9-d11b-40ea-bc8c-05f7c19cdb73": "zonas_arqueologicas",
    "1b01eaf7-9e50-4b34-a911-665fc90fe6fd": "afluencia_turistas",
    "a002e47e-1db2-4e37-b09a-0191018c2556": "turista_afluencia",
    "ce1590d7-7ea5-44db-80a8-4ecb77ee0a94": "derrama_visitantes",
    "5942ad3c-ad95-45e7-8f34-bb074510d7cd": "derrama_turistas",
}


def leer_catalogo() -> dict:
    """Lee la página pública y extrae el token, los destinos y las zonas tal como los presenta SITUR-Q.

    Devuelve {"token": ..., "unidades": [...], "html": ...}. Cada unidad trae el cuerpo exacto que espera la API
    en el campo destinationsByZone:
      - destino suelto (Cancún, Cozumel...):         isGroup = False
      - miembro de una zona (Chetumal, Tulum...):     se consulta como destino suelto con su propio id
      - zona (Riviera Maya, Grand Costa Maya):        isGroup = True, con la lista de sus miembros
      - zona especial (Caribe Mexicano = todo el estado): isSpecial = True
    """
    pagina = requests.get(PAGINA, headers=ENCABEZADOS, timeout=60).text
    token = re.search(r'const token = "([^"]+)"', pagina).group(1)

    entradas = []
    for m in re.finditer(r"<input[^>]*>", pagina):
        t = m.group(0)
        attr = lambda nombre: (re.search(r"\s" + nombre + r'="([^"]*)"', t) or [None, ""])[1]
        if "data-special-zone" in t:
            tipo = "zona_especial"
        elif "data-zone-length" in t:
            tipo = "zona"
        elif "data-zone-destination" in t:
            tipo = "miembro"
        elif "data-destination" in t:
            tipo = "destino"
        else:
            continue
        # \sid= evita confundir el id propio con data-zone-id (error que se detectó al explorar la página)
        entradas.append({"tipo": tipo, "id": attr("id"), "nombre": html.unescape(attr("name")), "zona": attr("data-zone-id")})

    unidades = []
    for e in entradas:
        if e["tipo"] in ("destino", "miembro"):
            cuerpo = [{"groupId": e["id"], "name": e["nombre"], "isGroup": False, "isSpecial": False, "isSelected": True}]
        elif e["tipo"] == "zona":
            miembros = [{"destinationId": m["id"], "name": m["nombre"], "isSelected": True}
                        for m in entradas if m["tipo"] == "miembro" and m["zona"] == e["id"]]
            cuerpo = [{"groupId": e["id"], "name": e["nombre"], "isGroup": True, "isSpecial": False,
                       "isSelected": True, "lstDestinations": miembros}]
        else:
            cuerpo = [{"groupId": e["id"], "name": e["nombre"], "isGroup": True, "isSpecial": True,
                       "isSelected": True, "lstDestinations": []}]
        unidades.append({**e, "cuerpo": cuerpo})
    return {"token": token, "unidades": unidades, "html": pagina}


def consultar(token: str, id_indicador: str, unidad: dict, anio: int, intentos: int = 3) -> dict:
    """Pide a la API un indicador para una unidad (destino o zona) y un año completo (meses 1 a 12).

    Reintenta hasta 3 veces si la red falla. Devuelve la respuesta JSON tal cual.
    """
    formulario = {
        "indicators": json.dumps([id_indicador]),
        "isOnline": "false",
        "isAccumulated": "false",
        "typeoptiongraphic": "",
        "isDestinationComparison": "false",
        "destinationsByZone": json.dumps(unidad["cuerpo"], ensure_ascii=False),
        "conditions": json.dumps([[["month", ">=", 1], ["year", "=", anio], ["month", "<=", 12], ["year", "=", anio]]]),
    }
    for intento in range(intentos):
        try:
            r = requests.post(API, headers={**ENCABEZADOS, "Authorization": f"Bearer {token}"},
                              files={k: (None, v) for k, v in formulario.items()}, timeout=60)
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError):
            if intento == intentos - 1:
                raise
            time.sleep(2 * (intento + 1))


def descargar_siturq(anios=range(2019, 2027), pausa: float = 0.2) -> list[dict]:
    """Descarga todos los INDICADORES × unidades × años y guarda un archivo JSON crudo por indicador.

    Cada archivo contiene una lista de registros {indicador, unidad, tipo, anio, respuesta}, donde "respuesta" es
    exactamente lo que devolvió la API. La pausa entre peticiones evita saturar el servidor público.
    Devuelve las filas del manifiesto que se registraron.
    """
    catalogo = leer_catalogo()
    carpeta = BRONZE / "siturq" / date.today().isoformat()
    carpeta.mkdir(parents=True, exist_ok=True)

    # Evidencia: la página tal como estaba el día de la descarga (de ahí salen los ids).
    pagina = carpeta / "_pagina_indicadores.html"
    pagina.write_text(catalogo["html"], encoding="utf-8")
    registrar("D1 SITUR-Q", pagina, PAGINA, nota="página pública de la que salen el token y los ids")

    registros_manifiesto = []
    for id_ind, nombre in INDICADORES.items():
        if (carpeta / f"{nombre}.json").exists():  # reanudación: ese indicador ya se bajó hoy
            print(f"{nombre:22s} ya estaba, se omite")
            continue
        bloque, filas, fallidas = [], 0, 0
        for unidad in catalogo["unidades"]:
            for anio in anios:
                base = {"indicador": nombre, "id_indicador": id_ind, "unidad": unidad["nombre"],
                        "tipo_unidad": unidad["tipo"], "anio": anio}
                try:
                    resp = consultar(catalogo["token"], id_ind, unidad, anio)
                    filas += len(resp.get("data") or [])
                    bloque.append({**base, "respuesta": resp})
                except requests.RequestException as e:
                    # Regla de oro 5: el hueco se declara, no se rellena. Queda el error exacto del servidor.
                    fallidas += 1
                    bloque.append({**base, "respuesta": None, "error": repr(e)})
                time.sleep(pausa)
        archivo = carpeta / f"{nombre}.json"
        archivo.write_text(json.dumps(bloque, ensure_ascii=False), encoding="utf-8")
        nota = f"{len(catalogo['unidades'])} unidades × {len(list(anios))} años"
        if fallidas:
            nota += f"; {fallidas} consultas fallaron en el servidor (hueco declarado)"
        registros_manifiesto.append(registrar("D1 SITUR-Q", archivo, API, filas=filas, nota=nota))
        print(f"{nombre:22s} {filas:6d} filas, {fallidas} fallidas → {archivo.name}")
    return registros_manifiesto


if __name__ == "__main__":
    descargar_siturq()
