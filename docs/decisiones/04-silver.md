# 04 — Limpieza y orden de los datos (Fase 2: Silver y Gold) · EN CURSO

Autor: **Brandon Uriel García Sánchez** · 28-sep-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Decisiones de Brandon (28-sep-2026)
- **La página se construye en paralelo** a los datos, desde ahora.
- **DENUE se procesa completo** (6,138,075 negocios del país), no solo Quintana Roo, para tener volumen real en el
  criterio de Big Data.
- **Oferta turística** = giros SCIAN característicos del turismo (SECTUR/INEGI): alojamiento (721), alimentos y bebidas
  (722), agencias de viajes (5615), transporte turístico (487), museos y sitios (712) y esparcimiento (713).

## Avance

### SITUR-Q → `datos/silver/siturq/` ✅
Código: `backend/torre/base/silver_siturq.py` (PySpark).

| Indicador | Filas | Cobertura |
|---|---:|---|
| Ocupación hotelera | 1,953 (693 marcadas como hueco) | 2020 – dic-2024 |
| Habitaciones / centros de hospedaje | 825 / 825 | 2022 – jul-2026 |
| Zonas arqueológicas | 910 | 2019 – jul-2026 |
| Aéreos (llegadas) | 450 (114 marcadas como hueco) | 2019 – dic-2024 |
| Afluencia de turistas | 600 (15 marcadas como hueco) | 2021 – mar-2024 |
| Derrama (visitantes / turistas) | 414 / 414 (9 y 9 marcadas como hueco) | 2022 – mar-2024 |
| Cruceristas | 273 | 2019 – jul-2026 |
| Tren Maya (movimiento / descensos) | 248 / 248 | 2024 – jul-2026 |
| Frontera con Belice | 180 | 2019 – jun-2026 |

Reglas, cada una verificada con los datos:
1. **Tren Maya:** algunos destinos traen 2 filas por mes (una por estación) y **se suman**. La suma cuadra exacto con
   el total que publica SITUR-Q para la zona. En descensos de ene-2025: Grand Costa Maya 7,084 = Chetumal (24 + 3,478)
   + Bacalar (213 + 3,369). En Riviera Maya: 17,031 = Playa del Carmen 8,585 + Tulum (1,717 + 6,729).
2. **Ocupación con 0 habitaciones disponibles = hueco**, no 0 %, porque es físicamente imposible. Así quedan 693 filas:
   todo 2025 y los años en que un destino aún no publicaba (por ejemplo, Mahahual antes de 2024).
3. **Afluencia y derrama en 0 = hueco.** Un destino no recibe cero turistas ni cero pesos en un mes. *Corrección del
   28-sep-2026:* la primera versión conservaba esos ceros y hacía parecer que había datos hasta abril y junio de 2024;
   en realidad terminan en marzo de 2024 (15 meses de afluencia y 9 de cada derrama pasan a hueco).
4. **Los demás ceros se conservan**, porque pueden ser reales (cruceristas de 2020, con los puertos cerrados; zonas
   arqueológicas cerradas).
5. **El indicador "Turista - Afluencia"** falló en las 120 consultas y no aporta filas.
6. **Llegadas aéreas: un mes en que TODOS los aeropuertos reportan 0 = hueco** (regla agregada el 28-sep-2026, al
   construir el mapa "Así llega la gente"). De 2019 a 2024 cada mes trae dato (en 2020, con la pandemia, las cifras
   bajan pero no llegan a cero en todos a la vez). Desde enero de 2025 los cuatro aeropuertos (Cancún, Cozumel,
   Chetumal y Tulum) y el agregado de Grand Costa Maya marcan 0 todos los meses: 72 filas de 2025 y 42 de 2026, 114 en
   total. Cancún no pudo recibir cero pasajeros en un año en que su ocupación semanal de DataTur promedió 72.2 % (máximo
   83.2 %); es la
   fuente la que dejó de publicar. Si en un mes al menos un aeropuerto trae dato, ningún cero de ese mes se toca
   (podría ser un aeropuerto cerrado de verdad). *Consecuencia:* la página usa **2024** como último año completo del
   avión (15,959,277 pasajeros) y lo dice en pantalla. *Prueba:* `test_regla_6_aereos`.
   *Opción descartada:* conservar los ceros; la página habría mostrado "0 pasajeros en avión en 2025".

