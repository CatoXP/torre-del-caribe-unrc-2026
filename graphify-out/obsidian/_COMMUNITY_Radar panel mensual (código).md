---
type: community
members: 36
---

# Radar: panel mensual (código)

**Members:** 36 nodes

## Members
- [[Contrato del cascarón (claves de pagina.js por fase)]] - rationale - docs/decisiones/06-pagina.md
- [[Contrato pagina.js ninguna cifra escrita a mano en el HTML]] - rationale - README.md
- [[Cómo correrlo comandos por fase]] - document - README.md
- [[DIBUJAR]] - code - frontend/app.js
- [[DataFrame]] - code
- [[Fase 2 (SilverGold) incompleta]] - rationale - docs/decisiones/09-auditoria-fases-1-4.md
- [[Fase 3 torre.radar.criterios + notebook 01_planteamiento]] - document - README.md
- [[Fase 4 torre.radar.panel → datosgoldradar_panel_mensual.parquet]] - document - README.md
- [[Holt-Winters aditivo (A3 Pronóstico, previsto)]] - concept - docs/metodologia/ECUACIONES.md
- [[Intervalo conformal al 90 %]] - concept - docs/metodologia/ECUACIONES.md
- [[Meses con dato por lugar y variable (de cuántos posibles). Sirve para ver qué…]] - rationale - backend/torre/radar/panel.py
- [[Modelo Poisson de huracanes]] - concept - docs/metodologia/ECUACIONES.md
- [[Modelo estocástico de dos etapas (IO, PuLPCBC)]] - concept - docs/metodologia/ECUACIONES.md
- [[Monte Carlo escenarios malo  probable  bueno]] - concept - docs/metodologia/ECUACIONES.md
- [[Módulos ocultos data-clave (pronostico, envivo, escenarios, presupuesto, campana)]] - code - frontend/index.html
- [[Ocupación mensual desde DataTur semanal Σ cuartos ocupados ÷ Σ cuartos…]] - rationale - backend/torre/radar/panel.py
- [[Path]] - code
- [[Página torre.base.ubicaciones, torre.base.ingesta_fotos]] - document - README.md
- [[Scripts Silver (silver_siturq, silver_datatur_ocupacion, silver_denue, silver_inah, silver_iter)]] - document - README.md
- [[Scripts de ingesta Fase 1 (ingesta_siturq, ingesta_datatur, ingesta_abiertas, ingesta_benchmarks, evidencia_sargazo)]] - document - README.md
- [[Series]] - code
- [[Una fila por lugar × mes, de DESDE al último mes publicado. Las celdas sin dato…]] - rationale - backend/torre/radar/panel.py
- [[Variables de SITUR-Q por lugar y mes (sin huecos el hueco queda como ausencia…]] - rationale - backend/torre/radar/panel.py
- [[Visitantes (nacionales + extranjeros) a zonas arqueológicas por lugar y mes.]] - rationale - backend/torre/radar/panel.py
- [[_datatur()]] - code - backend/torre/radar/panel.py
- [[_inah()]] - code - backend/torre/radar/panel.py
- [[_poblacion()]] - code - backend/torre/radar/panel.py
- [[_siturq()]] - code - backend/torre/radar/panel.py
- [[cobertura()]] - code - backend/torre/radar/panel.py
- [[frontenddatospagina.js]] - code - frontend/index.html
- [[guardar()]] - code - backend/torre/radar/panel.py
- [[panel.py]] - code - backend/torre/radar/panel.py
- [[panel_mensual()]] - code - backend/torre/radar/panel.py
- [[scipy==1.13.1 (Poisson y estadística)]] - concept - requirements.txt
- [[torre.api.datos_pagina → frontenddatospagina.js]] - document - README.md
- [[torre.documento.pdf  torre.documento.figuras (documento ejecutivo)]] - document - README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Radar_panel_mensual_código
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Radar decisiones y piezas]]
- 2 edges to [[_COMMUNITY_Radar índice y predicción (código)]]
- 2 edges to [[_COMMUNITY_Silver Censo (ITER) y criterios]]
- 1 edge to [[_COMMUNITY_Ecuaciones y fuentes del documento (Estados tranquilo  conc)]]
- 1 edge to [[_COMMUNITY_Pruebas del planteamiento]]
- 1 edge to [[_COMMUNITY_Planteamiento (HHI) y clustering de centros]]
- 1 edge to [[_COMMUNITY_Radar cadena de Markov semanal]]
- 1 edge to [[_COMMUNITY_Silver ocupación DataTur y Spark (pathlib)]]
- 1 edge to [[_COMMUNITY_Página app.js y animaciones]]
- 1 edge to [[_COMMUNITY_Página módulos, fases y chat]]
- 1 edge to [[_COMMUNITY_09 — Auditoría de las Fases 1 a 4 contra el plan]]

## Top bridge nodes
- [[panel.py]] - degree 17, connects to 7 communities
- [[Monte Carlo escenarios malo  probable  bueno]] - degree 4, connects to 1 community
- [[frontenddatospagina.js]] - degree 3, connects to 1 community
- [[Fase 2 (SilverGold) incompleta]] - degree 3, connects to 1 community
- [[DIBUJAR]] - degree 2, connects to 1 community