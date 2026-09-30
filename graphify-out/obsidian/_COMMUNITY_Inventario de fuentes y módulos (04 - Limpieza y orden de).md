---
type: community
members: 7
---

# Inventario de fuentes y módulos (04 - Limpieza y orden de)

**Members:** 7 nodes

## Members
- [[Bandera de comparabilidad (notas al pie DataTur)]] - concept - docs/decisiones/04-silver.md
- [[Corrección de conteo DENUE 6,138,075 e ITER 2,243]] - rationale - docs/decisiones/03-ingesta.md
- [[D2D2m DataTur ocupacion hotelera semanal y mensual]] - concept - docs/datos/INVENTARIO.md
- [[DENUE procesado completo (6,138,075 negocios)]] - rationale - docs/decisiones/04-silver.md
- [[DataTur una version por periodo (gana la mas reciente)]] - rationale - docs/decisiones/04-silver.md
- [[Fuentes que no coinciden Isla Mujeres (prensa vs DataTur)]] - rationale - docs/decisiones/04-silver.md
- [[Incidente crítico Big Data (baja latencia)]] - concept - OBJETIVO.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Inventario_de_fuentes_y_módulos_04_-_Limpieza_y_orden_de
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_SITUR-Q y reglas de datos]]
- 2 edges to [[_COMMUNITY_Fuentes del Radar (DENUE, Censo)]]
- 1 edge to [[_COMMUNITY_Ingesta de fuentes abiertas]]
- 1 edge to [[_COMMUNITY_Las 5 regiones de la campaña]]
- 1 edge to [[_COMMUNITY_Inventario de fuentes y módulos]]
- 1 edge to [[_COMMUNITY_Plan v3 y módulos A1 A3 A5 (Alternativa elegida fus)]]

## Top bridge nodes
- [[D2D2m DataTur ocupacion hotelera semanal y mensual]] - degree 7, connects to 4 communities
- [[Fuentes que no coinciden Isla Mujeres (prensa vs DataTur)]] - degree 5, connects to 2 communities
- [[DENUE procesado completo (6,138,075 negocios)]] - degree 4, connects to 2 communities
- [[Bandera de comparabilidad (notas al pie DataTur)]] - degree 3, connects to 1 community
- [[Corrección de conteo DENUE 6,138,075 e ITER 2,243]] - degree 2, connects to 1 community