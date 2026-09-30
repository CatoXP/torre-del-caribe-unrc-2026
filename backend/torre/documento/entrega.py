# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos (entregables)
# Qué hace:          Arma la carpeta de entrega de avances: los notebooks ejecutados (también en HTML, para abrirlos
#                    sin Jupyter), la página web lista para abrir con doble clic, los PDF del proyecto y las notas de
#                    decisión y ecuaciones. Al final la comprime en un .zip para enviarla o subirla.
# Por qué así:       El equipo y los profesores piden avances sin tener Python instalado. Todo lo que va en la carpeta
#                    sale de los archivos del proyecto tal como están (no se reescribe ninguna cifra): la página usa el
#                    mismo datos/pagina.js generado por datos_pagina.py y los notebooks ya vienen ejecutados.
#                    Alternativa descartada: pedir que clonen el repositorio y corran todo (necesita Python, Java y
#                    ~800 MB de datos).
# Datos de entrada:  notebooks/*.ipynb, frontend/, *.pdf de la raíz, docs/decisiones, docs/metodologia/ECUACIONES.md.
# Alimenta a:        La revisión de avances (profesores, equipo) y el coloquio.
#
# Uso:  cd backend && ..\.venv\Scripts\python -m torre.documento.entrega

import shutil
from datetime import date
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter

RAIZ = Path(__file__).resolve().parents[3]
NOTEBOOKS = ["01_planteamiento.ipynb", "02_radar.ipynb"]
PDFS = ["Documento_Ejecutivo_Torre_del_Caribe.pdf", "Hoja_de_Ruta_Torre_del_Caribe.pdf", "Plan_v3_Torre_del_Caribe.pdf"]

LEEME = """# Torre del Caribe · Avances al {fecha}

Proyecto del Problema Prototípico (UNRC · LCDN 5° semestre 2026-2). Autor: Brandon Uriel García Sánchez.
Campaña de turismo inteligente para el sur de Quintana Roo con ciencia de datos.

## Qué hay en esta carpeta
| Carpeta o archivo | Qué es | Cómo se abre |
|---|---|---|
| `pagina/index.html` | La página web del proyecto (funciona sin internet) | Doble clic; se abre en el navegador |
| `notebooks/*.html` | Los notebooks ya ejecutados, con sus tablas y gráficas | Doble clic; se abren en el navegador |
| `notebooks/*.ipynb` | Los mismos notebooks, para abrir en Jupyter o VS Code | Jupyter / VS Code |
| `Documento_Ejecutivo_Torre_del_Caribe.pdf` | Explicación no técnica de todo el proyecto, fase por fase | Cualquier lector de PDF |
| `Hoja_de_Ruta_Torre_del_Caribe.pdf` | Qué está hecho y qué sigue | PDF |
| `Plan_v3_Torre_del_Caribe.pdf` | El plan aprobado | PDF |
| `documentos/decisiones/` | Por qué se tomó cada decisión, con su evidencia | Cualquier editor de texto (Markdown) |
| `documentos/ECUACIONES.md` | Todas las ecuaciones con ejemplos resueltos a mano | Editor de texto (Markdown) |

## Notebooks
1. **01_planteamiento** (Fase 3): variables, actores y la concentración del turismo. En los cinco lugares vive el 12.3 %
   de la gente del estado, pero llega el 1.4 % de los pasajeros de avión.
2. **02_radar** (Fase 4): índice de presión turística, estados tranquilo / concurrido / saturado, predicción del mes
   siguiente contra "igual que el mes pasado", cadena de Markov del norte y agrupamiento de 55 centros turísticos.

## Estado del proyecto
- Fases 0, 1 y 3 completas; Fase 4 auditada y lista para revisión; Fase 2 en curso (faltan algunas fuentes).
- Todas las cifras salen de fuentes oficiales (SITUR-Q, SECTUR-DataTur, INEGI, INAH); lo que no existe se declara.
- El código completo está en el repositorio privado de GitHub `CatoXP/torre-del-caribe-unrc-2026`.
"""


def exportar_html(origen: Path, destino: Path) -> None:
    nb = nbformat.read(origen, as_version=4)
    html, _ = HTMLExporter(template_name="lab").from_notebook_node(nb)
    destino.write_text(html, encoding="utf-8")


def armar(fecha: date | None = None) -> Path:
    fecha = fecha or date.today()
    salida = RAIZ / "entregas" / f"Torre_del_Caribe_avances_{fecha.isoformat()}"
    if salida.exists():
        shutil.rmtree(salida)
    (salida / "notebooks").mkdir(parents=True)
    for n in NOTEBOOKS:
        origen = RAIZ / "notebooks" / n
        if not origen.exists():
            raise FileNotFoundError(f"Falta el notebook {n}: primero corre notebooks/_construir_*.py")
        shutil.copy2(origen, salida / "notebooks" / n)
        exportar_html(origen, salida / "notebooks" / n.replace(".ipynb", ".html"))
    # La página: la misma carpeta frontend (el botón "Documento" apunta a ../Documento_Ejecutivo..., que queda al lado)
    shutil.copytree(RAIZ / "frontend", salida / "pagina", ignore=shutil.ignore_patterns(".gitkeep"))
    for pdf in PDFS:
        if (RAIZ / pdf).exists():
            shutil.copy2(RAIZ / pdf, salida / pdf)
    shutil.copytree(RAIZ / "docs" / "decisiones", salida / "documentos" / "decisiones")
    shutil.copy2(RAIZ / "docs" / "metodologia" / "ECUACIONES.md", salida / "documentos" / "ECUACIONES.md")
    (salida / "LEEME.md").write_text(LEEME.format(fecha=fecha.strftime("%d/%m/%Y")), encoding="utf-8")
    zip_ruta = shutil.make_archive(str(salida), "zip", root_dir=salida.parent, base_dir=salida.name)
    return Path(zip_ruta)


if __name__ == "__main__":
    z = armar()
    print(f"{z} · {z.stat().st_size / 1e6:.1f} MB")
