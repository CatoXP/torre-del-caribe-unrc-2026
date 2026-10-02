# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos (API, Fase 9)
# Qué hace:          Servidor FastAPI que conecta la página con los modelos (plan B.5). Sirve la página y estos endpoints:
#                    GET  /api/salud        ¿está vivo el servidor? (la página lo pregunta antes de mostrar controles)
#                    GET  /api/radar        estado de hoy y del mes siguiente (A1)
#                    GET  /api/pronostico   calendario lugar × mes (A3); ?lugar= para filtrar
#                    GET  /api/escenarios   Monte Carlo malo/probable/bueno (A3); ?lugar= y ?golpe=
#                    POST /api/optimizar    RESUELVE el modelo de la Fase 6 con los supuestos que manda la página (< 2 s)
#                    GET  /api/stream       la Torre semana a semana como Server-Sent Events (A5); ?ms= ritmo
#                    GET  /api/campana      la campaña "El sur tiene espacio" (Fase 8)
#                    GET  /api/consulta     una consulta SQL de SOLO LECTURA al almacén DuckDB; ?sql=
# Por qué así:       - El plan pide que el backend calcule, no que sirva archivos fijos: /api/optimizar resuelve el MILP en
#                      vivo (0.3 s medidos) y /api/stream transmite la reproducción de la Fase 7.
#                    - Solo escucha en 127.0.0.1: es para la computadora del proyecto y el coloquio, no para internet. La
#                      página publicada en GitHub Pages sigue funcionando sin servidor (usa pagina.js).
#                    - La consulta es de solo lectura (conexión read_only) y además rechaza funciones que leen archivos o
#                      cambian la base: el almacén solo se consulta por sus vistas.
#                    - Alternativa descartada: Flask (sin validación de tipos ni documentación automática en /docs).
# Datos de entrada:  datos/gold/* (salidas de todas las fases) y frontend/.
# Alimenta a:        La página en localhost (controles de presupuesto y Torre en vivo) y el coloquio.
#
# Uso:  cd backend && ..\.venv\Scripts\python -m torre.api.servidor   → http://127.0.0.1:8000

import asyncio
import json
import re
import time

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from torre.base.entorno import RAIZ

GOLD = RAIZ / "datos" / "gold"
FRONT = RAIZ / "frontend"
LIMITE_FILAS = 1000
PROHIBIDO = re.compile(r"(?i)\b(read_\w+|glob|attach|detach|copy|install|load|pragma|set|export|import|create|insert|"
                       r"update|delete|drop|alter|call|checkpoint|vacuum)\b|;.+\S")

app = FastAPI(title="Torre del Caribe", version="1.0",
              description="Radar (A1), Pronóstico (A3), Torre en vivo (A5), presupuesto (IO) y campaña.")


def _registros(df: pd.DataFrame) -> list[dict]:
    return json.loads(df.to_json(orient="records", date_format="iso", force_ascii=False))


def _gold(nombre: str) -> pd.DataFrame:
    ruta = GOLD / f"{nombre}.parquet"
    if not ruta.exists():
        raise HTTPException(503, f"Falta {ruta.name}: corre primero la fase que lo genera")
    return pd.read_parquet(ruta)


@app.get("/api/salud")
def salud() -> dict:
    return {"ok": True, "almacen": (GOLD / "torre.duckdb").exists()}


@app.get("/api/radar")
def radar() -> dict:
    from torre.api.datos_pagina import radar as radar_pagina
    r = radar_pagina()
    if r is None:
        raise HTTPException(503, "El Radar (Fase 4) aún no tiene salidas")
    return r


@app.get("/api/pronostico")
def pronostico(lugar: str | None = None) -> list[dict]:
    c = _gold("pronostico_calendario")
    if lugar:
        c = c[c.lugar == lugar]
    return _registros(c)


@app.get("/api/escenarios")
def escenarios(lugar: str | None = None, golpe: float = Query(0.0, ge=0, le=0.5)) -> list[dict]:
    e = _gold("pronostico_escenarios")
    e = e[e.golpe_tormenta_supuesto == golpe]
    if lugar:
        e = e[e.lugar == lugar]
    return _registros(e)


