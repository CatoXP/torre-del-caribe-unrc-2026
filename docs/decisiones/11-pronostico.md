# 11 — A3 Pronóstico: ¿cuándo conviene ir y cuánto invertir? (Fase 5) · EN CURSO

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
   - Belice, mar-2020 → feb-2022. La frontera estuvo casi cerrada: de 57 a 2,864 cruces al mes, entre el 0 % y el 7 %
     del mismo mes de 2019. Reabrió en feb-2022 (42 %) y en mar-2022 ya estaba en 65 %.

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
| Chetumal · Belice | 90 | 66 | 0 | 0 | 24 |
| Cancún (referencia) | 55 | 55 | 0 | 0 | 0 |

**Consecuencia para declarar.** Las zonas reabrieron por debajo de su nivel anterior: Kohunlich tuvo 21,850 visitantes
en 2025 contra 42,813 en 2019. Por eso el nivel se toma de los meses posteriores a la reapertura y no del promedio
histórico.

Pruebas: `tests/test_pronostico.py`, 9 pruebas, cada una con un mes real revisado a mano.

## Siguientes piezas
2. **Minería:** forma del año y fuerza de la temporada de cada serie (descomposición estacional).
3. **ML:** tres modelos comparados en origen móvil contra una línea base, con error MAE/MAPE e intervalo conformal al
   90 % con su cobertura real:
   - Holt-Winters;
   - regresión con clima;
   - Gradient Boosting con rezagos.
4. **Estocástico:** probabilidad de tormenta por mes (Poisson con los 31 eventos) y Monte Carlo de escenarios malo /
   probable / bueno; sensibilidad al dólar y a la lluvia.
