# 07 — Sistema visual "Sur mexicano" (reemplaza al estilo Flighty del DESIGN.md)

Autor: **Brandon Uriel García Sánchez** · 28-sep-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Decisión
Brandon revisó la página y pidió rehacerla por completo. Estas fueron sus palabras:
- "se ve muy IA el font y todo";
- "veo mucho ruido e información innecesaria, no es nada visual";
- "calidad tipo Apple, hermoso";
- "tipografía de destino, viajes, mar, mexicano… colores vibrantes para México, identidad real".

La página se rediseñó desde cero con **Claude Design**, en el lienzo "Torre del Caribe — rediseño web" (tableros de
escritorio 1440 px y móvil 390 px). Después se programó igual en `frontend/`.

## El sistema
| Elemento | Decisión | Por qué |
|---|---|---|
| Colores | Rosa mexicano #E4007C · amarillo cempasúchil #FFB000 · turquesa Caribe #00A19A · añil #1B2A6B · verde selva #0B6E4F · barro #D2552B · cal #FFF6EA · tinta #1A1220 | Paleta mexicana en bloques de color completo, como la arquitectura de Luis Barragán. Cada sección tiene un color de fondo |
| Letras | **Bricolage Grotesque** (títulos y cifras, condensada y en mayúsculas) · **Figtree** (texto) | Voz de cartel y de viaje, con carácter. Van en `frontend/fuentes/` (licencia OFL), así funcionan sin internet |
| Motivo | Greca escalonada con el perfil de las pirámides mayas del sur | Identidad de Quintana Roo, no un adorno genérico. Se usa solo entre secciones |
| Fotos | 6 de Wikimedia Commons en alta resolución, a sangre completa | Brandon pidió que fuera visual. Cada foto lleva su crédito |
| Contenido | Una sola idea por sección y ~70 % menos texto | Brandon señaló el ruido. Los módulos futuros ya no aparecen como bloques grises; solo se nombran en "Lo que viene" |
| Movimiento | Paralaje de la portada, cifras que cuentan, cuartos que se llenan, mapa que vuela al hacer scroll, gráfica que se dibuja | Pocos momentos bien hechos en lugar de muchos efectos sueltos. Se apaga con "reducir movimiento" |

**Contraste:** el texto claro va solo sobre añil, rosa y tinta; sobre amarillo y turquesa, el texto es tinta.

## Opciones descartadas
- **Mantener el estilo Flighty del DESIGN.md con la letra del sistema.** Brandon lo vio genérico, "de IA".
- **Imitar literalmente a Apple.** Se tomaron sus principios de calidad (aire, fotografía y precisión), no su
  diseño. Además, las reglas de Claude Design prohíben recrear el diseño distintivo de otra empresa.
- **Papel picado.** Es un cliché nacional; la greca maya es propia del sur de Quintana Roo.
- **three.js para el mapa.** Se sigue con 3D en CSS: más ligero y sin dependencias.

## Consecuencias
- `docs/DESIGN.md` queda como referencia histórica. El sistema vigente es este documento.
- **Contrato del cascarón:** los espacios ocultos `data-clave` de `index.html` son `radar`, `pronostico`,
  `escenarios`, `presupuesto`, `envivo` y `campana`. Cada fase agrega su función en `DIBUJAR` (`frontend/app.js`) y
  su sección aparece sola.
- **Verificado:**
  - 1440 y 390 px, sin errores ni desplazamiento horizontal;
  - menú de celular probado;
  - 44 pruebas en verde.

## Secciones agregadas el mismo día (contenido en `06-pagina.md`)
Cada sección nueva tiene su propio bloque de color dentro del sistema:

| Sección | Color de fondo | Motivo del color |
|---|---|---|
| Así llega la gente | Tinta | Las burbujas de colores (amarillo avión, rosa tren, turquesa crucero, barro frontera) resaltan sobre fondo oscuro |
| Dónde se queda el dinero | Verde selva | Los cinco lugares van en amarillo; el resto, en gris verdoso |
| Las 12 fases | Rosa mexicano | Lista = blanco, en curso = amarillo, pendiente = borde punteado (el "cascarón" se ve a simple vista) |
| Quiénes somos | Cal | Avatares en rosa; la tarjeta por confirmar, punteada |
| Preguntas rápidas | Botón rosa fijo y panel cal | Siempre a mano sin tapar el contenido; se cierra con Esc |

La lista de las 12 fases reemplaza a "Lo que viene". Ajustes tras revisar las capturas: la rejilla de fases quedó más
ancha que el resto de la página (se alineó con el margen común) y en el celular el mapa cortaba la burbuja de Cancún
(se agregó margen al dibujo y los nombres van encima de las burbujas). Verificado en 1440 y 390 px; 49 pruebas en verde.
