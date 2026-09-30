# Autor: Brandon Uriel García Sánchez
# Módulo: Pronóstico
# Qué hace:          Pieza 3 de la Fase 5 (ML). Pronostica cada serie de 1 a 12 meses hacia adelante y mide el error con
#                    ORIGEN MÓVIL: se "regresa el reloj" a cada mes del pasado, se pronostica con lo que se sabía entonces
#                    y se compara con lo que pasó. Modelos:
#                      0. Línea base (ingenuo estacional): el mes pronosticado vale lo mismo que ese mes la última vez que
#                         hubo dato (ej. marzo de 2026 = marzo de 2025).
#                      1. Holt-Winters con forma del año fija: quita la temporada con los índices de la pieza 2, sigue el
#                         nivel con suavizamiento exponencial y vuelve a poner la temporada. Dos variantes: con tendencia
#                         amortiguada (la del plan) y sin tendencia (solo nivel). La segunda se agregó después de ver que
#                         la tendencia, aprendida en tramos cortos que incluyen la recuperación tras reabrir, se disparaba
#                         a 7–12 meses (Bahía: 33 % de error contra 13 % de la línea base). Se declara.
#                      2. Regresión con clima: log(visitantes) = nivel del tramo + mes + anomalía de lluvia + tormenta.
#                         Al pronosticar se usa el clima "normal" del mes (no se conoce el clima futuro): anomalía de
#                         lluvia 0 y la frecuencia histórica de tormentas de ese mes, ambas calculadas antes del origen.
#                      3. Gradient Boosting con rezagos: aprende de pares (origen pasado → mes destino) con el último
#                         valor, el promedio de los 3 últimos, el mismo mes del año anterior, el horizonte y el mes.
# Por qué así:       - Origen móvil y no una sola partición: con 60–90 meses útiles, un solo corte da pocas pruebas; el
#                      origen móvil da cientos de pronósticos y deja ver el error por horizonte (1–3, 4–6, 7–12 meses).
#                    - Holt-Winters clásico aprende la temporada de la serie continua y necesita ≥ 24 meses seguidos. Desde
#                      las reaperturas solo hay 20 (Bahía) y 17 (Ruta): no se puede. Por eso la temporada sale de los años
#                      completos ANTERIORES al origen (decisión de Brandon "Hueco + forma del año") y el nivel, del tramo
#                      posterior a la última reapertura. Nunca se usa información posterior al origen.
#                    - Escala multiplicativa (la temporada es proporcional al nivel, pieza 2) y error medido en MAE (en
#                      las unidades de la serie) y MAPE (%, comparable entre series; no hay ceros en meses útiles).
#                    - Solo se evalúan meses destino que entrenan (sin cierre, mes parcial ni pandemia).
# Datos de entrada:  datos/gold/pronostico_series.parquet (pieza 1); datos/silver/clima_diario y huracanes (Silver).
# Alimenta a:        Qué modelo usa el calendario de la campaña para decir cuántos visitantes esperar cada mes (y, en la
#                    Fase 6, cuánta capacidad libre hay para atraer gente sin saturar).

import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from torre.pronostico.forma import indice_estacional, razones

RAIZ = Path(__file__).resolve().parents[3]
GOLD = RAIZ / "datos" / "gold"
HORIZONTE = 12
MIN_TRAMO = 3        # meses útiles seguidos mínimos desde la última reapertura para poder pronosticar
PRIMER_ORIGEN = {"visitantes INAH": "2019-01-01", "Belice": "2023-06-01", "Cancún": "2023-01-01"}


def primer_origen(serie: str) -> pd.Timestamp:
    """Primer origen: cuando ya hay al menos un año completo antes para calcular la forma del año (INAH 2016–2018,
    Belice 2019 + medio año del tramo nuevo, Cancún 2022)."""
    return pd.Timestamp(next(v for k, v in PRIMER_ORIGEN.items() if k in serie))


def forma_hasta(s: pd.DataFrame, origen: pd.Timestamp) -> pd.Series | None:
    """Índices de la forma del año usando SOLO años completos que terminaron antes del origen (sin ver el futuro)."""
    r = razones(s[s.periodo <= origen])
    r = r[r.index < origen.year + (1 if origen.month == 12 else 0)]
    return indice_estacional(r) if len(r) else None


