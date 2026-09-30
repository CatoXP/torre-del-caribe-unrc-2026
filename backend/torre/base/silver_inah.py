# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Limpia la base de visitantes del INAH (DataTur, BdINAH: museos y zonas arqueológicas de todo el
#                    país, 2016–2026) y la guarda en Silver con una fila por sitio, mes y tipo de visitante (nacional o
#                    extranjero). A las zonas de Quintana Roo les agrega su papel en la campaña: promovida (una de las
#                    5 regiones), referencia, retirada o excluida.
# Por qué así:       - Es la fuente medida de presión turística que sí llega a 2026 en el sur (SITUR-Q no tiene
#                      ocupación hotelera 2025–2026). Sostiene la tabla de criterios de la Fase 3.
#                    - Duplicado detectado el 28-sep-2026: el bloque "Extranjero, septiembre de 2025" viene dos veces
#                      (283 sitios × 2). Una copia trae las cifras y la otra puros ceros. Se conserva la fila con cifra.
#                      Si alguna vez aparecen dos cifras distintas de cero para la misma llave, el proceso se detiene
#                      (regla de oro 5): no se elige una al azar.
#                    - El papel de cada zona sale de docs/regiones/REGIONES.md (D.5, 28-sep-2026). Alternativa
#                      descartada: guardar solo Quintana Roo; se conserva el país para comparar (criterio 2).
#                    - Los ceros se conservan: un mes con 0 visitantes suele ser un cierre (Muyil, jun-2024 a feb-2026)
#                      y se marca con sin_visitantes_flag, no se borra.
#                    - Excel → pandas (Spark no lee Excel) y Spark escribe el Parquet particionado, igual que DataTur.
# Datos de entrada:  datos/bronze/datatur/<fecha>/inah/BdINAH.zip (D4).
# Alimenta a:        Fase 3 (tabla de criterios de las 5 regiones), A1 Radar (visitas INAH como variable de presión) y
#                    la campaña (qué sitios de la ruta sur crecen en 2026).

import io
import zipfile
from pathlib import Path

import pandas as pd

from torre.base.entorno import RAIZ, crear_spark

BRONZE = RAIZ / "datos" / "bronze"
SILVER_INAH = RAIZ / "datos" / "silver" / "inah"

# Papel de cada sitio INAH de Quintana Roo en la campaña (docs/regiones/REGIONES.md, D.5).
PAPEL_QROO = {
    "Z.A. de Oxtankah": ("Bahía Calderitas–Oxtankah", "promovida"),
    "Z.A. de Kohunlich": ("Ruta arqueológica del sur", "promovida"),
    "Z.A. de Dzibanché-Kinichná": ("Ruta arqueológica del sur", "promovida"),
    "Z.A de Ichkabal": ("Ruta arqueológica del sur", "promovida"),
    "Z.A. de Tulum": ("Tulum", "referencia"),
    "Z.A. de El Rey": ("Cancún", "referencia"),
    "Z.A. de El Meco": ("Cancún", "referencia"),
    "Museo Maya de Cancún con Z. A": ("Cancún", "referencia"),
    "Z.A. de Xcaret": ("Riviera Maya", "referencia"),
    "Z.A. de Xelhá": ("Riviera Maya", "referencia"),
    "Z.A. de Cobá": ("Cobá + Punta Laguna", "retirada"),
    "Z.A. de Muyil": ("Muyil", "retirada"),
    "Z.A. de Chacchoben": ("Chacchoben", "excluida"),
    "Z.A. de San Gervasio": ("Cozumel", "excluida"),
}
LLAVE = ["estado", "nombre", "anio", "mes", "tipo_visitante"]


def leer_inah() -> pd.DataFrame:
    """Lee el Excel que viene dentro del zip más reciente de Bronze y pone nombres en español y snake_case."""
    zipf = sorted(BRONZE.glob("datatur/*/inah/BdINAH.zip"))[-1]
    with zipfile.ZipFile(zipf) as z:
        nombre = next(n for n in z.namelist() if n.lower().endswith(".xlsx"))
        d = pd.read_excel(io.BytesIO(z.read(nombre)))
    d = d.rename(columns={"Clasificación INAH": "clasificacion", "Estado": "estado", "Nombre": "nombre", "Año": "anio",
                          "id_mes": "mes", "Visitantes": "visitantes", "Tipo": "tipo_visitante"})
    d["tipo_visitante"] = d.tipo_visitante.str.lower()
    d["periodo"] = pd.to_datetime(dict(year=d.anio, month=d.mes, day=1)).dt.date
    d["archivo"] = str(zipf.relative_to(RAIZ))
    return d[["clasificacion", "estado", "nombre", "anio", "mes", "periodo", "tipo_visitante", "visitantes", "archivo"]]


def quitar_duplicados(d: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Por cada llave repetida conserva la fila con cifra. Se detiene si hay dos cifras distintas de cero."""
    grupos = d.groupby(LLAVE).visitantes
    conflicto = grupos.apply(lambda v: (v > 0).sum() > 1)
    if conflicto.any():
        raise ValueError(f"INAH: {int(conflicto.sum())} llaves con dos cifras distintas de cero; revisar a mano")
    antes = len(d)
    d = d.sort_values("visitantes", ascending=False).drop_duplicates(LLAVE, keep="first")
    return d.sort_values(LLAVE).reset_index(drop=True), antes - len(d)


def agregar_papel(d: pd.DataFrame) -> pd.DataFrame:
    es_qroo = d.estado == "Quintana Roo"
    d["region_campana"] = d.nombre.map(lambda n: PAPEL_QROO.get(n, (None, None))[0]).where(es_qroo)
    d["papel_campana"] = d.nombre.map(lambda n: PAPEL_QROO.get(n, (None, None))[1]).where(es_qroo)
    d["es_qroo"] = es_qroo
    d["sin_visitantes_flag"] = d.visitantes == 0
    return d


def construir_silver_inah(spark=None):
    spark = spark or crear_spark("silver-inah")
    d = leer_inah()
    d, quitadas = quitar_duplicados(d)
    d = agregar_papel(d)
    df = spark.createDataFrame(d.astype({"region_campana": "object", "papel_campana": "object"}))
    df.write.mode("overwrite").partitionBy("anio").parquet(str(SILVER_INAH))
    q = d[d.es_qroo]
    print(f"INAH Silver: {len(d):,} filas ({quitadas} duplicadas quitadas); Quintana Roo: {len(q):,} filas, "
          f"{q.nombre.nunique()} sitios")
    anual = (q[q.anio == 2025].groupby(["papel_campana", "region_campana"]).visitantes.sum()
             .sort_values(ascending=False))
    print("Visitantes 2025 por región y papel:\n" + anual.to_string())
    return d


if __name__ == "__main__":
    construir_silver_inah()
