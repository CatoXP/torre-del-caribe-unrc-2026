# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Limpia dos series de FRED (Reserva Federal de St. Louis) y las guarda en Silver:
#                    fred_diario  → tipo de cambio pesos por dólar (DEXMXUS), un dato por día hábil desde 1993;
#                    fred_mensual → promedio mensual del tipo de cambio y el índice de precios al consumidor de EE. UU.
#                    (CPIAUCSL), una fila por mes.
# Por qué así:       - Los días sin cotización (fines de semana no vienen; feriados de EE. UU. vienen vacíos: 336 de
#                      8,575 filas) se conservan vacíos con sin_dato_flag. No se copia el día anterior ni se interpola
#                      (regla de oro 1).
#                    - El promedio mensual usa solo los días observados y guarda cuántos fueron (n_dias_observados),
#                      para que se vea en qué se apoya cada cifra. Alternativa descartada: último dato del mes (depende
#                      de un solo día).
#                    - El mes en curso de 2026 se marca con mes_incompleto_flag: su promedio todavía puede cambiar.
#                    - CSV → pandas → Spark escribe el Parquet.
# Datos de entrada:  datos/bronze/fred/<fecha>/DEXMXUS.csv y CPIAUCSL.csv (D10).
# Alimenta a:        A3 Pronóstico: sensibilidad del escenario al tipo de cambio ("¿qué pasa si cambia el dólar?", que
#                    mueve la llegada de visitantes de EE. UU.) y deflactar costos en dólares de los canales (D13).

import pandas as pd

from torre.base.entorno import RAIZ, crear_spark

BRONZE = RAIZ / "datos" / "bronze"
SILVER_DIARIO = RAIZ / "datos" / "silver" / "fred_diario"
SILVER_MENSUAL = RAIZ / "datos" / "silver" / "fred_mensual"


def _serie(nombre: str) -> pd.DataFrame:
    archivo = sorted(BRONZE.glob(f"fred/*/{nombre}.csv"))[-1]
    d = pd.read_csv(archivo).rename(columns={"observation_date": "fecha", nombre: "valor"})
    d["fecha"] = pd.to_datetime(d.fecha)
    d["valor"] = pd.to_numeric(d.valor, errors="coerce")  # celda vacía → nulo (no cero)
    if d.fecha.duplicated().any():
        raise ValueError(f"FRED {nombre}: fechas repetidas")
    d["archivo"] = str(archivo.relative_to(RAIZ))
    return d


def tipo_cambio_diario() -> pd.DataFrame:
    d = _serie("DEXMXUS").rename(columns={"valor": "pesos_por_dolar"})
    d["anio"], d["mes"] = d.fecha.dt.year, d.fecha.dt.month
    d["sin_dato_flag"] = d.pesos_por_dolar.isna()
    d["fecha"] = d.fecha.dt.date
    return d[["fecha", "anio", "mes", "pesos_por_dolar", "sin_dato_flag", "archivo"]]


def mensual(diario: pd.DataFrame) -> pd.DataFrame:
    tc = (diario.groupby(["anio", "mes"])
          .agg(pesos_por_dolar=("pesos_por_dolar", "mean"),       # mean ignora los nulos: solo días observados
               n_dias_observados=("pesos_por_dolar", "count"),
               n_dias_sin_dato=("sin_dato_flag", "sum"))
          .reset_index())
    ultimo = pd.Timestamp(max(diario.fecha))
    tc["mes_incompleto_flag"] = (tc.anio == ultimo.year) & (tc.mes == ultimo.month)
    cpi = _serie("CPIAUCSL").rename(columns={"valor": "inflacion_eeuu_indice"})
    cpi["anio"], cpi["mes"] = cpi.fecha.dt.year, cpi.fecha.dt.month
    m = cpi[["anio", "mes", "inflacion_eeuu_indice"]].merge(tc, on=["anio", "mes"], how="outer")
    m["periodo"] = pd.to_datetime(dict(year=m.anio, month=m.mes, day=1)).dt.date
    m["mes_incompleto_flag"] = m.mes_incompleto_flag.fillna(False).astype(bool)
    return m.sort_values("periodo").reset_index(drop=True)[
        ["periodo", "anio", "mes", "pesos_por_dolar", "n_dias_observados", "n_dias_sin_dato", "mes_incompleto_flag",
         "inflacion_eeuu_indice"]]


def construir_silver_fred(spark=None):
    spark = spark or crear_spark("silver-fred")
    dia = tipo_cambio_diario()
    mes = mensual(dia)
    spark.createDataFrame(dia).write.mode("overwrite").partitionBy("anio").parquet(str(SILVER_DIARIO))
    spark.createDataFrame(mes.astype({"n_dias_observados": "Int64", "n_dias_sin_dato": "Int64"})) \
        .write.mode("overwrite").parquet(str(SILVER_MENSUAL))
    print(f"FRED Silver: {len(dia):,} días de tipo de cambio ({dia.fecha.min()} → {dia.fecha.max()}), "
          f"{int(dia.sin_dato_flag.sum())} sin dato; {len(mes):,} meses")
    print(mes[mes.anio >= 2025].tail(6).to_string(index=False))
    return dia, mes


if __name__ == "__main__":
    construir_silver_fred()
