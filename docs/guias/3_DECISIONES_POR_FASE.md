# Las decisiones del proyecto, fase por fase

Autor: **Brandon Uriel García Sánchez** · UNRC · LCDN 5° semestre 2026-2 · del 26 de septiembre al 2 de octubre de 2026.

---

## Cómo leer este documento

El proyecto se hizo en **12 fases (0 a 11)**, una a la vez. En cada punto donde había que elegir se siguió el mismo
protocolo:
1. Se explicó qué había que decidir y **con qué cifra real**.
2. Se presentaron **2 o 3 opciones** con pros y contras.
3. **Brandon eligió.**
4. La decisión quedó escrita con sus palabras, las opciones descartadas, la evidencia y la consecuencia.

Fuentes de este documento: las **25 notas** de `docs/decisiones/` (00 a 24) y los **registros de decisión** de
`OBJETIVO.md` (sección A.8). Las citas entre comillas son las palabras textuales de Brandon.

Cada fase trae también **los errores que se encontraron y cómo se corrigieron**. Son parte del valor del proyecto:
muestran que las cifras se revisaron y no se aceptaron a ciegas.

### Resumen

| Fase | Qué se hizo | Fechas | Estado | Nota |
|---|---|---|---|---|
| 0 | Plan, reglas y computadora lista (Spark) | 26–27 sep | Cerrada | 00, 02 |
| 1 | Descargar los datos oficiales | 27–28 sep | Cerrada | 03 |
| 2 | Limpiar y ordenar los datos | 28 sep – 2 oct | Cerrada | 04, 10, 18 |
| 3 | Elegir y medir los 5 lugares | 28 sep | Cerrada | 01, 05 |
| 4 | El Radar | 28–29 sep | Cerrada | 08, 09 |
| 5 | El Pronóstico | 30 sep – 1 oct | Cerrada | 11, 12, 15 |
| 6 | Repartir el presupuesto | 2 oct | Lista | 19 |
| 7 | La Torre en vivo | 2 oct | Lista | 20 |
| 8 | La campaña | 2 oct | Lista | 21 |
| 9 | Conectar la página con los modelos | 2 oct | Lista | 22 |
| 10 | Página final | 2 oct | Lista (sin prueba con personas) | 23 |
| 11 | Cierre y coloquio | 2 oct | Lista | 24 |
| — | La página web (en paralelo a todas) | 28 sep – 2 oct | En línea | 06, 07, 12–17 |

---

## Fase 0 — El plan, las reglas y la computadora

**Qué se buscaba:** decidir qué proyecto hacer, con qué reglas, y dejar la computadora lista para procesar millones de
datos.

| Decisión | Lo que eligió Brandon | Lo que se descartó y por qué |
|---|---|---|
| Estado | **Quintana Roo** | — |
| Empezar de cero | "Quiero que armemos desde 0 todos los sistemas que consultaste esos no me gustaron" | Reutilizar el proyecto anterior (`cauce`): Brandon no aprobó sus flujos |
| Qué alternativa | **Fusión A1 Radar + A3 Pronóstico + A5 Torre en vivo**: "A5 A1 y A3 como podemos fucionarlo dame el plan donde no se encimen" | A2 (voz del viajero) y A4 (portafolio) como ejes; la minería de texto de A2 se conservó para la campaña |
| Forma de trabajar | "necesitamos que lo desarrolles CONMIGO Y NO VIBEDEES TODO SIN SABER COMO CAJA NEGRO" | Programar todo de golpe |
| Ecuaciones | "que tengas las ecuaciones y como lo resolviste porque es un proyecto escolar sabes :)" → `ECUACIONES.md` | — |
| Herramientas | Repositorio git, mapa del proyecto (Graphify) | — |
| Computadora | Entorno propio con **PySpark 3.5.6 + Java 17 + winutils 3.3.6** | Spark en Docker (pesado de explicar en el coloquio); cambiar el Java de todo Windows (podía romper otros programas) |

