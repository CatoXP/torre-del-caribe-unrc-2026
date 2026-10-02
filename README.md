# Torre del Caribe

Campaña publicitaria inteligente para redistribuir los flujos turísticos de **Quintana Roo**, sustentada en
ciencia de datos. Problema Prototípico de 5° semestre, Licenciatura en Ciencias de Datos para Negocios
(UNRC), semestre 2026-2.

Autor: **Brandon Uriel García Sánchez**.

**Página en línea:** https://catoxp.github.io/torre-del-caribe-unrc-2026/ (se publica sola desde `frontend/` con GitHub Pages).

## Por dónde empezar
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
- [ ] Fase 2 — almacén y calidad (Silver/Gold con PySpark): **en curso**; SITUR-Q, DataTur, DENUE, INAH, Censo ITER, huracanes, clima y tipo de cambio listos (`docs/decisiones/04-silver.md`, `10-silver-fase5.md`)
- [ ] Fase 3 — planteamiento con datos: **lista para revisión**; las 5 regiones pasan los criterios y el notebook 01 mide variables, actores y concentración (`docs/decisiones/05-planteamiento.md`)
- [ ] Página web — en paralelo (decisión de Brandon), sistema "Sur mexicano": portada, el dato, los 5 lugares en mapa 3D, cómo llega la gente, dónde se queda el dinero, el norte como referencia, las 12 fases, quiénes somos y preguntas rápidas (`frontend/`, `docs/decisiones/06-pagina.md` y `07-diseno.md`)
- [ ] Fase 4 — Radar: **auditada y lista para revisión**; índice de presión (con llegadas por cuarto), predicción del mes siguiente (regresión logística), Markov del norte, clustering de 55 centros del país y sección en la página (`docs/decisiones/08-radar.md`)
- Auditoría de las Fases 1–4: todo se reproduce y las cifras de los documentos coinciden con el código (`docs/decisiones/09-auditoria-fases-1-4.md`)
- 104 pruebas en verde (`tests/`), incluida la que compara las cifras de los documentos con el cálculo

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

### Fase 2 — limpiar y ordenar los datos (`datos/silver/`, `datos/gold/`) · en curso
```bash
.venv\Scripts\python -m torre.base.silver_siturq             # SITUR-Q en formato largo (PySpark)
.venv\Scripts\python -m torre.base.silver_datatur_ocupacion  # ocupación DataTur 2022–2026 (PySpark)
.venv\Scripts\python -m torre.base.silver_denue             # 6.1 millones de negocios del país (PySpark, ~1.5 min)
.venv\Scripts\python -m torre.base.silver_inah              # visitantes INAH por zona y mes (PySpark)
.venv\Scripts\python -m torre.base.silver_iter              # Censo 2020 por localidad (PySpark)
.venv\Scripts\python -m torre.base.silver_huracanes         # HURDAT2 1851–2025 con distancia a Chetumal (PySpark)
.venv\Scripts\python -m torre.base.silver_clima             # clima diario 1950–2026 y horario 2019–2026, 8 puntos (PySpark)
.venv\Scripts\python -m torre.base.silver_fred              # tipo de cambio diario y mensual + inflación EE. UU. (PySpark)
.venv\Scripts\python -m pytest tests\test_silver.py -v       # reglas de limpieza con cifras conocidas
```

### Fase 3 — planteamiento con datos · en curso
```bash
.venv\Scripts\python -m torre.radar.criterios               # tabla de criterios de las 5 regiones → datos/gold/criterios_regiones.parquet
.venv\Scripts\python notebooks\_construir_01_planteamiento.py  # notebook 01: variables, actores y concentración (lo ejecuta completo)
```

### Fase 4 — Radar · lista para revisión
```bash
cd backend && ..\.venv\Scripts\python -m torre.radar.panel   # panel mensual 15 lugares × meses → datos/gold/radar_panel_mensual.parquet
cd backend && ..\.venv\Scripts\python -m torre.radar.indice  # índice de presión, estados y sensibilidad → datos/gold/radar_estado.parquet
cd backend && ..\.venv\Scripts\python -m torre.radar.prediccion  # índice comparable + modelos vs persistencia + predicción del mes siguiente
cd backend && ..\.venv\Scripts\python -m torre.radar.markov      # cadena de Markov semanal del norte: riesgo de saturarse a 1–8 semanas
cd backend && ..\.venv\Scripts\python -m torre.radar.clustering  # clustering jerárquico de los 55 centros turísticos del país (DataTur)
.venv\Scripts\python notebooks\_construir_02_radar.py              # notebook 02: el Radar completo, narrado (lo ejecuta todo)
cd backend && ..\.venv\Scripts\python -m torre.api.datos_pagina  # agrega "radar" a pagina.js → la sección aparece sola
```

### Fase 5 — Pronóstico (`datos/gold/pronostico_*`) · en curso
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

### Página web (`frontend/`)
```bash
cd backend && ..\.venv\Scripts\python -m torre.base.ubicaciones     # comprueba que los 5 lugares estén en Quintana Roo
cd backend && ..\.venv\Scripts\python -m torre.base.ingesta_fotos   # fotos con licencia libre (Wikimedia Commons)
cd backend && ..\.venv\Scripts\python -m torre.campana.fotos_comida  # 24 fotos de platillos (Commons, revisadas a ojo)
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
