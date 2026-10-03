# Torre del Caribe

**Una campaña de publicidad hecha con datos para llevar turistas al sur de Quintana Roo, sin llenarlo de más.**

Problema Prototípico *Turismo inteligente sustentable para México* · Universidad Nacional Rosario Castellanos ·
Licenciatura en Ciencias de Datos para Negocios, 5° semestre, 2026-2.

**Equipo:** Brandon Uriel García Sánchez (responsable técnico) · Maribel Mondragón Mercado · Jesús Ramírez Isidro ·
Enrique González Ortega.

**La página:** https://catoxp.github.io/torre-del-caribe-unrc-2026/

---

## En una página

Quintana Roo está lleno de un lado y vacío del otro. Cinco lugares del sur tienen el **12.3 %** de la gente del estado,
pero reciben el **1.4 %** de los pasajeros de avión. La zona arqueológica de Tulum recibe **15.5 veces** más visitantes
que las pirámides del sur, y en 2024 Chetumal dejó vacíos **4 de cada 10** cuartos de hotel.

La campaña **"El sur tiene espacio"** invita a la gente a Chetumal, la Bahía de Calderitas y Oxtankah, la Ruta de las
pirámides (Kohunlich, Dzibanché e Ichkabal), Maya Ka'an y la Laguna Milagros. Cancún, la Riviera Maya y Tulum solo
aparecen como referencia. La sostiene un sistema con tres pantallas que no se enciman:

| Pantalla | Pregunta | Horizonte |
|---|---|---|
| **Radar** | ¿Dónde hay espacio hoy? | El mes actual y el siguiente |
| **Pronóstico** | ¿Cuándo conviene ir y cuánto invertir? | De 1 a 12 meses |
| **Torre en vivo** | ¿Qué hace la campaña esta semana? | Semana a semana |

**Resultados**
- Con un presupuesto supuesto de $250,000 al año, el modelo de optimización reparte $187,500 en 9 meses y trae unos
  **957 visitantes**, a **$196** cada uno, sin anunciar nunca un lugar en su temporada alta.
- Las reglas de cuidado (temporada alta, capacidad y mínimo de 15 % por lugar) **no le cuestan ni un visitante** a la
  campaña.
- En 239 semanas reales, la Torre **pausó la campaña 48 veces** por mal clima, tormentas o exceso de gente, sin perder un
  peso.
- Todo sale de **8,134,802 registros** de 15 fuentes oficiales o abiertas. Lo que no existe se declara como hueco; no se
  inventa.

---

## Qué hay en este repositorio

```
1_Documentos/      Los documentos en PDF: tres guías, el documento ejecutivo y cinco de respaldo
2_Notebooks/       Cuatro notebooks ya ejecutados (.ipynb y .html), con todo el código dentro
3_Pagina_web/      La página de la campaña (la misma que está en línea)
datos/             Tablas limpias (silver), resultados (gold), manifiesto de lo descargado y diccionario
herramientas/      Hadoop para Windows (Spark lo necesita para escribir archivos) y las fuentes de letra
requirements.txt   Las librerías de Python, con versión fija
```

### Por dónde empezar

| Si eres… | Abre primero |
|---|---|
| Profesor o sinodal | `1_Documentos/1_Guia_tecnica.pdf` y el notebook de tu materia (tabla de abajo) |
| Integrante del equipo | `1_Documentos/2_Guia_sencilla.pdf`, luego `3_Decisiones_fase_por_fase.pdf` |
| Quien redacta el informe | `1_Documentos/4_Documento_ejecutivo.pdf` y `6_Mapa_del_informe_tecnico.pdf` |
| Quien prepara el coloquio | `1_Documentos/7_Guion_del_coloquio.pdf` |
| Quien solo quiere ver la campaña | La página en línea o `3_Pagina_web/index.html` |

### Dónde está cada materia

