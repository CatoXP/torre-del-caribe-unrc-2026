# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Comprueba que cada una de las 5 regiones (y cada pueblo y zona arqueológica que la forman) esté en
#                    Quintana Roo y en el municipio esperado, con tres pruebas independientes:
#                    1) el pueblo existe en el Censo 2020 de Quintana Roo (INEGI, clave de estado 23);
#                    2) la zona arqueológica aparece con Estado = "Quintana Roo" en la base del INAH;
#                    3) su coordenada cae dentro del polígono del municipio esperado (mapa municipal de Q. Roo).
# Por qué así:       Brandon pidió confirmar que los lugares sean de Quintana Roo y no de otros estados (28-sep-2026).
#                    Algunos nombres se repiten en otros lugares (hay un "Xul-Ha" en Puerto Morelos y un "Felipe Carrillo
#                    Puerto" en Solidaridad), así que no basta con buscar el nombre: se usa la clave oficial y el mapa.
#                    Alternativa descartada: confiar en notas de prensa; no son una fuente de ubicación.
# Datos de entrada:  datos/silver/iter, datos/silver/inah, datos/bronze/geo/*/quintana_roo.json y los puntos de clima
#                    de la Fase 1 (Kohunlich).
# Alimenta a:        La selección de regiones (Fase 3), el mapa de la página y las fotos de referencia.

import json
from pathlib import Path

import pandas as pd

from torre.base.entorno import RAIZ
from torre.base.silver_iter import REGION_LOCALIDADES

SILVER = RAIZ / "datos" / "silver"
BRONZE = RAIZ / "datos" / "bronze"

# Municipio esperado de cada región promovida (clave INEGI), según docs/regiones/REGIONES.md D.5.
MUNICIPIO_ESPERADO = {"004": "Othón P. Blanco", "002": "Felipe Carrillo Puerto", "006": "José María Morelos"}
ZONAS_INAH = {"Bahía Calderitas–Oxtankah": ["Z.A. de Oxtankah"],
              "Ruta arqueológica del sur": ["Z.A. de Kohunlich", "Z.A. de Dzibanché-Kinichná", "Z.A de Ichkabal"]}


def _dentro(lon: float, lat: float, anillo: list) -> bool:
    """Prueba del rayo: un punto está dentro de un polígono si una línea horizontal cruza su borde un número impar de veces."""
    dentro, j = False, len(anillo) - 1
    for i in range(len(anillo)):
        xi, yi = anillo[i][:2]
        xj, yj = anillo[j][:2]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            dentro = not dentro
        j = i
    return dentro


def municipio_de(lat: float, lon: float) -> str | None:
    """Clave del municipio de Quintana Roo que contiene el punto; None si el punto está fuera del estado."""
    geo = json.loads(sorted(BRONZE.glob("geo/*/quintana_roo.json"))[-1].read_text(encoding="utf-8"))
    for f in geo["features"]:
        poligonos = f["geometry"]["coordinates"] if f["geometry"]["type"] == "MultiPolygon" else [f["geometry"]["coordinates"]]
        if any(_dentro(lon, lat, p[0]) for p in poligonos):
            return f["properties"]["CVE_MUN"]
    return None


def verificar_regiones() -> pd.DataFrame:
    """Una fila por pueblo o zona arqueológica, con las pruebas que pasó. Todas deben ser True."""
    from torre.base.ingesta_abiertas import PUNTOS_CLIMA

    censo = pd.read_parquet(SILVER / "iter")
    inah = pd.read_parquet(SILVER / "inah", columns=["nombre", "estado"]).drop_duplicates()
    filas = []
    for region, localidades in REGION_LOCALIDADES.items():
        if "(referencia)" in region:
            continue
        for mun, loc, nombre in localidades:
            c = censo[(censo.cve_mun == mun) & (censo.cve_loc == loc)].iloc[0]
            en_poligono = municipio_de(float(c.latitud), float(c.longitud))
            filas.append({"region": region, "lugar": nombre, "tipo": "pueblo (Censo 2020)",
                          "municipio": MUNICIPIO_ESPERADO[mun], "lat": round(float(c.latitud), 4),
                          "lon": round(float(c.longitud), 4),
                          "censo_quintana_roo": c.localidad == nombre,  # el archivo del Censo es solo del estado 23
                          "dentro_del_municipio": en_poligono == mun})
        for zona in ZONAS_INAH.get(region, []):
            estados = set(inah[inah.nombre == zona].estado)
            filas.append({"region": region, "lugar": zona, "tipo": "zona arqueológica (INAH)", "municipio": None,
                          "inah_quintana_roo": estados == {"Quintana Roo"}})
    lat, lon = PUNTOS_CLIMA["kohunlich"]
    filas.append({"region": "Ruta arqueológica del sur", "lugar": "Kohunlich (punto del mapa)", "tipo": "coordenada",
                  "municipio": MUNICIPIO_ESPERADO["004"], "lat": lat, "lon": lon,
                  "dentro_del_municipio": municipio_de(lat, lon) == "004"})
    return pd.DataFrame(filas)


if __name__ == "__main__":
    v = verificar_regiones()
    pruebas = [c for c in ("censo_quintana_roo", "inah_quintana_roo", "dentro_del_municipio") if c in v]
    v["todo_bien"] = v[pruebas].apply(lambda f: all(x for x in f if pd.notna(x)), axis=1)
    print(v.drop(columns=["lat", "lon"]).to_string(index=False))
    print("\nResultado:", "TODOS en Quintana Roo y en su municipio" if v.todo_bien.all() else "HAY LUGARES QUE REVISAR")
