# 11 — A3 Pronóstico: ¿cuándo conviene ir y cuánto invertir? (Fase 5) · LISTA PARA REVISIÓN

Autor: **Brandon Uriel García Sánchez** · 30-sep-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Qué pregunta responde
El Radar (Fase 4) dice **dónde** hay presión **hoy**. El Pronóstico dice **cuándo**, en los próximos 1 a 12 meses:
- cuántos visitantes se esperan en cada lugar cada mes, con un rango del 90 %;
- en qué meses hay riesgo de tormenta;
- qué pasa en un escenario malo, uno probable y uno bueno.

Con eso, la campaña decide en qué meses anunciar cada lugar y cuánto dinero reservar (Fase 6).

## Decisión 1 — Qué se pronostica (Brandon, 30-sep-2026): "Medidas + norte"
El sur no tiene ocupación hotelera oficial en 2025–2026 (hallazgo de la Fase 1). Por eso se pronostican **solo series
medidas que llegan a 2026**:

| Serie | Lugar | Papel | Meses | Periodo |
|---|---|---|---:|---|
| Visitantes INAH a Oxtankah | Bahía Calderitas–Oxtankah | promovida | 127 | ene-2016 → jul-2026 |
| Visitantes INAH a Kohunlich + Dzibanché + Ichkabal | Ruta arqueológica del sur | promovida | 127 | ene-2016 → jul-2026 |
| Cruces desde Belice | Chetumal | promovida | 90 | ene-2019 → jun-2026 |
| Ocupación hotelera (cuartos ocupados ÷ disponibles) | Cancún | **referencia**: es el público de la campaña | 55 | ene-2022 → jul-2026 |

**Opciones descartadas**
- *Solo INAH:* Chetumal se quedaría sin serie propia y no se sabría en qué meses se llena el norte, que es cuando más
  gente se puede redirigir al sur.
- *Estimar la ocupación del sur 2025–2026 (`_est`):* contradice la decisión de la Fase 3 de mostrar "sin dato oficial"
  en lugar de estimar, y solo hay 36 meses de Chetumal (2022–2024), pocos para aprender la temporada.

**Huecos declarados**
- Maya Ka'an + Kantemó y Laguna Milagros–Xul-Ha no tienen serie mensual propia que llegue a 2026.
- El Tren Maya tiene solo 20 meses en Chetumal y 23 en Maya Ka'an. Para aprender la temporada hacen falta al menos 24,
  así que se usará como variable y no se pronostica.
- Esos lugares recibirán solo el calendario de lluvia y huracanes (Silver, `10-silver-fase5.md`).

## Decisión 2 — Meses que no entrenan (Brandon, 30-sep-2026): "Hueco + forma del año"
Un mes cerrado no es "cero demanda". Si el modelo aprendiera de esos ceros, creería que en abril puede haber 0
visitantes por temporada. Esos meses **se marcan y no entrenan**, pero su valor observado **se conserva**. El modelo
aprende la **forma del año** (qué meses suben o bajan) de todos los años abiertos, y el **nivel** actual de los meses
posteriores a la reapertura.

**Opciones descartadas**
- *Solo desde la reapertura:* son 19 meses, menos de los 24 necesarios para aprender la temporada.
- *Ceros como dato real:* enseña una temporada falsa.

**Reglas, comprobadas con los datos** (`backend/torre/pronostico/series.py`):
1. **Cierre:** la zona reporta 0 visitantes. En los datos: todas las zonas en abr–ago-2020 (COVID); Oxtankah de oct-2023
   a oct-2024 y la Ruta de feb-2024 a ene-2025 (obras).
2. **Mes parcial:** el mes justo antes de un cierre o justo después de reabrir. Ejemplos: Oxtankah reabre en nov-2024
   con 81 visitantes (dic-2024: 1,522); Dzibanché reabre en feb-2025 con 249.
3. **Pandemia:**
   - INAH, mar-2020 → dic-2021. En 2021 Kohunlich tuvo 22,425 visitantes, el 52 % de 2019, con aforo limitado. En 2022
     ya tuvo el 81 %.
   - Belice, mar-2020 → **jun-2022**. La frontera estuvo casi cerrada: de 57 a 2,864 cruces al mes, entre el 0 % y el 7 %
     del mismo mes de 2019. Reabrió en feb-2022 (41.7 %) y siguió recuperándose de marzo a junio (65.1, 69.5, 80.2 y
     82.2 %). Desde jul-2022 no bajó de 86 %. *Ajuste decidido por Brandon el 30-sep-2026* tras la pieza 2 (ver abajo):
     la primera versión terminaba en feb-2022.

   Estos límites son parámetros visibles en el código (`PANDEMIA_INAH`, `PANDEMIA_BELICE`).
