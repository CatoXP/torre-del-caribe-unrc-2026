---
type: community
members: 23
---

# Pronóstico: rango del 90 % (conformal)

**Members:** 23 nodes

## Members
- [[12 meses después del último mes publicado de cada serie, con el modelo elegido…]] - rationale - backend/torre/pronostico/seleccion.py
- [[Clima diario 1950-2026 y horario 2019-2026 (8 puntos)]] - concept - README.md
- [[Cuantil ⌈(n+1)·nivel⌉n de los errores de calibración (el más chico que…]] - rationale - backend/torre/pronostico/intervalos.py
- [[DataFrame_5]] - code
- [[DataFrame_6]] - code
- [[Por serie y modelo cuántos pronósticos tienen rango, qué % cayó dentro y qué…]] - rationale - backend/torre/pronostico/intervalos.py
- [[Por serie menor MAE entre los modelos con cobertura ≥ 80 %. Devuelve la tabla…]] - rationale - backend/torre/pronostico/seleccion.py
- [[Regresion con clima (modelo elegido para Bahia, Ruta y Belice)]] - concept - OBJETIVO.md
- [[Series_1]] - code
- [[agregar_intervalos()]] - code - backend/torre/pronostico/intervalos.py
- [[cobertura()]] - code - backend/torre/pronostico/intervalos.py
- [[correr()]] - code - backend/torre/pronostico/intervalos.py
- [[correr()_1]] - code - backend/torre/pronostico/seleccion.py
- [[cuantil_conformal()]] - code - backend/torre/pronostico/intervalos.py
- [[datosgoldpronostico_mes.parquet]] - document - docs/decisiones/11-pronostico.md
- [[elegir()]] - code - backend/torre/pronostico/seleccion.py
- [[intervalos.py]] - code - backend/torre/pronostico/intervalos.py
- [[math]] - concept
- [[ndarray]] - code
- [[pronostico__init__.py]] - code - backend/torre/pronostico/__init__.py
- [[pronostico_final()]] - code - backend/torre/pronostico/seleccion.py
- [[seleccion.py]] - code - backend/torre/pronostico/seleccion.py
- [[tramo_horizonte()]] - code - backend/torre/pronostico/intervalos.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pronóstico_rango_del_90__conformal
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Decisión 11 decisiones del Pronóstico]]
- 2 edges to [[_COMMUNITY_clustering.py]]
- 2 edges to [[_COMMUNITY_criterios.py]]
- 2 edges to [[_COMMUNITY_entrega.py]]
- 2 edges to [[_COMMUNITY_pdf.py]]
- 2 edges to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]
- 1 edge to [[_COMMUNITY_Pronóstico tormentas y escenarios]]
- 1 edge to [[_COMMUNITY_Pronóstico 5 modelos (origen móvil)]]
- 1 edge to [[_COMMUNITY_Silver Fase 5 huracanes (HURDAT2)]]
- 1 edge to [[_COMMUNITY_Estado de las fases (28-sep-2026)]]

## Top bridge nodes
- [[seleccion.py]] - degree 13, connects to 5 communities
- [[intervalos.py]] - degree 12, connects to 5 communities
- [[cuantil_conformal()]] - degree 7, connects to 1 community
- [[elegir()]] - degree 5, connects to 1 community
- [[Regresion con clima (modelo elegido para Bahia, Ruta y Belice)]] - degree 3, connects to 1 community