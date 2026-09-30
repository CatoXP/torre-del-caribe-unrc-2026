# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Limpia el Censo de Población y Vivienda 2020 de Quintana Roo por localidad (INEGI, ITER) y lo
#                    guarda en Silver: población, viviendas habitadas, servicios de las viviendas (agua entubada,
#                    drenaje, electricidad) y coordenadas en grados decimales. A cada localidad le pone la región de la
#                    campaña a la que pertenece (o "referencia"), para calcular turistas por residente.
# Por qué así:       - Decisión de Brandon (28-sep-2026): la población de cada región se mide POR LOCALIDAD, no por
#                      municipio, porque 4 de las 5 regiones están en Othón P. Blanco (233,648 habitantes) y a nivel
#                      municipio no se podrían distinguir. Alternativa descartada: municipio.
#                    - La lista de localidades de cada región es un criterio del proyecto; está en REGION_LOCALIDADES
#                      con su justificación y se defiende en docs/decisiones/05-planteamiento.md.
#                    - Servicios de vivienda = criterio 4 de selección (fragilidad de servicios: agua, drenaje).
#                    - INEGI reserva algunos valores con "*" (confidencialidad) o "N/D": se guardan como nulos con
#                      reservado_flag, nunca como 0 (regla de oro 1).
#                    - Se conservan solo las filas de localidad: las de total estatal (MUN 000), total municipal
#                      (LOC 0000) y "localidades de una o dos viviendas" (LOC 9998/9999) se separan con tipo_fila.
# Datos de entrada:  datos/bronze/iter/<fecha>/iter_23_cpv2020_csv.zip (D7).
# Alimenta a:        Fase 3 (tabla de criterios: turistas por residente y servicios), A1 Radar (presión por residente)
#                    y el mapa de la página (coordenadas de cada región).

import re
import zipfile

import pandas as pd

from torre.base.entorno import RAIZ, crear_spark

BRONZE_ITER = RAIZ / "datos" / "bronze" / "iter"
SILVER_ITER = RAIZ / "datos" / "silver" / "iter"
COLUMNAS = {"MUN": "cve_mun", "NOM_MUN": "municipio", "LOC": "cve_loc", "NOM_LOC": "localidad", "LATITUD": "latitud_gms",
            "LONGITUD": "longitud_gms", "POBTOT": "poblacion", "TVIVPARHAB": "viviendas_habitadas",
            "VPH_AGUADV": "viviendas_con_agua", "VPH_DRENAJ": "viviendas_con_drenaje", "VPH_C_ELEC": "viviendas_con_luz"}
NUMERICAS = ["poblacion", "viviendas_habitadas", "viviendas_con_agua", "viviendas_con_drenaje", "viviendas_con_luz"]

# Región de la campaña → localidades (clave de municipio, clave de localidad, nombre esperado). El nombre se comprueba
# al construir: si INEGI cambia una clave, el proceso se detiene en lugar de asignar la localidad equivocada.
REGION_LOCALIDADES = {
    "Chetumal": [("004", "0001", "Chetumal")],
    "Bahía Calderitas–Oxtankah": [("004", "0016", "Calderitas")],               # Oxtankah está junto a Calderitas
    "Laguna Milagros–Xul-Ha": [("004", "0114", "Xul-Ha"), ("004", "0037", "Huay-Pix")],  # las dos orillas habitadas
    "Ruta arqueológica del sur": [("004", "0064", "Nicolás Bravo"), ("004", "0245", "Morocoy"),
                                  ("004", "0033", "Francisco Villa")],         # poblados de acceso a Kohunlich y Dzibanché
    "Maya Ka'an + Kantemó": [("002", "0001", "Felipe Carrillo Puerto"), ("002", "0250", "Tihosuco"),
                             ("002", "0239", "Señor"), ("002", "0044", "Chunhuhub"), ("006", "0076", "Kantemó")],
    # Referencia (no se promueve): las cabeceras donde hoy está el turista.
    "Cancún (referencia)": [("005", "0001", "Cancún")],
    "Playa del Carmen (referencia)": [("008", "0001", "Playa del Carmen")],
    "Tulum (referencia)": [("009", "0001", "Tulum")],
}


