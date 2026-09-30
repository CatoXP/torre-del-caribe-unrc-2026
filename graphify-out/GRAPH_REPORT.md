# Graph Report - PP 5to semestre CASCO SANTO TOMAS  (2026-09-30)

## Corpus Check
- 0 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1360 nodes · 2411 edges · 114 communities (78 shown, 36 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 221 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- prediccion.py
- Planteamiento: concentración y HHI
- entorno.py
- ingesta_abiertas.py
- test_ingesta.py
- test_pagina.py
- datos_pagina.py
- Fotos y ubicación comprobada
- test_radar_clustering.py
- silver_datatur_ocupacion.py
- Pronóstico: series a pronosticar
- markov.py
- Entorno: Spark, JDK y prueba de humo
- silver_iter.py
- ingesta_siturq.py
- silver_denue.py
- test_planteamiento.py
- Pronóstico: pruebas de las series
- test_radar_panel.py
- test_radar_prediccion.py
- pathlib
- test_radar_indice.py
- Página: generador de datos
- test_silver.py
- 03 - Ingesta de fuentes oficiales (Fase 1: Bronze)
- app.js
- sys
- frontend/index.html (página pública)
- pandas
- Entorno: búsqueda de JDK
- silver_inah.py
- v
- Página: cuartos vacíos y chat
- descargar_datatur
- Silver Censo (ITER)
- DataFrame
- figuras.py
- Página: las 12 fases
- Página: dónde se queda el dinero
- Página: así llega la gente
- panel.py
- test_qroo_239_semanas
- test_nota_isla_mujeres
- test_denue_total_nacional
- test_denue_turisticos_qroo
- test_denue_sin_datos_personales
- test_inah_cifras_de_la_seleccion_de_regiones
- test_inah_kohunlich_crece_en_2026
- test_inah_papel_de_las_zonas
- test_iter_poblacion_de_las_5_regiones
- test_silver_fase5.py
- test_cero_real_se_conserva
- test_regla_6_aereos
- test_afluencia_y_derrama_terminan_en_marzo_2024
- test_cancun_semana_31_2026
- PLAN_v3.md (plan aprobado)
- Inventario de datos - fuentes oficiales verificadas
- Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan
- Decisión: la campaña promueve 5 regiones de Quintana Roo
- D6 DENUE INEGI (32 estados)
- 04 - Limpieza y orden de los datos (Fase 2: Silver y Gold)
- Reglas de oro (a–h)
- Ingesta: costos publicitarios y sargazo
- Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)
- 09 — Auditoría de las Fases 1 a 4 contra el plan
- Documento ejecutivo (DOCUMENTO_EJECUTIVO.md → PDF)
- Problema Prototípico: Turismo inteligente sustentable para México
- Opción D: ocupación DataTur + componente en ≥2 lugares
- Flighty — Style Reference (sistema de diseño)
- Decisión 2: Quintana Roo y fusión A1 + A3 + A5
- CLAUDE.md - Reglas del repositorio Torre del Caribe
- D1 SITUR-Q API (45 indicadores)
- Cap. 2 — El problema en números: ¿a dónde van los turistas?
- Estados tranquilo / concurrido / saturado
- Radar: panel mensual
- Regiones excluidas y sargazo
- Limitación: quiebre de 2025 (SITUR-Q deja de publicar ocupación)
- Hallazgo: zonas arqueológicas SITUR-Q = INAH agrupado por destino
- markov.py (DataFrame)
- datos_pagina.py (date)
- fixture
- figuras.py (Path)
- 10 — Datos limpios para el Pronóstico: huracanes, clima y tipo de cambio (Fase 2, cierre de la parte que usa la Fase 5)
- Contrato pagina.js y módulos ocultos
- DataFrame (DataFrame)
- SparkSession
- Decisiones cerradas (A.8)
- Fase 7 — Torre en vivo
- Regla de cierres: ≥12 meses seguidos abierta y sin cierres en 2026
- Clustering jerárquico Ward de 55 centros DataTur
- Rúbrica de evaluación (11 criterios, 100%)
- Incidente crítico Modelos Estocásticos: Incertidumbre en la demanda turística
- Incidente crítico Almacenamiento de Grandes Volúmenes: Cuando los datos del turismo no caben en una sola computadora
- Incidente crítico Investigación de Operaciones: Optimización de los flujos turísticos para un desarrollo sustentable
- Decisión 08 — A1 Radar (Fase 4)
- Página: secciones (documento ejecutivo)
- Criterio de selección de modelo: más aciertos y más cambios anticipados
- Incidente crítico Aprendizaje de Máquina: Turismo inteligente sustentable en México
- Sistema visual Sur mexicano
- Preguntas del Problema Prototípico
- Incidente crítico Mercadotecnia Digital: Estrategias digitales para la redistribución del turismo
- Cap. 3 — Preparación del equipo de cómputo (Fase 0)
- Error MAPE
- Gradient Boosting (Radar y Pronóstico)
- Rest-Mex 2025 (reseñas de viajeros)

## God Nodes (most connected - your core abstractions)
1. `Flighty — Style Reference (sistema de diseño)` - 49 edges
2. `Inventario de datos - fuentes oficiales verificadas` - 33 edges
3. `frontend/index.html (página pública)` - 27 edges
4. `Problema Prototípico: Turismo inteligente sustentable para México` - 27 edges
5. `04 - Limpieza y orden de los datos (Fase 2: Silver y Gold)` - 25 edges
6. `Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan` - 24 edges
7. `PLAN_v3.md (plan aprobado)` - 24 edges
8. `CLAUDE.md - Reglas del repositorio Torre del Caribe` - 21 edges
9. `Incidente crítico Aprendizaje de Máquina: Turismo inteligente sustentable en México` - 20 edges
10. `Decisión: la campaña promueve 5 regiones de Quintana Roo` - 18 edges

## Surprising Connections (you probably didn't know these)
- `Corrección de conteo: DENUE 6,138,075 e ITER 2,243` --references--> `_filas_csv_en_zip()`  [EXTRACTED]
  docs/decisiones/03-ingesta.md → backend/torre/base/ingesta_abiertas.py
- `Sección Cinco lugares (mapa 3D que sigue al scroll)` --shares_data_with--> `fichas_regiones()`  [INFERRED]
  frontend/index.html → backend/torre/api/datos_pagina.py
- `Sección Mientras tanto, en el norte (referencia)` --shares_data_with--> `referencia_norte()`  [INFERRED]
  frontend/index.html → backend/torre/api/datos_pagina.py
- `Sección El dato (4 de cada 10 cuartos)` --shares_data_with--> `cuartos_vacios_chetumal()`  [INFERRED]
  frontend/index.html → backend/torre/api/datos_pagina.py
