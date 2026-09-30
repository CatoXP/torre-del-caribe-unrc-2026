# Autor: Brandon Uriel García Sánchez
# Módulo: Pronóstico
# Qué hace:          Construye y ejecuta el notebook narrado notebooks/03_pronostico.ipynb (Fase 5): series y meses que no
#                    entrenan, forma del año, 5 modelos en origen móvil, rango del 90 % con su cobertura real, elección del
#                    modelo, pronóstico de 12 meses, Poisson de tormentas, Monte Carlo de escenarios y sensibilidad.
# Por qué así:       Igual que los notebooks 01 y 02: el texto se versiona como código y el notebook se ejecuta completo al
#                    construirse (si una celda falla, no se guarda). Corre toda la cadena de backend/torre/pronostico, así
#                    que ninguna cifra del notebook viene de una corrida vieja.
# Datos de entrada:  datos/silver/ y datos/gold/pronostico_series (a través de torre.pronostico).
# Alimenta a:        Criterios 3 (minería), 4 (ML) y 5 (estocásticos) de la rúbrica; capítulo 9 del documento ejecutivo.
#
# Uso:  .venv\Scripts\python notebooks\_construir_03_pronostico.py   (≈ 3 minutos)

from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

AQUI = Path(__file__).resolve().parent
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