| Materia (UCA) | Notebook | Qué se hizo |
|---|---|---|
| Grandes volúmenes de datos | `1_Datos_y_arquitectura`, y Spark Streaming en `3_Presupuesto_y_Torre_en_vivo` | Bronce → plata → oro con PySpark; DuckDB con modelo estrella; 239 semanas reproducidas en flujo |
| Planteamiento | `2_Donde_y_cuando` (parte A) | Variables, actores y concentración (índice de Herfindahl-Hirschman: 0.811 en avión) |
| Minería de datos | `2_Donde_y_cuando`, `3_…`, `4_Campana` | Índice de presión, forma del año, agrupamiento de Ward, Isolation Forest, minería de texto |
| Aprendizaje de máquina | `2_Donde_y_cuando` (partes B y C) | Clasificador del estado del mes siguiente; 5 modelos de pronóstico con rango conformal del 90 % |
| Procesos estocásticos | `2_Donde_y_cuando` (partes B y C) | Cadena de Markov semanal, Poisson de tormentas, Monte Carlo de 10,000 futuros |
| Investigación de Operaciones | `3_Presupuesto_y_Torre_en_vivo` (parte A) | Programación estocástica de dos etapas con PuLP y CBC, precios sombra y frontera de Pareto |
| Mercadotecnia digital | `4_Campana` | Dos viajeras ideales, marca, cinco anuncios con su dato, medios y diez indicadores |

---

## Empieza aquí: ver el proyecto en 5 minutos

No hace falta instalar nada para esto.

1. **Abre la página.** Entra a https://catoxp.github.io/torre-del-caribe-unrc-2026/ (o haz doble clic en
   `3_Pagina_web/index.html`, que funciona sin internet). Elige **Ruta de las pirámides** y **enero de 2027**: verás que
   es temporada alta y que la página te recomienda Chetumal o la Ruta en noviembre. Esa es la campaña funcionando.
2. **Abre un notebook ya ejecutado.** Haz doble clic en `2_Notebooks/2_Donde_y_cuando.html`. Se abre en el navegador con
   todo el código y todos los resultados. Busca "IPT = promedio": es el índice de presión de Cancún calculado paso a paso
   (0.1931).
3. **Abre la guía sencilla.** `1_Documentos/2_Guia_sencilla.pdf` explica, sin fórmulas difíciles, qué se hizo y por qué.

Con eso ya viste el resultado, el cálculo y la explicación.

---

## Cómo hacer cosas

### Cómo correr los notebooks en tu computadora

**Necesitas:** Python 3.11, unos 2 GB de espacio y, para los notebooks 1 y 3 (Spark), Java 17.

1. Instala Java 17 (una sola vez; en Windows pide permiso de administrador):

   ```bash
   winget install Microsoft.OpenJDK.17
   ```

2. Desde la carpeta del repositorio, crea un entorno e instala las librerías:

   ```bash
   python -m venv .venv
   .venv\Scripts\python -m pip install -r requirements.txt
   ```

3. Abre la carpeta en VS Code o en Jupyter, abre un notebook de `2_Notebooks/` y elige **Ejecutar todo**.

**Cómo saber que funcionó:** la primera celda imprime `Carpeta de la entrega: …` y, al final, las cifras coinciden con
las que ya traía el notebook (por ejemplo, `Visitantes esperados: 956.8` en el notebook 3).

**Cuánto tardan:** 1 Datos, unos 12 minutos con el crudo completo (si no, unos 2 minutos); 2 Dónde y cuándo, unos 2 minutos;
3 Presupuesto y Torre, unos 6 minutos; 4 Campaña, menos de 1 minuto.

**Si algo falla**

| Mensaje | Qué pasa | Qué hacer |
|---|---|---|
| `No encontré un JDK 17` | Spark necesita Java 17 | `winget install Microsoft.OpenJDK.17` y vuelve a abrir el notebook |
| `ModuleNotFoundError: torre…` | Se corrió una celda de abajo sin correr las de arriba | **Ejecutar todo** desde el principio: las celdas `%%modulo` registran el código |
| `UsageError: Cell magic %%modulo not found` | No se corrió la celda de preparación | Corre la primera celda de código del notebook |
| El notebook 1 dice "se usa la tabla limpia que ya viene" | El crudo (814 MB) no viene en el repositorio | Es lo esperado; las tablas limpias ya están en `datos/silver` |

