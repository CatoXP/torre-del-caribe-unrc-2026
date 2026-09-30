# Ecuaciones y "cómo lo resolví"

Autor: **Brandon Uriel García Sánchez** · Torre del Caribe (Problema Prototípico 5° · Quintana Roo)

Regla del proyecto (ver `OBJETIVO.md` A.7 y `CLAUDE.md` §1): todo cálculo, modelo o indicador se documenta en
**cinco partes**:
1. **Ecuación**, con cada símbolo definido.
2. **Supuestos**.
3. **Cómo se resolvió**, paso a paso.
4. **Ejemplo resuelto a mano** con números reales.
5. **Dónde está en el código**.

Estado de cada sección:
- ✅ **completa**: la ecuación ya se aplicó con datos reales.
- 🕓 **prevista**: la fórmula está definida y se completa contigo cuando llegue su fase.

---

## 1. Selección de regiones con visitantes del INAH ✅

**Datos:** DataTur `BdINAH.zip` → `Bd_INAH.xlsx`, descargado el 27-sep-2026. Columnas usadas: `Estado`, `Nombre`,
`Año`, `id_mes`, `Tipo` (Nacional / Extranjero) y `Visitantes`.

### 1.1 Ecuaciones
**Visitantes anuales del sitio** $s$ en el año $a$:
$$V_{s,a}=\sum_{m=1}^{12}\ \sum_{t\in\{\text{nac},\text{ext}\}} v_{s,a,m,t}$$
donde $v_{s,a,m,t}$ son las personas registradas en el sitio $s$, año $a$, mes $m$ y tipo de visitante $t$.

**Visitantes del periodo enero–julio** (así se comparan 2026 y 2025 con los mismos meses):
$$V^{\,1..7}_{s,a}=\sum_{m=1}^{7}\ \sum_{t} v_{s,a,m,t}$$

**Variación interanual del periodo** (en %):
$$\Delta\%_s=\left(\frac{V^{\,1..7}_{s,2026}}{V^{\,1..7}_{s,2025}}-1\right)\times 100$$

**Capacidad probada sin usar** (qué fracción de su máximo reciente no se está usando):
$$K_s = 1-\frac{V_{s,2025}}{V_{s,2019}}$$

**Proporción de extranjeros**:
$$E_{s,a}=\frac{\sum_m v_{s,a,m,\text{ext}}}{V_{s,a}}$$

### 1.2 Supuestos
- Las visitas a la zona arqueológica sirven como **indicador de presión turística** del destino; no son el total de
  turistas del destino.
- 2019 es el **año de referencia de capacidad**: es el último año completo antes de la pandemia, y en él el sitio
  demostró que podía recibir ese volumen.
- Un sitio **cerrado** no cuenta como "sin demanda". Muyil estuvo cerrada del 4-jun-2024 al 10-feb-2026 (INAH), por
  eso su $V_{2025}=0$ se interpreta como cierre, no como falta de interés. (Muyil se retiró de las regiones el
  28-sep-2026 precisamente por ese cierre y por colindar con Tulum.)
- Se comparan **los mismos meses** (ene–jul) para que la estacionalidad no distorsione la variación.

### 1.3 Cómo se resolvió
1. Se leyó el Excel oficial y se filtró `Estado = "Quintana Roo"` (3,609 filas).
2. Se sumaron los visitantes por sitio y año (ecuación $V_{s,a}$) y por sitio en ene–jul (ecuación $V^{1..7}_{s,a}$).
3. Se calcularon $\Delta\%$, $K_s$ y $E_{s,a}$ para cada sitio.
4. Se cruzó el resultado con las noticias de 2026 (sargazo, cierres, saturación) y con los criterios D.1 de
   `docs/regiones/REGIONES.md`.
5. Brandon eligió las regiones finales (decisión `docs/decisiones/01-regiones.md`).

### 1.4 Ejemplos resueltos a mano (números reales)
**Tulum (caída en 2026):**
$$\Delta\%_{\text{Tulum}}=\left(\frac{476{,}247}{692{,}946}-1\right)\times100=(0.6873-1)\times100=-31.3\%$$

**Kohunlich (capacidad probada sin usar):**
$$K_{\text{Kohunlich}}=1-\frac{21{,}850}{42{,}813}=1-0.5104=0.490\ \Rightarrow\ 49.0\%$$
Lectura: en 2025, Kohunlich recibió la mitad de lo que ya demostró poder recibir en 2019.
*(Hasta el 28-sep-2026 el ejemplo era Cobá, $K=0.744$; Cobá se retiró de las regiones por pertenecer al municipio de
Tulum. El método no cambia.)*

**Ruta arqueológica del sur contra Tulum (2025):**
$$V_{\text{ruta}}=21{,}850+6{,}592+38{,}186=66{,}628\qquad \frac{V_{\text{Tulum}}}{V_{\text{ruta}}}=\frac{1{,}031{,}443}{66{,}628}=15.5$$
Lectura: Tulum recibió 15.5 veces más visitantes que las tres zonas del sur juntas.

