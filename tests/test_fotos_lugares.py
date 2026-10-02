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
from torre.base.ubicaciones import MUNICIPIO_ESPERADO, municipio_de  # noqa: E402
from torre.campana.fotos_lugares import FOTOS  # noqa: E402

CARPETA = RAIZ / "frontend" / "fotos" / "lugares"
pytestmark = pytest.mark.skipif(not (CARPETA / "creditos.json").exists(), reason="Aún no se descargan las fotos")


@pytest.fixture(scope="module")
def creditos():
    return json.loads((CARPETA / "creditos.json").read_text(encoding="utf-8"))


def test_fotos_de_los_5_lugares(creditos):
    assert len(creditos) == sum(len(f) for _, f in FOTOS.values()) == 28
    assert {c["lugar"] for c in creditos} == set(FOTOS) and len(FOTOS) == 5


def test_coordenada_dentro_del_municipio(creditos):
    for c in creditos:
        mun = FOTOS[c["lugar"]][0]
        assert municipio_de(c["lat"], c["lon"]) == mun, f"{c['archivo']}: fuera de {MUNICIPIO_ESPERADO[mun]}"
        assert c["municipio"] == MUNICIPIO_ESPERADO[mun]


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
    texto = json.dumps(FOTOS, ensure_ascii=False)
    assert not re.search(r"m[eé]rida|campeche|tulum|canc[uú]n|bacalar|mahahual|cozumel", texto, re.I)
