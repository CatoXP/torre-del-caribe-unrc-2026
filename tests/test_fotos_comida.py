# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña (pruebas)
# Qué hace:          Pruebas de la galería de comida: cada foto existe, no cambió desde que se descargó (huella SHA-256),
#                    tiene licencia libre y crédito completo, y nada menciona un lugar excluido.
# Por qué así:       Regla de oro 4 (solo fuentes con licencia que lo permita) y 9 (solo los 5 lugares; el norte, como
#                    referencia). Una foto sin autor o con licencia restrictiva no puede publicarse.
# Datos de entrada:  frontend/fotos/comida/ (torre.campana.fotos_comida).
# Alimenta a:        La confianza en que la página puede publicarse sin problemas de derechos.

import hashlib
import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402
from torre.campana.fotos_comida import PLATILLOS  # noqa: E402

CARPETA = RAIZ / "frontend" / "fotos" / "comida"
pytestmark = pytest.mark.skipif(not (CARPETA / "creditos.json").exists(), reason="Aún no se descargan las fotos")


@pytest.fixture(scope="module")
def creditos():
    return json.loads((CARPETA / "creditos.json").read_text(encoding="utf-8"))


def test_veinticuatro_platillos(creditos):
    assert len(creditos) == len(PLATILLOS) == 24
    assert {c["clave"] for c in creditos} == set(PLATILLOS)


def test_archivos_intactos(creditos):
    for c in creditos:
        datos = (RAIZ / "frontend" / c["archivo"]).read_bytes()
        assert hashlib.sha256(datos).hexdigest() == c["sha256"], c["clave"]
        assert len(datos) < 300 * 1024, f"{c['clave']}: la foto pesa más de 300 KB"


def test_licencia_libre_y_credito_completo(creditos):
    for c in creditos:
        assert c["licencia"].startswith(("CC BY", "CC0", "Public domain")), c["clave"]
        assert c["autor"] and c["url_original"].startswith("https://commons.wikimedia.org/"), c["clave"]
        if c["licencia"].startswith("CC BY"):
            assert c["url_licencia"].startswith("http"), f"{c['clave']}: CC BY exige enlace a la licencia"


def test_ningun_lugar_excluido(creditos):
    excluidos = re.compile(r"tulum|canc[uú]n|playa del carmen|cozumel|holbox|isla mujeres|bacalar|mahahual|riviera maya",
                           re.I)
    for c in creditos:
        assert not excluidos.search(" ".join([c["nombre"], c["descripcion"], c["url_original"]])), c["clave"]


def test_grupos_validos(creditos):
    assert {c["grupo"] for c in creditos} == {"mar", "yucateca", "antojitos", "bebidas"}
