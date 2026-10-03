# Autor: Brandon Uriel García Sánchez
# Módulo: Documento (carpeta de entrega)
# Qué hace:          Arma la carpeta Entregable/ en la raíz del proyecto, la que se entrega a los profesores:
#                    1_Documentos/  las tres guías (LaTeX → PDF), el documento ejecutivo y los documentos de respaldo.
#                    2_Notebooks/   CUATRO notebooks autosuficientes, ya ejecutados (.ipynb y .html). Cada uno trae dentro
#                                   el código del proyecto que usa, así que no hay archivos .py sueltos que correr.
#                    3_Pagina_web/  la página, que se abre con doble clic en index.html, sin internet.
#                    datos/         las tablas limpias (Silver), los resultados (Gold), el manifiesto de lo descargado y
#                                   los costos de anuncios; herramientas/ (Hadoop para Windows y las fuentes de letra) y
#                                   requirements.txt para correr los notebooks.
# Por qué así:       Petición de Brandon (03-oct-2026): "una carpeta llamada Entregable donde no tengamos .py a lo tonto para
#                    ejecutar, simplemente varios notebooks (que sean mucho menos)… recopílame los datos también… quita lo
#                    de claude… la nueva es solo de entrega". Decidió 4 notebooks autosuficientes y los datos limpios +
#                    resultados (~370 MB, sin el crudo de 814 MB, del que va el manifiesto con huellas y direcciones).
#                    Cómo se logra sin .py: el código de cada módulo va en una celda que empieza con %%modulo; al correrla,
#                    la celda se registra como ese módulo (torre.radar.indice, por ejemplo). Así el notebook usa EXACTAMENTE
#                    el mismo código del proyecto y da las mismas cifras. El código se toma de backend/torre al armar la
#                    carpeta: los cambios se hacen en el proyecto y la carpeta se vuelve a generar, nunca a mano.
#                    Alternativa descartada: reescribir el código a mano dentro de los notebooks (dos versiones que se
#                    separan con el primer cambio y cifras que podrían no coincidir).
# Datos de entrada:  backend/torre/**, notebooks/0*.ipynb (texto y celdas de uso), docs/latex/, docs/**, frontend/, datos/.
# Alimenta a:        La entrega a los profesores (Entregables A, B y C del Problema Prototípico) y el coloquio.
#
# Uso:  cd backend && ..\.venv\Scripts\python -m torre.documento.entregable

import ast
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient
from nbconvert import HTMLExporter

from torre.documento.pdf import generar_pdf

RAIZ = Path(__file__).resolve().parents[3]
CODIGO = RAIZ / "backend" / "torre"
DESTINO = RAIZ / "Entregable"
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

# ---------------------------------------------------------------- el código del proyecto dentro de los notebooks

# Rutas que en el proyecto apuntan a docs/ y en la entrega a carpetas propias.
SUSTITUCIONES = [
    ('FIGURAS = RAIZ / "docs" / "ejecutivo" / "figuras"', 'FIGURAS = RAIZ / "2_Notebooks" / "figuras"'),
    ('SALIDA = RAIZ / "docs" / "datos" / "DICCIONARIO.md"', 'SALIDA = RAIZ / "datos" / "DICCIONARIO.md"'),
]


def fuente_modulo(nombre: str) -> str:
    """Código de torre.<paquete>.<módulo> tal como está en el proyecto, sin su bloque `if __name__ == "__main__":`
    (en el notebook las funciones se llaman desde las celdas de uso)."""
    ruta = CODIGO / Path(*nombre.split(".")[1:]).with_suffix(".py")
    texto = ruta.read_text(encoding="utf-8")
    lineas = texto.split("\n")
    for nodo in ast.parse(texto).body:
        if isinstance(nodo, ast.If) and "__name__" in ast.unparse(nodo.test):
            lineas = lineas[:nodo.lineno - 1] + lineas[nodo.end_lineno:]
            break
    texto = "\n".join(lineas).rstrip() + "\n"
    for a, b in SUSTITUCIONES:
        texto = texto.replace(a, b)
    return texto


