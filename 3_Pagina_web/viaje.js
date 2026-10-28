/*
  Autor: Brandon Uriel García Sánchez
  Módulo: Campaña (Cotiza tu viaje: el plan)
  Qué hace:          La lógica del plan de viaje de "Cotiza tu viaje" (la usa app.js, en la página y en la aplicación de
                     teléfono, que es la misma página en modo aplicación): el catálogo cerrado que puede usar la IA, el
                     armador por reglas, la revisión de lo que responde Gemini, el "por qué" del mes, el folio del cliente
                     y el documento que se guarda en Firestore.
  Por qué así:       Decisiones 33 y 35. Se separó de app.js cuando la aplicación tenía su propio código, para que no
                     hubiera dos copias de estas reglas (lo mismo que nos pasó con los notebooks, decisión 32). Hoy la
                     aplicación es la página, y el archivo se queda aparte porque son funciones puras (sin página ni red) para probarlas con Node
                     (tests/test_viaje.py), igual que cotizar.js. El precio NO está aquí: lo calcula cotizar.js.
  Datos de entrada:  window.TORRE_DATOS (pagina.js ← backend/torre/api/datos_pagina.py).
  Alimenta a:        Campaña: el plan de "Cotiza tu viaje" en la página y en la aplicación.
*/
(function (raiz) {
  "use strict";
  const MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
  const mesLargo = (ym) => { const [a, m] = ym.split("-").map(Number); return `${MESES[m - 1]} de ${a}`; };
  const num = (n) => Number(n).toLocaleString("es-MX");
  const MOMENTO_TXT = { dia: "Mañana", tarde: "Tarde", noche: "Noche" };
  const INTERES = { cultura: "Cultura maya", mar: "Mar y bahía", naturaleza: "Naturaleza", sabores: "Sabores", noche: "Noche" };
  const NIVEL_TEXTO = { alta: "Temporada alta", normal: "Mes normal", tranquila: "Mes tranquilo", "sin dato": "Sin dato de afluencia" };

  // Los lugares que se venden: los del sur. Cancún y la Riviera Maya son referencia y no entran al plan (decisión 17).
  const lugaresSur = (D) => (D.pronostico ? D.pronostico.lugares.filter((L) => L.papel !== "referencia") : []);

  // Catálogo cerrado: lo único que la IA puede elegir. Cada negocio y zona lleva un id estable.
  function catalogoViaje(D) {
    const P = D.pronostico, ids = new Map(), lugares = [];
    for (const L of lugaresSur(D)) {
      const item = (x, tipo, momento, k) => { const id = `${L.clave.slice(0, 3).toLowerCase()}-${tipo}-${momento}-${k}`; ids.set(id, { ...x, tipo, momento, lugar: L.clave }); return { id, n: x.n, t: x.t, km: x.km }; };
      const g = { zonas: L.zonas.map((z, k) => item(z, "zona", "dia", k)) };
      for (const m of ["dia", "tarde", "noche"]) {
        g[`hacer_${m}`] = L.hacer[m].slice(0, 6).map((x, k) => item(x, "hacer", m, k));
        g[`comer_${m}`] = L.comer[m].slice(0, 6).map((x, k) => item(x, "comer", m, k));
      }
      g.dormir = L.dormir.slice(0, 6).map((x, k) => item(x, "dormir", "noche", k));
      lugares.push({ clave: L.clave, nombre: L.nombre,
        meses: L.calendario.map((c, i) => ({ i, mes: mesLargo(P.meses[i]), nivel: c.nivel, lluvia_mm: c.lluvia, temp_max: c.temp, tormenta: c.tormenta })),
        intereses: Object.keys(INTERES).filter((k) => L.fotos.some((f) => (f.interes || []).includes(k))), ...g });
    }
    return { lugares, ids };
  }

  // Palabras del texto libre que delatan un interés (para el respaldo por reglas; la IA lee el texto completo).
  const PALABRAS_INTERES = { cultura: /histori|ruina|pir[aá]mide|maya|arqueol|museo|cultura|templo/i, mar: /\bmar\b|playa|bah[ií]a|nadar|agua|laguna|muelle/i,
    naturaleza: /naturaleza|selva|aves|p[aá]jaro|caminar|aire libre|animal/i, sabores: /comer|comida|marisco|sabor|restaurante|gastronom|cenar|tacos/i,
    noche: /noche|fiesta|\bbar\b|m[uú]sica|baile/i };
  const interesesDelTexto = (texto) => Object.keys(PALABRAS_INTERES).filter((k) => PALABRAS_INTERES[k].test(texto));

  // El "por qué" del mes siempre lo escribe la página con el pronóstico, nunca la IA: en la prueba del 19-oct-2026
  // Gemini llamó "tranquila" a una temporada alta.
  function porqueDelMes(D, L, mes) {
    const c = L.calendario[mes];
    return `${L.nombre} en ${mesLargo(D.pronostico.meses[mes])}: ${NIVEL_TEXTO[c.nivel].toLowerCase()} según nuestro pronóstico, con ${num(c.lluvia)} mm de lluvia en un mes normal.`;
  }

  // Respaldo por reglas: el mismo catálogo, sin IA.
  function armarPorReglas(p, cat, D) {
    const sur = lugaresSur(D);
    let L = sur.find((x) => x.clave === p.lugar);
    if (!L) {
      const puntos = (x) => p.intereses.reduce((a, k) => a + x.fotos.filter((f) => (f.interes || []).includes(k)).length, 0) + (p.intereses.includes("cultura") ? x.zonas.length * 2 : 0);
      L = [...sur].sort((a, b) => puntos(b) - puntos(a))[0];
    }
    const C = cat.lugares.find((x) => x.clave === L.clave);
    let mes = p.mes;
    if (mes === null || mes === undefined) { mes = L.calendario.findIndex((c) => c.nivel === "tranquila"); if (mes < 0) mes = Math.max(0, L.calendario.findIndex((c) => c.nivel !== "alta")); }
    const toma = (lista, k) => (lista.length ? [lista[k % lista.length].id] : []);
    const dias = Array.from({ length: p.dias }, (_, d) => {
      const tranquilo = p.ritmo === "tranquilo";
      const manana = d < C.zonas.length ? [C.zonas[d].id] : toma(C.hacer_dia, d);
      const momentos = [
        { momento: "dia", ids: [...manana, ...toma(C.comer_dia, d)] },
        { momento: "tarde", ids: [...(tranquilo ? [] : toma(C.hacer_tarde, d)), ...toma(C.comer_tarde, d)] },
        { momento: "noche", ids: [...toma(C.comer_noche, d), ...(d < p.dias - 1 ? toma(C.dormir, 0) : [])] },
      ].filter((m) => m.ids.length);
      return { momentos };
    });
    return { lugar: L.clave, mes, dias, fuente: "reglas", porque: porqueDelMes(D, L, mes) };
  }

  // Modelos de Gemini en orden de preferencia. Si uno falla se prueba el siguiente, porque cada modelo tiene su propia
  // cuota. Lo que vimos el 19-oct-2026: gemini-2.5-flash fue retirado (404), el nivel gratuito permite unos 5 pedidos
  // por minuto por modelo (429) y en horas pico Google responde "mucha demanda" (500).
  const MODELOS_IA = ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-flash-lite-latest"];
  const INSTRUCCION_IA = "Eres el planeador de viajes de Torre del Caribe, un equipo que vende viajes al sur de Quintana Roo (México). " +
    "Arma un itinerario usando SOLO los ids del catálogo que te damos (zonas arqueológicas y negocios reales del directorio del INEGI). " +
    "Nunca inventes lugares, negocios, horarios ni precios. Prefiere los meses con nivel 'tranquila' (hay espacio) salvo que el viajero pida un mes. " +
    "Cada día tiene momentos 'dia', 'tarde' y 'noche'; en la noche incluye un lugar para dormir excepto el último día. " +
    "Responde SOLO con JSON: {\"lugar\": clave, \"mes\": índice del mes, \"dias\": [{\"momentos\": [{\"momento\": \"dia\"|\"tarde\"|\"noche\", \"ids\": [id...], \"nota\": texto corto}]}], \"encaja\": texto}. " +
    "Escribe 'nota' y 'encaja' en el idioma del viajero. 'encaja' es UNA frase sobre por qué estos lugares van con lo que pidió el viajero; " +
    "no menciones el mes, el nivel, la lluvia ni ninguna cifra (eso lo explica la página).";

  // Gemini por Firebase AI Logic: configuración de un modelo. thinkingBudget 0: sin "razonamiento" extra. Medido el
  // 19-oct-2026 con el mismo pedido: 16.3 s → 4.2 s, y el plan siguió pasando la validación de ids. Los modelos "lite" no
  // aceptan ese ajuste (400) y ya responden en ~2 s.
  function modeloIA(ai, app, nombre) {
    return ai.getGenerativeModel(ai.getAI(app, { backend: new ai.GoogleAIBackend() }), {
      model: nombre,
      generationConfig: { responseMimeType: "application/json", temperature: 0.4, ...(/lite/.test(nombre) ? {} : { thinkingConfig: { thinkingBudget: 0 } }) },
      systemInstruction: INSTRUCCION_IA,
    });
  }

  function validarIA(x, p, cat) {
    const L = cat.lugares.find((l) => l.clave === x?.lugar);
    if (!L || !Number.isInteger(x.mes) || !L.meses[x.mes] || !Array.isArray(x.dias) || x.dias.length !== p.dias) return null;
    for (const d of x.dias) {
      if (!Array.isArray(d.momentos) || !d.momentos.length) return null;
      for (const m of d.momentos) {
        if (!MOMENTO_TXT[m.momento] || !Array.isArray(m.ids) || !m.ids.length || m.ids.length > 4) return null;
        if (m.ids.some((id) => !cat.ids.has(id))) return null;  // un id inventado tumba toda la respuesta
        m.nota = typeof m.nota === "string" ? m.nota.slice(0, 220) : "";
      }
    }
    // El mes: si el viajero eligió uno, manda el suyo. Si no, y la IA propone uno que no es tranquilo, se cambia al primer
    // mes tranquilo del lugar (la campaña manda a la gente a donde hay espacio).
    let mes = x.mes;
    if (Number.isInteger(p.mes) && L.meses[p.mes]) mes = p.mes;
    else if (L.meses[mes].nivel !== "tranquila") { const t = L.meses.findIndex((m) => m.nivel === "tranquila"); if (t >= 0) mes = t; }
    // La frase de la IA solo se queda si no trae cifras: las cifras salen de nuestros datos, no de la IA.
    const encaja = typeof x.encaja === "string" && !/\d/.test(x.encaja) ? x.encaja.slice(0, 300) : "";
    return { lugar: x.lugar, mes, dias: x.dias, encaja, fuente: "ia" };
  }

  // Folio del cliente (su ID): fecha + 5 caracteres al azar, sin 0/O ni 1/I/L para dictarlo sin confusiones.
  const ALFABETO_FOLIO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  function nuevoFolio(hoy = new Date()) {
    const d = `${String(hoy.getFullYear()).slice(2)}${String(hoy.getMonth() + 1).padStart(2, "0")}${String(hoy.getDate()).padStart(2, "0")}`;
    const azar = crypto.getRandomValues(new Uint32Array(5));
    return `TDC-${d}-${[...azar].map((x) => ALFABETO_FOLIO[x % ALFABETO_FOLIO.length]).join("")}`;
  }

  /**
   * El documento de la colección "solicitudes" (Firestore). Lo validan las reglas de firebase/firestore.rules
   * (torre.campana.nube): campos, tamaños y consentimiento. Junto va el costo estimado interno (cotizar.js) para que el
   * equipo arme el precio; el viajero no lo ve.
   * @param {object} c { folio, datos, it, p, q, L, mes (texto), cat, uid, idioma, creado, canal }
   */
  function documentoSolicitud(c) {
    const { datos, it, p, q, L, cat } = c;
    const itinerario = JSON.stringify({ lugar: L.nombre, mes: c.mes, dias: p.dias, pedido: p.texto, intereses: p.intereses, hospedaje: p.hospedaje,
      desde: p.vuelo ? "Vuelo desde otro país (llegada sugerida: Cancún) y Tren Maya al sur" : p.desdeCancun ? "Cancún / Playa del Carmen" : "sur",
      vuelo: p.vuelo ? { necesita: true, sale_de: p.salida || "sin especificar", llegada_sugerida: "Cancún (CUN)", fechas: datos.fechas || "por confirmar" } : null,
      plan: it.dias.map((d) => d.momentos.map((m) => ({ momento: m.momento, lugares: m.ids.map((id) => cat.ids.get(id).n) }))), fuente: it.fuente,
      ...(c.canal ? { canal: c.canal } : {}) }).slice(0, 8000);
    const precio = q ? JSON.stringify({ costo_conocido: q.costo, margen_sugerido: q.margen, precio_sugerido: q.precio, completo: q.completo,
      conceptos: q.conceptos.map((x) => [x.concepto, x.detalle, x.monto]),
      falta_cotizar: [...(p.vuelo ? ["Vuelo internacional a Cancún"] : []), ...q.faltan.map((x) => x.concepto)] }).slice(0, 2000) : undefined;
    const doc = { folio: c.folio, nombre: datos.nombre, medio: datos.medio, personas: datos.personas, itinerario,
      idioma: (c.idioma || "es").slice(0, 5), uid: c.uid, creado: c.creado, consentimiento: true, estado: "nueva" };
    if (datos.correo) doc.correo = datos.correo.slice(0, 120);
    if (datos.telefono) doc.telefono = datos.telefono.slice(0, 25);
    if (datos.fechas) doc.fechas = datos.fechas.slice(0, 80);
    if (datos.comentario) doc.comentario = datos.comentario.slice(0, 600);
    if (precio) doc.precio = precio;
    return doc;
  }

  const api = { MESES, MOMENTO_TXT, INTERES, NIVEL_TEXTO, MODELOS_IA, INSTRUCCION_IA, mesLargo, lugaresSur, catalogoViaje,
    interesesDelTexto, porqueDelMes, armarPorReglas, modeloIA, validarIA, nuevoFolio, documentoSolicitud };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else raiz.Viaje = api;
})(typeof window !== "undefined" ? window : this);
