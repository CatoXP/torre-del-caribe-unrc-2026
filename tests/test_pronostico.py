# Autor: Brandon Uriel García Sánchez
# Módulo: Pronóstico (pruebas)
# Qué hace:          Pruebas de la Fase 5: que las series a pronosticar tengan la forma esperada y que las reglas de los
#                    meses que no entrenan (cierre, mes parcial, pandemia) marquen los meses correctos.
# Por qué así:       Cada regla se comprueba con un mes real que se revisó a mano (docs/decisiones/11-pronostico.md).
# Datos de entrada:  datos/gold/pronostico_series.parquet (y Silver de INAH, SITUR-Q y DataTur).
# Alimenta a:        La confianza en el calendario de la campaña.

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402
from torre.pronostico import series  # noqa: E402

pytestmark = pytest.mark.skipif(not (RAIZ / "datos" / "silver" / "inah").exists(), reason="Falta Silver")

BAHIA = "Bahía Calderitas–Oxtankah · visitantes INAH"
RUTA = "Ruta arqueológica del sur · visitantes INAH"
BELICE = "Chetumal · cruces desde Belice"
CANCUN = "Cancún (referencia) · ocupación hotelera"
RIVIERA = "Riviera Maya (referencia) · ocupación hotelera"  # agregada el 01-oct-2026 (decisión 15)


@pytest.fixture(scope="module")
def t() -> pd.DataFrame:
    return series.construir()


def mes(t, serie, periodo):
    f = t[(t.serie == serie) & (t.periodo == pd.Timestamp(periodo))]
    assert len(f) == 1
    return f.iloc[0]


def test_cinco_series_y_meses(t):
    r = series.resumen(t)
    assert r.meses.to_dict() == {BAHIA: 127, CANCUN: 55, BELICE: 90, RIVIERA: 55, RUTA: 127}
    assert r.entrenan.to_dict() == {BAHIA: 90, CANCUN: 55, BELICE: 62, RIVIERA: 55, RUTA: 91}


def test_solo_el_norte_es_referencia(t):
    papel = t.groupby("serie").papel.first().to_dict()
    assert papel[CANCUN] == papel[RIVIERA] == "referencia"
    assert set(t[t.papel == "promovida"].lugar) == {"Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur", "Chetumal"}


def test_cierre_no_es_cero_demanda(t):
    f = mes(t, BAHIA, "2024-05-01")
    assert f.valor == 0 and f.motivo_hueco == "cierre" and not f.entrena_flag


def test_mes_parcial_al_reabrir(t):
    assert mes(t, BAHIA, "2024-11-01").motivo_hueco == "mes parcial"   # Oxtankah reabre con 81 visitantes
    assert mes(t, RUTA, "2025-02-01").motivo_hueco == "mes parcial"    # Dzibanché reabre con 249


def test_region_cerrada_si_una_zona_cierra(t):
    # ene-2025: Kohunlich ya abrió (750) pero Dzibanché sigue en 0 → la región no entrena ese mes.
    f = mes(t, RUTA, "2025-01-01")
    assert f.motivo_hueco == "cierre" and f.zonas_abiertas == 2  # Kohunlich e Ichkabal


def test_ichkabal_nuevo_no_es_cierre(t):
    assert mes(t, RUTA, "2019-06-01").entrena_flag  # antes de 2025 Ichkabal no existía


def test_pandemia(t):
    assert mes(t, RUTA, "2021-06-01").motivo_hueco == "pandemia"
    assert mes(t, RUTA, "2022-01-01").entrena_flag
    # Belice: la recuperación de mar–jun 2022 (65–82 % de 2019) cuenta como pandemia (decisión de Brandon)
    assert mes(t, BELICE, "2022-06-01").motivo_hueco == "pandemia" and mes(t, BELICE, "2022-07-01").entrena_flag


def test_valor_observado_se_conserva(t):
    # Belice abr-2020: 57 cruces; se marca, pero no se borra ni se cambia.
    assert mes(t, BELICE, "2020-04-01").valor == 57


def test_cancun_ocupacion_calculada_con_cuartos(t):
    assert mes(t, CANCUN, "2022-01-01").valor == pytest.approx(67.99, abs=0.01)


# ---------- Pieza 2: forma del año ----------
from torre.pronostico import forma  # noqa: E402


@pytest.fixture(scope="module")
def estacional(t):
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return forma.calcular(t)


def test_solo_anios_completos(t):
    assert forma.anios_completos(t[t.serie == BAHIA]) == [2016, 2017, 2018, 2019, 2022, 2025]
    assert forma.anios_completos(t[t.serie == RUTA]) == [2016, 2017, 2018, 2019, 2022, 2023]
    assert forma.anios_completos(t[t.serie == BELICE]) == [2019, 2023, 2024, 2025]


