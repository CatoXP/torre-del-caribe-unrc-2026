# Autor: Brandon Uriel García Sánchez
# Módulo: Pronóstico
# Qué hace:          Pieza 4 de la Fase 5 (Estocástico). Para los próximos 12 meses de cada lugar del sur:
#                      1. probabilidad de tormenta por mes (modelo de Poisson con los 31 eventos de 1966–2025);
#                      2. Monte Carlo de 10,000 futuros posibles → escenario malo / probable / bueno (percentiles 10 / 50 /
#                         90) y riesgo de rebasar la capacidad probada;
#                      3. sensibilidad a la lluvia, al tipo de cambio y al supuesto del golpe de una tormenta.
# Por qué así:       - Cada futuro simulado = pronóstico del modelo elegido × un año COMPLETO de errores reales del pasado
#                      (se toma un origen del origen móvil al azar y se copian sus errores de los 12 horizontes). Así se
#                      conserva que un año flojo suele ser flojo varios meses seguidos; sortear cada mes por separado haría
#                      el rango del año demasiado angosto. Si a ese origen le falta algún horizonte, ese mes se sortea de
#                      los errores del mismo tramo de horizonte.
#                    - Tormenta (decisión de Brandon, "Supuesto con barrido"): N_m ~ Poisson(λ_m) con λ_m MEDIDO; su efecto
#                      en visitantes NO se pudo estimar (solo 3 meses con tormenta en los datos usables: Earl 2016,
#                      Franklin 2017 y Lisa 2022), así que se prueba como SUPUESTO: el mes con tormenta pierde 0 %, 25 % o
#                      50 % de visitantes. Nunca se presenta como dato.
#                    - Sin efecto de la campaña (decisión de Brandon): estos escenarios son "lo que pasaría de todos
#                      modos"; la campaña entra en la Fase 6 con los costos y conversiones reunidos (D13).
#                    - Capacidad probada (decisión de Brandon): el mes más alto que cada lugar ya recibió en su historia
#                      (mismo criterio de "capacidad probada" de la selección de regiones). No es la capacidad física
#                      oficial, y así se dice.
#                    - Sensibilidades medidas con la misma regresión de la pieza 3 (nivel por tramo + mes): lluvia (Open-
#                      Meteo) y tipo de cambio (FRED, promedio mensual de pesos por dólar).
# Datos de entrada:  datos/gold/pronostico_{series, mes, backtest, eleccion}; datos/silver/{huracanes, clima_diario,
#                    fred_mensual}.
# Alimenta a:        Fase 6: cuánto presupuesto reservar para contingencias en los meses con riesgo de tormenta, qué meses
#                    no conviene empujar (riesgo de rebasar la capacidad probada) y el escenario malo con el que se prueba
#                    que el plan aguanta.

from pathlib import Path

import numpy as np
import pandas as pd

from torre.pronostico import modelos

RAIZ = Path(__file__).resolve().parents[3]
GOLD = RAIZ / "datos" / "gold"
SILVER = RAIZ / "datos" / "silver"
R = 10_000
SEMILLA = 2026
GOLPES_SUPUESTOS = (0.0, 0.25, 0.50)   # SUPUESTO: fracción de visitantes que se pierde el mes de una tormenta
ANIO_INICIO, ANIO_FIN = 1966, 2025


# ---------- 1. Poisson de tormentas ----------
def poisson_tormentas() -> pd.DataFrame:
    """λ_m = eventos que empezaron en el mes m ÷ 60 años; P(al menos una) = 1 − e^(−λ_m)."""
    from torre.base.silver_huracanes import eventos_sur

    ev = eventos_sur(pd.read_parquet(SILVER / "huracanes"))
    anios = ANIO_FIN - ANIO_INICIO + 1
    n = ev.mes.value_counts().reindex(range(1, 13), fill_value=0)
    t = pd.DataFrame({"mes": range(1, 13), "eventos": n.to_numpy()})
    t["lambda"] = t.eventos / anios
    t["prob_tormenta"] = 1 - np.exp(-t["lambda"])
    return t


