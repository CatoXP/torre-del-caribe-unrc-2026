# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña (pruebas)
# Qué hace:          Pruebas de los 10 idiomas de la página: cada diccionario cubre todas las frases, ninguna traducción
#                    pierde ni inventa una cifra, un mes, un lugar o una etiqueta, y el maya yucateco no se publica sin
#                    revisión.
# Por qué así:       Una cifra no puede cambiar al traducir (regla de oro 1). Decisión 16.
# Datos de entrada:  docs/idiomas, frontend/idiomas, frontend/idiomas.js.
# Alimenta a:        La confianza en la página para visitantes extranjeros.

import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402
from torre.campana import idiomas  # noqa: E402

CLAVES = json.loads((RAIZ / "docs" / "idiomas" / "claves.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("lang", idiomas.IDIOMAS)
def test_diccionario_completo_y_con_sus_marcas(lang):
    d, faltan = idiomas.armar(lang, CLAVES)  # armar() se detiene si una marca no coincide
    assert not faltan and len(d["frases"]) == len(CLAVES) >= 454


@pytest.mark.parametrize("lang", idiomas.IDIOMAS)
def test_archivo_publicado_al_dia(lang):
    js = (RAIZ / "frontend" / "idiomas" / f"{lang}.js").read_text(encoding="utf-8")
    datos = json.loads(js[js.index("= {") + 2:js.rindex(";")])
    assert datos == idiomas.armar(lang, CLAVES)[0]


def test_ejemplo_de_marcas():
    # "Llega {n0} % menos gente…" en alemán conserva {n0}; si alguien borra la cifra, armar() falla.
    assert idiomas.marcas("Llega {n0} % <b>{p0}</b>") == idiomas.marcas("{n0} % <b>{p0}</b> weniger")
    assert idiomas.marcas("{n0} y {n1}") != idiomas.marcas("{n0}")


def test_maya_en_revision():
    js = (RAIZ / "frontend" / "idiomas.js").read_text(encoding="utf-8")
    assert re.search(r'c: "yua", n: "Maaya t\'aan", enRevision: true', js)
    assert not (RAIZ / "frontend" / "idiomas" / "yua.js").exists()  # no se publica hasta que lo revise un hablante
