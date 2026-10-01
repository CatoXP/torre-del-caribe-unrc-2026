---
type: community
members: 8
---

# Silver: reglas de SITUR-Q (ejecutivo)

**Members:** 8 nodes

## Members
- [[Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)]] - document - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Cifras corregidas por la fuente gana la versión más reciente (2,804 cifras semanales)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Cómo llega la gente avión 15,959,277 (2024), crucero 7,556,937, Belice 653,306, Tren Maya 560,241 (2025)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Hallazgo ocupación semanal de ene-2022 a jul-2026, 239 semanas por centro]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Regla 1 Silver Tren Maya suma estaciones]] - rationale - docs/decisiones/04-silver.md
- [[Regla 6 de Silver mes aéreo con todos los aeropuertos en 0 = hueco (114 meses-aeropuerto)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Regla Tren Maya se suma por estación (7,084 = 3,502 + 3,582)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Regla ceros imposibles = dato faltante]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Silver_reglas_de_SITUR-Q_ejecutivo
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Silver fuentes que no coinciden]]
- 2 edges to [[_COMMUNITY_D1 SITUR-Q API (45 indicadores)]]
- 1 edge to [[_COMMUNITY_planteamiento.py]]
- 1 edge to [[_COMMUNITY_Ingesta manifiesto y riesgos]]

## Top bridge nodes
- [[Regla 1 Silver Tren Maya suma estaciones]] - degree 3, connects to 2 communities
- [[Cómo llega la gente avión 15,959,277 (2024), crucero 7,556,937, Belice 653,306, Tren Maya 560,241 (2025)]] - degree 3, connects to 2 communities
- [[Regla 6 de Silver mes aéreo con todos los aeropuertos en 0 = hueco (114 meses-aeropuerto)]] - degree 3, connects to 1 community
- [[Regla ceros imposibles = dato faltante]] - degree 2, connects to 1 community