# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Toma de los datos limpios (Silver) las cifras que muestra la página web y las escribe en
#                    frontend/datos/pagina.js. Arma una "ficha" por cada una de las 5 regiones (para comer, para dormir,
#                    cuánta gente vive ahí, cuántos llegaron en tren, visitantes a sus zonas arqueológicas) y la
#                    referencia del norte. Cada cifra viaja con su fuente y su periodo ("¿Cómo lo sabemos?").
# Por qué así:       - La página es para público no técnico: se entregan cifras que se leen en palabras de todos los
#                      días. Los negocios se cuentan por localidad de cada región (misma lista que el Censo,
#                      REGION_LOCALIDADES), no por municipio, igual que la población (decisión de Brandon, 28-sep-2026).
#                    - Regla de oro 9: la portada y las fichas solo hablan de las 5 regiones. Cancún y Riviera Maya
#                      aparecen únicamente en la sección "¿Por qué el sur?", etiquetadas como referencia.
#                    - Un .js generado permite abrir la página con doble clic y sin internet hasta que exista el
#                      backend FastAPI (Fase 9). Alternativa descartada: escribir cifras a mano (regla de oro 2).
#                    - Si una región no tiene un dato, la ficha lo dice ("sin dato"); no se rellena (regla de oro 1).
# Datos de entrada:  datos/silver/{siturq, datatur_ocupacion, denue, inah, iter} y datos/bronze/geo (polígonos).
# Alimenta a:        La página (portada, "Conoce los 5 lugares", "¿Por qué el sur?").

import json
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from torre.base.silver_iter import REGION_LOCALIDADES
from torre.campana.aportes import preparar as preparar_aportes
from torre.campana.vitrina import vitrina

RAIZ = Path(__file__).resolve().parents[3]
SILVER = RAIZ / "datos" / "silver"
BRONZE = RAIZ / "datos" / "bronze"
SALIDA = RAIZ / "frontend" / "datos" / "pagina.js"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
         "noviembre", "diciembre"]

# Lo que no son cifras: descripción corta y la advertencia de cada región, tomadas de docs/regiones/REGIONES.md (D.5).
# El orden es el de la ruta: de la ciudad hacia el interior.
REGIONES = [
    {"clave": "Chetumal", "nombre": "Chetumal", "icono": "ciudad", "corto": "Capital frente a la bahía",
     "que_es": "La capital del estado, frente a la bahía, con el Museo de la Cultura Maya.",
     "cuidado": "Se vigila el sargazo que apareció en los canales de entrada de la bahía (septiembre de 2026).",
     "siturq": "Chetumal"},
    {"clave": "Bahía Calderitas–Oxtankah", "nombre": "Calderitas y Oxtankah", "icono": "pescado", "corto": "Mariscos y una ciudad maya junto al mar",
     "que_es": "Pueblo de pescadores junto a la bahía y la zona arqueológica de Oxtankah, casi siempre sin filas.",
     "cuidado": "Comparte con Chetumal la vigilancia del sargazo en la bahía.",
     "inah": ["Z.A. de Oxtankah"]},
    {"clave": "Ruta arqueológica del sur", "nombre": "Ruta de las pirámides", "icono": "piramide", "corto": "Tres ciudades mayas en la selva",
     "que_es": "Kohunlich, Dzibanché e Ichkabal: tres ciudades mayas en la selva, lejos del mar.",
     "cuidado": "Los poblados cercanos casi no tienen hoteles: la visita se hace desde Chetumal.",
     "inah": ["Z.A. de Kohunlich", "Z.A. de Dzibanché-Kinichná", "Z.A de Ichkabal"]},
    {"clave": "Maya Ka'an + Kantemó", "nombre": "Maya Ka'an", "icono": "casa", "corto": "Pueblos mayas y la cueva de Kantemó",
     "que_es": "Pueblos mayas con turismo comunitario y la cueva de Kantemó.",
     "cuidado": "Hay pocos cuartos de hotel: la campaña pone un límite de visitantes para no rebasar a los pueblos.",
     "siturq": "Maya Ka'an"},
    {"clave": "Laguna Milagros–Xul-Ha", "nombre": "Laguna Milagros y Xul-Ha", "icono": "ola", "corto": "Una laguna tranquila y sus pueblos",
     "que_es": "Una laguna del mismo sistema que Bacalar, con pueblos a la orilla.",
     "cuidado": "La laguna es frágil: visitas con límite estricto y sin actividades que la dañen.",
     "sin_estadistica": True},
]


def _cifra(valor, fuente: str, periodo: str) -> dict:
    return {"valor": valor, "fuente": fuente, "periodo": periodo}


def _mes(d: date) -> str:
    return f"{MESES[d.month - 1]} de {d.year}"


def _rango_semana(lunes: date) -> str:
    domingo = lunes + timedelta(days=6)
    if lunes.month == domingo.month:
        return f"{lunes.day} al {domingo.day} de {MESES[lunes.month - 1]} de {lunes.year}"
    return f"{lunes.day} de {MESES[lunes.month - 1]} al {domingo.day} de {MESES[domingo.month - 1]} de {domingo.year}"


def _siturq(indicador: str, unidad: str) -> tuple[float, date] | None:
    """Último valor publicado (no hueco) de un indicador de SITUR-Q para una unidad; None si no hay."""
    s = pd.read_parquet(SILVER / "siturq")
    s = s[(s.indicador.astype(str) == indicador) & (s.unidad == unidad) & ~s.hueco_flag]
    if s.empty:
        return None
    fila = s.sort_values("periodo").iloc[-1]
    return float(fila.valor), date.fromisoformat(str(fila.periodo)[:10])


def _negocios_por_region() -> dict:
    """Negocios turísticos del DENUE en las localidades de cada región, por giro."""
    d = pd.read_parquet(SILVER / "denue", filters=[("cve_ent", "=", 23)],
                        columns=["cve_mun", "cve_loc", "categoria_turistica", "es_turistico"])
    d = d[d.es_turistico]
    salida = {}
    for region, localidades in REGION_LOCALIDADES.items():
        m = pd.Series(False, index=d.index)
        for mun, loc, _ in localidades:
            m |= (d.cve_mun == mun) & (d.cve_loc == loc)
        salida[region] = d[m].categoria_turistica.value_counts().to_dict()
    return salida


def fichas_regiones() -> list[dict]:
    from torre.base.ingesta_abiertas import PUNTOS_CLIMA

    censo = pd.read_parquet(SILVER / "iter")
    inah = pd.read_parquet(SILVER / "inah")
    inah = inah[inah.es_qroo]
    inah["anio"] = inah.anio.astype(int)
    ultimo_anio = int(inah.anio.max())
    ultimo_mes = int(inah[inah.anio == ultimo_anio].mes.max())
    negocios = _negocios_por_region()
    f_denue = "INEGI, directorio de negocios (DENUE)"
    fichas = []
    for i, r in enumerate(REGIONES, start=1):
        pob = censo[censo.region_campana == r["clave"]]
        giros = negocios[r["clave"]]
        ficha = {
            "numero": i, "nombre": r["nombre"], "icono": r["icono"], "corto": r["corto"], "que_es": r["que_es"],
            "cuidado": r["cuidado"],
            "viven": _cifra(int(pob.poblacion.sum()), "INEGI, Censo de Población 2020", "2020"),
            "para_comer": _cifra(int(giros.get("Alimentos y bebidas", 0)), f_denue, "directorio vigente"),
            "para_dormir": _cifra(int(giros.get("Alojamiento", 0)), f_denue, "directorio vigente"),
            "localidades": ", ".join(pob.localidad),
            "sin_estadistica": r.get("sin_estadistica", False),
        }
        # Punto del mapa: la primera localidad de la región (Censo 2020); la ruta se ubica en Kohunlich.
        principal = pob.iloc[0]
        ficha["lat"], ficha["lon"] = round(float(principal.latitud), 4), round(float(principal.longitud), 4)
        if r["clave"] == "Ruta arqueológica del sur":
            ficha["lat"], ficha["lon"] = PUNTOS_CLIMA["kohunlich"]
        if "siturq" in r:
            tren = _siturq("tren_maya_descenso", r["siturq"])
            cuartos = _siturq("habitaciones", r["siturq"])
            if tren:
                ficha["llegaron_en_tren"] = _cifra(int(tren[0]), "Sistema de información turística de Quintana Roo (Tren Maya)", _mes(tren[1]))
            if cuartos:
                ficha["cuartos_de_hotel"] = _cifra(int(cuartos[0]), "Sistema de información turística de Quintana Roo", _mes(cuartos[1]))
        if "inah" in r:
            z = inah[inah.nombre.isin(r["inah"])]
            ficha["visitantes_zonas"] = _cifra(int(z[z.anio == 2025].visitantes.sum()),
                                               "Instituto Nacional de Antropología e Historia (INAH)", "2025")
            antes = z[(z.anio == ultimo_anio - 1) & (z.mes <= ultimo_mes)].visitantes.sum()
            ahora = z[(z.anio == ultimo_anio) & (z.mes <= ultimo_mes)].visitantes.sum()
            ficha["cambio_visitantes_pct"] = _cifra(round((ahora / antes - 1) * 100, 1),
                                                    "Instituto Nacional de Antropología e Historia (INAH)",
                                                    f"enero a {MESES[ultimo_mes - 1]} de {ultimo_anio} contra el mismo periodo de {ultimo_anio - 1}")
        fichas.append(ficha)
    # Foto de referencia de cada lugar (backend/torre/base/ingesta_fotos.py). Si no hay foto, la ficha va sin foto.
    creditos = RAIZ / "frontend" / "fotos" / "creditos.json"
    if creditos.exists():
        fotos = {c["region"]: c for c in json.loads(creditos.read_text(encoding="utf-8"))}
        for ficha in fichas:
            c = fotos.get(ficha["nombre"])
            if c:
                ficha["foto"] = {k: c[k] for k in ("archivo_local", "muestra", "autor", "licencia", "url_licencia", "url_original")}
    return fichas


