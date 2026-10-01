---
type: community
members: 9
---

# D1 SITUR-Q API (45 indicadores)

**Members:** 9 nodes

## Members
- [[D1 SITUR-Q API (45 indicadores)]] - concept - docs/datos/INVENTARIO.md
- [[Hueco sin ocupacion hotelera oficial 2025-2026]] - concept - docs/datos/INVENTARIO.md
- [[Presión de llegada medida (cruceristas + Tren Maya + cruces de Belice por habitación y por residente)]] - rationale - docs/datos/INVENTARIO.md
- [[Regla 1 No inventar datos]] - rationale - CLAUDE.md
- [[Regla 2 Silver ocupacion con 0 habitaciones = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Regla 3 Silver afluencia y derrama en 0 = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Regla 4 Silver los demas ceros se conservan]] - rationale - docs/decisiones/04-silver.md
- [[Regla de oro estimado != medido (sufijo _est)]] - rationale - CLAUDE.md
- [[Sin flechas origen-destino en el mapa de llegadas]] - rationale - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/D1_SITUR-Q_API_45_indicadores
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Silver fuentes que no coinciden]]
- 3 edges to [[_COMMUNITY_Inventario de fuentes (D1–D14)]]
- 3 edges to [[_COMMUNITY_03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]]
- 2 edges to [[_COMMUNITY_04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]]
- 2 edges to [[_COMMUNITY_Silver reglas de SITUR-Q (ejecutivo)]]
- 2 edges to [[_COMMUNITY_CLAUDE.md - Reglas del repositorio Torre del Caribe]]
- 1 edge to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]

## Top bridge nodes
- [[D1 SITUR-Q API (45 indicadores)]] - degree 11, connects to 6 communities
- [[Regla 1 No inventar datos]] - degree 5, connects to 2 communities
- [[Hueco sin ocupacion hotelera oficial 2025-2026]] - degree 5, connects to 2 communities
- [[Presión de llegada medida (cruceristas + Tren Maya + cruces de Belice por habitación y por residente)]] - degree 4, connects to 2 communities
- [[Regla 3 Silver afluencia y derrama en 0 = hueco]] - degree 4, connects to 1 community