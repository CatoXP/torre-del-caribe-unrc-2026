---
type: community
members: 12
---

# 04 - Limpieza y orden de los datos (Fase 2: Silver y Gold)

**Members:** 12 nodes

## Members
- [[04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]] - document - docs/decisiones/04-silver.md
- [[Bandera de comparabilidad (notas al pie DataTur)]] - concept - docs/decisiones/04-silver.md
- [[Corrección de conteo DENUE 6,138,075 e ITER 2,243]] - rationale - docs/decisiones/03-ingesta.md
- [[D2D2m DataTur ocupacion hotelera semanal y mensual]] - concept - docs/datos/INVENTARIO.md
- [[DENUE procesado completo (6,138,075 negocios)]] - rationale - docs/decisiones/04-silver.md
- [[DataTur una version por periodo (gana la mas reciente)]] - rationale - docs/decisiones/04-silver.md
- [[Fase 2 — Limpieza y orden de los datos (SilverGold)]] - concept - docs/plan/HOJA_DE_RUTA.md
- [[Fuentes que no coinciden Isla Mujeres (prensa vs DataTur)]] - rationale - docs/decisiones/04-silver.md
- [[Incidente crítico Big Data (baja latencia)]] - concept - OBJETIVO.md
- [[Regla 6 Silver mes aereo con todos los aeropuertos en 0 = hueco]] - rationale - docs/decisiones/04-silver.md
- [[Revisión con datos oficiales Isla Mujeres (DataTur 74.7 % feb  43.2 % abr 2026)]] - concept - docs/regiones/REGIONES.md
- [[pyspark==3.5.6]] - concept - requirements.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/04_-_Limpieza_y_orden_de_los_datos_Fase_2_Silver_y_Gold
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_D1 SITUR-Q API (45 indicadores)]]
- 5 edges to [[_COMMUNITY_D6 DENUE INEGI (32 estados)]]
- 3 edges to [[_COMMUNITY_Decisiones cerradas (A.8)]]
- 3 edges to [[_COMMUNITY_Fase 7 — Torre en vivo]]
- 2 edges to [[_COMMUNITY_Entorno Spark, JDK y prueba de humo]]
- 2 edges to [[_COMMUNITY_Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)]]
- 2 edges to [[_COMMUNITY_silver_datatur_ocupacion.py]]
- 2 edges to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]
- 1 edge to [[_COMMUNITY_ingesta_abiertas.py]]
- 1 edge to [[_COMMUNITY_silver_denue.py]]
- 1 edge to [[_COMMUNITY_test_silver.py]]
- 1 edge to [[_COMMUNITY_Decisión la campaña promueve 5 regiones de Quintana Roo]]
- 1 edge to [[_COMMUNITY_CLAUDE.md - Reglas del repositorio Torre del Caribe]]
- 1 edge to [[_COMMUNITY_Ingesta costos publicitarios y sargazo]]
- 1 edge to [[_COMMUNITY_Decisión 08 — A1 Radar (Fase 4)]]

## Top bridge nodes
- [[04 - Limpieza y orden de los datos (Fase 2 Silver y Gold)]] - degree 25, connects to 13 communities
- [[D2D2m DataTur ocupacion hotelera semanal y mensual]] - degree 7, connects to 3 communities
- [[Regla 6 Silver mes aereo con todos los aeropuertos en 0 = hueco]] - degree 5, connects to 2 communities
- [[pyspark==3.5.6]] - degree 4, connects to 2 communities
- [[Fuentes que no coinciden Isla Mujeres (prensa vs DataTur)]] - degree 5, connects to 1 community