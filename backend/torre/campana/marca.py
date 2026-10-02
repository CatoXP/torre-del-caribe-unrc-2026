# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña (mercadotecnia, Fase 8)
# Qué hace:          Arma la campaña "El sur tiene espacio" con los 10 elementos del Problema Prototípico que le tocan:
#                    buyer persona (2), branding (identidad, personalidad, propuesta de valor, posicionamiento, elementos
#                    visuales), mensajes por persona y canal, medios justificados, piezas, implementación (calendario) e
#                    indicadores (KPI). Cada atributo de persona lleva su etiqueta: DATO (medido), DERIVADO (calculado de
#                    datos) o SUPUESTO (no hay dato; se declara). Cada mensaje lleva el dato que lo respalda.
# Por qué así:       Decisiones de Brandon del 02-oct-2026 (docs/decisiones/21-campana.md): dos personas (nacional que
#                    vuelve; extranjera que ya está en Cancún), nombre "El sur tiene espacio", tono que combina lo
#                    cercano y tranquilo, el orgullo cultural y la aventura ("es un orgullo ser mexicano").
#                    - Un mensaje no puede prometer lo que el dato no sostiene: "sin multitudes" se apoya en 15.5 veces
#                      menos visitantes que Tulum (INAH 2025); no se dan horas de viaje ni precios (no hay dato).
#                    - El lenguaje sale de las reseñas de 5 estrellas (texto.py) y evita lo que hunde una reseña (ruido,
#                      suciedad, precio, multitudes).
#                    - Los largos de los anuncios se revisan con los límites de cada plataforma (Google: título ≤ 30,
#                      descripción ≤ 90; Facebook/Instagram: título ≤ 40, texto ≤ 125 recomendado).
# Datos de entrada:  datos/silver/inah, nacionalidad; datos/gold/campana_*, presupuesto_*, pronostico_*, envivo_*;
#                    ENDUTIH 2025 (D11, cifras transcritas del PDF oficial con su página).
# Alimenta a:        La sección "La campaña" de la página, el capítulo 12 del documento ejecutivo y el coloquio.

import json

import pandas as pd

from torre.base.entorno import RAIZ

SILVER = RAIZ / "datos" / "silver"
GOLD = RAIZ / "datos" / "gold"
SALIDA = GOLD / "campana.json"

# ENDUTIH 2025 (INEGI, reporte de resultados del 16-jun-2026): cifras leídas del PDF de Bronze, con su página.
ENDUTIH = {"internet_qroo_pct": (92.1, "pág. 10"), "mensajeria_pct": (90.6, "pág. 17"),
           "redes_sociales_pct": (80.4, "pág. 17"), "audio_video_pct": (77.8, "pág. 17")}
LIMITES = {"google_titulo": 30, "google_descripcion": 90, "meta_titulo": 40, "meta_texto": 125}


def cifras() -> dict:
    i = pd.read_parquet(SILVER / "inah")
    q = i[i.es_qroo & (i.anio.astype(int) == 2025)]
    v = q.groupby("region_campana").visitantes.sum()
    nac = q[q.papel_campana == "promovida"].groupby(["region_campana", "tipo_visitante"]).visitantes.sum().unstack()
    n = pd.read_parquet(SILVER / "nacionalidad")
    c = n[(n.lugar_campana == "Cancún") & (n.anio.astype(int) == 2025)]
    tot = c.llegadas_extranjeros.sum()
    pais = c.groupby("pais").llegadas_extranjeros.sum() / tot * 100
    mes = c.groupby("mes").llegadas_extranjeros.sum()
    che = n[(n.lugar_campana == "Chetumal") & (n.anio.astype(int) == 2025)].llegadas_extranjeros.sum()
    return {
        "tulum": int(v["Tulum"]), "ruta": int(v["Ruta arqueológica del sur"]), "bahia": int(v["Bahía Calderitas–Oxtankah"]),
        "veces_ruta": round(v["Tulum"] / v["Ruta arqueológica del sur"], 1),
        "pct_nac_bahia": round(nac.loc["Bahía Calderitas–Oxtankah", "nacional"] / nac.loc["Bahía Calderitas–Oxtankah"].sum() * 100, 1),
        "pct_nac_ruta": round(nac.loc["Ruta arqueológica del sur", "nacional"] / nac.loc["Ruta arqueológica del sur"].sum() * 100, 1),
        "cancun_extranjeros": int(tot), "chetumal_extranjeros": int(che),
        "pct_eeuu": round(pais["Estados Unidos"], 1), "pct_canada": round(pais["Canadá"], 1),
        "pct_mujeres": round(c[c.sexo == "mujer"].llegadas_extranjeros.sum() / tot * 100, 1),
        "mes_pico": int(mes.idxmax()), "mes_bajo": int(mes.idxmin()),
    }


