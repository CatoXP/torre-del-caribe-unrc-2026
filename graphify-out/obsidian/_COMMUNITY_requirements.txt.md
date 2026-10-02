---
type: community
members: 13
---

# requirements.txt

**Members:** 13 nodes

## Members
- [[Corrección de conteo DENUE 6,138,075 e ITER 2,243]] - rationale - docs/decisiones/03-ingesta.md
- [[DENUE procesado completo (6,138,075 negocios)]] - rationale - docs/decisiones/04-silver.md
- [[Incidente Big Data cuando los datos no caben en una computadora]] - concept - OBJETIVO.md
- [[PuLP==2.9.0 (programación linealentera con CBC)]] - concept - requirements.txt
- [[duckdb==1.1.3 (consulta rápida para la API)]] - concept - requirements.txt
- [[fastapi + uvicorn (backend web)]] - concept - requirements.txt
- [[mlxtend==0.23.1 (reglas de asociación)]] - concept - requirements.txt
- [[nbformatnbclientnbconvert + mistune==3.0.2 (notebooks narrados y exportados)]] - concept - requirements.txt
- [[pyspark==3.5.6]] - concept - requirements.txt
- [[requirements.txt]] - document - requirements.txt
- [[scikit-learn==1.5.2 (clasificador, Isolation Forest, TF-IDF)]] - concept - requirements.txt
- [[scipy==1.13.1 (Poisson y estadística)]] - concept - requirements.txt
- [[statsmodels==0.14.4 (Holt-Winters, STL)]] - concept - requirements.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/requirementstxt
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_D6 DENUE INEGI (32 estados)]]
- 2 edges to [[_COMMUNITY_requirements.txt (02 — Entorno de trabajo )]]
- 1 edge to [[_COMMUNITY_ingesta_abiertas.py]]
- 1 edge to [[_COMMUNITY_Cap. 5 — Limpieza y orden de los datos (Fase 2, Silver con PySpark)]]
- 1 edge to [[_COMMUNITY_Fase 1 ingesta Bronze (353 archivos, 8,134,802]]
- 1 edge to [[_COMMUNITY_Fase 5 Pronóstico series medidas, huecos de cierrepandemia]]

## Top bridge nodes
- [[Incidente Big Data cuando los datos no caben en una computadora]] - degree 5, connects to 3 communities
- [[requirements.txt]] - degree 11, connects to 2 communities
- [[DENUE procesado completo (6,138,075 negocios)]] - degree 4, connects to 1 community
- [[pyspark==3.5.6]] - degree 3, connects to 1 community
- [[Corrección de conteo DENUE 6,138,075 e ITER 2,243]] - degree 2, connects to 1 community