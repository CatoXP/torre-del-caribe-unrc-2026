# Autor: Brandon Uriel García Sánchez
# Módulo: Pronóstico
# Qué hace:          Pieza 3c de la Fase 5. Le pone a cada pronóstico un rango del 90 % (intervalo conformal) y mide su
#                    COBERTURA REAL: de cada 100 meses, en cuántos el valor real cayó dentro del rango. El plan exige
#                    reportarla aunque salga peor que 90 %.
# Por qué así:       - Conformal secuencial: para un pronóstico hecho en el origen o, el tamaño del rango sale SOLO de los
#                      errores de pronósticos anteriores cuyo mes destino ya había pasado en o (sin ver el futuro).
#                    - Error en escala logarítmica, |ln(pronóstico ÷ real)|, porque la temporada es multiplicativa: el
#                      rango es "± X %" y no "± N visitantes", y sirve igual en enero (alto) que en septiembre (bajo).
#                    - Un tamaño por tramo de horizonte (1–3, 4–6, 7–12 meses): pronosticar a 10 meses es más incierto que
#                      a 1, y un solo tamaño cubriría de más lo cercano y de menos lo lejano.
#                    - Cuantil ⌈(n+1)·0.9⌉/n de los errores de calibración (garantía de cobertura ≥ 90 % si los errores
#                      futuros se parecen a los pasados). Se exige n ≥ 20; con menos no se da rango.
#                    - Alternativa descartada: intervalo de la fórmula de cada modelo (supone errores normales y no existe
#                      igual para Gradient Boosting ni para la línea base); el conformal trata a todos por igual.
# Datos de entrada:  datos/gold/pronostico_backtest.parquet (pieza 3, modelos.py).
# Alimenta a:        El rango "mínimo–máximo esperado" que ve el público en el calendario, y el escenario malo / bueno del
#                    Monte Carlo (pieza 4); en la Fase 6, cuánta capacidad libre se puede prometer con 90 % de confianza.

import math
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
GOLD = RAIZ / "datos" / "gold"
NIVEL = 0.90
MIN_CALIBRACION = 20


def tramo_horizonte(h: pd.Series) -> pd.Series:
    return pd.cut(h, [0, 3, 6, 12], labels=["1–3", "4–6", "7–12"]).astype(str)


def cuantil_conformal(errores: np.ndarray, nivel: float = NIVEL) -> float:
    """Cuantil ⌈(n+1)·nivel⌉/n de los errores de calibración (el más chico que garantiza la cobertura)."""
    n = len(errores)
    k = min(math.ceil((n + 1) * nivel), n)
    return float(np.sort(errores)[k - 1])


def agregar_intervalos(b: pd.DataFrame) -> pd.DataFrame:
    b = b.copy()
    b["tramo_h"] = tramo_horizonte(b.horizonte)
    # Un pronóstico ≤ 0 visitantes es un error total (Holt-Winters con tendencia dio −240 en la Bahía, origen may-2025):
    # cuenta como error infinito, no se descarta en silencio.
    razon = (b.pronostico / b.real).where(b.pronostico > 0)
    b["error_log"] = np.abs(np.log(razon)).fillna(np.inf)
    q = np.full(len(b), np.nan)
    for _, g in b.groupby(["serie", "modelo", "tramo_h"]):
        destinos, errores = g.destino.to_numpy(), g.error_log.to_numpy()
        for i, o in zip(g.index, g.origen):
            cal = errores[destinos <= o]  # errores ya conocidos en el origen
            if len(cal) >= MIN_CALIBRACION:
                q[b.index.get_loc(i)] = cuantil_conformal(cal)
    b["q_log"] = q
    b["minimo_90"] = b.pronostico * np.exp(-b.q_log)
    b["maximo_90"] = b.pronostico * np.exp(b.q_log)
    b["dentro_flag"] = (b.real >= b.minimo_90) & (b.real <= b.maximo_90)
    return b


def cobertura(b: pd.DataFrame) -> pd.DataFrame:
    """Por serie y modelo: cuántos pronósticos tienen rango, qué % cayó dentro y qué tan ancho es el rango (± % típico)."""
    x = b.dropna(subset=["q_log"])
    c = x.groupby(["serie", "modelo"]).agg(con_rango=("dentro_flag", "size"), cobertura_pct=("dentro_flag", "mean"),
                                           ancho_mediano_pct=("q_log", "median")).reset_index()
    c["cobertura_pct"] = (c.cobertura_pct * 100).round(1)
    c["ancho_mediano_pct"] = ((np.exp(c.ancho_mediano_pct) - 1) * 100).round(1)  # rango "± X %" hacia arriba
    return c


def correr():
    b = agregar_intervalos(pd.read_parquet(GOLD / "pronostico_backtest.parquet"))
    c = cobertura(b)
    b.to_parquet(GOLD / "pronostico_backtest.parquet", index=False)
    c.to_parquet(GOLD / "pronostico_cobertura.parquet", index=False)
    return b, c


if __name__ == "__main__":
    b, c = correr()
    pd.set_option("display.width", 200)
    print(c.to_string(index=False))
