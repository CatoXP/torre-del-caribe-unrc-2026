# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos (pruebas)
# Qué hace:          Pruebas de las tablas Silver que necesita la Fase 5 (Pronóstico): huracanes (HURDAT2), clima
#                    (Open-Meteo) y tipo de cambio e inflación (FRED). Forma de la tabla y cifras conocidas.
# Por qué así:       Cada regla de limpieza de docs/decisiones/10-silver-fase5.md se comprueba con un caso real: la
#                    definición de "tormenta que afecta al sur", la hora local, los días sin cotización que no se rellenan.
# Datos de entrada:  datos/silver/huracanes, clima_diario, clima_horario, fred_diario, fred_mensual; Bronze de FRED.
# Alimenta a:        La confianza en el Pronóstico (Poisson de huracanes, variables de clima y de tipo de cambio).

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402
from torre.base.silver_huracanes import eventos_sur, km_haversine  # noqa: E402

SILVER = RAIZ / "datos" / "silver"
pytestmark = pytest.mark.skipif(not (SILVER / "huracanes").exists(), reason="Aún no se construye Silver de la Fase 5")


@pytest.fixture(scope="module")
def huracanes() -> pd.DataFrame:
    return pd.read_parquet(SILVER / "huracanes")


@pytest.fixture(scope="module")
def dia() -> pd.DataFrame:
    return pd.read_parquet(SILVER / "clima_diario")


@pytest.fixture(scope="module")
def fred_mes() -> pd.DataFrame:
    return pd.read_parquet(SILVER / "fred_mensual")


# ---------- Huracanes ----------
def test_hurdat2_completo(huracanes):
    assert len(huracanes) == 55_524
    assert huracanes.id_tormenta.nunique() == 1_988


def test_lineas_irregulares_se_conservan_sin_inventar(huracanes):
    raras = huracanes[huracanes.formato_irregular_flag]
    assert len(raras) == 2
    sin_lat = raras[raras.lat.isna()]
    assert len(sin_lat) == 1 and sin_lat.iloc[0].id_tormenta == "AL231975"  # latitud no se adivina
    assert not raras.afecta_sur_flag.any()


def test_faltantes_oficiales_son_nulos(huracanes):
    assert not (huracanes.presion_mb == -999).any() and huracanes.presion_mb.isna().any()


def test_haversine_a_mano():
    # 1 grado de latitud sobre el mismo meridiano = 2·π·6371/360 = 111.19 km
    assert km_haversine(18.5, -88.3, 19.5, -88.3) == pytest.approx(111.19, abs=0.01)
    assert km_haversine(18.5, -88.3, 18.5, -88.3) == 0


def test_31_eventos_desde_1966(huracanes):
    ev = eventos_sur(huracanes)
    assert len(ev) == 31
    assert round(len(ev) / 60, 3) == 0.517
    assert ev.mes.value_counts().sort_index().to_dict() == {5: 1, 6: 3, 7: 1, 8: 9, 9: 8, 10: 6, 11: 3}


def test_dean_2007_y_carmen_1974(huracanes):
    ev = eventos_sur(huracanes).set_index("nombre")
    assert ev.loc["DEAN"].viento_max_kt == 150 and ev.loc["DEAN"].mes == 8
    assert ev.loc["CARMEN"].km_min == pytest.approx(15.3)


# ---------- Clima ----------
def test_clima_diario_forma(dia):
    assert len(dia) == 224_232
    assert dia.punto.nunique() == 8
    assert not dia.sin_dato_flag.any()


def test_clima_papel_de_los_puntos(dia):
    papel = dia.groupby("punto").papel_campana.first().to_dict()
    assert {p for p, v in papel.items() if v == "promovida"} == {"chetumal", "kohunlich", "felipe_carrillo_puerto"}
    assert papel["tulum"] == "referencia" and papel["bacalar"] == "excluida"


def test_lluvia_junio_chetumal(dia):
    # Lluvia media de junio 1991–2020 en Chetumal: suma por mes y promedio de los 30 años.
    j = dia[(dia.punto == "chetumal") & (dia.mes == 6) & dia.anio.astype(int).between(1991, 2020)]
    assert j.groupby("anio", observed=True).lluvia_mm.sum().mean() == pytest.approx(195, abs=0.5)


def test_clima_horario_hora_local():
    h = pd.read_parquet(SILVER / "clima_horario", columns=["fecha_hora_utc", "fecha_hora_local", "sin_dato_flag"])
    assert len(h) == 542_784
    assert ((h.fecha_hora_utc - h.fecha_hora_local) == pd.Timedelta(hours=5)).all()
    assert not h.sin_dato_flag.any()


# ---------- FRED ----------
def test_dias_sin_cotizacion_no_se_rellenan():
    d = pd.read_parquet(SILVER / "fred_diario")
    assert len(d) == 8_575 and int(d.sin_dato_flag.sum()) == 336
    assert d[d.sin_dato_flag].pesos_por_dolar.isna().all()


def test_promedio_mensual_con_dias_observados(fred_mes):
    # Agosto de 2026: promedio de los días con dato, calculado directo del CSV crudo.
    crudo = pd.read_csv(sorted((RAIZ / "datos" / "bronze").glob("fred/*/DEXMXUS.csv"))[-1])
    ago = pd.to_numeric(crudo[crudo.observation_date.str.startswith("2026-08")].DEXMXUS, errors="coerce")
    fila = fred_mes[fred_mes.periodo.astype(str) == "2026-08-01"].iloc[0]
    assert fila.pesos_por_dolar == pytest.approx(ago.mean()) == pytest.approx(17.0609, abs=1e-4)
    assert fila.n_dias_observados == ago.notna().sum() == 21
    assert fila.inflacion_eeuu_indice == pytest.approx(334.131)


def test_mes_en_curso_marcado(fred_mes):
    marcados = fred_mes[fred_mes.mes_incompleto_flag]
    assert len(marcados) == 1 and str(marcados.iloc[0].periodo) == "2026-09-01"
