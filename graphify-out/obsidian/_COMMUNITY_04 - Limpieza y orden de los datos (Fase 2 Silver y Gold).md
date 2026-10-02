---
type: community
members: 14
---

# 04 - Limpieza y orden de los datos (Fase 2: Silver y Gold)

**Members:** 14 nodes

## Members
- [[04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]] - document - docs/decisiones/04-silver.md
- [[Bandera de comparabilidad (notas al pie DataTur)]] - concept - docs/decisiones/04-silver.md
- [[D1 SITUR-Q API (45 indicadores)]] - concept - docs/datos/INVENTARIO.md
- [[D2D2m DataTur ocupacion hotelera semanal y mensual]] - concept - docs/datos/INVENTARIO.md
- [[DataTur una version por periodo (gana la mas reciente)]] - rationale - docs/decisiones/04-silver.md
- [[Fuentes que no coinciden Isla Mujeres (prensa vs DataTur)]] - rationale - docs/decisiones/04-silver.md
- [[Hueco sin ocupacion hotelera oficial 2025-2026]] - concept - docs/datos/INVENTARIO.md
- [[Regla 1 Silver Tren Maya suma estaciones]] - rationale - docs/decisiones/04-silver.md
- [[Regla 1 No inventar datos]] - rationale - CLAUDE.md
- [[Regla 2 Silver ocupacion con 0 habitaciones = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Regla 3 Silver afluencia y derrama en 0 = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Regla 4 Silver los demas ceros se conservan]] - rationale - docs/decisiones/04-silver.md
- [[Regla 6 Silver mes aereo con todos los aeropuertos en 0 = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Revisión con datos oficiales Isla Mujeres (DataTur 74.7 % feb  43.2 % abr 2026)]] - concept - docs/regiones/REGIONES.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/04_-_Limpieza_y_orden_de_los_datos_Fase_2_Silver_y_Gold
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_D6 DENUE INEGI (32 estados)]]
- 5 edges to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]
- 3 edges to [[_COMMUNITY_CLAUDE.md - Reglas del repositorio Torre del Caribe]]
- 3 edges to [[_COMMUNITY_Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)]]
- 3 edges to [[_COMMUNITY_03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]]
- 2 edges to [[_COMMUNITY_Selección de regiones con visitantes INAH]]
- 2 edges to [[_COMMUNITY_D6 DENUE INEGI (32 estados) (Incidente Big Data cuan)]]
- 2 edges to [[_COMMUNITY_Pronóstico (A3, Fase 5) visitantes 1-12 meses (Fusión A1 Radar + A3 Pro)]]
- 1 edge to [[_COMMUNITY_entorno.py]]
- 1 edge to [[_COMMUNITY_test_silver.py]]
- 1 edge to [[_COMMUNITY_silver_datatur_ocupacion.py]]
- 1 edge to [[_COMMUNITY_silver_siturq.py]]
- 1 edge to [[_COMMUNITY_silver_denue.py]]
- 1 edge to [[_COMMUNITY_Decisión la campaña promueve 5 regiones de Quintana Roo]]
- 1 edge to [[_COMMUNITY_Hoja de ruta del proyecto]]

## Top bridge nodes
- [[04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]] - degree 24, connects to 13 communities
- [[D1 SITUR-Q API (45 indicadores)]] - degree 11, connects to 4 communities
- [[D2D2m DataTur ocupacion hotelera semanal y mensual]] - degree 7, connects to 3 communities
- [[Hueco sin ocupacion hotelera oficial 2025-2026]] - degree 5, connects to 3 communities
- [[Fuentes que no coinciden Isla Mujeres (prensa vs DataTur)]] - degree 5, connects to 2 communities