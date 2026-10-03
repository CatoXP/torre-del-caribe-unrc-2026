# Torre del Caribe

Campaña publicitaria inteligente para redistribuir los flujos turísticos de **Quintana Roo**, sustentada en
ciencia de datos. Problema Prototípico de 5° semestre, Licenciatura en Ciencias de Datos para Negocios
(UNRC), semestre 2026-2.

Autor: **Brandon Uriel García Sánchez**. Equipo: Maribel Mondragón Mercado, Jesús Ramírez Isidro y Enrique González Ortega.

**Página en línea:** https://catoxp.github.io/torre-del-caribe-unrc-2026/ (se publica sola desde `frontend/` con GitHub Pages).

## Por dónde empezar
**Para entregar a los profesores: la carpeta `Entregable/`** (no va a git por los datos; se genera con
`cd backend && ..\.venv\Scripts\python -m torre.documento.entregable`). Tiene:
- `1_Documentos/`: las tres guías en PDF (la técnica, fórmula por fórmula con cada ejemplo resuelto a mano; la sencilla;
  y las decisiones de las 12 fases), el documento ejecutivo y los documentos de respaldo;
- `2_Notebooks/`: cuatro notebooks autosuficientes ya ejecutados (.ipynb y .html), con el código del proyecto dentro;
- `3_Pagina_web/`: la página, que se abre sin internet;
- `datos/`: las tablas limpias, los resultados y el manifiesto de lo descargado.

Las guías se escriben en LaTeX en [`docs/latex/`](docs/latex/) (`bash compilar.sh`, con MiKTeX) y sus cifras las vigila
`tests/test_guias.py`. Los cambios se hacen en este proyecto y la carpeta se vuelve a generar; nunca se edita a mano.

1. [`OBJETIVO.md`](OBJETIVO.md): qué se pidió, textual, y las reglas del proyecto.
2. [`docs/plan/PLAN_v3.md`](docs/plan/PLAN_v3.md): el plan aprobado (Radar + Pronóstico + Torre en vivo).
3. [`docs/datos/INVENTARIO.md`](docs/datos/INVENTARIO.md): de dónde sale cada dato.
4. [`docs/regiones/REGIONES.md`](docs/regiones/REGIONES.md): qué regiones se promueven y por qué.
5. [`docs/decisiones/`](docs/decisiones/): el porqué de cada decisión.
6. [`docs/ejecutivo/DOCUMENTO_EJECUTIVO.md`](docs/ejecutivo/DOCUMENTO_EJECUTIVO.md): explicación no técnica del proyecto (estilo UNRC).

