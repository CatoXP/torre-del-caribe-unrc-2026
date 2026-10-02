---
type: community
members: 12
---

# silver_clima.py (silver_fred.py)

**Members:** 12 nodes

## Members
- [[DataFrame_17]] - code
- [[FRED (tipo de cambio)]] - concept - docs/metodologia/ECUACIONES.md
- [[FRED CPIAUCSL (inflación de EE. UU.)]] - concept - docs/decisiones/10-silver-fase5.md
- [[FRED DEXMXUS (tipo de cambio diario peso-dólar)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Sensibilidad a lluvia y tipo de cambio]] - concept - docs/metodologia/ECUACIONES.md
- [[Tipo de cambio mensual (solo días observados)]] - concept - docs/metodologia/ECUACIONES.md
- [[_serie()]] - code - backend/torre/base/silver_fred.py
- [[construir_silver_fred()]] - code - backend/torre/base/silver_fred.py
- [[mensual()]] - code - backend/torre/base/silver_fred.py
- [[mes_incompleto_flag (mes en curso)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[silver_fred.py]] - code - backend/torre/base/silver_fred.py
- [[tipo_cambio_diario()]] - code - backend/torre/base/silver_fred.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/silver_climapy_silver_fredpy
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Pronóstico tormentas y escenarios]]
- 1 edge to [[_COMMUNITY_Pronóstico forma del año y modelos]]
- 1 edge to [[_COMMUNITY_entorno.py]]
- 1 edge to [[_COMMUNITY_test_radar_panel.py]]
- 1 edge to [[_COMMUNITY_Selección de regiones con visitantes INAH]]

## Top bridge nodes
- [[silver_fred.py]] - degree 8, connects to 2 communities
- [[Sensibilidad a lluvia y tipo de cambio]] - degree 3, connects to 2 communities
- [[FRED DEXMXUS (tipo de cambio diario peso-dólar)]] - degree 4, connects to 1 community