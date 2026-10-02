# Autor: Brandon Uriel García Sánchez
# Módulo: Pronóstico
# Qué hace:          Pieza 2 de la Fase 5 (Minería). Calcula la "forma del año" de cada serie: un índice por mes que dice
#                    cuánto sube o baja ese mes contra el promedio del año (1.30 = 30 % arriba; 0.70 = 30 % abajo), qué
#                    tan fuerte es la temporada (0 = no hay temporada; 1 = el mes lo explica todo) y si cada lugar del
#                    sur sube y baja en los mismos meses que el norte (Cancún).
# Por qué así:       - Descomposición clásica MULTIPLICATIVA sobre años completos: índice del mes = promedio, entre los años
#                      completos, de (valor del mes ÷ promedio de ese año). Multiplicativa porque la temporada escala con el
#                      nivel: Kohunlich reabrió a la mitad de su nivel de 2019 y un "+2,000 visitantes en marzo" de 2019
#                      no aplica igual en 2025; un "+30 %", sí.
#                    - Solo años con los 12 meses entrenables (decisión de Brandon "Hueco + forma del año"): un año con meses
#                      cerrados tiene un promedio sesgado. Bahía y Ruta: 6 años; Belice y Cancún: 4.
#                    - Alternativa del plan descartada: STL (Loess). STL necesita una serie continua y las nuestras tienen
#                      huecos (COVID, obras de 2024); solo podría usar el tramo continuo más largo (≈ 50 meses) y tiraría
#                      los años posteriores. Se conserva como SEGUNDA OPINIÓN sobre ese tramo (correlación de índices).
#                    - Fuerza de la temporada (Wang, Smith y Hyndman, 2006) en escala logarítmica:
#                      F = max(0, 1 − Var(resto) / Var(temporada + resto)).
#                    - Descartado: marcar "meses de oportunidad" cuando Cancún pasa de 1.00 y el sur queda abajo. Cancún
#                      varía poco (0.87 a 1.08) y la regla cambiaba con diferencias de 0.02; en su lugar se mide si el
#                      sur acompaña al norte (correlación de las dos formas del año), sin umbral arbitrario.
# Datos de entrada:  datos/gold/pronostico_series.parquet (pieza 1, series.py).
# Alimenta a:        Calendario de la campaña: en qué meses conviene promover cada lugar del sur (sus meses bajos, con
#                    espacio) y en qué meses el público del norte es más grande (meses altos de Cancún). También es la
#                    parte estacional de los modelos de pronóstico (pieza 3).

from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
GOLD = RAIZ / "datos" / "gold"
SERIE_NORTE = "Cancún (referencia) · ocupación hotelera"


def anios_completos(s: pd.DataFrame) -> list[int]:
    """Años con los 12 meses entrenables (sin cierre, mes parcial ni pandemia)."""
    n = s[s.entrena_flag].groupby(s.periodo.dt.year).size()
    return sorted(int(a) for a in n[n == 12].index)


def razones(s: pd.DataFrame) -> pd.DataFrame:
    """Tabla año × mes con valor ÷ promedio del año, solo en años completos."""
    x = s[s.periodo.dt.year.isin(anios_completos(s))].copy()
    x["anio"], x["mes"] = x.periodo.dt.year, x.periodo.dt.month
    x["razon"] = x.valor / x.groupby("anio").valor.transform("mean")
    return x.pivot(index="anio", columns="mes", values="razon")


def indice_estacional(r: pd.DataFrame) -> pd.Series:
    """Promedio por mes de las razones, reescalado para que los 12 índices promedien exactamente 1."""
    i = r.mean(axis=0)
    return i / i.mean()


def fuerza_estacional(r: pd.DataFrame, indice: pd.Series) -> float:
    """F = max(0, 1 − Var(e) / Var(s + e)) en logaritmos: s = log(índice del mes), e = log(razón ÷ índice)."""
    s = np.log(indice.reindex(r.columns).to_numpy())[None, :].repeat(len(r), axis=0)
    e = np.log(r.to_numpy()) - s
    return max(0.0, 1 - np.var(e) / np.var(s + e))


