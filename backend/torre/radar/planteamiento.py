# Autor: Brandon Uriel García Sánchez
# Módulo: Radar
# Qué hace:          Arma el planteamiento del problema con datos (Fase 3, criterio 1 de la rúbrica):
#                    1) inventario de variables: qué mide cada una, de qué fuente, qué periodo cubre y cuántos huecos tiene;
#                    2) actores: quién participa en el turismo de las 5 regiones, con una cifra medida de cada uno;
#                    3) concentración: qué parte de las llegadas, cuartos, visitantes, negocios y población tiene la
#                       unidad más grande del estado y qué parte tienen los 5 lugares (cuota e índice de Herfindahl).
# Por qué así:       La pregunta central habla de "una distribución más equilibrada de los flujos". Para decir que hoy
#                    NO está equilibrada hace falta medir la concentración, no solo afirmarla. Se usa el índice de
#                    Herfindahl-Hirschman (HHI) porque es el estándar para medir concentración, se explica con una suma
#                    de cuadrados y se puede resolver a mano (docs/metodologia/ECUACIONES.md §2).
#                    Alternativa descartada: el coeficiente de Gini. Pide ordenar y acumular (curva de Lorenz) y con
#                    4 aeropuertos da un número poco estable; el HHI se lee directo como "cuota de la más grande".
#                    Los 5 lugares se cuentan con las mismas localidades del Censo que la página y los criterios
#                    (REGION_LOCALIDADES, decisión de Brandon del 28-sep-2026), así que las cifras cuadran entre sí.
# Datos de entrada:  datos/silver/{siturq, datatur_ocupacion, inah, denue, iter}.
# Alimenta a:        Planteamiento (notebook 01) y, después, al Radar (Fase 4): las variables marcadas como "presión"
#                    y "capacidad" son los candidatos del índice de presión turística.

from pathlib import Path

import pandas as pd

from torre.base.silver_iter import REGION_LOCALIDADES

RAIZ = Path(__file__).resolve().parents[3]
SILVER = RAIZ / "datos" / "silver"

# Los 5 lugares (REGION_LOCALIDADES también trae Cancún, Playa del Carmen y Tulum como referencia: esos no cuentan).
LOCALIDADES_5 = {r: locs for r, locs in REGION_LOCALIDADES.items() if "referencia" not in r}
# SITUR-Q tiene 4 tipos de unidad: "destino", "zona" (Riviera Maya, Grand Costa Maya), "miembro" (destino que está dentro
# de una zona: Playa del Carmen, Tulum, Chetumal, Bacalar, Mahahual) y "zona_especial" (Caribe Mexicano). Para un total
# estatal sin contar dos veces se suman solo destinos + zonas. OJO: una zona NO es la suma de sus miembros publicados
# (Riviera Maya jul-2026: 59,632 cuartos contra 22,923 de Playa del Carmen + Tulum), así que sumar miembros perdería
# cuartos; y "Caribe Mexicano" no dice qué contiene, así que se deja fuera. Ver comprobar_zonas().
NIVEL_ESTATAL = {"destino", "zona"}
# Unidades de SITUR-Q que corresponden a los 5 lugares (las otras 3 regiones no tienen serie hotelera propia).
UNIDADES_LUGARES = {"Chetumal", "Maya Ka'an"}
AEROPUERTOS = ["Cancún", "Cozumel", "Chetumal", "Tulum"]

# Descripción de cada variable: esto es clasificación del proyecto, no dato. Las cifras (periodo, filas, huecos) se
# calculan en inventario_variables(). Papel: presión = demanda que llega; capacidad = lo que puede recibir;
# comunidad = quien vive ahí; hueco = existe en la fuente pero no se puede usar.
VARIABLES = {
    # clave: (nombre, unidad de medida, papel, módulos que la usan)
    "aereos_llegadas": ("Pasajeros que llegan en avión", "pasajeros/mes", "presión", "A1, A3"),
    "tren_maya_descenso": ("Personas que bajan del Tren Maya", "personas/mes", "presión", "A1, A3, A5"),
    "tren_maya_movimiento": ("Movimiento total del Tren Maya (suben y bajan)", "personas/mes", "presión", "A3"),
    "cruceristas": ("Cruceristas que bajan en el puerto", "personas/mes", "presión", "A1, A3, A5"),
    "frontera_belice": ("Cruces por la frontera con Belice", "cruces/mes", "presión", "A1, A3, A5"),
    "zonas_arqueologicas": ("Visitantes a zonas arqueológicas (SITUR-Q)", "visitantes/mes", "presión", "A1"),
    "ocupacion_hotelera": ("Ocupación hotelera mensual", "% de cuartos ocupados", "presión", "A1, A3"),
    "habitaciones": ("Cuartos de hotel disponibles", "cuartos", "capacidad", "A1, IO"),
    "centros_hospedaje": ("Hoteles y hospedajes", "establecimientos", "capacidad", "A1"),
    "afluencia_turistas": ("Afluencia de turistas", "turistas/mes", "hueco", "—"),
    "derrama_turistas": ("Derrama económica de turistas", "sin unidad publicada", "hueco", "—"),
    "derrama_visitantes": ("Derrama económica de visitantes", "sin unidad publicada", "hueco", "—"),
    "datatur_semanal": ("Ocupación hotelera semanal (norte)", "% de cuartos ocupados", "presión", "A1, A5"),
    "inah_visitantes": ("Visitantes a museos y zonas del INAH", "visitantes/mes", "presión", "A1, A3"),
    "denue_turisticos": ("Negocios turísticos (6 giros SCIAN)", "negocios", "capacidad", "A1, Campaña"),
    "iter_poblacion": ("Población por localidad (Censo 2020)", "habitantes", "comunidad", "A1, IO"),
    "iter_drenaje": ("Viviendas con drenaje (Censo 2020)", "viviendas", "comunidad", "A1"),
}


