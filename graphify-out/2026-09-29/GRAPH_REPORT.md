# Graph Report - PP 5to semestre CASCO SANTO TOMAS  (2026-09-29)

## Corpus Check
- 0 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1239 nodes · 2147 edges · 108 communities (71 shown, 37 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 196 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Radar: panel mensual (código)
- Planteamiento (HHI) y clustering de centros
- Ingesta SITUR-Q
- Ingesta de fuentes abiertas
- Entorno Spark en Windows
- Pruebas de ingesta
- Radar: cadena de Markov semanal
- Ingesta de benchmarks y PDF
- Pruebas del planteamiento
- Radar: pruebas del panel
- Radar: pruebas del índice
- Radar: pruebas de la predicción
- Silver SITUR-Q y DENUE
- Datos de la página web
- Pruebas Silver
- Página: app.js y animaciones
- Ingesta y Silver DataTur
- Silver ocupación DataTur y Spark
- Pruebas de criterios
- Radar: pruebas de Markov
- Radar: pruebas del clustering
- Auditoría: cifras de los documentos
- Fotos de Wikimedia y pruebas de la página
- Silver INAH
- Pruebas SITUR-Q (Tren Maya, huecos)
- Documento ejecutivo y gráficas UNRC
- Fixtures de pruebas
- Radar: índice y predicción (código)
- Prueba: 239 semanas DataTur
- test_nota_isla_mujeres()
- Prueba: total DENUE
- test_denue_turisticos_qroo()
- test_denue_sin_datos_personales()
- Prueba: cifras INAH
- Pruebas Silver (test_inah_kohunlich_crec)
- test_inah_papel_de_las_zonas()
- Pruebas Silver (test_iter_poblacion_de_l)
- Pruebas Silver (test_cero_real_se_conser)
- test_regla_6_aereos()
- Pruebas Silver (test_afluencia_y_derrama)
- test_cancun_semana_31_2026()
- Silver Censo (ITER) y criterios
- Plan v3 y módulos A1 A3 A5
- Las 5 regiones de la campaña
- Fase 0: entorno y fundación
- Inventario de fuentes y módulos
- Radar: decisiones y piezas
- Fuentes del Radar (DENUE, Censo)
- SITUR-Q y reglas de datos
- Reglas de oro y ecuaciones
- Inventario de fuentes y módulos (04 - Limpieza y orden de)
- Plan v3 y módulos A1 A3 A5 (OBJETIVO — Torre del Car)
- duckdb==1.1.3 (consulta rápida para la API)
- Las 5 regiones de la campaña (fastapi + uvicorn (backe)
- Ecuaciones y fuentes del documento (PuLP==2.9.0 (programació)
- Ecuaciones y fuentes del documento (statsmodels==0.14.4 (Hol)
- DESIGN.md Flighty (histórico)
- Problema Prototípico y entregables
- Reglas del repositorio (CLAUDE.md)
- Ecuaciones y fuentes del documento
- Radar: índice y quiebre de 2025
- Radar: comparación de modelos
- Estado de las fases
- Ecuaciones y fuentes del documento (Estados tranquilo / conc)
- Página: secciones y límites de datos
- Costos publicitarios y evidencia
- Tabla de criterios y sus pruebas (Foco en 5 regiones (Chet)
- Radar: decisiones y piezas
- Radar: decisiones y piezas (Limitación: quiebre de 2)
- Radar: pruebas del panel (Hallazgo: zonas arqueoló)
- Ecuaciones y fuentes del documento (Reglas de asociación (so)
- Página: módulos, fases y chat
- Objetivo, README y decisiones (Documento ejecutivo (DOC)
- Tabla de criterios y sus pruebas (fixture)
- Radar: panel mensual (Fase 4) (Path)
- Silver ocupación DataTur y Spark (pathlib)
- DataFrame
- SparkSession
- Tabla de criterios y sus pruebas (Regla de cierres: ≥12 me)
- Rúbrica y evidencia integradora
- El problema en números (cap. 2)
- Incidente minería y buyer persona
- Incidente estocásticos
- Incidente Big Data
- Incidente investigación de operaciones
- Incidente ML y preguntas secundarias
- Incidente ML y preguntas secundarias (¿Cómo distribuir mejor l)
- Bronze y privacidad
- Incidente investigación de operaciones (Incidente crítico Mercad)
- Estado de las fases (Estado de las fases (28-)
- Inventario de fuentes y módulos (Cap. 5 — Limpieza y orde)
- Plan v3 y módulos A1 A3 A5 (Alternativa elegida: fus)
- EQUIPO
- Reglas del documento ejecutivo
- 09 — Auditoría de las Fases 1 a 4 contra el plan
- Radar en el documento ejecutivo
- Radar en el documento ejecutivo (Cinco regiones promovida)
- Clustering jerárquico Ward de 55 centros DataTur
- Rediseño 'Sur mexicano' (Claude Design)

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
- `Concentración (HHI): 5 lugares con 12.3 % de población pero 1.4 % de llegadas en avión; avión HHI 0.81` --references--> `cuotas_y_hhi()`  [INFERRED]
  docs/ejecutivo/DOCUMENTO_EJECUTIVO.md → backend/torre/radar/planteamiento.py
- `Corrección de conteo: DENUE 6,138,075 e ITER 2,243` --references--> `_filas_csv_en_zip()`  [EXTRACTED]
  docs/decisiones/03-ingesta.md → backend/torre/base/ingesta_abiertas.py
- `Sección El dato (4 de cada 10 cuartos)` --shares_data_with--> `cuartos_vacios_chetumal()`  [INFERRED]
  frontend/index.html → backend/torre/api/datos_pagina.py
- `Sección 'Con datos oficiales' y tabla de criterios` --shares_data_with--> `calcular_criterios()`  [INFERRED]
  frontend/index.html → backend/torre/radar/criterios.py
- `D11 ENDUTIH 2025 INEGI` --shares_data_with--> `Buyer persona`  [EXTRACTED]
  docs/datos/INVENTARIO.md → PROBLEMA PROTOTÍPICO 5°- LCDN-2026-2.pdf

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

## Communities (108 total, 37 thin omitted)

### Community 10 - "Radar: panel mensual (código)"
Cohesion: 0.07
Nodes (35): cobertura(), _datatur(), guardar(), _inah(), panel_mensual(), _poblacion(), _siturq(), Modelo estocástico de dos etapas (IO, PuLP/CBC) (+27 more)

### Community 11 - "Planteamiento (HHI) y clustering de centros"
Cohesion: 0.12
Nodes (28): agrupar(), centros_completos(), correr(), describir(), perfiles(), actores(), _anio_completo(), comprobar_zonas() (+20 more)

### Community 13 - "Ingesta SITUR-Q"
Cohesion: 0.13
Nodes (20): capturar_evidencia(), consultar(), descargar_siturq(), leer_catalogo(), registrar(), sha256_de(), Path, Visita cada fuente, guarda HTML + captura + párrafos relevantes y devuelve esos… (+12 more)

### Community 14 - "Ingesta de fuentes abiertas"
Cohesion: 0.14
Nodes (22): _bajar(), _bajar_con_espera(), clima(), denue(), descargar_abiertas(), endutih(), _es_zip(), _filas_csv_en_zip() (+14 more)

### Community 15 - "Entorno Spark en Windows"
Cohesion: 0.12
Nodes (18): buscar_jdk17(), configurar_entorno(), crear_spark(), _ruta_corta(), construir_silver_denue(), descomprimir(), test_spark_lee_csv_y_escribe_parquet(), Path (+10 more)

### Community 16 - "Pruebas de ingesta"
Cohesion: 0.14
Nodes (21): filas_manifiesto(), test_benchmarks_travel_google_2025(), test_denue_32_estados(), test_geojson_11_municipios(), test_inah_tulum_2025(), test_manifiesto_huellas_coinciden(), test_restmex_208051_resenas(), test_siturq_bacalar_145_hoteles_ene_2025() (+13 more)

### Community 18 - "Radar: cadena de Markov semanal"
Cohesion: 0.24
Nodes (16): a_k_semanas(), backtest(), correr(), estacionaria(), estados(), matriz(), ocupacion_semanal(), transiciones() (+8 more)

### Community 20 - "Ingesta de benchmarks y PDF"
Cohesion: 0.15
Nodes (14): a_numero(), descargar_benchmarks(), generar_pdf(), _separar_listas(), Path, $2.12' → 2.12 · '8.73%' → 8.73 · ' $44.70' → 44.70. Devuelve None si no hay…, Inserta una línea en blanco antes de cada lista que va pegada a un párrafo. El…, Convierte un Markdown del proyecto en PDF con portada y estilo UNRC. Sirve para… (+6 more)

### Community 21 - "Pruebas del planteamiento"
Cohesion: 0.12
Nodes (13): conc(), test_ejemplo_a_mano_aviones(), test_hhi_casos_extremos(), test_poblacion_de_los_5_lugares_cuadra_con_criterios(), test_zonas_no_son_suma_de_miembros(), DataFrame, fixture, Reparto parejo → HHI = 1/N y HHI* = 0; una unidad dominante → HHI* cerca de 1. (+5 more)

### Community 23 - "Radar: pruebas del panel"
Cohesion: 0.15
Nodes (11): _anual(), p(), test_cifras_conocidas(), test_inah_sin_doble_conteo(), test_laguna_sin_datos_se_declara(), test_ocupacion_no_suma_filas(), DataFrame, fixture (+3 more)

### Community 26 - "Radar: pruebas del índice"
Cohesion: 0.15
Nodes (9): r(), test_ejemplo_a_mano_cancun(), test_ipt_de_juguete(), test_validez_norte_arriba_del_sur_2025_2026(), fixture, Pesos iguales solo sobre lo que existe: (0.2 + 0.6) / 2 = 0.4; una fila sin…, ECUACIONES.md §2.1: Cancún jul-2026 → (0.0497 + 0.0001 + 0.0011 + 0.7214) / 4 =…, La prueba que falló con mín–máx sin DataTur: en 2025–2026 el norte de… (+1 more)

### Community 27 - "Radar: pruebas de la predicción"
Cohesion: 0.15
Nodes (8): r(), test_f1_macro_a_mano(), test_indice_comparable_sin_quiebre(), test_sesgo_5_lugares_casi_sin_cambios(), fixture, Cada lugar usa siempre las mismas medidas: Chetumal, tren por habitante y…, ECUACIONES.md §2.2: F1 por clase con la matriz de confusión de la regresión…, Auditoría: en los 12 meses de prueba los 5 lugares casi no cambiaron de estado;…

### Community 28 - "Silver SITUR-Q y DENUE"
Cohesion: 0.23
Nodes (11): a_snake(), construir_silver_siturq(), leer_indicador(), DataFrame, Path, SparkSession, Ocupación hotelera' → 'ocupacion_hotelera' (sin acentos, minúsculas, guiones…, Lee un JSON de Bronze y lo deja en formato largo: una fila por unidad-año-mes-… (+3 more)

### Community 3 - "Datos de la página web"
Cohesion: 0.08
Nodes (40): _cifra(), criterios(), cuartos_vacios_chetumal(), fases_del_proyecto(), fichas_regiones(), _foto_portada(), generar(), hospedaje() (+32 more)

### Community 33 - "Pruebas Silver"
Cohesion: 0.17
Nodes (8): test_inah_sin_llaves_repetidas(), test_iter_filas_y_total_estatal(), test_iter_reservados_son_nulos_no_ceros(), test_ocupacion_publicada_coincide_con_calculada(), La ocupación que publica DataTur debe ser ocupados ÷ disponibles; se tolera 0.5…, El bloque duplicado 'Extranjero, sep-2025' (283 filas en cero) ya no está:…, 2,243 filas (todas las del CSV de conjunto_de_datos, sin descartar ninguna);…, Lo que INEGI reserva con '*' queda como nulo con reservado_flag, nunca como 0…

### Community 4 - "Página: app.js y animaciones"
Cohesion: 0.10
Nodes (38): acercarA(), alAparecer(), alternarGiro(), arrastrar(), camara(), capitulos(), cifrasDe(), construirMapa() (+30 more)

### Community 40 - "Ingesta y Silver DataTur"
Cohesion: 0.24
Nodes (8): contar_filas(), descargar_datatur(), enlaces_de(), Devuelve las rutas de los .zip/.xlsx publicados en una página de DataTur, sin…, Cuenta las filas de todas las hojas de los Excel dentro de un zip (o de un…, Descarga todos los archivos de las categorías pedidas y los registra en el…, io, requests

### Community 41 - "Silver ocupación DataTur y Spark"
Cohesion: 0.24
Nodes (9): construir_silver_ocupacion(), leer_archivo(), _numero(), Path, SparkSession, Número o None. 'n.d.' / 'n.c.' / vacío → None., Lee un zip de DataTur (semanal o mensual) y devuelve una fila por centro y año., openpyxl (+1 more)

### Community 46 - "Pruebas de criterios"
Cohesion: 0.20
Nodes (8): test_ocupacion_2024_sin_promediar_porcentajes(), test_presion_por_residente(), test_regla_de_12_meses_abierta(), Dzibanché reabrió en feb-2025: de feb-2025 a jul-2026 son 18 meses; Oxtankah…, Chetumal 2024: 458,696 / 791,016 = 58.0 %. Maya Ka'an: 38.6 %. Norte: 73–77 %., Ruta sur: 66,628 visitantes / 6,098 residentes = 10.93; Tulum: 1,031,443 /…, pytest, torre_base_entorno

### Community 47 - "Radar: pruebas de Markov"
Cohesion: 0.20
Nodes (5): r(), test_dos_semanas_a_mano(), fixture, P(saturado en 2 semanas | tranquilo hoy) = Σ_j p_tj · p_js = 0.922·0 +…, torre_radar

### Community 48 - "Radar: pruebas del clustering"
Cohesion: 0.22
Nodes (5): r(), test_silueta_a_mano_cancun(), fixture, s(i) = (b − a) / máx(a, b): a = distancia media a su grupo, b = distancia media…, numpy

### Community 49 - "Auditoría: cifras de los documentos"
Cohesion: 0.25
Nodes (8): cifras(), test_cifra_escrita_coincide_con_el_calculo(), textos(), parametrize, fixture, Cada cifra recalculada desde Gold o desde las funciones, con el formato con que…, sys, warnings

### Community 5 - "Fotos de Wikimedia y pruebas de la página"
Cohesion: 0.06
Nodes (34): descargar_fotos(), _limpiar(), _pedir(), _slug(), _dentro(), municipio_de(), verificar_regiones(), datos() (+26 more)

### Community 51 - "Silver INAH"
Cohesion: 0.43
Nodes (7): agregar_papel(), construir_silver_inah(), leer_inah(), quitar_duplicados(), DataFrame, Lee el Excel que viene dentro del zip más reciente de Bronze y pone nombres en…, Por cada llave repetida conserva la fila con cifra. Se detiene si hay dos…

### Community 58 - "Pruebas SITUR-Q (Tren Maya, huecos)"
Cohesion: 0.25
Nodes (8): test_bacalar_ocupacion_ene_2024(), test_ocupacion_2025_es_hueco_no_cero(), test_tren_maya_suma_estaciones_chetumal(), test_tren_maya_zona_igual_suma_destinos(), v(), Chetumal trae 2 estaciones: 24 + 3,478 = 3,502 descensos en ene-2025., El total de zona Grand Costa Maya (7,084) es igual a la suma de sus destinos ya…, En 2025 SITUR-Q reporta 0 habitaciones disponibles (imposible): debe ser hueco,…

### Community 6 - "Documento ejecutivo y gráficas UNRC"
Cohesion: 0.09
Nodes (39): cobertura_ocupacion_siturq(), costos_publicitarios_travel(), estilo_unrc(), _leer_inah(), ocupacion_semanal_qroo(), oferta_turistica_municipios(), _pie(), _ultimo() (+31 more)

### Community 63 - "Fixtures de pruebas"
Cohesion: 0.48
Nodes (7): censo(), datatur(), denue(), inah(), siturq(), DataFrame, fixture

### Community 7 - "Radar: índice y predicción (código)"
Cohesion: 0.09
Nodes (38): calcular(), componentes(), elegir_componentes(), estados(), guardar(), ipt(), minmax(), sensibilidad() (+30 more)

### Community 9 - "Silver Censo (ITER) y criterios"
Cohesion: 0.07
Nodes (36): asignar_regiones(), construir_silver_iter(), _grados(), leer_iter(), calcular_criterios(), _meses_abierta(), _ocupacion_2024(), tabla() (+28 more)

### Community 0 - "Plan v3 y módulos A1 A3 A5"
Cohesion: 0.06
Nodes (64): D12 GeoJSON Q. Roo, D5 Rest-Mex 2025 (208,051 reseñas), Hueco: conversión de Facebook para Travel no publicada, A3 Pronóstico, A5 Torre en vivo, A1 Radar, Backend FastAPI (endpoints /api/radar, /api/pronostico, /api/optimizar, /api/stream…), Branding (identidad, personalidad, propuesta de valor, posicionamiento) (+56 more)

### Community 1 - "Las 5 regiones de la campaña"
Cohesion: 0.07
Nodes (56): D2 DataTur ocupación semanal (7 centros de Q. Roo), D4 DataTur BdINAH (visitas a zonas arqueológicas), Criterios 6 (IO) y 9 (propuesta e impacto) de la rúbrica, Riesgos que se vigilan (sargazo en la bahía, laguna frágil, poca oferta en Maya Ka'an), Tope estricto de capacidad en el modelo de IO, Ruta arqueológica del sur (Kohunlich, Dzibanché, Ichkabal), Bacalar (condicionada, laguna en deterioro), Cancún (referencia / región emisora) (+48 more)

### Community 12 - "Fase 0: entorno y fundación"
Cohesion: 0.09
Nodes (25): 02 — Entorno de trabajo (Fase 0: cimientos), Paquete cauce (proyecto anterior, descartado), Mapa del proyecto (Graphify), Crisis de Tulum (ventas −60 %), Sargazo récord 2026 (>104,700 t; 56 de 140 playas en rojo), JDK 17 (OpenJDK 17.0.20.1 de Microsoft), Prueba de humo Fase 0 (22.93 s, suma = 6), PySpark 3.5.6 (no 4.x) (+17 more)

### Community 17 - "Inventario de fuentes y módulos"
Cohesion: 0.11
Nodes (21): D10 FRED (peso-dolar, CPI), D11 ENDUTIH 2025 INEGI, D13 Benchmarks de costo por canal (WordStream 2025 / LocaliQ 2026), D14 DESIGN.md (tokens y componentes), D1 SITUR-Q (API getCharData, 45 indicadores), D2m DataTur ocupación mensual, D3 DataTur BD_Nacionalidad (521,364 filas), D4 DataTur DB_AFAC, BaseDatosCruceros y Compendio 2024 (+13 more)

### Community 31 - "Radar: decisiones y piezas"
Cohesion: 0.17
Nodes (12): Decisión 08 — A1 Radar (Fase 4), Pieza 1: panel mensual 15 lugares × 55 meses, Índice de presión turística IPT_{d,t}, Corrección: la ocupación no se suma (3 filas SITUR-Q), Protocolo de trabajo conjunto (anti-caja negra), Radar: tabla mensual de 15 lugares × 55 meses y hallazgo del doble conteo SITUR-Q/INAH, Radar: tres decisiones del equipo (pesos iguales, cortes comunes, predicción de estados), Cap. 8 — El Radar: ¿dónde hay presión y dónde hay espacio? (Fase 4) (+4 more)

### Community 34 - "Fuentes del Radar (DENUE, Censo)"
Cohesion: 0.22
Nodes (11): A1 Radar, D6 DENUE INEGI (32 estados), D7 Censo 2020 ITER Q. Roo, Índice de Presión Turística, Municipio Othón P. Blanco, Presión de llegada medida (cruceristas + Tren Maya + cruces de Belice por habitación y por residente), Oferta turística (SCIAN 721, 722, 5615, 487, 712, 713), Privacidad: se descartan raz_social, telefono y correoelec (+3 more)

### Community 35 - "SITUR-Q y reglas de datos"
Cohesion: 0.33
Nodes (11): Revisión con datos oficiales: Isla Mujeres (DataTur 74.7 % feb / 43.2 % abr 2026), Regla 1 Silver: Tren Maya suma estaciones, Regla 1: No inventar datos, D1 SITUR-Q API (45 indicadores), Hueco: sin ocupacion hotelera oficial 2025-2026, Indicador SITUR-Q 'Turista - Afluencia' roto (120/120 error 500), 04 - Limpieza y orden de los datos (Fase 2: Silver y Gold), Regla 6 Silver: mes aereo con todos los aeropuertos en 0 = hueco (+3 more)

### Community 44 - "Reglas de oro y ecuaciones"
Cohesion: 0.27
Nodes (10): Ecuaciones y 'cómo lo resolví', Regla de las cinco partes (ecuación, supuestos, método, ejemplo a mano, código), Fuentes excluidas (EVI, ENGATUR, OSM, Google Trends, TripAdvisor), Regla de oro (f): ecuaciones y 'cómo lo resolví', Evidencia oficial: visitantes INAH en Q. Roo (BdINAH), Prueba de cifras de documentos (tests/test_documentos.py), Documentación en cinco partes (ecuación, supuestos, resolución, ejemplo a mano, código), Documento ejecutivo no técnico estilo UNRC (+2 more)

### Community 59 - "Inventario de fuentes y módulos (04 - Limpieza y orden de)"
Cohesion: 0.33
Nodes (7): Bandera de comparabilidad (notas al pie DataTur), Corrección de conteo: DENUE 6,138,075 e ITER 2,243, DENUE procesado completo (6,138,075 negocios), Fuentes que no coinciden: Isla Mujeres (prensa vs DataTur), DataTur: una version por periodo (gana la mas reciente), Incidente crítico: Big Data (baja latencia), D2/D2m DataTur ocupacion hotelera semanal y mensual

### Community 68 - "Plan v3 y módulos A1 A3 A5 (OBJETIVO — Torre del Car)"
Cohesion: 0.50
Nodes (5): OBJETIVO — Torre del Caribe (ancla del proyecto), Graphify como mapa del proyecto, Rúbrica (11 criterios, nivel Excelente), Los 6 incidentes críticos, Sesgo: el modelo no se puede validar en los 5 lugares

### Community 2 - "DESIGN.md Flighty (histórico)"
Cohesion: 0.11
Nodes (51): Quick Start: CSS Custom Properties (:root), Quick Start: Tailwind v4 @theme, Amber Download Button, Announcement Bar, Award Badge Pair, Sistema de radios (pill 999px, cards 16px, floating cards 20px), Apple Product Pages, Arc Browser (+43 more)

### Community 22 - "Problema Prototípico y entregables"
Cohesion: 0.15
Nodes (14): Destinos saturados/limitados: Cozumel, Isla Mujeres, Holbox, Pregunta central del Problema Prototípico, Preguntas secundarias (7), Actores: autoridades, prestadores de servicios, comunidades, turistas, plataformas, científicos de datos, Capacidad de carga del destino, Habilidades blandas (pensamiento crítico, negociación, trabajo en equipo, etc.), Licenciatura en Ciencias de Datos para Negocios (5° semestre, 2026-2), Redistribución de flujos turísticos (+6 more)

### Community 29 - "Reglas del repositorio (CLAUDE.md)"
Cohesion: 0.18
Nodes (12): Convenciones de código (snake_case en español, _est, _flag, encabezado), CLAUDE.md - Reglas del repositorio Torre del Caribe, Regla 6: Desde cero (nada del proyecto anterior), Regla 5: Si falta un dato, se detiene y se avisa, Regla de oro: documento ejecutivo no tecnico estilo UNRC, Arquitectura de datos bronze / silver / gold, Graphify como mapa del proyecto (no correr graphify update a mano), Manifiesto Bronze con huella SHA-256 (MANIFIESTO.csv) (+4 more)

### Community 30 - "Ecuaciones y fuentes del documento"
Cohesion: 0.17
Nodes (12): HURDAT2 (huracanes 1851–2025), Incidente crítico: Estocásticos, Documento ejecutivo Torre del Caribe, Censo 2020 por localidad (ITER), Fotos con licencia libre de Wikimedia Commons, Maqueta 3D del sur de Quintana Roo, Página web de la campaña, Pronóstico (cuándo ir y cuánto invertir) (+4 more)

### Community 42 - "Radar: índice y quiebre de 2025"
Cohesion: 0.27
Nodes (10): Índice de Presión Turística (IPT), Predicción ago-2026: 5 lugares tranquilos; Mahahual 0.40 de saturarse, Quiebre de 2025 (pérdida de ocupación SITUR-Q), Ecuación del IPT (pesos iguales sobre componentes disponibles), Normalización mín–máx z = (x − min)/(max − min), Oferta turística DENUE = giros SCIAN 721, 722, 5615, 487, 712, 713, Escala mín–máx común a todo el estado, Índice comparable (lo que publica el Radar) (+2 more)

### Community 43 - "Radar: comparación de modelos"
Cohesion: 0.31
Nodes (10): Gradient Boosting, Índice comparable IPT^c, Backtesting con origen móvil (12 reentrenamientos, 156 predicciones), Puntaje de Brier, Random Forest (B = 400 árboles), Cadena de Markov semanal (matriz de transición, P^k, estacionaria), F1-macro y cambios anticipados, Línea base de persistencia ŷ(t+1) = y(t) (+2 more)

### Community 45 - "Estado de las fases"
Cohesion: 0.22
Nodes (10): Incidente crítico: Investigación de Operaciones, Conversión en Facebook para turismo: supuesto declarado, Riesgos y datos que no existen, Fase 10 — Pulido final de la página, Fase 11 — Cierre y coloquio, Fase 6 — Reparto del presupuesto (optimización), Fase 9 — Servidor local conectado a la página, Hoja de ruta del proyecto (+2 more)

### Community 52 - "Ecuaciones y fuentes del documento (Estados tranquilo / conc)"
Cohesion: 0.25
Nodes (8): Estados tranquilo / concurrido / saturado, scikit-learn==1.5.2 (clasificador, Isolation Forest, TF-IDF), Sección de la página #radar '¿Dónde hay espacio hoy?', Isolation Forest (A5 Torre en vivo), Modelo estocástico de dos etapas (Investigación de Operaciones), Cortes por percentiles comunes p50/p90, Cadena de Markov semanal, solo norte, Regla de pausa (IPT > u o anomalía > τ → y = 0)

### Community 53 - "Página: secciones y límites de datos"
Cohesion: 0.25
Nodes (8): INAH visitantes a zonas arqueológicas, Capacidad probada sin usar (Kohunlich 49 %), Cifras oficiales conocidas verificadas, Sección: cómo llega la gente (avión, crucero, Belice, Tren Maya), Laguna Milagros y Xul-Ha, SITUR-Q (sistema estatal de indicadores), Tren Maya (pasajeros por estación), Regla: no inventar datos (huecos declarados)

### Community 55 - "Costos publicitarios y evidencia"
Cohesion: 0.29
Nodes (8): playwright==1.49.1 (navegador automatizado), Datos que no existen: ocupación SITUR-Q termina dic-2024; afluencia y derrama hasta mar-2024; 'Turista - Afluencia' no responde, Regla: ceros imposibles = dato faltante, Vigilancia del sargazo en la Bahía de Chetumal (canales al Caribe, no en la costa; pausa automática si llega), Cap. 4 — Recolección de los datos oficiales (Fase 1): 15 fuentes, 353 archivos, 8,134,802 registros, Costos publicitarios WordStream / LocaliQ, Navegador automatizado Playwright, Fase 7 — Torre en vivo

### Community 56 - "Tabla de criterios y sus pruebas (Foco en 5 regiones (Chet)"
Cohesion: 0.25
Nodes (8): Meses seguidos abierta A_z (criterio de cierres ≥12), Variación interanual ene–jul Δ%, Capacidad probada sin usar K_s = 1 − V2025/V2019, Índice de Herfindahl-Hirschman (HHI y HHI*), Razón contra la población ρ, Selección de regiones con visitantes del INAH (§1), Tabla de criterios de las 5 regiones (§1-bis), Foco en 5 regiones (Chetumal, Calderitas–Oxtankah, Ruta arqueológica del sur, Maya Ka'an + Kantemó, Laguna Milagros–Xul-Ha)

### Community 61 - "Radar: decisiones y piezas"
Cohesion: 0.29
Nodes (7): Cruces de Belice (solo Chetumal), DataTur (ocupación semanal, Sectur), Prueba de validez del IPT (comparar_escalas, variantes A–D), Opción D: ocupación DataTur + componente en ≥2 lugares, Prueba de validez del índice, DataTur y SITUR-Q no miden lo mismo (reconciliación), Diferencia DataTur vs SITUR-Q se declara, no se ajusta

### Community 69 - "Radar: decisiones y piezas (Limitación: quiebre de 2)"
Cohesion: 0.67
Nodes (3): Limitación: quiebre de 2025 (SITUR-Q deja de publicar ocupación), SITUR-Q (Gobierno de Quintana Roo), Predecir con el índice comparable (decisión 7)

### Community 8 - "Página: módulos, fases y chat"
Cohesion: 0.07
Nodes (40): Chat de preguntas rápidas (respuestas fijas, no IA), Módulo 'La campaña' (Fase 8, oculto), Módulo pronóstico 'Mejor mes para ir' (Fase 5, oculto), Módulos ocultos: en vivo, escenarios, presupuesto, Sección 'El dato': 4 de cada 10 cuartos vacíos en Chetumal, Sección '¿Dónde se queda el dinero?', Sección 'Quiénes somos' (científicos de datos UNRC), Sección 'Con datos oficiales' y tabla de criterios (+32 more)

### Community 64 - "Silver ocupación DataTur y Spark (pathlib)"
Cohesion: 0.47
Nodes (4): nbclient, nbformat, pathlib, Notebook 02_radar

### Community 19 - "Rúbrica y evidencia integradora"
Cohesion: 0.14
Nodes (17): Criterio 10: Informe técnico y comunicación de resultados (4%), Criterio 11: Coloquio: exposición y defensa (4%), Criterio 1: Planteamiento y comprensión del problema (8%), Criterio 2: Gestión y almacenamiento de grandes volúmenes de datos (12%), Criterio 3: Minería de datos (12%), Criterio 4: Aprendizaje de máquina (12%), Criterio 5: Modelos estocásticos (10%), Criterio 7: Mercadotecnia Digital (8%) (+9 more)

### Community 24 - "El problema en números (cap. 2)"
Cohesion: 0.17
Nodes (13): Tulum recibe 15.5 veces más que la ruta del sur (1,031,443 ÷ 66,628), Tulum −31.3 % entre ene–jul 2025 y ene–jul 2026 (476,247 ÷ 692,946 − 1), Cinco criterios de selección: sin sargazo, sin crisis 2026, no saturadas, ecosistema que aguante, con datos oficiales, Chacchoben y San Gervasio no se promueven (más del 90 % son cruceristas), Kohunlich: 49.0 % de capacidad probada sin usar (1 − 21,850 ÷ 42,813), Regiones retiradas: Cobá (municipio de Tulum), Muyil (cerrada jun-2024 a feb-2026), Ribera del Río Hondo (sin estadística), Cap. 2.1 — Qué regiones promueve la campaña (5 regiones), Cap. 2 — El problema en números: ¿a dónde van los turistas? (+5 more)

### Community 25 - "Incidente minería y buyer persona"
Cohesion: 0.21
Nodes (13): Análisis de sentimiento, Buyer persona, Detección de comunidades en redes sociales, P5: Características de visitantes para recomendar destinos alternativos, Preguntas Minería: ¿manipular el libre mercado o corregir sesgos? ¿parche o turismo regenerativo? desinformación de bots, Reglas de asociación, Sesgos en los datos (destinos con menor huella digital invisibilizados), Incidente crítico Minería de Datos: Cuando los datos no mienten, pero los patrones sí importan (+5 more)

### Community 32 - "Incidente estocásticos"
Cohesion: 0.18
Nodes (12): Análisis de sensibilidad de variables (precio transporte, clima, tipo de cambio, sentimiento en redes), Asignación y optimización del presupuesto de la campaña, Desarrollo del branding de la marca, Intervalo de confianza (90%) de la demanda esperada, Modelo de optimización para asignar presupuesto entre destinos, temporadas y canales sin rebasar capacidad de carga, ¿Promocionar varios destinos simultáneamente o concentrar recursos en uno solo bajo incertidumbre?, Entregable A: Campaña publicitaria del estado seleccionado, Incidente crítico Modelos Estocásticos: Incertidumbre en la demanda turística (+4 more)

### Community 37 - "Incidente Big Data"
Cohesion: 0.20
Nodes (11): Arquitectura distribuida de Big Data, Integración de datos en tiempo real para ajustar la campaña (baja latencia), ¿Cómo diseñar una estrategia de almacenamiento de grandes volúmenes de datos turísticos heterogéneos, escalable y responsable?, Privacidad y riesgos de datos de movilidad/geolocalización de turistas, Incidente crítico Almacenamiento de Grandes Volúmenes: Cuando los datos del turismo no caben en una sola computadora, INEGI (2025). Cuenta Satélite del Turismo de México 2024, NIST (2020). Big data, Computer Security Resource Center, NIST SP 1500-1r2 (2019). Big Data Definitions (+3 more)

### Community 38 - "Incidente investigación de operaciones"
Cohesion: 0.18
Nodes (11): Criterio 6: Investigación de Operaciones (12%), Escenarios optimista, moderado y pesimista, P4: Escenarios de redistribución sin reducir la actividad económica, Preguntas IO: ¿Qué significa que una distribución sea óptima? ¿Qué priorizar si los objetivos se contraponen?, Incidente crítico Investigación de Operaciones: Optimización de los flujos turísticos para un desarrollo sustentable, OMT (2005). Indicadores de desarrollo sostenible para los destinos turísticos, Canca Ortiz & Villa Caro (2021). Introducción a la investigación de operaciones, Meyer Krumholz et al. (2002). Turismo y desarrollo sostenible (+3 more)

### Community 39 - "Incidente ML y preguntas secundarias"
Cohesion: 0.20
Nodes (11): Modelo predictivo como producto de consultoría (suscripciones/licencias), ¿Cómo usar el aprendizaje de máquina para un turismo más inteligente sin aumentar la presión sobre recursos y comunidades?, Si un algoritmo puede predecir dónde estarán los turistas, ¿puede ayudar a decidir dónde deberían estar?, Turismo inteligente (smart tourism), Incidente crítico Aprendizaje de Máquina: Turismo inteligente sustentable en México, OMT (2018). 'Overtourism'? Understanding and managing urban tourism growth, SECTUR (2026). DataTur: Sistema Nacional de Información Estadística del Sector Turismo, UNWTO et al. (2019). 'Overtourism'? Volume 2: Case studies (+3 more)

### Community 50 - "Incidente ML y preguntas secundarias (¿Cómo distribuir mejor l)"
Cohesion: 0.25
Nodes (9): Criterio 9: Propuesta de solución e impacto (8%), Indicadores de desempeño e impacto, ¿Cómo distribuir mejor los flujos turísticos para beneficiar a las comunidades y disminuir el impacto ambiental?, P1: Patrones temporales, espaciales y de comportamiento de la concentración turística, P2: Variables relacionadas con la saturación o baja actividad turística, P3: Estimación de la demanda turística futura bajo incertidumbre, P6: Impacto de la redistribución en comunidades receptoras y destinos saturados, P7: Evaluación de viabilidad, sustentabilidad y efectividad de la redistribución (+1 more)

### Community 54 - "Bronze y privacidad"
Cohesion: 0.25
Nodes (8): Manifiesto con huella SHA-256, Depósitos Bronze / Silver / Gold, DENUE del INEGI, Sección: dónde se queda el dinero (tamaño de hoteles), Clima Open-Meteo, PySpark 3.5.6 + Java 17, Serie de derrama económica descartada, Oferta turística por giros SCIAN (SECTUR/INEGI)

### Community 57 - "Incidente investigación de operaciones (Incidente crítico Mercad)"
Cohesion: 0.25
Nodes (8): ¿Qué acciones implementar si la campaña genera una afluencia mayor a la capacidad del destino?, Preguntas detonadoras de Mercadotecnia Digital (mercado objetivo, medios, presupuesto, indicadores), Propuesta de valor del destino, Simulación de Monte Carlo (riesgo de rebasar capacidad de carga), Incidente crítico Mercadotecnia Digital: Estrategias digitales para la redistribución del turismo, SECTUR & SEMARNAT (2026). Decálogo para la inversión turística sustentable, SECTUR (2025). Programa Sectorial de Turismo 2025-2030, SECTUR (2026). 2025 marca un año histórico para el turismo en México

### Community 60 - "Estado de las fases (Estado de las fases (28-)"
Cohesion: 0.29
Nodes (7): Fase 2 — Limpieza y orden de los datos (Silver/Gold), Fase 3 — Planteamiento con datos (tabla de criterios; cómo medir presión sin ocupación), Fases 9-11 — conexión backend, pulido y cierre, Estado de las fases (28-sep-2026), El sur se mide con presión de llegada medida, sin estimar ocupación, Reseñas Rest-Mex 2025, Fase 8 — La campaña (reseñas, buyer persona, marca)

### Community 62 - "Inventario de fuentes y módulos (Cap. 5 — Limpieza y orde)"
Cohesion: 0.29
Nodes (7): Hallazgo: ocupación semanal de ene-2022 a jul-2026, 239 semanas por centro, Cifras corregidas por la fuente: gana la versión más reciente (2,804 cifras semanales), Cómo llega la gente: avión 15,959,277 (2024), crucero 7,556,937, Belice 653,306, Tren Maya 560,241 (2025), Regla: Tren Maya se suma por estación (7,084 = 3,502 + 3,582), Regla 6 de Silver: mes aéreo con todos los aeropuertos en 0 = hueco (114 meses-aeropuerto), Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark), Sin flechas origen-destino en el mapa de llegadas

### Community 67 - "Plan v3 y módulos A1 A3 A5 (Alternativa elegida: fus)"
Cohesion: 0.40
Nodes (5): A5 Torre en vivo (que hace la campana esta semana), Entregables A (campaña), B (informe), C (productos técnicos) y coloquio, Problema Prototípico (pregunta central y 7 secundarias), Quintana Roo, Alternativa elegida: fusión A1 Radar + A3 Pronóstico + A5 Torre en vivo

### Community 65 - "09 — Auditoría de las Fases 1 a 4 contra el plan"
Cohesion: 0.33
Nodes (6): 09 — Auditoría de las Fases 1 a 4 contra el plan, Manifiesto Bronze (377 archivos; 353 fuentes oficiales, 8,134,802 registros), Primer commit a GitHub (datos crudos fuera), Veredicto: Fases 1, 3 y 4 completas; Fase 2 incompleta, Revisión completa de las fases 1 a 4, Reproducibilidad (8 tablas Gold idénticas, SEMILLA = 0)

### Community 36 - "Radar en el documento ejecutivo"
Cohesion: 0.24
Nodes (11): Agrupamiento jerárquico de 55 centros del país, Cadena de Markov semanal del norte, Índice comparable (mismas medidas en el tiempo), Índice de presión turística (0 a 1), Persistencia (línea base: igual que este mes), Radar (¿dónde hay presión y dónde hay espacio?), Regresión logística (modelo elegido del Radar), SECTUR-DataTur (ocupación semanal y llegadas) (+3 more)

### Community 66 - "Radar en el documento ejecutivo (Cinco regiones promovida)"
Cohesion: 0.40
Nodes (6): Bahía de Chetumal: Calderitas y Oxtankah, Chetumal, ECOSUR (El Colegio de la Frontera Sur), Vigilancia del sargazo en la Bahía de Chetumal, Cinco regiones promovidas, Cancún, Riviera Maya y Tulum solo como referencia

### Community 70 - "Clustering jerárquico Ward de 55 centros DataTur"
Cohesion: 0.67
Nodes (3): Clustering de centros del país (faltaba contra el plan), Clustering jerárquico Ward de 55 centros DataTur, Coeficiente de silueta

## Knowledge Gaps
- **177 isolated node(s):** `MODULOS`, `Criterios 6 (IO) y 9 (propuesta e impacto) de la rúbrica`, `Bacalar (condicionada, laguna en deterioro)`, `Chacchoben (descartada)`, `Cozumel (excluida, saturada por cruceros)` (+172 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 444 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `frontend/index.html (página pública)` connect `Página: módulos, fases y chat` to `Radar: panel mensual (código)`, `Datos de la página web`, `Página: app.js y animaciones`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `Problema Prototípico: Turismo inteligente sustentable para México` connect `Problema Prototípico y entregables` to `Plan v3 y módulos A1 A3 A5`, `Incidente estocásticos`, `Incidente Big Data`, `Incidente investigación de operaciones`, `Incidente ML y preguntas secundarias`, `Incidente ML y preguntas secundarias (¿Cómo distribuir mejor l)`, `Rúbrica y evidencia integradora`, `Incidente investigación de operaciones (Incidente crítico Mercad)`, `Incidente minería y buyer persona`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `PLAN_v3.md (plan aprobado)` connect `Plan v3 y módulos A1 A3 A5` to `Las 5 regiones de la campaña`, `Plan v3 y módulos A1 A3 A5 (Alternativa elegida: fus)`, `Reglas de oro y ecuaciones`, `Inventario de fuentes y módulos`, `Ingesta de benchmarks y PDF`, `Problema Prototípico y entregables`, `Reglas del repositorio (CLAUDE.md)`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Inventario de datos - fuentes oficiales verificadas` (e.g. with `DataTur: 135 archivos semanales de ocupación (2024-S01 → 2026-S31, 7 centros de Q. Roo)` and `SITUR-Q: API con 45 indicadores`) actually correct?**
  _`Inventario de datos - fuentes oficiales verificadas` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `MODULOS`, `Criterios 6 (IO) y 9 (propuesta e impacto) de la rúbrica`, `Bacalar (condicionada, laguna en deterioro)` to the rest of the system?**
  _177 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Radar: panel mensual (código)` be split into smaller, more focused modules?**
  _Cohesion score 0.07142857142857142 - nodes in this community are weakly interconnected._
- **Should `Planteamiento (HHI) y clustering de centros` be split into smaller, more focused modules?**
  _Cohesion score 0.11724137931034483 - nodes in this community are weakly interconnected._