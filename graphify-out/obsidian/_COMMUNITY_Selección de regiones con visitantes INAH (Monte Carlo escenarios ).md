---
type: community
members: 7
---

# Selección de regiones con visitantes INAH (Monte Carlo: escenarios )

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
TABLE source_file, type FROM #community/Selección_de_regiones_con_visitantes_INAH_Monte_Carlo_escenarios_
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Pronóstico tormentas y escenarios]]
- 1 edge to [[_COMMUNITY_Pronóstico forma del año y modelos]]
- 1 edge to [[_COMMUNITY_escenarios.py (calendario.py)]]
- 1 edge to [[_COMMUNITY_Hoja de ruta del proyecto]]

## Top bridge nodes
- [[Monte Carlo escenarios malo  probable  bueno (10,000 futuros)]] - degree 6, connects to 2 communities
- [[Fase 6 — Reparto del presupuesto (optimización)]] - degree 3, connects to 1 community
- [[Origen móvil (backtest de 12 meses)]] - degree 2, connects to 1 community
- [[Poisson de tormentas (31 eventos; 40.3 % al menos una al año)]] - degree 2, connects to 1 community