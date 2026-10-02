/*
  Autor: Brandon Uriel García Sánchez
  Módulo: Campaña (página web)
  Qué hace:          Da vida a la página "Sur mexicano": portada con paralaje, el dato con su pictograma de cuartos,
                     los cinco lugares (el mapa 3D vuela a cada lugar mientras se hace scroll), la gráfica del norte
                     (referencia), la línea de tiempo del proyecto y las cifras de evidencia.
  Por qué así:       - Público no técnico: pocas palabras, cifras en lenguaje de todos los días, cada dato con fuente.
                     - 3D con perspectiva CSS + SVG, sin librerías y sin internet. Alternativa descartada: three.js.
                     - Pretext (skill design-html) equilibra los títulos de varias líneas.
                     - CASCARÓN de fases futuras: cada módulo (radar, pronostico, escenarios, presupuesto, envivo,
                       campana) tiene su espacio oculto en index.html (data-clave). Si datos/pagina.js trae su clave, se
                       dibuja y aparece; si no, solo se nombra en "Lo que viene". Nunca se muestra un número inventado.
                     - Todo movimiento respeta "reducir movimiento" del sistema.
  Datos de entrada:  window.TORRE_DATOS (frontend/datos/pagina.js ← backend/torre/api/datos_pagina.py ← Silver/Gold).
  Alimenta a:        La campaña: lo que ve el público.
*/

const D = window.TORRE_DATOS;
const SVG = "http://www.w3.org/2000/svg";
const QUIETO = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const num = (n) => Number(n).toLocaleString("es-MX");
const MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
const fechaLarga = (iso) => { const [a, m, d] = iso.split("-").map(Number); return `${d} de ${MESES[m - 1]} de ${a}`; };
const suave = (t) => 1 - Math.pow(1 - t, 3);
const $ = (id) => document.getElementById(id);

function el(tipo, atributos = {}, padre = null) {
  const nodo = document.createElementNS(SVG, tipo);
  for (const [k, v] of Object.entries(atributos)) nodo.setAttribute(k, v);
  if (padre) padre.appendChild(nodo);
  return nodo;
}
const credito = (f) => `${f.muestra}. Foto: <span data-no-traducir>${f.autor}</span>, <a href="${f.url_licencia}" rel="license" data-no-traducir>${f.licencia}</a>, vía Wikimedia Commons.`;

// ---------- Animaciones comunes ----------
function contar(nodo) {  // la cifra sube hasta su valor real y termina exactamente en él
  const final = Number(nodo.dataset.contar);
  if (QUIETO || !Number.isFinite(final) || nodo.dataset.contado) return;
  nodo.dataset.contado = "1";
  const dec = Number(nodo.dataset.decimales || 0);  // p. ej. 1.4 %: sin esto la cifra terminaría redondeada a 1
  const inicio = performance.now(), dur = 1300;
  const paso = (t) => {
    const k = Math.min(1, (t - inicio) / dur);
    const v = final * suave(k);
    nodo.textContent = dec ? v.toLocaleString("es-MX", { minimumFractionDigits: dec, maximumFractionDigits: dec }) : num(Math.round(v));
    if (k < 1) requestAnimationFrame(paso);
  };
  requestAnimationFrame(paso);
}

function alAparecer(nodos, alVer, umbral = 0.18) {
  const obs = new IntersectionObserver((entradas) => entradas.forEach((e) => {
    if (!e.isIntersecting) return;
    alVer(e.target);
    obs.unobserve(e.target);
  }), { threshold: umbral });
  nodos.forEach((n) => obs.observe(n));
}

async function equilibrarTitulos() {  // Pretext: el ancho más angosto con el mismo número de líneas
  const P = window.Pretext;
  if (!P) return;
  await document.fonts.ready;
  const titulos = [...document.querySelectorAll(".equilibrar")];
  const acomodar = () => titulos.forEach((t) => {
    t.style.maxWidth = "";
    const e = getComputedStyle(t);
    const alto = parseFloat(e.lineHeight) || parseFloat(e.fontSize);
    const ancho = t.clientWidth;
    const texto = t.textContent.trim();
    const fuente = `${e.fontStyle} ${e.fontWeight} ${e.fontSize} ${e.fontFamily}`;
    const h = P.prepare(e.textTransform === "uppercase" ? texto.toUpperCase() : texto, fuente);
    const lineas = P.layout(h, ancho, alto).lineCount;
    if (lineas < 2) return;
    let bajo = ancho / lineas, alto2 = ancho;
    while (alto2 - bajo > 2) {
      const medio = (bajo + alto2) / 2;
      if (P.layout(h, medio, alto).lineCount <= lineas) alto2 = medio; else bajo = medio;
    }
    t.style.maxWidth = `${Math.ceil(alto2) + 6}px`;
  });
  acomodar();
  let espera;
  new ResizeObserver(() => { clearTimeout(espera); espera = setTimeout(acomodar, 150); }).observe(document.body);
}

// ---------- Barra ----------
// Día / noche (decisión 16). El cambio se abre como un círculo desde el botón (View Transitions); sin esa función del
// navegador, o con movimiento reducido, cambia directo. La elección se recuerda en este navegador.
function tema() {
  const boton = $("tema"), raiz = document.documentElement;
  const pintar = () => {
    const noche = raiz.dataset.tema === "noche";
    boton.setAttribute("aria-pressed", noche);
    boton.setAttribute("aria-label", noche ? "Modo día" : "Modo noche");
  };
  pintar();
  boton.addEventListener("click", () => {
    const cambiar = () => {
      raiz.dataset.tema = raiz.dataset.tema === "noche" ? "dia" : "noche";
      try { localStorage.setItem("tema", raiz.dataset.tema); } catch (e) { /* sin almacenamiento: solo esta visita */ }
      pintar();
    };
    if (QUIETO || !document.startViewTransition) { cambiar(); return; }
    const r = boton.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2;
    const radio = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    document.startViewTransition(cambiar).ready.then(() => raiz.animate(
      { clipPath: [`circle(0px at ${x}px ${y}px)`, `circle(${radio}px at ${x}px ${y}px)`] },
      { duration: 650, easing: "cubic-bezier(.2,.7,.2,1)", pseudoElement: "::view-transition-new(root)" }));
  });
}

function barra() {
  const b = $("barra"), menu = $("menu"), enlaces = $("enlaces");
  const revisar = () => b.classList.toggle("solida", window.scrollY > window.innerHeight * 0.8);
  revisar();
  window.addEventListener("scroll", revisar, { passive: true });
  menu.addEventListener("click", () => {
    const abierta = enlaces.classList.toggle("abierta");
    menu.setAttribute("aria-expanded", abierta);
  });
  enlaces.addEventListener("click", (e) => { if (e.target.closest("a")) { enlaces.classList.remove("abierta"); menu.setAttribute("aria-expanded", false); } });
  const as = [...enlaces.querySelectorAll("a")];
  const obs = new IntersectionObserver((es) => es.forEach((e) => {
    if (e.isIntersecting) as.forEach((a) => a.setAttribute("aria-current", a.getAttribute("href") === `#${e.target.id}`));
  }), { rootMargin: "-45% 0px -50% 0px" });
  ["inicio", "que-hacer", "vive", "lugares", "preguntas", "datos"].forEach((id) => $(id) && obs.observe($(id)));
}

// ---------- Anuncio del Radar (arriba de todo). Solo si pagina.js trae "radar"; el texto sale de sus datos. ----------
function anuncio() {
  const R = D.radar, a = $("anuncio"), P = D.pronostico;
  // Con el planeador: este mes, qué lugar está en temporada alta y cuál del sur tiene espacio (decisión 17).
  if (P) {
    const ym = P.meses[0], llenos = P.lugares.filter((l) => l.calendario[0].nivel === "alta").map((l) => l.nombre);
    const libre = P.lugares.find((l) => l.papel !== "referencia" && l.calendario[0].nivel === "tranquila");
    // Cada pedazo es un bloque aparte (data-bloque) para que se traduzca solo, sin importar cuántos lugares estén llenos.
    a.innerHTML = `<span class="anuncio-punto" aria-hidden="true"></span><b data-bloque>${esc(mesDe(ym).largo)}:</b> `
      + (llenos.length ? llenos.map((n) => `<span data-bloque>${esc(n)}, temporada alta</span>`).join(" ")
        : `<span data-bloque>sin temporada alta en los cinco lugares</span>`)
      + (libre ? `<span class="anuncio-extra" data-bloque> · ${esc(libre.nombre)}, tranquilo</span>` : "")
      + `<span class="anuncio-ir" data-bloque> · Planea tu viaje →</span>`;
    a.href = "#inicio";
    a.hidden = false;
    return;
  }
  if (!R) return;
  const n = R.lugares.length, tranquilos = R.lugares.filter((l) => l.estado === "tranquilo").length;
  const sinDato = R.lugares.filter((l) => l.indice === null).map((l) => l.nombre);
  a.innerHTML = `<span class="anuncio-punto" aria-hidden="true"></span><b>Radar, ${R.mes}:</b> ${tranquilos} de los ${n} lugares del sur, tranquilos${sinDato.length ? `<span class="anuncio-extra"> · ${sinDato.join(", ")}, sin dato oficial</span>` : ""}<span class="anuncio-ir"> · Ver el Radar →</span>`;
  a.hidden = false;
}

// ---------- El problema en una imagen: qué parte del estado está en los 5 lugares ----------
function problema() {
  const C = D.concentracion;
  if (!C) { $("problema").hidden = true; return; }
  const p = C.poblacion_pct, redondo = (v) => (v >= 10 ? Math.round(v) : v.toLocaleString("es-MX"));
  const menor = C.dimensiones.reduce((a, b) => (b.pct < a.pct ? b : a));
  $("t-problema").innerHTML = `Aquí vive el <em>${redondo(p)} %</em>. Llega el <em>${redondo(menor.pct)} %</em>.`;
  $("problema-bajada").textContent = `En los cinco lugares vive el ${p.toLocaleString("es-MX")} % de la gente de Quintana Roo, pero llega solo el ${menor.pct.toLocaleString("es-MX")} % ${menor.texto}. Cada barra es la parte del turismo del estado que tienen; la raya, su parte de la gente.`;
  const tope = Math.max(p, ...C.dimensiones.map((d) => d.pct)) * 1.15;
  $("problema-barras").innerHTML = C.dimensiones.map((d, i) => `
    <li class="problema-fila revela" style="--i:${i}">
      <p><b data-contar="${d.pct}" data-decimales="1">${d.pct.toLocaleString("es-MX")}</b><b> %</b> <span>${d.texto}</span> <small>(${d.periodo})</small></p>
      <div class="problema-pista" aria-hidden="true">
        <span class="problema-relleno${d.pct >= p ? " arriba" : ""}" style="--w:${(d.pct / tope * 100).toFixed(1)}%"></span>
        <span class="problema-gente" style="--x:${(p / tope * 100).toFixed(1)}%"></span>
      </div>
    </li>`).join("");
  $("problema-nota").textContent = `La raya marca el ${p.toLocaleString("es-MX")} %: la parte de la gente del estado que vive en los cinco lugares (Censo 2020). Los negocios siguen a la gente; los visitantes, no. Fuente: ${C.fuente}.`;
}

// ---------- Portada ----------
function portada() {
  const f = D.pronostico ? null : D.portada, foto = $("portada-foto");
  if (f) {
    foto.style.backgroundImage = `url("${f.archivo_local}")`;
    $("credito-portada").innerHTML = credito(f);
  }
  const listo = () => requestAnimationFrame(() => document.body.classList.add("cargada"));
  const primera = D.pronostico ? D.pronostico.lugares[plan.lugar].fotos?.[0]?.archivo : f?.archivo_local;
  if (primera && !QUIETO) { const img = new Image(); img.onload = listo; img.onerror = listo; img.src = primera; } else listo();
  if (!QUIETO) {  // paralaje suave de la foto mientras se sale de la portada
    let pendiente = false;
    window.addEventListener("scroll", () => {
      if (pendiente) return;
      pendiente = true;
      requestAnimationFrame(() => {
        const y = Math.min(window.scrollY, window.innerHeight);
        foto.style.translate = `0 ${y * 0.28}px`; $("portada-foto-b").style.translate = `0 ${y * 0.28}px`;
        pendiente = false;
      });
    }, { passive: true });
  }
}

// ---------- El dato ----------
function elDato() {
  const c = D.cuartos_vacios_chetumal;
  $("dato-numero").textContent = c.vacios_de_cada_10;
  $("dato-texto").textContent = `cuartos de hotel en Chetumal se quedaron vacíos en ${c.anio}.`;
  $("dato-fuente").textContent = `${num(c.noches_ocupadas)} de ${num(c.noches_disponibles)} noches ocupadas · Fuente: gobierno de Quintana Roo`;
  const ocupados = 10 - c.vacios_de_cada_10;
  $("cuartos").innerHTML = Array.from({ length: 10 }, (_, i) => `<span class="cuarto${i >= ocupados ? " vacio" : ""}" style="--i:${i}"></span>`).join("");
  alAparecer([$("cuartos")], (n) => n.classList.add("visible"), 0.4);
}