# ---------- 2. Monte Carlo ----------
def errores_por_origen(backtest: pd.DataFrame, serie: str, modelo: str) -> tuple[dict, dict]:
    """Errores con signo en logaritmos, ln(real ÷ pronóstico): por origen (vector de 12 horizontes, con huecos) y por
    tramo de horizonte (para sortear los horizontes que le falten a un origen)."""
    b = backtest[(backtest.serie == serie) & (backtest.modelo == modelo) & (backtest.pronostico > 0)].copy()
    b["e"] = np.log(b.real / b.pronostico)
    por_origen = {o: g.set_index("horizonte").e.reindex(range(1, 13)).to_numpy() for o, g in b.groupby("origen")}
    por_tramo = {k: g.e.to_numpy() for k, g in b.groupby("tramo_h")}
    return por_origen, por_tramo


def capacidad_probada(t: pd.DataFrame, serie: str) -> tuple[float, pd.Timestamp]:
    s = t[(t.serie == serie) & t.entrena_flag]
    fila = s.loc[s.valor.idxmax()]
    return float(fila.valor), fila.periodo


def simular(pron: pd.DataFrame, backtest: pd.DataFrame, poisson: pd.DataFrame, golpe: float,
            rng: np.random.Generator) -> np.ndarray:
    """Matriz R × 12 de futuros posibles para una serie (pron = sus 12 meses de pronóstico, ordenados)."""
    serie, modelo = pron.serie.iloc[0], pron.modelo.iloc[0]
    por_origen, por_tramo = errores_por_origen(backtest, serie, modelo)
    origenes = list(por_origen)
    tramo = modelos_tramo(pron.horizonte.to_numpy())
    E = np.array([por_origen[origenes[i]] for i in rng.integers(len(origenes), size=R)])  # R × 12 con huecos
    for j, k in enumerate(tramo):
        vacios = np.isnan(E[:, j])
        E[vacios, j] = rng.choice(por_tramo[k], size=vacios.sum())
    D = pron.esperado_est.to_numpy()[None, :] * np.exp(E)
    if golpe > 0 and pron.papel.iloc[0] == "promovida":
        lam = pron.periodo.dt.month.map(poisson.set_index("mes")["lambda"]).to_numpy()
        tormenta = rng.poisson(lam[None, :], size=D.shape) > 0
        D = np.where(tormenta, D * (1 - golpe), D)
    return D


def modelos_tramo(h: np.ndarray) -> list[str]:
    return ["1–3" if x <= 3 else "4–6" if x <= 6 else "7–12" for x in h]


