---
type: community
members: 5
---

# PLAN_v3.md (plan aprobado) (Lakehouse PySpark Bronze)

**Members:** 5 nodes

## Members
- [[Fase 0 — Cimientos]] - concept - docs/plan/PLAN_v3.md
- [[Fase 1 — Ingesta (Bronze)]] - concept - docs/plan/PLAN_v3.md
- [[Fase 2 — Almacén y calidad (SilverGold con PySpark)]] - concept - docs/plan/PLAN_v3.md
- [[Lakehouse PySpark Bronze → Silver → Gold]] - concept - docs/plan/PLAN_v3.md
- [[Reconciliación SITUR-Q vs DataTur (Cancún, Riviera Maya)]] - concept - docs/plan/PLAN_v3.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/PLAN_v3md_plan_aprobado_Lakehouse_PySpark_Bronze
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Plan v3 estructura]]
- 2 edges to [[_COMMUNITY_PLAN_v3.md (plan aprobado)]]
- 1 edge to [[_COMMUNITY_03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]]
- 1 edge to [[_COMMUNITY_Cap. 2 — El problema en números ¿a dónde van los turistas]]
- 1 edge to [[_COMMUNITY_README — Torre del Caribe]]
- 1 edge to [[_COMMUNITY_Plan v3 recorrido de la página]]
- 1 edge to [[_COMMUNITY_Plan v3 A3 Pronóstico]]

## Top bridge nodes
- [[Lakehouse PySpark Bronze → Silver → Gold]] - degree 6, connects to 3 communities
- [[Fase 2 — Almacén y calidad (SilverGold con PySpark)]] - degree 5, connects to 2 communities
- [[Reconciliación SITUR-Q vs DataTur (Cancún, Riviera Maya)]] - degree 4, connects to 2 communities
- [[Fase 1 — Ingesta (Bronze)]] - degree 4, connects to 1 community
- [[Fase 0 — Cimientos]] - degree 2, connects to 1 community