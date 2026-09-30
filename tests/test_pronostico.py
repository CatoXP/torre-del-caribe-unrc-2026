# Autor: Brandon Uriel García Sánchez
# Módulo: Pronóstico (pruebas)
# Qué hace:          Pruebas de la Fase 5: que las series a pronosticar tengan la forma esperada y que las reglas de los
#                    meses que no entrenan (cierre, mes parcial, pandemia) marquen los meses correctos.
# Por qué así:       Cada regla se comprueba con un mes real que se revisó a mano (docs/decisiones/11-pronostico.md).
# Datos de entrada:  datos/gold/pronostico_series.parquet (y Silver de INAH, SITUR-Q y DataTur).
# Alimenta a:        La confianza en el calendario de la campaña.

import sys
from pathlib import Path

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


@pytest.fixture(scope="module")
def t() -> pd.DataFrame:
    return series.construir()


def mes(t, serie, periodo):
    f = t[(t.serie == serie) & (t.periodo == pd.Timestamp(periodo))]
    assert len(f) == 1
    return f.iloc[0]


def test_cuatro_series_y_meses(t):
    r = series.resumen(t)
    assert r.meses.to_dict() == {BAHIA: 127, CANCUN: 55, BELICE: 90, RUTA: 127}
    assert r.entrenan.to_dict() == {BAHIA: 90, CANCUN: 55, BELICE: 66, RUTA: 91}


def test_solo_cancun_es_referencia(t):
    assert t.groupby("serie").papel.first().to_dict()[CANCUN] == "referencia"
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
    assert mes(t, BELICE, "2022-02-01").motivo_hueco == "pandemia" and mes(t, BELICE, "2022-03-01").entrena_flag


def test_valor_observado_se_conserva(t):
    # Belice abr-2020: 57 cruces; se marca, pero no se borra ni se cambia.
    assert mes(t, BELICE, "2020-04-01").valor == 57


def test_cancun_ocupacion_calculada_con_cuartos(t):
    assert mes(t, CANCUN, "2022-01-01").valor == pytest.approx(67.99, abs=0.01)