# ---------- Lugares de la parte del viajero (decisión 17, 02-oct-2026) ----------
# Brandon: "esos dos como no tenemos datos cámbialos por Cancún y Riviera Maya" — en toda la parte del viajero (portada,
# Qué hacer, Vive el sur, Los lugares, postales, preguntas). "Los datos" (Radar, problema) conserva el análisis de las 5
# regiones originales. Cancún y Riviera Maya van como REFERENCIA etiquetada: la campaña no los promueve y, si su mes está
# lleno, la página recomienda el sur.
VIAJERO_SUR = ["Chetumal", "Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur"]
VIAJERO_NORTE = [
    {"clave": "Cancún", "nombre": "Cancún", "icono": "ola", "corto": "Referencia: la ciudad del Caribe más visitada",
     "que_es": "La ciudad más visitada del Caribe mexicano: la zona hotelera, la laguna Nichupté y zonas mayas dentro de la ciudad.",
     "cuidado": "Referencia: la campaña no lo promueve. Tiene sargazo en 2026 y está en temporada alta de noviembre a abril.",
     "localidad": "Cancún (referencia)", "siturq": "Cancún",
     "inah": ["Z.A. de El Meco", "Z.A. de El Rey", "Museo Maya de Cancún con Z. A"]},
    {"clave": "Riviera Maya", "nombre": "Riviera Maya", "icono": "ola", "corto": "Referencia: Playa del Carmen y su Quinta Avenida",
     "que_es": "Playa del Carmen, el centro de la Riviera Maya: la Quinta Avenida, el parque Fundadores y la playa del pueblo.",
     "cuidado": "Referencia: la campaña no la promueve. Tiene sargazo en 2026; su ocupación bajó y se llena en noviembre y diciembre.",
     "localidad": "Playa del Carmen (referencia)", "siturq": "Riviera Maya"},
]


def fichas_viajero(fichas: list[dict]) -> list[dict]:
    """Los 5 lugares de la parte del viajero: los 3 del sur con serie (sus fichas de siempre) y Cancún y Riviera Maya."""
    from torre.campana.estrellas import estrellas
    from torre.campana.lugares import centros

    sur = {r["clave"]: f for r, f in zip(REGIONES, fichas)}
    salida = [{**sur[c], "clave": c, "referencia": False} for c in VIAJERO_SUR]
    censo = pd.read_parquet(SILVER / "iter")
    inah = pd.read_parquet(SILVER / "inah")
    inah = inah[inah.es_qroo]
    inah["anio"] = inah.anio.astype(int)
    negocios, est, cen = _negocios_por_region(), estrellas(), centros()
    f_denue = "INEGI, directorio de negocios (DENUE)"
    rf = RAIZ / "frontend" / "fotos" / "lugares" / "creditos.json"
    fotos = json.loads(rf.read_text(encoding="utf-8")) if rf.exists() else []
    for r in VIAJERO_NORTE:
        pob = censo[censo.region_campana == r["localidad"]]
        giros = negocios[r["localidad"]]
        f = {"clave": r["clave"], "nombre": r["nombre"], "icono": r["icono"], "corto": r["corto"], "que_es": r["que_es"],
             "cuidado": r["cuidado"], "referencia": True,
             "viven": _cifra(int(pob.poblacion.sum()), "INEGI, Censo de Población 2020", "2020"),
             "para_comer": _cifra(int(giros.get("Alimentos y bebidas", 0)), f_denue, "directorio vigente"),
             "para_dormir": _cifra(int(giros.get("Alojamiento", 0)), f_denue, "directorio vigente"),
             "localidades": ", ".join(pob.localidad), "sin_estadistica": False,
             "estrellas": est[r["clave"]]}
        f["lat"], f["lon"] = (round(v, 4) for v in cen[r["clave"]])
        cuartos = _siturq("habitaciones", r["siturq"])
        if cuartos:
            f["cuartos_de_hotel"] = _cifra(int(cuartos[0]), "Sistema de información turística de Quintana Roo", _mes(cuartos[1]))
        if "inah" in r:
            z = inah[inah.nombre.isin(r["inah"])]
            f["visitantes_zonas"] = _cifra(int(z[z.anio == 2025].visitantes.sum()),
                                           "Instituto Nacional de Antropología e Historia (INAH)", "2025")
        foto = next((x for x in fotos if x["lugar"] == r["clave"] and x.get("tipo", "lugar") == "lugar"), None)
        if foto:
            f["foto"] = {"archivo_local": foto["archivo"], **{k: foto[k] for k in ("muestra", "autor", "licencia", "url_licencia",
                                                                                   "url_original")}}
        salida.append(f)
    for i, f in enumerate(salida, start=1):
        f["numero"] = i
    return salida


def cuartos_vacios_chetumal() -> dict:
    """Parte de las noches de cuarto que quedaron vacías en Chetumal en el último año completo con dato oficial.

    O = Σ cuartos ocupados / Σ cuartos disponibles (ECUACIONES.md, A1: nunca se promedian porcentajes).
    Se usa el último año con los 12 meses publicados; en SITUR-Q es 2024 (2025 viene vacío = hueco).
    """
    s = pd.read_parquet(SILVER / "siturq")
    o = s[(s.indicador.astype(str) == "ocupacion_hotelera") & (s.unidad == "Chetumal") & ~s.hueco_flag]
    p = o.pivot_table(index=["anio", "mes"], columns="variable", values="valor").reset_index()
    completos = p.groupby("anio").mes.nunique()
    anio = int(completos[completos == 12].index.max())
    a = p[p.anio == anio]
    ocupacion = a.total_de_habitaciones_ocupadas.sum() / a.numero_de_habitaciones_disponibles.sum()
    return {"vacios_de_cada_10": round((1 - ocupacion) * 10), "ocupacion_pct": round(ocupacion * 100, 1),
            "noches_ocupadas": int(a.total_de_habitaciones_ocupadas.sum()),
            "noches_disponibles": int(a.numero_de_habitaciones_disponibles.sum()), "anio": anio,
            "fuente": "Sistema de información turística de Quintana Roo (ocupación hotelera)"}


def mapa_municipios(decimales: int = 3) -> dict:
    """Polígonos de los 11 municipios, redondeados a 3 decimales (unos 100 m) para que la página cargue rápido."""
    ruta = sorted(BRONZE.glob("geo/*/quintana_roo.json"))[-1]
    geo = json.loads(ruta.read_text(encoding="utf-8"))
    salida = []
    for f in geo["features"]:
        poligonos = f["geometry"]["coordinates"] if f["geometry"]["type"] == "MultiPolygon" else [f["geometry"]["coordinates"]]
        anillos = []
        for poligono in poligonos:
            anillo, previo = [], None
            for lon, lat in poligono[0]:  # solo el contorno exterior
                punto = (round(lon, decimales), round(lat, decimales))
                if punto != previo:
                    anillo.append(punto)
                previo = punto
            if len(anillo) > 3:
                anillos.append(anillo)
        salida.append({"cve_mun": f["properties"]["CVE_MUN"], "nombre": f["properties"]["NOM_MUN"], "anillos": anillos})
    return {"municipios": salida}


