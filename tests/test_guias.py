# Autor: Brandon Uriel García Sánchez
# Módulo: Documento (pruebas de las guías)
# Qué hace:          Recalcula con los datos y el código las cifras clave de las tres guías (docs/guias/) y comprueba que
#                    el texto diga exactamente eso. Si una fuente se vuelve a descargar y una cifra cambia, la prueba
#                    falla y obliga a corregir la guía.
# Por qué así:       Regla de oro 2 (toda cifra es rastreable). Las guías son lo que Brandon enseña a los profesores: no
#                    pueden quedarse con un número viejo. Mismo enfoque que tests/test_documentos.py.
# Datos de entrada:  datos/silver, datos/gold y las funciones del paquete torre.
# Alimenta a:        La confianza en la defensa del proyecto (guía técnica, sencilla y de decisiones).

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from torre.base.entorno import RAIZ  # noqa: E402

GOLD = RAIZ / "datos" / "gold"
SILVER = RAIZ / "datos" / "silver"
pytestmark = pytest.mark.skipif(not (GOLD / "campana.json").exists(), reason="Faltan salidas de las fases")
TECNICA = (RAIZ / "docs" / "guias" / "1_GUIA_TECNICA.md").read_text(encoding="utf-8")
SENCILLA = (RAIZ / "docs" / "guias" / "2_GUIA_SENCILLA.md").read_text(encoding="utf-8")


def en(texto: str, *cifras: str):
    for c in cifras:
        assert c in texto, f"La guía no dice «{c}»"


def test_inah_tulum_y_ruta():
    i = pd.read_parquet(SILVER / "inah")
    q = i[i.es_qroo]
    q = q.assign(anio=q.anio.astype(int))
    tulum = q[q.nombre == "Z.A. de Tulum"]
    e26 = tulum[(tulum.anio == 2026) & (tulum.mes <= 7)].visitantes.sum()
    e25 = tulum[(tulum.anio == 2025) & (tulum.mes <= 7)].visitantes.sum()
    assert (e26, e25) == (476_247, 692_946)
    assert round((e26 / e25 - 1) * 100, 1) == -31.3
    v = q[q.anio == 2025].groupby("region_campana").visitantes.sum()
    assert v["Ruta arqueológica del sur"] == 66_628 and round(v["Tulum"] / v["Ruta arqueológica del sur"], 1) == 15.5
    en(TECNICA, "476{,}247", "692{,}946", "-31.3", "66{,}628", "15.5")
    en(SENCILLA, "15.5 veces")


def test_concentracion_y_radar():
    from torre.radar.planteamiento import concentracion
    c = concentracion().set_index("dimension")
    assert round(c.loc["Llegadas en avión", "hhi_normalizado"], 3) == 0.811
    en(TECNICA, "0.811", "12.3 %", "1.4 %")
    ic = pd.read_parquet(GOLD / "radar_indice_comparable.parquet").ipt_comparable.dropna()
    assert (round(ic.quantile(0.5), 3), round(ic.quantile(0.9), 3)) == (0.186, 0.756)
    m = pd.read_parquet(GOLD / "radar_modelos.parquet").set_index("modelo").aciertos
    assert (m["Regresión logística"], m["Persistencia (línea base)"]) == (130, 126)
    p = pd.read_parquet(GOLD / "radar_markov_matriz.parquet")
    assert round(p.loc["tranquilo", "tranquilo"], 3) == 0.922 and round(p.loc["concurrido", "saturado"], 3) == 0.069
    en(TECNICA, "0.186", "0.756", "0.1931", "130", "0.922")


def test_forma_holt_winters_y_regresion():
    from statsmodels.tsa.holtwinters import ExponentialSmoothing

    import torre.pronostico.modelos as M
    s = pd.read_parquet(GOLD / "pronostico_series.parquet")
    r = s[s.lugar == "Ruta arqueológica del sur"]
    o = r.periodo.max()
    S = M.forma_hasta(r, o)
    assert round(S[1], 3) == 1.606
    y = M.tramo_actual(r, o)
    z = (y / y.index.month.map(S).values).to_numpy()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        f = ExponentialSmoothing(z, initialization_method="estimated").fit()
    assert round(f.params["smoothing_level"], 4) == 0.1183
    assert round(f.forecast(1)[0] * S[1]) == 8_559
    b = s[s.lugar == "Bahía Calderitas–Oxtankah"]
    assert round(M.regresion_con_clima(b, b.periodo.max(), pd.DatetimeIndex(["2026-12-01"]))[0]) == 1_311
    assert round(np.exp(7.0382 + 0.1404)) == 1_311
    en(TECNICA, "1.606", "0.1183", "5{,}329.4", "8{,}559", "7.0382", "0.1404", "1{,}311")