// ---------- Cinco lugares: mapa 3D + capítulos ----------
// Municipios de los lugares del viajero: Othón P. Blanco (sur) y, como referencia, Benito Juárez y Solidaridad (decisión 17)
const MUNICIPIOS_LUGARES = new Set(["004", "005", "008"]);
const LUGARES = () => D.lugares_viajero || D.regiones;
const VISTA_GENERAL = { rx: 50, rz: -12, s: 1, tx: 0, ty: 0 };
const mapa = { estado: { rx: 12, rz: 0, s: 0.9, tx: 0, ty: 0 }, anim: null, girando: false, pines: {}, pos: {} };

function camara() {
  const e = mapa.estado, r = $("mapa3d").style;
  r.setProperty("--rx", `${e.rx}deg`); r.setProperty("--rz", `${e.rz}deg`); r.setProperty("--s", e.s);
  r.setProperty("--tx", `${e.tx}px`); r.setProperty("--ty", `${e.ty}px`);
}

function volar(destino, dur = 1100) {
  cancelAnimationFrame(mapa.anim);
  const desde = { ...mapa.estado }, hasta = { ...desde, ...destino };
  if (QUIETO) { mapa.estado = hasta; camara(); return; }
  const inicio = performance.now();
  const paso = (t) => {
    const k = suave(Math.min(1, (t - inicio) / dur));
    for (const c of Object.keys(hasta)) mapa.estado[c] = desde[c] + (hasta[c] - desde[c]) * k;
    camara();
    if (k < 1) mapa.anim = requestAnimationFrame(paso);
  };
  mapa.anim = requestAnimationFrame(paso);
}

function construirMapa() {
  const svg = $("mapa");
  const lats = LUGARES().map((r) => r.lat), lons = LUGARES().map((r) => r.lon);
  const [s, n, o, e] = [Math.min(...lats) - 0.3, Math.max(...lats) + 0.28, Math.min(...lons) - 0.35, Math.max(...lons) + 0.4];
  const k = Math.cos(((s + n) / 2) * Math.PI / 180);
  const H = 640, esc = H / (n - s), W = (e - o) * k * esc;
  const x = (lon) => (lon - o) * k * esc, y = (lat) => (n - lat) * esc;
  svg.setAttribute("viewBox", `0 0 ${W.toFixed(0)} ${H}`);
  mapa.W = W; mapa.H = H;

  const defs = el("defs", {}, svg);
  el("rect", { x: 0, y: 0, width: W, height: H, rx: 28 }, el("clipPath", { id: "recorte-placa" }, defs));
  const silueta = el("g", { id: "silueta" }, defs);
  const trazos = D.mapa.municipios.map((m) => ({ m, d: m.anillos.map((a) => "M" + a.map(([lo, la]) => `${x(lo).toFixed(1)},${y(la).toFixed(1)}`).join("L") + "Z").join("") }));
  trazos.forEach(({ d }) => el("path", { d, fill: "currentColor" }, silueta));

  // Placa (mar) con grosor y tierra en relieve: copias desplazadas que, al inclinarse, se ven como volumen.
  for (let i = 12; i >= 1; i -= 1) el("rect", { x: 0, y: i, width: W, height: H, rx: 28, fill: i > 6 ? "#4DB8AE" : "#6CCAC0" }, svg);
  el("rect", { x: 0, y: 0, width: W, height: H, rx: 28, class: "placa" }, svg);
  const tierra = el("g", { "clip-path": "url(#recorte-placa)" }, svg);
  for (let i = 6; i >= 1; i -= 1) el("use", { href: "#silueta", y: i, style: `color:${i > 3 ? "#D9B98A" : "#EFD6AE"}` }, tierra);
  const globo = $("globo");
  for (const { m, d } of trazos) {
    const p = el("path", { d, class: MUNICIPIOS_LUGARES.has(m.cve_mun) ? "tierra con-lugar" : "tierra" }, tierra);
    p.addEventListener("pointerenter", () => { globo.textContent = m.nombre; globo.hidden = false; });
    p.addEventListener("pointerleave", () => { globo.hidden = true; });
  }
  $("mapa3d").addEventListener("pointermove", (ev) => {
    const r = ev.currentTarget.getBoundingClientRect();
    globo.style.transform = `translate(${ev.clientX - r.left + 14}px, ${ev.clientY - r.top + 14}px)`;
  });

  const capa = $("pines");
  LUGARES().forEach((r, i) => {
    const px = x(r.lon), py = y(r.lat);
    mapa.pos[r.numero] = { px, py };
    const pin = document.createElement("button");
    pin.type = "button";
    pin.className = "pin";
    pin.style.left = `${(px / W) * 100}%`;
    pin.style.top = `${(py / H) * 100}%`;
    pin.style.setProperty("--i", i);
    pin.setAttribute("aria-label", `${r.numero}. ${r.nombre}: ir a su descripción`);
    pin.innerHTML = `<span class="pin-pie"><span class="pin-nombre">${r.nombre}</span><span class="pin-cabeza"><span>${r.numero}</span></span><span class="pin-sombra"></span></span>`;
    pin.addEventListener("click", () => document.getElementById(`lugar-${r.numero}`).scrollIntoView({ behavior: QUIETO ? "auto" : "smooth", block: "center" }));
    capa.appendChild(pin);
    mapa.pines[r.numero] = pin;
  });
  camara();
  arrastrar();
  $("vista-general").addEventListener("click", () => { detenerGiro(); marcar(null); volar(VISTA_GENERAL); });
  $("girar").addEventListener("click", alternarGiro);
  alAparecer([$("mapa3d")], (m) => { m.classList.add("visto"); volar(VISTA_GENERAL, 1500); }, 0.35);
}

function arrastrar() {
  const zona = $("mapa3d");
  let inicio = null;
  zona.addEventListener("pointerdown", (ev) => {
    if (ev.target.closest(".pin, .boton-icono") || ev.pointerType === "touch") return;  // en pantallas táctiles, el dedo hace scroll
    inicio = { x: ev.clientX, y: ev.clientY, rx: mapa.estado.rx, rz: mapa.estado.rz };
    zona.setPointerCapture(ev.pointerId);
    zona.classList.add("arrastrando");
    cancelAnimationFrame(mapa.anim);
    detenerGiro();
  });
  zona.addEventListener("pointermove", (ev) => {
    if (!inicio) return;
    mapa.estado.rz = inicio.rz + (ev.clientX - inicio.x) * 0.35;
    mapa.estado.rx = Math.max(0, Math.min(66, inicio.rx - (ev.clientY - inicio.y) * 0.25));
    camara();
  });
  const soltar = () => { inicio = null; zona.classList.remove("arrastrando"); };
  zona.addEventListener("pointerup", soltar);
  zona.addEventListener("pointercancel", soltar);
}

function detenerGiro() { mapa.girando = false; $("girar").setAttribute("aria-pressed", "false"); }
function alternarGiro() {
  mapa.girando = !mapa.girando;
  $("girar").setAttribute("aria-pressed", mapa.girando);
  if (!mapa.girando || QUIETO) return;
  cancelAnimationFrame(mapa.anim);
  let previo = performance.now();
  const girar = (t) => {
    if (!mapa.girando) return;
    mapa.estado.rz += (t - previo) * 0.012;
    previo = t;
    camara();
    requestAnimationFrame(girar);
  };
  requestAnimationFrame(girar);
}

function marcar(numero) {
  Object.entries(mapa.pines).forEach(([n, p]) => p.classList.toggle("activo", Number(n) === numero));
}

function acercarA(numero) {
  const { px, py } = mapa.pos[numero];
  const factor = $("mapa-escena").clientWidth / mapa.W;
  volar({ s: 1.35, tx: (mapa.W / 2 - px) * factor, ty: (mapa.H / 2 - py) * factor, rx: 50, rz: mapa.estado.rz }, 1200);
}

// Las tres cifras de cada lugar, en palabras de todos los días. Si falta un dato oficial, se dice.
function cifrasDe(r) {
  const s = (v, t) => `<div class="stat"><b data-contar="${v}">${num(v)}</b><span>${t}</span></div>`;
  // Norte (referencia): cuartos de hotel, parte de 5 estrellas (categoría oficial, DataTur) y visitantes a sus zonas
  if (r.referencia) return (r.cuartos_de_hotel ? s(r.cuartos_de_hotel.valor, `cuartos de hotel (${r.cuartos_de_hotel.periodo})`) : "")
    + (r.estrellas ? `<div class="stat"><b>${r.estrellas.por_categoria["5"]} %</b><span>de los cuartos son de 5 estrellas (${r.estrellas.anio})</span></div>` : "")
    + (r.visitantes_zonas ? s(r.visitantes_zonas.valor, `visitantes a sus zonas arqueológicas en ${r.visitantes_zonas.periodo}`) : s(r.para_comer.valor, "lugares para comer"));
  const comer = s(r.para_comer.valor, "lugares para comer");
  const dormir = s(r.para_dormir.valor, r.para_dormir.valor === 1 ? "lugar para dormir" : "lugares para dormir");
  if (r.visitantes_zonas) return s(r.visitantes_zonas.valor, `visitantes a sus zonas arqueológicas en ${r.visitantes_zonas.periodo}`) + comer + dormir;
  if (r.llegaron_en_tren) return comer + dormir + s(r.llegaron_en_tren.valor, `llegaron en el Tren Maya en ${r.llegaron_en_tren.periodo}`);
  return comer + dormir + `<div class="stat sin"><b>Sin dato</b><span>no hay estadística oficial de turistas</span></div>`;
}

// Semáforo del Radar dentro de la ficha (solo si pagina.js ya trae "radar"; si no, la ficha queda como antes).
function semaforoDe(r) {
  const l = D.radar && D.radar.lugares.find((x) => x.nombre === r.nombre);
  if (!l) return "";
  const sig = l.estado_siguiente_est ? `<span>· ${D.radar.mes_siguiente} (estimado): ${l.estado_siguiente_est}</span>` : "";
  return `<p class="semaforo"><span>Radar, ${D.radar.mes}:</span>${pildora(l.indice === null ? null : l.estado)}${sig}</p>`;
}

function capitulos() {
  const lista = $("capitulos");
  lista.innerHTML = LUGARES().map((r) => `
    <li class="capitulo" id="lugar-${r.numero}" data-n="${r.numero}">
      <p class="capitulo-num">${String(r.numero).padStart(2, "0")} / ${String(LUGARES().length).padStart(2, "0")}</p>
      <h3>${r.nombre}${r.referencia ? ` <span class="etiqueta-ref">Referencia: la campaña no lo promueve</span>` : ""}</h3>
      ${r.foto ? `<figure class="capitulo-foto"><img src="${r.foto.archivo_local}" alt="${r.foto.muestra}" loading="lazy"><figcaption>${credito(r.foto)}</figcaption></figure>` : ""}
      <p class="capitulo-que">${r.que_es}</p>
      <div class="stats">${cifrasDe(r)}</div>
      ${semaforoDe(r)}
      <p class="cuidado"><svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M10 2.5 1.8 17h16.4L10 2.5Zm0 6v4m0 2.6h.01" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg><span>${r.cuidado}</span></p>
    </li>`).join("");
  // El capítulo que está al centro de la pantalla es el "activo": el mapa vuela hacia él.
  const obs = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    const n = Number(e.target.dataset.n);
    lista.querySelectorAll(".capitulo").forEach((c) => c.classList.toggle("activo", c === e.target));
    e.target.querySelectorAll("[data-contar]").forEach(contar);
    marcar(n);
    detenerGiro();
    acercarA(n);
  }), { rootMargin: "-45% 0px -45% 0px" });
  lista.querySelectorAll(".capitulo").forEach((c) => obs.observe(c));
}

