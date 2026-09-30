# Autor: Brandon Uriel García Sánchez
# Módulo: Radar (pruebas)
# Qué hace:          Comprueba la tabla de criterios de la Fase 3 (datos/gold/criterios_regiones.parquet) con cifras que
#                    se pueden recalcular a mano (docs/metodologia/ECUACIONES.md §2).
# Por qué así:       La tabla confirma las 5 regiones: si una regla o una fuente cambia, estas pruebas lo detectan.
# Datos de entrada:  backend/torre/radar/criterios.py (lee Silver).
# Alimenta a:        La confianza en la selección de regiones y en los topes de la Fase 6.

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402

pytestmark = pytest.mark.skipif(not (RAIZ / "datos" / "silver" / "inah").exists(), reason="Faltan tablas Silver")


@pytest.fixture(scope="module")
def tabla():
    from torre.radar.criterios import calcular_criterios

    return calcular_criterios().set_index("region")


def test_las_5_regiones_pasan_sargazo_y_cierres(tabla):
    promovidas = tabla[tabla.papel == "promovida"]
    assert len(promovidas) == 5
    assert promovidas.c2_pasa.all() and not (promovidas.c1_sargazo == "afectada").any()


def test_regla_de_12_meses_abierta(tabla):
    """Dzibanché reabrió en feb-2025: de feb-2025 a jul-2026 son 18 meses; Oxtankah reabrió en nov-2024: 21."""
    assert tabla.loc["Ruta arqueológica del sur", "c2_meses_abierta_min"] == 18
    assert tabla.loc["Bahía Calderitas–Oxtankah", "c2_meses_abierta_min"] == 21


def test_ocupacion_2024_sin_promediar_porcentajes(tabla):
    """Chetumal 2024: 458,696 / 791,016 = 58.0 %. Maya Ka'an: 38.6 %. Norte: 73–77 %."""
    assert tabla.loc["Chetumal", "c3_ocupacion_2024_pct"] == 58.0
    assert tabla.loc["Maya Ka'an + Kantemó", "c3_ocupacion_2024_pct"] == 38.6
    assert tabla.loc["Cancún", "c3_ocupacion_2024_pct"] == 76.1


def test_presion_por_residente(tabla):
    """Ruta sur: 66,628 visitantes / 6,098 residentes = 10.93; Tulum: 1,031,443 / 33,374 = 30.91."""
    assert tabla.loc["Ruta arqueológica del sur", "c3_visitantes_inah_por_residente"] == 10.93
    assert tabla.loc["Tulum", "c3_visitantes_inah_por_residente"] == 30.91
    assert not tabla.loc["Tulum", "c2_pasa"]  # cierres de negocios reportados en 2026
