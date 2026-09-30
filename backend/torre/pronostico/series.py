# Autor: Brandon Uriel García Sánchez
# Módulo: Pronóstico
# Qué hace:          Pieza 1 de la Fase 5. Arma las series mensuales que se van a pronosticar (una fila por serie y mes)
#                    y marca cada mes que NO sirve para entrenar, con su motivo: cierre, mes parcial o pandemia.
# Por qué así:       - Qué se pronostica (decisión de Brandon, 30-sep-2026, "Medidas + norte"): solo series MEDIDAS que
#                      llegan a 2026. Visitantes INAH de la Bahía (Oxtankah) y de la Ruta arqueológica (Kohunlich +
#                      Dzibanché + Ichkabal), 127 meses; cruces desde Belice por Chetumal, 90 meses; y ocupación hotelera
#                      de Cancún como REFERENCIA (es el público de la campaña, no un lugar que se promueve), 55 meses.
#                      Descartadas: estimar la ocupación del sur 2025–2026 (contradice la Fase 3) y solo INAH (Chetumal
#                      quedaría sin serie). Maya Ka'an y Laguna Milagros no tienen serie propia: se declara.
#                    - Meses que no entrenan (decisión de Brandon, "Hueco + forma del año"): un mes cerrado no es "cero
#                      demanda". Si se entrenara con esos ceros, el modelo aprendería que abril puede tener 0 visitantes.
#                      Reglas, en este orden:
#                        1. cierre: la zona reporta 0 visitantes (INAH: COVID abr–ago-2020, obras de 2024);
#                        2. mes parcial: el mes justo antes de un cierre o justo después de reabrir (Kohunlich ene-2025:
#                           750 visitantes, contra 3,481 en feb-2025);
#                        3. pandemia: de mar-2020 a dic-2021 en el INAH (2021 quedó en 52 % del nivel de 2019 en
#                           Kohunlich, con aforo limitado; 2022 ya en 81 %) y de mar-2020 a jun-2022 en Belice. La frontera
#                           reabrió en feb-2022 (41.7 % del mismo mes de 2019), pero de marzo a junio siguió recuperándose
#                           (65.1, 69.5, 80.2 y 82.2 %); desde jul-2022 no bajó de 86 %. Decisión de Brandon (30-sep-2026):
#                           esos 4 meses son recuperación, no temporada (STL los confundía con temporada: pieza 2).
#                      El valor observado se conserva; solo se marca. Los límites de la pandemia son parámetros visibles.
#                    - Región = suma de sus zonas. Si una zona que ya existía está en cierre o en mes parcial, el mes de
#                      la región entero se marca (sumar solo las abiertas bajaría el total de forma artificial).
#                      Ichkabal abrió en ene-2025: antes no existía, así que su ausencia no es cierre.
# Datos de entrada:  datos/silver/inah, datos/silver/siturq (frontera_belice), datos/silver/datatur_ocupacion.
# Alimenta a:        Los modelos de pronóstico (pieza 3) → calendario de la campaña: en qué meses conviene promover cada
#                    lugar y en qué meses el norte está lleno (cuando más gente puede redirigirse al sur).

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
SILVER = RAIZ / "datos" / "silver"
GOLD = RAIZ / "datos" / "gold"

PANDEMIA_INAH = ("2020-03-01", "2021-12-01")
PANDEMIA_BELICE = ("2020-03-01", "2022-06-01")
ZONAS = {
    "Bahía Calderitas–Oxtankah": ["Z.A. de Oxtankah"],
    "Ruta arqueológica del sur": ["Z.A. de Kohunlich", "Z.A. de Dzibanché-Kinichná", "Z.A de Ichkabal"],
}


def _motivos_zona(v: pd.Series) -> pd.Series:
    """Motivo por mes de UNA zona (índice = periodo, ordenado): 'cierre', 'mes parcial' o nulo."""
    cerrado = v == 0
    parcial = ~cerrado & (cerrado.shift(1, fill_value=False) | cerrado.shift(-1, fill_value=False))
    return pd.Series(None, index=v.index, dtype="object").mask(parcial, "mes parcial").mask(cerrado, "cierre")


def _pandemia(periodo: pd.Series, limites: tuple[str, str]) -> pd.Series:
    return periodo.between(pd.Timestamp(limites[0]), pd.Timestamp(limites[1]))


