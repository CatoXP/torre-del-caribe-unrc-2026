# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña (Investigación de Operaciones, Fase 6)
# Qué hace:          Reparte el presupuesto de la campaña entre meses, lugares del sur y canales (Google, Facebook) con un
#                    modelo estocástico de dos etapas resuelto con PuLP/CBC:
#                    - Etapa 1 (se decide hoy): x[mes, lugar, canal] = pesos.
#                    - Etapa 2 (recurso): para cada escenario del Pronóstico (malo, probable, bueno), y[escenario, mes,
#                      lugar] ∈ {0,1} dice si el anuncio sigue encendido. Si ese escenario más los visitantes que trae la
#                      campaña rebasa la capacidad probada, el anuncio se pausa y esas conversiones se pierden.
#                    Después mide cuánto cuesta cada regla, traza la frontera de Pareto (visitantes contra qué tan
#                    lleno se permite un lugar) y repite todo con los supuestos movidos (sensibilidad).
# Por qué así:       Decisiones de Brandon del 02-oct-2026 (docs/decisiones/19-presupuesto.md):
#                    - Objetivo: visitantes (conversiones) esperados hacia los 3 lugares del sur. Descartados: derrama
#                      (SITUR-Q no trae unidad y termina en mar-2024) y visitantes con castigo (exige elegir un peso).
#                    - Presupuesto: $250,000 MXN al año (supuesto) → prorrateado a los meses que tienen pronóstico.
#                    - Conversión de Facebook para turismo: no publicada → barrido 3 % / 5.75 % (Google Travel) / mediana
#                      de Facebook en todas las industrias.
#                    - Restricciones: cero anuncio en temporada alta, tope de capacidad probada, piso de equidad de 15 %
#                      por lugar y tope de 70 % por canal.
#                    - Como todos los lugares convierten igual (no hay dato de respuesta por lugar), el máximo de
#                      visitantes tiene muchas soluciones. Se desempata en un segundo paso (lexicográfico): con el mismo
#                      número de visitantes, el dinero va donde hay más espacio libre. Sin ese paso, el resultado
#                      dependería de cómo recorre CBC las soluciones y no se podría explicar.
#                    - Escenarios con pesos 30/40/30 (regla de Swanson para resumir p10/p50/p90).
#                    - Supuesto declarado: cada conversión cuenta como un visitante más (cota alta: protege la capacidad).
# Datos de entrada:  datos/bronze/benchmarks/<fecha>/benchmarks_tablas.csv (D13: costo por clic y conversión),
#                    datos/silver/fred_mensual (pesos por dólar), datos/gold/pronostico_escenarios y pronostico_calendario.
# Alimenta a:        La decisión de cuánto dinero poner en cada lugar, mes y canal (Fase 6) y las reglas que la Torre en
#                    vivo ejecuta cada semana (Fase 7).

from dataclasses import dataclass, field, replace

import pandas as pd
import pulp

from torre.base.entorno import RAIZ

GOLD = RAIZ / "datos" / "gold"
SILVER = RAIZ / "datos" / "silver"
BENCHMARKS = sorted((RAIZ / "datos" / "bronze" / "benchmarks").glob("*/benchmarks_tablas.csv"))

SUR = ["Chetumal", "Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur"]
ESCENARIOS = {"malo": ("malo_p10_est", 0.3), "probable": ("probable_p50_est", 0.4), "bueno": ("bueno_p90_est", 0.3)}
PRESUPUESTO_ANUAL = 250_000.0  # MXN, supuesto elegido por Brandon
PISO_EQUIDAD = 0.15
TOPE_CANAL = 0.70


@dataclass(frozen=True)
class Supuestos:
    """Todo lo que el modelo supone. La sensibilidad cambia uno a la vez con dataclasses.replace."""
    presupuesto_anual: float = PRESUPUESTO_ANUAL
    cvr_facebook: float | None = None   # None = la de Google Travel (5.75 %), el caso base del barrido
    cpc_facebook_usd: float | None = None  # None = WordStream 2025 Travel
    golpe_tormenta: float = 0.0
    piso_equidad: float = PISO_EQUIDAD
    tope_canal: float = TOPE_CANAL
    temporada_alta: bool = True          # regla: cero anuncio en temporada alta
    capacidad: bool = True               # regla: tope de capacidad probada
    equidad: bool = True                 # regla: piso por lugar
    canales: bool = True                 # regla: tope por canal
    ocupacion_max: float | None = None   # frontera de Pareto: ningún lugar pasa de esta fracción de su capacidad
    nombre: str = "Base"
    extra: dict = field(default_factory=dict)