**Kohunlich (crecimiento en 2026):**
$$\Delta\%_{\text{Kohunlich}}=\left(\frac{14{,}164}{12{,}480}-1\right)\times100=+13.5\%$$

### 1.5 Dónde está en el código
Hoy es un cálculo exploratorio hecho en la sesión del 27-sep-2026. En la **Fase 1** pasa a
`backend/torre/base/ingesta_datatur.py` (lectura de `BdINAH`) y en la **Fase 3** al notebook
`notebooks/01_planteamiento.ipynb`, con una prueba de realidad que reproduce $-31.3\%$ para Tulum.

---

## 1-bis. Tabla de criterios de las 5 regiones (Fase 3) ✅

### Ecuaciones
- **Ocupación hotelera anual** de la región $d$ (criterio 3), con la suma de los 12 meses:
  $$O_{d,2024}=\frac{\sum_{m=1}^{12}\text{cuartos ocupados}_{d,m}}{\sum_{m=1}^{12}\text{cuartos disponibles}_{d,m}}\times100$$
- **Visitantes por residente** (criterio 3): $R_d=\dfrac{V_{d,2025}}{P_d}$, donde $V_{d,2025}$ son los visitantes INAH de las
  zonas de la región en 2025 y $P_d$ es la población 2020 de sus localidades (Censo, por localidad).
