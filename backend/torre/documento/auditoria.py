# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos (calidad de la página, Fase 10)
# Qué hace:          Audita la página en 4 vistas (escritorio y celular, de día y de noche) con un navegador automatizado:
#                    1. Accesibilidad con axe-core (el estándar abierto que usan los navegadores y Lighthouse): reglas
#                       WCAG 2.1 A y AA, con su gravedad y cuántos elementos fallan.
#                    2. Lo que pide el proyecto: sin errores de JavaScript, sin llamadas a otros sitios, sin imágenes
#                       rotas, sin desborde horizontal, todas las imágenes con texto alternativo (o marcadas decorativas),
#                       un solo título principal, botones con nombre, y que se pueda recorrer con el teclado.
#                    3. Peso de la página.
#                    Escribe docs/ejecutivo/AUDITORIA_PAGINA.md.
# Por qué así:       Decisión de Brandon (02-oct-2026, docs/decisiones/23-pagina-final.md): la Fase 10 se cierra con
#                    revisión automática y se DECLARA que no hubo prueba con personas. axe-core y no una lista propia: es
#                    un estándar verificable por cualquiera.
# Datos de entrada:  frontend/index.html (la página como la ve el visitante, sin servidor).
# Alimenta a:        La Fase 10 (página final) y el criterio 10 de la rúbrica (informe visualmente adecuado).
#
# Uso:  cd backend && ..\.venv\Scripts\python -m torre.documento.auditoria

from collections import Counter

from torre.base.entorno import RAIZ

PAGINA = (RAIZ / "frontend" / "index.html").as_uri()
SALIDA = RAIZ / "docs" / "ejecutivo" / "AUDITORIA_PAGINA.md"
VISTAS = [("Escritorio, día", 1280, 900, "dia"), ("Escritorio, noche", 1280, 900, "noche"),
          ("Celular, día", 390, 844, "dia"), ("Celular, noche", 390, 844, "noche")]

REVISION_PROPIA = """() => {
  const imgs = [...document.images];
  const sinAlt = imgs.filter(i => !i.hasAttribute('alt')).map(i => i.src.split('/').pop());
  const rotas = imgs.filter(i => i.complete && i.naturalWidth === 0 && i.src).map(i => i.src.split('/').pop());
  const botones = [...document.querySelectorAll('button, a[href], [role=button]')].filter(b => {
    const r = b.getBoundingClientRect(); if (!r.width && !r.height) return false;
    return !(b.innerText.trim() || b.getAttribute('aria-label') || b.getAttribute('title') || b.querySelector('img[alt]:not([alt=""])'));
  }).map(b => b.outerHTML.slice(0, 80));
  return {h1: document.querySelectorAll('h1').length, lang: document.documentElement.lang, sinAlt, rotas, botonesSinNombre: botones,
          desborde: document.documentElement.scrollWidth - innerWidth};
}"""


def revelar_todo(pg):
    """Baja por toda la página para que se dibujen las secciones que aparecen al hacer scroll."""
    alto = pg.evaluate("document.body.scrollHeight")
    for y in range(0, alto, 700):
        pg.evaluate(f"window.scrollTo(0, {y})")
        pg.wait_for_timeout(60)
    # Todo lo que entra con animación se deja en su estado final antes de medir (si no, axe mide a media transición).
    pg.evaluate("document.querySelectorAll('.revela, .fases, .pres-grafica').forEach(e => e.classList.add('visible'))")
    pg.wait_for_timeout(3000)


def teclado(pg, pasos: int = 40) -> dict:
    """Recorre la página con Tab: ¿cada elemento enfocado se ve (tiene contorno o cambia de estilo)?"""
    pg.evaluate("window.scrollTo(0, 0)")
    pg.locator("body").focus()
    enfocados, sin_marca = 0, []
    for _ in range(pasos):
        pg.keyboard.press("Tab")
        info = pg.evaluate("""() => { const e = document.activeElement; if (!e || e === document.body) return null;
          const s = getComputedStyle(e); return {tag: e.tagName, texto: (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 30),
          marca: s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0 || s.boxShadow !== 'none'}; }""")
        if info:
            enfocados += 1
            if not info["marca"]:
                sin_marca.append(f"{info['tag']} «{info['texto']}»")
    return {"enfocados": enfocados, "sin_marca": sin_marca}


