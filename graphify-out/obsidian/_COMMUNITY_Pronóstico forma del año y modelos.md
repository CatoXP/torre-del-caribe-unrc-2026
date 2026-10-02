---
type: community
members: 52
---

# Pronóstico: forma del año y modelos

**Members:** 52 nodes

## Members
- [[Años con los 12 meses entrenables (sin cierre, mes parcial ni pandemia).]] - rationale - backend/torre/pronostico/forma.py
- [[Cada mes destino = el último valor útil de ese mismo mes del año, visto desde…]] - rationale - backend/torre/pronostico/modelos.py
- [[Correlación entre el índice de este método y el que da STL (en logaritmos)…]] - rationale - backend/torre/pronostico/forma.py
- [[Correlación entre la forma del año de cada lugar del sur y la de Cancún cerca…]] - rationale - backend/torre/pronostico/forma.py
- [[DataFrame_24]] - code
- [[DataFrame_25]] - code
- [[DatetimeIndex]] - code
- [[Desestacionaliza el tramo actual con la forma del año previa al origen, ajusta…]] - rationale - backend/torre/pronostico/modelos.py
- [[El tramo más largo de meses seguidos que entrenan (para la segunda opinión con…]] - rationale - backend/torre/pronostico/forma.py
- [[F = max(0, 1 − Var(e)  Var(s + e)) en logaritmos s = log(índice del mes), e =…]] - rationale - backend/torre/pronostico/forma.py
- [[Gradient Boosting (por histogramas) entrenado con todos los pares pasados (o' →…]] - rationale - backend/torre/pronostico/modelos.py
- [[Igual que la anterior pero solo con nivel (suavizamiento exponencial simple)…]] - rationale - backend/torre/pronostico/modelos.py
- [[Lluvia total de cada mes (mm) en el punto y si ese mes empezó una tormenta que…]] - rationale - backend/torre/pronostico/modelos.py
- [[MAE y MAPE por serie y modelo, en total y por tramo de horizonte; 'vs base' =…]] - rationale - backend/torre/pronostico/modelos.py
- [[Meses útiles del tramo en curso al origen (desde el último mes que no entrena).]] - rationale - backend/torre/pronostico/modelos.py
- [[Mínimos cuadrados sobre log(valor) un nivel por tramo + 11 meses + anomalía de…]] - rationale - backend/torre/pronostico/modelos.py
- [[Número de tramo de cada mes útil sube cada vez que la serie pasa por meses que…]] - rationale - backend/torre/pronostico/modelos.py
- [[Primer origen cuando ya hay al menos un año completo antes para calcular la…]] - rationale - backend/torre/pronostico/modelos.py
- [[Promedio por mes de las razones, reescalado para que los 12 índices promedien…]] - rationale - backend/torre/pronostico/forma.py
- [[Rasgos de un par (origen o → destino d) usando solo meses útiles hasta o (x =…]] - rationale - backend/torre/pronostico/modelos.py
- [[Series_4]] - code
- [[Series_5]] - code
- [[Tabla año × mes con valor ÷ promedio del año, solo en años completos.]] - rationale - backend/torre/pronostico/forma.py
- [[Timestamp_2]] - code
- [[Una fila por (serie, modelo, origen, horizonte) con el pronóstico y el valor…]] - rationale - backend/torre/pronostico/modelos.py
- [[_rasgos()]] - code - backend/torre/pronostico/modelos.py
- [[_tramos()]] - code - backend/torre/pronostico/modelos.py
- [[acompana_al_norte()]] - code - backend/torre/pronostico/forma.py
- [[anios_completos()]] - code - backend/torre/pronostico/forma.py
- [[calcular()_1]] - code - backend/torre/pronostico/forma.py
- [[clima_mensual()]] - code - backend/torre/pronostico/modelos.py
- [[correr()_6]] - code - backend/torre/pronostico/modelos.py
- [[forma.py]] - code - backend/torre/pronostico/forma.py
- [[forma_hasta()]] - code - backend/torre/pronostico/modelos.py
- [[fuerza_estacional()]] - code - backend/torre/pronostico/forma.py
- [[gradient_boosting_rezagos()]] - code - backend/torre/pronostico/modelos.py
- [[guardar()_4]] - code - backend/torre/pronostico/forma.py
- [[holt_winters_forma_fija()]] - code - backend/torre/pronostico/modelos.py
- [[holt_winters_sin_tendencia()]] - code - backend/torre/pronostico/modelos.py
- [[indice_estacional()]] - code - backend/torre/pronostico/forma.py
- [[ingenuo_estacional()]] - code - backend/torre/pronostico/modelos.py
- [[metricas()]] - code - backend/torre/pronostico/modelos.py
- [[modelos.py]] - code - backend/torre/pronostico/modelos.py
- [[ndarray_2]] - code
- [[origen_movil()_1]] - code - backend/torre/pronostico/modelos.py
- [[primer_origen()]] - code - backend/torre/pronostico/modelos.py
- [[razones()]] - code - backend/torre/pronostico/forma.py
- [[regresion_con_clima()]] - code - backend/torre/pronostico/modelos.py
- [[segunda_opinion_stl()]] - code - backend/torre/pronostico/forma.py
- [[tramo_actual()]] - code - backend/torre/pronostico/modelos.py
- [[tramo_continuo()]] - code - backend/torre/pronostico/forma.py
- [[Índices de la forma del año usando SOLO años completos que terminaron antes del…]] - rationale - backend/torre/pronostico/modelos.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pronóstico_forma_del_año_y_modelos
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Silver FRED y series a pronosticar]]
- 4 edges to [[_COMMUNITY_numpy]]
- 3 edges to [[_COMMUNITY_Pronóstico tormentas y escenarios]]
- 3 edges to [[_COMMUNITY_Planeador NLP de negocios (DENUE)]]
- 2 edges to [[_COMMUNITY_test_planteamiento.py]]
- 2 edges to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_Radar índice de presión (código)]]
- 1 edge to [[_COMMUNITY_ECUACIONES]]
- 1 edge to [[_COMMUNITY_Pronóstico rango del 90 % y elección]]

## Top bridge nodes
- [[modelos.py]] - degree 23, connects to 5 communities
- [[forma.py]] - degree 15, connects to 4 communities
- [[regresion_con_clima()]] - degree 10, connects to 1 community
- [[gradient_boosting_rezagos()]] - degree 9, connects to 1 community
- [[holt_winters_forma_fija()]] - degree 9, connects to 1 community