# ---------- Parámetros (todos de archivos) ----------
def benchmarks() -> dict:
    """Costo por clic y conversión de la categoría Travel (D13) y la mediana de conversión de Facebook."""
    b = pd.read_csv(BENCHMARKS[-1])
    t = b[b.categoria == "Travel"].set_index(["clave_pagina", "metrica"]).valor
    fb = b[b.clave_pagina.str.contains("facebook") & (b.metrica == "Average CVR")].valor
    return {"cpc_google_usd": float(t["wordstream_google_2025", "Average CPC"]),
            "cvr_google": float(t["wordstream_google_2025", "Average CVR"]) / 100,
            "cpc_facebook_usd": float(t["wordstream_facebook_2025", "Average CPC"]),
            "cpc_facebook_localiq_usd": float(t["localiq_facebook_2026", "Average CPC"]),
            "cvr_facebook_mediana": round(float(fb.median()) / 100, 4),
            "archivo": str(BENCHMARKS[-1].relative_to(RAIZ))}


def pesos_por_dolar() -> tuple[float, str]:
    """Último mes completo de FRED (no se usa un mes a medias)."""
    f = pd.read_parquet(SILVER / "fred_mensual")
    f = f[~f.mes_incompleto_flag & f.pesos_por_dolar.notna()].sort_values("periodo").iloc[-1]
    return float(f.pesos_por_dolar), str(pd.Timestamp(f.periodo).date())


def tabla_meses(golpe: float = 0.0) -> pd.DataFrame:
    """Lugar × mes con nivel de temporada, capacidad probada y los tres escenarios del Monte Carlo.
    Solo entran los meses que tienen calendario Y escenarios para los 3 lugares (no se extrapola)."""
    cal = pd.read_parquet(GOLD / "pronostico_calendario.parquet")
    cal = cal[cal.lugar.isin(SUR)][["lugar", "periodo", "nivel"]]
    esc = pd.read_parquet(GOLD / "pronostico_escenarios.parquet")
    esc = esc[esc.lugar.isin(SUR) & (esc.golpe_tormenta_supuesto == golpe)]
    t = cal.merge(esc[["lugar", "periodo", "capacidad_probada", "riesgo_rebasar_capacidad"]
                      + [c for c, _ in ESCENARIOS.values()]], on=["lugar", "periodo"], how="inner")
    completos = t.groupby("periodo").lugar.nunique()
    t = t[t.periodo.isin(completos[completos == len(SUR)].index)].sort_values(["periodo", "lugar"])
    t["libre"] = 1 - t.probable_p50_est / t.capacidad_probada  # fracción de la capacidad que queda libre
    return t.reset_index(drop=True)


def canales(s: Supuestos) -> dict:
    """Conversiones por peso de cada canal: r = conversión ÷ (costo por clic en dólares × pesos por dólar)."""
    b = benchmarks()
    tc, _ = pesos_por_dolar()
    cvr_fb = b["cvr_google"] if s.cvr_facebook is None else s.cvr_facebook
    cpc_fb = b["cpc_facebook_usd"] if s.cpc_facebook_usd is None else s.cpc_facebook_usd
    return {"Google": {"cpc_mxn": b["cpc_google_usd"] * tc, "cvr": b["cvr_google"]},
            "Facebook": {"cpc_mxn": cpc_fb * tc, "cvr": cvr_fb}}


