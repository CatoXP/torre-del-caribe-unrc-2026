# Autor: Brandon Uriel García Sánchez
# Módulo: Radar
# Qué hace:          Pieza 3 de la Fase 4. Predice el estado (tranquilo / concurrido / saturado) de cada lugar el mes
#                    siguiente. Compara tres modelos de aprendizaje de máquina contra una línea base honesta
#                    (persistencia: "el mes que viene estará igual que este") con validación temporal.
# Por qué así:       - Brandon pidió "con los datos que tenemos inferimos los futuros haciendo ML" (28-sep-2026).
#                    - Índice comparable (decisión de Brandon, 29-sep-2026): para entrenar, cada lugar usa solo las
#                      medidas que tiene HOY y solo los meses en que las tiene todas. Así un cambio de estado siempre es
#                      un cambio real y no la pérdida de un dato (el quiebre de 2025: Chetumal 0.54 → 0.05 al perder la
#                      ocupación de SITUR-Q). Descartadas: entrenar solo 2025–2026 (19 meses por lugar) y entrenar todo
#                      con una bandera "tiene ocupación" (el modelo aprendería el cambio de datos).
#                    - Línea base de persistencia: un modelo que no le gana a "igual que este mes" no sirve, y se dice.
#                    - Validación temporal (entrenar con el pasado, probar con los últimos 12 meses que el modelo no
#                      vio), nunca aleatoria: en series de tiempo mezclar meses filtra el futuro al entrenamiento.
#                    - Métrica F1-macro: pesa igual las tres clases; "saturado" es solo ~10 % de los casos y la
#                      exactitud simple premiaría a un modelo que nunca dice "saturado".
# Datos de entrada:  indice.py (componentes z del panel mensual; datos/silver vía panel.py).
# Alimenta a:        Campaña: si se espera que un lugar pase a "saturado" el mes siguiente, su anuncio se pausa antes
#                    de que se llene (regla anti-colapso); Torre en vivo (Fase 7) vigila si la predicción se cumple.

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from torre.radar.indice import CORTES, calcular
from torre.radar.panel import GOLD

ESTADOS = ["tranquilo", "concurrido", "saturado"]
INICIO_PRUEBA = pd.Timestamp("2025-08-01")  # los últimos 12 meses objetivo (ago-2025 a jul-2026) quedan para la prueba
SEMILLA = 0


def indice_comparable(base: pd.DataFrame, comps: list[str]) -> tuple[pd.DataFrame, tuple[float, float]]:
    """IPT con las medidas que cada lugar tiene en su último mes con dato, solo en los meses en que las tiene todas."""
    filas = []
    for lugar, g in base.groupby("lugar"):
        g = g.sort_values("periodo")
        con = g[g.ipt.notna()]
        if con.empty:
            continue
        actuales = [k for k in comps if pd.notna(con.iloc[-1][f"z_{k}"])]
        Z = g[[f"z_{k}" for k in actuales]]
        completo = Z.notna().all(axis=1)
        filas.append(g.assign(ipt_comparable=Z.mean(axis=1).where(completo), medidas=", ".join(actuales))
                     [["lugar", "es_de_los_5", "periodo", "ipt_comparable", "medidas"]])
    t = pd.concat(filas, ignore_index=True)
    u50, u90 = np.nanquantile(t.ipt_comparable, CORTES)
    t["estado"] = np.select([t.ipt_comparable.isna(), t.ipt_comparable < u50, t.ipt_comparable <= u90],
                            [None, "tranquilo", "concurrido"], default="saturado")
    return t, (float(u50), float(u90))


def tabla_de_aprendizaje(t: pd.DataFrame) -> pd.DataFrame:
    """Una fila por lugar y mes t: lo que se sabe en t (índice, rezagos, mes del año) y el estado de t+1 (objetivo)."""
    filas = []
    for _, g in t.groupby("lugar"):
        g = g.sort_values("periodo").copy()
        g["ipt_1"] = g.ipt_comparable.shift(1)
        g["ipt_2"] = g.ipt_comparable.shift(2)
        g["cambio"] = g.ipt_comparable - g.ipt_1
        g["estado_hoy"] = g.estado
        g["objetivo"] = g.estado.shift(-1)
        g["periodo_objetivo"] = g.periodo.shift(-1)
        filas.append(g)
    d = pd.concat(filas, ignore_index=True)
    d["mes_sin"] = np.sin(2 * np.pi * d.periodo.dt.month / 12)  # la temporada como círculo: diciembre queda junto a enero
    d["mes_cos"] = np.cos(2 * np.pi * d.periodo.dt.month / 12)
    d["es_de_los_5"] = d.es_de_los_5.astype(int)
    return d.dropna(subset=["ipt_comparable", "ipt_1", "ipt_2", "objetivo"]).reset_index(drop=True)


RASGOS = ["ipt_comparable", "ipt_1", "ipt_2", "cambio", "mes_sin", "mes_cos", "es_de_los_5"]


def modelos() -> dict:
    return {
        "Regresión logística": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced")),
        "Random Forest": RandomForestClassifier(n_estimators=400, min_samples_leaf=3, class_weight="balanced",
                                                random_state=SEMILLA),
        "Gradient Boosting": GradientBoostingClassifier(random_state=SEMILLA),
    }