## Estado
- [x] Plan aprobado y documentos fuente escritos (27-sep-2026)
- [x] Fase 0 — entorno: PySpark 3.5.6 + Java 17 + winutils; prueba de humo en verde (27-sep-2026, `docs/decisiones/02-entorno.md`)
- [x] Fase 1 — ingesta: 353 archivos oficiales, 8,134,802 registros, 824 MB; 11 pruebas en verde; D13 y sargazo cerrados con Playwright (28-sep-2026, `docs/decisiones/03-ingesta.md`)
- [x] Fase 2 — almacén y calidad: las 14 fuentes en Silver (PySpark), almacén DuckDB con modelo estrella y diccionario de datos (02-oct-2026, `docs/decisiones/04-silver.md`, `10-silver-fase5.md`, `18-cierre-fase-2.md`)
- [x] Fase 3 — planteamiento con datos (cerrada 02-oct-2026); las 5 regiones pasan los criterios y el notebook 01 mide variables, actores y concentración (`docs/decisiones/05-planteamiento.md`)
- [ ] Página web — en paralelo (decisión de Brandon), sistema "Sur mexicano": portada, el dato, los 5 lugares en mapa 3D, cómo llega la gente, dónde se queda el dinero, el norte como referencia, las 12 fases, quiénes somos y preguntas rápidas (`frontend/`, `docs/decisiones/06-pagina.md` y `07-diseno.md`)
- [x] Fase 4 — Radar (cerrada 02-oct-2026); índice de presión (con llegadas por cuarto), predicción del mes siguiente (regresión logística), Markov del norte, clustering de 55 centros del país y sección en la página (`docs/decisiones/08-radar.md`)
- [x] Fase 5 — Pronóstico (cerrada 01-oct-2026): series, forma del año, 5 modelos en origen móvil, rango del 90 %, Poisson + Monte Carlo y planeador (`docs/decisiones/11-pronostico.md`, `12`–`15`)
- [x] Fase 6 — Reparto del presupuesto (02-oct-2026): modelo estocástico de dos etapas con PuLP/CBC; 957 visitantes con $250,000 al año; las reglas ambientales no cuestan visitantes (`docs/decisiones/19-presupuesto.md`)
- [x] Fase 7 — Torre en vivo (02-oct-2026): 239 semanas reproducidas con Spark Structured Streaming; 48 pausas; "¿Ibas al norte?" 6 semanas (`docs/decisiones/20-torre-en-vivo.md`)
- [x] Fase 8 — Campaña "El sur tiene espacio" (02-oct-2026): 2 personas con datos, 5 anuncios con respaldo y 10 KPI (`docs/decisiones/21-campana.md`)
- [x] Fase 9 — Servidor FastAPI: 8 endpoints, optimizador en vivo (< 0.3 s), SSE y consulta de solo lectura (`docs/decisiones/22-backend.md`)
- [x] Fase 10 — Página final auditada con axe-core (WCAG 2.1 AA): 0 fallas en 4 vistas; sin prueba con personas (declarado, `docs/decisiones/23-pagina-final.md`)
- [x] Fase 11 — Cierre: trazabilidad, mapa del informe, guion del coloquio con los 4 integrantes (`docs/decisiones/24-cierre.md`)
- Auditoría de las Fases 1–4: todo se reproduce y las cifras de los documentos coinciden con el código (`docs/decisiones/09-auditoria-fases-1-4.md`)
- 279 pruebas en verde (`tests/`), incluidas las que comparan las cifras de los documentos (`test_documentos.py`) y de las guías (`test_guias.py`) con el cálculo

## Cómo correrlo
```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
winget install Microsoft.OpenJDK.17      # una sola vez (pide permiso de administrador)
.venv\Scripts\python -m pytest -v        # prueba de humo de Spark
```

### Fase 1 — descargar las fuentes oficiales a `datos/bronze/`
```bash
set PYTHONPATH=backend
.venv\Scripts\python -m torre.base.ingesta_siturq      # SITUR-Q (~20 min)
.venv\Scripts\python -m torre.base.ingesta_datatur     # DataTur (171 archivos)
.venv\Scripts\python -m torre.base.ingesta_abiertas    # Rest-Mex, DENUE, ITER, clima, huracanes, FRED, ENDUTIH, mapa
.venv\Scripts\python -m playwright install chromium    # una sola vez: navegador para páginas que bloquean descargas
.venv\Scripts\python -m torre.base.ingesta_benchmarks   # costos publicitarios (WordStream / LocaliQ) con capturas
.venv\Scripts\python -m torre.base.evidencia_sargazo    # evidencia pública del sargazo en la Bahía de Chetumal
.venv\Scripts\python -m pytest tests -v                # huellas + cifras oficiales conocidas
.venv\Scripts\python -m torre.documento.figuras        # gráficas del documento ejecutivo
```

