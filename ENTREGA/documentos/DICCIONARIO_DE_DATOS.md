# Diccionario de datos — Torre del Caribe

Autor: **Brandon Uriel García Sánchez** · Generado por `python -m torre.base.diccionario` desde el almacén `datos/gold/torre.duckdb`. **No se edita a mano**: el significado de cada columna vive en `backend/torre/base/diccionario.py`.

Capas: **Silver** = limpio y tipado (una vista por tabla) · **Estrella** = dim_lugar, dim_tiempo, hechos_mes · **Gold** = salidas de los modelos (su método está en la nota de decisión de su fase y en `docs/metodologia/ECUACIONES.md`). Sufijos: `_est` estimado, `_flag` bandera.

| Tabla | Renglones | Qué es |
|---|---:|---|
| [`silver_afac`](#silver_afac) | 19,277 | Pasajeros por aerolínea en México, por mes (AFAC vía DataTur, 2016 → jul-2026). Nacional. |
| [`silver_clima_diario`](#silver_clima_diario) | 224,232 | Clima diario de 8 puntos de Quintana Roo (Open-Meteo, 1950 → 2026). |
| [`silver_clima_horario`](#silver_clima_horario) | 542,784 | Clima por hora de 8 puntos (Open-Meteo, 2019 → 2026), con hora local. |
| [`silver_cruceros`](#silver_cruceros) | 3,895 | Arribos y pasajeros de crucero por puerto y mes (DataTur, 2016 → jul-2026). |
| [`silver_datatur_ocupacion`](#silver_datatur_ocupacion) | 23,341 | Ocupación hotelera semanal y mensual por centro turístico (DataTur, 2022 → 2026). |
| [`silver_denue`](#silver_denue) | 6,138,075 | Negocios del país con giro, tamaño y coordenadas (DENUE INEGI), con su categoría turística. |
| [`silver_fred_diario`](#silver_fred_diario) | 8,575 | Pesos por dólar por día (FRED, DEXMXUS). |
| [`silver_fred_mensual`](#silver_fred_mensual) | 957 | Pesos por dólar promedio del mes e inflación de EE. UU. (FRED). |
| [`silver_huracanes`](#silver_huracanes) | 55,524 | Posiciones de todas las tormentas del Atlántico cada 6 horas (HURDAT2, NOAA, 1851 → 2025). |
| [`silver_inah`](#silver_inah) | 71,278 | Visitantes a museos y zonas arqueológicas por mes y tipo (INAH vía DataTur, 2016 → 2026). |
| [`silver_iter`](#silver_iter) | 2,243 | Población y viviendas por localidad (Censo 2020, ITER Quintana Roo). |
| [`silver_nacionalidad`](#silver_nacionalidad) | 521,363 | Llegadas de extranjeros por avión, por aeropuerto, país y sexo (UPM vía DataTur, 2012 → jul-2026). |
| [`silver_restmex`](#silver_restmex) | 207,873 | Reseñas de turistas con calificación de 1 a 5 (Rest-Mex 2025, CC-BY-4.0). |
| [`silver_siturq`](#silver_siturq) | 7,340 | Indicadores turísticos de Quintana Roo por destino y mes (SITUR-Q, API pública). |
| [`dim_lugar`](#dim_lugar) | 15 | Dimensión de lugares: cada lugar con su papel (promovido, referencia o comparación). |
| [`dim_tiempo`](#dim_tiempo) | 192 | Dimensión de tiempo: un renglón por mes, de 2012 a 2027. |
| [`hechos_mes`](#hechos_mes) | 3,287 | Hechos: una medida por lugar, mes y variable, con su fuente. Un hueco no tiene renglón. |
| [`gold_campana_aspectos`](#gold_campana_aspectos) | 36 | Fase 8. Temas de las reseñas: % que los menciona y riesgo relativo de reseña mala. |
| [`gold_campana_palabras`](#gold_campana_palabras) | 40 | Fase 8. Palabras que distinguen reseñas de 5 estrellas y malas (log-odds). |
| [`gold_campana_reglas`](#gold_campana_reglas) | 30 | Fase 8. Reglas de asociación (Apriori) que terminan en reseña mala o de 5 estrellas. |
| [`gold_criterios_regiones`](#gold_criterios_regiones) | 8 | Fase 3. Tabla de los 5 criterios por región (sargazo, cierres, saturación, fragilidad, datos). |
| [`gold_envivo_decisiones`](#gold_envivo_decisiones) | 717 | Fase 7. Qué hizo la Torre cada semana en cada lugar del sur y cuánto dinero gastó o guardó. |
| [`gold_envivo_norte`](#gold_envivo_norte) | 239 | Fase 7. Semanas con el norte saturado y si se encendió "¿Ibas al norte?". |
| [`gold_envivo_senales`](#gold_envivo_senales) | 239 | Fase 7. Las cuatro señales de cada semana: norte, tormentas, clima raro y llegadas. |
| [`gold_lugares_clasificados`](#gold_lugares_clasificados) | 49,844 | Planeador. Negocios del DENUE clasificados por léxico (hospedaje, comida, qué hacer). |
| [`gold_lugares_recomendados`](#gold_lugares_recomendados) | 294 | Planeador. Negocios recomendados por lugar y momento del día. |
| [`gold_presupuesto_pareto`](#gold_presupuesto_pareto) | 10 | Fase 6. Frontera de Pareto: visitantes esperados según la ocupación máxima permitida. |
| [`gold_presupuesto_pausas`](#gold_presupuesto_pausas) | 60 | Fase 6. Si el anuncio sigue encendido en cada escenario (malo, probable, bueno), donde hay gasto. |
| [`gold_presupuesto_plan`](#gold_presupuesto_plan) | 54 | Fase 6. Pesos y visitantes esperados (_est) por mes, lugar y canal del plan óptimo. |
| [`gold_presupuesto_precios_sombra`](#gold_presupuesto_precios_sombra) | 6 | Fase 6. Precio sombra y holgura del presupuesto, la equidad y los topes por canal. |
| [`gold_presupuesto_reglas`](#gold_presupuesto_reglas) | 4 | Fase 6. Visitantes que cuesta cada regla (resolviendo el modelo sin ella). |
| [`gold_presupuesto_sensibilidad`](#gold_presupuesto_sensibilidad) | 8 | Fase 6. El modelo resuelto con cada supuesto movido (conversión, clic, tormentas, presupuesto). |
| [`gold_pronostico_backtest`](#gold_pronostico_backtest) | 9,930 | Fase 5. Cada pronóstico del origen móvil contra el dato real. |
| [`gold_pronostico_calendario`](#gold_pronostico_calendario) | 75 | Fase 5. Calendario lugar × mes: temporada alta, tormenta, lluvia y otro mes u otro lugar. |
| [`gold_pronostico_cobertura`](#gold_pronostico_cobertura) | 25 | Fase 5. Qué tanto el rango del 90 % contuvo al dato real, por modelo y horizonte. |
| [`gold_pronostico_eleccion`](#gold_pronostico_eleccion) | 25 | Fase 5. Modelo elegido por serie (menor error con rango confiable). |
| [`gold_pronostico_escenarios`](#gold_pronostico_escenarios) | 132 | Fase 5. Monte Carlo: escenarios malo/probable/bueno por mes y riesgo de rebasar capacidad. |
| [`gold_pronostico_escenarios_anual`](#gold_pronostico_escenarios_anual) | 11 | Fase 5. Escenarios sumados al año, por supuesto de golpe de tormenta. |
| [`gold_pronostico_forma_anio`](#gold_pronostico_forma_anio) | 60 | Fase 5. Forma del año: índice estacional de cada mes por serie. |
| [`gold_pronostico_fuerza_estacional`](#gold_pronostico_fuerza_estacional) | 5 | Fase 5. Fuerza estacional por serie (clásica y STL). |
| [`gold_pronostico_mes`](#gold_pronostico_mes) | 60 | Fase 5. Pronóstico de los próximos 12 meses con su rango del 90 % (_est). |
| [`gold_pronostico_metricas`](#gold_pronostico_metricas) | 25 | Fase 5. Errores (MAE, MAPE) de cada modelo por serie. |
| [`gold_pronostico_poisson_tormentas`](#gold_pronostico_poisson_tormentas) | 12 | Fase 5. Probabilidad de tormenta por mes (Poisson, 1966–2025). |
| [`gold_pronostico_sensibilidad`](#gold_pronostico_sensibilidad) | 6 | Fase 5. Efecto de lluvia y dólar en cada serie, con su p-valor. |
| [`gold_pronostico_series`](#gold_pronostico_series) | 454 | Fase 5. Series mensuales que se pronostican, con huecos y tramos marcados. |
| [`gold_radar_clusters_centros`](#gold_radar_clusters_centros) | 55 | Fase 4. Agrupamiento Ward de los centros turísticos del país (DataTur). |
| [`gold_radar_estado`](#gold_radar_estado) | 825 | Fase 4. Índice de presión y estado (tranquilo/concurrido/saturado) por lugar y mes. |
| [`gold_radar_indice_comparable`](#gold_radar_indice_comparable) | 770 | Fase 4. Índice comparable (mismas medidas en todos los lugares). |
| [`gold_radar_markov_backtest`](#gold_radar_markov_backtest) | 9 | Fase 4. Prueba de la cadena de Markov semanal contra la persistencia. |
| [`gold_radar_markov_matriz`](#gold_radar_markov_matriz) | 3 | Fase 4. Matriz de transición semanal entre estados (norte, DataTur). |
| [`gold_radar_markov_riesgo`](#gold_radar_markov_riesgo) | 7 | Fase 4. Probabilidad de cada estado a 1–8 semanas. |
| [`gold_radar_modelos`](#gold_radar_modelos) | 4 | Fase 4. Comparación de clasificadores del estado del mes siguiente. |
| [`gold_radar_panel_mensual`](#gold_radar_panel_mensual) | 825 | Fase 4. Panel lugar × mes con todas las variables de presión. |
| [`gold_radar_prediccion`](#gold_radar_prediccion) | 13 | Fase 4. Estado esperado del mes siguiente por lugar (_est). |
| [`gold_radar_sesgo`](#gold_radar_sesgo) | 2 | Fase 4. Aciertos del modelo en los 5 lugares contra el norte (sesgo). |
| [`gold_reconciliacion_cruceros`](#gold_reconciliacion_cruceros) | 182 | Fase 2. Cruceristas: DataTur contra SITUR-Q, mes a mes, en Cozumel y Mahahual. |

## silver_afac

Pasajeros por aerolínea en México, por mes (AFAC vía DataTur, 2016 → jul-2026). Nacional. **19,277 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `mes` | BIGINT | 0.0 % | 1 | Mes (1–12). |
| `tipo_vuelo` | VARCHAR | 0.0 % | internacional | nacional o internacional. |
| `servicio` | VARCHAR | 0.0 % | fletamento | regular o fletamento. |
| `region_aerolinea` | VARCHAR | 0.0 % | Canadiense | Región de origen de la aerolínea. |
| `aerolinea` | VARCHAR | 0.0 % | Air Transat | Aerolínea. |
| `periodo` | DATE | 0.0 % | 2016-01-01 | Primer día del mes. |
| `archivo` | VARCHAR | 0.0 % | datos\bronze\datatur\2026-09-28\afac\DB_… | Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2). |
| `pasajeros` | BIGINT | 0.0 % | 52930 | Pasajeros (AFAC: transportados; cruceros: pasajeros que llegaron en el mes). |
| `sumada_flag` | BOOLEAN | 0.0 % | False | Verdadero si el renglón suma dos cifras de la misma etiqueta (Virgin America + Alaska, 2016–ene-2018). |
| `anio` | BIGINT | 0.0 % | 2016 | Año. |

## silver_clima_diario

Clima diario de 8 puntos de Quintana Roo (Open-Meteo, 1950 → 2026). **224,232 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `punto` | VARCHAR | 0.0 % | bacalar | Punto de clima (8 puntos de Quintana Roo). |
| `region_campana` | VARCHAR | 0.0 % | Bacalar | Región de la campaña a la que pertenece. |
| `papel_campana` | VARCHAR | 0.0 % | excluida | Papel en la campaña: promovida, referencia, retirada o excluida (docs/regiones/REGIONES.md). |
| `fecha` | DATE | 0.0 % | 1950-01-01 | Fecha. |
| `mes` | BIGINT | 0.0 % | 1 | Mes (1–12). |
| `temp_max_c` | DOUBLE | 0.0 % | 25.0 | Temperatura máxima del día (°C). |
| `lluvia_mm` | DOUBLE | 0.0 % | 7.3 | Lluvia (mm). |
| `viento_max_kmh` | DOUBLE | 0.0 % | 10.5 | Viento máximo del día (km/h). |
| `sin_dato_flag` | BOOLEAN | 0.0 % | False | Verdadero si la fuente no trae dato (hueco; no se rellena). |
| `lat` | DOUBLE | 0.0 % | 18.664322 | Latitud (grados). |
| `lon` | DOUBLE | 0.0 % | -88.41019 | Longitud (grados). |
| `fuente_tipo` | VARCHAR | 0.0 % | reanálisis ERA5 (Open-Meteo) | Tipo de dato de la fuente (observado o reanálisis). |
| `archivo` | VARCHAR | 0.0 % | datos\bronze\clima\2026-09-28\diario\bac… | Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2). |
| `anio` | BIGINT | 0.0 % | 1950 | Año. |

## silver_clima_horario

Clima por hora de 8 puntos (Open-Meteo, 2019 → 2026), con hora local. **542,784 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `punto` | VARCHAR | 0.0 % | bacalar | Punto de clima (8 puntos de Quintana Roo). |
| `region_campana` | VARCHAR | 0.0 % | Bacalar | Región de la campaña a la que pertenece. |
| `papel_campana` | VARCHAR | 0.0 % | excluida | Papel en la campaña: promovida, referencia, retirada o excluida (docs/regiones/REGIONES.md). |
| `fecha_hora_utc` | TIMESTAMP | 0.0 % | 2019-01-01 06:00:00 | Fecha y hora en UTC, como la entrega la fuente. |
| `fecha_hora_local` | TIMESTAMP | 0.0 % | 2019-01-01 01:00:00 | Fecha y hora local (UTC − 5 h). |
| `temp_c` | DOUBLE | 0.0 % | 25.2 | Temperatura (°C). |
| `lluvia_mm` | DOUBLE | 0.0 % | 0.0 | Lluvia (mm). |
| `viento_kmh` | DOUBLE | 0.0 % | 9.4 | Viento (km/h). |
| `sin_dato_flag` | BOOLEAN | 0.0 % | False | Verdadero si la fuente no trae dato (hueco; no se rellena). |
| `lat` | DOUBLE | 0.0 % | 18.664322 | Latitud (grados). |
| `lon` | DOUBLE | 0.0 % | -88.41019 | Longitud (grados). |
| `fuente_tipo` | VARCHAR | 0.0 % | reanálisis ERA5 (Open-Meteo) | Tipo de dato de la fuente (observado o reanálisis). |
| `archivo` | VARCHAR | 0.0 % | datos\bronze\clima\2026-09-28\horario\ba… | Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2). |
| `anio` | BIGINT | 0.0 % | 2018 | Año. |

## silver_cruceros

Arribos y pasajeros de crucero por puerto y mes (DataTur, 2016 → jul-2026). **3,895 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `estado` | VARCHAR | 0.0 % | Baja California Sur | Entidad federativa. |
| `puerto` | VARCHAR | 0.0 % | Santa Rosalía | Puerto de cruceros. |
| `mes` | BIGINT | 0.0 % | 1 | Mes (1–12). |
| `periodo` | DATE | 0.0 % | 2016-01-01 | Primer día del mes. |
| `arribos` | BIGINT | 0.0 % | 0 | Barcos que llegaron en el mes. |
| `pasajeros` | BIGINT | 0.0 % | 0 | Pasajeros (AFAC: transportados; cruceros: pasajeros que llegaron en el mes). |
| `lat` | DOUBLE | 0.0 % | 27.322009 | Latitud (grados). |
| `lon` | DOUBLE | 0.0 % | -112.251764 | Longitud (grados). |
| `litoral` | VARCHAR | 0.0 % | Pacífico | Pacífico o Golfo-Caribe. |
| `archivo` | VARCHAR | 0.0 % | datos\bronze\datatur\2026-09-28\cruceros… | Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2). |
| `puerto_sin_cruceros_flag` | BOOLEAN | 0.0 % | False | Verdadero si el puerto tiene 0 pasajeros en toda la serie (catálogo sin cruceros). |
| `es_qroo` | BOOLEAN | 0.0 % | False | Verdadero si es de Quintana Roo. |
| `papel_campana` | VARCHAR | 0.0 % | NaN | Papel en la campaña: promovida, referencia, retirada o excluida (docs/regiones/REGIONES.md). |
| `anio` | BIGINT | 0.0 % | 2016 | Año. |

## silver_datatur_ocupacion

Ocupación hotelera semanal y mensual por centro turístico (DataTur, 2022 → 2026). **23,341 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `anio` | BIGINT | 0.0 % | 2022 | Año. |
| `archivo` | VARCHAR | 0.0 % | 2024-MES_11_Publico.zip | Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2). |
| `centro` | VARCHAR | 0.0 % | 3/ Datos No Comparables Con El Periodo A… | Centro turístico (nombre limpio). |
| `centro_crudo` | VARCHAR | 0.0 % | 3/ Datos no comparables con el periodo a… | Centro turístico tal como viene en el archivo. |
| `cuartos_disponibles` | DOUBLE | 1.6 % | 0.0 | Cuartos disponibles promedio diario. |
| `cuartos_ocupados` | DOUBLE | 1.6 % | 0.0 | Cuartos ocupados promedio diario. |
| `es_qroo` | BOOLEAN | 0.0 % | False | Verdadero si es de Quintana Roo. |
| `estado` | VARCHAR | 16.5 % | GRO | Entidad federativa. |
| `mes` | BIGINT | 80.9 % | 11 | Mes (1–12). |
| `no_disponible_flag` | BOOLEAN | 0.0 % | False | Verdadero si la fuente marca el dato como no disponible. |
| `nota_al_pie` | VARCHAR | 87.7 % | Para establecer una comparación con peri… | Nota al pie de la fuente (bandera de comparabilidad). |
| `ocupacion_pct` | DOUBLE | 1.8 % | 43.81 | Ocupación hotelera (%). |
| `periodo` | DATE | 0.0 % | 2022-11-01 | Primer día del mes. |
| `semana` | BIGINT | 19.1 % | 23 | Semana del año (ISO). |
| `tipo_fila` | VARCHAR | 0.0 % | desglose | Tipo de renglón en la fuente (dato, total o nota). |
| `n_versiones` | BIGINT | 0.0 % | 1 | Cuántas veces se publicó la misma semana o mes. |
| `revisado_flag` | BOOLEAN | 0.0 % | False | Verdadero si la cifra cambió entre publicaciones (se conserva la última). |
| `ocupacion_calc_pct` | DOUBLE | 1.8 % | 43.81 | Ocupación recalculada como ocupados ÷ disponibles × 100 (comprobación). |
| `frecuencia` | VARCHAR | 0.0 % | mensual | semanal o mensual. |

## silver_denue

Negocios del país con giro, tamaño y coordenadas (DENUE INEGI), con su categoría turística. **6,138,075 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `id` | VARCHAR | 0.0 % | 10000528 | Identificador del negocio en el DENUE. |
| `nom_estab` | VARCHAR | 0.1 % | SOPORTE TECNICO PARA TU CELULAR I FIX | Nombre del establecimiento. |
| `codigo_act` | VARCHAR | 0.0 % | 466212 | Código SCIAN de la actividad. |
| `nombre_act` | VARCHAR | 0.0 % | Comercio al por menor de teléfonos y otr… | Actividad económica. |
| `per_ocu` | VARCHAR | 0.0 % | 0 a 5 personas | Personal ocupado (rango, como lo publica INEGI). |
| `tipoUniEco` | VARCHAR | 0.0 % | Fijo | Tipo de unidad económica (fija o semifija). |
| `entidad` | VARCHAR | 0.0 % | Aguascalientes | Entidad federativa. |
| `cve_mun` | VARCHAR | 0.0 % | 001 | Clave INEGI del municipio. |
| `municipio` | VARCHAR | 0.0 % | Aguascalientes | Municipio. |
| `cve_loc` | VARCHAR | 0.0 % | 0001 | Clave INEGI de la localidad. |
| `localidad` | VARCHAR | 0.0 % | Aguascalientes | Localidad. |
| `cod_postal` | VARCHAR | 0.1 % | 20010 | Código postal. |
| `latitud` | DOUBLE | 0.0 % | 21.89409389 | Latitud (grados). |
| `longitud` | DOUBLE | 0.0 % | -102.32130723 | Longitud (grados). |
| `fecha_alta` | VARCHAR | 0.0 % | 2024-11 | Fecha de alta en el DENUE. |
| `scian_3` | VARCHAR | 0.0 % | 466 | Subsector SCIAN (3 dígitos). |
| `categoria_turistica` | VARCHAR | 85.7 % | Alimentos y bebidas | Categoría turística (hospedaje, alimentos, etc.). |
| `es_turistico` | BOOLEAN | 0.0 % | False | Verdadero si el giro es turístico. |
| `personas_min` | INTEGER | 0.0 % | 0 | Límite inferior del rango de personal. |
| `personas_max` | INTEGER | 0.2 % | 5 | Límite superior del rango de personal. |
| `coordenadas_flag` | BOOLEAN | 0.0 % | False | Verdadero si las coordenadas caen fuera de su municipio o faltan. |
| `es_qroo` | BOOLEAN | 0.0 % | False | Verdadero si es de Quintana Roo. |
| `fuente` | VARCHAR | 0.0 % | INEGI DENUE, descarga 2026-09-28 | Fuente oficial. |
| `cve_ent` | VARCHAR | 0.0 % | 01 | Clave INEGI de la entidad. |

## silver_fred_diario

Pesos por dólar por día (FRED, DEXMXUS). **8,575 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `fecha` | DATE | 0.0 % | 1993-11-08 | Fecha. |
| `mes` | BIGINT | 0.0 % | 11 | Mes (1–12). |
| `pesos_por_dolar` | DOUBLE | 0.0 % | 3.152 | Pesos mexicanos por dólar. |
| `sin_dato_flag` | BOOLEAN | 0.0 % | False | Verdadero si la fuente no trae dato (hueco; no se rellena). |
| `archivo` | VARCHAR | 0.0 % | datos\bronze\fred\2026-09-28\DEXMXUS.csv | Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2). |
| `anio` | BIGINT | 0.0 % | 1993 | Año. |

## silver_fred_mensual

Pesos por dólar promedio del mes e inflación de EE. UU. (FRED). **957 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `periodo` | DATE | 0.0 % | 1947-01-01 | Primer día del mes. |
| `anio` | BIGINT | 0.0 % | 1947 | Año. |
| `mes` | BIGINT | 0.0 % | 1 | Mes (1–12). |
| `pesos_por_dolar` | DOUBLE | 0.0 % | nan | Pesos mexicanos por dólar. |
| `n_dias_observados` | DOUBLE | 0.0 % | nan | Días con cotización en el mes. |
| `n_dias_sin_dato` | DOUBLE | 0.0 % | nan | Días hábiles sin cotización (feriados). |
| `mes_incompleto_flag` | BOOLEAN | 0.0 % | False | Verdadero si el mes aún no termina. |
| `inflacion_eeuu_indice` | DOUBLE | 0.0 % | 21.48 | Índice de precios al consumidor de EE. UU. |

## silver_huracanes

Posiciones de todas las tormentas del Atlántico cada 6 horas (HURDAT2, NOAA, 1851 → 2025). **55,524 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `id_tormenta` | VARCHAR | 0.0 % | AL011851 | Identificador de la tormenta (HURDAT2). |
| `nombre` | VARCHAR | 0.0 % | UNNAMED | Nombre (tormenta o sitio INAH). |
| `mes` | BIGINT | 0.0 % | 6 | Mes (1–12). |
| `fecha` | DATE | 0.0 % | 1851-06-25 | Fecha. |
| `hora_utc` | BIGINT | 0.0 % | 0 | Hora UTC (HHMM). |
| `marca` | VARCHAR | 97.7 % | L | Marca especial del registro (p. ej., L = toca tierra). |
| `estado_sistema` | VARCHAR | 0.0 % | HU | Tipo de sistema (HU huracán, TS tormenta tropical, etc.). |
| `lat` | DOUBLE | 0.0 % | 28.0 | Latitud (grados). |
| `lon` | DOUBLE | 0.0 % | -94.8 | Longitud (grados). |
| `viento_kt` | DOUBLE | 0.0 % | 80.0 | Viento sostenido (nudos). |
| `presion_mb` | DOUBLE | 0.0 % | nan | Presión central (mb); vacío si la fuente trae −999. |
| `km_chetumal` | DOUBLE | 0.0 % | 1247.1 | Distancia a Chetumal (km). |
| `dentro_radio_flag` | BOOLEAN | 0.0 % | False | Verdadero si pasa a ≤ 200 km de Chetumal. |
| `tormenta_o_huracan_flag` | BOOLEAN | 0.0 % | True | Verdadero si el viento es ≥ 34 nudos. |
| `era_satelital_flag` | BOOLEAN | 0.0 % | False | Verdadero desde 1966 (era satelital). |
| `afecta_sur_flag` | BOOLEAN | 0.0 % | False | Verdadero si cumple las tres reglas anteriores. |
| `formato_irregular_flag` | BOOLEAN | 0.0 % | False | Verdadero si la línea original venía mal formada. |
| `archivo` | VARCHAR | 0.0 % | datos\bronze\huracanes\2026-09-28\hurdat… | Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2). |
| `anio` | BIGINT | 0.0 % | 1851 | Año. |

## silver_inah

Visitantes a museos y zonas arqueológicas por mes y tipo (INAH vía DataTur, 2016 → 2026). **71,278 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `clasificacion` | VARCHAR | 0.0 % | Museos | Museo o zona arqueológica. |
| `estado` | VARCHAR | 0.0 % | Aguascalientes | Entidad federativa. |
| `nombre` | VARCHAR | 0.0 % | Museo Regional de Historia de Aguascalie… | Nombre (tormenta o sitio INAH). |
| `mes` | BIGINT | 0.0 % | 1 | Mes (1–12). |
| `periodo` | DATE | 0.0 % | 2016-01-01 | Primer día del mes. |
| `tipo_visitante` | VARCHAR | 0.0 % | extranjero | nacional o extranjero. |
| `visitantes` | BIGINT | 0.0 % | 38 | Visitantes en el mes. |
| `archivo` | VARCHAR | 0.0 % | datos\bronze\datatur\2026-09-28\inah\BdI… | Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2). |
| `region_campana` | VARCHAR | 0.4 % | NaN | Región de la campaña a la que pertenece. |
| `papel_campana` | VARCHAR | 0.4 % | NaN | Papel en la campaña: promovida, referencia, retirada o excluida (docs/regiones/REGIONES.md). |
| `es_qroo` | BOOLEAN | 0.0 % | False | Verdadero si es de Quintana Roo. |
| `sin_visitantes_flag` | BOOLEAN | 0.0 % | False | Verdadero si el mes tiene 0 visitantes (suele ser cierre). |
| `anio` | BIGINT | 0.0 % | 2016 | Año. |

## silver_iter

Población y viviendas por localidad (Censo 2020, ITER Quintana Roo). **2,243 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `cve_mun` | VARCHAR | 0.0 % | 000 | Clave INEGI del municipio. |
| `municipio` | VARCHAR | 0.0 % | Total de la entidad Quintana Roo | Municipio. |
| `cve_loc` | VARCHAR | 0.0 % | 0000 | Clave INEGI de la localidad. |
| `localidad` | VARCHAR | 0.0 % | Total de la Entidad | Localidad. |
| `poblacion` | DOUBLE | 0.0 % | 1857985.0 | Habitantes (Censo 2020). |
| `viviendas_habitadas` | DOUBLE | 0.0 % | 575489.0 | Viviendas particulares habitadas. |
| `viviendas_con_agua` | DOUBLE | 0.0 % | 558100.0 | Viviendas con agua entubada. |
| `viviendas_con_drenaje` | DOUBLE | 0.0 % | 556294.0 | Viviendas con drenaje. |
| `viviendas_con_luz` | DOUBLE | 0.0 % | 562025.0 | Viviendas con electricidad. |
| `tipo_fila` | VARCHAR | 0.0 % | total_estatal | Tipo de renglón en la fuente (dato, total o nota). |
| `reservado_flag` | BOOLEAN | 0.0 % | False | Verdadero si INEGI reserva el dato por confidencialidad. |
| `latitud` | DOUBLE | 0.0 % | nan | Latitud (grados). |
| `longitud` | DOUBLE | 0.0 % | nan | Longitud (grados). |
| `archivo` | VARCHAR | 0.0 % | datos\bronze\iter\2026-09-28\iter_23_cpv… | Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2). |
| `region_campana` | VARCHAR | 99.3 % | Maya Ka'an + Kantemó | Región de la campaña a la que pertenece. |
| `papel_campana` | VARCHAR | 99.3 % | promovida | Papel en la campaña: promovida, referencia, retirada o excluida (docs/regiones/REGIONES.md). |

## silver_nacionalidad

Llegadas de extranjeros por avión, por aeropuerto, país y sexo (UPM vía DataTur, 2012 → jul-2026). **521,363 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `mes` | BIGINT | 0.0 % | 1 | Mes (1–12). |
| `periodo` | DATE | 0.0 % | 2012-01-01 | Primer día del mes. |
| `aeropuerto` | VARCHAR | 0.0 % | Acapulco, Gro. | Aeropuerto de llegada. |
| `pais` | VARCHAR | 0.0 % | Alemania | País de nacionalidad. |
| `region_mundo` | VARCHAR | 0.0 % | Europa | Región del mundo. |
| `sexo` | VARCHAR | 0.0 % | hombre | hombre, mujer o no disponible. |
| `llegadas_extranjeros` | BIGINT | 0.0 % | 1 | Extranjeros que llegaron por avión en el mes. |
| `archivo` | VARCHAR | 0.0 % | datos\bronze\datatur\2026-09-28\nacional… | Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2). |
| `es_qroo` | BOOLEAN | 0.0 % | False | Verdadero si es de Quintana Roo. |
| `lugar_campana` | VARCHAR | 84.0 % | Cancún | Lugar de la campaña al que pertenece. |
| `papel_campana` | VARCHAR | 84.0 % | referencia | Papel en la campaña: promovida, referencia, retirada o excluida (docs/regiones/REGIONES.md). |
| `anio` | BIGINT | 0.0 % | 2012 | Año. |

## silver_restmex

Reseñas de turistas con calificación de 1 a 5 (Rest-Mex 2025, CC-BY-4.0). **207,873 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `titulo` | VARCHAR | 0.0 % | esperanzados con los delfines | Título de la reseña. |
| `resena` | VARCHAR | 0.0 % | ¿Cómo puede alguien resistir el nombre s… | Texto de la reseña. |
| `calificacion` | INTEGER | 0.0 % | 4 | Calificación de 1 a 5. |
| `pueblo` | VARCHAR | 0.0 % | Loreto | Pueblo reseñado. |
| `tipo` | VARCHAR | 0.0 % | restaurante | hotel, restaurante o atractivo. |
| `es_qroo` | BOOLEAN | 0.0 % | False | Verdadero si es de Quintana Roo. |
| `papel_campana` | VARCHAR | 58.6 % | referencia | Papel en la campaña: promovida, referencia, retirada o excluida (docs/regiones/REGIONES.md). |
| `n_palabras` | INTEGER | 0.0 % | 56 | Palabras de la reseña. |
| `archivo` | VARCHAR | 0.0 % | datos\bronze\restmex\2026-09-28\Rest-Mex… | Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2). |
| `estado` | VARCHAR | 0.0 % | Baja California Sur | Entidad federativa. |

## silver_siturq

Indicadores turísticos de Quintana Roo por destino y mes (SITUR-Q, API pública). **7,340 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `unidad` | VARCHAR | 0.0 % | Cozumel | Destino o zona de SITUR-Q. |
| `anio` | BIGINT | 0.0 % | 2025 | Año. |
| `mes` | INTEGER | 0.0 % | 12 | Mes (1–12). |
| `tipo_unidad` | VARCHAR | 0.0 % | destino | destino, zona o zona especial. |
| `variable` | VARCHAR | 0.0 % | total_de_llegadas_de_pasajeros | Variable medida. |
| `valor` | DOUBLE | 11.4 % | 0.0 | Valor de la variable. |
| `n_registros_fuente` | BIGINT | 0.0 % | 1 | Registros de la fuente que se sumaron. |
| `hueco_flag` | BOOLEAN | 0.0 % | True | Verdadero si la fuente trae 0 o vacío donde debería haber dato (hueco declarado). |
| `periodo` | DATE | 0.0 % | 2025-12-01 | Primer día del mes. |
| `fuente` | VARCHAR | 0.0 % | SITUR-Q, descarga 2026-09-28 | Fuente oficial. |
| `indicador` | VARCHAR | 0.0 % | aereos_llegadas | Indicador de SITUR-Q (ocupación, cruceristas, Tren Maya, etc.). |

## dim_lugar

Dimensión de lugares: cada lugar con su papel (promovido, referencia o comparación). **15 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `lugar` | VARCHAR | 0.0 % | Chetumal | Lugar. |
| `es_de_los_5` | BOOLEAN | 0.0 % | True | Verdadero si es una de las 5 regiones de la campaña. |
| `papel` | VARCHAR | 0.0 % | promovido | promovido, referencia o comparación. |

## dim_tiempo

Dimensión de tiempo: un renglón por mes, de 2012 a 2027. **192 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `periodo` | DATE | 0.0 % | 2012-01-01 | Primer día del mes. |
| `anio` | BIGINT | 0.0 % | 2012 | Año. |
| `mes` | BIGINT | 0.0 % | 1 | Mes (1–12). |
| `trimestre` | BIGINT | 0.0 % | 1 | Trimestre (1–4). |

## hechos_mes

Hechos: una medida por lugar, mes y variable, con su fuente. Un hueco no tiene renglón. **3,287 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `lugar` | VARCHAR | 0.0 % | Bacalar | Lugar. |
| `periodo` | DATE | 0.0 % | 2024-12-01 | Primer día del mes. |
| `variable` | VARCHAR | 0.0 % | llegadas_tren | Variable medida. |
| `valor` | DOUBLE | 0.0 % | 2306.0 | Valor de la variable. |
| `fuente` | VARCHAR | 0.0 % | SITUR-Q (Tren Maya) | Fuente oficial. |

## gold_campana_aspectos

Fase 8. Temas de las reseñas: % que los menciona y riesgo relativo de reseña mala. **36 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `pueblo` | VARCHAR | 0.0 % | Bacalar | Pueblo reseñado. |
| `aspecto` | VARCHAR | 0.0 % | multitudes | Ver la nota de decisión de su fase. |
| `resenas` | BIGINT | 0.0 % | 1103 | Ver la nota de decisión de su fase. |
| `pct_menciona` | DOUBLE | 0.0 % | 10.192201071890594 | Ver la nota de decisión de su fase. |
| `pct_malas` | DOUBLE | 0.0 % | 9.15684496826836 | Ver la nota de decisión de su fase. |
| `pct_malas_pueblo` | DOUBLE | 0.0 % | 4.999075956385141 | Ver la nota de decisión de su fase. |
| `riesgo_relativo` | DOUBLE | 0.0 % | 1.831707509179301 | Ver la nota de decisión de su fase. |

## gold_campana_palabras

Fase 8. Palabras que distinguen reseñas de 5 estrellas y malas (log-odds). **40 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `palabra` | VARCHAR | 0.0 % | excelente | Ver la nota de decisión de su fase. |
| `en_cinco` | BIGINT | 0.0 % | 18952 | Ver la nota de decisión de su fase. |
| `en_malas` | BIGINT | 0.0 % | 144 | Ver la nota de decisión de su fase. |
| `delta` | DOUBLE | 0.0 % | 1.7107044666107356 | Ver la nota de decisión de su fase. |
| `z` | DOUBLE | 0.0 % | 31.038785547713555 | Ver la nota de decisión de su fase. |
| `lado` | VARCHAR | 0.0 % | reseñas de 5 estrellas | Ver la nota de decisión de su fase. |

## gold_campana_reglas

Fase 8. Reglas de asociación (Apriori) que terminan en reseña mala o de 5 estrellas. **30 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `si` | VARCHAR | 0.0 % | comida + servicio | Ver la nota de decisión de su fase. |
| `entonces` | VARCHAR | 0.0 % | reseña de 5 | Ver la nota de decisión de su fase. |
| `soporte` | DOUBLE | 0.0 % | 0.2009954993196646 | Ver la nota de decisión de su fase. |
| `confianza` | DOUBLE | 0.0 % | 0.7813291139240506 | Ver la nota de decisión de su fase. |
| `lift` | DOUBLE | 0.0 % | 1.1182075583200848 | Ver la nota de decisión de su fase. |

## gold_criterios_regiones

Fase 3. Tabla de los 5 criterios por región (sargazo, cierres, saturación, fragilidad, datos). **8 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `region` | VARCHAR | 0.0 % | Chetumal | Ver la nota de decisión de su fase. |
| `papel` | VARCHAR | 0.0 % | promovida | promovido, referencia o comparación. |
| `c1_sargazo` | VARCHAR | 0.0 % | vigilancia | Ver la nota de decisión de su fase. |
| `c1_evidencia` | VARCHAR | 0.0 % | Sin sargazo en su costa; sí en los canal… | Ver la nota de decisión de su fase. |
| `c2_meses_abierta_min` | DOUBLE | 50.0 % | 21.0 | Ver la nota de decisión de su fase. |
| `c2_meses_cerrada_2026` | DOUBLE | 50.0 % | 0.0 | Ver la nota de decisión de su fase. |
| `c2_pasa` | BOOLEAN | 0.0 % | True | Ver la nota de decisión de su fase. |
| `c2_evidencia` | VARCHAR | 0.0 % | Sin zona INAH; sin cierres reportados en… | Ver la nota de decisión de su fase. |
| `c3_ocupacion_2024_pct` | DOUBLE | 37.5 % | 58.0 | Ver la nota de decisión de su fase. |
| `c3_visitantes_inah_por_residente` | DOUBLE | 50.0 % | 1.98 | Ver la nota de decisión de su fase. |
| `c3_negocios_turisticos_por_mil` | DOUBLE | 0.0 % | 8.5 | Ver la nota de decisión de su fase. |
| `c4_viviendas_sin_agua_pct` | DOUBLE | 0.0 % | 1.4 | Ver la nota de decisión de su fase. |
| `c4_viviendas_sin_drenaje_pct` | DOUBLE | 0.0 % | 1.1 | Ver la nota de decisión de su fase. |
| `c4_fragilidad_documental` | VARCHAR | 75.0 % | Poca oferta instalada: límite por capaci… | Ver la nota de decisión de su fase. |
| `c5_series_oficiales` | BIGINT | 0.0 % | 4 | Ver la nota de decisión de su fase. |
| `c5_cuales` | VARCHAR | 0.0 % | negocios (INEGI), Censo 2020, ocupación … | Ver la nota de decisión de su fase. |
| `poblacion_2020` | BIGINT | 0.0 % | 169028 | Ver la nota de decisión de su fase. |
| `negocios_turisticos` | BIGINT | 0.0 % | 1442 | Ver la nota de decisión de su fase. |
| `visitantes_inah_2025` | DOUBLE | 50.0 % | 11017.0 | Ver la nota de decisión de su fase. |

## gold_envivo_decisiones

Fase 7. Qué hizo la Torre cada semana en cada lugar del sur y cuánto dinero gastó o guardó. **717 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `semana` | TIMESTAMP_NS | 0.0 % | 2022-01-03 00:00:00 | Semana del año (ISO). |
| `lugar` | VARCHAR | 0.0 % | Chetumal | Lugar. |
| `pesos_plan` | DOUBLE | 0.0 % | 1130.0022999999999 | Ver la nota de decisión de su fase. |
| `pesos_gastados` | DOUBLE | 0.0 % | 1130.0022999999999 | Ver la nota de decisión de su fase. |
| `motivo` | VARCHAR | 93.3 % | clima raro (150 mm de lluvia en la seman… | Ver la nota de decisión de su fase. |
| `accion` | VARCHAR | 0.0 % | encendido | Ver la nota de decisión de su fase. |
| `arrastre` | DOUBLE | 0.0 % | 0.0 | Ver la nota de decisión de su fase. |
| `sin_dato_tormentas` | BOOLEAN | 0.0 % | False | Ver la nota de decisión de su fase. |
| `lote` | BIGINT | 0.0 % | 0 | Ver la nota de decisión de su fase. |

## gold_envivo_norte

Fase 7. Semanas con el norte saturado y si se encendió "¿Ibas al norte?". **239 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `semana` | TIMESTAMP_NS | 0.0 % | 2022-01-03 00:00:00 | Semana del año (ISO). |
| `norte_lleno` | VARCHAR | 96.2 % | Riviera Maya | Ver la nota de decisión de su fase. |
| `ibas_al_norte` | BOOLEAN | 0.0 % | False | Ver la nota de decisión de su fase. |
| `destino` | VARCHAR | 97.5 % | Bahía Calderitas–Oxtankah | Ver la nota de decisión de su fase. |
| `cancun_pct` | DOUBLE | 0.0 % | 73.04 | Ver la nota de decisión de su fase. |
| `riviera_pct` | DOUBLE | 0.0 % | 71.53999999999999 | Ver la nota de decisión de su fase. |
| `lote` | BIGINT | 0.0 % | 0 | Ver la nota de decisión de su fase. |

## gold_envivo_senales

Fase 7. Las cuatro señales de cada semana: norte, tormentas, clima raro y llegadas. **239 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `semana` | TIMESTAMP_NS | 0.0 % | 2022-01-03 00:00:00 | Semana del año (ISO). |
| `cancun_ocupacion_pct` | DOUBLE | 0.0 % | 73.04 | Ver la nota de decisión de su fase. |
| `cancun_estado` | VARCHAR | 0.0 % | concurrido | Ver la nota de decisión de su fase. |
| `cancun_ocupacion_4sem` | DOUBLE | 0.0 % | 73.04 | Ver la nota de decisión de su fase. |
| `riviera_ocupacion_pct` | DOUBLE | 0.0 % | 71.53999999999999 | Ver la nota de decisión de su fase. |
| `riviera_estado` | VARCHAR | 0.0 % | concurrido | Ver la nota de decisión de su fase. |
| `riviera_ocupacion_4sem` | DOUBLE | 0.0 % | 71.53999999999999 | Ver la nota de decisión de su fase. |
| `tormenta_nombre` | VARCHAR | 98.7 % | Lisa | Ver la nota de decisión de su fase. |
| `tormenta` | BOOLEAN | 12.6 % | False | Ver la nota de decisión de su fase. |
| `chetumal_clima_raro` | BOOLEAN | 0.0 % | False | Ver la nota de decisión de su fase. |
| `chetumal_puntaje_anomalia` | DOUBLE | 0.0 % | 0.5401325119164591 | Ver la nota de decisión de su fase. |
| `chetumal_lluvia_mm` | DOUBLE | 0.0 % | 43.2 | Ver la nota de decisión de su fase. |
| `chetumal_viento_max_kmh` | DOUBLE | 0.0 % | 20.8 | Ver la nota de decisión de su fase. |
| `kohunlich_clima_raro` | BOOLEAN | 0.0 % | False | Ver la nota de decisión de su fase. |
| `kohunlich_puntaje_anomalia` | DOUBLE | 0.0 % | 0.5419523955915229 | Ver la nota de decisión de su fase. |
| `kohunlich_lluvia_mm` | DOUBLE | 0.0 % | 43.0 | Ver la nota de decisión de su fase. |
| `kohunlich_viento_max_kmh` | DOUBLE | 0.0 % | 17.6 | Ver la nota de decisión de su fase. |
| `chetumal_mes_dato` | TIMESTAMP_NS | 49.0 % | 2024-03-01 00:00:00 | Ver la nota de decisión de su fase. |
| `chetumal_llegadas` | VARCHAR | 49.0 % | dentro | Ver la nota de decisión de su fase. |
| `bahia_mes_dato` | TIMESTAMP_NS | 0.0 % | 2020-02-01 00:00:00 | Ver la nota de decisión de su fase. |
| `bahia_llegadas` | VARCHAR | 40.2 % | dentro | Ver la nota de decisión de su fase. |
| `ruta_mes_dato` | TIMESTAMP_NS | 0.0 % | 2020-02-01 00:00:00 | Ver la nota de decisión de su fase. |
| `ruta_llegadas` | VARCHAR | 38.1 % | dentro | Ver la nota de decisión de su fase. |
| `corte_p50` | DOUBLE | 0.0 % | 71.16000000000001 | Ver la nota de decisión de su fase. |
| `corte_p90` | DOUBLE | 0.0 % | 85.924 | Ver la nota de decisión de su fase. |

## gold_lugares_clasificados

Planeador. Negocios del DENUE clasificados por léxico (hospedaje, comida, qué hacer). **49,844 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `id` | VARCHAR | 0.0 % | 10006855 | Identificador del negocio en el DENUE. |
| `nom_estab` | VARCHAR | 0.1 % | CARNICERIA Y POLLERIA YAHIR | Nombre del establecimiento. |
| `codigo_act` | VARCHAR | 0.0 % | 461121 | Código SCIAN de la actividad. |
| `nombre_act` | VARCHAR | 0.0 % | Comercio al por menor de carnes rojas | Actividad económica. |
| `cve_mun` | VARCHAR | 0.0 % | 004 | Clave INEGI del municipio. |
| `cve_loc` | VARCHAR | 0.0 % | 0016 | Clave INEGI de la localidad. |
| `localidad` | VARCHAR | 0.0 % | Calderitas | Localidad. |
| `latitud` | DOUBLE | 0.0 % | 18.55448302 | Latitud (grados). |
| `longitud` | DOUBLE | 0.0 % | -88.25736325 | Longitud (grados). |
| `lugar` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah | Lugar. |
| `clasificado` | BOOLEAN | 0.0 % | False | Ver la nota de decisión de su fase. |
| `tipo` | VARCHAR | 85.6 % | Antojitos | hotel, restaurante o atractivo. |
| `grupo` | VARCHAR | 85.6 % | comer | Ver la nota de decisión de su fase. |
| `momento` | VARCHAR | 85.6 % | noche | Ver la nota de decisión de su fase. |
| `regla` | VARCHAR | 85.6 % | giro 722513 | Ver la nota de decisión de su fase. |

## gold_lugares_recomendados

Planeador. Negocios recomendados por lugar y momento del día. **294 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `lugar` | VARCHAR | 0.0 % | Chetumal | Lugar. |
| `grupo` | VARCHAR | 0.0 % | hacer | Ver la nota de decisión de su fase. |
| `momento` | VARCHAR | 0.0 % | dia | Ver la nota de decisión de su fase. |
| `nombre` | VARCHAR | 0.0 % | Excel Servicios Turisticos | Nombre (tormenta o sitio INAH). |
| `tipo` | VARCHAR | 0.0 % | Agencia de viajes y tours | hotel, restaurante o atractivo. |
| `localidad` | VARCHAR | 0.0 % | Chetumal | Localidad. |
| `km` | DOUBLE | 0.0 % | 0.3 | Ver la nota de decisión de su fase. |
| `de_otro_lugar_flag` | BOOLEAN | 0.0 % | False | Ver la nota de decisión de su fase. |
| `lat` | DOUBLE | 0.0 % | 18.49343 | Latitud (grados). |
| `lon` | DOUBLE | 0.0 % | -88.30106 | Longitud (grados). |
| `regla` | VARCHAR | 0.0 % | giro 561510 | Ver la nota de decisión de su fase. |
| `denue_id` | BIGINT | 0.0 % | 10185856 | Ver la nota de decisión de su fase. |

## gold_presupuesto_pareto

Fase 6. Frontera de Pareto: visitantes esperados según la ocupación máxima permitida. **10 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `ocupacion_max` | DOUBLE | 0.0 % | 1.0 | Ver la nota de decisión de su fase. |
| `estado` | VARCHAR | 0.0 % | Optimal | Entidad federativa. |
| `visitantes_esperados` | DOUBLE | 0.0 % | 956.7759729999996 | Ver la nota de decisión de su fase. |
| `lugares_sin_meses` | VARCHAR | 30.0 % | Chetumal | Ver la nota de decisión de su fase. |

## gold_presupuesto_pausas

Fase 6. Si el anuncio sigue encendido en cada escenario (malo, probable, bueno), donde hay gasto. **60 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `escenario` | VARCHAR | 0.0 % | malo | Ver la nota de decisión de su fase. |
| `periodo` | TIMESTAMP_NS | 0.0 % | 2026-10-01 00:00:00 | Primer día del mes. |
| `lugar` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah | Lugar. |
| `encendido` | BIGINT | 0.0 % | 1 | Ver la nota de decisión de su fase. |
| `pesos` | DOUBLE | 0.0 % | 13276.2678 | Ver la nota de decisión de su fase. |

## gold_presupuesto_plan

Fase 6. Pesos y visitantes esperados (_est) por mes, lugar y canal del plan óptimo. **54 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `periodo` | TIMESTAMP_NS | 0.0 % | 2026-10-01 00:00:00 | Primer día del mes. |
| `lugar` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah | Lugar. |
| `canal` | VARCHAR | 0.0 % | Google | Ver la nota de decisión de su fase. |
| `pesos` | DOUBLE | 0.0 % | 3982.8771 | Ver la nota de decisión de su fase. |
| `conversiones_est` | DOUBLE | 0.0 % | 6.331803619106682 | Ver la nota de decisión de su fase. |

## gold_presupuesto_precios_sombra

Fase 6. Precio sombra y holgura del presupuesto, la equidad y los topes por canal. **6 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `regla` | VARCHAR | 0.0 % | presupuesto | Ver la nota de decisión de su fase. |
| `precio_sombra` | DOUBLE | 0.0 % | 0.0015897562 | Ver la nota de decisión de su fase. |
| `holgura` | DOUBLE | 0.0 % | -0.0 | Ver la nota de decisión de su fase. |

## gold_presupuesto_reglas

Fase 6. Visitantes que cuesta cada regla (resolviendo el modelo sin ella). **4 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `regla` | VARCHAR | 0.0 % | Cero anuncio en temporada alta | Ver la nota de decisión de su fase. |
| `visitantes_con_regla` | DOUBLE | 0.0 % | 956.7759729999996 | Ver la nota de decisión de su fase. |
| `visitantes_sin_regla` | DOUBLE | 0.0 % | 956.775982999997 | Ver la nota de decisión de su fase. |
| `costo_visitantes` | DOUBLE | 0.0 % | 9.999997473641997e-06 | Ver la nota de decisión de su fase. |
| `costo_pct` | DOUBLE | 0.0 % | 1.0451764786978401e-06 | Ver la nota de decisión de su fase. |

## gold_presupuesto_sensibilidad

Fase 6. El modelo resuelto con cada supuesto movido (conversión, clic, tormentas, presupuesto). **8 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `caso` | VARCHAR | 0.0 % | Base | Ver la nota de decisión de su fase. |
| `presupuesto_periodo` | DOUBLE | 0.0 % | 187500.0 | Ver la nota de decisión de su fase. |
| `visitantes_esperados` | DOUBLE | 0.0 % | 956.7759729999996 | Ver la nota de decisión de su fase. |
| `pesos_por_visitante` | DOUBLE | 0.0 % | 195.97064024516436 | Ver la nota de decisión de su fase. |
| `pct_Chetumal` | DOUBLE | 0.0 % | 21.618644853333333 | Ver la nota de decisión de su fase. |
| `pct_Bahía Calderitas–Oxtankah` | DOUBLE | 0.0 % | 36.89352181333334 | Ver la nota de decisión de su fase. |
| `pct_Ruta arqueológica del sur` | DOUBLE | 0.0 % | 41.48779893333333 | Ver la nota de decisión de su fase. |
| `pct_Google` | DOUBLE | 0.0 % | 29.999965439999997 | Ver la nota de decisión de su fase. |
| `pct_Facebook` | DOUBLE | 0.0 % | 70.00000016000001 | Ver la nota de decisión de su fase. |
| `pausas_en_escenarios` | BIGINT | 0.0 % | 0 | Ver la nota de decisión de su fase. |

## gold_pronostico_backtest

Fase 5. Cada pronóstico del origen móvil contra el dato real. **9,930 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `serie` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah · visitantes I… | Ver la nota de decisión de su fase. |
| `modelo` | VARCHAR | 0.0 % | Línea base (ingenuo estacional) | Ver la nota de decisión de su fase. |
| `origen` | TIMESTAMP_NS | 0.0 % | 2019-01-01 00:00:00 | Ver la nota de decisión de su fase. |
| `destino` | TIMESTAMP_NS | 0.0 % | 2019-02-01 00:00:00 | Ver la nota de decisión de su fase. |
| `horizonte` | BIGINT | 0.0 % | 1 | Ver la nota de decisión de su fase. |
| `pronostico` | DOUBLE | 0.0 % | 999.0 | Ver la nota de decisión de su fase. |
| `real` | DOUBLE | 0.0 % | 925.0 | Ver la nota de decisión de su fase. |
| `error_abs` | DOUBLE | 0.0 % | 74.0 | Ver la nota de decisión de su fase. |
| `error_pct` | DOUBLE | 0.0 % | 8.0 | Ver la nota de decisión de su fase. |
| `tramo_h` | VARCHAR | 0.0 % | 1–3 | Ver la nota de decisión de su fase. |
| `error_log` | DOUBLE | 0.0 % | 0.0769610411361284 | Ver la nota de decisión de su fase. |
| `q_log` | DOUBLE | 27.3 % | 0.5760130441152072 | Ver la nota de decisión de su fase. |
| `minimo_90` | DOUBLE | 27.3 % | 396.8673894912427 | Ver la nota de decisión de su fase. |
| `maximo_90` | DOUBLE | 27.3 % | 1255.9258160237387 | Ver la nota de decisión de su fase. |
| `dentro_flag` | BOOLEAN | 0.0 % | False | Ver la nota de decisión de su fase. |

## gold_pronostico_calendario

Fase 5. Calendario lugar × mes: temporada alta, tormenta, lluvia y otro mes u otro lugar. **75 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `lugar` | VARCHAR | 0.0 % | Chetumal | Lugar. |
| `papel` | VARCHAR | 0.0 % | promovida | promovido, referencia o comparación. |
| `periodo` | TIMESTAMP_NS | 0.0 % | 2026-10-01 00:00:00 | Primer día del mes. |
| `mes` | BIGINT | 0.0 % | 10 | Mes (1–12). |
| `prob_tormenta` | DOUBLE | 0.0 % | 0.09516258196404048 | Ver la nota de decisión de su fase. |
| `lluvia_normal_mm` | DOUBLE | 0.0 % | 189.0 | Ver la nota de decisión de su fase. |
| `temp_max_normal_c` | DOUBLE | 0.0 % | 29.1 | Ver la nota de decisión de su fase. |
| `punto_clima` | VARCHAR | 0.0 % | chetumal | Ver la nota de decisión de su fase. |
| `indice` | DOUBLE | 0.0 % | 1.007 | Ver la nota de decisión de su fase. |
| `esperado_est` | DOUBLE | 34.7 % | 52238.42056900706 | Ver la nota de decisión de su fase. |
| `minimo_90_est` | DOUBLE | 34.7 % | 41883.0663029679 | Ver la nota de decisión de su fase. |
| `maximo_90_est` | DOUBLE | 34.7 % | 65154.078352450735 | Ver la nota de decisión de su fase. |
| `riesgo_capacidad` | DOUBLE | 34.7 % | 0.0313 | Ver la nota de decisión de su fase. |
| `unidad` | VARCHAR | 34.7 % | cruces al mes | Destino o zona de SITUR-Q. |
| `dentro_del_pronostico_flag` | BOOLEAN | 0.0 % | True | Ver la nota de decisión de su fase. |
| `ocupacion_est` | DOUBLE | 73.3 % | 65.25 | Ver la nota de decisión de su fase. |
| `ocupacion_tipica_pct` | DOUBLE | 60.0 % | 67.5 | Ver la nota de decisión de su fase. |
| `corte_radar_pct` | DOUBLE | 60.0 % | 71.16 | Ver la nota de decisión de su fase. |
| `nivel` | VARCHAR | 0.0 % | normal | Ver la nota de decisión de su fase. |
| `otro_lugar` | VARCHAR | 78.7 % | Bahía Calderitas–Oxtankah | Ver la nota de decisión de su fase. |
| `otro_mes` | BIGINT | 88.0 % | 2 | Ver la nota de decisión de su fase. |

## gold_pronostico_cobertura

Fase 5. Qué tanto el rango del 90 % contuvo al dato real, por modelo y horizonte. **25 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `serie` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah · visitantes I… | Ver la nota de decisión de su fase. |
| `modelo` | VARCHAR | 0.0 % | Gradient Boosting con rezagos | Ver la nota de decisión de su fase. |
| `con_rango` | BIGINT | 0.0 % | 288 | Ver la nota de decisión de su fase. |
| `cobertura_pct` | DOUBLE | 0.0 % | 85.8 | Ver la nota de decisión de su fase. |
| `ancho_mediano_pct` | DOUBLE | 0.0 % | 83.3 | Ver la nota de decisión de su fase. |

## gold_pronostico_eleccion

Fase 5. Modelo elegido por serie (menor error con rango confiable). **25 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `serie` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah · visitantes I… | Ver la nota de decisión de su fase. |
| `modelo` | VARCHAR | 0.0 % | Gradient Boosting con rezagos | Ver la nota de decisión de su fase. |
| `pronosticos` | BIGINT | 0.0 % | 366 | Ver la nota de decisión de su fase. |
| `mae` | DOUBLE | 0.0 % | 230.282 | Ver la nota de decisión de su fase. |
| `mape` | DOUBLE | 0.0 % | 28.744 | Ver la nota de decisión de su fase. |
| `mae_vs_base` | DOUBLE | 0.0 % | 1.405 | Ver la nota de decisión de su fase. |
| `mape_h1–3` | DOUBLE | 0.0 % | 33.226 | Ver la nota de decisión de su fase. |
| `mape_h4–6` | DOUBLE | 0.0 % | 27.122 | Ver la nota de decisión de su fase. |
| `mape_h7–12` | DOUBLE | 0.0 % | 25.479 | Ver la nota de decisión de su fase. |
| `con_rango` | BIGINT | 0.0 % | 288 | Ver la nota de decisión de su fase. |
| `cobertura_pct` | DOUBLE | 0.0 % | 85.8 | Ver la nota de decisión de su fase. |
| `ancho_mediano_pct` | DOUBLE | 0.0 % | 83.3 | Ver la nota de decisión de su fase. |
| `rango_confiable_flag` | BOOLEAN | 0.0 % | True | Ver la nota de decisión de su fase. |
| `elegido_flag` | BOOLEAN | 0.0 % | False | Ver la nota de decisión de su fase. |

## gold_pronostico_escenarios

Fase 5. Monte Carlo: escenarios malo/probable/bueno por mes y riesgo de rebasar capacidad. **132 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `serie` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah · visitantes I… | Ver la nota de decisión de su fase. |
| `lugar` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah | Lugar. |
| `papel` | VARCHAR | 0.0 % | promovida | promovido, referencia o comparación. |
| `periodo` | TIMESTAMP_NS | 0.0 % | 2026-08-01 00:00:00 | Primer día del mes. |
| `golpe_tormenta_supuesto` | DOUBLE | 0.0 % | 0.0 | Ver la nota de decisión de su fase. |
| `esperado_est` | DOUBLE | 0.0 % | 878.9161486036836 | Ver la nota de decisión de su fase. |
| `malo_p10_est` | DOUBLE | 0.0 % | 684.0979851760322 | Ver la nota de decisión de su fase. |
| `probable_p50_est` | DOUBLE | 0.0 % | 930.1573232586031 | Ver la nota de decisión de su fase. |
| `bueno_p90_est` | DOUBLE | 0.0 % | 1201.8793667959392 | Ver la nota de decisión de su fase. |
| `prob_tormenta` | DOUBLE | 18.2 % | 0.1392920235749422 | Ver la nota de decisión de su fase. |
| `capacidad_probada` | DOUBLE | 0.0 % | 1639.0 | Ver la nota de decisión de su fase. |
| `capacidad_probada_mes` | TIMESTAMP_NS | 0.0 % | 2017-04-01 00:00:00 | Ver la nota de decisión de su fase. |
| `riesgo_rebasar_capacidad` | DOUBLE | 0.0 % | 0.0197 | Ver la nota de decisión de su fase. |

## gold_pronostico_escenarios_anual

Fase 5. Escenarios sumados al año, por supuesto de golpe de tormenta. **11 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `serie` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah · visitantes I… | Ver la nota de decisión de su fase. |
| `lugar` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah | Lugar. |
| `golpe_tormenta_supuesto` | DOUBLE | 0.0 % | 0.0 | Ver la nota de decisión de su fase. |
| `malo_p10_est` | DOUBLE | 0.0 % | 10106.040387779822 | Ver la nota de decisión de su fase. |
| `probable_p50_est` | DOUBLE | 0.0 % | 11216.815745739326 | Ver la nota de decisión de su fase. |
| `bueno_p90_est` | DOUBLE | 0.0 % | 13084.667919346348 | Ver la nota de decisión de su fase. |
| `esperado_modelo_est` | DOUBLE | 0.0 % | 10770.909593302425 | Ver la nota de decisión de su fase. |
| `riesgo_algun_mes_sobre_capacidad` | DOUBLE | 0.0 % | 0.242 | Ver la nota de decisión de su fase. |

## gold_pronostico_forma_anio

Fase 5. Forma del año: índice estacional de cada mes por serie. **60 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `serie` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah · visitantes I… | Ver la nota de decisión de su fase. |
| `lugar` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah | Lugar. |
| `papel` | VARCHAR | 0.0 % | promovida | promovido, referencia o comparación. |
| `mes` | BIGINT | 0.0 % | 1 | Mes (1–12). |
| `indice` | DOUBLE | 0.0 % | 1.2508 | Ver la nota de decisión de su fase. |
| `minimo_anios` | DOUBLE | 0.0 % | 0.7507 | Ver la nota de decisión de su fase. |
| `maximo_anios` | DOUBLE | 0.0 % | 1.5641 | Ver la nota de decisión de su fase. |
| `n_anios` | BIGINT | 0.0 % | 6 | Ver la nota de decisión de su fase. |

## gold_pronostico_fuerza_estacional

Fase 5. Fuerza estacional por serie (clásica y STL). **5 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `serie` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah · visitantes I… | Ver la nota de decisión de su fase. |
| `lugar` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah | Lugar. |
| `papel` | VARCHAR | 0.0 % | promovida | promovido, referencia o comparación. |
| `anios_usados` | VARCHAR | 0.0 % | 2016, 2017, 2018, 2019, 2022, 2025 | Ver la nota de decisión de su fase. |
| `n_anios` | BIGINT | 0.0 % | 6 | Ver la nota de decisión de su fase. |
| `fuerza_estacional` | DOUBLE | 0.0 % | 0.684 | Ver la nota de decisión de su fase. |
| `mes_mas_alto` | BIGINT | 0.0 % | 12 | Ver la nota de decisión de su fase. |
| `mes_mas_bajo` | BIGINT | 0.0 % | 9 | Ver la nota de decisión de su fase. |
| `corr_con_stl` | DOUBLE | 0.0 % | 0.96 | Ver la nota de decisión de su fase. |
| `meses_tramo_stl` | BIGINT | 0.0 % | 50 | Ver la nota de decisión de su fase. |

## gold_pronostico_mes

Fase 5. Pronóstico de los próximos 12 meses con su rango del 90 % (_est). **60 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `serie` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah · visitantes I… | Ver la nota de decisión de su fase. |
| `lugar` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah | Lugar. |
| `papel` | VARCHAR | 0.0 % | promovida | promovido, referencia o comparación. |
| `modelo` | VARCHAR | 0.0 % | Regresión con clima | Ver la nota de decisión de su fase. |
| `ultimo_dato` | TIMESTAMP_NS | 0.0 % | 2026-07-01 00:00:00 | Ver la nota de decisión de su fase. |
| `periodo` | TIMESTAMP_NS | 0.0 % | 2026-08-01 00:00:00 | Primer día del mes. |
| `horizonte` | BIGINT | 0.0 % | 1 | Ver la nota de decisión de su fase. |
| `esperado_est` | DOUBLE | 0.0 % | 878.9161486036836 | Ver la nota de decisión de su fase. |
| `minimo_90_est` | DOUBLE | 0.0 % | 631.7030917588872 | Ver la nota de decisión de su fase. |
| `maximo_90_est` | DOUBLE | 0.0 % | 1222.874490174544 | Ver la nota de decisión de su fase. |
| `unidad` | VARCHAR | 0.0 % | visitantes al mes | Destino o zona de SITUR-Q. |

## gold_pronostico_metricas

Fase 5. Errores (MAE, MAPE) de cada modelo por serie. **25 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `serie` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah · visitantes I… | Ver la nota de decisión de su fase. |
| `modelo` | VARCHAR | 0.0 % | Gradient Boosting con rezagos | Ver la nota de decisión de su fase. |
| `pronosticos` | BIGINT | 0.0 % | 366 | Ver la nota de decisión de su fase. |
| `mae` | DOUBLE | 0.0 % | 230.282 | Ver la nota de decisión de su fase. |
| `mape` | DOUBLE | 0.0 % | 28.744 | Ver la nota de decisión de su fase. |
| `mae_vs_base` | DOUBLE | 0.0 % | 1.405 | Ver la nota de decisión de su fase. |
| `mape_h1–3` | DOUBLE | 0.0 % | 33.226 | Ver la nota de decisión de su fase. |
| `mape_h4–6` | DOUBLE | 0.0 % | 27.122 | Ver la nota de decisión de su fase. |
| `mape_h7–12` | DOUBLE | 0.0 % | 25.479 | Ver la nota de decisión de su fase. |

## gold_pronostico_poisson_tormentas

Fase 5. Probabilidad de tormenta por mes (Poisson, 1966–2025). **12 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `mes` | BIGINT | 0.0 % | 1 | Mes (1–12). |
| `eventos` | BIGINT | 0.0 % | 0 | Ver la nota de decisión de su fase. |
| `lambda` | DOUBLE | 0.0 % | 0.0 | Ver la nota de decisión de su fase. |
| `prob_tormenta` | DOUBLE | 0.0 % | 0.0 | Ver la nota de decisión de su fase. |

## gold_pronostico_sensibilidad

Fase 5. Efecto de lluvia y dólar en cada serie, con su p-valor. **6 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `serie` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah · visitantes I… | Ver la nota de decisión de su fase. |
| `lugar` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah | Lugar. |
| `variable` | VARCHAR | 0.0 % | lluvia (+100 mm sobre lo normal) | Variable medida. |
| `coeficiente` | DOUBLE | 0.0 % | -0.10166703915681943 | Ver la nota de decisión de su fase. |
| `efecto_pct` | DOUBLE | 0.0 % | -9.666972478837865 | Ver la nota de decisión de su fase. |
| `p_valor` | DOUBLE | 0.0 % | 0.03884417905751221 | Ver la nota de decisión de su fase. |
| `meses` | BIGINT | 0.0 % | 90 | Ver la nota de decisión de su fase. |
| `significativo_flag` | BOOLEAN | 0.0 % | True | Ver la nota de decisión de su fase. |

## gold_pronostico_series

Fase 5. Series mensuales que se pronostican, con huecos y tramos marcados. **454 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `serie` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah · visitantes I… | Ver la nota de decisión de su fase. |
| `lugar` | VARCHAR | 0.0 % | Bahía Calderitas–Oxtankah | Lugar. |
| `papel` | VARCHAR | 0.0 % | promovida | promovido, referencia o comparación. |
| `periodo` | TIMESTAMP_NS | 0.0 % | 2016-01-01 00:00:00 | Primer día del mes. |
| `valor` | DOUBLE | 0.0 % | 1178.0 | Valor de la variable. |
| `unidad` | VARCHAR | 0.0 % | visitantes al mes | Destino o zona de SITUR-Q. |
| `motivo_hueco` | VARCHAR | 77.8 % | mes parcial | Ver la nota de decisión de su fase. |
| `entrena_flag` | BOOLEAN | 0.0 % | True | Ver la nota de decisión de su fase. |
| `zonas_abiertas` | DOUBLE | 44.1 % | 1.0 | Ver la nota de decisión de su fase. |
| `fuente` | VARCHAR | 0.0 % | INAH vía DataTur (BdINAH) | Fuente oficial. |

## gold_radar_clusters_centros

Fase 4. Agrupamiento Ward de los centros turísticos del país (DataTur). **55 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `centro` | VARCHAR | 0.0 % | Acapulco | Centro turístico (nombre limpio). |
| `ene` | DOUBLE | 0.0 % | 46.32279219148847 | Ver la nota de decisión de su fase. |
| `feb` | DOUBLE | 0.0 % | 43.42142234986946 | Ver la nota de decisión de su fase. |
| `mar` | DOUBLE | 0.0 % | 43.60016605473966 | Ver la nota de decisión de su fase. |
| `abr` | DOUBLE | 0.0 % | 52.18833062669166 | Ver la nota de decisión de su fase. |
| `may` | DOUBLE | 0.0 % | 47.009411146818096 | Ver la nota de decisión de su fase. |
| `jun` | DOUBLE | 0.0 % | 39.31020359306153 | Ver la nota de decisión de su fase. |
| `jul` | DOUBLE | 0.0 % | 45.311371815483554 | Ver la nota de decisión de su fase. |
| `ago` | DOUBLE | 0.0 % | 49.67579468159002 | Ver la nota de decisión de su fase. |
| `sep` | DOUBLE | 0.0 % | 31.457136613944172 | Ver la nota de decisión de su fase. |
| `oct` | DOUBLE | 0.0 % | 28.515729061315863 | Ver la nota de decisión de su fase. |
| `nov` | DOUBLE | 0.0 % | 33.564323193195364 | Ver la nota de decisión de su fase. |
| `dic` | DOUBLE | 0.0 % | 43.59838908753808 | Ver la nota de decisión de su fase. |
| `grupo` | INTEGER | 0.0 % | 2 | Ver la nota de decisión de su fase. |
| `es_qroo` | BOOLEAN | 0.0 % | False | Verdadero si es de Quintana Roo. |
| `nivel` | DOUBLE | 0.0 % | 42.0 | Ver la nota de decisión de su fase. |

## gold_radar_estado

Fase 4. Índice de presión y estado (tranquilo/concurrido/saturado) por lugar y mes. **825 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `lugar` | VARCHAR | 0.0 % | Bacalar | Lugar. |
| `es_de_los_5` | BOOLEAN | 0.0 % | False | Verdadero si es una de las 5 regiones de la campaña. |
| `periodo` | TIMESTAMP_NS | 0.0 % | 2022-01-01 00:00:00 | Primer día del mes. |
| `llegadas_tren_x1000hab` | DOUBLE | 75.9 % | 184.08238205476172 | Ver la nota de decisión de su fase. |
| `cruceristas_x1000hab` | DOUBLE | 86.7 % | 2441.036926608218 | Ver la nota de decisión de su fase. |
| `cruces_belice_x1000hab` | DOUBLE | 93.5 % | 16.943938282414745 | Ver la nota de decisión de su fase. |
| `visitantes_inah_x1000hab` | DOUBLE | 53.3 % | 978.5263830126926 | Ver la nota de decisión de su fase. |
| `llegadas_x_cuarto` | DOUBLE | 62.5 % | 1.5312084993359893 | Ver la nota de decisión de su fase. |
| `ocupacion_pct` | DOUBLE | 50.1 % | 66.49917467715312 | Ocupación hotelera (%). |
| `z_llegadas_tren_x1000hab` | DOUBLE | 75.9 % | 0.36435455838205094 | Ver la nota de decisión de su fase. |
| `z_cruceristas_x1000hab` | DOUBLE | 86.7 % | 0.0 | Ver la nota de decisión de su fase. |
| `z_visitantes_inah_x1000hab` | DOUBLE | 53.3 % | 0.15166534079491745 | Ver la nota de decisión de su fase. |
| `z_llegadas_x_cuarto` | DOUBLE | 62.5 % | 0.0035442755132823675 | Ver la nota de decisión de su fase. |
| `z_ocupacion_pct` | DOUBLE | 50.1 % | 0.6890318372769348 | Ver la nota de decisión de su fase. |
| `ipt` | DOUBLE | 14.8 % | 0.15166534079491745 | Ver la nota de decisión de su fase. |
| `n_componentes` | INTEGER | 0.0 % | 1 | Ver la nota de decisión de su fase. |
| `componentes` | VARCHAR | 0.0 % | visitantes_inah_x1000hab | Ver la nota de decisión de su fase. |
| `estado` | VARCHAR | 0.0 % | tranquilo | Entidad federativa. |
| `corte_p50` | DOUBLE | 0.0 % | 0.25773704634515626 | Ver la nota de decisión de su fase. |
| `corte_p90` | DOUBLE | 0.0 % | 0.7662546174519894 | Ver la nota de decisión de su fase. |

## gold_radar_indice_comparable

Fase 4. Índice comparable (mismas medidas en todos los lugares). **770 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `lugar` | VARCHAR | 0.0 % | Bacalar | Lugar. |
| `es_de_los_5` | BOOLEAN | 0.0 % | False | Verdadero si es una de las 5 regiones de la campaña. |
| `periodo` | TIMESTAMP_NS | 0.0 % | 2022-01-01 00:00:00 | Primer día del mes. |
| `ipt_comparable` | DOUBLE | 33.8 % | 0.21980038437529914 | Ver la nota de decisión de su fase. |
| `medidas` | VARCHAR | 0.0 % | llegadas_tren_x1000hab, visitantes_inah_… | Ver la nota de decisión de su fase. |
| `estado` | VARCHAR | 33.8 % | concurrido | Entidad federativa. |
| `corte_p50` | DOUBLE | 0.0 % | 0.1864548890075533 | Ver la nota de decisión de su fase. |
| `corte_p90` | DOUBLE | 0.0 % | 0.7559985923793381 | Ver la nota de decisión de su fase. |

## gold_radar_markov_backtest

Fase 4. Prueba de la cadena de Markov semanal contra la persistencia. **9 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `k_semanas` | BIGINT | 0.0 % | 1 | Ver la nota de decisión de su fase. |
| `metodo` | VARCHAR | 0.0 % | Markov | Ver la nota de decisión de su fase. |
| `brier` | DOUBLE | 0.0 % | 0.2 | Ver la nota de decisión de su fase. |
| `exactitud` | DOUBLE | 0.0 % | 0.887 | Ver la nota de decisión de su fase. |
| `casos` | BIGINT | 0.0 % | 364 | Ver la nota de decisión de su fase. |

## gold_radar_markov_matriz

Fase 4. Matriz de transición semanal entre estados (norte, DataTur). **3 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `tranquilo` | DOUBLE | 0.0 % | 0.9216867469879518 | Ver la nota de decisión de su fase. |
| `concurrido` | DOUBLE | 0.0 % | 0.0783132530120482 | Ver la nota de decisión de su fase. |
| `saturado` | DOUBLE | 0.0 % | 0.0 | Ver la nota de decisión de su fase. |
| `desde` | VARCHAR | 0.0 % | tranquilo | Ver la nota de decisión de su fase. |

## gold_radar_markov_riesgo

Fase 4. Probabilidad de cada estado a 1–8 semanas. **7 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `centro` | VARCHAR | 0.0 % | Akumal | Centro turístico (nombre limpio). |
| `estado_hoy` | VARCHAR | 0.0 % | tranquilo | Ver la nota de decisión de su fase. |
| `ocupacion_hoy_pct` | DOUBLE | 0.0 % | 34.4 | Ver la nota de decisión de su fase. |
| `sem_1` | DOUBLE | 0.0 % | 0.0 | Ver la nota de decisión de su fase. |
| `sem_2` | DOUBLE | 0.0 % | 0.005392828800230864 | Ver la nota de decisión de su fase. |
| `sem_3` | DOUBLE | 0.0 % | 0.013367288586916253 | Ver la nota de decisión de su fase. |
| `sem_4` | DOUBLE | 0.0 % | 0.02228037082435728 | Ver la nota de decisión de su fase. |
| `sem_5` | DOUBLE | 0.0 % | 0.031203246249902998 | Ver la nota de decisión de su fase. |
| `sem_6` | DOUBLE | 0.0 % | 0.039639534428072845 | Ver la nota de decisión de su fase. |
| `sem_7` | DOUBLE | 0.0 % | 0.04735107054192612 | Ver la nota de decisión de su fase. |
| `sem_8` | DOUBLE | 0.0 % | 0.054250661332433864 | Ver la nota de decisión de su fase. |
| `semana` | TIMESTAMP_NS | 0.0 % | 2026-07-27 00:00:00 | Semana del año (ISO). |

## gold_radar_modelos

Fase 4. Comparación de clasificadores del estado del mes siguiente. **4 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `modelo` | VARCHAR | 0.0 % | Persistencia (línea base) | Ver la nota de decisión de su fase. |
| `f1_macro` | DOUBLE | 0.0 % | 0.774 | Ver la nota de decisión de su fase. |
| `exactitud` | DOUBLE | 0.0 % | 0.808 | Ver la nota de decisión de su fase. |
| `exactitud_5_lugares` | DOUBLE | 0.0 % | 0.958 | Ver la nota de decisión de su fase. |
| `n_entrenamiento` | BIGINT | 0.0 % | 312 | Ver la nota de decisión de su fase. |
| `n_prueba` | BIGINT | 0.0 % | 156 | Ver la nota de decisión de su fase. |
| `f1_macro_origen_movil` | DOUBLE | 0.0 % | 0.774 | Ver la nota de decisión de su fase. |
| `exactitud_origen_movil` | DOUBLE | 0.0 % | 0.808 | Ver la nota de decisión de su fase. |
| `aciertos` | BIGINT | 0.0 % | 126 | Ver la nota de decisión de su fase. |
| `casos` | BIGINT | 0.0 % | 156 | Ver la nota de decisión de su fase. |
| `cambios_reales` | BIGINT | 0.0 % | 30 | Ver la nota de decisión de su fase. |
| `cambios_acertados` | BIGINT | 0.0 % | 0 | Ver la nota de decisión de su fase. |
| `falsas_alarmas` | BIGINT | 0.0 % | 0 | Ver la nota de decisión de su fase. |

## gold_radar_panel_mensual

Fase 4. Panel lugar × mes con todas las variables de presión. **825 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `lugar` | VARCHAR | 0.0 % | Bacalar | Lugar. |
| `es_de_los_5` | BOOLEAN | 0.0 % | False | Verdadero si es una de las 5 regiones de la campaña. |
| `periodo` | TIMESTAMP_NS | 0.0 % | 2022-01-01 00:00:00 | Primer día del mes. |
| `llegadas_tren` | DOUBLE | 75.9 % | 2306.0 | Ver la nota de decisión de su fase. |
| `cruceristas` | DOUBLE | 86.7 % | 206314.0 | Ver la nota de decisión de su fase. |
| `cruces_belice` | DOUBLE | 93.5 % | 2864.0 | Ver la nota de decisión de su fase. |
| `visitantes_inah` | DOUBLE | 46.7 % | 12258.0 | Ver la nota de decisión de su fase. |
| `ocupacion_pct` | DOUBLE | 50.1 % | 66.49917467715312 | Ocupación hotelera (%). |
| `ocupacion_siturq_pct` | DOUBLE | 62.2 % | 66.49917467715312 | Ver la nota de decisión de su fase. |
| `ocupacion_datatur_pct` | DOUBLE | 73.3 % | 66.76554855415984 | Ver la nota de decisión de su fase. |
| `cuartos_noche_ocupados` | DOUBLE | 62.2 % | 27395.0 | Ver la nota de decisión de su fase. |
| `cuartos_noche_disponibles` | DOUBLE | 62.2 % | 41196.0 | Ver la nota de decisión de su fase. |
| `cuartos` | DOUBLE | 20.0 % | 1370.0 | Ver la nota de decisión de su fase. |
| `hoteles` | DOUBLE | 20.0 % | 132.0 | Ver la nota de decisión de su fase. |
| `fuente_ocupacion` | VARCHAR | 0.0 % | SITUR-Q | Ver la nota de decisión de su fase. |
| `poblacion` | DOUBLE | 6.7 % | 12527.0 | Habitantes (Censo 2020). |

## gold_radar_prediccion

Fase 4. Estado esperado del mes siguiente por lugar (_est). **13 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `lugar` | VARCHAR | 0.0 % | Bacalar | Lugar. |
| `es_de_los_5` | BIGINT | 0.0 % | 0 | Verdadero si es una de las 5 regiones de la campaña. |
| `periodo` | TIMESTAMP_NS | 0.0 % | 2026-07-01 00:00:00 | Primer día del mes. |
| `estado_hoy` | VARCHAR | 0.0 % | concurrido | Ver la nota de decisión de su fase. |
| `ipt_comparable` | DOUBLE | 0.0 % | 0.3135385626030444 | Ver la nota de decisión de su fase. |
| `ipt_1` | DOUBLE | 0.0 % | 0.2698323378627603 | Ver la nota de decisión de su fase. |
| `ipt_2` | DOUBLE | 0.0 % | 0.28062301342412327 | Ver la nota de decisión de su fase. |
| `medidas` | VARCHAR | 0.0 % | llegadas_tren_x1000hab, visitantes_inah_… | Ver la nota de decisión de su fase. |
| `cambio` | DOUBLE | 0.0 % | 0.04370622474028413 | Ver la nota de decisión de su fase. |
| `mes_sin` | DOUBLE | 0.0 % | -0.4999999999999997 | Ver la nota de decisión de su fase. |
| `mes_cos` | DOUBLE | 0.0 % | -0.8660254037844388 | Ver la nota de decisión de su fase. |
| `estado_mes_siguiente_est` | VARCHAR | 0.0 % | concurrido | Ver la nota de decisión de su fase. |
| `mes_siguiente` | TIMESTAMP_NS | 0.0 % | 2026-08-01 00:00:00 | Ver la nota de decisión de su fase. |
| `modelo` | VARCHAR | 0.0 % | Regresión logística | Ver la nota de decisión de su fase. |
| `prob_concurrido` | DOUBLE | 0.0 % | 0.8012833823719945 | Ver la nota de decisión de su fase. |
| `prob_saturado` | DOUBLE | 0.0 % | 0.0009543228562065892 | Ver la nota de decisión de su fase. |
| `prob_tranquilo` | DOUBLE | 0.0 % | 0.19776229477179885 | Ver la nota de decisión de su fase. |

## gold_radar_sesgo

Fase 4. Aciertos del modelo en los 5 lugares contra el norte (sesgo). **2 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `grupo` | VARCHAR | 0.0 % | resto del estado | Ver la nota de decisión de su fase. |
| `casos` | BIGINT | 0.0 % | 108 | Ver la nota de decisión de su fase. |
| `exactitud_modelo` | DOUBLE | 0.0 % | 0.778 | Ver la nota de decisión de su fase. |
| `exactitud_persistencia` | DOUBLE | 0.0 % | 0.741 | Ver la nota de decisión de su fase. |
| `cambios_reales` | BIGINT | 0.0 % | 28 | Ver la nota de decisión de su fase. |
| `cambios_acertados` | BIGINT | 0.0 % | 8 | Ver la nota de decisión de su fase. |
| `falsas_alarmas` | BIGINT | 0.0 % | 4 | Ver la nota de decisión de su fase. |

## gold_reconciliacion_cruceros

Fase 2. Cruceristas: DataTur contra SITUR-Q, mes a mes, en Cozumel y Mahahual. **182 renglones.**

| Columna | Tipo | Vacíos | Ejemplo | Significado |
|---|---|---:|---|---|
| `puerto` | VARCHAR | 0.0 % | Cozumel | Puerto de cruceros. |
| `periodo` | DATE | 0.0 % | 2019-01-01 | Primer día del mes. |
| `pasajeros_datatur` | BIGINT | 0.0 % | 485834 | Pasajeros de crucero según DataTur. |
| `cruceristas_siturq` | DOUBLE | 0.0 % | 503256.0 | Cruceristas según SITUR-Q. |
| `diferencia` | DOUBLE | 0.0 % | 17422.0 | SITUR-Q − DataTur. |
| `diferencia_pct` | DOUBLE | 15.4 % | 3.59 | Diferencia como % de DataTur. |
