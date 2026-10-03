# 08 — A1 Radar: índice de presión, estados y predicción (Fase 4) · CERRADA

> **Estado actualizado el 02-oct-2026:** Brandon dio el visto bueno y la fase quedó cerrada (`OBJETIVO.md`, A.8).

Autor: **Brandon Uriel García Sánchez** · 28-sep-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Qué responde el Radar
**¿Dónde hay presión y dónde hay espacio?** Para cada lugar y cada mes, un **índice de presión turística** (IPT) de 0 a
1 y un estado en palabras de todos los días: **tranquilo, concurrido o saturado**. Además, **qué estado se espera**
en los meses siguientes, con un modelo de aprendizaje de máquina y una cadena de Markov.

## Decisiones de Brandon (28-sep-2026)

### 1. Pesos del índice: iguales, con análisis de sensibilidad
Cada variable del índice pesa lo mismo. Después se mueve cada peso ±50 % y se reporta qué lugares cambian de estado.
- **Evidencia que motivó la pregunta:** en 2025–2026 el sur solo tiene 4 series mensuales medidas (Tren Maya, cruces de
  Belice, visitantes a zonas arqueológicas y cuartos de hotel); el norte, además, tiene ocupación semanal de DataTur
  (Cancún promedia 74.2 % en 239 semanas).
- **Por qué:** es fácil de defender ante el jurado y no premia al norte por tener más series.
- **Opciones descartadas:**
  - *Componentes principales:* pesos objetivos, pero difíciles de explicar y poco estables con 19 meses de datos del sur.
  - *Criterio del equipo:* subjetivo; cada número habría que justificarlo.

### 2. Cortes entre estados: percentiles comunes a todo el estado
Los mismos cortes para todos los lugares, sacados de todos los datos del estado juntos. Propuesta inicial: debajo de la
mediana (p50) = tranquilo; entre p50 y p90 = concurrido; arriba de p90 = saturado. Se muestra qué pasa si se mueven.
- **Por qué:** el norte y el sur quedan en la misma escala. Un lugar que nunca se llena no sale "saturado" solo por
  compararse contra sí mismo.
- **Opciones descartadas:**
  - *Terciles de cada lugar:* todo lugar saldría "saturado" un tercio del tiempo aunque nunca se llene (Cozumel promedia
    53 % de ocupación semanal).
  - *Grupos k-means:* los grupos pueden no significar tranquilo o saturado, y cambian al agregar datos.

### 3. Inferir los estados futuros con aprendizaje de máquina
Con los datos que existen, un modelo predice el estado del mes siguiente (palabras de Brandon: "con los datos que tenemos
inferimos los futuros haciendo ML"). Encaja en el plan (Parte B.2): un **clasificador** (logística, Random Forest y
Gradient Boosting, comparados con validación temporal y F1-macro) y una **cadena de Markov** para 1 a 8 semanas en el
norte. El pronóstico de niveles a 1–12 meses sigue siendo de la Fase 5 (A3); el Radar predice **estados**, no cantidades.

### 4. Escala de las variables: mín–máx (29-sep-2026)
$z=(x-\min)/(\max-\min)$, con mínimo y máximo comunes a todo el estado (la ecuación del plan).
- **Evidencia presentada antes de decidir:** en la escala mín–máx, el mes típico (la mediana) de visitantes INAH por
  mil habitantes cae en 0.02, el de Tren Maya en 0.06, el de cruceros en 0.11, el de ocupación en 0.70 y el de Belice en
  0.74.
- **Opciones descartadas:**
  - *Percentil común:* compara mejor variables con colas largas, pero pierde las proporciones.
  - *Mín–máx sobre logaritmo:* más difícil de explicar.

### 5. Corrección tras la prueba de validez: opción D (29-sep-2026)
Con mín–máx y solo SITUR-Q, el índice **falló la prueba de validez**:
- Cancún salía "tranquilo" en julio de 2026 (IPT 0.025), porque SITUR-Q dejó de publicar ocupación en 2025. Para ese
  mes DataTur marca 68.8 %.
- Chetumal (0.57) salía más presionado que Cancún (0.27) en 2024, por los cruces de Belice.

Se compararon cuatro variantes con datos reales, con el IPT promedio de 2025–2026 (`comparar_escalas`, exploración):

