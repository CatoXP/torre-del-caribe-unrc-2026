# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos (auditoría de documentos, 29-sep-2026)
# Qué hace:          Recalcula con el código las cifras clave de las Fases 3 y 4 y comprueba que los documentos
#                    (ECUACIONES.md, notas de decisión, documento ejecutivo) digan exactamente eso.
# Por qué así:       Regla de oro 2: toda cifra es rastreable. Un documento que dice 136 cuando el código da 135 es un
#                    error que el jurado puede encontrar. Esta prueba falla si una cifra escrita ya no cuadra con los
#                    datos (por ejemplo, después de volver a descargar una fuente).
# Datos de entrada:  datos/gold (salidas del Radar y del planteamiento) y docs/.
# Alimenta a:        La confianza en todo lo que se entrega (informe, coloquio y página).

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "backend"))
GOLD = RAIZ / "datos" / "gold"
pytestmark = pytest.mark.skipif(not (GOLD / "radar_modelos.parquet").exists(), reason="Aún no existen las salidas del Radar")

DOCS = {"ec": RAIZ / "docs/metodologia/ECUACIONES.md", "radar": RAIZ / "docs/decisiones/08-radar.md",
        "plan": RAIZ / "docs/decisiones/05-planteamiento.md", "ejec": RAIZ / "docs/ejecutivo/DOCUMENTO_EJECUTIVO.md",
        "silver5": RAIZ / "docs/decisiones/10-silver-fase5.md", "pron": RAIZ / "docs/decisiones/11-pronostico.md"}


@pytest.fixture(scope="module")
def textos():
    return {k: p.read_text(encoding="utf-8") for k, p in DOCS.items()}