- `Destinos saturados/limitados: Cozumel, Isla Mujeres, Holbox` --conceptually_related_to--> `Capacidad de carga del destino`  [INFERRED]
  docs/decisiones/00-fundacion.md → PROBLEMA PROTOTÍPICO 5°- LCDN-2026-2.pdf

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Arquitectura de datos Bronze -> Silver -> Gold con PySpark** — docs_ejecutivo_documento_ejecutivo_manifiesto_sha256 [EXTRACTED 0.95]
- **Flujo del Radar: panel mensual -> índice -> índice comparable -> predicción y Markov** — docs_ejecutivo_documento_ejecutivo_indice_comparable [EXTRACTED 0.95]
- **Cadena de integración de las seis UCA en la campaña publicitaria inteligente** — problema_prototípico_5_lcdn_2026_2_evidencia_integradora, problema_prototípico_5_lcdn_2026_2_incidente_big_data, problema_prototípico_5_lcdn_2026_2_incidente_mineria_datos, problema_prototípico_5_lcdn_2026_2_incidente_aprendizaje_maquina, problema_prototípico_5_lcdn_2026_2_incidente_estocasticos, problema_prototípico_5_lcdn_2026_2_incidente_investigacion_operaciones, problema_prototípico_5_lcdn_2026_2_incidente_mercadotecnia_digital, problema_prototípico_5_lcdn_2026_2_campana_publicitaria_inteligente [EXTRACTED 1.00]
- **Las 5 regiones que promueve la campaña** — docs_regiones_regiones_chetumal, docs_regiones_regiones_bahia_calderitas_oxtankah, docs_plan_plan_v3_region_ruta_arqueologica_sur, docs_regiones_regiones_maya_kaan_interior_kantemo, docs_regiones_regiones_laguna_milagros_xul_ha [EXTRACTED 1.00]
- **Las 5 regiones vigentes a promover (Parte G / Regla 9)** — docs_plan_plan_v3_region_chetumal, docs_regiones_regiones_bahia_calderitas_oxtankah, docs_plan_plan_v3_region_ruta_arqueologica_sur, docs_plan_plan_v3_region_maya_kaan_kantemo, docs_regiones_regiones_laguna_milagros_xul_ha [EXTRACTED 1.00]
- **Contrato del cascarón: datos por fase a la página** — docs_decisiones_06_pagina_contrato_cascaron, frontend_index_modulos_data_clave, frontend_datos_pagina, frontend_app_dibujar, frontend_index_fases [EXTRACTED 1.00]
- **Las cinco regiones de la campaña** — docs_regiones_regiones_chetumal, docs_ejecutivo_documento_ejecutivo_bahia_calderitas_oxtankah, docs_plan_plan_v3_region_ruta_arqueologica_sur, docs_regiones_regiones_maya_kaan_interior_kantemo, docs_ejecutivo_documento_ejecutivo_laguna_milagros_xul_ha [EXTRACTED 1.00]
- **Insumos externos del Pronóstico (clima, huracanes, tipo de cambio)** — docs_ejecutivo_documento_ejecutivo_fuente_open_meteo, docs_ejecutivo_documento_ejecutivo_fuente_noaa_huracanes, docs_ejecutivo_documento_ejecutivo_fuente_fred_tipo_cambio, docs_ejecutivo_documento_ejecutivo_pronostico [EXTRACTED 1.00]
- **Comparación de formas de predecir el estado del Radar** — docs_ejecutivo_documento_ejecutivo_persistencia, docs_ejecutivo_documento_ejecutivo_regresion_logistica, docs_ejecutivo_documento_ejecutivo_random_forest_gradient_boosting, docs_metodologia_ecuaciones_cadena_markov_semanal [EXTRACTED 1.00]
- **Pipeline del Radar: índice, estados, predicción y Markov** — docs_ejecutivo_documento_ejecutivo_indice_comparable, docs_decisiones_08_radar_estados_radar, docs_ejecutivo_documento_ejecutivo_regresion_logistica, docs_ejecutivo_documento_ejecutivo_agrupamiento_jerarquico [EXTRACTED 1.00]
- **Tres módulos que alimentan la campaña (Radar, Pronóstico, Torre en vivo)** — docs_ejecutivo_documento_ejecutivo_radar, docs_ejecutivo_documento_ejecutivo_pronostico, docs_ejecutivo_documento_ejecutivo_torre_en_vivo, docs_ejecutivo_documento_ejecutivo_campana_basada_en_datos [EXTRACTED 1.00]
- **Identidad visual UNRC aplicada al documento ejecutivo** — docs_ejecutivo_guia_estilo_unrc_color_guinda, docs_ejecutivo_guia_estilo_unrc_color_dorado, docs_ejecutivo_guia_estilo_unrc_tipografia_patria, docs_ejecutivo_guia_estilo_unrc_tipografia_noto_sans, docs_ejecutivo_guia_estilo_unrc_regla_nunca_texto_negro [EXTRACTED 1.00]
- **Estafeta A3 → A1 → A5 → Campaña** — docs_plan_plan_v3_a3_pronostico, docs_plan_plan_v3_a1_radar, docs_plan_plan_v3_a5_torre_en_vivo, docs_plan_plan_v3_programacion_estocastica_dos_etapas [EXTRACTED 1.00]
- **Evidencia para no promover playa en 2026** — docs_decisiones_00_fundacion_sargazo_2026, docs_decisiones_00_fundacion_crisis_tulum, docs_decisiones_00_fundacion_destinos_saturados, docs_decisiones_00_fundacion_decision_no_playa [EXTRACTED 1.00]
- **Colores de señal y componentes que los usan (acción, conversión, alerta)** — docs_design_signal_light_color_system, docs_design_color_signal_blue, docs_design_color_amber_alert, docs_design_color_alert_red, docs_design_primary_blue_button, docs_design_amber_download_button, docs_design_floating_notification_card [EXTRACTED 1.00]
- **Flujo de datos: Bronze → Silver → Gold → DuckDB/Streaming → API → página** — docs_plan_plan_v3_lakehouse_bronze_silver_gold, docs_plan_plan_v3_duckdb_sobre_gold, docs_plan_plan_v3_spark_structured_streaming, docs_plan_plan_v3_backend_fastapi_endpoints, docs_plan_plan_v3_pagina_web_recorrido [EXTRACTED 1.00]
- **Módulos futuros ocultos que se encienden con su clave de pagina.js** — frontend_index_seccion_radar, frontend_index_modulo_pronostico, frontend_index_modulos_envivo_escenarios_presupuesto, frontend_index_modulo_campana, frontend_index_patron_data_clave, frontend_datos_pagina [EXTRACTED 1.00]
- **Insumos Silver externos de la Fase 5 (huracanes, clima, tipo de cambio)** — docs_decisiones_10_silver_fase5_hurdat2, docs_decisiones_10_silver_fase5_clima_era5, docs_decisiones_10_silver_fase5_fred_dexmxus, docs_decisiones_10_silver_fase5_cpiaucsl [EXTRACTED 1.00]
- **Los 6 incidentes críticos del Problema Prototípico** — objetivo_incidente_estocasticos, objetivo_incidente_io, objetivo_incidente_big_data, objetivo_incidente_ml, objetivo_incidente_mineria, objetivo_incidente_mercadotecnia [EXTRACTED 1.00]
- **Pila del entorno Fase 0 (PySpark 3.5.6 + JDK 17 + winutils 3.3.6 + .venv)** — docs_decisiones_02_entorno_pyspark_3_5_6, docs_decisiones_02_entorno_jdk_17, docs_decisiones_02_entorno_winutils_hadoop_dll, docs_decisiones_02_entorno_venv_aislado, backend_torre_base_entorno, docs_decisiones_02_entorno_prueba_de_humo [EXTRACTED 1.00]
- **Piezas del Pronóstico A3 (series, modelos, estocástico)** — docs_decisiones_11_pronostico_pronostico_series_parquet, docs_decisiones_11_pronostico_descomposicion_estacional, docs_metodologia_ecuaciones_holt_winters, docs_decisiones_11_pronostico_regresion_con_clima, docs_decisiones_11_pronostico_gradient_boosting_rezagos, docs_metodologia_ecuaciones_intervalo_conformal, docs_metodologia_ecuaciones_poisson_huracanes, docs_metodologia_ecuaciones_monte_carlo_escenarios [EXTRACTED 1.00]
- **Flujo del Radar: panel → IPT → índice comparable → predicción del estado** — docs_decisiones_08_radar_panel_mensual, docs_plan_plan_v3_indice_presion_turistica, docs_decisiones_08_radar_indice_comparable, docs_metodologia_ecuaciones_regresion_logistica_multiclase, docs_decisiones_08_radar_prediccion_agosto_2026, docs_decisiones_08_radar_seccion_donde_hay_espacio_hoy [EXTRACTED 1.00]
- **Predicción del estado del mes siguiente del Radar (modelos comparados en origen móvil)** — docs_metodologia_ecuaciones_persistencia_linea_base, docs_metodologia_ecuaciones_regresion_logistica_multiclase, docs_metodologia_ecuaciones_random_forest, docs_metodologia_ecuaciones_gradient_boosting, docs_metodologia_ecuaciones_backtesting_origen_movil, docs_metodologia_ecuaciones_f1_macro [EXTRACTED 1.00]
- **Tres horizontes: Radar, Pronóstico y Torre en vivo alimentando la campaña** — docs_plan_plan_v3_a1_radar, docs_plan_plan_v3_a3_pronostico, docs_plan_plan_v3_a5_torre_en_vivo, docs_plan_plan_v3_campana_mercadotecnia, docs_plan_plan_v3_estafeta_entre_modulos [EXTRACTED 1.00]
- **Huecos declarados en lugar de inventar datos** — docs_ejecutivo_documento_ejecutivo_sin_flechas_od, docs_ejecutivo_documento_ejecutivo_derrama_no_usada, docs_decisiones_08_radar_laguna_sin_dato, docs_ejecutivo_documento_ejecutivo_regla_ceros_hueco, docs_plan_hoja_de_ruta_conversion_facebook_supuesto [INFERRED 0.85]
- **Modo oscuro 'sala de control' de Flighty** — docs_design_light_to_dark_transition, docs_design_color_deep_indigo, docs_design_color_midnight_ink, docs_design_press_logo_card, docs_design_dark_ghost_button, docs_design_section_divider_band, docs_design_gradient_system [INFERRED 0.85]
- **Flujo de publicación: datos_pagina → pagina.js → index.html → GitHub Pages** — backend_torre_api_datos_pagina, frontend_datos_pagina, frontend_index, _github_workflows_pagina, readme_pagina_en_linea [INFERRED 0.85]
- **Huecos y diferencias de datos que se declaran en vez de rellenarse** — objetivo_regla_no_inventar_datos, docs_decisiones_08_radar_laguna_milagros_sin_dato_oficial, docs_decisiones_08_radar_quiebre_de_2025, docs_decisiones_08_radar_datatur_menor_que_situr_q_declarado, objetivo_regla_6_de_silver, docs_decisiones_09_auditoria_fases_1_4_sesgo_norte_sur [INFERRED 0.85]
- **Reglas de Silver para distinguir hueco de cero real** — docs_decisiones_04_silver_regla_ocupacion_hueco, docs_decisiones_04_silver_regla_afluencia_derrama_hueco, docs_decisiones_04_silver_regla_ceros_reales, docs_decisiones_04_silver_regla_6_aereos, claude_regla_no_inventar_datos [INFERRED 0.85]

