# Autor: Brandon Uriel García Sánchez
# Módulo: Radar
# Qué hace:          Pieza 1 de la Fase 4. Arma el panel mensual del Radar: una fila por lugar y mes (2022-01 al último
#                    mes publicado) con las variables candidatas del índice de presión turística, y una tabla de
#                    cobertura que dice cuántos meses con dato tiene cada lugar en cada variable.
# Por qué así:       - Mensual y no semanal: el sur solo se publica por mes (SITUR-Q, INAH). La ocupación semanal de
#                      DataTur (solo norte) se usa aparte, en la cadena de Markov (pieza 3).
#                    - Visitantes a zonas arqueológicas: se toman del INAH zona por zona y NO de SITUR-Q, porque la
#                      serie "zonas arqueológicas" de SITUR-Q es el mismo dato del INAH agrupado por destino (Chetumal
#                      2025 = 39,459 = Oxtankah 11,017 + Kohunlich 21,850 + Dzibanché 6,592). Usar las dos contaría dos
#                      veces a los mismos visitantes. Cada zona se asigna a UN solo lugar (ZONA_A_LUGAR).
#                    - Sin avión: un aeropuerto no es un destino (a Cancún llega gente que va a toda la Riviera) y
#                      además la serie termina en 2024 (regla 6 de Silver).
#                    - Sin zonas de SITUR-Q (Riviera Maya, Grand Costa Maya, Caribe Mexicano): suman lugares que ya
#                      están en el panel (ver planteamiento.py, comprobar_zonas()).
#                    - Un hueco se queda como nulo; no se rellena (regla de oro 1).
# Datos de entrada:  datos/silver/{siturq, inah, iter}.
# Alimenta a:        Índice de presión y estados (pieza 2, indice.py) → decisión de la campaña: dónde anunciar y dónde
#                    no (un lugar "saturado" no se promueve).

from pathlib import Path

import pandas as pd

from torre.base.silver_iter import REGION_LOCALIDADES

RAIZ = Path(__file__).resolve().parents[3]
SILVER = RAIZ / "datos" / "silver"
GOLD = RAIZ / "datos" / "gold"
DESDE = "2022-01-01"  # primer mes con cuartos de hotel publicados en SITUR-Q

# Lugares del Radar: los 5 de la campaña + los destinos de SITUR-Q del resto del estado (referencia para la escala
# común de percentiles, decisión de Brandon del 28-sep-2026).
LUGARES_5 = ["Chetumal", "Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur", "Maya Ka'an + Kantemó",
             "Laguna Milagros–Xul-Ha"]
SITURQ_A_LUGAR = {"Chetumal": "Chetumal", "Maya Ka'an": "Maya Ka'an + Kantemó",  # los 2 de la campaña con serie propia
                  "Cancún": "Cancún", "Costa Mujeres": "Costa Mujeres", "Isla Mujeres": "Isla Mujeres",
                  "Holbox": "Holbox", "Cozumel": "Cozumel", "Puerto Morelos": "Puerto Morelos",
                  "Playa del Carmen": "Playa del Carmen", "Tulum": "Tulum", "Bacalar": "Bacalar", "Mahahual": "Mahahual"}
# Cada zona arqueológica del INAH va a un solo lugar. Misma agrupación que SITUR-Q, salvo Ichkabal: SITUR-Q la suma a
# Bacalar, pero en el proyecto es parte de la Ruta arqueológica del sur (decisión de regiones, 01-regiones.md).
ZONA_A_LUGAR = {"Z.A. de Oxtankah": "Bahía Calderitas–Oxtankah", "Z.A. de Kohunlich": "Ruta arqueológica del sur",
                "Z.A. de Dzibanché-Kinichná": "Ruta arqueológica del sur", "Z.A de Ichkabal": "Ruta arqueológica del sur",
                "Z.A. de Chacchoben": "Bacalar", "Z.A. de Tulum": "Tulum", "Z.A. de Cobá": "Tulum", "Z.A. de Muyil": "Tulum",
                "Z.A. de Xelhá": "Tulum", "Z.A. de San Gervasio": "Cozumel", "Z.A. de El Rey": "Cancún",
                "Z.A. de El Meco": "Costa Mujeres", "Z.A. de Xcaret": "Playa del Carmen"}
# Zonas que el INAH lista pero que nunca registran visitantes (0 en todos sus meses, 2016–2023): no son un destino.
# Si algún día registran visitantes, _inah() se detiene para asignarlas a un lugar.
ZONAS_SIN_VISITA = {"Z.A. de Chakanbakán"}
# Localidades del Censo para la población de los lugares de referencia (los 5 usan REGION_LOCALIDADES).
# Costa Mujeres no es una localidad del Censo: queda sin población (se declara).
LOCALIDAD_REFERENCIA = {"Cancún": [("005", "0001")], "Isla Mujeres": [("003", "0001")], "Holbox": [("007", "0012")],
                        "Cozumel": [("001", "0001")], "Puerto Morelos": [("011", "0001")],
                        "Playa del Carmen": [("008", "0001")], "Tulum": [("009", "0001")], "Bacalar": [("010", "0001")],
                        "Mahahual": [("004", "0053")]}
