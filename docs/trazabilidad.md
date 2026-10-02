# Trazabilidad — de la cifra visible a su archivo crudo

Autor: **Brandon Uriel García Sánchez** · 02-oct-2026 · Regla de oro 2: *toda cifra es rastreable (archivo crudo →
función → salida)*.

## Cómo usar esta tabla
**Para defender una cifra frente al jurado** se sigue su fila de izquierda a derecha:
1. el archivo oficial descargado (Bronze, con su SHA-256 en `datos/bronze/MANIFIESTO.csv`);
2. la función que la calcula;
3. la tabla donde queda (Silver/Gold);
4. la prueba automática que avisa si deja de coincidir.

**Para cualquier otra cifra:**
- las de los documentos las compara `tests/test_documentos.py` (35 cifras);
- las de la página salen todas de `backend/torre/api/datos_pagina.py`;
- el significado de cada columna está en `docs/datos/DICCIONARIO.md`.

| Cifra | Dónde se ve | Archivo crudo (Bronze) | Función | Salida | Prueba |
|---|---|---|---|---|---|
| 8,134,802 registros oficiales en 353 archivos | Fases, Evidencia | `datos/bronze/**` | `base.manifiesto` | `MANIFIESTO.csv` | `test_ingesta.py` |
| 6,138,075 negocios del país | Fase 2, diccionario | `denue/*/denue_*_csv.zip` | `base.silver_denue` | `silver/denue` | `test_silver.py` |
| Los 5 lugares = 12.3 % de la población y 1.4 % de los pasajeros de avión | "El problema" | ITER, SITUR-Q | `radar.planteamiento.concentracion` | (cálculo) | `test_planteamiento.py` |
| Tulum 1,031,443 visitantes y la Ruta 66,628 en 2025 (15.5 veces menos) | Campaña, propuesta de valor | `datatur/*/inah/BdINAH.zip` | `base.silver_inah` → `campana.marca.cifras` | `silver/inah`, `gold/campana.json` | `test_campana.py` |
| Oxtankah 94.8 % y la Ruta 63.3 % de visitantes nacionales (2025) | Persona "La que vuelve" | BdINAH | `campana.marca.cifras` | `gold/campana.json` | `test_campana.py` |
| Chetumal: 250 extranjeros por avión en 2025; Cancún 9,408,423 | Persona "La que baja", Fase 2 | `datatur/*/nacionalidad/BD_Nacionalidad.zip` | `base.silver_nacionalidad` | `silver/nacionalidad`, `hechos_mes` | `test_silver_fase2.py` |
| Cancún: EE. UU. 56.3 %, Canadá 17.1 %, mujeres 53.4 % | Persona "La que baja" | BD_Nacionalidad | `campana.marca.cifras` | `gold/campana.json` | `test_campana.py` |
| Cruceristas en Cozumel 2025: DataTur 4,724,255 contra SITUR-Q 4,915,242 (+4.04 %) | Fase 2, conciliación | `BaseDatosCruceros.zip`, API SITUR-Q | `base.silver_cruceros.reconciliar_siturq` | `gold/reconciliacion_cruceros.parquet` | `test_silver_fase2.py` |
| Cortes del Radar semanal: p50 71.16 %, p90 85.92 % | Torre, norte | DataTur semanal | `radar.markov.estados` | `gold/envivo_senales.parquet` | `test_envivo.py` |
| Estado del mes siguiente (regresión logística; 130 de 156 aciertos) | Radar | Silver de varias fuentes | `radar.prediccion` | `gold/radar_prediccion.parquet` | `test_radar_prediccion.py` |
| Probabilidad de tormenta en agosto: 13.9 % | Planeador, Fase 5 | `huracanes/*/hurdat2-*.txt` | `pronostico.escenarios` (Poisson) | `gold/pronostico_poisson_tormentas.parquet` | `test_pronostico.py` |
| Pronóstico de 12 meses con rango del 90 % | Planeador | INAH, SITUR-Q (Belice) | `pronostico.modelos`, `intervalos`, `seleccion` | `gold/pronostico_mes.parquet` | `test_pronostico.py` |
| Temporada alta por lugar y mes | Planeador, presupuesto | Fase 5 | `pronostico.calendario` | `gold/pronostico_calendario.parquet` | `test_planeador.py` |
| Cancún 67.8 % de cuartos de 5★ (35,537 cuartos) | Ficha de Cancún | Compendio DataTur 2024, `5_2.xlsx` | `campana.estrellas` | (en la página) | `test_vitrina.py` |
| 957 visitantes con $187,500; $196 cada uno | Presupuesto, KPI | D13 benchmarks, FRED, Gold Fase 5 | `campana.presupuesto.resolver` | `gold/presupuesto_plan.parquet` | `test_presupuesto.py` |
| Google 1.59 y Facebook 6.61 visitantes por cada $1,000 | Presupuesto | `benchmarks/*/benchmarks_tablas.csv`, FRED | `campana.presupuesto.canales` | (cálculo) | `test_presupuesto.py` |
| Tope por canal: cuesta 29.5 % de los visitantes; las reglas ambientales, 0 | Presupuesto | — | `campana.presupuesto.costo_de_reglas` | `gold/presupuesto_reglas.parquet` | `test_presupuesto.py` |
| Hasta 40 % de la capacidad no se pierde ningún visitante | Presupuesto (Pareto) | — | `campana.presupuesto.pareto` | `gold/presupuesto_pareto.parquet` | `test_presupuesto.py` |
| 239 semanas en 239 lotes; 48 pausas; 6 semanas "¿Ibas al norte?" | Torre en vivo | DataTur, HURDAT2, Open-Meteo, Gold | `envivo.senales`, `envivo.torre` | `gold/envivo_decisiones.parquet` | `test_envivo.py` |
| Clima raro: 21 semanas (Chetumal) y 17 (Kohunlich) | Torre en vivo | `clima/*` (Open-Meteo horario) | `envivo.senales.anomalias_clima` | `gold/envivo_senales.parquet` | `test_envivo.py` |
| Ruido 2.76×, suciedad 1.89×, calma 0.41× en reseñas malas | Campaña | `restmex/*/Rest-Mex_2025_train.csv` | `campana.texto.aspectos` | `gold/campana_aspectos.parquet` | `test_campana.py` |
| Ruido + servicio ⇒ reseña mala, lift 2.82 | Campaña | Rest-Mex | `campana.texto.reglas_asociacion` | `gold/campana_reglas.parquet` | `test_campana.py` |
| Internet en Q. Roo 92.1 %; mensajería 90.6 %; redes 80.4 % | Persona, medios | `endutih/*/ENDUTIH_25_RR.pdf` (págs. 10 y 17) | `campana.marca.ENDUTIH` (transcrita con su página) | `gold/campana.json` | — (cifra transcrita del PDF oficial) |
| Modelo resuelto en 274 ms | "Pruébalo tú" (servidor) | — | `api.servidor.optimizar` | (respuesta de la API) | `test_api.py` (< 2 s) |
| 0 fallas de accesibilidad WCAG 2.1 AA en 4 vistas | Fase 10 | — | `documento.auditoria` | `docs/ejecutivo/AUDITORIA_PAGINA.md` | (se regenera) |

## Lo que se declara como hueco, no como cifra
- Ocupación hotelera del sur en 2025–2026: SITUR-Q publica ceros.
- Estado de origen, edad e ingreso del visitante nacional.
- Conversión de Facebook para turismo: se usa un barrido de supuestos.
- Tormentas de 2026: HURDAT2 aún no se publica.
- Reseñas de los 5 lugares: Rest-Mex no las cubre.
- Derrama económica por lugar: la de SITUR-Q no trae unidad y termina en marzo de 2024.
