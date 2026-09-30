# 05 — Planteamiento con datos (Fase 3) · EN CURSO

Autor: **Brandon Uriel García Sánchez** · 28-sep-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Qué se resuelve en esta fase
1. La **tabla de criterios** (D.1 de `docs/regiones/REGIONES.md`) calculada con datos para las 5 regiones, con Cancún,
   Riviera Maya y Tulum al lado como referencia.
2. Las **variables, actores y relaciones** del problema (notebook `notebooks/01_planteamiento.ipynb`).
3. Cómo se trata el sur, que no tiene ocupación hotelera oficial en 2025–2026.

## Decisiones de Brandon (28-sep-2026)

### 1. Foco en 5 regiones
Chetumal · Bahía Calderitas–Oxtankah · Ruta arqueológica del sur · Maya Ka'an + Kantemó · Laguna Milagros–Xul-Ha.
Cancún, Riviera Maya y Tulum solo como referencia. Detalle y evidencia en `01-regiones.md`.

### 2. La población de cada región se mide por localidad (Censo 2020, ITER)
**Por qué:** 4 de las 5 regiones están en Othón P. Blanco (233,648 habitantes). Con la cifra municipal, Chetumal,
Calderitas, Laguna Milagros y la ruta sur tendrían el mismo denominador y no se podrían comparar entre sí.

| Región | Localidades (clave INEGI) | Población 2020 |
|---|---|---:|
| Chetumal | Chetumal (004-0001) | 169,028 |
| Bahía Calderitas–Oxtankah | Calderitas (004-0016) | 5,551 |
| Laguna Milagros–Xul-Ha | Xul-Ha (004-0114) 2,341 + Huay-Pix (004-0037) 1,841 | 4,182 |
| Ruta arqueológica del sur | Nicolás Bravo (004-0064) 3,699 + Morocoy (004-0245) 1,436 + Francisco Villa (004-0033) 963 | 6,098 |
| Maya Ka'an + Kantemó | Felipe Carrillo Puerto (002-0001) 30,754 + Tihosuco (002-0250) 5,228 + Chunhuhub (002-0044) 4,375 + Señor (002-0239) 3,785 + Kantemó (006-0076) 246 | 44,388 |

- **Criterio para elegir las localidades:** la localidad que da nombre a la región; en la laguna, las dos orillas
  habitadas; en la ruta sur, los poblados de acceso a Kohunlich y Dzibanché; en Maya Ka'an, la cabecera y los pueblos
  de las experiencias comunitarias promovidas por el Estado en 2026, más Kantemó.
- **Opción descartada:** población municipal (motivo arriba).
- **Riesgo declarado:** la lista es un criterio del proyecto, no una delimitación oficial. Está escrita en
  `backend/torre/base/silver_iter.py` (`REGION_LOCALIDADES`), y el código se detiene si una clave no corresponde al
  nombre esperado.

### 3-bis. Regla del criterio de cierres: 12 meses seguidos abierta
Las zonas de la ruta sur y Oxtankah también cerraron por obras en 2024: Oxtankah de oct-2023 a oct-2024, Kohunlich de
mar a dic-2024 y Dzibanché de feb-2024 a ene-2025. Muyil salió por cierre, así que hacía falta una regla que se aplique
igual a todas las zonas. **Decisión de Brandon:** una zona pasa si lleva al menos 12 meses seguidos abierta y no tuvo
cierres en 2026. Con la regla, Oxtankah (21 meses), Kohunlich (19) y Dzibanché (18) pasan; Muyil (6) queda fuera.
**Opción descartada:** "ningún cierre desde 2024". Sacaría a la ruta sur y a Calderitas–Oxtankah, y quedarían 3 regiones.

