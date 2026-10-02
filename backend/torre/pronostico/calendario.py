# Autor: Brandon Uriel García Sánchez
# Módulo: Pronóstico
# Qué hace:          Calendario del planeador de viaje de la página: para cada lugar del planeador y cada mes que una
#                    persona puede elegir (del mes en curso a diciembre del año siguiente) dice cómo va a estar —
#                    temporada alta, normal o tranquila—, cuánta gente se espera (con su rango del 90 % si el mes está
#                    dentro del pronóstico), el clima normal, el riesgo de tormenta y, si es temporada alta, a qué otro
#                    lugar o en qué otro mes conviene ir.
# Por qué así:       - Regla de Brandon (01-oct-2026, "Forma del año + capacidad"): un mes es TEMPORADA ALTA si su
#                      índice de la forma del año es ≥ 1.20 (20 % o más arriba de un mes promedio) o si tiene ≥ 10 % de
#                      riesgo de rebasar la capacidad probada (Monte Carlo, pieza 4). Descartado: usar el semáforo del
#                      Radar (es del mes actual y los 5 lugares salen siempre tranquilos).
#                    - Para leerlo sin tecnicismos: índice < 1.00 = "tranquila" (menos gente que un mes promedio);
#                      1.00 a 1.19 = "normal".
#                    - Lugares del planeador (decisión de Brandon, 01-oct-2026, decisión 15): los 3 lugares del sur con
#                      serie (Chetumal, Bahía y Ruta) y Cancún y Riviera Maya como REFERENCIA. Maya Ka'an y la Laguna
#                      Milagros salieron del planeador porque no tienen serie: solo decían "sin dato". Siguen en el
#                      resto de la página. Cancún y Riviera Maya están para quien piensa ir al norte: si el mes está
#                      lleno, el planeador le recomienda un lugar del sur. NUNCA se recomienda ir al norte.
#                    - Temporada alta en el norte (Brandon, "Cortes del Radar"): su ocupación hotelera varía poco
#                      (Cancún: 64 % en sep, 80 % en mar), así que con la regla del índice ≥ 1.20 nunca saldría alta.
#                      Se usa el corte p50 del Radar (torre.radar.markov: 71.2 % de la ocupación semanal de los 7
#                      centros del norte): ocupación esperada ≥ p50 = alta ("concurrido" o "saturado" en el Radar);
#                      abajo = tranquila. Descartados: el índice ≥ 1.20 (nunca alta) y solo saturado ≥ p90 = 85.9 %
#                      (ningún mes pronosticado llega).
#                    - Tormentas en el norte: la probabilidad del sur cuenta tormentas a ≤ 200 km de Chetumal y no
#                      sirve para Cancún. Se aplica la MISMA regla (≤ 200 km, ≥ 34 nudos, 1966–2025) alrededor del punto
#                      de clima de cada lugar del norte.
#                    - Recomendación cuando es temporada alta: (1) el lugar del sur con el índice más bajo ese mes que
#                      no esté en temporada alta y (2) el mes más tranquilo del mismo lugar que no sea temporada alta,
#                      esté fuera de la temporada de tormentas (probabilidad < 9 %, la marca de la gráfica de escenarios)
#                      y llueva menos que el mes mediano del año en ese punto (Chetumal: 97 mm). Sin la condición de
#                      lluvia el mes sugerido casi siempre era junio, el más lluvioso (195 mm): tranquilo, pero mal
#                      consejo para un viajero.
#                    - Meses dentro del pronóstico (hasta jul-2027; Belice hasta jun-2027): cifra esperada _est con su
#                      rango. Meses después: solo la forma del año ("mes típico"), sin cifra. En el norte, la ocupación
#                      típica del mes (promedio de los años completos 2022–2025, medida).
#                    - Clima normal 1991–2020 del punto más cercano (Chetumal para Chetumal, Bahía y Laguna; Kohunlich
#                      para la Ruta; Cancún y Playa del Carmen para el norte).
# Datos de entrada:  datos/gold/pronostico_{series, forma_anio, mes, escenarios, poisson_tormentas};
#                    datos/silver/clima_diario, datos/silver/huracanes, datos/silver/datatur_ocupacion (cortes del Radar).
# Alimenta a:        Planeador "¿Cuándo conviene ir?" de la página: redirige a quien elige un mes saturado hacia otro
#                    lugar o mes del sur (la redistribución que pide el Problema Prototípico, hecha visible al viajero).

from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
GOLD = RAIZ / "datos" / "gold"
SILVER = RAIZ / "datos" / "silver"

ALTA_INDICE = 1.20
ALTA_RIESGO = 0.10
TORMENTA_TEMPORADA = 0.09
SUR = {  # lugar que se promueve → (serie del pronóstico, punto de clima)
    "Chetumal": ("Chetumal · cruces desde Belice", "chetumal"),
    "Bahía Calderitas–Oxtankah": ("Bahía Calderitas–Oxtankah · visitantes INAH", "chetumal"),
    "Ruta arqueológica del sur": ("Ruta arqueológica del sur · visitantes INAH", "kohunlich"),
}
NORTE = {  # referencia (no se promueve) → (serie de ocupación hotelera, punto de clima)
    "Cancún": ("Cancún (referencia) · ocupación hotelera", "cancun"),
    "Riviera Maya": ("Riviera Maya (referencia) · ocupación hotelera", "playa_del_carmen"),
}
LUGARES = {**SUR, **NORTE}


