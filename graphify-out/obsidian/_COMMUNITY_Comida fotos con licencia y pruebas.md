---
type: community
members: 20
---

# Comida: fotos con licencia y pruebas

**Members:** 20 nodes

## Members
- [[Fotos de Wikimedia Commons con licencia libre y crédito]] - rationale - docs/decisiones/13-comida.md
- [[GET con reintentos Commons limita las consultas seguidas.]] - rationale - backend/torre/campana/fotos_comida.py
- [[Regla de oro 4 sin scraping prohibido]] - rationale - docs/decisiones/13-comida.md
- [[Response]] - code
- [[_limpiar()]] - code - backend/torre/campana/fotos_comida.py
- [[_pedir()]] - code - backend/torre/campana/fotos_comida.py
- [[creditos()]] - code - tests/test_fotos_comida.py
- [[creditos.json (fotos de comida)]] - document - docs/decisiones/13-comida.md
- [[descargar()]] - code - backend/torre/campana/fotos_comida.py
- [[fixture_1]] - code
- [[fotos_comida.py]] - code - backend/torre/campana/fotos_comida.py
- [[hashlib]] - concept
- [[pil]] - concept
- [[requests]] - concept
- [[test_archivos_intactos()]] - code - tests/test_fotos_comida.py
- [[test_fotos_comida.py]] - code - tests/test_fotos_comida.py
- [[test_grupos_validos()]] - code - tests/test_fotos_comida.py
- [[test_licencia_libre_y_credito_completo()]] - code - tests/test_fotos_comida.py
- [[test_ningun_lugar_excluido()]] - code - tests/test_fotos_comida.py
- [[test_veinticuatro_platillos()]] - code - tests/test_fotos_comida.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Comida_fotos_con_licencia_y_pruebas
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Ingesta DataTur y costos publicitarios]]
- 4 edges to [[_COMMUNITY_ingesta_siturq.py]]
- 3 edges to [[_COMMUNITY_ingesta_fotos.py]]
- 2 edges to [[_COMMUNITY_sys]]
- 1 edge to [[_COMMUNITY_ingesta_abiertas.py]]
- 1 edge to [[_COMMUNITY_silver_datatur_ocupacion.py]]
- 1 edge to [[_COMMUNITY_entorno.py]]
- 1 edge to [[_COMMUNITY_PLAN_v3.md (plan aprobado)]]
- 1 edge to [[_COMMUNITY_sys (sys)]]
- 1 edge to [[_COMMUNITY_pathlib (pathlib)]]
- 1 edge to [[_COMMUNITY_Hoja de ruta del proyecto]]

## Top bridge nodes
- [[test_fotos_comida.py]] - degree 16, connects to 6 communities
- [[fotos_comida.py]] - degree 15, connects to 5 communities
- [[requests]] - degree 5, connects to 4 communities
- [[hashlib]] - degree 4, connects to 2 communities
- [[Response]] - degree 2, connects to 1 community