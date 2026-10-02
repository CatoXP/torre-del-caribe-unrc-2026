---
type: community
members: 12
---

# silver_clima.py

**Members:** 12 nodes

## Members
- [[Clima Open-Meteo ERA5 (clima_diario y clima_horario)]] - concept - docs/decisiones/10-silver-fase5.md
- [[DataFrame_16]] - code
- [[Hallazgo la temporada de lluvias coincide con la de huracanes (ago–oct)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Hora local de Quintana Roo (UTC−5 fijo desde 2015)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Hueco sin punto de clima para Laguna Milagros–Xul-Ha ni Calderitas (se usa Chetumal)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[Une todos los archivos de un tipo ('diario' u 'horario') de la descarga más…]] - rationale - backend/torre/base/silver_clima.py
- [[_leer()]] - code - backend/torre/base/silver_clima.py
- [[_papel()]] - code - backend/torre/base/silver_clima.py
- [[clima_diario()]] - code - backend/torre/base/silver_clima.py
- [[clima_horario()]] - code - backend/torre/base/silver_clima.py
- [[construir_silver_clima()]] - code - backend/torre/base/silver_clima.py
- [[silver_clima.py]] - code - backend/torre/base/silver_clima.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/silver_climapy
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_entorno.py]]
- 1 edge to [[_COMMUNITY_ingesta_siturq.py]]
- 1 edge to [[_COMMUNITY_test_radar_panel.py]]
- 1 edge to [[_COMMUNITY_Selección de regiones con visitantes INAH]]
- 1 edge to [[_COMMUNITY_Silver Fase 5 huracanes (HURDAT2)]]

## Top bridge nodes
- [[silver_clima.py]] - degree 9, connects to 3 communities
- [[Clima Open-Meteo ERA5 (clima_diario y clima_horario)]] - degree 5, connects to 1 community
- [[Hallazgo la temporada de lluvias coincide con la de huracanes (ago–oct)]] - degree 2, connects to 1 community