def dependencias(nombre: str) -> list[str]:
    """Módulos de torre que importa un módulo (arriba o dentro de una función), en el orden en que aparecen."""
    texto = fuente_modulo(nombre)
    deps = []
    for paquete, nombres in re.findall(r"from (torre(?:\.\w+)+) import ([\w, ]+)", texto):
        if paquete.count(".") == 1:     # from torre.pronostico import modelos → el módulo es torre.pronostico.modelos
            deps += [f"{paquete}.{n.strip().split(' as ')[0]}" for n in nombres.split(",")]
        else:
            deps.append(paquete)
    return [d for i, d in enumerate(deps) if d not in deps[:i] and d != nombre]


def explicacion(nombre: str) -> str:
    """El encabezado del archivo (Qué hace / Por qué así) resumido en una línea para la celda de texto."""
    texto = fuente_modulo(nombre)
    m = re.search(r"# Qué hace:\s+(.+?)(?:\n# Por qué|\n#\s*\n)", texto, re.S)
    que = re.sub(r"\s*\n#\s+", " ", m.group(1)).strip() if m else ""
    return f"**`{nombre}`** — {_limpiar_texto(que)}"


class Armador:
    """Junta las celdas de un notebook. Antes de cada módulo agrega los módulos de los que depende (si aún no están),
    para que el notebook corra de arriba abajo."""

    def __init__(self):
        self.celdas, self.hechos = [], set()

    def texto(self, t: str):
        self.celdas.append(md(t.strip()))

    def celda(self, c: str):
        self.celdas.append(code(c.strip()))

    def modulos(self, nombres: list[str], titulo: str = "El código de esta parte"):
        pendientes = []

        def agregar(n):
            if n in self.hechos or n in pendientes:
                return
            for d in dependencias(n):
                agregar(d)
            pendientes.append(n)
        for n in nombres:
            agregar(n)
        if not pendientes:
            return
        self.texto(f"### {titulo}\nCada celda de código de abajo es un archivo del paquete `torre`, completo y sin cambios "
                   "(con su encabezado: qué hace, por qué así, de qué datos sale y a qué decisión alimenta). Al correrla, "
                   "la celda queda registrada como ese módulo y las celdas siguientes lo usan.\n\n"
                   + "\n".join(f"- {explicacion(n)}" for n in pendientes))
        for n in pendientes:
            self.celdas.append(code(f"%%modulo {n}\n{fuente_modulo(n)}"))
            self.hechos.add(n)


PREPARAR = '''%matplotlib inline
# Preparación: se corre una vez, al inicio. Encuentra la carpeta de la entrega y define %%modulo, la instrucción que
# convierte una celda de código en un módulo del paquete `torre` (así el notebook no necesita archivos .py).
import os, sys, types, warnings
from pathlib import Path
from IPython.core.magic import register_cell_magic
warnings.filterwarnings("ignore")

RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datos" / "silver").is_dir())
FIGURAS = RAIZ / "2_Notebooks" / "figuras"
FIGURAS.mkdir(parents=True, exist_ok=True)


def _paquete(nombre):
    if nombre not in sys.modules:
        m = types.ModuleType(nombre); m.__path__ = []
        sys.modules[nombre] = m
        if "." in nombre:
            padre, hijo = nombre.rsplit(".", 1)
            setattr(_paquete(padre), hijo, m)
    return sys.modules[nombre]


@register_cell_magic
def modulo(linea, celda):
    """%%modulo torre.radar.indice → ejecuta la celda como el módulo torre.radar.indice."""
    nombre = linea.strip()
    padre, hijo = nombre.rsplit(".", 1)
    m = types.ModuleType(nombre)
    # Ruta simbólica: el código calcula la raíz del proyecto con Path(__file__).parents[3], y aquí da la carpeta de entrega.
    m.__file__ = str(RAIZ / "codigo" / Path(*nombre.split(".")).with_suffix(".py"))
    sys.modules[nombre] = m
    setattr(_paquete(padre), hijo, m)
    try:  # para que Spark pueda mandar a sus trabajadores las funciones definidas aquí
        from pyspark import cloudpickle
        cloudpickle.register_pickle_by_value(m)
    except Exception:
        pass
    exec(compile(celda, m.__file__, "exec"), m.__dict__)


import pandas as pd
pd.set_option("display.max_colwidth", 70)
pd.set_option("display.width", 200)
print("Carpeta de la entrega:", RAIZ)'''

