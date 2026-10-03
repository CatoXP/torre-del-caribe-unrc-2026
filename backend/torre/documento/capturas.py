# Autor: Brandon Uriel García Sánchez
# Módulo: Documento (capturas de la página)
# Qué hace:          Toma las capturas de la página tal como está hoy (escritorio, celular, noche e inglés) para el
#                    documento ejecutivo: una por sección, con nombre fijo (docs/ejecutivo/capturas/pNN_*.png).
# Por qué así:       Las capturas c01–c24 se tomaron a mano en cada rediseño y quedaron viejas (portada y secciones que ya
#                    no existen así). Con un programa, cualquiera puede volver a tomarlas igual tras un cambio, y el
#                    documento siempre muestra la página real. Alternativa descartada: capturas a mano (se desactualizan).
# Datos de entrada:  frontend/index.html, abierta sin servidor (la misma vista que GitHub Pages).
# Alimenta a:        Capítulo 6 del documento ejecutivo (la página web) y el criterio 10 de la rúbrica.
#
# Uso:  cd backend && ..\.venv\Scripts\python -m torre.documento.capturas

from torre.base.entorno import RAIZ

PAGINA = (RAIZ / "frontend" / "index.html").as_uri()
SALIDA = RAIZ / "docs" / "ejecutivo" / "capturas"

# (archivo, id de la sección); se toma la sección desde su borde superior, a la altura de una pantalla.
SECCIONES = [
    ("p03_que_hacer", "que-hacer"), ("p05_vive_el_sur", "vive"),
    ("p06_preguntas", "preguntas"), ("p08_el_dato", "dato"), ("p09_problema", "problema"), ("p10_radar", "radar"),
    ("p11_como_llega", "movimiento"), ("p12_dinero", "dinero"), ("p13_presupuesto", "presupuesto"),
    ("p14_torre_en_vivo", "envivo"), ("p15_campana", "campana"), ("p16_norte", "norte"), ("p17_fases", "fases"),
    ("p18_equipo", "equipo"),
]


def _revelar(pg):
    """Baja por toda la página para que se dibujen las secciones que aparecen al hacer scroll y deja las animaciones
    en su estado final (si no, la captura sale a media transición)."""
    alto = pg.evaluate("document.body.scrollHeight")
    for y in range(0, alto, 700):
        pg.evaluate(f"window.scrollTo(0, {y})")
        pg.wait_for_timeout(50)
    pg.evaluate("document.querySelectorAll('.revela, .fases, .pres-grafica, .aparece').forEach(e => e.classList.add('visible'))")
    pg.wait_for_timeout(1500)


def _elegir(pg, lugar: str, mes: str, anio: str):
    """Elige lugar y mes en el planeador de la portada, como lo haría un visitante."""
    pg.locator("#elige .planea-lugar", has_text=lugar).first.click()
    pg.locator("#elige .planea-mes", has_text=mes).filter(has_text=anio).first.click()
    pg.wait_for_timeout(700)


# Lo fijo (barra de arriba, botón del chat, aviso de temporada alta) se esconde en las capturas de sección: si no, tapa
# el contenido. La portada sí se captura con todo, como la ve el visitante.
OCULTAR_FIJOS = """header, .barra, #anuncio, .chat-boton, #aviso-lleno, .aviso-lleno, .progreso { visibility: hidden !important; }"""


def _seccion(pg, id_: str, archivo: str, alto_max: int = 1500, desde: int = 0):
    """Captura la sección completa (hasta alto_max px), desde su borde superior más `desde` px."""
    pg.evaluate(f"document.getElementById('{id_}').scrollIntoView({{block: 'start'}})")
    pg.wait_for_timeout(900)
    caja = pg.evaluate(f"(() => {{ const e = document.getElementById('{id_}'); const r = e.getBoundingClientRect();"
                       f" return {{y: r.top + window.scrollY, h: e.offsetHeight}}; }})()")
    pg.screenshot(path=str(SALIDA / f"{archivo}.png"), full_page=True,
                  clip={"x": 0, "y": caja["y"] + desde, "width": 1280, "height": min(caja["h"] - desde, alto_max)})


def capturar() -> list[str]:
    from playwright.sync_api import sync_playwright
    SALIDA.mkdir(parents=True, exist_ok=True)
    hechas = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        # Escritorio, de día, en español.
        pg = b.new_page(locale="es-MX", viewport={"width": 1280, "height": 960})
        pg.add_init_script("try { localStorage.setItem('idioma', 'es'); localStorage.setItem('tema', 'dia'); } catch (e) {}")
        pg.goto(PAGINA, wait_until="networkidle")
        pg.wait_for_timeout(1500)
        _elegir(pg, "Ruta", "ene", "2027")
        pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(600)
        pg.screenshot(path=str(SALIDA / "p01_portada.png")); hechas.append("p01_portada")
        _revelar(pg)
        estilo = pg.add_style_tag(content=OCULTAR_FIJOS)
        _seccion(pg, "planea", "p02_asi_va_a_estar"); hechas.append("p02_asi_va_a_estar")
        for archivo, id_ in SECCIONES:
            _seccion(pg, id_, archivo); hechas.append(archivo)
        # En "Los lugares" el título se desvanece al bajar (el mapa queda fijo): se toma desde el mapa.
        _seccion(pg, "lugares", "p04_lugares", alto_max=1050, desde=430); hechas.append("p04_lugares")
        # Quien iba al norte: Cancún en enero (temporada alta) y la recomendación del sur.
        _elegir(pg, "Cancún", "ene", "2027")
        _seccion(pg, "planea", "p07_ibas_al_norte", alto_max=900); hechas.append("p07_ibas_al_norte")
        estilo.evaluate("e => e.remove()")
        pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(800)
        # El chat de preguntas rápidas.
        pg.locator("#chat-boton").click(); pg.wait_for_timeout(500)
        pg.locator("#chat input, #chat textarea").first.fill("¿Hay sargazo en Chetumal?")
        pg.keyboard.press("Enter"); pg.wait_for_timeout(800)
        pg.screenshot(path=str(SALIDA / "p22_chat.png")); hechas.append("p22_chat")
        pg.close()
        # De noche y en inglés.
        for archivo, ajuste in [("p19_noche", "localStorage.setItem('tema', 'noche'); localStorage.setItem('idioma', 'es');"),
                                ("p20_ingles", "localStorage.setItem('tema', 'dia'); localStorage.setItem('idioma', 'en');")]:
            pg = b.new_page(locale="es-MX", viewport={"width": 1280, "height": 800})
            pg.add_init_script(f"try {{ {ajuste} }} catch (e) {{}}")
            pg.goto(PAGINA, wait_until="networkidle"); pg.wait_for_timeout(1500)
            pg.screenshot(path=str(SALIDA / f"{archivo}.png")); hechas.append(archivo)
            pg.close()
        # Celular.
        pg = b.new_page(locale="es-MX", viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg.add_init_script("try { localStorage.setItem('idioma', 'es'); localStorage.setItem('tema', 'dia'); } catch (e) {}")
        pg.goto(PAGINA, wait_until="networkidle"); pg.wait_for_timeout(1500)
        pg.screenshot(path=str(SALIDA / "p21_celular.png")); hechas.append("p21_celular")
        pg.close()
        b.close()
    return hechas


if __name__ == "__main__":
    for h in capturar():
        print("✓", h)