def tramo_actual(s: pd.DataFrame, origen: pd.Timestamp) -> pd.Series:
    """Meses útiles del tramo en curso al origen (desde el último mes que no entrena)."""
    x = s[s.periodo <= origen].set_index("periodo")
    malos = x.index[~x.entrena_flag]
    desde = malos.max() if len(malos) else x.index.min() - pd.offsets.MonthBegin(1)
    return x.valor[(x.index > desde) & x.entrena_flag]


def ingenuo_estacional(s: pd.DataFrame, origen: pd.Timestamp, destinos: pd.DatetimeIndex) -> np.ndarray:
    """Cada mes destino = el último valor útil de ese mismo mes del año, visto desde el origen."""
    x = s[(s.periodo <= origen) & s.entrena_flag]
    ultimo = x.sort_values("periodo").groupby(x.periodo.dt.month).valor.last()
    return np.array([ultimo.get(d.month, np.nan) for d in destinos])


def holt_winters_forma_fija(s: pd.DataFrame, origen: pd.Timestamp, destinos: pd.DatetimeIndex) -> np.ndarray:
    """Desestacionaliza el tramo actual con la forma del año previa al origen, ajusta nivel + tendencia amortiguada
    (suavizamiento exponencial de Holt) y multiplica el pronóstico por el índice de cada mes destino."""
    from statsmodels.tsa.holtwinters import ExponentialSmoothing

    S = forma_hasta(s, origen)
    y = tramo_actual(s, origen)
    if S is None or len(y) < MIN_TRAMO:
        return np.full(len(destinos), np.nan)
    z = (y / y.index.month.map(S).values).to_numpy()
    h = [(d.year - origen.year) * 12 + d.month - origen.month for d in destinos]
    if len(z) < 6:  # tramo muy corto: nivel = promedio desestacionalizado (sin tendencia)
        nivel = np.full(max(h), z.mean())
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            m = ExponentialSmoothing(z, trend="add", damped_trend=True, initialization_method="estimated").fit()
        nivel = m.forecast(max(h))
    return np.array([nivel[k - 1] * S[d.month] for k, d in zip(h, destinos)])


def holt_winters_sin_tendencia(s: pd.DataFrame, origen: pd.Timestamp, destinos: pd.DatetimeIndex) -> np.ndarray:
    """Igual que la anterior pero solo con nivel (suavizamiento exponencial simple): el pronóstico desestacionalizado es
    plano y la temporada la pone la forma del año."""
    from statsmodels.tsa.holtwinters import ExponentialSmoothing

    S = forma_hasta(s, origen)
    y = tramo_actual(s, origen)
    if S is None or len(y) < MIN_TRAMO:
        return np.full(len(destinos), np.nan)
    z = (y / y.index.month.map(S).values).to_numpy()
    if len(z) < 6:
        nivel = z.mean()
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            nivel = ExponentialSmoothing(z, initialization_method="estimated").fit().forecast(1)[0]
    return np.array([nivel * S[d.month] for d in destinos])


# ---------- Clima: lluvia del mes y tormentas que afectan al sur ----------
PUNTO_CLIMA = {"Bahía Calderitas–Oxtankah": "chetumal", "Ruta arqueológica del sur": "kohunlich",
               "Chetumal": "chetumal", "Cancún": "cancun"}
_CLIMA: dict = {}


def clima_mensual(punto: str) -> pd.DataFrame:
    """Lluvia total de cada mes (mm) en el punto y si ese mes empezó una tormenta que afectó al sur (0/1)."""
    if punto not in _CLIMA:
        from torre.base.silver_huracanes import eventos_sur

        d = pd.read_parquet(RAIZ / "datos" / "silver" / "clima_diario", columns=["punto", "anio", "mes", "lluvia_mm"])
        d = d[d.punto == punto].assign(anio=lambda x: x.anio.astype(int))
        c = d.groupby(["anio", "mes"]).lluvia_mm.sum().reset_index()
        ev = eventos_sur(pd.read_parquet(RAIZ / "datos" / "silver" / "huracanes"))
        ev = set(zip(ev.anio.astype(int), ev.mes))
        c["tormenta"] = [int((a, m) in ev) for a, m in zip(c.anio, c.mes)]
        c["periodo"] = pd.to_datetime(dict(year=c.anio, month=c.mes, day=1))
        _CLIMA[punto] = c.set_index("periodo")
    return _CLIMA[punto]


