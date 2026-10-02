---
type: community
members: 10
---

# entorno.py

**Members:** 10 nodes

## Members
- [[02 — Entorno de trabajo (Fase 0 cimientos)]] - document - docs/decisiones/02-entorno.md
- [[Decisión Fase 0 .venv (Python 3.11.9) + PySpark 3.5.6 + JDK 17 + winutilshadoop.dll 3.3.6]] - rationale - docs/decisiones/02-entorno.md
- [[Entorno aislado .venv]] - rationale - docs/decisiones/02-entorno.md
- [[Huellas SHA-256 de winutils.exe y hadoop.dll]] - rationale - docs/decisiones/02-entorno.md
- [[JDK 17 (OpenJDK 17.0.20.1 de Microsoft)]] - concept - docs/decisiones/02-entorno.md
- [[Opción descartada Spark dentro de Docker]] - rationale - docs/decisiones/02-entorno.md
- [[Opción descartada cambiar el Java de todo Windows]] - rationale - docs/decisiones/02-entorno.md
- [[Opción descartada instalar en el Python global]] - rationale - docs/decisiones/02-entorno.md
- [[PySpark 3.5.6 (no 4.x)]] - concept - docs/decisiones/02-entorno.md
- [[winutils.exe + hadoop.dll 3.3.6 (herramientashadoopbin)]] - concept - docs/decisiones/02-entorno.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/entornopy
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_buscar_jdk17]]
- 1 edge to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]
- 1 edge to [[_COMMUNITY_silver_denue.py]]
- 1 edge to [[_COMMUNITY_Hoja de ruta fases 5 a 7]]
- 1 edge to [[_COMMUNITY_PLAN_v3.md (plan aprobado)]]
- 1 edge to [[_COMMUNITY_requirements.txt]]

## Top bridge nodes
- [[02 — Entorno de trabajo (Fase 0 cimientos)]] - degree 7, connects to 3 communities
- [[Decisión Fase 0 .venv (Python 3.11.9) + PySpark 3.5.6 + JDK 17 + winutilshadoop.dll 3.3.6]] - degree 6, connects to 1 community
- [[JDK 17 (OpenJDK 17.0.20.1 de Microsoft)]] - degree 4, connects to 1 community
- [[winutils.exe + hadoop.dll 3.3.6 (herramientashadoopbin)]] - degree 4, connects to 1 community
- [[Entorno aislado .venv]] - degree 3, connects to 1 community