# Guía técnica: cómo se hizo Torre del Caribe, fórmula por fórmula

Autor: **Brandon Uriel García Sánchez** · UNRC · LCDN 5° semestre 2026-2 · versión del 2 de octubre de 2026.

---

## 0. Cómo leer esta guía

Esta guía explica **todo** lo que hace el proyecto: de dónde sale cada dato, qué hace cada archivo de código, qué fórmula
se usó, cómo se resolvió a mano con números reales y por qué se eligió ese método y no otro. Está escrita para que
puedas defender cada pieza frente a un profesor sin tener que abrir el código.

Cada método sigue siempre el mismo orden:

| Parte | Qué contesta |
|---|---|
| **Pregunta** | Qué duda del problema resuelve este método |
| **Datos** | De qué archivo oficial sale (y cuántos registros) |
| **Fórmula** | La ecuación, con cada símbolo explicado |
| **A mano** | Un ejemplo con números reales del proyecto, que coincide con lo que da el código |
| **Código** | Archivo y función donde está |
| **Por qué así** | Qué alternativa se descartó y por qué |
| **Si te preguntan** | La respuesta corta para el profesor |

Todas las cifras de esta guía se recalcularon el 2 de octubre de 2026 con los datos del proyecto, y las principales las
vigila una prueba automática (`tests/test_guias.py`): si una cifra cambia, la prueba falla.

Dos convenciones:
- **Medido** = sale directo de una fuente oficial. **Estimado** = sale de un modelo, y en las tablas lleva el sufijo
  `_est`.
- **Hueco** = un dato que no existe. Nunca se rellena con ceros ni con promedios: se declara.

---

## 1. El proyecto en una página

**La pregunta del Problema Prototípico:** ¿cómo diseñar una campaña basada en ciencia de datos que promueva un destino de
Quintana Roo, atraiga visitantes de forma responsable y reparta mejor el turismo, aprovechando la capacidad que sobra
y sin saturar?

**La respuesta del proyecto:** el norte del estado (Cancún, la Riviera Maya, Tulum) está lleno y con sargazo; el sur
tiene espacio. Los cinco lugares de la campaña tienen el **12.3 %** de la población del estado pero reciben el **1.4 %**
de los pasajeros de avión. La campaña "**El sur tiene espacio**" promueve el sur sin saturarlo.

El sistema tiene **tres módulos** que responden tres preguntas distintas, más la campaña:

| Módulo | Pregunta | Horizonte | Técnicas |
|---|---|---|---|
| **A1 Radar** | ¿Dónde hay presión y dónde hay espacio? | Hoy (meses y semanas) | Índice de presión, clustering, clasificador, cadena de Markov |
| **A3 Pronóstico** | ¿Cuándo conviene ir y cuánto dinero invertir? | 1 a 12 meses | Forma del año, 5 modelos de series de tiempo, intervalo conformal, Poisson, Monte Carlo, optimización |
| **A5 Torre en vivo** | ¿Qué hace la campaña esta semana? | Semana a semana | Streaming con Spark, Isolation Forest, motor de reglas |
| **Campaña** | ¿A quién, con qué mensaje, en qué canal? | Todo el plan | Minería de texto, buyer persona, KPI |

**Cómo se pasan la estafeta** (esto es la integración, criterio 8 de la rúbrica):
1. El **Pronóstico** dice qué meses van a estar llenos (temporada alta) y cuánta gente se espera.
2. El **presupuesto** (Investigación de Operaciones) usa eso para repartir el dinero solo en meses con espacio.
3. El **Radar** dice si un lugar ya está saturado hoy.
4. La **Torre en vivo** revisa cada semana el clima, las tormentas y las llegadas, y pausa el anuncio si algo sale mal.
5. La **campaña** pone el mensaje y el público, y la Torre mide sus indicadores.

**Las 12 fases (0 a 11)** se hicieron una por una; la guía de decisiones (documento 3) cuenta qué se decidió en cada una.

---

## 2. Antes de las fórmulas: las preguntas incómodas

### 2.1 ¿Por qué aparece Claude en el proyecto?

**Lo que pasó, tal cual:** el código, las notas y los documentos se construyeron trabajando con **Claude Code**, un
asistente de programación con inteligencia artificial (de la empresa Anthropic), en sesiones de trabajo contigo. Por eso:

| Dónde aparece | Qué es |
|---|---|
| Cada commit dice `Co-Authored-By: Claude` (todos los del historial) | Git registra que el asistente participó en ese cambio |
| `CLAUDE.md` en la raíz | Las **reglas que tú le diste** al asistente: no inventar datos, una fase a la vez, que tú decides, etc. |
| La carpeta `.claude/` | La configuración del asistente (permisos y ganchos) |
| `graphify-out/` | Un mapa del proyecto que el asistente consulta para no perder el contexto |
| La nota 07 menciona "Claude Design" | La herramienta con la que se rediseñó la página |

**Cómo se trabajó (y esto lo puedes demostrar con los archivos):**
- **Tú fijaste el problema y las reglas** (`OBJETIVO.md`, `CLAUDE.md`).
- **En cada punto donde había que elegir, el asistente te presentó 2 o 3 opciones con datos y tú elegiste.** Hay
  **más de 40 registros de decisión** en `OBJETIVO.md` (sección A.8) y **25 notas de decisión** en `docs/decisiones/`, cada una
  con tus palabras textuales, las opciones descartadas y la evidencia.
- El asistente programó cada pieza; las piezas se corrieron, se revisaron con datos reales y quedaron con pruebas
  automáticas (276).

**Qué te recomiendo (con honestidad):** **decláralo tú, antes de que te pregunten.** Revisa la política de tu profesor y
de la UNRC sobre el uso de inteligencia artificial y di algo como: *"Usé un asistente de programación con IA como
herramienta. Las decisiones del proyecto son mías y están documentadas con mis palabras; el código lo revisé y lo
entiendo, y cada cifra se puede rastrear a su fuente oficial."* Lo que vuelve defendible el proyecto no es esconder la
herramienta, sino **poder explicar cada pieza**: para eso es esta guía.

### 2.2 ¿Por qué hay tantos archivos `.py`?

Porque el proyecto sigue una regla: **una pieza = un archivo**, y cada archivo empieza con un encabezado que dice qué
hace, por qué así, de qué datos sale y a qué decisión de la campaña alimenta. Así cada pieza se puede probar y explicar
sola. Son **55 archivos** en 7 carpetas (paquete `backend/torre/`):

| Carpeta | Archivos | Para qué sirve | Fases |
|---|---:|---|---|
| `base/` | 23 | Descargar las fuentes (Bronze), limpiarlas con Spark (Silver), almacén DuckDB y diccionario | 0, 1, 2 |
| `radar/` | 7 | Planteamiento, criterios de las regiones, índice de presión, clasificador, Markov, clustering | 3, 4 |
| `pronostico/` | 7 | Series de tiempo, forma del año, 5 modelos, rango del 90 %, escenarios, calendario | 5 |
| `campana/` | 9 | Presupuesto (IO), minería de texto, marca y mensajes, lugares (NLP), fotos, idiomas | 6, 8 |
| `envivo/` | 3 | Señales semanales, motor de reglas y la reproducción con Spark Streaming | 7 |
| `api/` | 2 | Los datos de la página (`pagina.js`) y el servidor FastAPI | 9 |
| `documento/` | 4 | Gráficas, PDF, auditoría de la página y carpeta de entrega | 10, 11 |

Además: `tests/` (25 archivos, 276 pruebas), `notebooks/` (6 notebooks narrados, cada uno con su constructor), `frontend/` (la
página) y `docs/` (decisiones, ecuaciones, guías, diccionario).

**Los archivos de `base/` en detalle** (los demás se explican en su sección):

| Archivo | Qué hace |
|---|---|
| `entorno.py` | Prepara Java 17 y Hadoop para que Spark funcione en Windows y crea la sesión de Spark |
| `manifiesto.py` | Registra cada archivo descargado con su huella SHA-256, tamaño, URL y número de registros |
| `ingesta_siturq.py`, `ingesta_datatur.py`, `ingesta_abiertas.py` | Descargan las fuentes oficiales a `datos/bronze/` |
| `ingesta_benchmarks.py`, `evidencia_sargazo.py` | Abren páginas con un navegador automatizado y guardan tablas y capturas como evidencia |
| `ingesta_fotos.py`, `ubicaciones.py` | Fotos con licencia libre y comprobación de que cada lugar está en Quintana Roo |
| `silver_*.py` (12 archivos) | Una limpieza por fuente: SITUR-Q, DataTur, DENUE, INAH, Censo, clima, huracanes, FRED, nacionalidad, AFAC, cruceros, reseñas |
| `almacen.py`, `diccionario.py` | El almacén DuckDB con el modelo estrella y el diccionario de 56 tablas |

**Si te preguntan "¿por qué no un solo notebook?":** porque un notebook gigante no se puede probar por partes ni
reutilizar. Los 6 notebooks (`notebooks/01`–`07`; no hay 04) **narran** el proceso y llaman a las funciones del paquete; las
funciones viven en los `.py` para que las pruebas las vigilen.

### 2.3 ¿Dónde están las UCA (las materias)?

