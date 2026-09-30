# Inventario de datos — fuentes oficiales verificadas

Autor: **Brandon Uriel García Sánchez** · extraído del plan v3 aprobado (`docs/plan/PLAN_v3.md`) el 27-sep-2026.

Cada fuente dice de dónde viene, qué campos trae, cómo se verificó y a qué módulo alimenta. Regla de oro: si un dato no está aquí, no existe para el proyecto.

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
| D15 | **Wikimedia Commons** (API oficial `commons.wikimedia.org/w/api.php`), agregada el 28-sep-2026 a petición de Brandon | Una foto de referencia por región, con licencia libre (CC BY 3.0 o CC BY-SA 4.0): autor, licencia, enlace y coordenada en `frontend/fotos/creditos.json` | Descargadas con `backend/torre/base/ingesta_fotos.py`; las que traen coordenada se comprobaron dentro de su municipio | Página (fichas de los 5 lugares). La licencia exige mostrar autor y licencia junto a la foto |

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

## Conteos reales tras la descarga (Fase 1, 28-sep-2026)
Los conteos por fuente, las huellas SHA-256 y los problemas encontrados están en `docs/decisiones/03-ingesta.md` y en
`datos/bronze/MANIFIESTO.csv`. En total: **353 archivos, 8,134,802 registros, 824 MB**.

**Corrección importante al hueco de ocupación:** SITUR-Q no tiene ocupación hotelera de 2025–2026 para **ningún**
destino (no solo el sur). Para esos años solo existe la ocupación semanal de DataTur de los 7 centros del norte.

## D13 extraído (28-sep-2026)
Valores de la categoría Travel y hueco de Facebook: ver `docs/decisiones/03-ingesta.md`, sección "Pendientes del plan
cerrados". Archivo: `datos/bronze/benchmarks/2026-09-28/benchmarks_tablas.csv` (386 filas, 23 industrias, con capturas).

## Cobertura real de DataTur (Fase 2, 28-sep-2026)
La ocupación hotelera de DataTur cubre de **enero de 2022 a julio de 2026**, no solo desde 2024: cada archivo compara
tres años del mismo periodo. La serie semanal limpia trae 239 semanas completas para cada uno de los 7 centros de
Quintana Roo. **Número de centros:** el primer archivo mensual revisado traía 54 centros. Al unir los 31 archivos
mensuales (con sus tres años cada uno) aparecen **96 centros** en el reporte mensual y 66 en el semanal, porque SECTUR
agregó ciudades con el tiempo. Detalle en `docs/decisiones/04-silver.md`.
