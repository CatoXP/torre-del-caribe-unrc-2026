---
type: community
members: 29
---

# silver_clima.py

**Members:** 29 nodes

## Members
- [[Clima Open-Meteo ERA5 (clima_diario y clima_horario)]] - concept - docs/decisiones/10-silver-fase5.md
- [[DataFrame_26]] - code
- [[DataFrame_27]] - code
- [[Definición tormenta que afecta al sur (≤200 km de Chetumal, ≥34 kt, desde 1966)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[FRED CPIAUCSL (inflación de EE. UU.)]] - concept - docs/decisiones/10-silver-fase5.md
- [[FRED DEXMXUS (tipo de cambio diario peso-dólar)]] - concept - docs/decisiones/10-silver-fase5.md
- [[FRED tipo de cambio peso-dólar]] - concept - docs/metodologia/ECUACIONES.md
- [[HURDAT2 (trayectorias de huracanes, 1851–2025)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Hallazgo la temporada de lluvias coincide con la de huracanes (ago–oct)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Hora local de Quintana Roo (UTC−5 fijo desde 2015)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Hora local de Quintana Roo (UTC−5 fijo)]] - concept - docs/metodologia/ECUACIONES.md
- [[Hueco sin punto de clima para Laguna Milagros–Xul-Ha ni Calderitas (se usa Chetumal)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[Sensibilidad a lluvia y tipo de cambio]] - concept - docs/metodologia/ECUACIONES.md
- [[Tipo de cambio mensual (solo días observados)]] - concept - docs/metodologia/ECUACIONES.md
- [[Une todos los archivos de un tipo ('diario' u 'horario') de la descarga más…]] - rationale - backend/torre/base/silver_clima.py
- [[_leer()]] - code - backend/torre/base/silver_clima.py
- [[_papel()]] - code - backend/torre/base/silver_clima.py
- [[_serie()]] - code - backend/torre/base/silver_fred.py
- [[clima_diario()]] - code - backend/torre/base/silver_clima.py
- [[clima_horario()]] - code - backend/torre/base/silver_clima.py
- [[construir_silver_clima()]] - code - backend/torre/base/silver_clima.py
- [[construir_silver_fred()]] - code - backend/torre/base/silver_fred.py
- [[formato_irregular_flag (2 líneas mal escritas de HURDAT2)]] - rationale - docs/decisiones/10-silver-fase5.md
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
- 2 edges to [[_COMMUNITY_entorno.py]]
- 2 edges to [[_COMMUNITY_numpy]]
- 1 edge to [[_COMMUNITY_10 — Datos limpios para el Pronóstico huracanes, clima y tipo de cambio (Fase 2, cierre de la parte que usa la Fase 5)]]
- 1 edge to [[_COMMUNITY_ECUACIONES.md — Ecuaciones y cómo lo resolví]]
- 1 edge to [[_COMMUNITY_test_silver_fase5.py]]
- 1 edge to [[_COMMUNITY_escenarios.py]]
- 1 edge to [[_COMMUNITY_ingesta_datatur.py (ingesta_siturq.py)]]

## Top bridge nodes
- [[silver_clima.py]] - degree 10, connects to 3 communities
- [[silver_fred.py]] - degree 9, connects to 2 communities
- [[Sensibilidad a lluvia y tipo de cambio]] - degree 3, connects to 2 communities
- [[HURDAT2 (trayectorias de huracanes, 1851–2025)]] - degree 3, connects to 1 community
- [[Definición tormenta que afecta al sur (≤200 km de Chetumal, ≥34 kt, desde 1966)]] - degree 3, connects to 1 community