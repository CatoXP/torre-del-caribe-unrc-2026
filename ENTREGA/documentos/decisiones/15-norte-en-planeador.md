# 15 — Cancún y Riviera Maya en el planeador, como referencia que redirige al sur

Autor: **Brandon Uriel García Sánchez** · 01-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Qué pidió Brandon
> mira esos dos como no tenemos datos cambialos por cancun y riviera maya

"Esos dos" son **Maya Ka'an** y la **Laguna Milagros–Xul-Ha**. En el planeador ("Planea tu viaje") solo decían "sin
dato", porque ninguna fuente oficial publica sus visitantes. Sobre qué ve quien elige el norte, Brandon dijo:

> Que aparezca, pero si Cancún está lleno o Riviera está lleno en ese mes que seleccionaron, le recomendamos de manera
> que sí se vea y no pase desapercibido en un scroll que puede elegir otro lugar, y así no rompemos la regla.

## La regla que se ajusta
La **regla de oro 9** decía que el norte no aparece en la portada. Con esta decisión, Cancún y Riviera Maya **sí
aparecen en el planeador**, pero:
- llevan la etiqueta **"Referencia: la campaña no lo promueve"**;
- van aparte, bajo el rótulo **"¿Ibas al norte?"**;
- si el mes está lleno, el planeador **siempre recomienda un lugar del sur**. Nunca recomienda ir al norte.

Así el norte funciona como la puerta de entrada de la campaña: quien pensaba ir a Cancún ve que está lleno y se le
ofrece el sur. Esa es la redistribución que pide el Problema Prototípico, hecha visible al viajero. Maya Ka'an y la
Laguna Milagros **siguen** en "Los lugares" y en el mapa; solo salieron del planeador.

## Decisión 1 — Temporada alta en el norte: los cortes del Radar
Cancún y Riviera Maya se miden con **ocupación hotelera** (SECTUR-DataTur, 55 meses de 2022 a 2026), no con visitantes.
Su ocupación cambia poco a lo largo del año: en Cancún, 64.5 % en septiembre y 80.7 % en marzo. Con la regla del sur
(índice de la forma del año ≥ 1.20), **Cancún nunca saldría en temporada alta**, porque su índice más alto es 1.08.

| Opción | Qué pasa | |
|---|---|---|
| **Cortes del Radar (elegida)** | Temporada alta si la ocupación esperada es ≥ 71.2 %, el corte p50 que el Radar ya usa para "concurrido" (decisión 08) | Cancún queda en temporada alta de noviembre a abril |
| Misma regla que el sur | Índice ≥ 1.20 | Cancún y Riviera Maya nunca salen en temporada alta y nunca se recomienda el sur |
| Solo saturado (≥ 85.9 %) | Corte p90 del Radar | Ningún mes pronosticado llega (el máximo es 78.9 %) |

- **Por qué:** reusa una decisión que Brandon ya defendió (los cortes comunes del Radar) y no inventa un umbral nuevo.
- **Evidencia:** `torre.radar.markov.estados` (p50 = 71.16 % de la ocupación semanal de los 7 centros del norte) y
  `torre.pronostico.calendario.nivel_norte`.
- **Meses fuera del pronóstico** (agosto a diciembre de 2027): se usa la ocupación típica de ese mes, que es el promedio
  medido de los años completos 2022–2025 (`ocupacion_tipica`).

## Decisión 2 — Riviera Maya en el Pronóstico, con el mismo método
- `series.py` arma la serie con la misma función que la de Cancún (`serie_norte`); su papel es **referencia**.
- Pasa por los mismos 5 modelos, el mismo rango del 90 % y el mismo criterio de Brandon: el menor error entre los
  modelos cuyo rango atrapa el valor real al menos 8 de cada 10 veces.
- **Lo que se declara:**
  - En la Riviera Maya, solo los dos Holt-Winters pasan el 80 % de cobertura. La línea base llega a 66.7 %; la
    regresión con clima y Gradient Boosting, a 74.4 %.
  - Se elige **Holt-Winters sin tendencia** (97.1 % de cobertura), aunque comete **72 % más error que repetir el año
    anterior** (MAE 1.724 veces el de la línea base).
  - Su ocupación bajó en 2026: 58.2 % en julio de 2026, contra 66.4 % en julio de 2025. El pronóstico supone que la
    baja sigue, y por eso deja a la Riviera Maya "tranquila" hasta julio de 2027.
  - La página lo dice en "¿Cómo lo sabemos?".
