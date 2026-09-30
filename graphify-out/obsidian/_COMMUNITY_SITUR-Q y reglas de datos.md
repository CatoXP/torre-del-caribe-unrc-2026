---
type: community
members: 11
---

# SITUR-Q y reglas de datos

**Members:** 11 nodes

## Members
- [[04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]] - document - docs/decisiones/04-silver.md
- [[D1 SITUR-Q API (45 indicadores)]] - concept - docs/datos/INVENTARIO.md
- [[Hueco sin ocupacion hotelera oficial 2025-2026]] - concept - docs/datos/INVENTARIO.md
- [[Indicador SITUR-Q 'Turista - Afluencia' roto (120120 error 500)]] - concept - docs/decisiones/03-ingesta.md
- [[Regla 1 Silver Tren Maya suma estaciones]] - rationale - docs/decisiones/04-silver.md
- [[Regla 1 No inventar datos]] - rationale - CLAUDE.md
- [[Regla 2 Silver ocupacion con 0 habitaciones = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Regla 3 Silver afluencia y derrama en 0 = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Regla 4 Silver los demas ceros se conservan]] - rationale - docs/decisiones/04-silver.md
- [[Regla 6 Silver mes aereo con todos los aeropuertos en 0 = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Revisión con datos oficiales Isla Mujeres (DataTur 74.7 % feb  43.2 % abr 2026)]] - concept - docs/regiones/REGIONES.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SITUR-Q_y_reglas_de_datos
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Fuentes del Radar (DENUE, Censo)]]
- 5 edges to [[_COMMUNITY_Inventario de fuentes y módulos (04 - Limpieza y orden de)]]
- 4 edges to [[_COMMUNITY_Inventario de fuentes y módulos]]
- 3 edges to [[_COMMUNITY_Inventario de fuentes y módulos (Cap. 5 — Limpieza y orde)]]
- 3 edges to [[_COMMUNITY_Ingesta SITUR-Q]]
- 3 edges to [[_COMMUNITY_Página módulos, fases y chat]]
- 2 edges to [[_COMMUNITY_Reglas del repositorio (CLAUDE.md)]]
- 2 edges to [[_COMMUNITY_Entorno Spark en Windows]]
- 1 edge to [[_COMMUNITY_Silver SITUR-Q y DENUE]]
- 1 edge to [[_COMMUNITY_Pruebas Silver]]
- 1 edge to [[_COMMUNITY_Silver ocupación DataTur y Spark]]
- 1 edge to [[_COMMUNITY_Las 5 regiones de la campaña]]
- 1 edge to [[_COMMUNITY_Plan v3 y módulos A1 A3 A5 (Alternativa elegida fus)]]

## Top bridge nodes
- [[04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]] - degree 25, connects to 11 communities
- [[D1 SITUR-Q API (45 indicadores)]] - degree 11, connects to 3 communities
- [[Hueco sin ocupacion hotelera oficial 2025-2026]] - degree 5, connects to 3 communities
- [[Regla 1 No inventar datos]] - degree 5, connects to 2 communities
- [[Regla 6 Silver mes aereo con todos los aeropuertos en 0 = hueco]] - degree 5, connects to 2 communities