# Evidencias

Capturas de la página y de una solicitud de cotización real, tomadas con programas (Playwright), para que se puedan
repetir igual después de cualquier cambio.

## `pagina/`: la página, sección por sección

Cada sección de la página de la campaña (https://catoxp.github.io/torre-del-caribe-unrc-2026/), en el orden en que la ve
el viajero: portada, "Así va a estar", qué hacer, los lugares, cómo trabajamos, Descubre, la historia, Cotiza tu viaje,
consejos, fauna, cómo llegar, tu viaje soñado, preguntas, "¿Ibas al norte?" y "Los datos" (Radar, Pronóstico, presupuesto,
Torre en vivo y campaña). Al final: modo noche, inglés y celular.

## `solicitudes/`: cómo llega una solicitud a la base de datos

Hicimos una solicitud **de prueba** en la página, como lo haría un viajero, con datos evidentes de prueba (ningún dato
personal real). Se guardó en Firebase (Firestore, colección `solicitudes`) con el folio que está en
`folio_de_prueba.txt`.

| Paso | Captura | Qué pasa |
|---|---|---|
| 1 | `s1_pedido.png` | El viajero escribe su viaje con sus palabras y elige lugar, mes, días y personas. |
| 2 | `s2_plan.png` | La página arma el plan con piezas de nuestro catálogo (Gemini o, si no responde, reglas) y calcula el precio estimado con `cotizar.js`. La IA nunca pone el precio. |
| 3 | `s3_formulario.png` | "Quiero este viaje": nombre, cómo contactarlo, fechas y el aviso de privacidad. Sin la casilla de consentimiento no se envía. |
| 4 | `s4_folio.png` | El viajero recibe su folio (`TDC-AAMMDD-XXXXX`). Con ese folio el equipo encuentra la solicitud en la consola de Firebase. |
| 5 | `s5_consola_firestore.png` (si está) | El documento guardado en Firestore → `solicitudes`, visto desde la consola del equipo. |

### Qué se guarda y quién lo puede ver

- Cada solicitud es un documento cuyo nombre es el folio. Guarda: nombre, correo o teléfono, medio de contacto, personas,
  fechas, comentario, el plan, el precio estimado, el idioma, la fecha y el consentimiento.
- Las reglas de Firestore (`firebase/firestore.rules`) solo dejan **crear** solicitudes: con una sesión anónima, con el
  consentimiento marcado, con un folio de la forma correcta y con cada campo dentro de su tamaño. **Nadie puede leerlas,
  cambiarlas ni borrarlas desde la página**: solo el equipo, desde la consola de Firebase.
- La IA no recibe ningún dato personal: solo la descripción del viaje.
