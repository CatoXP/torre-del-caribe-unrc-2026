# Guion del coloquio — "El sur tiene espacio" (15 minutos)

Equipo: **Brandon Uriel García Sánchez · Maribel Mondragón Mercado · Jesús Ramírez Isidro · Enrique González Ortega**
UNRC · LCDN 5° semestre 2026-2 · Problema Prototípico: *Turismo inteligente sustentable* (Quintana Roo).

> **Propuesta de reparto.** El equipo la ajusta como prefiera. Las reglas del coloquio: 15 minutos como máximo, **todos
> participan**, se defiende con evidencia y **la campaña es el centro**, no cada materia por separado. Por eso el orden
> sigue la historia de la campaña: la promesa, por qué, dónde y cuándo, cuánto y cómo se cuida, y cómo se mide.

**Qué tener abierto**
- La página con el servidor local (`cd backend && ..\.venv\Scripts\python -m torre.api.servidor` → http://127.0.0.1:8000).
- El PDF del documento ejecutivo.
- Sin internet también funciona.

---

## 0:00–0:45 · Apertura — Enrique
- **En pantalla:** la portada de la página, eligiendo Cancún en diciembre. Sale el aviso "lleno" y la recomendación de
  un lugar del sur.
- **Frase:** "Quintana Roo tiene el Caribe más visitado de México, pero no todo está lleno. Nuestra campaña se llama
  *El sur tiene espacio*, y cada cosa que promete está medida."
- **Cifra gancho:** Tulum recibió **1,031,443** visitantes en sus ruinas en 2025; las pirámides del sur, **66,628**:
  15.5 veces menos (INAH).

## 0:45–4:15 · El problema y los datos — Brandon
- **El problema en una cifra:** los 5 lugares tienen el **12.3 %** de la población del estado, pero reciben el **1.4 %**
  de los pasajeros de avión. Sección "El problema".
- **Los datos:**
  - **14 fuentes oficiales**, **8.1 millones de registros** y 6.1 millones de negocios del DENUE.
  - Procesados con **PySpark** de Bronze a Silver a Gold.
  - Consultables en un **almacén DuckDB** con modelo estrella y un diccionario de 56 tablas.
- **Calidad (incidente de Big Data, "fuentes que no coinciden"):**
  - en Mahahual, SITUR-Q cuenta entre 11 % y 35 % más cruceristas que DataTur;
  - se declara y no se cambia de fuente a la mitad.
- **El hallazgo que define a quién le habla la campaña:** al aeropuerto de Chetumal llegaron **250 extranjeros** en 2025;
  a Cancún, **9.4 millones**.
- **Si preguntan "¿y la ocupación del sur?":** SITUR-Q no la publica desde 2025. Es un hueco declarado, no se inventa;
  por eso el sur se mide con llegadas reales (INAH, Belice, Tren Maya).

## 4:15–7:45 · Dónde y cuándo — Maribel
- **Radar (dónde hay espacio hoy):**
  - un índice de presión con pesos iguales;
  - estados tranquilo, concurrido o saturado;
  - una regresión logística para el mes siguiente, que acierta 130 de 156 meses que nunca vio;
  - honestidad: repetir el mes anterior acierta 126, así que el modelo agrega poco y se dice.
- **Pronóstico (cuándo conviene ir):**
  - 5 modelos comparados en origen móvil y un rango del 90 % cuya cobertura se midió;
  - Poisson de tormentas: agosto **13.9 %**;
  - Monte Carlo de 10,000 futuros: escenarios malo, probable y bueno.
- **En pantalla:** "Así va a estar" con la Ruta en mayo, y la gráfica de escenarios (figura f12 del documento).
- **Si preguntan por la incertidumbre:** el rango del 90 % se cumplió entre 80 y 94 de cada 100 veces según la serie, y
  se reporta aunque haya salido peor.

## 7:45–11:15 · Cuánto dinero y cómo se cuida — Jesús
- **Optimización (Investigación de Operaciones):**
  - modelo estocástico de dos etapas con PuLP/CBC;
  - **$250,000 al año** (supuesto) → **957 visitantes** en 9 meses, **$196 cada uno**.
- **En vivo:** mover el presupuesto en "Pruébalo tú". El modelo se resuelve en ~0.3 s; con $500,000 salen 1,914
  visitantes.
- **La respuesta al incidente de IO, "¿cuánto cuesta la regla ambiental?":**
  - las reglas de temporada alta, capacidad y equidad cuestan **0 visitantes** a este presupuesto;
  - la que sí cuesta es el tope por canal (29.5 %), y se mantiene para no depender de una plataforma.
- **Frontera de Pareto:** se puede prometer que ningún mes con anuncio pasa del **40 %** de su capacidad sin perder un
  visitante.
- **Torre en vivo:**
  - **239 semanas reales** reproducidas con **Spark Structured Streaming**;
  - el anuncio se pausó **48 veces**;
  - el Isolation Forest marcó las 3 semanas de tormenta (Lisa, Nadine, Sara) sin saber que hubo tormenta.
- **En vivo:** "Escuchar en vivo" en la sección de la Torre.

## 11:15–14:15 · La campaña y cómo se mide — Enrique
- **Lo que dicen 85,987 reseñas:**
  - el ruido (2.76×), la suciedad (1.89×), el precio (1.66×) y las multitudes (1.52×) hunden una opinión;
  - la calma (0.41×) y la cultura (0.48×) la protegen.
  - "Eso es justo lo que el sur ofrece."
- **Dos viajeras:** "La que vuelve al sur" (nacional, 95 % de Oxtankah) y "La que baja del norte" (EE. UU. 56 %, Canadá
  17 %, ya en Cancún). Cada rasgo dice si es dato, cálculo, supuesto o hueco.
- **Marca:** "El sur tiene espacio", con un tono cercano, orgulloso de lo maya y lo mexicano, y aventurero.
- **Anuncios:**
  - 5 anuncios con su dato de respaldo, sin precios ni horas de viaje, porque no hay dato;
  - "La que baja del norte" solo se activa cuando Cancún está lleno y el sur tiene espacio.
- **10 indicadores con meta:** costo por visitante ≤ $196, +957 visitantes, 0 semanas con anuncio en temporada alta, ≤ 40 %
  de capacidad. El económico queda como hueco declarado.

## 14:15–15:00 · Cierre — Maribel
- "Elegimos promover sin crear un nuevo colapso: la campaña nunca anuncia un lugar lleno, se pausa sola con mal clima y
  manda a quien iba al norte hacia donde hay espacio."
- **Invitar a preguntas.** La evidencia de cada cifra está en `docs/trazabilidad.md`.

---

## Preguntas probables y quién responde
| Pregunta | Quién | Respuesta corta (con cifra) |
|---|---|---|
| ¿Por qué no promueven Tulum o Bacalar? | Brandon | Sargazo, cierres y saturación de 2026 (`REGIONES.md`); Tulum −31.3 % de visitas INAH en ene–jul 2026 |
| ¿Cómo saben que el modelo no se equivoca? | Maribel | Validación en origen móvil con meses que nunca vio; cobertura del 90 % medida y reportada |
| ¿Qué pasa si la campaña funciona demasiado bien? | Jesús | La Torre pausa; la capacidad probada y el tope de 40 % (Pareto) son restricciones del modelo |
| ¿Por qué Facebook se lleva el 70 %? | Jesús | 6.61 contra 1.59 visitantes por cada $1,000; sin tope se iría el 100 %, y el tope cuesta 29.5 % |
| ¿De dónde salen las personas? | Enrique | INAH (nacional/extranjero), Unidad de Política Migratoria (país, sexo, mes) y ENDUTIH; los huecos se declaran |
| ¿Y la privacidad? | Brandon | No se guarda ningún dato personal: todo viene agregado (DENUE sin teléfono ni correo; Rest-Mex sin identificadores) |
| ¿La página funciona sin internet? | Brandon | Sí: todo es local; la auditoría no encontró llamadas a otros sitios ni fallas WCAG 2.1 AA |
| ¿Probaron la página con personas? | Maribel | No. Se declara; se hizo una auditoría automática con axe-core (0 fallas en 4 vistas) |
