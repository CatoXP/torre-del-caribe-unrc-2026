# Autor: Brandon Uriel García Sánchez
# Módulo: Torre en vivo (pruebas, Fase 7)
# Qué hace:          Pruebas del motor de reglas (casos hechos a mano) y de la reproducción completa (cifras conocidas).
# Por qué así:       El motor es una función pura: cada regla de docs/decisiones/20-torre-en-vivo.md se prueba con una
#                    semana inventada SOLO para la prueba (no se muestra ni se guarda), y la reproducción con datos reales.
# Datos de entrada:  datos/gold/envivo_*.parquet; torre.envivo.motor.
# Alimenta a:        La confianza en la Fase 7.

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402
from torre.envivo.motor import Memoria, Plan, decidir, lunes_del_mes  # noqa: E402

GOLD = RAIZ / "datos" / "gold"
SUR = ["Chetumal", "Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur"]
PLAN = Plan(pesos_mes={(10, l): 4000.0 for l in SUR}, alta={(12, l) for l in SUR},
            libre={(10, "Chetumal"): 0.2, (10, "Bahía Calderitas–Oxtankah"): 0.6, (10, "Ruta arqueológica del sur"): 0.5})


def semana(**k):
    base = {"semana": "2025-10-06", "tormenta": False, "chetumal_clima_raro": False, "kohunlich_clima_raro": False,
            "chetumal_llegadas": "dentro", "bahia_llegadas": "dentro", "ruta_llegadas": "dentro",
            "cancun_estado": "concurrido", "riviera_estado": "concurrido"}
    return base | k


def test_lunes_del_mes():
    assert lunes_del_mes(pd.Timestamp("2025-10-06")) == 4  # octubre de 2025: 6, 13, 20 y 27
    assert lunes_del_mes(pd.Timestamp("2025-12-01")) == 5


def test_semana_tranquila_gasta_lo_planeado():
    d, n = decidir(semana(), PLAN, Memoria())
    assert all(x["accion"] == "encendido" and x["pesos_gastados"] == 1000 for x in d)  # 4,000 ÷ 4 lunes
    assert not n["ibas_al_norte"]


def test_clima_raro_pausa_solo_su_punto_y_el_dinero_pasa_a_la_siguiente():
    m = Memoria()
    d, _ = decidir(semana(chetumal_clima_raro=True, chetumal_lluvia_mm=80.0), PLAN, m)
    acc = {x["lugar"]: x["accion"] for x in d}
    assert acc == {"Chetumal": "pausado", "Bahía Calderitas–Oxtankah": "pausado", "Ruta arqueológica del sur": "encendido"}
    assert m.arrastre["Chetumal"] == 1000
    d, _ = decidir(semana(semana="2025-10-13"), PLAN, m)
    assert {x["lugar"]: x["pesos_gastados"] for x in d}["Chetumal"] == 2000 and m.arrastre["Chetumal"] == 0


def test_tormenta_pausa_los_tres_y_sin_dato_no_pausa():
    d, _ = decidir(semana(tormenta=True, tormenta_nombre="Prueba"), PLAN, Memoria())
    assert all(x["accion"] == "pausado" for x in d)
    d, _ = decidir(semana(tormenta=None), PLAN, Memoria())
    assert all(x["accion"] == "encendido" and x["sin_dato_tormentas"] for x in d)


def test_llegadas_arriba_pausan_abajo_no():
    d, _ = decidir(semana(ruta_llegadas="arriba", ruta_mes_dato="2025-09-01", bahia_llegadas="abajo"), PLAN, Memoria())
    acc = {x["lugar"]: x["accion"] for x in d}
    assert acc["Ruta arqueológica del sur"] == "pausado" and acc["Bahía Calderitas–Oxtankah"] == "encendido"


def test_temporada_alta_y_fuera_del_plan():
    d, _ = decidir(semana(semana="2025-12-01"), PLAN, Memoria())
    assert all(x["accion"] == "temporada alta" and x["pesos_gastados"] == 0 for x in d)
    d, _ = decidir(semana(semana="2025-08-04"), PLAN, Memoria())
    assert all(x["accion"] == "fuera del plan" for x in d)


def test_norte_lleno_manda_al_sur_con_mas_espacio_y_nunca_al_norte():
    d, n = decidir(semana(riviera_estado="saturado", chetumal_clima_raro=True), PLAN, Memoria())
    assert n["ibas_al_norte"] and n["destino"] == "Ruta arqueológica del sur"  # la Bahía (más libre) está pausada
    d, n = decidir(semana(riviera_estado="saturado"), PLAN, Memoria())
    assert n["destino"] == "Bahía Calderitas–Oxtankah"
    d, n = decidir(semana(semana="2025-12-01", cancun_estado="saturado"), PLAN, Memoria())
    assert n["norte_lleno"] == "Cancún" and not n["ibas_al_norte"]  # nadie encendido: no hay a dónde mandar


# ---------- Reproducción real ----------
pytestmark_real = pytest.mark.skipif(not (GOLD / "envivo_decisiones.parquet").exists(), reason="Aún no corre la Torre")


@pytestmark_real
def test_reproduccion_completa_y_en_orden():
    d = pd.read_parquet(GOLD / "envivo_decisiones.parquet")
    s = pd.read_parquet(GOLD / "envivo_senales.parquet")
    assert len(s) == 239 and d.semana.nunique() == 239 and d.lote.nunique() == 239
    assert d.groupby("lote").semana.first().is_monotonic_increasing
    assert d.pesos_gastados.sum() == pytest.approx(d.pesos_plan.sum())  # nada se pierde: lo pausado se gasta después


@pytestmark_real
def test_cifras_conocidas_de_la_reproduccion():
    s = pd.read_parquet(GOLD / "envivo_senales.parquet")
    assert round(s.corte_p90.iloc[0], 2) == 85.92 and round(s.corte_p50.iloc[0], 2) == 71.16
    assert set(s.tormenta_nombre.dropna()) == {"Lisa", "Nadine", "Sara"}
    assert s[s.semana > "2025-12-31"].tormenta.isna().all()  # HURDAT2 2026 aún no existe
    assert s.chetumal_clima_raro.sum() == 21 and s.kohunlich_clima_raro.sum() == 17
    d = pd.read_parquet(GOLD / "envivo_decisiones.parquet")
    pausas = d[d.accion == "pausado"].groupby("lugar").size()
    assert pausas.to_dict() == {"Bahía Calderitas–Oxtankah": 14, "Chetumal": 19, "Ruta arqueológica del sur": 15}
    n = pd.read_parquet(GOLD / "envivo_norte.parquet")
    assert n.ibas_al_norte.sum() == 6 and not n.destino.dropna().isin(["Cancún", "Riviera Maya"]).any()
