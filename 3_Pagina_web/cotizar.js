/*
  Autor: Brandon Uriel García Sánchez
  Módulo: Campaña (precio estimado del viaje)
  Qué hace:          Calcula el precio estimado de un itinerario de "Cotiza tu viaje": costo = tarifas oficiales (entradas
                     del INAH) + tarifario del equipo (hospedaje, comida, transporte, guía, tren); precio = costo × (1 +
                     margen), con el margen según qué tan lleno está el mes (5 % a 30 %).
  Por qué así:       Decisión 28 (19-oct-2026). El precio lo calcula este código y NUNCA la IA: un modelo de lenguaje inventa
                     cifras y se equivoca con la aritmética, y cada peso tiene que poder rastrearse (reglas de oro 1 y 2).
                     Si un concepto no tiene tarifa, no se rellena: queda en "faltan" y la página dice "se cotiza al
                     contactarte". Es una función pura (sin página ni red) para probarla con Node (tests/test_viaje.py).
  Datos de entrada:  D.tarifas (backend/torre/campana/tarifas.py ← docs/tarifas/).
  Alimenta a:        Campaña: el precio del servicio que vende el equipo.
*/
(function (raiz) {
  "use strict";
  const redondo = (x) => Math.round(x);

  // Cuántas veces se cobra una tarifa según su unidad (hospedaje: cuartos dobles por noche).
  function veces(unidad, v) {
    if (unidad === "noche") return v.noches * v.cuartos;
    if (unidad === "persona_dia") return v.personas * v.dias;
    if (unidad === "grupo_dia") return v.dias;
    if (unidad === "persona") return v.personas;
    return null;
  }

  /**
   * @param {object} pedido  { zonas: [nombre INAH…], dias, personas, nivel ("tranquila"|"normal"|"alta"|"sin dato"),
   *                           hospedaje ("sencillo"|"medio"|"alto"), desdeCancun (bool), nacional (bool) }
   * @param {object} tarifas D.tarifas: { oficiales, equipo, margen: { niveles, minimo, maximo } }
   */
  function cotizar(pedido, tarifas) {
    const dias = Math.max(1, Math.min(10, Math.round(pedido.dias || 1)));
    const personas = Math.max(1, Math.min(20, Math.round(pedido.personas || 1)));
    const v = { dias, personas, noches: dias - 1, cuartos: Math.ceil(personas / 2) };
    const conceptos = [], faltan = [];

    // 1. Entradas del INAH (oficial). La tarifa para nacionales solo si la ficha la publica.
    for (const zona of pedido.zonas || []) {
      const t = (tarifas.oficiales || []).find((x) => x.concepto === "entrada_inah" && x.zona === zona);
      if (!t) { faltan.push({ concepto: "entrada", detalle: zona }); continue; }
      const unitario = pedido.nacional && t.nacional !== null && t.nacional !== undefined ? t.nacional : t.general;
      conceptos.push({ concepto: "entrada", detalle: zona, unitario, veces: personas, monto: unitario * personas,
        fuente: `${t.fuente}, consultada el ${t.consultado}` });
    }

    // 2. Lo que cotiza el equipo. Hospedaje solo si hay noches; tren solo si viene de Cancún.
    const equipo = tarifas.equipo || [];
    const pedir = [];
    if (v.noches > 0) pedir.push(["hospedaje", pedido.hospedaje || "medio"]);
    pedir.push(["comida", "general"], ["transporte_local", "general"]);
    if (pedido.desdeCancun) pedir.push(["tren_maya", "general"]);
    for (const [concepto, categoria] of pedir) {
      const t = equipo.find((x) => x.concepto === concepto && x.categoria === categoria);
      const n = t ? veces(t.unidad, v) : null;
      if (!t || n === null) { faltan.push({ concepto, detalle: categoria }); continue; }
      conceptos.push({ concepto, detalle: categoria, unitario: t.monto, veces: n, monto: t.monto * n,
        fuente: `Tarifario del equipo (${t.cotizo}, ${t.fecha})` });
    }

    // 3. Margen según el nivel del mes, siempre dentro del rango del equipo (5 % a 30 %).
    const m = tarifas.margen || { niveles: {}, minimo: 0.05, maximo: 0.3 };
    const bruto = m.niveles[pedido.nivel] ?? m.niveles["sin dato"] ?? m.minimo;
    const margen = Math.min(m.maximo, Math.max(m.minimo, bruto));

    const costo = conceptos.reduce((a, c) => a + c.monto, 0);
    const precio = redondo(costo * (1 + margen));
    return {
      conceptos: conceptos.map((c) => ({ ...c, monto: redondo(c.monto) })),
      faltan,
      completo: faltan.length === 0,
      costo: redondo(costo),
      margen,
      ganancia: precio - redondo(costo),
      // Si falta algo, el total es solo de lo conocido: la página lo dice ("desde") y no lo presenta como precio final.
      precio,
      porPersona: redondo(precio / personas),
      personas, dias, noches: v.noches,
    };
  }

  const api = { cotizar };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else raiz.Cotizar = api;
})(typeof window !== "undefined" ? window : this);
