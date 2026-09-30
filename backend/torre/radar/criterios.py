# Autor: Brandon Uriel García Sánchez
# Módulo: Radar
# Qué hace:          Calcula la tabla de criterios de selección (D.1 de docs/regiones/REGIONES.md) para las 5 regiones
#                    que promueve la campaña, con Cancún, Riviera Maya (Playa del Carmen) y Tulum como referencia:
#                    1) sargazo, 2) cierres, 3) saturación, 4) servicios y fragilidad, 5) datos oficiales disponibles.
#                    La guarda en datos/gold/criterios_regiones.parquet.
# Por qué así:       - Fase 3: la selección de regiones pasa de "evidencia de prensa" a una tabla calculada con datos.
#                    - Criterio 2 (decisión de Brandon, 28-sep-2026): una zona pasa si lleva al menos 12 meses seguidos
#                      abierta y no tuvo cierres en 2026. Alternativa descartada: "ningún cierre desde 2024" (sacaría a
#                      la ruta sur y a Oxtankah, que cerraron por obras en 2024).
#                    - Criterio 3 usa tres medidas que no requieren umbral todavía (los umbrales de "saturado" se fijan
#                      en la Fase 4): ocupación hotelera 2024 (Σ ocupados / Σ disponibles, misma fuente y año para todos),
#                      visitantes INAH por residente y negocios turísticos por cada mil habitantes.
#                    - Población y negocios por localidad (decisión de Brandon, 05-planteamiento.md).
#                    - Sargazo y fragilidad ecológica no tienen serie oficial: se registran como evidencia documental
#                      con su fuente (docs/regiones/REGIONES.md), marcadas como tal. No se inventa un número.
# Datos de entrada:  datos/silver/{siturq, inah, iter, denue}.
# Alimenta a:        La confirmación de las 5 regiones (Fase 3), el Índice de Presión Turística (Fase 4) y los topes de
#                    capacidad del modelo de IO (Fase 6).

import pandas as pd

from torre.base.entorno import RAIZ
from torre.base.silver_iter import REGION_LOCALIDADES

SILVER = RAIZ / "datos" / "silver"
GOLD = RAIZ / "datos" / "gold"
MESES_MINIMOS_ABIERTA = 12  # regla del criterio 2 (decisión de Brandon)

# Cómo se busca cada región en cada fuente. Sargazo y fragilidad: evidencia documental de REGIONES.md.
REGIONES = [
    {"region": "Chetumal", "papel": "promovida", "iter": "Chetumal", "denue": "Chetumal", "inah": None,
     "siturq": "Chetumal", "sargazo": ("vigilancia", "Sin sargazo en su costa; sí en los canales de entrada de la bahía (ECOSUR, 28-sep-2026)"),
     "fragilidad": None},
    {"region": "Bahía Calderitas–Oxtankah", "papel": "promovida", "iter": "Bahía Calderitas–Oxtankah",
     "denue": "Bahía Calderitas–Oxtankah", "inah": "Bahía Calderitas–Oxtankah", "siturq": None,
     "sargazo": ("vigilancia", "Misma bahía que Chetumal; sin reporte en la costa de Calderitas"), "fragilidad": None},
    {"region": "Ruta arqueológica del sur", "papel": "promovida", "iter": "Ruta arqueológica del sur",
     "denue": "Ruta arqueológica del sur", "inah": "Ruta arqueológica del sur", "siturq": None,
     "sargazo": ("no aplica", "Tierra adentro, lejos del mar"), "fragilidad": None},
    {"region": "Maya Ka'an + Kantemó", "papel": "promovida", "iter": "Maya Ka'an + Kantemó",
     "denue": "Maya Ka'an + Kantemó", "inah": None, "siturq": "Maya Ka'an",
     "sargazo": ("no aplica", "Pueblos del interior, lejos del mar"), "fragilidad": "Poca oferta instalada: límite por capacidad"},
    {"region": "Laguna Milagros–Xul-Ha", "papel": "promovida", "iter": "Laguna Milagros–Xul-Ha",
     "denue": "Laguna Milagros–Xul-Ha", "inah": None, "siturq": None,
     "sargazo": ("no aplica", "Laguna interior, no es playa de mar abierto"),
     "fragilidad": "Sistema lagunar frágil, el mismo de Bacalar (UNAM Global): límite estricto"},
    {"region": "Cancún", "papel": "referencia", "iter": "Cancún", "denue": "Cancún (referencia)", "inah": "Cancún",
     "siturq": "Cancún", "sargazo": ("afectada", "Sargazo excesivo en la zona norte en 2026 (Excélsior)"), "fragilidad": None},
    {"region": "Riviera Maya (Playa del Carmen)", "papel": "referencia", "iter": "Playa del Carmen",
     "denue": "Playa del Carmen (referencia)", "inah": None, "siturq": "Playa del Carmen",
     "sargazo": ("afectada", "Sargazo severo en 2026 (Reportur)"), "fragilidad": None},
    {"region": "Tulum", "papel": "referencia", "iter": "Tulum", "denue": "Tulum (referencia)", "inah": "Tulum",
     "siturq": "Tulum", "sargazo": ("afectada", "Inicio de la franja más afectada Tulum–Xcalak (PorEsto, 2026)"),
     "fragilidad": None, "cierres_prensa": "Cierres de negocios y ventas −60 % en 2026 (La Jornada, 16-jul-2026)"},
]


def _ocupacion_2024(siturq: pd.DataFrame, unidad: str | None) -> float | None:
    """Ocupación hotelera de 2024 = Σ cuartos ocupados / Σ cuartos disponibles (nunca promedio de porcentajes)."""
    if not unidad:
        return None
    o = siturq[(siturq.indicador.astype(str) == "ocupacion_hotelera") & (siturq.unidad == unidad) & ~siturq.hueco_flag
               & (siturq.anio == 2024)]
    p = o.pivot_table(index="mes", columns="variable", values="valor")
    if len(p) < 12:
        return None
    return round(p.total_de_habitaciones_ocupadas.sum() / p.numero_de_habitaciones_disponibles.sum() * 100, 1)


