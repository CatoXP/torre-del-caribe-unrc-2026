# Autor: Brandon Uriel García Sánchez
# Módulo: Radar (pruebas de la cadena de Markov semanal, Fase 4 pieza 3b)
# Qué hace:          Revisa los conteos y la matriz de transición, el ejemplo a dos semanas resuelto a mano
#                    (ECUACIONES.md §2.3) y que el backtest compare contra la persistencia sin ver el futuro.
# Por qué así:       La probabilidad de saturación del norte decide cuándo ofrecerle el sur al turista; si la matriz está
#                    mal contada, la campaña se activa a destiempo.
# Datos de entrada:  datos/silver/datatur_ocupacion (a través de torre.radar.markov).
# Alimenta a:        La confianza en el Radar (Fase 4) y en la Torre en vivo (Fase 7).

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from torre.radar import markov as mk  # noqa: E402

pytestmark = pytest.mark.skipif(not (mk.SILVER / "datatur_ocupacion").exists(), reason="Aún no existe Silver")


@pytest.fixture(scope="module")
def r():
    return mk.correr()


def test_conteos_y_matriz(r):
    assert int(r["n"].to_numpy().sum()) == 1_666           # 7 centros × 238 pares de semanas consecutivas
    assert np.allclose(r["P"].sum(axis=1), 1)
    assert round(r["P"].loc["tranquilo", "tranquilo"], 3) == round(765 / 830, 3) == 0.922


def test_cortes_comunes(r):
    assert (round(r["cortes"][0], 1), round(r["cortes"][1], 1)) == (71.2, 85.9)


def test_dos_semanas_a_mano(r):
    """P(saturado en 2 semanas | tranquilo hoy) = Σ_j p_tj · p_js = 0.922·0 + 0.078·0.069 + 0·0.726 ≈ 0.005."""
    P = r["P"]
    a_mano = sum(P.loc["tranquilo", j] * P.loc[j, "saturado"] for j in mk.ESTADOS)
    assert a_mano == pytest.approx(mk.a_k_semanas(P, "tranquilo", 2)["saturado"])
    assert round(a_mano, 3) == 0.005


def test_estacionaria(r):
    pi = r["pi"]
    assert np.allclose(pi.to_numpy() @ r["P"].to_numpy(), pi.to_numpy()) and pi.sum() == pytest.approx(1)


def test_markov_mejor_calibrado_que_persistencia(r):
    b = r["backtest"].set_index(["k_semanas", "metodo"]).brier
    for k in (1, 4, 8):
        assert b[(k, "Markov")] < b[(k, "Persistencia")]