// ---------- Mientras tanto, en el norte (referencia) ----------
function elNorte() {
  const R = D.referencia_norte, semanas = R.semanas, n = semanas.length;
  $("t-norte").innerHTML = `Cancún llega a <em>${Math.round(R.maximo_cancun / 10)} de cada 10</em>.`;
  $("norte-sub").textContent = `Cuartos de hotel ocupados cada semana, de 2022 a la última semana publicada (${R.ultima_semana}). Solo para comparar: la campaña no promueve el norte.`;
  const c = D.cuartos_vacios_chetumal;
  $("comparacion").innerHTML = `Mientras tanto, en Chetumal, <strong>${c.vacios_de_cada_10} de cada 10</strong> cuartos se quedaron vacíos en ${c.anio}.`;

  const svg = $("grafica");
  const [W, H, izq, der, arr, aba] = [1200, 340, 34, 8, 10, 32];
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  const x = (i) => izq + (i / (n - 1)) * (W - izq - der);
  const y = (v) => arr + (1 - v / 100) * (H - arr - aba);
  for (const v of [0, 50, 100]) {
    el("line", { x1: izq, x2: W - der, y1: y(v), y2: y(v), class: "eje" }, svg);
    el("text", { x: 0, y: y(v) + 4, class: "eje-texto" }, svg).textContent = v / 10;
  }
  semanas.forEach((s, i) => {
    if (s.slice(5, 7) === "01" && Number(s.slice(8, 10)) <= 7) el("text", { x: x(i), y: H - 6, "text-anchor": "middle", class: "eje-texto" }, svg).textContent = s.slice(0, 4);
  });
  const recorte = el("rect", { x: 0, y: 0, width: W, height: H }, el("clipPath", { id: "recorte-grafica" }, el("defs", {}, svg)));
  const g = el("g", { "clip-path": "url(#recorte-grafica)" }, svg);
  const trazo = (serie, clase) => {
    let d = "", abierto = false;
    serie.forEach((v, i) => {
      if (v === null) { abierto = false; return; }  // un hueco corta la línea: no se inventa el tramo
      d += `${abierto ? "L" : "M"}${x(i).toFixed(1)},${y(v).toFixed(1)}`; abierto = true;
    });
    el("path", { d, class: `linea ${clase}` }, g);
  };
  trazo(R.centros["Riviera Maya"], "l-riviera");
  trazo(R.centros["Cancún"], "l-cancun");
  const cabezal = el("line", { y1: arr, y2: H - aba, class: "cabezal" }, svg);
  const punto = el("circle", { r: 7, class: "punto" }, svg);
  const cifra = $("lectura-cifra");
  function mostrar(i) {
    recorte.setAttribute("width", x(i) + 2);
    cabezal.setAttribute("x1", x(i)); cabezal.setAttribute("x2", x(i));
    const v = R.centros["Cancún"][i];
    if (v !== null) { punto.setAttribute("cx", x(i)); punto.setAttribute("cy", y(v)); cifra.textContent = Math.round(v / 10); }
    $("lectura-semana").textContent = `Semana del ${fechaLarga(semanas[i])}`;
  }
  let reloj = null, i = n - 1;
  const boton = $("reproducir");
  const parar = () => { clearInterval(reloj); reloj = null; boton.textContent = "Reproducir"; };
  const reproducir = () => {
    if (i >= n - 1) i = 0;
    boton.textContent = "Pausa";
    reloj = setInterval(() => { mostrar(i); i += 1; if (i >= n) { i = n - 1; parar(); } }, 70);
  };
  boton.addEventListener("click", () => (reloj ? parar() : reproducir()));
  mostrar(n - 1);
  if (!QUIETO) alAparecer([svg], () => { i = 0; reproducir(); }, 0.45);
}

// ---------- Módulos de fases futuras (cascarón) ----------
const MODULOS = [
  { clave: "radar", fase: 4, nombre: "Semáforo semanal de cada lugar" },
  { clave: "pronostico", fase: 5, nombre: "El mejor mes para ir" },
  { clave: "escenarios", fase: 5, nombre: "Escenarios malo, probable y bueno" },
  { clave: "presupuesto", fase: 6, nombre: "Reparto del presupuesto" },
  { clave: "envivo", fase: 7, nombre: "La torre en vivo" },
  { clave: "campana", fase: 8, nombre: "La campaña" },
];
const DIBUJAR = {
  // Cada fase agrega aquí su función cuando sus datos existan, p. ej. pronostico: (caja, datos) => { ... }.
  radar: dibujarRadar,
  pronostico: dibujarPlaneador,
  presupuesto: dibujarPresupuesto,
  envivo: dibujarEnvivo,
};

// ---------- La torre, semana a semana (Fase 7): reproducción de datos históricos reales ----------
const ACCION = { e: ["encendido", "a-encendido"], p: ["pausado", "a-pausado"], a: ["temporada alta", "a-alta"], f: ["fuera del plan", "a-fuera"] };
const MESES_CORTOS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
const fechaCorta = (s) => { const [a, m, d] = s.split("-"); return `${+d} ${MESES_CORTOS[+m - 1]} ${a}`; };

function dibujarEnvivo(caja, V) {
  const n = V.semanas.length;
  const total = Object.values(V.pausas).reduce((a, b) => a + b, 0);
  caja.innerHTML = `
    <p class="rotulo claro revela">La torre</p>
    <h2 class="h2 claro revela equilibrar" id="t-envivo">La campaña, <em>semana</em> a semana.</h2>
    <p class="bajada-clara revela">Reproducción de datos históricos reales: ${n} semanas, del ${fechaCorta(V.desde)} al ${fechaCorta(V.hasta)}. Cada semana la torre revisa el clima, las tormentas, la gente que llegó al sur y qué tan lleno está el norte, y decide qué anuncio se enciende y cuál se pausa.</p>
    <div class="vivo-panel revela">
      <div class="vivo-controles">
        <button class="boton-linea claro" type="button" id="vivo-boton">Reproducir</button>
        <input type="range" id="vivo-rango" min="0" max="${n - 1}" value="${n - 1}" aria-label="Semana">
        <b id="vivo-fecha" aria-live="polite"></b>
      </div>
      <div class="vivo-norte" id="vivo-norte"></div>
      <div class="vivo-lugares" id="vivo-lugares"></div>
      <div class="vivo-lineas" aria-hidden="true">${V.lugares.map((l, j) => `<div class="vivo-linea"><small>${l}</small><div>${V.semanas.map((s, i) => `<i class="${ACCION[s.l[j]][1]}" data-i="${i}"></i>`).join("")}</div></div>`).join("")}<span class="vivo-cursor" id="vivo-cursor"></span></div>
      <p class="vivo-leyenda">${Object.values(ACCION).map(([t, c]) => `<span><i class="${c}"></i>${t}</span>`).join("")}</p>
    </div>
    <div class="dinero-rejilla vivo-cifras">
      <div class="dinero-caja revela"><b>${total}</b><span>veces que se pausó el anuncio de un lugar (contando cada lugar y semana): ${V.pausas_clima} con clima raro, ${V.pausas_tormenta} con tormenta cerca (${V.tormentas.join(", ")}) y ${V.pausas_llegadas} porque llegó más gente de la esperada; algunas tuvieron más de un motivo. El dinero pausado se gastó en la siguiente semana permitida.</span></div>
      <div class="dinero-caja revela"><b>${V.ibas_al_norte}</b><span>semanas con "¿Ibas al norte?" encendido: Cancún o la Riviera Maya pasaron de ${V.corte_saturado} % de ocupación y el sur tenía espacio. El norte nunca se anuncia.</span></div>
    </div>
    <details class="como claro revela"><summary>¿Cómo lo sabemos?</summary><div class="como-dentro">
      <p>Las semanas se procesan como si llegaran una por una, con Spark Structured Streaming: ${V.lotes} lotes, uno por semana y en orden. Así funcionaría con datos que llegan cada semana. El dinero de cada semana es el del plan de la Fase 6, aplicado por mes del año; de julio a septiembre no hay plan porque el pronóstico no llega ahí.</p>
      <p>"Clima raro" lo decide un modelo (Isolation Forest) que aprende de todas las semanas anteriores: una semana es rara si es más rara que 19 de cada 20 que ya conocía. Las tormentas de 2026 todavía no se publican; esas semanas dicen "sin dato de tormentas" y no se pausan por eso. Las llegadas del sur se comparan con el rango esperado del pronóstico del mes anterior.</p>
      <p>Fuente: ${V.fuente}.</p></div></details>`;
  const rango = $("vivo-rango"), boton = $("vivo-boton");
  const mostrar = (i) => {
    const s = V.semanas[i];
    rango.value = i;
    $("vivo-fecha").textContent = `Semana del ${fechaCorta(s.s)}`;
    $("vivo-norte").innerHTML = `<span>Cancún <b>${s.c ?? "—"} %</b></span><span>Riviera Maya <b>${s.r ?? "—"} %</b></span>${s.n
      ? `<span class="vivo-aviso">¿Ibas al norte? Anuncio encendido → ${s.n}</span>`
      : s.ll ? `<span class="vivo-aviso apagado">${s.ll} lleno, pero ningún lugar del sur tiene anuncio esta semana</span>` : ""}`;
    $("vivo-lugares").innerHTML = V.lugares.map((l, j) => {
      const [t, c] = ACCION[s.l[j]];
      return `<div class="vivo-lugar"><small>${l}</small><span class="vivo-estado ${c}">${t}</span>${s.m[j] ? `<p>${s.m[j]}</p>` : ""}</div>`;
    }).join("") + (s.t ? `<p class="vivo-nota">Sin dato de tormentas: el registro de 2026 aún no se publica.</p>` : "");
    $("vivo-cursor").style.left = `calc(var(--etiqueta) + (100% - var(--etiqueta)) * ${(i + 0.5) / n})`;
  };
  let reloj = null;
  const parar = () => { clearInterval(reloj); reloj = null; boton.textContent = "Reproducir"; };
  boton.addEventListener("click", () => {
    if (reloj) return parar();
    let i = +rango.value >= n - 1 ? 0 : +rango.value;
    boton.textContent = "Pausa";
    reloj = setInterval(() => { mostrar(i); i += 1; if (i >= n) parar(); }, QUIETO ? 0 : 140);
  });
  rango.addEventListener("input", () => { parar(); mostrar(+rango.value); });
  caja.querySelector(".vivo-lineas").addEventListener("click", (e) => { if (e.target.dataset.i) { parar(); mostrar(+e.target.dataset.i); } });
  // Arranca en la semana más reciente con algún anuncio encendido (julio a septiembre no tienen plan).
  const ultima = V.semanas.map((s, i) => (s.l.includes("e") ? i : -1)).filter((i) => i >= 0).pop() ?? n - 1;
  mostrar(ultima);
}

// ---------- El presupuesto (Fase 6): cuánto dinero, dónde y cuándo ----------
const COLOR_LUGAR = { "Ruta arqueológica del sur": "p-ruta", "Bahía Calderitas–Oxtankah": "p-bahia", Chetumal: "p-chetumal" };
const pesos = (n) => `$${Math.round(n).toLocaleString("es-MX")}`;

function dibujarPresupuesto(caja, P) {
  const tope = Math.max(...P.meses.map((m) => Object.values(m.pesos).reduce((a, b) => a + b, 0)));
  const fb = P.canales.find((c) => c.nombre === "Facebook"), go = P.canales.find((c) => c.nombre === "Google");
  const costo = P.reglas.filter((r) => Math.abs(r.costo_pct) >= 0.05);
  const gratis = P.reglas.filter((r) => Math.abs(r.costo_pct) < 0.05).map((r) => r.regla.toLowerCase());
  caja.innerHTML = `
    <p class="rotulo revela">El presupuesto</p>
    <h2 class="h2 revela equilibrar" id="t-presupuesto">¿Cuánto dinero, <em>dónde</em> y cuándo?</h2>
    <p class="radar-bajada revela">Con ${pesos(P.presupuesto_anual)} al año (un supuesto: no hay presupuesto real todavía), la campaña traería unos <b>${P.visitantes.toLocaleString("es-MX")} visitantes</b> más al sur de ${P.desde} a ${P.hasta}: ${pesos(P.pesos_por_visitante)} por cada uno. Nunca se anuncia un lugar en su temporada alta ni se rebasa su capacidad.</p>
    <div class="pres-cifras">
      <div class="revela"><b>${P.visitantes.toLocaleString("es-MX")}</b><span>visitantes esperados con ${pesos(P.presupuesto_periodo)} en ${P.n_meses} meses</span></div>
      <div class="revela"><b>${fb.pct} / ${go.pct}</b><span>% en Facebook / Google: Facebook trae ${fb.por_mil} por cada $1,000 y Google ${go.por_mil}</span></div>
      <div class="revela"><b>${P.sin_perder_pct} %</b><span>ningún mes con anuncio pasa de esta parte de su capacidad, sin perder un solo visitante</span></div>
    </div>
    <figure class="pres-grafica revela">
      <div class="pres-meses" role="img" aria-label="Pesos por mes y lugar">${P.meses.map((m) => {
        const total = Object.values(m.pesos).reduce((a, b) => a + b, 0);
        const barras = P.orden.map((l) => m.pesos[l] ? `<i class="${COLOR_LUGAR[l]}" style="--h:${(m.pesos[l] / tope) * 100}%" title="${l}: ${pesos(m.pesos[l])}"></i>` : "").join("");
        return `<div class="pres-mes"><small>${total ? pesos(total) : "Temporada alta"}</small><div class="pres-pila">${barras}</div><span>${m.mes}</span></div>`;
      }).join("")}</div>
      <figcaption class="pres-leyenda">${P.lugares.map((l) => `<span><i class="${COLOR_LUGAR[l.nombre]}"></i>${l.nombre}: ${pesos(l.pesos)} (${l.pct} %)</span>`).join("")}</figcaption>
    </figure>
    <p class="pres-regla revela">¿Cuánto cuestan las reglas? ${gratis.length ? `<b>Nada</b> a este presupuesto: ${gratis.join(", ")}. La campaña es chica frente al espacio que hay. ` : ""}${costo.map((r) => `Sin el ${r.regla.toLowerCase()} llegarían ${r.costo_pct} % más visitantes, pero todo dependería de una sola plataforma.`).join(" ")}</p>
    <details class="como revela"><summary>¿Cómo lo sabemos?</summary><div class="como-dentro">
      <p>Un modelo de optimización reparte los pesos entre meses, los tres lugares del sur y dos canales para traer el máximo de visitantes. Cada canal convierte según su costo por clic y su tasa de conversión de la categoría de viajes (promedios de anunciantes de Estados Unidos, usados como supuesto). Facebook no publica su conversión para turismo: con 3 % llegarían ${P.facebook_3.toLocaleString("es-MX")} visitantes y con la mediana de todas las industrias, ${P.facebook_mediana.toLocaleString("es-MX")}.</p>
      <p>Las reglas: cero anuncio en temporada alta; los visitantes esperados más los de la campaña no pasan del mes más alto que cada lugar ya recibió; cada lugar recibe al menos 15 % del dinero; ningún canal más de 70 %. El modelo revisa además los escenarios malo, probable y bueno del pronóstico y deja fuera los meses donde, si el año sale bueno, el lugar se llenaría. Como todos los lugares convierten igual, el dinero se reparte en proporción al espacio libre de cada mes.</p>
      <p>Fuente: ${P.fuente}.</p></div></details>`;
  alAparecer([caja.querySelector(".pres-grafica")], (g) => g.classList.add("visible"), 0.3);
}

