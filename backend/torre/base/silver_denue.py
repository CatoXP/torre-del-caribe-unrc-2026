# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Procesa con PySpark los 6.1 millones de negocios del DENUE (INEGI, 32 estados) y los guarda en
#                    Silver: giro (código SCIAN), tamaño (personas ocupadas), ubicación (estado, municipio, localidad,
#                    latitud y longitud) y si es oferta turística. Se particiona por estado.
# Por qué así:       - Volumen real: es la tabla más grande del proyecto y sostiene el criterio de Big Data. Brandon
#                      decidió procesarla completa (28-sep-2026) para comparar Quintana Roo contra el país.
#                    - Privacidad (incidente de Big Data): se DESCARTAN razón social, teléfono y correo. La razón social
#                      puede ser el nombre de una persona física (la primera fila del archivo de Q. Roo lo es). Para la
#                      campaña bastan el giro, el tamaño y la ubicación.
#                    - Oferta turística = giros característicos del turismo según SECTUR/INEGI (decisión de Brandon):
#                      721 alojamiento, 722 alimentos y bebidas, 5615 agencias de viajes, 487 transporte turístico,
#                      712 museos y sitios históricos, 713 esparcimiento.
#                    - Los archivos vienen en latin-1 (verificado el 28-sep-2026), no en UTF-8.
#                    - Spark no lee zips: los CSV se descomprimen en una carpeta temporal que se borra al final. Bronze
#                      no se toca.
# Datos de entrada:  datos/bronze/denue/<fecha>/denue_*_csv.zip (D6; 33 archivos, el Estado de México en 2 partes).
# Alimenta a:        A1 Radar (densidad de oferta turística por destino), la selección de regiones (Fase 3) y la campaña
#                    (qué servicios hay para el visitante en cada lugar).

import shutil
import zipfile
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from torre.base.entorno import RAIZ, crear_spark

BRONZE_DENUE = RAIZ / "datos" / "bronze" / "denue"
SILVER_DENUE = RAIZ / "datos" / "silver" / "denue"
TEMPORAL = RAIZ / "datos" / "silver" / "_temporal_denue"

# Prefijo SCIAN → categoría turística. Se revisa primero el prefijo de 4 dígitos (5615) y luego los de 3.
CATEGORIAS_TURISTICAS = {
    "721": "Alojamiento", "722": "Alimentos y bebidas", "5615": "Agencias de viajes",
    "487": "Transporte turístico", "712": "Museos y sitios históricos", "713": "Esparcimiento",
}
COLUMNAS = ["id", "nom_estab", "codigo_act", "nombre_act", "per_ocu", "tipoUniEco", "cve_ent", "entidad", "cve_mun",
            "municipio", "cve_loc", "localidad", "cod_postal", "latitud", "longitud", "fecha_alta"]


def descomprimir(carpeta: Path) -> Path:
    """Extrae solo el CSV de datos de cada zip a la carpeta temporal (se omiten diccionario y metadatos)."""
    if TEMPORAL.exists():
        shutil.rmtree(TEMPORAL)
    TEMPORAL.mkdir(parents=True)
    for z in sorted(carpeta.glob("denue_*_csv.zip")):
        with zipfile.ZipFile(z) as arch:
            for n in arch.namelist():
                if n.startswith("conjunto_de_datos/") and n.lower().endswith(".csv"):
                    (TEMPORAL / Path(n).name).write_bytes(arch.read(n))
    return TEMPORAL


def construir_silver_denue(spark: SparkSession | None = None):
    spark = spark or crear_spark("silver-denue")
    carpeta = sorted(p for p in BRONZE_DENUE.iterdir() if p.is_dir())[-1]
    temporal = descomprimir(carpeta)
    try:
        crudo = (spark.read.option("header", True).option("encoding", "ISO-8859-1")
                 .option("quote", '"').option("escape", '"').csv(str(temporal / "*.csv")))
        n_crudo = crudo.count()

        scian = F.col("codigo_act")
        categoria = F.when(scian.startswith("5615"), CATEGORIAS_TURISTICAS["5615"])
        for prefijo in ("721", "722", "487", "712", "713"):
            categoria = categoria.when(scian.startswith(prefijo), CATEGORIAS_TURISTICAS[prefijo])

        # "11 a 30 personas" → mínimo 11 y máximo 30; "251 y más personas" → mínimo 251, sin máximo.
        rango = F.regexp_extract_all(F.col("per_ocu"), F.lit(r"(\d+)"), 1)
        lat, lon = F.col("latitud").cast("double"), F.col("longitud").cast("double")

        silver = (crudo.select(*COLUMNAS)
                  .dropDuplicates(["id"])                                       # un negocio, una fila
                  .withColumn("localidad", F.trim("localidad"))
                  .withColumn("scian_3", F.substring("codigo_act", 1, 3))
                  .withColumn("categoria_turistica", categoria)
                  .withColumn("es_turistico", F.col("categoria_turistica").isNotNull())
                  .withColumn("personas_min", rango.getItem(0).cast("int"))
                  .withColumn("personas_max", rango.getItem(1).cast("int"))
                  .withColumn("latitud", lat).withColumn("longitud", lon)
                  # Bandera de calidad: coordenadas vacías o fuera de México (latitud 14–33 N, longitud 86–119 O).
                  .withColumn("coordenadas_flag", ~(lat.between(14, 33) & lon.between(-119, -86)) | lat.isNull())
                  .withColumn("es_qroo", F.col("cve_ent") == "23")
                  .withColumn("fuente", F.lit(f"INEGI DENUE, descarga {carpeta.name}")))
        silver.write.mode("overwrite").partitionBy("cve_ent").parquet(str(SILVER_DENUE))
    finally:
        shutil.rmtree(temporal, ignore_errors=True)  # la carpeta temporal nunca se queda en disco
    resultado = spark.read.parquet(str(SILVER_DENUE))
    return resultado, n_crudo


if __name__ == "__main__":
    df, n_crudo = construir_silver_denue()
    total = df.count()
    print(f"Registros leídos: {n_crudo:,} | negocios únicos en Silver: {total:,} | duplicados quitados: {n_crudo - total:,}")
    df.groupBy("es_qroo", "es_turistico").count().orderBy("es_qroo", "es_turistico").show()
    (df.where("es_qroo and es_turistico").groupBy("municipio", "categoria_turistica").count()
     .groupBy("municipio").pivot("categoria_turistica").sum("count").fillna(0).orderBy("municipio").show(truncate=False))
    print("Coordenadas con problema:", df.where("coordenadas_flag").count())