### Fase 2 — limpiar y ordenar los datos (`datos/silver/`, `datos/gold/`) · cerrada
```bash
.venv\Scripts\python -m torre.base.silver_siturq             # SITUR-Q en formato largo (PySpark)
.venv\Scripts\python -m torre.base.silver_datatur_ocupacion  # ocupación DataTur 2022–2026 (PySpark)
.venv\Scripts\python -m torre.base.silver_denue             # 6.1 millones de negocios del país (PySpark, ~1.5 min)
.venv\Scripts\python -m torre.base.silver_inah              # visitantes INAH por zona y mes (PySpark)
.venv\Scripts\python -m torre.base.silver_iter              # Censo 2020 por localidad (PySpark)
.venv\Scripts\python -m torre.base.silver_huracanes         # HURDAT2 1851–2025 con distancia a Chetumal (PySpark)
.venv\Scripts\python -m torre.base.silver_clima             # clima diario 1950–2026 y horario 2019–2026, 8 puntos (PySpark)
.venv\Scripts\python -m torre.base.silver_fred              # tipo de cambio diario y mensual + inflación EE. UU. (PySpark)
.venv\Scripts\python -m torre.base.silver_nacionalidad      # extranjeros por avión, aeropuerto y país 2012–2026 (PySpark)
.venv\Scripts\python -m torre.base.silver_afac              # pasajeros por aerolínea 2016–2026, duplicados resueltos (PySpark)
.venv\Scripts\python -m torre.base.silver_cruceros          # cruceros por puerto + conciliación con SITUR-Q (PySpark)
.venv\Scripts\python -m torre.base.silver_restmex           # 207,873 reseñas Rest-Mex (PySpark lee el CSV directo)
.venv\Scripts\python -m torre.base.almacen                  # almacén DuckDB: vistas + dim_lugar, dim_tiempo, hechos_mes
.venv\Scripts\python -m torre.base.diccionario              # docs/datos/DICCIONARIO.md (44 tablas)
.venv\Scripts\python -m pytest tests\test_silver.py -v       # reglas de limpieza con cifras conocidas
```

### Fase 3 — planteamiento con datos · cerrada
```bash
.venv\Scripts\python -m torre.radar.criterios               # tabla de criterios de las 5 regiones → datos/gold/criterios_regiones.parquet
.venv\Scripts\python notebooks\_construir_01_planteamiento.py  # notebook 01: variables, actores y concentración (lo ejecuta completo)
```

### Fase 4 — Radar · cerrada
```bash
cd backend && ..\.venv\Scripts\python -m torre.radar.panel   # panel mensual 15 lugares × meses → datos/gold/radar_panel_mensual.parquet
cd backend && ..\.venv\Scripts\python -m torre.radar.indice  # índice de presión, estados y sensibilidad → datos/gold/radar_estado.parquet
cd backend && ..\.venv\Scripts\python -m torre.radar.prediccion  # índice comparable + modelos vs persistencia + predicción del mes siguiente
cd backend && ..\.venv\Scripts\python -m torre.radar.markov      # cadena de Markov semanal del norte: riesgo de saturarse a 1–8 semanas
cd backend && ..\.venv\Scripts\python -m torre.radar.clustering  # clustering jerárquico de los 55 centros turísticos del país (DataTur)
.venv\Scripts\python notebooks\_construir_02_radar.py              # notebook 02: el Radar completo, narrado (lo ejecuta todo)
cd backend && ..\.venv\Scripts\python -m torre.api.datos_pagina  # agrega "radar" a pagina.js → la sección aparece sola
```

### Fase 5 — Pronóstico (`datos/gold/pronostico_*`) · cerrada
```bash
cd backend
..\.venv\Scripts\python -m torre.pronostico.series       # series a pronosticar y meses que no entrenan
..\.venv\Scripts\python -m torre.pronostico.forma        # forma del año y fuerza de la temporada
..\.venv\Scripts\python -m torre.pronostico.modelos      # 5 modelos en origen móvil (~1.5 min)
..\.venv\Scripts\python -m torre.pronostico.intervalos   # rango del 90 % y cobertura real
..\.venv\Scripts\python -m torre.pronostico.seleccion    # modelo elegido y pronóstico de 12 meses
..\.venv\Scripts\python -m torre.pronostico.escenarios   # Poisson de tormentas, Monte Carlo y sensibilidad
..\.venv\Scripts\python -m torre.pronostico.calendario   # planeador: temporada alta y recomendación por lugar y mes
..\.venv\Scripts\python -m torre.campana.lugares         # NLP por léxico sobre el DENUE: qué hacer, comer y dormir
```

### Fase 6 — Reparto del presupuesto (`datos/gold/presupuesto_*`) · lista
```bash
cd backend
..\.venv\Scripts\python -m torre.campana.presupuesto     # modelo de dos etapas (PuLP/CBC), costo de reglas, Pareto y sensibilidad
cd ..
.venv\Scripts\python notebooks\_construir_05_optimizacion.py   # notebook narrado 05
```

