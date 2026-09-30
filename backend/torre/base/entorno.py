# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Prepara el entorno para que PySpark funcione en Windows y crea la sesión de Spark.
# Por qué así:       En esta máquina el Java por defecto es 1.8 (verificado el 26-sep-2026) y PySpark necesita
#                    Java 17. En lugar de cambiar el Java de todo Windows, este módulo apunta JAVA_HOME al JDK 17
#                    solo para el proceso del proyecto. HADOOP_HOME apunta a herramientas/hadoop (winutils.exe y
#                    hadoop.dll 3.3.6), sin los cuales Spark no puede escribir Parquet en Windows.
#                    Alternativa descartada: correr Spark en Docker (funciona, pero es más pesado de explicar y de
#                    arrancar el día del coloquio).
# Datos de entrada:  Ninguno (solo configura el entorno).
# Alimenta a:        Todas las tuberías de Bronze → Silver → Gold (criterio 2 de la rúbrica).

import glob
import os
import sys
from pathlib import Path

# Raíz del proyecto: este archivo vive en backend/torre/base/, así que subimos tres niveles.
RAIZ = Path(__file__).resolve().parents[3]
HADOOP_HOME = RAIZ / "herramientas" / "hadoop"


def buscar_jdk17() -> Path:
    """Busca un JDK 17 instalado en las rutas estándar de Windows.

    Devuelve la carpeta del JDK. Si no hay uno, lanza un error que dice exactamente
    cómo instalarlo; no se sigue con otro Java porque PySpark fallaría más adelante.
    """
    candidatos = []
    for patron in (r"C:\Program Files\Microsoft\jdk-17*",
                   r"C:\Program Files\Eclipse Adoptium\jdk-17*",
                   r"C:\Program Files\Java\jdk-17*"):
        candidatos.extend(glob.glob(patron))
    if not candidatos:
        raise RuntimeError(
            "No encontré un JDK 17. Instálalo con:\n"
            "    winget install Microsoft.OpenJDK.17\n"
            "y vuelve a correr la prueba."
        )
    # Si hay varios, se usa el de versión más alta. Como texto, "jdk-17.0.9" quedaría después de
    # "jdk-17.0.20", así que se ordena por los números de la versión y no alfabéticamente.
    def version(ruta: str) -> tuple:
        numeros = "".join(c if c.isdigit() else " " for c in Path(ruta).name).split()
        return tuple(int(n) for n in numeros)
    return Path(max(candidatos, key=version))


def configurar_entorno() -> dict:
    """Fija JAVA_HOME, HADOOP_HOME y PATH solo para este proceso. Devuelve lo que configuró."""
    jdk = buscar_jdk17()
    os.environ["JAVA_HOME"] = str(jdk)
    os.environ["HADOOP_HOME"] = str(HADOOP_HOME)
    # Se antepone al PATH para que gane sobre el Java 8 del sistema.
    os.environ["PATH"] = os.pathsep.join([str(jdk / "bin"), str(HADOOP_HOME / "bin"), os.environ["PATH"]])
    # Spark arranca "trabajadores" de Python cuando recibe datos creados en Python. En Windows, si no se le dice qué
    # Python usar, se queda esperando y falla con "Accept timed out" (visto el 28-sep-2026 al construir la ocupación
    # de DataTur). Se le indica el mismo Python del proyecto (.venv).
    python = _ruta_corta(sys.executable)
    os.environ["PYSPARK_PYTHON"] = python
    os.environ["PYSPARK_DRIVER_PYTHON"] = python
    return {"JAVA_HOME": str(jdk), "HADOOP_HOME": str(HADOOP_HOME), "PYSPARK_PYTHON": python}


def _ruta_corta(ruta: str) -> str:
    """Devuelve la ruta "corta" de Windows, sin espacios (por ejemplo, la carpeta "PP 5to semestre..." pasa a "PP5TOS~1").

    La carpeta del proyecto tiene espacios ("PP 5to semestre ...") y los scripts de Spark la cortan en "5to"
    ("'5to' is not recognized", visto el 28-sep-2026). La ruta corta evita el problema. Fuera de Windows no cambia nada.
    """
    if os.name != "nt":
        return ruta
    import ctypes

    buffer = ctypes.create_unicode_buffer(1024)
    n = ctypes.windll.kernel32.GetShortPathNameW(ruta, buffer, len(buffer))
    return buffer.value if 0 < n < len(buffer) else ruta


def crear_spark(nombre_app: str = "torre-del-caribe"):
    """Crea una sesión de Spark local que usa todos los núcleos de la máquina.

    local[*]    = modo local con todos los núcleos (12 en esta máquina).
    driver 4g   = memoria para el proceso principal (la máquina tiene 16 GB).
    timeZone    = UTC, para que las fechas no se muevan entre máquinas.
    progreso    = apagado, para que los resúmenes se lean limpios.
    """
    configurar_entorno()
    from pyspark.sql import SparkSession  # se importa después de fijar JAVA_HOME

    return (
        SparkSession.builder.appName(nombre_app)
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.session.timeZone", "UTC")
        # Sin barra de progreso en la terminal: tapaba los resúmenes impresos por los procesos.
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
