/* Configuración de Firebase (decisión 27): proyecto "Quintana Roo" del equipo (quintana-roo-3c2e8). Si este valor es
   null, la página NO se conecta a ningún sitio y los corazones solo se guardan en el navegador del visitante.
   No es secreta (Google la diseñó para ir en páginas públicas): la protegen las reglas de firebase/firestore.rules
   (torre.campana.nube). Sin measurementId: no usamos Google Analytics para no rastrear a los visitantes.
   appCheck: clave pública del sitio en Fraud Defense (antes reCAPTCHA Enterprise), clave "Torre del Caribe" con dominios
   catoxp.github.io y localhost. Con ella Gemini comprueba que la petición viene de nuestra página (decisión 28). */
window.TORRE_FIREBASE = {
  apiKey: "AIzaSyDbl8gLTgkquMdeKnEUwF-2enuAn-oPvQ8",
  authDomain: "quintana-roo-3c2e8.firebaseapp.com",
  projectId: "quintana-roo-3c2e8",
  storageBucket: "quintana-roo-3c2e8.firebasestorage.app",
  messagingSenderId: "645323500039",
  appId: "1:645323500039:web:d888da9b0328bbbd1358a2",
  appCheck: "6Lehv_ctAAAAAG7cO7hRKIJNMo-6BJY0HHbJroNF",
};
