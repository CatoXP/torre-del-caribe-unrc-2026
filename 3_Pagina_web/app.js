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
  as.map((a) => a.getAttribute("href")).filter((h) => h.startsWith("#")).forEach((h) => $(h.slice(1)) && obs.observe($(h.slice(1))));
}

// ---------- Anuncio del Radar (arriba de todo). Solo si pagina.js trae "radar"; el texto sale de sus datos. ----------
function anuncio() {
  const R = D.radar, a = $("anuncio"), P = D.pronostico;
  if (!a) return;  // datos.html no lleva anuncio
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

// Ficha de cada lugar (decisión 25): foto, qué es y fotos de mañana, tarde y noche. Sin cifras, semáforo ni avisos:
// el equipo las quitó de la parte del viajero; el Radar completo y las cifras siguen en datos.html.
// Tres fotos más en cada ficha (decisión 25): una de mañana, una de tarde y una de noche cuando existen.
function masFotos(r) {
  const L = D.pronostico && D.pronostico.lugares.find((x) => x.clave === r.clave);
  if (!L || !L.fotos) return "";
  const elegidas = ["dia", "tarde", "noche"].map((m) => repartir(L.fotos.filter((f) => f.momento === m && f.archivo !== (r.foto && r.foto.archivo_local)), 1)[0]).filter(Boolean);
  if (!elegidas.length) return "";
  return `<ul class="capitulo-mas">${elegidas.map((f) => `<li><img src="${esc(f.archivo)}" alt="${esc(f.muestra)}" loading="lazy"><small>${creditoCorto(f)}</small></li>`).join("")}</ul>`;
}

function capitulos() {
  const lista = $("capitulos");
  lista.innerHTML = LUGARES().map((r) => `
    <li class="capitulo" id="lugar-${r.numero}" data-n="${r.numero}">
      <p class="capitulo-num">${String(r.numero).padStart(2, "0")} / ${String(LUGARES().length).padStart(2, "0")}</p>
      <h3>${r.nombre}${r.referencia ? ` <span class="etiqueta-ref">Referencia: la campaña no lo promueve</span>` : ""}</h3>
      ${r.foto ? `<figure class="capitulo-foto"><img src="${r.foto.archivo_local}" alt="${r.foto.muestra}" loading="lazy"><figcaption>${credito(r.foto)}</figcaption></figure>` : ""}
      ${masFotos(r)}
      <p class="capitulo-que">${r.que_es}</p>
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
  campana: dibujarCampana,
};

// ---------- La campaña (Fase 8): "El sur tiene espacio" ----------
const TIPO_DATO = { dato: "Dato", derivado: "Derivado", supuesto: "Supuesto", hueco: "Sin dato" };
const ASPECTO = { ruido: "Ruido", limpieza: "Suciedad", precio: "Precio", multitudes: "Multitudes", servicio: "Servicio",
  comida: "Comida", naturaleza: "Naturaleza", cultura: "Cultura", calma: "Calma" };

function piezaAnuncio(m) {
  if (m.canal.startsWith("Google")) return `<div class="ad ad-google"><small>Patrocinado · catoxp.github.io/torre-del-caribe-unrc-2026</small>
    <h4>${m.titulos.join(" | ")}</h4><p>${m.descripcion}</p></div>`;
  if (m.canal.startsWith("Facebook")) return `<div class="ad ad-meta"><div class="ad-cabeza"><i></i><b>El sur tiene espacio</b><small>Publicidad</small></div>
    <p>${m.texto}</p><img src="${m.foto}" alt="" loading="lazy"><div class="ad-pie"><b>${m.titulo}</b><span>${m.idioma === "en" ? "Plan your trip" : "Planea tu viaje"}</span></div></div>`;
  return `<div class="ad ad-whats"><p>${m.texto}</p><small>Compartido por WhatsApp</small></div>`;
}

function dibujarCampana(caja, C) {
  const M = C.marca, T = C.texto;
  const maxRR = Math.max(...T.aspectos.map((a) => a.riesgo_relativo));
  caja.innerHTML = `
    <p class="rotulo revela">La campaña</p>
    <h2 class="h2 revela equilibrar" id="t-campana">${M.nombre}<em>.</em></h2>
    <p class="radar-bajada revela">${M.lema} <span class="lema-en" lang="en">${M.nombre_en}: ${M.lema_en}</span></p>
    <div class="camp-marca">
      <div class="revela"><small>Propuesta de valor</small><p>${M.propuesta_valor}</p></div>
      <div class="revela"><small>Posicionamiento</small><p>${M.posicionamiento}</p></div>
      <div class="revela"><small>Personalidad</small><ul>${M.personalidad.map((p) => `<li>${p}</li>`).join("")}</ul></div>
    </div>
    <h3 class="camp-sub revela">A quién le habla</h3>
    <div class="camp-personas">${C.personas.map((p) => `<article class="persona-camp revela"><h4>${p.nombre}</h4><p>${p.quien}</p>
      <dl>${p.atributos.map((a) => `<div><dt>${a.que} <span class="etq etq-${a.tipo}">${TIPO_DATO[a.tipo]}</span></dt><dd>${a.valor}<small>${a.fuente}</small></dd></div>`).join("")}</dl></article>`).join("")}</div>
    <h3 class="camp-sub revela">Lo que dicen 85,987 reseñas de Quintana Roo</h3>
    <p class="camp-nota revela">Cuántas veces más seguido es mala una reseña (1–2 estrellas) cuando habla de cada tema. Más de 1: aleja; menos de 1: protege. Ninguna reseña es de los cinco lugares: dicen qué molesta en los destinos llenos.</p>
    <ul class="camp-aspectos revela">${T.aspectos.map((a) => `<li><span>${ASPECTO[a.aspecto]}</span><i class="${a.riesgo_relativo > 1 ? "aleja" : "protege"}" style="--w:${(a.riesgo_relativo / maxRR) * 100}%"></i><b>${a.riesgo_relativo.toFixed(2)}×</b></li>`).join("")}</ul>
    <p class="camp-palabras revela"><b>Palabras de las reseñas de 5 estrellas:</b> ${T.palabras_cinco.join(", ")}.</p>
    <h3 class="camp-sub revela">Los anuncios</h3>
    <div class="camp-anuncios">${C.mensajes.map((m) => `<figure class="revela">${piezaAnuncio(m)}<figcaption><b>${C.personas.find((p) => p.clave === m.persona).nombre} · ${m.canal}</b>Respaldo: ${m.respaldo}</figcaption></figure>`).join("")}</div>
    <h3 class="camp-sub revela">Dónde y cuándo</h3>
    <div class="camp-medios">${C.medios.map((m) => `<div class="revela"><b>${m.pct ? `${m.pct} %` : "Sin costo"}</b><h4>${m.medio}</h4><p>${m.por_que}</p></div>`).join("")}</div>
    <ol class="camp-meses revela">${C.calendario.map((c) => `<li><b>${c.mes}</b><span>${c.pesos ? pesos(c.pesos) : "Sin anuncio (temporada alta)"}</span><small>${c.personas.map((p) => C.personas.find((x) => x.clave === p).nombre).join(" + ") || "—"}</small></li>`).join("")}</ol>
    <h3 class="camp-sub revela">Cómo se mide</h3>
    <div class="tabla-envoltura revela"><table class="tabla camp-kpis"><thead><tr><th>Indicador</th><th>Cómo se calcula</th><th>Meta</th><th>Fuente</th><th>Cada</th></tr></thead>
      <tbody>${C.kpis.map((k) => `<tr><td><b>${k.kpi}</b></td><td>${k.formula}</td><td>${k.meta}</td><td>${k.fuente}</td><td>${k.frecuencia}</td></tr>`).join("")}</tbody></table></div>
    <details class="como revela"><summary>¿Cómo lo sabemos?</summary><div class="como-dentro">
      <p>Cada rasgo de las viajeras dice si es un <b>dato</b> (medido por una fuente oficial), <b>derivado</b> (calculado con datos), <b>supuesto</b> (no hay dato y se declara) o <b>sin dato</b>. Ningún anuncio promete algo que no esté respaldado: "con espacio" sale de que Tulum recibió ${C.cifras.veces_ruta} veces más visitantes que la Ruta en 2025 (INAH). No se dan precios ni horas de viaje porque no hay dato oficial.</p>
      <p>Los temas de las reseñas se buscan con una lista de palabras a la vista (no con una caja negra); las reglas de asociación (Apriori) confirman que ruido con mal servicio, o suciedad con multitudes, hunden una reseña. Fuentes: INAH 2025, Unidad de Política Migratoria vía DataTur, Rest-Mex 2025, ENDUTIH 2025 (INEGI), WordStream 2025 y el modelo de la Fase 6.</p></div></details>`;
}

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
  caja.mostrarSemana = mostrar; caja.pararReproduccion = parar;
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
// Regla de temporada alta (decisión del equipo): el mes está 20 % o más arriba de un mes promedio, o tiene 10 % o más
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
  // Lo primero de la página: elegir lugar y mes en la portada (decisión del equipo, 01-oct-2026).
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
    <div class="elige-botones"><button type="button" class="boton boton-claro" id="portada-cotiza">Cotiza tu viaje
      <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 8h10m0 0-4-4m4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    <a class="boton-linea claro" href="#planea">Ver cómo va a estar</a></div>`;
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
  // Decisión 28: el botón principal lleva al cotizador con el lugar (si es del sur) y el mes elegidos
  $("portada-cotiza").addEventListener("click", () => { const L = P.lugares[plan.lugar]; irACotizar({ lugar: L.papel !== "referencia" ? L.clave : undefined, mes: plan.mes }); });
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

// Portada animada (decisión 25): las fotos comprobadas del lugar elegido pasan solas cada 7 s con un zoom lento (Ken
// Burns) y un fundido. Usa las mismas fotos de la galería, sin archivo de video. Con "reducir movimiento" se queda la
// primera foto fija, y se detiene mientras la portada no se ve (no gasta batería al leer el resto de la página).
const carrusel = { L: null, i: 0, reloj: null, visible: true, MAX: 6, CADA: 7000 };
function fotoPortada(L) {
  if (carrusel.L !== L) { carrusel.L = L; carrusel.i = 0; ponerFotoPortada(L, 0); }
  clearInterval(carrusel.reloj);
  const n = Math.min((L.fotos || []).length, carrusel.MAX);
  if (QUIETO || n < 2) return;
  carrusel.reloj = setInterval(() => {
    if (!carrusel.visible || document.hidden) return;
    carrusel.i = (carrusel.i + 1) % n;
    ponerFotoPortada(carrusel.L, carrusel.i);
  }, carrusel.CADA);
}
if ("IntersectionObserver" in window && $("inicio")) new IntersectionObserver(([e]) => { carrusel.visible = e.isIntersecting; }).observe($("inicio"));

function ponerFotoPortada(L, i) {
  // Fundido entre dos capas. Crédito siempre visible (licencia).
  const x = L.fotos && L.fotos[i];
  if (!x) return;
  const a = $("portada-foto"), b = $("portada-foto-b");
  const entra = a.classList.contains("oculta") ? a : b, sale = entra === a ? b : a;
  if (entra.dataset.src === x.archivo && !entra.classList.contains("oculta")) return;
  entra.style.backgroundImage = `url("${x.archivo}")`; entra.dataset.src = x.archivo;
  entra.classList.remove("oculta"); sale.classList.add("oculta");
  if (!QUIETO) {  // el zoom vuelve a empezar en la capa que entra; cada foto se acerca hacia un lado distinto
    entra.classList.remove("kb", "kb-izq"); void entra.offsetWidth;
    entra.classList.add("kb"); if (i % 2) entra.classList.add("kb-izq");
  }
  a.setAttribute("aria-label", `${x.muestra}, ${L.nombre}`);
  corazonPortada(x.archivo);
  $("credito-portada").innerHTML = `${esc(x.muestra)}. Foto: <span data-no-traducir>${esc(x.autor)}</span>, <a href="${esc(x.url_licencia || x.url_original)}" rel="license noopener noreferrer" target="_blank" data-no-traducir>${esc(x.licencia)}</a>, vía Wikimedia Commons.`;
}

function galeriaLugar(L) {
  const caja = $("lugar-fotos");
  if (!caja || !L.fotos) return;
  // Es el álbum completo del lugar, pero empieza por las fotos que no salen en otras secciones (reparto de fotos)
  const orden = L.fotos.map((f, i) => ({ f, i })).sort((a, b) => (USO.get(a.f.archivo) || 0) - (USO.get(b.f.archivo) || 0) || a.i - b.i).map((x) => x.f);
  caja.innerHTML = `<p class="lugar-fotos-titulo">Así se ve ${esc(conArticulo(L.nombre))}</p>
    <ul tabindex="0" aria-label="${esc(L.fotos.length)} fotos; se recorren de lado">${orden.map((x) => `<li><figure><img src="${esc(x.archivo)}" alt="${esc(x.muestra)}" loading="lazy" width="${x.ancho}" height="${x.alto}">
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

// Aviso fijo abajo de la pantalla (decisión del equipo, 01-oct-2026: "que sí se vea y no pase desapercibido en un scroll"). Sale
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

// Crédito corto de una foto de Commons (la licencia CC BY pide nombrar al autor y la licencia junto a la foto)
const creditoCorto = (f) => `Foto: <span data-no-traducir>${esc(f.autor)}</span>, <a href="${esc(f.url_licencia || f.url_original)}" rel="license noopener noreferrer" target="_blank" data-no-traducir>${esc(f.licencia)}</a>`;

function tarjetaNegocio(x) {
  const donde = x.km === null ? "" : x.otro ? `en ${esc(x.loc)}, a ${num(Math.round(x.km))} km` : x.km < 1 ? "en el centro" : `a ${x.km} km del centro`;
  // Foto propia solo si una foto comprobada es de ESE negocio o zona (decisión 25); las demás tarjetas, sin foto.
  const foto = x.foto ? `<figure class="negocio-foto"><img src="${esc(x.foto.archivo)}" alt="${esc(x.foto.muestra)}" loading="lazy"><figcaption>${creditoCorto(x.foto)}</figcaption></figure>` : "";
  return `<li class="negocio${x.otro ? " lejos" : ""}${x.foto ? " con-foto" : ""}">${foto}<b data-no-traducir>${esc(x.n)}</b><small>${esc(x.t)}${donde ? ` · ${donde}` : ""}</small>${enlacesGoogle(x)}</li>`;
}

// FINDING-002 (decisión 25): cada lista muestra los 3 lugares más cercanos y "Ver N más" despliega el resto. Antes, "Qué
// hacer" ocupaba 8 pantallas en escritorio y 10 en celular de tarjetas iguales. No se quita ningún negocio.
const VISIBLES = 3;
function listaCorta(lista) {
  const resto = lista.length - VISIBLES;
  return `<ul class="negocios${resto > 0 ? " corto" : ""}">${lista.map(tarjetaNegocio).join("")}</ul>`
    + (resto > 0 ? `<button type="button" class="ver-mas" aria-expanded="false" data-n="${resto}">Ver ${resto} más</button>` : "");
}
function conectarVerMas(caja) {
  caja.querySelectorAll(".ver-mas").forEach((b) => b.addEventListener("click", () => {
    const lista = b.previousElementSibling, abierta = lista.classList.toggle("corto") === false;
    b.setAttribute("aria-expanded", abierta);
    b.textContent = abierta ? "Ver menos" : `Ver ${b.dataset.n} más`;  // idiomas.js lo vuelve a traducir solo
  }));
}

// Reparto de fotos (20-oct-2026): con 146 fotos la página mostraba solo 45 distintas, porque cada sección tomaba las
// primeras de cada lugar (la del Templo del Búho salía 6 veces). repartir() entrega primero las menos usadas, en el orden
// de la curaduría. Las de "Vive el sur" (fijas en la vitrina) y la primera de la portada cuentan como ya usadas.
const USO = new Map();
function usar(archivo) { USO.set(archivo, (USO.get(archivo) || 0) + 1); }
function repartir(lista, n) {
  const elegidas = lista.map((f, i) => ({ f, i }))
    .sort((a, b) => (USO.get(a.f.archivo) || 0) - (USO.get(b.f.archivo) || 0) || a.i - b.i).slice(0, n).map((x) => x.f);
  elegidas.forEach((f) => usar(f.archivo));
  return elegidas;
}
function presembrarUso() {
  (JSON.stringify(D.vitrina || {}).match(/fotos\/lugares\/[a-z_0-9]+\.jpg/g) || []).forEach(usar);
  const L0 = carrusel.L; if (L0 && L0.fotos && L0.fotos[0]) usar(L0.fotos[0].archivo);
}

// Fotos de un momento del día (decisión 25). Si el lugar no tiene (la Ruta de tarde y de noche: las zonas cierran), se
// usan las de Chetumal, donde están los negocios de ese bloque, y la franja lo dice.
function fotosDelMomento(P, L, momento) {
  const propias = (L.fotos || []).filter((f) => f.momento === momento);
  if (propias.length || L.papel === "referencia") return { fotos: propias, de: null };
  const cerca = P.lugares.find((x) => x.clave === "Chetumal");
  return { fotos: cerca ? cerca.fotos.filter((f) => f.momento === momento) : [], de: cerca ? cerca.nombre : null };
}

function franjaMomento(P, L, momento) {
  const { fotos, de } = fotosDelMomento(P, L, momento);
  if (!fotos.length) return "";
  return `<div class="momento-fotos">${de ? `<p class="momento-fotos-de">En ${esc(de)}, donde están los lugares de este momento</p>` : ""}
    <ul class="n${Math.min(fotos.length, 4)}">${repartir(fotos, 4).map((f, i) => `<li style="--i:${i}"><figure><img src="${esc(f.archivo)}" alt="${esc(f.muestra)}" loading="lazy" width="${f.ancho}" height="${f.alto}">
      <figcaption>${esc(f.muestra)}<small>${creditoCorto(f)}</small></figcaption></figure></li>`).join("")}</ul></div>`;
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
  // Decisión 28: si en "Descubre" se eligió un interés, primero las experiencias de ese interés (si no hay, todas)
  const todas = delLugar.concat(delSur), filtradas = DESCUBRE.interes ? todas.filter((e) => (e.interes || []).includes(DESCUBRE.interes)) : todas;
  const experiencias = filtradas.length ? filtradas : todas;
  const rutasVer = clave ? V.rutas.filter((r) => r.lugares.includes(clave)) : V.rutas;
  const exp = experiencias.map((e, i) => `
    <article class="experiencia revela" style="--i:${i}">
      <div class="experiencia-foto"><img src="${esc(e.foto)}" alt="" loading="lazy"></div>
      <div class="experiencia-texto">
        ${e.lugar !== clave ? `<p class="experiencia-lugar">En el sur · ${esc((LUGARES().find((x) => x.clave === e.lugar) || { nombre: e.lugar }).nombre)}</p>` : e.referencia ? `<p class="experiencia-lugar ref">Referencia: la campaña no lo promueve</p>` : ""}
        <h3>${esc(e.titulo)}</h3>
        <p>${esc(e.texto)}</p>
        <p class="experiencia-dato">${esc(e.dato)} <small>Fuente: ${esc(e.fuente)}</small></p>
        <ul class="experiencia-lugares${e.negocios.length > VISIBLES ? " corto" : ""}">${e.negocios.map((x) => `<li><b data-no-traducir>${esc(x.n)}</b><small data-no-traducir>${esc(x.loc)}</small>${enlacesGoogle(x)}</li>`).join("")}</ul>
        ${e.negocios.length > VISIBLES ? `<button type="button" class="ver-mas" aria-expanded="false" data-n="${e.negocios.length - VISIBLES}">Ver ${e.negocios.length - VISIBLES} más</button>` : ""}
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
  conectarVerMas(caja);  // FINDING-003: 3 lugares por experiencia y "Ver N más", como en "Qué hacer"
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

// ---------- ¿Dónde hay espacio? El Radar para el viajero (decisión 25) ----------
// Solo los lugares del viajero (decisión 17): los tres del sur y, como referencia, Cancún y Playa del Carmen (Riviera
// Maya). Sin escala de 0 a 1 ni explicación del modelo: eso queda en datos.html#radar. El mes es el último publicado.
const ESPACIO_LUGARES = ["Chetumal", "Calderitas y Oxtankah", "Ruta de las pirámides", "Cancún", "Playa del Carmen"];
const ESPACIO_FOTO = { "Playa del Carmen": "Riviera Maya" };  // el lugar del viajero cuyas fotos son de Playa del Carmen
function espacio() {
  const R = D.radar, caja = $("espacio");
  if (!caja || !R) return;
  const todos = [...R.lugares, ...R.referencia];
  const lugares = ESPACIO_LUGARES.map((n) => todos.find((l) => l.nombre === n)).filter(Boolean);
  const fotoDe = (nombre) => {
    const v = LUGARES().find((x) => x.nombre === (ESPACIO_FOTO[nombre] || nombre));
    const L = v && D.pronostico && D.pronostico.lugares.find((x) => x.clave === v.clave);
    return L && L.fotos && L.fotos[0];
  };
  const tarjeta = (l, i) => {
    const f = fotoDe(l.nombre), ref = l.nombre === "Cancún" || l.nombre === "Playa del Carmen";
    return `<li class="espacio-lugar revela${ref ? " ref" : ""}" style="--i:${i}">
      ${f ? `<img src="${esc(f.archivo)}" alt="${esc(f.muestra)}" loading="lazy" width="${f.ancho}" height="${f.alto}">` : ""}
      <div class="espacio-texto">
        <h3 data-no-traducir>${esc(l.nombre)}</h3>
        ${ref ? `<p class="espacio-ref">Referencia: la campaña no lo promueve</p>` : ""}
        ${pildora(l.indice === null ? null : l.estado)}
        ${l.estado_siguiente_est ? `<p class="espacio-sig">En ${esc(R.mes_siguiente)}: <b>${esc(l.estado_siguiente_est)}</b> (estimado)</p>` : ""}
      </div></li>`;
  };
  const n = R.norte_semanal, riesgo = n && Math.max(...n.riesgo_saturarse["Cancún"]);
  caja.innerHTML = `
    <div class="espacio-dentro">
      <p class="rotulo claro revela">El Radar</p>
      <h2 class="h2 claro revela equilibrar" id="t-espacio">¿Dónde hay <em>espacio</em>?</h2>
      <p class="bajada-clara revela">Así estuvo cada lugar en ${esc(R.mes)} (el último mes con datos oficiales) y lo que esperamos para ${esc(R.mes_siguiente)}.</p>
      <ul class="espacio-lista">${lugares.map(tarjeta).join("")}</ul>
      ${n ? `<p class="espacio-norte revela">Cancún, semana del ${esc(n.semana)}: <b>${n.ocupacion_hoy_pct["Cancún"]} %</b> de los cuartos de hotel ocupados. Probabilidad de que se llene en las próximas 8 semanas: <b>${pct(riesgo)} o menos</b>.</p>` : ""}
      <p class="espacio-como"><a href="datos.html#radar">Cómo lo calculamos →</a></p>
    </div>`;
  caja.hidden = false;
}

// ---------- Video de la banda del cierre, "El viaje de tus sueños" (decisiones 25 y 29) ----------
// Se carga y reproduce solo cuando la banda está en pantalla (preload="none": no pesa al abrir la página) y se pausa al
// salir. Con "reducir movimiento" se queda el póster fijo.
function videoBanda() {
  const v = $("llamado-video");
  if (!v) return;
  if (QUIETO || !("IntersectionObserver" in window)) return;
  new IntersectionObserver(([e]) => {
    if (e.isIntersecting) { const p = v.play(); if (p && p.catch) p.catch(() => {}); } else v.pause();
  }, { threshold: 0.15 }).observe(v);
}

// ---------- Tu viaje soñado: corazones en las fotos (decisión 26) ----------
// Cada foto comprobada lleva un corazón. Lo que el visitante guarda vive SOLO en su navegador (localStorage): no se manda
// a ningún lado y no hay contadores de otras personas, porque la página es estática y esa cifra no existe (regla de oro
// 1: no se inventa). Con lo guardado, la página sugiere el lugar y el mes más tranquilo según el pronóstico (Fase 5).
// Alternativas descartadas por el equipo: contador en el servidor (solo funcionaría en localhost) y un servicio externo
// (rompe "sin llamadas a otros sitios").
const FAV = { clave: "favoritos", lista: [], fotos: new Map() };
const SVG_CORAZON = `<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 20.5s-7.5-4.6-9.3-9.2C1.4 7.9 3.6 4.5 7 4.5c2 0 3.5 1.1 5 3 1.5-1.9 3-3 5-3 3.4 0 5.6 3.4 4.3 6.8-1.8 4.6-9.3 9.2-9.3 9.2Z"/></svg>`;
const URL_PAGINA = "https://catoxp.github.io/torre-del-caribe-unrc-2026/";

function favoritos() {
  const P = D.pronostico;
  if (!P || !$("favoritos")) return;
  // Índice de las fotos que pueden guardarse: las de los lugares del viajero y su comida, con su lugar y su crédito.
  // Solo fotos del sur (auditoría del 20-oct-2026): Cancún y Riviera Maya son referencia y la campaña no los promueve,
  // así que sus fotos no llevan corazón (un favorito del norte mandaría al cotizador a un lugar que no vendemos).
  P.lugares.filter((L) => L.papel !== "referencia").forEach((L) => [...(L.fotos || []), ...(L.comida || [])].forEach((f) => FAV.fotos.set(f.archivo, { ...f, clave: L.clave, lugar: L.nombre })));
  try { FAV.lista = (JSON.parse(localStorage.getItem(FAV.clave)) || []).filter((a) => FAV.fotos.has(a)); } catch (e) { FAV.lista = []; }
  sembrarCorazones();
  // Las secciones se redibujan al elegir otro lugar: los corazones se vuelven a poner donde falten.
  let pendiente = false;
  new MutationObserver(() => { if (pendiente) return; pendiente = true; requestAnimationFrame(() => { pendiente = false; sembrarCorazones(); }); })
    .observe($("principal"), { childList: true, subtree: true });
  document.addEventListener("click", (e) => {
    const b = e.target.closest(".corazon");
    if (b && b.dataset.foto) { e.preventDefault(); alternarFavorito(b.dataset.foto, b); }
  });
  pintarFavoritos();
  conectarNube();
}

function sembrarCorazones() {
  document.querySelectorAll("#principal img").forEach((img) => {
    const src = img.getAttribute("src");
    // No llevan corazón: las copias de la tira de postales (aria-hidden), las miniaturas de tarjetas y las del
    // itinerario de Cotiza (son chicas, solo ilustran el plan y competirían con "Quiero cotizar este viaje").
    if (!FAV.fotos.has(src) || img.closest('[aria-hidden="true"], .negocio-foto, .parada-foto, .favoritos')) return;
    const caja = img.parentElement;
    if (caja.querySelector(":scope > .corazon")) return;
    caja.classList.add("con-corazon");
    caja.insertAdjacentHTML("beforeend", botonCorazon(src));
  });
  // Toda foto con corazón (también las de "Tu viaje soñado") se abre en grande: se puede enfocar con Tab.
  document.querySelectorAll("#principal .con-corazon > img:not([tabindex])").forEach((img) => {
    if (FAV.fotos.has(img.getAttribute("src"))) { img.tabIndex = 0; img.setAttribute("role", "button"); img.classList.add("ampliable"); }
  });
}

// ---------- Visor: las fotos con corazón se ven en grande (20-oct-2026) ----------
// Clic (o Enter) en una foto con corazón abre un <dialog> con la foto, el lugar, el crédito y el mismo corazón.
// Las flechas pasan a la foto anterior o siguiente de la misma sección. Solo fotos del catálogo del sur (FAV.fotos).
const VISOR = { lista: [], i: 0 };
function visorFotos() {
  const d = document.createElement("dialog");
  d.className = "visor"; d.id = "visor"; d.setAttribute("aria-label", "Foto en grande");
  d.innerHTML = `<figure class="visor-figura"><img id="visor-img" alt=""><figcaption>
      <p class="visor-lugar" id="visor-lugar"></p><p class="visor-muestra" id="visor-muestra"></p><p class="visor-credito" id="visor-credito"></p></figcaption></figure>
    <div class="visor-corazon" id="visor-corazon"></div>
    <button type="button" class="visor-boton visor-cerrar" id="visor-cerrar" aria-label="Cerrar"><svg viewBox="0 0 16 16" width="18" height="18" aria-hidden="true"><path d="M3.5 3.5l9 9m0-9-9 9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></button>
    <button type="button" class="visor-boton visor-ant" id="visor-ant" aria-label="Foto anterior"><svg viewBox="0 0 16 16" width="18" height="18" aria-hidden="true"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    <button type="button" class="visor-boton visor-sig" id="visor-sig" aria-label="Foto siguiente"><svg viewBox="0 0 16 16" width="18" height="18" aria-hidden="true"><path d="m6 3 5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    <p class="visor-cuenta" id="visor-cuenta" aria-hidden="true"></p>`;
  document.body.appendChild(d);
  const mostrar = (k) => {
    VISOR.i = (k + VISOR.lista.length) % VISOR.lista.length;
    const src = VISOR.lista[VISOR.i], f = FAV.fotos.get(src);
    const img = $("visor-img"); img.src = src; img.alt = f.muestra; img.width = f.ancho; img.height = f.alto;
    $("visor-lugar").textContent = f.lugar;
    $("visor-muestra").textContent = f.muestra;
    $("visor-credito").innerHTML = `Foto: <span data-no-traducir>${esc(f.autor)}</span>, <a href="${esc(f.url_licencia || f.url_original)}" rel="license noopener noreferrer" target="_blank" data-no-traducir>${esc(f.licencia)}</a>, vía Wikimedia Commons.`;
    $("visor-corazon").innerHTML = botonCorazon(src);
    $("visor-cuenta").textContent = `${VISOR.i + 1} / ${VISOR.lista.length}`;
    d.classList.toggle("solo-una", VISOR.lista.length < 2);
  };
  const abrir = (img) => {
    const zona = img.closest("section") || document.body;
    VISOR.lista = [...new Set([...zona.querySelectorAll(".con-corazon > img")].map((x) => x.getAttribute("src")).filter((s) => FAV.fotos.has(s)))];
    mostrar(Math.max(0, VISOR.lista.indexOf(img.getAttribute("src"))));
    d.showModal();
    $("visor-cerrar").focus();  // el foco entra al visor: Esc, flechas y Tab funcionan ahí
  };
  // Toda la foto abre el visor (en el mosaico el pie va encima de la imagen), salvo el corazón y los enlaces.
  document.addEventListener("click", (e) => {
    const fig = e.target.closest("#principal .con-corazon"), img = fig && fig.querySelector(":scope > img.ampliable");
    if (img && !e.target.closest(".corazon, a, button")) { e.preventDefault(); abrir(img); }
  });
  document.addEventListener("keydown", (e) => {
    const img = e.target.closest && e.target.closest(".con-corazon > img");
    if (img && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); abrir(img); }
  });
  $("visor-cerrar").addEventListener("click", () => d.close());
  $("visor-ant").addEventListener("click", () => mostrar(VISOR.i - 1));
  $("visor-sig").addEventListener("click", () => mostrar(VISOR.i + 1));
  d.addEventListener("click", (e) => { if (e.target === d) d.close(); });  // tocar fuera de la foto cierra
  document.addEventListener("keydown", (e) => {
    if (!d.open) return;
    if (e.key === "ArrowLeft") { e.preventDefault(); mostrar(VISOR.i - 1); }
    if (e.key === "ArrowRight") { e.preventDefault(); mostrar(VISOR.i + 1); }
  });
  // Deslizar con el dedo en el celular
  let x0 = null;
  d.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  d.addEventListener("touchend", (e) => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(dx) > 50) mostrar(VISOR.i + (dx < 0 ? 1 : -1)); });
}

const botonCorazon = (src) => `<button type="button" class="corazon${NUBE.lista && cuentaDe(src) > 0 ? " con-cuenta" : ""}" data-foto="${esc(src)}" aria-pressed="${FAV.lista.includes(src)}" aria-label="Me gusta esta foto">${SVG_CORAZON}${cuentaHTML(src)}</button>`;

// ---------- Contador global de corazones con Firebase (decisión 27) ----------
// Solo si frontend/firebase-config.js trae configuración. Cada visitante entra con una cuenta ANÓNIMA (sin datos
// personales) y suma 1 por foto; las reglas de firebase/firestore.rules (torre.campana.nube) impiden inflar el número.
// Si Firebase no carga o no responde, la página sigue igual: favoritos en el navegador y sin números.
const NUBE = { lista: false, cuentas: new Map(), fs: null, db: null, uid: null };
const SDK_FIREBASE = "https://www.gstatic.com/firebasejs/12.6.0";  // 12.x trae firebase-ai (Gemini, decisión 28)
const idFoto = (archivo) => archivo.split("/").pop().toLowerCase().replace(/\.[a-z]+$/, "");  // igual que nube.py
const cuentaDe = (src) => NUBE.cuentas.get(idFoto(src)) || 0;
const cuentaHTML = (src) => (NUBE.lista && cuentaDe(src) > 0 ? `<span class="corazon-n">${num(cuentaDe(src))}</span>` : "");

async function conectarNube() {
  const cfg = window.TORRE_FIREBASE;
  if (!cfg || !cfg.projectId || !FAV.fotos.size) return;
  try {
    const [appMod, fs, authMod] = await Promise.all([import(`${SDK_FIREBASE}/firebase-app.js`),
      import(`${SDK_FIREBASE}/firebase-firestore.js`), import(`${SDK_FIREBASE}/firebase-auth.js`)]);
    const app = appMod.initializeApp(cfg), db = fs.getFirestore(app), auth = authMod.getAuth(app);
    if (cfg.emulador) {  // solo para las pruebas locales con el emulador de Firebase (nunca en la página publicada)
      fs.connectFirestoreEmulator(db, "127.0.0.1", 8080);
      authMod.connectAuthEmulator(auth, "http://127.0.0.1:9099", { disableWarnings: true });
    }
    NUBE.uid = (await authMod.signInAnonymously(auth)).user.uid;
    // Se escuchan EN VIVO solo las fotos de la página: si otra persona pone un corazón, la cifra cambia aquí también
    // (la prueba con dos navegadores mostró que leer una sola vez dejaba cifras viejas). "in" acepta hasta 30 ids por
    // consulta, así que van en tandas de 30; la página está lista cuando llega la primera respuesta de cada tanda.
    const ids = [...new Set([...FAV.fotos.keys()].map(idFoto))], tandas = [];
    Object.assign(NUBE, { fs, db, app, cfg });  // app: la usa también Gemini (armarConIA)
    let pendiente = false;
    const repintar = () => { if (pendiente) return; pendiente = true; requestAnimationFrame(() => { pendiente = false; pintarCuentas(); if (document.querySelector("#favoritos .fav-sub") || !document.querySelector(".fav-vacio")) pintarFavoritos(); }); };
    for (let k = 0; k < ids.length; k += 30) tandas.push(new Promise((listo, falla) => {
      fs.onSnapshot(fs.query(fs.collection(db, "fotos"), fs.where(fs.documentId(), "in", ids.slice(k, k + 30))), (s) => {
        s.docChanges().forEach((c) => NUBE.cuentas.set(c.doc.id, c.type === "removed" ? 0 : Number(c.doc.data().corazones) || 0));
        listo();
        if (NUBE.lista) repintar();
      }, falla);
    }));
    await Promise.all(tandas);
    NUBE.lista = true;
    pintarCuentas();
    pintarFavoritos();
    pruebaPortada();
  } catch (e) { NUBE.lista = false; }  // sin conexión, bloqueado o sin configurar: la página sigue sin números
}

// App Check (decisión 28): Gemini solo responde a peticiones que traen un comprobante de que vienen de nuestra página,
// para que nadie gaste la cuota del equipo desde fuera. El comprobante lo da Fraud Defense de Google, antes reCAPTCHA
// Enterprise (clave pública del sitio en firebase-config.js, campo appCheck). Se carga solo cuando el visitante empieza a usar "Cotiza tu viaje", así el resto
// de los visitantes no descarga reCAPTCHA. En localhost se usa el modo de depuración de Firebase: la consola del
// navegador imprime un token que el equipo registra en Firebase → App Check → Manage debug tokens.
let appCheckListo = null;
function prepararAppCheck() {
  const cfg = NUBE.cfg;
  if (!NUBE.app || !cfg || !cfg.appCheck) return Promise.resolve(false);
  if (!appCheckListo) {
    if (/^(localhost|127\.0\.0\.1)$/.test(location.hostname) && self.FIREBASE_APPCHECK_DEBUG_TOKEN === undefined) self.FIREBASE_APPCHECK_DEBUG_TOKEN = true;
    appCheckListo = import(`${SDK_FIREBASE}/firebase-app-check.js`)
      .then((m) => {
        // Fraud Defense (antes reCAPTCHA Enterprise) es el recomendado; reCAPTCHA v3 clásico queda como respaldo.
        const proveedor = cfg.appCheckClasico ? new m.ReCaptchaV3Provider(cfg.appCheck) : new m.ReCaptchaEnterpriseProvider(cfg.appCheck);
        m.initializeAppCheck(NUBE.app, { provider: proveedor, isTokenAutoRefreshEnabled: true });
        return true;
      })
      .catch(() => false);  // si reCAPTCHA no carga, Gemini responderá 401 y entra el armador por reglas
  }
  return appCheckListo;
}

function pintarCuentas() {
  document.querySelectorAll(".corazon[data-foto]").forEach((b) => {
    const n = cuentaDe(b.dataset.foto);
    let s = b.querySelector(".corazon-n");
    if (NUBE.lista && n > 0) { if (!s) { s = document.createElement("span"); s.className = "corazon-n"; b.appendChild(s); } s.textContent = num(n); }
    else if (s) s.remove();
    b.classList.toggle("con-cuenta", NUBE.lista && n > 0);
  });
}

// Voto en la nube: el voto del visitante y el +1 (o −1) van en un mismo lote; las reglas rechazan cualquier otra cosa.
async function votarNube(src, guardada) {
  if (!NUBE.lista) return;
  const { fs, db } = NUBE, id = idFoto(src), antes = cuentaDe(src);
  NUBE.cuentas.set(id, Math.max(0, antes + (guardada ? 1 : -1)));  // se ve al instante
  pintarCuentas();
  try {
    const lote = fs.writeBatch(db), voto = fs.doc(db, "votos", `${id}_${NUBE.uid}`), foto = fs.doc(db, "fotos", id);
    if (guardada) { lote.set(voto, { foto: id, uid: NUBE.uid }); lote.set(foto, { corazones: fs.increment(1) }, { merge: true }); }
    else { lote.delete(voto); lote.set(foto, { corazones: fs.increment(-1) }, { merge: true }); }
    await lote.commit();
    if (document.querySelector(".fav-top") || guardada) pintarFavoritos();  // "N personas la guardaron" al día
  } catch (e) {  // ya había votado (o nunca votó) desde este navegador: se regresa la cifra a como estaba
    NUBE.cuentas.set(id, antes);
    pintarCuentas();
  }
}

function alternarFavorito(src, boton) {
  const i = FAV.lista.indexOf(src);
  if (i >= 0) FAV.lista.splice(i, 1); else FAV.lista.unshift(src);
  try { localStorage.setItem(FAV.clave, JSON.stringify(FAV.lista)); } catch (e) { /* sin almacenamiento: dura esta visita */ }
  const guardada = i < 0;
  document.querySelectorAll(".corazon").forEach((b) => { if (b.dataset.foto === src) b.setAttribute("aria-pressed", guardada); });
  if (boton && guardada && !QUIETO) { boton.classList.remove("late"); void boton.offsetWidth; boton.classList.add("late"); }
  pintarFavoritos(guardada);
  votarNube(src, guardada);
}

// Las 4 fotos con más corazones de todos los visitantes (solo cifras reales de Firebase; si no hay, no aparece).
function favoritasDeTodos() {
  if (!NUBE.lista) return "";
  const top = [...FAV.fotos.keys()].filter((a) => cuentaDe(a) > 0)
    .sort((a, b) => cuentaDe(b) - cuentaDe(a)).filter((a, k, xs) => xs.findIndex((x) => idFoto(x) === idFoto(a)) === k).slice(0, 4);
  if (!top.length) return "";
  return `<h3 class="fav-sub">Las favoritas de los viajeros</h3><ul class="fav-fotos fav-top">${top.map((a, k) => { const f = FAV.fotos.get(a), n = cuentaDe(a);
    return `<li style="--i:${k}"><figure class="con-corazon"><img src="${esc(a)}" alt="${esc(f.muestra)}" loading="lazy" width="${f.ancho}" height="${f.alto}">${botonCorazon(a)}
      <figcaption>${esc(f.muestra)}<small>${n === 1 ? `${num(n)} persona la guardó` : `${num(n)} personas la guardaron`}</small></figcaption></figure></li>`; }).join("")}</ul>`;
}

// El corazón de la portada sigue a la foto que está pasando (carrusel de la portada).
function corazonPortada(src) {
  const b = $("corazon-portada");
  if (!b || !FAV.fotos.size) return;
  if (!FAV.fotos.has(src)) { b.hidden = true; return; }  // foto de Cancún o Riviera Maya (referencia): sin corazón
  b.innerHTML = SVG_CORAZON + cuentaHTML(src); b.dataset.foto = src; b.hidden = false; b.classList.toggle("con-cuenta", cuentaDe(src) > 0);
  b.setAttribute("aria-label", "Me gusta esta foto");
  b.setAttribute("aria-pressed", FAV.lista.includes(src));
}

function pintarFavoritos(recienGuardada = false) {
  const caja = $("favoritos"), P = D.pronostico, n = FAV.lista.length;
  $("fav-n").textContent = n;
  const cont = $("fav-contador");
  cont.classList.toggle("tiene", n > 0);
  if (recienGuardada && !QUIETO) { cont.classList.remove("brinca"); void cont.offsetWidth; cont.classList.add("brinca"); }
  const cabeza = `<p class="rotulo revela visible">Tu viaje soñado</p>
    <h2 class="h2 revela visible equilibrar" id="t-favoritos">Guarda lo que te <em>enamore</em>.</h2>`;
  if (!n) {
    caja.innerHTML = `<div class="favoritos-dentro">${cabeza}
      <div class="fav-vacio"><span class="fav-vacio-corazon" aria-hidden="true">${SVG_CORAZON}</span>
        <p><b>Todavía no guardas ninguna foto.</b> Toca el corazón en las fotos que te gusten: aquí se arma tu viaje, con el lugar que más te gustó y el mes más tranquilo para ir.</p>
        <a class="boton boton-tinta" href="#planea">Ver las fotos</a></div>${favoritasDeTodos()}</div>`;
    return;
  }
  // El lugar con más fotos guardadas y su primer mes tranquilo del calendario (si no hay, el primero que no sea temporada alta).
  const cuenta = {};
  FAV.lista.forEach((a) => { const c = FAV.fotos.get(a).clave; cuenta[c] = (cuenta[c] || 0) + 1; });
  const clave = Object.keys(cuenta).sort((a, b) => cuenta[b] - cuenta[a] || FAV.lista.findIndex((x) => FAV.fotos.get(x).clave === a) - FAV.lista.findIndex((x) => FAV.fotos.get(x).clave === b))[0];
  const li = P.lugares.findIndex((L) => L.clave === clave), L = P.lugares[li];
  let mi = L.calendario.findIndex((c) => c.nivel === "tranquila");
  const tranquilo = mi >= 0;
  if (!tranquilo) mi = Math.max(0, L.calendario.findIndex((c) => c.nivel !== "alta"));
  const mes = mesDe(P.meses[mi]).largo;
  const ref = L.papel === "referencia" ? `<p><span class="etiqueta-ref">Referencia: la campaña no lo promueve</span></p>` : "";
  caja.innerHTML = `<div class="favoritos-dentro">${cabeza}
    <div class="fav-resumen">
      <p class="fav-tu-lugar">Tu lugar: <b>${esc(L.nombre)}</b></p>${ref}
      <p class="fav-cuenta">${cuenta[clave]} de tus ${n} fotos guardadas son de ahí.</p>
      <p class="fav-mes">${tranquilo ? "Mes más tranquilo para ir" : "Primer mes sin temporada alta"}: <b>${esc(mes)}</b></p>
      <div class="fav-botones">
        <button type="button" class="boton boton-claro" id="fav-cotizar">Cotizar con mis favoritas</button>
        <button type="button" class="boton-linea" id="fav-planear">Ver cómo va a estar</button>
        <button type="button" class="boton-linea" id="fav-compartir">Compartir mi viaje</button>
        <button type="button" class="fav-borrar" id="fav-borrar">Borrar todo</button>
      </div>
      <p class="fav-nota">${NUBE.lista ? "Tus fotos se guardan en este navegador. Cada corazón se suma, sin ningún dato tuyo, al contador de la foto (Firebase, de Google)." : "Tus fotos se guardan solo en este navegador; no se envían a ningún lado."}</p>
    </div>
    ${favoritasDeTodos()}
    <ul class="fav-fotos">${FAV.lista.map((a, k) => { const f = FAV.fotos.get(a);
      return `<li style="--i:${k}"><figure class="con-corazon"><img src="${esc(a)}" alt="${esc(f.muestra)}" loading="lazy" width="${f.ancho}" height="${f.alto}">${botonCorazon(a)}
        <figcaption>${esc(f.muestra)}<small>Foto: <span data-no-traducir>${esc(f.autor)}</span>, <span data-no-traducir>${esc(f.licencia)}</span></small></figcaption></figure></li>`; }).join("")}</ul></div>`;
  // Decisión 28: las fotos guardadas dicen qué le gusta al viajero; van al cotizador como lugar e intereses
  $("fav-cotizar").addEventListener("click", () => {
    const cuentaInt = {};
    FAV.lista.forEach((a) => (FAV.fotos.get(a).interes || []).forEach((k) => { cuentaInt[k] = (cuentaInt[k] || 0) + 1; }));
    const intereses = Object.keys(cuentaInt).sort((a, b) => cuentaInt[b] - cuentaInt[a]).slice(0, 3);
    irACotizar({ lugar: L.papel !== "referencia" ? L.clave : undefined, mes: mi, intereses });
  });
  $("fav-planear").addEventListener("click", () => {
    plan.lugar = li; plan.mes = mi; pintarPlan(P); dibujarQueHacer(P);
    $("planea").scrollIntoView({ behavior: QUIETO ? "auto" : "smooth" });
  });
  $("fav-compartir").addEventListener("click", () => {
    const lugares = [...new Set(FAV.lista.map((a) => FAV.fotos.get(a).lugar))].join(", ");
    const texto = `Mi viaje soñado al sur de Quintana Roo: ${lugares}. Mejor mes para ${L.nombre}: ${mes}.`;
    if (navigator.share) navigator.share({ title: "Torre del Caribe", text: texto, url: URL_PAGINA }).catch(() => {});
    else window.open(`https://wa.me/?text=${encodeURIComponent(`${texto} ${URL_PAGINA}`)}`, "_blank", "noopener");
  });
  $("fav-borrar").addEventListener("click", () => {
    FAV.lista = [];
    try { localStorage.removeItem(FAV.clave); } catch (e) { /* nada */ }
    document.querySelectorAll(".corazon").forEach((b) => b.setAttribute("aria-pressed", "false"));
    pintarFavoritos();
  });
}

// =====================================================================================================================
// Decisión 28 (19-oct-2026): la página vende el servicio de planear el viaje. Secciones nuevas: Por qué el sur, Descubre,
// Cotiza tu viaje, Consejos para viajar y Cómo llegar. Todo sale de pagina.js (datos oficiales del proyecto); el precio, de
// cotizar.js; el plan, de Gemini (Firebase AI Logic) o, si no responde, de reglas. Nada se inventa.
// =====================================================================================================================
const INTERES = { cultura: "Cultura maya", mar: "Mar y bahía", naturaleza: "Naturaleza", sabores: "Sabores", noche: "Noche" };
const DESCUBRE = { interes: null };
const lugaresSur = () => (D.pronostico ? D.pronostico.lugares.filter((L) => L.papel !== "referencia") : []);

// ---------- Por qué el sur: tres cifras grandes, cada una con su fuente ----------
// ---------- Historia (decisión 31): línea de tiempo de los 5 lugares, cada hecho con su fuente oficial ----------
// Sale de docs/historia/linea_tiempo.csv (INAH, Gobierno de Quintana Roo, INAFED, FONATUR). Se filtra por lugar; un
// separador marca el paso de la época maya a la moderna. La línea se dibuja al bajar (CSS, con "reducir movimiento" no).
const COLOR_HITO = { "Chetumal": "rosa", "Bahía Calderitas–Oxtankah": "turquesa", "Ruta arqueológica del sur": "amarillo",
  "Cancún": "anil", "Riviera Maya": "anil", "Quintana Roo": "verde" };
function historia() {
  const caja = $("historia"), H = D.historia;
  if (!caja || !H || !H.length) return;
  const nombre = (c) => (LUGARES().find((x) => x.clave === c) || { nombre: c }).nombre;
  const ref = (c) => c === "Cancún" || c === "Riviera Maya";
  const lugares = [...new Set(H.map((h) => h.lugar))];
  const anios = Math.floor((new Date().getFullYear() - Math.min(...H.map((h) => h.orden))) / 100) * 100;
  const hecho = (h, i) => `<li class="hito revela c-${COLOR_HITO[h.lugar] || "rosa"}" data-lugar="${esc(h.lugar)}" style="--i:${i % 4}">
      <p class="hito-cuando">${esc(h.cuando)}</p>
      <div class="hito-cuerpo"><p class="hito-lugar"><span>${esc(nombre(h.lugar))}</span>${ref(h.lugar) ? ` <span class="etiqueta-ref">Referencia</span>` : ""}</p>
        <p class="hito-hecho">${esc(h.hecho)}</p>
        <a class="hito-fuente" href="${esc(h.url)}" target="_blank" rel="noopener noreferrer">Fuente: ${esc(h.fuente)}</a></div></li>`;
  const moderna = H.findIndex((h) => h.orden >= 1500);
  const items = H.map((h, i) => (i === 0 ? `<li class="hito-era revela"><span>Época maya</span></li>` : "") +
    (i === moderna ? `<li class="hito-era revela"><span>Época moderna</span></li>` : "") + hecho(h, i)).join("");
  caja.innerHTML = `<div class="historia-dentro">
    <header class="cabeza-doble"><div><p class="rotulo claro revela">Historia</p>
      <h2 class="h2 claro revela" id="t-historia">Más de ${num(anios)} años <em>de historia</em>.</h2></div>
      <p class="cabeza-bajada revela">De las primeras ciudades mayas a la fundación de Chetumal y el nacimiento del estado. Cada fecha sale de una fuente oficial.</p></header>
    <div class="historia-filtros revela" role="group" aria-label="Filtrar por lugar">
      <button type="button" class="chip-interes" data-l="" aria-pressed="true">Todos</button>
      ${lugares.map((l) => `<button type="button" class="chip-interes" data-l="${esc(l)}" aria-pressed="false">${esc(nombre(l))}</button>`).join("")}</div>
    <ol class="linea">${items}</ol>
  </div>`;
  caja.querySelectorAll(".historia-filtros .chip-interes").forEach((b) => b.addEventListener("click", () => {
    const l = b.dataset.l;
    caja.querySelectorAll(".historia-filtros .chip-interes").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    caja.querySelectorAll(".hito").forEach((h) => { h.hidden = !!l && h.dataset.lugar !== l; });
    caja.querySelectorAll(".hito-era").forEach((e) => { e.hidden = !!l; });
  }));
  caja.hidden = false;
}

// ---------- Naturaleza del sur (decisión 31): 12 especies con observación verificada de iNaturalist ----------
function fauna() {
  const caja = $("fauna"), F = D.fauna;
  if (!caja || !F || !F.length) return;
  caja.innerHTML = `<div class="fauna-dentro">
    <header class="cabeza-doble"><div><p class="rotulo revela">Naturaleza del sur</p>
      <h2 class="h2 revela" id="t-fauna">La selva también <em>te recibe</em>.</h2></div>
      <p class="cabeza-bajada revela">Monos, tucanes, garzas e iguanas que se han visto en Chetumal, Kohunlich y Dzibanché. Cada foto es una observación confirmada por la comunidad de iNaturalist.</p></header>
    <ul class="fauna-rejilla">${F.map((f, i) => `<li class="especie revela" style="--i:${i % 6}"><figure>
      <img src="${esc(f.archivo)}" alt="${esc(f.comun)}" loading="lazy" width="${f.ancho}" height="${f.alto}">
      <figcaption><b>${esc(f.comun)}</b><i data-no-traducir>${esc(f.especie)}</i>
        <small>Visto en <span data-no-traducir>${esc(f.donde)}</span> · Foto: <a href="${esc(f.url_original)}" target="_blank" rel="noopener noreferrer" data-no-traducir>${esc(f.autor)}</a>, <a href="${esc(f.url_licencia)}" rel="license noopener noreferrer" target="_blank" data-no-traducir>${esc(f.licencia)}</a>, vía iNaturalist.</small></figcaption></figure></li>`).join("")}</ul>
  </div>`;
  caja.hidden = false;
}

// ---------- Un día en el sur (decisión 29) ----------
// Video de 26 s en bucle (video/un-dia-sur/, solo fotos comprobadas). Encima, la frase de la parte del día, el lugar y el
// crédito de la foto que se está viendo, con los tiempos del mismo guion del video (D.video_dia). Se carga y reproduce
// solo con la sección en pantalla; en pantallas verticales usa la versión 1080×1350. Con "reducir movimiento" queda la
// imagen fija y se ven las tres frases.
function unDia() {
  const caja = $("un-dia"), V = D.video_dia, v = $("un-dia-video");
  if (!caja || !V || !v) return;
  const vertical = window.matchMedia("(max-aspect-ratio: 4/5), (max-width: 640px)").matches;
  const base = `video/un-dia-sur${vertical ? "-vertical" : ""}`;
  v.poster = `${base}.jpg`;
  v.innerHTML = `<source src="${base}.webm" type="video/webm"><source src="${base}.mp4" type="video/mp4">`;
  caja.hidden = false;
  const partes = [...caja.querySelectorAll(".un-dia-parte")], tramos = [...caja.querySelectorAll(".un-dia-barra li")];
  const lugar = $("un-dia-lugar"), credito = $("un-dia-credito");
  let toma = -1, parte = "";
  const ponerToma = (k) => {
    if (k === toma) return;
    toma = k; const x = V.tomas[k];
    lugar.textContent = x.muestra;
    credito.innerHTML = `Foto: <span data-no-traducir>${esc(x.autor)}</span>, <span data-no-traducir>${esc(x.licencia)}</span>, vía Wikimedia Commons.`;
    lugar.classList.remove("entra"); void lugar.offsetWidth; lugar.classList.add("entra");
  };
  const pintar = (s) => {
    const p = V.partes.find((x) => s >= x.desde && s < x.hasta) || V.partes[0];
    if (p.clave !== parte) {
      parte = p.clave;
      partes.forEach((el) => el.classList.toggle("activa", el.dataset.parte === parte));
    }
    tramos.forEach((li) => { const x = V.partes.find((q) => q.clave === li.dataset.parte);
      li.style.setProperty("--lleno", Math.max(0, Math.min(1, (s - x.desde) / (x.hasta - x.desde)))); });
    // El lugar cambia a la mitad del fundido de cada toma, cuando la foto nueva ya domina el cuadro
    let k = 0; V.tomas.forEach((x, i) => { if (s >= x.entra + (x.fundido || 0) / 2) k = i; });
    ponerToma(s >= V.partes[V.partes.length - 1].hasta ? 0 : k);
  };
  pintar(0);
  if (QUIETO || !("IntersectionObserver" in window)) { caja.classList.add("quieto"); return; }
  // Mientras se reproduce, la barra se llena cuadro a cuadro; timeupdate y seeked cubren pausas, saltos y el bucle.
  let pidiendo = false;
  const ciclo = () => { pintar(v.currentTime); if (!v.paused && !v.ended) requestAnimationFrame(ciclo); else pidiendo = false; };
  const arrancar = () => { if (!pidiendo) { pidiendo = true; requestAnimationFrame(ciclo); } };
  ["play", "playing", "timeupdate", "seeked"].forEach((ev) => v.addEventListener(ev, () => { pintar(v.currentTime); arrancar(); }));
  new IntersectionObserver(([e]) => {
    if (e.isIntersecting) { const r = v.play(); if (r && r.catch) r.catch(() => caja.classList.add("quieto")); } else v.pause();
  }, { threshold: 0.25 }).observe(caja);
}

// ---------- Descubre lo que te gusta: mosaico de fotos del sur filtrado por interés ----------
function descubre() {
  const caja = $("descubre"), sur = lugaresSur();
  if (!caja || !sur.length) return;
  const fotos = sur.flatMap((L) => L.fotos.map((f) => ({ ...f, lugar: L.nombre, clave: L.clave })));
  const cuenta = (k) => fotos.filter((f) => f.interes.includes(k)).length;
  const pintar = () => {
    const k = DESCUBRE.interes, vis = (k ? fotos.filter((f) => f.interes.includes(k)) : fotos)
      // intercalar lugares para que el mosaico no sea de un solo sitio
      .sort((a, b) => (a.archivo.match(/_(\d+)\./) || [0, 0])[1] - (b.archivo.match(/_(\d+)\./) || [0, 0])[1]);
    const vis2 = repartir(vis, 11);
    $("descubre-mosaico").innerHTML = vis2.map((f, i) => `<li class="mosaico-${i}" style="--i:${i}"><figure>
      <img src="${esc(f.archivo)}" alt="${esc(f.muestra)}" loading="lazy" width="${f.ancho}" height="${f.alto}">
      <figcaption><b>${esc(f.muestra)}</b><small>${esc(f.lugar)} · Foto: <span data-no-traducir>${esc(f.autor)}</span>, <span data-no-traducir>${esc(f.licencia)}</span></small></figcaption></figure></li>`).join("");
    caja.querySelectorAll(".chip-interes").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.k === (k || ""))));
  };
  caja.innerHTML = `<div class="descubre-dentro">
    <header class="cabeza-doble"><div><p class="rotulo revela">Descubre</p>
    <h2 class="h2 revela" id="t-descubre">El sur, a tu <em>manera</em>.</h2></div>
    <p class="cabeza-bajada descubre-bajada revela">Elige lo que te mueve. Todas las fotos se tomaron en estos lugares: guarda las que te enamoren.</p></header>
    <div class="chips revela" role="group" aria-label="Intereses">
      <button type="button" class="chip-interes" data-k="" aria-pressed="true">Todo <small>${fotos.length}</small></button>
      ${Object.entries(INTERES).map(([k, n]) => `<button type="button" class="chip-interes" data-k="${k}" aria-pressed="false">${n} <small>${cuenta(k)}</small></button>`).join("")}
    </div>
    <ul class="mosaico" id="descubre-mosaico"></ul>
    <button type="button" class="boton boton-tinta descubre-cotiza revela" id="descubre-cotiza">Cotizar un viaje así
      <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 8h10m0 0-4-4m4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
  </div>`;
  caja.querySelectorAll(".chip-interes").forEach((b) => b.addEventListener("click", () => {
    DESCUBRE.interes = b.dataset.k || null;
    const cambiar = () => { pintar(); vive(); };
    if (!QUIETO && document.startViewTransition) document.startViewTransition(cambiar); else cambiar();
  }));
  $("descubre-cotiza").addEventListener("click", () => irACotizar({ intereses: DESCUBRE.interes ? [DESCUBRE.interes] : [] }));
  pintar();
  caja.hidden = false;
}

