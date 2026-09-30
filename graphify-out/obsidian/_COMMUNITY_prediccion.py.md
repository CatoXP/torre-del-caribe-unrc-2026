---
type: community
members: 60
---

# prediccion.py

**Members:** 60 nodes

## Members
- [[Backtesting con origen móvil (validación temporal)]] - concept - docs/metodologia/ECUACIONES.md
- [[Backtesting con origen móvil para cada mes objetivo de la prueba se reentrena…]] - rationale - backend/torre/radar/prediccion.py
- [[Cortes comunes percentiles p50 y p90 del IPT de todos los lugares y meses con…]] - rationale - backend/torre/radar/indice.py
- [[DataFrame]] - code
- [[DataFrame_1]] - code
- [[Decisión 11 — A3 Pronóstico (Fase 5, en curso)]] - document - docs/decisiones/11-pronostico.md
- [[Decisión 1 pronosticar 'Medidas + norte']] - rationale - docs/decisiones/11-pronostico.md
- [[Entrena con los objetivos antes de INICIO_PRUEBA y evalúa en los 12 meses…]] - rationale - backend/torre/radar/prediccion.py
- [[Escala mín–máx común]] - concept - docs/metodologia/ECUACIONES.md
- [[Escala mín–máx común (decisión 4)]] - rationale - docs/decisiones/08-radar.md
- [[Holt-Winters aditivo]] - concept - docs/metodologia/ECUACIONES.md
- [[Hueco Tren Maya con menos de 24 meses (variable, no se pronostica)]] - rationale - docs/decisiones/11-pronostico.md
- [[IPT = Σ w_k z_k  Σ w_k, solo con los componentes que el lugar tiene ese mes.…]] - rationale - backend/torre/radar/indice.py
- [[IPT con las medidas que cada lugar tiene en su último mes con dato, solo en los…]] - rationale - backend/torre/radar/prediccion.py
- [[Incidente crítico Aprendizaje de máquina (turismo más sustentable)]] - concept - OBJETIVO.md
- [[Intervalo conformal al 90 %]] - concept - docs/metodologia/ECUACIONES.md
- [[Llegadas por cuarto (tren + cruceros)]] - concept - docs/metodologia/ECUACIONES.md
- [[Los candidatos que tienen dato en al menos MIN_LUGARES lugares (los demás no se…]] - rationale - backend/torre/radar/indice.py
- [[Modelo estocástico de dos etapas (Investigación de Operaciones)]] - concept - docs/metodologia/ECUACIONES.md
- [[Monte Carlo de escenarios malo  probable  bueno]] - concept - docs/metodologia/ECUACIONES.md
- [[Mueve el peso de cada componente a 0.5 y a 1.5 (los demás en 1) y cuenta…]] - rationale - backend/torre/radar/indice.py
- [[Ocupación hotelera de Cancún (serie de referencia)]] - concept - docs/decisiones/11-pronostico.md
- [[Path]] - code
- [[Pieza 2 descomposición estacional (forma y fuerza de la temporada)]] - concept - docs/decisiones/11-pronostico.md
- [[Puntaje de anomalía Isolation Forest]] - concept - docs/metodologia/ECUACIONES.md
- [[Random Forest elegido (136156 aciertos, 7 cambios anticipados)]] - rationale - docs/decisiones/08-radar.md
- [[Reentrena el modelo elegido con TODO lo disponible y predice el mes siguiente…]] - rationale - backend/torre/radar/prediccion.py
- [[Regla de pausa semanal de la campaña]] - concept - docs/metodologia/ECUACIONES.md
- [[Sensibilidad de pesos del IPT (0.5  1.5)]] - concept - docs/metodologia/ECUACIONES.md
- [[Serie de cruces desde Belice (Chetumal)]] - concept - docs/decisiones/11-pronostico.md
- [[Sesgo (punto del plan, Fase 4) el mismo origen móvil del modelo elegido,…]] - rationale - backend/torre/radar/prediccion.py
- [[Sesgo medido el modelo no anticipa cambios en los 5 lugares]] - rationale - docs/metodologia/ECUACIONES.md
- [[Una fila por lugar y mes t lo que se sabe en t (índice, rezagos, mes del año)…]] - rationale - backend/torre/radar/prediccion.py
- [[calcular()]] - code - backend/torre/radar/indice.py
- [[comparar()]] - code - backend/torre/radar/prediccion.py
- [[componentes()]] - code - backend/torre/radar/indice.py
- [[correr()]] - code - backend/torre/radar/prediccion.py
- [[elegir_componentes()]] - code - backend/torre/radar/indice.py
- [[estados()]] - code - backend/torre/radar/indice.py
- [[guardar()]] - code - backend/torre/radar/indice.py
- [[indice.py]] - code - backend/torre/radar/indice.py
- [[indice_comparable()]] - code - backend/torre/radar/prediccion.py
- [[ipt()]] - code - backend/torre/radar/indice.py
- [[minmax()]] - code - backend/torre/radar/indice.py
- [[modelos()]] - code - backend/torre/radar/prediccion.py
- [[origen_movil()]] - code - backend/torre/radar/prediccion.py
- [[predecir_mes_siguiente()]] - code - backend/torre/radar/prediccion.py
- [[prediccion.py]] - code - backend/torre/radar/prediccion.py
- [[scikit-learn==1.5.2 (clasificador, Isolation Forest, TF-IDF)]] - concept - requirements.txt
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
- [[Índice de presión turística (IPT) con pesos iguales]] - concept - docs/metodologia/ECUACIONES.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/prediccionpy
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Criterio de selección de modelo más aciertos y más cambios anticipados]]
- 3 edges to [[_COMMUNITY_panel.py]]
- 2 edges to [[_COMMUNITY_Reglas de oro (a–h)]]
- 2 edges to [[_COMMUNITY_test_radar_clustering.py]]
- 2 edges to [[_COMMUNITY_Fotos y ubicación comprobada]]
- 2 edges to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan]]
- 1 edge to [[_COMMUNITY_test_radar_indice.py]]
- 1 edge to [[_COMMUNITY_test_radar_prediccion.py]]
- 1 edge to [[_COMMUNITY_Pronóstico pruebas de las series]]
- 1 edge to [[_COMMUNITY_Decisión 08 — A1 Radar (Fase 4)]]
- 1 edge to [[_COMMUNITY_Fase 7 — Torre en vivo]]
- 1 edge to [[_COMMUNITY_silver_iter.py]]
- 1 edge to [[_COMMUNITY_Pronóstico series a pronosticar]]
- 1 edge to [[_COMMUNITY_test_silver_fase5.py]]
- 1 edge to [[_COMMUNITY_entorno.py]]

## Top bridge nodes
- [[prediccion.py]] - degree 22, connects to 6 communities
- [[indice.py]] - degree 15, connects to 5 communities
- [[Decisión 11 — A3 Pronóstico (Fase 5, en curso)]] - degree 11, connects to 5 communities
- [[Índice de presión turística (IPT) con pesos iguales]] - degree 8, connects to 2 communities
- [[predecir_mes_siguiente()]] - degree 6, connects to 1 community