# (indicador, variable) de SITUR-Q → columna del panel. OJO: "ocupacion_hotelera" trae TRES filas por mes (cuartos-noche
# disponibles, cuartos-noche ocupados y el porcentaje). La primera versión del panel las sumaba (corrección del
# 29-sep-2026). Ahora se guardan los cuartos-noche y el porcentaje se recalcula como ocupados ÷ disponibles, igual que en
# la tabla de criterios (nunca se suman ni se promedian porcentajes).
INDICADORES = {("tren_maya_descenso", "total"): "llegadas_tren", ("cruceristas", "cruceristas"): "cruceristas",
               ("frontera_belice", "total_cruces_fronterizos"): "cruces_belice",
               ("ocupacion_hotelera", "total_de_habitaciones_ocupadas"): "cuartos_noche_ocupados",
               ("ocupacion_hotelera", "numero_de_habitaciones_disponibles"): "cuartos_noche_disponibles",
               ("habitaciones", "total_de_habitaciones"): "cuartos", ("centros_hospedaje", "total_de_hoteles"): "hoteles"}
VARIABLES = ["llegadas_tren", "cruceristas", "cruces_belice", "visitantes_inah", "ocupacion_pct",
             "ocupacion_siturq_pct", "ocupacion_datatur_pct", "cuartos_noche_ocupados", "cuartos_noche_disponibles",
             "cuartos", "hoteles"]
# Ocupación de DataTur (semanal, 2022–2026) para los 4 lugares del panel que DataTur mide con el mismo nombre. SITUR-Q
# dejó de publicar ocupación en 2025; sin esta fuente el Radar calificaba a Cancún "tranquilo" en jul-2026 (IPT 0.025)
# cuando DataTur marca 68.8 %. Decisión de Brandon del 29-sep-2026 (opción D, 08-radar.md). Cada lugar usa UNA sola
# fuente de ocupación en toda su historia (ocupacion_pct), para no contar la ocupación dos veces ni cambiar de fuente
# a media serie. Akumal, Playacar y "Riviera Maya" de DataTur no son lugares del panel y no se usan.
DATATUR_A_LUGAR = {"Cancun": "Cancún", "Playa Del Carmen": "Playa del Carmen", "Cozumel": "Cozumel",
                   "Isla Mujeres": "Isla Mujeres"}


def _siturq() -> pd.DataFrame:
    """Variables de SITUR-Q por lugar y mes (sin huecos: el hueco queda como ausencia de fila → nulo en el panel)."""
    s = pd.read_parquet(SILVER / "siturq")
    llave = pd.Series(list(zip(s.indicador.astype(str), s.variable)), index=s.index)
    s = s[~s.hueco_flag & s.unidad.isin(SITURQ_A_LUGAR) & llave.isin(INDICADORES)]
    s = s.assign(lugar=s.unidad.map(SITURQ_A_LUGAR), columna=llave[s.index].map(INDICADORES),
                 periodo=pd.to_datetime(s.periodo.astype(str)))
    repetidas = s.duplicated(["lugar", "periodo", "columna"])
    if repetidas.any():  # una variable debe traer una sola fila por lugar y mes; si no, se detiene (no se suma a ciegas)
        raise ValueError(f"Filas repetidas en SITUR-Q: {s[repetidas][['lugar', 'periodo', 'columna']].head().to_dict('records')}")
    t = s.pivot(index=["lugar", "periodo"], columns="columna", values="valor").reset_index()
    t["ocupacion_siturq_pct"] = 100 * t.cuartos_noche_ocupados / t.cuartos_noche_disponibles
    return t


def _datatur() -> pd.DataFrame:
    """Ocupación mensual desde DataTur semanal: Σ cuartos ocupados ÷ Σ cuartos disponibles de las semanas que empiezan
    en el mes (nunca el promedio de porcentajes). Una semana que cruza de mes cuenta en el mes de su lunes (se declara)."""
    o = pd.read_parquet(SILVER / "datatur_ocupacion",
                        columns=["centro", "es_qroo", "frecuencia", "periodo", "cuartos_ocupados", "cuartos_disponibles"])
    o = o[o.es_qroo & (o.frecuencia == "semanal") & o.centro.isin(DATATUR_A_LUGAR)]
    o = o.assign(lugar=o.centro.map(DATATUR_A_LUGAR),
                 periodo=pd.to_datetime(o.periodo.astype(str)).dt.to_period("M").dt.to_timestamp())
    m = o.groupby(["lugar", "periodo"], as_index=False)[["cuartos_ocupados", "cuartos_disponibles"]].sum()
    m["ocupacion_datatur_pct"] = 100 * m.cuartos_ocupados / m.cuartos_disponibles
    return m[["lugar", "periodo", "ocupacion_datatur_pct"]]


