# 12 — Planea tu viaje y Qué hacer: el pronóstico al servicio del viajero

Autor: **Brandon Uriel García Sánchez** · 01-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Qué pidió Brandon (01-oct-2026)
> Front end acuerdate que es como si alguien se mete a la pagina a planear sus vacaciones y el quiere ir a enero y vemos
> que tal esta para 2027 o cualquier mes pero le diga dependiendo que parte de quintana roo escogio y mes y en base a eso
> te diga como va a estar y si ve flujos super altos o temporada alta re recomiende otra parte. Tambien quiero que
> agreges que hacer en la pagina un icono de sol que cuando escrolleas se vuelve luna y sean 3 secciones la parte de De
> dia puedes hacer esto, tarde puedes ir tal lugar y noche tal lugar todo eso dependiendo que lugar escogio la persona
> cambia, hospedagues hacer el NLP para recomendar donde, hospedarse y restuaramntes o comidas que esten cerca y
> recomendarlo mediante google maps y webscraping NLP y integralo a la pagina.

**Lo que no se pudo hacer tal cual, y por qué.** El scraping de Google Maps lo prohíben sus términos de uso y la regla 4
de `CLAUDE.md`. Además, las reseñas que sí se pueden usar (Rest-Mex) no cubren ninguno de los 5 lugares: solo Tulum,
Isla Mujeres y Bacalar. Se le presentaron opciones a Brandon y eligió las tres decisiones de abajo.

## Decisión 1 — De dónde salen los lugares: "DENUE + botón Google Maps"
- Negocios **oficiales** del Directorio Estadístico Nacional de Unidades Económicas (INEGI), con nombre y coordenadas,
  ordenados por cercanía al centro del lugar elegido.
- Cada tarjeta es un enlace a la dirección pública de Google Maps (`https://www.google.com/maps/search/?api=1&query=lat,lon`).
  Abre Google Maps en otra pestaña con esas coordenadas. No usa scraping ni llave, y la página no descarga nada de
  Google: sigue funcionando sin internet hasta que alguien da clic.
- **Descartadas:**
  - *solo nuestro mapa:* 100 % sin internet, pero menos útil para llegar;
  - *API oficial de Google Places:* llave con tarjeta, la página dejaría de funcionar sin internet, los términos
    prohíben guardar los datos y la llave quedaría expuesta en un repositorio público.
- **Límite que se declara:** el DENUE no trae calificaciones ni horarios. El orden es por cercanía, no por calidad, y la
  página lo dice.

## Decisión 2 — Qué hace el NLP: "Clasificar giros y nombres"
Clasificador de texto **por léxico**: un diccionario de raíces de palabra lleva a una categoría. Lee el nombre del
negocio y, si el nombre no dice nada, usa el giro oficial (código SCIAN). Decide tres cosas:
- el **tipo de lugar**: mariscos, cocina yucateca, antojitos, tacos, café y desayunos, bar, museo, balneario, hotel…;
- el **grupo**: qué hacer, dónde comer o dónde dormir;
- el **momento sugerido**: día, tarde o noche.

No hay etiquetas para entrenar un modelo estadístico, así que un léxico es lo honesto y es explicable regla por regla
(`backend/torre/campana/lugares.py`).

**Reglas, cada una con el caso real que la motivó**

| Regla | Caso que falló sin ella |
|---|---|
| Las raíces cuentan solo al **inicio de una palabra** | "MICHELADAS" contiene "HELAD" (de helados) y salía como heladería; "BARBACOA" contiene "BAR" |
| El **nombre gana al giro** | "ROSTIZERÍA EL PECHUGÓN" (giro de pizzas) y "HOTEL COSTA AZUL" (giro de casa de huéspedes) |
| Cocina internacional se revisa antes que comida casera | "QUINTANA ROLL **COCINA** JAPONESA" salía como comida casera |
| "Cocina yucateca" y "Antojitos" son categorías separadas | "QUESADILLAS AL ESTILO PUEBLA" salía como yucateca |
| "Desayun…" va a la mañana | "EL PATIO DE MI CASA DESAYUNOS" salía como plan de tarde |
| Solo señales sin alcohol vuelven bebida a un bar | "DISCO ROCK SHOTS **CAFE**" salía como desayuno |
| Se excluye lo que no le sirve a un visitante | "ANTOJITOS SIN NOMBRE" (no se puede encontrar), cooperativas escolares, clubes de nutrición, gimnasios, lotería, moteles, banquetes, puestos de canicas, un estacionamiento de hotel y centros para adultos |

**Resultado.**
- De 2,042 negocios turísticos de las localidades de los 5 lugares, 1,587 quedan clasificados: 1,043 por el nombre y
  544 por el giro. Se excluyen 455.
