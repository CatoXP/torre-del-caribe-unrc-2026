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
pre { background: #FAF6EF; border-left: 3pt solid #BC955C; padding: 6pt 10pt; font-size: 8.5pt; line-height: 1.4;
      white-space: pre-wrap; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
math { font-size: 1.08em; }
math[display="block"] { display: block math; margin: 9pt auto; text-align: center; font-size: 1.18em; }
.indice { page-break-after: always; }
.indice h2 { margin-top: 0; }
.indice ol { list-style: none; padding-left: 0; line-height: 1.7; font-size: 10pt; }
.indice ol ol { padding-left: 14pt; }
.indice ol ol { font-size: 9pt; color: #6B6B6B; line-height: 1.5; }
.indice a { color: #3A3A3A; text-decoration: none; }
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


def _matematicas(md: str) -> tuple[str, dict]:
    """Cambia cada fórmula LaTeX por una marca y guarda su versión MathML (Chromium la dibuja sin internet).
    Delimitadores: \[ … \] para fórmula en su propio renglón y \( … \) dentro del texto. No se usa $ porque el
    signo de pesos aparece en el texto ($250,000)."""
    import re

    from latex2mathml.converter import convert

    marcas = {}

    def guardar(latex: str, modo: str) -> str:
        # 250{,}000 → un solo número "250,000" (si no, MathML separa la coma y queda "250, 000").
        latex = re.sub(r"\d+(?:\{,\}\d{3})+(?:\.\d+)?", lambda m: r"\text{" + m.group(0).replace("{,}", ",") + "}", latex)
        clave = f"MATEMATICAQ{len(marcas):04d}Q"
        marcas[clave] = convert(latex.strip(), display=modo)
        return clave

    md = re.sub(r"\\\[(.+?)\\\]", lambda m: guardar(m.group(1), "block"), md, flags=re.S)
    md = re.sub(r"\\\((.+?)\\\)", lambda m: guardar(m.group(1), "inline"), md, flags=re.S)
    return md, marcas


def _indice(html: str) -> tuple[str, str]:
    """Pone un id a cada título h2/h3 y arma el índice del documento con ellos."""
    import re

    entradas, n = [], [0]

    def marcar(m):
        n[0] += 1
        nivel, texto = m.group(1), m.group(2)
        entradas.append((nivel, texto, f"s{n[0]}"))
        return f'<h{nivel} id="s{n[0]}">{texto}</h{nivel}>'

    html = re.sub(r"<h([23])>(.+?)</h\1>", marcar, html)
    partes, abierto = ["<div class='indice'><h2>Contenido</h2><ol>"], False
    for nivel, texto, ancla in entradas:
        limpio = re.sub(r"<[^>]+>", "", texto)
        if nivel == "2":
            if abierto:
                partes.append("</ol></li>")
                abierto = False
            partes.append(f"<li><a href='#{ancla}'>{limpio}</a>")
            partes.append("<ol>")
            abierto = True
        else:
            partes.append(f"<li><a href='#{ancla}'>{limpio}</a></li>")
    if abierto:
        partes.append("</ol></li>")
    partes.append("</ol></div>")
    return html, "".join(partes).replace("<ol></ol>", "")


def generar_pdf(fuente_md: Path = FUENTE_MD, salida: Path = SALIDA,
                subtitulo: str = "Documento ejecutivo del proyecto<br>Campaña inteligente para redistribuir el turismo en Quintana Roo",
                matematicas: bool = False, indice: bool = False, conservar_html: bool = False) -> Path:
    """Convierte un Markdown del proyecto en PDF con portada y estilo UNRC. Sirve para el documento ejecutivo, la hoja de
    ruta y las guías (con fórmulas e índice)."""
    texto = _separar_listas(fuente_md.read_text(encoding="utf-8"))
    # El encabezado del Markdown se reemplaza por una portada; el resto se convierte tal cual.
    cuerpo_md = texto.split("---", 1)[1] if "---" in texto else texto
    marcas = {}
    if matematicas:
        cuerpo_md, marcas = _matematicas(cuerpo_md)
    cuerpo = markdown.markdown(cuerpo_md, extensions=["tables", "sane_lists", "fenced_code"])
    for clave, mathml in marcas.items():
        cuerpo = cuerpo.replace(f"<p>{clave}</p>", mathml).replace(clave, mathml)
    tabla_indice = ""
    if indice:
        cuerpo, tabla_indice = _indice(cuerpo)
    portada = f"""
    <div class="portada">
      <div class="inst">UNIVERSIDAD NACIONAL ROSARIO CASTELLANOS</div>
      <div class="titulo">Torre del Caribe</div>
      <div class="sub">{subtitulo}</div>
      <div class="datos">
        Licenciatura en Ciencias de Datos para Negocios · 5° semestre, 2026-2<br>
        Problema Prototípico: <em>Turismo inteligente sustentable para México</em><br>
        Responsable técnico: <strong>Brandon Uriel García Sánchez</strong><br>
        Equipo: Maribel Mondragón Mercado · Jesús Ramírez Isidro · Enrique González Ortega
      </div>
    </div>"""
    base = fuente_md.parent.as_uri() + "/"  # para que las gráficas (figuras/...) se encuentren
    html = (f"<!doctype html><html lang='es'><head><meta charset='utf-8'><base href='{base}'>"
            f"<style>{CSS.replace('{f}', FUENTES.as_uri())}</style></head><body>{portada}{tabla_indice}{cuerpo}</body></html>")
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
    if not conservar_html:
        temporal.unlink()
    return salida


if __name__ == "__main__":
    print(generar_pdf())