def personas(k: dict, asp: pd.DataFrame) -> list[dict]:
    q = asp[asp.pueblo == "Quintana Roo (3 pueblos)"].set_index("aspecto").riesgo_relativo
    return [
        {"clave": "vuelve", "nombre": "La que vuelve al sur",
         "quien": "Viajera mexicana que ya conoce o tiene cerca el sur de Quintana Roo y busca un viaje con historia, "
                  "comida y calma.",
         "atributos": [
             ("Origen", f"Nacional: {k['pct_nac_bahia']} % de los visitantes de Oxtankah y {k['pct_nac_ruta']} % de los de la Ruta en 2025", "dato", "INAH 2025"),
             ("Estado de origen", "No se publica de qué estado vienen los visitantes nacionales", "hueco", "—"),
             ("Cuándo viaja", "Diciembre a abril (temporada alta del sur); la campaña la invita en mayo–junio y octubre–noviembre, con espacio", "derivado", "Forma del año, Fase 5"),
             ("Qué valora", f"Calma y cultura: una reseña que habla de calma es mala {q['calma']:.2f} veces lo normal; de cultura, {q['cultura']:.2f}", "derivado", "Rest-Mex 2025, texto.py"),
             ("Qué la aleja", f"Ruido ({q['ruido']:.1f}×), suciedad ({q['limpieza']:.1f}×), precio ({q['precio']:.1f}×) y multitudes ({q['multitudes']:.1f}×) en reseñas malas", "derivado", "Rest-Mex 2025"),
             ("Cómo se informa", f"Mensajería ({ENDUTIH['mensajeria_pct'][0]} %) y redes sociales ({ENDUTIH['redes_sociales_pct'][0]} %) en el teléfono", "dato", f"ENDUTIH 2025, {ENDUTIH['mensajeria_pct'][1]}"),
             ("Edad e ingreso", "No hay dato oficial por destino: no se fija", "hueco", "—")]},
        {"clave": "baja", "nombre": "La que baja del norte",
         "quien": "Viajera de Estados Unidos o Canadá que ya está en Cancún o la Riviera Maya y puede bajar al sur en Tren "
                  "Maya o por carretera.",
         "atributos": [
             ("Origen", f"Estados Unidos {k['pct_eeuu']} % y Canadá {k['pct_canada']} % de los {k['cancun_extranjeros']:,} extranjeros que llegaron a Cancún en 2025", "dato", "UPM vía DataTur"),
             ("Sexo", f"Mujeres {k['pct_mujeres']} %", "dato", "UPM vía DataTur"),
             ("Por qué no llega sola al sur", f"El aeropuerto de Chetumal recibió {k['chetumal_extranjeros']} extranjeros en 2025", "dato", "UPM vía DataTur"),
             ("Cuándo está", f"Más llegadas en {['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'][k['mes_pico']-1]}, menos en {['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'][k['mes_bajo']-1]}; Cancún en temporada alta de noviembre a abril", "dato", "UPM; planeador Fase 5"),
             ("Qué la aleja del norte", "Multitudes, precio y sargazo (destinos excluidos por sargazo 2026)", "derivado", "Rest-Mex; REGIONES.md"),
             ("Cómo se informa", "Busca en Google y usa redes desde el destino", "supuesto", "Benchmarks de viajes (D13); sin encuesta propia"),
             ("Idioma", "Inglés (y español)", "derivado", "País de origen")]},
    ]