### Cómo volver a limpiar los datos desde cero

El crudo no viene en el repositorio porque pesa 814 MB. `datos/bronze/MANIFIESTO.csv` dice de dónde salió cada uno de
los 353 archivos (dirección, fecha y huella SHA-256). Para rehacer la limpieza:

1. Descarga los archivos con las funciones de descarga del notebook 1 (sección "Cómo se descargó"), o pídelos al equipo.
2. Ponlos en `datos/bronze/` respetando las carpetas del manifiesto.
3. Corre el notebook 1. La celda de Spark dirá `¿Está el crudo completo para volver a limpiar? sí` y las 12 limpiezas se
   ejecutarán de nuevo.

### Cómo consultar los datos con SQL

Después de correr el notebook 1, el almacén queda en `datos/gold/torre.duckdb`:

```python
import duckdb
con = duckdb.connect("datos/gold/torre.duckdb", read_only=True)
con.sql("SELECT lugar, variable, count(*) FROM hechos_mes GROUP BY ALL ORDER BY lugar").show()
```

El significado de cada tabla y columna está en `datos/DICCIONARIO.md` (también en `1_Documentos/8_Diccionario_de_datos.pdf`).

---

## Referencia

### Los documentos (`1_Documentos/`)

| Archivo | Qué es |
|---|---|
| `1_Guia_tecnica.pdf` | Todo el proyecto fórmula por fórmula, cada una con su fundamento y un ejemplo resuelto a mano con números reales (85 págs.) |
| `2_Guia_sencilla.pdf` | Lo mismo sin tecnicismos, con comparaciones y cuentas de calculadora (62 págs.) |
| `3_Decisiones_fase_por_fase.pdf` | Cada decisión de las 12 fases: opciones, evidencia, qué se eligió y qué cambió (46 págs.) |
| `4_Documento_ejecutivo.pdf` | Documento no técnico, con gráficas y capturas de la página, capítulo por fase |
| `5_Trazabilidad_de_las_cifras.pdf` | De dónde sale cada cifra visible: archivo crudo, función, salida y prueba |
| `6_Mapa_del_informe_tecnico.pdf` | Qué alimenta cada una de las 23 secciones obligatorias del informe |
| `7_Guion_del_coloquio.pdf` | Los 15 minutos del coloquio repartidos entre los cuatro integrantes |
| `8_Diccionario_de_datos.pdf` | Las 56 tablas, columna por columna |
| `9_Auditoria_de_la_pagina.pdf` | Revisión de accesibilidad (WCAG 2.1 AA): 0 fallas en 4 vistas |

### Los notebooks (`2_Notebooks/`)

Cada notebook se lee de arriba abajo y alterna tres tipos de celda: texto que explica, celdas `%%modulo` con el código y
celdas que usan ese código y muestran resultados. Las gráficas que generan quedan en `2_Notebooks/figuras/`.

| Notebook | Partes | Módulos de código que trae |
|---|---|---|
| `1_Datos_y_arquitectura` | Manifiesto, descarga, Spark, limpieza de 12 fuentes, consultas sobre 6.1 millones de negocios, almacén DuckDB, diccionario, huecos | 20 |
| `2_Donde_y_cuando` | A. Planteamiento · B. Radar · C. Pronóstico | 16 |
| `3_Presupuesto_y_Torre_en_vivo` | A. Presupuesto (IO) · B. Torre en vivo (Spark Structured Streaming) | 10 |
| `4_Campana` | Minería de texto, personas, marca, anuncios, medios, calendario, indicadores | 3 |

### Los datos (`datos/`)

| Carpeta | Contenido | Tamaño |
|---|---|---|
| `silver/` | Las 14 tablas limpias en Parquet: DENUE (6,138,075 negocios), clima diario y horario, nacionalidades, reseñas, INAH, huracanes, ocupación hotelera, vuelos, tipo de cambio, SITUR-Q, cruceros y Censo 2020 | 360 MB |
| `gold/` | Los resultados de los modelos (Radar, Pronóstico, presupuesto, Torre y campaña) y el modelo estrella | 4 MB |
| `bronze/` | El manifiesto de los 353 archivos descargados, las tablas de costos de anuncios (con sus capturas de evidencia) y el mapa de municipios | 20 MB |
| `DICCIONARIO.md` | Cada tabla y columna, con tipo, porcentaje de vacíos, un ejemplo real y su significado | |

