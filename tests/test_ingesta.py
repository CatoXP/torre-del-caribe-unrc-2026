# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos (pruebas)
# Qué hace:          Pruebas de la Fase 1 sobre lo ya descargado en datos/bronze/:
#                    - contrato: los archivos existen, tienen la forma esperada y su huella coincide con el manifiesto;
#                    - realidad: reproducen cifras oficiales que se verificaron a mano el 27-sep-2026.
# Por qué así:       Si alguien cambia un archivo crudo o la fuente cambia su formato, estas pruebas lo detectan.
#                    Las cifras de "realidad" salen de consultas hechas antes de programar la ingesta
#                    (ver docs/decisiones/01-regiones.md y el plan, tabla D1-detalle).
# Datos de entrada:  datos/bronze/MANIFIESTO.csv y los archivos que lista.
# Alimenta a:        La confianza en todas las cifras de la campaña.

import csv
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.manifiesto import MANIFIESTO, RAIZ, sha256_de  # noqa: E402

pytestmark = pytest.mark.skipif(not MANIFIESTO.exists(), reason="Aún no se corre la ingesta (Fase 1)")


def filas_manifiesto(fuente_empieza: str = "") -> list[dict]:
    with open(MANIFIESTO, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["fuente"].startswith(fuente_empieza)]


def ultimo_json_siturq(nombre: str) -> list[dict]:
    """Lee el archivo más reciente de un indicador de SITUR-Q."""
    rutas = sorted((RAIZ / "datos" / "bronze" / "siturq").glob(f"*/{nombre}.json"))
    if not rutas:
        pytest.skip(f"No hay descarga de SITUR-Q para {nombre}")
    return json.loads(rutas[-1].read_text(encoding="utf-8"))


def valor(bloque: list[dict], unidad: str, anio: int, mes: int, campo: str):
    """Busca un valor dentro de las respuestas crudas de la API (unidad, año, mes, campo)."""
    for reg in bloque:
        if reg["unidad"] == unidad and reg["anio"] == anio:
            for fila in reg["respuesta"].get("data") or []:
                if int(fila.get("Mes", 0)) == mes:
                    return fila.get(campo)
    return None


# --- Contrato -------------------------------------------------------------------------------------------------
def test_manifiesto_huellas_coinciden():
    """Cada archivo del manifiesto existe y su SHA-256 es el registrado (nadie lo modificó)."""
    for r in filas_manifiesto():
        ruta = RAIZ / r["archivo"]
        assert ruta.exists(), f"Falta {r['archivo']}"
        assert sha256_de(ruta) == r["sha256"], f"Huella distinta: {r['archivo']}"


def test_siturq_tiene_15_unidades_por_indicador():
    bloque = ultimo_json_siturq("ocupacion_hotelera")
    assert len({reg["unidad"] for reg in bloque}) == 15


# --- Realidad (cifras verificadas a mano el 27-sep-2026) --------------------------------------------------------
def test_siturq_bacalar_ocupacion_ene_2024():
    bloque = ultimo_json_siturq("ocupacion_hotelera")
    assert float(valor(bloque, "Bacalar", 2024, 1, "Ocupación hotelera")) == pytest.approx(66.5)


def test_siturq_tren_maya_gran_costa_maya_ene_2025():
    bloque = ultimo_json_siturq("tren_maya_movimiento")
    assert int(valor(bloque, "Grand Costa Maya", 2025, 1, "Total")) == 14437


def test_siturq_bacalar_145_hoteles_ene_2025():
    bloque = ultimo_json_siturq("centros_hospedaje")
    assert int(valor(bloque, "Bacalar", 2025, 1, "Total de hoteles")) == 145


def test_restmex_208051_resenas():
    """HuggingFace reportó 208,051 filas para vg055/Rest-Mex2025 (consulta del 27-sep-2026)."""
    filas = [r for r in filas_manifiesto("D5") if r["archivo"].endswith(".csv")]
    assert filas and int(filas[-1]["filas"]) == 208051


def test_inah_tulum_2025():
    """Visitantes 2025 a la Z.A. de Tulum = 1,031,443 (cálculo del 27-sep-2026, docs/metodologia/ECUACIONES.md §1)."""
    import io
    import zipfile

    import pandas as pd

    rutas = sorted((RAIZ / "datos" / "bronze" / "datatur").glob("*/inah/BdINAH.zip"))
    if not rutas:
        pytest.skip("No hay BdINAH descargado")
    with zipfile.ZipFile(rutas[-1]) as z:
        df = pd.read_excel(io.BytesIO(z.read(next(n for n in z.namelist() if n.endswith(".xlsx")))))
    tulum = df[(df["Nombre"] == "Z.A. de Tulum") & (df["Año"] == 2025)]["Visitantes"].sum()
    assert tulum == 1031443


def test_geojson_11_municipios():
    filas = filas_manifiesto("D12")
    assert filas and int(filas[-1]["filas"]) == 11


def test_benchmarks_travel_google_2025():
    """Tabla oficial de WordStream 2025, Travel: CPC $2.12 y CTR 8.73 % (extraída con Playwright el 28-sep-2026)."""
    import pandas as pd

    rutas = sorted((RAIZ / "datos" / "bronze" / "benchmarks").glob("*/benchmarks_tablas.csv"))
    if not rutas:
        pytest.skip("No hay benchmarks descargados")
    d = pd.read_csv(rutas[-1])
    t = d[(d.clave_pagina == "wordstream_google_2025") & (d.categoria == "Travel")].set_index("metrica")["valor"]
    assert t["Average CPC"] == pytest.approx(2.12)
    assert t["Average CTR"] == pytest.approx(8.73)


def test_denue_32_estados():
    """Los 32 estados están presentes (el Estado de México viene en dos partes)."""
    notas = {r["nota"].split()[-1].split("_")[0] for r in filas_manifiesto("D6")}
    assert len(notas) == 32
