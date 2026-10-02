# 20 — Fase 7: la Torre en vivo (la campaña, semana a semana)

Autor: **Brandon Uriel García Sánchez** · 02-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## La pregunta
¿Qué hace la campaña **esta semana**? La Torre vigila datos que cambian cada semana y ejecuta la etapa 2 que dejó prevista
la Fase 6: pausar un anuncio y mover su dinero. Responde a dos incidentes críticos:
- **Big Data:** una arquitectura de baja latencia para ajustar la campaña *durante* su ejecución.
- **Mercadotecnia:** qué hacer si la afluencia rebasa la capacidad.

## Decisiones de Brandon (02-oct-2026)
| Decisión | Elegida | Descartadas |
|---|---|---|
| Señales | **Las cuatro:** ocupación del norte (DataTur semanal), tormentas cerca (HURDAT2), clima raro (Isolation Forest) y llegadas mensuales del sur contra lo esperado | — |
| Regla del sur | **Pausar esa semana**; el dinero pasa a la siguiente semana permitida del mismo lugar | Bajar a la mitad (se anunciaría con mal clima); solo avisar |
| Regla del norte | **Encender "¿Ibas al norte?"** si Cancún o Riviera Maya están saturados (≥ 85.92 %, p90 del Radar), hacia el lugar del sur encendido con más espacio libre ese mes | Solo marcar |
| Página | **Reproducción grabada** (GitHub Pages es estático) | Además, transmisión en vivo con FastAPI en localhost |
| Corte del clima raro | **Más raro que el 95 %** de las semanas que el bosque ya conoce | Más raro que el 99 % (casi nunca pausa); quitar la señal |

**Por qué hubo que decidir el corte:**
- El corte automático del Isolation Forest (`contamination="auto"`) marcaba **47 % de las semanas de Chetumal**, e incluso
  13–26 % dentro de su propio entrenamiento. Con 156 semanas no distingue.
- Además, desde 2022 llueve más y hace más calor que en 2019–2021.
- Se pasó a una ventana creciente (cada año aprende de todos los anteriores) con corte en el percentil 95. Así quedan
  21 semanas raras en Chetumal (8.8 %) y 17 en Kohunlich (7.1 %).

## Cómo funciona (`backend/torre/envivo/`)
1. **`senales.py`:** una fila por semana (lunes), 239 semanas, del 3-ene-2022 al 27-jul-2026.
   - **Norte:** ocupación de Cancún y Riviera Maya con su estado. El promedio de 4 semanas sale de una ventana deslizante
     de Spark.
   - **Tormentas:** HURDAT2 con la regla de la Fase 5. **2026 no se ha publicado → sin dato** (30 semanas), que no es
     "sin tormenta".
   - **Clima raro:** Isolation Forest por punto (Chetumal para Chetumal y la Bahía; Kohunlich para la Ruta). Usa lluvia
     de la semana, lluvia del peor día, viento, calor y la época del año (seno y coseno).
   - **Llegadas:** el dato real del mes anterior contra el rango del 90 % del pronóstico a un mes del modelo elegido
     (backtest de la Fase 5). Se supone que se conoce al empezar el mes siguiente; en realidad tarda 1–2 meses.
2. **`motor.py`:** reglas puras, probadas una por una (`tests/test_envivo.py`).
   - Llegadas **por debajo** del rango no pausan: es espacio, justo lo que la campaña busca.
3. **`torre.py`:** escribe una semana por archivo JSON. **Spark Structured Streaming** los lee con
   `maxFilesPerTrigger = 1` (una semana por lote, `trigger(availableNow=True)`), y en cada lote el motor decide.
   - Resultado: **239 lotes, en orden**, comprobado.
   - Cambiar la carpeta por una fuente real no cambia el motor.
   - El dinero es el plan de la Fase 6 por mes del año ("si este plan hubiera corrido en 2022–2026"). Julio a septiembre
     no tienen plan, porque el pronóstico no llega: ahí la Torre vigila, pero no gasta.

## Resultados
| Lugar | Encendido | Pausado | Temporada alta | Fuera del plan |
|---|---:|---:|---:|---:|
| Chetumal | 145 | 19 | 18 | 57 |
| Bahía Calderitas–Oxtankah | 106 | 14 | 62 | 57 |
| Ruta arqueológica del sur | 104 | 15 | 63 | 57 |

- **48 pausas de lugar-semana** en total. Algunas tuvieron más de un motivo:
  - 44 con clima raro;
  - 9 con tormenta cerca: Lisa (oct-2022), Nadine (oct-2024) y Sara (nov-2024), que pausaron los tres lugares;
  - 5 porque llegó más gente de la esperada a Chetumal en mayo de 2025.
- **Validación independiente:** el Isolation Forest marcó como raras **las tres semanas de tormenta sin saber que hubo
  tormenta**.
- **No se pierde dinero:** los $876,901 planeados en las semanas con plan se gastaron todos; lo pausado se gastó en la
  siguiente semana permitida.
- **El norte casi nunca se satura en lo semanal:** Cancún 1 semana y Riviera Maya 9. "¿Ibas al norte?" se encendió
  **6 semanas**, todas hacia la Bahía. La señal fuerte del norte es la temporada (Fase 5), no la semana.

## Evidencia
- `tests/test_envivo.py` (9 pruebas):
  - 7 son reglas del motor con semanas armadas solo para la prueba, que no se muestran ni se guardan;
  - 2 son la reproducción real: completa, en orden, con dinero conservado, cortes 71.16/85.92, tormentas, 21/17 semanas
    raras, 14/19/15 pausas y 6 semanas al norte.
- `notebooks/06_torre_en_vivo.ipynb`.
- `docs/metodologia/ECUACIONES.md` §5.
- Página: sección "La campaña, semana a semana" en "Los datos".

## Consecuencia
La Fase 7 queda **lista**. La campaña (Fase 8) usa esto así:
- los anuncios del sur tienen reglas de pausa automáticas;
- el mensaje "¿Ibas al norte?" se reserva para semanas de norte saturado y temporada alta.

**Limitaciones:**
- el sur no tiene ningún dato semanal oficial;
- las tormentas de 2026 todavía no se conocen;
- se supone que el dato mensual se conoce un mes después;
- el plan de dinero se aplicó a años pasados.