# ---------- El modelo ----------
def resolver(s: Supuestos = Supuestos()) -> dict:
    t = tabla_meses(s.golpe_tormenta)
    meses = sorted(t.periodo.unique())
    B = s.presupuesto_anual * len(meses) / 12  # prorrateo a los meses con pronóstico
    ch = canales(s)
    r = {c: v["cvr"] / v["cpc_mxn"] for c, v in ch.items()}
    filas = {(row.periodo, row.lugar): row for row in t.itertuples()}
    idx = list(filas)
    U = max(r.values()) * B  # cota de conversiones en una celda

    m = pulp.LpProblem("presupuesto", pulp.LpMaximize)
    x = {(p, l, c): pulp.LpVariable(f"x_{i}_{c}", lowBound=0) for i, (p, l) in enumerate(idx) for c in ch}
    y = {(e, p, l): pulp.LpVariable(f"y_{e}_{i}", cat="Binary") for e in ESCENARIOS for i, (p, l) in enumerate(idx)}
    w = {(e, p, l): pulp.LpVariable(f"w_{e}_{i}", lowBound=0) for e in ESCENARIOS for i, (p, l) in enumerate(idx)}
    conv = {(p, l): pulp.lpSum(r[c] * x[p, l, c] for c in ch) for (p, l) in idx}
    m += (pulp.lpSum(x.values()) <= B, "presupuesto")
    for (p, l), f in filas.items():
        if s.temporada_alta and f.nivel == "alta":
            for c in ch:
                x[p, l, c].upBound = 0
        if s.capacidad:
            m += (conv[p, l] <= f.capacidad_probada - f.probable_p50_est, f"cap_{idx.index((p, l))}")
        if s.ocupacion_max is not None:
            holgura = s.ocupacion_max * f.capacidad_probada - f.probable_p50_est
            if holgura <= 0:
                for c in ch:
                    x[p, l, c].upBound = 0
            else:
                m += (conv[p, l] <= holgura, f"pareto_{idx.index((p, l))}")
        for e, (col, _) in ESCENARIOS.items():
            base = getattr(f, col)
            M = max(base + U - f.capacidad_probada, 0)
            # Recurso: si el escenario e + la campaña rebasa la capacidad, el anuncio se pausa (y = 0).
            m += (base + conv[p, l] <= f.capacidad_probada + M * (1 - y[e, p, l]), f"rec_{e}_{idx.index((p, l))}")
            m += (w[e, p, l] <= conv[p, l], f"w1_{e}_{idx.index((p, l))}")
            m += (w[e, p, l] <= U * y[e, p, l], f"w2_{e}_{idx.index((p, l))}")
    sin_meses = [l for l in SUR if all(x[p, l2, c].upBound == 0 for (p, l2, c) in x if l2 == l)]
    if s.equidad:
        for l in SUR:
            if l in sin_meses:  # en la frontera de Pareto un lugar puede quedarse sin meses: su piso no aplica
                continue
            m += (pulp.lpSum(x[p, l2, c] for (p, l2, c) in x if l2 == l) >= s.piso_equidad * B, f"equidad_{SUR.index(l)}")
    if s.canales:
        for c in ch:
            m += (pulp.lpSum(x[p, l, c2] for (p, l, c2) in x if c2 == c) <= s.tope_canal * B, f"canal_{c}")

    esperado = pulp.lpSum(ESCENARIOS[e][1] * w[e, p, l] for (e, p, l) in w)
    # Paso 1: máximo de visitantes esperados.
    m.setObjective(esperado)
    m.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[m.status] != "Optimal":
        return {"estado": pulp.LpStatus[m.status], "supuestos": s}
    z1 = pulp.value(esperado)
    # Paso 2 (desempate, decisión de Brandon: "proporcional al espacio"): con al menos esos visitantes, cada mes
    # permitido recibe dinero en proporción a su espacio libre, con la misma mezcla de canales:
    #   meta[m, l, c] = libre[m, l] / Σ libre (celdas permitidas) × total del canal c
    # y se minimiza Σ |x − meta|. Permitida = no es temporada alta, cabe en la regla de Pareto y ni el escenario
    # bueno rebasa la capacidad (así el recurso nunca tiene que pausar un mes donde se gastó).
    m += (esperado >= z1 * (1 - 1e-7), "lexicografico")
    permitida = {k: (x[k + (next(iter(ch)),)].upBound != 0) and f.bueno_p90_est < f.capacidad_probada
                 for k, f in filas.items()}
    total_libre = sum(filas[k].libre for k in idx if permitida[k])
    d = {k: pulp.LpVariable(f"d_{idx.index(k[:2])}_{k[2]}", lowBound=0) for k in x}
    for (p, l, c) in x:
        meta = (filas[p, l].libre / total_libre if permitida[p, l] else 0.0) * pulp.lpSum(
            x[p2, l2, c] for (p2, l2, c2) in x if c2 == c)
        m += (d[p, l, c] >= x[p, l, c] - meta, f"d1_{idx.index((p, l))}_{c}")
        m += (d[p, l, c] >= meta - x[p, l, c], f"d2_{idx.index((p, l))}_{c}")
    m.setObjective(-pulp.lpSum(d.values()))
    m.solve(pulp.PULP_CBC_CMD(msg=False))
    desvio = sum(v.value() for v in d.values()) / B

    plan = pd.DataFrame([{"periodo": p, "lugar": l, "canal": c, "pesos": x[p, l, c].value() or 0.0,
                          "conversiones_est": (x[p, l, c].value() or 0.0) * r[c]} for (p, l, c) in x])
    gasto = plan.groupby(["periodo", "lugar"]).pesos.sum()
    # Una pausa solo importa donde hay dinero puesto (en una celda sin gasto, y no cambia nada).
    pausas = pd.DataFrame([{"escenario": e, "periodo": p, "lugar": l, "encendido": round(y[e, p, l].value()),
                            "pesos": gasto[p, l]} for (e, p, l) in y])
    pausas = pausas[pausas.pesos > 0.5]
    return {"estado": "Optimal", "supuestos": s, "presupuesto": B, "meses": meses, "canales": ch, "r": r,
            "visitantes_esperados": pulp.value(esperado), "plan": plan, "pausas": pausas, "tabla": t,
            "permitida": permitida, "desvio_proporcional": desvio, "sin_meses": sin_meses, "modelo": m, "x": x, "y": y, "idx": idx}