| Variante | Cancún | Isla Mujeres | Chetumal | Ruta del sur | Problema |
|---|---:|---:|---:|---:|---|
| A. Mín–máx, solo SITUR-Q | 0.02 | sin dato | 0.39 | 0.14 | El norte "desaparece" en 2025 |
| B. + ocupación DataTur | 0.28 | 0.45 | 0.39 | 0.14 | Chetumal arriba de Cancún por Belice |
| C. Percentil + DataTur | 0.44 | 0.25 | 0.48 | 0.71 | La ruta arriba de Cancún; Cozumel bajo |
| **D. B sin componentes de un solo lugar** | **0.28** | **0.45** | **0.05** | **0.14** | Quiebre de 2025 (abajo) |

**Decisión de Brandon: opción D.** Tiene tres partes:
- La ocupación de los 4 lugares que DataTur mide (Cancún, Playa del Carmen, Cozumel e Isla Mujeres) viene de DataTur en
  toda su historia (2022–2026).
- Un componente entra al índice solo si lo tienen al menos 2 lugares. Así sale Belice, que solo tiene Chetumal y se
  comparaba contra sí mismo. Belice sigue en el panel y en la página.
- Se conserva la escala mín–máx.

### 6. Corrección del panel: la ocupación no se suma (29-sep-2026)
El indicador `ocupacion_hotelera` de SITUR-Q trae tres filas por mes: cuartos-noche disponibles, cuartos-noche ocupados
y el porcentaje. La primera versión del panel las sumaba, y la "ocupación" llegaba a 2,560,068.

Ahora el porcentaje se recalcula como ocupados ÷ disponibles (Chetumal 2024 = 58.0 %, igual que la tabla de criterios).
El panel se detiene si una variable trae dos filas en el mismo mes. Lo vigila la prueba `test_ocupacion_no_suma_filas`.

### 7. Para predecir se usa el índice comparable (29-sep-2026)
Cada lugar usa solo las medidas que tiene en su último mes publicado, y solo en los meses en que las tiene todas. Un
cambio de estado es entonces siempre un cambio real.
- **Evidencia:** el quiebre de 2025 (Chetumal 0.54 → 0.05).
- **Opciones descartadas:**
  - *Entrenar solo con 2025–2026:* 19 meses por lugar.
  - *Entrenar todo con una bandera "tiene ocupación":* el modelo aprendería el cambio de datos en vez de la presión.
- **Costo:** algunos lugares empiezan cuando llegó el Tren Maya (Chetumal, dic-2024; Cancún, ene-2024).

### 8. El Radar publica el índice comparable (29-sep-2026)
Un solo índice para el estado de hoy y para la predicción, con cortes p50 = 0.228 y p90 = 0.752.
- **Por qué:** con dos índices, Cancún salía "tranquilo" en uno y "concurrido" en el otro en el mismo mes (jul-2026).
- **Opción descartada:** publicar el índice de la pieza 2, que tiene toda la historia pero también el quiebre.
- La pieza 2 (`radar_estado.parquet`) queda como paso intermedio: de ahí salen las $z$ y la sensibilidad.

### 9. Modelo elegido: Random Forest (29-sep-2026)
Backtesting con origen móvil: 12 reentrenamientos, 156 predicciones y 23 cambios reales de estado.

| Modelo | Aciertos | Cambios anticipados | Falsas alarmas | F1-macro |
|---|---:|---:|---:|---:|
| Persistencia ("igual que este mes") | 133 | 0 | 0 | 0.808 |
| Regresión logística | 133 | 3 | 3 | 0.834 |
| **Random Forest** | **136** | **7** | **4** | 0.796 |
| Gradient Boosting | 132 | 8 | 9 | 0.718 |

**Criterio de Brandon:** el que más acierta y más cambios anticipa, porque la regla anti-colapso necesita anticipar.
**Opción descartada:** elegir por F1-macro, la métrica del plan, que daba la regresión logística; esa acierta lo mismo que
la persistencia. **Lectura honesta para el coloquio:** el estado se repite el 85 % de los meses, así que el
aprendizaje de máquina agrega poco (+3 aciertos de 156). Su valor está en los 7 cambios que anticipa.

### 10. Cadena de Markov: semanal y solo el norte (29-sep-2026)
Con los 7 centros de DataTur (239 semanas cada uno), estados por percentiles comunes de la ocupación semanal
(p50 = 71.2 %, p90 = 85.9 %) y riesgo de saturarse a 1–8 semanas.
- **Por qué:** es lo que marca el plan (Markov en semanas, el Pronóstico en meses) y no repite al clasificador mensual.
  Sirve a la campaña: cuando el norte se va a saturar, es el momento de ofrecerle el sur a ese turista.
