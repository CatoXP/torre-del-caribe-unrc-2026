# Autor: Brandon Uriel García Sánchez
# Módulo: Radar (pruebas del índice de presión, Fase 4 pieza 2)
# Qué hace:          Reproduce el ejemplo resuelto a mano de ECUACIONES.md §2 (Cancún, jul-2026), revisa las reglas del
#                    índice (pesos iguales, mín–máx común, cortes p50/p90, componentes de un solo lugar fuera) y la prueba
#                    de validez que motivó la opción D (el norte por encima del sur en 2025–2026).
# Por qué así:       El índice decide dónde NO se anuncia la campaña; si cambia en silencio, la campaña se equivoca.
# Datos de entrada:  datos/silver/ a través de torre.radar.panel e indice.
# Alimenta a:        La confianza en el Radar (Fase 4).

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from torre.radar import indice as ix  # noqa: E402
from torre.radar.panel import SILVER  # noqa: E402

pytestmark = pytest.mark.skipif(not (SILVER / "siturq").exists(), reason="Aún no existe Silver")


@pytest.fixture(scope="module")
def r():
    return ix.calcular()


def test_ipt_de_juguete():
    """Pesos iguales solo sobre lo que existe: (0.2 + 0.6) / 2 = 0.4; una fila sin nada → nulo, nunca 0."""
    z = pd.DataFrame({"lugar": ["a", "b"], "es_de_los_5": [True, True], "periodo": [0, 0],
                      "z_x": [0.2, np.nan], "z_y": [0.6, np.nan]})
    t = ix.ipt(z, ["x", "y"])
    assert t.ipt.iloc[0] == pytest.approx(0.4) and np.isnan(t.ipt.iloc[1])


def test_belice_fuera_por_ser_de_un_solo_lugar(r):
    _, _, comps = r
    assert "cruces_belice_x1000hab" not in comps
    assert comps == ["llegadas_tren_x1000hab", "cruceristas_x1000hab", "visitantes_inah_x1000hab", "llegadas_x_cuarto",
                     "ocupacion_pct"]


def test_ejemplo_a_mano_cancun(r):
    """ECUACIONES.md §2.1: Cancún jul-2026 → (0.0497 + 0.0001 + 0.0011 + 0.7214) / 4 = 0.1931 < p50 = 0.2577 → tranquilo."""
    base, cortes, _ = r
    fila = base[(base.lugar == "Cancún") & (base.periodo == "2026-07-01")].iloc[0]
    assert round(fila.ipt, 4) == 0.1931 and round(cortes[0], 4) == 0.2577 and fila.estado == "tranquilo"


def test_cortes_son_percentiles_comunes(r):
    base, (p50, p90), _ = r
    con = base[base.ipt.notna()]
    assert (con.ipt < p50).mean() == pytest.approx(0.5, abs=0.01)
    assert (con.ipt > p90).mean() == pytest.approx(0.1, abs=0.01)


def test_laguna_sin_dato_oficial_nunca_tranquila(r):
    base, _, _ = r
    assert (base[base.lugar == "Laguna Milagros–Xul-Ha"].estado == "sin dato oficial").all()


def test_validez_norte_arriba_del_sur_2025_2026(r):
    """La prueba que falló con mín–máx sin DataTur: en 2025–2026 el norte de referencia debe quedar arriba del sur."""
    base, _, _ = r
    m = base[base.periodo.dt.year >= 2025].groupby("lugar").ipt.mean()
    norte = m[["Cancún", "Playa del Carmen", "Cozumel", "Isla Mujeres", "Tulum"]].min()
    sur = m[["Chetumal", "Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur", "Maya Ka'an + Kantemó"]].max()
    assert norte > sur
