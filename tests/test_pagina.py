# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña (pruebas de la página)
# Qué hace:          Revisa las cifras que muestra la página (frontend/datos/pagina.js): que solo hablen de las 5
#                    regiones y que reproduzcan cifras conocidas.
# Por qué así:       Regla de oro 9 (28-sep-2026): la portada y las fichas nunca muestran lugares con sargazo, cierres o
#                    saturación. Esta prueba falla si alguien vuelve a meter Tulum, Cancún o Cobá en las fichas.
# Datos de entrada:  frontend/datos/pagina.js (generado por backend/torre/api/datos_pagina.py).
# Alimenta a:        La confianza en lo que ve el público.

import json
from pathlib import Path

import pytest

PAGINA = Path(__file__).resolve().parents[1] / "frontend" / "datos" / "pagina.js"
pytestmark = pytest.mark.skipif(not PAGINA.exists(), reason="Aún no se generan los datos de la página")


@pytest.fixture(scope="module")
def datos() -> dict:
    t = PAGINA.read_text(encoding="utf-8")
    return json.loads(t[t.index("{"):t.rindex("}") + 1])


def test_solo_las_5_regiones(datos):
    nombres = [r["nombre"] for r in datos["regiones"]]
    assert nombres == ["Chetumal", "Calderitas y Oxtankah", "Ruta de las pirámides", "Maya Ka'an", "Laguna Milagros y Xul-Ha"]
    texto_fichas = json.dumps(datos["regiones"], ensure_ascii=False)
    for fuera in ("Tulum", "Cancún", "Cobá", "Muyil", "Riviera", "Cozumel", "Holbox", "Mahahual"):
        assert fuera not in texto_fichas


def test_cuartos_vacios_chetumal(datos):
    """2024: 458,696 de 791,016 noches ocupadas = 58.0 % → 4 de cada 10 vacías (sin promediar porcentajes)."""
    c = datos["cuartos_vacios_chetumal"]
    assert (c["anio"], c["noches_ocupadas"], c["noches_disponibles"], c["vacios_de_cada_10"]) == (2024, 458_696, 791_016, 4)


def test_cifras_de_las_fichas(datos):
    r = {x["nombre"]: x for x in datos["regiones"]}
    assert r["Chetumal"]["viven"]["valor"] == 169_028 and r["Chetumal"]["llegaron_en_tren"]["valor"] == 3_843
    assert r["Ruta de las pirámides"]["visitantes_zonas"]["valor"] == 66_628
    assert r["Calderitas y Oxtankah"]["visitantes_zonas"]["valor"] == 11_017


def test_hueco_declarado_en_la_laguna(datos):
    """Laguna Milagros–Xul-Ha no tiene estadística turística propia: se declara, no se inventa."""
    laguna = next(x for x in datos["regiones"] if x["nombre"] == "Laguna Milagros y Xul-Ha")
    assert laguna["sin_estadistica"] and "llegaron_en_tren" not in laguna and "visitantes_zonas" not in laguna


def test_ubicaciones_en_quintana_roo():
    """Cada pueblo y zona de las 5 regiones está en Quintana Roo y en su municipio (Censo, INAH y mapa municipal)."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
    from torre.base.ubicaciones import verificar_regiones

    v = verificar_regiones()
    for columna in ("censo_quintana_roo", "inah_quintana_roo", "dentro_del_municipio"):
        assert v[columna].dropna().all(), f"falló {columna}"


def test_fotos_con_credito_y_licencia_libre(datos):
    """Cada lugar tiene foto local con autor y licencia libre (la licencia exige mostrar el crédito)."""
    for r in datos["regiones"]:
        f = r["foto"]
        assert (PAGINA.parents[1] / f["archivo_local"]).exists()
        assert f["autor"] and f["licencia"].startswith(("CC BY", "CC0", "Public domain")) and f["url_original"]


# --- Secciones nuevas: cómo se mueven, el dinero, las fases y las preguntas rápidas -------------------------------------
def test_movimiento_cifras_conocidas(datos):
    """Totales por modo = último año completo de SITUR-Q (el avión se queda en 2024 por la regla 6 de Silver)."""
    m = datos["movimiento"]["modos"]
    assert (m["avion"]["anio"], m["avion"]["total"]) == (2024, 15_959_277)
    assert (m["tren"]["anio"], m["tren"]["total"]) == (2025, 560_241)
    assert (m["crucero"]["anio"], m["crucero"]["total"]) == (2025, 7_556_937)
    assert (m["frontera"]["anio"], m["frontera"]["total"]) == (2025, 653_306)
    for modo in m.values():  # cada total es la suma de sus puntos: nada se agrega por fuera
        assert sum(p["valor"] for p in modo["puntos"]) == modo["total"]


def test_hospedaje_cifras_conocidas(datos):
    h = datos["hospedaje"]
    por_hotel = {d["lugar"]: round(d["cuartos_por_hotel"], 1) for d in h["destinos"]}
    assert por_hotel["Chetumal"] == 27.1 and por_hotel["Cancún"] == 219.4
    sur = h["tamano_negocios"]["municipios_de_los_lugares"]
    assert (sur["chicos"], sur["medianos"], sur["grandes"]) == (107, 38, 0)
    assert "unidad" in h["hueco_derrama"]  # la derrama se declara como hueco, no se muestra


def test_doce_fases(datos):
    assert [f["fase"] for f in datos["fases"]] == [str(i) for i in range(12)]


def test_radar_solo_5_lugares_y_referencias(datos):
    """Regla de oro 9 en el Radar: los 5 lugares + Cancún, Playa del Carmen y Tulum como referencia; nada más."""
    r = datos["radar"]
    assert [l["nombre"] for l in r["lugares"]] == [x["nombre"] for x in datos["regiones"]]
    assert [l["nombre"] for l in r["referencia"]] == ["Cancún", "Playa del Carmen", "Tulum"]
    texto = json.dumps({k: r[k] for k in ("lugares", "referencia")}, ensure_ascii=False)
    for fuera in ("Mahahual", "Holbox", "Bacalar", "Cozumel", "Isla Mujeres", "Costa Mujeres"):
        assert fuera not in texto


def test_radar_laguna_sin_dato_y_prediccion_estimada(datos):
    lug = {l["nombre"]: l for l in datos["radar"]["lugares"]}
    assert lug["Laguna Milagros y Xul-Ha"]["estado"] == "sin dato oficial" and lug["Laguna Milagros y Xul-Ha"]["indice"] is None
    assert all("estado_siguiente_est" in l for l in lug.values())  # regla de oro 3: lo estimado lleva _est
    m = datos["radar"]["modelo"]
    assert (m["aciertos"], m["casos"], m["aciertos_persistencia"]) == (130, 156, 126)


def test_preguntas_sin_precios_inventados(datos):
    """El chat no da precios (no hay fuente oficial abierta) y la respuesta de espacio usa la cifra de SITUR-Q."""
    p = {q["pregunta"]: q["respuesta"] for q in datos["preguntas"]}
    assert p["¿Cuánto cuesta ir?"].startswith("No damos precios")
    assert "$" not in json.dumps(datos["preguntas"], ensure_ascii=False)
    assert "458,696 de 791,016" in p["¿Hay espacio en Chetumal?"]
