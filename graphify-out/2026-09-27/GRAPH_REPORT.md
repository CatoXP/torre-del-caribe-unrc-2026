# Graph Report - PP 5to semestre CASCO SANTO TOMAS  (2026-09-27)

## Corpus Check
- 13 files · ~27,830 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 375 nodes · 848 edges · 20 communities
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 124 edges (avg confidence: 0.86)
- Token cost: 208,276 input · 0 output

## Community Hubs (Navigation)
- Regiones y evidencia INAH
- Sistema de diseño Flighty
- Reglas y estructura del repo
- Fuentes de datos y huecos
- Incidentes estocástico y marketing
- A3 Pronóstico y ecuaciones
- Campaña y minería de texto
- Minería y buyer persona
- IO dos etapas y Pareto
- Problema prototípico base
- Incidente Big Data (NIST)
- Entregables oficiales
- Front-end y secciones
- A5 Torre en vivo
- Fusión e integración
- Criterios de la rúbrica
- Incidente IO y escenarios
- Incidente ML y referencias
- Backend FastAPI
- Preguntas secundarias e impacto

## God Nodes (most connected - your core abstractions)
1. `Flighty — Style Reference (sistema de diseño)` - 50 edges
2. `A3 Pronóstico` - 29 edges
3. `01 — Regiones que promueve la campaña` - 28 edges
4. `A1 Radar` - 28 edges
5. `Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan` - 24 edges
6. `Problema Prototípico: Turismo inteligente sustentable para México` - 21 edges
7. `Incidente crítico Aprendizaje de Máquina: Turismo inteligente sustentable en México` - 20 edges
8. `A5 Torre en vivo` - 20 edges
9. `Selección final D.5 (8 destinos + 2 emisoras)` - 18 edges
10. `Incidente crítico Mercadotecnia Digital: Estrategias digitales para la redistribución del turismo` - 17 edges

## Surprising Connections (you probably didn't know these)
- `Floating Notification Card` --semantically_similar_to--> `Integración de datos en tiempo real para ajustar la campaña (baja latencia)`  [AMBIGUOUS] [semantically similar]
  docs/DESIGN.md → PROBLEMA PROTOTÍPICO 5°- LCDN-2026-2.pdf
- `Flighty — Style Reference (sistema de diseño)` --conceptually_related_to--> `Desarrollo del branding de la marca`  [INFERRED]
  docs/DESIGN.md → PROBLEMA PROTOTÍPICO 5°- LCDN-2026-2.pdf
- `Regiones emisoras o de referencia: Cancún y Riviera Maya` --conceptually_related_to--> `Buyer persona`  [INFERRED]
  docs/plan/PLAN_v3.md → PROBLEMA PROTOTÍPICO 5°- LCDN-2026-2.pdf
- `A1 Radar` --semantically_similar_to--> `A1 Radar`  [INFERRED] [semantically similar]
  CLAUDE.md → docs/plan/PLAN_v3.md
- `Decisión: regiones finales (8 destinos + 2 emisoras)` --semantically_similar_to--> `Selección final D.5 (8 destinos + 2 emisoras)`  [INFERRED] [semantically similar]
  OBJETIVO.md → docs/regiones/REGIONES.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cadena de integración de las seis UCA en la campaña publicitaria inteligente** — problema_prototípico_5_lcdn_2026_2_evidencia_integradora, problema_prototípico_5_lcdn_2026_2_incidente_big_data, problema_prototípico_5_lcdn_2026_2_incidente_mineria_datos, problema_prototípico_5_lcdn_2026_2_incidente_aprendizaje_maquina, problema_prototípico_5_lcdn_2026_2_incidente_estocasticos, problema_prototípico_5_lcdn_2026_2_incidente_investigacion_operaciones, problema_prototípico_5_lcdn_2026_2_incidente_mercadotecnia_digital, problema_prototípico_5_lcdn_2026_2_campana_publicitaria_inteligente [EXTRACTED 1.00]
