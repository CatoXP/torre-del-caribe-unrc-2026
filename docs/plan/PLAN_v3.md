# Plan v3 — Fusión A1 + A3 + A5: "Torre del Caribe"
### Radar (hoy) · Pronóstico (próximos meses) · Tiempo casi real (esta semana)

Autor: **Brandon Uriel García Sánchez** · UNRC · Lic. en Ciencias de Datos para Negocios · 5° semestre 2026-2
Problema Prototípico: *Turismo inteligente sustentable para México* · Estado: **Quintana Roo**

> **Nota sobre `OBJETIVO.md`:** todavía no existe como archivo porque el modo plan solo permite escribir
> este plan. Su contenido completo y literal está en la **Parte A** de este documento. Al aprobar el plan,
> el primer paso es crear `OBJETIVO.md` con esa Parte A y regenerar el PDF.

---

# PARTE A — Contenido literal de `OBJETIVO.md`

## A.1 Tus instrucciones, textuales (sin corregir nada)

**Prompt original (26-sep-2026):**
> Mira esta la nueva pagina que vamos a hacer te mande el DESIGN.MD la quiero convertir en una pagina web
> donde apliquemos el problema prototipico pero en vez que generos todo de una vez quiero que explicitamente
> me hagas un plan completo de como podemos abarcar el problema prototipico y entreguemos la campaña de
> marketing y los 6 incidentes criticos en una pagina web de front end y el back-end sea todo lo que pide
> desde usar pyspark, desde ml, desde operaciones de investiagacion, marketing como dije (LA PARTE MÁS
> IMPORTANTE ES LA VISUALIZACION Y CAPTAR ATENCION) Crear nuestro bayer persona analizar variables, flujos
> pero quiero saber que haces y no que seas una caja negra me expliques el porque tomaste una decisión y el
> porque lo hiciste argumentandomelo con datos reales y no supociciones o alucinaciones. El entregable final
> es todo el flujo de machine learning documentado con comentarios en español mi nombre en el codigo el
> porque lo hice y su .README explicando el porque se tomo esa decision y todo, este es el prompt más largo
> que te estoy dando y vas a consultar, metelo en un md o lo que sea para que no te salgas del objetivo. NO
> QUIERO STREAMLIT quiero una pagina real web real con el DESIGN y el backend conectada a ella.
>
> ARMAME EL PLAN QUIERO 5 ALTERNATIVAS CON CADA RUBRICA CUMPLIDA, DONDE YA SABES QUE ESTAN LOS DATOS Y ESTE
> TODO CONFIRMADO SIN TEMAS I COMPLICACIONES ( QUIERO EVITAR QUE TU HAGAS 1 ALTERNATIVA Y EN PLENO
> DESARROLLO NO SEA POSIBLE REALIZARLO)

**Autor:** "Por ahora ponme a mi Brandon Uriel Garcia Sanchez" · **Estado:** Quintana Roo.

**Segunda instrucción:**
> Quiero que armemos desde 0 todos los sistemas que consultaste esos no me gustaron y quiero que tu lo hagas
> otra vez desde 0 y lo armemos los dos juntos esto metelo a las instrucciones de objetivo, junto con que
> necesitamos que lo desarrolles CONMIGO Y NO VIBEDEES TODO SIN SABER COMO CAJA NEGRO para saber que haces y
> el porque como quedamos anteriormente, el front end es full amigable para usuario no tecnico
>
> VUelve a formulas las 5 alternativas sin toamr en cuenta esos flujos de IA y ML que estaban en el anterior
> proyecto mal hecho.

**Tercera instrucción (elección):**
> A5 A1 y A3 como podemos fucionarlo dame el plan donde no se encimen ambas y se compaginen para no estar
> saturado y funcionen en la pagina, (...) Y pasame el plan completo literal que vamos a hacer de cada cosa
> los datos que vamos a tomar, y todo los datos que definimos en objetivo pero con A5, A1 y A3

## A.2 Mandatos derivados (lo que no se negocia)
1. **Desde cero.** Nada del proyecto anterior (código `cauce`, modelos, salidas, personas, gemelo, semáforo,
   malla, priores, cifras). Esa carpeta ya no existe.
2. **Contigo, sin caja negra, sin "vibecodear".** Protocolo de la sección A.6.
3. **Web real** (no Streamlit) con el `DESIGN.md` (Flighty) + **backend conectado que calcula**.
4. **Front amigable para público no técnico.** Lo más importante es la visualización y captar la atención.
5. PySpark, minería, ML, estocásticos, IO, mercadotecnia, buyer persona, variables y flujos.
6. Solo **datos reales confirmados**. Un hueco se declara, no se rellena ni se inventa.
7. Entregable: flujo de ML documentado, comentarios en español con tu nombre, el porqué de cada decisión,
   README, notebooks.
8. **Alternativa elegida:** fusión **A1 Radar + A3 Pronóstico + A5 Tiempo casi real**, sin encimarse.

## A.3 El Problema Prototípico (textual del PDF oficial)
**Pregunta central:** *¿Cómo diseñar una campaña publicitaria basada en Ciencia de Datos que permita promover
estratégicamente un destino turístico del estado seleccionado, atraer segmentos de visitantes de manera
responsable y contribuir a una distribución más equilibrada de los flujos turísticos, aprovechando la
capacidad disponible y reduciendo los impactos económicos, sociales y ambientales asociados con la
saturación turística en el mismo?*

**Preguntas secundarias:**
1. ¿Qué patrones temporales, espaciales y de comportamiento caracterizan la concentración de turistas en determinados destinos?
2. ¿Qué variables están relacionadas con la saturación o baja actividad turística de los diferentes destinos del estado?
3. ¿Cómo puede estimarse la demanda turística futura considerando la incertidumbre y variabilidad del comportamiento de los visitantes?
4. ¿Qué escenarios de redistribución de turistas permitirían disminuir la presión sobre los destinos saturados sin reducir significativamente la actividad económica del estado?
5. ¿Qué características de los visitantes pueden utilizarse para diseñar estrategias de recomendación de destinos alternativos en el mismo estado?
6. ¿Qué impacto tendría una estrategia de redistribución sobre las comunidades receptoras y sobre los destinos actualmente saturados?
7. ¿Cómo puede evaluarse si una propuesta de redistribución turística es viable, sustentable y efectiva?

**Los 10 elementos obligatorios de la campaña (Entregable A):** recopilación, integración y análisis de datos · patrones, tendencias y relaciones ·
público objetivo y **buyer persona** · escenarios y apoyo a decisiones · **branding** (identidad, personalidad,
propuesta de valor, posicionamiento, elementos visuales) · medios y canales justificados con datos · **piezas
publicitarias** · **implementación** en canales · asignación y optimización del presupuesto · **indicadores** de
desempeño e impacto (alcance, interacción, conversión, afluencia, presupuesto, efectos económicos, sociales y
ambientales).

**Informe técnico (Entregable B, 30–40 págs.):** Portada · Introducción · Planteamiento · Pregunta central y
secundarias · Justificación · Fuentes de datos · Arquitectura y almacenamiento · Preparación y calidad ·
Minería · Aprendizaje de máquina · Estocásticos y escenarios · Investigación de Operaciones · Mercadotecnia
digital · Integración de resultados · Diseño y justificación de la campaña · Comparación de escenarios ·
Presupuesto y optimización · Indicadores · Propuesta final · Conclusiones · Limitaciones · Referencias · Anexos.

**Productos técnicos (Entregable C):** bases de datos, diccionario de datos, código, modelos, notebooks,
consultas, diagramas, visualizaciones, resultados de simulaciones, resultados de optimización, documentación.

**Coloquio:** 15 minutos máximo, **todos los integrantes participan** y defienden con evidencia; la campaña
es el centro; no presentar cada UCA aislada.

## A.4 Rúbrica (nivel "Excelente", textual)
| # | Criterio | Peso | Excelente |
|---|---|---|---|
| 1 | Planteamiento | 8 % | Delimita el problema, identifica variables, actores y relaciones; problemática analizable con datos |
| 2 | Grandes volúmenes | 12 % | Integra diversas fuentes; estructura, documenta, transforma y almacena considerando calidad y arquitectura |
| 3 | Minería | 12 % | Identifica patrones, tendencias y relaciones con técnicas pertinentes y los interpreta en función del problema |
| 4 | Aprendizaje de máquina | 12 % | Construye, valida, compara e interpreta modelos con métricas adecuadas y justifica la selección |
| 5 | Estocásticos | 10 % | Incorpora la incertidumbre, genera escenarios pertinentes y analiza implicaciones para decidir |
| 6 | Investigación de Operaciones | 12 % | Formula variables de decisión, función objetivo y restricciones; solución justificable |
| 7 | Mercadotecnia digital | 8 % | Estrategia integral sustentada en datos; plan mercadológico, branding, buyer persona, medios digitales |
| 8 | Integración | 10 % | Articula los seis componentes; los resultados de cada uno alimentan las decisiones de los demás |
| 9 | Propuesta e impacto | 8 % | Compara escenarios; alternativa viable y equilibrada entre economía, distribución y ambiente |
| 10 | Informe | 4 % | Claro, riguroso, visualmente adecuado, argumentación técnica sólida |
| 11 | Coloquio | 4 % | 15 min, todos participan y defienden con evidencia |