**Evidencia:** la prueba de humo leyó un CSV de 3 filas con Spark, escribió Parquet y la suma dio 6, la esperada.

**Por qué no playa:** desde el inicio se decidió no promover destinos de playa en 2026. Había sargazo récord (más de
104,700 toneladas; 56 de 140 playas en rojo), una crisis en Tulum (ventas −60 %) y Cozumel estaba saturado por cruceros.

---

## Fase 1 — Descargar los datos oficiales (Bronze)

**Qué se buscaba:** bajar todas las fuentes con código reproducible, sin modificarlas, y contar sus registros.

| Decisión | Lo que se eligió | Lo que se descartó y por qué |
|---|---|---|
| Cómo descargar | Programas que guardan cada archivo con su huella SHA-256 | Exportar a mano desde las páginas: no se puede repetir |
| DENUE | **Los 32 estados** (6.1 millones de negocios) | Solo Quintana Roo: la rúbrica pide volumen real |
| Limpiar al descargar | No: Bronze idéntico a la fuente | Limpiar al vuelo: se pierde el original |
| Costos de anuncios (D13) | Leer las tablas con un navegador automatizado y guardar captura | Copiar cifras de resúmenes web (uno decía CTR 8.24 %; la tabla oficial dice 8.73 %) |
| Sargazo en la bahía | Guardar como evidencia las publicaciones públicas (ECOSUR) | Extraer el semáforo de Facebook: lo prohíben sus términos |

**Resultado:** **353 archivos, 8,134,802 registros, 824 MB.**

**Hallazgo que cambió el plan:** SITUR-Q no publica ocupación hotelera de 2025–2026 para **ningún** destino. Para esos
años, solo existe la ocupación semanal de DataTur, y solo para 7 centros del norte.

**Errores encontrados y corregidos:**
- El conteo del DENUE sumaba el diccionario de datos de cada zip como si fueran negocios: 6,139,989 en lugar de
  6,138,075. Spark y un lector independiente dieron la cifra correcta; se corrigió la función y el manifiesto.
- El Censo contaba un catálogo como localidades: 2,257 en lugar de **2,243**.
- La API de SITUR-Q rechazaba las peticiones; se resolvió enviando los mismos encabezados que el navegador.
- Open-Meteo respondía "demasiadas peticiones"; se pidió un año por consulta, con espera y reintento.

---

## Fase 2 — Limpiar y ordenar los datos (Silver y Gold)

**Qué se buscaba:** convertir 14 fuentes distintas en tablas limpias, con las mismas reglas, y dejarlas consultables.

| Decisión | Lo que eligió Brandon | Lo que se descartó y por qué |
|---|---|---|
| La página | **Construirla en paralelo** a los datos, desde la Fase 2 | Esperar al final |
| Oferta turística | Giros SCIAN característicos del turismo (721, 722, 5615, 487, 712, 713) | — |
| Tren Maya | Sumar las estaciones de cada destino (cuadra exacto con el total de zona) | — |
| Ceros imposibles | **Hueco, no cero** (ocupación con 0 cuartos; los 4 aeropuertos en 0 todo 2025) | Conservar los ceros: la página diría "0 pasajeros en avión en 2025" |
| Tormenta que afecta al sur | **≤ 200 km de Chetumal, viento ≥ 34 nudos, desde 1966** (31 eventos en 60 años) | 100 km (muy pocos eventos), 300 km (mete tormentas lejanas), desde 1851 (antes de los satélites se perdían tormentas) |
| Feriados sin tipo de cambio | **Se quedan vacíos** | Copiar el día anterior: inventa una cotización |
| AFAC: dos aerolíneas con la misma etiqueta | **Sumarlas** (Virgin America + Alaska, 25 casos; 0.035 % de los pasajeros) | Dos renglones marcados; dejar AFAC fuera |
| Base de consulta | **DuckDB** con modelo estrella, sin servidor | PostgreSQL: exige un servidor y el proyecto debe correr sin internet |