// ---------- El Radar (Fase 4) ----------
// Estado en palabras + color (nunca solo color). "Sin dato oficial" es un estado aparte: no saber ≠ tranquilo.
const CLASE_ESTADO = { tranquilo: "e-tranquilo", concurrido: "e-concurrido", saturado: "e-saturado" };
const pildora = (estado) => `<span class="estado ${CLASE_ESTADO[estado] || "e-sin"}">${estado ? estado[0].toUpperCase() + estado.slice(1) : "Sin dato oficial"}</span>`;
const pct = (p) => `${Math.round(p * 100)} %`;

function filaRadar(l, R) {
  const c1 = R.cortes.concurrido_desde, c2 = R.cortes.saturado_desde;
  const pista = l.indice === null
    ? `<div class="radar-pista sin" aria-hidden="true"></div>`
    : `<div class="radar-pista" aria-hidden="true"><i class="z-tranquilo" style="width:${c1 * 100}%"></i><i class="z-concurrido" style="width:${(c2 - c1) * 100}%"></i><i class="z-saturado" style="flex:1"></i><span class="radar-marca" data-x="${(l.indice * 100).toFixed(1)}"></span></div>`;
  const medidas = l.medidas ? `Medido con: ${l.medidas.join(", ")}` : "No hay estadística oficial de turistas para este lugar";
  const siguiente = l.estado_siguiente_est
    ? `<small>${R.mes_siguiente} (estimado): ${l.estado_siguiente_est}, ${pct(l.probabilidad_siguiente)}</small>` : "";
  return `<li class="radar-fila revela"><div><h3>${l.nombre}</h3><small>${medidas}</small></div>${pista}
    <div class="radar-derecha">${pildora(l.indice === null ? null : l.estado)}${siguiente}</div></li>`;
}

function dibujarRadar(caja, R) {
  const tranquilos = R.lugares.filter((l) => l.estado === "tranquilo").length;
  const n = R.norte_semanal;
  caja.innerHTML = `
    <p class="rotulo revela">El Radar</p>
    <h2 class="h2 revela equilibrar" id="t-radar">¿Dónde hay <em>espacio</em> hoy?</h2>
    <p class="radar-bajada revela">En ${R.mes}, ${tranquilos} de los cinco lugares están tranquilos. La raya negra es el lugar en una escala de 0 (lo más bajo registrado en todo el estado) a 1 (lo más alto).</p>
    <ul class="radar-lista">${R.lugares.map((l) => filaRadar(l, R)).join("")}</ul>
    <p class="rotulo radar-ref-titulo revela">Solo como referencia · la campaña no los promueve</p>
    <ul class="radar-lista ref">${R.referencia.map((l) => filaRadar(l, R)).join("")}</ul>
    <div class="radar-norte revela" id="radar-norte">
      <div><h3>¿Se va a llenar Cancún?</h3>
        <p>Semana del ${n.semana}: ${n.ocupacion_hoy_pct["Cancún"]} % de cuartos ocupados, una semana ${n.estado_hoy["Cancún"].replace(/o$/, "a")} para los hoteles del norte (esta medida es solo de hoteles y semanal; la lista de arriba es mensual y suma más medidas). Probabilidad de que se sature en cada una de las próximas 8 semanas (estimada; cada barra llega hasta 25 %). Cuando sube, es el momento de mostrarle el sur a quien planea ir al norte.</p></div>
      <div class="riesgo" role="img" aria-label="Probabilidad de saturación de Cancún semana por semana">${n.riesgo_saturarse["Cancún"].map((p, i) =>
        `<div style="--i:${i}"><b>${pct(p)}</b><span style="--h:${Math.max(Math.round(p * 400), 3)}px"></span>sem ${i + 1}</div>`).join("")}</div>
    </div>
    <details class="como revela"><summary>¿Cómo lo sabemos?</summary><div class="como-dentro">
      <p>Cada mes se mide la gente que llega (Tren Maya, cruceros, zonas arqueológicas) por cada mil habitantes y los cuartos de hotel ocupados. Todo se pasa a la misma escala de 0 a 1 y se promedia; cada medida pesa lo mismo. Si el resultado queda en la mitad baja de todo el estado, el lugar está <b>tranquilo</b>; en el 10 % más alto, <b>saturado</b>; en medio, <b>concurrido</b>.</p>
      <p>El estado del mes siguiente lo estima un modelo (${R.modelo.nombre}). Probado con los últimos 12 meses, que nunca vio, acertó ${R.modelo.aciertos} de ${R.modelo.casos}; repetir el mes anterior acierta ${R.modelo.aciertos_persistencia}. Su valor es que anticipó ${R.modelo.cambios_anticipados} de los ${R.modelo.cambios_reales} cambios de estado.${R.modelo.cambios_en_los_5 !== null && R.modelo.cambios_en_los_5 !== undefined ? ` Ojo: en los cinco lugares de la campaña hubo ${R.modelo.cambios_en_los_5 === 0 ? "ningún cambio" : R.modelo.cambios_en_los_5 === 1 ? "un solo cambio" : `solo ${R.modelo.cambios_en_los_5} cambios`} de estado en esos meses, así que ahí el modelo casi no se ha podido poner a prueba.` : ""}</p>
      <p>La ocupación de Cancún, Playa del Carmen, Cozumel e Isla Mujeres viene de la Secretaría de Turismo (DataTur), que marca menos ocupación que el sistema estatal para los mismos lugares (hasta 19 puntos menos en Isla Mujeres). Por eso el norte puede verse un poco más vacío de lo que está; la conclusión de que el sur tiene espacio no cambia.</p>
      <p>Fuente: ${R.fuente}.</p></div></details>`;
  // La raya se mueve cuando aparece su fila (se observa la fila y no la raya: la raya es muy chica para el umbral).
  alAparecer([...caja.querySelectorAll(".radar-fila")], (fila) => {
    const m = fila.querySelector(".radar-marca");
    if (m) m.style.left = `${m.dataset.x}%`;
  }, 0.4);
  alAparecer([caja.querySelector("#radar-norte")], (nodo) => nodo.classList.add("visible"), 0.35);
}