def _fila(clave: str, fuente: str, datos: pd.DataFrame, hueco: pd.Series | None = None, corte: str = "") -> dict:
    nombre, unidad, papel, modulos = VARIABLES[clave]
    hueco = pd.Series(False, index=datos.index) if hueco is None else hueco
    con_dato = datos[~hueco]
    periodo = (f"{str(con_dato.periodo.min())[:7]} a {str(con_dato.periodo.max())[:7]}"
               if "periodo" in datos and not con_dato.empty else corte)
    return {"variable": nombre, "clave": clave, "fuente": fuente, "unidad_medida": unidad, "papel": papel,
            "modulos": modulos, "periodo_con_dato": periodo if not con_dato.empty else "sin dato",
            "filas": len(datos), "huecos": int(hueco.sum()), "pct_hueco": round(100 * hueco.mean(), 1)}


def inventario_variables() -> pd.DataFrame:
    """Una fila por variable del problema: qué mide, de dónde viene, qué periodo cubre y cuántos huecos tiene."""
    filas = []
    s = pd.read_parquet(SILVER / "siturq")
    for indicador, d in s.groupby(s.indicador.astype(str)):
        if indicador in VARIABLES:
            filas.append(_fila(indicador, "SITUR-Q", d, d.hueco_flag))
    o = pd.read_parquet(SILVER / "datatur_ocupacion")
    o = o[o.es_qroo & (o.frecuencia == "semanal")]
    filas.append(_fila("datatur_semanal", "SECTUR-DataTur", o, o.ocupacion_pct.isna()))
    i = pd.read_parquet(SILVER / "inah")
    filas.append(_fila("inah_visitantes", "INAH (DataTur)", i[i.es_qroo]))
    d = pd.read_parquet(SILVER / "denue", filters=[("cve_ent", "=", 23)], columns=["es_turistico"])
    filas.append(_fila("denue_turisticos", "INEGI, DENUE", d[d.es_turistico], corte="un corte (descarga 2026-09-28)"))
    c = pd.read_parquet(SILVER / "iter")
    loc = c[c.tipo_fila == "localidad"]
    filas.append(_fila("iter_poblacion", "INEGI, Censo 2020 (ITER)", loc, loc.poblacion.isna(), corte="2020 (un corte)"))
    filas.append(_fila("iter_drenaje", "INEGI, Censo 2020 (ITER)", loc, loc.viviendas_con_drenaje.isna(), corte="2020 (un corte)"))
    orden = {"presión": 0, "capacidad": 1, "comunidad": 2, "hueco": 3}
    return pd.DataFrame(filas).sort_values(["papel", "variable"], key=lambda x: x.map(orden) if x.name == "papel" else x,
                                           ignore_index=True)


# ---------- Concentración ----------
def cuotas_y_hhi(valores: pd.Series) -> dict:
    """Cuota de cada unidad y el índice de Herfindahl-Hirschman (HHI).

    s_i = x_i / Σx          (cuota de la unidad i, entre 0 y 1)
    HHI = Σ s_i²            (1/N si todas pesan igual; 1 si una sola lo tiene todo)
    HHI* = (HHI − 1/N) / (1 − 1/N)   (normalizado: 0 = reparto parejo, 1 = todo en una unidad)
    """
    valores = valores[valores > 0].astype(float)
    if len(valores) < 2:
        raise ValueError("Hacen falta al menos 2 unidades con valor para medir concentración")
    cuota = valores / valores.sum()
    n = len(cuota)
    hhi = float((cuota ** 2).sum())
    return {"cuotas": cuota.sort_values(ascending=False), "n": n, "hhi": hhi,
            "hhi_normalizado": (hhi - 1 / n) / (1 - 1 / n), "mayor": cuota.idxmax(), "cuota_mayor": float(cuota.max())}


