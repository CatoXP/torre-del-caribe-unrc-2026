---
type: community
members: 44
---

# Silver Fase 5: huracanes (HURDAT2)

**Members:** 44 nodes

## Members
- [[1. Huracanes → `datossilverhuracanes` ✅]] - document - docs/decisiones/10-silver-fase5.md
- [[10 — Datos limpios para el Pronóstico huracanes, clima y tipo de cambio (Fase 2, cierre de la parte que usa la Fase 5)]] - document - docs/decisiones/10-silver-fase5.md
- [[10-silver-fase5]] - document - docs/decisiones/10-silver-fase5.md
- [[2. Clima → `datossilverclima_diario` y `datossilverclima_horario` ✅]] - document - docs/decisiones/10-silver-fase5.md
- [[3. Tipo de cambio e inflación de EE. UU. → `datossilverfred_diario` y `datossilverfred_mensual` ✅]] - document - docs/decisiones/10-silver-fase5.md
- [[Consecuencia]] - document - docs/decisiones/10-silver-fase5.md
- [[DataFrame_18]] - code
- [[DataFrame_19]] - code
- [[Definición tormenta que afecta al sur (≤200 km de Chetumal, ≥34 kt, desde 1966)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[Distancia de haversine]] - concept - docs/metodologia/ECUACIONES.md
- [[Distancia sobre la esfera terrestre (radio 6,371 km). Ecuación en ECUACIONES.md…]] - rationale - backend/torre/base/silver_huracanes.py
- [[Evidencia de que funciona]] - document - docs/decisiones/10-silver-fase5.md
- [[HURDAT2 (trayectorias de huracanes)]] - concept - docs/metodologia/ECUACIONES.md
- [[HURDAT2 (trayectorias de huracanes, 1851–2025)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Por qué ahora]] - document - docs/decisiones/10-silver-fase5.md
- [[Recorre el archivo una línea de encabezado (id, nombre, n puntos) seguida de n…]] - rationale - backend/torre/base/silver_huracanes.py
- [[Tormenta que afecta al sur (≤200 km, ≥34 nudos, ≥1966)]] - concept - docs/metodologia/ECUACIONES.md
- [[Una fila por tormenta que afecta al sur mes del primer punto que cumple la…]] - rationale - backend/torre/base/silver_huracanes.py
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
- [[math]] - concept
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
- 3 edges to [[_COMMUNITY_ECUACIONES.md — Ecuaciones y cómo lo resolví]]
- 2 edges to [[_COMMUNITY_Pronóstico forma del año y modelos]]
- 2 edges to [[_COMMUNITY_lugares.py]]
- 2 edges to [[_COMMUNITY_test_radar_panel.py]]
- 2 edges to [[_COMMUNITY_sys]]
- 1 edge to [[_COMMUNITY_escenarios.py (Decisión 3 temporada al)]]
- 1 edge to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan]]
- 1 edge to [[_COMMUNITY_Contrato pagina.js ninguna cifra escrita a mano en el HTML]]
- 1 edge to [[_COMMUNITY_Pronóstico tormentas y escenarios]]
- 1 edge to [[_COMMUNITY_entorno.py]]
- 1 edge to [[_COMMUNITY_Ingesta DataTur y costos publicitarios]]
- 1 edge to [[_COMMUNITY_sys (sys)]]
- 1 edge to [[_COMMUNITY_pathlib (pathlib)]]
- 1 edge to [[_COMMUNITY_silver_clima.py]]

## Top bridge nodes
- [[test_silver_fase5.py]] - degree 23, connects to 4 communities
- [[silver_huracanes.py]] - degree 12, connects to 4 communities
- [[10-silver-fase5]] - degree 8, connects to 3 communities
- [[Distancia de haversine]] - degree 6, connects to 2 communities
- [[Tormenta que afecta al sur (≤200 km, ≥34 nudos, ≥1966)]] - degree 5, connects to 2 communities