# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña
# Qué hace:          Construye y ejecuta el notebook narrado notebooks/07_campana.ipynb (Fase 8): minería de 85,987
#                    reseñas, buyer persona con el origen de cada rasgo, marca, mensajes con respaldo, medios y KPI.
# Por qué así:       Igual que los notebooks 01–06: el texto se versiona como código y se ejecuta completo al construirse.
# Datos de entrada:  datos/silver/restmex, inah, nacionalidad; datos/gold (Fases 5–7) a través de torre.campana.
# Alimenta a:        Criterios 3 (minería) y 7 (mercadotecnia) de la rúbrica; capítulo 12 del documento ejecutivo.
#
# Uso:  .venv\Scripts\python notebooks\_construir_07_campana.py

from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

AQUI = Path(__file__).resolve().parent
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

celdas = [
    md("""# 07 · La campaña: "El sur tiene espacio"
**Torre del Caribe** · Fase 8 (Mercadotecnia digital) · Autor: **Brandon Uriel García Sánchez** · UNRC, LCDN 5° semestre 2026-2

| | |
|---|---|
| **Qué hace** | Convierte los datos en una campaña: qué molesta y qué enamora en las reseñas, a quién se le habla, con qué palabras, en qué canal, cuándo y cómo se mide. |
| **Decisiones de Brandon** | Dos personas (la que vuelve al sur; la que baja del norte) · nombre "El sur tiene espacio" · tono que combina calma, orgullo cultural y aventura (`docs/decisiones/21-campana.md`). |
| **Código** | `backend/torre/campana/texto.py` (minería) y `marca.py` (campaña). |
| **Ecuaciones** | `docs/metodologia/ECUACIONES.md` §6.0. |"""),

    code("""import sys, json, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
RAIZ = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(RAIZ / "backend"))
import pandas as pd
from torre.campana import texto as tx, marca as mk
pd.set_option("display.max_colwidth", 120)"""),

    md("""## 1. Temas de las reseñas y su riesgo
Léxico a la vista (`tx.ASPECTOS`). Riesgo relativo $RR_a=\\dfrac{P(\\text{mala}\\mid a)}{P(\\text{mala})}$: más de 1, el tema
aleja; menos de 1, protege."""),

    code("""r = tx.marcar_aspectos(tx.leer())
print(f"{len(r):,} reseñas · malas {r.mala.mean():.2%} · de 5 estrellas {r.cinco.mean():.2%}")
a = tx.aspectos(r)
a[a.pueblo == "Quintana Roo (3 pueblos)"].sort_values("riesgo_relativo", ascending=False).round(2)"""),

    md("""## 2. Reglas de asociación (Apriori)
Transacciones = temas mencionados + la calificación. soporte $=\\#\\{A\\cup B\\}/N$, confianza $=sop(A\\cup B)/sop(A)$,
lift $=conf/sop(B)$."""),

    code("""reg = tx.reglas_asociacion(r)
display(reg[reg.entonces.str.contains("mala")].head(8).round(4))
reg[reg.entonces == "reseña de 5"].head(6).round(4)"""),

    md("""## 3. El lenguaje del turista (log-odds con prior de Dirichlet informativo)"""),

    code("""p = tx.palabras_que_distinguen(r)
p.groupby("lado").palabra.apply(lambda x: ", ".join(x))"""),

    md("""## 4. Las dos viajeras ideales
Cada rasgo dice si es **dato**, **derivado**, **supuesto** o **hueco**."""),

    code("""c = json.loads((RAIZ / "datos" / "gold" / "campana.json").read_text(encoding="utf-8"))
for persona in c["personas"]:
    print("\\n" + persona["nombre"].upper(), "—", persona["quien"])
    display(pd.DataFrame(persona["atributos"], columns=["rasgo", "valor", "tipo", "fuente"]))"""),

    md("""## 5. Marca, mensajes, medios, calendario y KPI"""),

    code("""print(json.dumps(c["marca"], ensure_ascii=False, indent=1))
print("Revisión de largos de anuncios:", mk.revisar_largos(c["mensajes"]) or "todo dentro de los límites")
display(pd.DataFrame(c["mensajes"])[["persona", "canal", "idioma", "respaldo"]])
display(pd.DataFrame(c["medios"]))
display(pd.DataFrame(c["calendario"]))
pd.DataFrame(c["kpis"])"""),

    md("""## 6. Qué se concluye
1. **Lo que hunde una reseña es lo que sobra en los destinos llenos:** ruido (2.76×), suciedad (1.89×), precio (1.66×) y
   multitudes (1.52×). Lo que la protege es lo que el sur ofrece: calma (0.41×) y cultura (0.48×).
2. **Dos viajeras, dos caminos:** la nacional ya es el 95 % de la Bahía; la extranjera está en Cancún (9.4 millones en
   2025) y casi no llega al sur por avión (250 en Chetumal). Por eso hay un mensaje para volver y otro para bajar.
3. **Ningún anuncio promete lo que no está medido:** sin precios ni horas de viaje; "con espacio" se apoya en 15.5 veces
   menos visitantes que Tulum.
4. **Limitaciones:** Rest-Mex no cubre los cinco lugares; muchas reseñas son traducciones; no hay dato del estado de
   origen del visitante nacional ni de edad o ingreso; los canales y conversiones son promedios de EE. UU."""),
]

nb = nbf.v4.new_notebook(cells=celdas, metadata={
    "kernelspec": {"name": "python3", "display_name": "Python 3 (.venv)", "language": "python"},
    "language_info": {"name": "python"}})
NotebookClient(nb, timeout=1800, kernel_name="python3", resources={"metadata": {"path": str(AQUI)}}).execute()
salida = AQUI / "07_campana.ipynb"
nbf.write(nb, salida)
print(f"Notebook ejecutado y guardado: {salida}")