INSTRUCCIONES = """
| | |
|---|---|
| **Cómo correrlo** | Python 3.11 con `pip install -r requirements.txt` (en la carpeta de la entrega). Para Spark (notebooks 1 y 3), además Java 17: `winget install Microsoft.OpenJDK.17`. Abrir en Jupyter o VS Code y elegir *Ejecutar todo*. |
| **Datos** | Los lee de `datos/` (tablas limpias y resultados). Ya viene ejecutado: se puede leer sin correrlo. |
| **Código** | Va dentro del notebook: cada celda que empieza con `%%modulo` es un archivo del proyecto, completo. |
"""


def _limpiar_uso(fuente: str) -> str:
    """Celdas de uso de los notebooks del proyecto: sin las líneas que buscaban el paquete en backend/ y con las rutas de
    la entrega."""
    fuera = ("RAIZ = Path.cwd().parent", 'sys.path.insert(0, str(RAIZ / "backend"))')
    lineas = [l for l in fuente.split("\n") if not l.strip().startswith(fuera)]
    t = "\n".join(lineas)
    return t.replace('RAIZ / "docs" / "ejecutivo" / "figuras"', "FIGURAS")


def _limpiar_texto(t: str) -> str:
    """Texto de los notebooks del proyecto: las rutas del repositorio se cambian por lo que hay en la entrega."""
    t = re.sub(r"`?backend/torre/(\w+)/(\w+)\.py`?", r"`torre.\1.\2`", t)
    t = re.sub(r"`?backend/torre/(\w+)/?`?", r"`torre.\1`", t)
    t = re.sub(r"`?docs/decisiones/[\w-]+\.md`?", "*Las decisiones, fase por fase* (PDF)", t)
    t = re.sub(r"`?docs/metodologia/ECUACIONES\.md`?( §[\d.\-a-z]+)?", "*Guía técnica* (PDF)", t)
    t = t.replace("docs/ejecutivo/figuras/", "2_Notebooks/figuras/").replace("docs/datos/DICCIONARIO.md", "datos/DICCIONARIO.md")
    return re.sub(r"`(\w+)\.py`", r"``", t)


def uso_de(notebook: str, a: Armador, nivel: str):
    """Agrega las celdas (texto y uso) de un notebook del proyecto. Su título pasa a ser el de una parte."""
    nb = nbf.read(RAIZ / "notebooks" / f"{notebook}.ipynb", as_version=4)
    for i, c in enumerate(nb.cells):
        if c.cell_type == "markdown":
            t = _limpiar_texto(c.source)
            if i == 0:
                t = re.sub(r"^# ", f"## {nivel} · ", t, count=1)
            else:
                t = re.sub(r"^(#+) ", lambda m: "#" + m.group(1) + " ", t, flags=re.M)
            a.texto(t)
        else:
            a.celda(_limpiar_uso(c.source))


# ---------------------------------------------------------------- los cuatro notebooks