- **Negocios turísticos por cada mil habitantes** (criterio 3): $N_d=\dfrac{\#\text{negocios turísticos}_d}{P_d}\times1000$.
- **Viviendas sin servicio** (criterio 4): $S_d=\left(1-\dfrac{\sum \text{viviendas con agua}}{\sum \text{viviendas habitadas}}\right)\times100$,
  solo con las localidades cuyo dato no reservó el INEGI (lo mismo para drenaje).
- **Meses seguidos abierta** (criterio 2): $A_z=\max\{k: v_{z,T}>0,\dots,v_{z,T-k+1}>0\}$, contando hacia atrás desde el
  último mes publicado $T$. La región toma la zona menos abierta, $A_d=\min_z A_z$, y **pasa si** $A_d\ge12$ y no hubo
  meses en cero en 2026 (regla de Brandon, 28-sep-2026).

### Supuestos
- Ocupación: 2024 es el último año con los 12 meses publicados en SITUR-Q para el sur. Se usa el mismo año y la misma
  fuente para todas las regiones, así la comparación es justa.
- Un mes con 0 visitantes (nacionales + extranjeros) es un mes cerrado.
- Sargazo y fragilidad ecológica no tienen serie oficial: son evidencia documental con su fuente
  (`docs/regiones/REGIONES.md`) y así se marcan.

### Cómo se resolvió
Conteo y cocientes sobre las tablas limpias; no hay estimación ni parámetros. Pasos:
1. Filtrar cada fuente con las localidades o zonas de la región.
2. Sumar antes de dividir.
3. Guardar la tabla en `datos/gold/criterios_regiones.parquet`.

### Ejemplos resueltos a mano (números reales)
- **Ocupación de Chetumal 2024:** $O=\dfrac{458{,}696}{791{,}016}\times100=57.99\approx58.0\%$. Es decir, 4 de cada 10
  cuartos vacíos. Referencias: Cancún 76.1 %, Playa del Carmen 76.9 %, Tulum 73.7 %.
- **Visitantes por residente en la ruta sur:** $R=\dfrac{21{,}850+6{,}592+38{,}186}{3{,}699+1{,}436+963}=\dfrac{66{,}628}{6{,}098}=10.93$.
  Tulum: $\dfrac{1{,}031{,}443}{33{,}374}=30.91$. La ruta recibe un tercio de la presión por residente de Tulum, así que
  también necesitará tope.
- **Negocios por mil en Calderitas:** $N=\dfrac{70}{5{,}551}\times1000=12.6$.
- **Meses seguidos abierta de Dzibanché:** su último mes en cero fue enero de 2025. De febrero de 2025 a julio de 2026
  son $11+7=18\ge12$ → **pasa**. Muyil reabrió en febrero de 2026, así que solo lleva 6 meses → no pasaría.

### Dónde está en el código
`backend/torre/radar/criterios.py` → `calcular_criterios()`, `_ocupacion_2024()` y `_meses_abierta()`. Pruebas:
`tests/test_criterios.py`.

---

## 1-ter. Concentración del turismo en Quintana Roo (Fase 3, planteamiento) ✅

### Ecuaciones
Para una dimensión (llegadas en avión, cuartos, visitantes INAH, negocios o población) repartida entre $N$ unidades
(aeropuertos, destinos, sitios o municipios) con valores $x_1,\dots,x_N$:
- **Cuota** de la unidad $i$: $s_i=\dfrac{x_i}{\sum_{j=1}^{N}x_j}$, con $0\le s_i\le1$ y $\sum_i s_i=1$.
- **Índice de Herfindahl-Hirschman**: $HHI=\sum_{i=1}^{N}s_i^2$. Vale $1/N$ si todas pesan igual y 1 si una sola unidad
  lo tiene todo.
- **HHI normalizado** (para comparar dimensiones con distinto $N$): $HHI^*=\dfrac{HHI-1/N}{1-1/N}$, entre 0 (reparto
  parejo) y 1 (todo en una unidad).
- **Cuota de los 5 lugares**: $s_{5}=\dfrac{\sum_{i\in\text{5 lugares}}x_i}{\sum_j x_j}$, contada en las localidades del
  Censo de cada región (misma lista que los criterios y la página).
- **Razón contra la población**: $\rho=\dfrac{s_5^{\text{dimensión}}}{s_5^{\text{población}}}$. Si $\rho=1$, los 5 lugares
  tienen de esa dimensión la misma parte que de habitantes; si $\rho<1$, menos.

### Supuestos
- Las unidades no se enciman. En los cuartos de SITUR-Q se suman solo **destinos y zonas**: una zona no es la suma de
  sus miembros publicados (Riviera Maya, julio de 2026: 59,632 cuartos contra 22,923 de Playa del Carmen + Tulum) y
  "Caribe Mexicano" no dice qué contiene, así que queda fuera.
- Cada dimensión usa su último periodo completo: avión 2024 (regla 6 de Silver), cuartos julio de 2026, INAH 2025,
  negocios el corte del DENUE y población 2020.
- $\rho$ es una comparación, no una meta: nada dice que el turismo deba repartirse según la población.

### Cómo se resolvió
Conteos, sumas y cocientes sobre las tablas limpias; no hay parámetros que estimar. Pasos:
1. Agrupar la dimensión por unidad.
2. Dividir cada valor entre el total.
3. Elevar al cuadrado y sumar.

### Ejemplo resuelto a mano (llegadas en avión, 2024)
| Aeropuerto | Pasajeros $x_i$ | Cuota $s_i$ | $s_i^2$ |
|---|---:|---:|---:|
| Cancún | 14,769,302 | 0.92544 | 0.856433 |
| Tulum | 620,384 | 0.03887 | 0.001511 |
| Cozumel | 352,067 | 0.02206 | 0.000487 |
| Chetumal | 217,524 | 0.01363 | 0.000186 |
| **Total** | **15,959,277** | **1** | **0.858617** |

$HHI=0.8586$; $\;HHI^*=\dfrac{0.8586-0.25}{1-0.25}=0.811$. Casi todo el tráfico aéreo entra por una sola puerta.
Los 5 lugares (solo Chetumal tiene aeropuerto) tienen $s_5=0.0136$ (1.4 %), y la razón contra la población es
$\rho=\dfrac{1.4}{12.3}=0.11$: su parte de las llegadas aéreas es la novena parte de su parte de la población.

**Resultado completo:**

| Dimensión | Unidad más grande (cuota) | $HHI^*$ | Cuota de los 5 lugares | $\rho$ |
|---|---|---:|---:|---:|
| Llegadas en avión (2024) | Cancún (92.5 %) | 0.811 | 1.4 % | 0.11 |
| Cuartos de hotel (jul-2026) | Riviera Maya (42.4 %) | 0.219 | 1.7 % | 0.14 |
| Visitantes a sitios del INAH (2025) | Z.A. de Tulum (54.2 %) | 0.276 | 4.1 % | 0.33 |
| Negocios turísticos (DENUE) | Benito Juárez (38.7 %) | 0.133 | 14.4 % | 1.17 |
| Población (2020) | Benito Juárez (49.1 %) | 0.225 | 12.3 % | 1.00 |

Lectura: en los 5 lugares vive el 12.3 % de la gente del estado y está el 14.4 % de sus negocios turísticos, pero tienen
menos del 5 % de las llegadas en avión, de los cuartos de hotel y de los visitantes del INAH. Los negocios están en proporción a la gente que vive ahí; los
visitantes, no. Ojo: muchos de esos negocios (sobre todo restaurantes de Chetumal) atienden también a los residentes.

### Dónde está en el código
`backend/torre/radar/planteamiento.py` → `cuotas_y_hhi()`, `concentracion()` y `comprobar_zonas()`. Notebook:
`notebooks/01_planteamiento.ipynb`. Pruebas: `tests/test_planteamiento.py`.

---

## 2. A1 Radar (Fase 4) ✅

> **Actualizado tras la auditoría del 29-sep-2026** (`docs/decisiones/09-auditoria-fases-1-4.md`): se agregó el componente
> "llegadas por cuarto" que pedía el plan, se midió el sesgo y se agregó el clustering de centros del país (§2.4).

### 2.1 Índice de presión turística y estados ✅

**Ecuaciones** (lugar $d$, mes $t$, componente $k$):
- **Ocupación** (nunca se suman ni se promedian porcentajes):
  $O_{d,t}=100\cdot\dfrac{\sum_{\text{semanas o filas del mes}}\text{cuartos ocupados}}{\sum\text{cuartos disponibles}}$
- **Llegadas por mil habitantes:** $x_{k,d,t}=\dfrac{L_{k,d,t}}{P_d}\times1000$, con $L_k$ = personas que bajan del Tren
  Maya, cruceristas o visitantes INAH, y $P_d$ la población 2020 de las localidades del lugar.
- **Llegadas por cuarto** (agregado tras la auditoría; decisión de Brandon: tren + cruceros):
  $x_{\text{cuarto},d,t}=\dfrac{\text{Tren Maya}_{d,t}+\text{cruceristas}_{d,t}}{\text{cuartos}_{d,t}}$ (si no hay ni tren ni
  crucero ese mes, queda vacío, no 0).
- **Componentes que entran:** solo los que tienen dato en al menos 2 lugares: $\{k:\#\{d: x_{k,d,\cdot}\neq\varnothing\}\ge2\}$.
  Entran tren, cruceros e INAH por habitante, llegadas por cuarto y ocupación; sale cruces con Belice (solo Chetumal).
  La densidad de oferta (negocios por mil habitantes) no entra: es un solo corte en el tiempo y no puede señalar un mes.
- **Escala mín–máx común** (decisión de Brandon): $z_{k,d,t}=\dfrac{x_{k,d,t}-\min_{d',t'}x_{k}}{\max_{d',t'}x_{k}-\min_{d',t'}x_{k}}$,
  con mínimo y máximo de todos los lugares y meses juntos.
- **Índice con pesos iguales** sobre los componentes disponibles $A_{d,t}$:
  $IPT_{d,t}=\dfrac{\sum_{k\in A_{d,t}}w_k\,z_{k,d,t}}{\sum_{k\in A_{d,t}}w_k}$, con $w_k=1$. Si $A_{d,t}=\varnothing$ → "sin dato oficial".
- **Estados con percentiles comunes:** $u_{50}$ y $u_{90}$ = percentiles 50 y 90 del IPT de todos los lugares y meses:
  tranquilo si $IPT<u_{50}$; concurrido si $u_{50}\le IPT\le u_{90}$; saturado si $IPT>u_{90}$.
- **Sensibilidad:** para cada $k$, $w_k\in\{0.5,\,1.5\}$ con los demás en 1; se cuenta la parte de lugar-mes que cambia
  de estado.

**Supuestos:**
- Las llegadas por habitante miden la presión sobre la comunidad (1,000 visitantes pesan más en Nicolás Bravo que en
  Chetumal); las llegadas por cuarto, la presión sobre el hospedaje.
- Cada lugar usa una sola fuente de ocupación en toda su historia: DataTur (semanal, 2022–2026) para Cancún, Playa del
  Carmen, Cozumel e Isla Mujeres; SITUR-Q (mensual, hasta dic-2024) para los demás.
- Una semana de DataTur que cruza de mes cuenta en el mes de su lunes.

**Cómo se resolvió:** cálculo directo, sin parámetros estimados.
1. Armar el panel (`panel.py`).
2. Dividir las llegadas entre la población y entre los cuartos.
3. Escalar cada componente con su mínimo y máximo común.
4. Promediar lo disponible.
5. Sacar los percentiles 50 y 90 del índice y clasificar.

**Ejemplo resuelto a mano (Cancún, julio de 2026; 888,797 habitantes):**

| Componente | Dato | $x$ | mín | máx | $z$ |
|---|---:|---:|---:|---:|---:|
| Tren Maya | 22,316 personas | 25.1081 por mil | 0 | 505.2287 | $25.1081/505.2287=0.0497$ |
| INAH (El Rey) | 854 visitantes | 0.9608 por mil | 0 | 6,451.8787 | $0.0001$ |
| Llegadas por cuarto | 22,316 en tren | 0.4709 por cuarto | 0 | 432.0230 | $0.4709/432.0230=0.0011$ |
| Ocupación (DataTur) | — | 68.78 % | 17.97 | 88.40 | $(68.78-17.97)/(88.40-17.97)=0.7214$ |

$IPT=\dfrac{0.0497+0.0001+0.0011+0.7214}{4}=0.1931$. Como $0.1931<u_{50}=0.2577$, el estado es **tranquilo**
($u_{90}=0.7663$).

**Resultado (jul-2026):**
- Concurrido: Mahahual (0.731, cruceros), Isla Mujeres (0.510) y Bacalar (0.314).
- Tranquilo: Holbox (0.228), Cancún (0.193), Cozumel (0.191), Playa del Carmen (0.160) y Tulum (0.145).
- Los 5 lugares, tranquilos entre 0.009 y 0.129: Ruta 0.129, Chetumal 0.025, Oxtankah 0.020, Maya Ka'an 0.009.
- Laguna Milagros: "sin dato oficial".

**Sensibilidad:** con cada peso a 0.5 o 1.5 cambia de estado entre el 0.6 % y el 6.0 % de los lugar-mes. Lo que más mueve
el resultado es la ocupación (6.0 % con peso 1.5).

**Limitaciones declaradas:**
- **Quiebre de 2025:** los lugares cuya ocupación venía de SITUR-Q la pierden. No es que se vaciaran:
  - Chetumal: 0.54 en 2024 → 0.03 en 2025.
  - Puerto Morelos: 0.39 → 0.05.
  - Maya Ka'an: 0.23 → 0.01.

  Se trata con el índice comparable (§2.2).
- **Llegadas por cuarto quedan dominadas por los puertos de crucero.** Mahahual llega a 432 cruceristas por cuarto al
  mes (sus pasajeros no duermen en hoteles), y el mes típico cae en 0.003 de la escala. Para el resto del estado este
  componente casi siempre vale cerca de 0. Brandon decidió mantener tren + cruceros. La opción descartada, solo tren,
  dejaba el mes típico en 0.12 de la escala.
- **DataTur mide menos ocupación que SITUR-Q para el mismo lugar** (Cancún −1.6 puntos, Cozumel −14.5, Isla Mujeres
  −19.3). Va en el sentido conservador: el norte se ve menos lleno. Se declara, sin ajustar (auditoría §3.1).

**Dónde está en el código:** `backend/torre/radar/indice.py` → `componentes()`, `elegir_componentes()`, `minmax()`,
`ipt()`, `estados()` y `sensibilidad()`. Pruebas: `tests/test_radar_indice.py`.

### 2.2 Índice comparable y predicción del estado del mes siguiente ✅

**Ecuaciones:**
- **Índice comparable** (es el que publica el Radar, decisión de Brandon del 29-sep-2026). Sea $S_d$ el conjunto de medidas
  que el lugar $d$ tiene en su último mes publicado:
  $IPT^{c}_{d,t}=\dfrac1{|S_d|}\sum_{k\in S_d}z_{k,d,t}$, definido solo en los meses $t$ en que existen **todas** las
  medidas de $S_d$. Estados con percentiles comunes del índice comparable: $u_{50}=0.186$ y $u_{90}=0.756$.
- **Rasgos en el mes $t$:** $IPT^c_t$, $IPT^c_{t-1}$, $IPT^c_{t-2}$, el cambio $IPT^c_t-IPT^c_{t-1}$, el mes como círculo
  $\left(\sin\frac{2\pi m}{12},\cos\frac{2\pi m}{12}\right)$ y si es uno de los 5 lugares. **Objetivo:** el estado en $t+1$.
- **Línea base de persistencia:** $\hat y_{t+1}=y_t$.
- **Regresión logística multiclase:** $P(y=k\mid x)=\dfrac{e^{\beta_k^\top x}}{\sum_j e^{\beta_j^\top x}}$, estimada por
  máxima verosimilitud con pesos de clase balanceados y rasgos estandarizados.
- **Random Forest:** $\hat P(y=k\mid x)=\frac1B\sum_{b=1}^{B}\hat P_b(y=k\mid x)$, promedio de $B=400$ árboles, cada uno
  entrenado con una muestra con reemplazo.
- **Gradient Boosting:** suma de árboles pequeños $F_M(x)=\sum_{m=1}^{M}\nu\,h_m(x)$; cada árbol $h_m$ corrige los
  errores de los anteriores.
- **Métricas:**
  - Por clase: $P_k=\dfrac{VP_k}{VP_k+FP_k}$, $R_k=\dfrac{VP_k}{VP_k+FN_k}$ y $F1_k=\dfrac{2P_kR_k}{P_k+R_k}$.
  - $F1_{\text{macro}}=\frac13\sum_kF1_k$.
  - Exactitud = aciertos ÷ casos.
  - **Cambios anticipados:** aciertos en los meses en que $y_{t+1}\ne y_t$.

**Supuestos:**
- El estado del mes siguiente depende de los últimos tres meses y de la temporada.
- Los meses de prueba nunca se usan para entrenar: validación temporal.

**Cómo se resolvió (backtesting con origen móvil):** para cada uno de los 12 meses objetivo de prueba (ago-2025 a
jul-2026) se reentrena cada modelo con todo lo anterior y se predice solo ese mes. Son 12 reentrenamientos y 156
predicciones, de las cuales 30 son cambios reales de estado.

| Modelo | Aciertos (de 156) | Cambios anticipados (de 30) | Falsas alarmas | $F1_{\text{macro}}$ |
|---|---:|---:|---:|---:|
| Persistencia (línea base) | 126 | 0 | 0 | 0.774 |
| **Regresión logística (elegida)** | **130** | **8** | **4** | 0.793 |
| Random Forest | 130 | 6 | 2 | 0.766 |
| Gradient Boosting | 128 | 7 | 5 | 0.731 |

**Elección (criterio de Brandon):** el modelo que más acierta y, a igualdad, el que más cambios anticipa. Con el índice
original ese criterio daba Random Forest (136 de 156, contra 133 de la persistencia). Tras agregar "llegadas por cuarto",
la regresión logística y Random Forest empatan en 130 aciertos y la logística anticipa más cambios (8 contra 6). Se
respeta el criterio, no el nombre del modelo.

**Lectura honesta:** el estado se repite el 81 % de los meses (126 de 156), así que el aprendizaje de máquina agrega
poco (+4 aciertos) sobre "igual que este mes". Su valor está en los 8 cambios que anticipa.

**Ejemplo resuelto a mano:** $F1_{\text{macro}}$ de la regresión logística con su matriz de confusión en el origen móvil
(filas = real, columnas = predicho):

| | tranquilo | concurrido | saturado |
|---|---:|---:|---:|
| **tranquilo** | 75 | 12 | 0 |
| **concurrido** | 10 | 50 | 2 |
| **saturado** | 0 | 2 | 5 |

- Tranquilo: $P=\frac{75}{85}=0.882$, $R=\frac{75}{87}=0.862$, $F1=0.872$.
- Concurrido: $P=\frac{50}{64}=0.781$, $R=\frac{50}{62}=0.806$, $F1=0.794$.
- Saturado: $P=\frac57=0.714$, $R=\frac57=0.714$, $F1=0.714$.
- $F1_{\text{macro}}=\frac{0.872+0.794+0.714}{3}=0.793$. Aciertos: $75+50+5=130$.

**Qué pesa en el modelo:** promedio de $|\beta|$ entre las tres clases, con rasgos estandarizados.

| Rasgo | $\lvert\beta\rvert$ |
|---|---:|
| Índice del mes | 1.07 |
| Índice de dos meses antes | 1.04 |
| Índice del mes anterior | 0.95 |
| Temporada (coseno) | 0.80 |
| Cambio | 0.40 |
| Ser uno de los 5 lugares | 0.35 |
| Temporada (seno) | 0.11 |

**Sesgo (punto del plan, medido en la auditoría):** en los 12 meses de prueba, los 5 lugares tuvieron solo 2 cambios de
estado en 48 casos, y el modelo no anticipó ninguno (exactitud 0.958, igual a la persistencia). En el resto del estado
hubo 28 cambios en 108 casos, y el modelo anticipó 8 (exactitud 0.778 contra 0.741 de la persistencia). **Conclusión:** el
modelo anticipa cambios en los lugares de referencia; en los 5 lugares de la campaña casi no ha habido cambios con qué
probarlo.

**Predicción para agosto de 2026** (`estado_mes_siguiente_est`):
- Los 5 lugares siguen tranquilos, con probabilidad de 0.98 a 1.00, salvo Laguna Milagros, que no tiene dato.
- Mahahual sigue concurrido, con 0.40 de probabilidad de saturarse.

**Dónde está en el código:** `backend/torre/radar/prediccion.py` → `indice_comparable()`, `tabla_de_aprendizaje()`,
`comparar()`, `origen_movil()`, `sesgo()` y `predecir_mes_siguiente()`. Pruebas: `tests/test_radar_prediccion.py`.

### 2.3 Cadena de Markov semanal del norte (pieza 3b) ✅

**Ecuaciones:**
- **Estado semanal** de cada centro de DataTur: ocupación $O_{c,w}=100\cdot\frac{\text{ocupados}}{\text{disponibles}}$.
  Tranquilo si $O<u_{50}$, concurrido si $u_{50}\le O\le u_{90}$ y saturado si $O>u_{90}$, con los percentiles comunes
  de las 1,673 semanas de los 7 centros: $u_{50}=71.2\,\%$ y $u_{90}=85.9\,\%$.
- **Matriz de transición** (máxima verosimilitud): $\hat p_{ij}=\dfrac{n_{ij}}{\sum_j n_{ij}}$, con $n_{ij}$ = número de
  veces que un centro pasó del estado $i$ al $j$ entre dos semanas consecutivas.
- **Pronóstico a $k$ semanas:** $\pi_{t+k}=\pi_t\,P^k$, con $\pi_t$ = 1 en el estado actual.
- **Distribución estacionaria:** $\pi=\pi P$, $\sum\pi=1$ (vector propio de $P^\top$ con valor propio 1).
- **Puntaje de Brier:** $B=\frac1N\sum_n\sum_j\left(p_{n,j}-\mathbb 1[y_n=j]\right)^2$. Vale 0 si es perfecto; más bajo es
  mejor.

**Supuestos:**
- Propiedad de Markov: el estado de la semana siguiente depende solo del de esta semana.
- La matriz es la misma para los 7 centros y en el tiempo (homogénea). Por eso dos centros en el mismo estado tienen el
  mismo riesgo. Es una limitación declarada.

**Cómo se resolvió:** conteo de 1,666 pares de semanas consecutivas y división entre el total de cada fila; potencias de
la matriz para $k=1\dots8$. Backtest con las últimas 52 semanas: para cada semana, $P$ se estima solo con transiciones
anteriores.

**Conteos y matriz (filas = esta semana, columnas = la siguiente):**

| $n_{ij}$ | tranquilo | concurrido | saturado | $\hat p_{ij}$ | tranquilo | concurrido | saturado |
|---|---:|---:|---:|---|---:|---:|---:|
| **tranquilo** | 765 | 65 | 0 | | 0.922 | 0.078 | 0.000 |
| **concurrido** | 67 | 555 | 46 | | 0.100 | 0.831 | 0.069 |
| **saturado** | 2 | 44 | 122 | | 0.012 | 0.262 | 0.726 |

**Ejemplo resuelto a mano:**
- Fila tranquilo: $\hat p=\frac{765}{830}=0.922$.
- ¿Qué probabilidad hay de que un centro hoy tranquilo esté saturado dentro de 2 semanas?
  $\sum_j p_{t,j}\,p_{j,s}=0.922\cdot0+0.078\cdot0.069+0\cdot0.726=0.005$.
- A largo plazo: $\pi=(0.513,\,0.389,\,0.098)$. Es decir, el norte pasa el 9.8 % de las semanas saturado.

**Backtest (364 casos por horizonte):**

| Horizonte | Brier Markov | Brier persistencia | Brier frecuencia simple | Exactitud Markov | Exactitud persistencia |
|---|---:|---:|---:|---:|---:|
| 1 semana | **0.200** | 0.225 | 0.544 | 0.887 | 0.887 |
| 4 semanas | **0.389** | 0.484 | 0.549 | 0.723 | 0.758 |
| 8 semanas | **0.490** | 0.676 | 0.555 | 0.632 | 0.662 |

**Lectura:** la cadena da **mejores probabilidades** que la persistencia en los tres horizontes (Brier más bajo). Si
solo se toma el estado más probable, no le gana a la persistencia a 4 y 8 semanas. Su valor está en la probabilidad
("14 % de riesgo de saturarse"), no en una sola etiqueta.

**Semana del 27 de julio de 2026:** Playacar está concurrida (81.7 %), con 6.9 % de probabilidad de saturarse la
semana siguiente y 13.9 % en 5 semanas. Los otros 6 centros están tranquilos, con 5.4 % a 8 semanas.

**Dónde está en el código:** `backend/torre/radar/markov.py` → `estados()`, `transiciones()`, `matriz()`,
`estacionaria()`, `a_k_semanas()` y `backtest()`. Pruebas: `tests/test_radar_markov.py`.

### 2.4 Clustering jerárquico de los centros turísticos del país ✅

**Ecuaciones:**
- **Perfil de cada centro** $c$: la ocupación de cada mes del año en 2022–2026,
  $p_{c,m}=100\cdot\dfrac{\sum_{\text{años}}\text{ocupados}_{c,m}}{\sum_{\text{años}}\text{disponibles}_{c,m}}$, con
  $m=1\dots12$. Es un vector de 12 números por centro.
- **Distancia** entre centros: euclidiana, $d(c,c')=\sqrt{\sum_m (p_{c,m}-p_{c',m})^2}$.
- **Ward:** en cada paso se unen los dos grupos $A,B$ que menos aumentan la varianza interna,
  $\Delta(A,B)=\dfrac{|A|\,|B|}{|A|+|B|}\,\lVert\bar p_A-\bar p_B\rVert^2$.
