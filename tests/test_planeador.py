# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña y Pronóstico (pruebas)
# Qué hace:          Pruebas del planeador de viaje: el clasificador de texto (NLP por léxico) de los negocios del DENUE,
#                    las recomendaciones por momento del día y el calendario de temporada alta / recomendación.
# Por qué así:       Cada regla se prueba con un caso real que salió mal en la revisión y se corrigió (docs/decisiones/
#                    12-planeador.md): micheladas que parecían helados, un estacionamiento de hotel, una disco con "café".
# Datos de entrada:  datos/silver/denue, datos/gold/pronostico_*, datos/gold/lugares_recomendados.
# Alimenta a:        La confianza en lo que la página le recomienda a un viajero.

import sys
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402
from torre.campana import lugares  # noqa: E402
from torre.pronostico import calendario  # noqa: E402

GOLD = RAIZ / "datos" / "gold"
pytestmark = pytest.mark.skipif(not (GOLD / "pronostico_mes.parquet").exists(), reason="Falta la Fase 5")


# ---------- NLP por léxico ----------
@pytest.mark.parametrize("nombre, giro, tipo", [
    ("MICHELADAS LA CRUDALIA", "722412", "Bar o cantina"),        # "MICHELADAS" contiene "HELAD": no es helado
    ("BARBACOA EL TARAHUMARA", "722519", "Tacos y tortas"),       # "BARBACOA" contiene "BAR": no es bar
    ("DISCO ROCK SHOTS CAFE", "722411", "Centro nocturno"),       # "CAFE" no vuelve bebida a una disco
    ("AGUAS FRESCAS Y RASPADOS", "722412", "Café, desayunos y postres"),
    ("MARISCOS Y ANTOJITOS EL GUERO", "722513", "Mariscos y pescado"),  # el orden del léxico importa
    ("ROSTIZERIA EL PECHUGON", "722517", "Asados y pollos"),      # el nombre gana al giro
    ("HOTEL COSTA AZUL", "721311", "Hotel"),                      # el nombre gana al giro en hospedaje
    ("RESTAURANT QUINTANA ROLL COCINA JAPONESA", "722511", "Cocina internacional"),
    ("QUESADILLAS AL ESTILO PUEBLA", "722513", "Antojitos"),       # no es "yucateca"
    ("EL PATIO DE MI CASA DESAYUNOS", "722511", "Café, desayunos y postres"),
    ("PIBIL MAYA", "722511", "Cocina yucateca"),
    ("SALADE SALAD & JUICE BAR", "722511", "Café, desayunos y postres"),  # bar de jugos, no de noche (norte)
])
def test_clasificador(nombre, giro, tipo):
    assert lugares.clasificar(nombre, giro)["tipo"] == tipo


@pytest.mark.parametrize("nombre, giro", [
    ("ANTOJITOS SIN NOMBRE", "722513"), ("MANHATTAN MENS CLUB", "722411"),
    ("ESTACIONAMIENTO DEL HOTEL EL DORADO", "721112"), ("COOPERATIVA ESCOLAR", "722519"),
    ("PUESTO DE CANICAS FRONTON MAGICO", "713998"), ("GIMNASIO FUERZA", "713943"), ("MOTEL LAS PALMAS", "721113"),
    ("VENTA DE VOLETOS DEL FERRI", "487210"),  # taquilla del ferri a Cozumel (regla de oro 9)
])
def test_excluidos(nombre, giro):
    assert lugares.clasificar(nombre, giro) is None


def test_raiz_al_inicio_de_palabra():
    assert lugares.tiene("BAR MAR CARIBE", ["BAR"]) and not lugares.tiene("BARBACOA", ["BAR"])
    assert not lugares.tiene("MICHELADAS", ["HELAD"]) and lugares.tiene("HELADOS", ["HELAD"])


def test_enlace_de_google_maps():
    assert lugares.enlace_maps(18.5, -88.3) == "https://www.google.com/maps/search/?api=1&query=18.5%2C-88.3"
    assert "Kohunlich" in lugares.enlace_maps(texto="Zona Arqueológica de Kohunlich")


# ---------- Recomendaciones ----------
@pytest.fixture(scope="module")
def rec():
    return pd.read_parquet(GOLD / "lugares_recomendados.parquet")


def test_solo_los_5_lugares_y_el_norte_aparte(rec):
    assert set(rec.lugar) == set(lugares.LUGARES) | set(lugares.NORTE) and len(lugares.LUGARES) == 5
    sur = rec[rec.lugar.isin(lugares.LUGARES)]
    prohibidos = "Bacalar|Mahahual|Tulum|Canc|Playa del Carmen|Cozumel|Holbox"
    assert not sur.localidad.str.contains(prohibidos).any()  # el sur nunca se completa con el norte
    # Cancún y Riviera Maya (decisión 15): solo sus propios negocios, nunca de otro lugar.
    norte = rec[rec.lugar.isin(list(lugares.NORTE))]
    assert set(norte.localidad) == {"Cancún", "Playa del Carmen"} and not norte.de_otro_lugar_flag.any()
    assert not rec.nombre.str.contains("Ferri|Voletos|Boletos", case=False).any()  # taquillas del ferri a Cozumel


