# Autor: Brandon Uriel García Sánchez
# Módulo: Radar
# Qué hace:          Construye y ejecuta el notebook narrado notebooks/02_radar.ipynb (Fase 4): panel mensual, índice de
#                    presión, prueba de validez, índice comparable, modelos contra la persistencia y cadena de Markov.
# Por qué así:       Igual que el notebook 01: el texto se versiona como código y el notebook se ejecuta completo al
#                    construirse (si una celda falla, no se guarda). Las cifras salen de backend/torre/radar al ejecutar.
# Datos de entrada:  datos/silver/ (a través de torre.radar).
# Alimenta a:        Criterios 3 (minería), 4 (ML) y 5 (estocásticos) de la rúbrica; capítulo 8 del documento ejecutivo.
#
# Uso:  .venv\Scripts\python notebooks\_construir_02_radar.py

from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

AQUI = Path(__file__).resolve().parent
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

celdas = [
    md("""# 02 · El Radar: ¿dónde hay presión y dónde hay espacio?
**Torre del Caribe** · Fase 4 (A1 Radar) · Autor: **Brandon Uriel García Sánchez** · UNRC, LCDN 5° semestre 2026-2

| | |
|---|---|
| **Qué hace** | Califica cada lugar, mes por mes, como tranquilo, concurrido o saturado; predice el estado del mes siguiente y el riesgo semanal de que el norte se sature. |
| **Decisiones de Brandon** | Pesos iguales con sensibilidad · percentiles comunes (p50/p90) · escala mín–máx · opción D (ocupación DataTur y componentes de ≥ 2 lugares) · llegadas por cuarto · índice comparable · modelo con más aciertos (hoy, regresión logística) · Markov semanal del norte · clustering con k por silueta (`docs/decisiones/08-radar.md` y `09-auditoria-fases-1-4.md`). |
| **Código** | `backend/torre/radar/`: `panel.py`, `indice.py`, `prediccion.py`, `markov.py`. |
| **Ecuaciones** | `docs/metodologia/ECUACIONES.md` §2. |
| **Alimenta a** | La campaña: un lugar saturado no se promueve; si se espera que se sature, el anuncio se pausa antes. |"""),

    code("""%matplotlib inline
import sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
RAIZ = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(RAIZ / "backend"))

import pandas as pd
import matplotlib.pyplot as plt
from torre.radar import panel as pn, indice as ix, prediccion as pr, markov as mk
from torre.documento.figuras import estilo_unrc, GUINDA, DORADO, GRIS_TEXTO, GRIS_SUAVE
pd.set_option("display.max_colwidth", 60)
estilo_unrc()"""),

    md("""## 1. El panel mensual
Una fila por lugar y mes (enero de 2022 al último mes publicado): los 5 lugares y los destinos del resto del estado,
que dan la escala común. Dos cuidados que se aprendieron al armarlo:
- Los visitantes a zonas arqueológicas se toman del INAH zona por zona: la serie de SITUR-Q es el mismo dato agrupado
  (Chetumal 2025 = Oxtankah + Kohunlich + Dzibanché = 39,459).
- La ocupación de SITUR-Q trae tres filas por mes (disponibles, ocupados y porcentaje): se recalcula como ocupados ÷
  disponibles, nunca se suman ni se promedian porcentajes."""),

    code("""panel = pn.panel_mensual()
print(f"{len(panel):,} filas · {panel.lugar.nunique()} lugares · {panel.periodo.min():%Y-%m} a {panel.periodo.max():%Y-%m}")
pn.cobertura(panel)[["meses_posibles", "llegadas_tren", "cruceristas", "cruces_belice", "visitantes_inah", "ocupacion_pct"]]"""),

    md("""Los 5 lugares no comparten ninguna variable, y la Laguna Milagros no tiene ninguna: el Radar la muestra como
**sin dato oficial**, nunca como tranquila.

## 2. El índice de presión turística
$z=\\dfrac{x-\\min}{\\max-\\min}$ con mínimo y máximo de todo el estado; $IPT=$ promedio de las $z$ disponibles (pesos
iguales). Un componente entra solo si lo tienen al menos 2 lugares (sale Belice, que solo tiene Chetumal)."""),

    code("""base, cortes, comps = ix.calcular()
print("Componentes del índice:", comps)
print(f"Cortes comunes: p50 = {cortes[0]:.3f}, p90 = {cortes[1]:.3f}")
cancun = base[(base.lugar == "Cancún") & (base.periodo == "2026-07-01")].iloc[0]
print("\\nEjemplo a mano, Cancún jul-2026:")
for k in comps:
    if pd.notna(cancun[f"z_{k}"]):
        print(f"  {k:26s} x = {cancun[k]:10.4f}   z = {cancun[f'z_{k}']:.4f}")
print(f"  IPT = promedio = {cancun.ipt:.4f} → {cancun.estado}")"""),

    code("""# Sensibilidad: ¿cuántos lugar-mes cambian de estado si un peso se mueve ±50 %?
ix.sensibilidad(base, comps)"""),

    md("""**Prueba de validez.** La primera versión (solo SITUR-Q) calificaba a Cancún "tranquilo" en julio de 2026 porque
SITUR-Q dejó de publicar ocupación en 2025; DataTur marca 68.8 %. Con la opción D (ocupación de DataTur para los 4
lugares que mide y sin componentes de un solo lugar), el norte queda arriba del sur en 2025–2026:"""),

    code("""m = base[base.periodo.dt.year >= 2025].groupby("lugar").ipt.mean().round(3)
m.drop(["Costa Mujeres", "Laguna Milagros–Xul-Ha"], errors="ignore").sort_values(ascending=False).to_frame("IPT promedio 2025–2026")"""),

    md("""## 3. El índice comparable (el que publica el Radar)
En 2025 los lugares que tenían la ocupación de SITUR-Q la pierden y su índice cae (Chetumal 0.54 → 0.05) sin que
llegue menos gente. Por eso cada lugar se mide siempre con las mismas medidas, las que tiene hoy."""),

    code("""t, cortes_c = pr.indice_comparable(base, comps)
print(f"Cortes del índice comparable: p50 = {cortes_c[0]:.3f}, p90 = {cortes_c[1]:.3f}")
t.dropna(subset=["ipt_comparable"]).groupby("lugar").agg(desde=("periodo", "min"), meses=("periodo", "size"), medidas=("medidas", "first"))"""),

    code("""# Gráfica: el índice comparable de los 5 lugares contra la referencia del norte.
fig, ax = plt.subplots(figsize=(9, 4))
lugares = {"Chetumal": GUINDA, "Bahía Calderitas–Oxtankah": "#565393", "Ruta arqueológica del sur": "#58A65D",
           "Maya Ka'an + Kantemó": "#F26E50"}
referencia = {"Cancún": GRIS_TEXTO, "Tulum": GRIS_SUAVE}
for l, c in {**lugares, **referencia}.items():
    s = t[t.lugar == l].set_index("periodo").ipt_comparable.rolling(3, min_periods=1).mean()
    ax.plot(s.index, s.values, color=c, lw=2.4 if l in lugares else 1.6, ls="-" if l in lugares else "--",
            label=l if l in lugares else f"{l} (referencia)")
ax.axhspan(cortes_c[0], cortes_c[1], color=DORADO, alpha=.12, lw=0)
ax.axhspan(cortes_c[1], 1, color=GUINDA, alpha=.08, lw=0)
ax.text(t.periodo.min(), cortes_c[0] + .01, "concurrido", fontsize=8.5, color=GRIS_TEXTO)
ax.text(t.periodo.min(), cortes_c[1] + .01, "saturado", fontsize=8.5, color=GRIS_TEXTO)
ax.set_ylim(0, 1); ax.set_ylabel("Índice de presión (0 a 1)")
ax.set_title("Los cinco lugares se mantienen en la franja tranquila")
ax.legend(frameon=False, fontsize=8, ncol=2, loc="upper left")
fig.text(0.01, -0.03, "Promedio móvil de 3 meses. Fuentes: SITUR-Q, INAH, SECTUR-DataTur, Censo 2020. "
         "Cálculo: backend/torre/radar", fontsize=7.5, color=GRIS_TEXTO)
fig.savefig(RAIZ / "docs" / "ejecutivo" / "figuras" / "f08_radar.png")
plt.show()"""),

    md("""## 4. ¿Se puede anticipar el mes siguiente?
Tres modelos contra la **persistencia** ("el mes que viene igual que este"), con backtesting de origen móvil: para cada
uno de los últimos 12 meses se reentrena con todo lo anterior y se predice ese mes."""),

    code("""r = pr.correr()
r["metricas"][["modelo", "aciertos", "casos", "cambios_reales", "cambios_acertados", "falsas_alarmas", "f1_macro_origen_movil"]]"""),

    md("""**Lectura honesta:** el estado se repite ocho de cada diez meses, así que la persistencia ya acierta mucho. El
criterio de Brandon elige el modelo que más acierta y, a igualdad, el que más cambios anticipa (tras la auditoría, la
regresión logística: 130 de 156 y 8 de 30 cambios).

**Sesgo** (punto del plan): el mismo backtest separado entre los 5 lugares y el resto del estado."""),

    code("""print("Modelo elegido:", r["mejor"])
r["sesgo"]"""),

    md("""Los 5 lugares casi no cambiaron de estado en la prueba: el modelo no se puede validar ahí. Predicción para el mes
siguiente (estimada):"""),

    code("""r["prediccion"][["lugar", "estado_hoy", "estado_mes_siguiente_est", "prob_tranquilo", "prob_concurrido", "prob_saturado"]].round(2)"""),

    md("""## 5. Cadena de Markov semanal del norte
Estados por percentiles comunes de la ocupación semanal de los 7 centros de DataTur; $\\hat p_{ij}=n_{ij}/\\sum_j n_{ij}$ y
$\\pi_{t+k}=\\pi_tP^k$."""),

    code("""mkv = mk.correr()
print(f"Cortes: p50 = {mkv['cortes'][0]:.1f} %, p90 = {mkv['cortes'][1]:.1f} % · transiciones: {int(mkv['n'].to_numpy().sum()):,}")
mkv["P"].round(3)"""),

    code("""print("Largo plazo (π = πP):", mkv["pi"].round(3).to_dict())
mkv["backtest"]"""),

    code("""mkv["riesgo"].round(3)"""),

    md("""## 6. Minería: el norte comparado con los centros turísticos del país
Clustering jerárquico (Ward) de los centros de DataTur con sus 55 meses completos, por su perfil de ocupación de 12
meses. El número de grupos se elige con la silueta (decisión de Brandon)."""),

    code("""from torre.radar import clustering as cl
from scipy.cluster.hierarchy import dendrogram
cls = cl.correr()
print(f"Centros completos: {len(cls['perfiles'])} · excluidos: {len(cls['excluidos'])}")
print("Silueta por k:", {k: round(v, 3) for k, v in cls["siluetas"].items()}, "→ k =", cls["k"])
cls["tabla"]"""),

    code("""fig, ax = plt.subplots(figsize=(10, 4))
dendrogram(cls["Z"], labels=list(cls["perfiles"].index), leaf_font_size=6, color_threshold=cls["Z"][-cls["k"] + 1, 2], ax=ax)
ax.set_title("Centros turísticos del país agrupados por su ocupación mensual (Ward)")
ax.set_ylabel("Distancia de Ward")
plt.show()"""),

    md("""## 7. Qué se concluye
1. **Los cinco lugares están tranquilos** en el último mes publicado y el modelo espera que sigan así; la Laguna Milagros
   no tiene dato oficial y así se muestra.
2. **La validez se probó, no se supuso:** la primera versión del índice falló con un caso conocido (Cancún) y se corrigió
   con datos, no a ojo.
3. **El aprendizaje de máquina agrega poco pero algo:** +4 aciertos de 156 sobre la persistencia y 8 cambios anticipados,
   todos en lugares de referencia (los 5 lugares casi no cambiaron de estado).
4. **La cadena de Markov da probabilidades mejor calibradas** que la persistencia a 1, 4 y 8 semanas; su valor es el
   riesgo, no una etiqueta.
5. **El norte de Quintana Roo está en el grupo de los destinos más llenos del país** (k = 2 por silueta).
6. **Limitaciones declaradas:** el sur no tiene ocupación oficial desde 2025 ni datos semanales; la matriz de Markov es
   la misma para los 7 centros; las llegadas por cuarto quedan dominadas por los puertos de crucero; DataTur marca menos
   ocupación que SITUR-Q para el mismo lugar."""),
]

nb = nbf.v4.new_notebook(cells=celdas, metadata={
    "kernelspec": {"name": "python3", "display_name": "Python 3 (.venv)", "language": "python"},
    "language_info": {"name": "python"}})
NotebookClient(nb, timeout=1200, kernel_name="python3", resources={"metadata": {"path": str(AQUI)}}).execute()
salida = AQUI / "02_radar.ipynb"
nbf.write(nb, salida)
print(f"Notebook ejecutado y guardado: {salida}")
