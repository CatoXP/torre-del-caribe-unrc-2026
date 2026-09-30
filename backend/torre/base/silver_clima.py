# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Limpia el clima de Open-Meteo (reanálisis ERA5) de 8 puntos de Quintana Roo y lo guarda en Silver en
#                    dos tablas: clima_diario (1950–2026: temperatura máxima, lluvia del día y viento máximo) y
#                    clima_horario (2019–2026: temperatura, lluvia y viento de cada hora).
# Por qué así:       - Dos tablas porque responden preguntas distintas: la diaria da 76 años para medir la temporada de
#                      lluvias (variable del Pronóstico mensual) y la horaria alimenta el flujo casi en tiempo real de
#                      la Torre en vivo (Fase 7). Alternativa descartada: una sola tabla con huecos donde no hay hora.
#                    - Horas: el crudo horario viene en UTC (utc_offset_seconds = 0) y el diario ya viene en hora de
#                      Cancún. Se guardan las dos horas en la tabla horaria. Quintana Roo usa UTC−5 fijo desde el
#                      1-feb-2015, así que en 2019–2026 la hora local es UTC − 5 h sin cambios de horario.
#                    - Revisión del 30-sep-2026: 128 archivos, 224,232 filas diarias y 542,784 horarias, 0 nulos. Si
#                      algún día llega un nulo, se conserva nulo con sin_dato_flag (regla de oro 1: no se rellena).
#                    - Es reanálisis (modelo meteorológico que asimila observaciones), no una estación: se declara en
#                      la columna fuente_tipo. No lleva _est porque es un producto oficial, no un cálculo nuestro.
#                    - Cada punto lleva su papel en la campaña (regla de oro 9): promovida, referencia o excluida.
#                    - JSON → pandas → Spark escribe el Parquet particionado por año.
# Datos de entrada:  datos/bronze/clima/<fecha>/diario/<punto>_<década>s.json y horario/<punto>_<año>.json (D8).
# Alimenta a:        A3 Pronóstico (lluvia y temperatura como variables del modelo con clima; en qué meses la lluvia
#                    cambia el mensaje de la campaña) y A5 Torre en vivo (alertas de lluvia o viento de la semana).

import json

import pandas as pd

from torre.base.entorno import RAIZ, crear_spark

BRONZE = RAIZ / "datos" / "bronze"
SILVER_DIARIO = RAIZ / "datos" / "silver" / "clima_diario"
SILVER_HORARIO = RAIZ / "datos" / "silver" / "clima_horario"

# Papel de cada punto (docs/regiones/REGIONES.md; regla de oro 9 de CLAUDE.md).
PAPEL_PUNTO = {
    "chetumal": ("Chetumal", "promovida"),
    "kohunlich": ("Ruta arqueológica del sur", "promovida"),
    "felipe_carrillo_puerto": ("Maya Ka'an + Kantemó", "promovida"),
    "cancun": ("Cancún", "referencia"),
    "playa_del_carmen": ("Riviera Maya", "referencia"),
    "tulum": ("Tulum", "referencia"),
    "bacalar": ("Bacalar", "excluida"),
    "coba": ("Cobá + Punta Laguna", "excluida"),
}
NOMBRES = {"temperature_2m_max": "temp_max_c", "precipitation_sum": "lluvia_mm", "wind_speed_10m_max": "viento_max_kmh",
           "temperature_2m": "temp_c", "precipitation": "lluvia_mm", "wind_speed_10m": "viento_kmh"}


def _leer(tipo: str) -> pd.DataFrame:
    """Une todos los archivos de un tipo ('diario' u 'horario') de la descarga más reciente."""
    carpeta = sorted(BRONZE.glob("clima/*/"))[-1] / tipo
    partes = []
    for archivo in sorted(carpeta.glob("*.json")):
        crudo = json.loads(archivo.read_text(encoding="utf-8"))
        clave = "daily" if tipo == "diario" else "hourly"
        p = pd.DataFrame(crudo[clave]).rename(columns=NOMBRES)
        p["punto"] = archivo.stem.rsplit("_", 1)[0]
        p["lat"], p["lon"] = crudo["latitude"], crudo["longitude"]  # celda de la malla ERA5 que devolvió la API
        p["archivo"] = str(archivo.relative_to(RAIZ))
        partes.append(p)
    d = pd.concat(partes, ignore_index=True)
    duplicadas = d.duplicated(["punto", "time"]).sum()
    if duplicadas:  # regla de oro 5: dos lecturas del mismo punto y hora no se resuelven solas
        raise ValueError(f"Clima {tipo}: {duplicadas} filas repetidas por punto y tiempo")
    return d


def _papel(d: pd.DataFrame) -> pd.DataFrame:
    d["region_campana"] = d.punto.map(lambda p: PAPEL_PUNTO[p][0])
    d["papel_campana"] = d.punto.map(lambda p: PAPEL_PUNTO[p][1])
    d["fuente_tipo"] = "reanálisis ERA5 (Open-Meteo)"
    return d


def clima_diario() -> pd.DataFrame:
    d = _leer("diario")
    d["fecha"] = pd.to_datetime(d.pop("time")).dt.date
    d["anio"] = pd.to_datetime(d.fecha).dt.year
    d["mes"] = pd.to_datetime(d.fecha).dt.month
    d["sin_dato_flag"] = d[["temp_max_c", "lluvia_mm", "viento_max_kmh"]].isna().any(axis=1)
    return _papel(d)[["punto", "region_campana", "papel_campana", "fecha", "anio", "mes", "temp_max_c", "lluvia_mm",
                      "viento_max_kmh", "sin_dato_flag", "lat", "lon", "fuente_tipo", "archivo"]]


def clima_horario() -> pd.DataFrame:
    d = _leer("horario")
    d["fecha_hora_utc"] = pd.to_datetime(d.pop("time"))
    d["fecha_hora_local"] = d.fecha_hora_utc - pd.Timedelta(hours=5)  # UTC−5 fijo en Q. Roo desde 2015
    d["anio"] = d.fecha_hora_local.dt.year
    d["sin_dato_flag"] = d[["temp_c", "lluvia_mm", "viento_kmh"]].isna().any(axis=1)
    return _papel(d)[["punto", "region_campana", "papel_campana", "fecha_hora_utc", "fecha_hora_local", "anio", "temp_c",
                      "lluvia_mm", "viento_kmh", "sin_dato_flag", "lat", "lon", "fuente_tipo", "archivo"]]


def construir_silver_clima(spark=None):
    spark = spark or crear_spark("silver-clima")
    dia, hora = clima_diario(), clima_horario()
    spark.createDataFrame(dia).write.mode("overwrite").partitionBy("anio").parquet(str(SILVER_DIARIO))
    spark.createDataFrame(hora).write.mode("overwrite").partitionBy("anio").parquet(str(SILVER_HORARIO))
    print(f"Clima Silver: diario {len(dia):,} filas ({dia.fecha.min()} → {dia.fecha.max()}), "
          f"horario {len(hora):,} filas; puntos: {dia.punto.nunique()}; sin dato: {int(dia.sin_dato_flag.sum())} días, "
          f"{int(hora.sin_dato_flag.sum())} horas")
    lluvia = (dia[(dia.punto == "chetumal") & dia.anio.between(1991, 2020)]
              .groupby(["anio", "mes"]).lluvia_mm.sum().groupby("mes").mean().round(0))
    print("Chetumal, lluvia media mensual 1991–2020 (mm):", lluvia.to_dict())
    return dia, hora


if __name__ == "__main__":
    construir_silver_clima()
