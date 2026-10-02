# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña (pruebas)
# Qué hace:          Pruebas de la vitrina (postales, experiencias y rutas) y de la validación de los aportes del equipo.
# Por qué así:       Lo que convence de viajar tiene que salir de datos que existen (regla de oro 1): sin precios, sin
#                    fotos del norte en las postales, cada experiencia con su fuente y cada aporte con autor, fecha,
#                    lugar y permiso (decisión 16).
# Datos de entrada:  datos/gold, datos/silver, frontend/fotos/lugares, docs/aportes.
# Alimenta a:        La confianza en las secciones "Vive el sur", "Postales" y "Lo que vivimos".

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402
from torre.campana import aportes, vitrina  # noqa: E402

pytestmark = pytest.mark.skipif(not (RAIZ / "datos" / "gold" / "lugares_clasificados.parquet").exists(),
                                reason="Falta Gold")


@pytest.fixture(scope="module")
def v():
    return vitrina.vitrina(4, {"chicos": 107, "medianos": 38, "grandes": 0})


def test_postales_solo_del_sur(v):
    assert len(v["postales"]) == 28
    assert not {p["lugar"] for p in v["postales"]} & {"Cancún", "Riviera Maya"}
    assert all(p["autor"] and p["licencia"] for p in v["postales"])


def test_experiencias_con_fuente_y_sin_precios(v):
    import json
    assert len(v["experiencias"]) == 6
    assert all(e["fuente"] and e["dato"] and e["negocios"] for e in v["experiencias"])
    texto = json.dumps(v, ensure_ascii=False)
    assert "$" not in texto and "precio" not in texto.replace("Sin precios", "").replace("sin precios", "")
    for e in v["experiencias"]:
        assert (RAIZ / "frontend" / e["foto"]).exists(), e["foto"]


def test_dato_de_las_piramides(v):
    # Ejemplo a mano: Kohunlich 21,850 + Dzibanché 6,592 + Ichkabal 38,186 = 66,628 en 2025 → 66,628 / 365 = 182.5 → 183
    p = next(e for e in v["experiencias"] if e["clave"] == "piramides")
    assert "183 personas al día" in p["dato"]


def test_rutas(v):
    r = {x["titulo"]: x for x in v["rutas"]}
    assert r["Bahía y pirámides"]["km"] == [8, 59] and r["Bahía y pirámides"]["mes"] == 5
    assert r["Pueblos de Maya Ka'an"]["planeador"] is None  # sin serie: no se manda al planeador
    assert all(len(x["km"]) == len(x["paradas"]) - 1 for x in v["rutas"])
    # Cada ruta lleva foto real (un comentario mal puesto la había borrado: la página mostraba una imagen rota)
    assert all((RAIZ / "frontend" / x["foto"]).exists() for x in v["rutas"])


BUENO = {"tipo": "resena", "lugar": "Chetumal", "autor": "A. B.", "fecha": "2026-09-01", "texto": "x", "permiso": True,
         "estrellas": 5}


@pytest.mark.parametrize("cambio, motivo", [
    ({"lugar": "Tulum"}, "lugar fuera"), ({"permiso": False}, "faltan campos"), ({"autor": ""}, "faltan campos"),
    ({"estrellas": 6}, "estrellas"), ({"fecha": "2099-01-01"}, "fecha futura"), ({"fecha": "ayer"}, "AAAA-MM-DD"),
    ({"tipo": "foto", "archivo": "no_existe.jpg"}, "no existe"),
])
def test_aporte_rechazado(cambio, motivo):
    assert motivo in aportes.validar({**BUENO, **cambio})


def test_aporte_bueno():
    assert aportes.validar(BUENO) is None
