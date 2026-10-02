---
type: community
members: 11
---

# 03 - Ingesta de fuentes oficiales (Fase 1: Bronze)

**Members:** 11 nodes

## Members
- [[03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]] - document - docs/decisiones/03-ingesta.md
- [[Correccion de conteo (_filas_csv_en_zip excluye diccionario y catalogos)]] - rationale - docs/decisiones/03-ingesta.md
- [[D13 Benchmarks de costo por canal (WordStream  LocaliQ)]] - concept - docs/plan/PLAN_v3.md
- [[D7 Censo 2020 ITER Q. Roo]] - concept - docs/datos/INVENTARIO.md
- [[Evidencia de sargazo en la Bahia de Chetumal (ECOSUR, Reportur)]] - concept - docs/decisiones/03-ingesta.md
- [[Extraccion con Playwright + Chromium (benchmarks y sargazo)]] - concept - docs/decisiones/03-ingesta.md
- [[Fase 1 353 archivos, 8,134,802 registros, 824 MB]] - concept - docs/decisiones/03-ingesta.md
- [[Hueco conversión de Facebook para Travel no publicada]] - concept - docs/decisiones/03-ingesta.md
- [[Indicador SITUR-Q 'Turista - Afluencia' roto (120120 error 500)]] - concept - docs/decisiones/03-ingesta.md
- [[Manifiesto Bronze con huella SHA-256 (MANIFIESTO.csv)]] - concept - docs/decisiones/03-ingesta.md
- [[Manifiesto con huella SHA-256]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/03_-_Ingesta_de_fuentes_oficiales_Fase_1_Bronze
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_D1 SITUR-Q API (45 indicadores)]]
- 3 edges to [[_COMMUNITY_Parte G — Foco en 5 regiones]]
- 3 edges to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]
- 3 edges to [[_COMMUNITY_ingesta_datatur.py (manifiesto.py)]]
- 2 edges to [[_COMMUNITY_D6 DENUE INEGI (32 estados)]]
- 1 edge to [[_COMMUNITY_Índice de Presión Turística (IPT)]]
- 1 edge to [[_COMMUNITY_PLAN_v3.md (plan aprobado) (Lakehouse PySpark Bronze)]]
- 1 edge to [[_COMMUNITY_PLAN_v3.md (plan aprobado)]]
- 1 edge to [[_COMMUNITY_ingesta_abiertas.py]]
- 1 edge to [[_COMMUNITY_test_ingesta.py]]
- 1 edge to [[_COMMUNITY_ingesta_datatur.py]]
- 1 edge to [[_COMMUNITY_ingesta_datatur.py (ingesta_siturq.py)]]
- 1 edge to [[_COMMUNITY_Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)]]
- 1 edge to [[_COMMUNITY_Fase 1 recolección de 15 fuentes oficiales]]

## Top bridge nodes
- [[03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]] - degree 18, connects to 9 communities
- [[D7 Censo 2020 ITER Q. Roo]] - degree 5, connects to 4 communities
- [[D13 Benchmarks de costo por canal (WordStream  LocaliQ)]] - degree 5, connects to 3 communities
- [[Evidencia de sargazo en la Bahia de Chetumal (ECOSUR, Reportur)]] - degree 4, connects to 2 communities
- [[Manifiesto con huella SHA-256]] - degree 3, connects to 2 communities