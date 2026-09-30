# Graph Report - PP 5to semestre CASCO SANTO TOMAS  (2026-09-29)

## Corpus Check
- 71 files · ~99,564 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 5, .ipynb 2, .css 1)

## Summary
- 1249 nodes · 2164 edges · 108 communities (69 shown, 39 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 196 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9ab68990`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- PLAN_v3.md (plan aprobado)
- Decisión: la campaña promueve 5 regiones de Quintana Roo
- Flighty — Style Reference (sistema de diseño)
- datos_pagina.py
- app.js
- test_pagina.py
- figuras.py
- prediccion.py
- frontend/index.html (página pública)
- silver_iter.py
- panel.py
- markov.py
- 00 — Fundación del proyecto
- ingesta_siturq.py
- ingesta_abiertas.py
- entorno.py
- test_ingesta.py
- Inventario de datos - fuentes oficiales verificadas
- DataFrame
- Rúbrica de evaluación (11 criterios, 100%)
- README Torre del Caribe
- test_planteamiento.py
- Problema Prototípico: Turismo inteligente sustentable para México
- test_radar_panel.py
- Cinco regiones promovidas
- Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan
- test_radar_indice.py
- pandas
- ingesta_datatur.py
- CLAUDE.md - Reglas del repositorio Torre del Caribe
- ingesta_fotos.py
- clustering.py
- Incidente crítico Modelos Estocásticos: Incertidumbre en la demanda turística
- test_silver.py
- D6 DENUE INEGI (32 estados)
- D1 SITUR-Q API (45 indicadores)
- Página web de la campaña
- Incidente crítico Almacenamiento de Grandes Volúmenes: Cuando los datos del turismo no caben en una sola computadora
- Incidente crítico Investigación de Operaciones: Optimización de los flujos turísticos para un desarrollo sustentable
- Incidente crítico Aprendizaje de Máquina: Turismo inteligente sustentable en México
- descargar_datatur
- silver_datatur_ocupacion.py
- Índice de Presión Turística (IPT)
- Criterio de selección de modelo: más aciertos y más cambios anticipados
- Decisión 08 — A1 Radar (Fase 4)
- Hoja de ruta del proyecto
- pytest
- test_radar_markov.py
- test_radar_clustering.py
- Sistema visual Sur mexicano
- Decisión 06 — La página para público no técnico
- silver_inah.py
- Índice comparable (lo que publica el Radar)
- Cifras oficiales conocidas verificadas
- Depósitos Bronze / Silver / Gold
- Fase 7 — Torre en vivo
- Foco en 5 regiones (Chetumal, Calderitas–Oxtankah, Ruta arqueológica del sur, Maya Ka'an + Kantemó, Laguna Milagros–Xul-Ha)
- Incidente crítico Mercadotecnia Digital: Estrategias digitales para la redistribución del turismo
- v
- 04 - Limpieza y orden de los datos (Fase 2: Silver y Gold)
- Estado de las fases (28-sep-2026)
- Opción D: ocupación DataTur + componente en ≥2 lugares
- Decisión 05: Planteamiento con datos (Fase 3)
- DataFrame
- pathlib
- 09 — Auditoría de las Fases 1 a 4 contra el plan
- Decisiones cerradas hasta hoy (A.8)
- 03 - Ingesta de fuentes oficiales (Fase 1: Bronze)
- Path
- Limitación: quiebre de 2025 (SITUR-Q deja de publicar ocupación)
- Clustering jerárquico Ward de 55 centros DataTur
- EQUIPO
- Hallazgo: zonas arqueológicas SITUR-Q = INAH agrupado por destino
- Cap. 3 — Preparación del equipo de cómputo (Fase 0)
- Reglas de asociación (soporte, confianza, lift)
- Rediseño 'Sur mexicano' (Claude Design)
- test_qroo_239_semanas
- test_nota_isla_mujeres
- test_denue_total_nacional
- test_denue_turisticos_qroo
- test_denue_sin_datos_personales
- test_inah_cifras_de_la_seleccion_de_regiones
- test_inah_kohunlich_crece_en_2026
- test_inah_papel_de_las_zonas
- test_iter_poblacion_de_las_5_regiones
- test_cero_real_se_conserva
- test_regla_6_aereos
- test_afluencia_y_derrama_terminan_en_marzo_2024
- test_cancun_semana_31_2026
- DataFrame
- SparkSession
- Documento ejecutivo (DOCUMENTO_EJECUTIVO.md → PDF)
- Regla de cierres: ≥12 meses seguidos abierta y sin cierres en 2026
- fixture
- Series
- duckdb==1.1.3 (consulta rápida para la API)
- fastapi + uvicorn (backend web)
- PuLP==2.9.0 (programación lineal/entera con CBC)
- statsmodels==0.14.4 (Holt-Winters, STL)

## God Nodes (most connected - your core abstractions)
1. `Flighty — Style Reference (sistema de diseño)` - 49 edges
2. `Inventario de datos - fuentes oficiales verificadas` - 33 edges
3. `Problema Prototípico: Turismo inteligente sustentable para México` - 27 edges
4. `04 - Limpieza y orden de los datos (Fase 2: Silver y Gold)` - 25 edges
5. `Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan` - 24 edges
6. `PLAN_v3.md (plan aprobado)` - 23 edges
7. `frontend/index.html (página pública)` - 22 edges
8. `CLAUDE.md - Reglas del repositorio Torre del Caribe` - 21 edges
9. `Incidente crítico Aprendizaje de Máquina: Turismo inteligente sustentable en México` - 20 edges
10. `03 - Ingesta de fuentes oficiales (Fase 1: Bronze)` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Destinos saturados/limitados: Cozumel, Isla Mujeres, Holbox` --conceptually_related_to--> `Capacidad de carga del destino`  [INFERRED]
  docs/decisiones/00-fundacion.md → PROBLEMA PROTOTÍPICO 5°- LCDN-2026-2.pdf
- `Sección El dato (4 de cada 10 cuartos)` --shares_data_with--> `cuartos_vacios_chetumal()`  [INFERRED]
  frontend/index.html → backend/torre/api/datos_pagina.py
- `Concentración (HHI): 5 lugares con 12.3 % de población pero 1.4 % de llegadas en avión; avión HHI 0.81` --references--> `cuotas_y_hhi()`  [INFERRED]
  docs/ejecutivo/DOCUMENTO_EJECUTIVO.md → backend/torre/radar/planteamiento.py
- `Corrección de conteo: DENUE 6,138,075 e ITER 2,243` --references--> `_filas_csv_en_zip()`  [EXTRACTED]
  docs/decisiones/03-ingesta.md → backend/torre/base/ingesta_abiertas.py
- `Sección 'Con datos oficiales' y tabla de criterios` --shares_data_with--> `calcular_criterios()`  [INFERRED]
  frontend/index.html → backend/torre/radar/criterios.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Arquitectura de datos Bronze -> Silver -> Gold con PySpark** — docs_ejecutivo_documento_ejecutivo_manifiesto_sha256 [EXTRACTED 0.95]
- **Flujo del Radar: panel mensual -> índice -> índice comparable -> predicción y Markov** — docs_ejecutivo_documento_ejecutivo_indice_comparable [EXTRACTED 0.95]
- **Cadena de integración de las seis UCA en la campaña publicitaria inteligente** — problema_prototípico_5_lcdn_2026_2_evidencia_integradora, problema_prototípico_5_lcdn_2026_2_incidente_big_data, problema_prototípico_5_lcdn_2026_2_incidente_mineria_datos, problema_prototípico_5_lcdn_2026_2_incidente_aprendizaje_maquina, problema_prototípico_5_lcdn_2026_2_incidente_estocasticos, problema_prototípico_5_lcdn_2026_2_incidente_investigacion_operaciones, problema_prototípico_5_lcdn_2026_2_incidente_mercadotecnia_digital, problema_prototípico_5_lcdn_2026_2_campana_publicitaria_inteligente [EXTRACTED 1.00]
- **Las 5 regiones que promueve la campaña** — docs_regiones_regiones_chetumal, docs_regiones_regiones_bahia_calderitas_oxtankah, docs_plan_plan_v3_region_ruta_arqueologica_sur, docs_regiones_regiones_maya_kaan_interior_kantemo, docs_regiones_regiones_laguna_milagros_xul_ha [EXTRACTED 1.00]
- **Las 5 regiones vigentes a promover (Parte G / Regla 9)** — docs_plan_plan_v3_region_chetumal, docs_regiones_regiones_bahia_calderitas_oxtankah, docs_plan_plan_v3_region_ruta_arqueologica_sur, docs_plan_plan_v3_region_maya_kaan_kantemo, docs_regiones_regiones_laguna_milagros_xul_ha [EXTRACTED 1.00]
- **Comparación de modelos con origen móvil y criterio de Brandon** — docs_metodologia_ecuaciones_origen_movil, docs_metodologia_ecuaciones_persistencia, docs_metodologia_ecuaciones_regresion_logistica_multiclase, docs_metodologia_ecuaciones_random_forest, docs_metodologia_ecuaciones_gradient_boosting, docs_metodologia_ecuaciones_f1_macro, docs_decisiones_08_radar_seleccion_de_modelo_criterio_brandon [EXTRACTED 1.00]
- **Contrato del cascarón: datos por fase a la página** — docs_decisiones_06_pagina_contrato_cascaron, frontend_index_modulos_data_clave, frontend_datos_pagina, frontend_app_dibujar, frontend_index_fases [EXTRACTED 1.00]
- **Las cinco regiones de la campaña** — docs_ejecutivo_documento_ejecutivo_chetumal, docs_ejecutivo_documento_ejecutivo_bahia_calderitas_oxtankah, docs_plan_plan_v3_region_ruta_arqueologica_sur, docs_regiones_regiones_maya_kaan_interior_kantemo, docs_ejecutivo_documento_ejecutivo_laguna_milagros_xul_ha [EXTRACTED 1.00]
- **Pipeline del Radar: índice, estados, predicción y Markov** — docs_ejecutivo_documento_ejecutivo_indice_de_presion, docs_ejecutivo_documento_ejecutivo_indice_comparable, docs_decisiones_08_radar_estados_radar, docs_ejecutivo_documento_ejecutivo_regresion_logistica, docs_ejecutivo_documento_ejecutivo_cadena_de_markov, docs_ejecutivo_documento_ejecutivo_agrupamiento_jerarquico [EXTRACTED 1.00]
- **Identidad visual UNRC aplicada al documento ejecutivo** — docs_ejecutivo_guia_estilo_unrc_color_guinda, docs_ejecutivo_guia_estilo_unrc_color_dorado, docs_ejecutivo_guia_estilo_unrc_tipografia_patria, docs_ejecutivo_guia_estilo_unrc_tipografia_noto_sans, docs_ejecutivo_guia_estilo_unrc_regla_nunca_texto_negro [EXTRACTED 1.00]
- **Estafeta A3 → A1 → A5 → Campaña** — docs_plan_plan_v3_a3_pronostico, docs_plan_plan_v3_a1_radar, docs_plan_plan_v3_a5_torre_en_vivo, docs_plan_plan_v3_programacion_estocastica_dos_etapas [EXTRACTED 1.00]
- **Evidencia para no promover playa en 2026** — docs_decisiones_00_fundacion_sargazo_2026, docs_decisiones_00_fundacion_crisis_tulum, docs_decisiones_00_fundacion_destinos_saturados, docs_decisiones_00_fundacion_decision_no_playa [EXTRACTED 1.00]
- **Colores de señal y componentes que los usan (acción, conversión, alerta)** — docs_design_signal_light_color_system, docs_design_color_signal_blue, docs_design_color_amber_alert, docs_design_color_alert_red, docs_design_primary_blue_button, docs_design_amber_download_button, docs_design_floating_notification_card [EXTRACTED 1.00]
- **Flujo de datos: Bronze → Silver → Gold → DuckDB/Streaming → API → página** — docs_plan_plan_v3_lakehouse_bronze_silver_gold, docs_plan_plan_v3_duckdb_sobre_gold, docs_plan_plan_v3_spark_structured_streaming, docs_plan_plan_v3_backend_fastapi_endpoints, docs_plan_plan_v3_pagina_web_recorrido [EXTRACTED 1.00]
- **Pila del entorno Fase 0 (PySpark 3.5.6 + JDK 17 + winutils 3.3.6 + .venv)** — docs_decisiones_02_entorno_pyspark_3_5_6, docs_decisiones_02_entorno_jdk_17, docs_decisiones_02_entorno_winutils_hadoop_dll, docs_decisiones_02_entorno_venv_aislado, backend_torre_base_entorno, docs_decisiones_02_entorno_prueba_de_humo [EXTRACTED 1.00]
- **Flujo del Radar: panel → IPT → índice comparable → predicción del estado** — docs_decisiones_08_radar_panel_mensual, docs_plan_plan_v3_indice_presion_turistica, docs_decisiones_08_radar_indice_comparable, docs_metodologia_ecuaciones_regresion_logistica_multiclase, docs_decisiones_08_radar_prediccion_agosto_2026, docs_decisiones_08_radar_seccion_donde_hay_espacio_hoy [EXTRACTED 1.00]
- **Tres horizontes: Radar, Pronóstico y Torre en vivo alimentando la campaña** — docs_plan_plan_v3_a1_radar, docs_plan_plan_v3_a3_pronostico, docs_plan_plan_v3_a5_torre_en_vivo, docs_plan_plan_v3_campana_mercadotecnia, docs_plan_plan_v3_estafeta_entre_modulos [EXTRACTED 1.00]
- **Huecos declarados en lugar de inventar datos** — docs_ejecutivo_documento_ejecutivo_sin_flechas_od, docs_ejecutivo_documento_ejecutivo_derrama_no_usada, docs_decisiones_08_radar_laguna_sin_dato, docs_ejecutivo_documento_ejecutivo_regla_ceros_hueco, docs_plan_hoja_de_ruta_conversion_facebook_supuesto [INFERRED 0.85]
- **Principios de honestidad con los datos** — docs_ejecutivo_documento_ejecutivo_no_inventar_datos, docs_ejecutivo_documento_ejecutivo_ceros_como_faltantes, docs_ejecutivo_documento_ejecutivo_dato_oficial_sobre_prensa, docs_ejecutivo_documento_ejecutivo_no_escoger_datos_a_conveniencia, docs_ejecutivo_documento_ejecutivo_derrama_economica_descartada, docs_ejecutivo_documento_ejecutivo_doble_conteo_inah_siturq [INFERRED 0.85]
- **Modo oscuro 'sala de control' de Flighty** — docs_design_light_to_dark_transition, docs_design_color_deep_indigo, docs_design_color_midnight_ink, docs_design_press_logo_card, docs_design_dark_ghost_button, docs_design_section_divider_band, docs_design_gradient_system [INFERRED 0.85]
- **Principios de honestidad: no inventar, declarar huecos, dato oficial primero, sin cherry-picking** — docs_ejecutivo_documento_ejecutivo_no_inventar_datos [INFERRED 0.85]
- **Huecos y diferencias de datos que se declaran en vez de rellenarse** — objetivo_regla_no_inventar_datos, docs_decisiones_08_radar_laguna_milagros_sin_dato_oficial, docs_decisiones_08_radar_quiebre_de_2025, docs_decisiones_08_radar_datatur_menor_que_situr_q_declarado, objetivo_regla_6_de_silver, docs_decisiones_09_auditoria_fases_1_4_sesgo_norte_sur [INFERRED 0.85]
- **Reglas de Silver para distinguir hueco de cero real** — docs_decisiones_04_silver_regla_ocupacion_hueco, docs_decisiones_04_silver_regla_afluencia_derrama_hueco, docs_decisiones_04_silver_regla_ceros_reales, docs_decisiones_04_silver_regla_6_aereos, claude_regla_no_inventar_datos [INFERRED 0.85]

## Communities (108 total, 39 thin omitted)

### Community 0 - "PLAN_v3.md (plan aprobado)"
Cohesion: 0.06
Nodes (58): D12 GeoJSON Q. Roo, Inferir estados futuros con ML (clasificador + Markov), Índice de Herfindahl-Hirschman (concentración), Planteamiento con datos (Fase 3), PLAN_v3.md (plan aprobado), A1 Radar, A3 Pronóstico, A5 Torre en vivo (+50 more)

### Community 1 - "Decisión: la campaña promueve 5 regiones de Quintana Roo"
Cohesion: 0.07
Nodes (55): Regla 9: Solo 5 regiones, D4 DataTur BdINAH (visitas a zonas arqueológicas), 01 — Regiones que promueve la campaña, Criterios 6 (IO) y 9 (propuesta e impacto) de la rúbrica, Decisión: la campaña promueve 5 regiones de Quintana Roo, Revisión del 28-sep-2026: de 8 a 5 regiones, Riesgos que se vigilan (sargazo en la bahía, laguna frágil, poca oferta en Maya Ka'an), Tope estricto de capacidad en el modelo de IO (+47 more)

### Community 2 - "Flighty — Style Reference (sistema de diseño)"
Cohesion: 0.11
Nodes (51): Agent Prompt Guide (prompts de componentes), Amber Download Button, Announcement Bar, Award Badge Pair, Sistema de radios (pill 999px, cards 16px, floating cards 20px), Apple Product Pages, Arc Browser, Linear (+43 more)

### Community 3 - "datos_pagina.py"
Cohesion: 0.07
Nodes (47): _cifra(), concentracion_pagina(), criterios(), cuartos_vacios_chetumal(), evidencia_pagina(), ultimo_mes(), fases_del_proyecto(), fichas_regiones() (+39 more)

### Community 4 - "app.js"
Cohesion: 0.09
Nodes (40): acercarA(), alAparecer(), alternarGiro(), arrastrar(), camara(), capitulos(), cifrasDe(), CLASE_ESTADO (+32 more)

### Community 5 - "test_pagina.py"
Cohesion: 0.09
Nodes (16): datos(), fixture, El chat no da precios (no hay fuente oficial abierta) y la respuesta de espacio…, 2024: 458,696 de 791,016 noches ocupadas = 58.0 % → 4 de cada 10 vacías (sin…, Laguna Milagros–Xul-Ha no tiene estadística turística propia: se declara, no se…, Cada pueblo y zona de las 5 regiones está en Quintana Roo y en su municipio…, Cada lugar tiene foto local con autor y licencia libre (la licencia exige…, Totales por modo = último año completo de SITUR-Q (el avión se queda en 2024… (+8 more)

### Community 6 - "figuras.py"
Cohesion: 0.09
Nodes (39): cobertura_ocupacion_siturq(), costos_publicitarios_travel(), estilo_unrc(), _leer_inah(), ocupacion_semanal_qroo(), oferta_turistica_municipios(), _pie(), Path (+31 more)

### Community 7 - "prediccion.py"
Cohesion: 0.09
Nodes (37): calcular(), componentes(), elegir_componentes(), estados(), guardar(), ipt(), minmax(), DataFrame (+29 more)

### Community 8 - "frontend/index.html (página pública)"
Cohesion: 0.17
Nodes (15): Ocupación hotelera anual O_{d,2024} (sumar antes de dividir), frontend/index.html (página pública), Módulo 'La campaña' (Fase 8, oculto), Módulo pronóstico 'Mejor mes para ir' (Fase 5, oculto), Módulos ocultos: en vivo, escenarios, presupuesto, Patrón data-clave: secciones ocultas que aparecen con su clave en pagina.js, Sección 'El dato': 4 de cada 10 cuartos vacíos en Chetumal, Sección '¿Dónde se queda el dinero?' (+7 more)

### Community 9 - "silver_iter.py"
Cohesion: 0.07
Nodes (35): asignar_regiones(), construir_silver_iter(), _grados(), leer_iter(), DataFrame, Convierte '88°17\\'52.436" W' a grados decimales (−88.2979). Así publica el…, calcular_criterios(), _meses_abierta() (+27 more)

### Community 10 - "panel.py"
Cohesion: 0.06
Nodes (42): cobertura(), _datatur(), guardar(), _inah(), panel_mensual(), _poblacion(), DataFrame, Path (+34 more)

### Community 11 - "markov.py"
Cohesion: 0.11
Nodes (34): a_k_semanas(), backtest(), correr(), estacionaria(), estados(), matriz(), ocupacion_semanal(), Pares (estado de la semana t, estado de la semana t+1) del mismo centro, solo… (+26 more)

### Community 12 - "00 — Fundación del proyecto"
Cohesion: 0.29
Nodes (7): Encabezado obligatorio de archivo de codigo, Mapa del proyecto (Graphify), Decisión 1: empezar desde cero, Decisión 4: herramientas (git local + Graphify), 00 — Fundación del proyecto, Paquete cauce (proyecto anterior, descartado), Brandon Uriel García Sánchez

### Community 13 - "ingesta_siturq.py"
Cohesion: 0.17
Nodes (14): consultar(), descargar_siturq(), leer_catalogo(), Descarga todos los INDICADORES × unidades × años y guarda un archivo JSON crudo…, Lee la página pública y extrae el token, los destinos y las zonas tal como los…, Pide a la API un indicador para una unidad (destino o zona) y un año completo…, Path, Huella SHA-256 del archivo, leída en bloques de 1 MB para no cargar archivos… (+6 more)

### Community 14 - "ingesta_abiertas.py"
Cohesion: 0.14
Nodes (22): _bajar(), _bajar_con_espera(), clima(), denue(), descargar_abiertas(), endutih(), _es_zip(), _filas_csv_en_zip() (+14 more)

### Community 15 - "entorno.py"
Cohesion: 0.06
Nodes (41): buscar_jdk17(), configurar_entorno(), crear_spark(), Path, Busca un JDK 17 instalado en las rutas estándar de Windows. Devuelve la carpeta…, Fija JAVA_HOME, HADOOP_HOME y PATH solo para este proceso. Devuelve lo que…, Devuelve la ruta "corta" de Windows, sin espacios (por ejemplo, la carpeta "PP…, Crea una sesión de Spark local que usa todos los núcleos de la máquina.… (+33 more)

### Community 16 - "test_ingesta.py"
Cohesion: 0.14
Nodes (21): filas_manifiesto(), Tabla oficial de WordStream 2025, Travel: CPC $2.12 y CTR 8.73 % (extraída con…, Los 32 estados están presentes (el Estado de México viene en dos partes)., Lee el archivo más reciente de un indicador de SITUR-Q., Busca un valor dentro de las respuestas crudas de la API (unidad, año, mes,…, Cada archivo del manifiesto existe y su SHA-256 es el registrado (nadie lo…, HuggingFace reportó 208,051 filas para vg055/Rest-Mex2025 (consulta del…, Visitantes 2025 a la Z.A. de Tulum = 1,031,443 (cálculo del 27-sep-2026,… (+13 more)

### Community 17 - "Inventario de datos - fuentes oficiales verificadas"
Cohesion: 0.11
Nodes (21): A3 Pronostico (cuando conviene ir, 1-12 meses), Regla de oro: sin scraping prohibido (TripAdvisor, Google Maps), Inventario de datos - fuentes oficiales verificadas, D10 FRED (peso-dolar, CPI), D12 GeoJSON Quintana Roo, D13 Benchmarks de costo por canal (WordStream 2025 / LocaliQ 2026), D14 DESIGN.md (tokens y componentes), D15 Wikimedia Commons (fotos con licencia libre) (+13 more)

### Community 19 - "Rúbrica de evaluación (11 criterios, 100%)"
Cohesion: 0.14
Nodes (17): Campaña publicitaria inteligente para la redistribución sustentable de flujos turísticos (producto integrador), Presentación para el Coloquio de la Licenciatura, Criterio 10: Informe técnico y comunicación de resultados (4%), Criterio 11: Coloquio: exposición y defensa (4%), Criterio 1: Planteamiento y comprensión del problema (8%), Criterio 2: Gestión y almacenamiento de grandes volúmenes de datos (12%), Criterio 3: Minería de datos (12%), Criterio 4: Aprendizaje de máquina (12%) (+9 more)

### Community 20 - "README Torre del Caribe"
Cohesion: 0.20
Nodes (10): generar_pdf(), Path, Inserta una línea en blanco antes de cada lista que va pegada a un párrafo. El…, Convierte un Markdown del proyecto en PDF con portada y estilo UNRC. Sirve para…, _separar_listas(), Documento ejecutivo Torre del Caribe, markdown, Fase 2 — limpieza Silver/Gold con PySpark (+2 more)

### Community 21 - "test_planteamiento.py"
Cohesion: 0.13
Nodes (12): 17 variables y 7 actores medidos del problema, conc(), DataFrame, fixture, Reparto parejo → HHI = 1/N y HHI* = 0; una unidad dominante → HHI* cerca de 1., ECUACIONES.md §1-ter: avión 2024, HHI = 0.8586, HHI* = 0.811, Chetumal 1.4 %., Los actores usan 229,247 habitantes: la suma de las 5 regiones de la tabla de…, Por eso el total estatal de cuartos suma destinos + zonas y no miembros (ver… (+4 more)

### Community 22 - "Problema Prototípico: Turismo inteligente sustentable para México"
Cohesion: 0.15
Nodes (14): Pregunta central del Problema Prototípico, Preguntas secundarias (7), Actores: autoridades, prestadores de servicios, comunidades, turistas, plataformas, científicos de datos, Capacidad de carga del destino, Habilidades blandas (pensamiento crítico, negociación, trabajo en equipo, etc.), Licenciatura en Ciencias de Datos para Negocios (5° semestre, 2026-2), Problema Prototípico: Turismo inteligente sustentable para México, Redistribución de flujos turísticos (+6 more)

### Community 23 - "test_radar_panel.py"
Cohesion: 0.15
Nodes (11): _anual(), p(), DataFrame, fixture, ocupacion_hotelera trae 3 filas por mes; el porcentaje es ocupados ÷…, La suma del panel = la suma de todas las zonas arqueológicas del INAH en…, Laguna Milagros no tiene serie turística: todo su panel queda nulo (no se…, test_cifras_conocidas() (+3 more)

### Community 24 - "Cinco regiones promovidas"
Cohesion: 0.12
Nodes (19): Bahía de Chetumal: Calderitas y Oxtankah, Cap. 2.1 — Qué regiones promueve la campaña (5 regiones), Cap. 2 — El problema en números: ¿a dónde van los turistas?, Chetumal, Tulum recibe 15.5 veces más que la ruta del sur (1,031,443 ÷ 66,628), Tulum −31.3 % entre ene–jul 2025 y ene–jul 2026 (476,247 ÷ 692,946 − 1), Cinco criterios de selección: sin sargazo, sin crisis 2026, no saturadas, ecosistema que aguante, con datos oficiales, Cinco regiones promovidas (+11 more)

### Community 25 - "Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan"
Cohesion: 0.21
Nodes (13): D11 ENDUTIH 2025 INEGI, D3 DataTur BD_Nacionalidad (521,364 filas), TF-IDF y reglas de asociación (minería de texto de la campaña), Análisis de sentimiento, Buyer persona, Detección de comunidades en redes sociales, Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan, Preguntas Minería: ¿manipular el libre mercado o corregir sesgos? ¿parche o turismo regenerativo? desinformación de bots (+5 more)

### Community 26 - "test_radar_indice.py"
Cohesion: 0.15
Nodes (9): fixture, r(), Pesos iguales solo sobre lo que existe: (0.2 + 0.6) / 2 = 0.4; una fila sin…, ECUACIONES.md §2.1: Cancún jul-2026 → (0.0497 + 0.0001 + 0.0011 + 0.7214) / 4 =…, La prueba que falló con mín–máx sin DataTur: en 2025–2026 el norte de…, test_ejemplo_a_mano_cancun(), test_ipt_de_juguete(), test_validez_norte_arriba_del_sur_2025_2026() (+1 more)

### Community 27 - "pandas"
Cohesion: 0.10
Nodes (17): pandas, parametrize, sys, cifras(), fixture, Cada cifra recalculada desde Gold o desde las funciones, con el formato con que…, test_cifra_escrita_coincide_con_el_calculo(), textos() (+9 more)

### Community 28 - "ingesta_datatur.py"
Cohesion: 0.25
Nodes (10): capturar_evidencia(), Visita cada fuente, guarda HTML + captura + párrafos relevantes y devuelve esos…, a_numero(), descargar_benchmarks(), $2.12' → 2.12 · '8.73%' → 8.73 · ' $44.70' → 44.70. Devuelve None si no hay…, csv, datetime, playwright_sync_api (+2 more)

### Community 29 - "CLAUDE.md - Reglas del repositorio Torre del Caribe"
Cohesion: 0.20
Nodes (11): CLAUDE.md - Reglas del repositorio Torre del Caribe, Arquitectura de datos bronze / silver / gold, Convenciones de código (snake_case en español, _est, _flag, encabezado), Graphify como mapa del proyecto (no correr graphify update a mano), Protocolo de trabajo con Brandon (anti-caja negra), Regla de oro: toda cifra rastreable (crudo -> funcion -> salida), Regla 6: Desde cero (nada del proyecto anterior), Regla 5: Si falta un dato, se detiene y se avisa (+3 more)

### Community 30 - "ingesta_fotos.py"
Cohesion: 0.13
Nodes (19): descargar_fotos(), _limpiar(), _pedir(), GET con reintentos: Commons limita las consultas seguidas (visto el…, _slug(), _dentro(), municipio_de(), DataFrame (+11 more)

### Community 31 - "clustering.py"
Cohesion: 0.27
Nodes (11): agrupar(), centros_completos(), correr(), describir(), perfiles(), DataFrame, Filas mensuales de centros (no agregados) y la lista de los que se excluyen por…, Una fila por centro, 12 columnas: ocupación de cada mes del año, 2022–2026… (+3 more)

### Community 32 - "Incidente crítico Modelos Estocásticos: Incertidumbre en la demanda turística"
Cohesion: 0.18
Nodes (12): Análisis de sensibilidad de variables (precio transporte, clima, tipo de cambio, sentimiento en redes), Asignación y optimización del presupuesto de la campaña, Desarrollo del branding de la marca, Entregable A: Campaña publicitaria del estado seleccionado, Incidente crítico Modelos Estocásticos: Incertidumbre en la demanda turística, Intervalo de confianza (90%) de la demanda esperada, Modelo de optimización para asignar presupuesto entre destinos, temporadas y canales sin rebasar capacidad de carga, ¿Promocionar varios destinos simultáneamente o concentrar recursos en uno solo bajo incertidumbre? (+4 more)

### Community 33 - "test_silver.py"
Cohesion: 0.17
Nodes (8): La ocupación que publica DataTur debe ser ocupados ÷ disponibles; se tolera 0.5…, El bloque duplicado 'Extranjero, sep-2025' (283 filas en cero) ya no está:…, 2,243 filas (todas las del CSV de conjunto_de_datos, sin descartar ninguna);…, Lo que INEGI reserva con '*' queda como nulo con reservado_flag, nunca como 0…, test_inah_sin_llaves_repetidas(), test_iter_filas_y_total_estatal(), test_iter_reservados_son_nulos_no_ceros(), test_ocupacion_publicada_coincide_con_calculada()

### Community 34 - "D6 DENUE INEGI (32 estados)"
Cohesion: 0.15
Nodes (16): A1 Radar (donde hay presion y espacio, hoy), Regla de oro: estimado != medido (sufijo _est), A1 Radar, D6 DENUE INEGI (32 estados), D7 Censo 2020 ITER Q. Roo, Presión de llegada medida (cruceristas + Tren Maya + cruces de Belice por habitación y por residente), Correccion de conteo (_filas_csv_en_zip excluye diccionario y catalogos), Índice de Presión Turística (+8 more)

### Community 35 - "D1 SITUR-Q API (45 indicadores)"
Cohesion: 0.17
Nodes (16): Regla 1: No inventar datos, D1 SITUR-Q API (45 indicadores), Hueco: sin ocupacion hotelera oficial 2025-2026, Indicador SITUR-Q 'Turista - Afluencia' roto (120/120 error 500), Regla 6 Silver: mes aereo con todos los aeropuertos en 0 = hueco, Regla 3 Silver: afluencia y derrama en 0 = hueco, Regla 4 Silver: los demas ceros se conservan, Regla 2 Silver: ocupacion con 0 habitaciones = hueco (+8 more)

### Community 36 - "Página web de la campaña"
Cohesion: 0.13
Nodes (22): Agrupamiento jerárquico de 55 centros del país, Cadena de Markov semanal del norte, Ceros imposibles como dato faltante, Sección: cómo llega la gente (avión, crucero, Belice, Tren Maya), El dato oficial tiene prioridad sobre la prensa, Serie de derrama económica descartada, Hallazgo: doble conteo INAH en SITUR-Q, Sección: dónde se queda el dinero (tamaño de hoteles) (+14 more)

### Community 37 - "Incidente crítico Almacenamiento de Grandes Volúmenes: Cuando los datos del turismo no caben en una sola computadora"
Cohesion: 0.18
Nodes (12): Arquitectura distribuida de Big Data, Integración de datos en tiempo real para ajustar la campaña (baja latencia), Incidente crítico Almacenamiento de Grandes Volúmenes: Cuando los datos del turismo no caben en una sola computadora, ¿Cómo diseñar una estrategia de almacenamiento de grandes volúmenes de datos turísticos heterogéneos, escalable y responsable?, Privacidad y riesgos de datos de movilidad/geolocalización de turistas, INEGI (2025). Cuenta Satélite del Turismo de México 2024, NIST (2020). Big data, Computer Security Resource Center, NIST SP 1500-1r2 (2019). Big Data Definitions (+4 more)

### Community 38 - "Incidente crítico Investigación de Operaciones: Optimización de los flujos turísticos para un desarrollo sustentable"
Cohesion: 0.18
Nodes (11): Criterio 6: Investigación de Operaciones (12%), Escenarios optimista, moderado y pesimista, Incidente crítico (dispositivo pedagógico de ética aplicada), Incidente crítico Investigación de Operaciones: Optimización de los flujos turísticos para un desarrollo sustentable, P4: Escenarios de redistribución sin reducir la actividad económica, Preguntas IO: ¿Qué significa que una distribución sea óptima? ¿Qué priorizar si los objetivos se contraponen?, Canca Ortiz & Villa Caro (2021). Introducción a la investigación de operaciones, Meyer Krumholz et al. (2002). Turismo y desarrollo sostenible (+3 more)

### Community 39 - "Incidente crítico Aprendizaje de Máquina: Turismo inteligente sustentable en México"
Cohesion: 0.12
Nodes (20): Criterio 9: Propuesta de solución e impacto (8%), Dilema: actividad económica vs. protección de recursos y comunidades, Incidente crítico Aprendizaje de Máquina: Turismo inteligente sustentable en México, Indicadores de desempeño e impacto, Modelo predictivo como producto de consultoría (suscripciones/licencias), ¿Cómo usar el aprendizaje de máquina para un turismo más inteligente sin aumentar la presión sobre recursos y comunidades?, ¿Cómo distribuir mejor los flujos turísticos para beneficiar a las comunidades y disminuir el impacto ambiental?, Si un algoritmo puede predecir dónde estarán los turistas, ¿puede ayudar a decidir dónde deberían estar? (+12 more)

### Community 40 - "descargar_datatur"
Cohesion: 0.29
Nodes (6): contar_filas(), descargar_datatur(), enlaces_de(), Devuelve las rutas de los .zip/.xlsx publicados en una página de DataTur, sin…, Cuenta las filas de todas las hojas de los Excel dentro de un zip (o de un…, Descarga todos los archivos de las categorías pedidas y los registra en el…

### Community 41 - "silver_datatur_ocupacion.py"
Cohesion: 0.22
Nodes (10): construir_silver_ocupacion(), leer_archivo(), _numero(), Path, SparkSession, Número o None. 'n.d.' / 'n.c.' / vacío → None., Lee un zip de DataTur (semanal o mensual) y devuelve una fila por centro y año., io (+2 more)

### Community 42 - "Índice de Presión Turística (IPT)"
Cohesion: 0.21
Nodes (12): Cortes por percentiles comunes p50/p90, Escala mín–máx común a todo el estado, Estados tranquilo / concurrido / saturado, Componente llegadas por cuarto (tren + cruceros), Pesos iguales con análisis de sensibilidad ±50 %, Ecuación del IPT (pesos iguales sobre componentes disponibles), Isolation Forest (A5 Torre en vivo), Modelo estocástico de dos etapas (Investigación de Operaciones) (+4 more)

### Community 43 - "Criterio de selección de modelo: más aciertos y más cambios anticipados"
Cohesion: 0.27
Nodes (11): Criterio de selección de modelo: más aciertos y más cambios anticipados, Sesgo: el modelo no se puede validar en los 5 lugares, Cadena de Markov semanal (matriz de transición, P^k, estacionaria), F1-macro y cambios anticipados, Gradient Boosting, Índice comparable IPT^c, Backtesting con origen móvil (12 reentrenamientos, 156 predicciones), Línea base de persistencia ŷ(t+1) = y(t) (+3 more)

### Community 44 - "Decisión 08 — A1 Radar (Fase 4)"
Cohesion: 0.16
Nodes (18): Decisión 08 — A1 Radar (Fase 4), Prueba de cifras de documentos (tests/test_documentos.py), Ecuaciones y 'cómo lo resolví', Regla de las cinco partes (ecuación, supuestos, método, ejemplo a mano, código), Documentación en cinco partes (ecuación, supuestos, resolución, ejemplo a mano, código), Índice de presión turística IPT_{d,t}, Fuentes excluidas (EVI, ENGATUR, OSM, Google Trends, TripAdvisor), Evidencia oficial: visitantes INAH en Q. Roo (BdINAH) (+10 more)

### Community 45 - "Hoja de ruta del proyecto"
Cohesion: 0.17
Nodes (13): Laguna Milagros 'sin dato oficial' en el Radar, Laguna Milagros y Xul-Ha, Regla: no inventar datos (huecos declarados), Conversión en Facebook para turismo: supuesto declarado, Construir todo desde cero, sin el proyecto anterior, Fase 10 — Pulido final de la página, Fase 11 — Cierre y coloquio, Fase 6 — Reparto del presupuesto (optimización) (+5 more)

### Community 46 - "pytest"
Cohesion: 0.20
Nodes (8): pytest, Dzibanché reabrió en feb-2025: de feb-2025 a jul-2026 son 18 meses; Oxtankah…, Chetumal 2024: 458,696 / 791,016 = 58.0 %. Maya Ka'an: 38.6 %. Norte: 73–77 %., Ruta sur: 66,628 visitantes / 6,098 residentes = 10.93; Tulum: 1,031,443 /…, test_ocupacion_2024_sin_promediar_porcentajes(), test_presion_por_residente(), test_regla_de_12_meses_abierta(), torre_base_entorno

### Community 47 - "test_radar_markov.py"
Cohesion: 0.22
Nodes (4): fixture, r(), P(saturado en 2 semanas | tranquilo hoy) = Σ_j p_tj · p_js = 0.922·0 +…, test_dos_semanas_a_mano()

### Community 48 - "test_radar_clustering.py"
Cohesion: 0.22
Nodes (5): fixture, r(), s(i) = (b − a) / máx(a, b): a = distancia media a su grupo, b = distancia media…, test_silueta_a_mano_cancun(), torre_radar

### Community 49 - "Sistema visual Sur mexicano"
Cohesion: 0.20
Nodes (10): Maqueta 3D en CSS + SVG (sin three.js), Claude Design (lienzo 'Torre del Caribe — rediseño web'), Greca escalonada maya, Paleta mexicana en bloques (rosa, cempasúchil, turquesa, añil...), Sistema visual Sur mexicano, Bricolage Grotesque + Figtree (locales, OFL), docs/DESIGN.md (estilo Flighty, histórico), Sección Cinco lugares (mapa 3D que sigue al scroll) (+2 more)

### Community 50 - "Decisión 06 — La página para público no técnico"
Cohesion: 0.29
Nodes (8): Pagina construida en paralelo a los datos, Decisión 06 — La página para público no técnico, Decisión 07 — Sistema visual "Sur mexicano", Asistente de preguntas rápidas (respuestas fijas), Dos frentes en paralelo: datos y página web, Página web: portada 'El sur tiene espacio', 5 lugares, ¿por qué el sur?, llegadas, dinero, 12 fases, quiénes somos, preguntas rápidas, Pretext (frontend/vendor/pretext.js), Contrato pagina.js (sin cifras a mano en el HTML)

### Community 51 - "silver_inah.py"
Cohesion: 0.43
Nodes (7): agregar_papel(), construir_silver_inah(), leer_inah(), DataFrame, quitar_duplicados(), Lee el Excel que viene dentro del zip más reciente de Bronze y pone nombres en…, Por cada llave repetida conserva la fila con cifra. Se detiene si hay dos…

### Community 52 - "Índice comparable (lo que publica el Radar)"
Cohesion: 0.50
Nodes (4): Índice comparable (lo que publica el Radar), Cadena de Markov semanal, solo norte, Predicción ago-2026: 5 lugares tranquilos; Mahahual 0.40 de saturarse, Sección de la página #radar '¿Dónde hay espacio hoy?'

### Community 53 - "Cifras oficiales conocidas verificadas"
Cohesion: 0.40
Nodes (5): INAH visitantes a zonas arqueológicas, Capacidad probada sin usar (Kohunlich 49 %), Cifras oficiales conocidas verificadas, Reseñas Rest-Mex 2025, Fase 8 — La campaña (reseñas, buyer persona, marca)

### Community 54 - "Depósitos Bronze / Silver / Gold"
Cohesion: 0.40
Nodes (5): Depósitos Bronze / Silver / Gold, DENUE del INEGI, Oferta turística por giros SCIAN (SECTUR/INEGI), Clima Open-Meteo, PySpark 3.5.6 + Java 17

### Community 55 - "Fase 7 — Torre en vivo"
Cohesion: 0.25
Nodes (9): Cap. 4 — Recolección de los datos oficiales (Fase 1): 15 fuentes, 353 archivos, 8,134,802 registros, Costos publicitarios WordStream / LocaliQ, Datos que no existen: ocupación SITUR-Q termina dic-2024; afluencia y derrama hasta mar-2024; 'Turista - Afluencia' no responde, Manifiesto con huella SHA-256, Navegador automatizado Playwright, Regla: ceros imposibles = dato faltante, Vigilancia del sargazo en la Bahía de Chetumal (canales al Caribe, no en la costa; pausa automática si llega), Fase 7 — Torre en vivo (+1 more)

### Community 56 - "Foco en 5 regiones (Chetumal, Calderitas–Oxtankah, Ruta arqueológica del sur, Maya Ka'an + Kantemó, Laguna Milagros–Xul-Ha)"
Cohesion: 0.25
Nodes (8): Capacidad probada sin usar K_s = 1 − V2025/V2019, Índice de Herfindahl-Hirschman (HHI y HHI*), Meses seguidos abierta A_z (criterio de cierres ≥12), Razón contra la población ρ, Selección de regiones con visitantes del INAH (§1), Tabla de criterios de las 5 regiones (§1-bis), Variación interanual ene–jul Δ%, Foco en 5 regiones (Chetumal, Calderitas–Oxtankah, Ruta arqueológica del sur, Maya Ka'an + Kantemó, Laguna Milagros–Xul-Ha)

### Community 57 - "Incidente crítico Mercadotecnia Digital: Estrategias digitales para la redistribución del turismo"
Cohesion: 0.25
Nodes (8): Incidente crítico Mercadotecnia Digital: Estrategias digitales para la redistribución del turismo, ¿Qué acciones implementar si la campaña genera una afluencia mayor a la capacidad del destino?, Preguntas detonadoras de Mercadotecnia Digital (mercado objetivo, medios, presupuesto, indicadores), Propuesta de valor del destino, SECTUR & SEMARNAT (2026). Decálogo para la inversión turística sustentable, SECTUR (2025). Programa Sectorial de Turismo 2025-2030, SECTUR (2026). 2025 marca un año histórico para el turismo en México, Simulación de Monte Carlo (riesgo de rebasar capacidad de carga)

### Community 58 - "v"
Cohesion: 0.25
Nodes (8): Chetumal trae 2 estaciones: 24 + 3,478 = 3,502 descensos en ene-2025., El total de zona Grand Costa Maya (7,084) es igual a la suma de sus destinos ya…, En 2025 SITUR-Q reporta 0 habitaciones disponibles (imposible): debe ser hueco,…, test_bacalar_ocupacion_ene_2024(), test_ocupacion_2025_es_hueco_no_cero(), test_tren_maya_suma_estaciones_chetumal(), test_tren_maya_zona_igual_suma_destinos(), v()

### Community 59 - "04 - Limpieza y orden de los datos (Fase 2: Silver y Gold)"
Cohesion: 0.29
Nodes (10): A5 Torre en vivo (que hace la campana esta semana), D2/D2m DataTur ocupacion hotelera semanal y mensual, Corrección de conteo: DENUE 6,138,075 e ITER 2,243, 04 - Limpieza y orden de los datos (Fase 2: Silver y Gold), Bandera de comparabilidad (notas al pie DataTur), DENUE procesado completo (6,138,075 negocios), Fuentes que no coinciden: Isla Mujeres (prensa vs DataTur), DataTur: una version por periodo (gana la mas reciente) (+2 more)

### Community 60 - "Estado de las fases (28-sep-2026)"
Cohesion: 0.20
Nodes (11): HURDAT2 (huracanes 1851–2025), El sur se mide con presión de llegada medida, sin estimar ocupación, Estado de las fases (28-sep-2026), Fase 2 — Limpieza y orden de los datos (Silver/Gold), Fase 3 — Planteamiento con datos (tabla de criterios; cómo medir presión sin ocupación), Fase 4 — Radar (¿dónde hay espacio?), Fase 5 — Pronóstico, Fases 9-11 — conexión backend, pulido y cierre (+3 more)

### Community 61 - "Opción D: ocupación DataTur + componente en ≥2 lugares"
Cohesion: 0.29
Nodes (7): Cruces de Belice (solo Chetumal), DataTur (ocupación semanal, Sectur), Opción D: ocupación DataTur + componente en ≥2 lugares, Prueba de validez del índice, Prueba de validez del IPT (comparar_escalas, variantes A–D), Quiebre de 2025 (pérdida de ocupación SITUR-Q), DataTur y SITUR-Q no miden lo mismo (reconciliación)

### Community 62 - "Decisión 05: Planteamiento con datos (Fase 3)"
Cohesion: 0.29
Nodes (7): Crisis de Tulum (ventas −60 %), Decisión 3: no promover playa en 2026, Destinos saturados/limitados: Cozumel, Isla Mujeres, Holbox, Sargazo récord 2026 (>104,700 t; 56 de 140 playas en rojo), Decisión 05: Planteamiento con datos (Fase 3), REGIONES.md — Selección de regiones con evidencia 2026, Regiones excluidas (Tulum, Playa, Mahahual, Cozumel, Isla Mujeres, Holbox, Cancún, Bacalar)

### Community 63 - "DataFrame"
Cohesion: 0.48
Nodes (7): censo(), datatur(), denue(), inah(), DataFrame, fixture, siturq()

### Community 64 - "pathlib"
Cohesion: 0.47
Nodes (4): Notebook 02_radar, nbclient, nbformat, pathlib

### Community 65 - "09 — Auditoría de las Fases 1 a 4 contra el plan"
Cohesion: 0.33
Nodes (6): 09 — Auditoría de las Fases 1 a 4 contra el plan, Manifiesto Bronze (377 archivos; 353 fuentes oficiales, 8,134,802 registros), Reproducibilidad (8 tablas Gold idénticas, SEMILLA = 0), Primer commit a GitHub (datos crudos fuera), Veredicto: Fases 1, 3 y 4 completas; Fase 2 incompleta, Revisión completa de las fases 1 a 4

### Community 66 - "Decisiones cerradas hasta hoy (A.8)"
Cohesion: 0.29
Nodes (7): Diferencia DataTur vs SITUR-Q se declara, no se ajusta, Chat de preguntas rápidas (respuestas fijas, no IA), Sección 'Con datos oficiales' y tabla de criterios, Decisiones cerradas hasta hoy (A.8), Oferta turística DENUE = giros SCIAN 721, 722, 5615, 487, 712, 713, Regla 6 de Silver: mes aéreo con todos en 0 es hueco, Regla de oro: no inventar datos; hueco se declara

### Community 67 - "03 - Ingesta de fuentes oficiales (Fase 1: Bronze)"
Cohesion: 0.47
Nodes (6): 03 - Ingesta de fuentes oficiales (Fase 1: Bronze), Evidencia de sargazo en la Bahia de Chetumal (ECOSUR, Reportur), Hueco: conversión de Facebook para Travel no publicada, Extraccion con Playwright + Chromium (benchmarks y sargazo), Fase 1: 353 archivos, 8,134,802 registros, 824 MB, D13 Benchmarks de costo por canal (WordStream / LocaliQ)

### Community 69 - "Limitación: quiebre de 2025 (SITUR-Q deja de publicar ocupación)"
Cohesion: 0.67
Nodes (3): Predecir con el índice comparable (decisión 7), Limitación: quiebre de 2025 (SITUR-Q deja de publicar ocupación), SITUR-Q (Gobierno de Quintana Roo)

### Community 70 - "Clustering jerárquico Ward de 55 centros DataTur"
Cohesion: 0.67
Nodes (3): Clustering de centros del país (faltaba contra el plan), Clustering jerárquico Ward de 55 centros DataTur, Coeficiente de silueta

## Knowledge Gaps
- **177 isolated node(s):** `MESES`, `MUNICIPIOS_LUGARES`, `VISTA_GENERAL`, `mapa`, `MODULOS` (+172 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 450 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `README Torre del Caribe` connect `README Torre del Caribe` to `PLAN_v3.md (plan aprobado)`, `Decisión 08 — A1 Radar (Fase 4)`, `Inventario de datos - fuentes oficiales verificadas`, `ingesta_datatur.py`, `Decisión 05: Planteamiento con datos (Fase 3)`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `PLAN_v3.md (plan aprobado)` connect `PLAN_v3.md (plan aprobado)` to `Decisión: la campaña promueve 5 regiones de Quintana Roo`, `D6 DENUE INEGI (32 estados)`, `Decisión 08 — A1 Radar (Fase 4)`, `Inventario de datos - fuentes oficiales verificadas`, `README Torre del Caribe`, `Problema Prototípico: Turismo inteligente sustentable para México`, `CLAUDE.md - Reglas del repositorio Torre del Caribe`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `frontend/index.html (página pública)` connect `frontend/index.html (página pública)` to `Decisiones cerradas hasta hoy (A.8)`, `datos_pagina.py`, `app.js`, `panel.py`, `Sistema visual Sur mexicano`, `Decisión 06 — La página para público no técnico`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Inventario de datos - fuentes oficiales verificadas` (e.g. with `DataTur: 135 archivos semanales de ocupación (2024-S01 → 2026-S31, 7 centros de Q. Roo)` and `SITUR-Q: API con 45 indicadores`) actually correct?**
  _`Inventario de datos - fuentes oficiales verificadas` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `MESES`, `MUNICIPIOS_LUGARES`, `VISTA_GENERAL` to the rest of the system?**
  _177 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `PLAN_v3.md (plan aprobado)` be split into smaller, more focused modules?**
  _Cohesion score 0.06291591046581972 - nodes in this community are weakly interconnected._
- **Should `Decisión: la campaña promueve 5 regiones de Quintana Roo` be split into smaller, more focused modules?**
  _Cohesion score 0.07003367003367003 - nodes in this community are weakly interconnected._