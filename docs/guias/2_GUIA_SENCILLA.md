# Guía sencilla: qué hicimos y por qué, sin tecnicismos

Autor: **Brandon Uriel García Sánchez** · UNRC · LCDN 5° semestre 2026-2 · versión del 2 de octubre de 2026.

---

## 1. La idea en 30 segundos

Quintana Roo tiene el Caribe más visitado de México, pero **no todo está lleno**. El norte (Cancún, la Riviera Maya,
Tulum) recibe a casi todos y en 2026 tiene sargazo y saturación. El sur tiene espacio: los cinco lugares de la campaña
tienen el **12.3 %** de la gente del estado, pero reciben el **1.4 %** de los pasajeros de avión.

El proyecto es una **campaña de publicidad hecha con datos**, "**El sur tiene espacio**", que invita a la gente al sur
**sin llenarlo de más**: nunca anuncia un lugar lleno, se pausa sola con mal clima y manda a quien iba al norte hacia
donde hay lugar.

Los cinco lugares: **Chetumal**, **la Bahía de Calderitas y Oxtankah**, **la Ruta de las pirámides** (Kohunlich, Dzibanché
e Ichkabal), **Maya Ka'an** y **la Laguna Milagros**. Cancún y la Riviera Maya solo aparecen como referencia.

---

## 2. Las tres preguntas que contesta el sistema

Piénsalo como el tablero de un aeropuerto, con tres pantallas:

| Pantalla | Pregunta | Ejemplo de respuesta |
|---|---|---|
| **El Radar** | ¿Dónde hay espacio hoy? | "En julio de 2026 los cinco lugares del sur están tranquilos; Cancún, concurrido" |
| **El Pronóstico** | ¿Cuándo conviene ir? | "En enero la Ruta recibe 61 % más gente que un mes normal; mejor ir en noviembre" |
| **La Torre** | ¿Qué hace la campaña esta semana? | "Esta semana pasa una tormenta: se pausa el anuncio y el dinero se guarda" |

Y encima de las tres, **la campaña**: a quién le habla, con qué palabras y por qué medio.

---

## 3. Las preguntas que te pueden hacer primero

### ¿Por qué aparece "Claude" en el proyecto?
Porque el proyecto se hizo con la ayuda de un **asistente de programación con inteligencia artificial** (Claude Code).
Por eso cada cambio guardado en el historial dice "Co-Authored-By: Claude" y existe un archivo `CLAUDE.md`, que tiene las
**reglas que tú le pusiste** al asistente: no inventar datos, ir fase por fase y que tú decides.

Lo que es tuyo y se puede comprobar: **elegiste en cada punto importante**. Hay más de 40 decisiones registradas con tus
palabras, las opciones que se descartaron y la razón (documento 3).

**Mi consejo: dilo tú primero.** Algo como: *"Usé un asistente de programación con IA como herramienta; las decisiones
son mías y están documentadas, y puedo explicar cada parte."* Revisa qué dice tu profesor o la UNRC sobre usar IA.

### ¿Por qué hay tantos archivos de código?
Porque cada archivo hace **una sola cosa**, como los cajones de un taller: uno descarga, otro limpia, otro calcula.
Así cada pieza se puede revisar y probar por separado. Son 55 archivos en 7 cajones:

| Cajón | Qué guarda |
|---|---|
| `base` | Descargar los datos oficiales y limpiarlos |
| `radar` | Medir dónde hay presión |
| `pronostico` | Predecir los próximos 12 meses |
| `campana` | Repartir el dinero, la marca y los mensajes |
| `envivo` | La Torre de cada semana |
| `api` | Lo que alimenta la página web |
| `documento` | Los PDF y las gráficas |

Los **notebooks** (6) cuentan la historia paso a paso y usan esos cajones. Las **pruebas** (276) revisan solas que las
cifras sigan siendo correctas.

### ¿Dónde está cada materia (UCA)?

