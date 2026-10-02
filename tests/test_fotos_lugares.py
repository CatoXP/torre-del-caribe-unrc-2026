# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña (pruebas)
# Qué hace:          Pruebas de las fotos de los 5 lugares: cada una existe, no cambió (huella SHA-256), tiene licencia
#                    libre y crédito, y su coordenada GPS cae dentro del municipio de su lugar.
# Por qué así:       Brandon (01-oct-2026): "que sean fotos de las zonas que sí sean de Quintana Roo". La regla de
#                    ubicación comprobada (docs/decisiones/06-pagina.md) se prueba aquí foto por foto, con el mismo mapa
#                    municipal (torre.base.ubicaciones.municipio_de).
# Datos de entrada:  frontend/fotos/lugares/ (torre.campana.fotos_lugares).
# Alimenta a:        La confianza en que cada foto de la página es del lugar que dice.

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402
from torre.base.ubicaciones import municipio_de  # noqa: E402
from torre.campana.fotos_lugares import FOTOS, MUNICIPIOS  # noqa: E402

NORTE = {"Cancún", "Riviera Maya"}  # referencia en el planeador (decisión 15)

CARPETA = RAIZ / "frontend" / "fotos" / "lugares"
pytestmark = pytest.mark.skipif(not (CARPETA / "creditos.json").exists(), reason="Aún no se descargan las fotos")


@pytest.fixture(scope="module")
def creditos():
    return json.loads((CARPETA / "creditos.json").read_text(encoding="utf-8"))


def test_fotos_de_los_5_lugares_y_el_norte(creditos):
    assert len(creditos) == sum(len(f) for _, f in FOTOS.values()) == 40
    assert {c["lugar"] for c in creditos} == set(FOTOS) and len(set(FOTOS) - NORTE) == 5
    assert sum(len(FOTOS[x][1]) for x in NORTE) == 12


def test_coordenada_dentro_del_municipio(creditos):
    for c in creditos:
        mun = FOTOS[c["lugar"]][0]
        assert municipio_de(c["lat"], c["lon"]) == mun, f"{c['archivo']}: fuera de {MUNICIPIOS[mun]}"
        assert c["municipio"] == MUNICIPIOS[mun]
    # Cancún en Benito Juárez y la Riviera Maya en Solidaridad (Playa del Carmen); el sur, en sus 2 municipios.
    assert FOTOS["Cancún"][0] == "005" and FOTOS["Riviera Maya"][0] == "008"
    assert {FOTOS[x][0] for x in set(FOTOS) - NORTE} <= {"004", "002"}


def test_archivos_intactos_y_ligeros(creditos):
    for c in creditos:
        datos = (RAIZ / "frontend" / c["archivo"]).read_bytes()
        assert hashlib.sha256(datos).hexdigest() == c["sha256"], c["archivo"]
        assert len(datos) < 450 * 1024, f"{c['archivo']} pesa más de 450 KB"


def test_licencia_libre_y_credito(creditos):
    for c in creditos:
        assert c["licencia"].startswith(("CC BY", "CC0", "Public domain")), c["archivo"]
        assert c["autor"] and c["url_original"].startswith("https://commons.wikimedia.org/"), c["archivo"]


def test_sin_fotos_de_otros_estados_ni_lugares_excluidos():
    # La galería de platillos (Mérida, Campeche…) se retiró: ninguna foto de la página sale de fuera de los 5 lugares.
    assert not (RAIZ / "frontend" / "fotos" / "comida").exists()
    import re
    sur = json.dumps({k: v for k, v in FOTOS.items() if k not in NORTE}, ensure_ascii=False)
    assert not re.search(r"m[eé]rida|campeche|tulum|canc[uú]n|bacalar|mahahual|cozumel", sur, re.I)
    # El norte es referencia, pero ni ahí entran Tulum, Cozumel ni otros lugares con sargazo o saturación.
    norte = json.dumps({k: FOTOS[k] for k in NORTE}, ensure_ascii=False)
    assert not re.search(r"m[eé]rida|campeche|tulum|bacalar|mahahual|cozumel|holbox|isla mujeres|sargaz", norte, re.I)