celdas = [
    md("""# 03 · El Pronóstico: ¿cuándo conviene ir?
**Torre del Caribe** · Fase 5 (A3 Pronóstico) · Autor: **Brandon Uriel García Sánchez** · UNRC, LCDN 5° semestre 2026-2

| | |
|---|---|
| **Qué hace** | Pronostica de 1 a 12 meses los visitantes de los lugares del sur (y la ocupación de Cancún como referencia), con un rango del 90 % cuya cobertura se mide; calcula el riesgo de tormenta por mes y los escenarios malo / probable / bueno. |
| **Decisiones de Brandon** | Series medidas + norte como referencia · cierre, mes parcial y pandemia no entrenan (Belice hasta jun-2022) · menor error con rango ≥ 80 % · tormenta: probabilidad medida y golpe como supuesto con barrido · escenarios sin campaña · capacidad probada (`docs/decisiones/11-pronostico.md`). |
| **Código** | `backend/torre/pronostico/`: `series.py`, `forma.py`, `modelos.py`, `intervalos.py`, `seleccion.py`, `escenarios.py`. |
| **Ecuaciones** | `docs/metodologia/ECUACIONES.md` §3. |
| **Alimenta a** | Fase 6: en qué meses anunciar cada lugar, cuánto reservar para tormentas y en qué meses no empujar (riesgo de rebasar la capacidad probada). |"""),

    code("""%matplotlib inline
import sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
RAIZ = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(RAIZ / "backend"))

import numpy as np
import pandas as pd
from IPython.display import Image, display
from torre.pronostico import series, forma, modelos, intervalos, seleccion, escenarios
from torre.documento import figuras
pd.set_option("display.max_colwidth", 60)
pd.set_option("display.width", 200)"""),

    md("""## 1. Qué se pronostica y qué meses no entrenan
El sur no tiene ocupación hotelera oficial desde 2025, así que se pronostican **series medidas que llegan a 2026**:
visitantes INAH de la Bahía (Oxtankah) y de la Ruta (Kohunlich + Dzibanché + Ichkabal), cruces desde Belice por Chetumal
y, como **referencia**, la ocupación de Cancún (el público de la campaña).

Un mes cerrado no es "cero demanda": los meses de **cierre**, **mes parcial** y **pandemia** se marcan y no entrenan
(su valor se conserva)."""),

    code("""t = series.construir()
series.guardar(t)
series.resumen(t)"""),

    code("""# Ejemplo de las reglas: la Ruta alrededor de las obras de 2024 y la reapertura de 2025
r = t[(t.serie.str.startswith("Ruta")) & t.periodo.between("2023-12-01", "2025-03-01")]
r[["periodo", "valor", "zonas_abiertas", "motivo_hueco", "entrena_flag"]]"""),

    md("""## 2. Minería: la forma del año
Índice del mes = promedio, entre los **años completos**, de (valor del mes ÷ promedio de ese año). Multiplicativo porque
la temporada escala con el nivel. STL solo se usa como segunda opinión (necesita series sin huecos)."""),

    code("""fa, fu = forma.calcular(t)
forma.guardar(fa, fu)
fu[["serie", "anios_usados", "fuerza_estacional", "mes_mas_alto", "mes_mas_bajo", "corr_con_stl"]]"""),

    code("""# Ejemplo a mano: Ruta, enero de 2019 = 7,935 ÷ (64,139 / 12)
rz = forma.razones(t[t.serie.str.startswith("Ruta")])
print("razón ene-2019:", round(7935 / (64139 / 12), 4), "| código:", round(rz.loc[2019, 1], 4))
print("índice de enero (promedio de 6 años):", round(rz[1].mean(), 4))
print("¿El sur acompaña al norte?", forma.acompana_al_norte(fa).to_dict())
display(Image(filename=figuras.forma_del_anio()))"""),

    md("""## 3. Aprendizaje de máquina: 5 modelos con origen móvil
Se "regresa el reloj" a cada mes desde 2019, se pronostican los 12 siguientes solo con lo que se sabía entonces y se
compara con lo que pasó. Solo cuentan los pares que **los 5 modelos** pudieron pronosticar. "vs base" < 1 = mejor que
repetir el mismo mes del año anterior."""),

    code("""b, m = modelos.correr()   # ≈ 1.5 minutos
m[["serie", "modelo", "pronosticos", "mape", "mae_vs_base", "mape_h1–3", "mape_h4–6", "mape_h7–12"]].round(3)"""),

    code("""# Hallazgo: la tendencia aprendida en plena reapertura produjo visitantes negativos
b[b.pronostico <= 0][["serie", "modelo", "origen", "destino", "pronostico", "real"]].round(1)"""),

    md("""## 4. El rango del 90 % y su cobertura real
Conformal secuencial: el tamaño del rango de un pronóstico sale solo de los errores ya conocidos en su origen,
$\\hat q = e_{(\\lceil (n+1)\\,0.9\\rceil)}$, en escala logarítmica y por tramo de horizonte. Se reporta la cobertura aunque
salga peor que 90 %."""),

    code("""b, c = intervalos.correr()
c.round(1)"""),

    md("""## 5. El modelo elegido (criterio de Brandon) y el pronóstico de 12 meses
Por serie, el menor error entre los modelos cuyo rango del 90 % se cumple al menos 80 de cada 100 veces."""),

    code("""e, f = seleccion.correr()
e[e.elegido_flag][["serie", "modelo", "mae_vs_base", "mape", "cobertura_pct", "ancho_mediano_pct"]].round(3)"""),

    code("""# Ejemplo a mano del rango: Bahía, dic-2026 (horizonte 5, tramo 4–6)
import math
err = b[(b.serie.str.startswith("Bahía")) & (b.modelo == "Regresión con clima") & (b.tramo_h == "4–6")].error_log
n = len(err); k = math.ceil((n + 1) * 0.9); q = np.sort(err.to_numpy())[k - 1]
fila = f[(f.lugar == "Bahía Calderitas–Oxtankah") & (f.periodo == "2026-12-01")].iloc[0]
print(f"n = {n}, k = {k}, q = {q:.4f} → {fila.esperado_est:,.1f} × e^±q = {fila.esperado_est*np.exp(-q):,.0f} a {fila.esperado_est*np.exp(q):,.0f}")
display(Image(filename=figuras.pronostico_12_meses()))"""),

    md("""## 6. Estocástico: tormentas, escenarios y sensibilidad
- **Poisson:** $P(N_m\\ge1)=1-e^{-\\hat\\lambda_m}$ con los 31 eventos de 1966–2025.
- **Monte Carlo:** 10,000 futuros = pronóstico × un año completo de errores reales × tormentas sorteadas; el golpe de una
  tormenta es un **supuesto** (0 / 25 / 50 %) porque no se pudo medir.
- **Capacidad probada:** el mes más alto que cada lugar ya recibió."""),

    code("""p, meses, anual, sens = escenarios.correr()
p.assign(prob_tormenta=lambda x: (x.prob_tormenta * 100).round(1))[["mes", "eventos", "lambda", "prob_tormenta"]]"""),

    code("""anual.round(0)"""),

    code("""x = meses[(meses.golpe_tormenta_supuesto == 0) & (meses.riesgo_rebasar_capacidad > 0.05)]
print("Meses con riesgo de rebasar la capacidad probada:")
display(x[["lugar", "periodo", "probable_p50_est", "capacidad_probada", "riesgo_rebasar_capacidad"]].round(3))
display(Image(filename=figuras.escenarios_12_meses()))"""),

    code("""sens[["lugar", "variable", "efecto_pct", "p_valor", "meses", "significativo_flag"]].round(3)"""),

    md("""## 7. Qué se concluye
1. **La temporada manda:** las zonas del sur se llenan en diciembre–enero y se vacían en septiembre, y se mueven con el
   norte; los cruces desde Belice van por su cuenta.
2. **Un modelo simple y bien planteado le gana a los complejos:** la regresión con nivel por tramo + mes se equivoca
   entre 10 % y 26 % menos que la línea base en el sur; Holt-Winters con tendencia llegó a pronosticar visitantes
   negativos y Gradient Boosting, con tan pocos datos, perdió contra la base en la Bahía y la Ruta.
3. **El rango del 90 % se cumple** 91 % (Bahía) y 94 % (Belice) de las veces; en la Ruta, 80 % (falla en 2023). Se
   reporta como salió.
4. **Las tormentas pesan en el mes, no en el año;** el riesgo de rebasar la capacidad probada está en diciembre y enero.
5. **Limitaciones declaradas:** el efecto de las tormentas es un supuesto (solo 3 meses con tormenta en los datos
   usables); el clima futuro se toma como normal; la capacidad probada no es la capacidad física oficial; Maya Ka'an y
   la Laguna Milagros no tienen serie propia; los escenarios no incluyen la campaña (Fase 6)."""),
]

nb = nbf.v4.new_notebook(cells=celdas, metadata={
    "kernelspec": {"name": "python3", "display_name": "Python 3 (.venv)", "language": "python"},
    "language_info": {"name": "python"}})
NotebookClient(nb, timeout=1800, kernel_name="python3", resources={"metadata": {"path": str(AQUI)}}).execute()
salida = AQUI / "03_pronostico.ipynb"
nbf.write(nb, salida)
print(f"Notebook ejecutado y guardado: {salida}")
