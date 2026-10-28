# Torre del Caribe

**Una campaña de publicidad hecha con datos para llevar turistas al sur de Quintana Roo, sin llenarlo de más.**

Problema Prototípico *Turismo inteligente sustentable para México* · Universidad Nacional Rosario Castellanos ·
Licenciatura en Ciencia de Datos para Negocios, 5.º semestre, 2026-2 · Equipo 2.

**Equipo:** Brandon Uriel García Sánchez · Maribel Mondragón Mercado · Jesús Ramírez Isidro · Enrique González Ortega.
**Tutor:** Carlos Orozco Rocha.

**La página:** https://catoxp.github.io/torre-del-caribe-unrc-2026/

---

## En una página

Quintana Roo está lleno de un lado y vacío del otro. Cinco lugares del sur tienen el **12.3 %** de la gente del estado,
pero reciben el **1.4 %** de los pasajeros de avión. La zona arqueológica de Tulum recibe **15.5 veces** más visitantes
que las pirámides del sur.

La campaña **"El sur tiene espacio"** invita a la gente a Chetumal, la Bahía de Calderitas y Oxtankah, la Ruta de las
pirámides (Kohunlich, Dzibanché e Ichkabal), Maya Ka'an y la Laguna Milagros. Cancún y la Riviera Maya solo aparecen
como referencia. La sostienen tres módulos que no se enciman:

| Módulo | Pregunta | Horizonte |
|---|---|---|
| **Radar** | ¿Dónde hay presión y dónde hay espacio? | El mes actual y el siguiente |
| **Pronóstico** | ¿Cuándo conviene ir y cuánto invertir? | De 1 a 12 meses |
| **Torre en vivo** | ¿Qué hace la campaña esta semana? | Semana a semana |

**Resultados**
- Con un presupuesto supuesto de $250,000 al año, el modelo de optimización reparte $187,500 en 9 meses y trae unos
  **957 visitantes**, a **$196** cada uno, sin anunciar nunca un lugar en su temporada alta.
- Las reglas de cuidado (temporada alta, capacidad y mínimo de 15 % por lugar) **no le cuestan ni un visitante** a la
  campaña.
- En 239 semanas reales, la Torre **pausó la campaña 48 veces** por mal clima, tormentas o exceso de gente, sin perder un
  peso.
- Esos 957 son el plan, no una promesa: en 10,000 futuros simulados (Monte Carlo) la campaña trae **788** en el caso
  más probable, entre 579 y 1,016, y en 82 % de los futuros trae menos que el plan. La cifra que más mueve el resultado
  es la conversión de Facebook.
- El Radar anticipa el estado del mes siguiente (tranquilo, concurrido o saturado) con Random Forest + año anterior:
  acierta **130 de 156** meses de prueba, en un año que el modelo nunca vio.
- Todo sale de 7.8 millones de renglones en 15 tablas limpias, de fuentes oficiales o abiertas. Lo que no existe se
  declara como hueco; no se inventa.

---

## Lo que queremos lograr

El Problema Prototípico pregunta:

> *¿Cómo diseñar una campaña publicitaria basada en Ciencia de Datos que permita promover estratégicamente un destino
> turístico del estado seleccionado, atraer segmentos de visitantes de manera responsable y contribuir a una distribución
> más equilibrada de los flujos turísticos, aprovechando la capacidad disponible y reduciendo los impactos económicos,
> sociales y ambientales asociados con la saturación turística en el mismo?*

**Nuestra respuesta:** una campaña que manda gente **solo a donde hay espacio y solo cuando hay espacio**. Medimos dónde
hay presión (Radar), pronosticamos cuándo conviene ir y cuánto invertir (Pronóstico) y, cada semana, la Torre decide si
la campaña sigue, se pausa o cambia de lugar. Lo que ve el viajero (la página, la aplicación y "Cotiza tu viaje") usa
esos mismos datos: le recomienda el sur, en meses tranquilos, y nunca le vende un lugar lleno.