| Materia | Qué se hizo, en una frase |
|---|---|
| Grandes volúmenes de datos | Se juntaron 8.1 millones de registros oficiales y se limpiaron con Spark |
| Minería de datos | Se encontraron patrones: qué meses se llenan, qué molesta a los turistas, qué semanas tienen clima raro |
| Aprendizaje de máquina | Modelos que predicen el estado del mes siguiente y los visitantes de los próximos 12 meses |
| Procesos estocásticos | Probabilidades: de tormenta, de que se llene un lugar y escenarios malo, probable y bueno |
| Investigación de Operaciones | Un modelo que reparte el dinero de la campaña de la mejor forma posible |
| Mercadotecnia digital | Las viajeras ideales, la marca, los anuncios y cómo se mide si funciona |

---

## 4. Los datos: de dónde salen

Todo sale de **fuentes oficiales**, descargadas con programas (no a mano) y guardadas sin tocar. Las principales:
- **SITUR-Q** (el sistema de turismo del estado): ocupación, Tren Maya, cruceros y cruces desde Belice.
- **SECTUR / DataTur:** la ocupación hotelera de cada semana, las visitas a las zonas arqueológicas (INAH) y de qué país
  vienen los extranjeros que llegan en avión.
- **INEGI:** los 6.1 millones de negocios del país (DENUE), el Censo 2020 y la encuesta de uso de internet (ENDUTIH).
- **NOAA:** todas las tormentas del Atlántico desde 1851.
- **Open-Meteo:** el clima de cada día desde 1950.
- **Rest-Mex:** 208,051 opiniones de turistas.

**Regla de oro:** si un dato no existe, **no se inventa**; se dice "sin dato". Ejemplo: desde 2025 el estado no publica
la ocupación de los hoteles del sur, y la página lo dice así.

---

## 5. Cómo se hizo, materia por materia

### Grandes volúmenes: tres cajas
Los datos pasan por tres cajas, como el agua por un filtro:
1. **Caja de bronce:** los archivos tal como llegan. Nunca se tocan, y cada uno tiene una "huella digital" que avisa si
   alguien lo cambia.
2. **Caja de plata:** los datos limpios y ordenados.
3. **Caja de oro:** los resultados de los modelos, listos para la página.

**¿Qué es Spark?** Un programa que reparte el trabajo entre los núcleos de la computadora, como si diez personas
limpiaran una lista enorme al mismo tiempo en lugar de una sola. Limpió, por ejemplo, los 6.1 millones de negocios del
país.

**Un detalle importante:** cero no siempre es cero. Si los cuatro aeropuertos dicen "0 pasajeros" todo 2025, no es que
nadie volara: es que dejaron de publicar. Eso se marca como **dato faltante**, no como cero.

**Cuando dos fuentes no coinciden:** el estado y la federación cuentan distinto a los cruceristas (en Mahahual el estado
cuenta entre 11 % y 35 % más). Se escoge una fuente por lugar y la diferencia se declara.

### Minería: encontrar patrones
- **¿Qué tan concentrado está el turismo?** Cancún recibe 92.5 % de los pasajeros de avión del estado; Chetumal, 1.4 %.
- **¿Qué meses se llenan?** La Ruta recibe en enero 61 % más gente que un mes promedio, y en septiembre la mitad.
- **¿Qué lugar está más presionado?** Un índice de 0 a 1 combina la gente que llega (en tren, en crucero, a las ruinas)
  por cada mil habitantes y los cuartos ocupados. Con él, cada lugar queda **tranquilo, concurrido o saturado**.
- **¿Qué semanas tienen clima raro?** Un modelo (Isolation Forest) aprende cómo es una semana normal y marca las raras.
  Marcó las tres semanas de tormenta sin que nadie le dijera que hubo tormenta.
- **¿Qué molesta al turista?** En 85,987 opiniones, las que hablan de **ruido** son malas 2.8 veces más seguido; las que
  hablan de **calma**, menos de la mitad de lo normal. Eso es justo lo que el sur ofrece.

### Aprendizaje de máquina: predecir
- **¿Cómo estará cada lugar el mes que entra?** El modelo acertó 130 de 156 meses que nunca había visto. "Igual que este
  mes" acierta 126, así que el modelo ayuda poco, pero anticipa 8 cambios que la regla simple no ve. Así se dice, sin
  exagerar.
