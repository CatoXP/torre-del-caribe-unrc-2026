---
type: community
members: 18
---

# silver_datatur_ocupacion.py

**Members:** 18 nodes

## Members
- [[Crea una sesión de Spark local que usa todos los núcleos de la máquina.…]] - rationale - backend/torre/base/entorno.py
- [[Lee un zip de DataTur (semanal o mensual) y devuelve una fila por centro y año.]] - rationale - backend/torre/base/silver_datatur_ocupacion.py
- [[Número o None. 'n.d.'  'n.c.'  vacío → None.]] - rationale - backend/torre/base/silver_datatur_ocupacion.py
- [[Path_3]] - code
- [[SparkSession]] - code
- [[Variación interanual ene–jul (Δ%)]] - concept - docs/metodologia/ECUACIONES.md
- [[_numero()]] - code - backend/torre/base/silver_datatur_ocupacion.py
- [[construir_silver_ocupacion()]] - code - backend/torre/base/silver_datatur_ocupacion.py
- [[crear_spark()]] - code - backend/torre/base/entorno.py
- [[ingesta_datatur.py]] - code - backend/torre/base/ingesta_datatur.py
- [[io]] - concept
- [[leer_archivo()]] - code - backend/torre/base/silver_datatur_ocupacion.py
- [[openpyxl]] - concept
- [[pyspark_sql]] - concept
- [[re]] - concept
- [[silver_datatur_ocupacion.py]] - code - backend/torre/base/silver_datatur_ocupacion.py
- [[silver_denue.py]] - code - backend/torre/base/silver_denue.py
- [[zipfile]] - concept

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/silver_datatur_ocupacionpy
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_silver_denue.py]]
- 5 edges to [[_COMMUNITY_03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]]
- 4 edges to [[_COMMUNITY_Entorno Spark, JDK y prueba de humo]]
- 3 edges to [[_COMMUNITY_ingesta_siturq.py]]
- 3 edges to [[_COMMUNITY_descargar_datatur]]
- 3 edges to [[_COMMUNITY_pathlib]]
- 2 edges to [[_COMMUNITY_ingesta_abiertas.py]]
- 2 edges to [[_COMMUNITY_04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]]
- 2 edges to [[_COMMUNITY_silver_inah.py]]
- 2 edges to [[_COMMUNITY_Silver Censo (ITER)]]
- 1 edge to [[_COMMUNITY_Entorno búsqueda de JDK]]
- 1 edge to [[_COMMUNITY_Fotos y ubicación comprobada]]
- 1 edge to [[_COMMUNITY_Ingesta costos publicitarios y sargazo]]
- 1 edge to [[_COMMUNITY_test_silver_fase5.py]]

## Top bridge nodes
- [[re]] - degree 9, connects to 6 communities
- [[ingesta_datatur.py]] - degree 13, connects to 4 communities
- [[silver_datatur_ocupacion.py]] - degree 13, connects to 4 communities
- [[silver_denue.py]] - degree 9, connects to 4 communities
- [[crear_spark()]] - degree 8, connects to 3 communities