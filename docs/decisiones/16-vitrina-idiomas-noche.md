# 16 — Una página que convence: vitrina, reseñas, día y noche y 10 idiomas

Autor: **Brandon Uriel García Sánchez** · 02-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Qué pidió Brandon
> vas a mejorar la página agregando más fotos a las comidas, reseñas reales, las estrellas del lugar, y más cosas para
> convencer a las personas de viajar a Quintana Roo, preguntas frecuentes, secciones para vender más cosas, una barra
> horizontal de imágenes bonitas, una versión para cambiar de idioma, en 10 idiomas, una versión nocturna y otra de día,
> con un botón y ese botón esté animado, animar toda la página, más contenido pero sin saturar y todo sea hermoso
> visualmente

## Lo que no existe y cómo se resolvió (regla de oro 1)
| Pedido | Qué se encontró | Qué eligió Brandon |
|---|---|---|
| Fotos de comida de los 5 lugares | En Commons hay 0 fotos de platillos tomadas ahí (decisión 14) | **Fotos y reseñas del equipo**, propias o con permiso |
| Reseñas reales | Rest-Mex no cubre los 5 lugares; copiar las de Google o TripAdvisor está prohibido (regla 4) | **Botón "Reseñas en Google"** en cada negocio, más las reseñas del equipo |
| Estrellas del lugar | Ver abajo | **Estrellas oficiales de hotel**: hueco declarado |
| Secciones para vender | No hay precios oficiales de nada | **Experiencias reales**, **rutas de 2 y 3 días** y **llamados de campaña**, sin precios |
| 10 idiomas | — | **Mercados que llegan**: la parte de "Los datos" queda en español |

**Estrellas oficiales: hueco declarado.** El Compendio Estadístico de DataTur 2024 (tabla 5_2) publica cuartos por
categoría (1 a 5 estrellas) solo para los 70 centros que monitorea. Cancún, Riviera Maya y Playa del Carmen están ahí,
pero **ninguno de los 5 lugares del sur**; la tabla 10_1 solo trae el total del estado. Por eso la página no muestra
estrellas por lugar. Las estrellas que aparezcan en "Lo que vivimos" son la opinión de quien escribe la reseña, y así
se dice.

## Decisión 1 — Vitrina con datos que existen (`backend/torre/campana/vitrina.py`)
- **Postales:** una tira horizontal con las 28 fotos comprobadas de los 5 lugares. Nunca lleva fotos del norte. Se
  mueve sola, se detiene al pasar el mouse y, con movimiento reducido, se recorre a mano.
- **Seis experiencias**, cada una con una cifra oficial y los negocios reales que la ofrecen:

  | Experiencia | Cifra |
  |---|---|
  | Pirámides en la selva | 66,628 visitantes en 2025 entre Kohunlich, Dzibanché e Ichkabal (INAH) = **unas 183 personas al día** |
  | Mariscos frente a la bahía | 21 marisquerías en Calderitas (DENUE) y 11,017 visitantes a Oxtankah (INAH) |
  | Una laguna dulce y un cenote | Sin estadística de visitantes: se cuida con límite estricto |
  | Museos de la cultura maya | 9 museos en Chetumal y Maya Ka'an (DENUE) |
  | Turismo comunitario maya | 107 hospedajes chicos, 38 medianos y 0 grandes en sus municipios (DENUE) |
  | Atardecer en el malecón | 4 de cada 10 cuartos de Chetumal vacíos en 2024 (SITUR-Q) |

- **Rutas:** "Bahía y pirámides" (2 días), "Laguna y selva" (3 días) y "Pueblos de Maya Ka'an" (2 días).
  - Las distancias son **en línea recta** entre los centros, porque no hay datos abiertos de distancias por carretera.
  - El mejor mes sale del planeador: que ningún lugar con dato esté en temporada alta, sin temporada de tormentas y con
    lluvia menor que la mediana. Para las dos primeras sale **mayo**.
  - Maya Ka'an no tiene serie, así que su mes se elige solo por clima: **febrero**, y se dice.
- **Descartado:** paquetes con precio, "lo más vendido" o calificaciones inventadas.