def precios_sombra(sol: dict) -> pd.DataFrame:
    """Fija las y de la solución y resuelve el LP del paso 1: el precio sombra de cada regla es cuántas conversiones
    gana el objetivo si esa regla se afloja en una unidad (un peso, en presupuesto, equidad y canal)."""
    s, t = sol["supuestos"], sol["tabla"]
    m = sol["modelo"]
    for v in sol["y"].values():
        v.lowBound = v.upBound = round(v.value())
        v.cat = pulp.LpContinuous
    del m.constraints["lexicografico"]
    # El objetivo del paso 1 se rearma con las w (variables "w_<escenario>_<celda>").
    w = [v for v in m.variables() if v.name.startswith("w_")]
    m.setObjective(pulp.lpSum(ESCENARIOS[v.name.split("_")[1]][1] * v for v in w))
    m.solve(pulp.PULP_CBC_CMD(msg=False))
    filas = []
    for nombre, c in m.constraints.items():
        if nombre.startswith(("presupuesto", "equidad", "canal")):
            filas.append({"regla": nombre, "precio_sombra": c.pi, "holgura": c.slack})
    return pd.DataFrame(filas)


def costo_de_reglas(base: Supuestos = Supuestos()) -> pd.DataFrame:
    """Cuántos visitantes esperados cuesta cada regla: se resuelve sin ella y se compara con el modelo completo."""
    v0 = resolver(base)["visitantes_esperados"]
    filas = []
    for regla, texto in [("temporada_alta", "Cero anuncio en temporada alta"), ("capacidad", "Tope de capacidad probada"),
                         ("equidad", "Piso de equidad de 15 % por lugar"), ("canales", "Tope de 70 % por canal")]:
        v = resolver(replace(base, **{regla: False}, nombre=f"sin {regla}"))["visitantes_esperados"]
        filas.append({"regla": texto, "visitantes_con_regla": v0, "visitantes_sin_regla": v,
                      "costo_visitantes": v - v0, "costo_pct": (v / v0 - 1) * 100})
    return pd.DataFrame(filas)


