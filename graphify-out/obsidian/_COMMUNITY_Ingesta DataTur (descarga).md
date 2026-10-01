---
type: community
members: 12
---

# Ingesta DataTur (descarga)

**Members:** 12 nodes

## Members
- [[Cuenta las filas de todas las hojas de los Excel dentro de un zip (o de un…]] - rationale - backend/torre/base/ingesta_datatur.py
- [[Descarga todos los archivos de las categorías pedidas y los registra en el…]] - rationale - backend/torre/base/ingesta_datatur.py
- [[Devuelve las rutas de los .zip.xlsx publicados en una página de DataTur, sin…]] - rationale - backend/torre/base/ingesta_datatur.py
- [[Variación interanual ene–jul (Δ%)]] - concept - docs/metodologia/ECUACIONES.md
- [[contar_filas()]] - code - backend/torre/base/ingesta_datatur.py
- [[descargar_datatur()]] - code - backend/torre/base/ingesta_datatur.py
- [[enlaces_de()]] - code - backend/torre/base/ingesta_datatur.py
- [[filas_xlsx()]] - code - backend/torre/base/ingesta_datatur.py
- [[ingesta_datatur.py]] - code - backend/torre/base/ingesta_datatur.py
- [[io]] - concept
- [[openpyxl]] - concept
- [[requests]] - concept

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Ingesta_DataTur_descarga
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Ingesta SITUR-Q y costos publicitarios]]
- 3 edges to [[_COMMUNITY_silver_datatur_ocupacion.py]]
- 2 edges to [[_COMMUNITY_ingesta_abiertas.py]]
- 1 edge to [[_COMMUNITY_ingesta_fotos.py]]
- 1 edge to [[_COMMUNITY_03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]]
- 1 edge to [[_COMMUNITY_pdf.py]]
- 1 edge to [[_COMMUNITY_silver_inah.py]]
- 1 edge to [[_COMMUNITY_Regresión logística multiclase (modelo elegido del Radar)]]

## Top bridge nodes
- [[ingesta_datatur.py]] - degree 14, connects to 4 communities
- [[io]] - degree 4, connects to 3 communities
- [[requests]] - degree 4, connects to 3 communities
- [[descargar_datatur()]] - degree 5, connects to 1 community
- [[Variación interanual ene–jul (Δ%)]] - degree 2, connects to 1 community