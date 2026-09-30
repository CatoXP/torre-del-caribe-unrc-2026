---
type: community
members: 7
---

# Radar: panel mensual

**Members:** 7 nodes

## Members
- [[Cap. 8 — El Radar ¿dónde hay presión y dónde hay espacio (Fase 4)]] - document - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Corrección la ocupación no se suma (3 filas SITUR-Q)]] - rationale - docs/decisiones/08-radar.md
- [[Laguna Milagros 'sin dato oficial']] - concept - docs/decisiones/08-radar.md
- [[Pieza 1 panel mensual 15 lugares × 55 meses]] - concept - docs/decisiones/08-radar.md
- [[Radar tabla mensual de 15 lugares × 55 meses y hallazgo del doble conteo SITUR-QINAH]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Radar tres decisiones del equipo (pesos iguales, cortes comunes, predicción de estados)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Visitantes INAH zona por zona (ZONA_A_LUGAR, sin doble conteo)]] - rationale - docs/decisiones/08-radar.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Radar_panel_mensual
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Reglas de oro (a–h)]]
- 1 edge to [[_COMMUNITY_Opción D ocupación DataTur + componente en ≥2 lugares]]
- 1 edge to [[_COMMUNITY_panel.py]]
- 1 edge to [[_COMMUNITY_test_radar_panel.py]]
- 1 edge to [[_COMMUNITY_Decisiones cerradas (A.8)]]

## Top bridge nodes
- [[Pieza 1 panel mensual 15 lugares × 55 meses]] - degree 7, connects to 3 communities
- [[Laguna Milagros 'sin dato oficial']] - degree 2, connects to 1 community
- [[Radar tres decisiones del equipo (pesos iguales, cortes comunes, predicción de estados)]] - degree 2, connects to 1 community