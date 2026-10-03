# 19 — Fase 6: reparto del presupuesto (Investigación de Operaciones)

Autor: **Brandon Uriel García Sánchez** · 02-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## La pregunta
¿Cuánto dinero de la campaña va a cada lugar del sur, en qué mes y por qué canal, para traer el máximo de visitantes sin
anunciar donde ya está lleno y sin rebasar la capacidad de nadie? Responde al incidente crítico de Investigación de
Operaciones: qué es "óptimo", qué priorizar si los objetivos chocan, qué restricciones son indispensables y qué pasa si
se cambian.

## Decisiones de Brandon (02-oct-2026)
| Decisión | Elegida | Descartadas y por qué |
|---|---|---|
| Objetivo | **Visitantes (conversiones) esperados hacia los 3 lugares del sur** | Derrama económica: la de SITUR-Q no trae unidad y termina en mar-2024, así que habría que suponer el gasto por persona. Visitantes con castigo por presión: obliga a elegir el peso del castigo. |
| Presupuesto | **$250,000 MXN al año** (supuesto; no hay presupuesto real) | Barrido de 3 montos; rendimiento por cada $10,000. |
| Conversión de Facebook (no publicada para turismo) | **Barrido: 3 % / 5.75 % (Google Travel, caso base) / 6.38 % (mediana de Facebook en todas las industrias)** | Usar Facebook solo para alcance; una sola tasa supuesta. |
| Restricciones | **Las cuatro:** cero anuncio en temporada alta · tope de capacidad probada · piso de equidad de 15 % por lugar · tope de 70 % por canal | — |
| Desempate (con el mismo máximo de visitantes) | **Proporcional al espacio libre** de cada mes | Tope de 25 % por mes (regla nueva); dejarlo concentrado (el óptimo puro mandaba todo el dinero de cada lugar a un solo mes). |

## El modelo (`backend/torre/campana/presupuesto.py`, ecuaciones en `ECUACIONES.md` §4)
**Programación estocástica de dos etapas**, resuelta con PuLP/CBC (simplex + *branch-and-bound*):
- **Etapa 1 (hoy):** $x_{m,l,c}$ = pesos por mes, lugar y canal.
  - Cada canal convierte $r_c=\text{conversión}_c/\text{costo por clic}_c$.
  - Google: $0.0575 / (2.12 \times 17.06) = 1.59$ visitantes por cada $1,000.
  - Facebook: $0.0575 / (0.51 \times 17.06) = 6.61$ por cada $1,000.
- **Etapa 2 (recurso):** en cada escenario del Monte Carlo (malo p10, probable p50, bueno p90; pesos 30/40/30, regla de
  Swanson), $y\in\{0,1\}$ pausa el anuncio si el escenario más la campaña rebasa la capacidad probada. Las conversiones de
  un mes pausado se pierden.
- **Meses:** oct-2026 a jun-2027, los 9 que tienen calendario y escenarios para los 3 lugares. Después no hay pronóstico,
  así que no se extrapola. El presupuesto se prorratea: $250,000 × 9/12 = **$187,500**.
- **Supuesto declarado:** cada conversión cuenta como un visitante más. Es una cota alta, que protege la capacidad.

## Resultados
- **957 visitantes esperados** con $187,500, unos **$196 por visitante**.
  - **Reparto por lugar:** Ruta 41.5 % ($77,790), Bahía 36.9 % ($69,175) y Chetumal 21.6 % ($40,535).
  - **Por canal:** 70 % Facebook y 30 % Google en cada mes.
- **Meses sin anuncio:**
  - diciembre en los tres lugares;
  - enero en la Ruta y la Bahía, marzo en la Ruta y abril en la Bahía.
  - Son todos de temporada alta: 20 de 27 combinaciones de mes y lugar quedan permitidas.
- **Costo de cada regla** (se resuelve sin ella y se compara):

  | Regla | Visitantes que cuesta |
  |---|---:|
  | Cero anuncio en temporada alta | 0 |
  | Tope de capacidad probada | 0 |
  | Piso de equidad de 15 % | 0 |
  | Tope de 70 % por canal | 282 (29.5 %) |

  A este presupuesto **las reglas ambientales y de equidad no cuestan nada**: la campaña es chica frente al espacio
  disponible. El tope por canal sí cuesta, y se mantiene por riesgo, para no depender de una sola plataforma.
- **Precios sombra** (LP con las $y$ fijas):
  - **Presupuesto:** un peso más trae 0.00159 visitantes, o sea 1.59 por cada $1,000, porque el peso extra va a Google.
  - **Tope de Facebook:** cada $1,000 que se le permiten a Facebook trae 5.02 visitantes más.
- **Frontera de Pareto** ($\varepsilon$-restricción sobre la ocupación del escenario probable):
  - Hasta **40 %** de la capacidad probada no se pierde ningún visitante. Ahí Chetumal y la Bahía se quedan sin meses y su
    piso de equidad deja de aplicar.
  - Con tope de 35 % llegan 537 y con 30 %, ninguno.
- **Sensibilidad:**

  | Caso | Visitantes |
  |---|---:|
  | Conversión de Facebook de 3 % | 542 |
  | Mediana de industrias | 1,052 |
  | Clic de Facebook a $0.42 (LocaliQ) | 1,143 |
  | Golpe de tormenta de 25 % o 50 % | sin cambio (los meses con riesgo ya están fuera) |
  | $500,000 al año | 1,914 |
  | $1,000,000 al año | 3,827 |

  El reparto por lugar y por canal casi no cambia en ningún caso.

## Hallazgo que conecta con la Fase 2
El aeropuerto de Chetumal recibió solo 250 extranjeros en 2025 (nota 18). El anuncio para el viajero extranjero tiene
que alcanzarlo antes del viaje o cuando ya está en Cancún. La segmentación por mercado y ciudad de origen se decide en la
Fase 8 (campaña), con el buyer persona.

## Evidencia
- **Pruebas:** `tests/test_presupuesto.py` (5):
  - el ejemplo a mano de 956.8;
  - cada regla comprobada sobre la solución;
  - el reparto proporcional exacto (desvío 0);
  - el costo de las reglas y el precio sombra del presupuesto;
  - que la frontera de Pareto no baje al aflojar el tope.
- **Notebook:** `notebooks/05_optimizacion.ipynb`.
- **Gráficas:** `docs/ejecutivo/figuras/f13_reparto_presupuesto.png` y `f14_frontera_pareto.png`.
- **Página:** sección "¿Cuánto dinero, dónde y cuándo?" en "Los datos".

## Consecuencia
La Fase 6 queda **lista**. El plan mensual (etapa 1) pasa a la Fase 7, la Torre en vivo, que vigila cada semana y
ejecuta la etapa 2: pausar un anuncio si un lugar se llena. También pasa a la Fase 8, que pone el mensaje y el público
de cada anuncio.

**Limitaciones:**
- los costos son promedios de anunciantes de Estados Unidos;
- la conversión de Facebook es un supuesto;
- no hay dato de cómo se agota la audiencia, y por eso se desempata en proporción al espacio;
- el plan cubre 9 meses.
