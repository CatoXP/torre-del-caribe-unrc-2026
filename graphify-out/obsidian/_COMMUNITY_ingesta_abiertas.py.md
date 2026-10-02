---
type: community
members: 23
---

# ingesta_abiertas.py

**Members:** 23 nodes

## Members
- [[Clima de 8 puntos (reanálisis ERA5 vía Open-Meteo), en partes pequeñas para…]] - rationale - backend/torre/base/ingesta_abiertas.py
- [[Como _bajar, pero si Open-Meteo responde 429 (demasiadas peticiones) espera y…]] - rationale - backend/torre/base/ingesta_abiertas.py
- [[Corre cada fuente por separado; si una falla, se reporta y se sigue con las…]] - rationale - backend/torre/base/ingesta_abiertas.py
- [[Cuenta las filas de datos (sin encabezado) de los CSV de la carpeta…]] - rationale - backend/torre/base/ingesta_abiertas.py
- [[DENUE de los 32 estados. Los estados más grandes vienen divididos en partes.…]] - rationale - backend/torre/base/ingesta_abiertas.py
- [[Descarga una URL a un archivo (salvo que ya exista, para poder reanudar) y…]] - rationale - backend/torre/base/ingesta_abiertas.py
- [[HURDAT2 se toma el archivo más reciente publicado en el índice de la NOAA.]] - rationale - backend/torre/base/ingesta_abiertas.py
- [[Path]] - code
- [[Pregunta al servidor el tipo de archivo sin descargarlo. INEGI responde una…]] - rationale - backend/torre/base/ingesta_abiertas.py
- [[_bajar()]] - code - backend/torre/base/ingesta_abiertas.py
- [[_bajar_con_espera()]] - code - backend/torre/base/ingesta_abiertas.py
- [[_es_zip()]] - code - backend/torre/base/ingesta_abiertas.py
- [[_filas_csv_en_zip()]] - code - backend/torre/base/ingesta_abiertas.py
- [[clima()]] - code - backend/torre/base/ingesta_abiertas.py
- [[denue()_1]] - code - backend/torre/base/ingesta_abiertas.py
- [[descargar_abiertas()]] - code - backend/torre/base/ingesta_abiertas.py
- [[endutih()]] - code - backend/torre/base/ingesta_abiertas.py
- [[fred()]] - code - backend/torre/base/ingesta_abiertas.py
- [[geojson()]] - code - backend/torre/base/ingesta_abiertas.py
- [[huracanes()_1]] - code - backend/torre/base/ingesta_abiertas.py
- [[ingesta_abiertas.py]] - code - backend/torre/base/ingesta_abiertas.py
- [[iter_qroo()]] - code - backend/torre/base/ingesta_abiertas.py
- [[restmex()]] - code - backend/torre/base/ingesta_abiertas.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ingesta_abiertaspy
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_ingesta_datatur.py (manifiesto.py)]]
- 2 edges to [[_COMMUNITY_ingesta_datatur.py (ingesta_siturq.py)]]
- 1 edge to [[_COMMUNITY_requirements.txt]]
- 1 edge to [[_COMMUNITY_silver_datatur_ocupacion.py]]
- 1 edge to [[_COMMUNITY_entorno.py (silver_denue.py)]]
- 1 edge to [[_COMMUNITY_ingesta_datatur.py]]
- 1 edge to [[_COMMUNITY_numpy]]
- 1 edge to [[_COMMUNITY_03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]]

## Top bridge nodes
- [[ingesta_abiertas.py]] - degree 23, connects to 7 communities
- [[_filas_csv_en_zip()]] - degree 5, connects to 1 community