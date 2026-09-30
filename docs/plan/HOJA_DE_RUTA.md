# Torre del Caribe
## Hoja de ruta del proyecto

---

## 1. Dónde está el proyecto (28 de septiembre de 2026, actualizado)

| Fase | Qué es | Estado |
|---|---|---|
| Plan y regiones | Plan aprobado; **5 regiones** a promover (sur y Maya Ka'an); Cancún, Riviera Maya y Tulum solo como referencia | ✅ Terminado (revisado el 28-sep) |
| Fase 0 — Preparación | Computadora lista para procesar datos grandes (PySpark, Java 17) | ✅ Terminado |
| Fase 1 — Recolección de datos | 353 archivos oficiales, 8,134,802 registros, costos publicitarios y evidencia de sargazo | ✅ Terminado |
| Fase 2 — Limpieza y orden de datos | Convertir los datos crudos en tablas limpias (Silver) y tablas finales (Gold) | 🔄 En curso (SITUR-Q, ocupación SECTUR 2022–2026, DENUE, INAH, Censo, huracanes, clima y tipo de cambio listos; faltan nacionalidades, reseñas, vuelos y cruceros —antes de la Fase 8— y el catálogo de datos y DuckDB —Fase 9—) |
| Página web | Sistema "Sur mexicano": los 5 lugares en mapa 3D, cómo llega la gente, dónde se queda el dinero, las 12 fases, quiénes somos y preguntas rápidas | 🔄 En curso |
| Fase 3 — Planteamiento con datos | Tabla de criterios de las 5 regiones, variables y actores | ✅ Lista para revisión (las 5 regiones pasan los criterios; notebook 01 con variables, actores y concentración: los 5 lugares tienen el 12.3 % de la población pero el 1.4 % de las llegadas en avión) |
| Fase 4 — Radar | Índice de presión y estados tranquilo / concurrido / saturado, con predicción del mes siguiente | ✅ Auditada y lista para revisión (índice de presión con llegadas por cuarto, predicción del mes siguiente con regresión logística, cadena de Markov del norte, clustering de 55 centros del país, notebook 02 y sección del Radar en la página; los 5 lugares, tranquilos en jul-2026) |
| Fases 5 a 11 | Pronóstico, presupuesto, torre en vivo, campaña, backend y cierre | ⏳ Pendiente |

**Cómo se trabaja cada fase:** primero se explica qué se hará y con qué dato; si hay una decisión real, Brandon
elige entre 2 o 3 opciones; se programa en piezas pequeñas; se prueba con cifras oficiales conocidas; se agrega el
capítulo correspondiente al documento ejecutivo en PDF.

---

## 2. Dos frentes que avanzan juntos

La campaña necesita dos cosas: **evidencia** (datos y modelos) y **una página web** que la muestre de forma atractiva
a cualquier persona. Por decisión del responsable técnico, ambos frentes avanzan al mismo tiempo:

| Frente de datos y modelos | Frente de la página web |
|---|---|
| Limpia los datos, construye los modelos y calcula los resultados | Muestra esos resultados con el sistema visual "Sur mexicano" (colores mexicanos en bloques, greca maya, fotos grandes; `docs/decisiones/07-diseno.md`) |
| Cada resultado queda en una tabla final (Gold) | La página lee esas tablas; cada vez que un modelo termina, su sección se "enciende" con datos reales |

---

## 3. Qué sigue, fase por fase

### Fase 2 — Limpieza y orden de los datos (en curso)
- **Qué se hace:** PySpark convierte los 8 millones de registros en tablas uniformes. Pone nombres claros, corrige
  tipos de dato, marca los huecos y suma las estaciones del Tren Maya. Después arma las tablas finales por destino y
  mes (Gold).
- **Avance:** listos SITUR-Q (12 indicadores) y la ocupación hotelera de SECTUR, que cubre **de 2022 a 2026** (239
  semanas por centro de Quintana Roo), y el directorio de negocios DENUE completo (6,138,075 negocios; 13,663
  turísticos en Quintana Roo). Siguen nacionalidades, zonas arqueológicas, vuelos, cruceros, clima, huracanes, reseñas
  y población.
- **Se entrega:** tablas limpias, diccionario de datos, reporte de calidad y comparación entre las dos fuentes que miden
  lo mismo (SITUR-Q contra DataTur en Cancún y Riviera Maya).

### Página web (en paralelo; pensada para público no técnico)
1. **Portada:** "El sur tiene espacio." Teléfono con los 5 lugares y tarjetas con cifras reales de esos lugares (por
   ejemplo, "4 de cada 10 cuartos vacíos en Chetumal durante 2024"). Nada del norte en la portada.
2. **"Conoce los 5 lugares":** mapa con los lugares numerados y una ficha de cada uno: lugares para comer y para
   dormir, cuánta gente vive ahí, cuántos llegaron en tren o visitaron sus pirámides, y un aviso de cuidado. Si un
   dato no existe, la ficha dice "sin dato". Después se conectará al Radar (Fase 4).
3. **"¿Por qué el sur?":** Cancún y la Riviera Maya solo como referencia ("de cada 10 cuartos, 7 ocupados").
4. **Así llega la gente:** mapa de todo el estado con las llegadas por avión, Tren Maya, crucero y frontera.
5. **Dónde se queda el dinero:** tamaño de los hoteles por destino y hospedajes chicos, medianos y grandes.
6. **Las 12 fases:** tarjetas que se llenan conforme avanza el proyecto.
7. **Quiénes somos** y **fuentes**, con nombres completos y botón para descargar el documento del proyecto.
8. **Preguntas rápidas:** asistente con respuestas fijas sacadas de los datos, cada una con su fuente.

Todo funciona sin internet, en la computadora, y se ve bien en celular.

### Fase 3 — Planteamiento con datos
- Tabla que califica las 5 regiones con los 5 criterios de selección, con Cancún, Riviera Maya y Tulum como referencia.
- **Decisión de Brandon:** cómo medir la presión turística en 2025–2026, cuando no hay ocupación oficial. Las opciones
  son usar llegadas medidas (Tren Maya, cruceros, Belice, habitaciones) o estimar la ocupación, marcándola como estimada.

### Fase 4 — Radar (¿dónde hay espacio?)
- Índice de presión turística por destino y semana; un modelo que clasifica cada destino como tranquilo, concurrido o
  saturado; y la probabilidad de que cambie en las próximas semanas (cadena de Markov).
- **Decisión de Brandon:** cuánto pesa cada factor del índice y dónde van los cortes entre tranquilo, concurrido y
  saturado.
- **Página:** la sección "¿Dónde hay espacio hoy?" pasa a datos del modelo.

### Fase 5 — Pronóstico (¿cuándo conviene ir?)
- Pronóstico de visitantes por mes con rango de confianza del 90 %, probabilidad de huracán por mes (175 años de
  registros) y escenarios malo, probable y bueno.
- **Página:** calendario de 12 meses tipo aplicación del clima, y la pestaña de escenarios.

### Fase 6 — Reparto del presupuesto
- Modelo de optimización que decide cuánto invertir por mes, destino y canal, sin rebasar la capacidad y con un piso
  mínimo para cada comunidad. Usa los costos publicitarios ya reunidos.
- **Decisión de Brandon:** qué se maximiza (visitantes o derrama) y cuáles restricciones son indispensables.
- **Página:** pestaña "Presupuesto" con controles que recalculan en vivo.

### Fase 7 — Torre en vivo (¿qué hace la campaña esta semana?)
- Reproduce semana a semana los datos reales de 2024 a 2026, detecta semanas anómalas y aplica las reglas de pausa (por
  ejemplo, sargazo en la Bahía de Chetumal).
- **Página:** pestaña "En vivo" con las decisiones que aparecen semana a semana.

### Fase 8 — La campaña
- Minería de 85,993 reseñas de Quintana Roo, buyer persona con datos reales (origen, sexo y aeropuerto de llegada),
  marca, mensajes, piezas publicitarias e indicadores.
- **Decisión de Brandon:** nombre de la campaña, tono y mensajes.
- **Página:** sección "La campaña".

### Fase 9 — Conexión de la página con el sistema
- Un servidor local que calcula en vivo (optimización y escenarios) y entrega los datos a la página.

### Fase 10 — Pulido final de la página
- Revisión en celular y escritorio, capturas para el documento y una prueba con una persona no técnica.

### Fase 11 — Cierre
- Documento ejecutivo completo, notebooks por materia, ensayo del coloquio de 15 minutos con reparto entre los
  integrantes.

---

## 4. Decisiones ya tomadas

| Decisión | Motivo principal |
|---|---|
| Estado: Quintana Roo | Es donde hay datos oficiales confirmados de todas las fuentes |
| Se promueve una ruta de cultura, bahía, lagunas y comunidad, no playa | Sargazo récord en 2026 y crisis de Tulum (−31.3 % de visitantes) |
| 5 regiones: Chetumal, Bahía Calderitas–Oxtankah, Ruta arqueológica del sur, Maya Ka'an + Kantemó y Laguna Milagros–Xul-Ha | Sin sargazo en su costa, sin cierres y sin saturación (datos del INAH y noticias de 2026) |
| Cancún, Riviera Maya y Tulum solo como referencia | Ahí está el turista al que se le habla, y ahí está la única ocupación hotelera medida en 2025–2026 |
| Sistema de tres horizontes: hoy, próximos meses y esta semana | Cada módulo responde una sola pregunta y no se enciman |
| Todo se construye desde cero, sin el proyecto anterior | Decisión del responsable técnico |
| La página se construye en paralelo | Lo visual es la prioridad del proyecto |
| DENUE se procesa completo (6.1 millones de negocios) | Volumen real para el criterio de Big Data |
| Oferta turística = giros característicos del turismo (SECTUR/INEGI) | Criterio oficial y defendible |

---

## 5. Riesgos y datos que no existen

| Tema | Situación | Cómo se maneja |
|---|---|---|
| Ocupación hotelera 2025–2026 | No existe en SITUR-Q para ningún destino; SECTUR sí la tiene para los 7 centros del norte | Decisión en la Fase 3 |
| Isla Mujeres | Las noticias decían 93.5–95 % de ocupación; SECTUR registra 74.7 % y 43.2 % (feb y abr 2026) | Queda fuera por el foco en 5 regiones; se conserva como ejemplo de fuentes que no coinciden |
| Sargazo en la Bahía de Chetumal | En los canales de entrada, no en la costa (28-sep) | Vigilancia; pausa automática si llega a la costa |
| Conversión en Facebook para turismo | No está publicada | Supuesto declarado en la Fase 6 |
| Costos publicitarios | Son promedios de EE. UU. | Se usan como referencia, no como medición de México |
| Laguna Milagros–Xul-Ha | Sin estadística turística propia | Se mide con población y directorio de negocios; se declara |
