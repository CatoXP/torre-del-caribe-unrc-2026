# Autor: Brandon Uriel García Sánchez
# Módulo: Pronóstico
# Qué hace:          Pieza 3d de la Fase 5. Elige el modelo de cada serie con el criterio de Brandon y produce el pronóstico
#                    real de los próximos 12 meses (desde el último mes publicado), con su rango del 90 %.
# Por qué así:       - Criterio (decisión de Brandon, 30-sep-2026, "Menor error con rango ≥ 80 %"): por serie, el modelo con
#                      menor error medio (MAE) en el origen móvil ENTRE los que tienen cobertura real ≥ 80 % de su rango
#                      del 90 %. Resultado: Regresión con clima para Bahía, Belice y Ruta; Línea base para Cancún.
#                      Descartados: "menor error sin importar el rango" (en la Ruta elegiría Holt-Winters sin tendencia,
#                      0.64 del error de la base, pero su rango solo acierta 72 de cada 100 veces) y "un solo modelo para
#                      todo" (en Cancún la regresión comete 58 % más error que repetir el mismo mes del año anterior).
#                    - El rango del pronóstico final usa TODOS los errores del origen móvil del modelo elegido, por tramo
#                      de horizonte (mismo método conformal de intervalos.py).
# Datos de entrada:  datos/gold/pronostico_series, pronostico_metricas, pronostico_cobertura, pronostico_backtest.
# Alimenta a:        Calendario de la campaña (cuántos visitantes esperar cada mes en cada lugar, con mínimo y máximo) y
#                    el Monte Carlo de escenarios (pieza 4) → presupuesto por mes en la Fase 6.

from pathlib import Path

import numpy as np
import pandas as pd

from torre.pronostico import modelos
from torre.pronostico.intervalos import cuantil_conformal, tramo_horizonte

RAIZ = Path(__file__).resolve().parents[3]
GOLD = RAIZ / "datos" / "gold"
COBERTURA_MINIMA = 80.0


def elegir(metricas: pd.DataFrame, cobertura: pd.DataFrame) -> pd.DataFrame:
    """Por serie: menor MAE entre los modelos con cobertura ≥ 80 %. Devuelve la tabla con la columna elegido_flag."""
    t = metricas.merge(cobertura, on=["serie", "modelo"])
    t["rango_confiable_flag"] = t.cobertura_pct >= COBERTURA_MINIMA
    candidatos = t[t.rango_confiable_flag]
    ganador = candidatos.loc[candidatos.groupby("serie").mae.idxmin(), ["serie", "modelo"]]
    t["elegido_flag"] = t.set_index(["serie", "modelo"]).index.isin(ganador.set_index(["serie", "modelo"]).index)
    return t


def pronostico_final(t: pd.DataFrame, elegidos: pd.DataFrame, backtest: pd.DataFrame) -> pd.DataFrame:
    """12 meses después del último mes publicado de cada serie, con el modelo elegido y su rango conformal del 90 %."""
    filas = []
    for serie, s in t.groupby("serie"):
        s = s.sort_values("periodo").reset_index(drop=True)
        nombre = elegidos[(elegidos.serie == serie) & elegidos.elegido_flag].modelo.iloc[0]
        origen = s.periodo.max()
        destinos = pd.date_range(origen + pd.offsets.MonthBegin(1), periods=modelos.HORIZONTE, freq="MS")
        pron = modelos.MODELOS[nombre](s, origen, destinos)
        err = backtest[(backtest.serie == serie) & (backtest.modelo == nombre)]
        h = np.arange(1, modelos.HORIZONTE + 1)
        tramo = tramo_horizonte(pd.Series(h))
        q = {k: cuantil_conformal(err[err.tramo_h == k].error_log.to_numpy()) for k in tramo.unique()}
        for d, p, k, hh in zip(destinos, pron, tramo, h):
            filas.append({"serie": serie, "lugar": s.lugar.iloc[0], "papel": s.papel.iloc[0], "modelo": nombre,
                          "ultimo_dato": origen, "periodo": d, "horizonte": int(hh), "esperado_est": p,
                          "minimo_90_est": p * np.exp(-q[k]), "maximo_90_est": p * np.exp(q[k]),
                          "unidad": s.unidad.iloc[0]})
    return pd.DataFrame(filas)


def correr():
    t = pd.read_parquet(GOLD / "pronostico_series.parquet")
    m = pd.read_parquet(GOLD / "pronostico_metricas.parquet")
    c = pd.read_parquet(GOLD / "pronostico_cobertura.parquet")
    b = pd.read_parquet(GOLD / "pronostico_backtest.parquet")
    e = elegir(m, c)
    f = pronostico_final(t, e, b)
    e.to_parquet(GOLD / "pronostico_eleccion.parquet", index=False)
    f.to_parquet(GOLD / "pronostico_mes.parquet", index=False)
    return e, f


if __name__ == "__main__":
    e, f = correr()
    pd.set_option("display.width", 200)
    print(e[e.elegido_flag][["serie", "modelo", "mae_vs_base", "mape", "cobertura_pct", "ancho_mediano_pct"]].to_string(index=False))
    f["mes"] = f.periodo.dt.strftime("%Y-%m")
    print(f.pivot(index="mes", columns="lugar", values="esperado_est").round(0).to_string())