def _mascara_localidades(df: pd.DataFrame) -> pd.Series:
    """Filas (DENUE o Censo) que caen en las localidades de los 5 lugares."""
    m = pd.Series(False, index=df.index)
    for localidades in LOCALIDADES_5.values():
        for mun, loc, _ in localidades:
            m |= (df.cve_mun == mun) & (df.cve_loc == loc)
    return m


def _anio_completo(s: pd.DataFrame, indicador: str, unidades: list[str]) -> tuple[int, pd.Series]:
    """Suma anual del último año en que todas las unidades tienen sus 12 meses con dato."""
    x = s[(s.indicador.astype(str) == indicador) & s.unidad.isin(unidades) & ~s.hueco_flag]
    meses = x.groupby(["anio", "unidad"]).mes.nunique().unstack()
    anio = int(meses[(meses == 12).all(axis=1)].index.max())
    return anio, x[x.anio == anio].groupby("unidad").valor.sum()


def concentracion() -> pd.DataFrame:
    """Cinco dimensiones del turismo en Quintana Roo: qué tan concentradas están y qué parte tienen los 5 lugares."""
    s = pd.read_parquet(SILVER / "siturq")
    filas = []

    def agregar(dimension, unidad_analisis, valores, cuota_lugares, periodo, fuente, nota=""):
        r = cuotas_y_hhi(valores)
        filas.append({"dimension": dimension, "unidad_de_analisis": unidad_analisis, "n_unidades": r["n"],
                      "total": float(valores.sum()), "mayor": r["mayor"], "cuota_mayor_pct": round(100 * r["cuota_mayor"], 1),
                      "hhi": round(r["hhi"], 3), "hhi_normalizado": round(r["hhi_normalizado"], 3),
                      "cuota_5_lugares_pct": round(100 * cuota_lugares, 1), "periodo": periodo, "fuente": fuente, "nota": nota})

    # 1) Llegadas en avión: último año completo (2024; desde 2025 la fuente publica ceros = hueco, regla 6).
    anio, aereo = _anio_completo(s, "aereos_llegadas", AEROPUERTOS)
    agregar("Llegadas en avión", "aeropuerto", aereo, aereo.get("Chetumal", 0) / aereo.sum(), str(anio), "SITUR-Q",
            "De los 5 lugares solo Chetumal tiene aeropuerto.")

    # 2) Cuartos de hotel: último mes publicado. Total estatal = destinos + zonas (ver NIVEL_ESTATAL).
    h = s[(s.indicador.astype(str) == "habitaciones") & ~s.hueco_flag]
    h = h[h.periodo == h.periodo.max()]
    cuartos = h[h.tipo_unidad.isin(NIVEL_ESTATAL)].groupby("unidad").valor.sum()
    lugares = h[h.unidad.isin(UNIDADES_LUGARES)].valor.sum()  # Chetumal es "miembro" de Grand Costa Maya: ya va en el total
    agregar("Cuartos de hotel", "destino o zona", cuartos, lugares / cuartos.sum(), str(h.periodo.max())[:7], "SITUR-Q",
            "Los 5 lugares = Chetumal + Maya Ka'an; las otras 3 regiones no tienen serie hotelera.")

    # 3) Visitantes a sitios del INAH en 2025 (último año completo).
    i = pd.read_parquet(SILVER / "inah")
    i = i[i.es_qroo & (i.anio == 2025)]
    sitios = i.groupby("nombre").visitantes.sum()
    promovidas = i[i.papel_campana == "promovida"].visitantes.sum()
    agregar("Visitantes a sitios del INAH", "sitio", sitios, promovidas / sitios.sum(), "2025", "INAH (DataTur)",
            "Los 5 lugares = Oxtankah, Kohunlich, Dzibanché e Ichkabal.")

    # 4) Negocios turísticos: HHI por municipio; cuota de los 5 lugares por sus localidades.
    d = pd.read_parquet(SILVER / "denue", filters=[("cve_ent", "=", 23)], columns=["cve_mun", "cve_loc", "municipio", "es_turistico"])
    d = d[d.es_turistico]
    agregar("Negocios turísticos", "municipio", d.groupby("municipio").size(), _mascara_localidades(d).mean(),
            "corte 2026-09", "INEGI, DENUE", "Cuota de los 5 lugares contada en sus localidades.")

    # 5) Población (la referencia: dónde vive la gente que recibe al turismo).
    c = pd.read_parquet(SILVER / "iter")
    mun = c[c.tipo_fila == "total_municipal"].set_index("municipio").poblacion
    estado = float(c[c.tipo_fila == "total_estatal"].poblacion.iloc[0])
    loc = c[c.tipo_fila == "localidad"]
    agregar("Población", "municipio", mun, loc[_mascara_localidades(loc)].poblacion.sum() / estado, "2020",
            "INEGI, Censo 2020", "Cuota de los 5 lugares contada en sus localidades.")
    tabla = pd.DataFrame(filas)
    # Razón contra la población: 1 = los 5 lugares tienen de esa dimensión la misma parte que de gente; 0.11 = la novena
    # parte. Es una comparación, no una meta: nadie dice que el turismo deba repartirse según la población.
    poblacion = tabla.loc[tabla.dimension == "Población", "cuota_5_lugares_pct"].iloc[0]
    tabla["razon_vs_poblacion"] = (tabla.cuota_5_lugares_pct / poblacion).round(2)
    return tabla


