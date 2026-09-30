# 06 — La página para público no técnico

> **Nota del 28-sep-2026:** el diseño visual descrito aquí fue reemplazado por el sistema "Sur mexicano"
> (`07-diseno.md`). Siguen vigentes las decisiones de contenido: honestidad de las cifras, ubicación comprobada, fotos
> con licencia libre y contrato del cascarón.

Autor: **Brandon Uriel García Sánchez** · 28-sep-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Decisión
Brandon pidió enfocarse en la página, "para gente no técnica". La página se reorganizó en cinco partes:
1. **Portada.** "El sur tiene espacio.", respaldado por una cifra medida.
2. **Conoce los 5 lugares.** Mapa con los lugares numerados y una ficha de cada uno.
3. **¿Por qué el sur?** El norte solo como referencia.
4. **Lo que viene.**
5. **Fuentes.** Con sus nombres completos.

## Evidencia
- **Cuartos vacíos en Chetumal, 2024:** 458,696 noches ocupadas de 791,016 disponibles = 58.0 % → 4 de cada 10 vacías.
  Se usa `cuartos_vacios_chetumal` en `backend/torre/api/datos_pagina.py`, que suma cuartos y no promedia porcentajes.
- **Fichas por lugar:** negocios del DENUE y población del Censo 2020, contados en las mismas localidades de cada
  región (`REGION_LOCALIDADES`, decisión de `05-planteamiento.md`), más datos del INAH y SITUR-Q. Las cifras de las
  fichas están en `docs/ejecutivo/DOCUMENTO_EJECUTIVO.md` §6.3.

## Opciones descartadas
- **Destacar Kohunlich (+13.5 %) y Dzibanché (+69.2 %) en la portada.** La ruta completa bajó 8.2 % en ene–jul 2026,
  porque Ichkabal cayó 27.5 %. Mostrar solo las zonas que suben sería escoger datos a conveniencia.
- **Mapa de negocios por municipio.** No dice qué hay en cada lugar, y a nivel municipio cuatro lugares comparten
  la misma cifra.
- **Gráfica con cuatro centros del norte y "ocupación hotelera".** Pedía conocimientos técnicos. Quedan dos líneas y una
  sola frase: "de cada 10 cuartos, X ocupados".

## Consecuencia
- `tests/test_pagina.py` falla si las fichas mencionan Tulum, Cancún, Cobá, Muyil u otro lugar fuera del foco (regla de
  oro 9), y comprueba las cifras clave.
- El diseño visual fino se revisa al final, junto con el Radar (Fase 4) y el calendario (Fase 5).

## Ampliación del 28-sep-2026: ubicación comprobada y fotos
Brandon pidió confirmar que los lugares sean de Quintana Roo y agregar fotos de referencia.

**Ubicación** (`backend/torre/base/ubicaciones.py`). Se hicieron tres pruebas independientes:
- los 11 pueblos están en el Censo 2020 de Quintana Roo;
- las 4 zonas arqueológicas tienen Estado = "Quintana Roo" en la base del INAH;
- cada coordenada cae dentro del polígono de su municipio: Othón P. Blanco, Felipe Carrillo Puerto o José María
  Morelos (Kantemó).

Resultado: todo en orden. No basta con buscar el nombre, porque hay un "Xul-Ha" en Puerto Morelos y un "Felipe
Carrillo Puerto" en Solidaridad; por eso se usan las claves oficiales. El directorio del INEGI confirma además que el
Museo de la Cultura Maya está en Chetumal.

**Fotos** (`backend/torre/base/ingesta_fotos.py`, fuente D15). Se usa Wikimedia Commons, que publica fotos con licencia
libre (CC BY / CC BY-SA) mediante una API oficial. Cumple la regla de oro 4: nada de Google Imágenes ni TripAdvisor. La
página muestra autor y licencia junto a cada foto, como exige la licencia.