- **Evidencia para no promover playa en 2026** — docs_decisiones_00_fundacion_sargazo_2026, docs_decisiones_00_fundacion_crisis_tulum, docs_decisiones_00_fundacion_destinos_saturados, docs_decisiones_00_fundacion_decision_no_playa, objetivo_regiones_propuestas [EXTRACTED 1.00]
- **Colores de señal y componentes que los usan (acción, conversión, alerta)** — docs_design_signal_light_color_system, docs_design_color_signal_blue, docs_design_color_amber_alert, docs_design_color_alert_red, docs_design_primary_blue_button, docs_design_amber_download_button, docs_design_floating_notification_card [EXTRACTED 1.00]
- **Fusión de tres horizontes A1 Radar + A3 Pronóstico + A5 Torre en vivo** — claude_modulo_a1_radar, docs_plan_plan_v3_a3_pronostico, docs_plan_plan_v3_a5_torre_en_vivo, objetivo_alternativa_fusion_a1_a3_a5 [EXTRACTED 1.00]
- **Regiones excluidas como destino a promover** — docs_regiones_regiones_tulum, docs_regiones_regiones_playa_del_carmen_puerto_morelos, docs_regiones_regiones_mahahual_xcalak, docs_regiones_regiones_cozumel, docs_regiones_regiones_isla_mujeres, docs_regiones_regiones_holbox, docs_regiones_regiones_cancun_costa_mujeres, docs_regiones_regiones_bacalar [EXTRACTED 1.00]
- **Las 5 regiones propuestas de la ruta sur–Maya Ka'an** — docs_regiones_regiones_chetumal, docs_regiones_regiones_bahia_chetumal_calderitas_oxtankah, docs_regiones_regiones_ruta_arqueologica_sur, docs_regiones_regiones_maya_kaan_interior, docs_regiones_regiones_muyil_sian_kaan, docs_regiones_regiones_ruta_sur_maya_kaan [EXTRACTED 1.00]
- **Modo oscuro 'sala de control' de Flighty** — docs_design_light_to_dark_transition, docs_design_color_deep_indigo, docs_design_color_midnight_ink, docs_design_press_logo_card, docs_design_dark_ghost_button, docs_design_section_divider_band, docs_design_gradient_system [INFERRED 0.85]
- **Ocho destinos que promueve la campaña** — docs_regiones_regiones_chetumal, docs_regiones_regiones_bahia_chetumal_calderitas_oxtankah, docs_regiones_regiones_ruta_arqueologica_sur, docs_regiones_regiones_maya_kaan_interior, docs_regiones_regiones_kantemo_jose_maria_morelos, docs_plan_plan_v3_coba_punta_laguna, docs_regiones_regiones_muyil_sian_kaan, docs_plan_plan_v3_laguna_milagros_xul_ha, docs_regiones_regiones_ribera_del_rio_hondo [EXTRACTED 1.00]
- **Emisoras Cancún y Riviera Maya dirigen al turista a la ruta sur–Maya Ka'an** — docs_regiones_regiones_cancun_costa_mujeres, docs_regiones_regiones_riviera_maya, docs_regiones_regiones_regiones_emisoras, docs_regiones_regiones_ruta_sur_maya_kaan [EXTRACTED 1.00]
- **Fusión de módulos A1 Radar + A3 Pronóstico + A5 Torre en vivo** — claude_modulo_a1_radar, docs_plan_plan_v3_a3_pronostico, docs_plan_plan_v3_a5_torre_en_vivo, objetivo_alternativa_fusion_a1_a3_a5 [EXTRACTED 1.00]
- **Estafeta A3 → A1 → A5 → Campaña** — docs_plan_plan_v3_a3_pronostico, docs_plan_plan_v3_a1_radar, docs_plan_plan_v3_a5_torre_en_vivo, docs_plan_plan_v3_campana, docs_plan_plan_v3_programacion_estocastica_dos_etapas [EXTRACTED 1.00]
- **Selección de regiones con visitantes INAH** — docs_metodologia_ecuaciones_visitantes_anuales, docs_metodologia_ecuaciones_variacion_interanual, docs_metodologia_ecuaciones_capacidad_probada_sin_usar, docs_metodologia_ecuaciones_proporcion_extranjeros, docs_plan_plan_v3_evidencia_inah, docs_plan_plan_v3_seleccion_final_regiones [EXTRACTED 1.00]
- **Incertidumbre → escenarios → optimización → pausa** — docs_metodologia_ecuaciones_poisson_huracanes, docs_metodologia_ecuaciones_monte_carlo, docs_metodologia_ecuaciones_equivalente_determinista, docs_metodologia_ecuaciones_modelo_dos_etapas, docs_metodologia_ecuaciones_regla_pausa [INFERRED 0.85]

## Communities (20 total, 0 thin omitted)

### Community 0 - "Regiones y evidencia INAH"
Cohesion: 0.09
Nodes (55): D3 DataTur BD_Nacionalidad (~521,364 filas), D4 DataTur BdINAH / DB_AFAC / BaseDatosCruceros / Compendio 2024, Tren Maya, movimiento de pasajeros, 01 — Regiones que promueve la campaña, Riesgos que se vigilan (regiones), Tope estricto en el modelo de IO, Capacidad probada sin usar K_s, Proporción de extranjeros E_{s,a} (+47 more)

