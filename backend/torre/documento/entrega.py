# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos (entregables)
# Qué hace:          Arma la carpeta ENTREGA/ en la raíz del proyecto con lo indispensable para enseñar el proyecto:
#                    1. Las tres guías en PDF (técnica fórmula por fórmula, sencilla y decisiones por fase), generadas
#                       desde docs/guias/*.md con fórmulas e índice, y el documento ejecutivo.
#                    2. Los 6 notebooks ya ejecutados, en .ipynb y en HTML (se abren con doble clic, sin Jupyter).
#                    3. Los documentos de respaldo: ecuaciones, trazabilidad, diccionario de datos, mapa del informe,
#                       guion del coloquio y las 25 notas de decisión.
#                    4. Un LEEME.md que dice qué abrir primero y dónde está cada materia (UCA).
#                    Además deja una copia comprimida, con la página web incluida, en entregas/ (no va a git).
# Por qué así:       Petición de Brandon (02-oct-2026): "crear una carpeta donde esté todo indispensable tipo notebooks
#                    para enseñarle a los profes, los pdf para explicarle lo que hice a los demás del equipo, las
#                    decisiones". Todo sale de los archivos del proyecto tal como están (no se reescribe ninguna cifra) y
#                    la carpeta se regenera con un comando, así que no puede quedar vieja.
#                    Alternativa descartada: copiar los archivos a mano (se desactualizan al primer cambio).
# Datos de entrada:  docs/guias/*.md, notebooks/*.ipynb, docs/**, Documento_Ejecutivo_Torre_del_Caribe.pdf, frontend/.
# Alimenta a:        La revisión de los profesores, el trabajo del equipo y el coloquio.
#
# Uso:  cd backend && ..\.venv\Scripts\python -m torre.documento.entrega

import shutil
from datetime import date
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter

from torre.documento.pdf import generar_pdf

RAIZ = Path(__file__).resolve().parents[3]
ENTREGA = RAIZ / "ENTREGA"
NOTEBOOKS = ["01_planteamiento", "02_radar", "03_pronostico", "05_optimizacion", "06_torre_en_vivo", "07_campana"]
GUIAS = [
    ("1_GUIA_TECNICA.md", "1_Guia_tecnica_formula_por_formula.pdf", "Guía técnica<br>Cómo se hizo, fórmula por fórmula"),
    ("2_GUIA_SENCILLA.md", "2_Guia_sencilla.pdf", "Guía sencilla<br>Qué hicimos y por qué, sin tecnicismos"),
    ("3_DECISIONES_POR_FASE.md", "3_Decisiones_fase_por_fase.pdf", "Las decisiones del proyecto<br>Fase por fase, de la 0 a la 11"),
]
DOCUMENTOS = {
    "ECUACIONES.md": RAIZ / "docs" / "metodologia" / "ECUACIONES.md",
    "TRAZABILIDAD.md": RAIZ / "docs" / "trazabilidad.md",
    "DICCIONARIO_DE_DATOS.md": RAIZ / "docs" / "datos" / "DICCIONARIO.md",
    "MAPA_DEL_INFORME.md": RAIZ / "docs" / "informe" / "MAPA_INFORME.md",
    "GUION_COLOQUIO.md": RAIZ / "docs" / "coloquio" / "GUION_COLOQUIO.md",
    "AUDITORIA_PAGINA.md": RAIZ / "docs" / "ejecutivo" / "AUDITORIA_PAGINA.md",
}