- **Opciones descartadas:**
  - *Mensual para todos:* repetía al clasificador y se encimaba con la Fase 5.
  - *Las dos:* más trabajo, con una parte duplicada.
- **Limitación declarada:** el sur no tiene datos semanales. La cadena cubre solo la referencia del norte.

## Actualización tras la auditoría (29-sep-2026)
La auditoría de las Fases 1–4 (`09-auditoria-fases-1-4.md`) encontró tres puntos del plan sin cubrir. Brandon decidió:

### 11. Se agrega "llegadas por cuarto"; la densidad de oferta no entra
$(\text{Tren Maya}+\text{cruceristas})\div\text{cuartos}$ del lugar ese mes. La densidad de oferta (negocios DENUE por
mil habitantes) no entra porque es un solo corte en el tiempo y no señala meses.

**Limitación que se le presentó a Brandon antes de fijarlo:**
- Con cruceros, el componente queda dominado por los puertos: Mahahual llega a 432 cruceristas por cuarto al mes y el
  mes típico cae en 0.003 de la escala.
- Con solo tren, el mes típico caía en 0.12.

**Brandon decidió mantener tren + cruceros**, y así se declara.

### 12. Clustering de los centros del país: k = 2
Clustering jerárquico (Ward) de los 55 centros de DataTur con los 55 meses completos, por su perfil de ocupación de
12 meses. El número de grupos sale de la silueta ($k=2$, 0.450).
- **Grupo 1:** playas muy ocupadas (64.5 %: Cancún, Riviera Maya, Playacar, Akumal, Playa del Carmen, Los Cabos).
- **Grupo 2:** el resto (41.1 %, con Cozumel e Isla Mujeres).
- **Opciones descartadas:** $k=7$ (más detalle, silueta 0.317) y $k=3$.

### 13. La diferencia entre DataTur y SITUR-Q se declara, no se ajusta
Cozumel −14.5, Isla Mujeres −19.3 y Cancún −1.6 puntos. El error va en sentido conservador (el norte se ve menos
lleno). **Opción descartada:** calibrar DataTur con SITUR-Q, que convertiría la ocupación 2025–2026 del norte en
estimación.

### 14. El criterio de elección del modelo da ahora la regresión logística
Con "llegadas por cuarto", el criterio de Brandon (más aciertos y, a igualdad, más cambios anticipados) da la regresión
logística: 130 de 156 y 8 de 30 cambios, contra 130 y 6 de Random Forest y 126 de la persistencia. Se respeta el
criterio, no el nombre del modelo. El código lo elige solo y la página lee el nombre del modelo de los datos.

### Cifras vigentes del Radar (tras la auditoría)

**Índice:**
- Cortes p50 = 0.258 y p90 = 0.766 (antes 0.308 / 0.763).
- Cancún jul-2026: IPT 0.1931, tranquilo (antes 0.2571).
- Sensibilidad: entre 0.6 % y 6.0 % cambian de estado.

**Índice comparable (lo que publica el Radar):** cortes p50 = 0.186 y p90 = 0.756.

