---
type: community
members: 11
---

# leer_archivo

**Members:** 11 nodes

## Members
- [[Lee un zip de DataTur (semanal o mensual) y devuelve una fila por centro y año.]] - rationale - backend/torre/base/silver_datatur_ocupacion.py
- [[Número o None. 'n.d.'  'n.c.'  vacío → None.]] - rationale - backend/torre/base/silver_datatur_ocupacion.py
- [[Path_8]] - code
- [[SparkSession_1]] - code
- [[_numero()]] - code - backend/torre/base/silver_datatur_ocupacion.py
- [[construir_silver_ocupacion()]] - code - backend/torre/base/silver_datatur_ocupacion.py
- [[io]] - concept
- [[leer_archivo()]] - code - backend/torre/base/silver_datatur_ocupacion.py
- [[pyspark_sql]] - concept
- [[silver_datatur_ocupacion.py]] - code - backend/torre/base/silver_datatur_ocupacion.py
- [[zipfile]] - concept

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/leer_archivo
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_silver_denue.py]]
- 3 edges to [[_COMMUNITY_ingesta_datatur.py]]
- 2 edges to [[_COMMUNITY_ingesta_abiertas.py]]
- 2 edges to [[_COMMUNITY_Ingesta costos publicitarios y sargazo]]
- 2 edges to [[_COMMUNITY_silver_inah.py]]
- 1 edge to [[_COMMUNITY_Censo (ITER) y criterios de regiones]]
- 1 edge to [[_COMMUNITY_buscar_jdk17]]
- 1 edge to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_04 - Limpieza y orden de los datos (Fase 2 Silver y Gold) (04 - Limpieza y orden de)]]
- 1 edge to [[_COMMUNITY_silver_siturq.py]]

## Top bridge nodes
- [[silver_datatur_ocupacion.py]] - degree 13, connects to 6 communities
- [[zipfile]] - degree 6, connects to 5 communities
- [[io]] - degree 4, connects to 3 communities
- [[pyspark_sql]] - degree 3, connects to 2 communities
- [[construir_silver_ocupacion()]] - degree 4, connects to 1 community