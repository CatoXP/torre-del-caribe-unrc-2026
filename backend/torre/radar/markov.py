# Autor: Brandon Uriel García Sánchez
# Módulo: Radar
# Qué hace:          Pieza 3b de la Fase 4. Cadena de Markov semanal de los 7 centros turísticos del norte que mide
#                    DataTur: estima la probabilidad de pasar de tranquilo / concurrido / saturado a cada estado de una
#                    semana a la siguiente y, con ella, la probabilidad de que cada centro esté saturado en 1 a 8 semanas.
# Por qué así:       - Decisión de Brandon (29-sep-2026): semanal y solo el norte, como dice el plan (Markov en semanas,
#                      el Pronóstico en meses; B.2). Descartadas: mensual para todos (repetía al clasificador de la pieza 3
#                      y se encimaba con la Fase 5) y las dos a la vez.
#                    - El sur no tiene datos semanales: la cadena cubre solo la referencia del norte y se dice.
#                    - Estados con percentiles comunes (misma decisión que el Radar): p50 y p90 de la ocupación semanal de
#                      los 7 centros juntos. La ocupación de cada semana es cuartos ocupados ÷ disponibles.
#                    - Una matriz para los 7 centros juntos (más de 1,600 transiciones). Se prueba contra la persistencia
#                      y contra la frecuencia simple de cada estado en las últimas 52 semanas, sin verlas al estimar.
# Datos de entrada:  datos/silver/datatur_ocupacion (semanal, 2022–2026).
# Alimenta a:        Campaña: cuando se espera que el norte se sature en las próximas semanas, es el momento de
#                    ofrecerle el sur a ese turista; Torre en vivo (Fase 7) usa la probabilidad semana a semana.

from pathlib import Path

import numpy as np
import pandas as pd

from torre.radar.panel import GOLD, SILVER

ESTADOS = ["tranquilo", "concurrido", "saturado"]
CORTES = (0.50, 0.90)
SEMANAS_PRUEBA = 52
HORIZONTE = 8


def ocupacion_semanal() -> pd.DataFrame:
    o = pd.read_parquet(SILVER / "datatur_ocupacion",
                        columns=["centro", "es_qroo", "frecuencia", "periodo", "cuartos_ocupados", "cuartos_disponibles"])
    o = o[o.es_qroo & (o.frecuencia == "semanal")].copy()
    o["semana"] = pd.to_datetime(o.periodo.astype(str))
    o["ocupacion_pct"] = 100 * o.cuartos_ocupados / o.cuartos_disponibles
    return o[["centro", "semana", "ocupacion_pct"]].sort_values(["centro", "semana"], ignore_index=True)


def estados(o: pd.DataFrame) -> tuple[pd.DataFrame, tuple[float, float]]:
    u50, u90 = np.quantile(o.ocupacion_pct, CORTES)
    o = o.copy()
    o["estado"] = np.select([o.ocupacion_pct < u50, o.ocupacion_pct <= u90], ESTADOS[:2], default=ESTADOS[2])
    return o, (float(u50), float(u90))


def transiciones(o: pd.DataFrame) -> pd.DataFrame:
    """Pares (estado de la semana t, estado de la semana t+1) del mismo centro, solo si las semanas son consecutivas."""
    o = o.sort_values(["centro", "semana"])
    sig = o.groupby("centro").shift(-1)
    consecutiva = (sig.semana - o.semana) == pd.Timedelta(days=7)
    return pd.DataFrame({"centro": o.centro, "semana": o.semana, "desde": o.estado, "hacia": sig.estado})[consecutiva]