### 3. El sur se mide con presión de llegada medida, sin estimar ocupación
**Por qué:** SITUR-Q no publica ocupación hotelera 2025–2026 para ningún destino (termina en dic-2024), y DataTur
semanal solo cubre 7 centros del norte. Lo que sí se mide hasta 2026 en el sur:
- personas que bajaron del Tren Maya en Chetumal: 3,843 en julio de 2026 (SITUR-Q);
- cruces desde Belice: 49,097 en junio de 2026 (SITUR-Q);
- visitantes INAH: ruta sur 66,628 y Oxtankah 11,017 en 2025;
- habitaciones: Chetumal 2,114 y Maya Ka'an 330 en julio de 2026 (SITUR-Q).

La ocupación 2025–2026 del sur se muestra como **"sin dato oficial"**. **Opción descartada:** estimarla con un modelo
entrenado en 2019–2024 y etiquetarla `_est`. Sería una cifra estimada donde no hay medición. Si hace falta, se evalúa en
la Fase 5 (A3 Pronóstico), con su validación ciega.

## Avance (34 pruebas en verde en todo el proyecto)
- ✅ **INAH en Silver** (`backend/torre/base/silver_inah.py`): 71,278 filas; se quitó un bloque duplicado de
  sep-2025; cada zona lleva su papel en la campaña. 4 pruebas nuevas en verde. Detalle en `04-silver.md`.
- ✅ **Censo 2020 (ITER) en Silver** (`backend/torre/base/silver_iter.py`): 2,243 filas y 2,207 localidades;
  población, viviendas y servicios (agua, drenaje, luz); lo que INEGI reserva con "*" queda como nulo (1,627
  localidades pequeñas tienen algún dato reservado). Las poblaciones de las 5 regiones coinciden con la tabla de arriba.
  3 pruebas nuevas en verde.
- ⚠️ **Segunda corrección de conteo de la Fase 1:** el Censo tiene 2,243 localidades, no 2,257. El conteo sumaba el
  catálogo `tam_loc` (14 filas). Total correcto de la Fase 1: 353 archivos y **8,134,802** registros. Detalle en
  `03-ingesta.md`.
- ✅ **Tabla de criterios** (`backend/torre/radar/criterios.py` → `datos/gold/criterios_regiones.parquet`), con 4
  pruebas en `tests/test_criterios.py` y ecuaciones en `ECUACIONES.md` §1-bis:

| Región | Sargazo | Cierres (meses seguidos abierta) | Ocupación 2024 | Visitantes INAH por residente | Negocios turísticos por 1,000 hab. | Viviendas sin drenaje | Series oficiales |
|---|---|---|---:|---:|---:|---:|---:|
| Chetumal | vigilancia | pasa (sin zona INAH) | 58.0 % | — | 8.5 | 1.1 % | 4 |
| Bahía Calderitas–Oxtankah | vigilancia | pasa (21) | sin dato | 2.0 | 12.6 | 1.4 % | 3 |
| Ruta arqueológica del sur | no aplica | pasa (18) | sin dato | 10.9 | 10.5 | 4.8 % | 3 |
| Maya Ka'an + Kantemó | no aplica | pasa (sin zona INAH) | 38.6 % | — | 8.7 | 5.1 % | 4 |
| Laguna Milagros–Xul-Ha | no aplica | pasa (sin zona INAH) | sin dato | — | 0.5 | 1.0 % | 2 |
| *Cancún (referencia)* | afectada | pasa (13) | 76.1 % | 0.1 | 5.7 | 1.7 % | 5 |
| *Playa del Carmen (referencia)* | afectada | pasa | 76.9 % | — | 6.4 | 4.1 % | 4 |
| *Tulum (referencia)* | afectada | **no pasa** (cierres de negocios 2026) | 73.7 % | 30.9 | 26.5 | 3.2 % | 5 |

  **Lectura:**
  - Las 5 regiones pasan sargazo y cierres.
  - Donde hay dato, sus hoteles se llenaron mucho menos en 2024 (58 % y 39 %, contra 74–77 % en el norte).
  - La ruta sur recibe 10.9 visitantes por residente: un tercio de Tulum, pero no es poco. Necesitará tope en la Fase 6.
  - Laguna Milagros es la región con menos datos (2 series) y casi sin oferta (0.5 negocios por mil): se promueve con
    límite estricto y como visita desde Chetumal.