## Communities (114 total, 36 thin omitted)

### Community 1 - "prediccion.py"
Cohesion: 0.05
Nodes (58): calcular(), componentes(), elegir_componentes(), estados(), guardar(), ipt(), minmax(), sensibilidad() (+50 more)

### Community 10 - "Planteamiento: concentración y HHI"
Cohesion: 0.08
Nodes (34): actores(), _anio_completo(), comprobar_zonas(), concentracion(), agregar(), cuotas_y_hhi(), _fila(), inventario_variables() (+26 more)

### Community 11 - "entorno.py"
Cohesion: 0.14
Nodes (23): clima_diario(), clima_horario(), construir_silver_clima(), _leer(), _papel(), construir_silver_fred(), mensual(), _serie() (+15 more)

### Community 12 - "ingesta_abiertas.py"
Cohesion: 0.14
Nodes (22): _bajar(), _bajar_con_espera(), clima(), denue(), descargar_abiertas(), endutih(), _es_zip(), _filas_csv_en_zip() (+14 more)

### Community 13 - "test_ingesta.py"
Cohesion: 0.14
Nodes (21): filas_manifiesto(), test_benchmarks_travel_google_2025(), test_denue_32_estados(), test_geojson_11_municipios(), test_inah_tulum_2025(), test_manifiesto_huellas_coinciden(), test_restmex_208051_resenas(), test_siturq_bacalar_145_hoteles_ene_2025() (+13 more)

### Community 14 - "test_pagina.py"
Cohesion: 0.09
Nodes (16): datos(), test_cuartos_vacios_chetumal(), test_fotos_con_credito_y_licencia_libre(), test_hueco_declarado_en_la_laguna(), test_movimiento_cifras_conocidas(), test_preguntas_sin_precios_inventados(), test_radar_solo_5_lugares_y_referencias(), test_ubicaciones_en_quintana_roo() (+8 more)

### Community 15 - "datos_pagina.py"
Cohesion: 0.17
Nodes (17): _cifra(), evidencia_pagina(), ultimo_mes(), fichas_regiones(), _mes(), _negocios_por_region(), _pruebas_automaticas(), radar() (+9 more)

### Community 16 - "Fotos y ubicación comprobada"
Cohesion: 0.15
Nodes (17): descargar_fotos(), _limpiar(), _pedir(), _slug(), _dentro(), municipio_de(), verificar_regiones(), DataFrame (+9 more)

### Community 17 - "test_radar_clustering.py"
Cohesion: 0.11
Nodes (10): r(), test_silueta_a_mano_cancun(), r(), test_dos_semanas_a_mano(), fixture, fixture, s(i) = (b − a) / máx(a, b): a = distancia media a su grupo, b = distancia media…, P(saturado en 2 semanas | tranquilo hoy) = Σ_j p_tj · p_js = 0.922·0 +… (+2 more)

### Community 18 - "silver_datatur_ocupacion.py"
Cohesion: 0.16
Nodes (15): crear_spark(), construir_silver_ocupacion(), leer_archivo(), _numero(), Path, SparkSession, Crea una sesión de Spark local que usa todos los núcleos de la máquina.…, Número o None. 'n.d.' / 'n.c.' / vacío → None. (+7 more)

### Community 19 - "Pronóstico: series a pronosticar"
Cohesion: 0.20
Nodes (17): construir(), guardar(), _motivos_zona(), _pandemia(), resumen(), serie_belice(), serie_cancun(), series_inah() (+9 more)

### Community 2 - "markov.py"
Cohesion: 0.05
Nodes (59): a_k_semanas(), backtest(), correr(), estacionaria(), estados(), matriz(), ocupacion_semanal(), transiciones() (+51 more)

### Community 20 - "Entorno: Spark, JDK y prueba de humo"
Cohesion: 0.17
Nodes (15): test_spark_lee_csv_y_escribe_parquet(), 02 — Entorno de trabajo (Fase 0: cimientos), JDK 17 (OpenJDK 17.0.20.1 de Microsoft), Prueba de humo Fase 0 (22.93 s, suma = 6), PySpark 3.5.6 (no 4.x), winutils.exe + hadoop.dll 3.3.6 (herramientas/hadoop/bin), Decisión Fase 0: .venv (Python 3.11.9) + PySpark 3.5.6 + JDK 17 + winutils/hadoop.dll 3.3.6, Opción descartada: cambiar el Java de todo Windows (+7 more)

