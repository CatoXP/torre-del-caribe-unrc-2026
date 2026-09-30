---
type: community
members: 22
---

# Pruebas de ingesta

**Members:** 22 nodes

## Members
- [[Busca un valor dentro de las respuestas crudas de la API (unidad, año, mes,…]] - rationale - tests/test_ingesta.py
- [[Cada archivo del manifiesto existe y su SHA-256 es el registrado (nadie lo…]] - rationale - tests/test_ingesta.py
- [[HuggingFace reportó 208,051 filas para vg055Rest-Mex2025 (consulta del…]] - rationale - tests/test_ingesta.py
- [[Lee el archivo más reciente de un indicador de SITUR-Q.]] - rationale - tests/test_ingesta.py
- [[Los 32 estados están presentes (el Estado de México viene en dos partes).]] - rationale - tests/test_ingesta.py
- [[Tabla oficial de WordStream 2025, Travel CPC $2.12 y CTR 8.73 % (extraída con…]] - rationale - tests/test_ingesta.py
- [[Visitantes 2025 a la Z.A. de Tulum = 1,031,443 (cálculo del 27-sep-2026,…]] - rationale - tests/test_ingesta.py
- [[filas_manifiesto()]] - code - tests/test_ingesta.py
- [[test_benchmarks_travel_google_2025()]] - code - tests/test_ingesta.py
- [[test_denue_32_estados()]] - code - tests/test_ingesta.py
- [[test_geojson_11_municipios()]] - code - tests/test_ingesta.py
- [[test_inah_tulum_2025()]] - code - tests/test_ingesta.py
- [[test_ingesta.py]] - code - tests/test_ingesta.py
- [[test_manifiesto_huellas_coinciden()]] - code - tests/test_ingesta.py
- [[test_restmex_208051_resenas()]] - code - tests/test_ingesta.py
- [[test_siturq_bacalar_145_hoteles_ene_2025()]] - code - tests/test_ingesta.py
- [[test_siturq_bacalar_ocupacion_ene_2024()]] - code - tests/test_ingesta.py
- [[test_siturq_tiene_15_unidades_por_indicador()]] - code - tests/test_ingesta.py
- [[test_siturq_tren_maya_gran_costa_maya_ene_2025()]] - code - tests/test_ingesta.py
- [[torre_base_manifiesto]] - concept
- [[ultimo_json_siturq()]] - code - tests/test_ingesta.py
- [[valor()]] - code - tests/test_ingesta.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pruebas_de_ingesta
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Ingesta de benchmarks y PDF]]
- 1 edge to [[_COMMUNITY_Fotos de Wikimedia y pruebas de la página]]
- 1 edge to [[_COMMUNITY_Auditoría cifras de los documentos]]
- 1 edge to [[_COMMUNITY_Pruebas de criterios]]
- 1 edge to [[_COMMUNITY_Silver ocupación DataTur y Spark (pathlib)]]
- 1 edge to [[_COMMUNITY_Ingesta SITUR-Q]]

## Top bridge nodes
- [[test_ingesta.py]] - degree 20, connects to 6 communities