| Pregunta secundaria | Cómo la respondemos | Notebook |
|---|---|---|
| 1. Patrones de la concentración de turistas | Concentración (Herfindahl-Hirschman), forma del año y agrupamiento | 2, 3 |
| 2. Variables de la saturación | Índice de presión turística y clasificador del Radar | 3, 4 |
| 3. Demanda futura con incertidumbre | Cinco modelos de pronóstico, rango del 90 %, Poisson, Markov y Monte Carlo | 4, 5 |
| 4. Redistribuir sin perder actividad económica | Programación estocástica del presupuesto y frontera de Pareto | 6 |
| 5. Qué recomendar a cada visitante | Segmentación, buyer persona, el planeador y "Cotiza tu viaje" | 3, 7 |
| 6. Impacto en comunidades y destinos saturados | Presión por habitante, límite de capacidad y pausas de la Torre | 3, 6 |
| 7. ¿Es viable, sustentable y efectiva? | Indicadores, escenarios y sensibilidad | 5, 6, 7 |

---

## Qué hay en esta carpeta

```
1_Documento/       El documento técnico del equipo: Torre_del_Caribe.pdf y su versión editable en Word (.docx)
2_Notebooks/       Siete notebooks, uno por materia, ya ejecutados (.ipynb y .html), dos Excel y las gráficas
3_Pagina_web/      La página de la campaña (la misma que está en línea); la aplicación de teléfono es esta misma página
4_Aplicacion_movil/  La aplicación de teléfono (la página en modo aplicación): el APK de Android, cómo instalarla y sus capturas
5_Evidencias/      Capturas de la página, sección por sección, y de una solicitud de cotización con su folio
datos/             Tablas limpias (silver), resultados (gold), diccionario de datos y lo poco del crudo que se usa
herramientas/      Hadoop para Windows (Spark lo necesita para escribir archivos) y las fuentes de letra
requirements.txt   Las librerías de Python, con versión fija
```

### Dónde está cada materia

| Materia (UCA) | Profesor | Notebook | Qué se hizo |
|---|---|---|---|
| Herramientas para el Almacenamiento de Grandes Volúmenes de Datos | Víctor Gabriel Cruz Arrona | `1_Grandes_volumenes_PySpark` | Arquitectura medallón con SHA-256; HURDAT2 de Bronze a Silver con PySpark; consultas sobre 6.1 millones de negocios; ventanas de tiempo; DuckDB con modelo estrella; 239 semanas en Spark Structured Streaming |
| Minería de Datos (planteamiento) | Luis Becerril Espinosa | `2_Planteamiento_y_analisis_de_datos` | Fuentes y huecos; concentración con el índice de Herfindahl-Hirschman; criterios de los 5 lugares; análisis exploratorio; la lluvia y el calor (ERA5 contra SMN) |
| Minería de Datos | Luis Becerril Espinosa | `3_Mineria_de_datos` | Índice de presión turística; agrupamiento de Ward; forma del año; Isolation Forest comparado con otros tres detectores; minería de texto (léxico, Apriori, log-odds) |
| Aprendizaje de Máquina | Raúl Jorge Domínguez Vilchis | `4_Aprendizaje_de_maquina` | Clasificador del estado del mes siguiente con entrenamiento, validación y prueba; cinco modelos de pronóstico en origen móvil; rango conformal del 90 % |
| Modelos Estocásticos para la Toma de Decisiones | René Chablé García | `5_Modelos_estocasticos` (+ `5_Poisson_tormentas.xlsx`) | Poisson de tormentas con sus pruebas (dispersión, tendencia, intervalos exactos); cadena de Markov semanal; Monte Carlo de 10,000 futuros; sensibilidad |
| Investigación de Operaciones | Carlos Orozco Rocha | `6_Investigacion_de_operaciones` (+ `6_Metodo_grafico.xlsx`) | Método gráfico; programación estocástica de dos etapas con PuLP y CBC; precios sombra; frontera de Pareto; sensibilidad; motor semanal |
| Mercadotecnia Digital | Víctor Hugo Reyes Anselmo | `7_Mercadotecnia_digital` | Segmentación, dos buyer persona, marca, mensajes con su dato, medios, embudo, indicadores y regla anti-colapso |

