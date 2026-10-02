---
type: community
members: 8
---

# D6 DENUE INEGI (32 estados) (Incidente Big Data: cuan)

**Members:** 8 nodes

## Members
- [[Chetumal]] - concept - OBJETIVO.md
- [[Corrección de conteo DENUE 6,138,075 e ITER 2,243]] - rationale - docs/decisiones/03-ingesta.md
- [[DENUE procesado completo (6,138,075 negocios)]] - rationale - docs/decisiones/04-silver.md
- [[Fase 1 cerrada Bronze 353 archivos, 8,134,802 registros]] - concept - OBJETIVO.md
- [[Incidente Big Data cuando los datos no caben en una computadora]] - concept - OBJETIVO.md
- [[SITUR-Q (sin ocupación 2025–2026)]] - concept - OBJETIVO.md
- [[Sección El dato (4 de cada 10 cuartos)]] - code - frontend/index.html
- [[pyspark==3.5.6]] - concept - requirements.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/D6_DENUE_INEGI_32_estados_Incidente_Big_Data_cuan
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]]
- 1 edge to [[_COMMUNITY_ingesta_abiertas.py]]
- 1 edge to [[_COMMUNITY_generar]]
- 1 edge to [[_COMMUNITY_02 — Entorno de trabajo (Fase 0 cimientos)]]
- 1 edge to [[_COMMUNITY_D6 DENUE INEGI (32 estados)]]
- 1 edge to [[_COMMUNITY_requirements.txt]]
- 1 edge to [[_COMMUNITY_frontendindex.html (página pública)]]
- 1 edge to [[_COMMUNITY_Decisión la campaña promueve 5 regiones de Quintana Roo (Laguna Milagros–Xul-Ha)]]
- 1 edge to [[_COMMUNITY_Regla no inventar datos (hueco se declara)]]
- 1 edge to [[_COMMUNITY_README — Torre del Caribe]]

## Top bridge nodes
- [[Incidente Big Data cuando los datos no caben en una computadora]] - degree 5, connects to 2 communities
- [[DENUE procesado completo (6,138,075 negocios)]] - degree 4, connects to 2 communities
- [[Sección El dato (4 de cada 10 cuartos)]] - degree 4, connects to 2 communities
- [[pyspark==3.5.6]] - degree 3, connects to 2 communities
- [[Fase 1 cerrada Bronze 353 archivos, 8,134,802 registros]] - degree 3, connects to 1 community