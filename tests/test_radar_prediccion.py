# Autor: Brandon Uriel García Sánchez
# Módulo: Radar (pruebas de la predicción del estado, Fase 4 pieza 3)
# Qué hace:          Revisa que el índice comparable no tenga el quiebre de 2025, que la validación sea temporal (nada
#                    del futuro en el entrenamiento), las cifras de la comparación contra la persistencia y el ejemplo
#                    de F1-macro resuelto a mano (ECUACIONES.md §2.2).
# Por qué así:       La predicción decide si un anuncio se pausa antes de que un lugar se llene; un modelo que "ve el
#                    futuro" al entrenar parecería mejor de lo que es.
# Datos de entrada:  datos/silver/ a través de torre.radar.panel, indice y prediccion.
# Alimenta a:        La confianza en el Radar (Fase 4).

import sys
import warnings
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from torre.radar import prediccion as pr  # noqa: E402
from torre.radar.panel import SILVER  # noqa: E402

pytestmark = pytest.mark.skipif(not (SILVER / "siturq").exists(), reason="Aún no existe Silver")


@pytest.fixture(scope="module")
def r():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return pr.correr()


def test_indice_comparable_sin_quiebre(r):
    """Cada lugar usa siempre las mismas medidas: Chetumal, tren por habitante y llegadas por cuarto, desde dic-2024."""
    t = r["t"].dropna(subset=["ipt_comparable"])
    assert t.groupby("lugar").medidas.nunique().max() == 1
    che = t[t.lugar == "Chetumal"]
    assert che.periodo.min() == pd.Timestamp("2024-12-01")
    assert che.medidas.iloc[0] == "llegadas_tren_x1000hab, llegadas_x_cuarto"


def test_validacion_temporal(r):
    ent, pru = r["detalle"]["entrenamiento"], r["detalle"]["prueba"]
    assert ent.periodo_objetivo.max() < pr.INICIO_PRUEBA <= pru.periodo_objetivo.min()


def test_comparacion_contra_persistencia(r):
    m = r["metricas"].set_index("modelo")
    assert (m.loc["Persistencia (línea base)", "aciertos"], m.loc["Regresión logística", "aciertos"]) == (126, 130)
    assert m.loc["Persistencia (línea base)", "cambios_acertados"] == 0  # por definición no anticipa ningún cambio
    # Criterio de Brandon: más aciertos y, a igualdad, más cambios anticipados (logística 130 y 8; Random Forest 130 y 6)
    assert r["mejor"] == "Regresión logística" and r["le_gana_a_persistencia"]
    assert (m.loc["Regresión logística", "cambios_acertados"], m.loc["Random Forest", "cambios_acertados"]) == (8, 6)


def test_f1_macro_a_mano():
    """ECUACIONES.md §2.2: F1 por clase con la matriz de confusión de la regresión logística (origen móvil) → 0.793."""
    def f1(vp, fp, fn):
        p, rr = vp / (vp + fp), vp / (vp + fn)
        return 2 * p * rr / (p + rr)
    macro = (f1(75, 10, 12) + f1(50, 14, 12) + f1(5, 2, 2)) / 3
    assert round(macro, 3) == 0.793


def test_sesgo_5_lugares_casi_sin_cambios(r):
    """Auditoría: en los 12 meses de prueba los 5 lugares casi no cambiaron de estado; el modelo no se valida ahí."""
    s = r["sesgo"].set_index("grupo")
    assert (s.loc["5 lugares", "casos"], s.loc["5 lugares", "cambios_reales"]) == (48, 2)
    assert s.loc["resto del estado", "cambios_acertados"] == 8


def test_prediccion_es_estimada_y_actual(r):
    p = r["prediccion"]
    assert "estado_mes_siguiente_est" in p  # regla de oro 3: lo estimado lleva _est
    assert (p.mes_siguiente == pd.Timestamp("2026-08-01")).all()
    assert "Costa Mujeres" not in set(p.lugar) and "Laguna Milagros–Xul-Ha" not in set(p.lugar)
