---
type: community
members: 13
---

# 04 - Limpieza y orden de los datos (Fase 2: Silver y Gold)

**Members:** 13 nodes

## Members
- [[A1 Radar]] - concept - docs/datos/INVENTARIO.md
- [[A1 Radar (donde hay presion y espacio, hoy)]] - concept - CLAUDE.md
- [[Clustering jerarquico de 55 centros (k = 2 por silueta)]] - concept - OBJETIVO.md
- [[Correccion de conteo (_filas_csv_en_zip excluye diccionario y catalogos)]] - rationale - docs/decisiones/03-ingesta.md
- [[Corrección de conteo DENUE 6,138,075 e ITER 2,243]] - rationale - docs/decisiones/03-ingesta.md
- [[D6 DENUE INEGI (32 estados)]] - concept - docs/datos/INVENTARIO.md
- [[D7 Censo 2020 ITER Q. Roo]] - concept - docs/datos/INVENTARIO.md
- [[DENUE procesado completo (6,138,075 negocios)]] - rationale - docs/decisiones/04-silver.md
- [[Municipio Othón P. Blanco]] - concept - docs/regiones/REGIONES.md
- [[Oferta turística (SCIAN 721, 722, 5615, 487, 712, 713)]] - rationale - docs/decisiones/04-silver.md
- [[Oferta turística = giros SCIAN característicos (721, 722, 5615, 487, 712, 713)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Privacidad se descartan raz_social, telefono y correoelec]] - rationale - docs/decisiones/04-silver.md
- [[Índice de Presión Turística]] - concept - docs/decisiones/04-silver.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/04_-_Limpieza_y_orden_de_los_datos_Fase_2_Silver_y_Gold
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Silver fuentes que no coinciden]]
- 2 edges to [[_COMMUNITY_Decisión la campaña promueve 5 regiones de Quintana Roo]]
- 2 edges to [[_COMMUNITY_Inventario de fuentes (D1–D14)]]
- 2 edges to [[_COMMUNITY_Índice de Presión Turística (IPT)]]
- 2 edges to [[_COMMUNITY_Estado de las fases (28-sep-2026)]]
- 2 edges to [[_COMMUNITY_D1 SITUR-Q API (45 indicadores)]]
- 2 edges to [[_COMMUNITY_CLAUDE.md - Reglas del repositorio Torre del Caribe]]
- 2 edges to [[_COMMUNITY_Dependencias fijadas (requirements)]]
- 1 edge to [[_COMMUNITY_ingesta_abiertas.py]]
- 1 edge to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan]]
- 1 edge to [[_COMMUNITY_clustering.py]]
- 1 edge to [[_COMMUNITY_frontendindex.html (página pública)]]
- 1 edge to [[_COMMUNITY_OBJETIVO — Torre del Caribe (ancla del proyecto)]]
- 1 edge to [[_COMMUNITY_markov.py]]
- 1 edge to [[_COMMUNITY_03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]]
- 1 edge to [[_COMMUNITY_Auditoría cifras de los documentos]]

## Top bridge nodes
- [[A1 Radar (donde hay presion y espacio, hoy)]] - degree 14, connects to 8 communities
- [[D6 DENUE INEGI (32 estados)]] - degree 9, connects to 3 communities
- [[D7 Censo 2020 ITER Q. Roo]] - degree 5, connects to 3 communities
- [[Clustering jerarquico de 55 centros (k = 2 por silueta)]] - degree 4, connects to 3 communities
- [[DENUE procesado completo (6,138,075 negocios)]] - degree 4, connects to 2 communities