# 03 — Ingesta de fuentes oficiales (Fase 1: Bronze)

Autor: **Brandon Uriel García Sánchez** · 28-sep-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Decisión
Todas las fuentes del inventario se descargan con código reproducible a `datos/bronze/<fuente>/<fecha>/`, sin
modificarlas, y cada archivo queda en `datos/bronze/MANIFIESTO.csv` con:
- su huella SHA-256,
- su tamaño,
- su URL de origen,
- la fecha de descarga,
- su número de registros.

## Resultado (conteos reales del manifiesto)
| Fuente | Archivos | Registros | MB |
|---|---:|---:|---:|
| D6 DENUE INEGI (32 estados) | 33 | 6,138,075 | 574.2 |
| D8 Open-Meteo (8 puntos; horario 2019→, diario 1950→) | 128 | 767,016 | 24.5 |
| D3 DataTur BD_Nacionalidad | 1 | 521,364 | 19.0 |
| D4 DataTur Compendio 2024 | 1 | 295,191 | 31.3 |
| D5 Rest-Mex 2025 | 1 | 208,051 | 89.0 |
| D4 DataTur BdINAH | 1 | 71,562 | 3.1 |
| D9 HURDAT2 NOAA | 1 | 57,512 | 7.1 |
| D2 DataTur ocupación hotelera (135 semanas + 31 meses) | 166 | 34,164 | 67.8 |
| D4 DataTur DB_AFAC | 1 | 19,578 | 0.7 |
| D10 FRED | 2 | 9,531 | 0.2 |
| D1 SITUR-Q (13 indicadores × 15 unidades × 2019–2026) | 14 | 6,607 | 3.2 |
| D4 DataTur cruceros | 1 | 3,897 | 0.2 |
| D7 Censo 2020 ITER Q. Roo | 1 | 2,243 | 0.3 |
| D11 ENDUTIH 2025 (PDF) | 1 | — | 2.0 |
| D12 GeoJSON Q. Roo | 1 | 11 | 1.5 |
| **Total** | **353** | **8,134,802** | **824.1** |

En DataTur, DENUE e ITER los conteos son "crudos": incluyen encabezados y notas de los Excel. El conteo limpio se hace
en Silver (Fase 2).

## Corrección del 28-sep-2026 (conteo)
En la Fase 2, Spark contó **6,138,075** negocios en el DENUE, contra 6,139,989 del conteo original de esta fase. Un
lector CSV independiente confirmó la cifra de Spark. La causa: cada zip del DENUE incluye un CSV con el diccionario de
datos (58 líneas) y la función de conteo lo sumaba como si fueran negocios (33 zips × 58 = 1,914). El Censo ITER tenía el
mismo error: 2,547 → 2,257 localidades (290 líneas de su diccionario). Se corrigió la función para excluir el
diccionario, el manifiesto y todas las cifras de este documento (total de ese momento: 8,134,816). Los archivos
descargados nunca estuvieron mal; solo el conteo.

**Segunda corrección (28-sep-2026, al abrir la Fase 3).** Al construir el Censo en Silver salieron 2,243 filas, no
2,257. La función corregida excluía el diccionario, pero seguía sumando el catálogo `catalogos/tam_loc.csv.csv` del
ITER (14 filas). Ahora `_filas_csv_en_zip` cuenta **solo** la carpeta `conjunto_de_datos`. El DENUE no cambia: sus zips
solo traen el diccionario y los datos. Cifras correctas: ITER **2,243** localidades y Fase 1 con **353 archivos y
8,134,802 registros**.

## Pruebas (11 de 11 en verde)
- **Huellas:** los 353 archivos coinciden con su SHA-256 registrado.
- **Cifras que ya se conocían y se reprodujeron:**
  - Bacalar ene-2024 = 66.5 % de ocupación
  - Tren Maya Gran Costa Maya ene-2025 = 14,437
  - Bacalar ene-2025 = 145 hoteles
  - Rest-Mex = 208,051 reseñas
  - Z.A. Tulum 2025 = 1,031,443 visitantes
  - 11 municipios en el GeoJSON
  - los 32 estados en DENUE
  - WordStream Google Ads 2025, categoría Travel: costo por clic de $2.12 y CTR de 8.73 %

Cómo se reproducen: `.venv\Scripts\python -m pytest tests -v`.

## Hallazgos que cambian el plan
1. **SITUR-Q no publica ocupación hotelera de 2025–2026 para ningún destino**, ni siquiera Cancún (figura
   `docs/ejecutivo/figuras/f02_cobertura_ocupacion_siturq.png`). Antes se creía que el hueco era solo del sur.
   Para 2025–2026, la ocupación medida existe **solo en DataTur semanal**, y solo para los 7 centros del norte.
   La Fase 3 decide cómo tratarlo para todos los destinos.