**Julio de 2026, índice comparable:**
- Concurridos: Mahahual 0.731, Isla Mujeres 0.510, Bacalar 0.314, Holbox 0.228, Cancún 0.193 y Cozumel 0.191.
- Tranquilos: Playa del Carmen 0.160, Tulum 0.145 y los 5 lugares (Ruta 0.129, Chetumal 0.025, Oxtankah 0.020,
  Maya Ka'an 0.009).
- Laguna Milagros: "sin dato oficial".

**Modelo:** regresión logística, 130 de 156 contra 126 de la persistencia, con 8 de 30 cambios anticipados y
4 falsas alarmas.

**Sesgo:**
- 5 lugares: 2 cambios en 48 casos, ninguno anticipado.
- Resto del estado: 8 de 28 cambios anticipados.

**Predicción ago-2026:** los 5 lugares siguen tranquilos (0.98–1.00). Mahahual, con 0.40 de probabilidad de saturarse.

**Markov:** sin cambios (no usa el índice).

## Plan de piezas (una a la vez; Brandon corre cada una)
1. **Panel mensual** (`backend/torre/radar/panel.py`): una tabla lugar × mes con las variables candidatas y qué tiene
   dato y qué no.
2. **Índice y estados** (`indice.py`): normalización mín–máx común, pesos iguales sobre las variables con dato,
   cortes p50/p90 y sensibilidad.
3. **Predicción** (`prediccion.py`): clasificador del estado del mes siguiente y cadena de Markov semanal del norte.
4. Notebook `02_radar`, ecuaciones en `ECUACIONES.md` §2, pruebas y la sección del Radar en la página (clave `radar`).

## Avance
- ✅ **Pieza 1 — panel mensual** (`backend/torre/radar/panel.py` → `datos/gold/radar_panel_mensual.parquet`): 825 filas
  = 15 lugares × 55 meses (ene-2022 a jul-2026). Los 5 lugares + 10 destinos de SITUR-Q del resto del estado, que dan la
  escala común de los percentiles. Pruebas: `tests/test_radar_panel.py` (5, en verde; 60 en todo el proyecto).

  **Hallazgo: la serie "zonas arqueológicas" de SITUR-Q es el dato del INAH agrupado por destino.** Cuadra exacto en
  2025:
  - Chetumal 39,459 = Oxtankah 11,017 + Kohunlich 21,850 + Dzibanché 6,592.
  - Bacalar 275,225 = Chacchoben 237,039 + Ichkabal 38,186.
  - Tulum 1,223,258 = Tulum 1,031,443 + Cobá 191,815.

  **Decisión:** los visitantes se toman del INAH zona por zona y cada zona va a un solo lugar (`ZONA_A_LUGAR`). La
  prueba `test_inah_sin_doble_conteo` confirma que la suma del panel es igual a la del INAH. **Opción descartada:**
  usar las dos series, que contaría dos veces a los mismos visitantes. Ichkabal va a la Ruta del sur y no a Bacalar,
  como en SITUR-Q, por la decisión de regiones. Chakanbakán se excluye: registra 0 visitantes en todos sus meses
  (2016–2023) y el código se detiene si algún día registra alguno.

  **Qué variables se quedan fuera y por qué:**
  - *Avión:* un aeropuerto no es un destino, y la serie termina en 2024.
  - *Zonas de SITUR-Q:* suman lugares que ya están en el panel.

  **Cobertura (meses con dato de 55):**

  | Lugar | Tren Maya | Cruceros | Belice | Visitantes INAH | Ocupación | Cuartos |
  |---|---:|---:|---:|---:|---:|---:|
  | Chetumal | 20 | — | 54 | — | 36 | 55 |
  | Bahía Calderitas–Oxtankah | — | — | — | 55 | — | — |
  | Ruta arqueológica del sur | — | — | — | 55 | — | — |
  | Maya Ka'an + Kantemó | 23 | — | — | — | 12 | 55 |
  | Laguna Milagros–Xul-Ha | — | — | — | — | — | — |
  | *Cancún (referencia)* | 31 | — | — | 55 | 36 | 55 |
  | *Tulum (referencia)* | 23 | — | — | 55 | 36 | 55 |

  **Lo que esto significa para la pieza 2:** los 5 lugares **no comparten ninguna variable**. Con pesos iguales, el
  índice de cada lugar será el promedio de las variables que sí tiene, y en pantalla se dirá con qué variables se
  calculó. La Laguna Milagros no tiene ninguna serie: el Radar la mostrará como "sin dato oficial", no como
  "tranquila".
- ✅ **Pieza 2 — índice y estados** *(cifras de antes de la auditoría; las vigentes están arriba)*
  (`backend/torre/radar/indice.py` → `datos/gold/radar_estado.parquet`). Ecuaciones y
  ejemplo a mano (Cancún, jul-2026: IPT 0.2571, tranquilo) en `ECUACIONES.md` §2.1. Pruebas en
  `tests/test_radar_indice.py`: 6, en verde; 67 en todo el proyecto.
  - **Cortes comunes:** p50 = 0.308 y p90 = 0.763. Con ellos, 351 lugar-mes salen tranquilos, 282 concurridos y
    70 saturados.
  - **Julio de 2026:**
    - Concurridos: Mahahual (0.728, por los cruceros), Isla Mujeres (0.510), Bacalar (0.467) y Holbox (0.456).
    - Tranquilos: Cancún (0.257), Tulum (0.218), Playa del Carmen (0.213) y Cozumel (0.181).
    - Los 5 lugares, tranquilos: Ruta 0.129, Chetumal 0.045, Oxtankah 0.020 y Maya Ka'an 0.015.
    - Laguna Milagros: "sin dato oficial".
  - **Sensibilidad:** con cada peso a 0.5 o 1.5 cambia de estado entre el 0 % y el 8.4 % de los lugar-mes. La
    ocupación es la que más mueve el resultado.
  - **Limitación declarada, el quiebre de 2025:** los lugares cuya ocupación venía de SITUR-Q la pierden en 2025.
    Chetumal pasa de 0.54 a 0.05, Puerto Morelos de 0.51 a 0.09 y Maya Ka'an de 0.25 a 0.02. Es un cambio en los datos
    disponibles, no una caída real. La pieza 3 lo tiene que tratar: un modelo entrenado con 2022–2024 aprendería
    estados que en 2025 cambian por falta de dato.
- ✅ **Pieza 3 — predicción** *(cifras de antes de la auditoría; las vigentes están arriba)*
  (`backend/torre/radar/prediccion.py`). Salidas en `datos/gold/`:
  `radar_indice_comparable.parquet` (lo que publica el Radar), `radar_modelos.parquet` y `radar_prediccion.parquet`.
  Ecuaciones, matriz de confusión y F1 resuelto a mano en `ECUACIONES.md` §2.2. Pruebas: `tests/test_radar_prediccion.py`
  (5); 72 en todo el proyecto.
  - **Qué pesa en el modelo:** el índice del mes (0.37), los dos meses anteriores (0.25 y 0.21), el cambio (0.07),
    ser uno de los 5 lugares (0.06) y la temporada (0.04).
  - **Predicción para agosto de 2026:** los 5 lugares siguen tranquilos (probabilidad 0.99–1.00; Laguna Milagros, sin
    dato). Mahahual podría pasar a saturado (0.54). Costa Mujeres no se predice porque su dato terminó en 2024.
- ✅ **Pieza 3b — cadena de Markov** (`backend/torre/radar/markov.py` → `datos/gold/radar_markov_matriz.parquet` y
  `radar_markov_riesgo.parquet`). Se contaron 1,666 transiciones semanales. Desde "saturado", el 72.6 % de las veces la
  semana siguiente sigue saturada. A largo plazo el norte pasa el 9.8 % de las semanas saturado.
  - **Backtest (52 semanas):** mejor Brier que la persistencia a 1, 4 y 8 semanas (0.200 contra 0.225; 0.389 contra
    0.484; 0.490 contra 0.676). En exactitud del estado más probable no le gana a 4 y 8 semanas: su valor es la
    probabilidad.
  - **Semana del 27-jul-2026:** Playacar está concurrida (81.7 %), con 13.9 % de riesgo de saturarse en 5 semanas.
  - Ecuaciones y ejemplo a mano en `ECUACIONES.md` §2.3. Pruebas: `tests/test_radar_markov.py` (5); 77 en todo el
    proyecto.
- ✅ **Pieza 4 — notebook y página.**
  - **Notebook `notebooks/02_radar.ipynb`:** lo construye y ejecuta completo `notebooks/_construir_02_radar.py`. Genera la
    figura `docs/ejecutivo/figuras/f08_radar.png`.
  - **Página, sección `#radar` "¿Dónde hay espacio hoy?":** se dibuja con `dibujarRadar` en `frontend/app.js` y sus
    datos salen de `radar()` en `datos_pagina.py`. Muestra los 5 lugares con su barra, su estado y el estado estimado
    del mes siguiente. Cancún, Playa del Carmen y Tulum van como "solo referencia" (regla de oro 9) y se agrega el
    riesgo semanal de saturación de Cancún (Markov).
  - **Semáforo en cada ficha** del mapa 3D.
  - **Pruebas en `tests/test_pagina.py`:** solo los 5 lugares y las 3 referencias; Laguna "sin dato oficial"; la
    predicción lleva `_est`. 79 pruebas en todo el proyecto.
  - Verificado en 1440 y 390 px, sin errores ni desplazamiento horizontal.
- ✅ **Auditoría** (`09-auditoria-fases-1-4.md`): se agregaron llegadas por cuarto, el clustering
  (`backend/torre/radar/clustering.py`, `tests/test_radar_clustering.py`), el análisis de sesgo (`sesgo()` →
  `datos/gold/radar_sesgo.parquet`) y la prueba de cifras de los documentos (`tests/test_documentos.py`).
  - Lo que falta para cerrar la fase: el visto bueno de Brandon.