def test_razon_a_mano(t):
    # Ruta, enero de 2019: 7,935 visitantes ÷ promedio del año (64,139 / 12 = 5,344.92) = 1.4846
    r = forma.razones(t[t.serie == RUTA])
    assert r.loc[2019, 1] == pytest.approx(7935 / (64139 / 12), abs=1e-4) == pytest.approx(1.4846, abs=1e-4)


def test_indices_promedian_uno(estacional):
    f, _ = estacional
    assert f.groupby("serie").indice.mean().round(3).eq(1).all()


def test_ruta_enero_alto_septiembre_bajo(estacional):
    f, r = estacional
    ruta = f[f.serie == RUTA].set_index("mes").indice
    assert ruta[1] == pytest.approx(1.606, abs=1e-3) and ruta[9] == pytest.approx(0.4963, abs=1e-3)
    assert r.set_index("serie").loc[RUTA, "fuerza_estacional"] == pytest.approx(0.793, abs=1e-3)


def test_stl_confirma_inah_y_explica_belice(estacional):
    _, r = estacional
    c = r.set_index("serie").corr_con_stl
    assert c[RUTA] > 0.9 and c[BAHIA] > 0.9 and c[CANCUN] > 0.9
    # Con mar–jun 2022 como pandemia (decisión de Brandon), el tramo empieza en jul-2022 y STL coincide (antes 0.446)
    assert c[BELICE] == pytest.approx(0.847, abs=1e-3)


def test_sur_acompana_al_norte(estacional):
    a = forma.acompana_al_norte(estacional[0])
    assert a["Ruta arqueológica del sur"] == pytest.approx(0.834, abs=1e-3) and a["Chetumal"] == pytest.approx(0.257, abs=1e-3)


# ---------- Pieza 3: modelos, origen móvil, rango del 90 % y elección ----------
from torre.pronostico import intervalos, modelos  # noqa: E402

GOLD = RAIZ / "datos" / "gold"


@pytest.fixture(scope="module")
def backtest():
    return pd.read_parquet(GOLD / "pronostico_backtest.parquet")


def test_forma_del_anio_no_ve_el_futuro(t):
    # Con origen jun-2019, la forma del año de la Ruta solo puede usar 2016–2018.
    s = t[t.serie == RUTA]
    esperado = forma.indice_estacional(forma.razones(s[s.periodo.dt.year <= 2018]))
    assert modelos.forma_hasta(s, pd.Timestamp("2019-06-01")).round(6).equals(esperado.round(6))


def test_comparacion_justa_mismos_pares(backtest):
    n = backtest.groupby(["serie", "modelo"]).size().unstack()
    assert (n.nunique(axis=1) == 1).all()  # todos los modelos se evalúan en los mismos (origen, destino)
    assert n.iloc[:, 0].to_dict() == {BAHIA: 366, CANCUN: 438, BELICE: 366, RIVIERA: 438, RUTA: 378}


def test_solo_destinos_que_entrenan(backtest, t):
    util = t.set_index(["serie", "periodo"]).entrena_flag
    assert util.reindex(pd.MultiIndex.from_frame(backtest[["serie", "destino"]])).all()


def test_error_log_a_mano(backtest):
    f = backtest[(backtest.serie == BAHIA) & (backtest.modelo == "Regresión con clima")].iloc[0]
    assert f.error_log == pytest.approx(abs(np.log(f.pronostico / f.real)))


def test_pronostico_negativo_es_error_total(backtest):
    neg = backtest[backtest.pronostico <= 0]
    assert len(neg) == 4 and set(neg.modelo) == {"Holt-Winters con tendencia amortiguada"}
    assert np.isinf(neg.error_log).all()


def test_cuantil_conformal_a_mano():
    # 20 errores 1..20: k = ⌈21 × 0.9⌉ = 19 → el 19.º más chico
    assert intervalos.cuantil_conformal(np.arange(1, 21, dtype=float)) == 19


def test_eleccion_de_brandon():
    e = pd.read_parquet(GOLD / "pronostico_eleccion.parquet")
    elegidos = e[e.elegido_flag].set_index("serie").modelo.to_dict()
    assert elegidos == {BAHIA: "Regresión con clima", BELICE: "Regresión con clima", RUTA: "Regresión con clima",
                        CANCUN: "Línea base (ingenuo estacional)", RIVIERA: "Holt-Winters sin tendencia"}
    # Riviera Maya: el mismo criterio elige un modelo con más error que la línea base, porque la línea base (66.7 %),
    # la regresión y Gradient Boosting (74.4 %) no llegan a 80 % de cobertura. Se declara en la decisión 15.
    rm = e[e.serie == RIVIERA].set_index("modelo")
    assert rm.loc["Holt-Winters sin tendencia", "mae_vs_base"] > 1
    assert rm.loc["Línea base (ingenuo estacional)", "cobertura_pct"] < 80 <= rm.loc["Holt-Winters sin tendencia", "cobertura_pct"]
    ruta = e[e.serie == RUTA].set_index("modelo")
    # Holt-Winters sin tendencia tiene menos error en la Ruta, pero su rango no llega a 80 %
    assert ruta.loc["Holt-Winters sin tendencia", "mae"] < ruta.loc["Regresión con clima", "mae"]
    assert ruta.loc["Holt-Winters sin tendencia", "cobertura_pct"] < 80 <= ruta.loc["Regresión con clima", "cobertura_pct"]