def _meses_abierta(inah: pd.DataFrame, region: str | None) -> tuple[int | None, int | None, str]:
    """Meses seguidos abierta (hasta el último mes publicado) de la zona MENOS abierta de la región, y meses en cero en
    el año más reciente. Un mes con 0 visitantes (nacionales + extranjeros) cuenta como cerrado."""
    if not region:
        return None, None, "sin zona arqueológica del INAH"
    z = inah[inah.region_campana == region].copy()
    z["anio"] = z.anio.astype(int)
    ultimo = int(z.anio.max())
    minimo, cero_ultimo, detalle = None, 0, []
    for nombre, g in z.groupby("nombre"):
        m = g.groupby(["anio", "mes"]).visitantes.sum().sort_index()
        seguidos = 0
        for v in reversed(m.values):
            if v == 0:
                break
            seguidos += 1
        cero_ultimo += int((m.loc[ultimo] == 0).sum()) if ultimo in m.index.get_level_values(0) else 0
        minimo = seguidos if minimo is None else min(minimo, seguidos)
        detalle.append(f"{nombre.replace('Z.A. de ', '').replace('Z.A de ', '')}: {seguidos}")
    return minimo, cero_ultimo, "; ".join(detalle)


def calcular_criterios() -> pd.DataFrame:
    siturq = pd.read_parquet(SILVER / "siturq")
    inah = pd.read_parquet(SILVER / "inah")
    inah = inah[inah.es_qroo]
    censo = pd.read_parquet(SILVER / "iter")
    denue = pd.read_parquet(SILVER / "denue", filters=[("cve_ent", "=", 23)], columns=["cve_mun", "cve_loc", "es_turistico"])
    denue = denue[denue.es_turistico]
    filas = []
    for r in REGIONES:
        pob = censo[censo.region_campana == r["iter"]]
        poblacion = int(pob.poblacion.sum())
        viviendas = pob.dropna(subset=["viviendas_con_agua", "viviendas_con_drenaje"])  # sin las reservadas por INEGI
        negocios = 0
        for mun, loc, _ in REGION_LOCALIDADES[r["denue"]]:
            negocios += int(((denue.cve_mun == mun) & (denue.cve_loc == loc)).sum())
        visitantes_2025 = None
        if r["inah"]:
            z = inah[(inah.region_campana == r["inah"]) & (inah.anio.astype(int) == 2025)]
            visitantes_2025 = int(z.visitantes.sum())
        meses, cero_2026, detalle = _meses_abierta(inah, r["inah"])
        if r.get("cierres_prensa"):
            pasa_cierres, motivo = False, r["cierres_prensa"]
        elif meses is None:
            pasa_cierres, motivo = True, "Sin zona INAH; sin cierres reportados en 2026 (evidencia documental)"
        else:
            pasa_cierres = meses >= MESES_MINIMOS_ABIERTA and cero_2026 == 0
            motivo = f"Meses seguidos abierta — {detalle}"
        tren = siturq[(siturq.indicador.astype(str) == "tren_maya_descenso") & (siturq.unidad == r["siturq"]) & ~siturq.hueco_flag] if r["siturq"] else pd.DataFrame()
        series = ["negocios (INEGI)", "Censo 2020"]
        ocup = _ocupacion_2024(siturq, r["siturq"])
        if ocup is not None:
            series.append("ocupación hotelera (hasta 2024)")
        if len(tren):
            series.append("Tren Maya")
        if r["inah"]:
            series.append("visitantes INAH")
        filas.append({
            "region": r["region"], "papel": r["papel"],
            "c1_sargazo": r["sargazo"][0], "c1_evidencia": r["sargazo"][1],
            "c2_meses_abierta_min": meses, "c2_meses_cerrada_2026": cero_2026, "c2_pasa": pasa_cierres, "c2_evidencia": motivo,
            "c3_ocupacion_2024_pct": ocup,
            "c3_visitantes_inah_por_residente": round(visitantes_2025 / poblacion, 2) if visitantes_2025 is not None else None,
            "c3_negocios_turisticos_por_mil": round(negocios / poblacion * 1000, 1),
            "c4_viviendas_sin_agua_pct": round((1 - viviendas.viviendas_con_agua.sum() / viviendas.viviendas_habitadas.sum()) * 100, 1),
            "c4_viviendas_sin_drenaje_pct": round((1 - viviendas.viviendas_con_drenaje.sum() / viviendas.viviendas_habitadas.sum()) * 100, 1),
            "c4_fragilidad_documental": r["fragilidad"],
            "c5_series_oficiales": len(series), "c5_cuales": ", ".join(series),
            "poblacion_2020": poblacion, "negocios_turisticos": negocios, "visitantes_inah_2025": visitantes_2025,
        })
    tabla = pd.DataFrame(filas)
    GOLD.mkdir(parents=True, exist_ok=True)
    tabla.to_parquet(GOLD / "criterios_regiones.parquet", index=False)
    return tabla


if __name__ == "__main__":
    t = calcular_criterios()
    pd.set_option("display.width", 250)
    print(t[["region", "c1_sargazo", "c2_meses_abierta_min", "c2_pasa", "c3_ocupacion_2024_pct",
             "c3_visitantes_inah_por_residente", "c3_negocios_turisticos_por_mil", "c4_viviendas_sin_agua_pct",
             "c4_viviendas_sin_drenaje_pct", "c5_series_oficiales"]].to_string(index=False))