- **Precisión medida:** se revisaron a mano 40 negocios al azar (semilla 2026), con 38 correctos. Con lo aprendido se
  corrigieron las reglas. Una **muestra nueva** (semilla 2027) dio **39 de 40**. El error de esa segunda muestra (la
  cocina japonesa) también se corrigió, así que ya no se volvió a medir.

**Momento sugerido** (regla por tipo de lugar; el DENUE no publica horarios):

| Momento | Qué hacer | Dónde comer |
|---|---|---|
| Día | Zonas arqueológicas (INAH), museos, zoológico, paseos en lancha, agencias de tours | Café, desayunos y postres |
| Tarde | Balnearios, parques, recreación | Mariscos, cocina yucateca, comida casera, a la carta, asados, internacional |
| Noche | Bares, cantinas, centros nocturnos | Antojitos, tacos y tortas, pizzas y hamburguesas, comida rápida |
| Noche | Dónde dormir: hoteles, hostales, posadas, cabañas, campamento | |

**Regla de oro 9.** Solo se recomiendan negocios de las localidades de los 5 lugares. Si un lugar no tiene de algo, se
completa con lo más cercano de los otros 4 y se marca "en Chetumal, a 51 km". Por ejemplo, la Ruta no tiene hoteles.
Nunca se recomienda algo de Bacalar, Mahahual ni el norte, y hay una prueba que lo verifica.

## Decisión 3 — Cuándo es temporada alta: "Forma del año + capacidad"
Un mes es **temporada alta** si su índice de la forma del año es ≥ 1.20 (Fase 5, pieza 2) **o** si tiene ≥ 10 % de
riesgo de rebasar la capacidad probada (Monte Carlo, pieza 4). Para leerlo sin tecnicismos:
- índice < 1.00: "mes tranquilo";
- de 1.00 a 1.19: "mes normal";
- lugares sin serie (Maya Ka'an, Laguna Milagros): "sin dato de afluencia". **No se inventa una temporada.**

*Descartada:* usar el semáforo del Radar, que es del mes actual y donde los 5 lugares salen siempre tranquilos.

**Qué recomienda cuando es temporada alta**
1. **Otro lugar:** el lugar del sur con el índice más bajo ese mes que no esté en temporada alta.
2. **Otro mes:** el mes más tranquilo del mismo lugar que cumpla tres condiciones:
   - no es temporada alta;
   - está fuera de la temporada de tormentas (probabilidad < 9 %);
   - llueve menos que el mes mediano del año en ese punto (97 mm en Chetumal, 84 mm en Kohunlich).

*Ajuste hecho al probarlo:* sin la condición de lluvia, el mes sugerido casi siempre era **junio**. Es tranquilo, pero es
el más lluvioso (195 mm) y sería un mal consejo. Con la condición, las sugerencias quedan así:
- Ruta: noviembre (índice 0.98, 76 mm).
- Bahía: mayo (0.88, 95 mm).
- Chetumal: febrero (0.87, 26 mm).

**Ejemplos con datos reales**
- **Ruta de las pirámides, enero de 2027:** temporada alta.
  - Llega 61 % más gente que en un mes promedio y hay 30 % de riesgo de rebasar el mes más lleno de su historia.
  - Se esperan unos 8,993 visitantes (entre 5,716 y 14,149).
  - La página recomienda **Chetumal** (índice 0.93, tranquilo) o **la Ruta en noviembre**.
- **Chetumal, diciembre de 2026:** temporada alta por el riesgo de capacidad (29 %), aunque su índice es 1.17.
- **Diciembre de 2026:** los tres lugares con dato están en temporada alta, así que solo se sugiere otro mes.

## Sol, atardecer y luna
"Qué hacer" tiene tres bloques: de día, por la tarde y de noche. Cada uno tiene el color de su cielo: crema, mango y añil.
Al bajar, un ícono pasa por tres fases:
- en el día, un sol;
- en la tarde pierde los rayos y se vuelve naranja;
- en la noche, una sombra entra por la derecha hasta dejar una luna.

La fase sigue al bloque que se está leyendo. Con "movimiento reducido" activado en el sistema, el ícono cambia de golpe
por bloque, sin animación.

## Evidencia de que funciona
- `tests/test_planeador.py` tiene 28 pruebas: los 11 casos del clasificador, 7 exclusiones, solo los 5 lugares, la regla
  de temporada alta y las recomendaciones de arriba.
- La revisión en navegador (escritorio de 1280 px y celular de 390 px) terminó sin errores de JavaScript, con las tres
  fases del ícono en su bloque.

## Consecuencia
La redistribución que pide el Problema Prototípico se vuelve visible para el viajero: quien elige un mes saturado ve otro
lugar u otro mes del sur. La oferta clasificada por lugar (`datos/gold/lugares_clasificados.parquet`) queda lista para
los mensajes de la campaña en la Fase 8.