def _tramos(x: pd.DataFrame) -> pd.Series:
    """Número de tramo de cada mes útil: sube cada vez que la serie pasa por meses que no entrenan (cierre, pandemia)."""
    return (~x.entrena_flag).cumsum()[x.entrena_flag]


def regresion_con_clima(s: pd.DataFrame, origen: pd.Timestamp, destinos: pd.DatetimeIndex) -> np.ndarray:
    """Mínimos cuadrados sobre log(valor): un nivel por tramo + 11 meses + anomalía de lluvia (cientos de mm) + tormenta.
    El pronóstico usa el nivel del tramo actual y el clima normal del mes destino (anomalía 0; tormenta = frecuencia
    histórica de ese mes, desde 1966 y antes del origen)."""
    x = s[s.periodo <= origen].sort_values("periodo").set_index("periodo")
    if len(tramo_actual(s, origen)) < MIN_TRAMO:
        return np.full(len(destinos), np.nan)
    clima = clima_mensual(PUNTO_CLIMA[s.lugar.iloc[0]])
    antes = clima[clima.index <= origen]
    normal = antes.groupby("mes").lluvia_mm.mean()
    frec_tormenta = antes[antes.anio >= 1966].groupby("mes").tormenta.mean()
    tramo = _tramos(x)
    y = np.log(x.valor[tramo.index])
    cl = clima.reindex(tramo.index)
    X = pd.DataFrame(index=tramo.index)
    for k in sorted(tramo.unique()):
        X[f"tramo_{k}"] = (tramo == k).astype(float)
    for m in range(2, 13):
        X[f"mes_{m}"] = (X.index.month == m).astype(float)
    X["lluvia_anom"] = (cl.lluvia_mm - cl.mes.map(normal)).to_numpy() / 100
    X["tormenta"] = cl.tormenta.to_numpy()
    X = X.loc[:, X.abs().sum() > 0]  # quita columnas sin información (ej. un mes que nunca aparece)
    beta, *_ = np.linalg.lstsq(X.to_numpy(), y.to_numpy(), rcond=None)
    b = dict(zip(X.columns, beta))
    ult = f"tramo_{tramo.iloc[-1]}"
    return np.array([np.exp(b[ult] + b.get(f"mes_{d.month}", 0.0)
                            + b.get("tormenta", 0.0) * frec_tormenta.get(d.month, 0.0)) for d in destinos])


def _rasgos(x: pd.Series, o: pd.Timestamp, d: pd.Timestamp) -> list | None:
    """Rasgos de un par (origen o → destino d) usando solo meses útiles hasta o (x = valores útiles indexados por mes)."""
    antes = x[x.index <= o]
    if len(antes) < 3:
        return None
    mismo = antes[antes.index.month == d.month]
    return [(d.year - o.year) * 12 + d.month - o.month, d.month, np.log(antes.iloc[-1]), np.log(antes.iloc[-3:].mean()),
            np.log(mismo.iloc[-1]) if len(mismo) else np.nan]


def gradient_boosting_rezagos(s: pd.DataFrame, origen: pd.Timestamp, destinos: pd.DatetimeIndex) -> np.ndarray:
    """Gradient Boosting (por histogramas) entrenado con todos los pares pasados (o' → d') con d' ≤ origen; predice
    log(valor) del mes destino. Pocos árboles, aprendizaje lento y hojas de ≥ 20 casos: hay pocos datos."""
    from sklearn.ensemble import HistGradientBoostingRegressor

    x = s[(s.periodo <= origen) & s.entrena_flag].set_index("periodo").valor
    if len(tramo_actual(s, origen)) < MIN_TRAMO:
        return np.full(len(destinos), np.nan)
    X, y = [], []
    for o in x.index:
        for d in x.index[(x.index > o) & (x.index <= o + pd.DateOffset(months=HORIZONTE))]:
            r = _rasgos(x, o, d)
            if r is not None:
                X.append(r)
                y.append(np.log(x[d]))
    if len(X) < 50:
        return np.full(len(destinos), np.nan)
    m = HistGradientBoostingRegressor(max_iter=150, learning_rate=0.05, min_samples_leaf=20, random_state=0)
    m.fit(np.array(X), np.array(y))
    return np.exp(m.predict(np.array([_rasgos(x, origen, d) for d in destinos])))


