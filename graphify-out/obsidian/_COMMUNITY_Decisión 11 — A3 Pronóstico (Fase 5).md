---
type: community
members: 5
---

# Decisión 11 — A3 Pronóstico (Fase 5)

**Members:** 5 nodes

## Members
- [[Criterio de elección menor MAE con cobertura ≥80 %]] - rationale - docs/metodologia/ECUACIONES.md
- [[Decisión 2 Hueco + forma del año (meses que no entrenan)]] - rationale - docs/decisiones/11-pronostico.md
- [[Descomposición clásica multiplicativa (forma del año)]] - concept - docs/decisiones/11-pronostico.md
- [[Error MAE, MAPE y error relativo]] - concept - docs/metodologia/ECUACIONES.md
- [[Holt-Winters con forma del año fija]] - concept - docs/metodologia/ECUACIONES.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Decisión_11__A3_Pronóstico_Fase_5
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_modelos.py]]
- 2 edges to [[_COMMUNITY_series.py]]
- 2 edges to [[_COMMUNITY_10 — Datos limpios para el Pronóstico huracanes, clima y tipo de cambio (Fase 2, cierre de la parte que usa la Fase 5)]]
- 2 edges to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan (Cadena de Markov semanal)]]
- 1 edge to [[_COMMUNITY_forma.py]]
- 1 edge to [[_COMMUNITY_ECUACIONES.md — Ecuaciones y cómo lo resolví]]
- 1 edge to [[_COMMUNITY_numpy]]

## Top bridge nodes
- [[Criterio de elección menor MAE con cobertura ≥80 %]] - degree 7, connects to 4 communities
- [[Descomposición clásica multiplicativa (forma del año)]] - degree 4, connects to 2 communities
- [[Holt-Winters con forma del año fija]] - degree 4, connects to 2 communities
- [[Decisión 2 Hueco + forma del año (meses que no entrenan)]] - degree 3, connects to 2 communities
- [[Error MAE, MAPE y error relativo]] - degree 2, connects to 1 community