**Hallazgos:**
- DataTur y SITUR-Q no miden lo mismo: en Isla Mujeres hay 19.3 puntos de diferencia. **Regla:** una fuente por lugar
  y la diferencia se declara.
- Las noticias decían que Isla Mujeres estaba al 93.5–95 %, pero DataTur registra 74.7 % y 43.2 %. Regla: el dato
  oficial va antes que la nota de prensa.
- Al aeropuerto de Chetumal llegaron **250 extranjeros** en 2025; a Cancún, 9.4 millones.
- En Mahahual, SITUR-Q cuenta siempre entre 11 % y 35 % más cruceristas que DataTur.

**Errores encontrados y corregidos:**
- La afluencia y la derrama de SITUR-Q parecían llegar hasta junio de 2024 por unos ceros. En realidad terminan en
  marzo de 2024.
- El archivo de huracanes trae dos líneas mal escritas. Una no dice si la latitud es norte o sur: se dejó vacía, no se
  adivinó. La primera exploración se saltaba esa línea sin avisar; el código final se detiene si no entiende una línea.
- El INAH traía repetido el bloque de extranjeros de septiembre de 2025, una copia con cifras y otra en ceros. Se
  conservó la de cifras.
- **Revisión del 2 de octubre:** el diccionario de datos se detuvo porque 12 tablas nuevas no tenían descripción. Se
  completaron; hoy son 56 tablas.

**Por qué se cerró hasta el final:** las Fases 3 y 4 avanzaron con las fuentes ya limpias. Las demás se limpiaron justo
antes de la fase que las usaba (clima y huracanes antes del Pronóstico; reseñas y nacionalidades antes de la campaña).

---

## Fase 3 — Elegir y medir los 5 lugares

**Qué se buscaba:** decidir qué lugares promover, con criterios medidos, y plantear el problema con datos.

| Decisión | Lo que eligió Brandon | Lo que se descartó y por qué |
|---|---|---|
| Cuántas regiones | Primero 8; luego **solo 5**: "no meter nada con sargazo, cierres o relación con Tulum" | Cobá (municipio de Tulum), Muyil (cerrada de 2024 a 2026 y colinda con Tulum), Río Hondo (sin datos propios) |
| Las 5 | Chetumal · Bahía Calderitas–Oxtankah · Ruta arqueológica del sur · Maya Ka'an + Kantemó · Laguna Milagros–Xul-Ha | Chacchoben (92 % de crucero), Kantunilkín (puerta de Holbox) |
| El norte | **Solo como referencia**: Cancún, Riviera Maya y Tulum | Quitarlo: se perdería la única ocupación medida de 2025–2026 |
| Población | **Por localidad** del Censo 2020 | Por municipio: 4 de los 5 lugares compartirían el mismo número |
| Cierres | **Pasa si lleva ≥ 12 meses seguidos abierta** y sin cierres en 2026 | "Ningún cierre desde 2024": dejaba solo 3 regiones |
| El sur sin ocupación | **Medir la presión de llegada** (Tren Maya, Belice, INAH) y mostrar "sin dato oficial" | Estimar la ocupación con un modelo: sería una cifra inventada donde no hay medición |
| Cuartos del estado | Sumar destinos + zonas (140,664 en julio de 2026) | Sumar destinos + miembros: perdía 36,709 cuartos de la Riviera Maya |

**Resultado:** las 5 regiones pasan los criterios. **La relación central:** tienen el 12.3 % de la gente del estado y
el 14.4 % de sus negocios turísticos, pero el **1.4 %** de los pasajeros de avión, el 1.7 % de los cuartos y el 4.1 %
de los visitantes del INAH.

**Hallazgo honesto:** Kohunlich (+13.5 %) y Dzibanché (+69.2 %) crecen en 2026, pero la Ruta completa bajó 8.2 %
porque Ichkabal cayó. Por eso no se destacan solo las que suben: sería escoger datos a conveniencia.

---

## Fase 4 — El Radar: ¿dónde hay espacio?