### Community 21 - "silver_iter.py"
Cohesion: 0.15
Nodes (16): calcular_criterios(), _meses_abierta(), _ocupacion_2024(), tabla(), DataFrame, fixture, Ocupación hotelera de 2024 = Σ cuartos ocupados / Σ cuartos disponibles (nunca…, Meses seguidos abierta (hasta el último mes publicado) de la zona MENOS abierta… (+8 more)

### Community 24 - "ingesta_siturq.py"
Cohesion: 0.17
Nodes (14): consultar(), descargar_siturq(), leer_catalogo(), registrar(), sha256_de(), Path, Descarga todos los INDICADORES × unidades × años y guarda un archivo JSON crudo…, Lee la página pública y extrae el token, los destinos y las zonas tal como los… (+6 more)

### Community 25 - "silver_denue.py"
Cohesion: 0.17
Nodes (14): construir_silver_denue(), descomprimir(), a_snake(), construir_silver_siturq(), leer_indicador(), Path, DataFrame, Path (+6 more)

### Community 28 - "test_planteamiento.py"
Cohesion: 0.13
Nodes (12): conc(), test_ejemplo_a_mano_aviones(), test_hhi_casos_extremos(), test_poblacion_de_los_5_lugares_cuadra_con_criterios(), test_zonas_no_son_suma_de_miembros(), DataFrame, fixture, Reparto parejo → HHI = 1/N y HHI* = 0; una unidad dominante → HHI* cerca de 1. (+4 more)

### Community 29 - "Pronóstico: pruebas de las series"
Cohesion: 0.20
Nodes (12): mes(), t(), test_cancun_ocupacion_calculada_con_cuartos(), test_cierre_no_es_cero_demanda(), test_ichkabal_nuevo_no_es_cierre(), test_mes_parcial_al_reabrir(), test_pandemia(), test_region_cerrada_si_una_zona_cierra() (+4 more)

### Community 30 - "test_radar_panel.py"
Cohesion: 0.15
Nodes (11): _anual(), p(), test_cifras_conocidas(), test_inah_sin_doble_conteo(), test_laguna_sin_datos_se_declara(), test_ocupacion_no_suma_filas(), DataFrame, fixture (+3 more)

### Community 31 - "test_radar_prediccion.py"
Cohesion: 0.14
Nodes (9): r(), test_f1_macro_a_mano(), test_indice_comparable_sin_quiebre(), test_sesgo_5_lugares_casi_sin_cambios(), fixture, Cada lugar usa siempre las mismas medidas: Chetumal, tren por habitante y…, ECUACIONES.md §2.2: F1 por clase con la matriz de confusión de la regresión…, Auditoría: en los 12 meses de prueba los 5 lugares casi no cambiaron de estado;… (+1 more)

### Community 32 - "pathlib"
Cohesion: 0.22
Nodes (10): armar(), exportar_html(), date, Path, Notebook 02_radar, nbclient, nbconvert, nbformat (+2 more)

### Community 35 - "test_radar_indice.py"
Cohesion: 0.15
Nodes (9): r(), test_ejemplo_a_mano_cancun(), test_ipt_de_juguete(), test_validez_norte_arriba_del_sur_2025_2026(), fixture, Pesos iguales solo sobre lo que existe: (0.2 + 0.6) / 2 = 0.4; una fila sin…, ECUACIONES.md §2.1: Cancún jul-2026 → (0.0497 + 0.0001 + 0.0011 + 0.7214) / 4 =…, La prueba que falló con mín–máx sin DataTur: en 2025–2026 el norte de… (+1 more)

### Community 36 - "Página: generador de datos"
Cohesion: 0.17
Nodes (12): concentracion_pagina(), criterios(), _foto_portada(), generar(), mapa_municipios(), Path, Polígonos de los 11 municipios, redondeados a 3 decimales (unos 100 m) para que…, Foto de la portada con su crédito (frontend/fotos/creditos.json,… (+4 more)

### Community 42 - "test_silver.py"
Cohesion: 0.17
Nodes (8): test_inah_sin_llaves_repetidas(), test_iter_filas_y_total_estatal(), test_iter_reservados_son_nulos_no_ceros(), test_ocupacion_publicada_coincide_con_calculada(), La ocupación que publica DataTur debe ser ocupados ÷ disponibles; se tolera 0.5…, El bloque duplicado 'Extranjero, sep-2025' (283 filas en cero) ya no está:…, 2,243 filas (todas las del CSV de conjunto_de_datos, sin descartar ninguna);…, Lo que INEGI reserva con '*' queda como nulo con reservado_flag, nunca como 0…

### Community 43 - "03 - Ingesta de fuentes oficiales (Fase 1: Bronze)"
Cohesion: 0.27
Nodes (8): capturar_evidencia(), a_numero(), descargar_benchmarks(), Visita cada fuente, guarda HTML + captura + párrafos relevantes y devuelve esos…, $2.12' → 2.12 · '8.73%' → 8.73 · ' $44.70' → 44.70. Devuelve None si no hay…, csv, datetime, playwright_sync_api

### Community 5 - "app.js"
Cohesion: 0.09
Nodes (38): acercarA(), alAparecer(), alternarGiro(), arrastrar(), camara(), capitulos(), cifrasDe(), construirMapa() (+30 more)

### Community 53 - "sys"
Cohesion: 0.20
Nodes (8): test_ocupacion_2024_sin_promediar_porcentajes(), test_presion_por_residente(), test_regla_de_12_meses_abierta(), Dzibanché reabrió en feb-2025: de feb-2025 a jul-2026 son 18 meses; Oxtankah…, Chetumal 2024: 458,696 / 791,016 = 58.0 %. Maya Ka'an: 38.6 %. Norte: 73–77 %., Ruta sur: 66,628 visitantes / 6,098 residentes = 10.93; Tulum: 1,031,443 /…, sys, torre_base_entorno

### Community 54 - "frontend/index.html (página pública)"
Cohesion: 0.33
Nodes (9): MODULOS, frontend/index.html (página pública), EQUIPO, Sección Quiénes somos (#equipo), Módulo 'La campaña' (Fase 8, oculto), Módulo pronóstico (Fase 5, oculto), Módulos ocultos: en vivo, escenarios, presupuesto, Sección #radar '¿Dónde hay espacio hoy?' (Fase 4) (+1 more)

### Community 57 - "pandas"
Cohesion: 0.25
Nodes (8): cifras(), test_cifra_escrita_coincide_con_el_calculo(), textos(), parametrize, fixture, Cada cifra recalculada desde Gold o desde las funciones, con el formato con que…, pytest, Auditoría de las Fases 1–4 (20 cifras de documentos = código)

### Community 59 - "Entorno: búsqueda de JDK"
Cohesion: 0.25
Nodes (7): buscar_jdk17(), configurar_entorno(), _ruta_corta(), Path, Busca un JDK 17 instalado en las rutas estándar de Windows. Devuelve la carpeta…, Fija JAVA_HOME, HADOOP_HOME y PATH solo para este proceso. Devuelve lo que…, Devuelve la ruta "corta" de Windows, sin espacios (por ejemplo, la carpeta "PP…

### Community 60 - "silver_inah.py"
Cohesion: 0.43
Nodes (7): agregar_papel(), construir_silver_inah(), leer_inah(), quitar_duplicados(), DataFrame, Lee el Excel que viene dentro del zip más reciente de Bronze y pone nombres en…, Por cada llave repetida conserva la fila con cifra. Se detiene si hay dos…

### Community 63 - "v"
Cohesion: 0.25
Nodes (8): test_bacalar_ocupacion_ene_2024(), test_ocupacion_2025_es_hueco_no_cero(), test_tren_maya_suma_estaciones_chetumal(), test_tren_maya_zona_igual_suma_destinos(), v(), Chetumal trae 2 estaciones: 24 + 3,478 = 3,502 descensos en ene-2025., El total de zona Grand Costa Maya (7,084) es igual a la suma de sus destinos ya…, En 2025 SITUR-Q reporta 0 habitaciones disponibles (imposible): debe ser hueco,…

### Community 64 - "Página: cuartos vacíos y chat"
Cohesion: 0.33
Nodes (7): cuartos_vacios_chetumal(), preguntas_rapidas(), Parte de las noches de cuarto que quedaron vacías en Chetumal en el último año…, Chat Preguntas rápidas (#chat), Sección El dato (4 de cada 10 cuartos), 4 de cada 10 cuartos vacíos en Chetumal 2024 (458,696/791,016), Chat de preguntas rápidas con respuestas fijas (no IA)

### Community 65 - "descargar_datatur"
Cohesion: 0.29
Nodes (6): contar_filas(), descargar_datatur(), enlaces_de(), Devuelve las rutas de los .zip/.xlsx publicados en una página de DataTur, sin…, Cuenta las filas de todas las hojas de los Excel dentro de un zip (o de un…, Descarga todos los archivos de las categorías pedidas y los registra en el…

### Community 66 - "Silver Censo (ITER)"
Cohesion: 0.48
Nodes (6): asignar_regiones(), construir_silver_iter(), _grados(), leer_iter(), DataFrame, Convierte '88°17\\'52.436" W' a grados decimales (−88.2979). Así publica el…

### Community 69 - "DataFrame"
Cohesion: 0.48
Nodes (7): censo(), datatur(), denue(), inah(), siturq(), DataFrame, fixture

### Community 7 - "figuras.py"
Cohesion: 0.09
Nodes (40): cobertura_ocupacion_siturq(), costos_publicitarios_travel(), estilo_unrc(), _leer_inah(), lluvia_y_huracanes(), ocupacion_semanal_qroo(), oferta_turistica_municipios(), _pie() (+32 more)

### Community 73 - "Página: las 12 fases"
Cohesion: 0.40
Nodes (5): fases_del_proyecto(), resumen_datos(), Cuántos archivos y registros oficiales se reunieron en la Fase 1 (manifiesto de…, Las 12 fases con su resultado real cuando ya existe (cifras de los datos, no…, Sección Las 12 fases (#fases)

### Community 75 - "Página: dónde se queda el dinero"
Cohesion: 0.67
Nodes (3): hospedaje(), Sección ¿Dónde se queda el dinero? (#dinero), El dinero se mide con el tamaño de los hoteles

### Community 76 - "Página: así llega la gente"
Cohesion: 0.50
Nodes (4): movimiento(), Llegadas del último año completo de cada medio de transporte, por lugar…, Sección Así llega la gente (#movimiento), No dibujar flechas origen–destino

### Community 8 - "panel.py"
Cohesion: 0.07
Nodes (37): generar_pdf(), _separar_listas(), agrupar(), centros_completos(), correr(), describir(), perfiles(), cobertura() (+29 more)

### Community 9 - "test_silver_fase5.py"
Cohesion: 0.07
Nodes (26): agregar_banderas(), construir_silver_huracanes(), eventos_sur(), km_haversine(), leer_hurdat2(), dia(), fred_mes(), huracanes() (+18 more)

### Community 0 - "PLAN_v3.md (plan aprobado)"
Cohesion: 0.06
Nodes (61): D12 GeoJSON Q. Roo, D5 Rest-Mex 2025 (208,051 reseñas), A3 Pronóstico, A5 Torre en vivo, A1 Radar, Backend FastAPI (endpoints /api/radar, /api/pronostico, /api/optimizar, /api/stream…), Branding (identidad, personalidad, propuesta de valor, posicionamiento), Brandon Uriel García Sánchez (+53 more)

### Community 26 - "Inventario de datos - fuentes oficiales verificadas"
Cohesion: 0.16
Nodes (15): D10 FRED (peso-dolar, CPI), D13 Benchmarks de costo por canal (WordStream 2025 / LocaliQ 2026), D14 DESIGN.md (tokens y componentes), D1 SITUR-Q (API getCharData, 45 indicadores), D2m DataTur ocupación mensual, D4 DataTur DB_AFAC, BaseDatosCruceros y Compendio 2024, D8 Open-Meteo archivo climatico, D9 HURDAT2 NOAA (1851-2025) (+7 more)

### Community 27 - "Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan"
Cohesion: 0.17
Nodes (15): D11 ENDUTIH 2025 INEGI, D3 DataTur BD_Nacionalidad (521,364 filas), Análisis de sentimiento, Buyer persona, Detección de comunidades en redes sociales, P5: Características de visitantes para recomendar destinos alternativos, Preguntas Minería: ¿manipular el libre mercado o corregir sesgos? ¿parche o turismo regenerativo? desinformación de bots, Reglas de asociación (+7 more)

### Community 3 - "Decisión: la campaña promueve 5 regiones de Quintana Roo"
Cohesion: 0.08
Nodes (51): D2 DataTur ocupación semanal (7 centros de Q. Roo), D4 DataTur BdINAH (visitas a zonas arqueológicas), Criterios 6 (IO) y 9 (propuesta e impacto) de la rúbrica, Riesgos que se vigilan (sargazo en la bahía, laguna frágil, poca oferta en Maya Ka'an), Tope estricto de capacidad en el modelo de IO, Ruta arqueológica del sur (Kohunlich, Dzibanché, Ichkabal), Bacalar (condicionada, laguna en deterioro), Cancún (referencia / región emisora) (+43 more)

### Community 37 - "D6 DENUE INEGI (32 estados)"
Cohesion: 0.21
Nodes (12): A1 Radar, D6 DENUE INEGI (32 estados), D7 Censo 2020 ITER Q. Roo, Índice de Presión Turística, Municipio Othón P. Blanco, Presión de llegada medida (cruceristas + Tren Maya + cruces de Belice por habitación y por residente), Oferta turística (SCIAN 721, 722, 5615, 487, 712, 713), Privacidad: se descartan raz_social, telefono y correoelec (+4 more)

### Community 38 - "04 - Limpieza y orden de los datos (Fase 2: Silver y Gold)"
Cohesion: 0.24
Nodes (12): Bandera de comparabilidad (notas al pie DataTur), Revisión con datos oficiales: Isla Mujeres (DataTur 74.7 % feb / 43.2 % abr 2026), Corrección de conteo: DENUE 6,138,075 e ITER 2,243, DENUE procesado completo (6,138,075 negocios), Fuentes que no coinciden: Isla Mujeres (prensa vs DataTur), DataTur: una version por periodo (gana la mas reciente), D2/D2m DataTur ocupacion hotelera semanal y mensual, Fase 2 — Limpieza y orden de los datos (Silver/Gold) (+4 more)

### Community 39 - "Reglas de oro (a–h)"
Cohesion: 0.23
Nodes (12): Decisión 08 — A1 Radar (Fase 4), Fuentes excluidas (EVI, ENGATUR, OSM, Google Trends, TripAdvisor), Evidencia oficial: visitantes INAH en Q. Roo (BdINAH), Prueba de cifras de documentos (tests/test_documentos.py), Documento ejecutivo no técnico estilo UNRC, Regla (f): ecuaciones y 'cómo lo resolví', Reglas de oro (a–h), Regla de cinco partes por cálculo (ecuación, supuestos, resolución, ejemplo, código) (+4 more)

### Community 70 - "Ingesta: costos publicitarios y sargazo"
Cohesion: 0.47
Nodes (6): Hueco: conversión de Facebook para Travel no publicada, D13 Benchmarks de costo por canal (WordStream / LocaliQ), Evidencia de sargazo en la Bahia de Chetumal (ECOSUR, Reportur), Extraccion con Playwright + Chromium (benchmarks y sargazo), Fase 1: 353 archivos, 8,134,802 registros, 824 MB, 03 - Ingesta de fuentes oficiales (Fase 1: Bronze)

### Community 71 - "Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)"
Cohesion: 0.33
Nodes (6): Regla 1 Silver: Tren Maya suma estaciones, Hallazgo: ocupación semanal de ene-2022 a jul-2026, 239 semanas por centro, Cifras corregidas por la fuente: gana la versión más reciente (2,804 cifras semanales), Regla: Tren Maya se suma por estación (7,084 = 3,502 + 3,582), Regla 6 de Silver: mes aéreo con todos los aeropuertos en 0 = hueco (114 meses-aeropuerto), Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)

### Community 23 - "09 — Auditoría de las Fases 1 a 4 contra el plan"
Cohesion: 0.15
Nodes (14): HURDAT2 (huracanes 1851–2025), 09 — Auditoría de las Fases 1 a 4 contra el plan, Manifiesto Bronze (377 archivos; 353 fuentes oficiales, 8,134,802 registros), Primer commit a GitHub (datos crudos fuera), Veredicto: Fases 1, 3 y 4 completas; Fase 2 incompleta, Reproducibilidad (8 tablas Gold idénticas, SEMILLA = 0), Workflow 'Publicar la página' (GitHub Pages), Job publicar (checkout → configure-pages → upload-pages-artifact frontend → deploy-pages) (+6 more)

### Community 33 - "Problema Prototípico: Turismo inteligente sustentable para México"
Cohesion: 0.17
Nodes (13): Destinos saturados/limitados: Cozumel, Isla Mujeres, Holbox, Pregunta central del Problema Prototípico, Preguntas secundarias (7), Actores: autoridades, prestadores de servicios, comunidades, turistas, plataformas, científicos de datos, Capacidad de carga del destino, Habilidades blandas (pensamiento crítico, negociación, trabajo en equipo, etc.), Licenciatura en Ciencias de Datos para Negocios (5° semestre, 2026-2), Redistribución de flujos turísticos (+5 more)

### Community 34 - "Opción D: ocupación DataTur + componente en ≥2 lugares"
Cohesion: 0.17
Nodes (13): Cruces de Belice (solo Chetumal), DataTur (ocupación semanal, Sectur), Prueba de validez del IPT (comparar_escalas, variantes A–D), Índice de Presión Turística (IPT), Opción D: ocupación DataTur + componente en ≥2 lugares, Predicción ago-2026: 5 lugares tranquilos; Mahahual 0.40 de saturarse, Prueba de validez del índice, Quiebre de 2025 (pérdida de ocupación SITUR-Q) (+5 more)

### Community 4 - "Flighty — Style Reference (sistema de diseño)"
Cohesion: 0.11
Nodes (51): Quick Start: CSS Custom Properties (:root), Quick Start: Tailwind v4 @theme, Amber Download Button, Announcement Bar, Award Badge Pair, Sistema de radios (pill 999px, cards 16px, floating cards 20px), Apple Product Pages, Arc Browser (+43 more)

### Community 44 - "Decisión 2: Quintana Roo y fusión A1 + A3 + A5"
Cohesion: 0.18
Nodes (11): Paquete cauce (proyecto anterior, descartado), Mapa del proyecto (Graphify), A2 Voz del viajero y A4 Portafolio (descartadas como ejes), DataTur: 135 archivos semanales de ocupación (2024-S01 → 2026-S31, 7 centros de Q. Roo), SITUR-Q: API con 45 indicadores, 00 — Fundación del proyecto, Decisión 1: empezar desde cero, Decisión 2: Quintana Roo y fusión A1 + A3 + A5 (+3 more)

### Community 46 - "CLAUDE.md - Reglas del repositorio Torre del Caribe"
Cohesion: 0.22
Nodes (10): Convenciones de código (snake_case en español, _est, _flag, encabezado), CLAUDE.md - Reglas del repositorio Torre del Caribe, Regla 6: Desde cero (nada del proyecto anterior), Regla 5: Si falta un dato, se detiene y se avisa, Regla de oro: documento ejecutivo no tecnico estilo UNRC, Arquitectura de datos bronze / silver / gold, Manifiesto Bronze con huella SHA-256 (MANIFIESTO.csv), Protocolo de trabajo con Brandon (anti-caja negra) (+2 more)

### Community 48 - "D1 SITUR-Q API (45 indicadores)"
Cohesion: 0.27
Nodes (10): Regla 1: No inventar datos, A5 Torre en vivo (que hace la campana esta semana), D1 SITUR-Q API (45 indicadores), Hueco: sin ocupacion hotelera oficial 2025-2026, Indicador SITUR-Q 'Turista - Afluencia' roto (120/120 error 500), Cómo llega la gente: avión 15,959,277 (2024), crucero 7,556,937, Belice 653,306, Tren Maya 560,241 (2025), Regla 3 Silver: afluencia y derrama en 0 = hueco, Regla 4 Silver: los demas ceros se conservan (+2 more)

### Community 51 - "Cap. 2 — El problema en números: ¿a dónde van los turistas?"
Cohesion: 0.20
Nodes (10): Encabezado obligatorio de cada archivo de código, Protocolo de trabajo conjunto (anti-caja negra), Sección Mientras tanto, en el norte (referencia), Referencia: Cancún, Riviera Maya y Tulum (no se promueven), Decisiones ya tomadas, Se promueve cultura, bahía, lagunas y comunidad, no playa (sargazo récord 2026, Tulum −31.3 %), Mandato desde cero (nada del proyecto anterior), Construir todo desde cero, sin el proyecto anterior (+2 more)

### Community 61 - "Estados tranquilo / concurrido / saturado"
Cohesion: 0.25
Nodes (8): Estados tranquilo / concurrido / saturado, Laguna Milagros 'sin dato oficial' en el Radar, Sección de la página #radar '¿Dónde hay espacio hoy?', Laguna Milagros–Xul-Ha sin estadística turística propia: se mide con población y DENUE, Cortes por percentiles comunes p50/p90, Cadena de Markov semanal, solo norte, Foco en 5 regiones (Chetumal, Calderitas–Oxtankah, Ruta arqueológica del sur, Maya Ka'an + Kantemó, Laguna Milagros–Xul-Ha), Región: Laguna Milagros–Xul-Ha

### Community 67 - "Radar: panel mensual"
Cohesion: 0.29
Nodes (7): Pieza 1: panel mensual 15 lugares × 55 meses, Corrección: la ocupación no se suma (3 filas SITUR-Q), Laguna Milagros: 'sin dato oficial', Radar: tabla mensual de 15 lugares × 55 meses y hallazgo del doble conteo SITUR-Q/INAH, Radar: tres decisiones del equipo (pesos iguales, cortes comunes, predicción de estados), Cap. 8 — El Radar: ¿dónde hay presión y dónde hay espacio? (Fase 4), Visitantes INAH zona por zona (ZONA_A_LUGAR, sin doble conteo)

### Community 74 - "Regiones excluidas y sargazo"
Cohesion: 0.40
Nodes (5): Crisis de Tulum (ventas −60 %), Sargazo récord 2026 (>104,700 t; 56 de 140 playas en rojo), Decisión 3: no promover playa en 2026, REGIONES.md — Selección de regiones con evidencia 2026, Regiones excluidas (Tulum, Playa, Mahahual, Cozumel, Isla Mujeres, Holbox, Cancún, Bacalar)

### Community 77 - "Limitación: quiebre de 2025 (SITUR-Q deja de publicar ocupación)"
Cohesion: 0.67
Nodes (3): Limitación: quiebre de 2025 (SITUR-Q deja de publicar ocupación), SITUR-Q (Gobierno de Quintana Roo), Predecir con el índice comparable (decisión 7)

### Community 68 - "10 — Datos limpios para el Pronóstico: huracanes, clima y tipo de cambio (Fase 2, cierre de la parte que usa la Fase 5)"
Cohesion: 0.29
Nodes (7): 10 — Datos limpios para el Pronóstico: huracanes, clima y tipo de cambio (Fase 2, cierre de la parte que usa la Fase 5), 1. Huracanes → `datos/silver/huracanes/` ✅, 2. Clima → `datos/silver/clima_diario/` y `datos/silver/clima_horario/` ✅, 3. Tipo de cambio e inflación de EE. UU. → `datos/silver/fred_diario/` y `datos/silver/fred_mensual/` ✅, Consecuencia, Evidencia de que funciona, Por qué ahora

### Community 72 - "Contrato pagina.js y módulos ocultos"
Cohesion: 0.53
Nodes (6): DIBUJAR, frontend/datos/pagina.js, Módulos ocultos data-clave (pronostico, envivo, escenarios, presupuesto, campana), torre.api.datos_pagina → frontend/datos/pagina.js, Contrato del cascarón (claves de pagina.js por fase), Contrato pagina.js: ninguna cifra escrita a mano en el HTML

### Community 55 - "Decisiones cerradas (A.8)"
Cohesion: 0.33
Nodes (9): 01 — Regiones que promueve la campaña, Decisión 06 — La página para público no técnico, Pretext (frontend/vendor/pretext.js), Decisiones cerradas hasta hoy (A.8), Decisión 05: Planteamiento con datos (Fase 3), Regla 6 de Silver: mes aéreo con todos en 0 es hueco, Criterio de cierres: ≥ 12 meses seguidos abierta y sin cierres en 2026, Presión de llegada medida en el sur (sin estimar ocupación 2025–2026) (+1 more)

### Community 6 - "Fase 7 — Torre en vivo"
Cohesion: 0.06
Nodes (41): Decisión 07 — Sistema visual "Sur mexicano", Datos que no existen: ocupación SITUR-Q termina dic-2024; afluencia y derrama hasta mar-2024; 'Turista - Afluencia' no responde, Regla: ceros imposibles = dato faltante, Vigilancia del sargazo en la Bahía de Chetumal (canales al Caribe, no en la costa; pausa automática si llega), Conversión en Facebook para turismo: supuesto declarado, Fase 3 — Planteamiento con datos (tabla de criterios; cómo medir presión sin ocupación), Fases 9-11 — conexión backend, pulido y cierre, Página web: portada 'El sur tiene espacio', 5 lugares, ¿por qué el sur?, llegadas, dinero, 12 fases, quiénes somos, preguntas rápidas (+33 more)

### Community 22 - "Rúbrica de evaluación (11 criterios, 100%)"
Cohesion: 0.14
Nodes (17): Criterio 10: Informe técnico y comunicación de resultados (4%), Criterio 11: Coloquio: exposición y defensa (4%), Criterio 1: Planteamiento y comprensión del problema (8%), Criterio 2: Gestión y almacenamiento de grandes volúmenes de datos (12%), Criterio 3: Minería de datos (12%), Criterio 4: Aprendizaje de máquina (12%), Criterio 5: Modelos estocásticos (10%), Criterio 7: Mercadotecnia Digital (8%) (+9 more)

### Community 40 - "Incidente crítico Modelos Estocásticos: Incertidumbre en la demanda turística"
Cohesion: 0.18
Nodes (12): Análisis de sensibilidad de variables (precio transporte, clima, tipo de cambio, sentimiento en redes), Asignación y optimización del presupuesto de la campaña, Desarrollo del branding de la marca, Intervalo de confianza (90%) de la demanda esperada, Modelo de optimización para asignar presupuesto entre destinos, temporadas y canales sin rebasar capacidad de carga, ¿Promocionar varios destinos simultáneamente o concentrar recursos en uno solo bajo incertidumbre?, Entregable A: Campaña publicitaria del estado seleccionado, Incidente crítico Modelos Estocásticos: Incertidumbre en la demanda turística (+4 more)

### Community 41 - "Incidente crítico Almacenamiento de Grandes Volúmenes: Cuando los datos del turismo no caben en una sola computadora"
Cohesion: 0.18
Nodes (12): Arquitectura distribuida de Big Data, Integración de datos en tiempo real para ajustar la campaña (baja latencia), ¿Cómo diseñar una estrategia de almacenamiento de grandes volúmenes de datos turísticos heterogéneos, escalable y responsable?, Privacidad y riesgos de datos de movilidad/geolocalización de turistas, Incidente crítico Almacenamiento de Grandes Volúmenes: Cuando los datos del turismo no caben en una sola computadora, INEGI (2025). Cuenta Satélite del Turismo de México 2024, NIST (2020). Big data, Computer Security Resource Center, SECTUR (2026). DataTur: Sistema Nacional de Información Estadística del Sector Turismo (+4 more)

### Community 45 - "Incidente crítico Investigación de Operaciones: Optimización de los flujos turísticos para un desarrollo sustentable"
Cohesion: 0.18
Nodes (11): Criterio 6: Investigación de Operaciones (12%), Escenarios optimista, moderado y pesimista, P4: Escenarios de redistribución sin reducir la actividad económica, Preguntas IO: ¿Qué significa que una distribución sea óptima? ¿Qué priorizar si los objetivos se contraponen?, Incidente crítico Investigación de Operaciones: Optimización de los flujos turísticos para un desarrollo sustentable, OMT (2005). Indicadores de desarrollo sostenible para los destinos turísticos, Canca Ortiz & Villa Caro (2021). Introducción a la investigación de operaciones, Meyer Krumholz et al. (2002). Turismo y desarrollo sostenible (+3 more)

### Community 47 - "Decisión 08 — A1 Radar (Fase 4)"
Cohesion: 0.29
Nodes (10): Graphify como mapa del proyecto (no correr graphify update a mano), Entregables A (campaña), B (informe), C (productos técnicos) y coloquio, Graphify como mapa del proyecto, Problema Prototípico (pregunta central y 7 secundarias), Quintana Roo, Rúbrica (11 criterios, nivel Excelente), Los 6 incidentes críticos, Alternativa elegida: fusión A1 Radar + A3 Pronóstico + A5 Torre en vivo (+2 more)

### Community 49 - "Página: secciones (documento ejecutivo)"
Cohesion: 0.20
Nodes (10): Ubicación comprobada por claves oficiales (3 pruebas), Dónde se queda el dinero: cuartos por hotel (Cancún 219 vs Chetumal 27) y hospedajes por tamaño (0 grandes en los 5 lugares), Las doce fases como tarjetas; módulos futuros ocultos hasta tener datos, Asistente de preguntas rápidas (respuestas fijas, sin IA), Ubicación comprobada con claves INEGI (3 pruebas) y fotos Wikimedia Commons, Cap. 6 — La página web (sistema Sur mexicano), Población por localidad (Censo 2020 ITER), no por municipio, No destacar Kohunlich/Dzibanché en portada (anti cherry-picking) (+2 more)

### Community 50 - "Criterio de selección de modelo: más aciertos y más cambios anticipados"
Cohesion: 0.22
Nodes (10): Oferta turística DENUE = giros SCIAN 721, 722, 5615, 487, 712, 713, Componente llegadas por cuarto (tren + cruceros), Criterio de selección de modelo: más aciertos y más cambios anticipados, Sesgo: el modelo no se puede validar en los 5 lugares, F1 macro y cambios anticipados, Índice comparable (IPT^c), Línea base de persistencia (ŷ_{t+1} = y_t), Random Forest (400 árboles) (+2 more)

### Community 52 - "Incidente crítico Aprendizaje de Máquina: Turismo inteligente sustentable en México"
Cohesion: 0.22
Nodes (10): Modelo predictivo como producto de consultoría (suscripciones/licencias), ¿Cómo usar el aprendizaje de máquina para un turismo más inteligente sin aumentar la presión sobre recursos y comunidades?, Si un algoritmo puede predecir dónde estarán los turistas, ¿puede ayudar a decidir dónde deberían estar?, Turismo inteligente (smart tourism), Incidente crítico Aprendizaje de Máquina: Turismo inteligente sustentable en México, OMT (2018). 'Overtourism'? Understanding and managing urban tourism growth, UNWTO et al. (2019). 'Overtourism'? Volume 2: Case studies, Belkaid & Kummitha (2026). Artificial intelligence in sustainable tourism development (+2 more)

### Community 56 - "Sistema visual Sur mexicano"
Cohesion: 0.22
Nodes (9): Sección Cinco lugares (mapa 3D que sigue al scroll), Portada 'El sur tiene espacio.', Claude Design (lienzo 'Torre del Caribe — rediseño web'), Greca escalonada maya, Paleta mexicana en bloques (rosa, cempasúchil, turquesa, añil...), Bricolage Grotesque + Figtree (locales, OFL), docs/DESIGN.md (estilo Flighty, histórico), Maqueta 3D en CSS + SVG (sin three.js) (+1 more)

### Community 58 - "Preguntas del Problema Prototípico"
Cohesion: 0.25
Nodes (9): Criterio 9: Propuesta de solución e impacto (8%), Indicadores de desempeño e impacto, ¿Cómo distribuir mejor los flujos turísticos para beneficiar a las comunidades y disminuir el impacto ambiental?, P1: Patrones temporales, espaciales y de comportamiento de la concentración turística, P2: Variables relacionadas con la saturación o baja actividad turística, P3: Estimación de la demanda turística futura bajo incertidumbre, P6: Impacto de la redistribución en comunidades receptoras y destinos saturados, P7: Evaluación de viabilidad, sustentabilidad y efectividad de la redistribución (+1 more)

### Community 62 - "Incidente crítico Mercadotecnia Digital: Estrategias digitales para la redistribución del turismo"
Cohesion: 0.25
Nodes (8): ¿Qué acciones implementar si la campaña genera una afluencia mayor a la capacidad del destino?, Preguntas detonadoras de Mercadotecnia Digital (mercado objetivo, medios, presupuesto, indicadores), Propuesta de valor del destino, Simulación de Monte Carlo (riesgo de rebasar capacidad de carga), Incidente crítico Mercadotecnia Digital: Estrategias digitales para la redistribución del turismo, SECTUR & SEMARNAT (2026). Decálogo para la inversión turística sustentable, SECTUR (2025). Programa Sectorial de Turismo 2025-2030, SECTUR (2026). 2025 marca un año histórico para el turismo en México

## Knowledge Gaps
- **167 isolated node(s):** `D13 Benchmarks de costo por canal (WordStream 2025 / LocaliQ 2026)`, `D14 DESIGN.md (tokens y componentes)`, `D1 SITUR-Q (API getCharData, 45 indicadores)`, `D2m DataTur ocupación mensual`, `D4 DataTur DB_AFAC, BaseDatosCruceros y Compendio 2024` (+162 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 459 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `frontend/index.html (página pública)` connect `frontend/index.html (página pública)` to `Página: cuartos vacíos y chat`, `Página: generador de datos`, `app.js`, `Fase 7 — Torre en vivo`, `Contrato pagina.js y módulos ocultos`, `Página: las 12 fases`, `Página: dónde se queda el dinero`, `Página: así llega la gente`, `datos_pagina.py`, `Cap. 2 — El problema en números: ¿a dónde van los turistas?`, `09 — Auditoría de las Fases 1 a 4 contra el plan`, `Decisiones cerradas (A.8)`, `Sistema visual Sur mexicano`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `04 - Limpieza y orden de los datos (Fase 2: Silver y Gold)` connect `04 - Limpieza y orden de los datos (Fase 2: Silver y Gold)` to `Decisión: la campaña promueve 5 regiones de Quintana Roo`, `D6 DENUE INEGI (32 estados)`, `Ingesta: costos publicitarios y sargazo`, `Fase 7 — Torre en vivo`, `Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)`, `test_silver.py`, `CLAUDE.md - Reglas del repositorio Torre del Caribe`, `D1 SITUR-Q API (45 indicadores)`, `silver_datatur_ocupacion.py`, `Entorno: Spark, JDK y prueba de humo`, `Decisiones cerradas (A.8)`, `silver_denue.py`, `Inventario de datos - fuentes oficiales verificadas`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `PLAN_v3.md (plan aprobado)` connect `PLAN_v3.md (plan aprobado)` to `Problema Prototípico: Turismo inteligente sustentable para México`, `Decisión: la campaña promueve 5 regiones de Quintana Roo`, `Reglas de oro (a–h)`, `Decisión 2: Quintana Roo y fusión A1 + A3 + A5`, `CLAUDE.md - Reglas del repositorio Torre del Caribe`, `Decisión 08 — A1 Radar (Fase 4)`, `Cap. 2 — El problema en números: ¿a dónde van los turistas?`, `09 — Auditoría de las Fases 1 a 4 contra el plan`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Inventario de datos - fuentes oficiales verificadas` (e.g. with `DataTur: 135 archivos semanales de ocupación (2024-S01 → 2026-S31, 7 centros de Q. Roo)` and `SITUR-Q: API con 45 indicadores`) actually correct?**
  _`Inventario de datos - fuentes oficiales verificadas` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `frontend/index.html (página pública)` (e.g. with `Job publicar (checkout → configure-pages → upload-pages-artifact frontend → deploy-pages)` and `Página web: portada 'El sur tiene espacio', 5 lugares, ¿por qué el sur?, llegadas, dinero, 12 fases, quiénes somos, preguntas rápidas`) actually correct?**
  _`frontend/index.html (página pública)` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `D13 Benchmarks de costo por canal (WordStream 2025 / LocaliQ 2026)`, `D14 DESIGN.md (tokens y componentes)`, `D1 SITUR-Q (API getCharData, 45 indicadores)` to the rest of the system?**
  _167 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `prediccion.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05367231638418079 - nodes in this community are weakly interconnected._