### Cómo están hechos los notebooks

Cada notebook se lee de arriba abajo, como lo explicaríamos en clase:

1. **Antes de cada celda de código** explicamos qué vamos a hacer y por qué.
2. **Dentro del código**, cada renglón lleva su comentario.
3. **Cada valor que elegimos** (un umbral, un número de árboles, un corte) aparece en una tabla con *por qué lo
   elegimos* y *qué alternativas descartamos*, con la cifra que lo justifica.
4. **Al terminar cada paso** comparamos nuestro resultado con el que guardó el proyecto (función `coincide`). Si una
   cifra no coincidiera, el notebook se detendría ahí: todo lo que se ve en un notebook es lo mismo que usa la página.

---

## Empieza aquí: ver el proyecto en 5 minutos

No hace falta instalar nada para esto.

1. **Abre la página.** Entra a https://catoxp.github.io/torre-del-caribe-unrc-2026/ (o haz doble clic en
   `3_Pagina_web/index.html`, que funciona sin internet).
2. **Abre un notebook ya ejecutado.** Haz doble clic en `2_Notebooks/5_Modelos_estocasticos.html`. Se abre en el
   navegador con todo el código y los resultados: la probabilidad de tormenta en agosto (14 %) sale paso a paso.
3. **Abre la aplicación.** En el teléfono, entra a https://catoxp.github.io/torre-del-caribe-unrc-2026/app/ o instala
   `4_Aplicacion_movil/Torre_del_Caribe.apk` en Android.
4. **Mira cómo llega una solicitud.** `5_Evidencias/solicitudes/` tiene, paso a paso, una solicitud de prueba: el plan,
   el formulario con el aviso de privacidad y el folio con el que se guardó en la base de datos.
5. **Abre el Excel de Poisson.** `2_Notebooks/5_Poisson_tormentas.xlsx` tiene el mismo cálculo con fórmulas de Excel,
   junto al valor de Python.

---

## Cómo correr los notebooks

**Necesitas:** Python 3.11, unos 2 GB de espacio y, para el notebook 1 (Spark), Java 17.

1. Instala Java 17 (una sola vez; en Windows pide permiso de administrador):

   ```bash
   winget install Microsoft.OpenJDK.17
   ```

2. Desde esta carpeta, crea un entorno e instala las librerías:

   ```bash
   python -m venv .venv
   .venv\Scripts\python -m pip install -r requirements.txt
   ```

3. Abre la carpeta en VS Code o en Jupyter, abre un notebook de `2_Notebooks/` y elige **Ejecutar todo**.

**Cómo saber que funcionó:** la primera celda imprime `Carpeta de la entrega: …` y cada comparación imprime
`✓ … coincide con el proyecto`.

**Cuánto tardan, aproximadamente:** 1 Grandes volúmenes, 7 minutos (la reproducción en streaming procesa 239 lotes);
2 Planteamiento, 1 minuto; 3 Minería, 1 minuto; 4 Aprendizaje de máquina, 5 minutos; 5 Estocásticos, menos de 1 minuto;
6 Investigación de Operaciones, menos de 1 minuto; 7 Mercadotecnia, menos de 1 minuto.

**Si algo falla**

| Mensaje | Qué pasa | Qué hacer |
|---|---|---|
| `Falta Java 17` | Spark necesita Java 17 | `winget install Microsoft.OpenJDK.17` y vuelve a abrir el notebook |
| `StopIteration` en la primera celda | El notebook no encuentra la carpeta `datos/silver` | Ábrelo desde `2_Notebooks/` de esta carpeta |
| `✗ … no coincide con el proyecto` | Se cambió un dato o un cálculo | Revisa qué se cambió; la entrega se arma solo si todo coincide |

### Cómo consultar los datos con SQL

El notebook 1 arma el almacén DuckDB con las rutas de esta carpeta. Para consultarlo aparte:

```python
import duckdb
con = duckdb.connect("datos/gold/torre.duckdb", read_only=True)
con.sql("SELECT lugar, variable, count(*) FROM hechos_mes GROUP BY ALL ORDER BY lugar").show()
```