def pareto(base: Supuestos = Supuestos(), topes=(1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.45, 0.4, 0.35, 0.3)) -> pd.DataFrame:
    """Frontera de Pareto por ε-restricción: si ningún lugar puede pasar del ε de su capacidad probada en el escenario
    probable, ¿cuántos visitantes esperados trae la campaña?"""
    filas = []
    for e in topes:
        sol = resolver(replace(base, ocupacion_max=e, nombre=f"ocupacion ≤ {e:.0%}"))
        filas.append({"ocupacion_max": e, "estado": sol["estado"],
                      "visitantes_esperados": sol.get("visitantes_esperados"),
                      "lugares_sin_meses": ", ".join(sol.get("sin_meses", [])) or None})
    return pd.DataFrame(filas)


def sensibilidad() -> pd.DataFrame:
    b = benchmarks()
    casos = [Supuestos(),
             Supuestos(cvr_facebook=0.03, nombre="Conversión Facebook 3 %"),
             Supuestos(cvr_facebook=b["cvr_facebook_mediana"],
                       nombre=f"Conversión Facebook {b['cvr_facebook_mediana']:.2%} (mediana de industrias)"),
             Supuestos(cpc_facebook_usd=b["cpc_facebook_localiq_usd"], nombre="Clic de Facebook a $0.42 (LocaliQ 2026)"),
             Supuestos(golpe_tormenta=0.25, nombre="Golpe de tormenta 25 %"),
             Supuestos(golpe_tormenta=0.5, nombre="Golpe de tormenta 50 %"),
             Supuestos(presupuesto_anual=500_000, nombre="Presupuesto $500,000 al año"),
             Supuestos(presupuesto_anual=1_000_000, nombre="Presupuesto $1,000,000 al año")]
    filas = []
    for s in casos:
        sol = resolver(s)
        p = sol["plan"]
        lug = p.groupby("lugar").pesos.sum() / sol["presupuesto"] * 100
        can = p.groupby("canal").pesos.sum() / sol["presupuesto"] * 100
        pausados = sol["pausas"].query("encendido == 0")
        filas.append({"caso": s.nombre, "presupuesto_periodo": sol["presupuesto"],
                      "visitantes_esperados": sol["visitantes_esperados"],
                      "pesos_por_visitante": sol["presupuesto"] / sol["visitantes_esperados"],
                      **{f"pct_{l}": lug.get(l, 0.0) for l in SUR}, **{f"pct_{c}": can.get(c, 0.0) for c in sol["canales"]},
                      "pausas_en_escenarios": len(pausados)})
    return pd.DataFrame(filas)


def construir() -> dict:
    sol = resolver()
    plan = sol["plan"]
    plan.to_parquet(GOLD / "presupuesto_plan.parquet", index=False)
    sol["pausas"].to_parquet(GOLD / "presupuesto_pausas.parquet", index=False)
    reglas = costo_de_reglas()
    reglas.to_parquet(GOLD / "presupuesto_reglas.parquet", index=False)
    par = pareto()
    par.to_parquet(GOLD / "presupuesto_pareto.parquet", index=False)
    sen = sensibilidad()
    sen.to_parquet(GOLD / "presupuesto_sensibilidad.parquet", index=False)
    sombra = precios_sombra(resolver())
    sombra.to_parquet(GOLD / "presupuesto_precios_sombra.parquet", index=False)
    b, (tc, mes_tc) = benchmarks(), pesos_por_dolar()
    print(f"Meses con pronóstico: {sol['meses'][0].date()} → {sol['meses'][-1].date()} ({len(sol['meses'])}); "
          f"presupuesto del periodo ${sol['presupuesto']:,.0f}; {tc:.2f} pesos por dólar ({mes_tc})")
    for c, v in sol["canales"].items():
        print(f"  {c}: clic ${v['cpc_mxn']:.2f} MXN, conversión {v['cvr']:.2%} → {sol['r'][c] * 1000:.2f} por cada $1,000")
    print(f"Visitantes esperados: {sol['visitantes_esperados']:,.1f}; desvío del reparto proporcional "
          f"{sol['desvio_proporcional']:.4f}; meses permitidos {sum(sol['permitida'].values())} de {len(sol['permitida'])}")
    print(plan.pivot_table(index="periodo", columns=["lugar", "canal"], values="pesos", aggfunc="sum").round(0).to_string())
    print(reglas.round(2).to_string(index=False)); print(par.to_string(index=False))
    print(sen.round(1).to_string(index=False)); print(sombra.to_string(index=False))
    return sol


if __name__ == "__main__":
    construir()