def series_inah() -> pd.DataFrame:
    i = pd.read_parquet(SILVER / "inah", columns=["nombre", "periodo", "visitantes", "estado"])
    i = i[i.estado == "Quintana Roo"]
    i["periodo"] = pd.to_datetime(i.periodo)
    salida = []
    for lugar, zonas in ZONAS.items():
        m = i[i.nombre.isin(zonas)].groupby(["periodo", "nombre"]).visitantes.sum().unstack().sort_index()
        motivos = pd.DataFrame({z: _motivos_zona(m[z].dropna()) for z in m.columns}).reindex(m.index)
        # El mes de la región hereda el motivo más fuerte de sus zonas (cierre > mes parcial).
        motivo = motivos.apply(lambda f: "cierre" if (f == "cierre").any() else
                               ("mes parcial" if (f == "mes parcial").any() else None), axis=1)
        s = pd.DataFrame({"periodo": m.index, "valor": m.sum(axis=1, min_count=1).values, "motivo_hueco": motivo.values,
                          "zonas_abiertas": m.gt(0).sum(axis=1).values})
        s.loc[s.motivo_hueco.isna() & _pandemia(s.periodo, PANDEMIA_INAH), "motivo_hueco"] = "pandemia"
        s["serie"], s["lugar"], s["papel"] = f"{lugar} · visitantes INAH", lugar, "promovida"
        s["unidad"], s["fuente"] = "visitantes al mes", "INAH vía DataTur (BdINAH)"
        salida.append(s)
    return pd.concat(salida, ignore_index=True)


def serie_belice() -> pd.DataFrame:
    s = pd.read_parquet(SILVER / "siturq")
    s = s[(s.unidad.astype(str) == "Chetumal") & (s.indicador.astype(str) == "frontera_belice") & ~s.hueco_flag]
    s = s.assign(periodo=pd.to_datetime(s.periodo)).sort_values("periodo")[["periodo", "valor"]]
    s["motivo_hueco"] = None
    s.loc[_pandemia(s.periodo, PANDEMIA_BELICE), "motivo_hueco"] = "pandemia"
    s["serie"], s["lugar"], s["papel"] = "Chetumal · cruces desde Belice", "Chetumal", "promovida"
    s["unidad"], s["fuente"] = "cruces al mes", "SITUR-Q (frontera México–Belice)"
    return s


def serie_cancun() -> pd.DataFrame:
    d = pd.read_parquet(SILVER / "datatur_ocupacion")
    c = d[(d.frecuencia == "mensual") & (d.centro.astype(str) == "Cancun") & (d.tipo_fila == "centro")]
    c = c.assign(periodo=pd.to_datetime(c.periodo)).sort_values("periodo")
    # Ocupación = cuartos ocupados / cuartos disponibles (nunca promediar porcentajes).
    s = pd.DataFrame({"periodo": c.periodo.values,
                      "valor": (c.cuartos_ocupados / c.cuartos_disponibles * 100).round(2).values})
    s["motivo_hueco"] = None
    s.loc[s.valor.isna(), "motivo_hueco"] = "sin publicar"
    s["serie"], s["lugar"], s["papel"] = "Cancún (referencia) · ocupación hotelera", "Cancún", "referencia"
    s["unidad"], s["fuente"] = "% de cuartos ocupados", "SECTUR-DataTur (monitoreo mensual)"
    return s


def construir() -> pd.DataFrame:
    t = pd.concat([series_inah(), serie_belice(), serie_cancun()], ignore_index=True)
    t["entrena_flag"] = t.valor.notna() & t.motivo_hueco.isna()
    columnas = ["serie", "lugar", "papel", "periodo", "valor", "unidad", "motivo_hueco", "entrena_flag",
                "zonas_abiertas", "fuente"]
    return t[columnas].sort_values(["serie", "periodo"]).reset_index(drop=True)


def resumen(t: pd.DataFrame) -> pd.DataFrame:
    """Cuántos meses tiene cada serie y cuántos entrenan, por motivo."""
    r = t.groupby("serie").agg(desde=("periodo", "min"), hasta=("periodo", "max"), meses=("periodo", "size"),
                               entrenan=("entrena_flag", "sum"))
    motivos = t.pivot_table(index="serie", columns="motivo_hueco", values="periodo", aggfunc="size", fill_value=0)
    return r.join(motivos).fillna(0)


def guardar(t: pd.DataFrame):
    GOLD.mkdir(parents=True, exist_ok=True)
    t.to_parquet(GOLD / "pronostico_series.parquet", index=False)


if __name__ == "__main__":
    t = construir()
    guardar(t)
    pd.set_option("display.width", 200)
    print(resumen(t).to_string())
