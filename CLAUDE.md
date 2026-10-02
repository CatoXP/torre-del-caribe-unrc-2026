# CLAUDE.md — Reglas del repositorio "Torre del Caribe"

Autor del proyecto: **Brandon Uriel García Sánchez** (UNRC · LCDN 5° semestre 2026-2).
Antes de hacer cualquier cosa, lee **`OBJETIVO.md`** (prompts literales, Problema Prototípico, rúbrica,
incidentes y protocolo) y **`docs/plan/PLAN_v3.md`** (plan aprobado).

## 1. Reglas de oro (no negociables)
1. **No inventar datos.** Si una serie no existe, no se genera, no se simula "para probar" y no se rellena con
   promedios. Un hueco se declara como hueco y se detiene el paso.
2. **Toda cifra es rastreable:** archivo crudo → función → salida. Si no se puede rastrear, no se muestra.
3. **Estimado ≠ medido.** Lo estimado lleva sufijo `_est`, su método y su error de validación.
4. **Sin scraping prohibido** por términos de uso (TripAdvisor, Google Maps). Solo fuentes de
   `docs/datos/INVENTARIO.md`.
5. **Si a media fase falta un dato, se detiene y se avisa.** No se improvisa.
6. **Desde cero:** nada del proyecto anterior (código `cauce`, modelos, salidas, personas, gemelo, semáforo,
   malla precalculada, priores Beta, cifras). La carpeta `nucleo/` es solo referencia histórica.
7. **Ecuaciones y "cómo lo resolví"** (proyecto escolar): cada modelo o cálculo documenta su ecuación en LaTeX,
   sus supuestos, el método de resolución paso a paso, un ejemplo resuelto a mano con números reales y dónde está en
   el código. Todo va en `docs/metodologia/ECUACIONES.md` y en el notebook de la fase.
8. **Documento ejecutivo para el equipo** (`docs/ejecutivo/DOCUMENTO_EJECUTIVO.md` → PDF `Documento_Ejecutivo_Torre_del_Caribe.pdf`, generado con `python -m torre.documento.pdf`): al cerrar cada
   fase se agrega su capítulo en lenguaje **no técnico**, para alguien nuevo. Explica qué hace cada proceso del código y
   por qué, con datos reales, gráficas y capturas. Se redacta **en tono de informe, en tercera persona**: nunca "ya
   decidimos...", "como te dije..." ni ninguna otra conversación entre IA y humano. Estilo UNRC obligatorio
   (`docs/ejecutivo/GUIA_ESTILO_UNRC.md`). Lo usa otra integrante del equipo para redactar el entregable en limpio.
9. **Solo 5 regiones** (instrucción de Brandon, 28-sep-2026): Chetumal · Bahía Calderitas–Oxtankah · Ruta
   arqueológica del sur (Kohunlich, Dzibanché, Ichkabal) · Maya Ka'an + Kantemó · Laguna Milagros–Xul-Ha. Nada con
   sargazo, cierres o saturación (Tulum, Cancún, Riviera Maya, Cozumel, Isla Mujeres, Holbox, Mahahual, Bacalar, Cobá,
   Muyil) se promueve ni aparece en la portada o en las piezas. Cancún, Riviera Maya y Tulum se usan **solo como
   referencia etiquetada**. **Excepción (Brandon, 01-oct-2026, decisión 15):** Cancún y Riviera Maya aparecen en el planeador bajo "¿Ibas al norte?" con la etiqueta "Referencia: la campaña no lo promueve"; si su mes está lleno, el planeador recomienda un lugar del sur (nunca el norte) con un aviso visible. Antes de mostrar un dato, preguntarse: ¿es de una de las 5 regiones? Si no, ¿es una
   referencia explícita? Si ninguna, no va.
10. **Sistema visual vigente: "Sur mexicano"** (`docs/decisiones/07-diseno.md`, rediseño con Claude Design del 28-sep-2026):
   colores mexicanos en bloques, Bricolage Grotesque + Figtree locales, greca maya, fotos grandes y poco texto.
   `docs/DESIGN.md` (Flighty) queda como referencia histórica.

## 2. Protocolo de trabajo con Brandon (anti-caja negra, sin "vibecodear")
1. Explicar qué se hará y por qué, **con la cifra real** que lo motiva.
2. Si hay decisión real: 2 o 3 opciones con pros y contras → **Brandon elige**.
3. Programar **piezas pequeñas** (una función o un notebook corto) comentadas en español.
4. **Brandon las corre**; se revisa el resultado juntos.
5. Cada decisión queda en `docs/decisiones/NN-nombre.md`: decisión · opciones descartadas · evidencia
   (cifra + archivo + función) · consecuencia. Escrita para que cualquier integrante la defienda en el coloquio.