def nb_datos() -> list:
    a = Armador()
    a.texto(f"""# 1 · Los datos: de las fuentes oficiales al almacén
**Torre del Caribe** · Grandes volúmenes de datos (criterio 2) · Autor: **Brandon Uriel García Sánchez** · Equipo: Maribel
Mondragón Mercado, Jesús Ramírez Isidro, Enrique González Ortega · UNRC, LCDN 5° semestre 2026-2

Este notebook recorre el camino de los datos: **qué se descargó** (caja de bronce), **cómo se limpió con Spark** (caja de
plata), **cómo se guarda y se consulta** (DuckDB y el modelo estrella) y **qué no existe** (huecos declarados).
{INSTRUCCIONES}
| **El crudo** | Los 353 archivos crudos (814 MB) no van en la entrega; va su manifiesto con huella SHA-256 y dirección de origen. Si la carpeta `datos/bronze` está completa, las celdas de limpieza vuelven a correr con Spark; si no, se saltan y se usan las tablas limpias que ya vienen. |""")
    a.celda(PREPARAR)
    a.texto("""## 1. Qué se descargó (la caja de bronce)
Cada archivo se descargó con un programa, sin modificarlo, y quedó anotado en el **manifiesto**: su huella SHA-256 (si se
cambia una coma, la huella cambia), su tamaño, su dirección de origen, la fecha y cuántos registros tiene.""")
    a.celda('''m = pd.read_csv(RAIZ / "datos" / "bronze" / "MANIFIESTO.csv")
# La evidencia del sargazo y las capturas de los costos de anuncios también están en el manifiesto, pero no son fuentes.
oficiales = m[~m.fuente.isin(["Evidencia sargazo", "D13 Benchmarks"])]
print(f"Fuentes oficiales: {len(oficiales)} archivos · {oficiales.filas.sum():,.0f} registros · {oficiales.bytes.sum() / 1e6:,.1f} MB")
(oficiales.groupby("fuente").agg(archivos=("archivo", "size"), registros=("filas", "sum"), MB=("bytes", lambda b: round(b.sum() / 1e6, 1)))
 .sort_values("registros", ascending=False))''')
    a.texto("""## 2. Cómo se descargó
Estas funciones bajan los datos de las fuentes oficiales. **No se vuelven a correr aquí** (descargan cientos de MB de
internet); se muestran para que se vea exactamente cómo se obtuvo cada archivo y cómo se registró en el manifiesto.""")
    a.modulos(["torre.base.manifiesto", "torre.base.ingesta_siturq", "torre.base.ingesta_datatur",
               "torre.base.ingesta_abiertas", "torre.base.ingesta_benchmarks"], "El código de la descarga")
    a.texto("""## 3. Spark
Spark reparte el trabajo entre los núcleos de la computadora. Corre en **modo local** (`local[*]`): el mismo programa
correría en un clúster de muchas computadoras cambiando solo la dirección del maestro. `crear_spark` (en
`torre.base.entorno`) apunta Java 17 y Hadoop solo dentro de este proceso.""")
    a.modulos(["torre.base.entorno"], "El código de la sesión de Spark")
    a.celda('''from torre.base.entorno import crear_spark
spark = crear_spark("entrega-datos")
print("Spark", spark.version, "· núcleos:", spark.sparkContext.defaultParallelism)
BRONZE_COMPLETO = (RAIZ / "datos" / "bronze" / "denue").is_dir()
print("¿Está el crudo completo para volver a limpiar?", "sí" if BRONZE_COMPLETO else "no: se usan las tablas limpias que ya vienen")''')
    a.texto("""## 4. La limpieza, una fuente a la vez (de bronce a plata)
Un archivo por fuente, porque cada una tiene sus propias trampas: ceros que en realidad son huecos, renglones repetidos,
notas al pie que parecen datos, aerolíneas con la misma etiqueta. Cada regla está escrita en el encabezado del módulo y
se comprobó con los datos.""")
    silver = ["siturq", "datatur_ocupacion", "denue", "inah", "iter", "clima", "huracanes", "fred", "nacionalidad",
              "afac", "cruceros", "restmex"]
    a.modulos([f"torre.base.silver_{s}" for s in silver], "El código de la limpieza")
    a.celda('''import time
import torre.base as b
trabajos = [("SITUR-Q", b.silver_siturq.construir_silver_siturq), ("DataTur ocupación", b.silver_datatur_ocupacion.construir_silver_ocupacion),
            ("DENUE (6.1 millones de negocios)", b.silver_denue.construir_silver_denue), ("INAH", b.silver_inah.construir_silver_inah),
            ("Censo 2020", b.silver_iter.construir_silver_iter), ("Clima", b.silver_clima.construir_silver_clima),
            ("Huracanes", b.silver_huracanes.construir_silver_huracanes), ("Tipo de cambio", b.silver_fred.construir_silver_fred),
            ("Nacionalidades", b.silver_nacionalidad.construir_silver_nacionalidad), ("Vuelos AFAC", b.silver_afac.construir_silver_afac),
            ("Cruceros", b.silver_cruceros.construir_silver_cruceros), ("Reseñas Rest-Mex", b.silver_restmex.construir_silver_restmex)]
for nombre, trabajo in trabajos:
    if not BRONZE_COMPLETO:
        print(f"· {nombre}: se usa la tabla limpia que ya viene"); continue
    t0 = time.time(); trabajo(spark)
    print(f"✓ {nombre}: limpio en {time.time() - t0:,.1f} s")''')
    a.celda('''# Las 14 tablas limpias que quedaron (leídas con Spark)
filas = []
for carpeta in sorted((RAIZ / "datos" / "silver").iterdir()):
    if carpeta.is_dir():
        n = spark.read.parquet(str(carpeta)).count()
        mb = sum(f.stat().st_size for f in carpeta.rglob("*.parquet")) / 1e6
        filas.append({"tabla": carpeta.name, "renglones": n, "MB": round(mb, 1)})
pd.DataFrame(filas).sort_values("renglones", ascending=False)''')
    a.texto("""## 5. Spark sobre la tabla grande: los negocios del país
La tabla del DENUE tiene más de 6 millones de negocios y está **partida por estado**: para leer Quintana Roo, Spark abre
solo la carpeta `cve_ent=23` (*partition pruning*). Las transformaciones se planean completas y se ejecutan hasta que se
pide un resultado (*evaluación perezosa*).""")
    a.celda('''from pyspark.sql import functions as F
denue = spark.read.parquet(str(RAIZ / "datos" / "silver" / "denue"))
print(f"Negocios en el país: {denue.count():,} · turísticos: {denue.where('es_turistico').count():,}")
(denue.where("es_qroo and es_turistico").groupBy("municipio").pivot("categoria_turistica").count()
 .fillna(0).orderBy(F.desc("Alimentos y bebidas")).toPandas())''')
    a.celda('''# Cuántos negocios turísticos hay en cada estado (las 10 con más)
(denue.where("es_turistico").groupBy("entidad").agg(F.count("*").alias("negocios_turisticos"))
 .orderBy(F.desc("negocios_turisticos")).limit(10).toPandas())''')
    a.texto("""## 6. El almacén: DuckDB y el modelo estrella
DuckDB es una base de datos en un solo archivo: lee las tablas de plata y oro sin copiarlas y responde en milisegundos, sin
servidor ni internet. La tabla de **hechos** tiene un renglón por lugar, mes y variable; a sus lados están las tablas de
lugares y de meses. **Un hueco no tiene renglón**: nunca se rellena con cero.""")
    a.modulos(["torre.base.almacen", "torre.base.diccionario"], "El código del almacén y del diccionario")
    a.celda('''from torre.base import almacen
almacen.construir_almacen()
almacen.consultar("""SELECT l.lugar, l.papel, count(*) AS renglones, min(h.periodo) AS desde, max(h.periodo) AS hasta
                     FROM hechos_mes h JOIN dim_lugar l USING (lugar) GROUP BY ALL ORDER BY renglones DESC""")''')
    a.texto("""## 7. El diccionario de datos
Se genera solo, desde el almacén: cada columna con su tipo, su porcentaje de vacíos, un ejemplo real y su significado. Si
una columna no tiene significado escrito, el programa se detiene. Queda en `datos/DICCIONARIO.md`.""")
    a.celda('''from torre.base import diccionario
texto = diccionario.generar()
print(texto[:1500])''')
    a.texto("""## 8. Lo que no existe (huecos declarados)
Un cero imposible no es un cero: es un dato que la fuente dejó de publicar. Se marca como hueco y nunca se rellena.""")
    a.celda('''s = pd.read_parquet(RAIZ / "datos" / "silver" / "siturq")
(s.groupby("indicador").agg(renglones=("valor", "size"), huecos=("hueco_flag", "sum"),
                             ultimo_con_dato=("periodo", lambda p: p[~s.loc[p.index, "hueco_flag"]].max()))
 .sort_values("huecos", ascending=False))''')
    a.celda("spark.stop()")
    return a.celdas


