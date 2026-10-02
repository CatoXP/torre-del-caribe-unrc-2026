# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña (pruebas, Fase 8)
# Qué hace:          Pruebas de la minería de texto (cifras conocidas) y de la campaña: personas con etiqueta de origen
#                    del dato, mensajes con respaldo y dentro de los límites de cada plataforma, fotos que existen, nunca
#                    anunciar el norte ni un dominio que no es del proyecto.
# Por qué así:       Reglas de oro 1, 2 y 9 aplicadas a la mercadotecnia: un anuncio no puede prometer lo que el dato no
#                    sostiene (docs/decisiones/21-campana.md).
# Datos de entrada:  datos/gold/campana*.{parquet,json}; torre.campana.texto y marca.
# Alimenta a:        La confianza en la Fase 8.

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402
from torre.campana.marca import LIMITES, revisar_largos  # noqa: E402
from torre.campana.texto import ASPECTOS, tokens  # noqa: E402

GOLD = RAIZ / "datos" / "gold"
pytestmark = pytest.mark.skipif(not (GOLD / "campana.json").exists(), reason="Aún no se arma la campaña")


@pytest.fixture(scope="module")
def c():
    return json.loads((GOLD / "campana.json").read_text(encoding="utf-8"))


def test_aspectos_cifras_conocidas():
    a = pd.read_parquet(GOLD / "campana_aspectos.parquet").set_index(["pueblo", "aspecto"])
    q = a.loc["Quintana Roo (3 pueblos)"]
    assert set(q.index) == set(ASPECTOS)
    assert q.loc["ruido", "riesgo_relativo"] == pytest.approx(2.76, abs=0.01)
    assert q.loc["calma", "riesgo_relativo"] == pytest.approx(0.41, abs=0.01)
    # riesgo relativo a mano: % malas entre las que tocan el tema ÷ % malas de todas
    assert q.loc["ruido", "riesgo_relativo"] == pytest.approx(q.loc["ruido", "pct_malas"] / q.loc["ruido", "pct_malas_pueblo"])


def test_reglas_de_asociacion():
    r = pd.read_parquet(GOLD / "campana_reglas.parquet")
    malas = r[r.entonces.str.contains("mala")].set_index("si")
    assert malas.loc["ruido + servicio", "lift"] == pytest.approx(2.82, abs=0.01)
    assert (r.lift >= 1).all() and r.confianza.between(0, 1).all()


def test_palabras_y_tokens():
    p = pd.read_parquet(GOLD / "campana_palabras.parquet")
    cinco = set(p[p.lado.str.contains("5")].palabra)
    assert {"excelente", "increíble"} <= cinco
    assert tokens("La comida estuvo deliciosa y el lugar muy tranquilo") == ["comida", "deliciosa", "tranquilo"]  # "estuvo", "el", "muy"... son palabras vacías


def test_personas_declaran_de_donde_sale_cada_rasgo(c):
    assert [p["clave"] for p in c["personas"]] == ["vuelve", "baja"]
    for p in c["personas"]:
        assert all(t in {"dato", "derivado", "supuesto", "hueco"} for _, _, t, _ in p["atributos"])
    assert c["cifras"]["chetumal_extranjeros"] == 250 and c["cifras"]["veces_ruta"] == 15.5


def test_mensajes_con_respaldo_y_limites(c):
    assert revisar_largos(c["mensajes"]) == []
    for m in c["mensajes"]:
        assert m["respaldo"] and m["lugar"] in {"Chetumal", "Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur"}
        texto = json.dumps(m, ensure_ascii=False).lower()
        assert "$" not in texto and "hora" not in texto  # sin precios ni horas de viaje: no hay dato
        if "foto" in m:
            assert (RAIZ / "frontend" / m["foto"]).exists()
    assert LIMITES["google_titulo"] == 30


def test_calendario_coherente_y_sin_dominio_inventado(c):
    for mes in c["calendario"]:
        assert (mes["pesos"] == 0) == (mes["personas"] == [])
    app = (RAIZ / "frontend" / "app.js").read_text(encoding="utf-8")
    assert "elsurtieneespacio.mx" not in app
