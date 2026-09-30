# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Convierte los 166 Excel de ocupación hotelera de DataTur (135 semanales y 31 mensuales) en una
#                    tabla limpia en Silver: centro turístico, año, semana o mes, cuartos disponibles, cuartos
#                    ocupados y porcentaje de ocupación, con una sola versión por periodo.
# Por qué así:       Cada archivo compara TRES años del mismo periodo: el de la semana 31 de 2026 trae la semana 31 de
#                    2024, 2025 y 2026; el de 2024 trae 2022, 2023 y 2024. Por eso la serie semanal va de 2022 a 2026
#                    (verificado el 28-sep-2026) y cada periodo aparece en varios archivos. DataTur marca las cifras
#                    como preliminares y las corrige después, así que se conserva la versión del ARCHIVO MÁS
#                    RECIENTE y se cuenta cuántas veces cambió (revisado_flag).
#                    Los Excel se leen con openpyxl porque Spark no lee Excel de forma nativa. Son archivos pequeños;
#                    la unión, la deduplicación y la escritura en Parquet las hace Spark.
#                    Se conservan los 54 centros del país (contexto nacional) y se marca es_qroo. Las filas de
#                    subtotal ("Total", "Centros de Playa"...) se marcan tipo_fila = "agregado".
#                    Las celdas "n.d." (no disponible) y "n.c." (no comparable) se guardan como nulo con bandera.
# Datos de entrada:  datos/bronze/datatur/<fecha>/hoteleria/*.zip (D2 y D2m).
# Alimenta a:        A1 Radar (ocupación semanal del norte), A3 Pronóstico y la reconciliación con SITUR-Q.

import io
import re
import zipfile
from datetime import date
from pathlib import Path

import openpyxl
from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F

from torre.base.entorno import RAIZ, crear_spark