## A.5 Los 6 incidentes críticos (preguntas que hay que responder)
- **Estocásticos — "¿Y si la campaña funciona mejor o peor?"**: intervalo de confianza al 90 %; escenarios
  optimista/moderado/pesimista con probabilidad; Monte Carlo del riesgo de rebasar la capacidad de carga;
  variables más sensibles (transporte, clima, tipo de cambio, sentimiento) y cómo monitorearlas en tiempo
  real; ¿varios destinos o uno solo?
- **Investigación de Operaciones — optimización sustentable**: ¿qué es "óptimo"?; ¿qué priorizar si los
  objetivos chocan?; ¿qué restricciones son indispensables y qué pasa si se cambian?; sensibilidad; asignar el
  presupuesto entre destinos, temporadas y canales sin rebasar la capacidad y sin generar desigualdades.
- **Big Data — "cuando los datos no caben en una computadora"**: fuentes heterogéneas, estructuradas y
  semiestructuradas, históricas y continuas; fuentes que no coinciden; qué guardar, transformar o descartar;
  riesgos de privacidad; arquitectura de **baja latencia** para ajustar la campaña **durante** su ejecución;
  evitar que la saturación solo se traslade.
- **Aprendizaje de máquina — ¿turismo más sustentable?**: métricas técnicas **y** de impacto; sesgo contra
  destinos con poca huella digital; ML como apoyo, no sustituto; producto de negocio escalable; momento óptimo
  para activar la campaña.
- **Minería — "los patrones sí importan"**: datos fragmentados y ruidosos; eventos raros (huracanes, sargazo);
  series con estacionalidad; interpretabilidad para no técnicos; capacidad de carga; ética y privacidad;
  patrones → buyer persona, mensajes, segmentos y canales.
- **Mercadotecnia digital — sin nuevo colapso**: mercado objetivo, buyer persona, propuesta de valor, medios,
  presupuesto, indicadores; promover sin dañar recursos ni cultura; ¿qué hacer si la afluencia rebasa la capacidad?

## A.6 Protocolo de trabajo conjunto (anti-caja negra)
1. Explico qué vamos a hacer y por qué, **con la cifra real** que lo motiva.
2. Si hay decisión real, te doy 2 o 3 opciones con pros y contras, y **tú eliges**.
3. Programo **una pieza pequeña** (una función o un notebook corto) comentada en español.
4. **La corres tú**; revisamos juntos el resultado y la explico línea por línea donde haga falta.
5. Se escribe `docs/decisiones/NN-*.md`: decisión, opciones descartadas, evidencia (cifra + archivo +
   función) y consecuencia, pensada para que tus compañeros la defiendan.
6. Checkpoint: "¿Se lo puedes explicar a un sinodal?". Si no, repasamos.
7. **Una fase a la vez**; no se abre la siguiente sin tu visto bueno.

Encabezado de cada archivo de código:
```python
# Autor: Brandon Uriel García Sánchez
# Módulo: (Radar | Pronóstico | Torre en vivo | Campaña | Base de datos)
# Qué hace:          ...
# Por qué así:       ... (decisión + alternativa descartada + evidencia)
# Datos de entrada:  ... (fuente oficial + archivo)
# Alimenta a:        ... (qué decisión de la campaña)
```

## A.7 Reglas de oro
(a) No inventar datos. (b) Toda cifra es rastreable: crudo → función → salida. (c) Lo estimado lleva sufijo
`_est` y su error. (d) Nada de scraping prohibido por términos de uso (TripAdvisor, Google). (e) Si a media
fase falta un dato, **se detiene y se avisa**.

---

# PARTE B — El plan fusionado

## B.1 La idea en una frase
**Tres horizontes de tiempo, un solo sistema y una sola campaña.** Como la app de vuelos del `DESIGN.md`, la
página responde tres preguntas que nunca se enciman:

| Módulo | Pregunta que responde (solo esa) | Horizonte | Unidad | Para quién en la página |
|---|---|---|---|---|
| **A1 Radar** | ¿**Dónde** hay presión y dónde hay espacio? | Hoy / estado | destino × semana (norte) y destino × mes (sur) | Turista y autoridad |
| **A3 Pronóstico** | ¿**Cuándo** conviene ir y **cuánto** invertir? | 1 a 12 meses | destino × mes | Turista (calendario) y autoridad (presupuesto) |
| **A5 Torre en vivo** | ¿Qué hace la campaña **esta semana**? | Semana a semana | destino × semana | Autoridad y sinodal |

**Cómo se pasan la estafeta (sin duplicar):**
```
A3 Pronóstico ──(plan mensual de presupuesto: etapa 1)──► CAMPAÑA
      ▲                                                     │
      │ nivel esperado por mes                              ▼
A1 Radar ◄──(estado real de la semana)── A5 Torre en vivo ──(dispara la etapa 2: pausar / reasignar)
      │                                                     ▲
      └──(probabilidad de saturación a 1–8 semanas)─────────┘
```
- A3 decide **el plan** (cuánto dinero por mes, destino y canal).
- A1 dice **el estado** (tranquilo / concurrido / saturado) y la probabilidad de cambiar en las próximas semanas.
- A5 **observa** la semana real, la compara con lo esperado y **ejecuta** los ajustes que A3 dejó previstos.

## B.2 Reparto sin encimarse: una técnica por módulo, cada una con su pregunta

| UCA | A1 Radar | A3 Pronóstico | A5 Torre en vivo | Campaña (común) |
|---|---|---|---|---|
| **Big Data** | — | — | **Spark Structured Streaming** (reproducción semanal) + SSE | — |
| *(base batch)* | *Lakehouse PySpark Bronze→Silver→Gold: lo usan los tres* | | | |
| **Minería** | Índice de Presión Turística + clustering de los 54 centros del país | Descomposición estacional (STL) y fuerza de temporada | Detección de anomalías (Isolation Forest) en ocupación semanal y clima | Minería de texto de 85,993 reseñas: temas, sentimiento por aspecto, reglas de asociación |
| **ML** | **Clasificador** de estado de saturación (logística vs Random Forest vs Gradient Boosting) | **Regresor/pronóstico** mensual (Holt-Winters vs regresión con clima vs Gradient Boosting) con **intervalos conformales al 90 %** | — (a propósito: no se agrega un tercer modelo) | — |
| **Estocásticos** | **Cadena de Markov** semanal de estados (1–8 semanas) | **Poisson de huracanes** (HURDAT2 1851–2025) + **Monte Carlo** mensual → escenarios malo/probable/bueno con probabilidad; sensibilidad | — | — |
| **IO** | Etapa 2 (recurso): **variables binarias** de activación semanal | Etapa 1: **programación estocástica de dos etapas** (presupuesto por mes × destino × canal) | Ejecuta la etapa 2 cuando ocurre el evento | — |
| **Marketing** | "Dónde": destinos con espacio | "Cuándo": calendario de temporada baja | "Ahora": reglas de encender/pausar anuncios; KPIs en vivo | Buyer persona, branding, medios, piezas, implementación, KPIs |

**Límites que evitan el encimamiento:**
- Markov (A1) solo trabaja en **semanas** (hasta 8). Monte Carlo (A3) solo trabaja en **meses** (1 a 12).
- El clasificador (A1) predice **un estado** (categoría). El pronóstico (A3) predice **un nivel** (número con rango).
- Un **solo** modelo de IO con dos etapas. A1 no tiene un optimizador propio: sus variables binarias son la etapa 2 del modelo de A3.
- A5 **no entrena modelos**: reproduce datos reales, detecta anomalías y ejecuta reglas.

