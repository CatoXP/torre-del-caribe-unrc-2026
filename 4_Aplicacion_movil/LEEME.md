# La aplicación de teléfono

La aplicación **es la página de la campaña en "modo aplicación"**: el mismo diseño, las mismas secciones y el mismo
"Cotiza tu viaje", con una barra de pestañas abajo. Su trabajo es vender el viaje, así que no enseña las cifras de los
modelos (decisión 35).

## Cómo instalarla

| Teléfono | Cómo |
|---|---|
| **Android (APK)** | Copia `Torre_del_Caribe.apk` al teléfono, ábrelo y acepta "Instalar apps de orígenes desconocidos". |
| **Cualquier teléfono (iPhone o Android), desde el navegador** | Entra a https://catoxp.github.io/torre-del-caribe-unrc-2026/app/ y elige "Agregar a la pantalla de inicio". |
| **Sin teléfono** | Abre `3_Pagina_web/index.html?app` en el navegador de la computadora, con la vista de teléfono (F12 → ícono de teléfono). |

## Las pestañas

| Pestaña | Qué hace |
|---|---|
| **Inicio** | Eliges lugar y mes y te dice si es mes tranquilo o temporada alta; si está lleno, recomienda otro lugar del sur u otro mes. |
| **Descubre** | Fotos comprobadas del sur por lo que te gusta, con corazón para guardarlas. |
| **Cotiza** (al centro) | Cuentas tu viaje, recibes un plan con lugares reales y, si te gusta, pides tu cotización con un folio. |
| **Tu viaje** | Tus fotos guardadas y el mes más tranquilo para ir. |
| **Más** | Consejos, qué hacer, los lugares, cómo llegar y preguntas. |

Además: diez idiomas (las pestañas también se traducen) y modo noche. Funciona sin internet: al instalarla guarda la
página y los datos; sin conexión, el plan sale con nuestras reglas.

## Capturas

- `capturas/android/`: el APK instalado en un emulador de Android 14 (Pixel 6), usado con toques reales y en inglés (el
  idioma del teléfono).
- `capturas/telefono/`: las mismas pantallas en un teléfono de 390 × 844: Inicio, Descubre, Cotiza (formulario, plan y
  resumen), Tu viaje, el menú "Más" y el inicio de noche en inglés.

## Lo que declaramos

- El APK es de **depuración** (firmado con la llave de prueba de Android). Para Google Play hacen falta una llave propia y
  una cuenta de desarrollador.
- Dentro del APK, el plan sale con nuestras reglas, con los mismos datos. La protección contra abuso de Firebase
  (reCAPTCHA) no responde dentro de la vista web de Android, así que Gemini no se puede llamar. En la página y en la versión
  del navegador sí funciona. Los corazones y las solicitudes sí funcionan desde el APK.
- No hicimos pruebas con personas.