// ---------- Planea tu viaje (Fase 5): ¿cuándo conviene ir? + qué hacer de día, tarde y noche ----------
// Regla de temporada alta (decisión de Brandon): el mes está 20 % o más arriba de un mes promedio, o tiene 10 % o más
// de riesgo de rebasar el mes más lleno de su historia. Los negocios vienen del DENUE (INEGI): sin reseñas ni horarios.
const esc = (t) => String(t ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const NIVEL = {
  alta: { texto: "Temporada alta", clase: "e-saturado" },
  normal: { texto: "Mes normal", clase: "e-concurrido" },
  tranquila: { texto: "Mes tranquilo", clase: "e-tranquilo" },
  "sin dato": { texto: "Sin dato de afluencia", clase: "e-sin" },
};
const MES_CORTO = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
const mesDe = (ym) => { const [a, m] = ym.split("-").map(Number); return { a, m, largo: `${MESES[m - 1]} de ${a}`, corto: MES_CORTO[m - 1] }; };
const plan = { lugar: 2, mes: 0 };  // empieza en la Ruta de las pirámides, mes en curso
const conArticulo = (nombre) => (/^(Ruta|Laguna)/.test(nombre) ? `la ${nombre}` : nombre);

function dibujarPlaneador(caja, P) {
  // Lo primero de la página: elegir lugar y mes en la portada (pedido de Brandon, 01-oct-2026).
  $("elige").innerHTML = `
    <div class="planea-lugares" role="radiogroup" aria-label="Lugar">${P.lugares.map((l, i) => {
      // Cancún y Riviera Maya son referencia (decisión 15): van aparte, con su rótulo, para quien pensaba ir al norte.
      const rotulo = i === 0 ? `<span class="planea-grupo">El sur</span>`
        : l.papel === "referencia" && P.lugares[i - 1].papel !== "referencia" ? `<span class="planea-grupo">¿Ibas al norte?</span>` : "";
      return `${rotulo}<button type="button" role="radio" class="planea-lugar${l.papel === "referencia" ? " ref-norte" : ""}" data-i="${i}">${esc(l.nombre)}</button>`;
    }).join("")}</div>
    <div class="planea-meses" role="radiogroup" aria-label="Mes">${P.meses.map((ym, i) => {
      const f = mesDe(ym);
      return `<button type="button" role="radio" class="planea-mes" data-i="${i}"><b>${f.corto}</b><small>${f.a}</small><i aria-hidden="true"></i></button>`;
    }).join("")}</div>
    <div class="elige-aviso" id="elige-aviso" role="status" aria-live="polite" hidden></div>
    <p class="planea-leyenda" aria-hidden="true"><span class="p-tranquila"></span>Tranquilo <span class="p-normal"></span>Normal <span class="p-alta"></span>Temporada alta</p>
    <a class="boton boton-claro" href="#planea">Ver cómo va a estar
      <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M8 3v10m0 0-4-4m4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a>`;
  caja.innerHTML = `
    <div class="planea-dentro">
      <p class="rotulo revela">Tu viaje</p>
      <h2 class="h2 revela equilibrar" id="t-planea">Así va a <em>estar</em>.</h2>
      <div class="planea-resultado revela" id="planea-resultado" aria-live="polite"></div>
      <div class="lugar-fotos revela" id="lugar-fotos"></div>
      <details class="como revela"><summary>¿Cómo lo sabemos?</summary><div class="como-dentro">
        <p><b>Temporada alta</b> quiere decir que ese mes llega 20 % o más gente que en un mes promedio del año, o que hay 10 % o más de probabilidad de rebasar el mes más lleno que el lugar ha tenido. Se calcula con los visitantes del INAH a las zonas arqueológicas y, en Chetumal, con los cruces desde Belice.</p>
        <p>Hasta ${esc(mesDe(P.ultimo_pronostico).largo)} hay un pronóstico con su rango: el valor real cayó dentro de ese rango entre 8 y 9 de cada 10 veces cuando se probó con meses que el modelo nunca vio. Después de esa fecha se muestra lo típico de cada mes.</p>
        <p><b>Cancún y Riviera Maya</b> están como referencia, para quien pensaba ir al norte; la campaña no los promueve. Ahí se mide la ocupación de los hoteles: es temporada alta si se espera ${P.regla.corte_norte} % de cuartos ocupados o más, el nivel que el Radar ya cuenta como "concurrido". Si el mes está lleno, te recomendamos un lugar del sur. Tómalo con cuidado en la Riviera Maya: su ocupación bajó (${P.riviera.ahora} % en ${esc(mesDe(P.riviera.mes).largo)}, contra ${P.riviera.antes} % un año antes), el pronóstico supone que sigue así y se equivoca más que solo repetir lo del año anterior; se usa porque es el único cuyo rango sí atrapó el valor real 8 de cada 10 veces.</p>
        <p>El clima es el normal de 1991 a 2020. El riesgo de tormenta cuenta las tormentas que pasaron a 200 km o menos del lugar desde 1966 (31 en el caso de Chetumal).</p>
        <p>Las fotos son de Wikimedia Commons, con licencia libre, y cada una se tomó dentro del municipio del lugar (su coordenada se comprobó con el mapa oficial). Las fotos de comida solo existen con licencia libre para Cancún y Playa del Carmen; las del sur las aportará el equipo.</p>
        <p>Fuente: ${esc(P.fuente)}.</p></div></details>
    </div>`;
  const elige = $("elige");
  elige.querySelectorAll(".planea-lugar").forEach((b) => b.addEventListener("click", () => { plan.lugar = +b.dataset.i; pintarPlan(P); dibujarQueHacer(P); }));
  elige.querySelectorAll(".planea-mes").forEach((b) => b.addEventListener("click", () => { plan.mes = +b.dataset.i; pintarPlan(P); }));
  // Flechas del teclado dentro de cada grupo (patrón de radio de WAI-ARIA)
  [[".planea-lugares", ".planea-lugar"], [".planea-meses", ".planea-mes"]].forEach(([g, b]) => {
    elige.querySelector(g).addEventListener("keydown", (e) => {
      if (!["ArrowRight", "ArrowLeft"].includes(e.key)) return;
      const botones = [...elige.querySelectorAll(b)], i = botones.indexOf(document.activeElement);
      const sig = botones[(i + (e.key === "ArrowRight" ? 1 : -1) + botones.length) % botones.length];
      sig.focus(); sig.click(); e.preventDefault();
    });
  });
  pintarPlan(P);
  dibujarQueHacer(P);
  vigilarAviso();
}

function fotoPortada(L) {
  // La foto de la portada cambia con el lugar (fundido entre dos capas). Crédito siempre visible (licencia).
  const x = L.fotos && L.fotos[0];
  if (!x) return;
  const a = $("portada-foto"), b = $("portada-foto-b");
  const entra = a.classList.contains("oculta") ? a : b, sale = entra === a ? b : a;
  if (entra.dataset.src === x.archivo && !entra.classList.contains("oculta")) return;
  entra.style.backgroundImage = `url("${x.archivo}")`; entra.dataset.src = x.archivo;
  entra.classList.remove("oculta"); sale.classList.add("oculta");
  a.setAttribute("aria-label", `${x.muestra}, ${L.nombre}`);
  $("credito-portada").innerHTML = `${esc(x.muestra)}. Foto: <span data-no-traducir>${esc(x.autor)}</span>, <a href="${esc(x.url_licencia || x.url_original)}" rel="license noopener noreferrer" target="_blank" data-no-traducir>${esc(x.licencia)}</a>, vía Wikimedia Commons.`;
}

function galeriaLugar(L) {
  const caja = $("lugar-fotos");
  if (!caja || !L.fotos) return;
  caja.innerHTML = `<p class="lugar-fotos-titulo">Así se ve ${esc(conArticulo(L.nombre))}</p>
    <ul>${L.fotos.map((x) => `<li><figure><img src="${esc(x.archivo)}" alt="${esc(x.muestra)}" loading="lazy" width="${x.ancho}" height="${x.alto}">
      <figcaption>${esc(x.muestra)}<small>Foto: <span data-no-traducir>${esc(x.autor)}</span>, <a href="${esc(x.url_licencia || x.url_original)}" rel="license noopener noreferrer" target="_blank" data-no-traducir>${esc(x.licencia)}</a></small></figcaption></figure></li>`).join("")}</ul>`;
}

function pintarPlan(P) {
  const L = P.lugares[plan.lugar], c = L.calendario[plan.mes], f = mesDe(P.meses[plan.mes]);
  fotoPortada(L);
  if ($("lugar-fotos") && $("lugar-fotos").dataset.lugar !== String(plan.lugar)) { galeriaLugar(L); $("lugar-fotos").dataset.lugar = plan.lugar; }
  document.querySelectorAll(".planea-lugar").forEach((b, i) => { b.setAttribute("aria-checked", i === plan.lugar); b.tabIndex = i === plan.lugar ? 0 : -1; });
  document.querySelectorAll(".planea-mes").forEach((b, i) => {
    const n = L.calendario[i].nivel;
    b.className = `planea-mes p-${n === "sin dato" ? "sin" : n}`;
    b.setAttribute("aria-checked", i === plan.mes); b.tabIndex = i === plan.mes ? 0 : -1;
    b.setAttribute("aria-label", `${MESES[mesDe(P.meses[i]).m - 1]} de ${mesDe(P.meses[i]).a}: ${NIVEL[n].texto.toLowerCase()}`);
  });
  const nv = NIVEL[c.nivel], norte = L.papel === "referencia";
  const corte = Math.round(P.regla.corte_norte), pron = c.ocupacion !== null;
  let que;
  if (norte) que = c.nivel === "alta"
    ? `Habrá mucha gente: ${pron ? "se espera que los hoteles pasen" : "los hoteles suelen pasar"} del ${corte} % de cuartos ocupados, lo que el Radar ya cuenta como "concurrido".`
    : `Hay espacio: ${pron ? "se espera que los hoteles queden" : "los hoteles suelen quedar"} debajo del ${corte} % de cuartos ocupados, lo que el Radar cuenta como "concurrido".`;
  else if (c.nivel === "sin dato") que = `${esc(L.nombre)} no tiene estadística oficial de visitantes, así que no podemos decir si estará lleno. Esto es lo que sí sabemos de ${esc(f.largo)}:`;
  else if (c.nivel === "alta") que = `Llega ${Math.round((c.indice - 1) * 100)} % más gente que en un mes promedio${c.riesgo >= P.regla.alta_riesgo ? `, y hay ${pct(c.riesgo)} de probabilidad de rebasar el mes más lleno de su historia` : ""}.`;
  else if (c.nivel === "tranquila") que = `Llega ${Math.round((1 - c.indice) * 100)} % menos gente que en un mes promedio: hay espacio.`;
  else que = "Llega más o menos la gente de un mes promedio.";
  const fuera = `Ese mes todavía no está en el pronóstico (llega hasta ${esc(mesDe(P.ultimo_pronostico).largo)})`;
  const cifra = norte
    ? (c.ocupacion !== null
      ? `<p class="planea-cifra">Se espera alrededor de <b>${Math.round(c.ocupacion)} %</b> ${esc(L.medida)}, muy probablemente entre ${Math.round(c.minimo)} y ${Math.round(c.maximo)} %.</p>`
      : `<p class="planea-cifra">${fuera}: en un ${MESES[f.m - 1]} típico, de 2022 a 2025, los hoteles estuvieron al <b>${Math.round(c.tipica)} %</b>.</p>`)
    : c.esperado !== null
      ? `<p class="planea-cifra">Se esperan alrededor de <b>${num(Math.round(c.esperado))}</b> ${esc(L.medida)}, muy probablemente entre ${num(Math.round(c.minimo))} y ${num(Math.round(c.maximo))}.</p>`
      : c.nivel !== "sin dato" ? `<p class="planea-cifra">${fuera}: esto es lo típico de ${MESES[f.m - 1]}.</p>` : "";
  const tormenta = c.tormenta === 0 ? "Sin tormentas registradas en este mes" : `${pct(c.tormenta)} de probabilidad de tormenta`;
  const k = consejoDe(P, L, c, f);
  const consejo = k ? `<div class="planea-consejo"><p class="rotulo claro">${k.rotulo}</p><p>${k.frase}</p><div class="planea-botones">${k.botones}</div></div>` : "";
  $("planea-resultado").innerHTML = `
    <div class="planea-tarjeta">
      <p class="planea-cuando">${esc(L.nombre)} · ${esc(f.largo)}${norte ? ` <span class="etiqueta-ref">Referencia: la campaña no lo promueve</span>` : ""}</p>
      <p class="estado-grande ${nv.clase}">${nv.texto}</p>
      <p class="planea-que">${que}</p>
      ${cifra}
      <ul class="planea-clima">
        <li><b>${num(c.lluvia)} mm</b><span>de lluvia en un ${MESES[f.m - 1]} normal</span></li>
        <li><b>${c.temp} °C</b><span>de máxima, en promedio</span></li>
        <li><b>${c.tormenta === 0 ? "0 %" : pct(c.tormenta)}</b><span>${tormenta.toLowerCase().startsWith("sin") ? "sin tormentas registradas en este mes" : "de probabilidad de tormenta"}</span></li>
      </ul>
    </div>${consejo}`;
  conectarBotones($("planea-resultado"), P);
  avisoLleno(P, L, c, f, k);
}

// Qué recomendar cuando el mes es temporada alta: otro lugar del sur (nunca el norte) y, en el sur, otro mes.
function consejoDe(P, L, c, f) {
  if (c.nivel !== "alta") return null;
  const norte = L.papel === "referencia", mes = MESES[f.m - 1], botones = [];
  if (c.otro_lugar) botones.push(`<button type="button" class="boton boton-claro" data-lugar="${esc(c.otro_lugar_clave)}">${norte ? "Cambiar a" : "Ver"} ${esc(c.otro_lugar)} en ${mes}</button>`);
  if (c.otro_mes) botones.push(`<button type="button" class="boton boton-tinta" data-mes="${c.otro_mes}">Ver ${esc(conArticulo(L.nombre))} en ${MESES[c.otro_mes - 1]}</button>`);
  const otroMes = c.otro_mes ? ` O ve a ${esc(conArticulo(L.nombre))} en <b>${MESES[c.otro_mes - 1]}</b>: menos gente, poca lluvia y fuera de la temporada de tormentas.` : "";
  let frase;
  if (norte) frase = c.otro_lugar
    ? `En ${mes}, <b>${esc(c.otro_lugar)}</b> no está en temporada alta: hay espacio, sin el gentío del norte.`
    : `En ${mes} el sur también tiene temporada alta. Si puedes mover tu viaje, busca los meses en verde.`;
  else frase = c.otro_lugar
    ? `En ${mes}, <b>${esc(c.otro_lugar)}</b> está más tranquilo.${otroMes}`
    : `Los lugares del sur con estadística están en temporada alta este mes.${otroMes.replace(" O ve", " Mejor ve")}`;
  return { rotulo: norte ? "Mejor ve al sur" : "Te conviene más", frase, botones: botones.join(""), corto: c.otro_lugar ? `${esc(c.otro_lugar)} está más tranquilo ese mes.` : "" };
}

function conectarBotones(caja, P) {
  caja.querySelectorAll("[data-lugar]").forEach((b) => b.addEventListener("click", () => {
    plan.lugar = P.lugares.findIndex((l) => l.clave === b.dataset.lugar); pintarPlan(P); dibujarQueHacer(P);
  }));
  caja.querySelectorAll("[data-mes]").forEach((b) => b.addEventListener("click", () => {
    const m = +b.dataset.mes;  // el mes con ese número más cercano al elegido (dic-2026 → nov-2026, no nov-2027)
    const opciones = P.meses.map((ym, k) => k).filter((k) => mesDe(P.meses[k]).m === m);
    plan.mes = opciones.sort((x, y) => Math.abs(x - plan.mes) - Math.abs(y - plan.mes))[0]; pintarPlan(P);
  }));
}

// Aviso fijo abajo de la pantalla (Brandon, 01-oct-2026: "que sí se vea y no pase desapercibido en un scroll"). Sale
// cuando el lugar y mes elegidos son temporada alta, mientras la persona está en la portada, el resultado o "Qué hacer";
// se cierra con la ×, y vuelve a salir si elige otra combinación llena.
const aviso = { cerrado: null, visible: false };
function avisoLleno(P, L, c, f, k) {
  const caja = $("aviso-lleno"), clave = `${plan.lugar}-${plan.mes}`, enPortada = $("elige-aviso");
  if (enPortada) {  // versión corta dentro de la portada, junto a los meses
    enPortada.hidden = !k;
    enPortada.innerHTML = k ? `<p><b>Temporada alta.</b> ${k.corto || (L.papel === "referencia" ? "El sur también está lleno ese mes." : "")}</p>${k.botones}` : "";
    if (k) conectarBotones(enPortada, P);
  }
  if (!caja) return;
  if (!k || aviso.cerrado === clave) { caja.hidden = true; caja.innerHTML = ""; return; }
  caja.innerHTML = `<p><b>${esc(L.nombre)} en ${esc(f.largo)}: temporada alta.</b> ${k.corto || (L.papel === "referencia" ? "El sur también está lleno ese mes." : "")}</p>
    <div class="aviso-botones">${k.botones}<button type="button" class="aviso-cerrar" aria-label="Cerrar aviso">×</button></div>`;
  conectarBotones(caja, P);
  caja.querySelector(".aviso-cerrar").addEventListener("click", () => { aviso.cerrado = clave; caja.hidden = true; });
  caja.hidden = false;
  caja.classList.toggle("fuera", !aviso.visible);
}

function vigilarAviso() {
  // El aviso solo flota mientras se ve el viaje (portada, resultado, qué hacer); en la parte de datos se esconde. Mientras
  // se ven los botones de lugar y mes, no flota (taparía los meses): ahí se muestra el aviso dentro de la portada.
  const zonas = ["inicio", "planea", "que-hacer"].map($).filter(Boolean), dentro = new Set();
  let eligiendo = false;
  const pintar = () => {
    aviso.visible = dentro.size > 0 && !eligiendo;
    const caja = $("aviso-lleno");
    if (caja) caja.classList.toggle("fuera", !aviso.visible);
  };
  const obs = new IntersectionObserver((es) => {
    es.forEach((e) => (e.isIntersecting ? dentro.add(e.target) : dentro.delete(e.target)));
    pintar();
  });
  zonas.forEach((z) => obs.observe(z));
  // "Eligiendo" = los meses se ven completos en pantalla (no basta con que asome un pedazo de la portada).
  new IntersectionObserver(([e]) => { eligiendo = e.intersectionRatio > 0.5; pintar(); }, { threshold: [0, 0.5, 1] })
    .observe(document.querySelector("#elige .planea-meses"));
}

// Qué hacer: tres bloques (día, tarde, noche). Al bajar, el cielo se oscurece y el sol se vuelve atardecer y luna.
const MOMENTOS = [
  { clave: "dia", titulo: "De día", bajada: "Zonas arqueológicas, museos y paseos; para empezar, un café o un desayuno." },
  { clave: "tarde", titulo: "Por la tarde", bajada: "Un balneario o un parque, y a comer: mariscos, cocina yucateca o comida casera." },
  { clave: "noche", titulo: "De noche", bajada: "Antojitos y tacos para cenar, un bar para cerrar el día y dónde dormir." },
];

// Dos enlaces por negocio (decisión 16): "Cómo llegar" va a las coordenadas del DENUE; "Reseñas" busca el negocio por
// nombre en Google Maps, donde se leen sus estrellas y opiniones. La página no copia ninguna reseña (regla de oro 4).
const enlacesGoogle = (x) => `<span class="negocio-enlaces">
    <a class="maps" href="${esc(x.maps)}" target="_blank" rel="noopener noreferrer">Cómo llegar<span aria-hidden="true"> ↗</span><span class="oculto"> (Google Maps, otra pestaña)</span></a>
    ${x.resenas ? `<a class="maps resenas" href="${esc(x.resenas)}" target="_blank" rel="noopener noreferrer"><span aria-hidden="true">★ </span>Reseñas<span aria-hidden="true"> ↗</span><span class="oculto"> en Google Maps (otra pestaña)</span></a>` : ""}</span>`;

function tarjetaNegocio(x) {
  const donde = x.km === null ? "" : x.otro ? `en ${esc(x.loc)}, a ${num(Math.round(x.km))} km` : x.km < 1 ? "en el centro" : `a ${x.km} km del centro`;
  return `<li class="negocio${x.otro ? " lejos" : ""}"><b data-no-traducir>${esc(x.n)}</b><small>${esc(x.t)}${donde ? ` · ${donde}` : ""}</small>${enlacesGoogle(x)}</li>`;
}

// ---------- Postales: tira horizontal que se mueve sola (se detiene al pasar el mouse o con movimiento reducido) ----------
function postales() {
  const V = D.vitrina, caja = $("postales");
  if (!V || !caja) return;
  // Las del lugar elegido arriba (decisión 17); sin planeador, todas.
  const L = D.pronostico && D.pronostico.lugares[plan.lugar];
  let fotos = L ? V.postales.filter((x) => x.lugar === L.clave) : V.postales;
  if (!fotos.length) fotos = V.postales;
  while (fotos.length < 8) fotos = fotos.concat(fotos);  // que la tira llene pantallas anchas
  const foto = (x, copia) => `<li${copia ? ' aria-hidden="true"' : ""}><figure><img src="${esc(x.archivo)}" alt="${copia ? "" : esc(x.muestra)}" loading="lazy" width="420" height="300">
    <figcaption><b>${esc(x.muestra)}</b><small data-no-traducir>${esc(x.autor)} · ${esc(x.licencia)}</small></figcaption></figure></li>`;
  // La tira se duplica para que el movimiento no tenga corte; la copia no se lee en voz alta.
  caja.innerHTML = `<p class="rotulo postales-rotulo">${L ? `Postales de ${esc(L.nombre)}` : "Postales del sur"} · fotos tomadas en cada lugar</p>
    <div class="tira" tabindex="0" aria-label="Fotos del lugar elegido; se pueden recorrer con las flechas"><ul class="tira-pista">${fotos.map((x, i) => foto(x, i >= V.postales.filter((y) => !L || y.lugar === L.clave).length)).join("")}${fotos.map((x) => foto(x, true)).join("")}</ul></div>`;
  caja.hidden = false;
}

// ---------- Vive el sur: experiencias reales y rutas de 2 y 3 días ----------
function vive() {
  const V = D.vitrina, caja = $("vive");
  if (!V || !caja) return;
  // Primero lo del lugar elegido arriba; después, lo del sur (si eliges el norte, se te propone bajar al sur).
  const L = D.pronostico && D.pronostico.lugares[plan.lugar], clave = L ? L.clave : null;
  const delLugar = V.experiencias.filter((e) => e.lugar === clave);
  const delSur = V.experiencias.filter((e) => e.lugar !== clave && !e.referencia);
  const experiencias = delLugar.concat(delSur);
  const rutasVer = clave ? V.rutas.filter((r) => r.lugares.includes(clave)) : V.rutas;
  const exp = experiencias.map((e, i) => `
    <article class="experiencia revela" style="--i:${i}">
      <div class="experiencia-foto"><img src="${esc(e.foto)}" alt="" loading="lazy"></div>
      <div class="experiencia-texto">
        ${e.lugar !== clave ? `<p class="experiencia-lugar">En el sur · ${esc((LUGARES().find((x) => x.clave === e.lugar) || { nombre: e.lugar }).nombre)}</p>` : e.referencia ? `<p class="experiencia-lugar ref">Referencia: la campaña no lo promueve</p>` : ""}
        <h3>${esc(e.titulo)}</h3>
        <p>${esc(e.texto)}</p>
        <p class="experiencia-dato">${esc(e.dato)} <small>Fuente: ${esc(e.fuente)}</small></p>
        <ul class="experiencia-lugares">${e.negocios.map((x) => `<li><b data-no-traducir>${esc(x.n)}</b><small data-no-traducir>${esc(x.loc)}</small>${enlacesGoogle(x)}</li>`).join("")}</ul>
      </div>
    </article>`).join("");
  const rutas = rutasVer.map((r, i) => `
    <article class="ruta revela" style="--i:${i}">
      <div class="ruta-foto"><img src="${esc(r.foto)}" alt="" loading="lazy"><span class="ruta-dias">${r.dias === 1 ? "1 día" : `${r.dias} días`}</span></div>
      <h3>${esc(r.titulo)}</h3>
      <ol class="ruta-paradas">${r.paradas.map((p, k) => `<li><span class="ruta-punto" aria-hidden="true"></span>${esc(p)}${k < r.km.length ? `<small class="ruta-km">${r.km[k] < 1 ? "a pie →" : `${num(r.km[k])} km →`}</small>` : ""}</li>`).join("")}</ol>
      <p class="ruta-mes">${r.referencia ? "Mes menos lleno" : "Mejor mes"}: <b>${MESES[r.mes - 1]}</b> · ${esc(r.por_que)}</p>
      ${D.pronostico && r.planeador ? `<button type="button" class="boton boton-claro ruta-boton" data-mes="${r.mes}" data-lugar="${esc(r.planeador)}">Ver cómo está en ${MESES[r.mes - 1]}</button>` : ""}
    </article>`).join("");
  caja.innerHTML = `
    <div class="vive-dentro">
      <p class="rotulo revela">Vive el sur</p>
      <h2 class="h2 revela equilibrar" id="t-vive">Lo que no te <em>cuentan</em> del Caribe.</h2>
      <p class="vive-bajada revela">Primero, lo del lugar que elegiste arriba; después, lo del sur. Lugares reales y una cifra oficial en cada uno. Sin precios: ninguna fuente oficial los publica.</p>
      <div class="experiencias">${exp}</div>
      <h3 class="vive-sub revela" id="rutas">Rutas de 2 y 3 días</h3>
      <div class="rutas">${rutas}</div>
      <p class="vive-nota">${esc(V.nota)}</p>
    </div>`;
  caja.hidden = false;
  alAparecer([...caja.querySelectorAll(".revela")], (n) => n.classList.add("visible"));
  // "Ver cómo está en mayo": lleva al planeador con ese mes (el primero de la lista con ese número de mes)
  caja.querySelectorAll(".ruta-boton").forEach((b) => b.addEventListener("click", () => {
    const P = D.pronostico, k = P.meses.findIndex((ym) => mesDe(ym).m === +b.dataset.mes);
    const l = P.lugares.findIndex((x) => x.clave === b.dataset.lugar);
    if (l >= 0) plan.lugar = l;
    if (k >= 0) plan.mes = k;
    pintarPlan(P); dibujarQueHacer(P);
    $("planea").scrollIntoView({ behavior: QUIETO ? "auto" : "smooth" });
  }));
}

// ---------- Lo que vivimos: fotos y reseñas del equipo (solo si hay aportes reales; decisión 16) ----------
function vivimos() {
  const A = D.aportes, caja = $("vivimos");
  if (!caja || !A || !A.length) return;
  const nombre = (c) => (LUGARES().find((r) => r.clave === c) || { nombre: c }).nombre;
  const estrellas = (n) => `<span class="estrellas" role="img" aria-label="${n} de 5 estrellas">${"★".repeat(n)}<span aria-hidden="true">${"★".repeat(5 - n)}</span></span>`;
  const fecha = (f) => { const [a, m] = f.split("-").map(Number); return `${MESES[m - 1]} de ${a}`; };
  caja.innerHTML = `
    <div class="vivimos-dentro">
      <p class="rotulo revela">Lo que vivimos</p>
      <h2 class="h2 revela equilibrar" id="t-vivimos">Fuimos, <em>probamos</em> y te contamos.</h2>
      <div class="vivimos-rejilla">${A.map((a) => a.tipo === "foto"
        ? `<figure class="aporte revela"><img src="${esc(a.archivo)}" alt="${esc(a.texto)}" loading="lazy" width="${a.ancho}" height="${a.alto}"><figcaption>${esc(a.texto)}<small>${esc(nombre(a.lugar))} · ${esc(a.autor)}, ${fecha(a.fecha)}</small></figcaption></figure>`
        : `<blockquote class="aporte resena revela">${estrellas(a.estrellas)}<p>“${esc(a.texto)}”</p><footer>${esc(a.autor)} · ${esc(nombre(a.lugar))}, ${fecha(a.fecha)}</footer></blockquote>`).join("")}</div>
      <p class="vive-nota">Fotos y opiniones del equipo, tomadas en cada lugar. Las estrellas son la opinión de quien escribe, no una calificación oficial.</p>
    </div>`;
  caja.hidden = false;
}

// ---------- Preguntas frecuentes (las mismas respuestas del chat, con su fuente) ----------
function preguntas() {
  const caja = $("preguntas");
  if (!caja || !D.preguntas) return;
  caja.innerHTML = `
    <div class="preguntas-dentro">
      <p class="rotulo revela">Preguntas frecuentes</p>
      <h2 class="h2 revela equilibrar" id="t-preguntas">Lo que todos <em>preguntan</em>.</h2>
      <div class="acordeon">${D.preguntas.map((p) => `
        <details class="pregunta revela"><summary><span>${esc(p.pregunta)}</span><i aria-hidden="true"></i></summary>
          <div class="respuesta"><p>${esc(p.respuesta)}</p><small>Fuente: ${esc(p.fuente)}</small></div></details>`).join("")}</div>
    </div>`;
  caja.hidden = false;
}

function dibujarQueHacer(P) {
  const caja = $("que-hacer"), L = P.lugares[plan.lugar];
  caja.hidden = false;
  caja.innerHTML = `
    <div class="cielo" aria-hidden="true"><svg viewBox="0 0 120 120" class="astro">
      <defs><mask id="luna-mascara"><rect width="120" height="120" fill="#fff"/><circle class="sombra" cx="150" cy="44" r="30" fill="#000"/></mask></defs>
      <g class="rayos">${Array.from({ length: 12 }, (_, i) => `<rect x="57" y="6" width="6" height="16" rx="3" transform="rotate(${i * 30} 60 60)"/>`).join("")}</g>
      <circle class="disco" cx="60" cy="60" r="28" mask="url(#luna-mascara)"/></svg></div>
    <div class="que-hacer-cabeza"><p class="rotulo">Qué hacer</p>
      <h2 class="h2 equilibrar" id="t-que-hacer">Un día en <em>${esc(L.nombre)}</em></h2>
      <p class="que-hacer-bajada">Lugares reales del directorio de negocios del INEGI, del más cercano al más lejano. No son reseñas ni anuncios pagados y el directorio no publica horarios: confirma antes de ir.</p>
      ${L.comida && L.comida.length ? `<div class="comida-galeria"><p class="lugar-fotos-titulo">Así se come en ${esc(L.nombre)}</p>
        <ul>${L.comida.map((x) => `<li><figure><img src="${esc(x.archivo)}" alt="${esc(x.muestra)}" loading="lazy" width="${x.ancho}" height="${x.alto}">
          <figcaption>${esc(x.muestra)}<small>Foto: <span data-no-traducir>${esc(x.autor)}</span>, <a href="${esc(x.url_licencia || x.url_original)}" rel="license noopener noreferrer" target="_blank" data-no-traducir>${esc(x.licencia)}</a></small></figcaption></figure></li>`).join("")}</ul></div>` : ""}</div>
    ${MOMENTOS.map((m) => {
      const hacer = (m.clave === "dia" ? L.zonas : []).concat(L.hacer[m.clave]);
      const comer = L.comer[m.clave];
      return `<div class="momento m-${m.clave}" data-momento="${m.clave}">
        <h3 class="momento-titulo">${m.titulo}</h3><p class="momento-bajada">${m.bajada}</p>
        <div class="momento-rejilla">
          <div><h4>Qué hacer</h4><ul class="negocios">${hacer.map(tarjetaNegocio).join("")}</ul></div>
          <div><h4>Dónde comer</h4><ul class="negocios">${comer.map(tarjetaNegocio).join("")}</ul></div>
          ${m.clave === "noche" ? `<div><h4>Dónde dormir</h4>${L.estrellas ? `<p class="estrellas-oficiales"><span aria-hidden="true">★★★★★</span> ${L.estrellas.por_categoria["5"]} % de los cuartos de hotel son de 5 estrellas (categoría oficial, ${L.estrellas.anio})</p>` : ""}<ul class="negocios">${L.dormir.map(tarjetaNegocio).join("")}</ul></div>` : ""}
        </div></div>`;
    }).join("")}
    <p class="que-hacer-nota">${L.estrellas ? `Categoría de hotel: ${esc(L.estrellas.fuente)}. ` : ""}Fuente: INEGI, Directorio Estadístico Nacional de Unidades Económicas (DENUE). El tipo de lugar y el momento del día los sugiere un clasificador de texto que lee el nombre y el giro oficial de cada negocio (acertó 39 de 40 en una revisión al azar). Cuando un lugar no tiene algo cerca, se muestra lo más cercano de los otros lugares del sur. "Ver en Google Maps" abre Google Maps en otra pestaña; esta página no descarga nada de Google.</p>`;
  cieloConScroll(caja);
  // Las postales y "Vive el sur" siguen al lugar elegido (decisión 17)
  postales();
  vive();
}

let cieloActivo = null;
function cieloConScroll(caja) {
  // p va de 0 (arriba del bloque de día) a 1 (abajo del de noche). El sol pierde los rayos, se pone naranja y una sombra
  // entra por la derecha hasta dejar una luna. Con movimiento reducido, cambia de golpe en cada bloque.
  const astro = caja.querySelector(".astro"), sombra = caja.querySelector(".sombra");
  const bloques = [...caja.querySelectorAll(".momento")];
  const pintar = (p) => {
    p = Math.min(1, Math.max(0, p));
    caja.style.setProperty("--p", p.toFixed(3));
    const rayos = Math.max(0, 1 - p * 2.2);
    astro.querySelector(".rayos").style.opacity = rayos;
    astro.querySelector(".rayos").style.transform = `scale(${0.6 + 0.4 * rayos})`;
    const luna = Math.min(1, Math.max(0, (p - 0.45) / 0.35));  // la sombra entra en el atardecer: luna completa al 80 %
    sombra.setAttribute("cx", (150 - 78 * luna).toFixed(1));
    astro.dataset.fase = p < 0.34 ? "dia" : p < 0.67 ? "tarde" : "noche";
  };
  if (cieloActivo) window.removeEventListener("scroll", cieloActivo);
  if (QUIETO) {
    alAparecer(bloques, (b) => pintar({ dia: 0, tarde: 0.5, noche: 1 }[b.dataset.momento]), 0.3);
    pintar(0); return;
  }
  let pendiente = false;
  cieloActivo = () => {
    if (pendiente) return; pendiente = true;
    requestAnimationFrame(() => {
      pendiente = false;
      // La fase sigue al bloque que cruza la línea de lectura (45 % de la pantalla): día, tarde o noche.
      const linea = window.innerHeight * 0.45;
      let p = 0;
      bloques.forEach((b, i) => {
        const r = b.getBoundingClientRect();
        if (r.top <= linea) p = (i + Math.min(1, (linea - r.top) / Math.max(1, r.height))) / bloques.length;
      });
      pintar(p);
    });
  };
  window.addEventListener("scroll", cieloActivo, { passive: true });
  cieloActivo();
}

function modulos() {
  MODULOS.forEach((m) => {
    const caja = document.querySelector(`[data-clave="${m.clave}"]`);
    if (D[m.clave] && caja && DIBUJAR[m.clave]) { DIBUJAR[m.clave](caja, D[m.clave]); caja.hidden = false; }
  });
}

// ---------- Las 12 fases: cada tarjeta se llena cuando su fase deja un resultado real ----------
function fases() {
  const estado = { lista: ["lista", "Lista"], "en curso": ["curso", "En curso"], pendiente: ["pendiente", "Pendiente"] };
  $("lista-fases").innerHTML = D.fases.map((f, i) => {
    const [clase, texto] = estado[f.estado];
    const final = f.resultado
      ? `<p class="fase-resultado">${f.resultado}${f.enlace ? `<br><a href="${f.enlace}">Verlo en la página →</a>` : ""}</p>`
      : `<p class="fase-llena">Se llena en esta fase</p>`;
    return `<li class="fase ${clase}" style="--i:${i}">
      <div class="fase-cabeza"><span class="fase-num">${f.fase}</span><span class="fase-estado">${texto}</span></div>
      <h3 class="fase-nombre">${f.nombre}</h3><p class="fase-entrega">${f.entrega}</p>${final}</li>`;
  }).join("");
  alAparecer([$("lista-fases")], (n) => n.classList.add("visible"), 0.1);
}

// ---------- ¿Cómo se mueve la gente? Mapa de todo el estado con llegadas por medio de transporte ----------
const MODOS_VISTA = [
  { clave: "avion", nombre: "Avión", color: "#FFB000", dx: -7, dy: -7 },
  { clave: "tren", nombre: "Tren Maya", color: "#FF4FA3", dx: 7, dy: -7 },
  { clave: "crucero", nombre: "Crucero", color: "#3FD3C9", dx: 7, dy: 7 },
  { clave: "frontera", nombre: "Frontera", color: "#FF7A45", dx: -7, dy: 7 },
];

function mapaMovimiento() {
  const M = D.movimiento, svg = $("mapa-mov"), globo = $("globo-mov");
  const todos = D.mapa.municipios.flatMap((m) => m.anillos.flat());
  const lons = todos.map((p) => p[0]), lats = todos.map((p) => p[1]);
  const [o, e, s, n] = [Math.min(...lons), Math.max(...lons), Math.min(...lats), Math.max(...lats)];
  const k = Math.cos(((s + n) / 2) * Math.PI / 180), H = 760, esc = H / (n - s), W = (e - o) * k * esc + 20;
  const x = (lon) => (lon - o) * k * esc + 10, y = (lat) => (n - lat) * esc;
  // Margen extra a la derecha y arriba: ahí caben la burbuja de Cancún y los nombres sin cortarse en el celular.
  svg.setAttribute("viewBox", `-10 -30 ${(W + 130).toFixed(0)} ${H + 50}`);
  for (const m of D.mapa.municipios) {
    const p = el("path", { class: "mun", d: m.anillos.map((a) => "M" + a.map(([lo, la]) => `${x(lo).toFixed(1)},${y(la).toFixed(1)}`).join("L") + "Z").join("") }, svg);
    el("title", {}, p).textContent = m.nombre;
  }
  // Ruta del Tren Maya como ESQUEMA: une las estaciones en su orden; no es el trazo exacto de la vía.
  const ruta = el("path", { class: "ruta", d: "M" + M.ruta_tren.map((r) => `${x(r.lon).toFixed(1)},${y(r.lat).toFixed(1)}`).join("L") }, svg);
  const burbujas = [], etiquetas = {};
  const capaBurbujas = el("g", {}, svg), capaNombres = el("g", {}, svg);  // los nombres van encima de todas las burbujas
  const A_LA_IZQUIERDA = new Set(["Playa del Carmen"]);  // su nombre a la derecha caería sobre la burbuja de Cozumel
  for (const mv of MODOS_VISTA) {
    for (const p of M.modos[mv.clave].puntos) {
      if (p.lat === undefined) continue;  // Holbox (Tren Maya): SITUR-Q no publica dónde está su estación
      const c = el("circle", { class: `burbuja m-${mv.clave}`, cx: x(p.lon) + mv.dx, cy: y(p.lat) + mv.dy, r: 0, "stroke-width": 1.5 }, capaBurbujas);
      const texto = `${p.lugar}: ${num(p.valor)} ${M.modos[mv.clave].texto} (${M.modos[mv.clave].anio})`;
      el("title", {}, c).textContent = texto;
      c.addEventListener("pointerenter", () => { globo.textContent = texto; globo.hidden = false; });
      c.addEventListener("pointerleave", () => { globo.hidden = true; });
      burbujas.push({ c, modo: mv.clave, valor: p.valor });
      const izq = A_LA_IZQUIERDA.has(p.lugar);
      if (!etiquetas[p.lugar]) etiquetas[p.lugar] = el("text", { class: "etiqueta", x: x(p.lon) + (izq ? -16 : 16), y: y(p.lat) + 4, "text-anchor": izq ? "end" : "start" }, capaNombres);
      etiquetas[p.lugar].textContent = p.lugar;
    }
  }
  svg.parentElement.addEventListener("pointermove", (ev) => {
    const r = ev.currentTarget.getBoundingClientRect();
    globo.style.transform = `translate(${ev.clientX - r.left + 14}px, ${ev.clientY - r.top + 14}px)`;
  });

  $("mov-totales").innerHTML = MODOS_VISTA.map((mv) => {
    const m = M.modos[mv.clave];
    return `<li class="t-${mv.clave}" data-modo="${mv.clave}"><b data-contar="${m.total}">${num(m.total)}</b><span>${m.texto} en ${m.anio}</span></li>`;
  }).join("");
  $("mov-nota").textContent = "Cada burbuja crece según las llegadas de su lugar. El avión llega hasta 2024: después la fuente dejó de publicar. " +
    "La línea rosa es un esquema del recorrido del Tren Maya. No existen datos públicos de viajes de un lugar a otro, así que no se dibujan. Fuente: SITUR-Q.";
  $("filtros").innerHTML = [`<button class="filtro" type="button" data-modo="todos" aria-pressed="true">Todos</button>`,
    ...MODOS_VISTA.map((mv) => `<button class="filtro" type="button" data-modo="${mv.clave}" aria-pressed="false"><i style="background:${mv.color}"></i>${mv.nombre}</button>`)].join("");

  const RMAX = 64, RMIN = 3.5;
  function mostrar(modo) {
    const visibles = burbujas.filter((b) => modo === "todos" || b.modo === modo);
    const maximo = Math.max(...visibles.map((b) => b.valor));  // escala común dentro de la vista elegida
    burbujas.forEach((b) => {
      const ver = visibles.includes(b);
      b.c.classList.toggle("oculta", !ver);
      b.c.style.r = `${ver ? Math.max(RMIN, Math.sqrt(b.valor / maximo) * RMAX).toFixed(1) : 0}px`;  // el área es proporcional a las llegadas
    });
    ruta.classList.toggle("ver", modo === "todos" || modo === "tren");
    document.querySelectorAll(".mov-totales li").forEach((li) => li.classList.toggle("apagado", modo !== "todos" && li.dataset.modo !== modo));
    document.querySelectorAll(".filtro").forEach((f) => f.setAttribute("aria-pressed", f.dataset.modo === modo));
  }
  $("filtros").addEventListener("click", (ev) => { const f = ev.target.closest(".filtro"); if (f) mostrar(f.dataset.modo); });
  alAparecer([svg], () => { mostrar("todos"); document.querySelectorAll(".mov-totales [data-contar]").forEach(contar); }, 0.3);
}

// ---------- ¿Dónde se queda el dinero? ----------
function dinero() {
  const h = D.hospedaje;
  const maximo = Math.max(...h.destinos.map((d) => d.cuartos_por_hotel));
  $("barras-hotel").innerHTML = [...h.destinos].sort((a, b) => b.cuartos_por_hotel - a.cuartos_por_hotel).map((d, i) =>
    `<li class="${d.es_de_los_lugares ? "nuestro" : ""}" style="--i:${i}"><span>${d.lugar}</span><span class="pista"><span class="relleno" style="--w:${(d.cuartos_por_hotel / maximo * 100).toFixed(1)}%"></span></span><b>${Math.round(d.cuartos_por_hotel)}</b></li>`).join("");
  $("nota-hotel").textContent = `Cuartos entre hoteles, ${h.mes}. En amarillo, los lugares de la campaña. Fuente: ${h.fuente_cuartos}.`;
  const t = h.tamano_negocios;
  const pila = (nombre, r) => {
    const total = r.chicos + r.medianos + r.grandes;
    const seg = (k, clase) => r[k] ? `<span class="${clase}" style="--w:${(r[k] / total * 100).toFixed(1)}%">${r[k] / total > .07 ? num(r[k]) : ""}</span>` : "";
    return `<div class="tamano"><p>${nombre} · ${num(total)} hospedajes</p><div class="pila">${seg("chicos", "s-chicos")}${seg("medianos", "s-medianos")}${seg("grandes", "s-grandes")}</div></div>`;
  };
  $("tamanos").innerHTML = pila("Municipios de los cinco lugares", t.municipios_de_los_lugares) + pila("Resto del estado", t.resto_del_estado) +
    `<p class="leyenda-tamano"><span><i class="s-chicos"></i>Chicos: hasta 10 personas</span><span><i class="s-medianos"></i>Medianos: 11 a 250</span><span><i class="s-grandes"></i>Grandes: más de 250</span></p>`;
  const sur = t.municipios_de_los_lugares;
  $("frase-tamano").innerHTML = sur.grandes === 0
    ? `En los municipios de los cinco lugares <strong>no hay ningún hospedaje grande</strong>: ${num(sur.chicos)} son chicos y ${num(sur.medianos)} medianos.`
    : `En los municipios de los cinco lugares hay ${num(sur.grandes)} hospedajes grandes, ${num(sur.chicos)} chicos y ${num(sur.medianos)} medianos.`;
  $("nota-tamano").textContent = `Fuente: ${h.fuente_negocios}.`;
  $("hueco-derrama").textContent = h.hueco_derrama;
  alAparecer([...document.querySelectorAll(".dinero-caja")], (n) => n.classList.add("visible"), 0.25);
}

// ---------- Quiénes somos ----------
function equipo() {
  const iniciales = (n) => n.split(" ").filter(Boolean).slice(0, 2).map((p) => p[0]).join("");
  $("personas").innerHTML = D.equipo.map((p) => p.nombre
    ? `<li class="persona revela"><span class="avatar" aria-hidden="true">${iniciales(p.nombre)}</span><h3>${p.nombre}</h3><p class="rol">${p.rol}</p><p class="hace">${p.hace}</p></li>`
    : `<li class="persona pendiente revela"><span class="avatar" aria-hidden="true">?</span><h3>Nombre por confirmar</h3><p class="rol">${p.rol}</p><p class="hace">${p.hace}</p></li>`).join("");
}

// ---------- Preguntas rápidas: respuestas fijas con datos del proyecto ----------
function chat() {
  const boton = $("chat-boton"), panel = $("chat"), mensajes = $("chat-mensajes"), entrada = $("chat-entrada");
  const P = D.preguntas;
  const limpiar = (t) => t.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[¿?¡!.,]/g, " ");
  const agregar = (clase, html) => {
    const m = document.createElement("div");
    m.className = `msg ${clase}`;
    m.innerHTML = html;
    mensajes.appendChild(m);
    mensajes.scrollTop = mensajes.scrollHeight;
    return m;
  };
  const responder = (texto, fija = null) => {
    agregar("yo", texto.replace(/</g, "&lt;"));
    const q = fija || (() => {
      const t = limpiar(texto);
      // En otro idioma también cuentan las palabras de la pregunta traducida (o pares de caracteres en chino, japonés y
      // coreano, que no separan palabras). Así "when is the best time to go?" encuentra "¿Cuándo conviene ir?".
      const trozos = (x) => { const y = limpiar(x); return /\s/.test(y.trim()) ? y.split(/\s+/).filter((w) => w.length > 3)
        : [...y.replace(/\s/g, "")].map((c, i, a) => c + (a[i + 1] || "")).filter((w) => w.length === 2); };
      let mejor = null, puntos = 0;
      for (const p of P) {
        let s = p.claves.reduce((acc, c) => acc + (t.includes(limpiar(c).trim()) ? 1 : 0), 0);
        const tr = window.Idiomas && Idiomas.traducirTexto(p.pregunta);
        if (tr) s += trozos(tr).filter((w) => t.includes(w)).length;
        if (s > puntos) { puntos = s; mejor = p; }
      }
      return mejor;
    })();
    const espera = agregar("bot", `<span class="escribiendo" aria-label="Escribiendo"><i></i><i></i><i></i></span>`);
    setTimeout(() => {
      // Respuesta y fuente en bloques separados: así cada uno coincide con su frase del diccionario y se traduce.
      espera.innerHTML = q ? `<p>${q.respuesta}</p><small>Fuente: ${q.fuente}</small>`
        : "<p>Todavía no tengo esa respuesta. Prueba con una de las preguntas de abajo: solo respondo lo que los datos del proyecto pueden sostener.</p>";
      mensajes.scrollTop = mensajes.scrollHeight;
    }, QUIETO ? 0 : 550);
  };
  $("chat-sugerencias").innerHTML = P.map((p, i) => `<button class="sugerencia" type="button" data-i="${i}">${p.pregunta}</button>`).join("");
  $("chat-sugerencias").addEventListener("click", (ev) => { const b = ev.target.closest(".sugerencia"); if (b) responder(b.textContent, P[Number(b.dataset.i)]); });
  $("chat-forma").addEventListener("submit", (ev) => { ev.preventDefault(); const t = entrada.value.trim(); if (t) { responder(t); entrada.value = ""; } });
  const abrir = (si) => {
    panel.hidden = !si;
    boton.setAttribute("aria-expanded", si);
    if (si) {
      if (!mensajes.children.length) agregar("bot", "Hola. Pregúntame sobre los cinco lugares, cómo llegar o de dónde salen los datos.");
      entrada.focus();
    } else boton.focus();
  };
  boton.addEventListener("click", () => abrir(true));
  $("chat-cerrar").addEventListener("click", () => abrir(false));
  panel.addEventListener("keydown", (ev) => { if (ev.key === "Escape") abrir(false); });
}

