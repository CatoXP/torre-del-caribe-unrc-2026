# Autor: Brandon Uriel García Sánchez
# Módulo: Torre en vivo (A5, Fase 7)
# Qué hace:          Arma una fila por semana (lunes) con las cuatro señales que vigila la Torre, elegidas por Brandon el
#                    02-oct-2026 (docs/decisiones/20-torre-en-vivo.md):
#                    1. Ocupación del norte: Cancún y Riviera Maya (DataTur semanal), con su estado según los cortes del
#                       Radar (p50/p90 de todas las semanas de Quintana Roo) y su promedio móvil de 4 semanas (ventana
#                       deslizante en Spark).
#                    2. Tormentas cerca: algún punto de HURDAT2 que afecta al sur esa semana (≤ 200 km de Chetumal,
#                       ≥ 34 nudos, la regla de la Fase 5). 2026 todavía no está publicado: se marca SIN DATO, no "sin
#                       tormenta".
#                    3. Clima raro: Isolation Forest sobre el clima semanal de Chetumal y Kohunlich (lluvia, lluvia del
#                       peor día, viento y calor, más la época del año), entrenado con 2019–2021 y aplicado a 2022–2026.
#                    4. Llegadas del sur: el dato real de cada mes contra el rango del 90 % del pronóstico a un mes del
#                       modelo elegido (backtest de la Fase 5). Se supone que el dato de un mes se conoce al empezar el
#                       siguiente (supuesto declarado: en la realidad se publica con 1–2 meses de retraso).
# Por qué así:       - Isolation Forest y no un umbral fijo: Brandon pidió que no se fije a mano qué es "raro"; el bosque lo
#                      aprende de 3 años de clima real. La época del año entra como seno y coseno, para que un aguacero de
#                      septiembre no se marque raro solo por ser septiembre.
#                    - Entrena con años ANTES de la reproducción, para no usar el futuro (misma regla del origen móvil).
#                    - El sur no tiene ningún dato semanal oficial: por eso sus señales son clima, tormentas y llegadas
#                      mensuales; la ocupación semanal solo existe para el norte.
# Datos de entrada:  datos/silver/datatur_ocupacion (D2), huracanes (D9), clima_horario (D8);
#                    datos/gold/pronostico_backtest y pronostico_eleccion (Fase 5).
# Alimenta a:        torre.envivo.motor (qué anuncio se enciende o se pausa cada semana).

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from torre.base.entorno import RAIZ, crear_spark
from torre.radar.markov import estados, ocupacion_semanal

SILVER = RAIZ / "datos" / "silver"
GOLD = RAIZ / "datos" / "gold"
SALIDA = GOLD / "envivo_senales.parquet"

NORTE = {"Cancun": "cancun", "Riviera Maya": "riviera"}
PUNTO_DE = {"Chetumal": "chetumal", "Bahía Calderitas–Oxtankah": "chetumal", "Ruta arqueológica del sur": "kohunlich"}
SERIE_DE = {"Chetumal": "Chetumal · cruces desde Belice",
            "Bahía Calderitas–Oxtankah": "Bahía Calderitas–Oxtankah · visitantes INAH",
            "Ruta arqueológica del sur": "Ruta arqueológica del sur · visitantes INAH"}
CLAVE = {"Chetumal": "chetumal", "Bahía Calderitas–Oxtankah": "bahia", "Ruta arqueológica del sur": "ruta"}
ENTRENA = ("2019-01-01", "2021-12-31")
ULTIMO_HURDAT = pd.Timestamp("2025-12-31")
VARIABLES_CLIMA = ["lluvia_mm", "lluvia_max_dia_mm", "viento_max_kmh", "temp_max_c", "epoca_sin", "epoca_cos"]


def lunes(f: pd.Series) -> pd.Series:
    f = pd.to_datetime(f)
    return (f - pd.to_timedelta(f.dt.weekday, unit="D")).dt.normalize()


