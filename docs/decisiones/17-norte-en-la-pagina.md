# 17 — Cancún y Riviera Maya en toda la parte del viajero, noche de verdad, comida y estrellas

Autor: **Brandon Uriel García Sánchez** · 02-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Qué pidió Brandon
> se te olvidó los cambios de meter cancún y riviera maya, como opciones, porque es que sigues mencionando otros cuando
> no tenemos datos de ninguno de ellos, sabes? y luego el modo nocturno no sirve. Y sigue faltando detalles

Después eligió:
- **"Toda la parte del viajero"** como alcance del cambio;
- los detalles "Fotos de comida", "Qué hacer completo", "Estrellas oficiales" y "Chat en tu idioma".

## Decisión 1 — Los cinco lugares del viajero
| Parte de la página | Antes | Ahora |
|---|---|---|
| Portada / planeador | Chetumal, Bahía, Ruta, Cancún, Riviera Maya (decisión 15) | Igual |
| Los lugares (mapa y fichas) | Los 5 de la campaña, con Maya Ka'an y la Laguna "sin dato" | Chetumal, Calderitas–Oxtankah, Ruta de las pirámides, **Cancún** y **Riviera Maya** |
| Vive el sur, rutas, postales | Experiencias y rutas de Maya Ka'an y la Laguna | Las del lugar elegido arriba; si es el norte, además, lo del sur |
| Barra de arriba | "Laguna Milagros y Xul-Ha, sin dato oficial" | Lo que dice el planeador este mes ("Cancún, temporada alta · Chetumal, tranquilo") |
| Preguntas frecuentes | "¿Qué hay en Maya Ka'an?", "¿Qué hay en la Laguna?" | Una pregunta por cada uno de los 5 lugares del viajero |

- **"Los datos" no cambia.** El Radar, el problema y las fases siguen siendo el análisis de las 5 regiones originales,
  porque así se construyeron las Fases 3 y 4.
- Cancún y Riviera Maya llevan siempre la etiqueta **"Referencia: la campaña no lo promueve"**. Su ficha dice que tienen
  sargazo en 2026 y cuándo se llenan.
- La regla de oro 9 se ajusta en `CLAUDE.md`.

## Decisión 2 — Modo noche de verdad
**Qué fallaba.** El botón sí cambiaba el tema, pero los bloques de color (turquesa, amarillo, rosa) eran "islas" que
guardaban su paleta de día. Por eso la portada y "Así va a estar" se veían igual.

**Cómo se arregló.**
- Cada bloque claro tiene ahora su versión de noche: turquesa muy profundo, ámbar oscuro y vino. El texto pasa a ser
  claro.
- La foto de la portada se oscurece.
- Solo los bloques que ya eran oscuros (añil, verde y tinta) siguen siendo islas.
- Se revisaron las 19 secciones de noche, en escritorio.

## Decisión 3 — Estrellas oficiales (`backend/torre/campana/estrellas.py`)
- **Fuente:** el Compendio Estadístico del Turismo en México 2024 (DataTur), tabla 5_2. Trae los cuartos-noche por
  categoría oficial para los 70 centros que monitorea.
- **Cancún:** 35,537 cuartos promedio en 2024. De ellos, **67.8 % son de 5 estrellas**, 21.7 % de 4 y 8.8 % de 3.
- **Playa del Carmen** (el centro de la Riviera Maya): 11,997 cuartos; **58.9 % de 5 estrellas**, 11.9 % de 4 y
  22.7 % de 3.
- **Para los lugares del sur sigue el hueco:** no están entre los 70 centros.
- **Cómo se muestra:**
  - la parte de 5 estrellas en la ficha, en "Dónde dormir" y en las experiencias del norte;
  - el total de cuartos de la ficha es el de SITUR-Q (registro estatal, 47,386 en Cancún). No se pone junto al de
    DataTur, porque son dos fuentes con distinta cobertura y dos cifras distintas del "mismo" dato confundirían.

## Decisión 4 — Fotos de comida, comprobadas
- Se buscaron en Commons fotos con coordenada dentro de Benito Juárez y Solidaridad.
  - De 68 con licencia libre se eligieron **8**, revisadas a ojo: panuchos, guacamole, una comida de mariscos, un puesto
    de quesadillas y una taquería en Cancún; fajitas, cocina mexicana y cenar en la calle en Playa del Carmen.
  - Se descartaron peces de acuario, bufés de hotel y fachadas.
- Salen en "Qué hacer" ("Así se come en…") cuando se elige Cancún o la Riviera Maya.
- En el sur sigue sin existir ninguna foto así; las aportará el equipo (decisión 16).

## Decisión 5 — "Qué hacer completo": todo sigue al lugar elegido
- **Postales:** las 6 fotos del lugar elegido.
- **Vive el sur:** primero las experiencias del lugar elegido; después, las del sur. Hay 9 en total, y las del norte van
  etiquetadas:
  - **Cancún:** zonas mayas (89,940 visitantes en 2025, INAH), la zona hotelera (estrellas) y antojitos (1,387 lugares,
    DENUE).
  - **Riviera Maya:** la Quinta Avenida (1,324 lugares para comer) y el Portal Maya (estrellas).
- **Rutas:**
  - Si se elige el norte, aparece **"Del Caribe al sur en Tren Maya"**: Cancún → Chetumal (334 km en línea recta) →
    Calderitas → Kohunlich, con el mejor mes del sur, mayo.
  - Además, "Cancún en 2 días" y "Playa del Carmen en un día". Su mes es el **menos lleno** de los meses secos y sin
    tormentas, que es abril, y se dice que aun así los hoteles van al 76 % y al 77 %.
  - Las rutas de Maya Ka'an y de la Laguna se retiraron.

## Decisión 6 — Chat en el idioma elegido
- El chat compara lo que se escribe con la pregunta **traducida**: por palabras en los idiomas con espacios y por pares de
  caracteres en chino, japonés y coreano.
- Responde en ese idioma. La respuesta y la fuente van en bloques separados para que cada una coincida con su frase del
  diccionario.
- **Ejemplos:** "When is the best time to go?" y "南部にサルガッサムはある" encuentran sus respuestas.

## Traducciones
- Se agregaron 79 frases nuevas en los 8 idiomas, para un total de **454 frases por idioma**, todas con sus marcas
  intactas.
- La barra de arriba se partió en pedazos (`data-bloque`), para que cada uno se traduzca solo, sin importar cuántos
  lugares estén llenos ese mes.

## Evidencia
- **Pruebas: 231 en total.**
  - `test_vitrina.py`: 5 lugares del viajero en postales y experiencias, el norte etiquetado, la ruta Tren Maya de
    334 km y el ejemplo a mano de estrellas (8,813,675 ÷ 13,006,487 = 67.8 %).
  - `test_fotos_lugares.py`: 48 fotos; las 8 de comida, solo del norte y con coordenada en su municipio.
  - `test_idiomas.py`: 454 frases por idioma.
- **Navegador:** sin errores JS, sin peticiones a internet, sin imágenes rotas y sin desborde, en escritorio y celular.
  Funcionan el chat en inglés y japonés, y el modo noche en todas las secciones.

## Consecuencia
La parte del viajero solo muestra lugares con datos. Quien llega pensando en Cancún o la Riviera Maya ve su información
real, las fotos de su comida y las estrellas de sus hoteles, y en cada sección se le ofrece bajar al sur.
