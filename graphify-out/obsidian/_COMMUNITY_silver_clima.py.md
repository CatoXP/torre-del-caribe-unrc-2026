---
type: community
members: 23
---

# silver_clima.py

**Members:** 23 nodes

## Members
- [[Clima Open-Meteo ERA5 (clima_diario y clima_horario)]] - concept - docs/decisiones/10-silver-fase5.md
- [[DataFrame_2]] - code
- [[DataFrame_3]] - code
- [[FRED CPIAUCSL (inflación de EE. UU.)]] - concept - docs/decisiones/10-silver-fase5.md
- [[FRED DEXMXUS (tipo de cambio diario peso-dólar)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Hora local de Quintana Roo (UTC−5 fijo desde 2015)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Hora local de Quintana Roo (UTC−5 fijo)]] - concept - docs/metodologia/ECUACIONES.md
- [[Hueco sin punto de clima para Laguna Milagros–Xul-Ha ni Calderitas (se usa Chetumal)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[Supuesto sitio cerrado no es 'sin demanda']] - rationale - docs/metodologia/ECUACIONES.md
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
TABLE source_file, type FROM #community/silver_climapy
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Regresión logística multiclase (modelo elegido del Radar)]]
- 2 edges to [[_COMMUNITY_entorno.py]]
- 2 edges to [[_COMMUNITY_criterios.py]]
- 2 edges to [[_COMMUNITY_pdf.py]]
- 2 edges to [[_COMMUNITY_Decisión 11 decisiones del Pronóstico]]
- 1 edge to [[_COMMUNITY_Ingesta SITUR-Q y costos publicitarios]]
- 1 edge to [[_COMMUNITY_Silver Fase 5 huracanes (HURDAT2)]]
- 1 edge to [[_COMMUNITY_Pronóstico tormentas y escenarios]]
- 1 edge to [[_COMMUNITY_Pronóstico series a pronosticar]]

## Top bridge nodes
- [[silver_clima.py]] - degree 11, connects to 4 communities
- [[silver_fred.py]] - degree 9, connects to 3 communities
- [[Supuesto sitio cerrado no es 'sin demanda']] - degree 4, connects to 3 communities
- [[Clima Open-Meteo ERA5 (clima_diario y clima_horario)]] - degree 6, connects to 2 communities
- [[FRED DEXMXUS (tipo de cambio diario peso-dólar)]] - degree 5, connects to 2 communities