- **Silueta** de un centro: $s(i)=\dfrac{b(i)-a(i)}{\max\{a(i),b(i)\}}$, con $a(i)$ la distancia media a su propio grupo
  y $b(i)$ la distancia media al grupo más cercano. El número de grupos $k$ es el de mayor silueta promedio (decisión de
  Brandon).

**Supuestos:**
- Solo centros reales (fila "centro" de DataTur) con sus 55 meses completos. Los agregados ("Total", "Centros de playa",
  "Ciudades") no son lugares. Los centros con meses vacíos no se rellenan, se excluyen: son 41, de los cuales 32 tienen
  solo 3 meses publicados y 9 tienen meses sin dato.
- Los 5 lugares de la campaña no están en DataTur: el clustering describe al norte y al país.

**Cómo se resolvió:**
1. Calcular los 12 promedios de cada centro (sumando cuartos, no porcentajes).
2. Unir con Ward.
3. Cortar el árbol en $k=2\dots8$ y calcular la silueta de cada corte.

| $k$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Silueta | **0.450** | 0.380 | 0.365 | 0.300 | 0.283 | 0.317 | 0.306 |

**Resultado ($k=2$):**
- **Grupo 1, playas y destinos muy ocupados:** 23 centros con 64.5 % de ocupación media. Entre ellos Playacar,
  Akumal, Cancún, Riviera Maya, Playa del Carmen y Los Cabos.