// ---------- Evidencia y pie ----------
function evidencia() {
  const r = D.resumen_datos;
  const cifra = (v, t) => `<div class="cifra revela"><b data-contar="${v}">${num(v)}</b><span>${t}</span></div>`;
  $("cifras").innerHTML = cifra(r.registros, "registros oficiales reunidos") + cifra(r.archivos, "archivos descargados y verificados") +
    cifra(D.regiones.length, "lugares comprobados en Quintana Roo");
  if (D.criterios) {
    const fmt = (v, suf = "") => (v === null || v === undefined ? "sin dato" : `${Number(v).toLocaleString("es-MX")}${suf}`);
    $("tabla-criterios").innerHTML = `<table class="tabla"><caption class="rotulo" style="caption-side:top;text-align:left;margin-bottom:10px">Criterios de selección</caption>
      <thead><tr><th>Lugar</th><th>Sargazo</th><th>Cierres</th><th>Hoteles ocupados 2024</th><th>Visitantes por habitante</th></tr></thead>
      <tbody>${D.criterios.map((c) => `<tr class="${c.papel}"><td>${c.region}${c.papel === "referencia" ? " (referencia)" : ""}</td><td>${c.c1_sargazo}</td>
        <td class="${c.c2_pasa ? "si" : "no"}">${c.c2_pasa ? "pasa" : "no pasa"}</td><td>${fmt(c.c3_ocupacion_2024_pct, " %")}</td>
        <td>${fmt(c.c3_visitantes_inah_por_residente)}</td></tr>`).join("")}</tbody></table>`;
  }
  probado();
  const fotos = [D.portada, ...D.regiones.map((x) => x.foto)].filter(Boolean);
  $("pie-creditos").innerHTML = "Fotos: " + fotos.map((f) => `${f.muestra} (${f.autor}, <a href="${f.url_original}">${f.licencia}</a>)`).join(" · ");
  $("pie-autor").textContent = `Torre del Caribe · Universidad Nacional Rosario Castellanos · Ciencias de Datos para Negocios, 2026-2 · Brandon Uriel García Sánchez · Datos del ${fechaLarga(D.generado)}`;
}