BRONZE_HOTELERIA = RAIZ / "datos" / "bronze" / "datatur"
SILVER = RAIZ / "datos" / "silver" / "datatur_ocupacion"
MESES = {m: i for i, m in enumerate(["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                                     "septiembre", "octubre", "noviembre", "diciembre"], start=1)}
# Columnas del Excel (misma posición en los 166 archivos): años en 2-4, 9-11 y 16-18.
AGREGADOS = {"Total", "Centros De Playa", "Integralmente Planeados", "Tradicionales", "Otros", "Ciudades",
             "Grandes", "Del Interior", "Fronterizas"}
BLOQUES = {"cuartos_disponibles": (2, 3, 4), "cuartos_ocupados": (9, 10, 11), "ocupacion_pct": (16, 17, 18)}


def _numero(celda):
    """Número o None. 'n.d.' / 'n.c.' / vacío → None."""
    return float(celda) if isinstance(celda, (int, float)) else None


def leer_archivo(ruta: Path) -> list[dict]:
    """Lee un zip de DataTur (semanal o mensual) y devuelve una fila por centro y año."""
    with zipfile.ZipFile(ruta) as z:
        nombre_xlsx = next(n for n in z.namelist() if n.lower().endswith(".xlsx"))
        libro = openpyxl.load_workbook(io.BytesIO(z.read(nombre_xlsx)), read_only=True, data_only=True)
    hoja = libro.worksheets[0]  # la primera hoja es el periodo; la segunda, el acumulado del año (no se usa)
    filas = list(hoja.iter_rows(values_only=True))
    libro.close()

    titulo = str(filas[1][2])
    anios = [int(re.sub(r"\D", "", str(filas[6][c]))) for c in BLOQUES["cuartos_disponibles"]]
    semanal = "Semana" in titulo
    periodo = int(re.search(r"Semana\s+(\d+)", titulo).group(1)) if semanal else \
        MESES[re.search(r"Mes de (\w+)", titulo).group(1).lower()]
    # Orden del archivo para decidir cuál es "el más reciente": (año del archivo, número de semana o mes).
    orden = (anios[-1], periodo)

    # Notas al pie del archivo ("4/ A partir del 1 de septiembre 2025 se actualizó la oferta hotelera..."). Los centros
    # las referencian con marcas como "ISLA MUJERES, Q. ROO /4". Se guardan porque indican cortes de comparabilidad.
    notas = {}
    for fila in filas[9:]:
        texto = str(fila[1] or "").strip()
        m = re.match(r"^(\d+)/\s*(.+)", texto)
        if m and not any(isinstance(c, (int, float)) for c in fila[2:19]):
            notas[m.group(1)] = m.group(2).strip()

    salida = []
    for fila in filas[9:]:
        centro_crudo = str(fila[1] or "").strip()
        # Solo son filas de datos las que traen algún número; así se descartan notas, fechas y la línea de "Fuente".
        if not centro_crudo or not any(isinstance(c, (int, float)) for c in fila[2:19]):
            continue
        es_centro = "," in centro_crudo
        nombre, _, estado = centro_crudo.partition(",")
        marca = re.search(r"/(\d+)", centro_crudo)
        # El estado se escribe distinto entre archivos ("Q.ROO", "Q. ROO", "B.C.S.1/", "BC", "B.C."): se quitan espacios,
        # puntos y marcas de nota, y queda la abreviatura limpia ("QROO", "BCS", "BC").
        estado = re.sub(r"[\s.]|/?\d+/?", "", estado).upper()
        if len(estado) > 5:  # no es una abreviatura de estado sino una nota al pie con comas y números: se descarta
            continue
        # Limpia marcas de nota ("/3", " 2/") y puntos finales: "Ciudad De México 2/" → "Ciudad De México".
        nombre = re.sub(r"\s*(/\d+|\d+/)\s*$", "", nombre).strip().rstrip(".").title()
        tipo = "centro" if es_centro else ("agregado" if nombre in AGREGADOS else "desglose")
        for i, anio in enumerate(anios):
            valores = {var: fila[cols[i]] for var, cols in BLOQUES.items()}
            salida.append({
                "frecuencia": "semanal" if semanal else "mensual",
                "centro": nombre, "estado": estado or None, "centro_crudo": centro_crudo, "tipo_fila": tipo,
                "es_qroo": estado == "QROO",
                "anio": anio, "semana": periodo if semanal else None, "mes": None if semanal else periodo,
                # Fecha de inicio del periodo: lunes de la semana ISO (así numera DataTur; la semana 31 de 2026 empieza
                # el 27-jul-2026, igual que dice el título del archivo) o el día 1 del mes.
                "periodo": date.fromisocalendar(anio, periodo, 1) if semanal else date(anio, periodo, 1),
                **{var: _numero(v) for var, v in valores.items()},
                "no_disponible_flag": any(isinstance(v, str) for v in valores.values()),
                "nota_al_pie": notas.get(marca.group(1)) if marca else None,
                "archivo": ruta.name, "orden_archivo": orden[0] * 100 + orden[1],
            })
    return salida


def construir_silver_ocupacion(spark: SparkSession | None = None):
    spark = spark or crear_spark("silver-datatur-ocupacion")
    carpeta = sorted(p for p in BRONZE_HOTELERIA.iterdir() if p.is_dir())[-1] / "hoteleria"
    registros = [r for ruta in sorted(carpeta.glob("*.zip")) for r in leer_archivo(ruta)]
    df = spark.createDataFrame(registros)

    # Una versión por centro-año-periodo: la del archivo más reciente. También se cuenta si cambió entre versiones.
    # La llave usa el nombre LIMPIO: DataTur cambia las marcas de nota al pie entre archivos ("ISLA MUJERES, Q. ROO /4"
    # en uno y sin "/4" en otro). Con el nombre crudo, una misma semana se contaba dos veces (visto el 28-sep-2026).
    llave = ["frecuencia", "centro", "estado", "tipo_fila", "anio", "semana", "mes"]
    w = Window.partitionBy(*llave).orderBy(F.col("orden_archivo").desc())
    versiones = (df.withColumn("rn", F.row_number().over(w))
                 .withColumn("n_versiones", F.count("*").over(Window.partitionBy(*llave)))
                 .withColumn("ocup_distintas", F.size(F.collect_set("ocupacion_pct").over(Window.partitionBy(*llave)))))
    silver = (versiones.where("rn = 1").drop("rn", "orden_archivo")
              .withColumn("revisado_flag", F.col("ocup_distintas") > 1).drop("ocup_distintas")
              # Comprobación interna: ocupación recalculada = ocupados / disponibles.
              .withColumn("ocupacion_calc_pct", F.round(F.col("cuartos_ocupados") / F.col("cuartos_disponibles") * 100, 2)))
    silver.write.mode("overwrite").partitionBy("frecuencia").parquet(str(SILVER))
    return spark.read.parquet(str(SILVER))


if __name__ == "__main__":
    df = construir_silver_ocupacion()
    df.groupBy("frecuencia").agg(F.count("*").alias("filas"), F.countDistinct("centro", "estado").alias("centros"),
                                 F.min("periodo").alias("desde"), F.max("periodo").alias("hasta"),
                                 F.sum(F.col("revisado_flag").cast("int")).alias("revisadas")).show()
    (df.where("es_qroo and tipo_fila = 'centro' and frecuencia = 'semanal'").groupBy("centro")
     .agg(F.count("*").alias("semanas"), F.round(F.avg("ocupacion_pct"), 1).alias("ocupacion_promedio"),
          F.sum(F.col("nota_al_pie").isNotNull().cast("int")).alias("semanas_con_nota"))
     .orderBy("centro").show(truncate=False))
    df.groupBy("tipo_fila").agg(F.countDistinct(F.concat_ws("|", "centro", "estado")).alias("n")).show()
    (df.where("es_qroo and nota_al_pie is not null").select("centro", "nota_al_pie").distinct().show(truncate=False))
