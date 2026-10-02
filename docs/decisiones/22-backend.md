# 22 — Fase 9: el servidor que conecta la página con los modelos

Autor: **Brandon Uriel García Sánchez** · 02-oct-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## La pregunta
El plan (B.5 y Fase 9) pide una web real con un backend que **calcula**, no un tablero con archivos fijos. También pide
que el optimizador responda en menos de 2 segundos.

## Decisión
Servidor **FastAPI** (`backend/torre/api/servidor.py`) que sirve la página y 8 endpoints:

| Endpoint | Qué hace | Módulo |
|---|---|---|
| `GET /api/salud` | La página pregunta si hay servidor antes de mostrar controles | — |
| `GET /api/radar` | Estado de hoy y del mes siguiente | A1 |
| `GET /api/pronostico?lugar=` | Calendario lugar × mes | A3 |
| `GET /api/escenarios?lugar=&golpe=` | Monte Carlo malo/probable/bueno | A3 |
| `POST /api/optimizar` | **Resuelve en vivo** el modelo de la Fase 6 con los supuestos que manda la página | IO |
| `GET /api/stream?ms=` | La Torre semana a semana como *Server-Sent Events* | A5 |
| `GET /api/campana` | La campaña "El sur tiene espacio" | Fase 8 |
| `GET /api/consulta?sql=` | Un `SELECT` de **solo lectura** al almacén DuckDB (máximo 1,000 filas) | Fase 2 |

**Tres reglas de diseño**
1. **Dos formas de ver la página.**
   - En la computadora del proyecto, con `python -m torre.api.servidor` y la dirección http://127.0.0.1:8000, aparecen
     **"Pruébalo tú"**, para mover el presupuesto, la conversión, el tope por canal, el piso por lugar y la regla de
     temporada alta, y **"Escuchar en vivo"** en la Torre.
   - En GitHub Pages, o abriendo el archivo, la página **no pregunta nada** y sigue con `pagina.js`, sin llamadas a
     internet.
2. **Solo escucha en 127.0.0.1**, para la computadora del proyecto y el coloquio.
3. **La consulta no puede cambiar ni leer otra cosa.** La conexión es `read_only` y además se rechaza todo lo que no
   empiece con `SELECT`/`WITH` y cualquier función que lea archivos (`read_*`, `glob`) o cambie la base (`copy`,
   `attach`, `drop`…).

**Alternativas descartadas**
- Flask: no valida tipos ni documenta sola. FastAPI publica `/docs`.
- Servir la página desde GitHub Pages con un servidor en la nube: el proyecto debe correr sin internet y no hay
  presupuesto de alojamiento.

## Evidencia
- `tests/test_api.py` (6 pruebas):
  - la página se sirve;
  - filtros y rangos validados (422 si `golpe=0.9` o `tope_canal=0.2`);
  - `/api/optimizar` da 956.8 visitantes en **menos de 2 s**, y con el doble de dinero, el doble de visitantes (el
    modelo es lineal);
  - la transmisión arranca en la semana 2022-01-03;
  - la campaña responde;
  - la consulta da las 15 filas de `dim_lugar` y rechaza 6 intentos de escribir o leer archivos.
- **Navegador contra el servidor real:**
  - el modelo se resolvió en **274 ms**, y con $500,000, en 220 ms (1,914 visitantes);
  - "Escuchar en vivo" avanzó del 7-mar al 25-abr-2022;
  - sin errores ni peticiones externas.
- **Dependencia nueva:** `httpx==0.27.2`, solo para el cliente de pruebas, fijada en `requirements.txt`.

## Consecuencia
La Fase 9 queda **lista**. La página puede **calcular en vivo** frente al jurado. La Fase 10 (página final probada con
personas reales) necesita al equipo: alguien no técnico tiene que usar la página mientras se le observa.
