---
type: community
members: 25
---

# entorno.py

**Members:** 25 nodes

## Members
- [[Capacidad probada sin usar (K_s = 1 − V2025V2019)]] - concept - docs/metodologia/ECUACIONES.md
- [[Clima Open-Meteo ERA5 (clima_diario y clima_horario)]] - concept - docs/decisiones/10-silver-fase5.md
- [[DataFrame_4]] - code
- [[DataFrame_5]] - code
- [[FRED CPIAUCSL (inflación de EE. UU.)]] - concept - docs/decisiones/10-silver-fase5.md
- [[FRED DEXMXUS (tipo de cambio diario peso-dólar)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Hora local de Quintana Roo (UTC−5 fijo desde 2015)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Hueco sin punto de clima para Laguna Milagros–Xul-Ha ni Calderitas (se usa Chetumal)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[Regresión con clima]] - concept - docs/decisiones/11-pronostico.md
- [[Supuesto sitio cerrado no es 'sin demanda']] - rationale - docs/metodologia/ECUACIONES.md
- [[Tipo de cambio mensual (promedio de días observados)]] - concept - docs/metodologia/ECUACIONES.md
- [[Une todos los archivos de un tipo ('diario' u 'horario') de la descarga más…]] - rationale - backend/torre/base/silver_clima.py
- [[_leer()]] - code - backend/torre/base/silver_clima.py
- [[_papel()]] - code - backend/torre/base/silver_clima.py
- [[_serie()]] - code - backend/torre/base/silver_fred.py
- [[clima_diario()]] - code - backend/torre/base/silver_clima.py
- [[clima_horario()]] - code - backend/torre/base/silver_clima.py
- [[construir_silver_clima()]] - code - backend/torre/base/silver_clima.py
- [[construir_silver_fred()]] - code - backend/torre/base/silver_fred.py
- [[mensual()]] - code - backend/torre/base/silver_fred.py
- [[mes_incompleto_flag (mes en curso)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[silver_clima.py]] - code - backend/torre/base/silver_clima.py
- [[silver_fred.py]] - code - backend/torre/base/silver_fred.py
- [[sin_dato_flag (huecos conservados vacíos)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[tipo_cambio_diario()]] - code - backend/torre/base/silver_fred.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/entornopy
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Fotos y ubicación comprobada]]
- 2 edges to [[_COMMUNITY_Entorno Spark, JDK y prueba de humo]]
- 1 edge to [[_COMMUNITY_prediccion.py]]
- 1 edge to [[_COMMUNITY_test_silver_fase5.py]]
- 1 edge to [[_COMMUNITY_Pronóstico series a pronosticar]]

## Top bridge nodes
- [[silver_clima.py]] - degree 9, connects to 2 communities
- [[silver_fred.py]] - degree 8, connects to 2 communities
- [[Clima Open-Meteo ERA5 (clima_diario y clima_horario)]] - degree 6, connects to 1 community
- [[FRED DEXMXUS (tipo de cambio diario peso-dólar)]] - degree 5, connects to 1 community
- [[Supuesto sitio cerrado no es 'sin demanda']] - degree 3, connects to 1 community