**Qué se buscaba:** un índice de presión de 0 a 1 por lugar y mes, estados en palabras (tranquilo, concurrido, saturado)
y una predicción.

| Decisión | Lo que eligió Brandon | Lo que se descartó y por qué |
|---|---|---|
| Pesos del índice | **Iguales**, con sensibilidad de ±50 % | Componentes principales (difícil de explicar, inestable con 19 meses); criterio del equipo (subjetivo) |
| Cortes | **Percentiles comunes a todo el estado** (p50 y p90) | Terciles de cada lugar (todo lugar saldría "saturado" un tercio del tiempo); k-means |
| Predecir | "Con los datos que tenemos inferimos los futuros haciendo ML" | — |
| Escala | **Mín–máx** | Percentil común; logaritmo |
| Cuando falló la prueba de validez | **Opción D:** ocupación de DataTur para 4 lugares del norte y un componente entra solo si lo tienen ≥ 2 lugares | Tres variantes más, comparadas con datos (tabla en la nota 08) |
| Qué índice publicar | **El comparable** (cada lugar con sus mismas medidas en toda su historia) | El índice con todo, que tenía el quiebre de 2025 |
| Elegir modelo | **El que más acierta y más cambios anticipa** | Elegir por F1-macro |
| Markov | **Semanal y solo el norte** | Mensual para todos (se encimaba con el Pronóstico) |
| Auditoría (Brandon: "vuelve a revisar… auditando todo del 1 al 4") | Agregar **llegadas por cuarto** (tren + cruceros), **clustering** de 55 centros (k = 2) y **medir el sesgo** | Densidad de oferta en el índice: es un solo corte en el tiempo |

**La prueba de validez que falló (y por qué es bueno contarlo):** la primera versión calificaba a Cancún "tranquilo" en
julio de 2026, porque SITUR-Q dejó de publicar su ocupación. DataTur decía 68.8 %. El índice se corrigió con datos, no a
ojo.

**Resultado:**
- La regresión logística acierta 130 de 156 meses que nunca vio, contra 126 de "igual que este mes". Anticipa 8 de 30
  cambios.
- La cadena de Markov da mejores probabilidades que la persistencia a 1, 4 y 8 semanas.
- El norte está en el grupo de los destinos más llenos del país.

**Lo que se declara:** el estado se repite el 81 % de los meses, así que el modelo agrega poco. En los 5 lugares casi no
hubo cambios con qué probarlo.

**Errores encontrados y corregidos:**
- La ocupación de SITUR-Q trae 3 filas por mes y el panel las sumaba: la "ocupación" llegaba a 2,560,068. Ahora se
  recalcula ocupados ÷ disponibles, y una prueba lo vigila.
- La serie de "zonas arqueológicas" de SITUR-Q es el mismo dato del INAH agrupado. Usar las dos contaba dos veces a los
  mismos visitantes.

---

## Fase 5 — El Pronóstico: ¿cuándo conviene ir?

**Qué se buscaba:** cuántos visitantes se esperan en cada lugar los próximos 12 meses, con su rango, y la probabilidad de
tormentas y escenarios.

| Decisión | Lo que eligió Brandon | Lo que se descartó y por qué |
|---|---|---|
| Qué pronosticar | **"Medidas + norte":** visitantes INAH (Bahía y Ruta), cruces de Belice (Chetumal) y Cancún como referencia | Solo INAH (Chetumal sin serie); estimar la ocupación del sur |
| Meses cerrados | **"Hueco + forma del año":** cierres, meses parciales y pandemia no entrenan | Solo desde la reapertura (19 meses, pocos); ceros como dato real (temporada falsa) |
| Pandemia en Belice | **Hasta junio de 2022** (de marzo a junio los cruces apenas iban en 65–82 %) | Hasta febrero de 2022 (la recuperación se confundía con temporada) |
| Elegir modelo | **"Menor error con rango ≥ 80 %"** | Menor error sin importar el rango; un solo modelo para todo |
| Golpe de una tormenta | **"Supuesto con barrido":** 0, 25 y 50 % | Solo mostrar la probabilidad |
| Efecto de la campaña en los escenarios | **"No, se ve en la Fase 6"** | Meter un +5 % o +10 % sin fuente |
| Capacidad | **"Capacidad probada":** el mes más alto que cada lugar ya recibió | Cuartos de hotel (se pronostican visitantes, no noches) |