# ---------- 1. Norte ----------
def norte(spark) -> tuple[pd.DataFrame, tuple[float, float]]:
    o, cortes = estados(ocupacion_semanal())
    o = o[o.centro.isin(NORTE)]
    # Promedio móvil de 4 semanas con una ventana deslizante de Spark (la semana y las 3 anteriores del mismo centro).
    from pyspark.sql import Window, functions as F
    # La semana viaja como texto: Spark convierte las fechas a su zona horaria y la unión de regreso fallaría.
    o["semana_txt"] = o.semana.dt.strftime("%Y-%m-%d")
    df = spark.createDataFrame(o[["centro", "semana_txt", "ocupacion_pct"]])
    w = Window.partitionBy("centro").orderBy("semana_txt").rowsBetween(-3, 0)
    m = df.withColumn("ocupacion_4sem", F.avg("ocupacion_pct").over(w)).toPandas()
    o = o.merge(m[["centro", "semana_txt", "ocupacion_4sem"]], on=["centro", "semana_txt"])
    filas = []
    for centro, clave in NORTE.items():
        x = o[o.centro == centro].set_index("semana")
        filas.append(x[["ocupacion_pct", "estado", "ocupacion_4sem"]].add_prefix(f"{clave}_"))
    return pd.concat(filas, axis=1).reset_index().rename(columns={"index": "semana"}), cortes


# ---------- 2. Tormentas ----------
def tormentas(semanas: pd.Series) -> pd.DataFrame:
    h = pd.read_parquet(SILVER / "huracanes", columns=["id_tormenta", "nombre", "fecha", "afecta_sur_flag"])
    h = h[h.afecta_sur_flag]
    h["semana"] = lunes(h.fecha)
    t = h.groupby("semana").agg(tormenta_nombre=("nombre", lambda n: ", ".join(sorted(set(n.str.title())))))
    r = pd.DataFrame({"semana": semanas})
    r = r.merge(t, on="semana", how="left")
    r["tormenta"] = r.tormenta_nombre.notna().astype(object)
    r.loc[r.semana > ULTIMO_HURDAT, "tormenta"] = None  # HURDAT2 2026 aún no se publica: no se sabe
    return r


# ---------- 3. Clima raro (Isolation Forest) ----------
def clima_semanal() -> pd.DataFrame:
    c = pd.read_parquet(SILVER / "clima_horario", columns=["punto", "fecha_hora_local", "temp_c", "lluvia_mm", "viento_kmh"])
    c = c[c.punto.isin(set(PUNTO_DE.values()))]
    c["dia"] = c.fecha_hora_local.dt.normalize()
    d = c.groupby(["punto", "dia"]).agg(lluvia=("lluvia_mm", "sum"), viento=("viento_kmh", "max"), temp=("temp_c", "max"))
    d = d.reset_index()
    d["semana"] = lunes(d.dia)
    s = d.groupby(["punto", "semana"]).agg(lluvia_mm=("lluvia", "sum"), lluvia_max_dia_mm=("lluvia", "max"),
                                            viento_max_kmh=("viento", "max"), temp_max_c=("temp", "max"),
                                            dias=("dia", "nunique")).reset_index()
    s = s[s.dias == 7]  # solo semanas completas
    ang = 2 * np.pi * s.semana.dt.isocalendar().week.astype(float) / 52.18
    s["epoca_sin"], s["epoca_cos"] = np.sin(ang), np.cos(ang)
    return s


CORTE_RARO = 0.95  # decisión de Brandon (02-oct-2026): raro = más raro que 19 de cada 20 semanas ya conocidas


def anomalias_clima(s: pd.DataFrame) -> pd.DataFrame:
    """Un bosque por punto y por año, entrenado con TODAS las semanas anteriores a ese año (ventana creciente, sin ver el
    futuro). s(x) = 2^(−E[h(x)]/c(n)). Una semana es rara si su s(x) pasa el percentil 95 de las semanas de entrenamiento.
    Descartado: el corte 'auto' del artículo original marcaba 47 % de las semanas de Chetumal (13–26 % incluso dentro de
    su propio entrenamiento): con 156 semanas no distingue y desde 2022 llueve más y hace más calor."""
    salida = []
    for punto, x in s.groupby("punto"):
        x = x.copy()
        x["puntaje_anomalia"], x["corte_anomalia"], x["clima_raro"], x["n_entrena"] = np.nan, np.nan, None, 0
        x["anio"] = x.semana.dt.year
        for anio in range(int(x.anio.min()), int(x.anio.max()) + 1):
            entrena = x[(x.semana >= ENTRENA[0]) & (x.semana < f"{anio}-01-01")]
            if anio < 2022 or len(entrena) < 52:
                continue  # 2019–2021 son la base de aprendizaje, no se califican
            bosque = IsolationForest(n_estimators=300, contamination="auto", random_state=0).fit(entrena[VARIABLES_CLIMA])
            corte = float(np.quantile(-bosque.score_samples(entrena[VARIABLES_CLIMA]), CORTE_RARO))
            esta = x.anio == anio
            x.loc[esta, "puntaje_anomalia"] = -bosque.score_samples(x.loc[esta, VARIABLES_CLIMA])  # más alto = más raro
            x.loc[esta, "corte_anomalia"] = corte
            x.loc[esta, "clima_raro"] = x.loc[esta, "puntaje_anomalia"] > corte
            x.loc[esta, "n_entrena"] = len(entrena)
        salida.append(x.drop(columns="anio"))
    return pd.concat(salida, ignore_index=True)


