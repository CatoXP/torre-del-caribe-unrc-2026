# 23 — Fase 10: página final, auditada sin prueba con personas

Autor: **Brandon Uriel García Sánchez** · 02-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Decisión
El plan pedía una "prueba de 5 segundos con una persona no técnica por sección".

Brandon eligió **"Solo la revisión automática"**:
- la Fase 10 se cierra con una auditoría automática;
- se **declara que no hubo prueba con personas**.

Opción descartada: dejar un guion para que el equipo hiciera la prueba con 3 a 5 personas. La fase quedaba abierta hasta
tener las respuestas.

## Qué se revisó (`backend/torre/documento/auditoria.py` → `docs/ejecutivo/AUDITORIA_PAGINA.md`)
- **Vistas:** cuatro: escritorio y celular, de día y de noche.
- **Accesibilidad:** con **axe-core**, el estándar abierto que usan los navegadores, sobre las reglas **WCAG 2.1 A y
  AA**.
- **Reglas del proyecto:**
  - sin errores de JavaScript;
  - sin llamadas a otros sitios;
  - sin imágenes rotas;
  - sin desborde;
  - un solo título principal;
  - botones con nombre;
  - recorrido con teclado con marca visible.

## Qué se encontró y cómo se corrigió
**Primera auditoría:** 1 a 3 reglas fallaban por vista, con **67** elementos en escritorio de día.

| Falla | Causa | Arreglo |
|---|---|---|
| Contraste en "Los lugares" (53 elementos) | Las fichas no activas se desvanecían enteras al 35 % | Solo se desvanece la foto; el texto queda legible |
| Etiquetas "Dato" (3.18:1) | Blanco sobre turquesa | Texto oscuro |
| Énfasis turquesa en títulos (2.98:1) | Turquesa sobre crema | Tono #00857F de día (el turquesa sigue de noche) |
| "ESPACIO" amarillo sobre rosa (2.49:1) | Amarillo sobre rosa | Tinta |
| Textos claros sobre verde y rosa (3.8–4.5:1) | Transparencia del texto | Texto más opaco o blanco |
| Botón de rutas de noche (1.52:1) | Texto claro sobre amarillo | Texto oscuro |
| Botón del chat sin nombre en celular | El texto se oculta en pantallas chicas | `aria-label="Pregúntanos"` |
| Tablas que se desplazan sin teclado | No eran enfocables | `tabindex="0"` y `role="region"` |

- **Auditoría final:** **0 fallas en las cuatro vistas**.
  - 32–33 reglas pasan.
  - Teclado: 40 de 40 tabulaciones con marca visible.
  - 0 errores de JavaScript, 0 llamadas a otros sitios y 0 imágenes sin texto alternativo.
- **Un falso positivo:** la auditoría medía las tarjetas de las fases a media animación. Ahora espera a que terminen.

## También en esta fase
**"Quiénes somos"** con los cuatro integrantes que confirmó Brandon: Brandon Uriel García Sánchez, Maribel Mondragón
Mercado, Jesús Ramírez Isidro y Enrique González Ortega.

## Consecuencia
La Fase 10 queda **lista, con la limitación declarada**: no hubo prueba con personas. Si el equipo la hace después, el
guion propuesto es simple:
1. 5 segundos por sección;
2. preguntar "¿qué entendiste?";
3. anotar si coincide con la pregunta de la sección.