| UCA (criterio de la rúbrica, peso) | Qué se hizo | Código | Notebook | Sección de esta guía |
|---|---|---|---|---|
| **Planteamiento** (8 %) | Variables, actores, concentración (HHI), criterios de las regiones | `radar/planteamiento.py`, `criterios.py` | 01 | §4.1, §4.2 |
| **Grandes volúmenes** (12 %) | Bronze→Silver→Gold con PySpark, 8.1 millones de registros, DuckDB, Spark Streaming | `base/`, `envivo/torre.py` | 06 | §3 |
| **Minería** (12 %) | Índice de presión, clustering Ward, forma del año, Isolation Forest, minería de texto, NLP | `radar/`, `pronostico/forma.py`, `envivo/senales.py`, `campana/texto.py` | 02, 03, 06, 07 | §4 |
| **Aprendizaje de máquina** (12 %) | Clasificador del estado (3 modelos) y pronóstico (5 modelos) con validación en origen móvil | `radar/prediccion.py`, `pronostico/modelos.py` | 02, 03 | §5 |
| **Estocásticos** (10 %) | Markov semanal, Poisson de tormentas, Monte Carlo de 10,000 futuros, sensibilidad | `radar/markov.py`, `pronostico/escenarios.py` | 02, 03 | §6 |
| **Investigación de Operaciones** (12 %) | Programación estocástica de dos etapas, precios sombra, Pareto | `campana/presupuesto.py`, `envivo/motor.py` | 05, 06 | §7 |
| **Mercadotecnia digital** (8 %) | Personas, marca, mensajes con respaldo, medios, KPI | `campana/marca.py`, `texto.py` | 07 | §8 |
| **Integración** (10 %) | La estafeta Pronóstico → presupuesto → Radar → Torre → campaña | todo | 05, 06 | §1, §9 |

### 2.4 ¿De dónde salen los datos?

**Todos de fuentes oficiales o abiertas**, descargadas con código (nunca a mano) a `datos/bronze/`, sin modificarlas. Cada
archivo queda en `datos/bronze/MANIFIESTO.csv` con su huella SHA-256. En total: **353 archivos y 8,134,802 registros**
(824 MB).

| Clave | Fuente | Qué trae | Registros | Para qué se usa |
|---|---|---|---:|---|
| D1 | **SITUR-Q** (sistema de información turística de Quintana Roo, API pública) | Ocupación, cuartos, Tren Maya, cruceristas, cruces de Belice, aviones | 6,607 | Radar, pronóstico de Belice, conciliación |
| D2 | **DataTur** (SECTUR), ocupación hotelera | 135 archivos semanales y 31 mensuales; 7 centros de Q. Roo × 239 semanas | 34,164 | Radar del norte, Markov, Torre |
| D3 | DataTur **BD_Nacionalidad** (Unidad de Política Migratoria) | Extranjeros que llegan en avión, por aeropuerto, país y sexo | 521,364 | Buyer persona |
| D4 | DataTur **BdINAH**, AFAC, cruceros, Compendio 2024 | Visitantes a zonas arqueológicas por mes; vuelos; cruceros; estrellas de hoteles | 390,228 | Pronóstico del sur, criterios, conciliación |
| D5 | **Rest-Mex 2025** (licencia CC-BY-4.0) | 208,051 reseñas de turistas con calificación 1–5 | 208,051 | Minería de texto |
| D6 | **DENUE** (INEGI), 32 estados | 6,138,075 negocios con giro y coordenadas | 6,138,075 | Oferta turística, NLP de lugares, volumen para Spark |
| D7 | **Censo 2020, ITER** (INEGI) | Población y viviendas por localidad | 2,243 | Presión por habitante, criterios |
| D8 | **Open-Meteo** (reanálisis ERA5) | Clima diario desde 1950 y horario desde 2019, 8 puntos | 767,016 | Regresión con clima, Isolation Forest |
| D9 | **HURDAT2** (NOAA) | Todas las tormentas del Atlántico, 1851–2025 | 57,512 | Poisson de tormentas |
| D10 | **FRED** (Reserva Federal de St. Louis) | Pesos por dólar diario; inflación de EE. UU. | 9,531 | Sensibilidad, presupuesto en pesos |
| D11 | **ENDUTIH 2025** (INEGI) | Uso de internet y apps (PDF oficial) | — | Medios de la campaña |
| D12 | GeoJSON de Q. Roo | Polígonos de municipios | 11 | Comprobar ubicaciones y fotos |
| D13 | WordStream y LocaliQ | Costo por clic y conversión de anuncios de viajes | 386 filas | Presupuesto (supuesto etiquetado) |
| D15 | Wikimedia Commons | Fotos con licencia libre y coordenada comprobada | — | Página |

**Lo que no existe y se declara como hueco:** la ocupación hotelera del sur en 2025–2026 (SITUR-Q publica ceros); el
estado de origen, la edad y el ingreso del visitante nacional; la conversión de Facebook para turismo; las tormentas de
2026; reseñas de los cinco lugares.

### 2.5 "¿Cómo inferiste?" — qué es medido y qué es estimado

**Inferir** aquí significa sacar una conclusión o un número que la fuente no dice directamente, usando un modelo que se
probó contra datos que no vio. El proyecto hace cuatro tipos de inferencia, y las cuatro se validaron:

| Inferencia | Con qué | Cómo se validó |
|---|---|---|
| Estado del mes siguiente (tranquilo/concurrido/saturado) | Regresión logística | 156 predicciones de meses que el modelo nunca vio: 130 aciertos contra 126 de "igual que este mes" |
| Visitantes de los próximos 12 meses con su rango | Regresión con clima y Holt-Winters | Origen móvil: miles de pronósticos del pasado comparados con lo que pasó; el rango del 90 % acertó 80–94 de cada 100 veces |
| Riesgo de tormenta y escenarios | Poisson y Monte Carlo | 60 años de tormentas reales; errores reales del pronóstico |
| Si una semana tiene clima raro | Isolation Forest | Marcó las 3 semanas de tormenta sin saber que hubo tormenta |

Todo lo estimado lleva `_est` y su error. Nada estimado se presenta como medido.

---

## 3. UCA Grandes volúmenes de datos (Big Data)

### 3.1 La arquitectura: Bronze → Silver → Gold

**Pregunta:** ¿cómo se guardan y transforman millones de registros de 14 fuentes distintas sin perder el rastro de cada
cifra?

**Respuesta:** la arquitectura "medallón", con tres capas:

| Capa | Carpeta | Qué contiene | Regla |
|---|---|---|---|
| **Bronze** | `datos/bronze/` | Los archivos tal como los publica la fuente (zip, Excel, JSON, CSV) | Nunca se modifican; cada uno con su huella SHA-256 |
| **Silver** | `datos/silver/` | Una tabla limpia por fuente, en formato Parquet, con nombres en español y banderas de calidad | La hace Spark; los huecos quedan como hueco |
| **Gold** | `datos/gold/` | Salidas de los modelos y el modelo estrella | Lo que usan la página y los documentos |

**Por qué así:** si alguien duda de una cifra, se puede volver al archivo crudo, que no se tocó, y repetir el camino.
**Alternativa descartada:** limpiar mientras se descarga; Bronze dejaría de ser idéntico a la fuente.

**La huella SHA-256** es como una huella digital del archivo: una cadena de 64 caracteres que cambia por completo si el
archivo cambia en un solo byte. La prueba `tests/test_ingesta.py` vuelve a calcular las 353 huellas y falla si alguna no
coincide.

### 3.2 Qué es Spark y qué hace exactamente aquí

**Spark** es un motor que procesa tablas grandes dividiéndolas en pedazos (*particiones*) y trabajando cada pedazo en
paralelo. En este proyecto corre en **modo local con todos los núcleos de la computadora** (`local[*]`, 12 núcleos, 4 GB
de memoria): es el mismo programa que correría en un clúster de muchas computadoras, solo que aquí el "clúster" es tu
laptop.

**Tres ideas que debes poder explicar:**
1. **DataFrame:** una tabla repartida en particiones. Se escribe como en pandas (`select`, `withColumn`, `groupBy`), pero
   Spark decide cómo repartir el trabajo.
2. **Evaluación perezosa:** las transformaciones (`withColumn`, `filter`) no se ejecutan al escribirlas; Spark arma un
   plan y lo ejecuta todo junto cuando se pide un resultado (`count`, `write`). Así optimiza el camino completo.
3. **Parquet particionado:** Spark escribe cada tabla Silver en formato Parquet (columnar y comprimido), partido en
   carpetas por una columna (por ejemplo, `cve_ent=23/` para Quintana Roo). Leer solo un estado no obliga a leer los 32.

**El trabajo más grande: el DENUE** (`base/silver_denue.py`), 6,138,075 negocios del país. Este es el código real,
simplificado:

```python
crudo = spark.read.option("header", True).option("encoding", "ISO-8859-1").csv("denue/*.csv")
silver = (crudo.select(*COLUMNAS)
          .dropDuplicates(["id"])                              # un negocio, una fila
          .withColumn("scian_3", F.substring("codigo_act", 1, 3))
          .withColumn("categoria_turistica", categoria)        # 721 alojamiento, 722 alimentos...
          .withColumn("coordenadas_flag", ~(lat.between(14, 33) & lon.between(-119, -86)))
          .withColumn("es_qroo", F.col("cve_ent") == "23"))
silver.write.mode("overwrite").partitionBy("cve_ent").parquet("datos/silver/denue")
```

Línea por línea:
- Lee los 33 CSV (el Estado de México viene en 2 partes) como **una sola** tabla.
- Quita duplicados por la clave del negocio (resultado: 0 duplicados).
- Saca el subsector SCIAN y la categoría turística.
- Marca con una **bandera** (`_flag`) las coordenadas fuera de México en vez de borrarlas.
- Escribe Parquet partido por estado.
- **Privacidad:** se descartan razón social, teléfono y correo; ningún modelo los necesita.

**Dónde se usa Spark:** las 12 limpiezas `silver_*.py` y la Torre en vivo (`envivo/senales.py` con una ventana deslizante
y `envivo/torre.py` con Structured Streaming). **Dónde no:** Spark no lee Excel, así que pandas abre los Excel de DataTur
e INAH y Spark hace la unión, la deduplicación y la escritura. Los modelos (scikit-learn, statsmodels, PuLP) trabajan
sobre tablas Gold que ya caben en memoria.

