---
type: community
members: 43
---

# Silver Fase 5: huracanes (HURDAT2)

**Members:** 43 nodes

## Members
- [[1. Huracanes → `datossilverhuracanes` ✅]] - document - docs/decisiones/10-silver-fase5.md
- [[10 — Datos limpios para el Pronóstico huracanes, clima y tipo de cambio (Fase 2, cierre de la parte que usa la Fase 5)]] - document - docs/decisiones/10-silver-fase5.md
- [[10-silver-fase5]] - document - docs/decisiones/10-silver-fase5.md
- [[2. Clima → `datossilverclima_diario` y `datossilverclima_horario` ✅]] - document - docs/decisiones/10-silver-fase5.md
- [[3. Tipo de cambio e inflación de EE. UU. → `datossilverfred_diario` y `datossilverfred_mensual` ✅]] - document - docs/decisiones/10-silver-fase5.md
- [[Consecuencia]] - document - docs/decisiones/10-silver-fase5.md
- [[DataFrame_17]] - code
- [[DataFrame_18]] - code
- [[Definición tormenta que afecta al sur (≤200 km de Chetumal, ≥34 kt, desde 1966)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[Distancia sobre la esfera terrestre (radio 6,371 km). Ecuación en ECUACIONES.md…]] - rationale - backend/torre/base/silver_huracanes.py
- [[Evidencia de que funciona]] - document - docs/decisiones/10-silver-fase5.md
- [[HURDAT2 (trayectorias de huracanes, 1851–2025)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Hallazgo la temporada de lluvias coincide con la de huracanes (ago–oct)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Job publicar (checkout → configure-pages → upload-pages-artifact frontend → deploy-pages)]] - code - .github/workflows/pagina.yml
- [[Por qué ahora]] - document - docs/decisiones/10-silver-fase5.md
- [[Recorre el archivo una línea de encabezado (id, nombre, n puntos) seguida de n…]] - rationale - backend/torre/base/silver_huracanes.py
- [[Una fila por tormenta que afecta al sur mes del primer punto que cumple la…]] - rationale - backend/torre/base/silver_huracanes.py
- [[Workflow 'Publicar la página' (GitHub Pages)]] - code - .github/workflows/pagina.yml
- [[agregar_banderas()]] - code - backend/torre/base/silver_huracanes.py
- [[construir_silver_huracanes()]] - code - backend/torre/base/silver_huracanes.py
- [[dia()]] - code - tests/test_silver_fase5.py
- [[eventos_sur()]] - code - backend/torre/base/silver_huracanes.py
- [[fixture_6]] - code
- [[formato_irregular_flag (2 líneas mal escritas de HURDAT2)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[fred_mes()]] - code - tests/test_silver_fase5.py
- [[huracanes()_1]] - code - tests/test_silver_fase5.py
- [[km_haversine()]] - code - backend/torre/base/silver_huracanes.py
- [[leer_hurdat2()]] - code - backend/torre/base/silver_huracanes.py
- [[silver_huracanes.py]] - code - backend/torre/base/silver_huracanes.py
- [[test_31_eventos_desde_1966()]] - code - tests/test_silver_fase5.py
- [[test_clima_diario_forma()]] - code - tests/test_silver_fase5.py
- [[test_clima_horario_hora_local()]] - code - tests/test_silver_fase5.py
- [[test_clima_papel_de_los_puntos()]] - code - tests/test_silver_fase5.py
- [[test_dean_2007_y_carmen_1974()]] - code - tests/test_silver_fase5.py
- [[test_dias_sin_cotizacion_no_se_rellenan()]] - code - tests/test_silver_fase5.py
- [[test_faltantes_oficiales_son_nulos()]] - code - tests/test_silver_fase5.py
- [[test_haversine_a_mano()]] - code - tests/test_silver_fase5.py
- [[test_hurdat2_completo()]] - code - tests/test_silver_fase5.py
- [[test_lineas_irregulares_se_conservan_sin_inventar()]] - code - tests/test_silver_fase5.py
- [[test_lluvia_junio_chetumal()]] - code - tests/test_silver_fase5.py
- [[test_mes_en_curso_marcado()]] - code - tests/test_silver_fase5.py
- [[test_promedio_mensual_con_dias_observados()]] - code - tests/test_silver_fase5.py
- [[test_silver_fase5.py]] - code - tests/test_silver_fase5.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Silver_Fase_5_huracanes_HURDAT2
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_test_silver_fase5.py (Modelo de Poisson de hur)]]
- 2 edges to [[_COMMUNITY_Inventario de datos - fuentes oficiales verificadas]]
- 2 edges to [[_COMMUNITY_criterios.py]]
- 2 edges to [[_COMMUNITY_Pruebas de criterios]]
- 1 edge to [[_COMMUNITY_Regresión logística multiclase (modelo elegido del Radar)]]
- 1 edge to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan]]
- 1 edge to [[_COMMUNITY_Decisión 11 decisiones del Pronóstico]]
- 1 edge to [[_COMMUNITY_Cómo correrlo comandos por fase]]
- 1 edge to [[_COMMUNITY_frontendindex.html (página pública)]]
- 1 edge to [[_COMMUNITY_entorno.py]]
- 1 edge to [[_COMMUNITY_Pronóstico rango del 90 % (conformal)]]
- 1 edge to [[_COMMUNITY_Ingesta SITUR-Q y costos publicitarios]]
- 1 edge to [[_COMMUNITY_pdf.py]]
- 1 edge to [[_COMMUNITY_Auditoría cifras de los documentos]]
- 1 edge to [[_COMMUNITY_entrega.py]]
- 1 edge to [[_COMMUNITY_silver_clima.py]]

## Top bridge nodes
- [[silver_huracanes.py]] - degree 13, connects to 6 communities
- [[test_silver_fase5.py]] - degree 23, connects to 4 communities
- [[10-silver-fase5]] - degree 8, connects to 4 communities
- [[eventos_sur()]] - degree 8, connects to 1 community
- [[Definición tormenta que afecta al sur (≤200 km de Chetumal, ≥34 kt, desde 1966)]] - degree 6, connects to 1 community