@pytest.fixture(scope="module")
def cifras():
    """Cada cifra recalculada desde Gold o desde las funciones, con el formato con que se escribe en los documentos."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from torre.radar import markov, planteamiento
        est = pd.read_parquet(GOLD / "radar_estado.parquet")
        comp = pd.read_parquet(GOLD / "radar_indice_comparable.parquet")
        mod = pd.read_parquet(GOLD / "radar_modelos.parquet").set_index("modelo")
        mk = markov.correr()
        conc = planteamiento.concentracion().set_index("dimension")
        from torre.base.silver_huracanes import eventos_sur
        hur = pd.read_parquet(RAIZ / "datos" / "silver" / "huracanes")
        ev = eventos_sur(hur)
        fm = pd.read_parquet(RAIZ / "datos" / "silver" / "fred_mensual")
        fu = pd.read_parquet(GOLD / "pronostico_fuerza_estacional.parquet").set_index("lugar")
        fa = pd.read_parquet(GOLD / "pronostico_forma_anio.parquet")
        ruta_ene = fa[(fa.lugar == "Ruta arqueológica del sur") & (fa.mes == 1)].indice.iloc[0]
        el = pd.read_parquet(GOLD / "pronostico_eleccion.parquet")
        el = el[el.elegido_flag].set_index("serie")
        pm = pd.read_parquet(GOLD / "pronostico_mes.parquet")
        dic = pm[(pm.lugar == "Bahía Calderitas–Oxtankah") & (pm.periodo == pd.Timestamp("2026-12-01"))].iloc[0]
        an = pd.read_parquet(GOLD / "pronostico_escenarios_anual.parquet")
        an = an[an.golpe_tormenta_supuesto == 0].set_index("lugar")
        po = pd.read_parquet(GOLD / "pronostico_poisson_tormentas.parquet")
    elegido = pd.read_parquet(GOLD / "radar_prediccion.parquet").modelo.iloc[0]  # el que eligió el criterio de Brandon
    md, pe = mod.loc[elegido], mod.loc["Persistencia (línea base)"]
    cancun = est[(est.lugar == "Cancún") & (est.periodo == "2026-07-01")].iloc[0]
    bt = mk["backtest"].set_index(["k_semanas", "metodo"]).brier
    return {
        "corte p50": f"p50 = {est.corte_p50.iloc[0]:.3f}", "corte p90": f"p90 = {est.corte_p90.iloc[0]:.3f}",
        "corte p50 (4 decimales)": f"u_{{50}}={est.corte_p50.iloc[0]:.4f}",
        "comparable p50": f"u_{{50}}={comp.corte_p50.iloc[0]:.3f}", "comparable p90": f"u_{{90}}={comp.corte_p90.iloc[0]:.3f}",
        "IPT de Cancún jul-2026": f"={cancun.ipt:.4f}",
        "aciertos del modelo": f"**{int(md.aciertos)}**", "aciertos de la persistencia": f"| {int(pe.aciertos)} |",
        "cambios anticipados": f"{int(md.cambios_acertados)} de los {int(md.cambios_reales)}",
        "Markov p50": f"{mk['cortes'][0]:.1f}", "Markov p90": f"{mk['cortes'][1]:.1f}",
        "transiciones": f"{int(mk['n'].to_numpy().sum()):,}",
        "Brier 1 semana": f"{bt[(1, 'Markov')]:.3f}", "Brier 4 semanas": f"{bt[(4, 'Markov')]:.3f}",
        "Brier 8 semanas": f"{bt[(8, 'Markov')]:.3f}",
        "HHI* avión": f"{conc.loc['Llegadas en avión', 'hhi_normalizado']:.3f}",
        "población": f"{conc.loc['Población', 'cuota_5_lugares_pct']:.1f} %",
        "negocios": f"{conc.loc['Negocios turísticos', 'cuota_5_lugares_pct']:.1f} %",
        "cuartos": f"{int(conc.loc['Cuartos de hotel', 'total']):,}",
        "puntos HURDAT2": f"{len(hur):,} puntos", "eventos sur": f"**{len(ev)} tormentas en 60 años**",
        "tasa anual": f"{len(ev)}/60=$ **{len(ev) / 60:.3f} por año**",
        "tipo de cambio ago-2026": f"{fm[fm.periodo.astype(str) == '2026-08-01'].pesos_por_dolar.iloc[0]:.4f} pesos",
        "fuerza Ruta": f"| {fu.loc['Ruta arqueológica del sur', 'fuerza_estacional']:.3f} |",
        "STL Belice": f"{fu.loc['Chetumal', 'corr_con_stl']:.3f}",
        "índice Ruta enero": f"$S_1=$ **{ruta_ene:.3f}**",
        "índice Ruta enero %": f"enero recibe {round((ruta_ene - 1) * 100)} % más",
        "Bahía vs base": f"**{el.loc['Bahía Calderitas–Oxtankah · visitantes INAH', 'mae_vs_base']:.3f}**",
        "cobertura Ruta": f"| {el.loc['Ruta arqueológica del sur · visitantes INAH', 'cobertura_pct']:.1f} % |",
        "máximo dic Bahía": f"**{dic.maximo_90_est:,.0f}**",
        "esperado dic Bahía": f"{dic.esperado_est:,.0f} visitantes",
        "probable Ruta": f"| {an.loc['Ruta arqueológica del sur', 'probable_p50_est']:,.0f} |",
        "al menos una tormenta": f"**{(1 - np.exp(-po['lambda'].sum())) * 100:.1f} %**",
        "riesgo capacidad Belice": f"| {an.loc['Chetumal', 'riesgo_algun_mes_sobre_capacidad'] * 100:.1f} % |",
    }


# (documento, clave de la cifra recalculada): la cifra, con el formato de arriba, debe aparecer tal cual en el documento.
AFIRMACIONES = [
    ("radar", "corte p50"), ("radar", "corte p90"), ("ec", "corte p50 (4 decimales)"),
    ("ec", "comparable p50"), ("ec", "comparable p90"), ("ec", "IPT de Cancún jul-2026"),
    ("ec", "aciertos del modelo"), ("ec", "aciertos de la persistencia"), ("ejec", "aciertos del modelo"),
    ("ejec", "cambios anticipados"), ("ec", "Markov p50"), ("ec", "Markov p90"), ("ec", "transiciones"),
    ("ec", "Brier 1 semana"), ("ec", "Brier 4 semanas"), ("ec", "Brier 8 semanas"), ("ec", "HHI* avión"),
    ("plan", "población"), ("plan", "negocios"), ("plan", "cuartos"),
    ("silver5", "puntos HURDAT2"), ("ejec", "eventos sur"), ("ec", "tasa anual"), ("silver5", "tipo de cambio ago-2026"),
    ("ec", "fuerza Ruta"), ("pron", "STL Belice"), ("ec", "índice Ruta enero"), ("ejec", "índice Ruta enero %"),
    ("ec", "Bahía vs base"), ("pron", "cobertura Ruta"), ("ec", "máximo dic Bahía"), ("ejec", "esperado dic Bahía"),
    ("ejec", "probable Ruta"), ("ec", "al menos una tormenta"), ("pron", "riesgo capacidad Belice"),
]


@pytest.mark.parametrize("doc, clave", AFIRMACIONES)
def test_cifra_escrita_coincide_con_el_calculo(textos, cifras, doc, clave):
    assert cifras[clave] in textos[doc], f"{DOCS[doc].name} no dice '{cifras[clave]}' ({clave}, lo que da el cálculo)"
