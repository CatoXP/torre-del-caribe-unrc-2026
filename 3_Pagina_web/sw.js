/*
  Autor: Brandon Uriel García Sánchez
  Módulo: Campaña (aplicación de teléfono)
  Qué hace:          El "trabajador" de la aplicación (service worker): guarda en el teléfono la página, los datos, las
                     traducciones y las fuentes al instalarla, y cada foto la primera vez que se ve. Sin internet, la
                     aplicación abre igual con lo guardado.
  Por qué así:       Decisiones 33 y 35. Se registra solo en modo aplicación (app.js, aplicacion()). Lo propio (HTML, JS,
                     CSS, datos) se pide primero a la red para que una versión nueva llegue sola, y si no hay red se usa lo
                     guardado; las fotos y las fuentes no cambian, así que se toman de lo guardado primero (ahorra datos del
                     celular). Nunca se guarda nada de Firebase ni de Google: esas llamadas pasan directo (los corazones y
                     las solicitudes no deben quedarse viejos). Los videos tampoco: pesan mucho y sin red no hacen falta.
  Datos de entrada:  Los archivos de frontend/ que usa index.html.
  Alimenta a:        La aplicación sin internet.
*/
const CAJA = "torre-app-v2";
const BASE = ["./", "index.html", "estilos.css", "app.js", "manifest.webmanifest", "iconos/icono-192.png", "datos/pagina.js",
  "firebase-config.js", "vendor/pretext.js", "idiomas.js", "cotizar.js", "viaje.js", "fuentes/fuentes.css"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CAJA).then((c) => c.addAll(BASE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CAJA).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

const guardarCopia = (pedido, r) => { if (r && r.ok && r.type === "basic") { const copia = r.clone(); caches.open(CAJA).then((c) => c.put(pedido, copia)); } return r; };

self.addEventListener("fetch", (e) => {
  const pedido = e.request, url = new URL(pedido.url);
  if (pedido.method !== "GET" || url.origin !== self.location.origin) return;  // Firebase y Google: directo a la red
  if (/\/video\//.test(url.pathname)) return;  // los videos van directo a la red (pesan mucho)
  const fija = /\/(fotos|fuentes)\//.test(url.pathname) || /\.(jpe?g|png|webp|woff2)$/i.test(url.pathname);
  if (fija) {
    e.respondWith(caches.match(pedido, { ignoreSearch: true }).then((g) => g || fetch(pedido).then((r) => guardarCopia(pedido, r))));
  } else {
    e.respondWith(fetch(pedido).then((r) => guardarCopia(pedido, r)).catch(() => caches.match(pedido, { ignoreSearch: true })
      .then((g) => g || (pedido.mode === "navigate" ? caches.match("index.html", { ignoreSearch: true }) : undefined))));
  }
});