def nivel(indice: float | None, riesgo: float | None) -> str:
    """Regla del sur: índice de la forma del año y riesgo de rebasar la capacidad probada."""
    if indice is None or pd.isna(indice):
        return "sin dato"
    if indice >= ALTA_INDICE or (riesgo is not None and not pd.isna(riesgo) and riesgo >= ALTA_RIESGO):
        return "alta"
    return "tranquila" if indice < 1 else "normal"


def nivel_norte(ocupacion: float | None, corte: float) -> str:
    """Regla del norte: ocupación hotelera esperada (o típica) contra el corte p50 del Radar."""
    if ocupacion is None or pd.isna(ocupacion):
        return "sin dato"
    return "alta" if ocupacion >= corte else "tranquila"


def corte_radar() -> float:
    """p50 de la ocupación semanal de los 7 centros del norte: el corte "tranquilo / concurrido" del Radar (decisión 08)."""
    from torre.radar.markov import estados, ocupacion_semanal

    return float(estados(ocupacion_semanal())[1][0])


def tormentas_punto(punto: str) -> pd.Series:
    """Probabilidad de al menos una tormenta por mes alrededor de un punto del norte, con la regla del sur:
    tormenta tropical o huracán (≥ 34 nudos) a ≤ 200 km, de 1966 a 2025. λ_m = tormentas ÷ 60 años; P = 1 − e^(−λ_m)."""
    from torre.base.ingesta_abiertas import PUNTOS_CLIMA
    from torre.base.silver_huracanes import RADIO_KM, VIENTO_MIN_KT, km_haversine
    from torre.pronostico.escenarios import ANIO_FIN, ANIO_INICIO

    d = pd.read_parquet(SILVER / "huracanes", columns=["id_tormenta", "anio", "mes", "fecha", "hora_utc", "lat", "lon",
                                                         "viento_kt"])
    d = d.assign(anio=d.anio.astype(int))
    d = d[d.anio.between(ANIO_INICIO, ANIO_FIN) & (d.viento_kt.fillna(0) >= VIENTO_MIN_KT) & d.lat.notna()]
    la, lo = PUNTOS_CLIMA[punto]
    d = d[[km_haversine(a, b, la, lo) <= RADIO_KM for a, b in zip(d.lat, d.lon)]]
    # Una tormenta cuenta una vez, en el mes de su primer punto dentro del radio (igual que eventos_sur).
    ev = d.sort_values(["fecha", "hora_utc"]).groupby("id_tormenta").mes.first()
    n = ev.value_counts().reindex(range(1, 13), fill_value=0)
    return 1 - np.exp(-n / (ANIO_FIN - ANIO_INICIO + 1))


def ocupacion_tipica(serie: str) -> pd.Series:
    """Ocupación promedio de cada mes del año en los años completos (2022–2025): lo típico, medido."""
    from torre.pronostico.forma import anios_completos

    t = pd.read_parquet(GOLD / "pronostico_series.parquet")
    s = t[t.serie == serie]
    s = s[s.periodo.dt.year.isin(anios_completos(s))]
    return s.groupby(s.periodo.dt.month).valor.mean()


def clima_normal() -> pd.DataFrame:
    """Lluvia total media del mes (mm) y máxima media (°C) en 1991–2020, por punto."""
    d = pd.read_parquet(SILVER / "clima_diario", columns=["punto", "anio", "mes", "lluvia_mm", "temp_max_c"])
    d = d[d.anio.astype(int).between(1991, 2020)]
    lluvia = d.groupby(["punto", "anio", "mes"], observed=True).lluvia_mm.sum().groupby(["punto", "mes"]).mean()
    temp = d.groupby(["punto", "mes"], observed=True).temp_max_c.mean()
    return pd.DataFrame({"lluvia_mm": lluvia.round(0), "temp_max_c": temp.round(1)}).reset_index()


def meses_elegibles(hoy: date | None = None) -> list[pd.Timestamp]:
    hoy = hoy or date.today()
    inicio = pd.Timestamp(hoy.year, hoy.month, 1)
    return list(pd.date_range(inicio, pd.Timestamp(hoy.year + 1, 12, 1), freq="MS"))


