---
type: community
members: 61
---

# Silver FRED y series a pronosticar

**Members:** 61 nodes

## Members
- [[Backtesting con origen móvil]] - concept - docs/metodologia/ECUACIONES.md
- [[Backtesting con origen móvil (validación temporal)]] - concept - docs/metodologia/ECUACIONES.md
- [[Capacidad probada sin usar K_s = 1 − V2025V2019]] - concept - docs/metodologia/ECUACIONES.md
- [[Cuántos meses tiene cada serie y cuántos entrenan, por motivo.]] - rationale - backend/torre/pronostico/series.py
- [[DataFrame]] - code
- [[DataFrame_1]] - code
- [[Decisión 11 — A3 Pronóstico (Fase 5, en curso)]] - document - docs/decisiones/11-pronostico.md
- [[Decisión 1 pronosticar 'Medidas + norte']] - rationale - docs/decisiones/11-pronostico.md
- [[Decisión 2 'Hueco + forma del año' (meses cerrados no entrenan)]] - rationale - docs/decisiones/11-pronostico.md
- [[Decisión técnica Holt-Winters con forma del año fija]] - rationale - docs/decisiones/11-pronostico.md
- [[Decisión 'Capacidad probada' (mes más alto ya recibido)]] - rationale - docs/decisiones/11-pronostico.md
- [[Decisión 'Menor error con rango ≥ 80 %']] - rationale - docs/decisiones/11-pronostico.md
- [[Decisión efecto de la campaña se ve en la Fase 6]] - rationale - docs/decisiones/11-pronostico.md
- [[Decisión mar–jun 2022 de Belice cuentan como pandemia]] - rationale - docs/decisiones/11-pronostico.md
- [[FRED CPIAUCSL (inflación de EE. UU.)]] - concept - docs/decisiones/10-silver-fase5.md
- [[FRED DEXMXUS (tipo de cambio diario peso-dólar)]] - concept - docs/decisiones/10-silver-fase5.md
- [[Fase 6 (asignación de la campaña y presupuesto)]] - concept - docs/decisiones/11-pronostico.md
- [[Gradient Boosting]] - concept - docs/metodologia/ECUACIONES.md
- [[Gradient Boosting con rezagos]] - concept - docs/decisiones/11-pronostico.md
- [[Hallazgo el clima casi no mejora el pronóstico]] - rationale - docs/decisiones/11-pronostico.md
- [[Hallazgo la Ruta no llega a 90 % de cobertura (caída de 2023)]] - rationale - docs/decisiones/11-pronostico.md
- [[Hallazgo las tormentas pesan en el mes, no en el año]] - rationale - docs/decisiones/11-pronostico.md
- [[Hallazgo riesgo de capacidad en meses pico (dic-2026, ene-2027)]] - rationale - docs/decisiones/11-pronostico.md
- [[Holt-Winters aditivo]] - concept - docs/metodologia/ECUACIONES.md
- [[Hueco Tren Maya con menos de 24 meses (variable, no se pronostica)]] - rationale - docs/decisiones/11-pronostico.md
- [[Intervalo conformal al 90 %]] - concept - docs/metodologia/ECUACIONES.md
- [[Meses que no entrenan (cierre, parcial, pandemia)]] - concept - docs/metodologia/ECUACIONES.md
- [[Monte Carlo de escenarios maloprobablebueno]] - concept - docs/metodologia/ECUACIONES.md
- [[Motivo por mes de UNA zona (índice = periodo, ordenado) 'cierre', 'mes…]] - rationale - backend/torre/pronostico/series.py
- [[Ocupación hotelera de Cancún (serie de referencia)]] - concept - docs/decisiones/11-pronostico.md
- [[Parámetros PANDEMIA_INAH y PANDEMIA_BELICE]] - concept - docs/decisiones/11-pronostico.md
- [[Pieza 2 descomposición estacional (forma y fuerza de la temporada)]] - concept - docs/decisiones/11-pronostico.md
- [[Regla región = suma de sus zonas]] - rationale - docs/decisiones/11-pronostico.md
- [[Reglas de cierre y mes parcial]] - concept - docs/decisiones/11-pronostico.md
- [[Regresión con clima]] - concept - docs/decisiones/11-pronostico.md
- [[Riesgo de rebasar la capacidad probada]] - concept - docs/metodologia/ECUACIONES.md
- [[STL como segunda opinión]] - concept - docs/metodologia/ECUACIONES.md
- [[Serie de cruces desde Belice (Chetumal)]] - concept - docs/decisiones/11-pronostico.md
- [[Serie de visitantes INAH Kohunlich + Dzibanché + Ichkabal (Ruta arqueológica del sur)]] - concept - docs/decisiones/11-pronostico.md
- [[Serie de visitantes INAH a Oxtankah (Bahía Calderitas–Oxtankah)]] - concept - docs/decisiones/11-pronostico.md
- [[Series]] - code
- [[Supuesto sitio cerrado no es 'sin demanda']] - rationale - docs/metodologia/ECUACIONES.md
- [[Tipo de cambio mensual (solo días observados)]] - concept - docs/metodologia/ECUACIONES.md
- [[_motivos_zona()]] - code - backend/torre/pronostico/series.py
- [[_pandemia()]] - code - backend/torre/pronostico/series.py
- [[_serie()]] - code - backend/torre/base/silver_fred.py
- [[construir()]] - code - backend/torre/pronostico/series.py
- [[construir_silver_fred()]] - code - backend/torre/base/silver_fred.py
- [[datosgoldpronostico_forma_anio.parquet]] - document - docs/decisiones/11-pronostico.md
- [[datosgoldpronostico_series.parquet]] - concept - docs/decisiones/11-pronostico.md
- [[guardar()]] - code - backend/torre/pronostico/series.py
- [[mensual()]] - code - backend/torre/base/silver_fred.py
- [[mes_incompleto_flag (mes en curso)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[resumen()]] - code - backend/torre/pronostico/series.py
- [[serie_belice()]] - code - backend/torre/pronostico/series.py
- [[serie_cancun()]] - code - backend/torre/pronostico/series.py
- [[series.py]] - code - backend/torre/pronostico/series.py
- [[series_inah()]] - code - backend/torre/pronostico/series.py
- [[silver_fred.py]] - code - backend/torre/base/silver_fred.py
- [[sin_dato_flag (huecos conservados vacíos)]] - rationale - docs/decisiones/10-silver-fase5.md
- [[tipo_cambio_diario()]] - code - backend/torre/base/silver_fred.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Silver_FRED_y_series_a_pronosticar
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Planeador NLP de negocios (DENUE)]]
- 5 edges to [[_COMMUNITY_Radar índice de presión (código)]]
- 4 edges to [[_COMMUNITY_Pronóstico forma del año y modelos]]
- 4 edges to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan]]
- 4 edges to [[_COMMUNITY_ECUACIONES]]
- 3 edges to [[_COMMUNITY_Pronóstico tormentas y escenarios]]
- 3 edges to [[_COMMUNITY_10-silver-fase5]]
- 2 edges to [[_COMMUNITY_test_planteamiento.py]]
- 2 edges to [[_COMMUNITY_silver_clima.py]]
- 2 edges to [[_COMMUNITY_Decisión la campaña promueve 5 regiones de Quintana Roo]]
- 1 edge to [[_COMMUNITY_Pronóstico rango del 90 % y elección]]
- 1 edge to [[_COMMUNITY_buscar_jdk17]]
- 1 edge to [[_COMMUNITY_pathlib]]
- 1 edge to [[_COMMUNITY_test_pronostico.py]]
- 1 edge to [[_COMMUNITY_markov.py]]
- 1 edge to [[_COMMUNITY_Censo (ITER) y criterios de regiones]]

## Top bridge nodes
- [[Decisión 11 — A3 Pronóstico (Fase 5, en curso)]] - degree 40, connects to 5 communities
- [[Monte Carlo de escenarios maloprobablebueno]] - degree 10, connects to 5 communities
- [[Backtesting con origen móvil]] - degree 9, connects to 4 communities
- [[series.py]] - degree 13, connects to 2 communities
- [[silver_fred.py]] - degree 8, connects to 2 communities