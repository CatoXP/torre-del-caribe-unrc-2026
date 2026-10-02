---
type: community
members: 12
---

# D6 DENUE INEGI (32 estados)

**Members:** 12 nodes

## Members
- [[04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]] - document - docs/decisiones/04-silver.md
- [[Bandera de comparabilidad (notas al pie DataTur)]] - concept - docs/decisiones/04-silver.md
- [[D2D2m DataTur ocupacion hotelera semanal y mensual]] - concept - docs/datos/INVENTARIO.md
- [[D6 DENUE INEGI (32 estados)]] - concept - docs/datos/INVENTARIO.md
- [[DataTur una version por periodo (gana la mas reciente)]] - rationale - docs/decisiones/04-silver.md
- [[Fuentes que no coinciden Isla Mujeres (prensa vs DataTur)]] - rationale - docs/decisiones/04-silver.md
- [[Municipio Othón P. Blanco]] - concept - docs/regiones/REGIONES.md
- [[Oferta turística (SCIAN 721, 722, 5615, 487, 712, 713)]] - rationale - docs/decisiones/04-silver.md
- [[Oferta turística = giros SCIAN característicos (721, 722, 5615, 487, 712, 713)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Privacidad se descartan raz_social, telefono y correoelec]] - rationale - docs/decisiones/04-silver.md
- [[Regla 6 Silver mes aereo con todos los aeropuertos en 0 = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Revisión con datos oficiales Isla Mujeres (DataTur 74.7 % feb  43.2 % abr 2026)]] - concept - docs/regiones/REGIONES.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/D6_DENUE_INEGI_32_estados
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_D1 SITUR-Q API (45 indicadores)]]
- 3 edges to [[_COMMUNITY_D6 DENUE INEGI (32 estados) (Índice de Presión Turíst)]]
- 3 edges to [[_COMMUNITY_requirements.txt]]
- 3 edges to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]
- 2 edges to [[_COMMUNITY_Parte G — Foco en 5 regiones]]
- 2 edges to [[_COMMUNITY_Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)]]
- 2 edges to [[_COMMUNITY_03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]]
- 2 edges to [[_COMMUNITY_Decisión la campaña promueve 5 regiones de Quintana Roo]]
- 1 edge to [[_COMMUNITY_Índice de Presión Turística (IPT)]]
- 1 edge to [[_COMMUNITY_entorno.py]]
- 1 edge to [[_COMMUNITY_test_silver.py]]
- 1 edge to [[_COMMUNITY_entorno.py (silver_siturq.py)]]
- 1 edge to [[_COMMUNITY_silver_datatur_ocupacion.py]]
- 1 edge to [[_COMMUNITY_entorno.py (silver_denue.py)]]
- 1 edge to [[_COMMUNITY_Hoja de ruta del proyecto]]

## Top bridge nodes
- [[04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]] - degree 23, connects to 14 communities
- [[D6 DENUE INEGI (32 estados)]] - degree 9, connects to 7 communities
- [[D2D2m DataTur ocupacion hotelera semanal y mensual]] - degree 7, connects to 2 communities
- [[Fuentes que no coinciden Isla Mujeres (prensa vs DataTur)]] - degree 5, connects to 2 communities
- [[Regla 6 Silver mes aereo con todos los aeropuertos en 0 = hueco]] - degree 4, connects to 2 communities