def nb_donde_y_cuando() -> list:
    a = Armador()
    a.texto(f"""# 2 · Dónde y cuándo: el planteamiento, el Radar y el Pronóstico
**Torre del Caribe** · Planteamiento (criterio 1), Minería de datos (3), Aprendizaje de máquina (4) y Procesos estocásticos (5)
· Autor: **Brandon Uriel García Sánchez** · UNRC, LCDN 5° semestre 2026-2

| Parte | Pregunta | Técnicas |
|---|---|---|
| A. Planteamiento | ¿Qué tan desigual está el turismo? | Cuotas e índice de Herfindahl-Hirschman |
| B. Radar | ¿Dónde hay espacio hoy y el mes que entra? | Índice de presión (minería), clasificador (ML), Markov (estocástico), Ward (minería) |
| C. Pronóstico | ¿Cuándo conviene ir en los próximos 12 meses? | Forma del año (minería), 5 modelos con origen móvil y rango conformal (ML), Poisson y Monte Carlo (estocástico) |
{INSTRUCCIONES}""")
    a.celda(PREPARAR)
    a.modulos(["torre.documento.figuras"], "Estilo de las gráficas (colores UNRC)")
    a.modulos(["torre.radar.planteamiento"], "El código de la Parte A")
    uso_de("01_planteamiento", a, "Parte A")
    a.modulos(["torre.radar.panel", "torre.radar.indice", "torre.radar.prediccion", "torre.radar.markov",
               "torre.radar.clustering"], "El código de la Parte B")
    uso_de("02_radar", a, "Parte B")
    a.modulos(["torre.pronostico.series", "torre.pronostico.forma", "torre.pronostico.modelos", "torre.pronostico.intervalos",
               "torre.pronostico.seleccion", "torre.pronostico.escenarios"], "El código de la Parte C")
    uso_de("03_pronostico", a, "Parte C")
    return a.celdas


