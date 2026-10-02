# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña (pruebas, Fase 6)
# Qué hace:          Pruebas del reparto del presupuesto: que cumpla cada regla elegida por Brandon y que el resultado
#                    coincida con el ejemplo resuelto a mano de docs/metodologia/ECUACIONES.md §4.
# Por qué así:       Un optimizador puede devolver "Optimal" con una restricción mal escrita; por eso cada regla se
#                    comprueba sobre la solución, no sobre el modelo.
# Datos de entrada:  datos/gold/presupuesto_*.parquet y torre.campana.presupuesto.
# Alimenta a:        La confianza en la Fase 6 (cuánto dinero, dónde y cuándo).

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402

GOLD = RAIZ / "datos" / "gold"
pytestmark = pytest.mark.skipif(not (GOLD / "presupuesto_plan.parquet").exists(), reason="Aún no se corre la Fase 6")


@pytest.fixture(scope="module")
def sol():
    from torre.campana.presupuesto import resolver
    return resolver()


def test_ejemplo_a_mano(sol):
    from torre.campana.presupuesto import benchmarks, pesos_por_dolar
    b, (tc, _) = benchmarks(), pesos_por_dolar()
    assert round(tc, 2) == 17.06
    r_g = b["cvr_google"] / (b["cpc_google_usd"] * tc)      # 0.0575 ÷ (2.12 × 17.06) = 1.59 por cada $1,000
    r_f = b["cvr_google"] / (b["cpc_facebook_usd"] * tc)    # 0.0575 ÷ (0.51 × 17.06) = 6.61 por cada $1,000
    assert round(r_g * 1000, 2) == 1.59 and round(r_f * 1000, 2) == 6.61
    B = 250_000 * 9 / 12
    assert sol["presupuesto"] == pytest.approx(187_500)
    assert sol["visitantes_esperados"] == pytest.approx(0.7 * B * r_f + 0.3 * B * r_g, rel=1e-6)
    assert round(sol["visitantes_esperados"], 1) == 956.8


def test_reglas_se_cumplen(sol):
    p, t = sol["plan"], sol["tabla"]
    B = sol["presupuesto"]
    assert p.pesos.sum() == pytest.approx(B, rel=1e-6)
    canal = p.groupby("canal").pesos.sum() / B
    assert canal.max() <= 0.70 + 1e-6
    lugar = p.groupby("lugar").pesos.sum() / B
    assert (lugar >= 0.15 - 1e-6).all() and len(lugar) == 3
    celda = p.groupby(["periodo", "lugar"]).agg(pesos=("pesos", "sum"), conv=("conversiones_est", "sum")).reset_index()
    c = celda.merge(t, on=["periodo", "lugar"])
    assert (c[c.nivel == "alta"].pesos < 0.01).all()  # cero anuncio en temporada alta
    assert (c.probable_p50_est + c.conv <= c.capacidad_probada + 1e-6).all()  # capacidad probada
    assert set(p.lugar) <= {"Chetumal", "Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur"}  # nunca el norte


def test_reparto_proporcional_al_espacio(sol):
    c = sol["plan"].groupby(["periodo", "lugar"]).pesos.sum()
    t = sol["tabla"].set_index(["periodo", "lugar"])
    permitidas = [k for k, v in sol["permitida"].items() if v]
    share = t.loc[permitidas, "libre"] / t.loc[permitidas, "libre"].sum()
    assert (c.loc[permitidas] / c.sum()).values == pytest.approx(share.values, abs=1e-6)
    assert sol["desvio_proporcional"] == pytest.approx(0, abs=1e-6)


def test_costo_de_reglas_y_precio_sombra():
    r = pd.read_parquet(GOLD / "presupuesto_reglas.parquet").set_index("regla")
    assert r.loc["Tope de 70 % por canal", "costo_pct"] == pytest.approx(29.51, abs=0.01)
    assert (r.drop("Tope de 70 % por canal").costo_visitantes.abs() < 1e-3).all()  # a este presupuesto no cuestan
    s = pd.read_parquet(GOLD / "presupuesto_precios_sombra.parquet").set_index("regla")
    assert s.loc["presupuesto", "precio_sombra"] * 1000 == pytest.approx(1.59, abs=0.01)  # el peso extra va a Google


def test_pareto_no_decrece():
    f = pd.read_parquet(GOLD / "presupuesto_pareto.parquet").sort_values("ocupacion_max")
    v = f.visitantes_esperados.values
    assert all(a <= b + 1e-3 for a, b in zip(v, v[1:]))  # tolerancia del solucionador (CBC)
    assert f.set_index("ocupacion_max").visitantes_esperados[0.4] == pytest.approx(956.78, abs=0.01)


def test_reparto_ruta_octubre_a_mano(sol):
    # ECUACIONES §4.4: libre = 1 − 3,688 / 10,465 = 0.6476; π = 0.6476 / 8.0004 = 0.0809
    t = sol["tabla"].set_index(["periodo", "lugar"])
    permitidas = [k for k, v in sol["permitida"].items() if v]
    assert len(permitidas) == 20 and t.loc[permitidas, "libre"].sum() == pytest.approx(8.0004, abs=1e-4)
    p = sol["plan"].set_index(["periodo", "lugar", "canal"]).pesos
    celda = (pd.Timestamp("2026-10-01"), "Ruta arqueológica del sur")
    assert p[celda + ("Facebook",)] == pytest.approx(10_624, abs=1)
    assert p[celda + ("Google",)] == pytest.approx(4_553, abs=1)