def referencia_norte() -> dict:
    """REFERENCIA (no se promueve): ocupación hotelera semanal de Cancún y Riviera Maya, 2022–2026. Es la única
    ocupación medida en 2025–2026; sirve para explicar por qué la campaña lleva gente al sur."""
    d = pd.read_parquet(SILVER / "datatur_ocupacion")
    d = d[(d.frecuencia == "semanal") & d.es_qroo & (d.tipo_fila == "centro") & d.centro.isin(["Cancun", "Riviera Maya"])].copy()
    d["periodo"] = pd.to_datetime(d.periodo).dt.date
    semanas = sorted(d.periodo.unique())
    series = {}
    for centro, g in d.groupby("centro"):
        g = g.set_index("periodo").ocupacion_pct.reindex(semanas)
        series["Cancún" if centro == "Cancun" else centro] = [None if pd.isna(v) else round(float(v), 1) for v in g]
    cancun = [v for v in series["Cancún"] if v is not None]
    return {"semanas": [s.isoformat() for s in semanas], "centros": series,
            "maximo_cancun": max(cancun), "fuente": "Secretaría de Turismo (DataTur), ocupación hotelera semanal",
            "ultima_semana": _rango_semana(semanas[-1])}


def _foto_portada() -> dict | None:
    """Foto de la portada con su crédito (frontend/fotos/creditos.json, ingesta_fotos.py)."""
    ruta = RAIZ / "frontend" / "fotos" / "creditos.json"
    if not ruta.exists():
        return None
    c = next((c for c in json.loads(ruta.read_text(encoding="utf-8")) if c["region"] == "Portada"), None)
    return {k: c[k] for k in ("archivo_local", "muestra", "autor", "licencia", "url_licencia", "url_original")} if c else None


def criterios() -> list[dict] | None:
    """Tabla de criterios de la Fase 3 (datos/gold/criterios_regiones.parquet), para la pestaña "Evidencia"."""
    ruta = RAIZ / "datos" / "gold" / "criterios_regiones.parquet"
    if not ruta.exists():
        return None
    t = pd.read_parquet(ruta)
    columnas = ["region", "papel", "c1_sargazo", "c2_pasa", "c2_meses_abierta_min", "c3_ocupacion_2024_pct",
                "c3_visitantes_inah_por_residente", "c3_negocios_turisticos_por_mil"]
    return json.loads(t[columnas].to_json(orient="records", force_ascii=False))


def resumen_datos() -> dict:
    """Cuántos archivos y registros oficiales se reunieron en la Fase 1 (manifiesto de Bronze)."""
    m = pd.read_csv(BRONZE / "MANIFIESTO.csv")
    m["filas"] = pd.to_numeric(m.filas, errors="coerce")
    datos = m[m.fuente != "Evidencia sargazo"]
    fase1 = datos[~datos.fuente.str.startswith("D13")]
    return {"archivos": int(len(fase1)), "registros": int(fase1.filas.sum()), "fuente": "Manifiesto de datos crudos (Fase 1)"}


# Las 12 fases del plan (docs/plan/HOJA_DE_RUTA.md): nombre, estado, qué entrega y a qué sección de la página lleva
# cuando ya tiene resultado. El resultado de cada fase se calcula en fases_del_proyecto() con datos reales; una fase
# pendiente no tiene resultado (la página dice "se llena en esta fase").
AVANCE = [
    ("0", "Preparar la computadora", "lista", "La computadora lista para procesar millones de datos.", None),
    ("1", "Reunir los datos oficiales", "lista", "Todos los datos oficiales descargados y verificados.", "#evidencia"),
    ("2", "Limpiar y ordenar los datos", "lista", "Los datos limpios, en tablas ordenadas.", "#evidencia"),
    ("3", "Elegir y medir los 5 lugares", "lista", "Los cinco lugares elegidos y medidos con datos.", "#lugares"),
    ("4", "Semáforo de cada lugar", "lista", "Cada lugar marcado como tranquilo, concurrido o saturado, mes a mes, con el estado esperado del mes siguiente.", "#radar"),
    ("5", "Mejor mes para ir y escenarios", "lista", "Un calendario de 12 meses con escenarios malo, probable y bueno.", "#planea"),
    ("6", "Repartir el presupuesto", "lista", "El dinero de la campaña repartido sin rebasar la capacidad de nadie.", "#presupuesto"),
    ("7", "Torre en vivo", "lista", "La torre que vigila cada semana y pausa anuncios si un lugar se llena.", "#envivo"),
    ("8", "La campaña", "lista", "A quién le hablamos, con qué mensajes y en qué canales.", "#campana"),
    ("9", "Conectar la página con los modelos", "pendiente", "La página calculando en vivo con los modelos.", None),
    ("10", "Página final", "pendiente", "La página final, probada con personas reales.", None),
    ("11", "Cierre y coloquio", "pendiente", "El documento final y la presentación ante el jurado.", None),
]


def fases_del_proyecto() -> list[dict]:
    """Las 12 fases con su resultado real cuando ya existe (cifras de los datos, no escritas a mano)."""
    import pyarrow.dataset as ds

    from torre.radar.planteamiento import concentracion

    r = resumen_datos()
    negocios = ds.dataset(SILVER / "denue", format="parquet", partitioning="hive").count_rows()
    resenas = ds.dataset(SILVER / "restmex", format="parquet", partitioning="hive").count_rows()
    c = concentracion().set_index("dimension").cuota_5_lugares_pct
    resultado = {
        "0": "PySpark 3.5.6 y Java 17 funcionando en la computadora del proyecto.",
        "1": f"{r['registros']:,} registros oficiales en {r['archivos']} archivos.",
        "2": f"Las 14 fuentes limpias, con {negocios:,} negocios y {resenas:,} reseñas, en un almacén de consulta rápida "
             f"con su diccionario de datos.",
        "3": f"Los 5 lugares pasan los criterios. Ahí vive el {c['Población']:.1f} % de la gente del estado, pero llega el "
             f"{c['Llegadas en avión']:.1f} % de los pasajeros de avión.",
    }
    rd = radar()
    if rd:
        tranquilos = sum(l["estado"] == "tranquilo" for l in rd["lugares"])
        m = rd["modelo"]
        resultado["4"] = (f"En {rd['mes']}, {tranquilos} de los 5 lugares están tranquilos. El modelo acierta {m['aciertos']} "
                          f"de {m['casos']} meses que nunca vio.")
    pr = pronostico_resumen()
    if pr:
        resultado["5"] = (f"Las zonas del sur se llenan en diciembre y enero y se vacían en septiembre. Agosto tiene "
                          f"{pr['prob_agosto']:.1f} % de probabilidad de tormenta. El rango del pronóstico se cumple entre "
                          f"{pr['cobertura_min']:.0f} y {pr['cobertura_max']:.0f} de cada 100 veces.")
    pz = presupuesto_pagina()
    if pz:
        resultado["6"] = (f"Con ${pz['presupuesto_anual']:,.0f} al año, unos {pz['visitantes']:,} visitantes más al sur en "
                          f"{pz['n_meses']} meses (${pz['pesos_por_visitante']} cada uno), sin anunciar en temporada alta "
                          f"y sin rebasar la capacidad de nadie.")
    ev7 = envivo_pagina()
    if ev7:
        resultado["7"] = (f"{len(ev7['semanas'])} semanas reales reproducidas: el anuncio se pausó "
                          f"{sum(ev7['pausas'].values())} veces por mal clima, tormentas o exceso de gente, y "
                          f"\"¿Ibas al norte?\" se encendió {ev7['ibas_al_norte']} semanas.")
    cp = campana_pagina()
    if cp:
        resultado["8"] = (f"\"{cp['marca']['nombre']}\": {len(cp['personas'])} viajeras ideales con datos, "
                          f"{len(cp['mensajes'])} anuncios con su dato de respaldo y {len(cp['kpis'])} indicadores que vigila la Torre.")
    return [{"fase": f, "nombre": n, "estado": e, "entrega": entrega, "enlace": enlace, "resultado": resultado.get(f)}
            for f, n, e, entrega, enlace in AVANCE]


