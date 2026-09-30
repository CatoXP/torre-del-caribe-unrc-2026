---
type: community
members: 11
---

# Fuentes del Radar (DENUE, Censo)

**Members:** 11 nodes

## Members
- [[A1 Radar]] - concept - docs/datos/INVENTARIO.md
- [[A1 Radar (donde hay presion y espacio, hoy)]] - concept - CLAUDE.md
- [[D6 DENUE INEGI (32 estados)]] - concept - docs/datos/INVENTARIO.md
- [[D7 Censo 2020 ITER Q. Roo]] - concept - docs/datos/INVENTARIO.md
- [[Municipio Othón P. Blanco]] - concept - docs/regiones/REGIONES.md
- [[Oferta turística (SCIAN 721, 722, 5615, 487, 712, 713)]] - rationale - docs/decisiones/04-silver.md
- [[Oferta turística = giros SCIAN característicos (721, 722, 5615, 487, 712, 713)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Presión de llegada medida (cruceristas + Tren Maya + cruces de Belice por habitación y por residente)]] - rationale - docs/datos/INVENTARIO.md
- [[Privacidad se descartan raz_social, telefono y correoelec]] - rationale - docs/decisiones/04-silver.md
- [[Regla de oro estimado != medido (sufijo _est)]] - rationale - CLAUDE.md
- [[Índice de Presión Turística]] - concept - docs/decisiones/04-silver.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Fuentes_del_Radar_DENUE_Censo
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_SITUR-Q y reglas de datos]]
- 4 edges to [[_COMMUNITY_Reglas del repositorio (CLAUDE.md)]]
- 3 edges to [[_COMMUNITY_Inventario de fuentes y módulos]]
- 2 edges to [[_COMMUNITY_Las 5 regiones de la campaña]]
- 2 edges to [[_COMMUNITY_Inventario de fuentes y módulos (04 - Limpieza y orden de)]]
- 2 edges to [[_COMMUNITY_Radar índice y quiebre de 2025]]
- 1 edge to [[_COMMUNITY_Plan v3 y módulos A1 A3 A5 (Alternativa elegida fus)]]

## Top bridge nodes
- [[D6 DENUE INEGI (32 estados)]] - degree 9, connects to 5 communities
- [[A1 Radar (donde hay presion y espacio, hoy)]] - degree 8, connects to 4 communities
- [[D7 Censo 2020 ITER Q. Roo]] - degree 5, connects to 4 communities
- [[Presión de llegada medida (cruceristas + Tren Maya + cruces de Belice por habitación y por residente)]] - degree 4, connects to 2 communities
- [[Índice de Presión Turística]] - degree 5, connects to 1 community