| Lugar | Foto | Autor · licencia | Ubicación comprobada |
|---|---|---|---|
| Chetumal | Malecón frente a la bahía | holachetumal · CC BY 3.0 | Coordenada en Othón P. Blanco |
| Calderitas y Oxtankah | Costa de Calderitas | holachetumal · CC BY 3.0 | Coordenada en Othón P. Blanco |
| Ruta de las pirámides | Templos de Dzibanché | Lugares INAH · CC BY-SA 4.0 | Sin coordenada; la subió el INAH |
| Maya Ka'an | Centro de Felipe Carrillo Puerto | AdriLov · CC BY-SA 4.0 | Coordenada en Felipe Carrillo Puerto |
| Laguna Milagros y Xul-Ha | La laguna | holachetumal · CC BY 3.0 | Coordenada en Othón P. Blanco |

**Descartadas:**
- las fotos de Tihosuco, porque su título dice "Yucatan" (Tihosuco es de Quintana Roo, pero el título confunde);
- las de "Kantemo", porque son de animales y su coordenada queda a unos 40 km del pueblo.

## Rediseño del 28-sep-2026: página completa, maqueta 3D y cascarón de las fases
Brandon pidió usar sus skills de páginas web y el DESIGN.md para hacer la página "hermosa", dejar el cascarón listo
para las demás fases y agregar un mapa 3D animado, que se pueda elegir y accionar, con animaciones en todo.

**Cómo se hizo:**
- Con la skill `design-html` (gstack), en modo guiado por el plan. La fuente de verdad es el recorrido de
  `PLAN_v3.md` B.5 más los tokens de `docs/DESIGN.md`. No hubo maquetas generadas por IA, porque el generador de
  imágenes de la skill necesita una llave de API que no está configurada.
- **Recorrido:**
  1. Anuncio.
  2. Portada.
  3. Los 5 lugares (maqueta 3D y fichas).
  4. Cuándo ir.
  5. La campaña.
  6. La torre de control, con 4 pestañas: En vivo, Escenarios, Presupuesto y Evidencia.
  7. Fuentes.
- **Maqueta 3D** con perspectiva del propio navegador (CSS) y SVG, sin librerías:
  - una placa con grosor y los municipios en relieve;
  - los marcadores quedan de pie porque se contra-rotan;
  - se gira arrastrando, y hay botones "Vista general", "Desde arriba" y "Girar solo";
  - al elegir un lugar, la cámara vuela hacia él.

  **Opción descartada:** three.js. Es más pesado, agrega otra dependencia que habría que descargar y explicar, y la
  página debe funcionar sin internet.
- **Animaciones:**
  - las cifras cuentan hasta su valor exacto al aparecer;
  - los botones tienen onda, brillo y hundimiento;
  - las pestañas tienen un indicador que se desliza;
  - las secciones aparecen al hacer scroll y la ficha entra con movimiento.

  Todo se apaga con la opción "reducir movimiento" del sistema.
- **Pretext** (motor de texto de la skill, licencia MIT) se copió a `frontend/vendor/pretext.js` para que funcione sin
  internet. Equilibra los títulos de varias líneas.
- **No se aplicaron dos reglas de la skill:** texto editable en la página (es pública, no un borrador) y modo oscuro
  automático (DESIGN.md ya define su paso de blanco a índigo). Tampoco se usan fuentes de Google, porque la página
  va sin internet y DESIGN.md pide la letra del sistema.

**Cascarón (contrato para las fases siguientes).** Cada sección futura revisa si `frontend/datos/pagina.js` ya trae su
clave. Si no, muestra su forma en gris con "Se llena en la Fase N" y **ningún número**:

| Clave en pagina.js | Sección que llena | Fase |
|---|---|---|
| `radar` | Semáforo de cada lugar (en la ficha) | 4 |
| `pronostico` | Calendario "Cuándo ir" | 5 |
| `escenarios` | Pestaña Escenarios (abanico malo / probable / bueno) | 5 |
| `presupuesto` | Pestaña Presupuesto (controles conectados al modelo) | 6 |
| `envivo` | Decisiones de la semana (pestaña En vivo) | 7 |
| `campana` | Viajero ideal, mensajes y anuncios; activa "Planear mi viaje" | 8 |

