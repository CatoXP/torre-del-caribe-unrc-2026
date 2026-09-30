# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos (prueba)
# Qué hace:          Prueba de humo de la Fase 0: Spark lee un CSV y escribe/lee Parquet en Windows.
# Por qué así:       Es el gate de la Fase 0 del plan. Si esto no pasa, ninguna fase de datos puede empezar.
#                    Usa una tabla mínima escrita aquí mismo (no son datos del proyecto, solo prueba la
#                    herramienta), así la prueba no depende de ninguna descarga.
# Datos de entrada:  Un CSV temporal de 3 filas creado por la prueba.
# Alimenta a:        Confianza en la arquitectura Bronze → Silver → Gold.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import crear_spark  # noqa: E402


def test_spark_lee_csv_y_escribe_parquet(tmp_path):
    # 1) CSV de prueba: tres destinos con un número cualquiera.
    csv = tmp_path / "prueba.csv"
    csv.write_text("destino,valor\nChetumal,1\nCoba,2\nMuyil,3\n", encoding="utf-8")

    spark = crear_spark("prueba-fase-0")
    try:
        # 2) Spark lee el CSV (con encabezado e infiriendo tipos).
        df = spark.read.csv(str(csv), header=True, inferSchema=True)
        assert df.count() == 3

        # 3) Spark escribe Parquet: aquí es donde falla en Windows si falta winutils.
        salida = tmp_path / "prueba.parquet"
        df.write.mode("overwrite").parquet(str(salida))

        # 4) Se vuelve a leer y se comprueba la suma (1 + 2 + 3 = 6): lo escrito es lo que se leyó.
        suma = spark.read.parquet(str(salida)).groupBy().sum("valor").collect()[0][0]
        assert suma == 6
    finally:
        spark.stop()