def test_seis_por_momento(rec):
    n = rec.groupby(["lugar", "grupo", "momento"]).size()
    assert (n <= lugares.POR_MOMENTO).all() and n.min() >= 5


def test_la_ruta_duerme_en_otro_lugar(rec):
    # La Ruta no tiene hoteles en sus localidades: todo lo de dormir viene de los otros 4 lugares y se marca.
    d = rec[(rec.lugar == "Ruta arqueológica del sur") & (rec.grupo == "dormir")]
    assert len(d) == 6 and d.de_otro_lugar_flag.all()


# ---------- Calendario y temporada alta ----------
@pytest.fixture(scope="module")
def cal():
    return calendario.calendario(hoy=date(2026, 10, 1))


def fila(cal, lugar, ym):
    return cal[(cal.lugar == lugar) & (cal.periodo == pd.Timestamp(ym))].iloc[0]


def test_meses_elegibles(cal):
    assert cal.periodo.min() == pd.Timestamp("2026-10-01") and cal.periodo.max() == pd.Timestamp("2027-12-01")
    assert cal.periodo.nunique() == 15


def test_regla_de_temporada_alta(cal):
    r = fila(cal, "Ruta arqueológica del sur", "2027-01-01")
    assert r.nivel == "alta" and r.indice == pytest.approx(1.606, abs=1e-3)  # por la forma del año (≥ 1.20)
    c = fila(cal, "Chetumal", "2026-12-01")
    assert c.indice < 1.2 and c.riesgo_capacidad >= 0.10 and c.nivel == "alta"  # por el riesgo de capacidad
    assert fila(cal, "Chetumal", "2027-01-01").nivel == "tranquila"


def test_lugares_del_planeador(cal):
    # Decisión 15: los 3 del sur con serie y Cancún y Riviera Maya como referencia. Maya Ka'an y la Laguna salieron
    # (sin serie, solo decían "sin dato"); nadie queda "sin dato".
    assert set(cal.lugar) == set(calendario.SUR) | set(calendario.NORTE)
    assert set(cal[cal.papel == "referencia"].lugar) == {"Cancún", "Riviera Maya"}
    assert (cal.nivel != "sin dato").all()


def test_norte_con_el_corte_del_radar(cal):
    # Ejemplo a mano: Cancún, enero de 2027, ocupación esperada 78.27 % ≥ p50 del Radar (71.16 %) → temporada alta.
    corte = calendario.corte_radar()
    assert corte == pytest.approx(71.16, abs=0.01)
    c = fila(cal, "Cancún", "2027-01-01")
    assert c.ocupacion_est == pytest.approx(78.27, abs=0.01) and c.nivel == "alta"
    assert fila(cal, "Cancún", "2026-10-01").nivel == "tranquila"  # 65.25 % < 71.16 %
    n = cal[cal.papel == "referencia"]
    ocup = n.ocupacion_est.fillna(n.ocupacion_tipica_pct)  # fuera del pronóstico, lo típico 2022–2025
    assert ((ocup >= corte) == (n.nivel == "alta")).all()


def test_nunca_recomienda_el_norte(cal):
    assert not cal.otro_lugar.isin(list(calendario.NORTE)).any()
    assert fila(cal, "Cancún", "2027-01-01").otro_lugar == "Chetumal"
    # En el norte no hay mes tranquilo, seco y sin tormentas a la vez: solo se sugiere otro lugar.
    assert cal[cal.papel == "referencia"].otro_mes.isna().all()


def test_tormentas_del_norte_con_la_misma_regla():
    t = calendario.tormentas_punto("cancun")
    assert len(t) == 12 and (t >= 0).all() and (t < 1).all()
    assert t[1:5].sum() == 0 and t[10] == t.max()  # sin tormentas de enero a mayo; octubre, el mes más riesgoso


def test_recomendaciones(cal):
    r = fila(cal, "Ruta arqueológica del sur", "2027-01-01")
    assert r.otro_lugar == "Chetumal" and r.otro_mes == 11       # noviembre: tranquilo, seco, sin tormentas
    assert fila(cal, "Bahía Calderitas–Oxtankah", "2027-01-01").otro_mes == 5
    assert fila(cal, "Chetumal", "2026-12-01").otro_mes == 2
    assert fila(cal, "Ruta arqueológica del sur", "2026-12-01").otro_lugar is None  # todo el sur con dato está en alta


def test_mes_sugerido_no_es_el_mas_lluvioso(cal):
    # Sin la condición de lluvia se sugería junio (195 mm en Chetumal). Ningún mes sugerido llueve más que la mediana.
    clima = calendario.clima_normal().set_index(["punto", "mes"]).lluvia_mm
    for _, f in cal[cal.otro_mes.notna()].iterrows():
        punto = calendario.LUGARES[f.lugar][1]
        assert clima[(punto, int(f.otro_mes))] < clima.loc[punto].median()
