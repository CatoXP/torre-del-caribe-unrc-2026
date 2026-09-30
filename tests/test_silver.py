# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos (pruebas)
# Qué hace:          Pruebas de la Fase 2 sobre datos/silver/: que la tabla tenga la forma esperada y que las reglas de
#                    limpieza reproduzcan cifras conocidas.
# Por qué así:       Cada regla de limpieza (sumar estaciones, ceros imposibles como hueco) se comprueba con un caso real.
# Datos de entrada:  datos/silver/siturq/ (Parquet).
# Alimenta a:        La confianza en Gold y en los modelos.

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402

SILVER_SITURQ = RAIZ / "datos" / "silver" / "siturq"
pytestmark = pytest.mark.skipif(not SILVER_SITURQ.exists(), reason="Aún no se construye Silver (Fase 2)")


@pytest.fixture(scope="module")
def siturq() -> pd.DataFrame:
    return pd.read_parquet(SILVER_SITURQ)  # pyarrow lee el Parquet que escribió Spark


def v(df, indicador, unidad, anio, mes, variable):
    fila = df[(df.indicador == indicador) & (df.unidad == unidad) & (df.anio == anio) & (df.mes == mes) & (df.variable == variable)]
    assert len(fila) == 1, f"Se esperaba 1 fila y hay {len(fila)}"
    return fila.iloc[0]


def test_columnas(siturq):
    assert {"indicador", "unidad", "anio", "mes", "periodo", "variable", "valor", "hueco_flag", "n_registros_fuente"} <= set(siturq.columns)


def test_bacalar_ocupacion_ene_2024(siturq):
    assert v(siturq, "ocupacion_hotelera", "Bacalar", 2024, 1, "ocupacion_hotelera").valor == pytest.approx(66.5)


def test_tren_maya_suma_estaciones_chetumal(siturq):
    """Chetumal trae 2 estaciones: 24 + 3,478 = 3,502 descensos en ene-2025."""
    fila = v(siturq, "tren_maya_descenso", "Chetumal", 2025, 1, "total")
    assert fila.valor == 3502 and fila.n_registros_fuente == 2


def test_tren_maya_zona_igual_suma_destinos(siturq):
    """El total de zona Grand Costa Maya (7,084) es igual a la suma de sus destinos ya agregados."""
    zona = v(siturq, "tren_maya_descenso", "Grand Costa Maya", 2025, 1, "total").valor
    miembros = sum(v(siturq, "tren_maya_descenso", u, 2025, 1, "total").valor for u in ("Chetumal", "Bacalar"))
    assert zona == miembros == 7084


def test_ocupacion_2025_es_hueco_no_cero(siturq):
    """En 2025 SITUR-Q reporta 0 habitaciones disponibles (imposible): debe ser hueco, no 0 %."""
    fila = v(siturq, "ocupacion_hotelera", "Cancún", 2025, 1, "ocupacion_hotelera")
    assert bool(fila.hueco_flag) and pd.isna(fila.valor)


def test_cero_real_se_conserva(siturq):
    """Los ceros reales se conservan: cruceristas, Tren Maya y zonas arqueológicas nunca se marcan como hueco."""
    reales = siturq[~siturq.indicador.isin(["ocupacion_hotelera", "afluencia_turistas", "derrama_turistas", "derrama_visitantes",
                                            "aereos_llegadas"])]
    assert not reales.hueco_flag.any()


def test_regla_6_aereos(siturq):
    """Regla 6: un mes de llegadas aéreas es hueco solo si TODOS los aeropuertos reportan 0; si uno trae dato, nada es hueco."""
    a = siturq[siturq.indicador == "aereos_llegadas"]
    assert a[a.hueco_flag].valor.isna().all()  # el hueco no guarda el 0 falso
    por_mes = a.groupby("periodo").agg(huecos=("hueco_flag", "sum"), filas=("hueco_flag", "size"), maximo=("valor", "max"))
    assert ((por_mes.huecos == 0) | (por_mes.huecos == por_mes.filas)).all()  # todo el mes es hueco o nada lo es
    assert (por_mes[por_mes.huecos == 0].maximo > 0).all()  # un mes con dato tiene al menos un aeropuerto con llegadas
    assert len(a) == 450 and a.hueco_flag.sum() == 114


