# Mapa del informe técnico — de cada sección a sus archivos

Autor: **Brandon Uriel García Sánchez** · 02-oct-2026.

El Problema Prototípico pide un informe técnico de 30 a 40 páginas (Entregable B). Esta tabla dice, para cada sección
obligatoria, de dónde sale el contenido. La redacción en limpio parte de dos fuentes:
- el **documento ejecutivo** (`Documento_Ejecutivo_Torre_del_Caribe.pdf`), que ya está en lenguaje no técnico, con
  gráficas y capturas;
- las **notas de decisión** (`docs/decisiones/`), que traen la evidencia y las opciones descartadas.

| Sección del informe | Contenido principal | Archivos | Capítulo del documento ejecutivo |
|---|---|---|---|
| Portada | Proyecto, equipo, UNRC, LCDN 5° 2026-2 | `README.md`, `docs/ejecutivo/GUIA_ESTILO_UNRC.md` | Portada |
| Introducción | Turismo concentrado en el norte; el sur con espacio | `OBJETIVO.md` (A.3), `docs/regiones/REGIONES.md` | 1 |
| Planteamiento del problema | Variables, actores y relaciones; 12.3 % de la población y 1.4 % de los pasajeros de avión | `docs/decisiones/05-planteamiento.md`, `notebooks/01_planteamiento.ipynb` | 2, 7 |
| Pregunta central y secundarias | Las 7 preguntas y qué módulo responde cada una | `OBJETIVO.md` A.3, `docs/plan/PLAN_v3.md` B.3 | 1 |
| Justificación | Sargazo, cierres y saturación de 2026; capacidad ociosa del sur | `docs/regiones/REGIONES.md`, `docs/decisiones/01-regiones.md` | 2 |
| Fuentes de datos | D1–D15, cobertura y huecos | `docs/datos/INVENTARIO.md`, `docs/decisiones/03-ingesta.md` | 4 |
| Arquitectura y almacenamiento | Bronze → Silver → Gold, PySpark, DuckDB con modelo estrella, streaming | `docs/decisiones/02-entorno.md`, `04-silver.md`, `18-cierre-fase-2.md`, `20-torre-en-vivo.md` | 3, 5 |
| Preparación y calidad | Reglas de limpieza, duplicados, conciliación entre fuentes, diccionario | `docs/decisiones/04-silver.md`, `10-silver-fase5.md`, `18-cierre-fase-2.md`, `docs/datos/DICCIONARIO.md` | 5 |
| Minería de datos | Índice de presión, clustering Ward, forma del año, Isolation Forest, minería de texto | `08-radar.md`, `09-auditoria-fases-1-4.md`, `11-pronostico.md`, `20-torre-en-vivo.md`, `21-campana.md` | 8, 9, 11, 12 |
| Aprendizaje de máquina | Clasificador del estado (logística contra RF y GB); pronóstico (5 modelos, origen móvil, rango conformal) | `08-radar.md`, `11-pronostico.md`, notebooks 02 y 03 | 8, 9 |
| Estocásticos y escenarios | Markov semanal, Poisson de tormentas, Monte Carlo malo/probable/bueno, sensibilidad | `08-radar.md`, `11-pronostico.md`, notebook 03 | 8, 9 |
| Investigación de Operaciones | Modelo estocástico de dos etapas, precios sombra, Pareto | `19-presupuesto.md`, notebook 05, `ECUACIONES.md` §4 | 10 |
| Mercadotecnia digital | Personas, marca, mensajes, medios, piezas, implementación | `21-campana.md`, notebook 07 | 12 |
| Integración de resultados | Estafeta Pronóstico → Radar → Torre → campaña | `docs/plan/PLAN_v3.md` B.1, `19-presupuesto.md`, `20-torre-en-vivo.md` | 10, 11 |
| Diseño y justificación de la campaña | "El sur tiene espacio": tono, lenguaje real de las reseñas, anuncios con respaldo | `21-campana.md` | 12 |
| Comparación de escenarios | Escenarios del Monte Carlo; sensibilidad del presupuesto (3 % / 5.75 % / 6.38 %, $500k, tormentas) | `11-pronostico.md`, `19-presupuesto.md` | 9, 10 |
| Presupuesto y optimización | $187,500 en 9 meses; 957 visitantes; costo de cada regla | `19-presupuesto.md`, `gold/presupuesto_*` | 10 |
| Indicadores | 10 KPI con fórmula, meta, fuente y frecuencia | `21-campana.md` | 12 |
| Propuesta final | Campaña en el sur con reglas anti-colapso automáticas | `21-campana.md`, `20-torre-en-vivo.md`, página | 10–12 |
| Conclusiones | Lo que se demostró con datos | Secciones "Qué se concluye" de los notebooks 01–07 | Todos |
| Limitaciones | Huecos declarados y supuestos | `docs/trazabilidad.md` (huecos), "Limitaciones" de cada nota | Todos |
| Referencias | Fuentes oficiales y métodos | `docs/datos/INVENTARIO.md`, `ECUACIONES.md` | — |
| Anexos | Ecuaciones con ejemplos a mano, diccionario, trazabilidad, auditoría | `docs/metodologia/ECUACIONES.md`, `docs/datos/DICCIONARIO.md`, `docs/trazabilidad.md`, `docs/ejecutivo/AUDITORIA_PAGINA.md` | — |

## Productos técnicos (Entregable C)
| Producto | Dónde está |
|---|---|
| Bases de datos | `datos/bronze`, `silver` y `gold` (no van a git por tamaño; se reconstruyen con el README); `datos/gold/torre.duckdb` |
| Diccionario de datos | `docs/datos/DICCIONARIO.md` |
| Código | `backend/torre/` (paquete comentado en español) |
| Modelos | `gold/radar_*`, `gold/pronostico_*`, `gold/presupuesto_*`, `gold/envivo_*`, `gold/campana*` |
| Notebooks | `notebooks/01`–`07` (se construyen y ejecutan con `_construir_*.py`) |
| Consultas | `/api/consulta` (solo lectura) y las vistas de `torre.duckdb` |
| Diagramas y visualizaciones | `docs/ejecutivo/figuras/`, `capturas/` y la página |
| Simulaciones | Monte Carlo (`pronostico.escenarios`) y reproducción de la Torre (`envivo.torre`) |
| Optimización | `campana.presupuesto` (PuLP/CBC) |
| Documentación | `README.md`, `docs/decisiones/00`–`24`, `ECUACIONES.md`, documento ejecutivo |