def nb_presupuesto_y_torre() -> list:
    a = Armador()
    a.texto(f"""# 3 · El presupuesto y la Torre en vivo
**Torre del Caribe** · Investigación de Operaciones (criterio 6) y Grandes volúmenes de datos en tiempo casi real (criterio 2)
· Autor: **Brandon Uriel García Sánchez** · UNRC, LCDN 5° semestre 2026-2

| Parte | Pregunta | Técnicas |
|---|---|---|
| A. Presupuesto | ¿Cuánto dinero va a cada lugar, mes y canal? | Programación estocástica de dos etapas (PuLP + CBC), precios sombra, Pareto |
| B. Torre en vivo | ¿Qué hace la campaña esta semana? | Spark Structured Streaming, Isolation Forest, motor de reglas |
{INSTRUCCIONES}""")
    a.celda(PREPARAR)
    a.modulos(["torre.documento.figuras"], "Estilo de las gráficas (colores UNRC)")
    a.modulos(["torre.campana.presupuesto"], "El código de la Parte A")
    uso_de("05_optimizacion", a, "Parte A")
    a.texto("""### El plan que pasa a la Torre
Se guarda el reparto (etapa 1) en `datos/gold/`, de donde lo lee la Torre para saber cuánto gastar cada semana.""")
    a.celda('''from torre.campana import presupuesto
presupuesto.construir();''')
    a.modulos(["torre.envivo.senales", "torre.envivo.motor", "torre.envivo.torre"], "El código de la Parte B")
    a.texto("""### La reproducción con Spark Structured Streaming
Primero se arman las señales de las 239 semanas (ocupación del norte, tormentas, clima raro y llegadas del sur). Después
cada semana se escribe como un archivo y **Spark Structured Streaming** los lee de uno en uno (`maxFilesPerTrigger = 1`),
en orden, como si fueran llegando; en cada lote, el motor de reglas decide si pausa o enciende cada anuncio.""")
    a.celda('''from torre.envivo import senales, torre
senales.construir()
resultado = torre.reproducir()
resultado''')
    uso_de("06_torre_en_vivo", a, "Parte B")
    return a.celdas


