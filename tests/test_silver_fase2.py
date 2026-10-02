# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos (pruebas)
# Qué hace:          Pruebas del cierre de la Fase 2: las cuatro tablas Silver que faltaban (nacionalidad, AFAC, cruceros
#                    y Rest-Mex), el almacén DuckDB con el modelo estrella y el diccionario de datos.
# Por qué así:       Cada regla de limpieza de docs/decisiones/18-cierre-fase-2.md se comprueba con una cifra real
#                    (contrato + realidad), como en las demás fases.
# Datos de entrada:  datos/silver/{nacionalidad,afac,cruceros,restmex}, datos/gold/torre.duckdb.
# Alimenta a:        La confianza en la Fase 8 (persona, texto) y en la Fase 6 (mercados).

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402
from torre.base.silver_restmex import nombre_legible  # noqa: E402

SILVER = RAIZ / "datos" / "silver"
ALMACEN = RAIZ / "datos" / "gold" / "torre.duckdb"
pytestmark = pytest.mark.skipif(not (SILVER / "restmex").exists() or not ALMACEN.exists(),
                                reason="Aún no se construye el cierre de la Fase 2")


@pytest.fixture(scope="module")
def nac() -> pd.DataFrame:
    return pd.read_parquet(SILVER / "nacionalidad")


# ---------- Nacionalidad ----------
def test_nacionalidad_completa_y_sin_mexicanos(nac):
    assert len(nac) == 521_363
    assert not nac.pais.str.contains("México", na=False).any()  # solo extranjeros


def test_extranjeros_por_avion_cifras_conocidas(nac):
    q = nac[nac.anio.astype(int) == 2025].groupby("lugar_campana").llegadas_extranjeros.sum()
    assert q["Cancún"] == 9_408_423
    assert q["Chetumal"] == 250  # el sur casi no recibe extranjeros por avión
    assert nac[nac.lugar_campana == "Tulum"].periodo.min() == pd.Timestamp("2024-02-01").date()


# ---------- AFAC ----------
def test_afac_duplicados_resueltos():
    a = pd.read_parquet(SILVER / "afac")
    llave = ["anio", "mes", "tipo_vuelo", "servicio", "region_aerolinea", "aerolinea"]
    assert len(a) == 19_277 and not a.duplicated(llave).any()
    assert a.sumada_flag.sum() == 25
    assert set(a[a.sumada_flag].aerolinea) == {"Virgin América (Alaska Airlines)"}
    assert a.groupby(a.anio.astype(int)).pasajeros.sum()[2025] == 122_722_745


# ---------- Cruceros ----------
def test_cruceros_y_puertos_sin_cruceros():
    c = pd.read_parquet(SILVER / "cruceros")
    assert len(c) == 3_895
    sin = set(c[c.es_qroo & c.puerto_sin_cruceros_flag].puerto)
    assert sin == {"Cancún", "Playa del Carmen", "Puerto Morelos", "Punta Venado"}
    anual = c[c.anio.astype(int) == 2025].groupby("puerto").pasajeros.sum()
    assert anual["Cozumel"] == 4_724_255 and anual["Mahahual"] == 2_379_422


def test_reconciliacion_cruceros_a_mano():
    r = pd.read_parquet(RAIZ / "datos" / "gold" / "reconciliacion_cruceros.parquet")
    r["anio"] = pd.to_datetime(r.periodo).dt.year
    coz = r[(r.puerto == "Cozumel") & (r.anio == 2025)][["pasajeros_datatur", "cruceristas_siturq"]].sum()
    # (4,915,242 ÷ 4,724,255 − 1) × 100 = 4.04 %
    assert round((coz.cruceristas_siturq / coz.pasajeros_datatur - 1) * 100, 2) == 4.04
    mah = r[r.puerto == "Mahahual"]
    assert (mah.groupby("anio")[["cruceristas_siturq", "pasajeros_datatur"]].sum().pipe(
        lambda x: x.cruceristas_siturq > x.pasajeros_datatur)).all()  # SITUR-Q siempre cuenta más en Mahahual


# ---------- Rest-Mex ----------
def test_restmex_sin_duplicados_y_sin_los_5_lugares():
    r = pd.read_parquet(SILVER / "restmex", columns=["pueblo", "tipo", "calificacion", "es_qroo", "estado"])
    assert len(r) == 207_873  # 208,051 − 178 idénticas
    q = r[r.es_qroo]
    assert set(q.pueblo) == {"Tulum", "Isla Mujeres", "Bacalar"}  # ninguno de los 5 lugares
    assert set(r.tipo) == {"hotel", "restaurante", "atractivo"} and r.calificacion.between(1, 5).all()


def test_nombre_legible():
    assert nombre_legible("QuintanaRoo") == "Quintana Roo"
    assert nombre_legible("Baja_CaliforniaSur") == "Baja California Sur"
    assert nombre_legible("Isla_Mujeres") == "Isla Mujeres"


# ---------- Almacén y diccionario ----------
def test_estrella_sin_huerfanos():
    from torre.base.almacen import consultar
    assert consultar("SELECT count(*) n FROM hechos_mes WHERE lugar NOT IN (SELECT lugar FROM dim_lugar)").n[0] == 0
    assert consultar("SELECT count(*) n FROM hechos_mes WHERE periodo NOT IN (SELECT periodo FROM dim_tiempo)").n[0] == 0
    assert consultar("SELECT count(*) n FROM hechos_mes WHERE valor IS NULL").n[0] == 0  # hueco = sin renglón
    cinco = consultar("SELECT lugar FROM dim_lugar WHERE papel = 'promovido'").lugar
    assert len(cinco) == 5


def test_almacen_coincide_con_silver():
    from torre.base.almacen import consultar
    v = consultar("""SELECT sum(valor) v FROM hechos_mes JOIN dim_tiempo USING (periodo)
                     WHERE lugar = 'Chetumal' AND variable = 'llegadas_extranjeros_avion' AND anio = 2025""").v[0]
    assert v == 250


def test_diccionario_cubre_silver():
    import duckdb

    from torre.base.diccionario import faltantes_silver
    with duckdb.connect(str(ALMACEN), read_only=True) as con:
        assert faltantes_silver(con) == []
    texto = (RAIZ / "docs" / "datos" / "DICCIONARIO.md").read_text(encoding="utf-8")
    assert "## silver_restmex" in texto and "## hechos_mes" in texto