4. **Región = suma de sus zonas.** Si una zona que ya existía está cerrada o en mes parcial, el mes de toda la región se
   marca. En ene-2025 Kohunlich ya había abierto (750 visitantes), pero Dzibanché seguía cerrada: sumar solo las
   abiertas bajaría el total de forma artificial. Ichkabal abrió en ene-2025; antes no existía, así que su ausencia no
   es un cierre.

**Resultado (pieza 1, `datos/gold/pronostico_series.parquet`)**

| Serie | Meses | Entrenan | Cierre | Mes parcial | Pandemia |
|---|---:|---:|---:|---:|---:|
| Bahía Calderitas–Oxtankah | 127 | 90 | 18 | 4 | 15 |
| Ruta arqueológica del sur | 127 | 91 | 18 | 4 | 14 |
| Chetumal · Belice | 90 | 62 | 0 | 0 | 28 |
| Cancún (referencia) | 55 | 55 | 0 | 0 | 0 |

**Consecuencia para declarar.** Las zonas reabrieron por debajo de su nivel anterior: Kohunlich tuvo 21,850 visitantes
en 2025 contra 42,813 en 2019. Por eso el nivel se toma de los meses posteriores a la reapertura y no del promedio
histórico.

Pruebas: `tests/test_pronostico.py`, 9 pruebas, cada una con un mes real revisado a mano.

## Pieza 2 — Forma del año (Minería) ✅
Código: `backend/torre/pronostico/forma.py` · Salidas: `datos/gold/pronostico_forma_anio.parquet` y
`pronostico_fuerza_estacional.parquet` · Ecuaciones y ejemplo a mano: `ECUACIONES.md` §3.2.

