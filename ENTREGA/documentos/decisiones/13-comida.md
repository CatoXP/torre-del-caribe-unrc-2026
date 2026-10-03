# 13 — La comida del sur: fotos de platillos en la página · RETIRADA

> **Retirada el 01-oct-2026** (`14-fotos-y-orden.md`). Las fotos eran de Mérida, Campeche y otros lugares fuera de
> Quintana Roo: rompían la ubicación comprobada (decisión 06) y la regla de oro 9. Se conserva esta nota como registro
> del error y de cómo se corrigió.

Autor: **Brandon Uriel García Sánchez** · 01-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Qué pidió Brandon
> Agrega muchisimas fotos de todo la comida de la vista nace el amor sabes

## Qué se hizo
- **Sección nueva "La comida del sur"** (`#comida`), con el título "De la vista nace el amor".
  - Mosaico de **24 platillos** de la península de Yucatán, cada uno con su nombre, una descripción corta y el crédito
    de la foto.
  - Filtros: del mar, cocina yucateca, antojitos, para beber y de postre.
  - Va en rosa mexicano, con texto blanco: el blanco sobre rosa tiene contraste 4.58:1 y pasa el mínimo de 4.5:1.
- **"Se te va a antojar"** en cada bloque de "Qué hacer", con cuatro fotos del tipo de comida de ese momento:
  - de día, bebidas, café y postres;
  - por la tarde, mar y cocina yucateca;
  - de noche, antojitos.

## De dónde salen las fotos (regla de oro 4)
- Todas son de **Wikimedia Commons**, con licencia libre: CC BY, CC BY-SA o CC0. Se bajaron con su API oficial
  (`backend/torre/campana/fotos_comida.py`).
- La licencia exige citar al autor y la licencia, así que **cada foto lleva su crédito en la página**.
- El programa se detiene si una foto no existe, tiene licencia restrictiva o menciona un lugar excluido.
- Se guardan a 1,000 px (2.6 MB en total), con huella SHA-256 en `frontend/fotos/comida/creditos.json`.
- **Opción descartada:** fotos de Google o TripAdvisor (prohibido por sus términos y por la regla 4).

## Cómo se eligieron (revisión a ojo)
La búsqueda automática en Commons trae ruido. Cada candidata se revisó en hojas de contacto antes de entrar. Se
**rechazaron**, entre otras:
- "Relleno negro": la búsqueda trajo **alfajores argentinos**. El relleno negro real salió de otra búsqueda.
- **Ceviches** de Perú, Israel y Brasil; **escabeches** de Filipinas, del País Vasco y de Argentina.
- **Tamales** de Venezuela (hallacas) y de Filipinas; **cocos** de Filipinas; **elotes** de Xochimilco; un
  **supermercado peruano**.
- Fotos de **restaurantes de Estados Unidos**.

También quedó fuera toda foto cuyo título, descripción o categorías mencionen Tulum, Cancún, Playa del Carmen, Cozumel,
Holbox, Isla Mujeres, Bacalar, Mahahual, Riviera Maya o Cobá (regla de oro 9).

## Lo que se declara
- Son **fotos de referencia del platillo**, tomadas en Mérida, Campeche, Oxkutzcab, Quintana Roo y otros lugares. **No
  son de los negocios del DENUE** que lista "Qué hacer", y la página lo dice.
- Las descripciones son cortas y generales: qué lleva cada platillo. No son cifras ni datos del proyecto.

## Los 24 platillos

| Grupo | Platillos |
|---|---|
| Del mar | Pescado tikin xic, pan de cazón, cóctel de camarones, vuelve a la vida, pescado frito |
| Cocina yucateca | Cochinita pibil, relleno negro, poc chuc, papadzules (foto tomada en Quintana Roo), sopa de lima, queso relleno, mucbipollo, frijol con puerco, chile habanero |
| Antojitos | Tacos de cochinita, panuchos, salbutes, empanadas, tamal en hoja de plátano, tacos al pastor |
| Para beber y de postre | Marquesitas, horchata, agua de chaya con piña, café de olla |

## Evidencia
- `tests/test_fotos_comida.py` tiene 5 pruebas: 24 fotos, huellas intactas, menos de 300 KB cada una, licencia libre
  con crédito completo, y ningún lugar excluido.
- La revisión en navegador (escritorio y celular) terminó sin errores. Los 24 platillos tienen crédito y no hay imágenes
  rotas.

**Ajuste que trajo esta pieza.** Con 8 secciones, el menú superior ya no cabía en una línea a 1,280 px. Ahora los
enlaces son más compactos, y por debajo de 1,240 px se usa el botón "Menú".

## Consecuencia
La comida se vuelve una razón visible para ir al sur. Las fotos y sus créditos quedan listos para las piezas
publicitarias de la Fase 8.