### Community 1 - "Sistema de diseño Flighty"
Cohesion: 0.11
Nodes (51): Agent Prompt Guide (prompts de componentes), Amber Download Button, Announcement Bar, Award Badge Pair, Sistema de radios (pill 999px, cards 16px, floating cards 20px), Apple Product Pages, Arc Browser, Linear (+43 more)

### Community 2 - "Reglas y estructura del repo"
Cohesion: 0.07
Nodes (47): Capas de datos bronze / silver / gold, Convenciones de código, Encabezado obligatorio de archivo de código, Mapa del proyecto (Graphify), A1 Radar, Protocolo de trabajo con Brandon (anti-caja negra), Regla 7: Ecuaciones y "cómo lo resolví", Reglas de oro (no negociables) (+39 more)

### Community 3 - "Fuentes de datos y huecos"
Cohesion: 0.10
Nodes (39): D1 SITUR-Q API (45 indicadores), D2 DataTur ocupación semanal (135 semanas, 7 centros Q. Roo), D2m DataTur ocupación mensual (31 meses, 54 centros), D6 DENUE INEGI (32 estados), D7 Censo 2020 ITER Q. Roo, Fuentes excluidas por no confirmarse (EVI, ENGATUR, OSM/Overpass, sargazo, Google Trends, TripAdvisor/Google), Hueco: afluencia de turistas / derrama del sur, Hueco: ocupación oficial del sur 2025–2026 (+31 more)

### Community 4 - "Incidentes estocástico y marketing"
Cohesion: 0.13
Nodes (18): Análisis de sensibilidad de variables (precio transporte, clima, tipo de cambio, sentimiento en redes), Asignación y optimización del presupuesto de la campaña, Incidente crítico Modelos Estocásticos: Incertidumbre en la demanda turística, Incidente crítico Mercadotecnia Digital: Estrategias digitales para la redistribución del turismo, Intervalo de confianza (90%) de la demanda esperada, Modelo de optimización para asignar presupuesto entre destinos, temporadas y canales sin rebasar capacidad de carga, ¿Qué acciones implementar si la campaña genera una afluencia mayor a la capacidad del destino?, ¿Promocionar varios destinos simultáneamente o concentrar recursos en uno solo bajo incertidumbre? (+10 more)

### Community 5 - "A3 Pronóstico y ecuaciones"
Cohesion: 0.27
Nodes (15): D10 FRED (DEXMXUS peso-dólar, CPIAUCSL), D9 HURDAT2 NOAA (1851–2025), Equivalente determinista resuelto con PuLP/CBC (simplex + branch-and-bound), Holt-Winters aditivo (nivel, tendencia, estacionalidad), Intervalo conformal al 90 % (ŷ ± q̂), Error MAPE, Monte Carlo: media, percentiles 10/50/90 y riesgo de rebasar la capacidad, Poisson de huracanes: λ_m y P(N_m ≥ 1) = 1 − e^{−λ_m} (+7 more)

### Community 6 - "Campaña y minería de texto"
Cohesion: 0.20
Nodes (14): D5 Rest-Mex 2025 (208,051 reseñas; 85,993 Q. Roo), Reglas de asociación (soporte, confianza, lift), Peso TF-IDF de un término, Branding de la campaña, Campaña (Mercadotecnia digital), Ecuaciones previstas por módulo (F.2), Fase 8 — Campaña (Mercadotecnia), Incidente crítico: Mercadotecnia digital (+6 more)

### Community 7 - "Minería y buyer persona"
Cohesion: 0.23
Nodes (12): D11 ENDUTIH 2025 INEGI, Análisis de sentimiento, Buyer persona, Detección de comunidades en redes sociales, Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan, P5: Características de visitantes para recomendar destinos alternativos, Preguntas Minería: ¿manipular el libre mercado o corregir sesgos? ¿parche o turismo regenerativo? desinformación de bots, Hand, Mannila & Smyth (2001). Principles of data mining (+4 more)

### Community 8 - "IO dos etapas y Pareto"
Cohesion: 0.30
Nodes (12): D13 Benchmarks de costo por canal (WordStream 2025 / LocaliQ 2026), Modelo de dos etapas: max Σ r x + E[Q(x, ξ)], Frontera de Pareto por ε-restricción (visitantes vs presión), Precios sombra ∂z*/∂b_i, /api/optimizar (POST), Fase 6 — IO (un modelo, dos etapas), Frontera de Pareto y precios sombra, Incidente crítico: Investigación de Operaciones (+4 more)