- **Grupo 2, el resto del país:** 32 centros con 41.1 %. Aquí quedan Cozumel e Isla Mujeres, junto a ciudades como
  Morelia, Oaxaca y Guadalajara.
- **Opción descartada:** $k=7$ (silueta 0.317). Da más detalle, pero grupos menos separados.

**Ejemplo resuelto a mano (silueta de Cancún):**
- Distancia media a los otros 22 centros de su grupo: $a=43.84$.
- Distancia media a los 32 del otro grupo: $b=116.21$.
- $s=\dfrac{116.21-43.84}{116.21}=0.623$. Cancún está bien asignado; el promedio de todos los centros es 0.450.

Perfil de Cancún (%): ene 76.4, feb 79.1, mar 80.1, abr 75.0, may 71.0, jun 72.7, jul 75.4, ago 72.0, sep 64.5, oct 67.5,
nov 75.6, dic 78.6.

**Dónde está en el código:** `backend/torre/radar/clustering.py` → `centros_completos()`, `perfiles()`, `agrupar()` y
`describir()`. Salida: `datos/gold/radar_clusters_centros.parquet`. Pruebas: `tests/test_radar_clustering.py`.

## 3. A3 Pronóstico 🕓
- **Holt-Winters aditivo**:
  - $\ell_t=\alpha(y_t-s_{t-m})+(1-\alpha)(\ell_{t-1}+b_{t-1})$
  - $b_t=\beta(\ell_t-\ell_{t-1})+(1-\beta)b_{t-1}$
  - $s_t=\gamma(y_t-\ell_t)+(1-\gamma)s_{t-m}$
  - pronóstico: $\hat y_{t+h}=\ell_t+h\,b_t+s_{t+h-m}$