### DataTur, ocupación hotelera → `datos/silver/datatur_ocupacion/` ✅
Código: `backend/torre/base/silver_datatur_ocupacion.py`. Los Excel se leen con openpyxl porque Spark no lee Excel de
forma nativa; la unión, la deduplicación y la escritura las hace Spark.

- **Cobertura mayor a la esperada: de enero de 2022 a julio de 2026.** Cada archivo compara tres años del mismo
  periodo: el de 2024 incluye 2022 y 2023.
- **Resultado:** 18,891 filas semanales (66 centros) y 4,450 mensuales (96 centros). Los 7 centros de Quintana Roo
  (Cancún, Riviera Maya, Playa del Carmen, Playacar, Akumal, Cozumel e Isla Mujeres) tienen las **239 semanas**
  completas.
- **Una versión por periodo:** cuando un periodo aparece en varios archivos, gana el más reciente, porque DataTur
  corrige sus cifras preliminares. Hubo **2,804 cifras semanales revisadas**.
- **Notas al pie guardadas como bandera de comparabilidad:**
  - Isla Mujeres: *"A partir del 1 de septiembre 2025 se actualizó la oferta hotelera del centro, por lo que los datos
    no son estrictamente comparables"* (148 semanas marcadas).
  - Cozumel (2025) y Akumal (2024): *"datos no comparables con el periodo anterior"*.
- **Ocupación promedio 2022–2026** (por semana): Playacar 83.2 %, Akumal 74.3 %, Cancún 74.2 %, Riviera Maya 73.1 %,
  Playa del Carmen 68.7 %, Cozumel 53.0 % e Isla Mujeres 51.8 %.

### DENUE (negocios del país) → `datos/silver/denue/` ✅
Código: `backend/torre/base/silver_denue.py` (PySpark, cerca de 1.5 minutos).

- **Qué se lee:** solo el CSV de la carpeta `conjunto_de_datos` de cada uno de los 33 zips (el Estado de México viene
  en 2 partes). Se descomprime en una carpeta temporal que se borra al terminar. Codificación ISO-8859-1.
- **Resultado:** **6,138,075 negocios, 0 duplicados** (por `id`) y 0 coordenadas fuera de México
  (latitud 14–33, longitud −119 a −86). Partido por estado (`cve_ent`).
- **Columnas nuevas:**
  - `scian_3`: los 3 primeros dígitos del código de actividad.
  - `categoria_turistica` y `es_turistico`: 5615 se revisa primero porque tiene 4 dígitos; después 721, 722, 487, 712 y 713.
  - `personas_min` / `personas_max`: salen del rango de personal ocupado ("0 a 5 personas").
  - `coordenadas_flag`: marca las coordenadas fuera de México.
  - `es_qroo`: marca los negocios de Quintana Roo.
- **Privacidad:** se descartan `raz_social`, `telefono` y `correoelec`. Ningún modelo las necesita.
- **Oferta turística:** 875,667 negocios turísticos en el país (14.3 %); **13,663 en Quintana Roo** (19.7 % de sus 69,260).