2. **Afluencia de turistas y derrama en SITUR-Q** van de 2021 a marzo de 2024.
3. **El indicador "Turista - Afluencia" de SITUR-Q está roto del lado del servidor:** las 120 de 120 consultas
   devolvieron error 500. Se guardó como hueco con el error exacto. El indicador "Afluencia de turistas" sí trae los datos.
4. **Tren Maya** trae 2 registros por mes en algunos destinos (probablemente uno por estación). Se agrega en Silver.

## Problemas encontrados y cómo se resolvieron
| Problema | Causa | Solución |
|---|---|---|
| La API de SITUR-Q respondía "Origin not allowed" | Solo acepta peticiones que vienen de su página | Se envían los mismos encabezados que el navegador (Origin y Referer) |
| La descarga de SITUR-Q se detuvo en un indicador | Error 500 repetido del servidor | Una consulta fallida se guarda como hueco y la descarga continúa |
| DENUE falló en el estado 15 | El Estado de México se publica en dos partes (`denue_15_1`, `denue_15_2`) | El código busca las partes cuando no existe el archivo único y revisa que cada descarga sea un zip real |
| Open-Meteo respondió 429 (demasiadas peticiones) | Pedir 7.7 años horarios de golpe rebasa el límite gratuito | Se pide un año (horario) o una década (diario) por consulta y, si hay 429, se espera y se reintenta |
| Dos archivos de clima duplicados | Quedaron del primer intento | Se eliminaron del disco y del manifiesto para no contar datos dos veces |

## Pendientes del plan cerrados el 28-sep-2026 (con Playwright)
**D13, costos por canal publicitario.** `backend/torre/base/ingesta_benchmarks.py` abre las 4 páginas con un navegador
automatizado (Playwright + Chromium) y guarda el HTML, una captura de página completa (evidencia) y todas las tablas.
Resultado: 386 filas de 23 industrias en `datos/bronze/benchmarks/2026-09-28/benchmarks_tablas.csv`.

| Categoría Travel | Costo por clic | Tasa de clics (CTR) | Tasa de conversión | Costo por lead |
|---|---:|---:|---:|---:|
| WordStream, Google Ads 2025 | $2.12 | 8.73 % | 5.75 % | $73.70 |
| LocaliQ, búsqueda 2026 | $2.14 | 9.32 % | 5.83 % | $44.70 |
| WordStream, Facebook Ads 2025 (campañas de tráfico) | $0.51 | 2.76 % | — | — |
| LocaliQ, Facebook Ads 2026 (campañas de tráfico) | $0.42 | 2.28 % | — | — |

- **Corrección:** un resumen de búsqueda web decía que el CTR de Travel en Google era 8.24 %. La tabla oficial dice
  **8.73 %**. Por eso se extrae de la fuente original.
- **Hueco declarado:** las tablas de conversión de Facebook (campañas de captación) **no incluyen la categoría
  Travel**. La conversión de Facebook para turismo no está publicada; se decide cómo tratarla en la Fase 6.
- **Limitación:** son promedios de anunciantes de EE. UU. En el modelo se usan como supuesto etiquetado.

**Sargazo en la Bahía de Chetumal.** El semáforo oficial diario (CEMAS/SEMA) solo se publica en Facebook, cuyos
términos prohíben extraerlo de forma automática: `sema.qroo.gob.mx` redirige a `qroo.gob.mx/sema/`, que no lo contiene.
Por eso `backend/torre/base/evidencia_sargazo.py` guarda como evidencia (HTML, captura y párrafos) las publicaciones
públicas. Estado al 28-sep-2026:
- **ECOSUR** (El Colegio de la Frontera Sur, Chetumal) confirma sargazo en los **canales de entrada a la bahía**: el
  Canal de Zaragoza y el río Bacalar Chico, en la frontera con Belice.
- **Reportur (28-sep)** cita a una bióloga: las acumulaciones "podrían desplazarse hacia áreas más cercanas a
  Chetumal", pero "el monitoreo determinará si es temporal".
- **No hay reporte de sargazo en la costa de la ciudad de Chetumal ni en Calderitas.**
- Conclusión: Chetumal y Calderitas–Oxtankah **siguen como destinos, con vigilancia**. Si se confirma sargazo en su
  costa, la Torre en vivo (A5) pausa su promoción.

## Opciones descartadas
- **Exportar a mano desde las páginas:** no es reproducible.
- **Descargar solo Quintana Roo de DENUE:** el criterio 2 de la rúbrica pide volumen real, y el total nacional da contexto.
- **Limpiar los datos mientras se descargan:** Bronze debe ser idéntico a la fuente; la limpieza va en Silver.

## Código
- `backend/torre/base/manifiesto.py`
- `backend/torre/base/ingesta_siturq.py`
- `backend/torre/base/ingesta_datatur.py`
- `backend/torre/base/ingesta_abiertas.py`
- `backend/torre/base/ingesta_benchmarks.py` (Playwright: costos publicitarios D13)
- `backend/torre/base/evidencia_sargazo.py` (Playwright: evidencia del sargazo en la Bahía de Chetumal)
- `tests/test_ingesta.py`