def test_rango_poisson_y_escenarios():
    m = pd.read_parquet(GOLD / "pronostico_mes.parquet")
    x = m[(m.lugar == "Bahía Calderitas–Oxtankah") & (m.periodo == "2026-12-01")].iloc[0]
    assert (round(x.minimo_90_est), round(x.maximo_90_est)) == (959, 1_793)
    p = pd.read_parquet(GOLD / "pronostico_poisson_tormentas.parquet").set_index("mes")
    assert round(p.loc[8, "prob_tormenta"] * 100, 1) == 13.9
    assert round((1 - np.exp(-p.eventos.sum() / 60)) * 100, 1) == 40.3
    e = pd.read_parquet(GOLD / "pronostico_escenarios.parquet")
    a = e[(e.lugar == "Bahía Calderitas–Oxtankah") & (e.golpe_tormenta_supuesto == 0) & (e.periodo == "2026-08-01")].iloc[0]
    assert (round(a.malo_p10_est), round(a.probable_p50_est), round(a.bueno_p90_est)) == (684, 930, 1_202)
    en(TECNICA, "959", "1{,}793", "13.9", "40.3", "684 / 930 / 1,202")
    en(SENCILLA, "13.9 %", "1,311 visitantes")


def test_presupuesto_torre_y_campana():
    from torre.campana.presupuesto import resolver
    sol = resolver()
    assert round(sol["visitantes_esperados"], 1) == 956.8
    assert round(sol["r"]["Google"] * 1000, 2) == 1.59 and round(sol["r"]["Facebook"] * 1000, 2) == 6.61
    en(TECNICA, "956.8", "1.59", "6.61", "10{,}624", "4{,}553")
    s = pd.read_parquet(GOLD / "envivo_senales.parquet")
    assert (s.chetumal_clima_raro.sum(), s.kohunlich_clima_raro.sum()) == (21, 17)
    d = pd.read_parquet(GOLD / "envivo_decisiones.parquet")
    assert (d.accion == "pausado").sum() == 48
    asp = pd.read_parquet(GOLD / "campana_aspectos.parquet").set_index(["pueblo", "aspecto"]).riesgo_relativo
    assert round(asp["Quintana Roo (3 pueblos)", "ruido"], 2) == 2.76
    en(TECNICA, "21 semanas raras", "48 pausas", "2.76", "2.82", "250", "9,408,423")
    en(SENCILLA, "957 visitantes", "$196", "250 extranjeros")


def test_isolation_forest_nadine():
    from torre.envivo.senales import anomalias_clima, clima_semanal
    c = anomalias_clima(clima_semanal())
    n = c[(c.punto == "chetumal") & (c.semana == "2024-10-14")].iloc[0]
    assert round(n.puntaje_anomalia, 3) == 0.712 and round(n.corte_anomalia, 3) == 0.543 and n.clima_raro
    c256 = 2 * (np.log(255) + 0.5772) - 2 * 255 / 256
    assert round(c256, 3) == 10.245
    en(TECNICA, "0.712", "0.543", "10.245")


def test_estructura_del_codigo():
    archivos = [f for f in (RAIZ / "backend" / "torre").glob("*/*.py") if f.name != "__init__.py"]
    assert len(archivos) == 55
    silver = list((RAIZ / "backend" / "torre" / "base").glob("silver_*.py"))
    assert len(silver) == 12
    tablas = (RAIZ / "docs" / "datos" / "DICCIONARIO.md").read_text(encoding="utf-8").count("\n## ")
    assert tablas == 56
    en(TECNICA, "**55 archivos**", "(12 archivos)", "56 tablas")


def test_imagenes_del_documento_ejecutivo_existen():
    # El 02-oct-2026 se encontró borrada capturas/c01_portada.png: el PDF habría salido sin ella sin que nadie lo notara.
    import re
    doc = RAIZ / "docs" / "ejecutivo" / "DOCUMENTO_EJECUTIVO.md"
    refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", doc.read_text(encoding="utf-8"))
    faltan = [r for r in refs if not (doc.parent / r).exists()]
    assert refs and faltan == [], f"Imágenes que faltan: {faltan}"
