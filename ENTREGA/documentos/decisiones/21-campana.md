# 21 — Fase 8: la campaña "El sur tiene espacio"

Autor: **Brandon Uriel García Sánchez** · 02-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## La pregunta
¿A quién le habla la campaña, con qué palabras, en qué canal, cuándo y cómo se sabe si funciona? Cubre estos elementos
obligatorios del Problema Prototípico:
- buyer persona;
- branding;
- medios justificados con datos;
- piezas publicitarias;
- implementación;
- indicadores.

Responde también al incidente de mercadotecnia: promover sin provocar un nuevo colapso.

## Decisiones de Brandon (02-oct-2026)
| Decisión | Elegida | Descartadas |
|---|---|---|
| Personas | **Dos:** "La que vuelve al sur" (nacional) y "La que baja del norte" (EE. UU. o Canadá, ya en Cancún o la Riviera) | Solo la nacional (deja fuera al extranjero que ya está a 334 km); solo la extranjera (la Bahía es 95 % nacional) |
| Nombre | **"El sur tiene espacio"** ("The south has room") | "Sur sin prisa" (no dice dónde); "Del Caribe al sur" (solo sirve para la extranjera) |
| Tono | **Combinar los tres:** cercano y tranquilo, orgullo cultural y aventura. En palabras de Brandon: "es un orgullo ser mexicano" | Uno solo de los tres |

## Minería de texto (`backend/torre/campana/texto.py`)
**Corpus:** 85,987 reseñas de Quintana Roo de Rest-Mex 2025 (Tulum, Isla Mujeres y Bacalar). Ninguna es de los 5
lugares; muchas son traducciones.
- **Temas con un léxico a la vista**, no LDA, porque así cada tema se define y se defiende palabra por palabra.
  - Riesgo relativo de que una reseña sea mala (1–2 estrellas) cuando toca el tema:

    | Tema | Riesgo relativo |
    |---|---:|
    | Ruido | 2.76 |
    | Suciedad | 1.89 |
    | Precio | 1.66 |
    | Multitudes | 1.52 |
    | Servicio | 1.18 |
    | Comida | 0.81 |
    | Naturaleza | 0.73 |
    | Cultura | 0.48 |
    | Calma | 0.41 |

- **Reglas de asociación (Apriori, soporte ≥ 0.1 %):**
  - Hacia reseña mala: ruido + servicio (lift 2.82), suciedad + multitudes (2.59), suciedad + precio (2.54).
  - Hacia reseña de 5: comida + servicio (1.12), calma + naturaleza (1.10).
- **Lenguaje real:**
  - Las reseñas de 5 estrellas dicen "excelente, increíble, hermoso, deliciosa, amable, ruinas, ambiente".
  - Las malas dicen "peor, horrible, dinero, caro, sucia, grosero".
  - Método: log-odds con prior de Dirichlet informativo.

**Conclusión:** lo que hunde una reseña es lo que sobra en los destinos llenos; lo que la protege (calma y cultura) es lo
que el sur ofrece. Esa es la promesa de la marca.

## Personas (`backend/torre/campana/marca.py`)
Cada rasgo lleva su etiqueta:
- **dato:** medido por una fuente oficial;
- **derivado:** calculado de datos;
- **supuesto:** no hay dato y se declara;
- **hueco:** no hay dato y no se llena.

**La que vuelve al sur**
| Rasgo | Valor | Etiqueta |
|---|---|---|
| Origen | Nacional: 94.8 % de los visitantes de Oxtankah y 63.3 % de los de la Ruta en 2025 (INAH) | dato |
| Cuándo viaja | De diciembre a abril; la campaña la invita en los meses con espacio | derivado |
| Qué valora y qué la aleja | Calma y cultura; ruido, suciedad, precio y multitudes (reseñas) | derivado |
| Cómo se informa | Mensajería 90.6 % y redes 80.4 % (ENDUTIH 2025) | dato |
| Estado de origen, edad e ingreso | No hay dato oficial | hueco |

**La que baja del norte**
| Rasgo | Valor | Etiqueta |
|---|---|---|
| Origen | De los 9,408,423 extranjeros que llegaron a Cancún en 2025, 56.3 % de Estados Unidos y 17.1 % de Canadá | dato |
| Sexo | 53.4 % mujeres | dato |
| Por qué no llega sola al sur | El aeropuerto de Chetumal recibió solo 250 extranjeros | dato |
| Cuándo está | Máximo en marzo, mínimo en septiembre | dato |
| Cómo se informa | Busca en Google y usa redes desde el destino | supuesto (sin encuesta propia) |

## Marca, mensajes y medios
- **Marca:**
  - Lema: "Pirámides, bahía y sabor del sur, con espacio para disfrutarlos".
  - Propuesta de valor: zonas mayas con 15.5 veces menos visitantes que Tulum (INAH 2025: 1,031,443 contra 66,628).
  - Posicionamiento: la opción cultural y tranquila del Caribe mexicano.
  - Elementos visuales: el sistema "Sur mexicano".
- **Mensajes:** 5 anuncios.
  - Google en español e inglés, Facebook/Instagram en español e inglés, y WhatsApp orgánico.
  - Cada uno tiene su dato de respaldo y los largos se revisan contra los límites de la plataforma: Google, título ≤ 30 y
    descripción ≤ 90; Meta, título ≤ 40 y texto ≤ 125.
  - **Sin precios ni horas de viaje**, porque no hay dato.
  - Las maquetas usan fotos reales comprobadas.
  - El dominio de los anuncios es el de la página real. Se quitó un dominio inventado de la primera versión.
- **Medios:**
  - Facebook/Instagram 70 % y Google 30 % (Fase 6).
  - WhatsApp y el botón de compartir, sin costo (90.6 % usa mensajería).
  - La página como destino de todos los anuncios.
- **Implementación:**
  - 9 meses de plan (oct-2026 a jun-2027).
  - "La que baja del norte" se activa solo en los meses en que Cancún está en temporada alta y el sur tiene espacio.
    Además, la Torre (Fase 7) la enciende por semana.
- **Indicadores (10):**
  - alcance, interacción (CTR ≥ 8.73 % / 2.76 %), conversión (≥ 5.75 %), costo por visitante (≤ $196);
  - afluencia (+957 sobre el escenario probable), presupuesto (100 %);
  - económico (**hueco:** SITUR-Q no publica ocupación del sur desde 2025);
  - social (nunca "saturado"), ambiental (0 semanas con anuncio en temporada alta o con mal clima), capacidad (≤ 40 %).

## Evidencia
- `tests/test_campana.py` (6 pruebas):
  - riesgo relativo a mano;
  - lift de ruido + servicio de 2.82;
  - palabras y tokens;
  - personas etiquetadas;
  - mensajes con respaldo y dentro de los límites, sin "$" ni "hora", con fotos que existen;
  - calendario coherente y sin dominio inventado.
- `notebooks/07_campana.ipynb`.
- `docs/metodologia/ECUACIONES.md` §6.0.
- Página: sección "El sur tiene espacio" en "Los datos".

## Consecuencia
La Fase 8 queda **lista**. Las fases 9 (backend), 10 (página final con prueba de personas reales) y 11 (cierre y
coloquio) son las que siguen.

**Limitaciones declaradas:**
- Rest-Mex no cubre los cinco lugares;
- no hay estado de origen, edad ni ingreso del visitante nacional;
- los costos y las conversiones son promedios de EE. UU.;
- el alcance no tiene meta hasta el primer mes real.