MODELOS = {"Línea base (ingenuo estacional)": ingenuo_estacional,
           "Holt-Winters con tendencia amortiguada": holt_winters_forma_fija,
           "Holt-Winters sin tendencia": holt_winters_sin_tendencia,
           "Regresión con clima": regresion_con_clima,
           "Gradient Boosting con rezagos": gradient_boosting_rezagos}


def origen_movil(t: pd.DataFrame, modelos: dict = MODELOS) -> pd.DataFrame:
    """Una fila por (serie, modelo, origen, horizonte) con el pronóstico y el valor real de los meses destino útiles."""
    filas = []
    for serie, s in t.groupby("serie"):
        s = s.sort_values("periodo").reset_index(drop=True)
        util = s.set_index("periodo").entrena_flag
        for origen in s.periodo[(s.periodo >= primer_origen(serie)) & s.entrena_flag]:
            destinos = pd.date_range(origen + pd.offsets.MonthBegin(1), periods=HORIZONTE, freq="MS")
            destinos = destinos[destinos.isin(util.index[util])]
            if len(destinos) == 0 or len(tramo_actual(s, origen)) < MIN_TRAMO:
                continue
            real = s.set_index("periodo").valor.reindex(destinos).to_numpy()
            for nombre, f in modelos.items():
                pron = f(s, origen, destinos)
                for d, p, r in zip(destinos, pron, real):
                    filas.append({"serie": serie, "modelo": nombre, "origen": origen, "destino": d,
                                  "horizonte": (d.year - origen.year) * 12 + d.month - origen.month,
                                  "pronostico": p, "real": r})
    b = pd.DataFrame(filas).dropna(subset=["pronostico"])
    # Solo pares (origen, destino) que TODOS los modelos pudieron pronosticar: comparación justa.
    n = b.groupby(["serie", "origen", "destino"]).modelo.transform("nunique")
    b = b[n == len(modelos)].copy()
    b["error_abs"] = (b.pronostico - b.real).abs()
    b["error_pct"] = b.error_abs / b.real * 100
    return b


def metricas(b: pd.DataFrame) -> pd.DataFrame:
    """MAE y MAPE por serie y modelo, en total y por tramo de horizonte; 'vs base' = MAE ÷ MAE de la línea base."""
    b = b.assign(tramo_h=pd.cut(b.horizonte, [0, 3, 6, 12], labels=["1–3", "4–6", "7–12"]))
    m = b.groupby(["serie", "modelo"]).agg(pronosticos=("error_abs", "size"), mae=("error_abs", "mean"),
                                           mape=("error_pct", "mean")).reset_index()
    base = m[m.modelo.str.startswith("Línea base")].set_index("serie").mae
    m["mae_vs_base"] = m.mae / m.serie.map(base)
    por_h = b.pivot_table(index=["serie", "modelo"], columns="tramo_h", values="error_pct", aggfunc="mean", observed=True)
    por_h.columns = [f"mape_h{c}" for c in por_h.columns]
    return m.merge(por_h.reset_index(), on=["serie", "modelo"]).round(3)


def correr():
    t = pd.read_parquet(GOLD / "pronostico_series.parquet")
    b = origen_movil(t)
    m = metricas(b)
    b.to_parquet(GOLD / "pronostico_backtest.parquet", index=False)
    m.to_parquet(GOLD / "pronostico_metricas.parquet", index=False)
    return b, m


if __name__ == "__main__":
    b, m = correr()
    pd.set_option("display.width", 220)
    print(m.to_string(index=False))
