# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Limpia el corpus de reseñas Rest-Mex 2025 (208,051 reseñas de turistas en México, con calificación de
#                    1 a 5, pueblo, estado y tipo: hotel, restaurante o atractivo) y lo guarda en Silver. PySpark lee
#                    el CSV directo (el texto trae saltos de línea dentro de las comillas).
# Por qué así:       - Es el único texto de turistas con licencia libre (CC-BY-4.0). TripAdvisor y Google no se pueden
#                      extraer (regla de oro 4).
#                    - Ojo con lo que NO cubre: en Quintana Roo solo trae Tulum (45,345), Isla Mujeres (29,826) y Bacalar
#                      (10,822). Ninguno de los 5 lugares de la campaña. Por eso sirve para saber qué molesta en los
#                      destinos llenos (multitudes, precio, sargazo), no para opinar del sur.
#                    - 178 filas idénticas en todas sus columnas (misma reseña dos veces) → se deja una. Revisado el
#                      02-oct-2026.
#                    - Nombres "QuintanaRoo" e "Isla_Mujeres" → "Quintana Roo" e "Isla Mujeres". Tipo en español.
#                    - Alternativa descartada: guardar solo Quintana Roo. El país entero sirve para comparar y es el
#                      volumen que se procesa con Spark.
# Datos de entrada:  datos/bronze/restmex/<fecha>/Rest-Mex_2025_train.csv (D5).
# Alimenta a:        Fase 8 (minería de texto: temas, sentimiento y lenguaje real para los mensajes de la campaña).

import re

from pyspark.sql import functions as F

from torre.base.entorno import RAIZ, crear_spark

BRONZE = RAIZ / "datos" / "bronze"
SILVER_RESTMEX = RAIZ / "datos" / "silver" / "restmex"

TIPOS = {"Hotel": "hotel", "Restaurant": "restaurante", "Attractive": "atractivo"}
# Papel de los pueblos de Quintana Roo en la campaña (docs/regiones/REGIONES.md).
PAPEL_QROO = {"Tulum": "referencia", "Isla Mujeres": "excluida", "Bacalar": "excluida"}


def nombre_legible(texto: str) -> str:
    """'QuintanaRoo' → 'Quintana Roo'; 'Estado_de_Mexico' → 'Estado de Mexico'; 'Baja_CaliforniaSur' → 'Baja California Sur'."""
    t = texto.replace("_", " ")
    return re.sub(r"(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ])", " ", t).strip()


def leer_restmex(spark):
    archivo = sorted(BRONZE.glob("restmex/*/Rest-Mex_2025_train.csv"))[-1]
    df = (spark.read.option("header", True).option("multiLine", True).option("escape", '"').option("quote", '"')
          .option("encoding", "UTF-8").csv(str(archivo)))
    return df, archivo


def limpiar(df, archivo):
    legible = F.udf(nombre_legible)
    mapa_tipo = F.create_map(*[F.lit(x) for kv in TIPOS.items() for x in kv])
    mapa_papel = F.create_map(*[F.lit(x) for kv in PAPEL_QROO.items() for x in kv])
    d = (df.dropDuplicates()
         .select(F.col("Title").alias("titulo"), F.col("Review").alias("resena"),
                 F.col("Polarity").cast("double").cast("int").alias("calificacion"),
                 legible("Town").alias("pueblo"), legible("Region").alias("estado"),
                 mapa_tipo[F.col("Type")].alias("tipo"))
         .withColumn("es_qroo", F.col("estado") == "Quintana Roo")
         .withColumn("papel_campana", F.when(F.col("es_qroo"), mapa_papel[F.col("pueblo")]))
         .withColumn("n_palabras", F.size(F.split(F.trim(F.col("resena")), r"\s+")))
         .withColumn("archivo", F.lit(str(archivo.relative_to(RAIZ)))))
    return d


def construir_silver_restmex(spark=None):
    spark = spark or crear_spark("silver-restmex")
    df, archivo = leer_restmex(spark)
    crudas = df.count()
    d = limpiar(df, archivo)
    d.write.mode("overwrite").partitionBy("estado").parquet(str(SILVER_RESTMEX))
    final = spark.read.parquet(str(SILVER_RESTMEX))
    n = final.count()
    print(f"Rest-Mex Silver: {n:,} reseñas ({crudas - n} idénticas quitadas de {crudas:,})")
    final.filter("es_qroo").groupBy("pueblo", "tipo").count().orderBy("pueblo", "tipo").show(truncate=False)
    nulos = final.filter(F.col("tipo").isNull() | F.col("calificacion").isNull()).count()
    if nulos:
        raise ValueError(f"Rest-Mex: {nulos} reseñas sin tipo o sin calificación; revisar la lectura del CSV")
    return final


if __name__ == "__main__":
    construir_silver_restmex()
