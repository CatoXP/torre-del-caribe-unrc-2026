# Autor: Brandon Uriel García Sánchez
# Módulo: Radar (pruebas del clustering de centros turísticos, Fase 4; agregado tras la auditoría)
# Qué hace:          Revisa que solo entren centros reales con sus 55 meses completos (sin agregados ni meses
#                    rellenados), el número de grupos por silueta y el ejemplo de silueta resuelto a mano (ECUACIONES §2.4).
# Por qué así:       Un agregado como "Total" o un centro con meses vacíos cambiaría los grupos sin que nadie lo note.
# Datos de entrada:  datos/silver/datatur_ocupacion (a través de torre.radar.clustering).
# Alimenta a:        La confianza en la minería del Radar (criterio 3 de la rúbrica).

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from torre.radar import clustering as cl  # noqa: E402

pytestmark = pytest.mark.skipif(not (cl.SILVER / "datatur_ocupacion").exists(), reason="Aún no existe Silver")


@pytest.fixture(scope="module")
def r():
    return cl.correr()


def test_solo_centros_completos(r):
    p = r["perfiles"]
    assert len(p) == 55 and not p.isna().any().any()
    for agregado in ("Total", "Centros De Playa", "Ciudades", "Grandes", "Otros"):
        assert agregado not in p.index


def test_k_por_silueta(r):
    assert r["k"] == max(r["siluetas"], key=r["siluetas"].get) == 2
    assert round(r["siluetas"][2], 3) == 0.450


def test_quintana_roo_en_sus_grupos(r):
    g = r["grupos"]
    assert g["Cancun"] == g["Riviera Maya"] == g["Playacar"] == g["Los Cabos"]
    assert g["Cozumel"] == g["Isla Mujeres"] != g["Cancun"]


def test_silueta_a_mano_cancun(r):
    """s(i) = (b − a) / máx(a, b): a = distancia media a su grupo, b = distancia media al otro grupo → 0.623."""
    p, g = r["perfiles"], r["grupos"]
    dist = np.sqrt(((p - p.loc["Cancun"]) ** 2).sum(axis=1))
    a = dist[(g == g["Cancun"]) & (dist.index != "Cancun")].mean()
    b = dist[g != g["Cancun"]].mean()
    assert (round(a, 2), round(b, 2), round((b - a) / max(a, b), 3)) == (43.84, 116.21, 0.623)