| Municipio (Q. Roo) | Alimentos | Alojamiento | Esparcimiento | Agencias | Museos | Transporte | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Benito Juárez | 4,429 | 277 | 363 | 177 | 13 | 34 | 5,293 |
| Solidaridad | 1,685 | 256 | 129 | 105 | 23 | 6 | 2,204 |
| Othón P. Blanco | 1,558 | 118 | 135 | 16 | 8 | 1 | 1,836 |
| Cozumel | 854 | 77 | 169 | 34 | 12 | 2 | 1,148 |
| Tulum | 703 | 288 | 36 | 21 | 31 | 1 | 1,080 |
| Bacalar | 259 | 136 | 18 | 6 | 2 | 1 | 422 |
| Lázaro Cárdenas | 234 | 153 | 11 | 6 | 0 | 1 | 405 |
| Felipe Carrillo Puerto | 356 | 17 | 22 | 3 | 4 | 0 | 402 |
| Isla Mujeres | 273 | 75 | 24 | 9 | 4 | 0 | 385 |
| Puerto Morelos | 252 | 32 | 26 | 5 | 4 | 0 | 319 |
| José María Morelos | 152 | 10 | 7 | 0 | 0 | 0 | 169 |

- **Error de conteo detectado en la Fase 1.** Spark contó 6,138,075 y el manifiesto decía 6,139,989. Un lector CSV
  independiente dio la cifra de Spark. La diferencia de 1,914 = 33 zips × 58 líneas del diccionario de datos, que la
  función de conteo sumaba como negocios. Se corrigió la función, el manifiesto y los documentos. El detalle está en
  `03-ingesta.md`.
- **Consecuencia para el Radar (A1):** la densidad de oferta por municipio entra al Índice de Presión Turística.
  Othón P. Blanco tiene oferta instalada; Felipe Carrillo Puerto y José María Morelos, muy poca. En ellos la
  capacidad es un límite duro de la optimización.

### INAH (visitantes a museos y zonas arqueológicas) → `datos/silver/inah/` ✅
Código: `backend/torre/base/silver_inah.py` (pandas lee el Excel; Spark escribe el Parquet particionado por año).
Se hizo al abrir la Fase 3, porque la tabla de criterios de las 5 regiones lo necesita.

- **Resultado:** 71,278 filas de todo el país (2016–2026), una por sitio, mes y tipo de visitante (nacional o
  extranjero). Quintana Roo: 3,594 filas de 16 sitios.
- **Duplicado encontrado:** el bloque "Extranjero, septiembre de 2025" viene dos veces en el archivo de DataTur
  (283 sitios × 2). Una copia trae las cifras y la otra puros ceros. Se conserva la fila con cifra. Si algún día
  aparecen dos cifras distintas de cero para la misma llave, el proceso se detiene en lugar de elegir una.
- **Papel de cada zona en la campaña** (`region_campana`, `papel_campana`), según `docs/regiones/REGIONES.md` D.5:

| Papel | Zonas | Visitantes 2025 |
|---|---|---:|
| Promovida · Ruta arqueológica del sur | Kohunlich, Dzibanché-Kinichná, Ichkabal | 66,628 |
| Promovida · Bahía Calderitas–Oxtankah | Oxtankah | 11,017 |
| Referencia · Tulum | Z.A. Tulum | 1,031,443 |
| Referencia · Cancún | El Rey, El Meco, Museo Maya de Cancún | 89,940 |
| Referencia · Riviera Maya | Xcaret, Xelhá | 238 |
| Retirada | Cobá (191,815) y Muyil (0: cerrada) | — |
| Excluida | Chacchoben (237,039, crucero) y San Gervasio (143,541, Cozumel) | — |

- **Los ceros se conservan** y se marcan con `sin_visitantes_flag`, porque suelen ser cierres (Muyil, jun-2024 a
  feb-2026), no falta de interés.
- **Chetumal, Maya Ka'an y Laguna Milagros–Xul-Ha no tienen zona INAH propia.** Se medirán con SITUR-Q, DENUE y el
  Censo; se declara.

