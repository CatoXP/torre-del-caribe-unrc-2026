---
type: community
members: 7
---

# Pronóstico: escenarios Monte Carlo

**Members:** 7 nodes

## Members
- [[Capacidad probada (mes más alto ya recibido)]] - rationale - docs/decisiones/11-pronostico.md
- [[Decisión efecto de campaña se ve en la Fase 6]] - rationale - docs/decisiones/11-pronostico.md
- [[Decisión tormentas como supuesto con barrido (02550 %)]] - rationale - docs/decisiones/11-pronostico.md
- [[Fase 6 — Reparto del presupuesto (optimización)]] - concept - docs/plan/HOJA_DE_RUTA.md
- [[Monte Carlo escenarios malo  probable  bueno (10,000 futuros)]] - concept - docs/decisiones/11-pronostico.md
- [[Origen móvil (backtest de 12 meses)]] - concept - docs/decisiones/11-pronostico.md
- [[Poisson de tormentas (31 eventos; 40.3 % al menos una al año)]] - concept - docs/decisiones/11-pronostico.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pronóstico_escenarios_Monte_Carlo
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_escenarios.py]]
- 1 edge to [[_COMMUNITY_Planeador calendario y temporada alta]]
- 1 edge to [[_COMMUNITY_modelos.py]]
- 1 edge to [[_COMMUNITY_Hoja de ruta del proyecto]]

## Top bridge nodes
- [[Monte Carlo escenarios malo  probable  bueno (10,000 futuros)]] - degree 6, connects to 2 communities
- [[Fase 6 — Reparto del presupuesto (optimización)]] - degree 3, connects to 1 community
- [[Origen móvil (backtest de 12 meses)]] - degree 2, connects to 1 community
- [[Poisson de tormentas (31 eventos; 40.3 % al menos una al año)]] - degree 2, connects to 1 community