- **¿Cuánta gente llegará en los próximos 12 meses?** Se probaron 5 formas de predecir y se eligió la de menor error. Por
  ejemplo, para la Bahía en diciembre de 2026 se esperan **1,311 visitantes, muy probablemente entre 959 y 1,793**.
- **¿Cómo se sabe que funciona?** Se "viajó al pasado": se predijo cada mes usando solo lo que se sabía entonces y se
  comparó con lo que pasó. El rango acertó entre 80 y 94 de cada 100 veces.

### Procesos estocásticos: las probabilidades
- **Tormentas:** en 60 años hubo 31 tormentas que pegaron al sur. En agosto hay **13.9 %** de probabilidad de una; de
  diciembre a abril, **0 %**.
- **Escenarios:** la computadora imagina **10,000 años posibles** y de ahí sale un escenario malo, uno probable y uno
  bueno. Para la Ruta: 55,811, 62,212 y 73,884 visitantes al año.
- **¿Se va a llenar Cancún?** Si esta semana está concurrido, hay 6.9 % de probabilidad de que la siguiente esté
  saturado.

### Investigación de Operaciones: repartir el dinero
Con un presupuesto supuesto de **$250,000 al año**, un modelo decide cuánto dinero va a cada lugar, cada mes y cada red
(Google o Facebook), para traer a la mayor cantidad de gente **sin anunciar en temporada alta ni llenar ningún lugar**.

- **Resultado:** unos **957 visitantes más** en 9 meses, a **$196 cada uno**. La Ruta recibe 41.5 % del dinero, la Bahía
  36.9 % y Chetumal 21.6 %.
- **¿Por qué 70 % en Facebook?** Por cada $1,000 trae 6.6 visitantes, contra 1.6 de Google. Se le puso un tope de 70 %
  para no depender de una sola plataforma.
- **El hallazgo más bonito:** las reglas de cuidado (no anunciar en temporada alta, no llenar, repartir entre los tres
  lugares) **no le cuestan ni un visitante** a la campaña.

### La Torre: cada semana
Se revivieron **239 semanas reales** como si llegaran una por una. Si había tormenta, clima raro o llegó más gente de la
esperada, el anuncio de ese lugar se pausaba y el dinero se guardaba para la siguiente semana buena. Se pausó 48 veces y
no se perdió ni un peso.

### Mercadotecnia: la campaña
- **Dos viajeras ideales:** "La que vuelve al sur" (mexicana: el 95 % de quienes visitan Oxtankah) y "La que baja del
  norte" (de Estados Unidos o Canadá, que ya está en Cancún, adonde llegaron 9.4 millones de extranjeros; a Chetumal
  llegaron 250).
- **Marca:** "El sur tiene espacio". Su tono es cercano, orgulloso de lo maya y lo mexicano, y aventurero.
- **Anuncios:** cinco, cada uno con el dato que lo respalda. No prometen precios ni tiempos de viaje porque no hay dato.
- **Cómo se mide:** 10 indicadores, por ejemplo costo por visitante de $196 o menos y cero anuncios en semanas de mal
  clima.

---

## 6. Lo que no se pudo medir (y se dice)
- La ocupación de los hoteles del sur desde 2025.
- De qué estado viene el turista mexicano, su edad y su ingreso.
- Cuántas personas compran después de ver un anuncio en Facebook de turismo.
- Las tormentas de 2026 (todavía no se publican).
- Opiniones de turistas sobre los cinco lugares.
- Una prueba de la página con personas reales.

---

## 7. Si solo puedes recordar cinco cifras
1. **12.3 % contra 1.4 %:** la gente del sur contra los pasajeros de avión que recibe.
2. **15.5 veces:** Tulum recibe 15.5 veces más visitantes que las pirámides del sur.
3. **957 visitantes por $187,500:** lo que trae la campaña en 9 meses.
4. **0 visitantes:** lo que cuestan las reglas de cuidado.
5. **250 extranjeros:** los que llegaron en avión a Chetumal en 2025, contra 9.4 millones a Cancún.
