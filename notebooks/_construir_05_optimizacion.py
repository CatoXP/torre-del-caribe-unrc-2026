# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña (Investigación de Operaciones)
# Qué hace:          Construye y ejecuta el notebook narrado notebooks/05_optimizacion.ipynb (Fase 6): parámetros, modelo
#                    de dos etapas, reparto, costo de cada regla, precios sombra, frontera de Pareto y sensibilidad.
# Por qué así:       Igual que los notebooks 01–03: el texto se versiona como código y el notebook se ejecuta completo al
#                    construirse (si una celda falla, no se guarda). Las cifras salen de torre.campana.presupuesto.
# Datos de entrada:  datos/gold/pronostico_*, datos/silver/fred_mensual, datos/bronze/benchmarks (por el paquete).
# Alimenta a:        Criterio 6 (Investigación de Operaciones) de la rúbrica; capítulo 10 del documento ejecutivo.
#
# Uso:  .venv\Scripts\python notebooks\_construir_05_optimizacion.py

from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

AQUI = Path(__file__).resolve().parent
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

celdas = [
    md("""# 05 · ¿Cuánto dinero, dónde y cuándo? Reparto del presupuesto
**Torre del Caribe** · Fase 6 (Investigación de Operaciones) · Autor: **Brandon Uriel García Sánchez** · UNRC, LCDN 5° semestre 2026-2

| | |
|---|---|
| **Qué hace** | Reparte el presupuesto entre meses, los 3 lugares del sur y dos canales (Google, Facebook) para traer el máximo de visitantes sin rebasar la capacidad de nadie. |
| **Decisiones de Brandon** | Objetivo: visitantes al sur · presupuesto $250,000 al año (supuesto) · conversión de Facebook con barrido · cero anuncio en temporada alta, capacidad probada, piso de 15 % por lugar y tope de 70 % por canal · desempate proporcional al espacio libre (`docs/decisiones/19-presupuesto.md`). |
| **Código** | `backend/torre/campana/presupuesto.py` (PuLP + CBC). |
| **Ecuaciones** | `docs/metodologia/ECUACIONES.md` §4. |
| **Alimenta a** | El plan de medios de la campaña (Fase 8) y las pausas que ejecuta la Torre en vivo (Fase 7). |"""),

    code("""%matplotlib inline
import sys, warnings
from dataclasses import replace
from pathlib import Path
warnings.filterwarnings("ignore")
RAIZ = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(RAIZ / "backend"))

import pandas as pd
import matplotlib.pyplot as plt
from torre.campana import presupuesto as pz
from torre.documento.figuras import estilo_unrc, GUINDA, DORADO, GRIS_TEXTO
pd.set_option("display.max_colwidth", 60)
estilo_unrc()"""),

    md("""## 1. Los parámetros, todos de archivos
- **Costo por clic y conversión** de la categoría *Travel* (WordStream 2025, capturado en la Fase 1, D13). Son promedios
  de anunciantes de EE. UU.: se usan como supuesto etiquetado.
- **Conversión de Facebook para turismo:** no está publicada. El caso base usa la de Google Travel (5.75 %) y la
  sensibilidad prueba 3 % y la mediana de Facebook en todas las industrias.
- **Pesos por dólar:** FRED, último mes completo.
- **Meses:** los que tienen calendario (temporada) y escenarios del Monte Carlo (Fase 5) para los 3 lugares."""),

    code("""b = pz.benchmarks(); tc, mes_tc = pz.pesos_por_dolar()
ch = pz.canales(pz.Supuestos())
print(f"Pesos por dólar: {tc:.4f} ({mes_tc})")
for c, v in ch.items():
    r = v['cvr'] / v['cpc_mxn']
    print(f"{c:9s} clic = ${v['cpc_mxn']:.2f} MXN · conversión {v['cvr']:.2%} · r = {v['cvr']:.4f} ÷ {v['cpc_mxn']:.2f} = {r*1000:.2f} por cada $1,000")
t = pz.tabla_meses()
t[["periodo", "lugar", "nivel", "probable_p50_est", "bueno_p90_est", "capacidad_probada", "libre"]].round(3)"""),

    md("""## 2. El modelo de dos etapas
**Etapa 1** (se decide hoy): $x_{m,l,c}\\ge0$, pesos en el mes $m$, lugar $l$ y canal $c$. Conversiones
$v_{m,l}=\\sum_c r_c\\,x_{m,l,c}$.

**Etapa 2** (recurso, por escenario $s\\in\\{$malo, probable, bueno$\\}$ con pesos 30/40/30): $y_{s,m,l}\\in\\{0,1\\}$
enciende o pausa el anuncio; si $D_{s,m,l}+v_{m,l}>C_l$ el anuncio se pausa y esas conversiones se pierden.

$$\\max\\ \\sum_s p_s\\sum_{m,l} w_{s,m,l}\\quad\\text{s. a.}\\quad w\\le v,\\ w\\le U\\,y,\\ D_{s}+v\\le C+M(1-y)$$
$$\\sum x\\le B,\\quad x_{m,l,\\cdot}=0\\ \\text{en temporada alta},\\quad D^{p50}_{m,l}+v_{m,l}\\le C_l,\\quad
\\sum_{m,c}x_{m,l,c}\\ge0.15B,\\quad \\sum_{m,l}x_{m,l,c}\\le0.70B$$

Paso 2 (desempate, lexicográfico): con el mismo máximo de visitantes, se minimiza $\\sum|x-\\text{meta}|$ con
meta $=\\dfrac{\\text{libre}_{m,l}}{\\sum\\text{libre}}\\times$ total del canal, y libre $=1-D^{p50}/C$."""),

    code("""sol = pz.resolver()
print(f"Presupuesto del periodo: ${sol['presupuesto']:,.0f} ({len(sol['meses'])} meses × $250,000 ÷ 12)")
print(f"Visitantes esperados: {sol['visitantes_esperados']:,.1f} → ${sol['presupuesto']/sol['visitantes_esperados']:,.0f} por visitante")
print(f"Meses permitidos: {sum(sol['permitida'].values())} de {len(sol['permitida'])}; pausas donde hay dinero: {len(sol['pausas'].query('encendido == 0'))}")
sol["plan"].pivot_table(index="periodo", columns="lugar", values="pesos", aggfunc="sum").round(0)"""),

    md("""**Ejemplo a mano.** Como Facebook rinde más por peso, se lleva su tope (70 %) y el resto va a Google:
$0.70\\times187{,}500\\times0.006608+0.30\\times187{,}500\\times0.001590=867.3+89.4=956.8$ visitantes."""),

    code("""fig, ax = plt.subplots(figsize=(10, 3.8))
tabla = sol["plan"].pivot_table(index="periodo", columns="lugar", values="pesos", aggfunc="sum")
tabla.index = [f"{p:%m-%Y}" for p in tabla.index]
tabla[["Ruta arqueológica del sur", "Bahía Calderitas–Oxtankah", "Chetumal"]].plot.bar(stacked=True, ax=ax,
    color=[GUINDA, DORADO, "#565393"], width=0.7)
ax.set_ylabel("Pesos"); ax.set_title("Reparto por mes y lugar"); ax.legend(frameon=False, fontsize=8)
plt.show()"""),

    md("""## 3. ¿Cuánto cuesta cada regla?
Se resuelve el modelo sin la regla y se compara. Además, el **precio sombra** (del LP con las $y$ fijas) dice cuántos
visitantes trae un peso más de holgura en esa regla."""),

    code("""display(pz.costo_de_reglas().round(2))
pz.precios_sombra(pz.resolver()).assign(por_cada_mil=lambda d: d.precio_sombra * 1000).round(4)"""),

    md("""## 4. Frontera de Pareto: visitantes contra espacio libre
$\\varepsilon$-restricción: ningún mes con anuncio puede pasar de $\\varepsilon$ veces su capacidad probada en el
escenario probable."""),

    code("""par = pz.pareto(); display(par)
fig, ax = plt.subplots(figsize=(7, 3.3))
ax.plot(par.ocupacion_max * 100, par.visitantes_esperados, marker="o", color=GUINDA)
ax.set_xlabel("Ocupación máxima permitida (%)"); ax.set_ylabel("Visitantes esperados"); plt.show()"""),

    md("""## 5. Sensibilidad: ¿qué pasa si los supuestos están mal?"""),

    code("""pz.sensibilidad().round(1)"""),

    md("""## 6. Qué se concluye
1. **Con $250,000 al año la campaña trae unos 957 visitantes** en los 9 meses con pronóstico (≈ $196 por visitante).
   Con conversión de Facebook de 3 %, 542; con la mediana de industrias, 1,052.
2. **Las reglas ambientales no cuestan visitantes a esta escala:** temporada alta, capacidad y equidad cuestan 0. La
   campaña es chica frente al espacio que hay. La única regla que cuesta es el tope por canal (−29.5 %), y es una
   decisión de riesgo (no depender de una sola plataforma), no de sustentabilidad.
3. **Se puede prometer más espacio sin perder visitantes:** ningún mes con anuncio pasa del 40 % de su capacidad
   probada, y los visitantes no cambian. Por debajo de 40 % la frontera cae (35 % → 537; 30 % → 0).
4. **El reparto no depende del supuesto de tormentas** (golpe 0/25/50 %): los meses con riesgo ya están fuera.
5. **Limitaciones declaradas:** costos de EE. UU.; conversión de Facebook supuesta; cada conversión cuenta como un
   visitante (cota alta); sin dato de cómo se agota la audiencia (por eso el desempate proporcional); el plan cubre
   oct-2026 a jun-2027 porque después no hay pronóstico."""),
]

nb = nbf.v4.new_notebook(cells=celdas, metadata={
    "kernelspec": {"name": "python3", "display_name": "Python 3 (.venv)", "language": "python"},
    "language_info": {"name": "python"}})
NotebookClient(nb, timeout=1800, kernel_name="python3", resources={"metadata": {"path": str(AQUI)}}).execute()
salida = AQUI / "05_optimizacion.ipynb"
nbf.write(nb, salida)
print(f"Notebook ejecutado y guardado: {salida}")