def pronostico_resumen() -> dict | None:
    """Cifras de la Fase 5 para la tarjeta de avance (salidas de torre.pronostico en Gold). None si aún no existen."""
    ruta_p, ruta_e = GOLD / "pronostico_poisson_tormentas.parquet", GOLD / "pronostico_eleccion.parquet"
    if not (ruta_p.exists() and ruta_e.exists()):
        return None
    p = pd.read_parquet(ruta_p).set_index("mes")
    e = pd.read_parquet(ruta_e)
    sur = e[e.elegido_flag & ~e.serie.str.startswith("Cancún")]
    return {"prob_agosto": float(p.loc[8, "prob_tormenta"] * 100), "cobertura_min": float(sur.cobertura_pct.min()),
            "cobertura_max": float(sur.cobertura_pct.max())}


# ---------- ¿Cómo se mueve la gente por Quintana Roo? (todo el estado; el norte, como referencia) ----------
# Unidad de SITUR-Q → localidad del Censo 2020 donde se dibuja (municipio, localidad). Las zonas que suman varios
# destinos (Riviera Maya, Grand Costa Maya, Caribe Mexicano) se omiten para no contar dos veces. La unidad "Holbox" del
# Tren Maya no se dibuja: su estación no está en la isla y SITUR-Q no publica cuál es; aparece solo en la lista.
PUNTOS_SITURQ = {"Cancún": ("005", "0001"), "Cozumel": ("001", "0001"), "Chetumal": ("004", "0001"),
                 "Tulum": ("009", "0001"), "Playa del Carmen": ("008", "0001"), "Puerto Morelos": ("011", "0001"),
                 "Bacalar": ("010", "0001"), "Maya Ka'an": ("002", "0001"), "Mahahual": ("004", "0053")}
MODOS = {  # indicador de SITUR-Q, unidades que cuentan, cómo se dice en la página
    "avion": ("aereos_llegadas", ["Cancún", "Cozumel", "Chetumal", "Tulum"], "pasajeros llegaron en avión"),
    "tren": ("tren_maya_descenso", ["Cancún", "Puerto Morelos", "Playa del Carmen", "Tulum", "Maya Ka'an", "Bacalar",
                                    "Chetumal", "Holbox"], "personas bajaron del Tren Maya"),
    "crucero": ("cruceristas", ["Cozumel", "Mahahual"], "cruceristas bajaron en el puerto"),
    "frontera": ("frontera_belice", ["Chetumal"], "cruces por la frontera con Belice"),
}
RUTA_TREN = ["Cancún", "Puerto Morelos", "Playa del Carmen", "Tulum", "Maya Ka'an", "Bacalar", "Chetumal"]  # orden de la línea


def movimiento() -> dict:
    """Llegadas del último año completo de cada medio de transporte, por lugar (SITUR-Q). Sin orígenes ni destinos
    inventados. El avión llega hasta 2024: desde 2025 la fuente dejó de publicar (regla 6 de silver_siturq.py)."""
    s = pd.read_parquet(SILVER / "siturq")
    s = s[~s.hueco_flag]
    censo = pd.read_parquet(SILVER / "iter")
    coords = {}
    for unidad, (mun, loc) in PUNTOS_SITURQ.items():
        f = censo[(censo.cve_mun == mun) & (censo.cve_loc == loc)].iloc[0]
        coords[unidad] = (round(float(f.latitud), 4), round(float(f.longitud), 4))
    modos = {}
    for clave, (indicador, unidades, texto) in MODOS.items():
        x = s[(s.indicador.astype(str) == indicador) & s.unidad.isin(unidades)]
        completos = x.groupby(["unidad", "anio"]).mes.nunique()
        # último año en que TODAS las unidades con datos tienen sus 12 meses (un año a medias no se suma)
        anio = max(a for a in completos.index.get_level_values(1).unique()
                   if (completos.xs(a, level=1) == 12).all() and len(completos.xs(a, level=1)) == x.unidad.nunique())
        puntos = []
        for u in unidades:
            meses = x[(x.unidad == u) & (x.anio == anio)]
            if meses.mes.nunique() != 12:
                continue
            p = {"lugar": u, "valor": int(meses.valor.sum())}
            if u in coords:
                p["lat"], p["lon"] = coords[u]
            puntos.append(p)
        modos[clave] = {"texto": texto, "anio": int(anio), "total": sum(p["valor"] for p in puntos), "puntos": puntos}
    ruta = [{"lugar": u, "lat": coords[u][0], "lon": coords[u][1]} for u in RUTA_TREN]
    return {"modos": modos, "ruta_tren": ruta, "fuente": "Sistema de información turística de Quintana Roo (SITUR-Q)"}


# ---------- ¿Dónde se queda el dinero? Lo que sí se mide: cuartos, hoteles y tamaño de los negocios ----------
ZONAS_SITURQ = {"Caribe Mexicano", "Riviera Maya", "Grand Costa Maya"}  # suman varios destinos: se omiten
UNIDADES_DE_LOS_LUGARES = {"Chetumal", "Maya Ka'an"}


def hospedaje() -> dict:
    s = pd.read_parquet(SILVER / "siturq")
    s = s[~s.hueco_flag & s.indicador.astype(str).isin(["habitaciones", "centros_hospedaje"]) & ~s.unidad.isin(ZONAS_SITURQ)]
    ultimo = s.periodo.max()
    u = s[s.periodo == ultimo].pivot_table(index="unidad", columns="indicador", values="valor", aggfunc="sum", observed=True)
    destinos = [{"lugar": k, "cuartos": int(f.habitaciones), "hoteles": int(f.centros_hospedaje),
                 "cuartos_por_hotel": round(f.habitaciones / f.centros_hospedaje, 1),
                 "es_de_los_lugares": k in UNIDADES_DE_LOS_LUGARES} for k, f in u.iterrows()]
    destinos.sort(key=lambda d: -d["cuartos"])
    mes = date.fromisoformat(str(ultimo)[:10])

    # Tamaño de los negocios de hospedaje (INEGI, personas que trabajan en cada uno).
    d = pd.read_parquet(SILVER / "denue", filters=[("cve_ent", "=", 23)], columns=["cve_mun", "categoria_turistica", "per_ocu"])
    a = d[d.categoria_turistica == "Alojamiento"]
    clase = a.per_ocu.map({"0 a 5 personas": "chicos", "6 a 10 personas": "chicos", "11 a 30 personas": "medianos",
                           "31 a 50 personas": "medianos", "51 a 100 personas": "medianos", "101 a 250 personas": "grandes",
                           "251 y más personas": "grandes"})
    def reparto(filtro):
        c = clase[filtro].value_counts()
        return {k: int(c.get(k, 0)) for k in ("chicos", "medianos", "grandes")}
    sur = a.cve_mun.isin(["002", "004", "006"])  # municipios de los 5 lugares
    return {"mes": _mes(mes), "destinos": destinos,
            "tamano_negocios": {"estado": reparto(pd.Series(True, index=a.index)), "municipios_de_los_lugares": reparto(sur),
                                "resto_del_estado": reparto(~sur)},
            "fuente_cuartos": "Sistema de información turística de Quintana Roo (SITUR-Q)",
            "fuente_negocios": "INEGI, directorio de negocios (DENUE): personas que trabajan en cada hospedaje",
            "hueco_derrama": "SITUR-Q publica una serie de derrama económica por destino hasta marzo de 2024, pero no dice su "
                             "unidad (pesos o dólares) y el total estatal es menor que el de Cancún. Por eso no se muestra."}


# ---------- Radar (Fase 4): ¿dónde hay presión y dónde hay espacio? ----------
GOLD = RAIZ / "datos" / "gold"
# Regla de oro 9: el Radar de la página muestra los 5 lugares; del resto solo Cancún, Playa del Carmen (Riviera Maya) y
# Tulum, etiquetados como referencia. Mahahual, Holbox, Bacalar, Cozumel o Isla Mujeres no aparecen.
REFERENCIA_RADAR = ["Cancún", "Playa del Carmen", "Tulum"]
MEDIDAS_EN_PALABRAS = {"llegadas_tren_x1000hab": "llegadas en Tren Maya", "cruceristas_x1000hab": "cruceristas",
                       "visitantes_inah_x1000hab": "visitantes a zonas arqueológicas", "ocupacion_pct": "cuartos ocupados",
                       "llegadas_x_cuarto": "llegadas por cuarto de hotel"}


