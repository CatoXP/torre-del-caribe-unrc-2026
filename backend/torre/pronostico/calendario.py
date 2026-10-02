# Autor: Brandon Uriel García Sánchez
# Módulo: Pronóstico
# Qué hace:          Calendario del planeador de viaje de la página: para cada uno de los 5 lugares y cada mes que una
#                    persona puede elegir (del mes en curso a diciembre del año siguiente) dice cómo va a estar —
#                    temporada alta, normal o tranquila—, cuánta gente se espera (con su rango del 90 % si el mes está
#                    dentro del pronóstico), el clima normal, el riesgo de tormenta y, si es temporada alta, a qué otro
#                    lugar o en qué otro mes conviene ir.
# Por qué así:       - Regla de Brandon (01-oct-2026, "Forma del año + capacidad"): un mes es TEMPORADA ALTA si su
#                      índice de la forma del año es ≥ 1.20 (20 % o más arriba de un mes promedio) o si tiene ≥ 10 % de
#                      riesgo de rebasar la capacidad probada (Monte Carlo, pieza 4). Descartado: usar el semáforo del
#                      Radar (es del mes actual y los 5 lugares salen siempre tranquilos).
#                    - Para leerlo sin tecnicismos: índice < 1.00 = "tranquila" (menos gente que un mes promedio);
#                      1.00 a 1.19 = "normal". Maya Ka'an y la Laguna Milagros no tienen serie propia: "sin dato de
#                      afluencia" (se muestra solo clima y tormenta; no se inventa una temporada).
#                    - Recomendación cuando es temporada alta: (1) el lugar del sur con el índice más bajo ese mes que
#                      no esté en temporada alta y (2) el mes más tranquilo del mismo lugar que no sea temporada alta,
#                      esté fuera de la temporada de tormentas (probabilidad < 9 %, la marca de la gráfica de escenarios)
#                      y llueva menos que el mes mediano del año en ese punto (Chetumal: 97 mm). Sin la condición de
#                      lluvia el mes sugerido casi siempre era junio, el más lluvioso (195 mm): tranquilo, pero mal
#                      consejo para un viajero.
#                    - Meses dentro del pronóstico (hasta jul-2027; Belice hasta jun-2027): cifra esperada _est con su
#                      rango. Meses después: solo la forma del año ("mes típico"), sin cifra.
#                    - Clima normal 1991–2020 del punto más cercano (Chetumal para Chetumal, Bahía y Laguna; Kohunlich
#                      para la Ruta; Felipe Carrillo Puerto para Maya Ka'an).
# Datos de entrada:  datos/gold/pronostico_{series, forma_anio, mes, escenarios, poisson_tormentas};
#                    datos/silver/clima_diario.
# Alimenta a:        Planeador "¿Cuándo conviene ir?" de la página: redirige a quien elige un mes saturado hacia otro
#                    lugar o mes del sur (la redistribución que pide el Problema Prototípico, hecha visible al viajero).

from datetime import date
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
GOLD = RAIZ / "datos" / "gold"
SILVER = RAIZ / "datos" / "silver"

ALTA_INDICE = 1.20
ALTA_RIESGO = 0.10
TORMENTA_TEMPORADA = 0.09
LUGARES = {  # lugar → (serie del pronóstico o None, punto de clima)
    "Chetumal": ("Chetumal · cruces desde Belice", "chetumal"),
    "Bahía Calderitas–Oxtankah": ("Bahía Calderitas–Oxtankah · visitantes INAH", "chetumal"),
    "Ruta arqueológica del sur": ("Ruta arqueológica del sur · visitantes INAH", "kohunlich"),
    "Maya Ka'an + Kantemó": (None, "felipe_carrillo_puerto"),
    "Laguna Milagros–Xul-Ha": (None, "chetumal"),
}


def nivel(indice: float | None, riesgo: float | None) -> str:
    if indice is None or pd.isna(indice):
        return "sin dato"
    if indice >= ALTA_INDICE or (riesgo is not None and not pd.isna(riesgo) and riesgo >= ALTA_RIESGO):
        return "alta"
    return "tranquila" if indice < 1 else "normal"


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
    tormenta = pd.read_parquet(GOLD / "pronostico_poisson_tormentas.parquet").set_index("mes").prob_tormenta
    clima = clima_normal().set_index(["punto", "mes"])

    filas = []
    for p in meses_elegibles(hoy):
        for lugar, (serie, punto) in LUGARES.items():
            m = p.month
            fila = {"lugar": lugar, "periodo": p, "mes": m, "prob_tormenta": float(tormenta[m]),
                    "lluvia_normal_mm": float(clima.loc[(punto, m), "lluvia_mm"]),
                    "temp_max_normal_c": float(clima.loc[(punto, m), "temp_max_c"]), "punto_clima": punto,
                    "indice": None, "esperado_est": None, "minimo_90_est": None, "maximo_90_est": None,
                    "riesgo_capacidad": None, "unidad": None, "dentro_del_pronostico_flag": False}
            if serie:
                fila["indice"] = float(forma[(forma.serie == serie) & (forma.mes == m)].indice.iloc[0])
                f = pron[(pron.serie == serie) & (pron.periodo == p)]
                if len(f):
                    f = f.iloc[0]
                    e = esc[(esc.serie == serie) & (esc.periodo == p)].iloc[0]
                    fila.update(esperado_est=float(f.esperado_est), minimo_90_est=float(f.minimo_90_est),
                                maximo_90_est=float(f.maximo_90_est), riesgo_capacidad=float(e.riesgo_rebasar_capacidad),
                                unidad=f.unidad, dentro_del_pronostico_flag=True)
            fila["nivel"] = nivel(fila["indice"], fila["riesgo_capacidad"])
            filas.append(fila)
    c = pd.DataFrame(filas)
    return recomendar(c, forma, tormenta, clima)


def recomendar(c: pd.DataFrame, forma: pd.DataFrame, tormenta: pd.Series, clima: pd.DataFrame) -> pd.DataFrame:
    """Si el mes es temporada alta: otro lugar (índice más bajo ese mes, sin temporada alta) y otro mes para el mismo
    lugar (índice más bajo entre los meses que no son alta y sin temporada de tormentas)."""
    c = c.copy()
    c["otro_lugar"], c["otro_mes"] = None, None
    for i, f in c[c.nivel == "alta"].iterrows():
        mismos = c[(c.periodo == f.periodo) & (c.lugar != f.lugar) & c.indice.notna() & (c.nivel != "alta")]
        if len(mismos):
            c.at[i, "otro_lugar"] = mismos.sort_values("indice").lugar.iloc[0]
        serie, punto = LUGARES[f.lugar]
        s = forma[forma.serie == serie].set_index("mes").indice
        lluvia = clima.loc[punto].lluvia_mm
        seco = lluvia < lluvia.median()
        candidatos = s[(s < ALTA_INDICE) & s.index.map(lambda m: tormenta[m] < TORMENTA_TEMPORADA and seco[m])]
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