**Si te preguntan "¿de verdad se necesitaba Spark?":** con honestidad: 8.1 millones de registros caben en una laptop, y
pandas podría con casi todo. Spark se usó porque (1) la rúbrica pide una arquitectura de grandes volúmenes, (2) el DENUE
nacional y el clima horario ya son pesados, y (3) el mismo código escala sin cambios a un clúster si mañana entran más
estados o años. El valor está en la arquitectura y el rastreo, no en el tamaño.

**Problemas de Windows que hubo que resolver** (están en `base/entorno.py`): Spark 3.5.6 necesita Java 17 (la máquina
tenía Java 8), los binarios `winutils.exe` y `hadoop.dll`, y la ruta corta de Windows porque la carpeta del proyecto
tiene espacios ("PP 5to semestre").

### 3.3 Reglas de limpieza: cero no es lo mismo que hueco

La regla más importante de la limpieza: **un cero que es físicamente imposible es un hueco**. Ejemplos reales:

| Caso | Regla | Por qué |
|---|---|---|
| Ocupación hotelera con 0 cuartos disponibles | Hueco | Es imposible ocupar cuartos que no existen |
| Los 4 aeropuertos reportan 0 pasajeros todo 2025 | Hueco | Cancún no pudo recibir cero pasajeros: la fuente dejó de publicar |
| Cruceristas en 0 en 2020 | Se conserva | Es real: los puertos cerraron por la pandemia |
| Zona arqueológica con 0 visitantes | Se conserva y se marca `sin_visitantes_flag` | Suele ser un cierre por obras |
| Ocupación de SITUR-Q (3 filas por mes) | Se recalcula ocupados ÷ disponibles | Nunca se suman ni se promedian porcentajes |

**Ocupación correcta (sumar antes de dividir):**

\[O=\frac{\sum \text{cuartos-noche ocupados}}{\sum \text{cuartos-noche disponibles}}\times100\]

**A mano, Chetumal 2024:** \(O=\dfrac{458{,}696}{791{,}016}\times100=57.99\approx58.0\,\%\). De cada 10 cuartos, 4 se
quedaron vacíos. Si se promediaran los 12 porcentajes mensuales, los meses con pocos cuartos pesarían igual que los
grandes y el resultado saldría distinto.

### 3.4 Cuando dos fuentes dicen cosas distintas (conciliación)

**Pregunta:** el incidente de Big Data pregunta qué hacer con "fuentes que no coinciden". El proyecto tiene dos casos
medidos:

\[\Delta\%=\left(\frac{S}{D}-1\right)\times100,\qquad S=\text{SITUR-Q},\ D=\text{DataTur}\]

**A mano, cruceristas de Cozumel en 2025:** \(\left(\dfrac{4{,}915{,}242}{4{,}724{,}255}-1\right)\times100=+4.04\,\%\).
En Mahahual: \(\left(\dfrac{2{,}641{,}695}{2{,}379{,}422}-1\right)\times100=+11.02\,\%\); SITUR-Q cuenta siempre más, entre
11 % y 35 % según el año.

**Ocupación:** DataTur marca menos que SITUR-Q para el mismo lugar (Cancún −1.6 puntos, Cozumel −14.5, Isla Mujeres
−19.3), aunque las dos se mueven juntas (correlación de 0.68 a 0.97).

**La regla del proyecto:** cada lugar usa **una sola fuente en toda su historia**, la diferencia se **declara** y no se
"ajusta". La diferencia va en sentido conservador: el norte se ve menos lleno de lo que diría SITUR-Q, así que la
conclusión "el sur tiene espacio" se sostiene igual.

### 3.5 El almacén DuckDB y el modelo estrella

**DuckDB** es una base de datos que vive en un solo archivo (`datos/gold/torre.duckdb`) y lee los Parquet de Silver y
Gold **sin copiarlos**. Responde una consulta en milisegundos sin levantar Spark. Tiene una vista por cada tabla (14 de
Silver, 39 de Gold) y un **modelo estrella**:

| Tabla | Tipo | Contenido |
|---|---|---|
| `dim_lugar` | Dimensión | 15 lugares con su papel (5 promovidos, 3 de referencia, 7 de comparación) |
| `dim_tiempo` | Dimensión | Un renglón por mes, 2012–2027 |
| `hechos_mes` | Hechos | 3,287 renglones: lugar × mes × variable × fuente. **Un hueco no tiene renglón** |

Ejemplo de consulta (la página la puede hacer en vivo con el servidor):

```sql
SELECT anio, SUM(valor) FROM hechos_mes JOIN dim_tiempo USING (periodo)
WHERE lugar = 'Chetumal' AND variable = 'llegadas_extranjeros_avion' GROUP BY anio
```

Resultado para 2025: **250** extranjeros llegaron en avión a Chetumal (contra 9,408,423 a Cancún).

**El diccionario de datos** (`docs/datos/DICCIONARIO.md`) se **genera solo** desde el almacén: 56 tablas, cada columna con
su tipo, % de vacíos, un ejemplo real y su significado. No puede quedar desactualizado.

### 3.6 Streaming: la Torre en vivo con Spark Structured Streaming

**Pregunta:** ¿cómo se ajusta la campaña **mientras** corre, semana por semana?

**Cómo funciona** (`envivo/torre.py`):
1. Cada semana real (239, de enero de 2022 a julio de 2026) se escribe como un archivo JSON en una carpeta.
2. Spark **escucha** esa carpeta con `readStream` y la opción `maxFilesPerTrigger = 1`: procesa **un archivo (una semana)
   por lote**, en orden de llegada.
3. En cada lote, una función (`foreachBatch`) le pasa la semana al motor de reglas, que decide qué anuncio se enciende
   o se pausa.
4. Al final se comprueba que llegaron **239 lotes, en orden**.

**Por qué así:** es la misma arquitectura que recibiría datos reales cada semana (una carpeta a la que llega un archivo
nuevo). Cambiar la fuente por una real no cambia el motor de reglas. En la página se muestra como "reproducción de datos
históricos reales", porque GitHub Pages no puede transmitir en vivo.

**Ventana deslizante** (`envivo/senales.py`): el promedio de ocupación de las últimas 4 semanas lo calcula Spark con una
ventana sobre cada centro:

\[\bar o_w=\frac14\sum_{k=0}^{3}o_{w-k}\]

---

## 4. UCA Minería de datos

### 4.1 Concentración del turismo (planteamiento)

**Pregunta:** ¿qué tan concentrado está el turismo en el norte?

**Fórmulas.** Para una dimensión repartida entre \(N\) unidades (aeropuertos, municipios…):
- Cuota: \(s_i=\dfrac{x_i}{\sum_j x_j}\).
- Índice de Herfindahl-Hirschman: \(HHI=\sum_i s_i^2\) (vale \(1/N\) si todos pesan igual y 1 si una unidad lo tiene todo).
- Normalizado: \(HHI^*=\dfrac{HHI-1/N}{1-1/N}\), entre 0 (reparto parejo) y 1 (todo en una).
- Razón contra la población: \(\rho=\dfrac{s_5^{\text{dimensión}}}{s_5^{\text{población}}}\).

**A mano, llegadas en avión 2024:**

| Aeropuerto | Pasajeros | Cuota \(s_i\) | \(s_i^2\) |
|---|---:|---:|---:|
| Cancún | 14,769,302 | 0.92544 | 0.856433 |
| Tulum | 620,384 | 0.03887 | 0.001511 |
| Cozumel | 352,067 | 0.02206 | 0.000487 |
| Chetumal | 217,524 | 0.01363 | 0.000186 |
| **Total** | **15,959,277** | **1** | **0.858617** |

\(HHI^*=\dfrac{0.8586-0.25}{0.75}=0.811\): casi todo entra por una puerta. Los cinco lugares (solo Chetumal tiene
aeropuerto) tienen el 1.4 % y el 12.3 % de la población: \(\rho=1.4/12.3=0.11\).

| Dimensión | Cuota de los 5 lugares | \(\rho\) |
|---|---:|---:|
| Llegadas en avión (2024) | 1.4 % | 0.11 |
| Cuartos de hotel (jul-2026) | 1.7 % | 0.14 |
| Visitantes INAH (2025) | 4.1 % | 0.33 |
| Negocios turísticos (DENUE) | 14.4 % | 1.17 |
| Población (2020) | 12.3 % | 1.00 |

**Lectura:** los negocios siguen a la población; los visitantes, no. **Código:** `radar/planteamiento.py`.

### 4.2 Por qué estas 5 regiones (tabla de criterios)

**Pregunta:** ¿qué lugares promover? Cinco criterios: sargazo, cierres, saturación, fragilidad y datos.

**Fórmulas clave:**
- Visitantes por residente: \(R_d=\dfrac{V_{d,2025}}{P_d}\), con la población **por localidad** (no por municipio).
- Meses seguidos abierta: se cuenta hacia atrás desde el último mes con dato; **pasa si ≥ 12** y sin cierres en 2026.
- Variación de un sitio: \(\Delta\%=\left(\dfrac{V_{2026}^{ene-jul}}{V_{2025}^{ene-jul}}-1\right)\times100\).

**A mano:**
- Tulum, enero–julio: \(\left(\dfrac{476{,}247}{692{,}946}-1\right)\times100=-31.3\,\%\).
- Ruta del sur por residente: \(R=\dfrac{21{,}850+6{,}592+38{,}186}{3{,}699+1{,}436+963}=\dfrac{66{,}628}{6{,}098}=10.93\);
  Tulum: \(\dfrac{1{,}031{,}443}{33{,}374}=30.91\).
- Tulum recibió \(1{,}031{,}443/66{,}628=15.5\) veces más visitantes que la ruta del sur en 2025.
- Dzibanché: último cero en enero de 2025; de febrero de 2025 a julio de 2026 son 18 meses ≥ 12 → **pasa**.

