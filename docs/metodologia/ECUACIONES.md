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

## 1-quater. Cierre de la Fase 2: duplicados y fuentes que no coinciden ✅
Decisiones en `docs/decisiones/18-cierre-fase-2.md`.

### Ecuaciones
- **Duplicados (AFAC):** para cada llave $k$ = (año, mes, tipo, servicio, región, aerolínea) con renglones
  $P_{k,1},\dots,P_{k,r}$:
  $$P_k=\begin{cases}\max_i P_{k,i} & \text{si a lo más una cifra es}>0\\ \sum_i P_{k,i} & \text{si hay dos o más}>0\ \text{y la etiqueta está autorizada}\\ \text{detener} & \text{en otro caso}\end{cases}$$
- **Diferencia entre fuentes** del mismo dato (cruceristas): $\Delta\%=\left(\frac{S}{D}-1\right)\times100$, con $S$ =
  SITUR-Q y $D$ = DataTur, sumados en el año.

### Supuestos
- Una copia en cero de una llave con cifra es un error de captura, no un mes sin pasajeros (misma regla que INAH).
- "Virgin América (Alaska Airlines)" agrupa a dos aerolíneas que volaban por separado hasta su fusión (2018). Por eso
  sus dos cifras se suman. Es decisión de Brandon.

### Cómo se resolvió
1. Se quitan los renglones idénticos (98).
2. Se cuentan las cifras mayores que cero por llave.
3. Se aplica la regla y se marca `sumada_flag`.
4. Para la conciliación se cruzan los meses con dato en las dos fuentes y se suman por año.

### Ejemplos resueltos a mano (números reales)
- *AFAC, enero de 2016, Virgin América (Alaska Airlines):* 144,372 + 12,209 = **156,581** pasajeros. En total hay 25
  llaves sumadas y en juego 369,311 de 1,042,673,534 pasajeros (0.035 %).
- *Cozumel, 2025:* $\left(\frac{4{,}915{,}242}{4{,}724{,}255}-1\right)\times100=$ **+4.04 %**.
  - *Mahahual, 2025:* $\left(\frac{2{,}641{,}695}{2{,}379{,}422}-1\right)\times100=$ **+11.02 %**.

### Dónde está en el código
`backend/torre/base/silver_afac.py` (`quitar_duplicados`), `silver_cruceros.py` (`reconciliar_siturq`). Pruebas:
`tests/test_silver_fase2.py`.

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

## 3. A3 Pronóstico ✅

### 3.0 Insumos limpios para el Pronóstico (Fase 2, Silver) ✅
Decisiones en `docs/decisiones/10-silver-fase5.md`.

**Ecuaciones**
- Distancia de un punto de trayectoria a Chetumal (fórmula de haversine, radio terrestre $R=6{,}371$ km):
  $$d=2R\,\arcsin\sqrt{\sin^2\!\frac{\Delta\varphi}{2}+\cos\varphi_1\cos\varphi_2\,\sin^2\!\frac{\Delta\lambda}{2}}$$
  con $\varphi$ = latitud y $\lambda$ = longitud en radianes; Chetumal = $(18.50,\,-88.30)$.
- Tormenta que **afecta al sur** (definición elegida por Brandon, 30-sep-2026): la tormenta $s$ es evento si
  $$\exists\,\text{punto } j \text{ de } s:\quad d_j\le 200\ \text{km}\ \wedge\ v_j\ge 34\ \text{nudos}\ \wedge\ \text{año}_j\ge 1966$$
  El **mes del evento** es el del primer punto que cumple la condición.