MIEMBROS = {"Grand Costa Maya": ["Chetumal", "Bacalar", "Mahahual"], "Riviera Maya": ["Playa del Carmen", "Tulum"]}


def comprobar_zonas() -> pd.DataFrame:
    """¿Una zona de SITUR-Q es la suma de sus miembros? (cuartos del último mes). Si no, sumar miembros perdería cuartos."""
    s = pd.read_parquet(SILVER / "siturq")
    h = s[(s.indicador.astype(str) == "habitaciones") & ~s.hueco_flag]
    h = h[h.periodo == h.periodo.max()].set_index("unidad").valor
    return pd.DataFrame([{"zona": z, "cuartos_zona": h[z], "suma_miembros": h[m].sum(), "miembros": ", ".join(m),
                          "diferencia": h[z] - h[m].sum()} for z, m in MIEMBROS.items()])


# ---------- Actores ----------
def actores() -> pd.DataFrame:
    """Quién participa en el turismo de los 5 lugares, qué papel tiene y una cifra medida de cada uno."""
    s = pd.read_parquet(SILVER / "siturq")
    s = s[~s.hueco_flag]
    c = pd.read_parquet(SILVER / "iter")
    loc = c[c.tipo_fila == "localidad"]
    d = pd.read_parquet(SILVER / "denue", filters=[("cve_ent", "=", 23)], columns=["cve_mun", "cve_loc", "es_turistico"])
    d = d[d.es_turistico]
    i = pd.read_parquet(SILVER / "inah")
    i = i[i.es_qroo & (i.anio == 2025) & (i.papel_campana == "promovida")]
    anio_tren, tren = _anio_completo(s, "tren_maya_descenso", ["Chetumal", "Maya Ka'an"])
    anio_bz, belice = _anio_completo(s, "frontera_belice", ["Chetumal"])
    indicadores = s.indicador.astype(str).nunique()
    o = pd.read_parquet(SILVER / "datatur_ocupacion", columns=["centro", "es_qroo", "frecuencia"])
    centros_norte = o[o.es_qroo & (o.frecuencia == "semanal")].centro.nunique()
    filas = [
        ("Comunidades de los 5 lugares", "Reciben a los visitantes; su tamaño pone el límite",
         f"{int(loc[_mascara_localidades(loc)].poblacion.sum()):,} habitantes", "Censo 2020"),
        ("Negocios turísticos locales", "Ofrecen comida, hospedaje, transporte y visitas",
         f"{int(_mascara_localidades(d).sum()):,} negocios en las localidades de los 5 lugares", "DENUE"),
        ("Visitantes que llegan en Tren Maya", "Demanda que ya llega al sur",
         f"{int(tren.sum()):,} bajaron en Chetumal y Maya Ka'an en {anio_tren}", "SITUR-Q"),
        ("Frontera con Belice", "Demanda de frontera de Chetumal",
         f"{int(belice.sum()):,} cruces en {anio_bz}", "SITUR-Q"),
        ("INAH", "Administra las 4 zonas arqueológicas de los 5 lugares",
         f"{int(i.visitantes.sum()):,} visitantes en 2025 en las 4 zonas", "INAH"),
        ("Gobierno de Quintana Roo (SITUR-Q)", "Mide el turismo del estado y publica los datos",
         f"{indicadores} indicadores con dato publicado", "SITUR-Q"),
        ("Secretaría de Turismo federal (DataTur)", "Mide la ocupación semanal del norte (la referencia)",
         f"{centros_norte} centros turísticos de Quintana Roo con ocupación semanal", "DataTur"),
    ]
    return pd.DataFrame(filas, columns=["actor", "papel", "cifra_medida", "fuente"])


if __name__ == "__main__":
    pd.set_option("display.width", 200, "display.max_columns", 20)
    print(inventario_variables()[["variable", "papel", "periodo_con_dato", "filas", "pct_hueco"]].to_string())
    print(concentracion().drop(columns=["fuente", "nota"]).to_string())
    print(comprobar_zonas().to_string())
    print(actores().to_string())
