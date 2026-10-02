---
type: community
members: 10
---

# D1 SITUR-Q API (45 indicadores)

**Members:** 10 nodes

## Members
- [[A1 Radar — ¿Dónde hay presión y dónde hay espacio]] - concept - CLAUDE.md
- [[A5 Torre en vivo — ¿Qué hace la campaña esta semana]] - concept - CLAUDE.md
- [[Alternativa elegida fusión A1 Radar + A3 Pronóstico + A5 Torre en vivo]] - concept - OBJETIVO.md
- [[D1 SITUR-Q API (45 indicadores)]] - concept - docs/datos/INVENTARIO.md
- [[Hueco sin ocupacion hotelera oficial 2025-2026]] - concept - docs/datos/INVENTARIO.md
- [[Paquete Python backendtorre (base · radar · pronostico · envivo · campana · api)]] - code - CLAUDE.md
- [[Presión de llegada medida (cruceristas + Tren Maya + cruces de Belice por habitación y por residente)]] - rationale - docs/datos/INVENTARIO.md
- [[Regla 2 Silver ocupacion con 0 habitaciones = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Regla 3 Silver afluencia y derrama en 0 = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Regla 4 Silver los demas ceros se conservan]] - rationale - docs/decisiones/04-silver.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/D1_SITUR-Q_API_45_indicadores
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_D6 DENUE INEGI (32 estados)]]
- 6 edges to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]
- 4 edges to [[_COMMUNITY_03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]]
- 2 edges to [[_COMMUNITY_CLAUDE.md - Reglas del repositorio Torre del Caribe]]
- 2 edges to [[_COMMUNITY_Fase 5 Pronóstico series medidas, huecos de cierrepandemia]]
- 1 edge to [[_COMMUNITY_D6 DENUE INEGI (32 estados) (Índice de Presión Turíst)]]
- 1 edge to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan]]
- 1 edge to [[_COMMUNITY_Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)]]
- 1 edge to [[_COMMUNITY_Parte G — Foco en 5 regiones]]
- 1 edge to [[_COMMUNITY_Fase 1 ingesta Bronze (353 archivos, 8,134,802]]
- 1 edge to [[_COMMUNITY_Reglas de oro (a–h) (Fase 4 Radar (índice co)]]

## Top bridge nodes
- [[A1 Radar — ¿Dónde hay presión y dónde hay espacio]] - degree 11, connects to 6 communities
- [[D1 SITUR-Q API (45 indicadores)]] - degree 11, connects to 4 communities
- [[A5 Torre en vivo — ¿Qué hace la campaña esta semana]] - degree 7, connects to 4 communities
- [[Alternativa elegida fusión A1 Radar + A3 Pronóstico + A5 Torre en vivo]] - degree 5, connects to 3 communities
- [[Hueco sin ocupacion hotelera oficial 2025-2026]] - degree 5, connects to 2 communities