def _grados(texto) -> float | None:
    """Convierte '88°17\\'52.436" W' a grados decimales (−88.2979). Así publica el ITER las coordenadas."""
    if not isinstance(texto, str):
        return None
    m = re.match(r"(\d+)°(\d+)'([\d.]+)\"\s*([NSEW])", texto.strip())
    if not m:
        return None
    g, mi, s, h = m.groups()
    valor = int(g) + int(mi) / 60 + float(s) / 3600
    return -valor if h in "SW" else valor


def leer_iter() -> pd.DataFrame:
    zipf = sorted(BRONZE_ITER.glob("*/iter_23_cpv2020_csv.zip"))[-1]
    with zipfile.ZipFile(zipf) as z:
        nombre = next(n for n in z.namelist() if "conjunto_de_datos" in n and n.endswith(".csv"))
        d = pd.read_csv(z.open(nombre), dtype=str)
    faltan = set(COLUMNAS) - set(d.columns)
    if faltan:
        raise ValueError(f"ITER: no existen las columnas {sorted(faltan)}; revisar el diccionario de datos")
    d = d[list(COLUMNAS)].rename(columns=COLUMNAS)
    d["tipo_fila"] = "localidad"
    d.loc[d.cve_loc == "0000", "tipo_fila"] = "total_municipal"
    d.loc[d.cve_mun == "000", "tipo_fila"] = "total_estatal"
    d.loc[d.cve_loc.isin(["9998", "9999"]), "tipo_fila"] = "localidades_pequenas"
    reservado = d[NUMERICAS].isin(["*", "N/D"]).any(axis=1)
    for c in NUMERICAS:
        d[c] = pd.to_numeric(d[c].where(~d[c].isin(["*", "N/D"])), errors="coerce").astype("Int64")
    d["reservado_flag"] = reservado
    d["latitud"] = d.latitud_gms.map(_grados)
    d["longitud"] = d.longitud_gms.map(_grados)
    d["archivo"] = str(zipf.relative_to(RAIZ))
    return d.drop(columns=["latitud_gms", "longitud_gms"])


def asignar_regiones(d: pd.DataFrame) -> pd.DataFrame:
    d["region_campana"] = None
    d["papel_campana"] = None
    for region, localidades in REGION_LOCALIDADES.items():
        for mun, loc, esperado in localidades:
            fila = (d.cve_mun == mun) & (d.cve_loc == loc)
            if fila.sum() != 1 or d.loc[fila, "localidad"].iloc[0] != esperado:
                encontrado = d.loc[fila, "localidad"].tolist()
                raise ValueError(f"ITER: {mun}-{loc} debía ser {esperado} y es {encontrado}; no se asigna a ciegas")
            d.loc[fila, "region_campana"] = region.replace(" (referencia)", "")
            d.loc[fila, "papel_campana"] = "referencia" if "(referencia)" in region else "promovida"
    return d


def construir_silver_iter(spark=None):
    spark = spark or crear_spark("silver-iter")
    d = asignar_regiones(leer_iter())
    spark.createDataFrame(d.astype({c: "float64" for c in NUMERICAS}).astype(
        {"region_campana": "object", "papel_campana": "object"})).write.mode("overwrite").parquet(str(SILVER_ITER))
    loc = d[d.tipo_fila == "localidad"]
    estatal = int(d.loc[d.tipo_fila == "total_estatal", "poblacion"].iloc[0])
    print(f"ITER Silver: {len(d):,} filas; {len(loc):,} localidades; población estatal {estatal:,}; "
          f"{int(loc.reservado_flag.sum()):,} localidades con algún dato reservado por INEGI")
    resumen = (d[d.region_campana.notna()].groupby(["papel_campana", "region_campana"])
               [["poblacion", "viviendas_habitadas", "viviendas_con_agua", "viviendas_con_drenaje"]].sum())
    print(resumen.to_string())
    return d


if __name__ == "__main__":
    construir_silver_iter()
