---
type: community
members: 10
---

# D1 SITUR-Q API (45 indicadores)

**Members:** 10 nodes

## Members
- [[A5 Torre en vivo (que hace la campana esta semana)]] - concept - CLAUDE.md
- [[Cómo llega la gente avión 15,959,277 (2024), crucero 7,556,937, Belice 653,306, Tren Maya 560,241 (2025)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[D1 SITUR-Q API (45 indicadores)]] - concept - docs/datos/INVENTARIO.md
- [[Hueco sin ocupacion hotelera oficial 2025-2026]] - concept - docs/datos/INVENTARIO.md
- [[Indicador SITUR-Q 'Turista - Afluencia' roto (120120 error 500)]] - concept - docs/decisiones/03-ingesta.md
- [[Regla 1 No inventar datos]] - rationale - CLAUDE.md
- [[Regla 2 Silver ocupacion con 0 habitaciones = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Regla 3 Silver afluencia y derrama en 0 = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Regla 4 Silver los demas ceros se conservan]] - rationale - docs/decisiones/04-silver.md
- [[Sin flechas origen-destino en el mapa de llegadas]] - rationale - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/D1_SITUR-Q_API_45_indicadores
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]]
- 3 edges to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]
- 3 edges to [[_COMMUNITY_Ingesta costos publicitarios y sargazo]]
- 2 edges to [[_COMMUNITY_D6 DENUE INEGI (32 estados)]]
- 2 edges to [[_COMMUNITY_Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)]]
- 2 edges to [[_COMMUNITY_CLAUDE.md - Reglas del repositorio Torre del Caribe]]
- 1 edge to [[_COMMUNITY_Decisión 08 — A1 Radar (Fase 4)]]
- 1 edge to [[_COMMUNITY_Página secciones (documento ejecutivo)]]

## Top bridge nodes
- [[D1 SITUR-Q API (45 indicadores)]] - degree 11, connects to 4 communities
- [[A5 Torre en vivo (que hace la campana esta semana)]] - degree 5, connects to 4 communities
- [[Hueco sin ocupacion hotelera oficial 2025-2026]] - degree 5, connects to 3 communities
- [[Regla 1 No inventar datos]] - degree 5, connects to 2 communities
- [[Cómo llega la gente avión 15,959,277 (2024), crucero 7,556,937, Belice 653,306, Tren Maya 560,241 (2025)]] - degree 3, connects to 2 communities