**Decisiones técnicas (presentadas con su razón):**
- Forma del año clásica en lugar de STL, porque las series tienen huecos. STL queda como segunda opinión y coincide.
- Holt-Winters con la forma del año fija, porque desde las reaperturas solo hay 17 a 20 meses seguidos. La variante sin
  tendencia se agregó después de ver que la tendencia pronosticaba −240 visitantes.

**Resultado:**
- La regresión con clima ganó en los tres lugares del sur (Bahía 15.7 % de error, Ruta 21.6 %, Belice 11.0 %).
- El rango del 90 % se cumplió entre 80 y 94 de cada 100 veces.
- Agosto tiene 13.9 % de probabilidad de tormenta, y la probabilidad de al menos una en el año es 40.3 %.
- Las tormentas pesan en el mes, no en el año.

**Lo que se declara:** la Ruta no llega a 90 % de cobertura con ningún modelo (en 2023 las visitas cayeron 10.7 % sin
aviso), y el clima casi no mejora el pronóstico.

### El planeador de viaje (parte de la Fase 5, en la página)
Brandon pidió: *"como si alguien se mete a la página a planear sus vacaciones… y si ve flujos súper altos o temporada
alta le recomiende otra parte… hospedajes… restaurantes… mediante Google Maps y webscraping NLP"*.

| Decisión | Lo que eligió Brandon | Lo que se descartó y por qué |
|---|---|---|
| De dónde salen los lugares | **DENUE + botón de Google Maps** (enlace público) | Scraping de Google Maps (prohibido por sus términos y por la regla 4); API de Google Places (llave con tarjeta, deja de funcionar sin internet) |
| El NLP | **Clasificador por léxico** de nombres y giros | Un modelo estadístico: no hay etiquetas para entrenarlo |
| Temporada alta | **Forma del año ≥ 1.20 o riesgo de capacidad ≥ 10 %** | El semáforo del Radar (es del mes actual) |
| Cancún y Riviera Maya | "Esos dos como no tenemos datos cámbialos por Cancún y Riviera Maya" · "que aparezca, pero si está lleno le recomendamos de manera que sí se vea" | Maya Ka'an y Laguna en el planeador: no tienen serie |
| Temporada alta del norte | **Cortes del Radar** (ocupación ≥ 71.2 %) | — |

**Ajuste al probarlo:** sin la condición de lluvia, el mes sugerido casi siempre era junio, el más lluvioso (195 mm). Se
agregó que el mes sugerido llueva menos que la mediana.

---

## Fase 6 — Repartir el presupuesto (Investigación de Operaciones)

**Qué se buscaba:** cuánto dinero va a cada lugar, mes y canal, para traer el máximo de visitantes sin anunciar donde
está lleno.

| Decisión | Lo que eligió Brandon | Lo que se descartó y por qué |
|---|---|---|
| Qué maximizar | **Visitantes al sur** | Derrama económica (la de SITUR-Q no trae unidad y termina en 2024); visitantes con castigo por presión (habría que inventar el peso) |
| Presupuesto | **Un solo monto: $250,000 al año** (supuesto) | Barrido de 3 montos; rendimiento por cada $10,000 |
| Conversión de Facebook (no publicada) | **Barrido 3 % / 5.75 % / 6.38 %** | Facebook solo para alcance; una sola tasa supuesta |
| Reglas | **Las cuatro:** cero anuncio en temporada alta, capacidad probada, mínimo de 15 % por lugar y tope de 70 % por canal | — |
| Desempate | **Proporcional al espacio libre** | Tope de 25 % por mes; dejarlo concentrado (el óptimo puro mandaba todo el dinero de cada lugar a un solo mes) |