# ---------- 4. Llegadas del sur contra lo esperado ----------
def llegadas() -> pd.DataFrame:
    b = pd.read_parquet(GOLD / "pronostico_backtest.parquet")
    e = pd.read_parquet(GOLD / "pronostico_eleccion.parquet")
    b = b.merge(e[e.elegido_flag][["serie", "modelo"]], on=["serie", "modelo"])
    b = b[(b.horizonte == 1) & b.minimo_90.notna()]
    filas = []
    for lugar, serie in SERIE_DE.items():
        x = b[b.serie == serie][["destino", "real", "pronostico", "minimo_90", "maximo_90"]].copy()
        x["lugar"] = lugar
        x["llegadas"] = np.select([x.real > x.maximo_90, x.real < x.minimo_90], ["arriba", "abajo"], default="dentro")
        filas.append(x)
    r = pd.concat(filas, ignore_index=True)
    r["se_conoce_desde"] = (pd.to_datetime(r.destino) + pd.offsets.MonthBegin(1))
    return r


def construir(spark=None) -> pd.DataFrame:
    spark = spark or crear_spark("envivo-senales")
    n, cortes = norte(spark)
    semanas = n.semana
    t = tormentas(semanas)
    clima = anomalias_clima(clima_semanal())
    ll = llegadas()
    s = n.merge(t, on="semana", how="left")
    for punto in sorted(set(PUNTO_DE.values())):
        c = clima[clima.punto == punto][["semana", "clima_raro", "puntaje_anomalia", "lluvia_mm", "viento_max_kmh"]]
        s = s.merge(c.add_prefix(f"{punto}_").rename(columns={f"{punto}_semana": "semana"}), on="semana", how="left")
    # Llegadas: en cada semana, el último mes que ya se conoce.
    for lugar, clave in CLAVE.items():
        x = ll[ll.lugar == lugar].sort_values("se_conoce_desde")[["se_conoce_desde", "destino", "llegadas"]]
        s = pd.merge_asof(s.sort_values("semana"), x.rename(columns={
            "se_conoce_desde": "semana_conocida", "destino": f"{clave}_mes_dato", "llegadas": f"{clave}_llegadas"}),
            left_on="semana", right_on="semana_conocida", direction="backward").drop(columns="semana_conocida")
        # Solo vale el dato del mes inmediato anterior (si el último conocido es más viejo, no hay señal).
        dato = pd.to_datetime(s[f"{clave}_mes_dato"])
        meses = (s.semana.dt.year * 12 + s.semana.dt.month) - (dato.dt.year * 12 + dato.dt.month)
        viejo = meses.isna() | (meses > 1)
        s.loc[viejo, f"{clave}_llegadas"] = None
    s["corte_p50"], s["corte_p90"] = cortes
    s = s.sort_values("semana").reset_index(drop=True)
    s.to_parquet(SALIDA, index=False)
    print(f"Señales: {len(s)} semanas ({s.semana.min().date()} → {s.semana.max().date()}); cortes del norte "
          f"p50 {cortes[0]:.2f} % / p90 {cortes[1]:.2f} %")
    print(f"  Cancún saturado: {(s.cancun_estado == 'saturado').sum()} semanas; Riviera: {(s.riviera_estado == 'saturado').sum()}")
    print(f"  Tormentas: {(s.tormenta == True).sum()} semanas ({', '.join(s.tormenta_nombre.dropna().unique())}); "  # noqa: E712
          f"sin dato (2026): {s.tormenta.isna().sum()}")
    for punto in sorted(set(PUNTO_DE.values())):
        e = clima[(clima.punto == punto) & (clima.n_entrena > 0)]
        print(f"  Clima raro en {punto}: entrena {int(e.n_entrena.min())}–{int(e.n_entrena.max())} semanas; marcadas {s[f'{punto}_clima_raro'].sum()} "
              f"de {s[f'{punto}_clima_raro'].notna().sum()} en la reproducción")
    for clave in CLAVE.values():
        print(f"  Llegadas {clave}: " + s[f"{clave}_llegadas"].value_counts(dropna=False).to_string().replace("\n", " · "))
    return s


if __name__ == "__main__":
    construir()
