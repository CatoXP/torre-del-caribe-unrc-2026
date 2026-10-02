---
type: community
members: 7
---

# Fase 2: limpieza y orden de los datos (Silver)

**Members:** 7 nodes

## Members
- [[Capas Bronze  Silver  Gold]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Fase 0 preparación del equipo de cómputo]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Fase 2 limpieza y orden de los datos (Silver)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[NOAA base de huracanes del Atlántico]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[PySpark 3.5.6 + Java 17]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Tipo de cambio Reserva Federal de St. Louis]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Tormenta que afecta al sur (200 km de Chetumal, 34 nudos, desde 1966)]] - rationale - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Fase_2_limpieza_y_orden_de_los_datos_Silver
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Fase 1 recolección de 15 fuentes oficiales]]
- 2 edges to [[_COMMUNITY_Pronóstico regresión con clima]]
- 1 edge to [[_COMMUNITY_Planeador Planea tu viaje]]
- 1 edge to [[_COMMUNITY_Regresión con clima (modelo elegido del sur) (Regla no inventar datos)]]

## Top bridge nodes
- [[Fase 2 limpieza y orden de los datos (Silver)]] - degree 7, connects to 3 communities
- [[Capas Bronze  Silver  Gold]] - degree 2, connects to 1 community
- [[Tipo de cambio Reserva Federal de St. Louis]] - degree 2, connects to 1 community
- [[Tormenta que afecta al sur (200 km de Chetumal, 34 nudos, desde 1966)]] - degree 2, connects to 1 community