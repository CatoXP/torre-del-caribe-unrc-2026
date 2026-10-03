/*
  Autor: Brandon Uriel García Sánchez
  Módulo: Campaña (página web)
  Qué hace:          Cambia la parte del viajero de la página a 10 idiomas (decisión 16, 02-oct-2026): español, inglés,
                     francés, alemán, italiano, portugués, chino, japonés, coreano y maya yucateco.
  Por qué así:       - Elegimos "Mercados que llegan": se traduce todo lo del viajero; "Los datos" se queda en español
                       para no meter errores en explicaciones técnicas y cifras.
                     - La página se arma con datos y cambia con cada clic (planeador, qué hacer). En vez de reescribir
                       cada texto del código, se traduce lo que ya está en pantalla: cada bloque de texto se "normaliza"
                       (las cifras se vuelven {n0}, {n1}…, los meses {m0}… y los lugares {p0}…) y se busca en el
                       diccionario del idioma. Así "Llega 29 % menos gente" y "Llega 40 % menos gente" son una sola
                       frase que traducir. Las cifras se escriben al estilo del idioma (Intl.NumberFormat) y los meses los
                       da el propio navegador (Intl.DateTimeFormat): no se traducen a mano.
                     - Lo que no está en el diccionario (nombres de negocios del DENUE, por ejemplo) se queda tal cual.
                     - El maya yucateco existe como diccionario pero NO aparece en el menú hasta que lo revise una persona
                       que lo hable (decisión del equipo).
                     - Descartado: un servicio de traducción en línea (la página funciona sin internet y no manda datos).
  Datos de entrada:  idiomas/<código>.js (un diccionario por idioma: frase normalizada en español → traducción).
  Alimenta a:        La campaña para el público internacional (mercados de los aeropuertos de Q. Roo).
*/
(function () {
  "use strict";
  const IDIOMAS = [
    { c: "es", n: "Español" }, { c: "en", n: "English" }, { c: "fr", n: "Français" }, { c: "de", n: "Deutsch" },
    { c: "it", n: "Italiano" }, { c: "pt", n: "Português" }, { c: "zh", n: "中文" }, { c: "ja", n: "日本語" },
    { c: "ko", n: "한국어" }, { c: "yua", n: "Maaya t'aan", enRevision: true },
  ];
  // Partes que se traducen (la parte del viajero). "Los datos" (#datos en adelante) se queda en español.
  const ZONAS = ["#barra", "#inicio", "#planea", "#que-hacer", "#postales", "#vive", "#llamado", "#lugares", "#vivimos",
    "#preguntas", "#aviso-lleno", "#chat", "#chat-boton", "#datos", ".saltar"];
  const MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
    "noviembre", "diciembre"];
  const CORTOS_ES = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"];
  const INLINE = new Set(["B", "EM", "STRONG", "I", "BR", "SMALL", "SPAN", "SUB", "SUP"]);
  const ATRIBUTOS = ["aria-label", "alt", "title", "placeholder"];
  // Una cifra empieza en un dígito que no sigue a una letra ni a "{" (así no se toca {n0}, {x1}…)
  const NUM = /(?<![\w{])\d[\d,]*(?:\.\d+)?/g;
  const RE_MES = new RegExp(`\\b(${MESES_ES.join("|")})\\b`, "gi");

  const estado = { lang: "es", dic: {}, lugares: {}, cargando: {} };
  window.IDIOMAS_TRAD = window.IDIOMAS_TRAD || {};

  // ---------- Normalizar: cifras, meses y lugares se vuelven marcas ----------
  const nombresLugares = () => Object.keys(estado.lugares).sort((a, b) => b.length - a.length);
  function normalizar(texto) {
    const n = [], m = [], p = [];
    let s = texto.replace(/\s+/g, " ").trim();
    s = s.replace(NUM, (x) => `{n${n.push(x) - 1}}`);
    s = s.replace(RE_MES, (x) => `{m${m.push(MESES_ES.indexOf(x.toLowerCase())) - 1}}`);
    for (const nombre of nombresLugares()) {
      if (s.includes(nombre)) s = s.split(nombre).join(`{p${p.push(nombre) - 1}}`);
    }
    return { clave: s, n, m, p };
  }

  // Cifra al estilo del idioma: "3,672" → "3.672" (de), "78.3" → "78,3" (fr). Los años se quedan sin separador.
  function cifra(x, lang) {
    if (/^(19|20)\d\d$/.test(x)) return x;
    const v = Number(x.replace(/,/g, ""));
    if (!isFinite(v)) return x;
    const dec = (x.split(".")[1] || "").length;
    return new Intl.NumberFormat(lang === "yua" ? "es-MX" : lang, { minimumFractionDigits: dec, maximumFractionDigits: dec }).format(v);
  }
  const mesLargo = (i, lang) => new Intl.DateTimeFormat(lang === "yua" ? "es-MX" : lang, { month: "long" }).format(new Date(2026, i, 15));
  const mesCorto = (i, lang) => new Intl.DateTimeFormat(lang === "yua" ? "es-MX" : lang, { month: "short" }).format(new Date(2026, i, 15)).replace(".", "").toUpperCase();

  function traducir(texto) {
    const lang = estado.lang, dic = estado.dic[lang];
    if (lang === "es" || !dic) return null;
    const t = texto.trim();
    if (!t || !/[A-Za-zÁÉÍÓÚáéíóúÑñ]/.test(t.replace(/\{x\d+\}/g, "").replace(/<[^>]+>/g, ""))) return null;
    const ci = CORTOS_ES.indexOf(t.toUpperCase());  // "oct" en los botones de mes (la mayúscula la pone el CSS)
    if (ci >= 0) return t === t.toUpperCase() ? mesCorto(ci, lang) : mesCorto(ci, lang).toLowerCase();
    const k = normalizar(t);
    let destino = dic[k.clave];
    if (destino === undefined && k.p.length === 1 && k.clave === "{p0}") destino = "{p0}";
    if (destino === undefined) return null;
    return destino
      .replace(/\{n(\d+)\}/g, (_, i) => cifra(k.n[+i] ?? "", lang))
      .replace(/\{m(\d+)\}/g, (_, i) => mesLargo(k.m[+i], lang))
      .replace(/\{p(\d+)\}/g, (_, i) => (estado.lugares[k.p[+i]] || {})[lang] || k.p[+i]);
  }

  // ---------- Bloques: un elemento con texto propio se traduce entero (con sus <b>, <em>… adentro) ----------
  function esBloque(el) {
    if (!(el instanceof Element) || el.closest("[data-no-traducir], script, style, svg")) return false;
    let texto = false;
    for (const h of el.childNodes) {
      if (h.nodeType === 3 && h.textContent.trim()) texto = true;
      else if (h.nodeType === 1 && h.hasAttribute("data-no-traducir")) continue;  // nombre propio: va como marca {x}
      else if (h.nodeType === 1 && (!INLINE.has(h.tagName) || h.hasAttribute("data-bloque"))) return false;  // data-bloque: se traduce aparte
      else if (h.nodeType === 1 && h.querySelector("*:not(b):not(em):not(strong):not(i):not(br):not(small):not(span):not([data-no-traducir]), [data-bloque]")) return false;
    }
    return texto || (el.children.length === 0 && el.textContent.trim().length > 0);
  }

  // HTML del bloque con las etiquetas simplificadas (<b>…</b>); se guardan las originales para volver a ponerlas.
  // Lo marcado con data-no-traducir (nombres de negocios, autores de fotos, licencias) se vuelve {x0}, {x1}… y se
  // devuelve intacto al final.
  function simplificar(el) {
    const tpl = document.createElement("template");
    tpl.innerHTML = el.innerHTML;
    const fijos = [];
    tpl.content.querySelectorAll("[data-no-traducir]").forEach((n) => {
      if (n.isConnected || n.parentNode) n.replaceWith(document.createTextNode(`{x${fijos.push(n.outerHTML) - 1}}`));
    });
    const etiquetas = [];
    const html = tpl.innerHTML.replace(/<(\/?)([a-z0-9]+)([^>]*)>/gi, (todo, cierre, tag) => {
      if (!cierre) etiquetas.push(todo);
      return `<${cierre}${tag.toLowerCase()}>`;
    });
    return { html, etiquetas, fijos };
  }
  function restaurar(html, etiquetas, fijos = []) {
    let i = 0;
    return html.replace(/<([a-z0-9]+)>/gi, (todo, tag) => {
      // findIndex (no indexOf): dos etiquetas iguales seguidas (<span aria-hidden>…) hacían que la tercera tomara la
      // de la segunda y el texto oculto "(Google Maps, otra pestaña)" quedaba a la vista.
      const k = etiquetas.findIndex((e, j) => j >= i && e.toLowerCase().startsWith(`<${tag.toLowerCase()}`));
      if (k < 0) return todo;
      i = k + 1;
      return etiquetas[k];
    }).replace(/\{x(\d+)\}/g, (_, k) => fijos[+k] ?? "");
  }

  // Lo último que esta función escribió en cada elemento: si la página lo cambió después, el texto nuevo es el español.
  const puesto = new WeakMap(), textoPuesto = new WeakMap();
  function traducirBloque(el) {
    if (el.dataset.es === undefined || puesto.get(el) !== el.innerHTML) el.dataset.es = el.innerHTML;
    const { html, etiquetas, fijos } = simplificar({ innerHTML: el.dataset.es });
    const t = traducir(html);
    const nuevo = t === null ? el.dataset.es : restaurar(t, etiquetas, fijos);
    if (el.innerHTML !== nuevo) el.innerHTML = nuevo;
    puesto.set(el, el.innerHTML);
    el.dataset.tr = estado.lang;
  }
  // Elementos con texto e ícono (botones con <svg>): se traduce cada pedazo de texto por separado.
  function traducirTextos(el) {
    for (const h of el.childNodes) {
      if (h.nodeType !== 3 || !/[A-Za-zÁÉÍÓÚáéíóúÑñ]/.test(h.textContent)) continue;
      if (h.__es === undefined || textoPuesto.get(h) !== h.textContent) h.__es = h.textContent;
      const t = traducir(h.__es);
      const nuevo = t === null ? h.__es : h.__es.replace(h.__es.trim(), t);
      if (h.textContent !== nuevo) h.textContent = nuevo;
      textoPuesto.set(h, h.textContent);
    }
  }
  function traducirAtributos(el) {
    for (const a of ATRIBUTOS) {
      if (!el.hasAttribute(a)) continue;
      const k = `es${a.replace(/-./g, (x) => x[1].toUpperCase())}`;
      if (el.dataset[k] === undefined) el.dataset[k] = el.getAttribute(a);
      const t = traducir(el.dataset[k]);
      el.setAttribute(a, t === null ? el.dataset[k] : t);
    }
  }

  function recorrer(raiz) {
    const zonas = ZONAS.flatMap((z) => [...document.querySelectorAll(z)]).filter((z) => raiz.contains(z) || z.contains(raiz));
    for (const zona of zonas) {
      const base = zona.contains(raiz) ? raiz : zona;
      const todos = [base, ...base.querySelectorAll("*")];
      const hechos = new Set();
      for (const el of todos) {
        if (!(el instanceof Element)) continue;
        traducirAtributos(el);
        if ([...hechos].some((h) => h.contains(el))) continue;
        if (el.dataset.tr === estado.lang && puesto.get(el) === el.innerHTML) { hechos.add(el); continue; }
        if (esBloque(el)) { traducirBloque(el); hechos.add(el); } else if (!el.closest("[data-no-traducir]")) traducirTextos(el);
      }
    }
  }

  // ---------- Volver a traducir lo que la página redibuja (planeador, qué hacer, aviso…) ----------
  let pendiente = false;
  const obs = new MutationObserver((cambios) => {
    if (estado.lang === "es" || pendiente) return;
    pendiente = true;
    requestAnimationFrame(() => {
      pendiente = false;
      obs.disconnect();
      for (const c of cambios) if (c.target.isConnected) recorrer(c.target instanceof Element ? c.target : c.target.parentElement);
      obs.observe(document.body, { childList: true, subtree: true });
    });
  });

  function cargar(lang) {
    if (lang === "es" || window.IDIOMAS_TRAD[lang]) return Promise.resolve();
    return estado.cargando[lang] || (estado.cargando[lang] = new Promise((ok, mal) => {
      const s = document.createElement("script");
      s.src = `idiomas/${lang}.js`; s.onload = ok; s.onerror = mal;
      document.head.appendChild(s);
    }));
  }

  async function poner(lang) {
    await cargar(lang).catch(() => { lang = "es"; });
    estado.lang = lang;
    estado.dic[lang] = (window.IDIOMAS_TRAD[lang] || {}).frases || {};
    if (lang !== "es") Object.entries((window.IDIOMAS_TRAD[lang] || {}).lugares || {}).forEach(([es, tr]) => {
      estado.lugares[es] = { ...(estado.lugares[es] || {}), [lang]: tr };
    });
    document.documentElement.lang = lang;
    obs.disconnect();
    if (lang === "es") {
      document.querySelectorAll("[data-es]").forEach((el) => { el.innerHTML = el.dataset.es; puesto.set(el, el.innerHTML); delete el.dataset.tr; });
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let h = w.nextNode(); h; h = w.nextNode()) if (h.__es !== undefined) { h.textContent = h.__es; textoPuesto.set(h, h.textContent); }
      ATRIBUTOS.forEach((a) => {
        const k = `es${a.replace(/-./g, (x) => x[1].toUpperCase())}`;
        document.querySelectorAll(`[data-${k.replace(/[A-Z]/g, (x) => "-" + x.toLowerCase())}]`).forEach((el) => el.setAttribute(a, el.dataset[k]));
      });
    } else {
      recorrer(document.body);
      obs.observe(document.body, { childList: true, subtree: true });
    }
    try { localStorage.setItem("idioma", lang); } catch (e) { /* solo esta visita */ }
    document.dispatchEvent(new CustomEvent("idioma", { detail: lang }));
  }

  // ---------- Selector (globo en la barra) ----------
  function selector() {
    const caja = document.getElementById("idioma");
    if (!caja) return;
    const visibles = IDIOMAS.filter((x) => !x.enRevision);
    caja.innerHTML = `<button type="button" class="idioma-boton" aria-haspopup="listbox" aria-expanded="false" aria-label="Idioma / Language">
        <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3Z" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>
        <span class="idioma-codigo">ES</span></button>
      <ul class="idioma-lista" role="listbox" aria-label="Idioma" hidden>${visibles.map((x) =>
        `<li role="option" tabindex="-1" data-lang="${x.c}" lang="${x.c}" aria-selected="false">${x.n}</li>`).join("")}</ul>`;
    const boton = caja.querySelector("button"), lista = caja.querySelector("ul"), opciones = [...lista.children];
    const abrir = (si) => { lista.hidden = !si; boton.setAttribute("aria-expanded", si); caja.classList.toggle("abierto", si); if (si) (opciones.find((o) => o.dataset.lang === estado.lang) || opciones[0]).focus(); };
    const marcar = () => {
      caja.querySelector(".idioma-codigo").textContent = estado.lang.toUpperCase();
      opciones.forEach((o) => o.setAttribute("aria-selected", o.dataset.lang === estado.lang));
    };
    boton.addEventListener("click", () => abrir(lista.hidden));
    opciones.forEach((o) => {
      o.addEventListener("click", () => { abrir(false); boton.focus(); poner(o.dataset.lang).then(marcar); });
      o.addEventListener("keydown", (e) => {
        const i = opciones.indexOf(o);
        if (e.key === "ArrowDown") { opciones[(i + 1) % opciones.length].focus(); e.preventDefault(); }
        if (e.key === "ArrowUp") { opciones[(i - 1 + opciones.length) % opciones.length].focus(); e.preventDefault(); }
        if (e.key === "Enter" || e.key === " ") { o.click(); e.preventDefault(); }
        if (e.key === "Escape") { abrir(false); boton.focus(); }
      });
    });
    document.addEventListener("click", (e) => { if (!caja.contains(e.target)) abrir(false); });
    document.addEventListener("idioma", marcar);
    marcar();
  }

  window.Idiomas = {
    lista: IDIOMAS, poner, normalizar,
    traducirTexto: (x) => traducir(x),  // para el chat: la pregunta en el idioma elegido (null si es español)
    // Para armar los diccionarios: todas las frases normalizadas que hoy se ven en la parte del viajero.
    claves() {
      const salida = new Set();
      ZONAS.flatMap((z) => [...document.querySelectorAll(z)]).forEach((zona) => {
        const hechos = new Set();
        [zona, ...zona.querySelectorAll("*")].forEach((el) => {
          ATRIBUTOS.forEach((a) => { const v = el.getAttribute && el.getAttribute(a); if (v && /[A-Za-zÁÉÍÓÚáéíóú]/.test(v)) salida.add(normalizar(v).clave); });
          if ([...hechos].some((h) => h.contains(el))) return;
          if (esBloque(el)) {
            hechos.add(el);
            const t = simplificar({ innerHTML: el.dataset.es ?? el.innerHTML }).html.trim();
            const solo = t.replace(/\{x\d+\}/g, "").replace(/<[^>]+>/g, "");
            if (/[A-Za-zÁÉÍÓÚáéíóúÑñ]/.test(solo) && CORTOS_ES.indexOf(t.toUpperCase()) < 0) salida.add(normalizar(t).clave);
          } else if (!el.closest("[data-no-traducir]")) {
            el.childNodes.forEach((h) => { if (h.nodeType === 3 && /[A-Za-zÁÉÍÓÚáéíóúÑñ]/.test(h.textContent)) salida.add(normalizar(h.__es ?? h.textContent).clave); });
          }
        });
      });
      return [...salida];
    },
    registrarLugares(lista) { lista.forEach((x) => { estado.lugares[x] = estado.lugares[x] || {}; }); },
  };

  document.addEventListener("DOMContentLoaded", () => {
    selector();
    let inicial = "es";
    try { inicial = localStorage.getItem("idioma") || (navigator.language || "es").slice(0, 2); } catch (e) { /* nada */ }
    if (!IDIOMAS.some((x) => x.c === inicial && !x.enRevision)) inicial = "es";
    // Espera a que app.js termine de dibujar (corre al final del body) antes de traducir.
    if (inicial !== "es") requestAnimationFrame(() => poner(inicial));
  });
})();