### Community 9 - "Problema prototípico base"
Cohesion: 0.18
Nodes (12): Actores: autoridades, prestadores de servicios, comunidades, turistas, plataformas, científicos de datos, Capacidad de carga del destino, Habilidades blandas (pensamiento crítico, negociación, trabajo en equipo, etc.), Licenciatura en Ciencias de Datos para Negocios (5° semestre, 2026-2), Problema Prototípico: Turismo inteligente sustentable para México, Redistribución de flujos turísticos, SECTUR (2021). Estrategia de Turismo Sostenible 2030, SECTUR (2021). Ordenamiento turístico sustentable (+4 more)

### Community 10 - "Incidente Big Data (NIST)"
Cohesion: 0.18
Nodes (12): Arquitectura distribuida de Big Data, Integración de datos en tiempo real para ajustar la campaña (baja latencia), Incidente crítico Almacenamiento de Grandes Volúmenes: Cuando los datos del turismo no caben en una sola computadora, ¿Cómo diseñar una estrategia de almacenamiento de grandes volúmenes de datos turísticos heterogéneos, escalable y responsable?, Privacidad y riesgos de datos de movilidad/geolocalización de turistas, INEGI (2025). Cuenta Satélite del Turismo de México 2024, NIST (2020). Big data, Computer Security Resource Center, NIST SP 1500-1r2 (2019). Big Data Definitions (+4 more)

### Community 11 - "Entregables oficiales"
Cohesion: 0.18
Nodes (11): Desarrollo del branding de la marca, Campaña publicitaria inteligente para la redistribución sustentable de flujos turísticos (producto integrador), Presentación para el Coloquio de la Licenciatura, Criterio 10: Informe técnico y comunicación de resultados (4%), Criterio 11: Coloquio: exposición y defensa (4%), Entregable A: Campaña publicitaria del estado seleccionado, Entregable B: Informe técnico (30-40 páginas), Entregable C: Productos técnicos (bases de datos, código, notebooks, modelos) (+3 more)

### Community 12 - "Front-end y secciones"
Cohesion: 0.24
Nodes (10): D12 GeoJSON Q. Roo, D14 DESIGN.md (tokens y componentes), Fase 10 — Front-end, Front-end HTML + CSS + JS (ECharts, GSAP), Reglas anti-saturación de la página, Sección 0: Barra de anuncio, Sección 1: Portada con tarjetas flotantes, Sección 2: ¿Dónde hay espacio hoy? (+2 more)

### Community 13 - "A5 Torre en vivo"
Cohesion: 0.38
Nodes (10): D8 Open-Meteo archivo (clima horario 8 puntos), Puntaje de anomalía Isolation Forest s(x) = 2^{−E[h(x)]/c(n)}, Regla de pausa: si IPT > u o s(x) > τ entonces y_{w,d} = 0, A5 Torre en vivo, /api/stream (SSE), Fase 7 — A5 Torre en vivo, Detección de anomalías con Isolation Forest, Motor de reglas de A5 (+2 more)

### Community 14 - "Fusión e integración"
Cohesion: 0.22
Nodes (10): Estafeta A3 → A1 → A5 → Campaña, Fase 11 — Cierre, Incidente crítico: Estocásticos, Incidente crítico: Minería, Incidente crítico: Aprendizaje de máquina, Límites que evitan el encimamiento, Problema Prototípico: turismo inteligente sustentable (Quintana Roo), Rúbrica de 11 criterios (nivel Excelente) (+2 more)

### Community 15 - "Criterios de la rúbrica"
Cohesion: 0.22
Nodes (10): Criterio 1: Planteamiento y comprensión del problema (8%), Criterio 2: Gestión y almacenamiento de grandes volúmenes de datos (12%), Criterio 3: Minería de datos (12%), Criterio 4: Aprendizaje de máquina (12%), Criterio 5: Modelos estocásticos (10%), Criterio 6: Investigación de Operaciones (12%), Criterio 7: Mercadotecnia Digital (8%), Criterio 8: Integración interdisciplinaria (10%) (+2 more)