def marca(k: dict) -> dict:
    return {
        "nombre": "El sur tiene espacio", "lema": "Pirámides, bahía y sabor del sur, con espacio para disfrutarlos.",
        "nombre_en": "The south has room", "lema_en": "Mayan pyramids, a quiet bay and southern food, with room to enjoy them.",
        "personalidad": ["Cercana y tranquila: habla de tú, frases cortas, promete calma.",
                         "Orgullosa de lo maya y de lo mexicano: Kohunlich, Dzibanché, Ichkabal, Oxtankah.",
                         "Con espíritu de aventura: selva, caminos y ruinas para recorrer sin prisa."],
        "propuesta_valor": f"El Caribe mexicano que todavía tiene espacio: zonas mayas con {k['veces_ruta']} veces menos visitantes que Tulum, una bahía tranquila y la comida del sur.",
        "posicionamiento": "Para quien quiere el Caribe mexicano sin multitudes, el sur de Quintana Roo es la opción cultural y tranquila; a diferencia de Tulum o Cancún, aquí hay espacio, y la campaña lo cuida: nunca anuncia un lugar lleno.",
        "visual": "Sistema \"Sur mexicano\" (decisión 07): rosa, amarillo, turquesa y añil en bloques; Bricolage Grotesque y Figtree; greca maya; fotos reales comprobadas en su municipio.",
    }


def mensajes(k: dict) -> list[dict]:
    r = f"INAH 2025: Tulum {k['tulum']:,} visitantes; Ruta {k['ruta']:,} ({k['veces_ruta']} veces menos)"
    return [
        {"persona": "vuelve", "canal": "Google (búsqueda)", "idioma": "es", "lugar": "Ruta arqueológica del sur",
         "titulos": ["Pirámides mayas con espacio", "Kohunlich, Dzibanché, Ichkabal", "El sur tiene espacio"],
         "descripcion": "Recorre la selva y las ruinas del sur sin multitudes. Planea tu viaje con calma.",
         "respaldo": r},
        {"persona": "vuelve", "canal": "Facebook / Instagram", "idioma": "es", "lugar": "Bahía Calderitas–Oxtankah",
         "titulo": "La bahía que te esperaba", "foto": "fotos/lugares/bahia_calderitasoxtankah_3.jpg",
         "texto": "Mariscos frente al mar, una ciudad maya en la orilla y una tarde tranquila. Es nuestro sur.",
         "respaldo": f"Oxtankah recibió {k['bahia']:,} visitantes en 2025 (INAH), {k['pct_nac_bahia']} % mexicanos"},
        {"persona": "vuelve", "canal": "WhatsApp (orgánico)", "idioma": "es", "lugar": "Chetumal",
         "texto": "¿Y si este puente nos vamos al sur? Chetumal, la bahía y las pirámides, con espacio. Mira el plan →",
         "respaldo": f"{ENDUTIH['mensajeria_pct'][0]} % usa mensajería en el teléfono (ENDUTIH 2025, {ENDUTIH['mensajeria_pct'][1]}); sin costo"},
        {"persona": "baja", "canal": "Google (búsqueda)", "idioma": "en", "lugar": "Ruta arqueológica del sur",
         "titulos": ["Mayan pyramids, with room", "The south has room", "Take the Tren Maya south"],
         "descripcion": "Cancún is busy. Southern Quintana Roo has jungle ruins, a calm bay and room for you.",
         "respaldo": f"{r}; Cancún en temporada alta nov–abr (planeador)"},
        {"persona": "baja", "canal": "Facebook / Instagram", "idioma": "en", "lugar": "Ruta arqueológica del sur",
         "titulo": "Your Caribbean trip, one stop south", "foto": "fotos/lugares/ruta_arqueologica_del_sur_2.jpg",
         "texto": "Pyramids in the jungle, few crowds and real southern food. Take the Tren Maya to Chetumal.",
         "respaldo": "Tren Maya con estación en Chetumal (SITUR-Q, descensos por estación); solo se muestra si la Torre "
                     "marca norte lleno y el sur con espacio (regla de la Fase 7)"},
    ]