// ---------- Consejos para viajar (20-oct-2026; sustituye al calendario "Cuándo ir") ----------
// Cinco consejos y una tarjeta para cotizar. Cada uno sale de un dato de pagina.js y dice su fuente: los meses
// tranquilos (pronóstico del proyecto), la lluvia y el calor (normales 1991–2020 del SMN, decisión 32), las tormentas (NOAA, HURDAT2) y
// las distancias (SITUR-Q e INEGI). Se usan los próximos 12 meses: así cada mes del año aparece una sola vez.
function consejos() {
  const caja = $("consejos"), P = D.pronostico, sur = lugaresSur(), LL = D.llegar;
  if (!caja || !P || !sur.length) return;
  const doce = P.meses.slice(0, 12).map((ym, i) => ({ i, f: mesDe(ym) }));
  const deLugar = (clave) => sur.find((L) => L.clave === clave) || sur[0];
  const che = deLugar("Chetumal"), ruta = deLugar("Ruta arqueológica del sur");
  const chip = (m, clase, extra = "") => `<li class="mes-chip ${clase}">${esc(MESES[m.f.m - 1])}${extra}</li>`;
  const chips = (lista, clase, extra) => `<ul class="mes-chips">${lista.map((m) => chip(m, clase, extra ? extra(m) : "")).join("")}</ul>`;
  const conAnio = (m) => ` <small>${m.f.a}</small>`;  // meses del pronóstico: el año distingue 2026 de 2027
  // 1. Meses tranquilos por lugar
  const tranquilos = sur.map((L) => ({ L, meses: doce.filter((m) => L.calendario[m.i].nivel === "tranquila") }));
  // 2. Lluvia en Chetumal: secos (< 60 mm) y lluviosos (≥ 150 mm). Los meses del clima normal se ordenan como una
  // temporada seguida: en el calendario y empezando después del hueco más grande (secos: dic, ene… abr; no ene… abr, dic).
  const enOrden = (xs) => {
    const s = [...xs].sort((a, b) => a.f.m - b.f.m);
    if (s.length < 2) return s;
    let corte = 0, hueco = -1;
    s.forEach((m, k) => { const sig = s[(k + 1) % s.length], h = (sig.f.m - m.f.m + 12) % 12 || 12; if (h > hueco) { hueco = h; corte = (k + 1) % s.length; } });
    return [...s.slice(corte), ...s.slice(0, corte)];
  };
  const secos = enOrden(doce.filter((m) => che.calendario[m.i].lluvia < 60));
  const lluviosos = enOrden(doce.filter((m) => che.calendario[m.i].lluvia >= 150));
  // 3. Calor en la Ruta: meses con máxima normal de 33 °C o más (con la estación del SMN, 32 °C se pasa 7 meses del año
  // y ya no distingue nada; 33 °C deja los cuatro más calurosos)
  const calor = enOrden(doce.filter((m) => ruta.calendario[m.i].temp >= 33));
  const tMax = Math.round(Math.max(...doce.map((m) => ruta.calendario[m.i].temp)));
  // 4. Tormentas: meses con 10 % o más de probabilidad
  const tormentas = enOrden(doce.filter((m) => che.calendario[m.i].tormenta >= 0.1));
  // 5. Distancias desde la estación y el aeropuerto de Chetumal
  const km = (clave) => { const x = LL && LL.lugares.find((l) => l.clave === clave); return x && x.tren ? x.tren.km : null; };
  const kmCal = km("Bahía Calderitas–Oxtankah"), kmRuta = km("Ruta arqueológica del sur");
  const mesTranquiloRuta = tranquilos.find((x) => x.L === ruta)?.meses[0];
  const tarjeta = (n, clase, titulo, cuerpo, fuente) => `<article class="consejo ${clase} revela" style="--i:${n}">
      <p class="consejo-n" aria-hidden="true">${String(n).padStart(2, "0")}</p><h3>${titulo}</h3>${cuerpo}<p class="consejo-fuente">Fuente: ${fuente}</p></article>`;
  caja.innerHTML = `<div class="consejos-dentro">
    <header class="cabeza-doble"><div><p class="rotulo claro revela">Consejos para viajar</p>
    <h2 class="h2 claro revela" id="t-consejos">Viaja <em>mejor</em> al sur.</h2></div>
    <p class="cabeza-bajada revela">Lo que conviene saber antes de ir, sacado de datos oficiales: cuándo hay espacio, cuándo llueve, cuándo hace más calor y dónde quedarte.</p></header>
    <div class="consejos-rejilla">
      ${tarjeta(1, "consejo-ancho", "Ve cuando hay espacio", `<p>Estos son los meses tranquilos de cada lugar en el próximo año. Viajar en un mes tranquilo es más agradable y te sale más barato.</p>
        <div class="consejo-lugares">${tranquilos.map(({ L, meses }) => `<div><p class="consejo-lugar">${esc(L.nombre)}</p>${meses.length ? chips(meses, "chip-tranquilo", conAnio) : "<p>Sin meses tranquilos en el próximo año.</p>"}</div>`).join("")}</div>`,
        "pronóstico del proyecto con datos del INAH y de la frontera")}
      ${tarjeta(2, "", "Elige la temporada seca", `<p>En Chetumal casi no llueve (menos de 60 mm al mes) en:</p>${chips(secos, "chip-seco")}
        <p>Y en estos meses llueve mucho (150 mm o más): lleva impermeable.</p>${chips(lluviosos, "chip-lluvia")}`, "normal climatológica 1991–2020 del Servicio Meteorológico Nacional, estación Chetumal")}
      ${calor.length ? tarjeta(3, "", "Madruga en la selva", `<p>En la Ruta de las pirámides la máxima normal llega a ${tMax} °C en:</p>${chips(calor, "chip-calor")}
        <p>Visita las zonas temprano, con agua, gorra y repelente.</p>`, "normal climatológica 1991–2020 del Servicio Meteorológico Nacional, estación Nicolás Bravo") : ""}
      ${tormentas.length ? tarjeta(4, "", "Ojo con las tormentas", `<p>Son los meses con más probabilidad de que pase una tormenta tropical cerca:</p>${chips(tormentas, "chip-tormenta", (m) => ` · ${pct(che.calendario[m.i].tormenta)}`)}
        <p>Si viajas en esos meses, revisa los avisos del Servicio Meteorológico Nacional antes de salir.</p>`, "registro histórico de huracanes de la NOAA (HURDAT2)") : ""}
      ${kmCal !== null && kmRuta !== null ? tarjeta(5, "", "Quédate en Chetumal", `<p>Desde la estación del Tren Maya y el aeropuerto de Chetumal, la bahía de Calderitas está a <b>${num(kmCal)} km</b> y la Ruta de las pirámides a <b>${num(kmRuta)} km</b>, en línea recta.</p>
        <p>Así duermes en la ciudad y sales de día a la bahía y a las pirámides.</p>`, "estaciones y aeropuertos de SITUR-Q, coordenadas del INEGI") : ""}
      <article class="consejo consejo-cotiza revela" style="--i:6"><h3>¿Te ayudamos a armarlo?</h3>
        <p>Te armamos el plan con lugares reales y el mes con más espacio. Si te gusta, te lo cotizamos.</p>
        <button type="button" class="boton boton-tinta" id="consejos-cotizar">Cotiza tu viaje</button></article>
    </div>
  </div>`;
  $("consejos-cotizar").addEventListener("click", () => irACotizar(mesTranquiloRuta ? { lugar: ruta.clave, mes: mesTranquiloRuta.i } : {}));
  caja.hidden = false;
}

