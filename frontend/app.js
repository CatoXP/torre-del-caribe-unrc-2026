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
const credito = (f) => `${f.muestra}. Foto: ${f.autor}, <a href="${f.url_licencia}" rel="license">${f.licencia}</a>, vía Wikimedia Commons.`;

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
  ["lugares", "radar", "movimiento", "dinero", "fases", "equipo"].forEach((id) => obs.observe($(id)));
}

// ---------- Anuncio del Radar (arriba de todo). Solo si pagina.js trae "radar"; el texto sale de sus datos. ----------
function anuncio() {
  const R = D.radar, a = $("anuncio");
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
  const f = D.portada, foto = $("portada-foto");
  if (f) {
    foto.style.backgroundImage = `url("${f.archivo_local}")`;
    $("credito-portada").innerHTML = credito(f);
  }
  const listo = () => requestAnimationFrame(() => document.body.classList.add("cargada"));
  if (f && !QUIETO) { const img = new Image(); img.onload = listo; img.onerror = listo; img.src = f.archivo_local; } else listo();
  if (!QUIETO) {  // paralaje suave de la foto mientras se sale de la portada
    let pendiente = false;
    window.addEventListener("scroll", () => {
      if (pendiente) return;
      pendiente = true;
      requestAnimationFrame(() => {
        const y = Math.min(window.scrollY, window.innerHeight);
        foto.style.translate = `0 ${y * 0.28}px`;
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
const MUNICIPIOS_LUGARES = new Set(["002", "004", "006"]);  // Felipe Carrillo Puerto, Othón P. Blanco, José María Morelos
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
  const lats = D.regiones.map((r) => r.lat), lons = D.regiones.map((r) => r.lon);
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
  D.regiones.forEach((r, i) => {
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
  lista.innerHTML = D.regiones.map((r) => `
    <li class="capitulo" id="lugar-${r.numero}" data-n="${r.numero}">
      <p class="capitulo-num">${String(r.numero).padStart(2, "0")} / ${String(D.regiones.length).padStart(2, "0")}</p>
      <h3>${r.nombre}</h3>
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
};

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
      let mejor = null, puntos = 0;
      for (const p of P) {
        const s = p.claves.reduce((acc, c) => acc + (t.includes(limpiar(c).trim()) ? 1 : 0), 0);
        if (s > puntos) { puntos = s; mejor = p; }
      }
      return mejor;
    })();
    const espera = agregar("bot", `<span class="escribiendo" aria-label="Escribiendo"><i></i><i></i><i></i></span>`);
    setTimeout(() => {
      espera.innerHTML = q ? `${q.respuesta}<small>Fuente: ${q.fuente}</small>`
        : "Todavía no tengo esa respuesta. Prueba con una de las preguntas de abajo: solo respondo lo que los datos del proyecto pueden sostener.";
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
    partes.push(tarjeta("El Radar contra \"igual que el mes pasado\"",
      `<p class="prueba-cifra"><b>${m.aciertos}</b> de ${m.casos}</p>
       <p>meses que el modelo nunca vio, acertados. Repetir el mes anterior acierta ${m.aciertos_persistencia}. Su valor: anticipó ${m.cambios_anticipados} de los ${m.cambios_reales} cambios de estado.</p>
       ${m.cambios_en_los_5 !== null && m.cambios_en_los_5 !== undefined ? `<p class="prueba-ojo">En los cinco lugares hubo ${m.cambios_en_los_5} cambios en esos meses: ahí el modelo casi no se ha podido probar.</p>` : ""}`));
  }
  const filas = E.markov.map((x) => `<tr><td>${x.semanas} ${x.semanas === 1 ? "semana" : "semanas"}</td><td>${x.brier_markov.toFixed(3)}</td><td>${x.brier_persistencia.toFixed(3)}</td></tr>`).join("");
  partes.push(tarjeta("¿Se llenará el norte? La cadena de Markov",
    `<p>Sus probabilidades fallan menos que "igual que la semana pasada" a 1, 4 y 8 semanas (error de Brier: más bajo es mejor).</p>
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