## B.3 Qué preguntas del PP responde cada módulo
| Pregunta | Dueño |
|---|---|
| 1 Patrones temporales, espaciales y de comportamiento | A1 (espacial), A3 (temporal), Campaña (comportamiento: reseñas y nacionalidad) |
| 2 Variables relacionadas con la saturación | A1 (importancia de variables del clasificador) |
| 3 Demanda futura con incertidumbre | A3 |
| 4 Escenarios de redistribución | A3 (IO + escenarios) |
| 5 Características para recomendar destinos | Campaña (persona) + A1 (dónde hay espacio) |
| 6 Impacto en comunidades y destinos saturados | A1 (turistas por residente) + A5 (monitoreo) |
| 7 Evaluar viabilidad, sustentabilidad y efectividad | A5 (KPIs en vivo) + A3 (comparación de escenarios) |

---

## B.4 Datos: exactamente qué tomamos, de dónde y para qué (todo verificado el 26–27 de septiembre de 2026)

| ID | Fuente oficial y URL | Qué campos / periodo | Verificación | Módulo |
|---|---|---|---|---|
| D1 | **SITUR-Q** API `returq.siturq.gob.mx/api/charts/getCharData` (token público incrustado en `siturq.gob.mx/indicadores-turisticos`) | 45 indicadores; destinos: Cancún, Isla Mujeres, Costa Mujeres, Puerto Morelos, Holbox, Cozumel, Riviera Maya, Playa del Carmen, Tulum, Maya Ka'an, Gran Costa Maya (Chetumal, Mahahual, Bacalar) | Consultas reales hechas: ver tabla D1-detalle | A1, A3, A5 |
| D2 | **DataTur ocupación semanal** `datatur.sectur.gob.mx/Documentoscompartidos/monitoreo/AAAA_Semana_NN.zip` | 135 semanas (2024-S01 → 2026-S31); campos `Centro, Cuartos disponibles promedio diario, Cuartos ocupados promedio, Ocupación`; **7 centros de Q. Roo**: Cancún, Cozumel, Isla Mujeres, Riviera Maya, Akumal, Playa del Carmen, Playacar (+ ~47 del país) | Abierto el archivo 2026-S31 | A1, A5 |
| D2m | DataTur ocupación **mensual** `…/monitoreo/AAAA-MES_NN_Publico.zip` | 31 meses (2024-01 → 2026-07), 54 centros del país | Listado y descarga 200 | A1 (clustering nacional), A3 |
| D3 | **DataTur BD_Nacionalidad** `…/upm/BD_Nacionalidad.zip` | **~521,364 filas**; `Año, Fecha, Mes, Aeropuerto, Origen (continente), País, Sexo, Valor`; aeropuertos Cancún, Cozumel, Chetumal y Tulum | Descargado y leído | Campaña (persona), A3 (variable) |
| D4 | DataTur **BdINAH** (3.1 MB), **DB_AFAC** (0.7 MB), **BaseDatosCruceros** (0.2 MB), **Compendio 2024** (31.3 MB) | Visitas a zonas arqueológicas (Tulum, Cobá vs Kohunlich, Chacchoben, Dzibanché, Oxtankah); tráfico aéreo; cruceros por puerto | HTTP 200 | A1 (presión), A3 |
| D5 | **Rest-Mex 2025** `huggingface.co/datasets/vg055/Rest-Mex2025` (CC-BY-4.0) | 208,051 reseñas; Q. Roo **85,993** (Tulum 45,345 · Isla Mujeres 29,826 · Bacalar 10,822); `Title, Review, Polarity 1–5, Town, Region, Type` | API de HuggingFace | Campaña (minería de texto) |
| D6 | **DENUE INEGI** `inegi.org.mx/contenidos/masiva/denue/denue_NN_csv.zip` (32 estados) | Establecimientos con SCIAN, municipio, **lat/lon**; volumen nacional para Spark | HTTP 200 (Q. Roo 5.9 MB, CDMX 45.4 MB…) | A1 (oferta), Big Data |
| D7 | **Censo 2020 ITER** Q. Roo `…/ccpv/2020/datosabiertos/iter/iter_23_cpv2020_csv.zip` | Población por localidad | HTTP 200 (270 KB) | A1 (turistas por residente) |
| D8 | **Open-Meteo archivo** `archive-api.open-meteo.com/v1/archive` | Horario 2019→2026 (temperatura, lluvia, viento) en 8 puntos; diario desde 1950 | HTTP 200 | A3 (variable exógena), A5 (flujo horario) |
| D9 | **HURDAT2** NOAA `nhc.noaa.gov/data/hurdat/hurdat2-1851-2025-*.txt` | Todas las tormentas del Atlántico 1851–2025 | HTTP 200 | A3 (Poisson) |
| D10 | **FRED** `fred.stlouisfed.org/graph/fredgraph.csv?id=DEXMXUS` y `CPIAUCSL` | Peso-dólar diario; inflación EE. UU. | CSV responde | A3 (sensibilidad), deflactar |
| D11 | **ENDUTIH 2025** INEGI (PDF de resultados) | Uso de internet y redes sociales | HTTP 200 (2.0 MB) | Campaña (hábitos digitales) |
| D12 | **GeoJSON Q. Roo** (PhantomInsights/mexico-geojson) | Polígonos | HTTP 200 (1.5 MB) | Mapas |
| D13 | **Benchmarks de costo por canal** WordStream 2025 / LocaliQ 2026 | Costo por clic, CTR, conversión del sector viajes | Páginas responden con navegador; los valores se leen juntos en la Fase 1, con captura | IO (costos). Son **de EE. UU.**: se etiquetan como supuesto |
| D14 | `DESIGN.md` (Escritorio) | Tokens y componentes | En disco | Front |

**D1-detalle: qué sí y qué no trae SITUR-Q (consultas reales del 27-sep-2026, Gran Costa Maya y sub-destinos)**
| Indicador | 2024 | 2025 | 2026 | Uso |
|---|---|---|---|---|
| Ocupación hotelera (Bacalar, Chetumal) | 12 meses (p. ej. Bacalar ene-2024 66.5 %; Chetumal 58.0 %) | **ceros = hueco** | vacío | A1/A3 con historia hasta dic-2024 |
| Habitaciones (capacidad) | 12 | 12 | ene–jul | A1 (capacidad), IO (restricción) |
| Centros de hospedaje (Bacalar 145 en 2025) | ✓ | ✓ | ✓ | A1 |
| Cruceristas | 12 | 12 | ene–jul | A1, A3, A5 |
| Cruces frontera México–Belice | 12 | 12 | ene–jun | A1, A3, A5 |
| Tren Maya, movimiento de pasajeros | ✓ | 12 (ene-2025: 14,437) | ene–jul (ene-2026: 19,780) | A1, A3, A5 |
| Afluencia de turistas / derrama (sur) | solo ene–mar | vacío | vacío | **Hueco**: en la Fase 1 se reintenta con "Exportar Excel"; si no aparece, se declara |

**Excluido porque no se pudo confirmar:** microdatos EVI (acceso restringido), ENGATUR, microdatos ENDUTIH,
OSM/Overpass (respondió 406; DENUE lo sustituye), serie de sargazo, Google Trends, TripAdvisor/Google.

**Consecuencia honesta para el sur:** no existe ocupación oficial del sur en 2025–2026. Por eso:
(1) el Radar del sur usa **presión de llegada medida** (cruceristas + Tren Maya + cruces de Belice por
habitación disponible y por residente) y **muestra "sin dato oficial"** donde falta la ocupación;
(2) el Pronóstico del sur trabaja sobre las series **medidas** (llegadas y capacidad) y, si decidimos pronosticar
ocupación, se entrena con 2019–2024, se valida con 2024 como prueba ciega y se etiqueta `_est`. **Esta decisión
la tomamos juntos en la Fase 3.**

---

## B.5 La página: fusionada sin saturar (DESIGN.md + público no técnico)

**Reglas anti-saturación**
- Cada sección responde **una** pregunta y tiene **una** visualización principal, **máximo 3 cifras** y **una frase**.
- El detalle técnico vive detrás de un botón **"¿Cómo lo sabemos?"** (panel desplegable), nunca en primer plano.
- La parte oscura usa **pestañas**: se ve un solo tablero a la vez.
- Máximo 4 tarjetas flotantes a la vez; el color siempre va acompañado de un ícono y un texto (accesibilidad).
- Lenguaje: "tranquilo / concurrido / saturado", "escenario malo / probable / bueno", "8 de cada 10".

**Recorrido (de blanco a índigo, como en el DESIGN.md)**