- **Error**: $MAPE=\dfrac{100}{n}\sum_t\left|\dfrac{y_t-\hat y_t}{y_t}\right|$
- **Intervalo conformal al 90 %**: $\hat y\pm\hat q$, donde $\hat q$ es el cuantil $\lceil (n+1)\,0.9\rceil/n$ de los residuos absolutos de calibración. La cobertura real se mide en el backtest.
- **Huracanes (Poisson)**: $\hat\lambda_m=\dfrac{\#\text{tormentas que afectan Q. Roo en el mes } m}{\#\text{años}}$ y $P(N_m\ge 1)=1-e^{-\hat\lambda_m}$
- **Monte Carlo**:
  - media: $\hat\mu=\dfrac1R\sum_{r=1}^{R}D^{(r)}$
  - escenarios malo / probable / bueno: percentiles 10 / 50 / 90 de $D^{(r)}$
  - riesgo de rebasar la capacidad: $\hat p=\dfrac1R\sum_r \mathbb 1\!\left[D^{(r)}>C\right]$

## 4. Investigación de Operaciones: modelo de dos etapas 🕓
$$\max_{x,y}\ \sum_{m,d,c} r_{d,c}\,x_{m,d,c}\;+\;\mathbb{E}_{\xi}\!\left[Q(x,\xi)\right]$$
Sujeto a:
- presupuesto: $\sum_{m,d,c}x_{m,d,c}\le B$
- capacidad: $\sum_c a_{d,c}\,x_{m,d,c}\le \text{capacidad libre}_{d,m}$
- regla ambiental: $x_{m,d,c}=0$ si el destino $d$ está "saturado" en el mes $m$
- piso de equidad: $\sum_{m,c}x_{m,d,c}\ge \phi\,B$ para cada destino promovido
- no negatividad: $x\ge 0$
- activación semanal en la etapa 2: $y_{w,d}\in\{0,1\}$

**Cómo se resuelve:** como **equivalente determinista**, con un escenario por cada muestra de Monte Carlo. Lo resuelve
PuLP/CBC (simplex más *branch-and-bound* para las variables binarias). Se reportan los precios sombra
$\partial z^*/\partial b_i$ y la frontera de Pareto (visitantes vs presión) por el método de $\varepsilon$-restricción.

## 5. A5 Torre en vivo 🕓
- **Puntaje de anomalía (Isolation Forest)**: $s(x)=2^{-\frac{E[h(x)]}{c(n)}}$, donde $h(x)$ es la profundidad de aislamiento y $c(n)=2H(n-1)-\frac{2(n-1)}{n}$
- **Regla de pausa**: si $IPT_{d,w}>u$ o $s(x)>\tau$, entonces $y_{w,d}=0$

## 6. Campaña: minería de texto 🕓
- **Peso de un término**: $\text{tfidf}(t,d)=tf(t,d)\cdot\log\dfrac{N}{df(t)}$
- **Reglas de asociación**:
  - soporte: $sop(A)=\dfrac{\#\{A\}}{N}$
  - confianza: $conf(A\Rightarrow B)=\dfrac{sop(A\cup B)}{sop(A)}$
  - lift: $\text{lift}=\dfrac{conf(A\Rightarrow B)}{sop(B)}$
