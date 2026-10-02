# 18 — Cierre de la Fase 2: las últimas cuatro tablas, el almacén y el diccionario de datos

Autor: **Brandon Uriel García Sánchez** · 02-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Qué pidió Brandon
> Sigue y acaba con esas fases pendientes

Se cierran tres cosas:
- la Fase 2, que quedaba en curso;
- las Fases 3 y 4, que estaban listas para revisión y reciben el visto bueno con esta instrucción;
- y se abre la Fase 6 con las decisiones del mismo día (nota 19).

## Qué faltaba de la Fase 2 (plan, `docs/plan/PLAN_v3.md`)
| Punto del plan | Antes | Ahora |
|---|---|---|
| 1. Silver de cada fuente | Faltaban nacionalidad, AFAC, cruceros y Rest-Mex | **Las 14 fuentes en Silver** |
| 2. Modelo estrella en Gold + diccionario automático | No existían | `dim_lugar`, `dim_tiempo`, `hechos_mes` + `docs/datos/DICCIONARIO.md` (44 tablas) |
| 3. Reconciliación entre fuentes | Ocupación SITUR-Q vs DataTur (nota 09) | + Cruceristas DataTur vs SITUR-Q |
| 4. DuckDB apuntando a Gold | No existía | `datos/gold/torre.duckdb`: una vista por tabla de Silver y de Gold |

## Las cuatro tablas nuevas

### 1. Nacionalidad (`torre.base.silver_nacionalidad`)
- **Contenido:** 521,363 renglones, de 2012 a julio de 2026, de llegadas de **extranjeros** por avión. La base no trae
  país "México", por eso la columna se llama `llegadas_extranjeros`.
- **Calidad:** 0 llaves repetidas.
- **Hallazgo para la campaña:**

  | Aeropuerto | Extranjeros que llegaron en 2025 |
  |---|---:|
  | Cancún | 9,408,423 |
  | Tulum | 323,948 |
  | Cozumel | 192,206 |
  | **Chetumal** | **250** |

  En 2024 llegaron a Chetumal 217,524 pasajeros (SITUR-Q) y solo 202 eran extranjeros. **El sur casi no recibe turismo
  internacional por avión**: su visitante extranjero entra por Cancún, por tierra (Belice, Tren Maya) o en crucero. Eso
  decide dónde anunciar (Fase 6).
- **Tulum:** su aeropuerto abre en feb-2024; antes no hay renglones, y eso no es un cero.

### 2. AFAC (`torre.base.silver_afac`)
Son pasajeros nacionales por aerolínea, 2016 → jul-2026. El archivo traía **300 llaves repetidas**:

| Caso | Llaves | Regla |
|---|---:|---|
| Renglones idénticos | 98 | Se deja uno |
| Una cifra y una copia en cero | 177 | Se conserva la cifra (misma regla que INAH) |
| Dos cifras distintas | 25 | Todas de "Virgin América (Alaska Airlines)", 2016 → ene-2018 |

- **Decisión de Brandon (las dos cifras): sumarlas**, con `sumada_flag`. Son dos aerolíneas que se fusionaron en 2018 y
  quedaron bajo una sola etiqueta. En juego hay 369,311 pasajeros de 1,042 millones (0.035 %).
- **Opciones descartadas:** dejar dos renglones marcados (obliga a recordarlo en cada suma) y dejar AFAC fuera.
- **Regla de paro:** si aparece otra etiqueta con dos cifras, el proceso se detiene (regla de oro 5).
- **Resultado:** 19,277 renglones; 122,722,745 pasajeros en 2025.

### 3. Cruceros (`torre.base.silver_cruceros`)
- **Contenido:** 3,895 renglones, sin repetidos.
- **Puertos sin cruceros:** Cancún, Playa del Carmen, Puerto Morelos y Punta Venado traen **0 en todos los meses**.
  Están en el catálogo pero no reciben cruceros, así que se marcan con `puerto_sin_cruceros_flag` y no se borran.
- **Reconciliación con SITUR-Q** (`gold/reconciliacion_cruceros.parquet`):

  | Año | Cozumel DataTur | Cozumel SITUR-Q | Dif. | Mahahual DataTur | Mahahual SITUR-Q | Dif. |
  |---|---:|---:|---:|---:|---:|---:|
  | 2019 | 4,569,853 | 4,772,311 | +4.4 % | 1,604,435 | 2,164,161 | +34.9 % |
  | 2024 | 4,619,126 | 4,598,918 | −0.4 % | 2,205,335 | 2,568,579 | +16.5 % |
  | 2025 | 4,724,255 | 4,915,242 | +4.0 % | 2,379,422 | 2,641,695 | +11.0 % |

  - En Cozumel las dos fuentes casi coinciden.
  - En Mahahual, **SITUR-Q siempre cuenta más**, entre 11 % y 35 %.
  - La regla no cambia: el Radar sigue con SITUR-Q (Fase 4), que es la fuente de todos los demás indicadores del sur.
    La diferencia se declara.

### 4. Rest-Mex (`torre.base.silver_restmex`)
- **Lectura:** PySpark lee el CSV directo, porque las reseñas traen saltos de línea dentro de las comillas.
- **Limpieza:**
  - quedan 207,873 reseñas, después de quitar 178 idénticas;
  - los nombres se hacen legibles ("QuintanaRoo" → "Quintana Roo");
  - el tipo se pasa a español.
- **Límite declarado:** en Quintana Roo solo hay **Tulum, Isla Mujeres y Bacalar**, ninguno de los 5 lugares. Sirve para
  saber qué molesta en los destinos llenos y con qué palabras habla el turista (Fase 8), no para opinar del sur.

## El almacén (`torre.base.almacen`) y el diccionario (`torre.base.diccionario`)
- **DuckDB** lee los mismos Parquet sin copiarlos:
  - 14 vistas de Silver y 27 de Gold;
  - responde en milisegundos sin levantar Spark.
  - **Opción descartada:** PostgreSQL, porque exige un servidor y el proyecto debe correr sin internet en cualquier
    computadora.
- **Modelo estrella:**
  - `hechos_mes` tiene 3,287 renglones: lugar × mes × variable, con su fuente.
  - **Un hueco no tiene renglón** y nunca se rellena con cero. Una prueba lo vigila.
  - Las dimensiones son 15 lugares (5 promovidos, 3 de referencia y 7 de comparación) y 192 meses.
- **Diccionario de datos generado** desde el almacén. Cada columna trae su tipo, el % de vacíos, un ejemplo real y su
  significado. Si una columna de Silver no tiene significado escrito, el proceso se detiene.

## Evidencia
- `tests/test_silver_fase2.py`: 10 pruebas con cifras conocidas, entre ellas:
  - Chetumal 250, Cancún 9,408,423;
  - 25 llaves sumadas en AFAC;
  - la conciliación de Cozumel a mano: (4,915,242 ÷ 4,724,255 − 1) × 100 = 4.04 %;
  - 207,873 reseñas;
  - la estrella sin huérfanos;
  - el almacén igual a Silver.
- `docs/metodologia/ECUACIONES.md` §1-quater.

## Consecuencia
La Fase 2 queda **cerrada**: las 14 fuentes oficiales están limpias, documentadas y consultables.
- Las Fases 3 y 4 quedan **cerradas** con el visto bueno de Brandon.
- El hallazgo de Chetumal (250 extranjeros por avión) entra a la Fase 6: el anuncio para el extranjero tiene que
  alcanzarlo **en Cancún o antes de llegar**, no en Chetumal.