def revisar_largos(m: list[dict]) -> list[str]:
    errores = []
    for x in m:
        if x["canal"].startswith("Google"):
            errores += [f"título largo: {t}" for t in x["titulos"] if len(t) > LIMITES["google_titulo"]]
            if len(x["descripcion"]) > LIMITES["google_descripcion"]:
                errores.append(f"descripción larga: {x['descripcion']}")
        elif x["canal"].startswith("Facebook"):
            if len(x["titulo"]) > LIMITES["meta_titulo"] or len(x["texto"]) > LIMITES["meta_texto"]:
                errores.append(f"anuncio largo: {x['titulo']}")
    return errores


def medios(k: dict) -> list[dict]:
    pr = pd.read_parquet(GOLD / "presupuesto_plan.parquet").groupby("canal").pesos.sum()
    tot = pr.sum()
    return [
        {"medio": "Facebook / Instagram (pagado)", "pct": round(pr["Facebook"] / tot * 100), "por_que":
         f"Rinde 6.61 visitantes por cada $1,000 (clic de $0.51 USD, WordStream 2025) y {ENDUTIH['redes_sociales_pct'][0]} % usa redes (ENDUTIH 2025). Tope de 70 % para no depender de una plataforma."},
        {"medio": "Google, búsqueda (pagado)", "pct": round(pr["Google"] / tot * 100), "por_que":
         "Llega a quien ya busca viajar (conversión medida de 5.75 % en Travel). Es el canal de la persona que baja del norte."},
        {"medio": "WhatsApp y compartir (orgánico)", "pct": 0, "por_que":
         f"{ENDUTIH['mensajeria_pct'][0]} % usa mensajería: el botón de compartir de la página no cuesta y viaja entre familia y amigos."},
        {"medio": "La página web (destino de todos los anuncios)", "pct": 0, "por_que":
         "Planeador por lugar y mes en 9 idiomas, sin internet externo; recomienda otro lugar del sur si el elegido está lleno."},
    ]


def calendario() -> list[dict]:
    plan = pd.read_parquet(GOLD / "presupuesto_plan.parquet")
    cal = pd.read_parquet(GOLD / "pronostico_calendario.parquet")
    alta_cancun = set(cal[(cal.lugar == "Cancún") & (cal.nivel == "alta")].periodo)
    filas = []
    for p, g in plan.groupby("periodo"):
        lug = g.groupby("lugar").pesos.sum()
        filas.append({"mes": f"{pd.Timestamp(p):%Y-%m}", "pesos": round(float(lug.sum())),
                      "lugares": [l for l, v in lug.items() if v > 0.5],
                      "personas": ([] if lug.sum() < 0.5 else ["vuelve"] + (["baja"] if p in alta_cancun else []))})
    return filas


