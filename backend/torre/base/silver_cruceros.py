# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Limpia la base de cruceros por puerto (DataTur, BaseDatosCruceros: arribos y pasajeros por mes,
#                    2016 → jul-2026) y la guarda en Silver. Después la compara con los cruceristas de SITUR-Q (la otra
#                    fuente del mismo dato) y guarda la diferencia en Gold.
# Por qué así:       - Los cruceros son la mayor presión de llegada del sur del estado (Mahahual: 2.38 millones de
#                      pasajeros en 2025) y alimentan la variable llegadas_x_cuarto del Radar.
#                    - Revisado el 02-oct-2026: 0 llaves repetidas. Cancún, Playa del Carmen, Puerto Morelos y Punta
#                      Venado vienen con 0 en TODOS los meses: están en el catálogo pero no reciben cruceros. Se conservan
#                      con puerto_sin_cruceros_flag; no se borran ni se rellenan.
#                    - Reconciliación (incidente de Big Data, "fuentes que no coinciden"): se compara mes a mes con SITUR-Q
#                      y se declara la diferencia. No se elige una fuente nueva: el Radar sigue con SITUR-Q (Fase 4).
# Datos de entrada:  datos/bronze/datatur/<fecha>/cruceros/BaseDatosCruceros.zip (D4); datos/silver/siturq (D1).
# Alimenta a:        A1 Radar (presión de llegada por cruceros), Fase 7 (vigilancia semanal de puertos) y el informe
#                    (reconciliación entre fuentes).

import io
import zipfile

import pandas as pd

from torre.base.entorno import RAIZ, crear_spark

BRONZE = RAIZ / "datos" / "bronze"
SILVER = RAIZ / "datos" / "silver"
SILVER_CRUCEROS = SILVER / "cruceros"
GOLD_RECONCILIACION = RAIZ / "datos" / "gold" / "reconciliacion_cruceros.parquet"

LLAVE = ["puerto", "anio", "mes"]
# Puertos de Quintana Roo → papel en la campaña (docs/regiones/REGIONES.md: Mahahual y Cozumel, excluidos).
PAPEL_QROO = {"Mahahual": "excluida", "Cozumel": "excluida", "Cancún": "referencia", "Playa del Carmen": "referencia",
              "Puerto Morelos": "excluida", "Punta Venado": "referencia"}
# Nombre del mismo puerto en SITUR-Q (columna unidad).
EN_SITURQ = {"Cozumel": "Cozumel", "Mahahual": "Mahahual"}


def leer_cruceros() -> pd.DataFrame:
    zipf = sorted(BRONZE.glob("datatur/*/cruceros/BaseDatosCruceros.zip"))[-1]
    with zipfile.ZipFile(zipf) as z:
        nombre = next(n for n in z.namelist() if n.lower().endswith(".xlsx"))
        d = pd.read_excel(io.BytesIO(z.read(nombre)))
    d = d.rename(columns={"Estado": "estado", "Puerto": "puerto", "Año": "anio", "Id_mes": "mes", "Arribos": "arribos",
                          "Pasajeros": "pasajeros", "Latitud": "lat", "Longitud": "lon", "Región": "litoral"})
    d["periodo"] = d.Fecha.dt.date
    d["archivo"] = str(zipf.relative_to(RAIZ))
    if d.duplicated(LLAVE).any():
        raise ValueError("Cruceros: llaves repetidas; revisar a mano")
    return d[["estado", "puerto", "anio", "mes", "periodo", "arribos", "pasajeros", "lat", "lon", "litoral", "archivo"]]


def agregar_banderas(d: pd.DataFrame) -> pd.DataFrame:
    total = d.groupby("puerto").pasajeros.transform("sum")
    d["puerto_sin_cruceros_flag"] = total == 0
    d["es_qroo"] = d.estado == "Quintana Roo"
    d["papel_campana"] = d.puerto.map(PAPEL_QROO).where(d.es_qroo)
    return d


def reconciliar_siturq(d: pd.DataFrame) -> pd.DataFrame:
    """Compara pasajeros de DataTur con cruceristas de SITUR-Q, mes a mes, en los puertos que tienen ambas fuentes."""
    s = pd.read_parquet(SILVER / "siturq")
    s = s[(s.indicador == "cruceristas") & ~s.hueco_flag]
    s = s.groupby(["unidad", "periodo"], observed=True).valor.sum().reset_index()
    filas = []
    for puerto, unidad in EN_SITURQ.items():
        dt = d[d.puerto == puerto][["periodo", "pasajeros"]]
        st = s[s.unidad == unidad][["periodo", "valor"]].rename(columns={"valor": "cruceristas_siturq"})
        st["periodo"] = pd.to_datetime(st.periodo).dt.date
        m = dt.merge(st, on="periodo", how="inner")
        m.insert(0, "puerto", puerto)
        filas.append(m.rename(columns={"pasajeros": "pasajeros_datatur"}))
    r = pd.concat(filas, ignore_index=True)
    r["diferencia"] = r.cruceristas_siturq - r.pasajeros_datatur
    r["diferencia_pct"] = (r.diferencia / r.pasajeros_datatur.where(r.pasajeros_datatur > 0) * 100).round(2)
    return r


def construir_silver_cruceros(spark=None) -> pd.DataFrame:
    spark = spark or crear_spark("silver-cruceros")
    d = agregar_banderas(leer_cruceros())
    spark.createDataFrame(d.astype({"papel_campana": "object"})).write.mode("overwrite").partitionBy("anio") \
        .parquet(str(SILVER_CRUCEROS))
    q = d[d.es_qroo]
    print(f"Cruceros Silver: {len(d):,} filas; Quintana Roo: {len(q):,} filas, "
          f"{q[q.puerto_sin_cruceros_flag].puerto.nunique()} puertos sin cruceros en toda la serie")
    r = reconciliar_siturq(d)
    r.to_parquet(GOLD_RECONCILIACION, index=False)
    anual = r.assign(anio=pd.to_datetime(r.periodo).dt.year).groupby(["puerto", "anio"])[
        ["pasajeros_datatur", "cruceristas_siturq"]].sum()
    anual["diferencia_pct"] = ((anual.cruceristas_siturq / anual.pasajeros_datatur - 1) * 100).round(2)
    print("DataTur vs SITUR-Q por año:\n" + anual.to_string())
    return d


if __name__ == "__main__":
    construir_silver_cruceros()