### Fase 7 — Torre en vivo (`datos/gold/envivo_*`) · lista
```bash
cd backend
..\.venv\Scripts\python -m torre.envivo.senales   # 239 semanas: norte, tormentas, clima raro (Isolation Forest), llegadas
..\.venv\Scripts\python -m torre.envivo.torre     # Spark Structured Streaming: una semana por lote + motor de reglas
cd ..
.venv\Scripts\python notebooks\_construir_06_torre_en_vivo.py   # notebook narrado 06
```

### Fase 8 — La campaña (`datos/gold/campana*`) · lista
```bash
cd backend
..\.venv\Scripts\python -m torre.campana.texto   # minería de 85,987 reseñas: temas, Apriori y palabras (log-odds)
..\.venv\Scripts\python -m torre.campana.marca   # personas, marca, 5 anuncios con respaldo, medios, calendario y 10 KPI
cd ..
.venv\Scripts\python notebooks\_construir_07_campana.py   # notebook narrado 07
```

### Fase 9 — Servidor que conecta la página con los modelos · lista
```bash
cd backend
..\.venv\Scripts\python -m torre.api.servidor   # http://127.0.0.1:8000 · documentación de la API en /docs
```
Con el servidor aparecen "Pruébalo tú" (presupuesto resuelto en vivo) y "Escuchar en vivo" (la Torre por SSE). Sin él,
la página funciona igual con `frontend/datos/pagina.js`.

### Fases 10 y 11 — Auditoría y cierre
```bash
cd backend && ..\.venv\Scripts\python -m torre.documento.auditoria   # axe-core en 4 vistas → docs/ejecutivo/AUDITORIA_PAGINA.md
```
Cierre: `docs/trazabilidad.md` · `docs/informe/MAPA_INFORME.md` · `docs/coloquio/GUION_COLOQUIO.md`.

### Página web (`frontend/`)
```bash
cd backend && ..\.venv\Scripts\python -m torre.base.ubicaciones     # comprueba que los 5 lugares estén en Quintana Roo
cd backend && ..\.venv\Scripts\python -m torre.base.ingesta_fotos   # fotos con licencia libre (Wikimedia Commons)
cd backend && ..\.venv\Scripts\python -m torre.campana.estrellas      # estrellas oficiales de Cancún y Playa del Carmen (DataTur 5_2)
cd backend && ..\.venv\Scripts\python -m torre.campana.vitrina        # postales, 6 experiencias y 3 rutas (decisión 16)
cd backend && ..\.venv\Scripts\python -m torre.campana.aportes        # fotos y reseñas del equipo (docs/aportes/LEEME.md)
cd backend && ..\.venv\Scripts\python -m torre.campana.idiomas        # 8 diccionarios desde docs/idiomas/*.tsv, con revisión de marcas
cd backend && ..\.venv\Scripts\python -m torre.campana.fotos_lugares # 40 fotos: 5 lugares + Cancún y Riviera Maya (coordenada comprobada en su municipio)
cd backend && ..\.venv\Scripts\python -m torre.api.datos_pagina   # saca de Silver las cifras de la página → frontend/datos/pagina.js
```
Después se abre `frontend/index.html` con doble clic: funciona sin internet y sin servidor (las fuentes Bricolage Grotesque y Figtree están en `frontend/fuentes/` y el motor de texto Pretext en `frontend/vendor/`). Las secciones de fases futuras se llenan solas cuando `pagina.js` trae su clave
(contrato en `docs/decisiones/06-pagina.md`). Ninguna cifra está escrita
a mano en el HTML; todas vienen de `pagina.js`, con su fuente y su periodo.

### Documentos en PDF
```bash
.venv\Scripts\python -m torre.documento.pdf    # regenera el documento ejecutivo en PDF (Documento_Ejecutivo_Torre_del_Caribe.pdf)
```
Los pasos de cada fase siguiente se agregan aquí al cerrarla.