### Las fuentes

Solo fuentes oficiales o abiertas, descargadas con programas y sin modificar. No se usó nada copiado de Google Maps ni de
TripAdvisor, porque sus términos de uso lo prohíben.

| Fuente | Quién la publica | Para qué se usó |
|---|---|---|
| SITUR-Q | Gobierno de Quintana Roo | Tren Maya, cruces desde Belice, cruceros, cuartos y ocupación hasta 2024 |
| DataTur | SECTUR | Ocupación semanal, visitantes del INAH, nacionalidades, vuelos (AFAC), cruceros, Compendio 2024 |
| DENUE, Censo 2020 (ITER), ENDUTIH 2025 | INEGI | Negocios, población por localidad y uso de internet |
| HURDAT2 | NOAA | Tormentas del Atlántico desde 1851 |
| Open-Meteo (reanálisis ERA5) | Open-Meteo | Clima diario desde 1950 y horario desde 2019 |
| FRED | Banco de la Reserva Federal de San Luis | Tipo de cambio e inflación de EE. UU. |
| Rest-Mex 2025 | Concurso académico, licencia CC BY 4.0 | 85,987 reseñas de Quintana Roo |
| WordStream y LocaliQ | Publicaciones abiertas (promedios de EE. UU.) | Costo por clic y conversión de anuncios de viajes |
| Wikimedia Commons | Autores individuales, licencias CC | Fotos de la página, cada una con su crédito y su ubicación comprobada |

---

## Por qué está hecho así

### Por qué cuatro notebooks con el código adentro

Construimos el proyecto como un paquete de Python (`torre`) con un archivo por tarea, para poder probar cada pieza por separado. Para la entrega juntamos ese código en cuatro notebooks: cada celda que empieza con `%%modulo` trae completo un
archivo del paquete y, al correrla, queda registrada como ese módulo. Así los notebooks usan **exactamente** el mismo
código que el proyecto y dan las mismas cifras, sin archivos `.py` sueltos. Descartamos reescribir el código a mano dentro de los notebooks, porque habría dos versiones que se separan con el primer cambio.

### Por qué no viene el crudo

Pesa 814 MB y se puede volver a descargar: el manifiesto guarda la dirección y la huella de cada archivo. Las tablas limpias (360 MB) alcanzan para correr todos los notebooks, así que dejamos fuera el crudo.

### Por qué no inventamos datos

Cuando un dato no existe (la ocupación hotelera del sur desde 2025, la conversión de Facebook para turismo, las reseñas de
los cinco lugares), lo declaramos como hueco o lo probamos como supuesto con varios valores. La lista completa está en el
capítulo "Lo que no se sabe" de la guía sencilla y en el capítulo de límites de la guía técnica.

### Cómo trabajamos

Hicimos el proyecto en 12 fases, una a la vez. En cada decisión de fondo pusimos sobre la mesa opciones con su evidencia
y elegimos una; todas están en `1_Documentos/3_Decisiones_fase_por_fase.pdf`. Para programar usamos un asistente de
programación con inteligencia artificial (Claude Code) como herramienta, con reglas que fijamos desde el inicio: no
inventar datos, explicar cada decisión con una cifra real y decidir siempre entre opciones. Las decisiones, la revisión y
la defensa del proyecto son del equipo.

---

## Créditos y licencias

- Datos: de sus fuentes oficiales (tabla de arriba). Rest-Mex 2025 se usa bajo licencia CC BY 4.0.
- Fotos de la página: Wikimedia Commons, con el autor y la licencia de cada una junto a la foto.
- Letras: Bricolage Grotesque, Figtree y Noto Sans (licencia SIL Open Font License).
- `herramientas/hadoop`: winutils y hadoop.dll 3.3.6 (Apache License 2.0), necesarios para que Spark escriba en Windows.
