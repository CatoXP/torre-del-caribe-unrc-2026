---
type: community
members: 9
---

# Ingesta: manifiesto y riesgos

**Members:** 9 nodes

## Members
- [[Cap. 4 — Recolección de los datos oficiales (Fase 1) 15 fuentes, 353 archivos, 8,134,802 registros]] - document - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Capa Bronze (15 fuentes, 353 archivos, 8,134,802 registros)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Costos publicitarios WordStreamLocaliQ (Playwright)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Datos que no existen ocupación SITUR-Q termina dic-2024; afluencia y derrama hasta mar-2024; 'Turista - Afluencia' no responde]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Manifiesto con huella SHA-256]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Rest-Mex 2025 (reseñas)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[Scripts de ingesta Fase 1 (ingesta_siturq, ingesta_datatur, ingesta_abiertas, ingesta_benchmarks, evidencia_sargazo)]] - document - README.md
- [[Vigilancia del sargazo en la Bahía de Chetumal (canales al Caribe, no en la costa; pausa automática si llega)]] - concept - docs/ejecutivo/DOCUMENTO_EJECUTIVO.md
- [[playwright==1.49.1 (navegador automatizado)]] - concept - requirements.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Ingesta_manifiesto_y_riesgos
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Regla no inventar datos]]
- 1 edge to [[_COMMUNITY_Dependencias fijadas (requirements)]]
- 1 edge to [[_COMMUNITY_CLAUDE.md - Reglas del repositorio Torre del Caribe]]
- 1 edge to [[_COMMUNITY_Cómo correrlo comandos por fase]]
- 1 edge to [[_COMMUNITY_Silver reglas de SITUR-Q (ejecutivo)]]
- 1 edge to [[_COMMUNITY_Pronóstico métodos (documento ejecutivo)]]
- 1 edge to [[_COMMUNITY_Capacidad probada y regiones]]

## Top bridge nodes
- [[Capa Bronze (15 fuentes, 353 archivos, 8,134,802 registros)]] - degree 6, connects to 2 communities
- [[playwright==1.49.1 (navegador automatizado)]] - degree 4, connects to 1 community
- [[Costos publicitarios WordStreamLocaliQ (Playwright)]] - degree 4, connects to 1 community
- [[Manifiesto con huella SHA-256]] - degree 3, connects to 1 community
- [[Datos que no existen ocupación SITUR-Q termina dic-2024; afluencia y derrama hasta mar-2024; 'Turista - Afluencia' no responde]] - degree 2, connects to 1 community