def test_pronostico_final_bahia_diciembre():
    f = pd.read_parquet(GOLD / "pronostico_mes.parquet")
    assert f.groupby("serie").size().eq(12).all()
    r = f[(f.lugar == "Bahía Calderitas–Oxtankah") & (f.periodo == pd.Timestamp("2026-12-01"))].iloc[0]
    assert (round(r.esperado_est), round(r.minimo_90_est), round(r.maximo_90_est)) == (1311, 959, 1793)
    assert (f.minimo_90_est < f.esperado_est).all() and (f.esperado_est < f.maximo_90_est).all()


# ---------- Pieza 4: Poisson de tormentas, Monte Carlo y sensibilidad ----------
from torre.pronostico import escenarios  # noqa: E402


def test_poisson_a_mano():
    p = escenarios.poisson_tormentas().set_index("mes")
    assert p.eventos.sum() == 31
    # agosto: 9 eventos en 60 años → λ = 0.15 → P = 1 − e^(−0.15) = 0.1393
    assert p.loc[8, "lambda"] == pytest.approx(0.15) and p.loc[8, "prob_tormenta"] == pytest.approx(0.1393, abs=1e-4)
    assert (p.loc[[12, 1, 2, 3, 4], "prob_tormenta"] == 0).all()
    # al menos una tormenta en el año: 1 − e^(−31/60) = 1 − 0.5965 = 0.4035
    assert 1 - np.exp(-p["lambda"].sum()) == pytest.approx(0.4035, abs=1e-4)


@pytest.fixture(scope="module")
def mc():
    return (pd.read_parquet(GOLD / "pronostico_escenarios.parquet"),
            pd.read_parquet(GOLD / "pronostico_escenarios_anual.parquet"))


def test_escenarios_ordenados(mc):
    meses, anual = mc
    assert (meses.malo_p10_est <= meses.probable_p50_est).all() and (meses.probable_p50_est <= meses.bueno_p90_est).all()
    assert (anual.malo_p10_est < anual.bueno_p90_est).all()


def test_golpe_de_tormenta_es_supuesto_y_solo_en_el_sur(mc):
    meses, anual = mc
    assert set(meses[meses.papel == "promovida"].golpe_tormenta_supuesto) == {0.0, 0.25, 0.5}
    assert set(meses[meses.papel == "referencia"].golpe_tormenta_supuesto) == {0.0}
    # un golpe más fuerte nunca sube el escenario malo del año
    for _, g in anual[anual.lugar != "Cancún"].groupby("lugar"):
        assert g.sort_values("golpe_tormenta_supuesto").malo_p10_est.is_monotonic_decreasing


def test_capacidad_probada(mc, t):
    meses, _ = mc
    cap = meses.groupby("lugar")[["capacidad_probada", "capacidad_probada_mes"]].first()
    assert cap.loc["Ruta arqueológica del sur", "capacidad_probada"] == 10465
    assert cap.loc["Ruta arqueológica del sur", "capacidad_probada_mes"] == pd.Timestamp("2018-01-01")
    assert mes(t, RUTA, "2018-01-01").valor == 10465


def test_riesgo_de_capacidad_en_meses_pico(mc):
    m = mc[0][mc[0].golpe_tormenta_supuesto == 0]
    peor = m.loc[m.groupby("lugar").riesgo_rebasar_capacidad.idxmax()].set_index("lugar").periodo.dt.month
    assert peor["Ruta arqueológica del sur"] == 1 and peor["Chetumal"] == 12 and peor["Bahía Calderitas–Oxtankah"] == 12


def test_sensibilidad_medida():
    s = pd.read_parquet(GOLD / "pronostico_sensibilidad.parquet").set_index(["lugar", "variable"])
    lluvia, dolar = "lluvia (+100 mm sobre lo normal)", "tipo de cambio (+1 peso por dólar)"
    assert s.loc[("Bahía Calderitas–Oxtankah", lluvia), "efecto_pct"] == pytest.approx(-9.667, abs=1e-3)
    assert s.loc[("Ruta arqueológica del sur", dolar), "significativo_flag"]
    assert not s.loc[("Chetumal", dolar), "significativo_flag"]  # la hipótesis del peso barato para Belice no se sostiene
