---
type: community
members: 17
---

# Entorno: Spark, JDK y prueba de humo

**Members:** 17 nodes

## Members
- [[02 — Entorno de trabajo (Fase 0 cimientos)]] - document - docs/decisiones/02-entorno.md
- [[Decisión Fase 0 .venv (Python 3.11.9) + PySpark 3.5.6 + JDK 17 + winutilshadoop.dll 3.3.6]] - rationale - docs/decisiones/02-entorno.md
- [[Entorno aislado .venv]] - rationale - docs/decisiones/02-entorno.md
- [[Huellas SHA-256 de winutils.exe y hadoop.dll]] - rationale - docs/decisiones/02-entorno.md
- [[JDK 17 (OpenJDK 17.0.20.1 de Microsoft)]] - concept - docs/decisiones/02-entorno.md
- [[Java 8 intacto (JAVA_HOME solo dentro del proceso)]] - rationale - docs/decisiones/02-entorno.md
- [[Opción descartada Spark dentro de Docker]] - rationale - docs/decisiones/02-entorno.md
- [[Opción descartada cambiar el Java de todo Windows]] - rationale - docs/decisiones/02-entorno.md
- [[Opción descartada instalar en el Python global]] - rationale - docs/decisiones/02-entorno.md
- [[Prueba de humo Fase 0 (22.93 s, suma = 6)]] - concept - docs/decisiones/02-entorno.md
- [[PySpark 3.5.6 (no 4.x)]] - concept - docs/decisiones/02-entorno.md
- [[entorno.py]] - code - backend/torre/base/entorno.py
- [[glob]] - concept
- [[os]] - concept
- [[test_entorno.py]] - code - tests/test_entorno.py
- [[test_spark_lee_csv_y_escribe_parquet()]] - code - tests/test_entorno.py
- [[winutils.exe + hadoop.dll 3.3.6 (herramientashadoopbin)]] - concept - docs/decisiones/02-entorno.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Entorno_Spark_JDK_y_prueba_de_humo
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_silver_datatur_ocupacion.py]]
- 3 edges to [[_COMMUNITY_Entorno búsqueda de JDK]]
- 2 edges to [[_COMMUNITY_04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]]
- 2 edges to [[_COMMUNITY_entorno.py]]
- 2 edges to [[_COMMUNITY_Fotos y ubicación comprobada]]
- 1 edge to [[_COMMUNITY_Decisión 2 Quintana Roo y fusión A1 + A3 + A5]]
- 1 edge to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]
- 1 edge to [[_COMMUNITY_PLAN_v3.md (plan aprobado)]]
- 1 edge to [[_COMMUNITY_Fase 7 — Torre en vivo]]
- 1 edge to [[_COMMUNITY_sys]]
- 1 edge to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_test_silver_fase5.py]]
- 1 edge to [[_COMMUNITY_silver_inah.py]]
- 1 edge to [[_COMMUNITY_Silver Censo (ITER)]]
- 1 edge to [[_COMMUNITY_silver_denue.py]]
- 1 edge to [[_COMMUNITY_silver_iter.py]]

## Top bridge nodes
- [[entorno.py]] - degree 24, connects to 12 communities
- [[02 — Entorno de trabajo (Fase 0 cimientos)]] - degree 8, connects to 3 communities
- [[Decisión Fase 0 .venv (Python 3.11.9) + PySpark 3.5.6 + JDK 17 + winutilshadoop.dll 3.3.6]] - degree 6, connects to 1 community
- [[Entorno aislado .venv]] - degree 3, connects to 1 community
- [[test_spark_lee_csv_y_escribe_parquet()]] - degree 2, connects to 1 community