// ---------- Cómo llegar: Tren Maya y avión, distancias en línea recta ----------
function comoLlegar() {
  const caja = $("llegar"), G = D.llegar;
  if (!caja || !G) return;
  const sur = G.lugares.filter((l) => !l.referencia), t = G.tren;
  const coords = (clave) => { const r = LUGARES().find((x) => x.clave === clave); return r ? enlaceMapsCoord(r.lat, r.lon) : null; };
  caja.innerHTML = `<div class="llegar-dentro">
    <header class="cabeza-doble"><div><p class="rotulo revela">Cómo llegar</p>
    <h2 class="h2 revela" id="t-llegar">Del Caribe al sur, <em>en tren</em> o en avión.</h2></div>
    <p class="cabeza-bajada revela">El Tren Maya une Cancún y Playa del Carmen con Chetumal, y Chetumal tiene aeropuerto. Desde ahí, los tres lugares del sur quedan cerca.</p></header>
    <div class="llegar-rejilla">
      <div class="tren revela"><p class="tren-titulo">Tren Maya</p>
        <ol class="tren-linea">${t.estaciones.map((e, i) => `<li class="${e === "Chetumal" ? "fin" : ""}"><b data-no-traducir>${esc(e)}</b>${i === t.estaciones.length - 2 && t.intermedias > 0 ? `<small class="tren-inter">${t.intermedias} estaciones más en el camino</small>` : ""}</li>`).join("")}</ol>
        <p class="tren-km">Cancún → Chetumal: <b>${num(t.km_cancun_chetumal)} km</b> en línea recta</p></div>
      <ul class="llegar-lugares">${sur.map((l) => `<li class="revela"><h3>${esc(l.nombre)}</h3>
        <p><span class="llegar-ic">Tren</span> Estación del Tren Maya en <b data-no-traducir>${esc(l.tren.nombre)}</b>${l.tren.km ? `, a ${num(l.tren.km)} km` : ""}</p>
        <p><span class="llegar-ic">Avión</span> Aeropuerto de <b data-no-traducir>${esc(l.avion.nombre)}</b>${l.avion.km ? `, a ${num(l.avion.km)} km` : ""}</p>
        ${coords(l.clave) ? `<a class="maps" href="${esc(coords(l.clave))}" target="_blank" rel="noopener noreferrer">Cómo llegar<span aria-hidden="true"> ↗</span><span class="oculto"> (Google Maps, otra pestaña)</span></a>` : ""}</li>`).join("")}</ul>
    </div>
    <p class="vive-nota">${esc(G.nota)} No hay datos abiertos de rutas de autobús: pregúntanos al cotizar.</p>
  </div>`;
  caja.hidden = false;
}
const enlaceMapsCoord = (lat, lon) => `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${lat},${lon}`)}`;

// ---------- Cotiza tu viaje ----------
const COTIZA = { pedido: null, it: null, cat: null };
const MOMENTO_TXT = { dia: "Mañana", tarde: "Tarde", noche: "Noche" };

function irACotizar(pre = {}) {
  const f = $("cotiza-forma");
  if (!f) return;
  if (pre.lugar) f.querySelector(`[name=lugar][value="${CSS.escape(pre.lugar)}"]`)?.click();
  if (pre.mes !== undefined) f.mes.value = String(pre.mes);
  if (pre.intereses) f.querySelectorAll("[name=interes]").forEach((x) => { x.checked = pre.intereses.includes(x.value); });
  $("cotiza").scrollIntoView({ behavior: QUIETO ? "auto" : "smooth" });
  setTimeout(() => f.texto.focus({ preventScroll: true }), QUIETO ? 0 : 600);
}

// Catálogo cerrado: lo único que la IA puede elegir. Cada negocio y zona lleva un id estable.
function catalogoViaje() {
  const P = D.pronostico, ids = new Map(), lugares = [];
  for (const L of lugaresSur()) {
    const item = (x, tipo, momento, k) => { const id = `${L.clave.slice(0, 3).toLowerCase()}-${tipo}-${momento}-${k}`; ids.set(id, { ...x, tipo, momento, lugar: L.clave }); return { id, n: x.n, t: x.t, km: x.km }; };
    const g = { zonas: L.zonas.map((z, k) => item(z, "zona", "dia", k)) };
    for (const m of ["dia", "tarde", "noche"]) {
      g[`hacer_${m}`] = L.hacer[m].slice(0, 6).map((x, k) => item(x, "hacer", m, k));
      g[`comer_${m}`] = L.comer[m].slice(0, 6).map((x, k) => item(x, "comer", m, k));
    }
    g.dormir = L.dormir.slice(0, 6).map((x, k) => item(x, "dormir", "noche", k));
    lugares.push({ clave: L.clave, nombre: L.nombre,
      meses: L.calendario.map((c, i) => ({ i, mes: mesDe(P.meses[i]).largo, nivel: c.nivel, lluvia_mm: c.lluvia, temp_max: c.temp, tormenta: c.tormenta })),
      intereses: Object.keys(INTERES).filter((k) => L.fotos.some((f) => f.interes.includes(k))), ...g });
  }
  return { lugares, ids };
}

// Palabras del texto libre que delatan un interés (para el respaldo por reglas; la IA lee el texto completo).
const PALABRAS_INTERES = { cultura: /histori|ruina|pir[aá]mide|maya|arqueol|museo|cultura|templo/i, mar: /\bmar\b|playa|bah[ií]a|nadar|agua|laguna|muelle/i,
  naturaleza: /naturaleza|selva|aves|p[aá]jaro|caminar|aire libre|animal/i, sabores: /comer|comida|marisco|sabor|restaurante|gastronom|cenar|tacos/i,
  noche: /noche|fiesta|\bbar\b|m[uú]sica|baile/i };
function pedidoDeLaForma(f) {
  const texto = f.texto.value.trim().slice(0, 600);
  const marcados = [...f.querySelectorAll("[name=interes]:checked")].map((x) => x.value);
  const delTexto = Object.keys(PALABRAS_INTERES).filter((k) => PALABRAS_INTERES[k].test(texto));
  return { texto, lugar: f.lugar.value || null, mes: f.mes.value === "" ? null : +f.mes.value,
    dias: +f.dias.value, personas: +f.personas.value, intereses: [...new Set([...marcados, ...delTexto])],
    hospedaje: f.hospedaje.value, desdeCancun: f.origen.value === "cancun" || /canc[uú]n|playa del carmen/i.test(texto),
    nacional: f.nacional.checked, ritmo: /activ|aventura/i.test(texto) ? "activo" : f.ritmo.value };
}

// Respaldo por reglas: el mismo catálogo, sin IA.
function armarPorReglas(p, cat) {
  const sur = lugaresSur();
  let L = sur.find((x) => x.clave === p.lugar);
  if (!L) {
    const puntos = (x) => p.intereses.reduce((a, k) => a + x.fotos.filter((f) => f.interes.includes(k)).length, 0) + (p.intereses.includes("cultura") ? x.zonas.length * 2 : 0);
    L = [...sur].sort((a, b) => puntos(b) - puntos(a))[0];
  }
  const C = cat.lugares.find((x) => x.clave === L.clave);
  let mes = p.mes;
  if (mes === null) { mes = L.calendario.findIndex((c) => c.nivel === "tranquila"); if (mes < 0) mes = Math.max(0, L.calendario.findIndex((c) => c.nivel !== "alta")); }
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
  return { lugar: L.clave, mes, dias, fuente: "reglas", porque: porqueDelMes(L, mes) };
}

// El "por qué" del mes siempre lo escribe la página con el pronóstico, nunca la IA: en la prueba del 19-oct-2026
// Gemini llamó "tranquila" a una temporada alta.
function porqueDelMes(L, mes) {
  const c = L.calendario[mes];
  return `${L.nombre} en ${mesDe(D.pronostico.meses[mes]).largo}: ${NIVEL[c.nivel].texto.toLowerCase()} según nuestro pronóstico, con ${num(c.lluvia)} mm de lluvia en un mes normal.`;
}

// Modelos de Gemini en orden de preferencia. Si uno falla se prueba el siguiente, porque cada modelo tiene su propia
// cuota. Lo que vimos el 19-oct-2026: gemini-2.5-flash fue retirado (404), el nivel gratuito permite unos 5 pedidos
// por minuto por modelo (429) y en horas pico Google responde "mucha demanda" (500).
const MODELOS_IA = ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-flash-lite-latest"];

// Gemini por Firebase AI Logic. La respuesta se valida id por id; si algo no cuadra, se descarta.
async function armarConIA(p, cat) {
  const cfg = window.TORRE_FIREBASE;
  if (!NUBE.app || !cfg) return null;
  await prepararAppCheck();  // antes de getAI: Gemini exige el comprobante de App Check
  const ai = await import(`${SDK_FIREBASE}/firebase-ai.js`);
  const modelos = cfg.modeloIA ? [cfg.modeloIA] : MODELOS_IA;
  const catalogo = { lugares: cat.lugares };
  const pedido = { ...p, idioma: document.documentElement.lang || "es" };
  const tiempo = new Promise((_, no) => setTimeout(() => no(new Error("tiempo")), 25000));
  for (const [i, nombre] of modelos.entries()) {
    try {
      const r = await Promise.race([modeloIA(ai, nombre).generateContent(JSON.stringify({ pedido, catalogo })), tiempo]);
      const it = validarIA(JSON.parse(r.response.text()), p, cat);
      if (it) it.porque = porqueDelMes(lugaresSur().find((L) => L.clave === it.lugar), it.mes);
      return it;
    } catch (e) {
      // Si se acabó el tiempo o era el último modelo, entra el armador por reglas.
      if (i === modelos.length - 1 || e?.message === "tiempo") throw e;
    }
  }
  return null;
}

function modeloIA(ai, nombre) {
  return ai.getGenerativeModel(ai.getAI(NUBE.app, { backend: new ai.GoogleAIBackend() }), {
    model: nombre,
    // thinkingBudget 0: sin "razonamiento" extra. Medido el 19-oct-2026 con el mismo pedido: 16.3 s → 4.2 s, y el plan
    // siguió pasando la validación de ids. Los modelos "lite" no aceptan ese ajuste (400) y ya responden en ~2 s.
    generationConfig: { responseMimeType: "application/json", temperature: 0.4, ...(/lite/.test(nombre) ? {} : { thinkingConfig: { thinkingBudget: 0 } }) },
    systemInstruction: "Eres el planeador de viajes de Torre del Caribe, un equipo que vende viajes al sur de Quintana Roo (México). " +
      "Arma un itinerario usando SOLO los ids del catálogo que te damos (zonas arqueológicas y negocios reales del directorio del INEGI). " +
      "Nunca inventes lugares, negocios, horarios ni precios. Prefiere los meses con nivel 'tranquila' (hay espacio) salvo que el viajero pida un mes. " +
      "Cada día tiene momentos 'dia', 'tarde' y 'noche'; en la noche incluye un lugar para dormir excepto el último día. " +
      "Responde SOLO con JSON: {\"lugar\": clave, \"mes\": índice del mes, \"dias\": [{\"momentos\": [{\"momento\": \"dia\"|\"tarde\"|\"noche\", \"ids\": [id...], \"nota\": texto corto}]}], \"encaja\": texto}. " +
      "Escribe 'nota' y 'encaja' en el idioma del viajero. 'encaja' es UNA frase sobre por qué estos lugares van con lo que pidió el viajero; " +
      "no menciones el mes, el nivel, la lluvia ni ninguna cifra (eso lo explica la página).",
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

function cotiza() {
  const caja = $("cotiza"), P = D.pronostico, sur = lugaresSur();
  if (!caja || !P || !sur.length) return;
  COTIZA.cat = catalogoViaje();
  const radio = (name, valor, texto, marcado) => `<label class="opcion"><input type="radio" name="${name}" value="${esc(valor)}"${marcado ? " checked" : ""}><span>${texto}</span></label>`;
  caja.innerHTML = `<div class="cotiza-dentro">
    <header class="cabeza-doble"><div><p class="rotulo claro revela">Cotiza tu viaje</p>
      <h2 class="h2 claro revela" id="t-cotiza">Cuéntanos tu viaje. <em>Te lo armamos.</em></h2></div>
      <p class="cabeza-bajada revela">Escríbelo con tus palabras. Te armamos un plan con lugares reales y el mes con más espacio. Si te gusta, te lo cotizamos. Sin compromiso.</p></header>
    <form class="cotiza-forma revela" id="cotiza-forma" novalidate>
      <label class="campo campo-texto"><span>¿Cómo te imaginas tu viaje?</span>
        <textarea name="texto" rows="3" maxlength="600" placeholder="Ej.: 3 días tranquilos con mi familia; nos gusta la historia y comer mariscos."></textarea></label>
      <fieldset class="campo"><legend>Lugar</legend><div class="opciones">${radio("lugar", "", "Que me recomienden", true)}${sur.map((L) => radio("lugar", L.clave, esc(L.nombre))).join("")}</div></fieldset>
      <div class="campos-fila">
        <label class="campo"><span>Mes</span><select name="mes"><option value="">El más tranquilo</option>${P.meses.map((ym, i) => `<option value="${i}">${esc(mesDe(ym).largo)}</option>`).join("")}</select></label>
        <label class="campo"><span>Días</span><input type="number" name="dias" min="1" max="5" value="3" inputmode="numeric"></label>
        <label class="campo"><span>Personas</span><input type="number" name="personas" min="1" max="12" value="2" inputmode="numeric"></label>
      </div>
      <fieldset class="campo"><legend>Te gusta</legend><div class="opciones">${Object.entries(INTERES).map(([k, n]) => `<label class="opcion"><input type="checkbox" name="interes" value="${k}"><span>${n}</span></label>`).join("")}</div></fieldset>
      <div class="campos-fila">
        <fieldset class="campo"><legend>Hospedaje</legend><div class="opciones">${radio("hospedaje", "sencillo", "Sencillo")}${radio("hospedaje", "medio", "Medio", true)}${radio("hospedaje", "alto", "Alto")}</div></fieldset>
        <fieldset class="campo"><legend>Ritmo</legend><div class="opciones">${radio("ritmo", "tranquilo", "Tranquilo", true)}${radio("ritmo", "activo", "Activo")}</div></fieldset>
        <fieldset class="campo"><legend>Llego desde</legend><div class="opciones">${radio("origen", "sur", "Ya estoy en el sur", true)}${radio("origen", "cancun", "Cancún o Playa del Carmen")}</div></fieldset>
      </div>
      <label class="opcion opcion-sola"><input type="checkbox" name="nacional"><span>Soy mexicano o residente en México (entradas del INAH más baratas)</span></label>
      <button type="submit" class="boton boton-claro cotiza-armar">Armar mi viaje
        <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 8h10m0 0-4-4m4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    </form>
    <div class="cotiza-resultado" id="cotiza-resultado" aria-live="polite"></div>
  </div>`;
  $("cotiza-forma").addEventListener("focusin", () => prepararAppCheck(), { once: true });  // reCAPTCHA se carga al empezar a escribir
  $("cotiza-forma").addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = e.currentTarget, p = pedidoDeLaForma(f), salida = $("cotiza-resultado");
    p.dias = Math.max(1, Math.min(5, p.dias || 1)); p.personas = Math.max(1, Math.min(12, p.personas || 1));
    salida.innerHTML = `<p class="cotiza-espera"><span class="escribiendo" aria-hidden="true"><i></i><i></i><i></i></span> Estamos armando tu viaje con nuestros datos…</p>`;
    salida.scrollIntoView({ behavior: QUIETO ? "auto" : "smooth", block: "start" });
    let it = null;
    try { it = await armarConIA(p, COTIZA.cat); } catch (err) { it = null; }
    if (!it) it = armarPorReglas(p, COTIZA.cat);
    COTIZA.pedido = p; COTIZA.it = it;
    pintarItinerario(it, p);
  });
  caja.hidden = false;
}

function pintarItinerario(it, p) {
  const P = D.pronostico, L = P.lugares.find((x) => x.clave === it.lugar), c = L.calendario[it.mes], f = mesDe(P.meses[it.mes]);
  const cat = COTIZA.cat;
  const zonas = [...new Set(it.dias.flatMap((d) => d.momentos.flatMap((m) => m.ids)).map((id) => cat.ids.get(id)).filter((x) => x.tipo === "zona").map((x) => x.n))];
  const q = window.Cotizar ? Cotizar.cotizar({ zonas, dias: p.dias, personas: p.personas, nivel: c.nivel, hospedaje: p.hospedaje, desdeCancun: p.desdeCancun, nacional: p.nacional }, D.tarifas) : null;
  const dias = it.dias.map((d, k) => `<li class="dia revela" style="--i:${k}"><p class="dia-num">Día ${k + 1}</p>
    ${d.momentos.map((m) => { const foto = fotosDelMomento(P, L, m.momento).fotos[k % Math.max(1, fotosDelMomento(P, L, m.momento).fotos.length)];
      return `<div class="parada"><p class="parada-momento">${MOMENTO_TXT[m.momento]}</p>
        ${foto ? `<figure class="parada-foto"><img src="${esc(foto.archivo)}" alt="${esc(foto.muestra)}" loading="lazy"></figure>` : ""}
        ${m.nota ? `<p class="parada-nota">${esc(m.nota)}</p>` : ""}
        <ul class="negocios">${k === 0 && m.momento === "dia" && p.desdeCancun ? `<li class="negocio traslado"><b>Tren Maya: Cancún → Chetumal</b><small>Sales temprano; ${num(D.llegar.tren.km_cancun_chetumal)} km en línea recta</small></li>` : ""}${m.ids.map((id) => tarjetaNegocio(cat.ids.get(id))).join("")}</ul></div>`; }).join("")}</li>`).join("");
  // Resumen del plan, sin precio (decisión del equipo, 19-oct-2026): el precio se manda al contactar al viajero.
  const nComer = it.dias.flatMap((d) => d.momentos.flatMap((m) => m.ids)).map((id) => cat.ids.get(id)).filter((x) => x.tipo === "comer").length;
  const resumen = `<aside class="ticket revela" aria-label="Tu plan">
      <p class="ticket-t">Tu viaje · ${esc(L.nombre)}</p>
      <p class="ticket-sub">${esc(f.largo)} · ${p.dias === 1 ? "1 día" : `${p.dias} días`} · ${p.personas === 1 ? "1 persona" : `${p.personas} personas`}</p>
      <ul class="ticket-filas">
        ${zonas.length ? `<li><span>Zonas arqueológicas</span><b>${zonas.length}</b></li>` : ""}
        <li><span>Lugares para comer</span><b>${nComer}</b></li>
        <li><span>Noches de hospedaje</span><b>${p.dias - 1}</b></li>
        ${p.desdeCancun ? `<li><span>Tren Maya desde Cancún</span><b>Incluido en el plan</b></li>` : ""}
      </ul>
      <p class="ticket-cta">¿Te gusta este plan?</p>
      <p class="ticket-nota">Pide tu cotización: te damos un folio y te escribimos con el precio final, con hoteles y transporte reales. Sin compromiso.</p>
      <button type="button" class="boton boton-claro ticket-boton" id="it-quiero-2">Quiero cotizar este viaje</button>
    </aside>`;
  $("cotiza-resultado").innerHTML = `<div class="itinerario">
      <header class="it-cabeza"><p class="it-fuente">${it.fuente === "ia" ? "Plan sugerido por IA (Gemini) con nuestros datos" : "Plan armado con nuestros datos"}</p>
        <h3 class="it-titulo">${esc(L.nombre)} · ${esc(f.largo)}</h3>
        <p class="estado-grande ${NIVEL[c.nivel].clase}">${NIVEL[c.nivel].texto}</p>
        ${it.porque ? `<p class="it-porque">${esc(it.porque)}</p>` : ""}
        ${it.encaja ? `<p class="it-porque" data-no-traducir>${esc(it.encaja)}</p>` : ""}</header>
      <div class="it-cuerpo"><ol class="dias">${dias}</ol>${resumen}</div>
      <div class="it-botones"><button type="button" class="boton boton-claro" id="it-quiero">Quiero cotizar este viaje</button>
        <button type="button" class="boton-linea claro" id="it-ajustar">Ajustar</button>
        <button type="button" class="boton-linea claro" id="it-compartir">Compartir</button></div>
      <div id="it-solicitud"></div>
    </div>`;
  const resultado = $("cotiza-resultado");
  alAparecer([...resultado.querySelectorAll(".revela")], (n) => { n.classList.add("visible"); n.querySelectorAll("[data-contar]").forEach(contar); });
  $("it-ajustar").addEventListener("click", () => $("cotiza-forma").scrollIntoView({ behavior: QUIETO ? "auto" : "smooth" }));
  $("it-compartir").addEventListener("click", () => {
    const texto = `Mi viaje al sur de Quintana Roo: ${L.nombre}, ${f.largo}, ${p.dias} días.`;
    if (navigator.share) navigator.share({ title: "Torre del Caribe", text: texto, url: URL_PAGINA }).catch(() => {});
    else window.open(`https://wa.me/?text=${encodeURIComponent(`${texto} ${URL_PAGINA}`)}`, "_blank", "noopener");
  });
  ["it-quiero", "it-quiero-2"].forEach((id) => $(id).addEventListener("click", () => formaSolicitud(it, p, q, L, f)));
}