def radar() -> dict | None:
    """Estado de hoy (índice comparable), estado estimado del mes siguiente (modelo elegido) y riesgo semanal del norte
    (Markov). Si las salidas del Radar no existen todavía, la página no dibuja la sección (contrato del cascarón)."""
    rutas = {n: GOLD / f"radar_{n}.parquet" for n in ("indice_comparable", "prediccion", "modelos", "markov_riesgo")}
    if not all(r.exists() for r in rutas.values()):
        return None
    t = pd.read_parquet(rutas["indice_comparable"])
    pred = pd.read_parquet(rutas["prediccion"]).set_index("lugar")
    mod = pd.read_parquet(rutas["modelos"]).set_index("modelo")
    riesgo = pd.read_parquet(rutas["markov_riesgo"]).set_index("centro")
    mes = t.dropna(subset=["ipt_comparable"]).periodo.max()
    hoy = t[t.periodo == mes].set_index("lugar")

    def fila(lugar: str, nombre: str) -> dict:
        if lugar not in hoy.index or pd.isna(hoy.loc[lugar, "ipt_comparable"]):
            return {"clave": lugar, "nombre": nombre, "estado": "sin dato oficial", "indice": None, "medidas": None,
                    "estado_siguiente_est": None, "probabilidad_siguiente": None}
        h = hoy.loc[lugar]
        p = pred.loc[lugar] if lugar in pred.index else None
        siguiente = p.estado_mes_siguiente_est if p is not None else None
        return {"clave": lugar, "nombre": nombre, "estado": h.estado, "indice": round(float(h.ipt_comparable), 3),
                "medidas": [MEDIDAS_EN_PALABRAS[m] for m in h.medidas.split(", ")],
                "estado_siguiente_est": siguiente,
                "probabilidad_siguiente": round(float(p[f"prob_{siguiente}"]), 2) if p is not None else None}

    elegido = pred.modelo.iloc[0]  # el modelo que eligió el criterio de Brandon en prediccion.py (no se escribe a mano)
    rf, pe = mod.loc[elegido], mod.loc["Persistencia (línea base)"]
    ses = pd.read_parquet(GOLD / "radar_sesgo.parquet").set_index("grupo") if (GOLD / "radar_sesgo.parquet").exists() else None
    semana = pd.Timestamp(riesgo.semana.iloc[0])
    norte = {"Cancún": "Cancun", "Riviera Maya": "Riviera Maya"}
    return {
        "mes": _mes(mes.date()), "mes_siguiente": _mes((mes + pd.offsets.MonthBegin(1)).date()),
        "cortes": {"concurrido_desde": round(float(t.corte_p50.iloc[0]), 3), "saturado_desde": round(float(t.corte_p90.iloc[0]), 3)},
        "lugares": [fila(r["clave"], r["nombre"]) for r in REGIONES],
        "referencia": [fila(l, l) for l in REFERENCIA_RADAR],
        "modelo": {"nombre": elegido, "aciertos": int(rf.aciertos), "casos": int(rf.casos),
                   "aciertos_persistencia": int(pe.aciertos), "cambios_anticipados": int(rf.cambios_acertados),
                   "cambios_reales": int(rf.cambios_reales),
                   "cambios_en_los_5": int(ses.loc["5 lugares", "cambios_reales"]) if ses is not None else None},
        "norte_semanal": {"semana": _rango_semana(semana.date()),
                          "riesgo_saturarse": {n: [round(float(riesgo.loc[c, f"sem_{k}"]), 3) for k in range(1, 9)]
                                               for n, c in norte.items()},
                          "estado_hoy": {n: riesgo.loc[c, "estado_hoy"] for n, c in norte.items()},
                          "ocupacion_hoy_pct": {n: float(riesgo.loc[c, "ocupacion_hoy_pct"]) for n, c in norte.items()}},
        "fuente": "Cálculo del proyecto con SITUR-Q, INAH, SECTUR-DataTur y el Censo 2020 (backend/torre/radar)",
    }


# ---------- El problema en una imagen (planteamiento, Fase 3) ----------
NOMBRE_DIMENSION = {"Llegadas en avión": "de los pasajeros que llegan en avión", "Cuartos de hotel": "de los cuartos de hotel",
                    "Visitantes a sitios del INAH": "de los visitantes a zonas arqueológicas",
                    "Negocios turísticos": "de los negocios turísticos", "Población": "de la gente del estado"}


def concentracion_pagina() -> dict:
    """Qué parte del total de Quintana Roo está en los 5 lugares (planteamiento.concentracion, ECUACIONES §1-ter)."""
    from torre.radar.planteamiento import concentracion

    c = concentracion().set_index("dimension")
    orden = ["Llegadas en avión", "Cuartos de hotel", "Visitantes a sitios del INAH", "Negocios turísticos"]
    return {"poblacion_pct": round(float(c.loc["Población", "cuota_5_lugares_pct"]), 1),
            "dimensiones": [{"dimension": d, "texto": NOMBRE_DIMENSION[d], "pct": round(float(c.loc[d, "cuota_5_lugares_pct"]), 1),
                             "periodo": str(c.loc[d, "periodo"]), "fuente": str(c.loc[d, "fuente"])} for d in orden],
            "fuente": "Cálculo del proyecto con SITUR-Q, INAH e INEGI (DENUE y Censo 2020)"}


# ---------- Evidencia: cómo se probó cada resultado ----------
def _pruebas_automaticas() -> int | None:
    """Cuántas pruebas automáticas tiene el proyecto (se cuentan con pytest, no se escriben a mano)."""
    import re
    import subprocess
    import sys

    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", str(RAIZ / "tests")], cwd=RAIZ,
                           capture_output=True, text=True, timeout=300)
        m = re.search(r"(\d+) tests? collected", r.stdout)
        return int(m.group(1)) if m else None
    except Exception:
        return None


def evidencia_pagina() -> dict | None:
    rutas = {n: GOLD / f"{n}.parquet" for n in ("radar_markov_backtest", "radar_clusters_centros")}
    if not all(r.exists() for r in rutas.values()):
        return None
    bt = pd.read_parquet(rutas["radar_markov_backtest"]).set_index(["k_semanas", "metodo"]).brier
    cl = pd.read_parquet(rutas["radar_clusters_centros"])
    grupo_cancun = int(cl.loc[cl.centro == "Cancun", "grupo"].iloc[0])
    lleno = cl[cl.grupo == grupo_cancun]
    s = pd.read_parquet(SILVER / "siturq", columns=["indicador", "periodo", "hueco_flag", "unidad"])
    s["indicador"] = s.indicador.astype(str)

    def ultimo_mes(indicador, unidades=None):
        x = s[(s.indicador == indicador) & ~s.hueco_flag]
        if unidades:
            x = x[x.unidad.isin(unidades)]
        return _mes(date.fromisoformat(str(x.periodo.max())[:10]))

    return {
        "markov": [{"semanas": k, "brier_markov": round(float(bt[(k, "Markov")]), 3),
                    "brier_persistencia": round(float(bt[(k, "Persistencia")]), 3)} for k in (1, 4, 8)],
        "clustering": {"centros": int(len(cl)), "grupos": int(cl.grupo.nunique()),
                       "centros_grupo_lleno": int(len(lleno)), "nivel_grupo_lleno": round(float(lleno.nivel.mean()), 1),
                       "nivel_resto": round(float(cl[cl.grupo != grupo_cancun].nivel.mean()), 1),
                       # Solo como referencia (regla de oro 9): centros del norte que DataTur mide; nombres con acentos
                       "qroo_en_grupo_lleno": sorted({"Cancun": "Cancún", "Playa Del Carmen": "Playa del Carmen"}.get(c, c)
                                                     for c in lleno[lleno.es_qroo == True].centro)},  # noqa: E712
        "pruebas": _pruebas_automaticas(),
        "huecos": [
            f"La ocupación hotelera oficial del sur termina en {ultimo_mes('ocupacion_hotelera', ['Chetumal', 'Maya Ka' + chr(39) + 'an'])}: "
            "después la fuente publica ceros imposibles, que se guardan como dato faltante.",
            f"Las llegadas en avión terminan en {ultimo_mes('aereos_llegadas')}: desde entonces todos los aeropuertos marcan cero.",
            "La derrama económica por destino no dice si está en pesos o en dólares: no se usa.",
            "La Laguna Milagros no tiene ninguna estadística turística oficial: aparece como “sin dato oficial”.",
            "Para los mismos lugares, la Secretaría de Turismo marca menos ocupación que el gobierno estatal: el norte puede "
            "verse un poco más vacío de lo que está.",
        ],
        "auditoria": "Revisión del 29 de septiembre de 2026 (docs/decisiones/09-auditoria-fases-1-4.md)",
    }


