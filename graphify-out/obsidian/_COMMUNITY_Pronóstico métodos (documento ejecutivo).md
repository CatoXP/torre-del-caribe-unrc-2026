---
type: community
members: 15
---

# Pronóstico: métodos (documento ejecutivo)

**Members:** 15 nodes

## Members
- [[Escenarios maloprobablebueno (10,000 futuros simulados)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Forma del año (índice estacional)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Holt-Winters (dos versiones)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Línea base (mismo mes del año anterior)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Meses cerrados marcados y fuera del entrenamiento]] - rationale - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[NOAA huracanes del Atlántico]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Open-Meteo (clima reanálisis)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Persistencia (igual que el mes pasado)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Probabilidad mensual de tormenta (40 % anual)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Pronóstico (A3) cuándo conviene ir]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Rango del 90 % y su cobertura real]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Regresión con clima (modelo elegido del Pronóstico en el sur)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[STL (método de contraste estacional)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Tormenta que afecta al sur (≤200 km de Chetumal, ≥34 nudos, desde 1966)]] - rationale - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Validación con origen móvil (regresar el reloj)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pronóstico_métodos_documento_ejecutivo
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Capacidad probada y regiones]]
- 2 edges to [[_COMMUNITY_Regla no inventar datos]]
- 1 edge to [[_COMMUNITY_Regresión logística multiclase (modelo elegido del Radar)]]
- 1 edge to [[_COMMUNITY_markov.py]]
- 1 edge to [[_COMMUNITY_Ingesta manifiesto y riesgos]]
- 1 edge to [[_COMMUNITY_Radar índice comparable y clustering (ejecutivo)]]

## Top bridge nodes
- [[Pronóstico (A3) cuándo conviene ir]] - degree 7, connects to 2 communities
- [[Persistencia (igual que el mes pasado)]] - degree 3, connects to 2 communities
- [[Regresión con clima (modelo elegido del Pronóstico en el sur)]] - degree 6, connects to 1 community
- [[Escenarios maloprobablebueno (10,000 futuros simulados)]] - degree 4, connects to 1 community
- [[Meses cerrados marcados y fuera del entrenamiento]] - degree 3, connects to 1 community