def _inah() -> pd.DataFrame:
    """Visitantes (nacionales + extranjeros) a zonas arqueológicas por lugar y mes."""
    i = pd.read_parquet(SILVER / "inah", columns=["nombre", "clasificacion", "periodo", "visitantes", "es_qroo"])
    i = i[i.es_qroo & (i.clasificacion == "Zona Arqueológica")]
    sin_visita = i[i.nombre.isin(ZONAS_SIN_VISITA)]
    if sin_visita.visitantes.sum() > 0:
        raise ValueError(f"Una zona de ZONAS_SIN_VISITA ya registra visitantes: {sorted(sin_visita[sin_visita.visitantes > 0].nombre.unique())}")
    i = i[~i.nombre.isin(ZONAS_SIN_VISITA)]
    faltan = set(i.nombre) - set(ZONA_A_LUGAR)
    if faltan:  # regla de oro 5: una zona sin lugar asignado detiene el paso
        raise ValueError(f"Zonas del INAH sin lugar asignado en ZONA_A_LUGAR: {sorted(faltan)}")
    i = i.assign(lugar=i.nombre.map(ZONA_A_LUGAR), periodo=pd.to_datetime(i.periodo.astype(str)))
    return i.groupby(["lugar", "periodo"], as_index=False).visitantes.sum().rename(columns={"visitantes": "visitantes_inah"})


def _poblacion() -> pd.Series:
    c = pd.read_parquet(SILVER / "iter", columns=["cve_mun", "cve_loc", "poblacion", "tipo_fila"])
    c = c[c.tipo_fila == "localidad"]
    localidades = {r: [(m, l) for m, l, _ in locs] for r, locs in REGION_LOCALIDADES.items() if r in LUGARES_5}
    localidades |= LOCALIDAD_REFERENCIA
    return pd.Series({lugar: c[c.set_index(["cve_mun", "cve_loc"]).index.isin(locs)].poblacion.sum()
                      for lugar, locs in localidades.items()}, name="poblacion")


def panel_mensual() -> pd.DataFrame:
    """Una fila por lugar × mes, de DESDE al último mes publicado. Las celdas sin dato quedan nulas."""
    datos = _siturq().merge(_inah(), on=["lugar", "periodo"], how="outer")
    lugares = LUGARES_5 + [l for l in SITURQ_A_LUGAR.values() if l not in LUGARES_5]
    meses = pd.date_range(DESDE, datos.periodo.max(), freq="MS")
    datos = datos.merge(_datatur(), on=["lugar", "periodo"], how="left")
    datatur = datos.lugar.isin(DATATUR_A_LUGAR.values())
    datos["ocupacion_pct"] = datos.ocupacion_datatur_pct.where(datatur, datos.ocupacion_siturq_pct)
    base = pd.MultiIndex.from_product([lugares, meses], names=["lugar", "periodo"]).to_frame(index=False)
    p = base.merge(datos, on=["lugar", "periodo"], how="left")
    for v in VARIABLES:
        if v not in p:
            p[v] = pd.NA
    p["fuente_ocupacion"] = p.lugar.isin(DATATUR_A_LUGAR.values()).map({True: "DataTur", False: "SITUR-Q"})
    p = p.merge(_poblacion(), left_on="lugar", right_index=True, how="left")
    p["es_de_los_5"] = p.lugar.isin(LUGARES_5)
    return p[["lugar", "es_de_los_5", "periodo", *VARIABLES, "fuente_ocupacion", "poblacion"]].sort_values(
        ["lugar", "periodo"], ignore_index=True)


def cobertura(panel: pd.DataFrame) -> pd.DataFrame:
    """Meses con dato por lugar y variable (de cuántos posibles). Sirve para ver qué variables pueden entrar al índice."""
    tabla = panel.groupby("lugar")[VARIABLES].count()
    tabla.insert(0, "meses_posibles", panel.groupby("lugar").size())
    return tabla.loc[LUGARES_5 + [l for l in tabla.index if l not in LUGARES_5]]


def guardar() -> Path:
    GOLD.mkdir(parents=True, exist_ok=True)
    salida = GOLD / "radar_panel_mensual.parquet"
    panel_mensual().to_parquet(salida, index=False)
    return salida


if __name__ == "__main__":
    pd.set_option("display.width", 200, "display.max_columns", 20)
    ruta = guardar()
    p = pd.read_parquet(ruta)
    print(f"{ruta} · {len(p):,} filas · {p.lugar.nunique()} lugares · {p.periodo.min():%Y-%m} a {p.periodo.max():%Y-%m}")
    print(cobertura(p).to_string())