# ---------- Quiénes somos ----------
EQUIPO = [
    {"nombre": "Brandon Uriel García Sánchez", "rol": "Responsable técnico", "hace": "Datos, modelos y esta página"},
    {"nombre": None, "rol": "Integrante del equipo", "hace": "Redacción del informe y la campaña"},
]


# ---------- Preguntas rápidas (el asistente responde con datos del proyecto; no inventa) ----------
def preguntas_rapidas(fichas: list[dict], mov: dict, hosp: dict, viajero: list[dict] | None = None) -> list[dict]:
    c = cuartos_vacios_chetumal()
    che = next(f for f in fichas if f["nombre"] == "Chetumal")
    avion_che = next((p["valor"] for p in mov["modos"]["avion"]["puntos"] if p["lugar"] == "Chetumal"), None)
    nombres = ", ".join(f["nombre"] for f in fichas[:-1]) + " y " + fichas[-1]["nombre"]
    lugares = []
    for f in (viajero or fichas):
        extra = (f"; {f['llegaron_en_tren']['valor']:,} personas llegaron en el Tren Maya en {f['llegaron_en_tren']['periodo']}"
                 if "llegaron_en_tren" in f else "")
        lugares.append({"pregunta": f"¿Qué hay en {f['nombre']}?", "claves": [f["nombre"].lower(), f["nombre"].split()[0].lower()],
                        "respuesta": f"{f['que_es']} Tiene {f['para_comer']['valor']:,} lugares para comer y {f['para_dormir']['valor']:,} "
                                     f"para dormir{extra}. " + (f"{f['cuidado']}" if f.get("referencia") else
                                     f"Cuidado: {f['cuidado'][0].lower() + f['cuidado'][1:]}"),
                        "fuente": "INEGI y gobierno de Quintana Roo"})
    por_hotel = {d["lugar"]: round(d["cuartos_por_hotel"]) for d in hosp["destinos"]}
    sur = hosp["tamano_negocios"]["municipios_de_los_lugares"]
    dinero = [
        # "hotel" también está aquí para que "¿cuánto cuesta el hotel?" sume 2 puntos y no caiga en "¿Hay espacio?".
        {"pregunta": "¿Cuánto cuesta ir?", "claves": ["cuesta", "precio", "precios", "costo", "barato", "caro", "tarifa", "hotel"],
         "respuesta": "No damos precios: ninguna fuente oficial abierta publica tarifas de hotel por lugar, y no las inventamos. "
                      f"Lo que sí sabemos es que en el sur los hoteles son chicos: {por_hotel['Chetumal']} cuartos por hotel en "
                      f"Chetumal contra {por_hotel['Cancún']} en Cancún ({hosp['mes']}).",
         "fuente": "Gobierno de Quintana Roo (SITUR-Q)"},
        {"pregunta": "¿Dónde se queda el dinero?", "claves": ["dinero", "queda", "derrama", "gana", "ganancia", "negocio", "negocios", "local"],
         "respuesta": f"En los municipios del sur que promueve la campaña no hay ningún hospedaje grande: {sur['chicos']:,} son chicos "
                      f"(hasta 10 personas) y {sur['medianos']:,} medianos. La derrama económica por destino no se muestra porque "
                      "la fuente no dice en qué unidad está.",
         "fuente": "INEGI (DENUE) y SITUR-Q"} if sur["grandes"] == 0 else
        {"pregunta": "¿Dónde se queda el dinero?", "claves": ["dinero", "queda", "derrama", "gana", "ganancia", "negocio", "negocios", "local"],
         "respuesta": f"En los municipios del sur que promueve la campaña hay {sur['chicos']:,} hospedajes chicos, {sur['medianos']:,} medianos "
                      f"y {sur['grandes']:,} grandes. La derrama económica por destino no se muestra porque la fuente no dice su unidad.",
         "fuente": "INEGI (DENUE) y SITUR-Q"},
    ]
    return [
        {"pregunta": "¿Qué lugares promueve la campaña?", "claves": ["lugares", "promueve", "donde", "dónde", "destinos", "cuales", "cuáles"],
         "respuesta": (f"El sur: {', '.join(f['nombre'] for f in (viajero or fichas) if not f.get('referencia'))}. "
                       "Cancún y la Riviera Maya aparecen como referencia, para quien pensaba ir al norte: si su mes está "
                       "lleno, te recomendamos un lugar del sur."), "fuente": "Selección de regiones del proyecto"},
        {"pregunta": "¿Por qué no Cancún o Tulum?", "claves": ["cancún", "cancun", "tulum", "norte", "riviera", "playa"],
         "respuesta": f"Tienen sargazo y se llenan: en su semana más llena, Cancún tuvo {round(D_MAX_CANCUN[0] / 10)} de cada 10 cuartos "
                      "ocupados, y en Tulum se reportaron cierres de negocios en 2026. La campaña lleva gente a donde sí hay espacio.",
         "fuente": "Secretaría de Turismo y notas verificadas de 2026"},
        {"pregunta": "¿Hay espacio en Chetumal?", "claves": ["espacio", "vacíos", "vacios", "cuartos", "hotel", "lleno"],
         "respuesta": f"Sí: en {c['anio']}, {c['vacios_de_cada_10']} de cada 10 cuartos de hotel de Chetumal se quedaron vacíos "
                      f"({c['noches_ocupadas']:,} de {c['noches_disponibles']:,} noches ocupadas).",
         "fuente": "Gobierno de Quintana Roo (SITUR-Q)"},
        {"pregunta": "¿Hay sargazo en el sur?", "claves": ["sargazo", "alga", "playa", "mar"],
         "respuesta": "En la costa de Chetumal y Calderitas no hay reporte de sargazo. Sí apareció en los canales de entrada de la "
                      "bahía (septiembre de 2026), así que se vigila. La ruta de las pirámides está "
                      "lejos del mar abierto.", "fuente": "ECOSUR y notas del 28 de septiembre de 2026"},
        {"pregunta": "¿Cómo llego al sur?", "claves": ["llego", "llegar", "tren", "avión", "avion", "camino", "transporte"],
         "respuesta": f"En {mov['modos']['avion']['anio']} llegaron {avion_che:,} pasajeros en avión a Chetumal, y el Tren Maya para en Chetumal, "
                      f"Bacalar, Cancún y Playa del Carmen. Solo en {che['llegaron_en_tren']['periodo']}, "
                      f"{che['llegaron_en_tren']['valor']:,} personas bajaron del tren en Chetumal.",
         "fuente": "Gobierno de Quintana Roo (SITUR-Q)"},
        *dinero,
        _cuando_conviene(),
        *lugares,
        {"pregunta": "¿De dónde salen los datos?", "claves": ["datos", "fuente", "fuentes", "sabemos", "oficial"],
         "respuesta": "De fuentes oficiales y abiertas: Secretaría de Turismo, gobierno de Quintana Roo, INEGI, INAH, NOAA, "
                      "Open-Meteo y la Reserva Federal. Las fotos, de Wikimedia Commons con licencia libre.",
         "fuente": "Inventario de fuentes del proyecto"},
        {"pregunta": "¿Quién hizo esto?", "claves": ["quién", "quien", "equipo", "hizo", "unrc", "escuela"],
         "respuesta": "Un equipo de estudiantes de Ciencias de Datos para Negocios de la Universidad Nacional Rosario "
                      "Castellanos (UNRC), como proyecto escolar 2026-2.", "fuente": "Torre del Caribe"},
    ]


def _cuando_conviene() -> dict:
    """Respuesta del chat con la forma del año de la Ruta (Fase 5): su mes más tranquilo y el más lleno."""
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
             "noviembre", "diciembre"]
    base = {"pregunta": "¿Cuándo conviene ir?", "claves": ["cuándo", "cuando", "mes", "fecha", "temporada"]}
    rf = GOLD / "pronostico_forma_anio.parquet"
    if not rf.exists():
        return base | {"respuesta": "Todavía no hay calendario: no damos una fecha que no esté probada con datos.",
                       "fuente": "Plan del proyecto"}
    f = pd.read_parquet(rf)
    r = f[f.lugar == "Ruta arqueológica del sur"].set_index("mes").indice
    return base | {
        "respuesta": f"Depende del lugar: arriba, en \"Planea tu viaje\", eliges lugar y mes y te decimos cómo va a estar. Por "
                     f"ejemplo, a la Ruta de las pirámides llega {round((1 - r.min()) * 100)} % menos gente que en un mes "
                     f"promedio en {meses[r.idxmin() - 1]}, y {round((r.max() - 1) * 100)} % más en {meses[r.idxmax() - 1]}.",
        "fuente": "INAH (BdINAH) y forma del año del proyecto (Fase 5)"}


