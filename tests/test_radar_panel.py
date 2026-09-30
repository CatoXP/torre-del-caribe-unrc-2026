# Autor: Brandon Uriel García Sánchez
# Módulo: Radar (pruebas del panel mensual, Fase 4 pieza 1)
# Qué hace:          Revisa la forma del panel (15 lugares × meses, sin filas repetidas) y que reproduzca cifras
#                    conocidas de SITUR-Q y del INAH. Comprueba además que ningún visitante del INAH se cuente dos veces.
# Por qué así:       El panel es la base del índice de presión: si una zona se asigna a dos lugares o se pierde, el
#                    Radar se equivoca en silencio. Estas pruebas lo impiden.
# Datos de entrada:  datos/silver/{siturq, inah, iter} (a través de torre.radar.panel).
# Alimenta a:        La confianza en el Radar (Fase 4).

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from torre.radar import panel as pn  # noqa: E402

pytestmark = pytest.mark.skipif(not (pn.SILVER / "siturq").exists(), reason="Aún no existe Silver")


@pytest.fixture(scope="module")
def p() -> pd.DataFrame:
    return pn.panel_mensual()


def _anual(p, lugar, variable, anio=2025):
    return p[(p.lugar == lugar) & (p.periodo.dt.year == anio)][variable].sum()


def test_forma(p):
    assert p.lugar.nunique() == 15 and not p.duplicated(["lugar", "periodo"]).any()
    assert p.periodo.min() == pd.Timestamp("2022-01-01")
    assert (p.groupby("lugar").size() == p.groupby("lugar").size().iloc[0]).all()  # todos con los mismos meses


def test_cifras_conocidas(p):
    assert _anual(p, "Chetumal", "llegadas_tren") == 53_825          # página: Tren Maya 2025
    assert _anual(p, "Chetumal", "cruces_belice") == 653_306          # página: frontera 2025
    assert _anual(p, "Ruta arqueológica del sur", "visitantes_inah") == 66_628   # selección de regiones
    assert _anual(p, "Bahía Calderitas–Oxtankah", "visitantes_inah") == 11_017
    assert p[(p.lugar == "Chetumal") & (p.periodo == "2026-07-01")].cuartos.iloc[0] == 2_114


def test_ocupacion_no_suma_filas(p):
    """ocupacion_hotelera trae 3 filas por mes; el porcentaje es ocupados ÷ disponibles (Chetumal 2024 = 58.0 %)."""
    c = p[(p.lugar == "Chetumal") & (p.periodo.dt.year == 2024)]
    assert round(100 * c.cuartos_noche_ocupados.sum() / c.cuartos_noche_disponibles.sum(), 1) == 58.0
    assert p.ocupacion_pct.dropna().between(0, 100).all()


def test_inah_sin_doble_conteo(p):
    """La suma del panel = la suma de todas las zonas arqueológicas del INAH en Quintana Roo (cada zona en un lugar)."""
    i = pd.read_parquet(pn.SILVER / "inah", columns=["clasificacion", "periodo", "visitantes", "es_qroo"])
    i = i[i.es_qroo & (i.clasificacion == "Zona Arqueológica")]
    i = i[pd.to_datetime(i.periodo.astype(str)) >= pn.DESDE]
    assert p.visitantes_inah.sum() == i.visitantes.sum()


def test_poblacion_de_los_5(p):
    pob = p.drop_duplicates("lugar").set_index("lugar").poblacion
    assert pob[pn.LUGARES_5].sum() == 229_247   # igual que la tabla de criterios y el planteamiento


def test_laguna_sin_datos_se_declara(p):
    """Laguna Milagros no tiene serie turística: todo su panel queda nulo (no se rellena)."""
    laguna = p[p.lugar == "Laguna Milagros–Xul-Ha"]
    assert laguna[pn.VARIABLES].isna().all().all()
