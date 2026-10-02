---
type: community
members: 82
---

# Pronóstico: forma del año y modelos

**Members:** 82 nodes

## Members
- [[12 meses después del último mes publicado de cada serie, con el modelo elegido…]] - rationale - backend/torre/pronostico/seleccion.py
- [[Años con los 12 meses entrenables (sin cierre, mes parcial ni pandemia).]] - rationale - backend/torre/pronostico/forma.py
- [[Backtesting con origen móvil]] - concept - docs/metodologia/ECUACIONES.md
- [[Cada mes destino = el último valor útil de ese mismo mes del año, visto desde…]] - rationale - backend/torre/pronostico/modelos.py
- [[Correlación entre el índice de este método y el que da STL (en logaritmos)…]] - rationale - backend/torre/pronostico/forma.py
- [[Correlación entre la forma del año de cada lugar del sur y la de Cancún cerca…]] - rationale - backend/torre/pronostico/forma.py
- [[Criterio de elección menor MAE con cobertura ≥80 %]] - rationale - docs/metodologia/ECUACIONES.md
- [[Cuantil ⌈(n+1)·nivel⌉n de los errores de calibración (el más chico que…]] - rationale - backend/torre/pronostico/intervalos.py
- [[DataFrame]] - code
- [[DataFrame_1]] - code
- [[DataFrame_2]] - code
- [[DataFrame_3]] - code
- [[DatetimeIndex]] - code
- [[Decisión Menor error con rango ≥ 80 %]] - rationale - docs/decisiones/11-pronostico.md
- [[Desestacionaliza el tramo actual con la forma del año previa al origen, ajusta…]] - rationale - backend/torre/pronostico/modelos.py
- [[El tramo más largo de meses seguidos que entrenan (para la segunda opinión con…]] - rationale - backend/torre/pronostico/forma.py
- [[F = max(0, 1 − Var(e)  Var(s + e)) en logaritmos s = log(índice del mes), e =…]] - rationale - backend/torre/pronostico/forma.py
- [[Gradient Boosting (por histogramas) entrenado con todos los pares pasados (o' →…]] - rationale - backend/torre/pronostico/modelos.py
- [[Gradient Boosting con rezagos]] - concept - docs/decisiones/11-pronostico.md
- [[Holt-Winters con forma del año fija]] - concept - docs/metodologia/ECUACIONES.md
- [[Igual que la anterior pero solo con nivel (suavizamiento exponencial simple)…]] - rationale - backend/torre/pronostico/modelos.py
- [[Lluvia total de cada mes (mm) en el punto y si ese mes empezó una tormenta que…]] - rationale - backend/torre/pronostico/modelos.py
- [[Línea base ingenuo estacional]] - concept - docs/metodologia/ECUACIONES.md
- [[Línea base mismo mes del año anterior (elegida en Cancún)]] - concept - docs/decisiones/11-pronostico.md
- [[MAE y MAPE por serie y modelo, en total y por tramo de horizonte; 'vs base' =…]] - rationale - backend/torre/pronostico/modelos.py
- [[Meses útiles del tramo en curso al origen (desde el último mes que no entrena).]] - rationale - backend/torre/pronostico/modelos.py
- [[Mínimos cuadrados sobre log(valor) un nivel por tramo + 11 meses + anomalía de…]] - rationale - backend/torre/pronostico/modelos.py
- [[Número de tramo de cada mes útil sube cada vez que la serie pasa por meses que…]] - rationale - backend/torre/pronostico/modelos.py
- [[Por serie y modelo cuántos pronósticos tienen rango, qué % cayó dentro y qué…]] - rationale - backend/torre/pronostico/intervalos.py
- [[Por serie menor MAE entre los modelos con cobertura ≥ 80 %. Devuelve la tabla…]] - rationale - backend/torre/pronostico/seleccion.py
- [[Primer origen cuando ya hay al menos un año completo antes para calcular la…]] - rationale - backend/torre/pronostico/modelos.py
- [[Promedio por mes de las razones, reescalado para que los 12 índices promedien…]] - rationale - backend/torre/pronostico/forma.py
- [[Rango conformal del 90 % y cobertura real]] - concept - docs/decisiones/11-pronostico.md
- [[Rango del 90 % por conformal secuencial]] - concept - docs/metodologia/ECUACIONES.md
- [[Rasgos de un par (origen o → destino d) usando solo meses útiles hasta o (x =…]] - rationale - backend/torre/pronostico/modelos.py
- [[Regresión con clima (modelo elegido en Bahía, Ruta y Belice)]] - concept - docs/decisiones/11-pronostico.md
- [[Regresión con clima (nivel por tramo + mes + lluvia + tormenta)]] - concept - docs/metodologia/ECUACIONES.md
- [[Series]] - code
- [[Series_1]] - code
- [[Series_2]] - code
- [[Tabla año × mes con valor ÷ promedio del año, solo en años completos.]] - rationale - backend/torre/pronostico/forma.py
- [[Timestamp]] - code
- [[Una fila por (serie, modelo, origen, horizonte) con el pronóstico y el valor…]] - rationale - backend/torre/pronostico/modelos.py
- [[_rasgos()]] - code - backend/torre/pronostico/modelos.py
- [[_tramos()]] - code - backend/torre/pronostico/modelos.py
- [[acompana_al_norte()]] - code - backend/torre/pronostico/forma.py
- [[agregar_intervalos()]] - code - backend/torre/pronostico/intervalos.py
- [[anios_completos()]] - code - backend/torre/pronostico/forma.py
- [[calcular()]] - code - backend/torre/pronostico/forma.py
- [[clima_mensual()]] - code - backend/torre/pronostico/modelos.py
- [[cobertura()]] - code - backend/torre/pronostico/intervalos.py
- [[correr()]] - code - backend/torre/pronostico/intervalos.py
- [[correr()_1]] - code - backend/torre/pronostico/modelos.py
- [[correr()_2]] - code - backend/torre/pronostico/seleccion.py
- [[cuantil_conformal()]] - code - backend/torre/pronostico/intervalos.py
- [[elegir()]] - code - backend/torre/pronostico/seleccion.py
- [[forma.py]] - code - backend/torre/pronostico/forma.py
- [[forma_hasta()]] - code - backend/torre/pronostico/modelos.py
- [[fuerza_estacional()]] - code - backend/torre/pronostico/forma.py
- [[gradient_boosting_rezagos()]] - code - backend/torre/pronostico/modelos.py
- [[guardar()]] - code - backend/torre/pronostico/forma.py
- [[holt_winters_forma_fija()]] - code - backend/torre/pronostico/modelos.py
- [[holt_winters_sin_tendencia()]] - code - backend/torre/pronostico/modelos.py
- [[indice_estacional()]] - code - backend/torre/pronostico/forma.py
- [[ingenuo_estacional()]] - code - backend/torre/pronostico/modelos.py
- [[intervalos.py]] - code - backend/torre/pronostico/intervalos.py
- [[metricas()]] - code - backend/torre/pronostico/modelos.py
- [[modelos.py]] - code - backend/torre/pronostico/modelos.py
- [[ndarray]] - code
- [[ndarray_1]] - code
- [[origen_movil()]] - code - backend/torre/pronostico/modelos.py
- [[primer_origen()]] - code - backend/torre/pronostico/modelos.py
- [[pronostico__init__.py]] - code - backend/torre/pronostico/__init__.py
- [[pronostico_final()]] - code - backend/torre/pronostico/seleccion.py
- [[razones()]] - code - backend/torre/pronostico/forma.py
- [[regresion_con_clima()]] - code - backend/torre/pronostico/modelos.py
- [[segunda_opinion_stl()]] - code - backend/torre/pronostico/forma.py
- [[seleccion.py]] - code - backend/torre/pronostico/seleccion.py
- [[tramo_actual()]] - code - backend/torre/pronostico/modelos.py
- [[tramo_continuo()]] - code - backend/torre/pronostico/forma.py
- [[tramo_horizonte()]] - code - backend/torre/pronostico/intervalos.py
- [[Índices de la forma del año usando SOLO años completos que terminaron antes del…]] - rationale - backend/torre/pronostico/modelos.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pronóstico_forma_del_año_y_modelos
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_ECUACIONES.md — Ecuaciones y cómo lo resolví]]
- 5 edges to [[_COMMUNITY_Pronóstico tormentas y escenarios]]
- 4 edges to [[_COMMUNITY_pandas]]
- 4 edges to [[_COMMUNITY_test_radar_panel.py]]
- 4 edges to [[_COMMUNITY_pathlib (pathlib)]]
- 2 edges to [[_COMMUNITY_Pronóstico series a pronosticar]]
- 2 edges to [[_COMMUNITY_prediccion.py]]
- 2 edges to [[_COMMUNITY_Silver Fase 5 huracanes (HURDAT2)]]
- 2 edges to [[_COMMUNITY_test_radar_prediccion.py]]
- 1 edge to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan]]
- 1 edge to [[_COMMUNITY_silver_clima.py (silver_fred.py)]]
- 1 edge to [[_COMMUNITY_Selección de regiones con visitantes INAH (Monte Carlo escenarios )]]

## Top bridge nodes
- [[modelos.py]] - degree 28, connects to 6 communities
- [[forma.py]] - degree 15, connects to 5 communities
- [[intervalos.py]] - degree 11, connects to 4 communities
- [[seleccion.py]] - degree 12, connects to 3 communities
- [[Backtesting con origen móvil]] - degree 9, connects to 3 communities