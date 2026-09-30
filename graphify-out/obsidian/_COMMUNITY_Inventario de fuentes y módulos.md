---
type: community
members: 21
---

# Inventario de fuentes y módulos

**Members:** 21 nodes

## Members
- [[A2 Voz del viajero y A4 Portafolio (descartadas como ejes)]] - concept - docs/decisiones/00-fundacion.md
- [[A3 Pronostico (cuando conviene ir, 1-12 meses)]] - concept - CLAUDE.md
- [[D1 SITUR-Q (API getCharData, 45 indicadores)]] - concept - docs/datos/INVENTARIO.md
- [[D10 FRED (peso-dolar, CPI)]] - concept - docs/datos/INVENTARIO.md
- [[D11 ENDUTIH 2025 INEGI]] - concept - docs/datos/INVENTARIO.md
- [[D12 GeoJSON Quintana Roo]] - concept - docs/datos/INVENTARIO.md
- [[D13 Benchmarks de costo por canal (WordStream 2025  LocaliQ 2026)]] - concept - docs/datos/INVENTARIO.md
- [[D14 DESIGN.md (tokens y componentes)]] - concept - docs/datos/INVENTARIO.md
- [[D15 Wikimedia Commons (fotos con licencia libre)]] - concept - docs/datos/INVENTARIO.md
- [[D2m DataTur ocupación mensual]] - concept - docs/datos/INVENTARIO.md
- [[D3 DataTur BD_Nacionalidad (521,364 filas)]] - concept - docs/datos/INVENTARIO.md
- [[D4 DataTur BdINAH, DB_AFAC, cruceros, Compendio 2024]] - concept - docs/datos/INVENTARIO.md
- [[D4 DataTur DB_AFAC, BaseDatosCruceros y Compendio 2024]] - concept - docs/datos/INVENTARIO.md
- [[D8 Open-Meteo archivo climatico]] - concept - docs/datos/INVENTARIO.md
- [[D9 HURDAT2 NOAA (1851-2025)]] - concept - docs/datos/INVENTARIO.md
- [[DataTur 135 archivos semanales de ocupación (2024-S01 → 2026-S31, 7 centros de Q. Roo)]] - concept - docs/decisiones/00-fundacion.md
- [[Decisión 2 Quintana Roo y fusión A1 + A3 + A5]] - rationale - docs/decisiones/00-fundacion.md
- [[Fuentes excluidas (EVI, ENGATUR, OSM, Google Trends, TripAdvisor)]] - concept - docs/datos/INVENTARIO.md
- [[Inventario de datos - fuentes oficiales verificadas]] - document - docs/datos/INVENTARIO.md
- [[Regla de oro sin scraping prohibido (TripAdvisor, Google Maps)]] - rationale - CLAUDE.md
- [[SITUR-Q API con 45 indicadores]] - concept - docs/decisiones/00-fundacion.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Inventario_de_fuentes_y_módulos
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Plan v3 y módulos A1 A3 A5]]
- 4 edges to [[_COMMUNITY_Las 5 regiones de la campaña]]
- 4 edges to [[_COMMUNITY_SITUR-Q y reglas de datos]]
- 3 edges to [[_COMMUNITY_Incidente minería y buyer persona]]
- 3 edges to [[_COMMUNITY_Fuentes del Radar (DENUE, Censo)]]
- 3 edges to [[_COMMUNITY_Reglas del repositorio (CLAUDE.md)]]
- 2 edges to [[_COMMUNITY_Fase 0 entorno y fundación]]
- 2 edges to [[_COMMUNITY_Ingesta SITUR-Q]]
- 1 edge to [[_COMMUNITY_Reglas de oro y ecuaciones]]
- 1 edge to [[_COMMUNITY_Ecuaciones y fuentes del documento]]
- 1 edge to [[_COMMUNITY_Plan v3 y módulos A1 A3 A5 (Alternativa elegida fus)]]
- 1 edge to [[_COMMUNITY_Inventario de fuentes y módulos (04 - Limpieza y orden de)]]
- 1 edge to [[_COMMUNITY_Ingesta de benchmarks y PDF]]

## Top bridge nodes
- [[Inventario de datos - fuentes oficiales verificadas]] - degree 33, connects to 9 communities
- [[Decisión 2 Quintana Roo y fusión A1 + A3 + A5]] - degree 6, connects to 3 communities
- [[A3 Pronostico (cuando conviene ir, 1-12 meses)]] - degree 6, connects to 3 communities
- [[Regla de oro sin scraping prohibido (TripAdvisor, Google Maps)]] - degree 4, connects to 2 communities
- [[D3 DataTur BD_Nacionalidad (521,364 filas)]] - degree 3, connects to 2 communities