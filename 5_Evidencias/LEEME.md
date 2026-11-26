# Evidencias

Capturas de la página y de una solicitud de cotización real, tomadas con programas (Playwright), para que se puedan
repetir igual después de cualquier cambio.

## `pagina/`: la página, sección por sección

Cada sección de la página de la campaña (https://catoxp.github.io/torre-del-caribe-unrc-2026/), en el orden en que la ve
el viajero: portada, "Así va a estar", qué hacer, los lugares, cómo trabajamos, Descubre, la historia, Cotiza tu viaje,
consejos, fauna, cómo llegar, tu viaje soñado, preguntas, "¿Ibas al norte?" y "Los datos" (Radar, Pronóstico, presupuesto,
Torre en vivo y campaña). Al final: modo noche, inglés y celular.

## `inferencia_y_firebase/`: cómo infiere la página y qué guarda Firebase

Recortes de la pieza exacta que se explica (no la página entera), tomados con
`backend/torre/documento/capturas_evidencias.py`. Se explican en el apartado 20 del documento ejecutivo.

| Captura | Qué muestra |
|---|---|
| `e01_radar_estados.png` | "Los datos": estado de cada lugar (tranquilo / concurrido / saturado / sin dato oficial) y el estado estimado del mes siguiente con su probabilidad. |
| `e02_radar_cancun_8_semanas.png` | Probabilidad de que Cancún se sature en cada una de las próximas 8 semanas. |
| `e03_radar_como_lo_sabemos.png` | Cómo se calcula el estado y cuántas veces acertó el modelo con meses que nunca vio. |
| `e04_planeador_meses.png` | El planeador: cada mes con su color (tranquilo, normal, temporada alta). |
| `e05_pronostico_mes.png` | El pronóstico de un mes con su rango ("muy probablemente entre…"). |
| `e06_temporada_alta_otra_opcion.png` | Mes de temporada alta: la página propone otro lugar del sur u otro mes. |
| `e07_ibas_al_norte.png` | Cancún en temporada alta (referencia) y la recomendación de ir al sur. |
| `e08_cotiza_quien_armo_el_plan.png` | "Cotiza tu viaje": quién armó el plan (IA o reglas) y el mes según nuestro pronóstico. |
| `e09_cotiza_un_dia_y_resumen.png` | Un día del plan con lugares reales del catálogo y el resumen sin precio. |
| `e10_ia_recibe.png` | Lo que la página manda a Gemini: el pedido sin datos personales y el catálogo cerrado con ids, sin precios. |
| `e11_celular_pronostico.png` | El pronóstico en un celular. |
| `e12_firebase_corazones.png` | Los contadores de corazones (`fotos/{id}`) leídos en vivo con la sesión anónima. |
| `e13_documento_solicitud.png` | Copia de `solicitudes/s5_documento_enviado.png`. |
| `e14_folio.png` | Copia de `solicitudes/s4_folio.png`. |

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
| 5 | `s5_documento_enviado.png` | El documento exacto que la página manda a Firestore, copiado en el navegador al enviar (también en `documento_de_prueba.json`). La página no puede volver a leerlo: las reglas solo dejan crear. |
| 6 | `s6_consola_firestore.png` (si está) | El mismo documento guardado en Firestore → `solicitudes`, visto desde la consola del equipo. La toma a mano quien tiene la cuenta de Google del equipo. |

**Después del folio.** La solicitud se queda guardada en Firestore con `estado: "nueva"`. No se manda ningún correo
automático (no hay extensión Trigger Email ni funciones en el servidor) y no hay un panel del equipo: el equipo abre la
consola de Firebase, busca el folio en `solicitudes` y le escribe al viajero por el medio que eligió.

### Qué se guarda y quién lo puede ver

- Cada solicitud es un documento cuyo nombre es el folio. Guarda: nombre, correo o teléfono, medio de contacto, personas,
  fechas, comentario, el plan, el precio estimado, el idioma, la fecha y el consentimiento.
- Las reglas de Firestore (`firebase/firestore.rules`) solo dejan **crear** solicitudes: con una sesión anónima, con el
  consentimiento marcado, con un folio de la forma correcta y con cada campo dentro de su tamaño. **Nadie puede leerlas,
  cambiarlas ni borrarlas desde la página**: solo el equipo, desde la consola de Firebase.
- La IA no recibe ningún dato personal: solo la descripción del viaje.
