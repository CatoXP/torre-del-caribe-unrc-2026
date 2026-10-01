---
type: community
members: 34
---

# Pronóstico: 5 modelos (origen móvil)

**Members:** 34 nodes

## Members
- [[Cada mes destino = el último valor útil de ese mismo mes del año, visto desde…]] - rationale - backend/torre/pronostico/modelos.py
- [[DataFrame_24]] - code
- [[DatetimeIndex]] - code
- [[Desestacionaliza el tramo actual con la forma del año previa al origen, ajusta…]] - rationale - backend/torre/pronostico/modelos.py
- [[Error MAPE]] - concept - docs/metodologia/ECUACIONES.md
- [[Gradient Boosting (por histogramas) entrenado con todos los pares pasados (o' →…]] - rationale - backend/torre/pronostico/modelos.py
- [[Igual que la anterior pero solo con nivel (suavizamiento exponencial simple)…]] - rationale - backend/torre/pronostico/modelos.py
- [[Lluvia total de cada mes (mm) en el punto y si ese mes empezó una tormenta que…]] - rationale - backend/torre/pronostico/modelos.py
- [[MAE y MAPE por serie y modelo, en total y por tramo de horizonte; 'vs base' =…]] - rationale - backend/torre/pronostico/modelos.py
- [[Meses útiles del tramo en curso al origen (desde el último mes que no entrena).]] - rationale - backend/torre/pronostico/modelos.py
- [[Mínimos cuadrados sobre log(valor) un nivel por tramo + 11 meses + anomalía de…]] - rationale - backend/torre/pronostico/modelos.py
- [[Número de tramo de cada mes útil sube cada vez que la serie pasa por meses que…]] - rationale - backend/torre/pronostico/modelos.py
- [[Primer origen cuando ya hay al menos un año completo antes para calcular la…]] - rationale - backend/torre/pronostico/modelos.py
- [[Rasgos de un par (origen o → destino d) usando solo meses útiles hasta o (x =…]] - rationale - backend/torre/pronostico/modelos.py
- [[Series_6]] - code
- [[Timestamp_1]] - code
- [[Una fila por (serie, modelo, origen, horizonte) con el pronóstico y el valor…]] - rationale - backend/torre/pronostico/modelos.py
- [[_rasgos()]] - code - backend/torre/pronostico/modelos.py
- [[_tramos()]] - code - backend/torre/pronostico/modelos.py
- [[clima_mensual()]] - code - backend/torre/pronostico/modelos.py
- [[correr()_6]] - code - backend/torre/pronostico/modelos.py
- [[forma_hasta()]] - code - backend/torre/pronostico/modelos.py
- [[gradient_boosting_rezagos()]] - code - backend/torre/pronostico/modelos.py
- [[holt_winters_forma_fija()]] - code - backend/torre/pronostico/modelos.py
- [[holt_winters_sin_tendencia()]] - code - backend/torre/pronostico/modelos.py
- [[ingenuo_estacional()]] - code - backend/torre/pronostico/modelos.py
- [[metricas()]] - code - backend/torre/pronostico/modelos.py
- [[modelos.py]] - code - backend/torre/pronostico/modelos.py
- [[ndarray_2]] - code
- [[origen_movil()_1]] - code - backend/torre/pronostico/modelos.py
- [[primer_origen()]] - code - backend/torre/pronostico/modelos.py
- [[regresion_con_clima()]] - code - backend/torre/pronostico/modelos.py
- [[tramo_actual()]] - code - backend/torre/pronostico/modelos.py
- [[Índices de la forma del año usando SOLO años completos que terminaron antes del…]] - rationale - backend/torre/pronostico/modelos.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pronóstico_5_modelos_origen_móvil
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Pronóstico forma del año]]
- 4 edges to [[_COMMUNITY_Decisión 11 decisiones del Pronóstico]]
- 3 edges to [[_COMMUNITY_Pronóstico tormentas y escenarios]]
- 3 edges to [[_COMMUNITY_Regresión logística multiclase (modelo elegido del Radar)]]
- 1 edge to [[_COMMUNITY_prediccion.py]]
- 1 edge to [[_COMMUNITY_Pronóstico rango del 90 % (conformal)]]
- 1 edge to [[_COMMUNITY_test_radar_prediccion.py]]
- 1 edge to [[_COMMUNITY_clustering.py]]
- 1 edge to [[_COMMUNITY_criterios.py]]
- 1 edge to [[_COMMUNITY_entrega.py]]
- 1 edge to [[_COMMUNITY_pdf.py]]

## Top bridge nodes
- [[modelos.py]] - degree 24, connects to 8 communities
- [[Error MAPE]] - degree 3, connects to 2 communities
- [[regresion_con_clima()]] - degree 10, connects to 1 community
- [[forma_hasta()]] - degree 9, connects to 1 community
- [[gradient_boosting_rezagos()]] - degree 9, connects to 1 community