**Datos reales que ya muestra la pestaña Evidencia:**
- 8,134,802 registros oficiales de 353 archivos;
- los 5 lugares comprobados en Quintana Roo;
- la tabla de criterios de la Fase 3;
- el avance por fase.

**Verificación:**
- 375, 768 y 1440 px, sin errores de consola y sin desplazamiento horizontal;
- clic en los marcadores y en las pestañas probado con Playwright;
- 44 pruebas en verde.


## Ampliación del 28-sep-2026: cómo se mueven, el dinero, las 12 fases, quiénes somos y preguntas rápidas
Brandon pidió: "un mapa de cómo viajan a todo Quintana Roo, ver dónde se queda el dinero (hoteles), un chat bot de
preguntas rápidas, quiénes somos (científicos de datos), y deja el cascarón de todas las fases".

| Sección | Qué muestra | Función (`datos_pagina.py`) | Evidencia |
|---|---|---|---|
| **Así llega la gente** (`#movimiento`) | Mapa de todo el estado con burbujas por lugar de llegada y botones por medio | `movimiento()` | Avión 2024 15,959,277 · Tren Maya 2025 560,241 · Crucero 2025 7,556,937 · Frontera 2025 653,306 |
| **Dónde se queda el dinero** (`#dinero`) | Cuartos por hotel por destino y hospedajes por tamaño | `hospedaje()` | Cancún 219.4 vs Chetumal 27.1 cuartos por hotel (jul-2026); municipios de los 5 lugares: 107 chicos, 38 medianos, 0 grandes |
| **Las 12 fases** (`#fases`) | Tarjeta por fase: lista, en curso o pendiente, con su resultado real | `fases_del_proyecto()` | Fases 0–3 con cifra; 4–11 "Se llena en esta fase" |
| **Quiénes somos** (`#equipo`) | Integrantes y cómo trabaja el equipo | `EQUIPO` | Brandon + "Nombre por confirmar" |
| **Preguntas rápidas** (`#chat`) | Asistente con respuestas fijas, cada una con fuente | `preguntas_rapidas()` | 15 respuestas armadas con las cifras de arriba |

**Decisiones de honestidad:**
- **Se usa el último año completo de cada medio.** El avión llega hasta 2024 porque desde 2025 todos los aeropuertos
  reportan 0 (regla 6 de Silver, `04-silver.md`).
- **No se dibujan flechas de origen a destino.** Ninguna fuente pública dice cuánta gente viaja de un lugar a otro
  dentro del estado. *Opción descartada:* flechas "estimadas" desde Cancún, que serían inventadas.
- **La ruta del Tren Maya es un esquema:** une las estaciones en su orden (Cancún → Chetumal), no sigue la vía real, y
  la nota lo dice. Holbox aparece en los datos del tren, pero SITUR-Q no dice dónde está su estación, así que no se
  dibuja.
- **Burbujas con área proporcional:** el radio es la raíz de las llegadas; si fuera proporcional al radio, Cancún
  parecería 4 veces más grande de lo que es en proporción.
- **El dinero se mide con el tamaño de los hoteles.** No hay gasto por turista por destino. *Opción descartada:* la
  serie de derrama de SITUR-Q: no dice su unidad (pesos o dólares) y el total estatal sale menor que Cancún. La página
  lo avisa en pantalla.
- **El chat no es un modelo de IA.** Busca palabras clave y devuelve respuestas fijas. Así no puede inventar cifras y
  funciona sin internet. No da precios, porque no hay fuente oficial abierta de tarifas. Si no sabe algo, lo dice.
  *Opción descartada:* un chatbot con modelo de lenguaje: necesita internet y podría responder cifras sin fuente.

**Verificación:**
- `tests/test_pagina.py`: totales por medio (y que cada total sea la suma de sus puntos), cifras de hospedaje, las 12
  fases y que el chat no dé precios.
- 1440 y 390 px sin desplazamiento horizontal ni errores de consola (Playwright).
- 49 pruebas en verde.