def test_afluencia_y_derrama_terminan_en_marzo_2024(siturq):
    """Afluencia y derrama con dato real llegan a marzo de 2024; los meses posteriores en 0 son huecos, no ceros."""
    f = siturq[siturq.indicador.isin(["afluencia_turistas", "derrama_turistas", "derrama_visitantes"]) & ~siturq.hueco_flag]
    assert str(f.periodo.max())[:7] == "2024-03"


# --- DataTur ocupación hotelera (semanal y mensual) --------------------------------------------------------------
SILVER_DATATUR = RAIZ / "datos" / "silver" / "datatur_ocupacion"


@pytest.fixture(scope="module")
def datatur() -> pd.DataFrame:
    if not SILVER_DATATUR.exists():
        pytest.skip("Aún no se construye la ocupación de DataTur en Silver")
    return pd.read_parquet(SILVER_DATATUR)


def test_cancun_semana_31_2026(datatur):
    """Cifras del archivo 2026_Semana_31 (vistas el 28-sep-2026): 37,337 cuartos disponibles y 67.53 % de ocupación."""
    f = datatur[(datatur.frecuencia == "semanal") & (datatur.centro == "Cancun") & (datatur.anio == 2026) & (datatur.semana == 31)]
    assert len(f) == 1
    assert f.iloc[0].cuartos_disponibles == 37337 and f.iloc[0].ocupacion_pct == pytest.approx(67.53)
    assert str(f.iloc[0].periodo)[:10] == "2026-07-27"  # lunes de la semana 31, igual que dice el título del archivo


def test_sin_duplicados(datatur):
    llave = ["frecuencia", "centro", "estado", "tipo_fila", "anio", "semana", "mes"]
    assert not datatur.duplicated(llave).any()


def test_qroo_239_semanas(datatur):
    """Del 3-ene-2022 al 27-jul-2026 hay 239 semanas; cada centro de Q. Roo debe tenerlas todas, sin repetir."""
    s = datatur[(datatur.frecuencia == "semanal") & datatur.es_qroo & (datatur.tipo_fila == "centro")]
    assert set(s.groupby("centro").size()) == {239} and s.centro.nunique() == 7


def test_ocupacion_publicada_coincide_con_calculada(datatur):
    """La ocupación que publica DataTur debe ser ocupados ÷ disponibles; se tolera 0.5 puntos por redondeo."""
    d = datatur.dropna(subset=["ocupacion_pct", "ocupacion_calc_pct"])
    assert ((d.ocupacion_pct - d.ocupacion_calc_pct).abs() <= 0.5).mean() > 0.99


def test_nota_isla_mujeres(datatur):
    """DataTur advierte que desde septiembre 2025 cambió la oferta hotelera de Isla Mujeres: debe quedar registrado."""
    notas = datatur[(datatur.centro == "Isla Mujeres") & datatur.nota_al_pie.notna()].nota_al_pie
    assert notas.str.contains("oferta hotelera", case=False).any()


# --- DENUE (INEGI) ---------------------------------------------------------------------------------------------
SILVER_DENUE = RAIZ / "datos" / "silver" / "denue"


@pytest.fixture(scope="module")
def denue() -> pd.DataFrame:
    if not SILVER_DENUE.exists():
        pytest.skip("Aún no se construye DENUE en Silver")
    return pd.read_parquet(SILVER_DENUE, columns=["id", "cve_ent", "es_turistico", "categoria_turistica", "municipio", "coordenadas_flag"])


def test_denue_total_nacional(denue):
    """6,138,075 negocios: lo cuentan igual Spark y un lector CSV independiente (28-sep-2026), sin duplicados."""
    assert len(denue) == 6_138_075 and denue.id.is_unique


def test_denue_turisticos_qroo(denue):
    """13,663 negocios turísticos en Quintana Roo con los giros SCIAN elegidos (721, 722, 5615, 487, 712, 713)."""
    assert int(((denue.cve_ent.astype(str) == "23") & denue.es_turistico).sum()) == 13_663


def test_denue_sin_datos_personales():
    """Privacidad: Silver no guarda razón social, teléfono ni correo."""
    import pyarrow.parquet as pq

    columnas = set(pq.read_schema(next(SILVER_DENUE.rglob("*.parquet"))).names)
    assert not columnas & {"raz_social", "telefono", "correoelec"}