def nb_campana() -> list:
    a = Armador()
    a.texto(f"""# 4 · La campaña "El sur tiene espacio"
**Torre del Caribe** · Mercadotecnia digital (criterio 7) y minería de texto (criterio 3) · Autor: **Brandon Uriel García
Sánchez** · UNRC, LCDN 5° semestre 2026-2

Qué molesta y qué enamora al turista (85,987 reseñas), las dos viajeras ideales, la marca, los anuncios, los medios, el
calendario y los indicadores. Cada rasgo dice si es un dato, un cálculo, un supuesto o un hueco.
{INSTRUCCIONES}""")
    a.celda(PREPARAR)
    a.modulos(["torre.campana.texto", "torre.campana.marca"], "El código de la campaña")
    a.texto("""### Se arma la campaña
`texto.construir()` mide los temas, las reglas de asociación y las palabras de las reseñas; `marca.construir()` arma las
personas, la marca, los mensajes, los medios, el calendario y los indicadores con las cifras de los otros notebooks, y lo
guarda en `datos/gold/campana.json`.""")
    a.celda('''from torre.campana import texto, marca
texto.construir()
marca.construir();''')
    uso_de("07_campana", a, "La campaña")
    return a.celdas


NOTEBOOKS = [("1_Datos_y_arquitectura", nb_datos), ("2_Donde_y_cuando", nb_donde_y_cuando),
             ("3_Presupuesto_y_Torre_en_vivo", nb_presupuesto_y_torre), ("4_Campana", nb_campana)]

# ---------------------------------------------------------------- documentos

DOCUMENTOS_MD = [
    ("docs/trazabilidad.md", "5_Trazabilidad_de_las_cifras.pdf", "Trazabilidad de las cifras<br>Archivo crudo → función → salida → prueba"),
    ("docs/informe/MAPA_INFORME.md", "6_Mapa_del_informe_tecnico.pdf", "Mapa del informe técnico<br>Qué alimenta cada sección del Entregable B"),
    ("docs/coloquio/GUION_COLOQUIO.md", "7_Guion_del_coloquio.pdf", "Guion del coloquio<br>15 minutos, cuatro integrantes"),
    ("docs/datos/DICCIONARIO.md", "8_Diccionario_de_datos.pdf", "Diccionario de datos<br>Las 56 tablas, columna por columna"),
    ("docs/ejecutivo/AUDITORIA_PAGINA.md", "9_Auditoria_de_la_pagina.pdf", "Auditoría de la página<br>Accesibilidad WCAG 2.1 AA"),
]
GUIAS_LATEX = [("1_guia_tecnica", "1_Guia_tecnica.pdf"), ("2_guia_sencilla", "2_Guia_sencilla.pdf"),
               ("3_decisiones", "3_Decisiones_fase_por_fase.pdf")]


def compilar_latex() -> None:
    """Compila las tres guías con XeLaTeX (MiKTeX), tres pasadas cada una (índice, referencias y páginas). El PATH va
    limpio porque MiKTeX se detiene si una entrada del PATH apunta a un archivo (lo mismo que docs/latex/compilar.sh)."""
    carpeta = RAIZ / "docs" / "latex"
    xelatex = Path(os.environ["LOCALAPPDATA"]) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64" / "xelatex.exe"
    env = {**os.environ, "PATH": os.pathsep.join([str(xelatex.parent), r"C:\Windows\System32", r"C:\Windows"])}
    (carpeta / "build").mkdir(exist_ok=True)
    for fuente, _ in GUIAS_LATEX:
        for _ in range(3):
            r = subprocess.run([str(xelatex), "-interaction=nonstopmode", "-halt-on-error", "-output-directory=build",
                                f"{fuente}.tex"], cwd=carpeta, env=env, capture_output=True)
            if r.returncode:
                raise RuntimeError(f"XeLaTeX falló en {fuente}.tex; ver docs/latex/build/{fuente}.log")


def documentos(destino: Path) -> None:
    destino.mkdir(parents=True)
    compilar_latex()
    for fuente, salida in GUIAS_LATEX:
        shutil.copy2(RAIZ / "docs" / "latex" / "build" / f"{fuente}.pdf", destino / salida)
    generar_pdf()  # el documento ejecutivo, con las capturas de hoy
    shutil.copy2(RAIZ / "Documento_Ejecutivo_Torre_del_Caribe.pdf", destino / "4_Documento_ejecutivo.pdf")
    for fuente, salida, subtitulo in DOCUMENTOS_MD:
        generar_pdf(RAIZ / fuente, destino / salida, subtitulo, matematicas=True)


# ---------------------------------------------------------------- datos, herramientas y página

