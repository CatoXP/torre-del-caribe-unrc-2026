# 10 — Datos limpios para el Pronóstico: huracanes, clima y tipo de cambio (Fase 2, cierre de la parte que usa la Fase 5)

Autor: **Brandon Uriel García Sánchez** · 30-sep-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Por qué ahora
La auditoría de las Fases 1–4 (`09-auditoria-fases-1-4.md`) encontró que la Fase 2 estaba incompleta. Tres fuentes que
necesita el Pronóstico seguían sin limpiar en Bronze: huracanes (D9), clima (D8) y tipo de cambio (D10). Sin ellas no
se pueden hacer el modelo de Poisson, la regresión con clima ni la sensibilidad al dólar. Esta nota cierra esa parte.
Nacionalidades, reseñas, vuelos y cruceros se limpian antes de la Fase 8, que es la que los usa.

## 1. Huracanes → `datos/silver/huracanes/` ✅
Código: `backend/torre/base/silver_huracanes.py` · Prueba: `tests/test_silver_fase5.py`.

**Decisión de Brandon (30-sep-2026):** una tormenta **afecta al sur** si al menos un punto de su trayectoria pasa a
**≤ 200 km de Chetumal** con viento **≥ 34 nudos** (tormenta tropical o huracán) y es de **1966 en adelante**.

| Opción | Eventos | Tasa por año | Por qué sí o por qué no |
|---|---:|---:|---|
| **200 km · ≥ 34 kt · desde 1966 (elegida)** | **31 en 60 años** | **0.517** | Cubre Chetumal, Bahía, la ruta arqueológica y Maya Ka'an sin sumar tormentas que solo pasan por Honduras o el norte de Yucatán |
| 100 km · ≥ 34 kt · desde 1966 | 13 | 0.217 | Muy pocos eventos para estimar una tasa por mes (hay meses con 0 y 1) |
| 300 km · ≥ 34 kt · desde 1966 | 59 | 0.983 | Mete tormentas que no traen viento fuerte a los 5 lugares |
| 200 km · ≥ 34 kt · desde 1851 | 82 en 175 años | 0.469 | Antes de los satélites se perdían tormentas en el mar: la tasa sale baja |

**Resultado:** 55,524 puntos de trayectoria de 1,988 tormentas, de 1851 a 2025. Se guardan todos, con la distancia a
Chetumal y banderas, para que el radio o el umbral se puedan cambiar en la Fase 5 sin volver al texto crudo.

Los 31 eventos se concentran de **agosto a octubre** (9 + 8 + 6 = 23 de 31, el 74 %). Entre ellos: Carmen (1974, 125
nudos a 15.3 km de Chetumal), Dean (2007, 150 nudos, tocó tierra a 67 km), Keith (2000) y Ernesto (2012).

**Reglas de limpieza**
1. **Faltantes oficiales:** en HURDAT2, −99 en viento y −999 en presión significan "sin dato". Se guardan vacíos, no como
   números.
2. **2 líneas mal escritas en el archivo oficial**, de 55,524:
   - 1969-09-29, 06 UTC: `63.3N    7.5E`, sin coma entre latitud y longitud. Se lee completa.
   - 1975-12-07, 00 UTC: `38.83,  51.0W`, latitud sin hemisferio. **La latitud queda vacía**, no se adivina.

   Las dos llevan `formato_irregular_flag` y están a más de 3,000 km de Chetumal, así que no cambian el conteo.
   *Hallazgo al programar:* la exploración inicial saltaba la segunda línea y contaba 55,523 puntos. El código final no
   salta nada: si una línea no se entiende, se detiene (regla de oro 5).
3. **Fecha:** se guarda como fecha, más la hora UTC como número (1330 = 13:30). PySpark en Windows no convierte marcas de
   tiempo anteriores a 1970.

## 2. Clima → `datos/silver/clima_diario/` y `datos/silver/clima_horario/` ✅
Código: `backend/torre/base/silver_clima.py`.