- ✅ **Ubicación comprobada:** los 11 pueblos y las 4 zonas están en Quintana Roo y en su municipio
  (`backend/torre/base/ubicaciones.py`; detalle en `06-pagina.md`).
- ✅ **Notebook `notebooks/01_planteamiento.ipynb`** (variables, actores y relaciones). Lo construye y ejecuta
  completo `notebooks/_construir_01_planteamiento.py`; las cifras salen de `backend/torre/radar/planteamiento.py`.
  Ecuaciones en `ECUACIONES.md` §1-ter; 6 pruebas en `tests/test_planteamiento.py`.
  - **Variables:** 17 en total, con fuente, periodo con dato y porcentaje de huecos. 9 miden presión, 3 capacidad,
    2 comunidad y 3 son huecos declarados (afluencia y las dos derramas).
  - **Actores** con una cifra medida cada uno: comunidades de los 5 lugares (229,247 habitantes), negocios turísticos
    en sus localidades (1,966), Tren Maya (58,086 bajaron en Chetumal y Maya Ka'an en 2025), frontera con Belice
    (653,306 cruces en 2025), INAH (77,645 visitantes en 2025 en las 4 zonas), SITUR-Q (12 indicadores) y DataTur
    (7 centros del norte). Falta el visitante como persona: entra en la Fase 8.
  - **Relación central, medida con cuotas y el índice de Herfindahl-Hirschman:**

    | Dimensión | Unidad más grande | $HHI^*$ | Cuota de los 5 lugares | Razón contra su población |
    |---|---|---:|---:|---:|
    | Llegadas en avión (2024) | Cancún, 92.5 % | 0.811 | 1.4 % | 0.11 |
    | Cuartos de hotel (jul-2026) | Riviera Maya, 42.4 % | 0.219 | 1.7 % | 0.14 |
    | Visitantes INAH (2025) | Tulum, 54.2 % | 0.276 | 4.1 % | 0.33 |
    | Negocios turísticos (DENUE) | Benito Juárez, 38.7 % | 0.133 | 14.4 % | 1.17 |
    | Población (2020) | Benito Juárez, 49.1 % | 0.225 | 12.3 % | 1.00 |

    Los negocios siguen a la población; los visitantes, no.

### 4. Cómo se suman los cuartos de SITUR-Q (hallazgo del notebook)
SITUR-Q publica zonas (Riviera Maya, Grand Costa Maya), destinos "miembro" dentro de ellas y una "zona especial"
(Caribe Mexicano). Se comprobó si una zona es la suma de sus miembros, con los cuartos de julio de 2026:
- Grand Costa Maya: 4,360 contra 4,315 de Chetumal + Bacalar + Mahahual (45 de diferencia).
- Riviera Maya: 59,632 contra 22,923 de Playa del Carmen + Tulum (**36,709 de diferencia**): la zona incluye lugares
  que no se publican por separado.

**Decisión:** el total estatal suma **destinos + zonas** (140,664 cuartos en julio de 2026), sin miembros y sin
"Caribe Mexicano", que no dice qué contiene (`NIVEL_ESTATAL` en `planteamiento.py`; prueba
`test_zonas_no_son_suma_de_miembros`). **Opción descartada:** sumar destinos + miembros; perdería 36,709 cuartos de la
Riviera Maya. **Consecuencia:** la página compara cuartos por hotel de cada unidad (un cociente), que no depende de esta
suma; el Radar (Fase 4) usará este mismo total.

## Estado de la fase
Los tres entregables de la Fase 3 están listos: tabla de criterios, notebook de planteamiento y tratamiento del sur. La
fase queda **lista para la revisión de Brandon**. La Fase 4 empieza con dos decisiones suyas: los pesos del índice de
presión y los cortes entre tranquilo, concurrido y saturado.
