# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Convierte las respuestas crudas de SITUR-Q (Bronze, JSON anidado) en una tabla larga y uniforme en
#                    Silver: indicador, unidad (destino o zona), año, mes, variable, valor y banderas de calidad.
#                    Se procesa con PySpark y se guarda en Parquet, particionado por indicador.
# Por qué así:       Cada indicador de SITUR-Q trae campos distintos ("Ocupación hotelera", "Total", "Cruceristas"...).
#                    Una tabla larga (una fila por destino-mes-variable) permite tratarlos todos igual en los modelos.
#                    Reglas aplicadas, cada una verificada con los datos el 28-sep-2026:
#                    1. Tren Maya: algunos destinos traen 2 filas por mes (una por estación). Se SUMAN, porque la suma
#                       cuadra exacto con el total de zona que publica SITUR-Q. Ejemplo, descensos de ene-2025:
#                       Grand Costa Maya 7,084 = Chetumal (24 + 3,478) + Bacalar (213 + 3,369).
#                    2. Ocupación hotelera: si "habitaciones disponibles" vale 0, el mes es un HUECO (nulo con bandera).
#                       Que no haya cuartos disponibles es imposible: el indicador de habitaciones sí reporta cuartos en
#                       2025. Esto afecta a todos los destinos en 2025.
#                    3. Afluencia de turistas y derrama: un 0 también es imposible (un destino no recibe cero turistas ni
#                       cero pesos en un mes); son casillas vacías y se marcan como HUECO. Corrección del 28-sep-2026: la
#                       primera versión los conservaba y hacía parecer que había datos hasta abril y junio de 2024, cuando
#                       en realidad terminan en marzo de 2024.
#                    4. En los demás indicadores el 0 se conserva, porque puede ser real (cruceristas de 2020, con los
#                       puertos cerrados por la pandemia; zonas arqueológicas cerradas).
#                    5. Las consultas que fallaron en la fuente (respuesta nula) no generan filas: son huecos declarados
#                       en Bronze.
#                    6. Llegadas en avión: un mes en que todos los aeropuertos marcan 0 a la vez es hueco (2025–2026);
#                       un 0 aislado se conserva (Tulum antes de abrir, dic-2023).
#                    Alternativa descartada: rellenar huecos con promedios. La regla de oro 1 lo prohíbe.
# Datos de entrada:  datos/bronze/siturq/<fecha>/*.json (D1).
# Alimenta a:        Gold (hechos por destino y mes), A1 Radar y A3 Pronóstico.

import re
import unicodedata
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T

from torre.base.entorno import RAIZ, crear_spark

BRONZE_SITURQ = RAIZ / "datos" / "bronze" / "siturq"
SILVER_SITURQ = RAIZ / "datos" / "silver" / "siturq"
# Campos que describen la fila (no son medidas) y se descartan al pasar a formato largo.
NO_MEDIDAS = {"Año", "Mes", "Destino", "Nombre de destino", "Activo", "Fecha de alta", "Fecha de modificación"}


def a_snake(texto: str) -> str:
    """'Ocupación hotelera' → 'ocupacion_hotelera' (sin acentos, minúsculas, guiones bajos)."""
    sin_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", sin_acentos.lower()).strip("_")


def leer_indicador(spark: SparkSession, archivo: Path) -> DataFrame:
    """Lee un JSON de Bronze y lo deja en formato largo: una fila por unidad-año-mes-variable."""
    crudo = spark.read.option("multiLine", True).json(str(archivo))
    # Si TODAS las consultas de un indicador fallaron (respuesta nula), Spark no puede inferir la estructura y la lee
    # como texto. Pasa con "turista_afluencia" (120 de 120 errores 500 en la fuente): ese indicador no aporta filas.
    if "respuesta" not in crudo.columns or not isinstance(crudo.schema["respuesta"].dataType, T.StructType):
        return None
    # Cada registro trae una lista "data" con las filas mensuales; se "desenrolla" (explode) en filas.
    filas = (crudo.where(F.col("respuesta").isNotNull())
             .select("indicador", "unidad", "tipo_unidad", "anio", F.explode_outer("respuesta.data").alias("f"))
             .where(F.col("f").isNotNull())
             .select("indicador", "unidad", "tipo_unidad", "anio", "f.*"))
    medidas = [c for c in filas.columns if c not in NO_MEDIDAS | {"indicador", "unidad", "tipo_unidad", "anio"}]
    if not medidas:
        return None
    # stack() convierte columnas en filas: (variable, valor). El valor llega como texto ("66.50") o número.
    pares = ", ".join(f"'{a_snake(m)}', cast(`{m}` as double)" for m in medidas)
    return (filas.select("indicador", "unidad", "tipo_unidad", "anio", F.col("Mes").cast("int").alias("mes"),
                         F.expr(f"stack({len(medidas)}, {pares}) as (variable, valor)")))