// Formulario de cotización (decisión 28): el viajero deja sus datos, recibe un FOLIO (su ID de cliente) y el equipo le
// escribe con el precio. Se guarda en Firestore (colección solicitudes, el folio es el id del documento); solo el equipo lo
// lee en la consola. Junto va el costo estimado interno (cotizar.js) para que el equipo arme el precio; el viajero no lo ve.
const ALFABETO_FOLIO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";  // sin 0/O ni 1/I/L, para dictarlo sin confusiones
function nuevoFolio() {
  const h = new Date(), d = `${String(h.getFullYear()).slice(2)}${String(h.getMonth() + 1).padStart(2, "0")}${String(h.getDate()).padStart(2, "0")}`;
  const azar = crypto.getRandomValues(new Uint32Array(5));
  return `TDC-${d}-${[...azar].map((x) => ALFABETO_FOLIO[x % ALFABETO_FOLIO.length]).join("")}`;
}

function formaSolicitud(it, p, q, L, f) {
  const caja = $("it-solicitud"), correo = window.TORRE_CONTACTO && window.TORRE_CONTACTO.correo;
  caja.innerHTML = `<form class="solicitud" id="solicitud-forma" novalidate>
    <p class="solicitud-t">Pide tu cotización</p>
    <p class="solicitud-sub">Te damos un folio y te escribimos con el precio de tu viaje a ${esc(L.nombre)}.</p>
    <div class="campos-fila"><label class="campo"><span>Nombre completo</span><input name="nombre" required minlength="2" maxlength="80" autocomplete="name"></label>
      <label class="campo"><span>Correo</span><input name="correo" type="email" maxlength="120" autocomplete="email"></label>
      <label class="campo"><span>WhatsApp o teléfono</span><input name="telefono" type="tel" maxlength="25" autocomplete="tel" inputmode="tel"></label></div>
    <fieldset class="campo"><legend>¿Cómo prefieres que te contactemos?</legend><div class="opciones">
      <label class="opcion"><input type="radio" name="medio" value="whatsapp" checked><span>WhatsApp</span></label>
      <label class="opcion"><input type="radio" name="medio" value="correo"><span>Correo</span></label>
      <label class="opcion"><input type="radio" name="medio" value="llamada"><span>Llamada</span></label></div></fieldset>
    <div class="campos-fila"><label class="campo"><span>Fechas que tienes en mente (opcional)</span><input name="fechas" maxlength="80" placeholder="Ej.: del 10 al 13 de ${esc(MESES[f.m - 1])}"></label>
      <label class="campo"><span>Personas</span><input name="personas" type="number" min="1" max="30" value="${p.personas}" inputmode="numeric"></label></div>
    <label class="campo"><span>Algo más que debamos saber (opcional)</span><textarea name="comentario" rows="2" maxlength="600" placeholder="Ej.: viajamos con niños, preferimos hotel con alberca…"></textarea></label>
    <details class="aviso"><summary>Aviso de privacidad</summary><div>
      <p>Torre del Caribe (equipo de estudiantes de la UNRC) usa tus datos solo para cotizar y organizar el viaje que pediste. No los compartimos ni los vendemos. Se guardan en Firebase (Google).</p>
      <p>Para pedir que los borremos, ${correo ? `escríbenos a <span data-no-traducir>${esc(correo)}</span>` : "dinos tu folio cuando te contactemos"}.</p></div></details>
    <label class="opcion opcion-sola"><input type="checkbox" name="consentimiento" required><span>Acepto el aviso de privacidad</span></label>
    <button type="submit" class="boton boton-claro">Enviar y obtener mi folio</button>
    <p class="solicitud-estado" id="solicitud-estado" role="status"></p></form>`;
  caja.querySelector("[name=nombre]").focus();
  $("solicitud-forma").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fm = e.currentTarget, estado = $("solicitud-estado");
    const correoV = fm.correo.value.trim(), telV = fm.telefono.value.trim();
    if (fm.nombre.value.trim().length < 2) { estado.textContent = "Escribe tu nombre."; fm.nombre.focus(); return; }
    if (!correoV && !telV) { estado.textContent = "Déjanos un correo o un teléfono para poder escribirte."; fm.correo.focus(); return; }
    if (correoV && !fm.correo.checkValidity()) { estado.textContent = "Revisa tu correo."; fm.correo.focus(); return; }
    if (telV && !/^[+\d][\d\s()-]{6,24}$/.test(telV)) { estado.textContent = "Revisa tu teléfono."; fm.telefono.focus(); return; }
    if (!fm.consentimiento.checked) { estado.textContent = "Para enviarla, acepta el aviso de privacidad."; return; }
    if (!NUBE.lista) { estado.textContent = "No pudimos conectarnos. Revisa tu internet e inténtalo de nuevo."; return; }
    estado.textContent = "Enviando…";
    try {
      const folio = await enviarSolicitud({ nombre: fm.nombre.value.trim(), correo: correoV, telefono: telV, medio: fm.medio.value,
        fechas: fm.fechas.value.trim(), personas: Math.max(1, Math.min(30, +fm.personas.value || p.personas)), comentario: fm.comentario.value.trim() }, it, p, q, L, f);
      try { localStorage.setItem("ultimoFolio", folio); } catch (err) { /* sin almacenamiento */ }
      caja.innerHTML = `<div class="solicitud-ok"><p class="solicitud-t">¡Listo! Recibimos tu solicitud.</p>
        <p class="folio-t">Tu folio</p><p class="folio" data-no-traducir>${esc(folio)}</p>
        <p>Guárdalo: con él te identificamos. Te escribiremos por ${esc({ whatsapp: "WhatsApp", correo: "correo", llamada: "teléfono" }[fm.medio.value])} con el precio de tu viaje a ${esc(L.nombre)} en ${esc(f.largo)}.</p></div>`;
    } catch (err) { estado.textContent = "No se pudo enviar. Inténtalo de nuevo en un momento."; }
  });
}

