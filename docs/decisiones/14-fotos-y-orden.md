# 14 — Fotos comprobadas de los 5 lugares y una página que empieza por el viaje

Autor: **Brandon Uriel García Sánchez** · 01-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Qué pidió Brandon
> pero que sean fotos de las zonas que si sean de quintana rooo y te di el grafo para que supieras el contexto de todo y
> no lo pierdas. Leelo y dime que show, tambien necesito foto dependiendo que escojan. Y quiero primero hasta arriba en el
> inicio donde escojas como el plan de viaje

> Tambien reestructura la pagina en las secciones tienes primero los datos y luego lo demás, yo diria todo como el plan
> el marketing, las reseñas, los hoteles hospedaje el dia noche y tarde como toda la pagina y luego al final o en otra
> seccion donde cliqueas esten los datos y ese pedo

## Qué estaba mal (y por qué)
La galería de platillos (decisión 13) usaba fotos de **Mérida, Campeche, Oxkutzcab y otros lugares fuera de Quintana
Roo**. Solo se había filtrado que no mencionaran lugares excluidos. Eso rompía dos reglas que el grafo del proyecto tenía
anotadas:
- la **ubicación comprobada** de `docs/decisiones/06-pagina.md`: cada foto debe tener coordenada dentro del municipio del
  lugar;
- la **regla de oro 9**: solo los 5 lugares.

**Corrección:** la galería de platillos se **retiró por completo** (fotos, código y pruebas).

## Decisión 1 — Solo fotos con coordenada comprobada en el municipio del lugar
- `backend/torre/campana/fotos_lugares.py` baja de Wikimedia Commons de 4 a 6 fotos por lugar, **28 en total**.
- Exige que cada una tenga **coordenada GPS** y que esa coordenada caiga en el polígono oficial de su municipio:
  Othón P. Blanco o Felipe Carrillo Puerto. Usa la misma función `municipio_de()` que validó los lugares.
- Si una foto no cumple, el proceso se detiene.
- Búsqueda: se buscaron fotos alrededor de cada pueblo del Censo 2020 y de las zonas arqueológicas. Salieron 331 fotos con
  coordenada dentro de los municipios, y de ellas se eligieron 28 revisándolas a ojo.
- **Rechazadas**, entre otras:
  - fotos de "Kohunlich" con coordenada en Felipe Carrillo Puerto, a más de 100 km (la coordenada está mal);
  - fotos satelitales;
  - insectos;
  - una serpiente en una cueva cuya coordenada no coincide con Kantemó.
- **Hueco declarado:** en Commons **no hay fotos de platillos tomadas en los 5 lugares**. De las 331 fotos con coordenada,
  0 son de comida; las que mencionaban comida eran fachadas de restaurantes. Se muestran esas fotos reales, por ejemplo
  el restaurante Bahía Villamar en Chetumal y los restaurantes de Calderitas. Fotos de platillos del sur requieren fotos
  propias o un permiso.
- Peso: 1,400 px, con calidad adaptable para quedar bajo 400 KB cada una (6.4 MB en total). Solo se descarga la foto que
  se ve.

## Decisión 2 — Foto según el lugar elegido
- La foto de la portada cambia con el lugar que se elige, con un fundido entre dos capas.
- Debajo, "Así se ve…" muestra todas las fotos de ese lugar.
- Cada foto lleva su crédito (autor y licencia), como pide la licencia.

## Decisión 3 — La página empieza por el viaje y termina con los datos
**Nuevo orden**

| Para el viajero (arriba) | Los datos (al final) |
|---|---|
| 1. Portada-planeador: elegir lugar y mes, con la foto del lugar | 6. Banda "Los datos", con enlaces a cada sección |
| 2. Así va a estar: temporada, gente esperada, clima, tormenta, recomendación y fotos del lugar | 7. El dato, el problema, el Radar |
| 3. Qué hacer de día, tarde y noche; dónde comer y dónde dormir | 8. Cómo llega la gente, el dinero, el norte |
| 4. Los cinco lugares (mapa 3D) | 9. Las fases, con datos oficiales, quiénes somos |
| 5. La campaña (se llena en la Fase 8) | |

- **Menú:** Planea tu viaje · Qué hacer · Los lugares · Los datos · Quiénes somos.
- **Datos al final, en la misma página.** Se eligió así, en lugar de una página aparte, para que nada se rompa: el mapa
  3D y las animaciones necesitan estar en la página.

**Reseñas: hueco declarado.** Las únicas reseñas con licencia que se pueden usar (Rest-Mex 2025) **no cubren ninguno de
los 5 lugares**; solo Tulum, Isla Mujeres y Bacalar. Mostrar reseñas sería inventarlas, así que no se muestran.

## Evidencia
- `tests/test_fotos_lugares.py` tiene 5 pruebas:
  - 28 fotos de los 5 lugares;
  - **cada coordenada cae en su municipio**;
  - huellas intactas y menos de 450 KB cada una;
  - licencia libre y crédito;
  - ninguna foto de fuera.

  La prueba de peso detectó una foto de 510 KB, y por eso se agregó la calidad adaptable.
- La revisión en navegador, en escritorio y en celular, terminó sin errores. La foto y la galería cambian al elegir otro
  lugar.