**Por qué por localidad:** 4 de los 5 lugares están en el municipio Othón P. Blanco; con la población municipal tendrían
el mismo denominador y no se podrían comparar. **Código:** `radar/criterios.py`.

### 4.3 El índice de presión turística (IPT)

**Pregunta:** ¿qué lugar está más presionado, si cada uno tiene medidas distintas?

**Datos:** panel de 15 lugares × 55 meses (enero de 2022 a julio de 2026) con: personas que bajan del Tren Maya, cruceristas
y visitantes INAH por cada mil habitantes, llegadas por cuarto de hotel y ocupación.

**Fórmulas** (lugar \(d\), mes \(t\), componente \(k\)):
1. Llevar cada medida a la misma escala, de 0 a 1, con mínimo y máximo **comunes a todo el estado** (min–max):
   \[z_{k,d,t}=\frac{x_{k,d,t}-\min_k}{\max_k-\min_k}\]
2. Promediar con **pesos iguales** las medidas que el lugar tiene:
   \[IPT_{d,t}=\frac{1}{|A_{d,t}|}\sum_{k\in A_{d,t}}z_{k,d,t}\]
3. Clasificar con los **percentiles** 50 y 90 de todos los lugares y meses: tranquilo si \(IPT<u_{50}\); concurrido si está
   entre \(u_{50}\) y \(u_{90}\); saturado si \(IPT>u_{90}\).

**A mano, Cancún, julio de 2026** (888,797 habitantes):

| Componente | Dato | \(x\) | mín | máx | \(z\) |
|---|---:|---:|---:|---:|---:|
| Tren Maya | 22,316 personas | 25.1081 por mil | 0 | 505.2287 | 0.0497 |
| INAH (El Rey) | 854 | 0.9608 por mil | 0 | 6,451.8787 | 0.0001 |
| Llegadas por cuarto | 22,316 | 0.4709 | 0 | 432.0230 | 0.0011 |
| Ocupación (DataTur) | — | 68.78 % | 17.97 | 88.40 | 0.7214 |

\[IPT=\frac{0.0497+0.0001+0.0011+0.7214}{4}=0.1931\]

**Ojo, hay dos índices y es importante entender por qué:**
- El **índice base** (arriba) usa todas las medidas que existan cada mes. Sus cortes son \(u_{50}=0.258\) y
  \(u_{90}=0.766\): Cancún, con 0.193, sale **tranquilo**.
- En 2025 SITUR-Q dejó de publicar ocupación del sur, y Chetumal "bajó" de 0.54 a 0.05 sin que llegara menos gente: fue
  un cambio en los datos, no en la realidad. Por eso el Radar **publica el índice comparable**: cada lugar usa solo las
  medidas que tiene hoy, y solo en los meses en que las tiene todas. Sus cortes son \(u_{50}=0.186\) y \(u_{90}=0.756\):
  Cancún, con el mismo 0.193, sale **concurrido**.

**Julio de 2026 (índice comparable, lo que ve la página):** concurridos Mahahual (0.731), Isla Mujeres (0.510), Bacalar
(0.314), Holbox (0.228), Cancún (0.193) y Cozumel (0.191); los cinco lugares de la campaña, tranquilos (Ruta 0.129,
Chetumal 0.025, Oxtankah 0.020, Maya Ka'an 0.009); Laguna Milagros, "sin dato oficial".

**Sensibilidad:** cada peso se movió a 0.5 y a 1.5; cambia de estado entre el 0.6 % y el 6.0 % de los lugar-mes.

**Por qué así (decisiones tuyas):** pesos iguales (fácil de defender; no premia al norte por tener más series),
percentiles comunes (un lugar que nunca se llena no sale "saturado" por compararse contra sí mismo) y la prueba de
validez que obligó a corregir el índice cuando Cancún salía "tranquilo" por falta de datos. **Código:**
`radar/indice.py` y `radar/prediccion.py` (`indice_comparable`).

### 4.4 Agrupamiento de los centros turísticos del país (clustering Ward)

**Pregunta:** ¿a qué se parece el norte de Quintana Roo dentro del país?

**Datos:** 55 centros de DataTur con sus 55 meses completos; cada uno es un vector de 12 ocupaciones (una por mes).

**Fórmulas:**
- Distancia euclidiana: \(d(c,c')=\sqrt{\sum_m (p_{c,m}-p_{c',m})^2}\).
- Ward une en cada paso los dos grupos que menos aumentan la varianza interna:
  \(\Delta(A,B)=\dfrac{|A||B|}{|A|+|B|}\lVert\bar p_A-\bar p_B\rVert^2\).
- Silueta: \(s(i)=\dfrac{b(i)-a(i)}{\max\{a(i),b(i)\}}\), con \(a\) la distancia media a su grupo y \(b\) al grupo más cercano.
  Se elige el número de grupos con la mayor silueta promedio.

**A mano (silueta de Cancún):** \(a=43.84\), \(b=116.21\), \(s=\dfrac{116.21-43.84}{116.21}=0.623\) (bien asignado).

**Resultado:** \(k=2\) (silueta 0.450): grupo 1, playas muy ocupadas (23 centros, 64.5 %: Cancún, Riviera Maya,
Playacar, Akumal, Playa del Carmen, Los Cabos); grupo 2, el resto del país (32 centros, 41.1 %). **Código:**
`radar/clustering.py`.

### 4.5 La forma del año (estacionalidad)

**Pregunta:** ¿qué meses se llenan y cuáles se vacían en cada lugar?

**Fórmulas** (descomposición clásica multiplicativa, solo con años completos):
1. Razón de cada mes contra el promedio de su año: \(r_{a,m}=\dfrac{y_{a,m}}{\bar y_a}\), con \(\bar y_a=\frac1{12}\sum_m y_{a,m}\).
2. Índice del mes: promedio de las razones de ese mes en todos los años, reescalado para que los 12 promedien 1.
3. Fuerza de la temporada: \(F_S=\max\!\left(0,\ 1-\dfrac{\operatorname{Var}(e)}{\operatorname{Var}(s+e)}\right)\), con
   \(s\) el índice y \(e\) lo que queda, en logaritmos (0 = no hay temporada; 1 = el mes lo explica todo).

**A mano (Ruta del sur, enero):** en 2019, Kohunlich + Dzibanché = 64,139 visitantes, \(\bar y=5{,}344.92\); en enero
hubo 7,935: \(r=7{,}935/5{,}344.92=1.4846\). Las seis razones de enero (2016–2019, 2022, 2023) suman 9.6359:
\(S_1=9.6359/6=1.606\). **En enero llega 61 % más gente que en un mes promedio**; en septiembre, la mitad (0.496).

| Serie | \(F_S\) | Mes más alto | Mes más bajo |
|---|---:|---|---|
| Ruta arqueológica del sur | 0.793 | enero (1.606) | septiembre (0.496) |
| Bahía Calderitas–Oxtankah | 0.684 | diciembre (1.402) | septiembre (0.647) |
| Chetumal (cruces desde Belice) | 0.655 | diciembre (1.172) | febrero (0.865) |
| Cancún (referencia) | 0.714 | marzo (1.084) | septiembre (0.867) |

**Por qué así y no STL:** STL (el método del plan) exige una serie continua, y estas tienen huecos (pandemia, cierres por
obras). STL se usó como **segunda opinión** en el tramo continuo más largo y coincide entre 0.85 y 0.97. **Por qué
multiplicativa:** la temporada escala con el nivel (Kohunlich reabrió a la mitad de su nivel de 2019; "+30 %" sigue
valiendo, "+2,000 visitantes" no). **Código:** `pronostico/forma.py`.

### 4.6 Clima raro con Isolation Forest (detección de anomalías)

**Pregunta:** ¿esta semana tuvo un clima tan raro que conviene pausar el anuncio?

**Idea:** un bosque de 300 árboles corta los datos al azar. Una semana **rara** queda sola con muy pocos cortes; una
semana normal necesita muchos.

\[s(x)=2^{-E[h(x)]/c(n)},\qquad c(n)=2H(n-1)-\frac{2(n-1)}{n},\qquad H(k)\approx\ln k+0.5772\]

\(h(x)\) = cortes para aislar \(x\); \(s\) cerca de 1 = muy raro. **Variables:** lluvia de la semana, lluvia del peor día,
viento máximo, temperatura máxima y la época del año (seno y coseno de la semana, para que un aguacero de septiembre no
salga raro solo por ser septiembre).

**A mano (Chetumal, semana del 14 de octubre de 2024, tormenta Nadine):** llovieron 148.7 mm (65.4 mm el peor día). Con
\(n=256\): \(c(256)=2(\ln255+0.5772)-\frac{2\cdot255}{256}=12.237-1.992=10.245\). El bosque da \(s=0.712\), mayor que el
corte \(0.543\): **rara**. Cortes para aislarla: \(E[h]=-10.245\times\log_2 0.712=-10.245\times(-0.489)=5.0\), contra unos 10 de una semana normal.

**Decisión clave (tuya):** el corte automático del método marcaba **47 %** de las semanas de Chetumal (no distinguía con
tan pocas semanas, y desde 2022 llueve más). Elegiste "más raro que el 95 % de las semanas que el bosque ya conoce",
aprendiendo de todos los años anteriores: 21 semanas raras en Chetumal y 17 en Kohunlich. **Validación:** marcó las 3
semanas de tormenta (Lisa, Nadine, Sara) **sin saber** que hubo tormenta. **Código:** `envivo/senales.py`.

### 4.7 Minería de texto de las reseñas

**Pregunta:** ¿qué molesta y qué enamora al turista, para escribir los mensajes?

**Datos:** 85,987 reseñas de Quintana Roo (Rest-Mex 2025): Tulum, Isla Mujeres y Bacalar. **Ojo:** ninguna es de los
cinco lugares; sirven para saber qué molesta en los destinos llenos.

