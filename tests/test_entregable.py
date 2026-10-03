# Autor: Brandon Uriel García Sánchez
# Módulo: Documento (pruebas de la carpeta de entrega)
# Qué hace:          Arma (sin ejecutar) los cuatro notebooks de Entregable/ y revisa que estén completos: cada módulo que
#                    usan va antes de su primer uso, todo el código compila, y el texto no manda a rutas del repositorio
#                    que no van en la entrega.
# Por qué así:       Los notebooks de la entrega toman el código de backend/torre al armarse. Si un módulo cambia de
#                    nombre o se agrega una dependencia, esta prueba lo avisa sin tener que correr Spark (la ejecución
#                    completa la hace torre.documento.entregable).
# Datos de entrada:  backend/torre/**, notebooks/0*.ipynb.
# Alimenta a:        La entrega a los profesores (Entregable/2_Notebooks).

import ast
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.documento import entregable as e  # noqa: E402


@pytest.fixture(scope="module")
def notebooks():
    return {nombre: construir() for nombre, construir in e.NOTEBOOKS}


def test_son_cuatro_y_traen_el_codigo(notebooks):
    assert list(notebooks) == ["1_Datos_y_arquitectura", "2_Donde_y_cuando", "3_Presupuesto_y_Torre_en_vivo", "4_Campana"]
    for celdas in notebooks.values():
        assert any(c.source.startswith("%%modulo ") for c in celdas)


def test_cada_modulo_va_antes_de_usarse_y_compila(notebooks):
    for nombre, celdas in notebooks.items():
        registrados = set()
        for c in celdas:
            if c.cell_type != "code":
                continue
            if c.source.startswith("%%modulo "):
                primera, cuerpo = c.source.split("\n", 1)
                ast.parse(cuerpo)  # el código del módulo compila
                for dep in e.dependencias(primera.split()[1]):
                    assert dep in registrados, f"{nombre}: {primera.split()[1]} usa {dep} antes de registrarlo"
                registrados.add(primera.split()[1])
                continue
            # Celdas de uso: lo que importan de torre ya debe estar registrado.
            for paquete, nombres in re.findall(r"from (torre(?:\.\w+)+) import ([\w, ]+)", c.source):
                mods = ([f"{paquete}.{n.strip().split(' as ')[0]}" for n in nombres.split(",")]
                        if paquete.count(".") == 1 else [paquete])
                for m in mods:
                    assert m in registrados, f"{nombre}: se usa {m} antes de registrarlo"


def test_sin_rutas_del_repositorio(notebooks):
    for nombre, celdas in notebooks.items():
        for c in celdas:
            if c.cell_type == "markdown":
                assert not re.search(r"backend/|docs/(decisiones|metodologia|ejecutivo)", c.source), (nombre, c.source[:120])
            elif not c.source.startswith("%%modulo "):
                assert 'RAIZ / "backend"' not in c.source and '"docs"' not in c.source, (nombre, c.source[:120])