// ---------- Cómo se probó cada resultado (evidencia ampliada; auditoría de las Fases 1–4) ----------
function probado() {
  const E = D.evidencia, R = D.radar, caja = $("probado");
  if (!E) return;
  const tarjeta = (titulo, cuerpo, clase = "") => `<article class="prueba revela ${clase}"><h3>${titulo}</h3>${cuerpo}</article>`;
  const partes = [];
  if (R) {
    const m = R.modelo;
    partes.push(tarjeta("El Radar contra “igual que el mes pasado”",
      `<p class="prueba-cifra"><b>${m.aciertos}</b> de ${m.casos}</p>
       <p>meses que el modelo nunca vio, acertados. Repetir el mes anterior acierta ${m.aciertos_persistencia}. Su valor: anticipó ${m.cambios_anticipados} de los ${m.cambios_reales} cambios de estado.</p>
       ${m.cambios_en_los_5 !== null && m.cambios_en_los_5 !== undefined ? `<p class="prueba-ojo">En los cinco lugares hubo ${m.cambios_en_los_5} cambios en esos meses: ahí el modelo casi no se ha podido probar.</p>` : ""}`));
  }
  const filas = E.markov.map((x) => `<tr><td>${x.semanas} ${x.semanas === 1 ? "semana" : "semanas"}</td><td>${x.brier_markov.toFixed(3)}</td><td>${x.brier_persistencia.toFixed(3)}</td></tr>`).join("");
  partes.push(tarjeta("¿Se llenará el norte? La cadena de Markov",
    `<p>Sus probabilidades fallan menos que “igual que la semana pasada” a 1, 4 y 8 semanas (error de Brier: más bajo es mejor).</p>
     <table class="prueba-tabla"><thead><tr><th>Horizonte</th><th>Markov</th><th>Igual que hoy</th></tr></thead><tbody>${filas}</tbody></table>`));
  const cl = E.clustering;
  partes.push(tarjeta("El norte, entre los más llenos del país",
    `<p class="prueba-cifra"><b>${cl.centros_grupo_lleno}</b> de ${cl.centros}</p>
     <p>centros turísticos del país forman el grupo más lleno (${cl.nivel_grupo_lleno} % de ocupación promedio, contra ${cl.nivel_resto} % del resto). Ahí están, como referencia, ${cl.qroo_en_grupo_lleno.join(", ")}.</p>`));
  if (E.pruebas) partes.push(tarjeta("Todo se vuelve a comprobar",
    `<p class="prueba-cifra"><b data-contar="${E.pruebas}">${E.pruebas}</b></p>
     <p>pruebas automáticas comparan las cifras con valores conocidos, incluidas las de los documentos. Al volver a correr todo, los resultados salen idénticos. ${E.auditoria}.</p>`));
  partes.push(tarjeta("Lo que no sabemos, dicho", `<ul>${E.huecos.map((h) => `<li>${h}</li>`).join("")}</ul>`, "prueba-ancha"));
  caja.innerHTML = `<h3 class="rotulo probado-titulo revela">Cómo se probó</h3><div class="probado-rejilla">${partes.join("")}</div>`;
  caja.hidden = false;
}

// Nombres de lugares que cambian dentro de las frases (para que el traductor los trate como marcas; idiomas.js)
if (window.Idiomas) Idiomas.registrarLugares([...new Set([...D.regiones.map((r) => r.nombre), ...LUGARES().map((r) => r.nombre),
  ...(D.pronostico ? D.pronostico.lugares.map((l) => l.nombre) : [])])]);
tema();
postales();
vive();
vivimos();
preguntas();
barra();
anuncio();
portada();
elDato();
problema();
construirMapa();
capitulos();
mapaMovimiento();
dinero();
elNorte();
modulos();
fases();
equipo();
evidencia();
chat();
alAparecer([...document.querySelectorAll(".revela")], (n) => { n.classList.add("visible"); n.querySelectorAll("[data-contar]").forEach(contar); if (n.dataset.contar) contar(n); });
equilibrarTitulos();
