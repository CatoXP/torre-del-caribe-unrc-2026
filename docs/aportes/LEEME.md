# Aportes del equipo: fotos y reseñas de los 5 lugares

Esta carpeta guarda el material **propio** del equipo para la sección "Lo que vivimos" de la página: fotos de la comida,
de los lugares y reseñas con estrellas. Mientras no haya ningún aporte, la sección no aparece.

## Por qué existe
- No hay fotos de platillos con licencia libre tomadas en los cinco lugares. En Wikimedia Commons hay 0.
- No hay reseñas con licencia de estos lugares: Rest-Mex no los cubre.
- Copiar reseñas o estrellas de Google o TripAdvisor está prohibido por sus términos (regla de oro 4).

Por eso se usa solo material del equipo o material con permiso (decisión 16).

## Cómo agregar un aporte
1. Si es una foto, guárdala en `docs/aportes/fotos/`. Si el celular guardó la ubicación, mejor: el programa revisa que
   se haya tomado en el municipio del lugar.
2. Agrega una entrada a `docs/aportes/aportes.json`:

```json
[
  {"tipo": "foto", "lugar": "Bahía Calderitas–Oxtankah", "archivo": "pescado_tikin_xic.jpg",
   "autor": "Nombre Apellido", "fecha": "2026-11-14", "texto": "Pescado tikin xic en Calderitas", "permiso": true},
  {"tipo": "resena", "lugar": "Ruta arqueológica del sur", "autor": "Nombre Apellido", "fecha": "2026-11-15",
   "estrellas": 5, "texto": "Subimos al Templo del Búho y no había nadie más.", "permiso": true}
]
```

3. Corre `cd backend && ..\.venv\Scripts\python -m torre.campana.aportes`. Te dice qué aportes quedaron listos y
   cuáles se rechazaron, con el motivo.
4. Regenera la página: `..\.venv\Scripts\python -m torre.api.datos_pagina`.

## Reglas
- `lugar` debe ser uno de los cinco lugares, escrito igual:
  - Chetumal
  - Bahía Calderitas–Oxtankah
  - Ruta arqueológica del sur
  - Maya Ka'an + Kantemó
  - Laguna Milagros–Xul-Ha
- `permiso: true` quiere decir que el autor aceptó que se publique. Si la foto es de otra persona, hace falta su permiso
  por escrito, y se guarda junto con la foto.
- Las **estrellas** (de 1 a 5) son la opinión de quien escribe. No son una calificación oficial, y la página lo dice.
- Nada inventado: si no fuiste, no escribes la reseña.