LEEME = """# Torre del Caribe · Carpeta de entrega

Proyecto del Problema Prototípico *Turismo inteligente sustentable* (UNRC · LCDN 5° semestre 2026-2), Quintana Roo.
Equipo: Brandon Uriel García Sánchez · Maribel Mondragón Mercado · Jesús Ramírez Isidro · Enrique González Ortega.
Generada el {fecha} con `python -m torre.documento.entrega` (no se edita a mano).

## Qué abrir primero
| Si eres… | Abre |
|---|---|
| Profesor o sinodal | `1_Guia_tecnica_formula_por_formula.pdf` y los notebooks de tu materia (tabla de abajo) |
| Integrante del equipo | `2_Guia_sencilla.pdf`, luego `3_Decisiones_fase_por_fase.pdf` |
| Quien redacta el informe | `4_Documento_ejecutivo.pdf` y `documentos/MAPA_DEL_INFORME.md` |
| Quien prepara el coloquio | `documentos/GUION_COLOQUIO.md` |

**La página web:** https://catoxp.github.io/torre-del-caribe-unrc-2026/ (o `frontend/index.html` del repositorio, sin
internet).

## Dónde está cada materia (UCA)
| Materia | Notebook (en `notebooks/`, ábrelo en .html) | Sección de la guía técnica |
|---|---|---|
| Planteamiento | `01_planteamiento` | §4.1 y §4.2 |
| Grandes volúmenes de datos | `06_torre_en_vivo` (Spark Streaming) y el código de `backend/torre/base/` | §3 |
| Minería de datos | `02_radar`, `03_pronostico`, `06_torre_en_vivo`, `07_campana` | §4 |
| Aprendizaje de máquina | `02_radar` (clasificador), `03_pronostico` (series de tiempo) | §5 |
| Procesos estocásticos | `02_radar` (Markov), `03_pronostico` (Poisson y Monte Carlo) | §6 |
| Investigación de Operaciones | `05_optimizacion` | §7 |
| Mercadotecnia digital | `07_campana` | §8 |

*No hay notebook 04:* el plan tenía un `04_escenarios` aparte, y esos escenarios quedaron dentro de `03_pronostico`.

## Contenido
| Archivo o carpeta | Qué es |
|---|---|
| `1_Guia_tecnica_formula_por_formula.pdf` | Todo el proyecto explicado: datos, código, cada fórmula con su ejemplo resuelto a mano y por qué se hizo así |
| `2_Guia_sencilla.pdf` | Lo mismo, sin tecnicismos |
| `3_Decisiones_fase_por_fase.pdf` | Cada decisión de las 12 fases: qué se eligió, qué se descartó y con qué evidencia |
| `4_Documento_ejecutivo.pdf` | El documento no técnico con gráficas y capturas, capítulo por fase |
| `notebooks/` | Los 6 notebooks ejecutados (.ipynb y .html) |
| `documentos/` | Ecuaciones, trazabilidad, diccionario de datos, mapa del informe, guion del coloquio, auditoría de la página y las 25 notas de decisión |

## Cómo se comprueba que las cifras son correctas
El repositorio tiene pruebas automáticas (`python -m pytest`). Entre ellas, `tests/test_guias.py` recalcula con los datos
las cifras de estas guías y `tests/test_documentos.py` las de los demás documentos.
"""


def exportar_html(origen: Path, destino: Path) -> None:
    nb = nbformat.read(origen, as_version=4)
    html, _ = HTMLExporter(template_name="lab").from_notebook_node(nb)
    destino.write_text(html, encoding="utf-8")


def armar(fecha: date | None = None) -> Path:
    fecha = fecha or date.today()
    if ENTREGA.exists():
        shutil.rmtree(ENTREGA)
    (ENTREGA / "notebooks").mkdir(parents=True)
    (ENTREGA / "documentos").mkdir()
    guias = RAIZ / "docs" / "guias"
    for fuente, salida, subtitulo in GUIAS:
        generar_pdf(guias / fuente, ENTREGA / salida, subtitulo, matematicas=True, indice=True)
    shutil.copy2(RAIZ / "Documento_Ejecutivo_Torre_del_Caribe.pdf", ENTREGA / "4_Documento_ejecutivo.pdf")
    for n in NOTEBOOKS:
        origen = RAIZ / "notebooks" / f"{n}.ipynb"
        if not origen.exists():
            raise FileNotFoundError(f"Falta el notebook {n}: primero corre notebooks/_construir_{n}.py")
        shutil.copy2(origen, ENTREGA / "notebooks" / origen.name)
        exportar_html(origen, ENTREGA / "notebooks" / f"{n}.html")
    for nombre, origen in DOCUMENTOS.items():
        shutil.copy2(origen, ENTREGA / "documentos" / nombre)
    shutil.copytree(RAIZ / "docs" / "decisiones", ENTREGA / "documentos" / "decisiones")
    (ENTREGA / "LEEME.md").write_text(LEEME.format(fecha=fecha.strftime("%d/%m/%Y")), encoding="utf-8")
    # Copia comprimida para mandar por correo (incluye la página para abrirla sin internet); no va a git.
    copia = RAIZ / "entregas" / f"Torre_del_Caribe_{fecha.isoformat()}"
    if copia.exists():
        shutil.rmtree(copia)
    shutil.copytree(ENTREGA, copia)
    shutil.copytree(RAIZ / "frontend", copia / "pagina", ignore=shutil.ignore_patterns(".gitkeep"))
    zip_ruta = shutil.make_archive(str(copia), "zip", root_dir=copia.parent, base_dir=copia.name)
    return Path(zip_ruta)


if __name__ == "__main__":
    z = armar()
    print(f"ENTREGA/ lista · copia comprimida: {z} · {z.stat().st_size / 1e6:.1f} MB")