| Tabla | Filas | Periodo | Variables |
|---|---:|---|---|
| clima_diario | 224,232 | 1-ene-1950 → 27-sep-2026 | temperatura máxima (°C), lluvia del día (mm), viento máximo (km/h) |
| clima_horario | 542,784 | 1-ene-2019 → 27-sep-2026 | temperatura (°C), lluvia (mm), viento (km/h) |

**Reglas**
1. **Dos tablas, no una.** La diaria da 76 años para medir la temporada de lluvias, y es la variable del Pronóstico
   mensual. La horaria alimenta la Torre en vivo (Fase 7).
2. **Hora local.** El crudo horario viene en UTC y el diario, en hora de Cancún (revisado en los 128 archivos). Quintana
   Roo usa UTC−5 fijo desde 2015, así que la hora local es la UTC menos 5 horas.
3. **Revisión de huecos:** 0 vacíos en los 128 archivos. Si algún día llega uno, se conserva vacío con `sin_dato_flag`.
4. **Reanálisis, no estación.** Open-Meteo entrega ERA5, un modelo meteorológico que asimila observaciones. Se declara en
   la columna `fuente_tipo`. No lleva `_est`, porque es un producto oficial y no un cálculo del proyecto.
5. **Papel de cada punto (regla de oro 9):**
   - promovidos: Chetumal, Kohunlich (ruta arqueológica) y Felipe Carrillo Puerto (Maya Ka'an);
   - referencia: Cancún, Playa del Carmen y Tulum;
   - excluidos: Bacalar y Cobá.

   *Hueco declarado:* no hay punto de clima propio para Laguna Milagros–Xul-Ha ni para la Bahía de Calderitas. Se usa
   el punto de Chetumal, que está a 7.7 km de Calderitas, a 13.6 km de Huay-Pix y a 18.9 km de Xul-Ha (coordenadas del
   Censo 2020, `datos/silver/iter`). Cuando se use, se dirá que es el clima de Chetumal.

**Primer patrón (dato real):** en Chetumal, la lluvia media de 1991–2020 va de 26 mm en febrero a 195 mm en junio y 188–189 mm
en septiembre y octubre. La temporada de lluvias coincide con la de huracanes.

## 3. Tipo de cambio e inflación de EE. UU. → `datos/silver/fred_diario/` y `datos/silver/fred_mensual/` ✅
Código: `backend/torre/base/silver_fred.py`.

- **Tipo de cambio diario (DEXMXUS):** 8,575 días hábiles, del 8-nov-1993 al 18-sep-2026. 336 días vienen vacíos
  (feriados de EE. UU.) y **se quedan vacíos**, con `sin_dato_flag`. *Opción descartada:* copiar el día anterior, porque
  inventa una cotización que no existió.
- **Promedio mensual:** solo con los días observados, guardando cuántos fueron (`n_dias_observados`). Agosto de 2026:
  21 días, 17.0609 pesos por dólar. *Opción descartada:* usar el último dato del mes, porque depende de un solo día.
- **Mes en curso:** septiembre de 2026 lleva `mes_incompleto_flag`, porque su promedio (13 días) todavía cambia.
- **Inflación de EE. UU. (CPIAUCSL):** índice mensual desde 1947. Sirve para pasar a pesos constantes los costos
  publicitarios en dólares (D13) en la Fase 6.

## Evidencia de que funciona
`tests/test_silver_fase5.py` tiene 13 pruebas en verde:
- 55,524 puntos y 1,988 tormentas;
- las 2 líneas irregulares, con la latitud vacía y sin inventar;
- 1° de latitud = 111.19 km, calculado a mano;
- 31 eventos y su reparto por mes, con Dean y Carmen;
- 224,232 días y 542,784 horas, sin huecos, con la hora local a UTC−5;
- los 336 feriados vacíos;
- el promedio de agosto de 2026, recalculado directo del CSV crudo.

## Consecuencia
La Fase 5 ya tiene sus tres insumos externos limpios. Faltan de la Fase 2, y no los usa la Fase 5:
- nacionalidades, reseñas, vuelos (AFAC) y cruceros, para la Fase 8;
- el modelo estrella con su diccionario de datos, y DuckDB, para la Fase 9.

Las ecuaciones y los ejemplos resueltos a mano están en `docs/metodologia/ECUACIONES.md` §3.0.
