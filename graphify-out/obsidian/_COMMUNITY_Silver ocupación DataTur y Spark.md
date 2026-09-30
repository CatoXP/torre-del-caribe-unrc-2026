---
type: community
members: 10
---

# Silver ocupación DataTur y Spark

**Members:** 10 nodes

## Members
- [[Lee un zip de DataTur (semanal o mensual) y devuelve una fila por centro y año.]] - rationale - backend/torre/base/silver_datatur_ocupacion.py
- [[Número o None. 'n.d.'  'n.c.'  vacío → None.]] - rationale - backend/torre/base/silver_datatur_ocupacion.py
- [[Path_9]] - code
- [[SparkSession_1]] - code
- [[_numero()]] - code - backend/torre/base/silver_datatur_ocupacion.py
- [[construir_silver_ocupacion()]] - code - backend/torre/base/silver_datatur_ocupacion.py
- [[leer_archivo()]] - code - backend/torre/base/silver_datatur_ocupacion.py
- [[openpyxl]] - concept
- [[pyspark_sql]] - concept
- [[silver_datatur_ocupacion.py]] - code - backend/torre/base/silver_datatur_ocupacion.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Silver_ocupación_DataTur_y_Spark
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Entorno Spark en Windows]]
- 2 edges to [[_COMMUNITY_Silver SITUR-Q y DENUE]]
- 2 edges to [[_COMMUNITY_Ingesta y Silver DataTur]]
- 1 edge to [[_COMMUNITY_Ingesta SITUR-Q]]
- 1 edge to [[_COMMUNITY_Silver ocupación DataTur y Spark (pathlib)]]
- 1 edge to [[_COMMUNITY_SITUR-Q y reglas de datos]]
- 1 edge to [[_COMMUNITY_Ingesta de benchmarks y PDF]]

## Top bridge nodes
- [[silver_datatur_ocupacion.py]] - degree 14, connects to 7 communities
- [[pyspark_sql]] - degree 3, connects to 2 communities
- [[construir_silver_ocupacion()]] - degree 4, connects to 1 community
- [[openpyxl]] - degree 2, connects to 1 community