**1. Temas con un léxico a la vista** (`campana/texto.py`, `ASPECTOS`): cada tema es una lista de raíces de palabras
(ruido, sucio, caro, gente, tranquil…). **Riesgo relativo** de que una reseña sea mala (1–2 estrellas) cuando toca el tema:

\[RR_a=\frac{P(\text{mala}\mid a)}{P(\text{mala})}\]

**A mano:** \(P(\text{mala})=3{,}597/85{,}987=0.04183\). Reseñas con ruido: 235 malas de 2,038, \(P=0.11531\):
\(RR=0.11531/0.04183=2.76\).

| Tema | \(RR\) | Lectura |
|---|---:|---|
| Ruido | 2.76 | Aleja |
| Suciedad | 1.89 | Aleja |
| Precio | 1.66 | Aleja |
| Multitudes | 1.52 | Aleja |
| Calma | 0.41 | Protege |
| Cultura | 0.48 | Protege |

**2. Reglas de asociación (Apriori):** qué combinaciones de temas llevan a una reseña mala.

\[\text{soporte}=\frac{\#\{A\cup B\}}{N},\qquad \text{confianza}=\frac{\text{sop}(A\cup B)}{\text{sop}(A)},\qquad \text{lift}=\frac{\text{confianza}}{\text{sop}(B)}\]

**A mano (ruido + servicio ⇒ mala):** 1,204 reseñas tocan ambos; 142 son malas. Soporte \(=142/85{,}987=0.00165\);
confianza \(=142/1{,}204=0.1179\); lift \(=0.1179/0.04183=2.82\): esa combinación hace 2.8 veces más probable una reseña
mala.

**3. El lenguaje real (log-odds con prior de Dirichlet):** compara qué palabras aparecen más en las reseñas de 5
estrellas que en las malas, corrigiendo las palabras raras. Las de 5 estrellas: *excelente, increíble, hermoso, deliciosa,
amable, ruinas, ambiente*. Las malas: *peor, horrible, dinero, caro, sucia, grosero*.

**Por qué léxico y no un modelo de temas (LDA):** cada tema se define y se defiende palabra por palabra; un tema de LDA
hay que adivinarlo. **Conclusión:** lo que hunde una reseña sobra en los destinos llenos; lo que la protege (calma,
cultura) es lo que el sur ofrece.

### 4.8 NLP de lugares (qué hacer, dónde comer y dormir)

**Pregunta:** de los negocios del DENUE, ¿cuáles recomendar de día, tarde y noche?

**Método:** clasificador por léxico sobre el **nombre** del negocio y, si el nombre no dice nada, su giro oficial (SCIAN).
Reglas aprendidas de errores reales: la raíz cuenta solo al inicio de una palabra ("MICHELADAS" contiene "HELAD"); el
nombre gana al giro ("HOTEL COSTA AZUL" con giro de casa de huéspedes). **Precisión medida:** 39 de 40 en una muestra
nueva revisada a mano. **No se hizo scraping** de Google Maps (lo prohíben sus términos): cada tarjeta es un enlace
público de Google Maps. **Código:** `campana/lugares.py`.

---

## 5. UCA Aprendizaje de máquina

### 5.1 Clasificador: ¿qué estado tendrá cada lugar el mes siguiente?

**Datos:** el índice comparable de cada lugar y mes. **Rasgos** (lo que el modelo ve): el índice de este mes y de los dos
anteriores, su cambio, el mes del año como círculo \(\left(\sin\frac{2\pi m}{12},\cos\frac{2\pi m}{12}\right)\) y si es
uno de los 5 lugares. **Objetivo:** el estado del mes siguiente.

**Los modelos comparados:**
- **Línea base, persistencia:** "igual que este mes", \(\hat y_{t+1}=y_t\). Todo modelo debe ganarle.
- **Regresión logística multiclase:** \(P(y=k\mid x)=\dfrac{e^{\beta_k^\top x}}{\sum_j e^{\beta_j^\top x}}\), estimada por
  máxima verosimilitud.
- **Random Forest:** promedio de 400 árboles, cada uno entrenado con una muestra al azar.
- **Gradient Boosting:** árboles pequeños sumados, cada uno corrige los errores del anterior: \(F_M(x)=\sum_m\nu\,h_m(x)\).

**Validación con origen móvil (la parte más importante):** en series de tiempo **no** se puede revolver al azar
entrenamiento y prueba, porque el modelo vería el futuro. Para cada uno de los 12 meses de prueba (agosto de 2025 a julio
de 2026) se reentrena con todo lo anterior y se predice solo ese mes: 12 reentrenamientos, 156 predicciones, 30 cambios
reales de estado.

| Modelo | Aciertos (de 156) | Cambios anticipados (de 30) | Falsas alarmas | F1-macro |
|---|---:|---:|---:|---:|
| Persistencia | 126 | 0 | 0 | 0.774 |
| **Regresión logística (elegida)** | **130** | **8** | 4 | 0.793 |
| Random Forest | 130 | 6 | 2 | 0.766 |
| Gradient Boosting | 128 | 7 | 5 | 0.731 |

**A mano (F1 de la logística),** con su matriz de confusión (filas = real):

| | tranquilo | concurrido | saturado |
|---|---:|---:|---:|
| **tranquilo** | 75 | 12 | 0 |
| **concurrido** | 10 | 50 | 2 |
| **saturado** | 0 | 2 | 5 |

- Tranquilo: precisión \(75/85=0.882\), sensibilidad \(75/87=0.862\), \(F1=\dfrac{2\cdot0.882\cdot0.862}{0.882+0.862}=0.872\).
- Concurrido: \(P=50/64=0.781\), \(R=50/62=0.806\), \(F1=0.794\). Saturado: \(F1=0.714\).
- \(F1_{\text{macro}}=(0.872+0.794+0.714)/3=0.793\). Aciertos: \(75+50+5=130\).

**Criterio de elección (tuyo):** el que más acierta y, a igualdad, el que más cambios anticipa (la regla anti-colapso
necesita anticipar). **Lectura honesta:** el estado se repite el 81 % de los meses, así que el modelo agrega poco (+4
aciertos); su valor está en los 8 cambios que anticipa. **Sesgo declarado:** en los cinco lugares hubo solo 2 cambios en
48 casos y el modelo no anticipó ninguno: no se puede decir que anticipe saturaciones del sur. **Código:**
`radar/prediccion.py`.

### 5.2 Pronóstico de visitantes: series de tiempo

#### De dónde salen las series de tiempo

| Serie | Lugar | Fuente y archivo | Meses | Entrenan |
|---|---|---|---:|---:|
| Visitantes INAH a Oxtankah | Bahía Calderitas–Oxtankah | DataTur `BdINAH.zip` → `silver/inah` | 127 (ene-2016 a jul-2026) | 90 |
| Kohunlich + Dzibanché + Ichkabal | Ruta arqueológica del sur | DataTur `BdINAH.zip` → `silver/inah` | 127 | 91 |
| Cruces desde Belice | Chetumal | API de SITUR-Q → `silver/siturq` | 90 (ene-2019 a jun-2026) | 62 |
| Ocupación hotelera | Cancún (referencia) | DataTur semanal → `silver/datatur_ocupacion` | 55 | 55 |

**Por qué estas:** el sur no tiene ocupación oficial en 2025–2026; se pronostica solo lo **medido** que llega a 2026.
Maya Ka'an y la Laguna no tienen serie mensual propia (hueco declarado).

**Meses que no entrenan** (`pronostico/series.py`): un mes cerrado no es "cero demanda". Se marcan y no entrenan (pero se
conservan): cierre (0 visitantes), mes parcial (justo antes de cerrar o después de reabrir) y pandemia (INAH mar-2020 a
dic-2021; Belice mar-2020 a jun-2022). Ejemplo, Ruta en 2025: diciembre de 2024 cierre; enero de 2025 cierre (Dzibanché
seguía cerrada); febrero de 2025 parcial; marzo de 2025 ya entrena.

#### Los cinco modelos

Notación: \(y_t\) = valor del mes \(t\); \(o\) = origen (último mes conocido); \(h\) = meses hacia adelante;
\(S_m\) = forma del año calculada solo con años anteriores al origen.

**1. Línea base (ingenuo estacional):** el mismo mes del año anterior. Sirve de vara para medir a los demás.

**2. Holt-Winters con la forma del año fija.** Se quita la temporada, \(z_t=y_t/S_{m(t)}\), y se suaviza el nivel:

\[\ell_t=\alpha z_t+(1-\alpha)\ell_{t-1},\qquad \hat y_{o+h}=\ell_o\,S_{m(o+h)}\]

(Hay dos variantes y las dos entraron a la comparación: **sin tendencia**, la de arriba, y **con tendencia amortiguada**, que agrega \(b_t\) y \(\phi\). La de tendencia perdió: aprendió la tendencia en plena reapertura y llegó a pronosticar −240 visitantes en la Bahía.)

**A mano (Ruta, origen julio de 2026):** \(\alpha=0.1183\) (lo estima statsmodels). Julio tuvo 5,057 visitantes y su
índice es 0.953: \(z=5{,}306.6\). El nivel de junio era 5,332.5:

\[\ell_{\text{jul}}=0.1183\times5{,}306.6+0.8817\times5{,}332.5=627.8+4{,}701.7=5{,}329.4\]

Enero de 2027: \(\hat y=5{,}329.4\times1.606=8{,}559\) visitantes. El código da 8,559.

**3. Regresión con clima** (mínimos cuadrados sobre el logaritmo):

\[\ln y_t=\tau_{k(t)}+\mu_{m(t)}+\beta\,\frac{L_t-\bar L_{m(t)}}{100}+\gamma\,T_t+\varepsilon_t\]

\(\tau_k\) = nivel del tramo (cambia en cada reapertura), \(\mu_m\) = efecto del mes, \(L_t\) = lluvia, \(T_t\) = 1 si hubo
tormenta. Para el futuro se usa el clima normal (lluvia anómala = 0; tormenta = frecuencia histórica del mes):

\[\hat y_{o+h}=\exp\big(\hat\tau_K+\hat\mu_m+\hat\gamma\,\hat p_m\big)\]

**A mano (Bahía, diciembre de 2026):** con 90 meses de entrenamiento, el nivel del tramo actual es
\(\hat\tau=7.0382\) y el efecto de diciembre \(\hat\mu_{12}=0.1404\); en diciembre nunca hubo tormenta (\(\hat p=0\)):

\[\hat y=e^{7.0382+0.1404}=e^{7.1786}=1{,}311\ \text{visitantes}\]

El coeficiente de la lluvia, \(\hat\beta=-0.115\), dice que cada 100 mm sobre lo normal se asocian a
\(e^{-0.115}-1=-10.9\,\%\) visitantes (\(p=0.027\)).

**4. Gradient Boosting con rezagos** (el quinto, contando las dos variantes de Holt-Winters): árboles que aprenden de todos los pares pasados (origen → destino) usando el último
valor, el promedio de 3 meses y el mismo mes del año anterior. 150 árboles.

#### Cómo se midió el error: origen móvil

Para cada mes del pasado se pronostican los 12 siguientes **usando solo lo que se sabía entonces** (incluida la forma del
año), y se compara con lo que pasó. Solo se comparan los pares que los 5 modelos pudieron pronosticar (366 en la Bahía,
378 en la Ruta, 366 en Belice, 438 en Cancún).

\[MAE=\frac1n\sum|y-\hat y|,\qquad MAPE=\frac{100}{n}\sum\left|\frac{y-\hat y}{y}\right|,\qquad \text{error relativo}=\frac{MAE_{\text{modelo}}}{MAE_{\text{base}}}\]

**A mano (error de un pronóstico):** Bahía, origen enero de 2019, destino febrero de 2019: pronóstico 1,058.48, real 925:
\(e=|\ln(1{,}058.48/925)|=0.1348\) (14.4 % arriba).

#### El rango del 90 % (intervalo conformal)

**Pregunta:** ¿qué tan seguro es el pronóstico? Se usan los errores reales del pasado:

\[\hat q=e_{(k)},\quad k=\lceil(n+1)\cdot0.9\rceil,\qquad \text{rango}=\big[\hat y\,e^{-\hat q},\ \hat y\,e^{\hat q}\big]\]

**A mano (Bahía, diciembre de 2026, 5 meses adelante):** hay \(n=105\) errores de calibración;
\(k=\lceil106\times0.9\rceil=96\); el 96.º error más chico es \(\hat q=0.3132\). Pronóstico 1,311.13:
mínimo \(=1{,}311.13\times e^{-0.3132}=959\); máximo \(=1{,}311.13\times e^{0.3132}=1{,}793\). Diciembre de 2025 tuvo 1,224.

**Cobertura real** (cuántas veces el dato cayó dentro): se mide y se reporta aunque salga peor.

#### Elección (tu criterio): el menor error entre los que tienen rango confiable (cobertura ≥ 80 %)

| Serie | Modelo elegido | Error vs base | MAPE | Cobertura real |
|---|---|---:|---:|---:|
| Bahía | Regresión con clima | 0.898 | 15.7 % | 91.3 % |
| Ruta | Regresión con clima | 0.737 | 21.6 % | 80.3 % |
| Chetumal (Belice) | Regresión con clima | 0.820 | 11.0 % | 94.1 % |
| Cancún (referencia) | Línea base | 1.000 | 3.8 % | 89.3 % |

**Hallazgos honestos:** la Ruta no llega a 90 % de cobertura con ningún modelo (en 2023 las visitas cayeron 10.7 % sin
aviso); el clima casi no mejora el pronóstico (sin clima los errores son casi iguales); en Cancún, repetir el año anterior
es lo mejor. **Código:** `pronostico/modelos.py`, `intervalos.py`, `seleccion.py`.

---

## 6. UCA Procesos estocásticos

### 6.1 Cadena de Markov semanal del norte

**Pregunta:** si Cancún está concurrido esta semana, ¿qué probabilidad hay de que se sature en las próximas semanas?

**Datos:** 7 centros de DataTur × 239 semanas. Estados por percentiles comunes de la ocupación semanal:
\(u_{50}=71.16\,\%\) y \(u_{90}=85.92\,\%\).

**Fórmulas:**
- Matriz de transición (máxima verosimilitud = contar y dividir): \(\hat p_{ij}=\dfrac{n_{ij}}{\sum_j n_{ij}}\).
- Pronóstico a \(k\) semanas: \(\pi_{t+k}=\pi_t P^k\).
- A largo plazo: \(\pi=\pi P\).
- Puntaje de Brier (calidad de las probabilidades): \(B=\frac1N\sum_n\sum_j(p_{n,j}-\mathbb 1[y_n=j])^2\); más bajo es mejor.

**Conteos y matriz** (filas = esta semana):

| | tranquilo | concurrido | saturado | | tranquilo | concurrido | saturado |
|---|---:|---:|---:|---|---:|---:|---:|
| **tranquilo** | 765 | 65 | 0 | → | 0.922 | 0.078 | 0.000 |
| **concurrido** | 67 | 555 | 46 | → | 0.100 | 0.831 | 0.069 |
| **saturado** | 2 | 44 | 122 | → | 0.012 | 0.262 | 0.726 |

**A mano:** fila tranquilo, \(765/830=0.922\). Probabilidad de que un centro tranquilo esté saturado en 2 semanas:
\(0.922\cdot0+0.078\cdot0.069+0\cdot0.726=0.005\). A largo plazo, \(\pi=(0.513,\,0.389,\,0.098)\): el norte pasa el
9.8 % de las semanas saturado.

**Validación (52 semanas de prueba):** Brier de Markov 0.200, 0.389 y 0.490 a 1, 4 y 8 semanas, contra 0.225, 0.484 y
0.676 de la persistencia: **mejores probabilidades**. **Supuesto declarado:** la misma matriz para los 7 centros.
**Código:** `radar/markov.py`.

### 6.2 Tormentas: definición y distancia

**Definición (tuya):** una tormenta **afecta al sur** si un punto de su trayectoria pasa a ≤ 200 km de Chetumal, con
viento ≥ 34 nudos (tormenta tropical o más) y es de 1966 en adelante (era satelital).

Distancia sobre la Tierra (haversine, \(R=6{,}371\) km):

\[d=2R\arcsin\sqrt{\sin^2\frac{\Delta\varphi}{2}+\cos\varphi_1\cos\varphi_2\sin^2\frac{\Delta\lambda}{2}}\]

**A mano (huracán Carmen, 1974, en 18.6° N 88.2° O):** \(\Delta\varphi=\Delta\lambda=0.1°=0.0017453\) rad;
\(a=7.6154\times10^{-7}+0.94832\cdot0.94777\cdot7.6154\times10^{-7}=1.4460\times10^{-6}\);
\(d=2\cdot6{,}371\cdot\arcsin(0.0012025)=15.3\) km → **evento**. Resultado: **31 eventos en 60 años**.

### 6.3 Poisson: probabilidad de tormenta por mes

\[N_m\sim\text{Poisson}(\lambda_m),\qquad \hat\lambda_m=\frac{\#\text{eventos del mes }m}{60},\qquad P(N_m\ge1)=1-e^{-\hat\lambda_m}\]

**A mano:** agosto tuvo 9 eventos en 60 años: \(\hat\lambda=0.15\), \(P=1-e^{-0.15}=13.9\,\%\). Septiembre:
\(8/60\Rightarrow12.5\,\%\). De diciembre a abril: 0 %. **Al menos una en el año:** \(1-e^{-31/60}=40.3\,\%\).

| Mes | may | jun | jul | ago | sep | oct | nov | dic–abr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Eventos | 1 | 3 | 1 | 9 | 8 | 6 | 3 | 0 |
| \(P(N\ge1)\) | 1.7 % | 4.9 % | 1.7 % | 13.9 % | 12.5 % | 9.5 % | 4.9 % | 0 % |

**Supuesto:** las tormentas llegan de forma independiente, a tasa constante por mes. **Código:** `pronostico/escenarios.py`.

### 6.4 Monte Carlo: escenarios malo, probable y bueno

**Pregunta (incidente de estocásticos):** ¿y si la campaña funciona mejor o peor? ¿qué tan probable es rebasar la
capacidad?

Para cada uno de **10,000 futuros** \(r\) y cada mes \(j\):

\[D^{(r)}_j=\hat y_j\cdot e^{\varepsilon^{(r)}_j}\cdot\big(1-\delta\,\mathbb 1[N^{(r)}_j\ge1]\big)\]

- \(\hat y_j\): el pronóstico del modelo elegido.
- \(\varepsilon^{(r)}_j\): errores reales copiados de **un mismo origen** del pasado, sorteado al azar (así se conserva que
  los meses flojos vienen juntos).
- \(N^{(r)}_j\): tormentas sorteadas con la Poisson del mes.
- \(\delta\in\{0,\,0.25,\,0.50\}\): el golpe de una tormenta. **Es un supuesto**: no se pudo medir (solo 3 meses con
  tormenta en el entrenamiento).

**Escenarios:** malo, probable y bueno = percentiles 10, 50 y 90 de los 10,000 futuros. **Riesgo de capacidad:**
\(\hat p_j=\frac1R\sum_r\mathbb 1[D^{(r)}_j>C]\), con \(C\) = el mes más alto que el lugar ya recibió (capacidad probada).

**Ilustración del mecanismo (Bahía, agosto de 2026):** el pronóstico es 879. Si un futuro sortea un error de \(-0.20\) y
una tormenta con \(\delta=0.5\): \(879\times e^{-0.20}\times0.5=879\times0.8187\times0.5=360\). Si sortea \(+0.10\) y no
hay tormenta: \(879\times1.105=971\). Con los 10,000 futuros, los percentiles dan 684 / 930 / 1,202.

| Lugar (año completo) | Malo / probable / bueno (sin golpe) | Con golpe de 50 % | Riesgo de que algún mes rebase la capacidad |
|---|---|---|---:|
| Ruta del sur | 55,811 / 62,212 / 73,884 | 54,751 / 61,440 / 72,628 | 30.9 % (cap. 10,465) |
| Bahía | 10,106 / 11,217 / 13,085 | 9,915 / 11,019 / 12,777 | 24.2 % (cap. 1,639) |
| Chetumal (Belice) | 551,986 / 620,304 / 671,956 | 535,346 / 606,138 / 660,162 | 38.3 % (cap. 65,792) |

**Lectura:** las tormentas pesan en el mes, no en el año (con el golpe más duro el año baja 1–2 %); el riesgo de
capacidad se concentra en diciembre y enero.

### 6.5 Sensibilidad: ¿qué variable mueve más?

Misma regresión, agregando una variable \(v\): \(\ln y_t=\tau_{k(t)}+\mu_{m(t)}+\theta v_t\); efecto \(=e^{\hat\theta}-1\).

| Lugar | +100 mm de lluvia | +1 peso por dólar |
|---|---|---|
| Bahía | **−9.7 %** (\(p=0.039\)) | −0.2 % (\(p=0.92\)) |
| Ruta | −0.6 % (\(p=0.92\)) | **+6.8 %** (\(p=0.011\)) |
| Chetumal (Belice) | **−4.7 %** (\(p=0.031\)) | +1.2 % (\(p=0.36\)) |

En negritas, \(p<0.05\). Son asociaciones, no causas probadas.

---

## 7. UCA Investigación de Operaciones

### 7.1 La pregunta y los parámetros

**Pregunta:** ¿cuánto dinero va a cada lugar, cada mes y en cada canal, para traer el máximo de visitantes sin anunciar
donde está lleno y sin rebasar la capacidad?

**Conversiones por peso de cada canal** (costo por clic y conversión de la categoría Travel, WordStream 2025; dólar de FRED,
agosto de 2026 = 17.0609):

\[r_c=\frac{\text{conversión}_c}{\text{costo por clic}_c\times\text{pesos por dólar}}\]

**A mano:** Google: \(r=\dfrac{0.0575}{2.12\times17.0609}=\dfrac{0.0575}{36.169}=0.001590\) → **1.59 visitantes por cada
$1,000**. Facebook: \(r=\dfrac{0.0575}{0.51\times17.0609}=\dfrac{0.0575}{8.701}=0.006608\) → **6.61 por cada $1,000**.
(La conversión de Facebook para turismo no está publicada: el caso base usa la de Google y se prueba 3 % y 6.38 %.)

**Supuesto declarado:** cada conversión cuenta como un visitante (cota alta: protege la capacidad).

### 7.2 El modelo completo (programación estocástica de dos etapas)

**Conjuntos:** meses \(m\) (oct-2026 a jun-2027, los 9 con pronóstico), lugares \(l\) (los 3 del sur), canales \(c\)
(Google, Facebook), escenarios \(s\) (malo, probable, bueno, con pesos 0.3, 0.4 y 0.3).

**Variables de decisión:**
- **Etapa 1 (se decide hoy):** \(x_{m,l,c}\ge0\) = pesos en el mes \(m\), lugar \(l\), canal \(c\).
- **Etapa 2 (recurso, se decide cuando se ve el escenario):** \(y_{s,m,l}\in\{0,1\}\) = el anuncio sigue encendido;
  \(w_{s,m,l}\ge0\) = visitantes que sí llegan.

Visitantes que trae la campaña: \(v_{m,l}=\sum_c r_c\,x_{m,l,c}\).

**Función objetivo** (visitantes esperados):

\[\max\ \sum_s p_s\sum_{m,l}w_{s,m,l}\]

**Restricciones:**
1. Presupuesto: \(\sum_{m,l,c}x_{m,l,c}\le B\), con \(B=250{,}000\times9/12=187{,}500\).
2. Cero anuncio en temporada alta: \(x_{m,l,c}=0\) si \((m,l)\) es alta (calendario de la Fase 5).
3. Capacidad probada: \(D^{p50}_{m,l}+v_{m,l}\le C_l\).
4. Equidad: \(\sum_{m,c}x_{m,l,c}\ge0.15\,B\) para cada lugar.
5. Tope por canal: \(\sum_{m,l}x_{m,l,c}\le0.70\,B\).
6. Recurso (si el escenario más la campaña rebasan la capacidad, el anuncio se pausa):
   \(D_{s,m,l}+v_{m,l}\le C_l+M(1-y_{s,m,l})\), \(w\le v\), \(w\le U\,y\).

**Qué es la "M grande":** un número suficientemente grande que "apaga" la restricción cuando \(y=0\). Si el anuncio sigue
(\(y=1\)), la capacidad debe respetarse; si se pausa (\(y=0\)), la restricción deja de obligar, pero \(w\le U\cdot0=0\): esas
conversiones se pierden. Así el modelo evita, desde hoy, gastar en meses donde un escenario bueno llenaría el lugar.

### 7.3 Cómo lo resuelve la computadora

**PuLP** arma el modelo (54 variables \(x\), 81 binarias \(y\), 81 \(w\)) y **CBC** lo resuelve:
- **Simplex:** recorre las esquinas de la región permitida (las restricciones lineales forman un poliedro) hasta la mejor.
- **Branch-and-bound:** como \(y\) solo puede valer 0 o 1, CBC resuelve versiones con \(y\) continua, y si una sale
  fraccionaria, "ramifica" (prueba \(y=0\) y \(y=1\)) y descarta las ramas que no pueden mejorar.
- Tarda **0.3 segundos**.

**Desempate en dos pasos (lexicográfico, decisión tuya):** como todos los lugares convierten igual, hay muchas soluciones
con el mismo máximo, y el modelo mandaba todo el dinero de cada lugar a un solo mes. Paso 1: el máximo \(z^*\). Paso 2:
con al menos \(z^*\) visitantes, repartir **proporcional al espacio libre**:

\[\min\sum\left|x_{m,l,c}-\pi_{m,l}\sum x_{\cdot,\cdot,c}\right|,\qquad \pi_{m,l}=\frac{\text{libre}_{m,l}}{\sum\text{libre}},\qquad \text{libre}=1-\frac{D^{p50}}{C}\]

(El valor absoluto se convierte en lineal con una variable auxiliar \(d\ge x-\text{meta}\) y \(d\ge\text{meta}-x\).)

### 7.4 Resultado, a mano

**El máximo:** Facebook rinde más por peso y se lleva su tope; Google el resto:

\[z^*=0.70\times187{,}500\times0.006608+0.30\times187{,}500\times0.001590=867.3+89.4=956.8\ \text{visitantes}\]

Unos **$196 por visitante**. Reparto: Ruta 41.5 % ($77,790), Bahía 36.9 % ($69,175), Chetumal 21.6 % ($40,535).

**El reparto proporcional (Ruta, octubre de 2026):** libre \(=1-3{,}688/10{,}465=0.6476\); con \(\sum\text{libre}=8.0004\)
en las 20 combinaciones permitidas, \(\pi=0.0809\): \(0.0809\times131{,}250=10{,}624\) pesos en Facebook y
\(0.0809\times56{,}250=4{,}553\) en Google. El código da lo mismo.

### 7.5 ¿Cuánto cuesta cada regla? (precios sombra y Pareto)

**Costo de cada regla** (se resuelve sin ella y se compara):

| Regla | Visitantes que cuesta |
|---|---:|
| Cero anuncio en temporada alta | 0 |
| Tope de capacidad | 0 |
| Equidad de 15 % | 0 |
| Tope de 70 % por canal | 282 (29.5 %) |

**Precio sombra** = cuánto mejora el objetivo si una restricción se afloja una unidad (\(\partial z^*/\partial b_i\)):
- Presupuesto: 0.00159 visitantes por peso (1.59 por cada $1,000), porque el peso extra iría a Google.
- Tope de Facebook: \(0.006608-0.001590=0.005019\) por peso; quitarlo suma \(0.30\times187{,}500\times0.005019=282.3\).

**Frontera de Pareto** (\(\varepsilon\)-restricción): se pide que ningún mes con anuncio pase de \(\varepsilon\) veces su
capacidad. Hasta \(\varepsilon=40\,\%\) no se pierde ningún visitante; con 35 % llegan 537 y con 30 %, ninguno.

**Respuesta al incidente de IO ("¿qué es óptimo?", "¿cuánto cuesta la regla ambiental?"):** óptimo = máximo de visitantes
cumpliendo reglas que tú elegiste; a este presupuesto las reglas ambientales y de equidad **no cuestan nada**; lo que
cuesta es no depender de una sola plataforma. **Sensibilidad:** con conversión de 3 % llegan 542; con 6.38 %, 1,052; con
$500,000 al año, 1,914. **Código:** `campana/presupuesto.py`.

### 7.6 La etapa 2 en la práctica: el motor de la Torre

Cada semana, para cada lugar, el motor (`envivo/motor.py`) decide: temporada alta (no se gasta), fuera del plan, pausado
(tormenta cerca, clima raro o llegó más gente de la esperada) o encendido. **El dinero pausado pasa a la siguiente semana
permitida:**

\[b=\frac{\text{pesos del mes}}{\#\text{lunes del mes}},\qquad g_w=(b+A_{w-1})\cdot\mathbb 1[\text{encendido}],\qquad A_w=A_{w-1}+b\ \text{si se pausa}\]

**A mano:** octubre tiene 4 lunes; con $4,000 en el mes, \(b=\$1{,}000\). Semana 1 pausada: \(A=1{,}000\). Semana 2
encendida: se gastan \(1{,}000+1{,}000=\$2{,}000\) y \(A=0\).

**Resultado de 239 semanas:** 48 pausas de lugar-semana (casi todas por clima raro; las 3 tormentas pausaron los 3
lugares); todo el dinero pausado se gastó después; "¿Ibas al norte?" se encendió 6 semanas.

---

## 8. UCA Mercadotecnia digital

### 8.1 Buyer persona: cada rasgo dice de dónde sale

| Persona | Rasgo | Valor | Tipo |
|---|---|---|---|
| **La que vuelve al sur** | Origen | Nacional: 94.8 % de Oxtankah y 63.3 % de la Ruta (INAH 2025) | dato |
| | Qué valora | Calma (0.41×) y cultura (0.48×) | derivado |
| | Cómo se informa | Mensajería 90.6 %, redes 80.4 % (ENDUTIH 2025) | dato |
| | Estado de origen, edad, ingreso | No hay dato oficial | hueco |
| **La que baja del norte** | Origen | De 9,408,423 extranjeros en Cancún (2025): EE. UU. 56.3 %, Canadá 17.1 % | dato |
| | Sexo | 53.4 % mujeres | dato |
| | Por qué no llega sola al sur | El aeropuerto de Chetumal recibió 250 extranjeros | dato |
| | Cómo se informa | Busca en Google y usa redes desde el destino | supuesto |

### 8.2 Marca

- **Nombre:** "El sur tiene espacio" ("The south has room").
- **Propuesta de valor:** el Caribe mexicano con espacio: zonas mayas con 15.5 veces menos visitantes que Tulum, una bahía
  tranquila y la comida del sur.
- **Personalidad:** cercana y tranquila, orgullosa de lo maya y de lo mexicano, con espíritu de aventura.
- **Posicionamiento:** la opción cultural y tranquila frente a Tulum y Cancún.

### 8.3 Mensajes con respaldo

Cinco anuncios (Google y Facebook/Instagram en español e inglés, y WhatsApp). Reglas: cada uno tiene su dato de respaldo;
**sin precios ni horas de viaje** (no hay dato); el largo se revisa contra los límites de cada plataforma (Google: título
≤ 30 y descripción ≤ 90; Meta: título ≤ 40, texto ≤ 125). La palabra "con espacio" se apoya en el 15.5.

### 8.4 Medios justificados

| Medio | Peso | Por qué (con dato) |
|---|---:|---|
| Facebook / Instagram | 70 % | 6.61 visitantes por cada $1,000; 80.4 % usa redes |
| Google búsqueda | 30 % | Llega a quien ya busca viajar; conversión medida 5.75 % |
| WhatsApp (orgánico) | sin costo | 90.6 % usa mensajería |
| La página | destino | Planeador en 9 idiomas, sin internet externo |

### 8.5 Indicadores (KPI) con su fórmula

| KPI | Fórmula | Meta |
|---|---|---|
| Interacción (CTR) | \(\dfrac{\text{clics}}{\text{impresiones}}\) | Google ≥ 8.73 %; Facebook ≥ 2.76 % |
| Conversión | \(\dfrac{\text{planes de viaje}}{\text{clics}}\) | ≥ 5.75 % |
| Costo por visitante | \(\dfrac{\text{pesos gastados}}{\text{conversiones}}\) | ≤ $196 |
| Afluencia | visitantes reales − escenario probable | +957 en 9 meses |
| Capacidad | \(\dfrac{\text{esperados}+\text{campaña}}{\text{capacidad probada}}\) | ≤ 40 % en meses con anuncio |
| Ambiental | semanas con anuncio en temporada alta o mal clima | 0 |
| Económico | ocupación hotelera de Chetumal | **hueco**: no se publica desde 2025 |

**Regla anti-colapso** (incidente de mercadotecnia): la campaña nunca anuncia un lugar lleno; la Torre pausa sola con mal
clima; "¿Ibas al norte?" manda a quien iba al norte hacia donde hay espacio.

---

## 9. Integración: cómo se pasan la estafeta (con archivos)

| Paso | Sale de | Archivo | Lo usa |
|---|---|---|---|
| 1 | Forma del año y Monte Carlo (Fase 5) | `gold/pronostico_calendario.parquet`, `pronostico_escenarios.parquet` | El presupuesto: temporada alta y capacidad |
| 2 | Presupuesto (Fase 6) | `gold/presupuesto_plan.parquet` | La Torre: cuánto gastar cada semana |
| 3 | Radar (Fase 4) | Cortes p50/p90 de la ocupación semanal | La Torre: cuándo el norte está saturado |
| 4 | Torre (Fase 7) | `gold/envivo_decisiones.parquet` | La campaña: KPI ambiental y "¿Ibas al norte?" |
| 5 | Campaña (Fase 8) | `gold/campana.json` | La página y el coloquio |

---

## 10. Cómo correr todo, en orden

```text
1. Fase 1 (descargas):      python -m torre.base.ingesta_siturq / ingesta_datatur / ingesta_abiertas
2. Fase 2 (Silver):         python -m torre.base.silver_<fuente>   (12 limpiezas con Spark)
                            python -m torre.base.almacen ; python -m torre.base.diccionario
3. Fase 3-4 (Radar):        python -m torre.radar.criterios / panel / indice / prediccion / markov / clustering
4. Fase 5 (Pronóstico):     python -m torre.pronostico.series / forma / modelos / intervalos / seleccion / escenarios / calendario
5. Fase 6 (Presupuesto):    python -m torre.campana.presupuesto
6. Fase 7 (Torre):          python -m torre.envivo.senales ; python -m torre.envivo.torre
7. Fase 8 (Campaña):        python -m torre.campana.texto ; python -m torre.campana.marca
8. Página y servidor:       python -m torre.api.datos_pagina ; python -m torre.api.servidor
9. Pruebas:                 python -m pytest      (276 pruebas)
```

(Todo desde `backend/` con el Python de `.venv`. El detalle está en `README.md`.)

---

## 11. Preguntas difíciles que te pueden hacer (y su respuesta)

| Pregunta | Respuesta corta |
|---|---|
| ¿Por qué no usaste el promedio de los porcentajes de ocupación? | Porque los meses con pocos cuartos pesarían igual que los grandes. Se suman cuartos y luego se divide |
| ¿Por qué validaste con origen móvil y no con un 80/20 al azar? | En series de tiempo, revolver al azar deja que el modelo vea el futuro; el origen móvil solo usa el pasado |
| ¿Tu modelo de clasificación sirve? | Le gana a "igual que este mes" por 4 aciertos de 156 y anticipa 8 de 30 cambios; en el sur casi no hubo cambios con qué probarlo, y así lo declaro |
| ¿Por qué Poisson? | Las tormentas son eventos raros e independientes en un mes: es la distribución natural para contar eventos raros |
| ¿Por qué copias errores de un mismo origen en el Monte Carlo? | Porque los meses flojos vienen juntos; sortear cada mes por separado haría el año demasiado parejo |
| ¿Qué es el golpe de tormenta de 50 %? | Un supuesto, no un dato: solo hubo 3 meses con tormenta para medirlo; por eso se prueba con 0, 25 y 50 % |
| ¿Qué es lo "estocástico" del modelo de IO? | La segunda etapa: la decisión de pausar depende del escenario malo, probable o bueno, cada uno con su probabilidad |
| ¿Qué significa el precio sombra? | Cuántos visitantes más traería relajar una regla una unidad; el del presupuesto es 1.59 por cada $1,000 |
| ¿Por qué Isolation Forest? | Detecta lo raro sin que alguien defina "raro"; validado: marcó las 3 tormentas sin saberlo |
| ¿De dónde sale la capacidad? | Es la capacidad probada: el mes más alto que el lugar ya recibió (no la capacidad física oficial) |
| ¿Inventaste algún dato? | No. Lo que no existe es hueco; lo estimado lleva `_est`; cada cifra se rastrea en `docs/trazabilidad.md` |
| ¿Por qué aparece Claude? | Porque usé un asistente de programación con IA; las decisiones son mías y están documentadas (ver §2.1) |

---

## 12. Glosario

| Término | Qué significa |
|---|---|
| Bronze / Silver / Gold | Capas de datos: crudo, limpio, resultados |
| Parquet | Formato de tabla en columnas, comprimido, que lee rápido |
| Spark | Motor que procesa tablas grandes en paralelo |
| Streaming | Procesar datos conforme llegan, uno por uno |
| Percentil 50 / 90 | El valor que deja abajo al 50 % / 90 % de los datos |
| Origen móvil | Validar un pronóstico usando solo lo que se sabía en cada momento del pasado |
| Intervalo conformal | Un rango que usa los errores reales del pasado para dar una cobertura garantizada |
| Persistencia | El modelo más simple: "igual que este mes"; sirve de vara para medir |
| Cadena de Markov | El estado de la semana siguiente depende solo del estado de esta semana |
| Poisson | Distribución para contar eventos raros en un periodo |
| Monte Carlo | Simular muchos futuros posibles y ver sus percentiles |
| Precio sombra | Cuánto mejora el resultado si una restricción se afloja una unidad |
| Frontera de Pareto | Lo mejor que se puede lograr en un objetivo para cada nivel del otro |
| Riesgo relativo | Cuántas veces más probable es algo en un grupo que en general |
| Lift | Cuánto más probable es la consecuencia cuando aparece la causa |
| `_est` | Sufijo de lo estimado |
| `_flag` | Sufijo de una bandera de calidad |
