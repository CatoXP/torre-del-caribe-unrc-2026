---
type: community
members: 40
---

# Radar: panel mensual

**Members:** 40 nodes

## Members
- [[Cadena de Markov semanal, solo norte]] - rationale - docs/decisiones/08-radar.md
- [[Cap. 8 — El Radar ¿dónde hay presión y dónde hay espacio (Fase 4)]] - document - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Corrección la ocupación no se suma (3 filas SITUR-Q)]] - rationale - docs/decisiones/08-radar.md
- [[Cortes por percentiles comunes p50p90]] - rationale - docs/decisiones/08-radar.md
- [[Cruces de Belice (solo Chetumal)]] - concept - docs/decisiones/08-radar.md
- [[DataFrame_28]] - code
- [[DataTur (ocupación semanal, Sectur)]] - concept - docs/decisiones/08-radar.md
- [[DataTur y SITUR-Q no miden lo mismo (reconciliación)]] - concept - docs/decisiones/09-auditoria-fases-1-4.md
- [[Diferencia DataTur vs SITUR-Q se declara, no se ajusta]] - rationale - docs/decisiones/08-radar.md
- [[Escala mín–máx común a todo el estado]] - rationale - docs/decisiones/08-radar.md
- [[Estados tranquilo  concurrido  saturado]] - concept - docs/decisiones/08-radar.md
- [[Laguna Milagros 'sin dato oficial']] - concept - docs/decisiones/08-radar.md
- [[Meses con dato por lugar y variable (de cuántos posibles). Sirve para ver qué…]] - rationale - backend/torre/radar/panel.py
- [[Ocupación mensual desde DataTur semanal Σ cuartos ocupados ÷ Σ cuartos…]] - rationale - backend/torre/radar/panel.py
- [[Opción D ocupación DataTur + componente en ≥2 lugares]] - rationale - docs/decisiones/08-radar.md
- [[Path_12]] - code
- [[Pesos iguales con análisis de sensibilidad ±50 %]] - rationale - docs/decisiones/08-radar.md
- [[Pieza 1 panel mensual 15 lugares × 55 meses]] - concept - docs/decisiones/08-radar.md
- [[Predicción ago-2026 5 lugares tranquilos; Mahahual 0.40 de saturarse]] - concept - docs/decisiones/08-radar.md
- [[Prueba de validez del IPT (comparar_escalas, variantes A–D)]] - concept - docs/decisiones/08-radar.md
- [[Prueba de validez del índice]] - concept - docs/decisiones/08-radar.md
- [[Quiebre de 2025 (pérdida de ocupación SITUR-Q)]] - concept - docs/decisiones/08-radar.md
- [[Radar tabla mensual de 15 lugares × 55 meses y hallazgo del doble conteo SITUR-QINAH]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Radar tres decisiones del equipo (pesos iguales, cortes comunes, predicción de estados)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Sección de la página radar '¿Dónde hay espacio hoy']] - concept - docs/decisiones/08-radar.md
- [[Series_6]] - code
- [[Una fila por lugar × mes, de DESDE al último mes publicado. Las celdas sin dato…]] - rationale - backend/torre/radar/panel.py
- [[Variables de SITUR-Q por lugar y mes (sin huecos el hueco queda como ausencia…]] - rationale - backend/torre/radar/panel.py
- [[Visitantes (nacionales + extranjeros) a zonas arqueológicas por lugar y mes.]] - rationale - backend/torre/radar/panel.py
- [[Visitantes INAH zona por zona (ZONA_A_LUGAR, sin doble conteo)]] - rationale - docs/decisiones/08-radar.md
- [[_datatur()]] - code - backend/torre/radar/panel.py
- [[_inah()]] - code - backend/torre/radar/panel.py
- [[_poblacion()]] - code - backend/torre/radar/panel.py
- [[_siturq()_1]] - code - backend/torre/radar/panel.py
- [[cobertura()_1]] - code - backend/torre/radar/panel.py
- [[guardar()_5]] - code - backend/torre/radar/panel.py
- [[panel.py]] - code - backend/torre/radar/panel.py
- [[panel_mensual()]] - code - backend/torre/radar/panel.py
- [[Índice comparable (lo que publica el Radar)]] - rationale - docs/decisiones/08-radar.md
- [[Índice de Presión Turística (IPT)]] - concept - docs/plan/PLAN_v3.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Radar_panel_mensual
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan]]
- 3 edges to [[_COMMUNITY_Radar índice de presión (código)]]
- 2 edges to [[_COMMUNITY_D6 DENUE INEGI (32 estados)]]
- 2 edges to [[_COMMUNITY_PLAN_v3.md (plan aprobado)]]
- 1 edge to [[_COMMUNITY_Decisión la campaña promueve 5 regiones de Quintana Roo]]
- 1 edge to [[_COMMUNITY_test_radar_panel.py]]
- 1 edge to [[_COMMUNITY_Censo (ITER) y criterios de regiones]]
- 1 edge to [[_COMMUNITY_Radar clustering de centros]]
- 1 edge to [[_COMMUNITY_markov.py]]
- 1 edge to [[_COMMUNITY_test_planteamiento.py]]
- 1 edge to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_Cap. 4 — Recolección de los datos oficiales (Fase 1) 15 fuentes, 353 archivos, 8,134,802 registros]]

## Top bridge nodes
- [[panel.py]] - degree 16, connects to 7 communities
- [[Índice de Presión Turística (IPT)]] - degree 13, connects to 5 communities
- [[Pieza 1 panel mensual 15 lugares × 55 meses]] - degree 7, connects to 1 community
- [[DataTur y SITUR-Q no miden lo mismo (reconciliación)]] - degree 4, connects to 1 community
- [[Radar tres decisiones del equipo (pesos iguales, cortes comunes, predicción de estados)]] - degree 2, connects to 1 community