def tramo_continuo(s: pd.DataFrame) -> pd.Series:
    """El tramo más largo de meses seguidos que entrenan (para la segunda opinión con STL)."""
    ok = s.sort_values("periodo").set_index("periodo").entrena_flag
    grupo = (ok != ok.shift()).cumsum()
    largos = ok[ok].groupby(grupo[ok]).size()
    g = largos.idxmax()
    return s.set_index("periodo").valor[(grupo == g) & ok]


def segunda_opinion_stl(s: pd.DataFrame, indice: pd.Series) -> tuple[float, int]:
    """Correlación entre el índice de este método y el que da STL (en logaritmos) sobre el tramo continuo más largo."""
    from statsmodels.tsa.seasonal import STL

    y = tramo_continuo(s)
    if len(y) < 24:
        return float("nan"), len(y)
    y.index = pd.DatetimeIndex(y.index, freq="MS")
    est = STL(np.log(y), period=12, robust=True).fit().seasonal
    stl = np.exp(est.groupby(est.index.month).mean())
    return float(np.corrcoef(np.log(stl.reindex(range(1, 13))), np.log(indice.reindex(range(1, 13))))[0, 1]), len(y)


def calcular(t: pd.DataFrame | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    t = pd.read_parquet(GOLD / "pronostico_series.parquet") if t is None else t
    filas, resumen = [], []
    for serie, s in t.groupby("serie"):
        r = razones(s)
        i = indice_estacional(r)
        corr, n_stl = segunda_opinion_stl(s, i)
        for m in range(1, 13):
            filas.append({"serie": serie, "lugar": s.lugar.iloc[0], "papel": s.papel.iloc[0], "mes": m,
                          "indice": round(float(i[m]), 4), "minimo_anios": round(float(r[m].min()), 4),
                          "maximo_anios": round(float(r[m].max()), 4), "n_anios": len(r)})
        resumen.append({"serie": serie, "lugar": s.lugar.iloc[0], "papel": s.papel.iloc[0],
                        "anios_usados": ", ".join(str(a) for a in r.index), "n_anios": len(r),
                        "fuerza_estacional": round(fuerza_estacional(r, i), 3),
                        "mes_mas_alto": int(i.idxmax()), "mes_mas_bajo": int(i.idxmin()),
                        "corr_con_stl": round(corr, 3), "meses_tramo_stl": n_stl})
    return pd.DataFrame(filas), pd.DataFrame(resumen)


def acompana_al_norte(forma: pd.DataFrame) -> pd.Series:
    """Correlación entre la forma del año de cada lugar del sur y la de Cancún: cerca de +1 = el sur sube y baja en los
    mismos meses que el norte; cerca de 0 = no se parecen; negativa = temporadas opuestas (el sur tiene espacio justo
    cuando el norte se llena)."""
    ancho = forma.pivot(index="mes", columns="lugar", values="indice")
    ancho = ancho.drop(columns=[c for c in ("Riviera Maya",) if c in ancho])
    return ancho.drop(columns="Cancún").apply(lambda c: np.corrcoef(np.log(c), np.log(ancho["Cancún"]))[0, 1]).round(3)


def guardar(forma: pd.DataFrame, resumen: pd.DataFrame):
    forma.to_parquet(GOLD / "pronostico_forma_anio.parquet", index=False)
    resumen.to_parquet(GOLD / "pronostico_fuerza_estacional.parquet", index=False)


if __name__ == "__main__":
    import warnings
    warnings.simplefilter("ignore")
    forma, resumen = calcular()
    guardar(forma, resumen)
    pd.set_option("display.width", 220)
    print(resumen.drop(columns=["lugar", "papel"]).to_string(index=False))
    print(forma.pivot(index="mes", columns="lugar", values="indice").round(2).to_string())
    print("Correlación de la forma del año con Cancún:", acompana_al_norte(forma).to_dict())
