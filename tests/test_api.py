# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos (pruebas de la API, Fase 9)
# Qué hace:          Prueba cada endpoint del servidor con el cliente de pruebas de FastAPI (sin abrir un puerto): forma de
#                    la respuesta, cifras conocidas, que /api/optimizar resuelva en menos de 2 s y que la consulta SQL sea
#                    de solo lectura.
# Por qué así:       El plan (Fase 9) pide "pruebas de API; el optimizador responde en menos de 2 s".
# Datos de entrada:  datos/gold/* a través de torre.api.servidor.
# Alimenta a:        La confianza en la página conectada a los modelos.

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402

GOLD = RAIZ / "datos" / "gold"
pytestmark = pytest.mark.skipif(not (GOLD / "campana.json").exists(), reason="Faltan salidas de las Fases 4–8")


@pytest.fixture(scope="module")
def cliente():
    from fastapi.testclient import TestClient

    from torre.api.servidor import app
    return TestClient(app)


def test_salud_y_pagina(cliente):
    assert cliente.get("/api/salud").json()["ok"]
    r = cliente.get("/")
    assert r.status_code == 200 and "Torre del Caribe" in r.text


def test_radar_pronostico_escenarios(cliente):
    assert "lugares" in cliente.get("/api/radar").json()
    p = cliente.get("/api/pronostico", params={"lugar": "Chetumal"}).json()
    assert p and all(x["lugar"] == "Chetumal" for x in p)
    e = cliente.get("/api/escenarios", params={"lugar": "Ruta arqueológica del sur", "golpe": 0.25}).json()
    assert e and all(x["golpe_tormenta_supuesto"] == 0.25 for x in e)
    assert cliente.get("/api/escenarios", params={"golpe": 0.9}).status_code == 422  # fuera de rango


def test_optimizar_en_vivo_menos_de_2_segundos(cliente):
    r = cliente.post("/api/optimizar", json={}).json()
    assert r["estado"] == "Optimal" and r["visitantes"] == pytest.approx(956.8, abs=0.1) and r["ms"] < 2000
    r2 = cliente.post("/api/optimizar", json={"presupuesto_anual": 500_000}).json()
    assert r2["visitantes"] == pytest.approx(2 * r["visitantes"], rel=1e-3)  # lineal: el doble de dinero, el doble
    assert cliente.post("/api/optimizar", json={"tope_canal": 0.2}).status_code == 422


def test_stream_sse(cliente):
    with cliente.stream("GET", "/api/stream", params={"ms": 20}) as r:
        assert r.headers["content-type"].startswith("text/event-stream")
        primeras = []
        for linea in r.iter_lines():
            if linea.startswith("data:"):
                primeras.append(linea)
            if len(primeras) == 2:
                break
    assert '"semana": "2022-01-03"' in primeras[0]


def test_campana(cliente):
    assert cliente.get("/api/campana").json()["marca"]["nombre"] == "El sur tiene espacio"


def test_consulta_solo_lectura(cliente):
    from torre.api.servidor import sql_permitido
    r = cliente.get("/api/consulta", params={"sql": "SELECT lugar, papel FROM dim_lugar ORDER BY lugar"}).json()
    assert len(r["filas"]) == 15 and not r["recortado"]
    for malo in ["DROP TABLE dim_lugar", "SELECT * FROM read_csv('C:/x.csv')", "SELECT 1; DROP TABLE x",
                 "COPY dim_lugar TO 'x.csv'", "ATTACH 'otra.db'", "SELECT * FROM glob('*')"]:
        assert not sql_permitido(malo)
        assert cliente.get("/api/consulta", params={"sql": malo}).status_code == 400