def escenarios() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Por serie, supuesto de golpe y mes: escenarios malo / probable / bueno y riesgo de rebasar la capacidad probada.
    Además, una tabla con el total de los 12 meses."""
    t = pd.read_parquet(GOLD / "pronostico_series.parquet")
    f = pd.read_parquet(GOLD / "pronostico_mes.parquet")
    b = pd.read_parquet(GOLD / "pronostico_backtest.parquet")
    p = poisson_tormentas()
    rng = np.random.default_rng(SEMILLA)
    meses, anual = [], []
    for serie, pron in f.groupby("serie"):
        pron = pron.sort_values("periodo").reset_index(drop=True)
        cap, cap_mes = capacidad_probada(t, serie)
        golpes = GOLPES_SUPUESTOS if pron.papel.iloc[0] == "promovida" else (0.0,)
        for golpe in golpes:
            D = simular(pron, b, p, golpe, rng)
            q10, q50, q90 = np.percentile(D, [10, 50, 90], axis=0)
            for j, fila in pron.iterrows():
                meses.append({"serie": serie, "lugar": fila.lugar, "papel": fila.papel, "periodo": fila.periodo,
                              "golpe_tormenta_supuesto": golpe, "esperado_est": fila.esperado_est,
                              "malo_p10_est": q10[j], "probable_p50_est": q50[j], "bueno_p90_est": q90[j],
                              "prob_tormenta": float(p.set_index("mes").prob_tormenta[fila.periodo.month])
                              if fila.papel == "promovida" else np.nan,
                              "capacidad_probada": cap, "capacidad_probada_mes": cap_mes,
                              "riesgo_rebasar_capacidad": float((D[:, j] > cap).mean())})
            total = D.sum(axis=1)
            anual.append({"serie": serie, "lugar": pron.lugar.iloc[0], "golpe_tormenta_supuesto": golpe,
                          "malo_p10_est": np.percentile(total, 10), "probable_p50_est": np.percentile(total, 50),
                          "bueno_p90_est": np.percentile(total, 90), "esperado_modelo_est": pron.esperado_est.sum(),
                          "riesgo_algun_mes_sobre_capacidad": float((D > cap).any(axis=1).mean())})
    return pd.DataFrame(meses), pd.DataFrame(anual)


# ---------- 3. Sensibilidad: lluvia y tipo de cambio ----------
def sensibilidad() -> pd.DataFrame:
    """Efecto medido de +100 mm de lluvia sobre lo normal y de +1 peso por dólar, con la regresión de la pieza 3
    (nivel por tramo + mes + la variable). Efecto en % = e^coef − 1. Solo meses que entrenan."""
    import statsmodels.api as sm

    t = pd.read_parquet(GOLD / "pronostico_series.parquet")
    fx = pd.read_parquet(SILVER / "fred_mensual", columns=["periodo", "pesos_por_dolar"])
    fx["periodo"] = pd.to_datetime(fx.periodo)
    fx = fx.set_index("periodo").pesos_por_dolar
    filas = []
    for serie, s in t[t.papel == "promovida"].groupby("serie"):
        x = s.sort_values("periodo").set_index("periodo")
        tramo = modelos._tramos(x)
        cl = modelos.clima_mensual(modelos.PUNTO_CLIMA[s.lugar.iloc[0]])
        normal = cl.groupby("mes").lluvia_mm.mean()
        variables = {"lluvia (+100 mm sobre lo normal)": (cl.reindex(tramo.index).lluvia_mm
                                                            - tramo.index.month.map(normal).to_numpy()) / 100,
                     "tipo de cambio (+1 peso por dólar)": fx.reindex(tramo.index)}
        for nombre, v in variables.items():
            X = pd.DataFrame(index=tramo.index)
            for k in sorted(tramo.unique()):
                X[f"t{k}"] = (tramo == k).astype(float)
            for m in range(2, 13):
                X[f"m{m}"] = (X.index.month == m).astype(float)
            X["v"] = v.to_numpy()
            ok = X.notna().all(axis=1)
            X = X[ok].loc[:, X[ok].abs().sum() > 0]
            r = sm.OLS(np.log(x.valor[X.index]).to_numpy(), X.to_numpy()).fit()
            i = list(X.columns).index("v")
            filas.append({"serie": serie, "lugar": s.lugar.iloc[0], "variable": nombre, "coeficiente": r.params[i],
                          "efecto_pct": (np.exp(r.params[i]) - 1) * 100, "p_valor": r.pvalues[i], "meses": int(ok.sum()),
                          "significativo_flag": r.pvalues[i] < 0.05})
    return pd.DataFrame(filas)


def correr():
    p = poisson_tormentas()
    meses, anual = escenarios()
    sens = sensibilidad()
    p.to_parquet(GOLD / "pronostico_poisson_tormentas.parquet", index=False)
    meses.to_parquet(GOLD / "pronostico_escenarios.parquet", index=False)
    anual.to_parquet(GOLD / "pronostico_escenarios_anual.parquet", index=False)
    sens.to_parquet(GOLD / "pronostico_sensibilidad.parquet", index=False)
    return p, meses, anual, sens


if __name__ == "__main__":
    import warnings
    warnings.simplefilter("ignore")
    p, meses, anual, sens = correr()
    pd.set_option("display.width", 220)
    print(p.round(4).to_string(index=False))
    print(anual.round(3).to_string(index=False))
    print(sens.round(4).to_string(index=False))
    x = meses[meses.golpe_tormenta_supuesto == 0]
    print(x.groupby("lugar").riesgo_rebasar_capacidad.max().round(4).to_dict())
    print(x.groupby("lugar")[["capacidad_probada", "capacidad_probada_mes"]].first().to_string())