6. **Una fase a la vez** (fases 0–11 del plan). No se abre la siguiente sin su visto bueno.

## 3. Reglas de estructura
```
OBJETIVO.md            ancla del proyecto (no se borra; solo se agregan decisiones)
CLAUDE.md              estas reglas
README.md              qué es, por qué y cómo correrlo
datos/bronze/          crudo, inmutable, con manifiesto SHA-256 (no va a git)
datos/silver/          limpio y tipado, Parquet particionado (no va a git)
datos/gold/            modelo estrella y salidas de modelos (no va a git)
backend/torre/         paquete Python: base · radar · pronostico · envivo · campana · api
frontend/              HTML + CSS + JS sin framework, sistema visual "Sur mexicano" (docs/decisiones/07-diseno.md), todo local
notebooks/             uno por UCA, narrados; llaman funciones del paquete
docs/plan/             plan aprobado
docs/datos/            inventario de fuentes y diccionario de datos
docs/regiones/         selección de regiones con evidencia
docs/metodologia/      ecuaciones y cómo se resolvió cada modelo
docs/ejecutivo/        documento ejecutivo no técnico (estilo UNRC) + gráficas y capturas
docs/decisiones/       una nota por decisión (ADR ligero)
docs/aportes/          fotos y reseñas propias del equipo (con permiso); ver LEEME.md
docs/idiomas/          traducciones fuente (.tsv) de la parte del viajero; se arman con torre.campana.idiomas
tests/                 pytest: contrato (forma) + realidad (cifra conocida)
```

## 4. Convenciones de código
- Python 3.11, dependencias fijadas en `requirements.txt`. PySpark 3.5.6 + JDK 17 + winutils 3.3.6.
- Nombres de columnas en **snake_case y en español**; `_est` para lo estimado, `_flag` para banderas.
- Comentarios en español. Encabezado obligatorio en cada archivo:
  ```python
  # Autor: Brandon Uriel García Sánchez
  # Módulo: (Radar | Pronóstico | Torre en vivo | Campaña | Base de datos)
  # Qué hace:          ...
  # Por qué así:       ... (decisión + alternativa descartada + evidencia)
  # Datos de entrada:  ... (fuente oficial + archivo)
  # Alimenta a:        ... (qué decisión de la campaña)
  ```
- Cada módulo declara **a qué decisión de campaña alimenta**; si no puede nombrarla, no se escribe.
- Front-end: sin llamadas a hosts externos; funciona en `localhost` sin internet. Lenguaje para público no
  técnico ("tranquilo / concurrido / saturado", "escenario malo / probable / bueno").

## 5. Los tres módulos (no se enciman)
| Módulo | Pregunta | Horizonte |
|---|---|---|
| A1 Radar | ¿Dónde hay presión y dónde hay espacio? | hoy (semanas) |
| A3 Pronóstico | ¿Cuándo conviene ir y cuánto invertir? | 1–12 meses |
| A5 Torre en vivo | ¿Qué hace la campaña esta semana? | semana a semana |

## 6. Mapa del proyecto (Graphify)
**Antes de hacer Glob o Grep, lee primero `graphify-out/GRAPH_REPORT.md`.** El grafo conecta reglas,
fuentes de datos, módulos, regiones y rúbrica. Se reconstruye con los hooks de git; si cambian documentos,
se vuelve a correr `/graphify .`.

**⚠️ En este proyecto NO se corre `graphify update .` a mano** (aunque la sección de abajo, escrita por Graphify, lo
sugiera). Verificado el 27-sep-2026: ese comando reprocesa **todos** los documentos con un extractor simple y
degradó el grafo de 476 a 292 y a 368 nodos. En su lugar:
- **Si cambian documentos:** `/graphify . --update` (re-extracción semántica solo de lo que cambió, con caché).
- **Si solo cambia código:** basta el hook `post-commit`, que es seguro porque solo toca los archivos del commit
  (probado: 476 → 479 nodos). El hook renombra las comunidades de forma automática; si hace falta, se re-etiquetan.
- **Después de cualquier reconstrucción:** borrar `graphify-out/obsidian/`, correr
  `graphify export obsidian --labels graphify-out/.graphify_labels.json` y regenerar los colores y la nota
  "00 Mapa del proyecto".

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