async function enviarSolicitud(datos, it, p, q, L, f) {
  const { fs, db } = NUBE, folio = nuevoFolio();
  const itinerario = JSON.stringify({ lugar: L.nombre, mes: f.largo, dias: p.dias, pedido: p.texto, intereses: p.intereses, hospedaje: p.hospedaje,
    desde: p.desdeCancun ? "Cancún / Playa del Carmen" : "sur", plan: it.dias.map((d) => d.momentos.map((m) => ({ momento: m.momento, lugares: m.ids.map((id) => COTIZA.cat.ids.get(id).n) }))), fuente: it.fuente }).slice(0, 8000);
  // Solo para el equipo: costo con tarifas conocidas y margen sugerido según el mes (el viajero no lo ve).
  const precio = q ? JSON.stringify({ costo_conocido: q.costo, margen_sugerido: q.margen, precio_sugerido: q.precio, completo: q.completo,
    conceptos: q.conceptos.map((c) => [c.concepto, c.detalle, c.monto]), falta_cotizar: q.faltan.map((x) => x.concepto) }).slice(0, 2000) : undefined;
  const doc = { folio, nombre: datos.nombre, medio: datos.medio, personas: datos.personas, itinerario,
    idioma: (document.documentElement.lang || "es").slice(0, 5), uid: NUBE.uid, creado: fs.serverTimestamp(), consentimiento: true, estado: "nueva" };
  if (datos.correo) doc.correo = datos.correo.slice(0, 120);
  if (datos.telefono) doc.telefono = datos.telefono.slice(0, 25);
  if (datos.fechas) doc.fechas = datos.fechas.slice(0, 80);
  if (datos.comentario) doc.comentario = datos.comentario.slice(0, 600);
  if (precio) doc.precio = precio;
  await fs.setDoc(fs.doc(db, "solicitudes", folio), doc);  // el folio es el id: crear sí, sobrescribir no (reglas)
  return folio;
}