El significado de cada tabla y columna está en `datos/DICCIONARIO.md`.

---

## Los datos (`datos/`)

| Carpeta | Contenido | Tamaño |
|---|---|---|
| `silver/` | Las 15 tablas limpias en Parquet: DENUE (6,138,075 negocios), clima diario y horario, normales del SMN, nacionalidades, reseñas, INAH, huracanes, ocupación hotelera, vuelos, tipo de cambio, SITUR-Q, cruceros y Censo 2020 | 360 MB |
| `gold/` | Los resultados de los modelos (Radar, Pronóstico, presupuesto, Torre y campaña) y el modelo estrella | 8 MB |
| `bronze/` | El manifiesto de los 380 archivos descargados y, completos, los crudos de huracanes, normales del SMN, costos de anuncios y el mapa de municipios | 27 MB |
| `DICCIONARIO.md` | Cada tabla y columna, con tipo, porcentaje de vacíos, un ejemplo real y su significado | |

El crudo completo pesa 814 MB y no viene en la carpeta; el manifiesto guarda la dirección, la fecha y la huella SHA-256
de cada archivo, y el notebook 1 comprueba las huellas de los que sí vienen.

### Las fuentes

Solo fuentes oficiales o abiertas, descargadas con programas y sin modificar. No se usó nada copiado de Google Maps ni de
TripAdvisor, porque sus términos de uso lo prohíben.

| Fuente | Quién la publica | Para qué se usó |
|---|---|---|
| SITUR-Q | Gobierno de Quintana Roo | Tren Maya, cruces desde Belice, cruceros, cuartos y ocupación hasta 2024 |
| DataTur | SECTUR | Ocupación semanal, visitantes del INAH, nacionalidades, vuelos (AFAC), cruceros |
| DENUE, Censo 2020 (ITER), ENDUTIH 2025 | INEGI | Negocios, población por localidad y uso de internet |
| HURDAT2 | NOAA | Tormentas del Atlántico desde 1851 |
| Open-Meteo (reanálisis ERA5) | Open-Meteo | Clima diario desde 1950 y horario desde 2019 (para los modelos) |
| Normales climatológicas 1991–2020 | SMN-CONAGUA | Lluvia y temperatura que ve el viajero |
| FRED | Banco de la Reserva Federal de San Luis | Tipo de cambio |
| Rest-Mex 2025 | Concurso académico, licencia CC BY 4.0 | 85,987 reseñas de Quintana Roo |
| WordStream y LocaliQ | Publicaciones abiertas (promedios de EE. UU.) | Costo por clic y conversión de anuncios de viajes |
| Wikimedia Commons e iNaturalist | Autores individuales, licencias CC | Fotos de la página, cada una con su crédito y su ubicación comprobada |

---

## Cómo trabajamos

Hicimos el proyecto en 12 fases, una a la vez. En cada decisión de fondo pusimos sobre la mesa opciones con su evidencia
y elegimos una. En la revisión final repasamos cada decisión con los datos y cambiamos dos: el clasificador del Radar
ahora se elige con un año de validación y se mide en otro año distinto (gana Random Forest + año anterior, decisión 34), y el clima que ve el
viajero sale de las estaciones del SMN en lugar del reanálisis. Para programar usamos un asistente de programación con
inteligencia artificial (Claude Code) como herramienta, con reglas que fijamos desde el inicio: no inventar datos,
explicar cada decisión con una cifra real y decidir siempre entre opciones. Las decisiones, la revisión y la defensa del
proyecto son del equipo.

## Créditos y licencias

- Datos: de sus fuentes oficiales (tabla de arriba). Rest-Mex 2025 se usa bajo licencia CC BY 4.0.
- Fotos de la página: Wikimedia Commons e iNaturalist, con el autor y la licencia de cada una junto a la foto.
- Letras: Bricolage Grotesque, Figtree y Noto Sans (licencia SIL Open Font License).
- `herramientas/hadoop`: winutils y hadoop.dll 3.3.6 (Apache License 2.0), necesarios para que Spark escriba en Windows.