## Decisión 2 — Reseñas: se leen en Google, se escriben aquí
- Cada negocio tiene dos botones: "Cómo llegar", con la coordenada del DENUE, y "★ Reseñas", que busca el nombre en
  Google Maps.
- La página **no copia ni descarga** ninguna reseña: la persona las lee en Google, al dar clic.
- **"Lo que vivimos"** (`aportes.py`, guía en `docs/aportes/LEEME.md`) muestra fotos y reseñas del equipo. Cada aporte
  necesita lugar, autor, fecha y permiso. Si la foto trae ubicación GPS, debe caer en el municipio del lugar. Hoy hay 0
  aportes, así que la sección no aparece.

## Decisión 3 — Día y noche
- Hay un botón en la barra: el sol con nube se vuelve luna con estrellas. Al cambiar, la página se abre como un círculo
  desde el botón (View Transitions). Se recuerda la elección; la primera vez se usa la que pide el sistema.
- De noche se oscurecen las superficies color cal. Los bloques de color (turquesa, amarillo, rosa, añil, verde) son
  **islas**: guardan su paleta de día, así que el texto sobre amarillo o turquesa sigue siendo tinta.
- **Descartado:** invertir colores con un filtro, porque el rosa y el turquesa se veían falsos.
- Los textos de color sobre fondo oscuro usan versiones más claras de los mismos tonos.

## Decisión 4 — 10 idiomas (`frontend/idiomas.js`, `backend/torre/campana/idiomas.py`)
- Idiomas: español, inglés, francés, alemán, italiano, portugués, chino, japonés y coreano. El **maya yucateco** está
  como plantilla vacía (`docs/idiomas/yua.tsv`) y no aparece en el menú hasta que lo traduzca y revise una persona que
  lo hable.
- **Cómo funciona:** se traduce lo que está en pantalla.
  - Cada frase se normaliza: las cifras se vuelven `{n0}`, los meses `{m0}`, los lugares `{p0}` y los nombres propios
    `{x0}`.
  - Así, "Llega 29 % menos gente" y "Llega 40 % menos gente" son una sola frase.
  - Las cifras se escriben al estilo de cada idioma y los meses los da el navegador (Intl).
  - Son **375 frases por idioma**. El programa se detiene si una traducción pierde o inventa una cifra, un mes, un lugar
    o una etiqueta.
- "Los datos" queda en español, como eligió Brandon. Al cambiar de idioma lo dice un aviso.
- Chino, japonés y coreano usan un interlineado normal: los títulos condensados encimaban los renglones.

## Decisión 5 — Animación sin saturar
Se agregaron movimientos discretos:
- la tira de postales;
- el botón de día y noche y su círculo;
- la greca del llamado de campaña, que avanza despacio;
- tarjetas que suben al pasar el mouse;
- un acordeón suave en las preguntas frecuentes;
- una línea de avance de lectura (rosa → amarillo → turquesa).

Todo se apaga con "movimiento reducido". Las **preguntas frecuentes** usan las mismas respuestas del chat, con su fuente.

## Evidencia
- Pruebas:
  - `tests/test_vitrina.py` (13): postales solo del sur, fuentes, sin precios, el ejemplo a mano de 183 por día, rutas
    con foto y validación de aportes;
  - `tests/test_idiomas.py` (18): 8 idiomas completos, marcas intactas y el maya sin publicar.
- Revisión en navegador, en escritorio y en celular, de día, de noche y en los 9 idiomas: sin errores, sin peticiones a
  internet, sin desborde y sin imágenes rotas.
- La revisión encontró y corrigió dos fallas:
  - una ruta sin foto, por un comentario que se tragó el campo;
  - el texto oculto "(Google Maps, otra pestaña)", que quedaba visible en otros idiomas porque dos etiquetas iguales se
    restauraban mal.

## Consecuencia
La página vende el sur con lo que sí existe: lugares reales, cifras oficiales, rutas y fotos comprobadas. Cada vacío se
declara y tiene un camino propio, que son los aportes del equipo. La Fase 8 (campaña) partirá de estas experiencias y
rutas para sus piezas.