// Prueba social en la portada: cifras reales (INAH) y, si ya hay, los corazones de todos los viajeros (Firebase).
function pruebaPortada() {
  const el = $("portada-prueba"), cc = D.campana && D.campana.cifras;
  if (!el || !cc) return;
  const total = NUBE.lista ? [...NUBE.cuentas.values()].reduce((a, b) => a + b, 0) : 0;
  el.innerHTML = `<span>${num(Math.round(cc.ruta / 365))} personas al día en las pirámides del sur (INAH 2025)</span>${total > 0 ? `<span>♥ ${num(total)} fotos guardadas por viajeros</span>` : ""}`;
  el.hidden = false;
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
          <figcaption>${esc(x.muestra)}<small>Foto: <span data-no-traducir>${esc(x.autor)}</span>, <a href="${esc(x.url_licencia || x.url_original)}" rel="license noopener noreferrer" target="_blank" data-no-traducir>${esc(x.licencia)}</a></small></figcaption></figure></li>`).join("")}</ul></div>` : ""}
      ${L.helados && L.helados.length ? `<div class="helados"><p class="lugar-fotos-titulo">Para el calor: helados y paletas</p>
        <p class="helados-nota">Paleterías y neverías registradas en el directorio del INEGI, las más cercanas al centro.</p>
        <ul class="negocios">${L.helados.map(tarjetaNegocio).join("")}</ul></div>` : ""}</div>
    ${MOMENTOS.map((m) => {
      const hacer = (m.clave === "dia" ? L.zonas : []).concat(L.hacer[m.clave]);
      const comer = L.comer[m.clave];
      return `<div class="momento m-${m.clave}" data-momento="${m.clave}">
        <h3 class="momento-titulo">${m.titulo}</h3><p class="momento-bajada">${m.bajada}</p>
        ${franjaMomento(P, L, m.clave)}
        <div class="momento-rejilla">
          <div><h4>Qué hacer</h4>${listaCorta(hacer)}</div>
          <div><h4>Dónde comer</h4>${listaCorta(comer)}</div>
          ${m.clave === "noche" ? `<div><h4>Dónde dormir</h4>${L.estrellas ? `<p class="estrellas-oficiales"><span aria-hidden="true">★★★★★</span> ${L.estrellas.por_categoria["5"]} % de los cuartos de hotel son de 5 estrellas (categoría oficial, ${L.estrellas.anio})</p>` : ""}${listaCorta(L.dormir)}</div>` : ""}
        </div></div>`;
    }).join("")}
    <p class="que-hacer-nota">${L.estrellas ? `Categoría de hotel: ${esc(L.estrellas.fuente)}. ` : ""}Fuente: INEGI, Directorio Estadístico Nacional de Unidades Económicas (DENUE). El tipo de lugar y el momento del día los sugiere un clasificador de texto que lee el nombre y el giro oficial de cada negocio (acertó 39 de 40 en una revisión al azar). Cuando un lugar no tiene algo cerca, se muestra lo más cercano de los otros lugares del sur. "Ver en Google Maps" abre Google Maps en otra pestaña; esta página no descarga nada de Google.</p>`;
  conectarVerMas(caja);
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
    ? `<li class="persona revela"><span class="avatar" aria-hidden="true" data-no-traducir>${iniciales(p.nombre)}</span><h3 data-no-traducir>${p.nombre}</h3><p class="rol">${p.rol}</p><p class="hace">${p.hace}</p></li>`
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
}

// ---------- Pie (las dos páginas) ----------
function pie() {
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
// Dos páginas con el mismo código (decisión 25): index.html es la del viajero y datos.html la de "Los datos". Cada
// sección se dibuja solo si está en la página abierta.
const siEsta = (id, f) => { if ($(id)) f(); };
tema();
barra();
postales();
vive();
vivimos();
espacio();
videoBanda();
preguntas();
anuncio();
siEsta("portada-foto", portada);
// Reparto de fotos: primero se marcan las fijas (vitrina y portada) y "Descubre", que va arriba, elige antes que
// "Los lugares" y "Qué hacer"; así cada sección muestra fotos distintas.
presembrarUso();
descubre();
siEsta("dato", elDato);
siEsta("problema", problema);
siEsta("mapa3d", construirMapa);
siEsta("capitulos", capitulos);
siEsta("mapa-mov", mapaMovimiento);
siEsta("dinero", dinero);
siEsta("norte", elNorte);
modulos();
unDia();
historia();
fauna();
cotiza();
consejos();
comoLlegar();
pruebaPortada();
favoritos();
visorFotos();
if ($("portada-foto") && carrusel.L) corazonPortada(carrusel.L.fotos[carrusel.i].archivo);
servidorLocal();
// Tablas que se desplazan de lado: se pueden alcanzar y mover con el teclado (auditoría axe, Fase 10).
document.querySelectorAll(".tabla-envoltura").forEach((t) => { t.tabIndex = 0; t.setAttribute("role", "region"); t.setAttribute("aria-label", "Tabla que se desplaza de lado"); });

// ---------- Fase 9: si la página la sirve el servidor del proyecto (localhost), los modelos responden en vivo ----------
// En GitHub Pages o abriendo el archivo no se pregunta nada: la página sigue con pagina.js y sin llamadas externas.
async function servidorLocal() {
  if (location.protocol !== "http:" || !["localhost", "127.0.0.1"].includes(location.hostname)) return;
  try { if (!(await (await fetch("/api/salud")).json()).ok) return; } catch { return; }
  const pres = $("presupuesto"), vivo = $("envivo");
  if (pres && !pres.hidden) {
    const panel = document.createElement("div");
    panel.className = "pres-prueba";
    panel.innerHTML = `<h3 class="camp-sub">Pruébalo tú <small>· el servidor resuelve el modelo en vivo</small></h3>
      <div class="pres-controles">
        <label>Presupuesto al año <b id="pp-monto"></b><input type="range" id="pp-presupuesto" min="50000" max="1000000" step="25000" value="250000"></label>
        <label>Conversión de Facebook <select id="pp-cvr"><option value="0.03">3 %</option><option value="" selected>5.75 % (Google Travel)</option><option value="0.0638">6.38 % (mediana)</option></select></label>
        <label>Tope por canal <b id="pp-tope-v"></b><input type="range" id="pp-tope" min="0.5" max="1" step="0.05" value="0.7"></label>
        <label>Piso por lugar <b id="pp-piso-v"></b><input type="range" id="pp-piso" min="0" max="0.33" step="0.01" value="0.15"></label>
        <label class="pp-check"><input type="checkbox" id="pp-alta" checked> Cero anuncio en temporada alta</label>
      </div>
      <p class="pres-resultado" id="pp-resultado" aria-live="polite"></p>`;
    pres.querySelector(".pres-regla").after(panel);
    const v = (id) => $(id).value;
    let espera;
    const resolver = async () => {
      $("pp-monto").textContent = pesos(+v("pp-presupuesto"));
      $("pp-tope-v").textContent = `${Math.round(v("pp-tope") * 100)} %`;
      $("pp-piso-v").textContent = `${Math.round(v("pp-piso") * 100)} %`;
      const cuerpo = { presupuesto_anual: +v("pp-presupuesto"), tope_canal: +v("pp-tope"), piso_equidad: +v("pp-piso"),
        temporada_alta: $("pp-alta").checked, cvr_facebook: v("pp-cvr") ? +v("pp-cvr") : null };
      const r = await (await fetch("/api/optimizar", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(cuerpo) })).json();
      $("pp-resultado").innerHTML = r.estado !== "Optimal" ? "Con esas reglas no hay reparto posible (el modelo no encuentra solución)." :
        `<b>${Math.round(r.visitantes).toLocaleString("es-MX")} visitantes</b> en ${r.meses} meses · ${pesos(r.pesos_por_visitante)} por visitante · ` +
        Object.entries(r.lugares).map(([l, p]) => `${l} ${p} %`).join(" · ") + ` · Facebook ${r.canales.Facebook ?? 0} % / Google ${r.canales.Google ?? 0} % <small>(resuelto en ${r.ms} ms)</small>`;
    };
    panel.querySelectorAll("input, select").forEach((c) => c.addEventListener("input", () => { clearTimeout(espera); espera = setTimeout(resolver, 250); }));
    resolver();
  }
  if (vivo && !vivo.hidden && vivo.mostrarSemana) {
    const b = document.createElement("button");
    b.className = "boton-linea claro"; b.type = "button"; b.textContent = "Escuchar en vivo";
    $("vivo-boton").after(b);
    let fuente = null;
    b.addEventListener("click", () => {
      if (fuente) { fuente.close(); fuente = null; b.textContent = "Escuchar en vivo"; return; }
      vivo.pararReproduccion();
      fuente = new EventSource("/api/stream?ms=150");
      b.textContent = "Dejar de escuchar";
      fuente.onmessage = (e) => vivo.mostrarSemana(JSON.parse(e.data).i);
      fuente.addEventListener("fin", () => { fuente.close(); fuente = null; b.textContent = "Escuchar en vivo"; });
    });
  }
}
siEsta("lista-fases", fases);
siEsta("personas", equipo);
siEsta("evidencia", evidencia);
pie();
siEsta("chat", chat);
alAparecer([...document.querySelectorAll(".revela")], (n) => { n.classList.add("visible"); n.querySelectorAll("[data-contar]").forEach(contar); if (n.dataset.contar) contar(n); });
equilibrarTitulos();