**Por qué hubo que desempatar:** todos los lugares convierten igual (no hay dato de respuesta por lugar), así que había
muchas soluciones con el mismo máximo. El modelo ponía los $131,250 de la Ruta en junio. Brandon eligió repartir según
el espacio libre de cada mes.

**Resultado:**
- **957 visitantes** con $187,500 en 9 meses, a $196 cada uno.
- Las reglas de cuidado **cuestan 0 visitantes**; el tope por canal cuesta 29.5 %.
- Hasta 40 % de ocupación no se pierde ningún visitante.
- El modelo se resuelve en 0.3 segundos.

---

## Fase 7 — La Torre en vivo

**Qué se buscaba:** que la campaña se ajuste cada semana mientras corre.

| Decisión | Lo que eligió Brandon | Lo que se descartó y por qué |
|---|---|---|
| Señales | **Las cuatro:** ocupación del norte, tormentas, clima raro y llegadas del sur | — |
| Qué hacer en el sur | **Pausar esa semana y guardar el dinero** | Bajar a la mitad (se anunciaría con mal clima); solo avisar |
| Qué hacer si el norte se llena | **Encender "¿Ibas al norte?"** hacia el sur con espacio | Solo marcar |
| Cómo mostrarlo | **Reproducción grabada** (GitHub Pages no transmite) | Además, en vivo en localhost (luego se agregó en la Fase 9) |
| Qué es "clima raro" | **Más raro que el 95 %** de las semanas conocidas | Más raro que el 99 % (casi nunca pausa); quitar la señal |

**El error que obligó a decidir:** el corte automático del Isolation Forest marcaba **47 %** de las semanas de Chetumal
como raras, lo que pausaría media campaña. Con el corte que eligió Brandon quedan 21 semanas en Chetumal y 17 en
Kohunlich.

**Resultado:**
- 239 semanas reales en 239 lotes de Spark Structured Streaming, en orden.
- 48 pausas, y no se perdió dinero.
- El modelo marcó las 3 semanas de tormenta **sin saber** que hubo tormenta.

---

## Fase 8 — La campaña "El sur tiene espacio"

**Qué se buscaba:** a quién le habla la campaña, con qué palabras, en qué canal, cuándo y cómo se mide.

| Decisión | Lo que eligió Brandon | Lo que se descartó y por qué |
|---|---|---|
| Personas | **Dos:** la que vuelve al sur (nacional) y la que baja del norte (EE. UU. o Canadá, ya en Cancún) | Solo la nacional; solo la extranjera |
| Nombre | **"El sur tiene espacio"** | "Sur sin prisa" (no dice dónde); "Del Caribe al sur" (solo para la extranjera) |
| Tono | "combina las 3, porque es un orgullo ser méxicano" (cercano y tranquilo + orgullo cultural + aventura) | Uno solo |

**De dónde salió el mensaje:** de 85,987 reseñas. Lo que hunde una reseña es el ruido (2.76×), la suciedad (1.89×), el
precio (1.66×) y las multitudes (1.52×); lo que la protege es la calma (0.41×) y la cultura (0.48×).

**Errores encontrados y corregidos:**
- Las maquetas de los anuncios mostraban un dominio inventado. Se cambió por la dirección real de la página.
- El calendario decía que había anuncio para el norte en un mes sin anuncios.

---

## Fase 9 — Conectar la página con los modelos

**Qué se buscaba:** que la página calcule en vivo, como pide el plan, y que el optimizador responda en menos de 2 segundos.

**Decisión:** un servidor **FastAPI** con 8 endpoints que solo funciona en la computadora del proyecto (127.0.0.1). En
GitHub Pages la página sigue estática y sin llamadas a otros sitios.

- **Descartados:** Flask, que no valida tipos ni se documenta solo, y un servidor en la nube, porque el proyecto debe
  correr sin internet.
- **Seguridad:** la consulta a la base es de **solo lectura** y rechaza cualquier intento de leer archivos o cambiar
  datos (6 intentos probados).