def matriz(tr: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """p_ij = n_ij / Σ_j n_ij (máxima verosimilitud de una cadena de Markov: contar y dividir)."""
    n = pd.crosstab(tr.desde, tr.hacia).reindex(index=ESTADOS, columns=ESTADOS, fill_value=0)
    return n.div(n.sum(axis=1), axis=0), n


def estacionaria(P: pd.DataFrame) -> pd.Series:
    """π tal que π = π P: la proporción de semanas en cada estado a largo plazo (vector propio de valor 1)."""
    val, vec = np.linalg.eig(P.to_numpy().T)
    v = np.real(vec[:, np.argmin(np.abs(val - 1))])
    return pd.Series(v / v.sum(), index=ESTADOS)


def a_k_semanas(P: pd.DataFrame, estado: str, k: int) -> pd.Series:
    """π_{t+k} = π_t P^k, con π_t = 1 en el estado actual."""
    pi = pd.Series(0.0, index=ESTADOS)
    pi[estado] = 1.0
    return pd.Series(pi.to_numpy() @ np.linalg.matrix_power(P.to_numpy(), k), index=ESTADOS)


def backtest(o: pd.DataFrame, k_lista=(1, 4, 8)) -> pd.DataFrame:
    """Para cada semana de prueba (las últimas 52), estima P solo con transiciones anteriores y predice k semanas
    adelante. Puntaje de Brier: promedio de Σ_j (p_j − 1[y=j])², 0 es perfecto. Se compara contra la persistencia
    (probabilidad 1 al estado actual) y contra la frecuencia simple de cada estado."""
    tr = transiciones(o)
    corte = o.semana.max() - pd.Timedelta(weeks=SEMANAS_PRUEBA)
    por_centro = {c: g.set_index("semana").estado for c, g in o.groupby("centro")}
    filas = []
    for k in k_lista:
        brier = {"Markov": [], "Persistencia": [], "Frecuencia simple": []}
        aciertos = {"Markov": 0, "Persistencia": 0, "Frecuencia simple": 0}
        n = 0
        for semana in sorted(o.loc[o.semana > corte, "semana"].unique()):
            ant = tr[tr.semana + pd.Timedelta(days=7) <= semana - pd.Timedelta(weeks=k - 1)]  # solo pasado conocido
            P, _ = matriz(ant)
            frec = o[o.semana <= semana - pd.Timedelta(weeks=k)].estado.value_counts(normalize=True).reindex(ESTADOS, fill_value=0)
            for c, serie in por_centro.items():
                origen = semana - pd.Timedelta(weeks=k)
                if origen not in serie.index or semana not in serie.index:
                    continue
                real = np.array([serie[semana] == e for e in ESTADOS], dtype=float)
                pers = np.array([serie[origen] == e for e in ESTADOS], dtype=float)
                pred = {"Markov": a_k_semanas(P, serie[origen], k).to_numpy(), "Persistencia": pers,
                        "Frecuencia simple": frec.to_numpy()}
                for nombre, p in pred.items():
                    brier[nombre].append(((p - real) ** 2).sum())
                    aciertos[nombre] += int(ESTADOS[int(np.argmax(p))] == serie[semana])
                n += 1
        for nombre in brier:
            filas.append({"k_semanas": k, "metodo": nombre, "brier": round(float(np.mean(brier[nombre])), 3),
                          "exactitud": round(aciertos[nombre] / n, 3), "casos": n})
    return pd.DataFrame(filas)


def correr() -> dict:
    o, cortes = estados(ocupacion_semanal())
    tr = transiciones(o)
    P, n = matriz(tr)
    ultima = o.semana.max()
    hoy = o[o.semana == ultima].set_index("centro")
    riesgo = pd.DataFrame({f"sem_{k}": {c: a_k_semanas(P, e, k)["saturado"] for c, e in hoy.estado.items()}
                           for k in range(1, HORIZONTE + 1)})
    riesgo.insert(0, "estado_hoy", hoy.estado)
    riesgo.insert(1, "ocupacion_hoy_pct", hoy.ocupacion_pct.round(1))
    GOLD.mkdir(parents=True, exist_ok=True)
    P.to_parquet(GOLD / "radar_markov_matriz.parquet")
    riesgo.reset_index(names="centro").assign(semana=ultima).to_parquet(GOLD / "radar_markov_riesgo.parquet", index=False)
    return {"o": o, "cortes": cortes, "P": P, "n": n, "pi": estacionaria(P), "riesgo": riesgo, "ultima": ultima,
            "backtest": backtest(o)}


if __name__ == "__main__":
    pd.set_option("display.width", 200, "display.max_columns", 20)
    r = correr()
    print(f"Cortes comunes de la ocupación semanal: p50 = {r['cortes'][0]:.1f} %, p90 = {r['cortes'][1]:.1f} %")
    print(f"Transiciones contadas: {int(r['n'].to_numpy().sum()):,}\n\nConteos n_ij (filas = esta semana, columnas = la siguiente):")
    print(r["n"].to_string())
    print("\nMatriz de transición P:")
    print(r["P"].round(3).to_string())
    print("\nDistribución estacionaria π (largo plazo):")
    print(r["pi"].round(3).to_string())
    print(f"\nProbabilidad de estar SATURADO en k semanas, desde la semana del {r['ultima']:%d-%m-%Y}:")
    print(r["riesgo"].round(3).to_string())
    print("\nBacktest (últimas 52 semanas; Brier: 0 es perfecto):")
    print(r["backtest"].to_string(index=False))
