# Torre del Caribe · Carpeta de entrega

Proyecto del Problema Prototípico *Turismo inteligente sustentable* (UNRC · LCDN 5° semestre 2026-2), Quintana Roo.
Equipo: Brandon Uriel García Sánchez · Maribel Mondragón Mercado · Jesús Ramírez Isidro · Enrique González Ortega.
Generada el 02/10/2026 con `python -m torre.documento.entrega` (no se edita a mano).

## Qué abrir primero
| Si eres… | Abre |
|---|---|
| Profesor o sinodal | `1_Guia_tecnica_formula_por_formula.pdf` y los notebooks de tu materia (tabla de abajo) |
| Integrante del equipo | `2_Guia_sencilla.pdf`, luego `3_Decisiones_fase_por_fase.pdf` |
| Quien redacta el informe | `4_Documento_ejecutivo.pdf` y `documentos/MAPA_DEL_INFORME.md` |
| Quien prepara el coloquio | `documentos/GUION_COLOQUIO.md` |

**La página web:** https://catoxp.github.io/torre-del-caribe-unrc-2026/ (o `frontend/index.html` del repositorio, sin
internet).

## Dónde está cada materia (UCA)
| Materia | Notebook (en `notebooks/`, ábrelo en .html) | Sección de la guía técnica |
|---|---|---|
| Planteamiento | `01_planteamiento` | §4.1 y §4.2 |
| Grandes volúmenes de datos | `06_torre_en_vivo` (Spark Streaming) y el código de `backend/torre/base/` | §3 |
| Minería de datos | `02_radar`, `03_pronostico`, `06_torre_en_vivo`, `07_campana` | §4 |
| Aprendizaje de máquina | `02_radar` (clasificador), `03_pronostico` (series de tiempo) | §5 |
| Procesos estocásticos | `02_radar` (Markov), `03_pronostico` (Poisson y Monte Carlo) | §6 |
| Investigación de Operaciones | `05_optimizacion` | §7 |
| Mercadotecnia digital | `07_campana` | §8 |

*No hay notebook 04:* el plan tenía un `04_escenarios` aparte, y esos escenarios quedaron dentro de `03_pronostico`.

## Contenido
| Archivo o carpeta | Qué es |
|---|---|
| `1_Guia_tecnica_formula_por_formula.pdf` | Todo el proyecto explicado: datos, código, cada fórmula con su ejemplo resuelto a mano y por qué se hizo así |
| `2_Guia_sencilla.pdf` | Lo mismo, sin tecnicismos |
| `3_Decisiones_fase_por_fase.pdf` | Cada decisión de las 12 fases: qué se eligió, qué se descartó y con qué evidencia |
| `4_Documento_ejecutivo.pdf` | El documento no técnico con gráficas y capturas, capítulo por fase |
| `notebooks/` | Los 6 notebooks ejecutados (.ipynb y .html) |
| `documentos/` | Ecuaciones, trazabilidad, diccionario de datos, mapa del informe, guion del coloquio, auditoría de la página y las 25 notas de decisión |

## Cómo se comprueba que las cifras son correctas
El repositorio tiene pruebas automáticas (`python -m pytest`). Entre ellas, `tests/test_guias.py` recalcula con los datos
las cifras de estas guías y `tests/test_documentos.py` las de los demás documentos.
