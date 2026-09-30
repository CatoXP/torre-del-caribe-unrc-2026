---
type: community
members: 12
---

# Pruebas Silver

**Members:** 12 nodes

## Members
- [[2,243 filas (todas las del CSV de conjunto_de_datos, sin descartar ninguna);…]] - rationale - tests/test_silver.py
- [[El bloque duplicado 'Extranjero, sep-2025' (283 filas en cero) ya no está…]] - rationale - tests/test_silver.py
- [[La ocupación que publica DataTur debe ser ocupados ÷ disponibles; se tolera 0.5…]] - rationale - tests/test_silver.py
- [[Lo que INEGI reserva con '' queda como nulo con reservado_flag, nunca como 0…]] - rationale - tests/test_silver.py
- [[test_columnas()]] - code - tests/test_silver.py
- [[test_denue_coordenadas_validas()]] - code - tests/test_silver.py
- [[test_inah_sin_llaves_repetidas()]] - code - tests/test_silver.py
- [[test_iter_filas_y_total_estatal()]] - code - tests/test_silver.py
- [[test_iter_reservados_son_nulos_no_ceros()]] - code - tests/test_silver.py
- [[test_ocupacion_publicada_coincide_con_calculada()]] - code - tests/test_silver.py
- [[test_silver.py]] - code - tests/test_silver.py
- [[test_sin_duplicados()]] - code - tests/test_silver.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pruebas_Silver
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Pruebas SITUR-Q (Tren Maya, huecos)]]
- 5 edges to [[_COMMUNITY_Fixtures de pruebas]]
- 2 edges to [[_COMMUNITY_Pruebas de criterios]]
- 1 edge to [[_COMMUNITY_Prueba 239 semanas DataTur]]
- 1 edge to [[_COMMUNITY_test_nota_isla_mujeres()]]
- 1 edge to [[_COMMUNITY_Prueba total DENUE]]
- 1 edge to [[_COMMUNITY_test_denue_turisticos_qroo()]]
- 1 edge to [[_COMMUNITY_test_denue_sin_datos_personales()]]
- 1 edge to [[_COMMUNITY_Prueba cifras INAH]]
- 1 edge to [[_COMMUNITY_Pruebas Silver (test_inah_kohunlich_crec)]]
- 1 edge to [[_COMMUNITY_test_inah_papel_de_las_zonas()]]
- 1 edge to [[_COMMUNITY_Pruebas Silver (test_iter_poblacion_de_l)]]
- 1 edge to [[_COMMUNITY_Pruebas Silver (test_cero_real_se_conser)]]
- 1 edge to [[_COMMUNITY_test_regla_6_aereos()]]
- 1 edge to [[_COMMUNITY_Pruebas Silver (test_afluencia_y_derrama)]]
- 1 edge to [[_COMMUNITY_test_cancun_semana_31_2026()]]
- 1 edge to [[_COMMUNITY_Pruebas del planteamiento]]
- 1 edge to [[_COMMUNITY_Auditoría cifras de los documentos]]
- 1 edge to [[_COMMUNITY_Silver ocupación DataTur y Spark (pathlib)]]
- 1 edge to [[_COMMUNITY_SITUR-Q y reglas de datos]]

## Top bridge nodes
- [[test_silver.py]] - degree 36, connects to 20 communities