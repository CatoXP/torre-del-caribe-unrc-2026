---
type: community
members: 15
---

# Pronóstico (documento ejecutivo)

**Members:** 15 nodes

## Members
- [[Capacidad probada sin usar (Kohunlich 49.0 %)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Cinco formas de pronosticar (línea base, 2 Holt-Winters, regresión con clima, Gradient Boosting)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Clima Open-Meteo (reanálisis 1950-2026, 8 puntos)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Escenarios maloprobablebueno con 10,000 futuros simulados]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Forma del año (índice estacional, contrastado con STL)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Huracanes NOAA (55,524 posiciones, 1,988 tormentas)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[INAH visitantes a zonas arqueológicas]] - concept - docs/decisiones/08-radar.md
- [[Planea tu viaje (temporada por lugar y mes, alternativas)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Pronóstico (A3, Fase 5) visitantes 1-12 meses]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Rango del 90 % con cobertura medida (Belice 94, Bahía 91, Ruta 80)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Regresión con clima (modelo elegido para el sur)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Riesgo de rebasar la capacidad probada (máximo histórico mensual)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Riesgo de tormenta por mes (ago 13.9 %, sep 12.5 %, 40 % anual)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Tormenta que afecta al sur (≤200 km de Chetumal, ≥34 nudos, desde 1966)]] - rationale - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Validación de origen móvil desde 2019 (regresar el reloj, 12 meses)]] - rationale - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pronóstico_documento_ejecutivo
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Índice de presión turística (0 a 1)]]
- 2 edges to [[_COMMUNITY_Índice de presión turística (0 a 1) (Regla no inventar datos)]]
- 1 edge to [[_COMMUNITY_Índice de presión turística (0 a 1) (Índice de presión turíst)]]
- 1 edge to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan]]
- 1 edge to [[_COMMUNITY_Capa Bronze (15 fuentes, 353 archivos, 8,134,802 registros)]]

## Top bridge nodes
- [[Pronóstico (A3, Fase 5) visitantes 1-12 meses]] - degree 9, connects to 2 communities
- [[Cinco formas de pronosticar (línea base, 2 Holt-Winters, regresión con clima, Gradient Boosting)]] - degree 4, connects to 1 community
- [[Planea tu viaje (temporada por lugar y mes, alternativas)]] - degree 4, connects to 1 community
- [[Capacidad probada sin usar (Kohunlich 49.0 %)]] - degree 3, connects to 1 community
- [[INAH visitantes a zonas arqueológicas]] - degree 2, connects to 1 community