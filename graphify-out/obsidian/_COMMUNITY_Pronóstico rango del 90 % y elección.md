---
type: community
members: 20
---

# Pronóstico: rango del 90 % y elección

**Members:** 20 nodes

## Members
- [[12 meses después del último mes publicado de cada serie, con el modelo elegido…]] - rationale - backend/torre/pronostico/seleccion.py
- [[Cuantil ⌈(n+1)·nivel⌉n de los errores de calibración (el más chico que…]] - rationale - backend/torre/pronostico/intervalos.py
- [[DataFrame_9]] - code
- [[DataFrame_10]] - code
- [[Por serie y modelo cuántos pronósticos tienen rango, qué % cayó dentro y qué…]] - rationale - backend/torre/pronostico/intervalos.py
- [[Por serie menor MAE entre los modelos con cobertura ≥ 80 %. Devuelve la tabla…]] - rationale - backend/torre/pronostico/seleccion.py
- [[Series_2]] - code
- [[agregar_intervalos()]] - code - backend/torre/pronostico/intervalos.py
- [[cobertura()]] - code - backend/torre/pronostico/intervalos.py
- [[correr()_1]] - code - backend/torre/pronostico/intervalos.py
- [[correr()_2]] - code - backend/torre/pronostico/seleccion.py
- [[cuantil_conformal()]] - code - backend/torre/pronostico/intervalos.py
- [[datosgoldpronostico_mes.parquet]] - document - docs/decisiones/11-pronostico.md
- [[elegir()]] - code - backend/torre/pronostico/seleccion.py
- [[intervalos.py]] - code - backend/torre/pronostico/intervalos.py
- [[math]] - concept
- [[ndarray]] - code
- [[pronostico_final()]] - code - backend/torre/pronostico/seleccion.py
- [[seleccion.py]] - code - backend/torre/pronostico/seleccion.py
- [[tramo_horizonte()]] - code - backend/torre/pronostico/intervalos.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pronóstico_rango_del_90__y_elección
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_ECUACIONES]]
- 2 edges to [[_COMMUNITY_numpy]]
- 2 edges to [[_COMMUNITY_test_planteamiento.py]]
- 2 edges to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_Silver FRED y series a pronosticar]]
- 1 edge to [[_COMMUNITY_Pronóstico tormentas y escenarios]]
- 1 edge to [[_COMMUNITY_Pronóstico forma del año y modelos]]
- 1 edge to [[_COMMUNITY_Silver Fase 5 huracanes (HURDAT2)]]
- 1 edge to [[_COMMUNITY_Planeador NLP de negocios (DENUE)]]

## Top bridge nodes
- [[seleccion.py]] - degree 11, connects to 5 communities
- [[intervalos.py]] - degree 10, connects to 3 communities
- [[math]] - degree 3, connects to 2 communities
- [[cuantil_conformal()]] - degree 7, connects to 1 community
- [[elegir()]] - degree 5, connects to 1 community