---
type: community
members: 2
---

# Prueba: cifras INAH

**Members:** 2 nodes

## Members
- [[Reproduce las cifras de docsregionesREGIONES.md D.4 (visitantes 2025).]] - rationale - tests/test_silver.py
- [[test_inah_cifras_de_la_seleccion_de_regiones()]] - code - tests/test_silver.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Prueba_cifras_INAH
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Pruebas Silver]]

## Top bridge nodes
- [[test_inah_cifras_de_la_seleccion_de_regiones()]] - degree 2, connects to 1 community