---
type: community
members: 18
---

# Radar: índice de presión (código)

**Members:** 18 nodes

## Members
- [[Cortes comunes percentiles p50 y p90 del IPT de todos los lugares y meses con…]] - rationale - backend/torre/radar/indice.py
- [[DataFrame_9]] - code
- [[Escala mín–máx común (decisión 4)]] - rationale - docs/decisiones/08-radar.md
- [[IPT = Σ w_k z_k  Σ w_k, solo con los componentes que el lugar tiene ese mes.…]] - rationale - backend/torre/radar/indice.py
- [[Los candidatos que tienen dato en al menos MIN_LUGARES lugares (los demás no se…]] - rationale - backend/torre/radar/indice.py
- [[Mueve el peso de cada componente a 0.5 y a 1.5 (los demás en 1) y cuenta…]] - rationale - backend/torre/radar/indice.py
- [[Path_3]] - code
- [[calcular()_1]] - code - backend/torre/radar/indice.py
- [[componentes()]] - code - backend/torre/radar/indice.py
- [[elegir_componentes()]] - code - backend/torre/radar/indice.py
- [[estados()]] - code - backend/torre/radar/indice.py
- [[guardar()_1]] - code - backend/torre/radar/indice.py
- [[indice.py]] - code - backend/torre/radar/indice.py
- [[ipt()]] - code - backend/torre/radar/indice.py
- [[minmax()]] - code - backend/torre/radar/indice.py
- [[sensibilidad()_1]] - code - backend/torre/radar/indice.py
- [[x_k de cada lugar y mes llegadas por mil habitantes y ocupación (%). Sin dato…]] - rationale - backend/torre/radar/indice.py
- [[z_k = (x_k − mín_k)  (máx_k − mín_k), con mín y máx de TODOS los lugares y…]] - rationale - backend/torre/radar/indice.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Radar_índice_de_presión_código
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_prediccion.py (Índice de Presión Turíst)]]
- 3 edges to [[_COMMUNITY_prediccion.py]]
- 1 edge to [[_COMMUNITY_pandas]]
- 1 edge to [[_COMMUNITY_test_radar_panel.py]]
- 1 edge to [[_COMMUNITY_pathlib (pathlib)]]
- 1 edge to [[_COMMUNITY_markov.py]]
- 1 edge to [[_COMMUNITY_test_radar_indice.py]]

## Top bridge nodes
- [[indice.py]] - degree 15, connects to 6 communities
- [[calcular()_1]] - degree 10, connects to 1 community
- [[estados()]] - degree 6, connects to 1 community
- [[ipt()]] - degree 6, connects to 1 community
- [[sensibilidad()_1]] - degree 6, connects to 1 community