D_MAX_CANCUN = [None]  # lo llena generar() con la ocupación semanal más alta de Cancún (referencia_norte)


# ---------- Planeador "¿Cuándo conviene ir?" y "Qué hacer" (Fase 5 + oferta del DENUE) ----------
MEDIDA_LUGAR = {"Chetumal": "cruces desde Belice", "Bahía Calderitas–Oxtankah": "visitantes a la zona de Oxtankah",
                "Ruta arqueológica del sur": "visitantes a Kohunlich, Dzibanché e Ichkabal",
                "Cancún": "de los cuartos de hotel ocupados", "Riviera Maya": "de los cuartos de hotel ocupados"}
# Lugares del planeador (decisión 15): los 3 del sur con serie y Cancún y Riviera Maya como referencia. Maya Ka'an y la
# Laguna Milagros no tienen serie y salieron del planeador; siguen en "Los lugares".
NORTE_PLANEADOR = [{"clave": "Cancún", "nombre": "Cancún", "icono": "ola"},
                   {"clave": "Riviera Maya", "nombre": "Riviera Maya", "icono": "ola"}]


def _negocio(f) -> dict:
    from torre.campana.lugares import enlace_maps

    # "maps" lleva a las coordenadas exactas del DENUE; "resenas" busca el negocio por nombre en Google Maps, donde la
    # persona lee sus reseñas y estrellas. La página no copia ni descarga ninguna (regla de oro 4, decisión 16).
    return {"n": f.nombre, "t": f.tipo, "km": float(f.km), "loc": f.localidad, "otro": bool(f.de_otro_lugar_flag),
            "maps": enlace_maps(f.lat, f.lon), "resenas": enlace_maps(texto=f"{f.nombre}, {f.localidad}, Quintana Roo")}


def presupuesto_pagina() -> dict | None:
    """Fase 6: reparto del presupuesto (torre.campana.presupuesto). None si sus salidas no existen todavía."""
    rutas = {n: GOLD / f"presupuesto_{n}.parquet" for n in ("plan", "reglas", "pareto", "sensibilidad", "precios_sombra")}
    if not all(r.exists() for r in rutas.values()):
        return None
    from torre.campana.presupuesto import PRESUPUESTO_ANUAL, tabla_meses
    plan = pd.read_parquet(rutas["plan"])
    sen = pd.read_parquet(rutas["sensibilidad"])
    base = sen[sen.caso == "Base"].iloc[0]
    t = tabla_meses()
    orden = ["Ruta arqueológica del sur", "Bahía Calderitas–Oxtankah", "Chetumal"]
    meses = []
    for p in sorted(plan.periodo.unique()):
        x = plan[plan.periodo == p].groupby("lugar").pesos.sum()
        alta = t[(t.periodo == p) & (t.nivel == "alta")].lugar.tolist()
        meses.append({"mes": f"{MESES[pd.Timestamp(p).month - 1][:3]} {pd.Timestamp(p).year % 100:02d}",
                      "pesos": {l: round(float(x.get(l, 0))) for l in orden}, "alta": alta})
    lug = plan.groupby("lugar").pesos.sum()
    can = plan.groupby("canal").agg(pesos=("pesos", "sum"), conv=("conversiones_est", "sum"))
    reglas = pd.read_parquet(rutas["reglas"])
    par = pd.read_parquet(rutas["pareto"]).sort_values("ocupacion_max")
    sin_perder = par[par.visitantes_esperados >= par.visitantes_esperados.max() - 1e-3].ocupacion_max.min()
    caso = lambda texto: float(sen[sen.caso.str.startswith(texto)].visitantes_esperados.iloc[0])
    return {
        "presupuesto_anual": PRESUPUESTO_ANUAL, "presupuesto_periodo": float(base.presupuesto_periodo),
        "desde": meses[0]["mes"], "hasta": meses[-1]["mes"], "n_meses": len(meses),
        "visitantes": round(float(base.visitantes_esperados)), "pesos_por_visitante": round(float(base.pesos_por_visitante)),
        "meses": meses, "orden": orden,
        "lugares": [{"nombre": l, "pesos": round(float(lug[l])), "pct": round(float(lug[l] / lug.sum() * 100), 1)} for l in orden],
        "canales": [{"nombre": c, "pct": round(float(v.pesos / can.pesos.sum() * 100)),
                     "por_mil": round(float(v.conv / v.pesos * 1000), 2)} for c, v in can.iterrows()],
        "reglas": [{"regla": r.regla, "costo_pct": round(float(r.costo_pct), 1)} for r in reglas.itertuples()],
        "sin_perder_pct": round(float(sin_perder) * 100),
        "facebook_3": round(caso("Conversión Facebook 3")), "facebook_mediana": round(caso("Conversión Facebook 6")),
        "fuente": "Modelo de dos etapas del proyecto (PuLP/CBC) · costos por clic y conversión: WordStream 2025, Travel · "
                  "dólar: FRED · escenarios y capacidad: Pronóstico (Fase 5)",
    }


def envivo_pagina() -> dict | None:
    """Fase 7: la reproducción semana a semana de la Torre (torre.envivo.torre). None si aún no corre."""
    rutas = {n: GOLD / f"envivo_{n}.parquet" for n in ("decisiones", "norte", "senales")}
    if not all(r.exists() for r in rutas.values()):
        return None
    d, nt, s = (pd.read_parquet(r) for r in rutas.values())
    letra = {"encendido": "e", "pausado": "p", "temporada alta": "a", "fuera del plan": "f"}
    orden = ["Chetumal", "Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur"]
    semanas = []
    for (sem, g), n in zip(d.groupby("semana", sort=True), nt.sort_values("semana").itertuples()):
        g = g.set_index("lugar")
        semanas.append({
            "s": f"{sem:%Y-%m-%d}", "c": round(float(n.cancun_pct), 1) if pd.notna(n.cancun_pct) else None,
            "r": round(float(n.riviera_pct), 1) if pd.notna(n.riviera_pct) else None,
            "n": n.destino, "ll": n.norte_lleno,
            "l": [letra[g.loc[l, "accion"]] for l in orden],
            "m": [g.loc[l, "motivo"] for l in orden], "t": bool(g.sin_dato_tormentas.iloc[0])})
    pausas = d[d.accion == "pausado"]
    return {
        "lugares": orden, "semanas": semanas, "desde": semanas[0]["s"], "hasta": semanas[-1]["s"],
        "lotes": int(d.lote.nunique()), "corte_saturado": round(float(s.corte_p90.iloc[0]), 1),
        "pausas": {l: int((pausas.lugar == l).sum()) for l in orden},
        "pausas_clima": int(pausas.motivo.str.contains("clima raro").sum()),
        "pausas_tormenta": int(pausas.motivo.str.contains("tormenta").sum()),
        "pausas_llegadas": int(pausas.motivo.str.contains("más gente").sum()),
        "tormentas": sorted(set(s.tormenta_nombre.dropna())),
        "ibas_al_norte": int(nt.ibas_al_norte.sum()), "norte_lleno": int(nt.norte_lleno.notna().sum()),
        "pesos_movidos": round(float(pausas.pesos_plan.sum())),
        "fuente": "DataTur (ocupación semanal), NOAA HURDAT2, Open-Meteo, INAH y SITUR-Q; reglas de la Fase 7 sobre el "
                  "plan de la Fase 6. Reproducción con Spark Structured Streaming",
    }


def campana_pagina() -> dict | None:
    """Fase 8: la campaña "El sur tiene espacio" (torre.campana.marca). None si aún no se arma."""
    ruta = GOLD / "campana.json"
    if not ruta.exists():
        return None
    c = json.loads(ruta.read_text(encoding="utf-8"))
    c["personas"] = [p | {"atributos": [{"que": a, "valor": v, "tipo": t, "fuente": f} for a, v, t, f in p["atributos"]]}
                     for p in c["personas"]]
    return c


