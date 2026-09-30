# Autor: Brandon Uriel García Sánchez
# Módulo: Radar (pruebas del planteamiento, Fase 3)
# Qué hace:          Comprueba que el planteamiento reproduce el ejemplo resuelto a mano de ECUACIONES.md §1-ter y que
#                    sus cifras cuadran con las de la tabla de criterios y la página.
# Por qué así:       Regla de oro 7: el ejemplo a mano y el código deben dar lo mismo. Si alguien cambia la regla de las
#                    zonas de SITUR-Q o la lista de localidades, estas pruebas lo detectan.
# Datos de entrada:  datos/silver/{siturq, inah, denue, iter}.
# Alimenta a:        La confianza en el planteamiento (criterio 1 de la rúbrica).

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from torre.radar import planteamiento as pl  # noqa: E402

pytestmark = pytest.mark.skipif(not (pl.SILVER / "siturq").exists(), reason="Aún no existe Silver")


@pytest.fixture(scope="module")
def conc() -> pd.DataFrame:
    return pl.concentracion().set_index("dimension")


def test_hhi_casos_extremos():
    """Reparto parejo → HHI = 1/N y HHI* = 0; una unidad dominante → HHI* cerca de 1."""
    r = pl.cuotas_y_hhi(pd.Series([5, 5, 5, 5]))
    assert r["hhi"] == pytest.approx(0.25) and r["hhi_normalizado"] == pytest.approx(0)
    assert pl.cuotas_y_hhi(pd.Series([999, 1]))["hhi_normalizado"] > 0.99


def test_ejemplo_a_mano_aviones(conc):
    """ECUACIONES.md §1-ter: avión 2024, HHI = 0.8586, HHI* = 0.811, Chetumal 1.4 %."""
    a = conc.loc["Llegadas en avión"]
    assert a.periodo == "2024" and a.total == 15_959_277
    assert (a.hhi, a.hhi_normalizado, a.cuota_5_lugares_pct) == (0.859, 0.811, 1.4)


def test_poblacion_de_los_5_lugares_cuadra_con_criterios():
    """Los actores usan 229,247 habitantes: la suma de las 5 regiones de la tabla de criterios (sin las referencias)."""
    fila = pl.actores().set_index("actor").loc["Comunidades de los 5 lugares"]
    assert fila.cifra_medida == "229,247 habitantes"


def test_cuota_de_los_5_lugares(conc):
    assert conc.loc["Población", "cuota_5_lugares_pct"] == 12.3
    assert conc.loc["Cuartos de hotel", "cuota_5_lugares_pct"] == 1.7
    assert conc.loc["Visitantes a sitios del INAH", "cuota_5_lugares_pct"] == 4.1
    assert conc.loc["Población", "razon_vs_poblacion"] == 1.0


def test_zonas_no_son_suma_de_miembros():
    """Por eso el total estatal de cuartos suma destinos + zonas y no miembros (ver NIVEL_ESTATAL)."""
    z = pl.comprobar_zonas().set_index("zona")
    assert z.loc["Riviera Maya", "diferencia"] > 30_000
    assert pl.concentracion().set_index("dimension").loc["Cuartos de hotel", "total"] == 140_664


def test_inventario_marca_los_huecos():
    inv = pl.inventario_variables().set_index("clave")
    assert set(inv[inv.papel == "hueco"].index) == {"afluencia_turistas", "derrama_turistas", "derrama_visitantes"}
    assert inv.loc["aereos_llegadas", "periodo_con_dato"] == "2019-01 a 2024-12"
