---
type: community
members: 23
---

# Ingesta SITUR-Q

**Members:** 23 nodes

## Members
- [[03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]] - document - docs/decisiones/03-ingesta.md
- [[Agrega (o actualiza) la fila de un archivo en el manifiesto y la devuelve. -…]] - rationale - backend/torre/base/manifiesto.py
- [[Descarga todos los INDICADORES × unidades × años y guarda un archivo JSON crudo…]] - rationale - backend/torre/base/ingesta_siturq.py
- [[Evidencia de sargazo en la Bahia de Chetumal (ECOSUR, Reportur)]] - concept - docs/decisiones/03-ingesta.md
- [[Extraccion con Playwright + Chromium (benchmarks y sargazo)]] - concept - docs/decisiones/03-ingesta.md
- [[Fase 1 353 archivos, 8,134,802 registros, 824 MB]] - concept - docs/decisiones/03-ingesta.md
- [[Huella SHA-256 del archivo, leída en bloques de 1 MB para no cargar archivos…]] - rationale - backend/torre/base/manifiesto.py
- [[Lee la página pública y extrae el token, los destinos y las zonas tal como los…]] - rationale - backend/torre/base/ingesta_siturq.py
- [[Path_2]] - code
- [[Pide a la API un indicador para una unidad (destino o zona) y un año completo…]] - rationale - backend/torre/base/ingesta_siturq.py
- [[Visita cada fuente, guarda HTML + captura + párrafos relevantes y devuelve esos…]] - rationale - backend/torre/base/evidencia_sargazo.py
- [[capturar_evidencia()]] - code - backend/torre/base/evidencia_sargazo.py
- [[consultar()]] - code - backend/torre/base/ingesta_siturq.py
- [[datetime]] - concept
- [[descargar_siturq()]] - code - backend/torre/base/ingesta_siturq.py
- [[evidencia_sargazo.py]] - code - backend/torre/base/evidencia_sargazo.py
- [[html]] - concept
- [[ingesta_siturq.py]] - code - backend/torre/base/ingesta_siturq.py
- [[leer_catalogo()]] - code - backend/torre/base/ingesta_siturq.py
- [[manifiesto.py]] - code - backend/torre/base/manifiesto.py
- [[registrar()]] - code - backend/torre/base/manifiesto.py
- [[sha256_de()]] - code - backend/torre/base/manifiesto.py
- [[time]] - concept

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Ingesta_SITUR-Q
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Ingesta de benchmarks y PDF]]
- 6 edges to [[_COMMUNITY_Ingesta y Silver DataTur]]
- 4 edges to [[_COMMUNITY_Ingesta de fuentes abiertas]]
- 3 edges to [[_COMMUNITY_SITUR-Q y reglas de datos]]
- 2 edges to [[_COMMUNITY_Plan v3 y módulos A1 A3 A5]]
- 2 edges to [[_COMMUNITY_Silver SITUR-Q y DENUE]]
- 2 edges to [[_COMMUNITY_Fotos de Wikimedia y pruebas de la página]]
- 2 edges to [[_COMMUNITY_Silver ocupación DataTur y Spark (pathlib)]]
- 2 edges to [[_COMMUNITY_Las 5 regiones de la campaña]]
- 2 edges to [[_COMMUNITY_Inventario de fuentes y módulos]]
- 2 edges to [[_COMMUNITY_Reglas del repositorio (CLAUDE.md)]]
- 1 edge to [[_COMMUNITY_Pruebas de ingesta]]
- 1 edge to [[_COMMUNITY_Datos de la página web]]
- 1 edge to [[_COMMUNITY_Silver ocupación DataTur y Spark]]
- 1 edge to [[_COMMUNITY_Plan v3 y módulos A1 A3 A5 (Alternativa elegida fus)]]
- 1 edge to [[_COMMUNITY_Página módulos, fases y chat]]

## Top bridge nodes
- [[03 - Ingesta de fuentes oficiales (Fase 1 Bronze)]] - degree 19, connects to 10 communities
- [[ingesta_siturq.py]] - degree 14, connects to 5 communities
- [[manifiesto.py]] - degree 12, connects to 5 communities
- [[datetime]] - degree 8, connects to 5 communities
- [[Evidencia de sargazo en la Bahia de Chetumal (ECOSUR, Reportur)]] - degree 5, connects to 3 communities