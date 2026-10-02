---
type: community
members: 59
---

# Radar: índice de presión (código)

**Members:** 59 nodes

## Members
- [[Backtesting con origen móvil para cada mes objetivo de la prueba se reentrena…]] - rationale - backend/torre/radar/prediccion.py
- [[Componente llegadas por cuarto (tren + cruceros)]] - rationale - docs/decisiones/08-radar.md
- [[Cortes comunes percentiles p50 y p90 del IPT de todos los lugares y meses con…]] - rationale - backend/torre/radar/indice.py
- [[Criterio de selección de modelo más aciertos y más cambios anticipados]] - rationale - docs/decisiones/08-radar.md
- [[DataFrame_15]] - code
- [[DataFrame_16]] - code
- [[Entrena con los objetivos antes de INICIO_PRUEBA y evalúa en los 12 meses…]] - rationale - backend/torre/radar/prediccion.py
- [[Escala mín–máx común]] - concept - docs/metodologia/ECUACIONES.md
- [[Escala mín–máx común (decisión 4)]] - rationale - docs/decisiones/08-radar.md
- [[Estados tranquiloconcurridosaturado por percentiles 50 y 90]] - concept - docs/metodologia/ECUACIONES.md
- [[F1 macro y cambios anticipados]] - concept - docs/metodologia/ECUACIONES.md
- [[IPT = Σ w_k z_k  Σ w_k, solo con los componentes que el lugar tiene ese mes.…]] - rationale - backend/torre/radar/indice.py
- [[IPT con las medidas que cada lugar tiene en su último mes con dato, solo en los…]] - rationale - backend/torre/radar/prediccion.py
- [[Limitación quiebre de 2025 (SITUR-Q deja de publicar ocupación del sur)]] - rationale - docs/metodologia/ECUACIONES.md
- [[Llegadas por cuarto (tren + cruceros)]] - concept - docs/metodologia/ECUACIONES.md
- [[Los candidatos que tienen dato en al menos MIN_LUGARES lugares (los demás no se…]] - rationale - backend/torre/radar/indice.py
- [[Línea base de persistencia]] - concept - docs/metodologia/ECUACIONES.md
- [[Línea base de persistencia (ŷ_{t+1} = y_t)]] - concept - docs/metodologia/ECUACIONES.md
- [[Línea base ingenuo estacional]] - concept - docs/metodologia/ECUACIONES.md
- [[Modelo estocástico de dos etapas (Investigación de Operaciones)]] - concept - docs/metodologia/ECUACIONES.md
- [[Mueve el peso de cada componente a 0.5 y a 1.5 (los demás en 1) y cuenta…]] - rationale - backend/torre/radar/indice.py
- [[Path_2]] - code
- [[Predicción del estado del mes siguiente (regresión logística multiclase elegida)]] - concept - docs/metodologia/ECUACIONES.md
- [[Random Forest (400 árboles)]] - concept - docs/metodologia/ECUACIONES.md
- [[Random Forest elegido (136156 aciertos, 7 cambios anticipados)]] - rationale - docs/decisiones/08-radar.md
- [[Reentrena el modelo elegido con TODO lo disponible y predice el mes siguiente…]] - rationale - backend/torre/radar/prediccion.py
- [[Regla de pausa semanal de la campaña]] - concept - docs/metodologia/ECUACIONES.md
- [[Regresión logística multiclase (modelo elegido del Radar)]] - concept - docs/metodologia/ECUACIONES.md
- [[Sensibilidad de pesos del IPT (0.5  1.5)]] - concept - docs/metodologia/ECUACIONES.md
- [[Sesgo (punto del plan, Fase 4) el mismo origen móvil del modelo elegido,…]] - rationale - backend/torre/radar/prediccion.py
- [[Sesgo el modelo no se puede validar en los 5 lugares]] - rationale - docs/decisiones/09-auditoria-fases-1-4.md
- [[Una fila por lugar y mes t lo que se sabe en t (índice, rezagos, mes del año)…]] - rationale - backend/torre/radar/prediccion.py
- [[calcular()]] - code - backend/torre/radar/indice.py
- [[comparar()]] - code - backend/torre/radar/prediccion.py
- [[componentes()]] - code - backend/torre/radar/indice.py
- [[correr()_5]] - code - backend/torre/radar/prediccion.py
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
- [[sensibilidad()_1]] - code - backend/torre/radar/indice.py
- [[sesgo()]] - code - backend/torre/radar/prediccion.py
- [[sklearn_ensemble]] - concept
- [[sklearn_linear_model]] - concept
- [[sklearn_metrics]] - concept
- [[sklearn_pipeline]] - concept
- [[sklearn_preprocessing]] - concept
- [[tabla_de_aprendizaje()]] - code - backend/torre/radar/prediccion.py
- [[x_k de cada lugar y mes llegadas por mil habitantes y ocupación (%). Sin dato…]] - rationale - backend/torre/radar/indice.py
- [[z_k = (x_k − mín_k)  (máx_k − mín_k), con mín y máx de TODOS los lugares y…]] - rationale - backend/torre/radar/indice.py
- [[Índice comparable IPTc]] - concept - docs/metodologia/ECUACIONES.md
- [[Índice de Presión Turística (IPT) con pesos iguales]] - concept - docs/metodologia/ECUACIONES.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Radar_índice_de_presión_código
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan]]
- 5 edges to [[_COMMUNITY_Silver FRED y series a pronosticar]]
- 3 edges to [[_COMMUNITY_Radar panel mensual]]
- 2 edges to [[_COMMUNITY_numpy]]
- 2 edges to [[_COMMUNITY_test_planteamiento.py]]
- 2 edges to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_Pronóstico forma del año y modelos]]
- 1 edge to [[_COMMUNITY_Radar clustering de centros]]
- 1 edge to [[_COMMUNITY_test_radar_indice.py]]
- 1 edge to [[_COMMUNITY_test_radar_prediccion.py]]
- 1 edge to [[_COMMUNITY_markov.py]]
- 1 edge to [[_COMMUNITY_requirements.txt]]
- 1 edge to [[_COMMUNITY_Hoja de ruta fases 5 a 7]]
- 1 edge to [[_COMMUNITY_Censo (ITER) y criterios de regiones]]
- 1 edge to [[_COMMUNITY_Planeador NLP de negocios (DENUE)]]

## Top bridge nodes
- [[prediccion.py]] - degree 21, connects to 5 communities
- [[indice.py]] - degree 15, connects to 5 communities
- [[Índice de Presión Turística (IPT) con pesos iguales]] - degree 16, connects to 3 communities
- [[Modelo estocástico de dos etapas (Investigación de Operaciones)]] - degree 5, connects to 2 communities
- [[Línea base ingenuo estacional]] - degree 5, connects to 2 communities