class Pedido(BaseModel):
    """Lo que la página puede mover. Los límites evitan pedir algo sin sentido (y que el modelo tarde)."""
    presupuesto_anual: float = Field(250_000, ge=10_000, le=10_000_000)
    cvr_facebook: float | None = Field(None, ge=0.005, le=0.2)
    piso_equidad: float = Field(0.15, ge=0, le=0.33)
    tope_canal: float = Field(0.70, ge=0.5, le=1.0)
    temporada_alta: bool = True
    capacidad: bool = True


@app.post("/api/optimizar")
def optimizar(p: Pedido) -> dict:
    from torre.campana.presupuesto import SUR, Supuestos, resolver
    inicio = time.perf_counter()
    sol = resolver(Supuestos(**p.model_dump(), nombre="Página"))
    ms = round((time.perf_counter() - inicio) * 1000)
    if sol["estado"] != "Optimal":
        return {"estado": sol["estado"], "ms": ms}
    plan = sol["plan"]
    B = sol["presupuesto"]
    lug = plan.groupby("lugar").pesos.sum()
    can = plan.groupby("canal").pesos.sum()
    return {"estado": "Optimal", "ms": ms, "presupuesto_periodo": round(B), "meses": len(sol["meses"]),
            "visitantes": round(sol["visitantes_esperados"], 1),
            "pesos_por_visitante": round(B / sol["visitantes_esperados"]) if sol["visitantes_esperados"] else None,
            "lugares": {l: round(float(lug.get(l, 0)) / B * 100, 1) for l in SUR},
            "canales": {c: round(float(v) / B * 100, 1) for c, v in can.items()}}


@app.get("/api/stream")
async def stream(ms: int = Query(150, ge=20, le=2000)) -> StreamingResponse:
    """Server-Sent Events: un evento por semana de la reproducción de la Fase 7, al ritmo pedido."""
    d = _gold("envivo_decisiones")
    n = _gold("envivo_norte").set_index("semana")

    async def eventos():
        for i, (sem, g) in enumerate(d.groupby("semana", sort=True)):
            dato = {"i": i, "semana": f"{sem:%Y-%m-%d}",
                    "lugares": {r.lugar: {"accion": r.accion, "motivo": r.motivo} for r in g.itertuples()},
                    "ibas_al_norte": n.loc[sem, "destino"] if bool(n.loc[sem, "ibas_al_norte"]) else None}
            yield f"data: {json.dumps(dato, ensure_ascii=False)}\n\n"
            await asyncio.sleep(ms / 1000)
        yield "event: fin\ndata: {}\n\n"

    return StreamingResponse(eventos(), media_type="text/event-stream")


@app.get("/api/campana")
def campana() -> dict:
    ruta = GOLD / "campana.json"
    if not ruta.exists():
        raise HTTPException(503, "La campaña (Fase 8) aún no se arma")
    return json.loads(ruta.read_text(encoding="utf-8"))


def sql_permitido(sql: str) -> bool:
    """Solo un SELECT (o WITH … SELECT) sobre las vistas del almacén; nada que lea archivos o cambie la base."""
    s = sql.strip().rstrip(";")
    return bool(re.match(r"(?is)^(select|with)\b", s)) and not PROHIBIDO.search(s)


@app.get("/api/consulta")
def consulta(sql: str = Query(..., max_length=2000)) -> dict:
    import duckdb
    if not sql_permitido(sql):
        raise HTTPException(400, "Solo se permite un SELECT sobre las vistas del almacén")
    with duckdb.connect(str(GOLD / "torre.duckdb"), read_only=True) as con:
        try:
            df = con.execute(f"SELECT * FROM ({sql.strip().rstrip(';')}) LIMIT {LIMITE_FILAS + 1}").df()
        except duckdb.Error as e:
            raise HTTPException(400, f"Error de SQL: {e}") from e
    return {"filas": _registros(df.head(LIMITE_FILAS)), "recortado": len(df) > LIMITE_FILAS}


# La página va al final para que /api/* tenga prioridad.
app.mount("/", StaticFiles(directory=str(FRONT), html=True), name="pagina")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