| # | Sección | Módulo | Qué ve un no técnico | Componente del DESIGN.md |
|---|---|---|---|---|
| 0 | Barra de anuncio | A5 | "Esta semana: Cancún concurrido · Bacalar con espacio · Ver en vivo →" | Announcement Bar índigo |
| 1 | Portada | A5 (datos) | Titular de 56 px + teléfono con **tarjetas flotantes** que llegan desde la API ("Tulum: saturado esta semana") | Hero + Floating Notification Cards |
| 2 | ¿Dónde hay espacio hoy? | **A1** | Mapa de Q. Roo con 3 colores e íconos; tocar un destino abre una tarjeta con 3 datos | Card + mapa |
| 3 | ¿Cuándo conviene ir? | **A3** | Calendario de 12 meses tipo app del clima: "marzo en Bacalar: 8 de 10 probabilidades de encontrar espacio" | Cards en rejilla |
| 4 | La campaña | Campaña | Buyer persona, marca, mensajes y piezas; botón azul "Planear mi viaje" | Primary Blue Button |
| — | *Transición a índigo: "La torre de control"* | | | Section Divider Band |
| 5 | Pestaña **En vivo** | **A5** | Reproductor semana a semana (2024-S01 → 2026-S31): el radar cambia de color y aparecen las decisiones ("Se pausó el anuncio de Tulum") | Dark cards |
| 6 | Pestaña **Escenarios** | **A3** | Abanico malo/probable/bueno; riesgo de huracán por mes; "¿qué pasa si cambia el dólar?" | Dark cards |
| 7 | Pestaña **Presupuesto** | IO | Controles deslizantes: el backend **resuelve el modelo en vivo** y reparte el dinero | Dark Ghost Button |
| 8 | Pestaña **Evidencia** | Todos | Métricas de los modelos, sesgo, calidad de datos, consola de consulta | Dark cards |
| 9 | Fuentes + descarga | — | Rejilla 4×2 con las fuentes oficiales; botón ámbar "Descargar informe" | Press Logo Cards + Amber Download |

**Tecnología (simple y explicable):** HTML + CSS + JavaScript sin framework; **ECharts** para gráficas y mapa
con GeoJSON; GSAP para animaciones; **EventSource (SSE)** para recibir el flujo en vivo; tipografía
`system-ui`; todo guardado localmente, así que funciona **sin internet** en `localhost`, en celular y en escritorio.

**Backend (FastAPI) — endpoints:**
`/api/radar?semana=` (A1) · `/api/pronostico?destino=` (A3) · `/api/escenarios` (A3) ·
`/api/optimizar` POST (IO, resuelve en vivo) · `/api/stream` SSE (A5) · `/api/campana` (persona, piezas, KPIs) ·
`/api/consulta` (solo lectura, DuckDB sobre Gold) · `/` sirve el front.

---

## B.6 Arquitectura de datos (Big Data, criterio 2)

```
FUENTES OFICIALES (D1–D13)
   │  ingesta reproducible + manifiesto SHA-256
   ▼
BRONZE  datos/bronze/<fuente>/<fecha_descarga>/   (crudo, inmutable)
   │  PySpark: tipado, nombres en español, banderas de calidad, deduplicación
   ▼
SILVER  datos/silver/<tabla>/  Parquet particionado por año
   │  PySpark / Spark SQL: modelo estrella, reconciliación entre fuentes, agregados
   ▼
GOLD    datos/gold/  hechos_semana, hechos_mes, dim_destino, dim_tiempo, resenas_temas, persona_origen…
   ├──► DuckDB (consultas en milisegundos para la API)
   └──► Spark Structured Streaming (A5): lee hechos_semana en orden y emite por ventana → SSE
```
- **Volumen real:** DENUE de 32 estados + ~521 k filas de nacionalidad + 208 k reseñas + 166 archivos DataTur
  + clima horario de 8 puntos (7.7 años) + HURDAT2. Los conteos exactos se registran en la Fase 1.
- **Reconciliación** (incidente de Big Data): Cancún y Riviera Maya aparecen en SITUR-Q y en DataTur → se
  comparan mes a mes y se documenta la diferencia y la regla elegida.
- **Retención y privacidad:** no se guarda ningún dato personal (Rest-Mex no tiene identificadores; D3 viene
  agregado). Se documenta qué se descarta y por qué.

---

## B.7 Plan de ejecución literal, fase por fase

Cada fase se hace con el protocolo A.6. **"Tú decides"** marca los puntos donde eliges.

### Fase 0 — Cimientos (sin datos todavía)
1. Crear `OBJETIVO.md` (Parte A literal), `CLAUDE.md` (reglas de oro + protocolo), `README.md` inicial y
   copia de `DESIGN.md` en `docs/`.
2. Estructura: `datos/{bronze,silver,gold}` · `backend/torre/{base,radar,pronostico,envivo,campana,api}` ·
   `frontend/` · `notebooks/` · `docs/decisiones/` · `tests/`.
3. Entorno: venv de Python 3.11; instalar **JDK 17** (winget `Microsoft.OpenJDK.17`), **pyspark 3.5.6**,
   **winutils/hadoop.dll 3.3.6** (`HADOOP_HOME`), pandas, pyarrow, duckdb, scikit-learn, statsmodels, scipy,
   PuLP, mlxtend, fastapi, uvicorn. Versiones fijadas en `requirements.txt`.
4. **Gate:** Spark lee un CSV y escribe Parquet en Windows. Si falla → respaldo con contenedor Docker de Spark 3.5.
- **Tú decides:** el nombre del proyecto y del paquete (propuesta: "Torre del Caribe", paquete `torre`).

### Fase 1 — Ingesta (Bronze)
1. `base/ingesta_siturq.py`: obtiene el token público de la página, descarga los indicadores elegidos por
   destino y mes (2019→2026) y guarda JSON crudo.
2. `base/ingesta_datatur.py`: 135 zips semanales + 31 mensuales + Nacionalidad + INAH + AFAC + Cruceros + Compendio.
3. `base/ingesta_restmex.py`, `ingesta_denue.py` (32 estados), `ingesta_iter.py`, `ingesta_clima.py` (8 puntos,
   horario 2019→2026 y diario 1950→2026), `ingesta_huracanes.py`, `ingesta_fred.py`, `ingesta_geo.py`.
4. D13: abrimos juntos las páginas de benchmarks en el navegador, capturamos los valores y los guardamos con captura como evidencia.
5. Manifiesto SHA-256 + tabla con **conteo real de filas por fuente** → `docs/decisiones/01-ingesta.md`.
- **Tú decides:** qué indicadores de SITUR-Q entran (propuesta: ocupación, habitaciones, centros de hospedaje,
  cruceristas, Belice, Tren Maya, aéreos, zonas arqueológicas, afluencia/derrama si aparecen).
- **Gate:** todas las fuentes descargadas y contadas; huecos listados.

### Fase 2 — Almacén y calidad (Silver/Gold con PySpark)
1. Trabajos de Spark por fuente: tipos, nombres en español (snake_case), banderas `_flag`, duplicados.
2. Modelo estrella y agregados en Gold; diccionario de datos generado automáticamente.
3. Reconciliación SITUR-Q vs DataTur (Cancún, Riviera Maya); reporte de calidad.
4. DuckDB apuntando a Gold.
- **Tú decides:** reglas de limpieza (qué se descarta; qué hacer con los ceros de 2025 de SITUR-Q, con la
  propuesta de declararlos hueco).
- **Gate:** pruebas de contrato y de realidad en verde (p. ej. 85,993 reseñas de Q. Roo; Bacalar ene-2024 = 66.5 %).