def kpis(k: dict) -> list[dict]:
    pz = pd.read_parquet(GOLD / "presupuesto_sensibilidad.parquet").query("caso == 'Base'").iloc[0]
    return [
        {"kpi": "Alcance", "formula": "Personas únicas que vieron un anuncio", "meta": "Se fija con el primer mes real (no hay dato previo)", "fuente": "Plataformas", "frecuencia": "Semanal"},
        {"kpi": "Interacción (CTR)", "formula": "Clics ÷ impresiones", "meta": "Google ≥ 8.73 %; Facebook ≥ 2.76 % (promedios de Travel)", "fuente": "Plataformas; WordStream 2025", "frecuencia": "Semanal"},
        {"kpi": "Conversión", "formula": "Planes de viaje o contactos ÷ clics", "meta": "≥ 5.75 % (Google Travel)", "fuente": "Página web", "frecuencia": "Semanal"},
        {"kpi": "Costo por visitante", "formula": "Pesos gastados ÷ conversiones", "meta": f"≤ ${pz.pesos_por_visitante:,.0f} (modelo de la Fase 6)", "fuente": "Plataformas + página", "frecuencia": "Mensual"},
        {"kpi": "Afluencia", "formula": "Visitantes reales − escenario probable del pronóstico", "meta": f"+{pz.visitantes_esperados:,.0f} en 9 meses, sin pasar la capacidad probada", "fuente": "INAH, SITUR-Q (Belice)", "frecuencia": "Mensual"},
        {"kpi": "Presupuesto", "formula": "Pesos gastados ÷ pesos planeados", "meta": "100 % (lo pausado se gasta después)", "fuente": "Torre en vivo", "frecuencia": "Semanal"},
        {"kpi": "Económico", "formula": "Ocupación hotelera de Chetumal", "meta": "Hueco: SITUR-Q no publica ocupación del sur desde 2025", "fuente": "—", "frecuencia": "—"},
        {"kpi": "Social", "formula": "Visitantes por cada 1,000 habitantes (Radar)", "meta": "El lugar sigue \"tranquilo\" o \"concurrido\", nunca \"saturado\"", "fuente": "Radar, Fase 4", "frecuencia": "Mensual"},
        {"kpi": "Ambiental", "formula": "Semanas con anuncio en temporada alta o con mal clima", "meta": "0 (la Torre las pausa)", "fuente": "Torre en vivo, Fase 7", "frecuencia": "Semanal"},
        {"kpi": "Capacidad", "formula": "(Esperados + campaña) ÷ capacidad probada", "meta": "≤ 40 % en los meses con anuncio (Pareto, Fase 6)", "fuente": "Pronóstico + presupuesto", "frecuencia": "Mensual"},
    ]


def construir() -> dict:
    k = cifras()
    asp = pd.read_parquet(GOLD / "campana_aspectos.parquet")
    pal = pd.read_parquet(GOLD / "campana_palabras.parquet")
    reg = pd.read_parquet(GOLD / "campana_reglas.parquet")
    m = mensajes(k)
    errores = revisar_largos(m)
    if errores:
        raise ValueError(f"Anuncios fuera de los límites de la plataforma: {errores}")
    q = asp[asp.pueblo == "Quintana Roo (3 pueblos)"].sort_values("riesgo_relativo", ascending=False)
    c = {"cifras": k, "personas": personas(k, asp), "marca": marca(k), "mensajes": m, "medios": medios(k),
         "calendario": calendario(), "kpis": kpis(k),
         "texto": {"aspectos": q[["aspecto", "pct_menciona", "riesgo_relativo"]].round(2).to_dict("records"),
                   "palabras_cinco": pal[pal.lado.str.contains("5")].palabra.head(12).tolist(),
                   "palabras_malas": pal[pal.lado.str.contains("1–2")].palabra.head(12).tolist(),
                   "reglas_malas": reg[reg.entonces.str.contains("mala")].head(5).round(3).to_dict("records")},
         "endutih": {k2: v[0] for k2, v in ENDUTIH.items()}}
    SALIDA.write_text(json.dumps(c, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(f"Campaña \"{c['marca']['nombre']}\": {len(c['personas'])} personas, {len(m)} mensajes (largos OK), "
          f"{len(c['calendario'])} meses, {len(c['kpis'])} KPI → {SALIDA.relative_to(RAIZ)}")
    for p in c["personas"]:
        print(f"  {p['nombre']}: " + "; ".join(f"{a} [{t}]" for a, _, t, _ in p["atributos"]))
    return c


if __name__ == "__main__":
    construir()