def planeador_pagina() -> dict | None:
    """Datos del planeador: calendario por lugar y mes (torre.pronostico.calendario) y qué hacer / comer / dormir por
    momento del día (torre.campana.lugares, DENUE). None si aún no existen sus salidas en Gold."""
    from torre.campana.lugares import ZONAS_INAH, enlace_maps
    from torre.pronostico.calendario import NORTE, SUR

    rc, rr = GOLD / "pronostico_calendario.parquet", GOLD / "lugares_recomendados.parquet"
    if not (rc.exists() and rr.exists()):
        return None
    cal, rec = pd.read_parquet(rc), pd.read_parquet(rr)
    forma = pd.read_parquet(GOLD / "pronostico_forma_anio.parquet")
    nombres = {r["clave"]: r["nombre"] for r in REGIONES}
    meses = sorted(cal.periodo.unique())

    def num(v, nd=0):
        return None if v is None or pd.isna(v) else round(float(v), nd)

    # Fotos de cada lugar con coordenada comprobada en su municipio (torre.campana.fotos_lugares)
    rf = RAIZ / "frontend" / "fotos" / "lugares" / "creditos.json"
    fotos = json.loads(rf.read_text(encoding="utf-8")) if rf.exists() else []
    from torre.campana.estrellas import estrellas
    estrellas_oficiales = estrellas()
    lugares = []
    for r in [r for r in REGIONES if r["clave"] in SUR] + NORTE_PLANEADOR:
        clave = r["clave"]
        c = cal[cal.lugar == clave].sort_values("periodo")
        calendario = [{"nivel": f.nivel, "indice": num(f.indice, 2), "esperado": num(f.esperado_est),
                       "minimo": num(f.minimo_90_est), "maximo": num(f.maximo_90_est),
                       "riesgo": num(f.riesgo_capacidad, 3), "tormenta": num(f.prob_tormenta, 3),
                       "lluvia": num(f.lluvia_normal_mm), "temp": num(f.temp_max_normal_c, 1),
                       "otro_lugar": nombres.get(f.otro_lugar) if f.otro_lugar else None,
                       "otro_lugar_clave": f.otro_lugar, "otro_mes": None if pd.isna(f.otro_mes) else int(f.otro_mes),
                       "ocupacion": num(f.ocupacion_est, 1), "tipica": num(f.ocupacion_tipica_pct, 1)}
                      for f in c.itertuples()]
        serie = forma[forma.lugar == clave] if clave != "Chetumal" else forma[forma.serie.str.startswith("Chetumal")]
        tipico = [round(float(v), 2) for v in serie.sort_values("mes").indice] if len(serie) else None
        x = rec[rec.lugar == clave]
        hacer = {m: [_negocio(f) for f in x[(x.momento == m) & (x.grupo == "hacer")].itertuples()]
                 for m in ("dia", "tarde", "noche")}
        comer = {m: [_negocio(f) for f in x[(x.momento == m) & (x.grupo == "comer")].itertuples()]
                 for m in ("dia", "tarde", "noche")}
        zonas = [{"n": z, "t": "Zona arqueológica (INAH)", "km": None, "loc": None, "otro": False,
                  "maps": enlace_maps(texto=f"{z}, Quintana Roo"), "resenas": enlace_maps(texto=f"{z}, Quintana Roo")}
                 for z in ZONAS_INAH.get(clave, [])]
        lugares.append({"clave": clave, "nombre": r["nombre"], "icono": r["icono"], "medida": MEDIDA_LUGAR.get(clave),
                        "papel": "referencia" if clave in NORTE else "promovida",
                        "calendario": calendario, "tipico": tipico, "zonas": zonas, "hacer": hacer, "comer": comer,
                        "dormir": [_negocio(f) for f in x[x.grupo == "dormir"].itertuples()],
                        "fotos": [{k: f[k] for k in ("archivo", "muestra", "autor", "licencia", "url_licencia",
                                                      "url_original", "ancho", "alto")}
                                  for f in sorted((f for f in fotos if f["lugar"] == clave and f.get("tipo", "lugar") == "lugar"),
                                                  key=lambda f: f["orden"])],
                        # Fotos de platillos con coordenada en su municipio (solo existen en el norte; decisión 17)
                        "comida": [{k: f[k] for k in ("archivo", "muestra", "autor", "licencia", "url_licencia",
                                                       "url_original", "ancho", "alto")}
                                   for f in sorted((f for f in fotos if f["lugar"] == clave and f.get("tipo") == "comida"),
                                                   key=lambda f: f["orden"])],
                        "estrellas": estrellas_oficiales.get(clave)})
    # Último mes medido de la Riviera Maya contra el mismo mes un año antes: por qué su pronóstico va más bajo.
    rm = pd.read_parquet(GOLD / "pronostico_series.parquet")
    rm = rm[(rm.lugar == "Riviera Maya") & rm.valor.notna()].set_index("periodo").valor
    ultimo = rm.index.max()
    return {
        "riviera": {"mes": ultimo.strftime("%Y-%m"), "ahora": num(rm[ultimo]),
                    "antes": num(rm.get(ultimo - pd.DateOffset(years=1)))},
        "meses": [pd.Timestamp(m).strftime("%Y-%m") for m in meses],
        "ultimo_pronostico": pd.Timestamp(cal[cal.dentro_del_pronostico_flag].periodo.max()).strftime("%Y-%m"),
        "lugares": lugares,
        "regla": {"alta_indice": 1.2, "alta_riesgo": 0.1,
                  "corte_norte": num(cal.corte_radar_pct.dropna().iloc[0], 1)},
        "fuente": "INAH (BdINAH), SITUR-Q (frontera con Belice), SECTUR-DataTur (ocupación hotelera de Cancún y Riviera "
                  "Maya), NOAA HURDAT2, Open-Meteo (clima 1991–2020) y pronóstico del proyecto (Fase 5); negocios: "
                  "INEGI, DENUE",
    }


def generar() -> Path:
    fichas = fichas_regiones()
    viajero = fichas_viajero(fichas)
    chetumal = next(f for f in fichas if f["nombre"] == "Chetumal")
    norte = referencia_norte()
    D_MAX_CANCUN[0] = norte["maximo_cancun"]
    mov, hosp = movimiento(), hospedaje()
    datos = {
        "generado": date.today().isoformat(),
        "regiones": fichas,
        "anuncio": chetumal["llegaron_en_tren"],
        "cuartos_vacios_chetumal": cuartos_vacios_chetumal(),
        "mapa": mapa_municipios(),
        "referencia_norte": norte,
        "portada": _foto_portada(),
        "criterios": criterios(),
        "resumen_datos": resumen_datos(),
        "fases": fases_del_proyecto(),
        "movimiento": mov,
        "hospedaje": hosp,
        "equipo": EQUIPO,
        "preguntas": preguntas_rapidas(fichas, mov, hosp, viajero),
        "lugares_viajero": viajero,
        # Vitrina (02-oct-2026, decisión 16): postales, experiencias y rutas, solo con datos que existen.
        # Fotos y reseñas del equipo (decisión 16); vacío = la sección "Lo que vivimos" no aparece.
        "aportes": preparar_aportes()["aportes"],
        "vitrina": vitrina(cuartos_vacios_chetumal()["vacios_de_cada_10"], hosp["tamano_negocios"]["municipios_de_los_lugares"]),
        # Secciones que se llenan en fases futuras. Mientras no existan, la página muestra su cascarón:
        # "pronostico" y "escenarios" (Fase 5), "presupuesto" (Fase 6), "envivo" (Fase 7), "campana" (Fase 8).
    }
    r = radar()  # Fase 4: solo se agrega si ya existen sus salidas en Gold
    if r:
        datos["radar"] = r
    pl = planeador_pagina()  # Fase 5: planeador y qué hacer
    if pl:
        datos["pronostico"] = pl
    pz = presupuesto_pagina()  # Fase 6: reparto del presupuesto
    if pz:
        datos["presupuesto"] = pz
    ev7 = envivo_pagina()  # Fase 7: la Torre semana a semana
    if ev7:
        datos["envivo"] = ev7
    cp = campana_pagina()  # Fase 8: la campaña
    if cp:
        datos["campana"] = cp
    datos["concentracion"] = concentracion_pagina()
    ev = evidencia_pagina()
    if ev:
        datos["evidencia"] = ev
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(
        "// Archivo generado por backend/torre/api/datos_pagina.py. No se edita a mano.\n"
        f"window.TORRE_DATOS = {json.dumps(datos, ensure_ascii=False, separators=(',', ':'))};\n",
        encoding="utf-8")
    return SALIDA


if __name__ == "__main__":
    ruta = generar()
    print(f"{ruta} · {ruta.stat().st_size / 1024:.0f} KB")
