# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Guarda como evidencia (HTML, captura de página completa y texto) las publicaciones públicas
#                    sobre el avance del sargazo hacia la Bahía de Chetumal, y extrae los párrafos que mencionan la
#                    bahía, Chetumal, Calderitas, Bacalar Chico o el canal Zaragoza. Todo se registra en el manifiesto.
# Por qué así:       El semáforo oficial diario del sargazo (CEMAS/SEMA Quintana Roo) solo se publica en Facebook
#                    (verificado el 28-sep-2026: sema.qroo.gob.mx redirige a qroo.gob.mx/sema/, que no lo contiene),
#                    y los términos de Facebook prohíben extraerlo de forma automática (regla de oro 4). Por eso la
#                    verificación se hace con fuentes públicas que sí se pueden consultar: El Colegio de la Frontera Sur
#                    (ECOSUR, centro de investigación con sede en Chetumal) y medios que citan al monitoreo.
#                    Esto NO es una serie de datos: es evidencia fechada para decidir si Chetumal y Calderitas-Oxtankah
#                    siguen como destinos (docs/decisiones/01-regiones.md).
# Datos de entrada:  Páginas públicas listadas en FUENTES (consultadas con Playwright).
# Alimenta a:        La condición de riesgo de las regiones 1 y 2, y la regla de pausa de A5.

import re
from datetime import date

from playwright.sync_api import sync_playwright

from torre.base.manifiesto import BRONZE, registrar

FUENTES = {
    "ecosur": "https://www.ecosur.mx/alarma-avance-de-sargazo-en-canales-de-chetumal-el-preludio-de-crisis-mayor/",
    "reportur_2026-09-28": "https://www.reportur.com/agencias/2026/09/28/qroo-acumulaciones-de-sargazo-se-desplazan-hacia-bahia-de-chetumal/",
    "jornada_maya": "https://www.lajornadamaya.mx/quintana-roo/268647/quintana-roo-alertan-por-posible-desplazamiento-de-sargazo-hacia-bahia-de-chetumal",
    "quintanarroense_2026-09-23": "https://elquintanarroense.com.mx/2026/09/23/avistan-sargazo-en-el-bahia-de-chetumal/",
    "sol_quintana_roo": "https://solquintanaroo.mx/sargazo-entra-a-bacalar-chico-y-amenaza-con-llegar-a-chetumal/",
}
CLAVES = re.compile(r"chetumal|calderitas|bah[ií]a|bacalar chico|zaragoza|oxtankah", re.I)
NAVEGADOR = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/131.0 Safari/537.36")


def capturar_evidencia() -> dict[str, list[str]]:
    """Visita cada fuente, guarda HTML + captura + párrafos relevantes y devuelve esos párrafos por fuente."""
    carpeta = BRONZE / "evidencia_sargazo" / date.today().isoformat()
    carpeta.mkdir(parents=True, exist_ok=True)
    hallazgos: dict[str, list[str]] = {}
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page(user_agent=NAVEGADOR, viewport={"width": 1366, "height": 900})
        for clave, url in FUENTES.items():
            try:
                pagina.goto(url, timeout=90_000, wait_until="domcontentloaded")
                pagina.wait_for_timeout(3_000)
            except Exception as e:  # una fuente caída no detiene las demás; se declara
                hallazgos[clave] = [f"NO DISPONIBLE: {e!r}"]
                continue
            parrafos = [t.strip() for t in pagina.locator("p").all_inner_texts() if CLAVES.search(t) and len(t.strip()) > 40]
            hallazgos[clave] = parrafos

            (carpeta / f"{clave}.html").write_text(pagina.content(), encoding="utf-8")
            pagina.screenshot(path=str(carpeta / f"{clave}.png"), full_page=True)
            (carpeta / f"{clave}_parrafos.txt").write_text(f"{url}\n\n" + "\n\n".join(parrafos), encoding="utf-8")
            registrar("Evidencia sargazo", carpeta / f"{clave}.html", url, filas=len(parrafos), nota="HTML; párrafos sobre la bahía")
            registrar("Evidencia sargazo", carpeta / f"{clave}.png", url, nota="captura de página completa")
            registrar("Evidencia sargazo", carpeta / f"{clave}_parrafos.txt", url, filas=len(parrafos), nota="párrafos relevantes extraídos")
        navegador.close()
    return hallazgos


if __name__ == "__main__":
    for fuente, parrafos in capturar_evidencia().items():
        print(f"\n=== {fuente} ({len(parrafos)} párrafos)")
        for t in parrafos[:6]:
            print("  •", t[:400])