**Decisión técnica: descomposición clásica multiplicativa sobre años completos, en lugar de STL.** El plan decía STL, pero
STL necesita una serie continua. Las nuestras tienen huecos, así que STL solo podría usar el tramo continuo más largo
(unos 50 meses) y tiraría los años posteriores, en contra de la decisión 2 ("la forma del año sale de todos los años
abiertos"). STL se conserva como **segunda opinión**. Es multiplicativa porque la temporada escala con el nivel: Kohunlich
reabrió a la mitad de su nivel de 2019.

| Serie | Años completos | Fuerza de la temporada | Más alto | Más bajo | Coincide con STL | Parecido con Cancún |
|---|---|---:|---|---|---:|---:|
| Ruta arqueológica del sur | 2016–2019, 2022, 2023 | 0.793 | ene 1.61 | sep 0.50 | 0.955 | 0.834 |
| Bahía Calderitas–Oxtankah | 2016–2019, 2022, 2025 | 0.684 | dic 1.40 | sep 0.65 | 0.960 | 0.716 |
| Chetumal · Belice | 2019, 2023–2025 | 0.655 | dic 1.17 | feb 0.87 | 0.847 | 0.257 |
| Cancún (referencia) | 2022–2025 | 0.714 | mar 1.08 | sep 0.87 | 0.966 | — |

**Hallazgos**
- Las zonas del sur se mueven con el norte (0.83 y 0.72); Chetumal-Belice, no (0.26).
- Septiembre es el mes más bajo en las zonas y en Cancún, y coincide con el pico de tormentas (`10-silver-fase5.md`).

**Belice: por qué STL no coincidía y decisión de Brandon (30-sep-2026).** Con la pandemia terminando en feb-2022, el tramo
continuo de Belice empezaba en mar-2022, cuando la frontera recién reabría. De marzo a junio los cruces iban en 65.1 %,
69.5 %, 80.2 % y 82.2 % del mismo mes de 2019. STL confundía esa recuperación con temporada: ponía marzo en 0.73, cuando
los años completos lo ponen entre 0.92 y 1.18. La correlación con este método era de 0.446.

**Decisión:** marzo–junio de 2022 cuentan como pandemia (recuperación, no temporada). Belice entrena 62 meses en lugar
de 66. Con eso el tramo de STL empieza en jul-2022 y la correlación sube a **0.847**. Desde julio de 2022 los cruces no
bajaron de 86 % del nivel de 2019.

- *Opción descartada:* dejar el fin de la pandemia en feb-2022. Conserva 4 meses más, pero entrena con cifras de
  recuperación.
- *Precisión:* la opción se presentó como "cuando los cruces vuelven a ≥ 80 %". Mayo de 2022 ya estaba en 80.2 %, así
  que por ese criterio literal el corte sería abril. El corte de junio se sostiene en el salto a ≥ 86 % desde julio.
- El índice estacional de esta pieza no cambia, porque 2022 no es un año completo de Belice.

**Descartado:** marcar "meses de oportunidad" cuando Cancún pasa de 1.00 y el sur queda abajo. Cancún varía poco (0.87
a 1.08) y la regla cambiaba con diferencias de 0.02. En su lugar se mide el parecido de las dos formas del año, sin
umbral.

## Pieza 3 — Modelos, rango del 90 % y elección (ML) ✅
Código: `modelos.py` (origen móvil), `intervalos.py` (conformal) y `seleccion.py` (elección y pronóstico final).
Salidas en `datos/gold/`: `pronostico_backtest`, `pronostico_metricas`, `pronostico_cobertura`, `pronostico_eleccion` y
`pronostico_mes`. Ecuaciones, tabla completa y ejemplos a mano: `ECUACIONES.md` §3.3.

**Cómo se comparó.** Origen móvil: en cada mes del pasado se pronostican los 12 siguientes solo con lo que se sabía
entonces. Se evalúan únicamente los pares que los 5 modelos pudieron pronosticar: 366 en la Bahía, 378 en la Ruta, 366
en Belice y 438 en Cancún. La forma del año se recalcula en cada origen con los años completos anteriores, sin ver el
futuro.

**Los cinco modelos**
- Línea base: el mismo mes del año anterior.
- Holt-Winters con forma del año fija, con tendencia amortiguada (la del plan).
- Holt-Winters sin tendencia.
- Regresión con clima: nivel por tramo + mes + anomalía de lluvia + tormenta.
- Gradient Boosting con rezagos.

**Decisión técnica: Holt-Winters con forma del año fija.** El Holt-Winters clásico necesita al menos 24 meses seguidos, y
desde las reaperturas solo hay 20 (Bahía) y 17 (Ruta). Por eso la temporada sale de la pieza 2 y el modelo solo sigue el
nivel. La variante sin tendencia se agregó después de ver que la tendencia se disparaba: en la Bahía, a 7–12 meses tuvo
33 % de error contra 13 % de la línea base, y llegó a pronosticar −240 visitantes (origen may-2025). Se declara que esta
variante nació de ese diagnóstico.

**Decisión de Brandon (30-sep-2026): "Menor error con rango ≥ 80 %".** Por serie, se elige el modelo de menor error
entre los que tienen un rango del 90 % que se cumple al menos 80 de cada 100 veces.

| Serie | Modelo elegido | Error vs base | MAPE | Cobertura real del rango del 90 % | Rango típico |
|---|---|---:|---:|---:|---:|
| Bahía Calderitas–Oxtankah | Regresión con clima | 0.898 | 15.7 % | 91.3 % | ±43 % |
| Ruta arqueológica del sur | Regresión con clima | 0.737 | 21.6 % | 80.3 % | ±51 % |
| Chetumal · Belice | Regresión con clima | 0.820 | 11.0 % | 94.1 % | ±26 % |
| Cancún (referencia) | Línea base | 1.000 | 3.8 % | 89.3 % | ±10 % |

**Opciones descartadas**
- *Menor error sin importar el rango:* en la Ruta elegiría Holt-Winters sin tendencia (0.639), pero su rango solo
  acierta 72 de cada 100 veces, y habría dos modelos que explicar.
- *Un solo modelo para todo:* en Cancún la regresión comete 58 % más error que repetir el mismo mes del año anterior.

**Hallazgos que se declaran**
- **La Ruta no llega a 90 % de cobertura con ningún modelo** (72–81 %). La falla se concentra en 2023: la cobertura de
  ese año fue de 67 % y los modelos pronosticaron 12 % de más, porque las visitas cayeron 10.7 % (de 46,295 a 41,322)
  sin aviso en la historia. En 2025–2026 la cobertura vuelve a 86–100 %.
- **El clima casi no mejora el pronóstico.** La misma regresión sin clima da 0.906, 0.842 y 0.721 en la Bahía, Belice y
  la Ruta. Al pronosticar se usa el clima normal, porque el futuro no se conoce, así que lo que gana es la estructura:
  nivel por tramo y mes.
- **Qué dicen los coeficientes del clima:**
  - Bahía: 100 mm de lluvia arriba de lo normal equivalen a −10.9 % de visitantes ($p=0.027$).
  - Belice: −4.3 % ($p=0.059$).
  - Tormentas: solo hay 3 meses con tormenta entre los de entrenamiento, así que su efecto no se puede estimar con estas
    series. Se declara para la pieza 4.
- **Pronóstico de los próximos 12 meses** frente a los mismos meses del año anterior:
  - Bahía: +0.6 %.
  - Ruta: +2.1 %.
  - Belice: −4.9 %.
  - Cancún: 0.0 %.

  Ejemplo: Bahía, dic-2026, 1,311 visitantes esperados, con rango de 959 a 1,793 (dic-2025: 1,224).

## Pieza 4 — Tormentas, escenarios y sensibilidad (Estocástico) ✅
Código: `escenarios.py`. Salidas en `datos/gold/pronostico_`: `poisson_tormentas`, `escenarios`, `escenarios_anual` y
`sensibilidad`. Ecuaciones y ejemplos a mano: `ECUACIONES.md` §3.4.

**Tres decisiones de Brandon (30-sep-2026)**
1. **Tormentas: "Supuesto con barrido".** La probabilidad por mes sí está medida (Poisson con los 31 eventos). Su efecto
   en visitantes no se pudo estimar: en los meses que entrenan solo hubo 3 con tormenta (Earl 2016, Franklin 2017 y Lisa
   2022); las otras seis cayeron en pandemia o en cierre. El efecto se prueba como **supuesto**: el mes con tormenta
   pierde 0 %, 25 % o 50 % de visitantes.
   *Opción descartada:* solo mostrar la probabilidad, sin golpe en el escenario malo.
2. **Campaña: "No, se ve en la Fase 6".** Estos escenarios son "lo que pasaría de todos modos". El efecto de la campaña
   entra en la Fase 6, con los costos y conversiones reunidos (D13).
   *Opción descartada:* meter ahora un efecto supuesto (+5 %, +10 %), que mezclaría un pronóstico medido con un número
   sin fuente.
3. **Capacidad: "Capacidad probada".** Es el mes más alto que cada lugar ya recibió, el mismo criterio de la selección
   de regiones: Ruta 10,465 (ene-2018), Bahía 1,639 (abr-2017) y Belice 65,792 (ago-2025).
   *Opciones descartadas:* cuartos de hotel (los pronósticos son visitantes a zonas y cruces, no noches de hotel; habría
   que suponer cuántos se hospedan) y dejarlo para la Fase 6.

**Resultados**
- **Probabilidad de tormenta por mes:** agosto 13.9 %, septiembre 12.5 %, octubre 9.5 %, junio y noviembre 4.9 %, mayo y
  julio 1.7 %, y de diciembre a abril 0 %. Al menos una en el año: 40.3 %.
- **Monte Carlo:** 10,000 futuros de 12 meses por lugar. Cada futuro copia un año completo de errores reales del origen
  móvil.

  | Lugar | Malo / probable / bueno (año, sin golpe) | Con golpe supuesto de 50 % | Riesgo de rebasar la capacidad probada |
  |---|---|---|---:|
  | Ruta arqueológica del sur | 55,811 / 62,212 / 73,884 | 54,751 / 61,440 / 72,628 | 30.9 % |
  | Bahía Calderitas–Oxtankah | 10,106 / 11,217 / 13,085 | 9,915 / 11,019 / 12,777 | 24.2 % |
  | Chetumal · Belice | 551,986 / 620,304 / 671,956 | 535,346 / 606,138 / 660,162 | 38.3 % |

- **Hallazgo 1: las tormentas pesan en el mes, no en el año.** Con el supuesto más duro (−50 %), el escenario probable del
  año baja solo 1.2 % (Ruta), 1.8 % (Bahía) y 2.3 % (Belice). Pesa más la incertidumbre del propio pronóstico. En la Fase
  6, la reserva para tormentas es por mes (agosto a octubre), no un recorte anual.
- **Hallazgo 2: el riesgo de capacidad está en los meses pico.** Dic-2026 en Chetumal (29 %) y en la Bahía (14 %), y
  ene-2027 en la Ruta (30 %). Empujar la campaña en diciembre y enero podría llevar a esos lugares por encima de lo que
  nunca han recibido.
- **Hallazgo 3: sensibilidades medidas.**
  - Lluvia: −9.7 % en la Bahía ($p=0.039$) y −4.7 % en Belice ($p=0.031$) por cada 100 mm sobre lo normal.
  - Tipo de cambio: +6.8 % en la Ruta por cada peso más por dólar ($p=0.011$).
  - La hipótesis de que un peso barato atrae más cruces desde Belice no se sostiene ($p=0.36$).
  - Son asociaciones, no causas probadas.
- **El escenario probable no es igual al pronóstico del modelo** (Bahía: 11,217 contra 10,771). El Monte Carlo usa los
  errores reales, y en la Bahía el modelo se quedó corto 6 % en la mediana.

## Estado de la fase
Las cuatro piezas del plan están hechas: minería (forma del año), ML (5 modelos con origen móvil, rango conformal con su
cobertura real) y estocástico (Poisson, Monte Carlo y sensibilidad). Falta el notebook narrado `03_pronostico` y el visto
bueno de Brandon para cerrar la fase.