### Fase 3 — Planteamiento con datos
1. Notebook `01_planteamiento`: variables, actores y relaciones; primeras cifras de concentración.
2. **Tú decides:** **qué destino o ruta promueve la campaña**, partiendo de las 5 regiones vigentes (Parte G:
   Chetumal · Bahía Calderitas–Oxtankah · Ruta arqueológica del sur · Maya Ka'an + Kantemó · Laguna Milagros–Xul-Ha),
   confirmadas con la tabla de criterios D.1 calculada con datos; Cancún, Riviera Maya y Tulum solo como referencia.
3. **Tú decides:** cómo tratar el sur sin ocupación 2025–2026 (presión de llegada medida vs pronóstico `_est`).

### Fase 4 — A1 Radar
1. **Minería:** Índice de Presión Turística = combinación de ocupación (D2/D1), llegadas por habitación
   (D1), turistas por residente (D1+D7), densidad de oferta (D6) y visitas INAH (D4). Pesos definidos
   **contigo**, con análisis de sensibilidad. Clustering jerárquico de los 54 centros (D2m).
2. **ML:** etiquetas tranquilo/concurrido/saturado (umbrales definidos contigo); clasificador (logística vs
   Random Forest vs Gradient Boosting); validación temporal; F1-macro; importancia de variables; **sesgo** entre
   norte (semanal) y sur (mensual).
3. **Estocástico:** matriz de transición de Markov con las 135 semanas → probabilidad de saturación a 1–8 semanas.
4. Salidas en Gold: `radar_estado`, `radar_markov`. Notebook `02_radar`. Nota `04-radar.md`.
- **Gate:** tabla de métricas y modelo elegido con justificación.

### Fase 5 — A3 Pronóstico
1. **Minería:** descomposición STL y fuerza estacional por destino.
2. **ML:** Holt-Winters vs regresión con clima (D8) vs Gradient Boosting con rezagos; backtesting con origen
   móvil; MAPE/MAE; **intervalos conformales al 90 %** con cobertura comprobada.
3. **Estocástico:** probabilidad mensual de huracán (Poisson con D9); Monte Carlo de demanda + choques +
   respuesta a la campaña → escenarios malo/probable/bueno con probabilidad; sensibilidad (dólar D10, lluvia D8,
   respuesta); riesgo de rebasar la capacidad (D1 habitaciones).
4. Salidas: `pronostico_mes`, `escenarios`, `sensibilidad`. Notebook `03_pronostico`, `04_escenarios`.
- **Gate:** la cobertura real del intervalo del 90 % se mide en el backtest y se reporta aunque salga peor.

### Fase 6 — IO (un modelo, dos etapas)
1. **Etapa 1 (A3):** variables `x[mes, destino, canal]` = presupuesto; objetivo: visitantes esperados hacia
   destinos con espacio (o derrama, lo elegimos contigo); restricciones: presupuesto total, capacidad por
   destino-mes, **cero promoción en estado saturado**, piso de equidad por comunidad, topes por canal (D13).
2. **Etapa 2 (A1 + A5):** variables binarias `y[semana, destino]` de activación; si el Radar pasa a
   "saturado" o llega un choque, se pausa y se reasigna.
3. Frontera de Pareto (visitantes vs presión) y precios sombra ("¿cuánto cuesta la regla ambiental?").
4. Notebook `05_optimizacion`. Nota `06-io.md`.
- **Tú decides:** la función objetivo y las restricciones indispensables.

### Fase 7 — A5 Torre en vivo
1. Spark Structured Streaming lee `hechos_semana` en orden cronológico (2024-S01 → 2026-S31) y clima horario;
   ventanas deslizantes.
2. Isolation Forest para anomalías (ocupación semanal y clima).
3. Motor de reglas: compara la semana real con lo esperado (A3) y con el estado (A1), y ejecuta la etapa 2.
4. FastAPI `/api/stream` (SSE). Se etiqueta en pantalla como **"reproducción de datos históricos reales"**.
5. Notebook `06_torre_en_vivo`. Nota `07-envivo.md`.
- **Gate:** la reproducción completa corre sin cortes y cada evento mostrado apunta a su fila de Gold.

### Fase 8 — Campaña (Mercadotecnia)
1. **Minería de texto** (D5): temas, sentimiento por aspecto (multitudes, precio, limpieza, naturaleza, ruido),
   reglas de asociación; comparación Tulum / Isla Mujeres vs Bacalar.
2. **Buyer persona(s):** origen, sexo y temporada por aeropuerto (D3) + qué valora (D5) + hábitos digitales
   (D11). Cada atributo con la etiqueta **dato / derivado / supuesto** y su fuente.
3. Branding (identidad, personalidad, propuesta de valor, posicionamiento, elementos visuales), mensajes con
   el lenguaje real de las reseñas, medios justificados, piezas, implementación, **KPIs** (alcance, interacción,
   conversión, afluencia, presupuesto, efectos económicos, sociales y ambientales; A5 los monitorea).
4. Regla anti-colapso: si el destino promovido pasa a "concurrido", la campaña baja de intensidad; si pasa a "saturado", se pausa.
- **Tú decides:** nombre de la campaña, tono y mensajes.

### Fase 9 — Backend
FastAPI con los endpoints de B.5; pruebas de API; el optimizador responde en menos de 2 s.

### Fase 10 — Front-end
1. Antes de escribir: cargar las guías de diseño; los tokens del `DESIGN.md` van en `:root`.
2. Construir las secciones 0 → 9 en ese orden, **una por sesión contigo**.
3. Prueba de 5 segundos con una persona no técnica por sección.
- **Tú decides:** la estética final de cada sección.

### Fase 11 — Cierre
Notebooks 01–07 narrados; README final (qué, por qué y cómo correr); diccionario de datos; `docs/trazabilidad.md`;
apoyo al informe técnico (mapa sección del informe → archivo); ensayo del coloquio de 15 min con reparto
entre los integrantes.

---

## B.8 Cobertura final de la rúbrica y de los incidentes
| Criterio | Cómo se llega a Excelente |
|---|---|
| 1 Planteamiento | Fase 3: variables, actores y relaciones con cifras |
| 2 Big Data | Lakehouse PySpark + streaming + reconciliación + retención |
| 3 Minería | Índice + clustering (A1), STL (A3), anomalías (A5), texto (Campaña) |
| 4 ML | Clasificador (A1) y pronóstico (A3), cada uno con 3 modelos comparados, métricas y sesgo |
| 5 Estocásticos | Markov (semanas) + Poisson/Monte Carlo (meses) + sensibilidad |
| 6 IO | Programación estocástica de dos etapas, Pareto, precios sombra |
| 7 Marketing | Persona con fuentes, branding, medios, piezas, implementación, KPIs |
| 8 Integración | Estafeta A3 → A1 → A5 → campaña (B.1), visible en la página |
| 9 Propuesta | Escenarios comparados con el equilibrio economía / distribución / ambiente |
| 10 Informe / 11 Coloquio | README, notas de decisión y un recorrido de 15 min por las secciones 0–9 |

| Incidente | Respuesta |
|---|---|
| Estocásticos | Intervalo conformal del 90 %, escenarios con probabilidad, riesgo de rebasar capacidad, sensibilidad, varios destinos vs uno |
| IO | "Óptimo" = compromiso explícito (Pareto); restricción ambiental dura; equidad; qué pasa al mover cada restricción |
| Big Data | Spark batch + streaming, fuentes que no coinciden, retención, privacidad, baja latencia |
| ML | Métricas + sesgo norte/sur y contra destinos con poca huella digital (Bacalar 10,822 vs Tulum 45,345 reseñas) |
| Minería | Licencias limpias, patrones → mensajes y segmentos, eventos raros (huracanes) |
| Marketing | Regla anti-colapso ejecutable y KPIs comunitarios y ambientales |

## B.9 Verificación de extremo a extremo
1. Un comando reconstruye todo: descarga oficial → Bronze → Silver → Gold → modelos → web.
2. `pytest` en verde (contrato y realidad).
3. `localhost:8000` con wifi apagado: el simulador recalcula en el backend; la reproducción en vivo corre completa; las tarjetas coinciden con Gold.
4. Recorrido con navegador (skill `/qa`) en móvil de 390 px y en escritorio, con captura de cada sección.
5. Prueba de 5 segundos con una persona no técnica.
6. Cada cifra visible está en `docs/trazabilidad.md`.

---

# PARTE C — Graphify: el grafo de conocimiento del proyecto

## C.1 Qué es (verificado el 27-sep-2026)
- Paquete `graphifyy` 0.9.70 en PyPI (repo `github.com/Graphify-Labs/graphify`), requiere Python ≥ 3.10.
  Tu Python es **3.11.9 ✓**. **No tienes `uv` ni `pipx`** → se usa la tercera vía: `pip install`.
- `graphify install` registra el skill en Claude Code: escribe una **sección en `CLAUDE.md`** y un hook
  PreToolUse en `.claude/hooks/`.
- `/graphify .` hace: (1) **extracción AST** local con tree-sitter (código, sin API); (2) **pase semántico con
  subagentes de Claude** para documentos, PDFs e imágenes (usa tu sesión de Claude Code, sin llave aparte);
  (3) deduplicación de entidades; (4) **detección de comunidades Leiden**; (5) nombrado de comunidades.
  Salidas en `graphify-out/`: `graph.json`, **`GRAPH_REPORT.md`** (god nodes, conexiones sorprendentes,
  preguntas sugeridas), `graph.html` (visual interactivo), `manifest.json`.
- Extras necesarios: **`[pdf]`** (para leer el PDF del Problema Prototípico y el plan) y **`[leiden]`**
  (comunidades). Sin ellos no falla, pero se pierde esa parte → se instala `graphifyy[pdf,leiden]`.
- `graphify hook install` instala hooks **post-commit / post-checkout** → **requiere repositorio git**.
  **Esta carpeta NO es repositorio git** (verificado) → antes hay que hacer `git init` (**tú decides**).
- Nota honesta: la documentación de Graphify describe `AGENTS.md` como archivo de la plataforma Codex; si
  `graphify-out/AGENTS.md` no aparece tras correrlo en Claude Code, te lo digo tal cual, no lo invento.

## C.2 Cómo "metemos toda la información al grafo"
Graphify construye el grafo **a partir de archivos**. Por eso, antes de correrlo, escribimos juntos los
documentos fuente (así el grafo conecta reglas, datos, módulos, regiones y rúbrica):

| Archivo | Contenido | Nodos que genera |
|---|---|---|
| `OBJETIVO.md` | Parte A literal (prompts, PP, rúbrica, incidentes, protocolo) | Preguntas, criterios, incidentes |
| `CLAUDE.md` | Reglas de oro, reglas de estructura, convenciones, protocolo + sección de Graphify + "leer `GRAPH_REPORT.md` antes de Glob/Grep" | Reglas |
| `docs/plan/PLAN_v3.md` | Este plan (Parte B) | Módulos A1/A3/A5, fases, estafeta |
| `docs/datos/INVENTARIO.md` | D1–D14 con URL, campos, verificación, huecos | Fuentes ↔ módulos |
| `docs/regiones/REGIONES.md` | Parte D (regiones seleccionadas y excluidas con evidencia) | Regiones ↔ datos ↔ campaña |
| `docs/DESIGN.md` | Copia del DESIGN.md | Componentes ↔ secciones de la página |
| `docs/decisiones/00-fundacion.md` | Primera nota de decisión | Decisiones |
| `PROBLEMA PROTOTÍPICO 5°- LCDN-2026-2.pdf` | Fuente oficial (vía extra `[pdf]`) | Requisitos oficiales |

Cada vez que agreguemos código o notas, el hook reconstruye el grafo (parte AST, sin costo) y se re-corre
`/graphify .` cuando cambien documentos.

## C.3 `.graphifyignore` (propuesto)
```
node_modules/
.next/
dist/
build/
.venv/
venv/
__pycache__/
datos/bronze/
datos/silver/
datos/gold/
*.parquet
*.zip
*.xlsx
graphify-out/
frontend/vendor/
nucleo/                      # copia del proyecto anterior: pediste no usar esos flujos
Plan_v2_Campana_QRoo.pdf     # versión vieja del plan
```
Los datos crudos y los Parquet se excluyen porque son pesados y no son conocimiento del proyecto; su
descripción vive en `docs/datos/INVENTARIO.md`. **Tú decides** si `nucleo/` se excluye (propuesta: sí).

## C.4 Pasos exactos (Fase 0-bis, antes de la Fase 1)
1. `git init` en la raíz (con tu permiso).
2. Crear los archivos de C.2.
3. `python -m pip install --user "graphifyy[pdf,leiden]"` → `graphify install` (te aviso que se usó la vía pip).
4. Crear `.graphifyignore` (C.3).
5. Correr `/graphify .` y explicarte en vivo cada etapa (AST → subagentes → Leiden).
6. Leer `graphify-out/GRAPH_REPORT.md` y darte: 5 god nodes, 3 comunidades más grandes, conexiones sorprendentes.
7. `graphify hook install`.
8. Confirmar que existen `graphify-out/GRAPH_REPORT.md`, la sección de Graphify en `CLAUDE.md` y, si aplica,
   `graphify-out/AGENTS.md`.
9. Regla permanente: **antes de cualquier Glob o Grep, leer `graphify-out/GRAPH_REPORT.md`** (va en `CLAUDE.md`
   y en mi memoria).

---

# PARTE D — Regiones de Quintana Roo: cuáles sí y cuáles no (con evidencia de 2026)

## D.1 Criterios de selección (se vuelven una tabla calculada con datos en la Fase 3)
1. **Sargazo:** fuera de la franja en rojo.
2. **Crisis económica o cierres** reportados en 2026.
3. **Saturación:** ocupación o presión de visitantes ya alta.
4. **Fragilidad ambiental o de servicios** (agua, basura, ecosistema).
5. **Hay datos confirmados** para medirla (SITUR-Q, DataTur, INAH, Tren Maya, aeropuerto).

## D.2 Situación 2026 (noticias verificadas)
- **Sargazo récord:** más de **104,700 t** recogidas y se prevén ~130,000 t (+35 % vs 2025); **56 de 140 playas
  en rojo** (agosto); la franja más afectada va **de Tulum a Xcalak** (incluye Mahahual). Solo 5 playas libres.
  [Cadena Política](https://cadenapolitica.com/2026/08/12/sargazo-quintana-roo-2026-record-historico-playas-afectadas/) ·
  [Ámbito](https://www.ambito.com/mexico/lifestyle/56-las-140-playas-del-litoral-quintana-roo-estanm-roja-abundante-presencia-sargazo-agosto-2026-n6308181) ·
  [PorEsto](https://www.poresto.com/quintana-roo/2026/5/16/sargazo-golpea-el-caribe-mexicano-32-playas-afectadas-y-solo-cinco-libres-en-2026.html)
- **Caribe en general:** ocupación de 59.6 % en la semana del 4 al 10 de julio de 2026; quiebran hoteles pequeños.
  [Infobae](https://www.infobae.com/america/agencias/2026/07/14/sargazo-falta-de-vuelos-y-crisis-global-tienen-al-caribe-mexicano-con-ocupacion-del-60/) ·
  [Reportur](https://www.reportur.com/estados-unidos/2026/07/15/qroo-quiebran-muchos-pequenos-hoteles-por-sargazo-y-flojo-mundial/)

## D.3 Regiones EXCLUIDAS como destino a promover
| Región | Motivo 2026 | Evidencia |
|---|---|---|
| **Tulum** | Crisis por sargazo: ventas −60 %, cierres de negocios, ocupación ene–may 69.88 % vs 76.86 % en 2025; conflicto por el Parque del Jaguar | [La Jornada](https://www.jornada.com.mx/noticia/2026/07/16/estados/sargazo-hunde-la-actividad-turistica-en-tulum-ventas-caen-hasta-60-y-cierran-negocios) · [El Quintanarroense](https://elquintanarroense.com.mx/2026/04/17/empresarios-de-tulum-advierten-de-cierres-de-negocios-y-caida-de-visitantes-por-restricciones-en-el-parque-del-jaguar/) |
| **Playa del Carmen, Puerto Morelos** | Sargazo severo; en Puerto Morelos rebasa la limpieza (ocupación 48.9 %) | [Reportur](https://www.reportur.com/mexico/2026/08/11/puerto-morelos-sargazo-rebasa-la-limpieza-de-playas-de-los-hoteles/) |
| **Mahahual y Xcalak** | Dentro de la franja roja Tulum–Xcalak; "situación crítica" según empresarios | [PorEsto](https://www.poresto.com/quintana-roo/2026/5/16/sargazo-golpea-el-caribe-mexicano-32-playas-afectadas-y-solo-cinco-libres-en-2026.html) |
| **Cozumel** | Sin sargazo en la costa oeste, pero **saturado por cruceros**: más de 1 millón de pasajeros en 330 barcos en 59 días; "se declara lleno" | [Reportur](https://www.reportur.com/cruceros/2026/03/15/cozumel-desbordada-con-330-cruceros-en-solo-59-dias/) · [Reportur](https://www.reportur.com/cruceros/2026/02/25/cozumel-se-declara-lleno-por-aeropuerto-cruceros-y-el-ferry/) |
| **Isla Mujeres** | Poco sargazo, pero ocupación de 93.5–95 %; carencias de agua y drenaje en la parte continental | [Quintana Roo Hoy](https://quintanaroohoy.com/quintanaroo/islamujeres/isla-mujeres-ocupacion-hotelera-febrero-2026/) · [Canal 10](https://noticias.canal10.tv/nota/empresarial-turismo/isla-mujeres-mantiene-ocupacion-del-95-por-ciento-en-hoteles-la-isla-llena-de-visitantes-2026-04-16) |
| **Holbox** | "Colapso crónico de infraestructura": basura (más de 90,000 t acumuladas), agua tratada fuera de norma, drenaje obsoleto | [Tribuna de México](https://tribunademexico.com/basura-holbox/) · [Un Mundo Sustentable](https://unmundosustentable.com/noticias/holbox-se-ahoga-fallas-electricas-e-ineficiencia-de-la-capa-afectan-al-turismo/) |
| **Cancún / Costa Mujeres** | Destino saturado de referencia; la zona norte con sargazo excesivo | [Excélsior](https://www.excelsior.com.mx/nacional/sargazo-quintana-roo-record-historico-playas-afectadas-2026) |
| **Bacalar** (condicionada) | Sin sargazo, pero la laguna está en **deterioro ecológico** (estromatolitos, pérdida del color turquesa; turismo +300 % entre 2009 y 2019). Si entra, es solo con tope estricto y sin actividades en la laguna | [UNAM Global](https://unamglobal.unam.mx/global_revista/laguna-bacalar-microbialitos-contaminacion/) · [El Quintanarroense](https://elquintanarroense.com.mx/2025/02/03/en-riesgo-el-color-azul-turquesa-de-la-laguna-de-bacalar/) |

## D.4 Las 5 regiones PROPUESTAS (sin sargazo en rojo, sin saturación y con capacidad)
| # | Región | Por qué sí (2026) | Su problema real (y cómo lo resuelve la campaña) | Datos con que se mide |
|---|---|---|---|---|
| 1 | **Chetumal (ciudad, malecón, Museo de la Cultura Maya)** | Capital en bahía, fuera de la franja de sargazo del mar abierto; 57.9 % de ocupación en 2024 con 632,303 turistas (+0.1 %) → **capacidad ociosa** | **Falta de demanda**: el turismo beliceño cayó hasta 60 % en 2026 → justo lo que la campaña atiende | SITUR-Q Chetumal (ocupación hasta 2024, habitaciones, Belice, Tren Maya), aeropuerto Chetumal (D3), DENUE |
| 2 | **Bahía de Chetumal: Calderitas y Oxtankah** | Litoral de bahía, pesca y gastronomía; Oxtankah es la mayor ciudad prehispánica de la bahía | Poca visibilidad | SITUR-Q Chetumal, INAH Oxtankah (D4), DENUE Calderitas |
| 3 | **Ruta arqueológica del sur: Kohunlich, Dzibanché-Kinichná, Ichkabal** | Tierra adentro (sin sargazo); reabiertas en 2025 con infraestructura nueva (PROMEZA) | Poca afluencia frente a Tulum y Cobá | BdINAH (D4) visitas mensuales, Tren Maya (D1) |
| 4 | **Maya Ka'an interior: Felipe Carrillo Puerto, Laguna de Ocom, Tihosuco, Señor, Chunhuhub** | Turismo comunitario (8 experiencias promovidas por el Estado en 2026), estación del Tren Maya, sin sargazo | Ingreso bajo en 76 comunidades → beneficio comunitario directo | SITUR-Q "Maya Ka'an", Tren Maya, ITER (población), DENUE |
| 5 | **Muyil y canales de Sian Ka'an (lado lagunar)** | Lagunas interiores, recorridos comunitarios de bajo impacto | Cercanía con la crisis de Tulum y reserva frágil → **tope de capacidad estricto** en el modelo de IO | SITUR-Q Maya Ka'an, INAH Muyil (se confirma en la Fase 1), ITER |

**Advertencias honestas**
- No encontré un reporte de sargazo de 2026 específico para la **Bahía de Chetumal**. Se verifica en la Fase 1
  (fuente de monitoreo CEMAS / Red de Monitoreo del Sargazo). Si la bahía resulta afectada, las regiones 1 y 2 se reevalúan.
- Las regiones 2, 3 y 5 no tienen serie hotelera propia en SITUR-Q: se miden con INAH, Tren Maya y DENUE, y la
  ocupación se toma del destino más cercano (Chetumal o Maya Ka'an). Esto se declara.
- La lista es una **propuesta**: en la Fase 3 la confirmamos con una tabla calculada con los 5 criterios de D.1,
  y **tú decides** el destino o la ruta que promueve la campaña.

**Consecuencia para el plan:** la campaña deja de ser "de playa". Se vuelve una **ruta sur–Maya Ka'an de
cultura, bahía, lagunas interiores y comunidad**, que evita el sargazo y la saturación. Eso encaja con la regla
anti-colapso (Marketing) y con el piso de equidad (IO).

---

# PARTE E — Selección final de regiones (decidida por Brandon el 27-sep-2026)

## E.1 Contexto
Brandon pidió mínimo 6 regiones de Quintana Roo sin los problemas de 2026 (sargazo, cierres, saturación).
Se verificó con **datos oficiales del INAH** (DataTur `BdINAH.zip`, descargado el 27-sep-2026; suma de
`Visitantes` por `Nombre` y `Año` con `Estado = Quintana Roo`) y con noticias de 2026. Brandon eligió **8
destinos a promover** y agregó **Cancún y Riviera Maya**.

## E.2 Evidencia INAH (visitantes por año; ene–jul 2026 vs ene–jul 2025)
| Sitio | 2019 | 2024 | 2025 | Var. ene–jul 2026 |
|---|---:|---:|---:|---:|
| Z.A. Tulum (referencia saturada) | 1,996,544 | 1,245,294 | 1,031,443 | **−31.3 %** |
| Z.A. Cobá | 750,113 | 207,812 | 191,815 | −3.7 % |
| Z.A. Chacchoben (92 % extranjeros, crucero) | 176,427 | 195,357 | 237,039 | +1.1 % |
| Z.A. Kohunlich | 42,813 | 6,222 | 21,850 | +13.5 % |
| Z.A. Ichkabal (abrió 2025) | — | — | 38,186 | −27.5 % |
| Z.A. Dzibanché-Kinichná | 21,326 | 945 | 6,592 | +69.2 % |
| Z.A. Oxtankah (95 % nacionales) | 13,772 | 1,603 | 11,017 | −4.6 % |
| Z.A. Muyil (cerrada jun-2024 → reabre 10-feb-2026) | 18,131 | 10,751 | 0 | 13,654 en 2026 |

## E.3 Regiones seleccionadas

**Destinos a promover (8):**
| # | Región | Estado | Condición / riesgo | Cómo se mide |
|---|---|---|---|---|
| 1 | Chetumal (ciudad) | ✅ | 🟡 Vigilar sargazo: detectado por primera vez en el canal Bacalar Chico hacia la bahía (23-sep-2026) | SITUR-Q Chetumal, aeropuerto Chetumal (D3), DENUE |
| 2 | Bahía: Calderitas–Oxtankah | ✅ | 🟡 Mismo riesgo de la bahía | SITUR-Q Chetumal, INAH Oxtankah, DENUE |
| 3 | Ruta arqueológica del sur (Kohunlich, Dzibanché, Ichkabal) | ✅ | Bajo; 66,628 visitantes en 2025, 15× menos que Tulum | INAH, Tren Maya |
| 4 | Maya Ka'an interior + Kantemó (FCP, Ocom, Tihosuco, Señor, Chunhuhub, J. M. Morelos) | ✅ | Pocos datos hoteleros | SITUR-Q "Maya Ka'an", ITER, DENUE |
| 5 | Cobá + Punta Laguna | ✅ | Municipio de Tulum (efecto de imagen); capacidad probada: −74 % vs 2019 | INAH Cobá, DENUE, ITER |
| 6 | Muyil (lado lagunar) | ✅ | Tope estricto (Sian Ka'an) | INAH Muyil, SITUR-Q Maya Ka'an |
| 7 | Laguna Milagros–Xul-Ha | ⚠️ condicionada | Mismo sistema lagunar frágil que Bacalar → tope estricto, sin actividades invasivas | DENUE, ITER (sin serie turística propia: se declara) |
| 8 | Ribera del Río Hondo | ⚠️ con hueco de datos | Sin serie turística propia; producto consolidado por el municipio en 2026 | DENUE, ITER (se declara hueco) |

**Regiones emisoras o de referencia (2), no destinos a promover:**
| Región | Papel | Por qué no se promueve |
|---|---|---|
| Cancún | Origen del público de la campaña y referencia de saturación (DataTur semanal) | Sargazo y saturación en 2026 |
| Riviera Maya (incl. Tulum, Playa) | Origen del público y referencia de saturación | Sargazo en rojo; Tulum −31.3 % en visitas INAH |

**Descartadas:** Chacchoben (92 % crucero), Kantunilkín–Chiquilá (evidencia débil, puerta de Holbox), además de las exclusiones de D.3.

## E.4 Pasos para aplicarlo (al salir del modo plan)
1. Reescribir `docs/regiones/REGIONES.md`: conservar D.1–D.3, reemplazar D.4 por E.2 y E.3 (con fuentes) y
   agregar la advertencia del sargazo en Bacalar Chico.
2. Agregar la decisión a la tabla A.8 de `OBJETIVO.md`.
3. Crear `docs/decisiones/01-regiones.md`: decisión, opciones descartadas, evidencia (cifras INAH + noticias) y
   el papel de Cancún y Riviera Maya como emisoras.
4. Actualizar la Fase 3 del plan (`docs/plan/PLAN_v3.md`): la tabla de criterios se calcula sobre estas 8 + 2.
5. Grafo: `/graphify . --update` (re-extrae solo los documentos cambiados) y volver a correr
   `graphify export obsidian --labels graphify-out/.graphify_labels.json` para que Obsidian muestre las regiones nuevas.
6. Actualizar mi memoria del proyecto con la selección.

**Verificación:** `graphify query "regiones seleccionadas"` debe devolver las 8 + 2; en Obsidian las notas de
Cobá, Muyil, Laguna Milagros y Río Hondo deben aparecer enlazadas; 0 enlaces rotos.

---

# PARTE F — Ecuaciones y "cómo lo resolví" (quinta instrucción, 27-sep-2026)

**Instrucción textual de Brandon (va a `OBJETIVO.md` A.1):**
> OTra cosa que me falto decirte es que tengas las ecuaciones y como lo resolviste porque es un proyecto escolar sabes :)

## F.1 Regla nueva (va a `CLAUDE.md` §1 y a `OBJETIVO.md` A.7)
Todo cálculo, modelo o indicador se entrega con **cinco partes**:
1. **Ecuación** en LaTeX, con cada símbolo definido y con sus unidades.
2. **Supuestos** del modelo y por qué se aceptan.
3. **Cómo se resolvió**: el método (por ejemplo, simplex/branch-and-bound, máxima verosimilitud, conteo), paso a paso.
4. **Ejemplo resuelto a mano** con números reales del proyecto (una fila o un mes), comparado contra el resultado del código.
5. **Dónde está en el código**: archivo y función.

Dónde vive: `docs/metodologia/ECUACIONES.md` (todas las ecuaciones en un solo lugar, una sección por
módulo), un bloque "Ecuaciones y resolución" en cada notebook y la versión resumida en la pestaña
"Evidencia" de la web (con KaTeX local, sin CDN).

## F.2 Ecuaciones previstas por módulo (se validan contigo en su fase)
**Selección de regiones (Fase 3, ya aplicada en la Parte E):**
- Visitantes anuales: $V_{s,a}=\sum_{m=1}^{12}\sum_{t\in\{nac,ext\}} v_{s,a,m,t}$
- Variación interanual del periodo: $\Delta\%=\left(\frac{V_{s,2026}^{ene-jul}}{V_{s,2025}^{ene-jul}}-1\right)\times100$
  (ejemplo: Tulum $\left(\frac{476{,}247}{692{,}946}-1\right)\times100=-31.3\%$)
- Capacidad ociosa probada: $1-\frac{V_{s,2025}}{V_{s,2019}}$ (Cobá: $1-\frac{191{,}815}{750{,}113}=0.744$)

**A1 Radar**
- Índice de Presión Turística: $IPT_{d,t}=\sum_k w_k\,z_{k,d,t}$, con $z=\frac{x-\min}{\max-\min}$ y $\sum w_k=1$
- Ocupación: $O=\frac{\text{cuartos ocupados}}{\text{cuartos disponibles}}$ (nunca promediar porcentajes); turistas por residente $=\frac{T}{P_{ITER}}$
- Clasificador logístico: $P(y=k\mid x)=\frac{e^{\beta_k^\top x}}{\sum_j e^{\beta_j^\top x}}$; métrica $F1_{macro}=\frac1K\sum_k\frac{2P_kR_k}{P_k+R_k}$
- Markov: $\hat p_{ij}=\frac{n_{ij}}{\sum_j n_{ij}}$; pronóstico a $k$ semanas: $\pi_{t+k}=\pi_t P^k$

**A3 Pronóstico**
- Holt-Winters aditivo: $\ell_t=\alpha(y_t-s_{t-m})+(1-\alpha)(\ell_{t-1}+b_{t-1})$,
  $b_t=\beta(\ell_t-\ell_{t-1})+(1-\beta)b_{t-1}$, $s_t=\gamma(y_t-\ell_t)+(1-\gamma)s_{t-m}$
- Error: $MAPE=\frac{100}{n}\sum\left|\frac{y_t-\hat y_t}{y_t}\right|$
- Intervalo conformal al 90 %: $\hat y\pm\hat q_{0.9}$, con $\hat q$ el cuantil $\lceil(n+1)0.9\rceil/n$ de los residuos absolutos de calibración
- Huracanes (Poisson): $\hat\lambda_m=\frac{\#\text{tormentas en el mes }m}{\#\text{años}}$, $P(N_m\ge1)=1-e^{-\hat\lambda_m}$
- Monte Carlo: $\hat\mu=\frac1R\sum_{r=1}^R D^{(r)}$; escenarios malo/probable/bueno = percentiles 10/50/90; riesgo $=\frac1R\sum\mathbb 1[D^{(r)}>C]$

**IO (dos etapas)**
$$\max_{x,y}\ \sum_{m,d,c} r_{d,c}\,x_{m,d,c}+\mathbb E_\xi\big[Q(x,\xi)\big]$$
s. a. $\sum x_{m,d,c}\le B$; $\;$ demanda inducida $\le$ capacidad libre$_{d,m}$; $\;x_{m,d,c}=0$ si el destino está saturado; $\;\sum_{m,c}x_{m,d,c}\ge \phi B$ (piso de equidad); $\;y_{w,d}\in\{0,1\}$ en la etapa 2.
Se resuelve como **equivalente determinista** (un escenario por muestra de Monte Carlo) con PuLP/CBC (simplex + branch-and-bound); se reportan precios sombra $\partial z^*/\partial b_i$ y la frontera de Pareto por $\varepsilon$-restricción.

**A5 Torre en vivo:** Isolation Forest, $s(x)=2^{-\frac{E[h(x)]}{c(n)}}$; regla de pausa: si $IPT_{d,w}>u$ o $s(x)>\tau$ → $y_{w,d}=0$.

**Campaña (texto):** TF-IDF $=tf\cdot\log\frac{N}{df}$; reglas de asociación con soporte, confianza $\frac{sop(A\cup B)}{sop(A)}$ y lift $\frac{conf}{sop(B)}$.

## F.3 Pasos al aplicarlo
1. Agregar la instrucción literal a `OBJETIVO.md` (A.1) y la regla F.1 a `OBJETIVO.md` A.7 y `CLAUDE.md` §1.
2. Crear `docs/metodologia/ECUACIONES.md` con F.2; la sección de selección de regiones va completa, con su ejemplo resuelto y los números INAH reales.
3. Actualizar el grafo (`/graphify . --update`) y re-exportar Obsidian.

---

## B.10 Primeros pasos al aprobar este plan (orden)
1. Crear `OBJETIVO.md` (Parte A literal) y regenerar el PDF del plan (`Plan_v3_Torre_del_Caribe.pdf`).
2. `git init` (con tu permiso) y crear los documentos de C.2 (`CLAUDE.md`, `docs/plan`, `docs/datos`, `docs/regiones`, `docs/DESIGN.md`, nota 00).
3. Instalar Graphify por pip con `[pdf,leiden]`, `.graphifyignore`, `/graphify .`, reporte (god nodes, comunidades, sorpresas), `graphify hook install`, verificación.
4. Esperar tu visto bueno para la Fase 0 (entorno PySpark) y seguir fase por fase.

**Decisiones ya tomadas (27-sep-2026):** `git init` = **sí** (repositorio local, nada se sube) · `nucleo/` =
**excluido del grafo** (sigue en disco).

---

# PARTE G — Foco en 5 regiones (séptima instrucción, 28-sep-2026)

**Reemplaza a la Parte E.3.** Brandon pidió no meter nada con sargazo, cierres o relación con Tulum y enfocarse en 5
regiones. Quedan: **Chetumal · Bahía Calderitas–Oxtankah · Ruta arqueológica del sur (Kohunlich, Dzibanché, Ichkabal)
· Maya Ka'an + Kantemó · Laguna Milagros–Xul-Ha**. Salen Cobá (municipio de Tulum), Muyil (cerrada de jun-2024 a
feb-2026, colinda con Tulum) y Ribera del Río Hondo (sin datos propios). **Cancún, Riviera Maya y Tulum** se usan solo
como referencia etiquetada: nunca se promueven ni aparecen en la portada o en las piezas. El diseño visual de la
página se revisa al final. Detalle: `docs/regiones/REGIONES.md` D.5 y `docs/decisiones/01-regiones.md`.