def comparar(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Entrena con los objetivos antes de INICIO_PRUEBA y evalúa en los 12 meses siguientes."""
    ent, pru = d[d.periodo_objetivo < INICIO_PRUEBA], d[d.periodo_objetivo >= INICIO_PRUEBA]
    resultados, predicciones = [], {"Persistencia (línea base)": pru.estado_hoy.to_numpy()}
    for nombre, m in modelos().items():
        m.fit(ent[RASGOS], ent.objetivo)
        predicciones[nombre] = m.predict(pru[RASGOS])
    cinco = pru.es_de_los_5.to_numpy() == 1
    for nombre, pred in predicciones.items():
        resultados.append({"modelo": nombre,
                           "f1_macro": round(f1_score(pru.objetivo, pred, average="macro", labels=ESTADOS, zero_division=0), 3),
                           "exactitud": round(accuracy_score(pru.objetivo, pred), 3),
                           "exactitud_5_lugares": round(accuracy_score(pru.objetivo[cinco], pred[cinco]), 3),
                           "n_entrenamiento": len(ent), "n_prueba": len(pru)})
    return pd.DataFrame(resultados), {"entrenamiento": ent, "prueba": pru, "predicciones": predicciones}


def origen_movil(d: pd.DataFrame) -> pd.DataFrame:
    """Backtesting con origen móvil: para cada mes objetivo de la prueba se reentrena con TODO lo anterior y se predice
    solo ese mes (12 reentrenamientos). Es más exigente que un solo corte y muestra si la ventaja sobre la persistencia
    se sostiene mes a mes."""
    meses = sorted(d.loc[d.periodo_objetivo >= INICIO_PRUEBA, "periodo_objetivo"].unique())
    reales, hoy, preds = [], [], {n: [] for n in ["Persistencia (línea base)", *modelos()]}
    for mes in meses:
        ent, pru = d[d.periodo_objetivo < mes], d[d.periodo_objetivo == mes]
        reales.append(pru.objetivo.to_numpy())
        hoy.append(pru.estado_hoy.to_numpy())
        preds["Persistencia (línea base)"].append(pru.estado_hoy.to_numpy())
        for nombre, m in modelos().items():
            m.fit(ent[RASGOS], ent.objetivo)
            preds[nombre].append(m.predict(pru[RASGOS]))
    y, h = np.concatenate(reales), np.concatenate(hoy)
    cambia = y != h  # meses en que el estado SÍ cambió: la persistencia los falla todos por definición
    filas = []
    for n, p in preds.items():
        p = np.concatenate(p)
        filas.append({"modelo": n,
                      "f1_macro_origen_movil": round(f1_score(y, p, average="macro", labels=ESTADOS, zero_division=0), 3),
                      "exactitud_origen_movil": round(accuracy_score(y, p), 3), "aciertos": int((y == p).sum()),
                      "casos": len(y), "cambios_reales": int(cambia.sum()), "cambios_acertados": int((y == p)[cambia].sum()),
                      "falsas_alarmas": int(((p != h) & (p != y)).sum())})  # predijo un cambio que no ocurrió
    return pd.DataFrame(filas)


def sesgo(d: pd.DataFrame, nombre: str) -> pd.DataFrame:
    """Sesgo (punto del plan, Fase 4): el mismo origen móvil del modelo elegido, separado entre los 5 lugares de la campaña
    y el resto del estado. Si en un grupo no hubo cambios de estado, el modelo no se puede validar ahí y se dice."""
    meses = sorted(d.loc[d.periodo_objetivo >= INICIO_PRUEBA, "periodo_objetivo"].unique())
    partes = []
    for mes in meses:
        ent, pru = d[d.periodo_objetivo < mes], d[d.periodo_objetivo == mes]
        m = modelos()[nombre]
        m.fit(ent[RASGOS], ent.objetivo)
        partes.append(pru.assign(pred=m.predict(pru[RASGOS])))
    r = pd.concat(partes)
    filas = []
    for grupo, g in r.groupby("es_de_los_5"):
        cambia = g.objetivo != g.estado_hoy
        filas.append({"grupo": "5 lugares" if grupo else "resto del estado", "casos": len(g),
                      "exactitud_modelo": round(accuracy_score(g.objetivo, g.pred), 3),
                      "exactitud_persistencia": round(accuracy_score(g.objetivo, g.estado_hoy), 3),
                      "cambios_reales": int(cambia.sum()), "cambios_acertados": int((g.pred == g.objetivo)[cambia].sum()),
                      "falsas_alarmas": int(((g.pred != g.estado_hoy) & (g.pred != g.objetivo)).sum())})
    return pd.DataFrame(filas)


def predecir_mes_siguiente(t: pd.DataFrame, d: pd.DataFrame, nombre: str) -> pd.DataFrame:
    """Reentrena el modelo elegido con TODO lo disponible y predice el mes siguiente al último mes publicado. Un lugar
    cuyo dato terminó antes (Costa Mujeres: solo ocupación de SITUR-Q, hasta dic-2024) no se predice."""
    m = modelos()[nombre]
    m.fit(d[RASGOS], d.objetivo)
    ultimo_mes = t.dropna(subset=["ipt_comparable"]).periodo.max()
    ultimos = []
    for _, g in t.groupby("lugar"):
        g = g.sort_values("periodo").dropna(subset=["ipt_comparable"])
        if len(g) < 3 or g.periodo.iloc[-1] != ultimo_mes:
            continue
        u = g.iloc[-1]
        ultimos.append({"lugar": u.lugar, "es_de_los_5": int(u.es_de_los_5), "periodo": u.periodo,
                        "estado_hoy": u.estado, "ipt_comparable": u.ipt_comparable, "ipt_1": g.ipt_comparable.iloc[-2],
                        "ipt_2": g.ipt_comparable.iloc[-3], "medidas": u.medidas})
    x = pd.DataFrame(ultimos)
    x["cambio"] = x.ipt_comparable - x.ipt_1
    x["mes_sin"] = np.sin(2 * np.pi * x.periodo.dt.month / 12)
    x["mes_cos"] = np.cos(2 * np.pi * x.periodo.dt.month / 12)
    x["estado_mes_siguiente_est"] = m.predict(x[RASGOS])  # _est: es una predicción, no una medición (regla de oro 3)
    prob = pd.DataFrame(m.predict_proba(x[RASGOS]), columns=[f"prob_{c}" for c in m.classes_])
    x["mes_siguiente"] = x.periodo + pd.offsets.MonthBegin(1)
    x["modelo"] = nombre
    return pd.concat([x, prob], axis=1)


def correr() -> dict:
    base, _, comps = calcular()
    t, cortes = indice_comparable(base, comps)
    d = tabla_de_aprendizaje(t)
    metricas, detalle = comparar(d)
    metricas = metricas.merge(origen_movil(d), on="modelo")
    # Criterio de elección (decisión de Brandon, 29-sep-2026): el modelo que más acierta en el origen móvil y, a igualdad,
    # el que más cambios de estado anticipa. Con el índice original quedó Random Forest (136 de 156; 7 de 23 cambios).
    # Tras la auditoría (se agregó "llegadas por cuarto") el mismo criterio da la regresión logística: 130 de 156 y
    # 8 de 30 cambios, contra 130 y 6 de Random Forest. Se respeta el criterio, no el nombre del modelo.
    # Descartado: elegir por F1-macro (el del plan), que daba la regresión logística: acierta lo mismo que la
    # persistencia (133) y solo anticipa 3 cambios, y anticipar cambios es lo que necesita la regla anti-colapso.
    modelos_ml = metricas[metricas.modelo != "Persistencia (línea base)"]
    mejor = modelos_ml.sort_values(["aciertos", "cambios_acertados"], ascending=False).iloc[0]
    base_aciertos = metricas.loc[metricas.modelo == "Persistencia (línea base)", "aciertos"].iloc[0]
    pred = predecir_mes_siguiente(t, d, mejor.modelo)
    ses = sesgo(d, mejor.modelo)
    GOLD.mkdir(parents=True, exist_ok=True)
    ses.to_parquet(GOLD / "radar_sesgo.parquet", index=False)
    t.assign(corte_p50=cortes[0], corte_p90=cortes[1]).to_parquet(GOLD / "radar_indice_comparable.parquet", index=False)
    metricas.to_parquet(GOLD / "radar_modelos.parquet", index=False)
    pred.to_parquet(GOLD / "radar_prediccion.parquet", index=False)
    return {"t": t, "cortes": cortes, "d": d, "metricas": metricas, "mejor": mejor.modelo,
            "le_gana_a_persistencia": bool(mejor.aciertos > base_aciertos), "prediccion": pred, "detalle": detalle,
            "sesgo": ses}


if __name__ == "__main__":
    pd.set_option("display.width", 200, "display.max_columns", 20, "display.max_colwidth", 60)
    r = correr()
    t = r["t"]
    print(f"Índice comparable: cortes p50 = {r['cortes'][0]:.3f}, p90 = {r['cortes'][1]:.3f}")
    print(t.dropna(subset=["ipt_comparable"]).groupby("lugar").agg(desde=("periodo", "min"), meses=("periodo", "size"),
                                                                    medidas=("medidas", "first")).to_string())
    print(f"\nTabla de aprendizaje: {len(r['d'])} filas; prueba desde {INICIO_PRUEBA:%Y-%m}")
    print(r["d"].objetivo.value_counts().to_string())
    print("\nComparación de modelos (prueba = últimos 12 meses):")
    print(r["metricas"].to_string(index=False))
    print(f"\nMejor modelo: {r['mejor']} · ¿le gana a la persistencia? {r['le_gana_a_persistencia']}")
    print("\nSesgo (5 lugares contra el resto):")
    print(r["sesgo"].to_string(index=False))
    print(r["prediccion"][["lugar", "estado_hoy", "estado_mes_siguiente_est", "mes_siguiente",
                           *[c for c in r["prediccion"] if c.startswith("prob_")]]].round(2).to_string(index=False))
