---
type: community
members: 40
---

# Radar: índice y predicción (código)

**Members:** 40 nodes

## Members
- [[Backtesting con origen móvil para cada mes objetivo de la prueba se reentrena…]] - rationale - backend/torre/radar/prediccion.py
- [[Cortes comunes percentiles p50 y p90 del IPT de todos los lugares y meses con…]] - rationale - backend/torre/radar/indice.py
- [[DataFrame_10]] - code
- [[DataFrame_11]] - code
- [[Entrena con los objetivos antes de INICIO_PRUEBA y evalúa en los 12 meses…]] - rationale - backend/torre/radar/prediccion.py
- [[Escala mín–máx común (decisión 4)]] - rationale - docs/decisiones/08-radar.md
- [[IPT = Σ w_k z_k  Σ w_k, solo con los componentes que el lugar tiene ese mes.…]] - rationale - backend/torre/radar/indice.py
- [[IPT con las medidas que cada lugar tiene en su último mes con dato, solo en los…]] - rationale - backend/torre/radar/prediccion.py
- [[Los candidatos que tienen dato en al menos MIN_LUGARES lugares (los demás no se…]] - rationale - backend/torre/radar/indice.py
- [[Mueve el peso de cada componente a 0.5 y a 1.5 (los demás en 1) y cuenta…]] - rationale - backend/torre/radar/indice.py
- [[Path_11]] - code
- [[Random Forest elegido (136156 aciertos, 7 cambios anticipados)]] - rationale - docs/decisiones/08-radar.md
- [[Reentrena el modelo elegido con TODO lo disponible y predice el mes siguiente…]] - rationale - backend/torre/radar/prediccion.py
- [[Sesgo (punto del plan, Fase 4) el mismo origen móvil del modelo elegido,…]] - rationale - backend/torre/radar/prediccion.py
- [[Una fila por lugar y mes t lo que se sabe en t (índice, rezagos, mes del año)…]] - rationale - backend/torre/radar/prediccion.py
- [[calcular()]] - code - backend/torre/radar/indice.py
- [[comparar()]] - code - backend/torre/radar/prediccion.py
- [[componentes()]] - code - backend/torre/radar/indice.py
- [[correr()_2]] - code - backend/torre/radar/prediccion.py
- [[elegir_componentes()]] - code - backend/torre/radar/indice.py
- [[estados()_1]] - code - backend/torre/radar/indice.py
- [[guardar()_1]] - code - backend/torre/radar/indice.py
- [[indice.py]] - code - backend/torre/radar/indice.py
- [[indice_comparable()]] - code - backend/torre/radar/prediccion.py
- [[ipt()]] - code - backend/torre/radar/indice.py
- [[minmax()]] - code - backend/torre/radar/indice.py
- [[modelos()]] - code - backend/torre/radar/prediccion.py
- [[origen_movil()]] - code - backend/torre/radar/prediccion.py
- [[predecir_mes_siguiente()]] - code - backend/torre/radar/prediccion.py
- [[prediccion.py]] - code - backend/torre/radar/prediccion.py
- [[sensibilidad()]] - code - backend/torre/radar/indice.py
- [[sesgo()]] - code - backend/torre/radar/prediccion.py
- [[sklearn_ensemble]] - concept
- [[sklearn_linear_model]] - concept
- [[sklearn_metrics]] - concept
- [[sklearn_pipeline]] - concept
- [[sklearn_preprocessing]] - concept
- [[tabla_de_aprendizaje()]] - code - backend/torre/radar/prediccion.py
- [[x_k de cada lugar y mes llegadas por mil habitantes y ocupación (%). Sin dato…]] - rationale - backend/torre/radar/indice.py
- [[z_k = (x_k − mín_k)  (máx_k − mín_k), con mín y máx de TODOS los lugares y…]] - rationale - backend/torre/radar/indice.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Radar_índice_y_predicción_código
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Radar panel mensual (código)]]
- 2 edges to [[_COMMUNITY_Radar pruebas del clustering]]
- 2 edges to [[_COMMUNITY_Pruebas del planteamiento]]
- 2 edges to [[_COMMUNITY_Silver ocupación DataTur y Spark (pathlib)]]
- 2 edges to [[_COMMUNITY_Radar decisiones y piezas]]
- 1 edge to [[_COMMUNITY_Planteamiento (HHI) y clustering de centros]]
- 1 edge to [[_COMMUNITY_Radar pruebas del índice]]
- 1 edge to [[_COMMUNITY_Radar pruebas de la predicción]]

## Top bridge nodes
- [[prediccion.py]] - degree 22, connects to 6 communities
- [[indice.py]] - degree 16, connects to 6 communities
- [[sklearn_metrics]] - degree 2, connects to 1 community