- **Lo existente no cambió.** Las 13 tablas del Pronóstico salen idénticas para el sur y para Cancún. Para lograrlo, la serie
  nueva se simula al final en el Monte Carlo: todas las series comparten el mismo generador de números al azar, y
  meterla en medio habría cambiado los sorteos de la Ruta.

## Decisión 3 — Tormentas del norte con la misma regla
La probabilidad de tormenta del sur cuenta las tormentas a 200 km o menos de **Chetumal**, así que no sirve para
Cancún. Se aplica la **misma regla** alrededor del punto de clima de cada lugar del norte: tormenta tropical o huracán
(≥ 34 nudos), a 200 km o menos, de 1966 a 2025 (`tormentas_punto`).
- **Cancún:** 45 tormentas en 60 años; octubre es el mes más riesgoso, con 19.5 %.
- **Riviera Maya:** 42 tormentas; octubre, con 18.1 %.

**Consecuencia:** en el norte no existe un mes que sea tranquilo, seco y fuera de la temporada de tormentas a la vez.
Por eso el planeador del norte solo sugiere **otro lugar del sur**, nunca otro mes.

## Decisión 4 — Fotos y negocios del norte
- **Fotos:** 6 de Cancún y 6 de la Riviera Maya, con la misma regla que las del sur: coordenada GPS dentro de su
  municipio (Benito Juárez y Solidaridad), licencia libre y revisión a ojo.
  - Se rechazaron las playas con sargazo (Cancún tiene varias en Commons) y todo lo que mencione Tulum o Cozumel.
  - En total quedan 40 fotos, todas comprobadas.
- **Negocios (DENUE):** Cancún y Playa del Carmen, el centro de la Riviera Maya. Cada uno usa solo sus propios
  negocios: el norte no se completa con otros lugares y el sur nunca se completa con el norte.
  - El clasificador ordenó 3,844 de 5,340 negocios turísticos de Cancún y 1,731 de 2,045 de Playa del Carmen.
  - En una muestra al azar de 40, 39 quedaron bien y 1 es dudosa ("Venta de cochinta", que su giro oficial pone como
    tacos y tortas).
  - La revisión encontró dos errores, que se corrigieron con prueba:
    - un bar de jugos ("Salade Salad & Juice Bar") salía como bar de noche;
    - la taquilla del ferri a Cozumel salía como paseo; ahora se excluye.

## Decisión 5 — El aviso que no se pierde al bajar
Cuando el lugar y el mes elegidos son temporada alta, del sur o del norte:
- **En la portada,** junto a los meses, aparece "Temporada alta. Chetumal está más tranquilo ese mes", con el botón
  "Cambiar a Chetumal".
- **Al bajar** (resultado y "Qué hacer"), el mismo aviso **flota fijo abajo de la pantalla**. Se esconde mientras se ven
  los meses, para no taparlos, y también en la parte de datos.
- Se cierra con la ×, y vuelve a salir si se elige otra combinación llena.

## Evidencia
- `tests/test_planeador.py`:
  - lugares del planeador;
  - corte del Radar con el ejemplo a mano (Cancún, enero de 2027: 78.27 % ≥ 71.16 % → alta);
  - nunca se recomienda el norte;
  - tormentas del norte;
  - el bar de jugos y el ferri.
- `tests/test_pronostico.py`: 5 series y la elección de la Riviera Maya con su advertencia.
- `tests/test_fotos_lugares.py`: 40 fotos, cada coordenada dentro de su municipio.
- En total pasan **200 pruebas**.
- La revisión en navegador, en escritorio y en celular, terminó sin errores, sin peticiones a internet y sin desborde.
  El aviso cambia de lugar con un clic y se esconde en la parte de datos.

## Consecuencia
El planeador ya no tiene lugares "sin dato". Quien piensa en Cancún o la Riviera Maya ve con cifras que en temporada
alta están llenos, y se le ofrece un lugar del sur con un clic. La Fase 6 (presupuesto) podrá usar esos meses llenos
del norte como los momentos en que más gente puede redirigirse.
