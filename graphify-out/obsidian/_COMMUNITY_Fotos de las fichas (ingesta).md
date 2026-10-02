---
type: community
members: 8
---

# Fotos de las fichas (ingesta)

**Members:** 8 nodes

## Members
- [[Fotos de Wikimedia Commons con licencia libre (fuente D15)]] - concept - docs/decisiones/06-pagina.md
- [[GET con reintentos Commons limita las consultas seguidas (visto el…]] - rationale - backend/torre/base/ingesta_fotos.py
- [[_limpiar()_1]] - code - backend/torre/base/ingesta_fotos.py
- [[_pedir()_1]] - code - backend/torre/base/ingesta_fotos.py
- [[_slug()_1]] - code - backend/torre/base/ingesta_fotos.py
- [[descargar_fotos()]] - code - backend/torre/base/ingesta_fotos.py
- [[hashlib]] - concept
- [[ingesta_fotos.py]] - code - backend/torre/base/ingesta_fotos.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Fotos_de_las_fichas_ingesta
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_fotos_lugares.py]]
- 2 edges to [[_COMMUNITY_Fotos comprobadas de los lugares]]
- 2 edges to [[_COMMUNITY_ingesta_datatur.py (manifiesto.py)]]
- 1 edge to [[_COMMUNITY_entorno.py]]
- 1 edge to [[_COMMUNITY_Fotos pruebas de ubicación]]
- 1 edge to [[_COMMUNITY_ingesta_datatur.py (ingesta_siturq.py)]]
- 1 edge to [[_COMMUNITY_ingesta_datatur.py]]

## Top bridge nodes
- [[ingesta_fotos.py]] - degree 12, connects to 5 communities
- [[hashlib]] - degree 4, connects to 3 communities
- [[descargar_fotos()]] - degree 5, connects to 1 community
- [[_pedir()_1]] - degree 4, connects to 1 community