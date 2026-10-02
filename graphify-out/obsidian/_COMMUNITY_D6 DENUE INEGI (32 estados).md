---
type: community
members: 10
---

# D6 DENUE INEGI (32 estados)

**Members:** 10 nodes

## Members
- [[A1 Radar]] - concept - docs/datos/INVENTARIO.md
- [[A1 Radar (donde hay presion y espacio, hoy)]] - concept - CLAUDE.md
- [[Correccion de conteo (_filas_csv_en_zip excluye diccionario y catalogos)]] - rationale - docs/decisiones/03-ingesta.md
- [[D6 DENUE INEGI (32 estados)]] - concept - docs/datos/INVENTARIO.md
- [[D7 Censo 2020 ITER Q. Roo]] - concept - docs/datos/INVENTARIO.md
- [[Municipio Othón P. Blanco]] - concept - docs/regiones/REGIONES.md
- [[Oferta turística (SCIAN 721, 722, 5615, 487, 712, 713)]] - rationale - docs/decisiones/04-silver.md
- [[Oferta turística = giros SCIAN característicos (721, 722, 5615, 487, 712, 713)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Privacidad se descartan raz_social, telefono y correoelec]] - rationale - docs/decisiones/04-silver.md
- [[Índice de Presión Turística]] - concept - docs/decisiones/04-silver.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/D6_DENUE_INEGI_32_estados
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]]
- 3 edges to [[_COMMUNITY_CLAUDE.md - Reglas del repositorio Torre del Caribe]]
- 2 edges to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]
- 2 edges to [[_COMMUNITY_Radar panel y estados (docs)]]
- 1 edge to [[_COMMUNITY_Selección de regiones con visitantes INAH]]
- 1 edge to [[_COMMUNITY_Decisión la campaña promueve 5 regiones de Quintana Roo]]
- 1 edge to [[_COMMUNITY_D6 DENUE INEGI (32 estados) (Incidente Big Data cuan)]]
- 1 edge to [[_COMMUNITY_Pronóstico (A3, Fase 5) visitantes 1-12 meses (Fusión A1 Radar + A3 Pro)]]
- 1 edge to [[_COMMUNITY_03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]]

## Top bridge nodes
- [[D6 DENUE INEGI (32 estados)]] - degree 9, connects to 4 communities
- [[A1 Radar (donde hay presion y espacio, hoy)]] - degree 8, connects to 3 communities
- [[D7 Censo 2020 ITER Q. Roo]] - degree 5, connects to 3 communities
- [[Correccion de conteo (_filas_csv_en_zip excluye diccionario y catalogos)]] - degree 4, connects to 2 communities
- [[Índice de Presión Turística]] - degree 5, connects to 1 community