## Fuentes que no coinciden: Isla Mujeres
En la selección de regiones (`01-regiones.md`), Isla Mujeres se excluyó en parte por noticias que reportaban 93.5 %
de ocupación en febrero de 2026 y 95 % en abril. **DataTur, la fuente oficial, registra 74.7 % en febrero y 43.2 % en
abril de 2026** (promedio semanal 2022–2026: 51.8 %). Además, DataTur advierte que la oferta hotelera de Isla Mujeres
se actualizó en septiembre de 2025, así que las cifras pueden no ser comparables entre fuentes.
**Consecuencia:** el argumento de "saturación" para Isla Mujeres no se sostiene con el dato oficial. Su exclusión se
**reevalúa en la Fase 3** con la tabla de criterios calculada con datos. La otra razón de exclusión (carencias de agua,
drenaje y basura en la parte continental) sigue en pie. Este es un ejemplo de lo que pide el incidente de Big Data:
fuentes que no coinciden y una regla explícita para elegir entre ellas (dato oficial sobre nota de prensa).

## Problemas encontrados y cómo se resolvieron
| Problema | Solución |
|---|---|
| El indicador roto de SITUR-Q hacía fallar la lectura: Spark leía sus respuestas nulas como texto | Si un archivo no trae ninguna respuesta con estructura, se omite |
| En Windows, Spark no encontraba su propio Python ("Accept timed out") | `entorno.py` le indica el Python del proyecto |
| La ruta de la carpeta tiene espacios ("PP 5to semestre") y los scripts de Spark la cortaban | Se usa la ruta corta de Windows, que no tiene espacios |
| Un mismo centro contaba dos veces por las marcas de nota ("ISLA MUJERES /4") | La deduplicación usa el nombre limpio |
| Las notas al pie del Excel se leían como centros | Solo cuentan las filas con números; las notas se guardan aparte |
| El conteo de la Fase 1 sumaba el diccionario de datos del DENUE como negocios | `_filas_csv_en_zip` ignora los CSV de diccionario; se recontó el manifiesto |
| Abreviaturas de estado distintas ("Q.ROO" / "Q. ROO", "BC" / "B.C.") | Se normalizan a "QROO", "BC", etc. |

## Pruebas (24 de 24 en verde, `tests/test_silver.py`; el Censo ITER se documenta en `05-planteamiento.md`)
- **SITUR-Q:**
  - Bacalar ene-2024 = 66.5 %.
  - Chetumal suma sus 2 estaciones (3,502).
  - La zona Grand Costa Maya = la suma de sus destinos (7,084).
  - La ocupación 2025 es hueco y no 0.
  - Los ceros reales se conservan, y la afluencia y la derrama con dato real terminan en marzo de 2024.
  - Regla 6: un mes aéreo es hueco completo o no lo es; 114 de 450 filas; los huecos no guardan el 0.
- **DataTur:**
  - Cancún semana 31 de 2026 = 37,337 cuartos y 67.53 %.
  - No hay duplicados.
  - Cada centro de Quintana Roo tiene 239 semanas.
  - La ocupación publicada coincide con ocupados ÷ disponibles en más del 99 % de las filas.
  - La nota de Isla Mujeres quedó registrada.
- **DENUE:**
  - 6,138,075 negocios, sin duplicados.
  - 13,663 negocios turísticos en Quintana Roo.
  - No existen las columnas de razón social, teléfono ni correo.
  - Todas las coordenadas están dentro de México.
- **INAH:**
  - 71,278 filas sin llaves repetidas (se quitó el bloque duplicado de sep-2025).
  - Visitantes 2025: Tulum 1,031,443; ruta del sur 66,628; Oxtankah 11,017 (las cifras de la selección de regiones).
  - Kohunlich ene–jul 2026 contra 2025: +13.5 %.
  - Solo las 4 zonas de las 5 regiones van como "promovida"; Cobá y Muyil como "retirada".

## Pendiente de la Fase 2
Nacionalidades, AFAC, cruceros, clima, huracanes, reseñas y tipo de cambio en
Silver. Después: tablas finales (Gold), diccionario de datos, reporte de calidad y reconciliación SITUR-Q contra DataTur.