### Community 16 - "Incidente IO y escenarios"
Cohesion: 0.20
Nodes (10): Escenarios optimista, moderado y pesimista, Incidente crítico (dispositivo pedagógico de ética aplicada), Incidente crítico Investigación de Operaciones: Optimización de los flujos turísticos para un desarrollo sustentable, P4: Escenarios de redistribución sin reducir la actividad económica, Preguntas IO: ¿Qué significa que una distribución sea óptima? ¿Qué priorizar si los objetivos se contraponen?, Canca Ortiz & Villa Caro (2021). Introducción a la investigación de operaciones, Meyer Krumholz et al. (2002). Turismo y desarrollo sostenible, OMT (2005). Indicadores de desarrollo sostenible para los destinos turísticos (+2 more)

### Community 17 - "Incidente ML y referencias"
Cohesion: 0.22
Nodes (10): Incidente crítico Aprendizaje de Máquina: Turismo inteligente sustentable en México, Modelo predictivo como producto de consultoría (suscripciones/licencias), ¿Cómo usar el aprendizaje de máquina para un turismo más inteligente sin aumentar la presión sobre recursos y comunidades?, Si un algoritmo puede predecir dónde estarán los turistas, ¿puede ayudar a decidir dónde deberían estar?, Belkaid & Kummitha (2026). Artificial intelligence in sustainable tourism development, Gretzel et al. (2015). Conceptual foundations for understanding smart tourism ecosystems, Gretzel et al. (2015). Smart tourism: Foundations and developments, OMT (2018). 'Overtourism'? Understanding and managing urban tourism growth (+2 more)

### Community 18 - "Backend FastAPI"
Cohesion: 0.22
Nodes (9): /api/campana, /api/consulta, /api/escenarios, /api/pronostico, /api/radar, Fase 9 — Backend, Backend FastAPI, KaTeX local (ecuaciones en la pestaña Evidencia, sin CDN) (+1 more)

### Community 19 - "Preguntas secundarias e impacto"
Cohesion: 0.29
Nodes (8): Criterio 9: Propuesta de solución e impacto (8%), Dilema: actividad económica vs. protección de recursos y comunidades, ¿Cómo distribuir mejor los flujos turísticos para beneficiar a las comunidades y disminuir el impacto ambiental?, P1: Patrones temporales, espaciales y de comportamiento de la concentración turística, P2: Variables relacionadas con la saturación o baja actividad turística, P3: Estimación de la demanda turística futura bajo incertidumbre, P6: Impacto de la redistribución en comunidades receptoras y destinos saturados, P7: Evaluación de viabilidad, sustentabilidad y efectividad de la redistribución

## Ambiguous Edges - Review These
- `Floating Notification Card` → `Integración de datos en tiempo real para ajustar la campaña (baja latencia)`  [AMBIGUOUS]
  docs/DESIGN.md · relation: semantically_similar_to
- `D13 Benchmarks de costo por canal (WordStream 2025 / LocaliQ 2026)` → `Hueco: ocupación oficial del sur 2025–2026`  [AMBIGUOUS]
  docs/datos/INVENTARIO.md · relation: conceptually_related_to

## Knowledge Gaps
- **66 isolated node(s):** `Paquete cauce (proyecto anterior, descartado)`, `Crisis de Tulum (ventas −60 %)`, `Sargazo récord 2026 (>104,700 t; 56 de 140 playas en rojo)`, `SITUR-Q: API con 45 indicadores`, `Fase 0 — entorno (PySpark, JDK 17)` (+61 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 69 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Floating Notification Card` and `Integración de datos en tiempo real para ajustar la campaña (baja latencia)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `D13 Benchmarks de costo por canal (WordStream 2025 / LocaliQ 2026)` and `Hueco: ocupación oficial del sur 2025–2026`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Buyer persona` connect `Minería y buyer persona` to `Regiones y evidencia INAH`, `Entregables oficiales`, `Incidentes estocástico y marketing`, `Campaña y minería de texto`?**
  _High betweenness centrality (0.501) - this node is a cross-community bridge._
- **Why does `Flighty — Style Reference (sistema de diseño)` connect `Sistema de diseño Flighty` to `Entregables oficiales`?**
  _High betweenness centrality (0.228) - this node is a cross-community bridge._
- **Why does `Entregable A: Campaña publicitaria del estado seleccionado` connect `Entregables oficiales` to `Incidentes estocástico y marketing`, `Minería y buyer persona`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan` (e.g. with `Criterio 3: Minería de datos (12%)` and `P1: Patrones temporales, espaciales y de comportamiento de la concentración turística`) actually correct?**
  _`Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Paquete cauce (proyecto anterior, descartado)`, `Crisis de Tulum (ventas −60 %)`, `Sargazo récord 2026 (>104,700 t; 56 de 140 playas en rojo)` to the rest of the system?**
  _66 weakly-connected nodes found - possible documentation gaps or missing edges._