def test_denue_coordenadas_validas(denue):
    assert not denue.coordenadas_flag.any()


# ---------- INAH (Fase 3: tabla de criterios de las 5 regiones) ----------
SILVER_INAH = RAIZ / "datos" / "silver" / "inah"


@pytest.fixture(scope="module")
def inah() -> pd.DataFrame:
    if not SILVER_INAH.exists():
        pytest.skip("Aún no se construye INAH en Silver")
    return pd.read_parquet(SILVER_INAH)


def test_inah_sin_llaves_repetidas(inah):
    """El bloque duplicado 'Extranjero, sep-2025' (283 filas en cero) ya no está: 71,561 − 283 = 71,278 filas únicas."""
    assert len(inah) == 71_278
    assert not inah.duplicated(["estado", "nombre", "anio", "mes", "tipo_visitante"]).any()


def test_inah_cifras_de_la_seleccion_de_regiones(inah):
    """Reproduce las cifras de docs/regiones/REGIONES.md D.4 (visitantes 2025)."""
    q = inah[(inah.es_qroo) & (inah.anio.astype(int) == 2025)]
    por_region = q.groupby("region_campana").visitantes.sum()
    assert por_region["Tulum"] == 1_031_443
    assert por_region["Ruta arqueológica del sur"] == 66_628
    assert por_region["Bahía Calderitas–Oxtankah"] == 11_017


def test_inah_kohunlich_crece_en_2026(inah):
    """Kohunlich ene–jul 2026 contra ene–jul 2025: +13.5 %."""
    k = inah[(inah.nombre == "Z.A. de Kohunlich") & (inah.mes <= 7)].groupby(inah.anio.astype(int)).visitantes.sum()
    assert round((k[2026] / k[2025] - 1) * 100, 1) == 13.5


def test_inah_papel_de_las_zonas(inah):
    """Solo las zonas de las 5 regiones van como 'promovida'; Cobá y Muyil quedaron como 'retirada'."""
    papel = inah[inah.es_qroo].drop_duplicates("nombre").set_index("nombre").papel_campana
    assert set(papel[papel == "promovida"].index) == {"Z.A. de Oxtankah", "Z.A. de Kohunlich",
                                                      "Z.A. de Dzibanché-Kinichná", "Z.A de Ichkabal"}
    assert papel["Z.A. de Cobá"] == "retirada" and papel["Z.A. de Muyil"] == "retirada"


# ---------- Censo 2020 ITER (Fase 3: población por localidad de cada región) ----------
SILVER_ITER = RAIZ / "datos" / "silver" / "iter"


@pytest.fixture(scope="module")
def censo() -> pd.DataFrame:
    if not SILVER_ITER.exists():
        pytest.skip("Aún no se construye ITER en Silver")
    return pd.read_parquet(SILVER_ITER)


def test_iter_filas_y_total_estatal(censo):
    """2,243 filas (todas las del CSV de conjunto_de_datos, sin descartar ninguna); población estatal 1,857,985."""
    assert len(censo) == 2_243
    assert int(censo.loc[censo.tipo_fila == "total_estatal", "poblacion"].iloc[0]) == 1_857_985


def test_iter_poblacion_de_las_5_regiones(censo):
    """Decisión de Brandon (28-sep-2026): población por localidad (docs/decisiones/05-planteamiento.md)."""
    p = censo[censo.papel_campana == "promovida"].groupby("region_campana").poblacion.sum()
    assert p.to_dict() == {"Bahía Calderitas–Oxtankah": 5_551, "Chetumal": 169_028, "Laguna Milagros–Xul-Ha": 4_182,
                           "Maya Ka'an + Kantemó": 44_388, "Ruta arqueológica del sur": 6_098}


def test_iter_reservados_son_nulos_no_ceros(censo):
    """Lo que INEGI reserva con '*' queda como nulo con reservado_flag, nunca como 0 (regla de oro 1)."""
    reservadas = censo[censo.reservado_flag]
    assert len(reservadas) > 0 and reservadas[["viviendas_con_agua", "viviendas_con_drenaje"]].isna().any(axis=1).all()
