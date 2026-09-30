# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Extrae con un navegador automatizado (Playwright + Chromium) las tablas de costos y
#                    desempeño publicitario por industria de WordStream 2025 y LocaliQ 2026 (Google Ads/búsqueda y
#                    Facebook). Guarda el HTML completo, una captura de pantalla de página completa y todas las tablas
#                    en un CSV largo, y registra todo en el manifiesto como fuente D13.
# Por qué así:       Estas páginas bloquean las descargas automáticas simples (respondieron 403 a una petición
#                    directa el 27-sep-2026), pero muestran sus datos en tablas HTML a cualquier navegador. Un navegador
#                    real las lee igual que una persona y deja captura como evidencia.
#                    Verificado el 28-sep-2026: el CTR de Travel en Google Ads 2025 según la tabla oficial es 8.73 %, no
#                    el 8.24 % de un resumen de búsqueda web. Por eso se extrae de la fuente y no de resúmenes.
#                    Limitación declarada: son promedios de anunciantes de EE. UU.; en el modelo se usan como supuesto
#                    etiquetado, no como medición de México.
# Datos de entrada:  D13 — wordstream.com y localiq.com (páginas públicas de benchmarks).
# Alimenta a:        Fase 6, investigación de operaciones (costo por clic y conversión por canal para repartir el presupuesto).

import csv
import re
from datetime import date

from playwright.sync_api import sync_playwright

from torre.base.manifiesto import BRONZE, registrar

PAGINAS = {
    "wordstream_google_2025": ("WordStream", "Google Ads", 2025, "https://www.wordstream.com/blog/2025-google-ads-benchmarks"),
    "wordstream_facebook_2025": ("WordStream", "Facebook Ads", 2025, "https://www.wordstream.com/blog/facebook-ads-benchmarks-2025"),
    "localiq_busqueda_2026": ("LocaliQ", "Búsqueda (Google/Microsoft)", 2026, "https://localiq.com/blog/search-advertising-benchmarks/"),
    "localiq_facebook_2026": ("LocaliQ", "Facebook Ads", 2026, "https://localiq.com/blog/facebook-advertising-benchmarks/"),
}
NAVEGADOR = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/131.0 Safari/537.36")


def a_numero(texto: str) -> float | None:
    """'$2.12' → 2.12 · '8.73%' → 8.73 · ' $44.70' → 44.70. Devuelve None si no hay número."""
    m = re.search(r"-?\d+(?:,\d{3})*(?:\.\d+)?", texto.replace("\xa0", " "))
    return float(m.group(0).replace(",", "")) if m else None


def descargar_benchmarks() -> list[dict]:
    carpeta = BRONZE / "benchmarks" / date.today().isoformat()
    carpeta.mkdir(parents=True, exist_ok=True)
    filas_csv, registros = [], []
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page(user_agent=NAVEGADOR, viewport={"width": 1366, "height": 900})
        for clave, (editor, canal, anio, url) in PAGINAS.items():
            pagina.goto(url, timeout=90_000, wait_until="domcontentloaded")
            pagina.wait_for_timeout(4_000)  # deja que termine de pintar las tablas

            html = carpeta / f"{clave}.html"
            html.write_text(pagina.content(), encoding="utf-8")
            captura = carpeta / f"{clave}.png"
            pagina.screenshot(path=str(captura), full_page=True)

            n_tablas = pagina.locator("table").count()
            for i in range(n_tablas):
                lineas = [l.split("\t") for l in pagina.locator("table").nth(i).inner_text().splitlines() if l.strip()]
                encabezado, cuerpo = lineas[0], lineas[1:]
                metrica = encabezado[1].strip() if len(encabezado) > 1 else f"tabla_{i}"
                for celdas in cuerpo:
                    if len(celdas) < 2:
                        continue
                    filas_csv.append({
                        "clave_pagina": clave, "editor": editor, "canal": canal, "anio": anio,
                        "tabla": i, "metrica": metrica, "categoria": celdas[0].strip(),
                        "valor_texto": celdas[1].strip(), "valor": a_numero(celdas[1]), "url": url,
                    })
            registros.append(registrar("D13 Benchmarks", html, url, filas=n_tablas, nota=f"{editor} {canal} {anio}: HTML ({n_tablas} tablas)"))
            registros.append(registrar("D13 Benchmarks", captura, url, nota="captura de página completa (evidencia)"))
        navegador.close()

    salida = carpeta / "benchmarks_tablas.csv"
    with open(salida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas_csv[0]))
        w.writeheader()
        w.writerows(filas_csv)
    registros.append(registrar("D13 Benchmarks", salida, "extraído de las 4 páginas con Playwright", filas=len(filas_csv),
                               nota="todas las tablas, todas las industrias"))
    return filas_csv


if __name__ == "__main__":
    filas = descargar_benchmarks()
    print(f"{len(filas)} filas extraídas")
    for f in filas:
        if f["categoria"].lower() == "travel":
            print(f"  {f['editor']:10s} {f['canal']:28s} {f['metrica']:14s} {f['valor_texto']}")
