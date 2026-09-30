# Autor: Brandon Uriel García Sánchez
# Módulo: Documento ejecutivo
# Qué hace:          Convierte docs/ejecutivo/DOCUMENTO_EJECUTIVO.md en un PDF con el estilo de la UNRC (portada,
#                    títulos en guinda, detalles en dorado, Noto Sans, gráficas) y lo guarda como
#                    Documento_Ejecutivo_Torre_del_Caribe.pdf en la raíz del proyecto.
# Por qué así:       El documento ejecutivo se entrega en PDF (petición de Brandon, 28-sep-2026). Se escribe en
#                    Markdown porque es fácil de mantener fase por fase, y este script produce el PDF con un solo
#                    comando. Chromium (el mismo navegador de Playwright) imprime el HTML a PDF con las gráficas y la
#                    tipografía incluidas.
# Datos de entrada:  docs/ejecutivo/DOCUMENTO_EJECUTIVO.md, docs/ejecutivo/figuras/*.png, herramientas/fuentes/.
# Alimenta a:        El entregable que redacta el equipo y la presentación del coloquio.

from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[3]
FUENTE_MD = RAIZ / "docs" / "ejecutivo" / "DOCUMENTO_EJECUTIVO.md"
SALIDA = RAIZ / "Documento_Ejecutivo_Torre_del_Caribe.pdf"
FUENTES = RAIZ / "herramientas" / "fuentes"

CSS = """
@font-face { font-family: 'Noto Sans'; src: url('{f}/NotoSans-Regular.ttf'); font-weight: 400; }
@font-face { font-family: 'Noto Sans'; src: url('{f}/NotoSans-SemiBold.ttf'); font-weight: 600; }
@font-face { font-family: 'Noto Sans'; src: url('{f}/NotoSans-Bold.ttf'); font-weight: 700; }
@page { size: Letter; margin: 22mm 20mm 20mm 20mm; }
body { font-family: 'Noto Sans', sans-serif; color: #3A3A3A; font-size: 10.5pt; line-height: 1.55; }
h1 { color: #9F2241; font-size: 26pt; margin: 0 0 4pt 0; }
h2 { color: #9F2241; font-size: 16pt; border-bottom: 2.5pt solid #BC955C; padding-bottom: 3pt; margin-top: 22pt;
     page-break-after: avoid; }
h3 { color: #9F2241; font-size: 12.5pt; margin-top: 14pt; page-break-after: avoid; }
strong { color: #3A3A3A; font-weight: 700; }
a { color: #9F2241; }
blockquote { border-left: 4pt solid #BC955C; background: #FAF6EF; margin: 10pt 0; padding: 6pt 12pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9pt; page-break-inside: avoid; }
th { background: #9F2241; color: white; text-align: left; padding: 4pt 6pt; }
td { border-bottom: 0.5pt solid #D9CBB5; padding: 4pt 6pt; vertical-align: top; }
tr:nth-child(even) td { background: #FAF6EF; }
img { max-width: 100%; max-height: 105mm; width: auto; display: block; margin: 8pt auto 2pt auto; page-break-inside: avoid; }
p > em:only-child { display: block; text-align: center; font-size: 8.5pt; color: #6B6B6B; }
hr { border: none; border-top: 1pt solid #D9CBB5; margin: 16pt 0; }
code { font-size: 9pt; background: #F4ECEE; padding: 0 3pt; border-radius: 2pt; }
.portada { height: 230mm; display: flex; flex-direction: column; justify-content: center; page-break-after: always;
           border-left: 10pt solid #9F2241; padding-left: 18pt; }
.portada .inst { color: #BC955C; font-weight: 700; letter-spacing: 1pt; font-size: 11pt; }
.portada .titulo { color: #9F2241; font-size: 38pt; font-weight: 700; line-height: 1.1; margin: 10pt 0; }
.portada .sub { font-size: 14pt; color: #3A3A3A; }
.portada .datos { margin-top: 40pt; font-size: 10.5pt; line-height: 1.8; }
"""


def _separar_listas(md: str) -> str:
    """Inserta una línea en blanco antes de cada lista que va pegada a un párrafo.

    El convertidor de Markdown exige esa línea en blanco; sin ella, "Texto:\\n- punto" sale en el PDF como texto corrido.
    """
    import re

    lineas, salida = md.splitlines(), []
    es_item = lambda l: re.match(r"\s*([-*]|\d+\.)\s", l) is not None
    for i, linea in enumerate(lineas):
        if es_item(linea) and i > 0 and lineas[i - 1].strip() and not es_item(lineas[i - 1]) \
                and not lineas[i - 1].lstrip().startswith(("|", ">")) and not linea.startswith((" ", "\t")):
            salida.append("")
        salida.append(linea)
    return "\n".join(salida)


def generar_pdf(fuente_md: Path = FUENTE_MD, salida: Path = SALIDA,
                subtitulo: str = "Documento ejecutivo del proyecto<br>Campaña inteligente para redistribuir el turismo en Quintana Roo") -> Path:
    """Convierte un Markdown del proyecto en PDF con portada y estilo UNRC. Sirve para el documento ejecutivo y la hoja de ruta."""
    texto = _separar_listas(fuente_md.read_text(encoding="utf-8"))
    # El encabezado del Markdown se reemplaza por una portada; el resto se convierte tal cual.
    cuerpo_md = texto.split("---", 1)[1] if "---" in texto else texto
    cuerpo = markdown.markdown(cuerpo_md, extensions=["tables", "sane_lists"])
    portada = f"""
    <div class="portada">
      <div class="inst">UNIVERSIDAD NACIONAL ROSARIO CASTELLANOS</div>
      <div class="titulo">Torre del Caribe</div>
      <div class="sub">{subtitulo}</div>
      <div class="datos">
        Licenciatura en Ciencias de Datos para Negocios · 5° semestre, 2026-2<br>
        Problema Prototípico: <em>Turismo inteligente sustentable para México</em><br>
        Responsable técnico: <strong>Brandon Uriel García Sánchez</strong>
      </div>
    </div>"""
    base = fuente_md.parent.as_uri() + "/"  # para que las gráficas (figuras/...) se encuentren
    html = (f"<!doctype html><html lang='es'><head><meta charset='utf-8'><base href='{base}'>"
            f"<style>{CSS.replace('{f}', FUENTES.as_uri())}</style></head><body>{portada}{cuerpo}</body></html>")
    temporal = fuente_md.parent / "_documento_para_pdf.html"
    temporal.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto(temporal.as_uri(), wait_until="networkidle")
        pagina.pdf(path=str(salida), format="Letter", print_background=True,
                   display_header_footer=True, header_template="<span></span>",
                   footer_template=("<div style='font-family:sans-serif;font-size:8px;color:#9F2241;width:100%;"
                                    "text-align:center'>Torre del Caribe · UNRC · página "
                                    "<span class='pageNumber'></span> de <span class='totalPages'></span></div>"),
                   margin={"top": "22mm", "bottom": "20mm", "left": "20mm", "right": "20mm"})
        navegador.close()
    temporal.unlink()
    return salida


if __name__ == "__main__":
    print(generar_pdf())