- Tasa anual observada: $\hat\lambda=\dfrac{\#\text{eventos}}{\#\text{años}}$.
- Tipo de cambio mensual (solo días observados): $\overline{TC}_m=\dfrac{1}{n_m}\sum_{t\in m,\ TC_t\neq\text{vacío}}TC_t$, con $n_m$ = días con dato.
- Hora local de Quintana Roo: $h_{local}=h_{UTC}-5\text{ h}$ (UTC−5 fijo desde el 1-feb-2015; sin horario de verano).

**Supuestos**
- La posición de HURDAT2 cada 6 horas representa la trayectoria. Entre dos puntos la tormenta pudo pasar un poco más
  cerca, así que el conteo es conservador.
- Desde 1966 no se pierden tormentas en el mar porque hay satélites, y las 60 temporadas son comparables entre sí.
- Un feriado sin cotización no tiene tipo de cambio; no se copia el del día anterior.

**Cómo se resolvió**
1. Se recorre el texto de HURDAT2: encabezado (id, nombre, $n$) y $n$ líneas de trayectoria. Se leen la posición, el
   viento y la presión con una expresión regular; −99 y −999 se vuelven vacíos.
2. A cada punto se le calcula $d$ con la fórmula de haversine y se le ponen las tres banderas: radio, viento y era
   satelital.
3. Se filtran los puntos que cumplen las tres, se agrupa por tormenta y se toma el primer mes → 31 eventos.
4. FRED: se agrupan los días por mes y se promedian solo los que tienen dato; se guarda $n_m$.

**Ejemplos resueltos a mano (números reales)**
- *Huracán Carmen, 2-sep-1974, 13:30 UTC, en 18.6° N, 88.2° W, 125 nudos:*
  $\Delta\varphi=\Delta\lambda=0.1°=0.0017453$ rad;
  $\sin^2(0.00087266)=7.6154\times10^{-7}$; $\cos 18.5°=0.94832$; $\cos 18.6°=0.94777$;
  $a=7.6154\times10^{-7}+0.94832\cdot0.94777\cdot7.6154\times10^{-7}=1.4460\times10^{-6}$;
  $d=2\cdot6371\cdot\arcsin(\sqrt{1.4460\times10^{-6}})=2\cdot6371\cdot0.0012025=$ **15.3 km** → dentro del radio, con
  viento ≥ 34 y año ≥ 1966: **es evento** (mes 9). El código da 15.3 km.
- *Huracán Dean, 21-ago-2007:* toca tierra (marca "L") en 18.7° N, 87.7° W con 150 nudos, a 67.0 km de Chetumal: **es
  evento** (mes 8).
- *Tasa:* 31 eventos entre 1966 y 2025 (60 temporadas): $\hat\lambda=31/60=$ **0.517 por año**. Por mes: mayo 1, junio 3,
  julio 1, agosto 9, septiembre 8, octubre 6 y noviembre 3.
- *Tipo de cambio de agosto de 2026:* 21 días hábiles, todos con dato; la suma es 358.2785, así que
  $\overline{TC}=358.2785/21=$ **17.0609 pesos por dólar**.

**Dónde está en el código**
`backend/torre/base/silver_huracanes.py` (`km_haversine`, `agregar_banderas`, `eventos_sur`) ·
`backend/torre/base/silver_fred.py` (`mensual`) · `backend/torre/base/silver_clima.py` (`clima_horario`). Pruebas:
`tests/test_silver_fase5.py`.

### 3.1 Series a pronosticar y meses que no entrenan (Fase 5, pieza 1) ✅
Decisiones en `docs/decisiones/11-pronostico.md` ("Medidas + norte" y "Hueco + forma del año").

**Reglas.** Para una zona $z$ con visitantes $y_{z,t}$ en el mes $t$:
- **Cierre:** $\text{cierre}_{z,t}\iff y_{z,t}=0$.
- **Mes parcial:** $\text{parcial}_{z,t}\iff y_{z,t}>0\ \wedge\ (y_{z,t-1}=0\ \lor\ y_{z,t+1}=0)$. Es el mes justo antes de
  cerrar o justo después de reabrir. Un mes sin dato porque la zona aún no existía (Ichkabal antes de 2025) no cuenta
  como cierre.
- **Región** $R$ (suma de sus zonas): $y_{R,t}=\sum_{z\in R}y_{z,t}$. El mes de la región toma el motivo más fuerte de sus
  zonas existentes, en este orden: cierre, luego mes parcial.
- **Pandemia:** $t\in[\text{mar-}2020,\ \text{dic-}2021]$ en el INAH y $t\in[\text{mar-}2020,\ \text{jun-}2022]$ en Belice.
- **Entrena:** $\text{entrena}_{R,t}=\mathbb 1[\text{sin motivo}]$. El valor $y_{R,t}$ se conserva siempre; solo se
  marca.

**Ejemplo resuelto a mano (Ruta arqueológica del sur, reapertura de 2025)**

| Mes | Kohunlich | Dzibanché | Ichkabal | Motivo de cada zona | Región |
|---|---:|---:|---:|---|---|
| dic-2024 | 0 | 0 | (no existía) | cierre, cierre | **cierre** |
| ene-2025 | 750 | 0 | 5,277 | parcial (dic = 0), cierre, — (abre por primera vez) | **cierre** (el más fuerte) |
| feb-2025 | 3,481 | 249 | 5,667 | —, parcial (ene = 0), — | **mes parcial** |
| mar-2025 | 2,039 | 488 | 4,434 | —, —, — | **entrena** |

Resultado: 90 meses entrenan en la Bahía (de 127), 91 en la Ruta (de 127), 62 en Belice (de 90) y 55 en Cancún (de 55).

**Dónde está en el código** `backend/torre/pronostico/series.py` (`_motivos_zona`, `_pandemia`, `series_inah`,
`serie_belice`, `serie_norte` para Cancún y Riviera Maya). Pruebas: `tests/test_pronostico.py`.

### 3.2 Forma del año y fuerza de la temporada (Fase 5, pieza 2) ✅
Decisión en `docs/decisiones/11-pronostico.md`.

**Ecuaciones** (descomposición clásica multiplicativa sobre años completos)
- Razón del mes $m$ del año $a$: $r_{a,m}=\dfrac{y_{a,m}}{\bar y_a}$, con $\bar y_a=\dfrac{1}{12}\sum_{m=1}^{12}y_{a,m}$.
- Índice del mes: $\tilde S_m=\dfrac{1}{|A|}\sum_{a\in A}r_{a,m}$, reescalado a $S_m=\dfrac{\tilde S_m}{\frac1{12}\sum_k\tilde S_k}$, de modo
  que $\frac1{12}\sum_m S_m=1$. Aquí $A$ = años con los 12 meses entrenables.
- Fuerza de la temporada (Wang, Smith y Hyndman, 2006), en logaritmos: con $s_{a,m}=\ln S_m$ y
  $e_{a,m}=\ln r_{a,m}-\ln S_m$,
  $$F_S=\max\!\left(0,\ 1-\frac{\operatorname{Var}(e)}{\operatorname{Var}(s+e)}\right)$$
  $F_S=0$: no hay temporada; $F_S=1$: el mes lo explica todo.
- ¿El sur acompaña al norte?: $\rho=\operatorname{corr}\big(\ln S^{\text{sur}}_m,\ \ln S^{\text{Cancún}}_m\big)$ sobre los 12 meses.

**Supuestos**
- La forma del año es la misma en todos los años completos; lo que cambia de un año a otro es el nivel. Se acepta
  porque el índice sale parecido año con año. En la Ruta, enero va de 1.25 a 1.83 y fue el mes más alto o el segundo en
  5 de los 6 años (en 2022, el tercero). Septiembre fue el más bajo o el segundo más bajo en los 6.
- La temporada es proporcional al nivel (multiplicativa). Kohunlich reabrió a la mitad de su nivel de 2019, y un "+30 %"
  sigue valiendo donde un "+2,000 visitantes" ya no.
- Un año con meses cerrados no entra, porque su promedio $\bar y_a$ saldría sesgado.

**Cómo se resolvió**
1. Se toman las series de la pieza 1 y se eligen los años con los 12 meses entrenables:
   - Bahía: 2016–2019, 2022 y 2025;
   - Ruta: 2016–2019, 2022 y 2023;
   - Belice: 2019 y 2023–2025;
   - Cancún: 2022–2025.
2. Se divide cada mes entre el promedio de su año y se promedian las razones por mes. Luego se reescala para que los 12
   índices promedien 1.
3. $F_S$ se calcula con las varianzas en logaritmos.
4. **Segunda opinión con STL.** STL (Loess) solo acepta series continuas, así que se corre sobre el tramo sin huecos más
   largo de cada serie y se correlaciona su índice con el de este método:
   - 0.955 a 0.966 en la Bahía, la Ruta y Cancún: coinciden.
   - 0.847 en Belice. Con la primera regla (pandemia hasta feb-2022) daba 0.446: el tramo empezaba en mar-2022, cuando
     los cruces iban en 65–82 % de 2019, y STL confundía la recuperación con temporada. Brandon decidió contar mar–jun
     2022 como pandemia, y el tramo ahora empieza en jul-2022.

**Ejemplo resuelto a mano (Ruta arqueológica del sur, enero)**
- 2019: Kohunlich 42,813 + Dzibanché 21,326 = 64,139 visitantes en el año. $\bar y_{2019}=64{,}139/12=5{,}344.92$.
  En enero hubo 7,935: $r_{2019,1}=7{,}935/5{,}344.92=$ **1.4846**.
- Las seis razones de enero: 1.5459 (2016), 1.7075 (2017), 1.8266 (2018), 1.4846 (2019), 1.2540 (2022) y
  1.8173 (2023). Su promedio es $\tilde S_1=9.6359/6=$ **1.606**.
- El promedio de los 12 $\tilde S_m$ es 1.0000, así que $S_1=$ **1.606**: en enero la Ruta recibe 61 % más que en un mes
  promedio.
- En septiembre, $S_9=0.496$: la mitad de un mes promedio.

**Resultados**

| Serie | Años | $F_S$ | Mes más alto | Mes más bajo | Corr. con STL | $\rho$ con Cancún |
|---|---:|---:|---|---|---:|---:|
| Ruta arqueológica del sur | 6 | 0.793 | enero (1.61) | septiembre (0.50) | 0.955 | 0.834 |
| Bahía Calderitas–Oxtankah | 6 | 0.684 | diciembre (1.40) | septiembre (0.65) | 0.960 | 0.716 |
| Chetumal · Belice | 4 | 0.655 | diciembre (1.17) | febrero (0.87) | 0.847 | 0.257 |
| Cancún (referencia) | 4 | 0.714 | marzo (1.08) | septiembre (0.87) | 0.966 | — |

**Dónde está en el código**
`backend/torre/pronostico/forma.py` (`anios_completos`, `razones`, `indice_estacional`, `fuerza_estacional`,
`segunda_opinion_stl`, `acompana_al_norte`). Salidas: `datos/gold/pronostico_forma_anio.parquet` y
`pronostico_fuerza_estacional.parquet`. Pruebas: `tests/test_pronostico.py`.

### 3.3 Modelos del Pronóstico, rango del 90 % y elección (Fase 5, pieza 3) ✅
Decisiones en `docs/decisiones/11-pronostico.md`.

**Ecuaciones.** $y_t$ = valor del mes $t$; $o$ = origen (último mes conocido); $h$ = horizonte (1–12);
$S_m$ = forma del año calculada **solo con años completos anteriores a $o$** (§3.2).
- **Línea base (ingenuo estacional):** $\hat y_{o+h}=y_{t^*}$, donde $t^*$ es el último mes útil antes de $o$ con el mismo
  mes del año que el destino.
- **Holt-Winters con forma del año fija.** Se desestacionaliza, $z_t=y_t/S_{m(t)}$, sobre el tramo desde la última
  reapertura.
  - Con tendencia amortiguada: $\ell_t=\alpha z_t+(1-\alpha)(\ell_{t-1}+\phi b_{t-1})$ y
    $b_t=\beta(\ell_t-\ell_{t-1})+(1-\beta)\phi b_{t-1}$. El pronóstico es
    $\hat y_{o+h}=\big(\ell_o+\sum_{i=1}^{h}\phi^i b_o\big)\,S_{m(o+h)}$.
  - Sin tendencia: $\ell_t=\alpha z_t+(1-\alpha)\ell_{t-1}$ y $\hat y_{o+h}=\ell_o\,S_{m(o+h)}$.
  - Con menos de 6 meses en el tramo: $\ell_o=\bar z$.
- **Regresión con clima** (mínimos cuadrados):
  $$\ln y_t=\sum_k \tau_k\,\mathbb 1[t\in\text{tramo }k]+\sum_{m=2}^{12}\mu_m\,\mathbb 1[m(t)=m]+\beta\,\frac{L_t-\bar L_{m(t)}}{100}+\gamma\,T_t+\varepsilon_t$$
  - $L_t$: lluvia del mes (mm).
  - $\bar L_m$: lluvia normal del mes, calculada antes de $o$.
  - $T_t$: 1 si ese mes empezó una tormenta que afecta al sur.

  El pronóstico usa el nivel del tramo actual $K$ y el clima normal, porque el clima futuro no se conoce:
  $$\hat y_{o+h}=\exp\!\big(\hat\tau_K+\hat\mu_{m}+\hat\gamma\,\hat p_m\big)$$
  con $\hat p_m$ = fracción de años (desde 1966) con tormenta en ese mes.
- **Gradient Boosting con rezagos:** $\ln y_d=f(h,\ m(d),\ \ln y_o,\ \ln\bar y_{o-2:o},\ \ln y_{t^*})$.
  - Árboles de decisión sumados que aprenden de todos los pares pasados (origen → destino).
  - Configuración: 150 árboles, tasa de aprendizaje 0.05 y hojas de al menos 20 casos.
- **Error:**
  - $MAE=\frac1n\sum|y-\hat y|$;
  - $MAPE=\frac{100}{n}\sum\left|\frac{y-\hat y}{y}\right|$;
  - error relativo $=MAE_{\text{modelo}}/MAE_{\text{línea base}}$ (menos de 1 = mejor que la base).
- **Rango del 90 % (conformal secuencial).** El error de cada pronóstico es $e=\left|\ln(\hat y/y)\right|$, e infinito si
  $\hat y\le0$. Para un pronóstico hecho en $o$ y tramo de horizonte $H\in\{1\text{–}3,\,4\text{–}6,\,7\text{–}12\}$, la
  calibración usa los $n$ errores de ese modelo y tramo cuyo mes destino ya había pasado en $o$ (se exige $n\ge20$):
  $$\hat q=e_{(k)},\quad k=\lceil (n+1)\cdot0.9\rceil,\qquad \text{rango}=\big[\hat y\,e^{-\hat q},\ \hat y\,e^{\hat q}\big]$$
  Cobertura real = % de meses en que $y$ cayó dentro del rango.
- **Criterio de elección (Brandon):** por serie, el menor $MAE$ entre los modelos con cobertura $\ge80\,\%$.

**Supuestos**
- Los errores del futuro se parecen a los del pasado; es lo que da la garantía del conformal. **Se rompió en la Ruta en
  2023**, cuando las visitas cayeron 10.7 % (de 46,295 a 41,322) sin aviso en la historia: la cobertura de ese año fue de
  67 %.
- El clima futuro se toma como "normal". Por eso la lluvia no puede mejorar mucho el pronóstico; su valor está en los
  escenarios (pieza 4).
- Cada reapertura tiene su propio nivel (decisión "Hueco + forma del año").

**Cómo se resolvió (origen móvil)**
1. Para cada mes $o$ útil desde el primer origen (INAH: ene-2019; Cancún: ene-2023; Belice: jun-2023) se usa solo lo
   conocido hasta $o$:
   - se recalcula la forma del año con los años completos anteriores;
   - se ajusta cada modelo;
   - se pronostican los 12 meses siguientes.
2. Se evalúan solo los meses destino que entrenan, y solo los pares que **los 5 modelos** pudieron pronosticar
   (comparación justa): 366 (Bahía), 378 (Ruta), 366 (Belice) y 438 (Cancún).
3. Se calcula el rango conformal de cada pronóstico con los errores ya conocidos en su origen y se mide la cobertura.
4. Se aplica el criterio de Brandon. Con el modelo elegido se pronostican los 12 meses después del último dato. El rango
   usa todos los errores del origen móvil de ese modelo.

**Resultados del origen móvil** (MAPE en %; "vs base" = MAE ÷ MAE de la línea base; el elegido va en negritas)

| Serie | Modelo | MAPE | vs base | MAPE 1–3 m | MAPE 7–12 m | Cobertura 90 % | Rango típico |
|---|---|---:|---:|---:|---:|---:|---:|
| Bahía | **Regresión con clima** | 15.7 | **0.898** | 17.5 | 14.0 | 91.3 % | ±43 % |
| Bahía | Holt-Winters sin tendencia | 19.4 | 1.078 | 20.9 | 16.5 | 96.5 % | ±63 % |
| Bahía | Holt-Winters con tendencia | 27.6 | 1.524 | 22.2 | 33.0 | 87.8 % | ±108 % |
| Bahía | Gradient Boosting | 28.7 | 1.405 | 33.2 | 25.5 | 85.8 % | ±83 % |
| Bahía | Línea base | 19.8 | 1.000 | 26.6 | 13.4 | 85.4 % | ±77 % |
| Ruta | **Regresión con clima** | 21.6 | **0.737** | 20.2 | 23.4 | 80.3 % | ±51 % |
| Ruta | Holt-Winters sin tendencia | 20.1 | 0.639 | 18.2 | 22.4 | 72.3 % | ±45 % |
| Ruta | Holt-Winters con tendencia | 26.7 | 0.930 | 19.9 | 35.5 | 81.3 % | ±55 % |
| Ruta | Gradient Boosting | 34.4 | 1.074 | 32.3 | 37.7 | 81.3 % | ±87 % |
| Ruta | Línea base | 27.9 | 1.000 | 28.6 | 27.8 | 74.3 % | ±63 % |
| Belice | **Regresión con clima** | 11.0 | **0.820** | 10.4 | 11.4 | 94.1 % | ±26 % |
| Belice | Holt-Winters sin tendencia | 13.0 | 0.973 | 10.1 | 14.3 | 94.1 % | ±41 % |
| Belice | Holt-Winters con tendencia | 17.1 | 1.238 | 10.3 | 22.6 | 92.8 % | ±52 % |
| Belice | Gradient Boosting | 13.1 | 0.987 | 12.1 | 13.3 | 90.7 % | ±34 % |
| Belice | Línea base | 13.1 | 1.000 | 12.4 | 13.6 | 89.9 % | ±33 % |
| Cancún | Regresión con clima | 6.0 | 1.584 | 5.5 | 6.2 | 93.2 % | ±15 % |
| Cancún | Holt-Winters sin tendencia | 6.3 | 1.684 | 5.6 | 5.9 | 99.7 % | ±16 % |
| Cancún | Holt-Winters con tendencia | 6.8 | 1.838 | 6.0 | 6.5 | 100.0 % | ±19 % |
| Cancún | Gradient Boosting | 3.9 | 1.044 | 4.2 | 3.6 | 95.8 % | ±11 % |
| Cancún | **Línea base** | 3.8 | **1.000** | 4.1 | 3.6 | 89.3 % | ±10 % |

**Hallazgos que se declaran**
- **La tendencia falla en tramos cortos.** Holt-Winters con tendencia pronosticó −240 visitantes para la Bahía en abril de
  2026 (origen may-2025), porque aprendió la tendencia en plena reapertura. Esos 4 pronósticos cuentan como error
  infinito en el rango.
- **El clima casi no mejora el pronóstico.** La misma regresión sin lluvia ni tormentas da 0.906 en la Bahía, 0.842 en
  Belice y 0.721 en la Ruta, contra 0.898, 0.820 y 0.737 con clima. Lo que gana es la estructura: nivel por tramo y
  mes.
- **Lo que sí dicen los coeficientes** (último origen):
  - Bahía: $\hat\beta=-0.115$ por cada 100 mm de lluvia arriba de lo normal, o sea $e^{-0.115}-1=$ **−10.9 %** visitantes
    ($p=0.027$).
  - Belice: −4.3 % ($p=0.059$).
  - Ruta y Cancún: sin efecto.
  - Tormentas: solo 3 meses con tormenta entre los meses de entrenamiento, así que su efecto no se puede estimar con
    estas series ($p>0.36$).
- En Cancún, repetir el mismo mes del año anterior es lo mejor (3.8 % de error): su ocupación cambia poco de un año a
  otro.

**Ejemplos resueltos a mano (números reales)**
- *Error de un pronóstico:* Bahía, origen ene-2019, destino feb-2019, regresión con clima. Pronóstico 1,058.48 y real
  925: $e=|\ln(1{,}058.48/925)|=|\ln 1.1443|=$ **0.1348**, es decir, 14.4 % arriba.
- *Rango del 90 %:* Bahía, dic-2026, horizonte 5 (tramo 4–6). La calibración tiene $n=105$ errores, así que
  $k=\lceil 106\times0.9\rceil=96$ y el 96.º error más chico es $\hat q=0.3132$. El pronóstico es 1,311.13 visitantes:
  - mínimo $=1{,}311.13\times e^{-0.3132}=1{,}311.13\times0.7311=$ **959**;
  - máximo $=1{,}311.13\times1.3678=$ **1,793**.

  El mismo mes de 2025 tuvo 1,224 visitantes.

**Pronóstico de los próximos 12 meses** (`datos/gold/pronostico_mes.parquet`, columnas `_est`). Frente a los mismos
meses del año anterior:
- Bahía: +0.6 %.
- Ruta: +2.1 %.
- Belice: −4.9 %, en línea con la caída de ene–jun 2026.
- Cancún: 0.0 %.

**Dónde está en el código**
- `backend/torre/pronostico/modelos.py`: `ingenuo_estacional`, `holt_winters_forma_fija`, `holt_winters_sin_tendencia`,
  `regresion_con_clima`, `gradient_boosting_rezagos`, `origen_movil` y `metricas`.
- `intervalos.py`: `cuantil_conformal`, `agregar_intervalos` y `cobertura`.
- `seleccion.py`: `elegir` y `pronostico_final`.
- Pruebas: `tests/test_pronostico.py`.

### 3.4 Tormentas, escenarios y sensibilidad (Fase 5, pieza 4) ✅
Decisiones en `docs/decisiones/11-pronostico.md`.

**Ecuaciones**
- **Poisson de tormentas.** $N_m$ = número de tormentas que afectan al sur en el mes $m$ (definición de §3.0):
  $$N_m\sim\text{Poisson}(\lambda_m),\qquad \hat\lambda_m=\frac{\#\text{eventos que empezaron en el mes }m\ (1966\text{–}2025)}{60},\qquad P(N_m\ge1)=1-e^{-\hat\lambda_m}$$
  Al menos una en el año: $1-e^{-\sum_m\hat\lambda_m}$.
- **Monte Carlo** ($R=10{,}000$ futuros, semilla 2026). Para el futuro $r$ y el mes $j$ ($j=1\ldots12$):
  $$D^{(r)}_j=\hat y_j\cdot e^{\,\varepsilon^{(r)}_j}\cdot\big(1-\delta\,\mathbb 1[N^{(r)}_j\ge1]\big)$$
  - $\hat y_j$: pronóstico del modelo elegido (§3.3).
  - $\varepsilon^{(r)}_j=\ln(\text{real}/\text{pronóstico})$: se copian los 12 errores de **un mismo origen** del origen móvil,
    sorteado al azar. Así se conserva que los meses flojos vienen juntos. Si a ese origen le falta un horizonte, ese
    error se sortea del mismo tramo de horizonte.
  - $N^{(r)}_j\sim\text{Poisson}(\hat\lambda_{m(j)})$.
  - $\delta\in\{0,\ 0.25,\ 0.50\}$ es el **supuesto** del golpe de una tormenta. No se pudo medir.
- **Escenarios:** malo, probable y bueno = percentiles 10, 50 y 90 de $D^{(r)}_j$. Para el año se usan los percentiles de
  $\sum_j D^{(r)}_j$.
- **Riesgo de rebasar la capacidad probada:** $\hat p_j=\frac1R\sum_r\mathbb 1\big[D^{(r)}_j>C\big]$, con
  $C=\max_t y_t$ = el mes más alto que el lugar ya recibió.
- **Sensibilidad** (misma regresión de §3.3, con todos los meses que entrenan): $\ln y_t=\tau_{k(t)}+\mu_{m(t)}+\theta\,v_t$.
  El efecto en % es $e^{\hat\theta}-1$, con $v$ = lluvia sobre lo normal (cientos de mm) o pesos por dólar (FRED).

**Supuestos**
- Los errores del futuro se parecen a los del origen móvil, incluido el sesgo de cada modelo. Por eso el escenario
  probable no es igual al pronóstico del modelo: en la Bahía el modelo se quedó corto 6 % en la mediana, así que el
  escenario probable queda arriba.
- Las tormentas llegan de forma independiente, a una tasa constante por mes (Poisson).
- $\delta$ es un supuesto y así se presenta; se prueba con 3 valores.
- Sin efecto de la campaña (decisión de Brandon): son escenarios "de todos modos".
- La capacidad probada no es la capacidad física oficial; es lo máximo que ya se ha recibido.

**Cómo se resolvió**
1. Se cuentan los 31 eventos por mes de inicio y se divide entre 60 años.
2. Para cada lugar y cada $\delta$ se generan 10,000 futuros de 12 meses y se sacan los percentiles y el riesgo de
   capacidad.
3. Se estiman las sensibilidades por mínimos cuadrados con errores estándar clásicos; se reporta el valor $p$.

**Ejemplos resueltos a mano (números reales)**
- *Agosto:* 9 eventos en 60 años, así que $\hat\lambda_8=0.15$ y $P=1-e^{-0.15}=1-0.8607=$ **13.9 %**.
  Septiembre: $8/60=0.1333$ y $P=$ **12.5 %**. De diciembre a abril: **0 %**.
- *Al menos una tormenta en el año:* $1-e^{-31/60}=1-e^{-0.5167}=1-0.5965=$ **40.3 %**.
- *Golpe esperado en agosto con el supuesto más duro ($\delta=0.5$):* $0.1393\times0.5=$ **7.0 %** menos visitantes ese
  mes en promedio. En el año pesa poco: el escenario probable de la Bahía baja **1.8 %** (de 11,217 a 11,019).
- *Lluvia en la Bahía:* $\hat\theta=-0.1017$, así que $e^{-0.1017}-1=$ **−9.7 %** visitantes por cada 100 mm sobre lo
  normal ($p=0.039$).

**Resultados: escenarios de los próximos 12 meses sin campaña** (total del año; malo / probable / bueno)

| Lugar | Modelo | Golpe 0 % (supuesto) | Golpe 50 % (supuesto) | Riesgo de que algún mes rebase la capacidad probada |
|---|---:|---|---|---:|
| Ruta arqueológica del sur | 64,511 | 55,811 / 62,212 / 73,884 | 54,751 / 61,440 / 72,628 | 30.9 % (cap. 10,465, ene-2018) |
| Bahía Calderitas–Oxtankah | 10,771 | 10,106 / 11,217 / 13,085 | 9,915 / 11,019 / 12,777 | 24.2 % (cap. 1,639, abr-2017) |
| Chetumal · Belice | 606,584 | 551,986 / 620,304 / 671,956 | 535,346 / 606,138 / 660,162 | 38.3 % (cap. 65,792, ago-2025) |

- Cancún (referencia), ocupación promedio del año: 68.3 % / 69.6 % / 70.7 %.
- El riesgo de capacidad se concentra en los meses pico: dic-2026 en Chetumal (29 %) y en la Bahía (14 %), y ene-2027 en
  la Ruta (30 %).

**Sensibilidad medida**

| Lugar | +100 mm de lluvia sobre lo normal | +1 peso por dólar |
|---|---|---|
| Bahía Calderitas–Oxtankah | **−9.7 %** ($p=0.039$) | −0.2 % ($p=0.92$) |
| Ruta arqueológica del sur | −0.6 % ($p=0.92$) | **+6.8 %** ($p=0.011$) |
| Chetumal · Belice | **−4.7 %** ($p=0.031$) | +1.2 % ($p=0.36$) |

En negritas, $p<0.05$. Es una asociación, no una causa probada. La hipótesis de que un peso barato atrae más cruces
desde Belice **no se sostiene** con estos datos.

**Dónde está en el código**
`backend/torre/pronostico/escenarios.py` (`poisson_tormentas`, `errores_por_origen`, `simular`, `escenarios`,
`capacidad_probada`, `sensibilidad`). Salidas en `datos/gold/pronostico_`: `poisson_tormentas`, `escenarios`,
`escenarios_anual` y `sensibilidad`. Pruebas: `tests/test_pronostico.py`.

### 3.5 Planeador de viaje: temporada alta, recomendación y cercanía ✅
Decisiones en `docs/decisiones/12-planeador.md`.

**Ecuaciones**
- **Temporada alta** del lugar $l$ en el mes $t$:
  $$\text{alta}_{l,t}\iff S_{l,m(t)}\ge1.20\ \ \lor\ \ \hat p^{\,cap}_{l,t}\ge0.10$$
  - $S$ es la forma del año (§3.2).
  - $\hat p^{\,cap}$ es el riesgo de rebasar la capacidad probada (§3.4); solo existe dentro del horizonte del
    pronóstico.
  - Fuera de alta: "tranquilo" si $S<1$ y "normal" si $1\le S<1.20$.
- **Otro lugar:** $l^*=\arg\min_{l'\ne l,\ \neg\text{alta}_{l',t}} S_{l',m(t)}$.
- **Otro mes** para el mismo lugar:
  $$m^*=\arg\min_{m}\ S_{l,m}\quad\text{s. a.}\quad S_{l,m}<1.20,\ \ P(N_m\ge1)<0.09,\ \ \bar L_{l,m}<\operatorname{mediana}_k\bar L_{l,k}$$
  - $P(N_m\ge1)$ es la probabilidad de tormenta (§3.4).
  - $\bar L$ es la lluvia normal de 1991–2020 del punto de clima del lugar.
- **Cercanía:** distancia de haversine (§3.0) entre el negocio y el centro del lugar. El orden alterna tipos: el más
  cercano de cada tipo, luego el segundo, y así.
- **Clasificador por léxico:** con $r$ = raíz y $w$ = palabras del nombre normalizado,
  $\text{tipo}(n)=$ la primera categoría $c$ con $\exists\,r\in R_c,\ w\in n:\ w$ empieza con $r$. Si ninguna aplica,
  decide el giro SCIAN.

**Ejemplos resueltos a mano (números reales)**
- *Ruta, enero de 2027:* $S=1.606\ge1.20$, así que es **alta**.
  - Otro lugar: ese mes Chetumal tiene $S=0.93$ y no es alta, así que se sugiere **Chetumal**.
  - Otro mes: candidatos con $S<1.20$, tormenta < 9 % y lluvia < 84 mm (mediana en Kohunlich):
    - febrero: $S=1.196$, 22 mm, tormenta 0 %;
    - abril: $S=1.06$, 38 mm, 0 %;
    - noviembre: $S=0.98$, 76 mm, 4.9 %.

    El mínimo es **noviembre**. Mayo ($S=0.68$) queda fuera porque llueven 92 mm, más que la mediana.
- *Chetumal, diciembre de 2026:* $S=1.17<1.20$, pero $\hat p^{\,cap}=0.29\ge0.10$, así que es **alta**.
- *Distancia:* el Museo de la Cultura Maya está a **53.0 km** del punto de la Ruta (Kohunlich).

**Dónde está en el código**
`backend/torre/pronostico/calendario.py` (`nivel`, `recomendar`, `clima_normal`) y `backend/torre/campana/lugares.py`
(`clasificar`, `tiene`, `recomendaciones`, `enlace_maps`). Pruebas: `tests/test_planeador.py`.

### 3.6 Cancún y Riviera Maya en el planeador: temporada alta del norte y tormentas por punto ✅
Decisiones en `docs/decisiones/15-norte-en-planeador.md`.

**Ecuaciones**
- **Ocupación del mes** $o_{l,t}$ del lugar del norte $l$: el pronóstico $\hat y_{l,t}$ si $t$ está en el horizonte; si
  no, la ocupación típica del mes, que es el promedio medido de los años completos $A$ (2022–2025):
  $$\bar o_{l,m}=\frac{1}{|A|}\sum_{a\in A} o_{l,a,m}$$
- **Temporada alta del norte** (cortes del Radar, decisión 08):
  $$\text{alta}_{l,t}\iff o_{l,t}\ge q_{0.50},\qquad q_{0.50}=\text{mediana de la ocupación semanal de los 7 centros del norte}=71.16\ \%$$
  Abajo del corte, "tranquila".
- **Otro lugar** (solo del sur, $\mathcal S$ = Chetumal, Bahía, Ruta):
  $$l^*=\arg\min_{l'\in\mathcal S,\ \neg\text{alta}_{l',t}} S_{l',m(t)}$$
  Nunca se recomienda un lugar del norte.
- **Tormentas alrededor de un punto** $p$: misma regla que el sur (§3.4), con la distancia al punto $p$:
  - $n_{p,m}$ = número de tormentas (≥ 34 nudos) cuyo primer punto a $\le 200$ km de $p$ cae en el mes $m$, de 1966 a 2025;
  - $\hat\lambda_{p,m}=n_{p,m}/60$ y $P(N_{p,m}\ge1)=1-e^{-\hat\lambda_{p,m}}$.

**Supuestos**
- El corte del Radar es semanal y se aplica a una ocupación mensual. Un mes promedia sus semanas, así que el corte p50
  sigue separando meses llenos de meses con espacio; el p90 casi nunca se alcanza en un promedio mensual.
- Fuera del horizonte del pronóstico se usa lo típico de 2022–2025. En la Riviera Maya eso es más alto que el pronóstico,
  porque el pronóstico supone que la baja de 2026 sigue; la página lo dice.

**Cómo se resolvió**
1. Se agregó la Riviera Maya a las series (`serie_norte`) y se corrió la Fase 5 completa. Las tablas del sur y de Cancún
   salieron idénticas.
2. Se calculó $q_{0.50}$ con `torre.radar.markov.estados`.
3. Para cada mes elegible se tomó $o_{l,t}$, se comparó con el corte y, si es alta, se buscó $l^*$.
4. Las tormentas por punto se contaron sobre HURDAT2 (Silver) con haversine.

**Ejemplos resueltos a mano (números reales)**
- *Cancún, enero de 2027:* $o=\hat y=78.27\ \%\ge71.16\ \%$, así que es **alta**.
  - Ese mes, en el sur: Chetumal $S=0.93$ (tranquila); Bahía $S=1.25$ (alta); Ruta $S=1.61$ (alta).
  - Por lo tanto, $l^*=$ **Chetumal**.
- *Cancún, octubre de 2026:* $o=65.25\ \%<71.16\ \%$, así que es **tranquila**.
- *Riviera Maya, diciembre de 2027* (fuera del horizonte): $\bar o=80.6\ \%\ge71.16\ \%$, así que es **alta**, con
  $l^*=$ Chetumal.
- *Tormentas en Cancún, octubre:* $n=13$, así que $\hat\lambda=13/60=0.2167$ y $P=1-e^{-0.2167}=0.195$ (**19.5 %**).
  - En el año: 45 tormentas, así que $P(\ge1)=1-e^{-45/60}=0.528$.
  - En Chetumal: 31 tormentas, 0.403.
- *Otro mes en el norte:* los meses secos de Cancún (noviembre a abril, lluvia menor que la mediana de 86.5 mm) tienen
  ocupación típica de 75.6 % a 80.7 %, todos ≥ 71.16 %. Los meses con menos de 71.16 % son septiembre (64.5 %) y octubre
  (67.5 %), que tienen tormenta ≥ 9 %. **No hay candidato**, así que solo se sugiere otro lugar.

**Dónde está en el código**
`backend/torre/pronostico/calendario.py` (`nivel_norte`, `corte_radar`, `tormentas_punto`, `ocupacion_tipica`,
`recomendar`) y `backend/torre/pronostico/series.py` (`serie_norte`). Pruebas: `tests/test_planeador.py` y
`tests/test_pronostico.py`.

## 4. Investigación de Operaciones: reparto del presupuesto en dos etapas ✅
Decisiones en `docs/decisiones/19-presupuesto.md`.

### 4.1 Ecuaciones
**Conjuntos.**
- $m$: los meses con pronóstico (oct-2026 a jun-2027).
- $l$: los 3 lugares del sur.
- $c$: los canales, Google y Facebook.
- $s$: los escenarios malo, probable y bueno, con $p_s$ = 0.3, 0.4 y 0.3.

**Parámetros.**
- $r_c=\dfrac{\text{conversión}_c}{\text{CPC}_c^{USD}\times TC}$: conversiones por peso.
- $D_{s,m,l}$: escenario del Monte Carlo.
- $C_l$: capacidad probada.
- $B=250{,}000\times\frac{|M|}{12}$.
- $U=\max_c r_c\,B$.

**Variables.**
- $x_{m,l,c}\ge0$: pesos.
- $y_{s,m,l}\in\{0,1\}$: anuncio encendido.
- $w_{s,m,l}\ge0$: conversiones que sí ocurren.

$$v_{m,l}=\sum_c r_c\,x_{m,l,c}\qquad\textbf{Paso 1:}\ \ z^*=\max\ \sum_s p_s\sum_{m,l}w_{s,m,l}$$
Sujeto a:
- $\sum_{m,l,c}x_{m,l,c}\le B$ (presupuesto).
- $x_{m,l,c}=0$ si $(m,l)$ es temporada alta (planeador, Fase 5).
- $D^{p50}_{m,l}+v_{m,l}\le C_l$ (capacidad probada).
- $\sum_{m,c}x_{m,l,c}\ge0.15\,B\ \ \forall l$ (equidad).
- $\sum_{m,l}x_{m,l,c}\le0.70\,B\ \ \forall c$ (canal).
- Recurso: $D_{s,m,l}+v_{m,l}\le C_l+M_{s,m,l}(1-y_{s,m,l})$, $\ w_{s,m,l}\le v_{m,l}$, $\ w_{s,m,l}\le U\,y_{s,m,l}$,
  con $M_{s,m,l}=\max(D_{s,m,l}+U-C_l,0)$.

**Paso 2 (desempate lexicográfico, proporcional al espacio).** Se agrega $\sum p_s w\ge z^*(1-10^{-7})$ y se resuelve:
$$\min\sum_{m,l,c}\left|x_{m,l,c}-\pi_{m,l}\sum_{m',l'}x_{m',l',c}\right|,\qquad \pi_{m,l}=\frac{\text{libre}_{m,l}}{\sum_{\text{permitidas}}\text{libre}},\quad \text{libre}_{m,l}=1-\frac{D^{p50}_{m,l}}{C_l}$$
- Permitida: no es temporada alta y $D^{p90}_{m,l}<C_l$.
- El valor absoluto se linealiza con $d\ge x-\text{meta}$, $d\ge\text{meta}-x$.

**Precio sombra** de la regla $i$: $\lambda_i=\partial z^*/\partial b_i$, del LP con las $y$ fijas.

**Frontera de Pareto** ($\varepsilon$-restricción): $D^{p50}_{m,l}+v_{m,l}\le\varepsilon\,C_l$ para $\varepsilon\in\{1,\dots,0.3\}$.
Si para algún $(m,l)$ no cabe, $x_{m,l,\cdot}=0$.

### 4.2 Supuestos
- Costos por clic y conversión de *Travel*: promedios de anunciantes de EE. UU. (WordStream 2025).
- La conversión de Facebook para turismo no está publicada. Base: 5.75 %, con barrido de 3 % y 6.38 %.
- Cada conversión es un visitante (cota alta para la capacidad).
- La respuesta es lineal: no hay dato de cómo se agota la audiencia.
- Los escenarios se resumen con p10/p50/p90 y pesos 30/40/30 (regla de Swanson).
- La "capacidad" es la capacidad probada, el mes más alto de la historia (Fase 5).

### 4.3 Cómo se resolvió
1. Se leen los parámetros de archivos: D13 (benchmarks), FRED (último mes completo: 17.06) y Gold de la Fase 5.
2. PuLP arma el MILP: 54 variables continuas $x$, 81 binarias $y$ y 81 continuas $w$.
3. CBC resuelve por *branch-and-bound* con simplex en cada nodo.
4. Se fija $z^*$ y se resuelve el paso 2 (LP).
5. Para los precios sombra se fijan las $y$, se quita el paso 2 y se lee el dual de cada restricción.
6. El costo de cada regla se mide resolviendo sin ella. Pareto y sensibilidad resuelven el modelo completo con el
   supuesto movido.

### 4.4 Ejemplos resueltos a mano (números reales)
- $r_{Google}=\dfrac{0.0575}{2.12\times17.0609}=\dfrac{0.0575}{36.169}=0.001590$, es decir, **1.59 visitantes por cada $1,000**.
- $r_{Facebook}=\dfrac{0.0575}{0.51\times17.0609}=\dfrac{0.0575}{8.701}=0.006608$, es decir, **6.61 por cada $1,000**.
- Facebook rinde más y se lleva su tope:
  - $0.70\times187{,}500=131{,}250$ pesos, que dan $131{,}250\times0.006608=867.3$.
  - Google recibe $56{,}250$ pesos, que dan $56{,}250\times0.001590=89.4$.
  - En total, $z^*=$ **956.8 visitantes**, y el código da 956.78.
- **Precio sombra del tope de Facebook:** $0.006608-0.001590=0.005019$. Cada peso que pasa de Google a Facebook suma
  0.005 visitantes, y quitar el tope suma $0.30\times187{,}500\times0.005019=282.3$ (+29.5 %).
- **Reparto proporcional:**
  - Ruta, oct-2026: libre $=1-3{,}688/10{,}465=0.6476$.
  - Con $\sum\text{libre}=8.0004$ en las 20 celdas permitidas, $\pi=0.6476/8.0004=0.0809$.
  - $0.0809\times131{,}250=$ **$10,624** en Facebook y $0.0809\times56{,}250=$ **$4,553** en Google. El código da
    $10,624 y $4,553 (`presupuesto_plan.parquet`).

### 4.5 Dónde está en el código
`backend/torre/campana/presupuesto.py`:
- `resolver` (modelo, pasos 1 y 2);
- `precios_sombra`, `costo_de_reglas`, `pareto` y `sensibilidad`.

Notebook: `notebooks/05_optimizacion.ipynb`. Pruebas: `tests/test_presupuesto.py`.

## 5. A5 Torre en vivo: señales semanales, Isolation Forest y reglas ✅
Decisiones en `docs/decisiones/20-torre-en-vivo.md`.

### 5.1 Ecuaciones
- **Estado del norte:** $\text{saturado}_w \iff o_w\ge q_{0.90}(o)$, con $q_{0.90}=85.92\,\%$ (Radar, Fase 4).
  Promedio móvil: $\bar o_w=\frac14\sum_{k=0}^{3}o_{w-k}$ (ventana deslizante de Spark).
- **Isolation Forest:** $s(x)=2^{-E[h(x)]/c(n)}$, con $c(n)=2H(n-1)-\dfrac{2(n-1)}{n}$ y $H(k)\approx\ln k+0.5772$.
  - $h(x)$: número de cortes al azar que aíslan a $x$.
  - Cada bosque usa $n=\min(256,\ \text{semanas de entrenamiento})$.
  - **Semana rara:** $s(x_w)>q_{0.95}\{s(x_i): i\ \text{en entrenamiento}\}$.
  - Entrenamiento de ventana creciente: todas las semanas desde 2019 hasta antes del año que se califica.
- **Llegadas:** $\text{arriba}_m\iff y_m>\hat y^{\,90\%}_{\max,m}$, con el pronóstico a 1 mes del modelo elegido.
- **Regla del sur** (lugar $l$, semana $w$):
  $$a_{l,w}=\begin{cases}\text{temporada alta}&(m(w),l)\in\mathcal A\\\text{fuera del plan}&(m(w),l)\notin\text{plan}\\\text{pausado}&\text{tormenta}_w\ \lor\ \text{raro}_{p(l),w}\ \lor\ \text{arriba}_{l,m(w)-1}\\\text{encendido}&\text{en otro caso}\end{cases}$$
  - **Dinero:** $g_{l,w}=\big(b_{l,w}+A_{l,w-1}\big)\,\mathbb 1[\text{encendido}]$, $\ A_{l,w}=\big(A_{l,w-1}+b_{l,w}\big)\,\mathbb 1[\text{pausado}]+A_{l,w-1}\,\mathbb 1[\text{alta o fuera}]$.
  - $b_{l,w}=\dfrac{\text{pesos del mes}}{\#\text{lunes del mes}}$.
- **Regla del norte:** si $\text{saturado}_w$ en Cancún o Riviera Maya, se anuncia el sur en
  $\arg\max_{l:\,a_{l,w}=\text{encendido}}\text{libre}_{m(w),l}$.

### 5.2 Supuestos
- El dato mensual de llegadas se conoce al empezar el mes siguiente (en la realidad tarda 1–2 meses).
- Sin dato de tormentas (2026) no pausa: no hay evidencia para pausar.
- El plan de la Fase 6 se aplica por mes del año a 2022–2026.
- La época del año entra como $\sin$ y $\cos$ de la semana, para no marcar raro un septiembre solo por ser lluvioso.

### 5.3 Cómo se resolvió
1. Se arman las señales con pandas y Spark (ventana deslizante).
2. Un bosque de 300 árboles por punto y año (scikit-learn, semilla 0).
3. Se escribe un JSON por semana con hora creciente.
4. Spark Structured Streaming lee con `maxFilesPerTrigger = 1` y `trigger(availableNow=True)`. En cada lote
   (`foreachBatch`) el motor decide y guarda el arrastre en memoria.
5. Se comprueba que llegaron 239 lotes en orden y que el dinero gastado es igual al planeado.

### 5.4 Ejemplos resueltos a mano (números reales)
- **Isolation Forest, Chetumal, semana del 14-oct-2024** (Nadine):
  - Llovieron 148.7 mm, con 65.4 mm el peor día.
  - Con 260 semanas de entrenamiento, $n=256$ y $c(256)=2(\ln255+0.5772)-\frac{2\cdot255}{256}=12.245-1.992=10.25$.
  - El bosque da $s=0.712$, que es mayor que el corte $q_{0.95}=0.543$: **rara**.
  - $E[h]=-c\cdot\log_2 s=-10.25\times\log_2 0.712=-10.25\times(-0.490)=$ **5.0 cortes** para aislarla, contra ~10 de una
    semana normal.
- **Dinero:**
  - Octubre tiene 4 lunes. Si un lugar tiene \$4,000 en el mes, $b=\$1{,}000$ por semana.
  - Si la semana 1 se pausa, $A=1{,}000$. En la semana 2, encendida, se gastan $1{,}000+1{,}000=\$2{,}000$ y $A=0$.
  - Es la prueba `test_clima_raro_pausa_solo_su_punto_y_el_dinero_pasa_a_la_siguiente`.

### 5.5 Dónde está en el código
`backend/torre/envivo/`:
- `senales.py`: `norte`, `tormentas`, `anomalias_clima`, `llegadas`;
- `motor.py`: `decidir`, `motivos_pausa`;
- `torre.py`: `reproducir`.

Notebook: `notebooks/06_torre_en_vivo.ipynb`. Pruebas: `tests/test_envivo.py`.

## 6. Campaña: minería de texto 🕓
- **Peso de un término**: $\text{tfidf}(t,d)=tf(t,d)\cdot\log\dfrac{N}{df(t)}$
- **Reglas de asociación**:
  - soporte: $sop(A)=\dfrac{\#\{A\}}{N}$
  - confianza: $conf(A\Rightarrow B)=\dfrac{sop(A\cup B)}{sop(A)}$
  - lift: $\text{lift}=\dfrac{conf(A\Rightarrow B)}{sop(B)}$


### 6.1 Vitrina: personas al día, mejor mes de una ruta y distancia en línea recta ✅
Decisiones en `docs/decisiones/16-vitrina-idiomas-noche.md`.

**Ecuaciones**
- **Personas al día en las zonas de la Ruta** en el último año completo $a$:
  $$\bar v=\frac{1}{365}\sum_{z\in\{K,D,I\}}\sum_{m=1}^{12} v_{z,a,m}$$
- **Mejor mes de una ruta** con lugares $L$ (los que tienen serie) y punto de clima $p$:
  $$m^*=\arg\min_{m\in\mathcal M}\ \frac{1}{|L|}\sum_{l\in L}S_{l,m},\qquad \mathcal M=\{m:\ \max_{l\in L}S_{l,m}<1.20,\ P(N_m\ge1)<0.09,\ \bar L_{p,m}<\operatorname{mediana}_k\bar L_{p,k}\}$$
  Si $L=\varnothing$ (Maya Ka'an), $m^*=\arg\min_{m}\bar L_{p,m}$ entre los meses sin temporada de tormentas.
- **Distancia** entre paradas: haversine (§3.0) entre los centros del Censo, **en línea recta**.

**Supuestos**
- La cifra al día es un promedio del año: hay días con más gente y días con menos.
- La distancia en línea recta subestima la de carretera. Se declara en la página.

**Ejemplos resueltos a mano (números reales)**
- *Pirámides:* en 2025, 21,850 (Kohunlich) + 6,592 (Dzibanché) + 38,186 (Ichkabal) = 66,628, y 66,628 ÷ 365 = 182.5,
  así que son **183 personas al día**.
- *Ruta "Bahía y pirámides":*
  - Lugares con serie: Chetumal, Bahía y Ruta. Clima de Chetumal, con lluvia mediana de 97 mm.
  - Meses sin tormenta (< 9 %) y secos: de enero a mayo y diciembre.
  - Se quitan los meses donde algún lugar tiene $S\ge1.20$: enero (Ruta 1.61), marzo (Ruta 1.37), abril (Bahía 1.34) y
    diciembre (Bahía 1.40).
  - Quedan febrero (promedio 1.04) y mayo (promedio de 0.68, 0.88 y 0.91 = 0.82). El mínimo es **mayo**.
- *Distancias:* Chetumal → Calderitas **8 km**; Calderitas → Kohunlich **59 km** (en línea recta).

**Dónde está en el código**
`backend/torre/campana/vitrina.py` (`experiencias`, `rutas`, `_mejor_mes`). Pruebas: `tests/test_vitrina.py`.

### 6.2 Estrellas oficiales y mes menos lleno del norte ✅
Decisiones en `docs/decisiones/17-norte-en-la-pagina.md`.

**Ecuaciones**
- **Parte de cuartos de la categoría** $k$ en el centro $c$, con $Q_{c,k}$ = cuartos-noche disponibles en 2024
  (Compendio DataTur, tabla 5_2):
  $$p_{c,k}=\frac{Q_{c,k}}{\sum_j Q_{c,j}}\times100,\qquad \bar C_c=\frac{\sum_j Q_{c,j}}{366}$$
  Se divide entre los cuartos-noche y no se promedian porcentajes.
- **Mes menos lleno de una ruta del norte:** $m^*=\arg\min_{m\in\mathcal M}\bar o_{l,m}$, con
  $\mathcal M=\{m: P(N_{p,m}\ge1)<0.09,\ \bar L_{p,m}<\operatorname{mediana}\}$. Es la ocupación típica de §3.6, con las
  tormentas alrededor de su punto.

**Ejemplos resueltos a mano (números reales)**
- *Cancún:*
  - Hay 8,813,675 cuartos-noche de 5 estrellas de un total de 13,006,487, así que $p=67.8\ \%$.
  - $\bar C=13{,}006{,}487/366=35{,}537$ cuartos.
- *Ruta "Cancún en 2 días":*
  - Los meses secos y sin tormentas son de enero a abril y diciembre.
  - Sus ocupaciones típicas: 75.9, 79.1, 80.7, 75.6 y 78.7 %. El mínimo es **abril (75.6 %)**, y se muestra como 76 %.

**Dónde está en el código**
`backend/torre/campana/estrellas.py` (`tabla`, `estrellas`) y `vitrina.py` (`_mejor_mes_norte`). Pruebas:
`tests/test_vitrina.py`.
