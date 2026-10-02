---
type: community
members: 18
---

# Radar: predicción del estado

**Members:** 18 nodes

## Members
- [[Cortes comunes percentiles p50 y p90 del IPT de todos los lugares y meses con…]] - rationale - backend/torre/radar/indice.py
- [[DataFrame_12]] - code
- [[Escala mín–máx común (decisión 4)]] - rationale - docs/decisiones/08-radar.md
- [[IPT = Σ w_k z_k  Σ w_k, solo con los componentes que el lugar tiene ese mes.…]] - rationale - backend/torre/radar/indice.py
- [[Los candidatos que tienen dato en al menos MIN_LUGARES lugares (los demás no se…]] - rationale - backend/torre/radar/indice.py
- [[Mueve el peso de cada componente a 0.5 y a 1.5 (los demás en 1) y cuenta…]] - rationale - backend/torre/radar/indice.py
- [[Path_2]] - code
- [[calcular()]] - code - backend/torre/radar/indice.py
- [[componentes()]] - code - backend/torre/radar/indice.py
- [[elegir_componentes()]] - code - backend/torre/radar/indice.py
- [[estados()_1]] - code - backend/torre/radar/indice.py
- [[guardar()_2]] - code - backend/torre/radar/indice.py
- [[indice.py]] - code - backend/torre/radar/indice.py
- [[ipt()]] - code - backend/torre/radar/indice.py
- [[minmax()]] - code - backend/torre/radar/indice.py
- [[sensibilidad()_1]] - code - backend/torre/radar/indice.py
- [[x_k de cada lugar y mes llegadas por mil habitantes y ocupación (%). Sin dato…]] - rationale - backend/torre/radar/indice.py
- [[z_k = (x_k − mín_k)  (máx_k − mín_k), con mín y máx de TODOS los lugares y…]] - rationale - backend/torre/radar/indice.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Radar_predicción_del_estado
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_prediccion.py]]
- 3 edges to [[_COMMUNITY_numpy]]
- 2 edges to [[_COMMUNITY_Índice de Presión Turística (IPT)]]
- 1 edge to [[_COMMUNITY_panel.py]]
- 1 edge to [[_COMMUNITY_test_radar_indice.py]]
- 1 edge to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan (Cadena de Markov semanal)]]

## Top bridge nodes
- [[indice.py]] - degree 18, connects to 6 communities
- [[calcular()]] - degree 10, connects to 1 community