def construir_silver_siturq(spark: SparkSession | None = None) -> DataFrame:
    """Une todos los indicadores de la descarga más reciente, aplica las reglas y guarda Silver en Parquet."""
    spark = spark or crear_spark("silver-siturq")
    carpeta = sorted(p for p in BRONZE_SITURQ.iterdir() if p.is_dir())[-1]  # descarga más reciente
    partes = [df for a in sorted(carpeta.glob("*.json")) if (df := leer_indicador(spark, a)) is not None]
    largo = partes[0]
    for df in partes[1:]:
        largo = largo.unionByName(df)

    # Regla 1: sumar filas repetidas del mismo destino-mes-variable (estaciones del Tren Maya).
    agregado = (largo.groupBy("indicador", "unidad", "tipo_unidad", "anio", "mes", "variable")
                .agg(F.sum("valor").alias("valor"), F.count("*").alias("n_registros_fuente")))

    # Regla 2: meses de ocupación con 0 habitaciones disponibles = hueco.
    sin_cuartos = (agregado.where((F.col("indicador") == "ocupacion_hotelera")
                                  & (F.col("variable") == "numero_de_habitaciones_disponibles") & (F.col("valor") == 0))
                   .select("indicador", "unidad", "anio", "mes").withColumn("hueco_flag", F.lit(True)))
    # Regla 3: en afluencia y derrama, el mes completo en 0 es una casilla vacía.
    flujos = ["afluencia_turistas", "derrama_turistas", "derrama_visitantes"]
    flujo_cero = (agregado.where(F.col("indicador").isin(flujos)).groupBy("indicador", "unidad", "anio", "mes")
                  .agg(F.max("valor").alias("maximo")).where("maximo = 0")
                  .select("indicador", "unidad", "anio", "mes").withColumn("hueco_flag", F.lit(True)))
    # Regla 6 (28-sep-2026): llegadas en avión. Si en un mes TODOS los aeropuertos reportan 0 a la vez, la fuente dejó de
    # publicar (así ocurre en todo 2025 y 2026: Cancún no recibió cero pasajeros) y el mes es hueco. Un 0 aislado se
    # conserva: el aeropuerto de Tulum abrió en diciembre de 2023, así que sus ceros de ese año son reales.
    aereos_cero = (agregado.where(F.col("indicador") == "aereos_llegadas").groupBy("anio", "mes")
                   .agg(F.max("valor").alias("maximo")).where("maximo = 0").select("anio", "mes"))
    aereos_hueco = (agregado.where(F.col("indicador") == "aereos_llegadas").join(aereos_cero, ["anio", "mes"])
                    .select("indicador", "unidad", "anio", "mes").distinct().withColumn("hueco_flag", F.lit(True)))
    sin_cuartos = sin_cuartos.unionByName(flujo_cero).unionByName(aereos_hueco)
    silver = (agregado.join(sin_cuartos, ["indicador", "unidad", "anio", "mes"], "left")
              .withColumn("hueco_flag", F.coalesce("hueco_flag", F.lit(False)))
              .withColumn("valor", F.when(F.col("hueco_flag"), F.lit(None).cast("double")).otherwise(F.col("valor")))
              .withColumn("periodo", F.make_date("anio", "mes", F.lit(1)))
              .withColumn("fuente", F.lit(f"SITUR-Q, descarga {carpeta.name}")))

    silver.write.mode("overwrite").partitionBy("indicador").parquet(str(SILVER_SITURQ))
    return spark.read.parquet(str(SILVER_SITURQ))


if __name__ == "__main__":
    df = construir_silver_siturq()
    resumen = (df.groupBy("indicador").agg(F.count("*").alias("filas"), F.sum(F.col("hueco_flag").cast("int")).alias("huecos"),
                                           F.min("periodo").alias("desde"), F.max("periodo").alias("hasta"))
               .orderBy("indicador"))
    resumen.show(truncate=False)