- **Resultado:** el modelo de presupuesto se resolvió en **274 milisegundos** desde la página.

---

## Fase 10 — La página final

| Decisión | Lo que eligió Brandon | Lo que se descartó |
|---|---|---|
| Prueba con personas | **"Solo la revisión automática"**, y se declara que no hubo prueba con personas | Dejar un guion para que el equipo la hiciera con 3 a 5 personas |

**Resultado de la revisión (axe-core, normas WCAG 2.1 AA, 4 vistas):** de **67 fallas a 0**.
- La mayoría eran textos con poco contraste en las fichas de "Los lugares".
- El botón del chat no tenía nombre en celular.
- Las tablas no se podían recorrer con el teclado.

**Equipo confirmado:** Brandon Uriel García Sánchez, Maribel Mondragón Mercado, Jesús Ramírez Isidro y Enrique González
Ortega.

---

## Fase 11 — Cierre y coloquio

**Qué quedó:**
- **Trazabilidad de cada cifra** (`docs/trazabilidad.md`).
- **Mapa del informe técnico**, con las 23 secciones (`docs/informe/MAPA_INFORME.md`).
- **Guion del coloquio de 15 minutos** con los 4 integrantes (`docs/coloquio/GUION_COLOQUIO.md`).
- **Diccionario de datos** de 56 tablas.
- **Estas tres guías.**

**Decisión sobre el coloquio:** el orden sigue **la historia de la campaña** y no las materias, porque la regla del
coloquio pide que la campaña sea el centro. Es una propuesta que el equipo puede ajustar.

---

## La página web (en paralelo a todas las fases)

| Cuándo | Decisión de Brandon | Qué cambió |
|---|---|---|
| 28 sep | "Para gente no técnica" | Lenguaje sencillo; cifras que no escogen datos a conveniencia |
| 28 sep | "Se ve muy IA el font… calidad tipo Apple, hermoso… colores vibrantes para México, identidad real" | Sistema visual **"Sur mexicano"**: rosa, amarillo, turquesa y añil, letras Bricolage y Figtree, greca maya |
| 1 oct | "Agrega muchísimas fotos de toda la comida, de la vista nace el amor" | Galería de 24 platillos (luego **retirada**) |
| 1 oct | "Que sean fotos de las zonas que sí sean de Quintana Roo… primero hasta arriba el plan de viaje… los datos al final" | Se retiró la galería (eran fotos de Mérida y Campeche); 28 fotos con **coordenada comprobada** en su municipio; la página empieza por el viaje |
| 2 oct | "Más fotos a las comidas, reseñas reales, las estrellas del lugar… 10 idiomas… versión nocturna" | Estrellas oficiales donde existen; 10 idiomas; modo noche; experiencias y rutas sin precios |
| 2 oct | "Se te olvidó meter Cancún y Riviera Maya como opciones… el modo nocturno no sirve" | Cancún y la Riviera en toda la parte del viajero, siempre como referencia; modo noche rehecho |

**El error más importante de la página, y cómo se corrigió:** la galería de comida usaba fotos de fuera de Quintana Roo.
Solo se había revisado que no mencionaran lugares excluidos. Se retiró completa, y desde entonces toda foto debe tener
coordenada GPS dentro del municipio de su lugar. Si no la tiene, el programa se detiene.

---

## Lo que estas decisiones tienen en común

1. **Ninguna cifra se inventó.** Cuando faltó un dato (ocupación del sur, conversión de Facebook, golpe de tormenta), se
   declaró como hueco o se probó como supuesto con varios valores.
2. **Cada modelo se comparó contra una regla simple**, como "igual que este mes" o "el mismo mes del año pasado", y se
   dice cuánto le gana.
3. **Cuando algo falló, se contó.** El índice que dio a Cancún como tranquilo, el corte de "clima raro" que marcaba casi
   la mitad de las semanas y las fotos de Mérida se corrigieron con datos, y quedaron escritos.