def calendario(hoy: date | None = None) -> pd.DataFrame:
    forma = pd.read_parquet(GOLD / "pronostico_forma_anio.parquet")
    pron = pd.read_parquet(GOLD / "pronostico_mes.parquet")
    esc = pd.read_parquet(GOLD / "pronostico_escenarios.parquet")
    esc = esc[esc.golpe_tormenta_supuesto == 0]
    tormenta_sur = pd.read_parquet(GOLD / "pronostico_poisson_tormentas.parquet").set_index("mes").prob_tormenta
    tormentas = {lugar: tormenta_sur for lugar in SUR} | {lugar: tormentas_punto(p) for lugar, (_, p) in NORTE.items()}
    clima = clima_normal().set_index(["punto", "mes"])
    corte = corte_radar()
    tipica = {lugar: ocupacion_tipica(serie) for lugar, (serie, _) in NORTE.items()}

    filas = []
    for p in meses_elegibles(hoy):
        for lugar, (serie, punto) in LUGARES.items():
            m = p.month
            fila = {"lugar": lugar, "papel": "referencia" if lugar in NORTE else "promovida", "periodo": p, "mes": m,
                    "prob_tormenta": float(tormentas[lugar][m]),
                    "lluvia_normal_mm": float(clima.loc[(punto, m), "lluvia_mm"]),
                    "temp_max_normal_c": float(clima.loc[(punto, m), "temp_max_c"]), "punto_clima": punto,
                    "indice": None, "esperado_est": None, "minimo_90_est": None, "maximo_90_est": None,
                    "riesgo_capacidad": None, "unidad": None, "dentro_del_pronostico_flag": False,
                    "ocupacion_est": None, "ocupacion_tipica_pct": None, "corte_radar_pct": None}
            if serie:
                fila["indice"] = float(forma[(forma.serie == serie) & (forma.mes == m)].indice.iloc[0])
                f = pron[(pron.serie == serie) & (pron.periodo == p)]
                if len(f):
                    f = f.iloc[0]
                    e = esc[(esc.serie == serie) & (esc.periodo == p)].iloc[0]
                    fila.update(esperado_est=float(f.esperado_est), minimo_90_est=float(f.minimo_90_est),
                                maximo_90_est=float(f.maximo_90_est), riesgo_capacidad=float(e.riesgo_rebasar_capacidad),
                                unidad=f.unidad, dentro_del_pronostico_flag=True)
            if lugar in NORTE:
                # Ocupación del mes: el pronóstico si el mes está dentro; si no, lo típico de ese mes.
                fila["ocupacion_tipica_pct"] = round(float(tipica[lugar][m]), 2)
                fila["ocupacion_est"] = fila["esperado_est"] if fila["dentro_del_pronostico_flag"] else None
                fila["corte_radar_pct"] = round(corte, 2)
                ocup = fila["ocupacion_est"] if fila["ocupacion_est"] is not None else fila["ocupacion_tipica_pct"]
                fila["nivel"] = nivel_norte(ocup, corte)
            else:
                fila["nivel"] = nivel(fila["indice"], fila["riesgo_capacidad"])
            filas.append(fila)
    c = pd.DataFrame(filas)
    return recomendar(c, forma, tormentas, clima, tipica, corte)


def recomendar(c: pd.DataFrame, forma: pd.DataFrame, tormentas: dict, clima: pd.DataFrame, tipica: dict,
               corte: float) -> pd.DataFrame:
    """Si el mes es temporada alta: otro lugar DEL SUR (índice más bajo ese mes, sin temporada alta; nunca el norte) y
    otro mes para el mismo lugar (el más tranquilo que no sea alta, fuera de la temporada de tormentas y seco)."""
    c = c.copy()
    c["otro_lugar"], c["otro_mes"] = None, None
    for i, f in c[c.nivel == "alta"].iterrows():
        mismos = c[(c.periodo == f.periodo) & (c.lugar != f.lugar) & c.lugar.isin(list(SUR)) & c.indice.notna()
                   & (c.nivel != "alta")]
        if len(mismos):
            c.at[i, "otro_lugar"] = mismos.sort_values("indice").lugar.iloc[0]
        serie, punto = LUGARES[f.lugar]
        # Qué tan lleno es cada mes del año: índice en el sur; ocupación típica en el norte (con su propio corte).
        s, tope = ((tipica[f.lugar], corte) if f.lugar in NORTE
                   else (forma[forma.serie == serie].set_index("mes").indice, ALTA_INDICE))
        lluvia = clima.loc[punto].lluvia_mm
        seco = lluvia < lluvia.median()
        tormenta = tormentas[f.lugar]
        candidatos = s[(s < tope) & s.index.map(lambda m: tormenta[m] < TORMENTA_TEMPORADA and seco[m])]
        if len(candidatos):
            c.at[i, "otro_mes"] = int(candidatos.idxmin())
    return c


def guardar(hoy: date | None = None) -> pd.DataFrame:
    c = calendario(hoy)
    c.to_parquet(GOLD / "pronostico_calendario.parquet", index=False)
    return c


if __name__ == "__main__":
    c = guardar()
    pd.set_option("display.width", 220)
    c["mes_txt"] = c.periodo.dt.strftime("%Y-%m")
    print(c.pivot(index="mes_txt", columns="lugar", values="nivel").to_string())
    print(c[c.nivel == "alta"][["mes_txt", "lugar", "indice", "riesgo_capacidad", "otro_lugar", "otro_mes"]].round(3)
          .to_string(index=False))
