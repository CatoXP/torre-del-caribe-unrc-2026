---
type: community
members: 13
---

# Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)

**Members:** 13 nodes

## Members
- [[Cap. 4 — Recolección de los datos oficiales (Fase 1) 15 fuentes, 353 archivos, 8,134,802 registros]] - document - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)]] - document - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Cifras corregidas por la fuente gana la versión más reciente (2,804 cifras semanales)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Cómo llega la gente avión 15,959,277 (2024), crucero 7,556,937, Belice 653,306, Tren Maya 560,241 (2025)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Datos que no existen ocupación SITUR-Q termina dic-2024; afluencia y derrama hasta mar-2024; 'Turista - Afluencia' no responde]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Hallazgo ocupación semanal de ene-2022 a jul-2026, 239 semanas por centro]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Regla 1 Silver Tren Maya suma estaciones]] - rationale - docs/decisiones/04-silver.md
- [[Regla 6 de Silver mes aéreo con todos los aeropuertos en 0 = hueco (114 meses-aeropuerto)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Regla Tren Maya se suma por estación (7,084 = 3,502 + 3,582)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Regla ceros imposibles = dato faltante]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Sin flechas origen-destino en el mapa de llegadas]] - rationale - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Vigilancia del sargazo en la Bahía de Chetumal (canales al Caribe, no en la costa; pausa automática si llega)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[playwright==1.49.1 (navegador automatizado)]] - concept - requirements.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Cap_5__Limpieza_y_orden_de_los_datos_Fase_2_Silver_con_PySpark
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_D6 DENUE INEGI (32 estados)]]
- 1 edge to [[_COMMUNITY_D1 SITUR-Q API (45 indicadores)]]
- 1 edge to [[_COMMUNITY_requirements.txt]]
- 1 edge to [[_COMMUNITY_Cap. 6 — La página web (sistema Sur mexicano)]]
- 1 edge to [[_COMMUNITY_03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]]

## Top bridge nodes
- [[Regla 1 Silver Tren Maya suma estaciones]] - degree 3, connects to 2 communities
- [[Cómo llega la gente avión 15,959,277 (2024), crucero 7,556,937, Belice 653,306, Tren Maya 560,241 (2025)]] - degree 3, connects to 1 community
- [[Regla 6 de Silver mes aéreo con todos los aeropuertos en 0 = hueco (114 meses-aeropuerto)]] - degree 3, connects to 1 community
- [[Cap. 4 — Recolección de los datos oficiales (Fase 1) 15 fuentes, 353 archivos, 8,134,802 registros]] - degree 3, connects to 1 community
- [[playwright==1.49.1 (navegador automatizado)]] - degree 2, connects to 1 community