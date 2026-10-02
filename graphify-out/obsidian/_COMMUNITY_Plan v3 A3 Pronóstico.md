---
type: community
members: 7
---

# Plan v3: A3 Pronóstico

**Members:** 7 nodes

## Members
- [[A3 Pronóstico]] - concept - docs/plan/PLAN_v3.md
- [[Clustering jerárquico de los 54 centros del país]] - concept - docs/plan/PLAN_v3.md
- [[D1 SITUR-Q (API de indicadores turísticos)]] - concept - docs/plan/PLAN_v3.md
- [[D2m DataTur ocupación mensual (54 centros)]] - concept - docs/plan/PLAN_v3.md
- [[Descomposición estacional STL]] - concept - docs/plan/PLAN_v3.md
- [[Hueco sin ocupación oficial del sur 2025–2026]] - rationale - docs/plan/PLAN_v3.md
- [[Inferir estados futuros con ML (clasificador + Markov)]] - rationale - docs/decisiones/08-radar.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Plan_v3_A3_Pronóstico
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_PLAN_v3.md (plan aprobado)]]
- 4 edges to [[_COMMUNITY_Plan v3 ecuaciones]]
- 4 edges to [[_COMMUNITY_Plan v3 estructura]]
- 2 edges to [[_COMMUNITY_Parte G — Foco en 5 regiones]]
- 1 edge to [[_COMMUNITY_PLAN_v3.md (plan aprobado) (Lakehouse PySpark Bronze)]]
- 1 edge to [[_COMMUNITY_Cap. 2 — El problema en números ¿a dónde van los turistas]]

## Top bridge nodes
- [[A3 Pronóstico]] - degree 16, connects to 4 communities
- [[D1 SITUR-Q (API de indicadores turísticos)]] - degree 6, connects to 3 communities
- [[Hueco sin ocupación oficial del sur 2025–2026]] - degree 4, connects to 2 communities
- [[Clustering jerárquico de los 54 centros del país]] - degree 2, connects to 1 community