def auditar() -> dict:
    from axe_playwright_python.sync_playwright import Axe
    from playwright.sync_api import sync_playwright
    axe = Axe()
    resultados = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for nombre, ancho, alto, tema in VISTAS:
            pg = b.new_page(locale="es-MX", viewport={"width": ancho, "height": alto})
            errores, externas, bytes_ = [], [], Counter()
            pg.on("pageerror", lambda e: errores.append(str(e)))
            pg.on("request", lambda r: externas.append(r.url) if r.url.startswith("http") else None)
            pg.on("response", lambda r: bytes_.update({"total": len(r.body()) if r.ok else 0}) if r.url.startswith("file") else None)
            pg.goto(PAGINA, wait_until="networkidle")
            if tema == "noche":
                pg.locator("#tema").click()
                pg.wait_for_timeout(900)
            revelar_todo(pg)
            ax = axe.run(pg, options={"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]}})
            fallas = [{"regla": v["id"], "gravedad": v["impact"], "que": v["help"], "elementos": len(v["nodes"]),
                       "ejemplo": v["nodes"][0]["target"][0] if v["nodes"] else ""} for v in ax.response["violations"]]
            propia = pg.evaluate(REVISION_PROPIA)
            tec = teclado(pg) if tema == "dia" else None
            resultados.append({"vista": nombre, "fallas": fallas, "pasan": len(ax.response["passes"]), "errores": errores,
                               "externas": externas, "propia": propia, "teclado": tec, "kb": round(bytes_["total"] / 1024)})
            pg.close()
        b.close()
    return {"vistas": resultados}


def escribir(r: dict) -> str:
    md = ["# Auditoría de la página — Torre del Caribe", "",
          "Autor: **Brandon Uriel García Sánchez** · Generada por `python -m torre.documento.auditoria` (no se edita a mano).",
          "", "Herramienta: **axe-core** (reglas WCAG 2.1 A y AA) en un navegador Chromium automatizado, más las revisiones "
          "propias del proyecto. **No hubo prueba con personas** (decisión de Brandon, nota 23).", "",
          "| Vista | Reglas que pasan | Fallas (reglas) | Elementos con falla | Errores JS | Llamadas a otros sitios | Imágenes sin alt | Desborde |",
          "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for v in r["vistas"]:
        md.append(f"| {v['vista']} | {v['pasan']} | {len(v['fallas'])} | {sum(f['elementos'] for f in v['fallas'])} | "
                  f"{len(v['errores'])} | {len(v['externas'])} | {len(v['propia']['sinAlt'])} | {v['propia']['desborde']} px |")
    for v in r["vistas"]:
        md += ["", f"## {v['vista']}", ""]
        if v["fallas"]:
            md += ["| Regla | Gravedad | Qué pide | Elementos | Ejemplo |", "|---|---|---|---:|---|"]
            md += [f"| `{f['regla']}` | {f['gravedad']} | {f['que']} | {f['elementos']} | `{str(f['ejemplo'])[:60]}` |" for f in v["fallas"]]
        else:
            md.append("Sin fallas de axe-core.")
        p = v["propia"]
        md.append(f"\n- Títulos principales (h1): {p['h1']} · idioma declarado: `{p['lang']}` · botones sin nombre: "
                  f"{len(p['botonesSinNombre'])} · imágenes rotas: {len(p['rotas'])}")
        if v["teclado"]:
            t = v["teclado"]
            md.append(f"- Teclado: {t['enfocados']} de 40 tabulaciones llegaron a un elemento; sin marca visible: "
                      f"{len(t['sin_marca'])}" + (f" ({', '.join(t['sin_marca'][:5])})" if t["sin_marca"] else ""))
    texto = "\n".join(md) + "\n"
    SALIDA.write_text(texto, encoding="utf-8")
    return texto


if __name__ == "__main__":
    r = auditar()
    print(escribir(r).split("\n## ")[0])
    for v in r["vistas"]:
        for f in v["fallas"]:
            print(v["vista"], "|", f["regla"], f["gravedad"], f["elementos"], f["ejemplo"])