def datos(destino: Path) -> None:
    origen = RAIZ / "datos"
    shutil.copytree(origen / "silver", destino / "silver")
    shutil.copytree(origen / "gold", destino / "gold", ignore=shutil.ignore_patterns("torre.duckdb*", "envivo_entrada*",
                                                                                      "envivo_checkpoint*"))
    (destino / "bronze").mkdir()
    shutil.copy2(origen / "bronze" / "MANIFIESTO.csv", destino / "bronze" / "MANIFIESTO.csv")
    # Lo poco del crudo que leen los notebooks: costos de anuncios (presupuesto) y el mapa de municipios.
    for sub in ("benchmarks", "geo"):
        shutil.copytree(origen / "bronze" / sub, destino / "bronze" / sub)


def herramientas(destino: Path) -> None:
    shutil.copytree(RAIZ / "herramientas" / "hadoop", destino / "hadoop")
    shutil.copytree(RAIZ / "herramientas" / "fuentes", destino / "fuentes")


def requirements(destino: Path) -> None:
    """Las dependencias que usan los notebooks (sin las de las pruebas, el servidor ni la auditoría de la página)."""
    fuera = ("pytest", "fastapi", "uvicorn", "httpx", "axe-playwright", "latex2mathml", "markdown")
    lineas = [l for l in (RAIZ / "requirements.txt").read_text(encoding="utf-8").splitlines()
              if l.strip() and not l.startswith("#") and not l.lower().startswith(fuera)]
    destino.write_text("\n".join(lineas + ["jupyter"]) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- armar

def ejecutar(nb, carpeta: Path, nombre: str, bronze_completo: Path | None = None) -> None:
    """Corre el notebook completo dentro de la carpeta de entrega. Si una celda falla, se detiene: no se guarda un
    notebook con errores. Para el notebook 1, el crudo completo se enlaza un momento (sin copiarlo) para que las celdas
    de limpieza corran de verdad; al terminar se quita el enlace."""
    enlace = DESTINO / "datos" / "bronze_minimo"
    if bronze_completo:
        (DESTINO / "datos" / "bronze").rename(enlace)
        subprocess.run(["cmd", "/c", "mklink", "/J", str(DESTINO / "datos" / "bronze"), str(bronze_completo)],
                       check=True, capture_output=True)
    try:
        t0 = time.time()
        NotebookClient(nb, timeout=3600, kernel_name="python3", resources={"metadata": {"path": str(carpeta)}}).execute()
        print(f"  ✓ {nombre}: {time.time() - t0:,.0f} s")
    finally:
        if bronze_completo:
            os.rmdir(DESTINO / "datos" / "bronze")  # quita el enlace, no el crudo
            enlace.rename(DESTINO / "datos" / "bronze")


def armar() -> Path:
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    DESTINO.mkdir()
    print("Datos…"); datos(DESTINO / "datos")
    herramientas(DESTINO / "herramientas")
    requirements(DESTINO / "requirements.txt")
    print("Página…")
    shutil.copytree(RAIZ / "frontend", DESTINO / "3_Pagina_web", ignore=shutil.ignore_patterns(".gitkeep"))
    print("Notebooks…")
    carpeta = DESTINO / "2_Notebooks"
    carpeta.mkdir()
    for nombre, construir in NOTEBOOKS:
        nb = nbf.v4.new_notebook(cells=construir())
        nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
        ejecutar(nb, carpeta, nombre, RAIZ / "datos" / "bronze" if nombre.startswith("1_") else None)
        nbf.write(nb, carpeta / f"{nombre}.ipynb")
        html, _ = HTMLExporter(template_name="lab").from_notebook_node(nb)
        (carpeta / f"{nombre}.html").write_text(html, encoding="utf-8")
    # Lo que los notebooks regeneran y no hace falta entregar dos veces.
    for sobra in ("envivo_entrada", "envivo_checkpoint"):
        for p in (DESTINO / "datos" / "gold").glob(f"{sobra}*"):
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    print("Documentos…"); documentos(DESTINO / "1_Documentos")
    return DESTINO


if __name__ == "__main__":
    d = armar()
    total = sum(f.stat().st_size for f in d.rglob("*") if f.is_file()) / 1e6
    print(f"Entregable/ lista · {total:,.0f} MB")
