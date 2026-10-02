# Autor: Brandon Uriel García Sánchez
# Módulo: Torre en vivo (A5, Fase 7)
# Qué hace:          Motor de reglas de la Torre: con las señales de una semana decide, para cada lugar del sur, si su
#                    anuncio se enciende, se pausa o no toca (temporada alta / fuera del plan), cuánto dinero se gasta y
#                    cuánto pasa a la siguiente semana; y si se enciende "¿Ibas al norte?" y hacia qué lugar del sur.
# Por qué así:       Reglas elegidas por Brandon el 02-oct-2026 (docs/decisiones/20-torre-en-vivo.md):
#                    - Sur: tormenta cerca, clima raro en su punto o llegadas del mes anterior por ARRIBA del rango del
#                      90 % → se PAUSA esa semana y su dinero se guarda para la siguiente semana permitida (etapa 2 del
#                      modelo de la Fase 6). Descartadas: bajar a la mitad (se anunciaría con mal clima) y solo avisar.
#                    - Norte: si Cancún o Riviera Maya están "saturados" (≥ p90 del Radar) se enciende "¿Ibas al norte?"
#                      hacia el lugar del sur encendido con más espacio libre ese mes. Nunca se anuncia el norte.
#                    - Llegadas por DEBAJO del rango no pausan: hay espacio, que es lo que la campaña busca.
#                    - Sin dato de tormentas (2026) no es "sin tormenta": la semana se anota, pero no pausa (no hay
#                      evidencia para pausar) y la página lo dice.
#                    Funciones puras (sin Spark ni archivos) para poder probarlas una por una.
# Datos de entrada:  Una fila de torre.envivo.senales + el plan mensual de la Fase 6 (datos/gold/presupuesto_plan).
# Alimenta a:        torre.envivo.torre (la reproducción semana a semana) y la página.

from dataclasses import dataclass, field

import pandas as pd

from torre.envivo.senales import CLAVE, PUNTO_DE

SUR = list(CLAVE)


@dataclass
class Plan:
    """Lo que la Fase 6 dejó decidido, por mes del año (1–12) y lugar."""
    pesos_mes: dict          # (mes, lugar) → pesos del mes
    alta: set                # {(mes, lugar)} en temporada alta
    libre: dict              # (mes, lugar) → fracción libre de la capacidad (escenario probable)


@dataclass
class Memoria:
    """Lo que la Torre recuerda de una semana a la siguiente: el dinero pausado que todavía no se gasta."""
    arrastre: dict = field(default_factory=lambda: {l: 0.0 for l in SUR})


def lunes_del_mes(semana: pd.Timestamp) -> int:
    """Cuántos lunes tiene el mes de esa semana (para repartir el dinero del mes en semanas)."""
    dias = pd.date_range(semana.replace(day=1), semana + pd.offsets.MonthEnd(0), freq="D")
    return int((dias.weekday == 0).sum())


def motivos_pausa(fila: dict, lugar: str) -> list[str]:
    clave, punto = CLAVE[lugar], PUNTO_DE[lugar]
    m = []
    if fila.get("tormenta") is True:
        m.append(f"tormenta cerca ({fila.get('tormenta_nombre')})")
    if fila.get(f"{punto}_clima_raro") is True:
        m.append(f"clima raro ({fila.get(f'{punto}_lluvia_mm', 0):.0f} mm de lluvia en la semana)")
    if fila.get(f"{clave}_llegadas") == "arriba":
        mes = pd.Timestamp(fila.get(f"{clave}_mes_dato"))
        m.append(f"llegó más gente de la esperada en {mes:%m/%Y}")
    return m


def decidir(fila: dict, plan: Plan, memoria: Memoria) -> tuple[list[dict], dict]:
    semana = pd.Timestamp(fila["semana"])
    mes = semana.month
    decisiones = []
    for lugar in SUR:
        base = {"semana": semana, "lugar": lugar, "pesos_plan": 0.0, "pesos_gastados": 0.0, "motivo": None}
        if (mes, lugar) in plan.alta:
            d = base | {"accion": "temporada alta"}
        elif (mes, lugar) not in plan.pesos_mes:
            d = base | {"accion": "fuera del plan"}
        else:
            semanal = plan.pesos_mes[mes, lugar] / lunes_del_mes(semana)
            motivos = motivos_pausa(fila, lugar)
            if motivos:
                memoria.arrastre[lugar] += semanal
                d = base | {"accion": "pausado", "pesos_plan": semanal, "motivo": "; ".join(motivos)}
            else:
                gasto = semanal + memoria.arrastre[lugar]
                memoria.arrastre[lugar] = 0.0
                d = base | {"accion": "encendido", "pesos_plan": semanal, "pesos_gastados": gasto}
        d["arrastre"] = memoria.arrastre[lugar]
        d["sin_dato_tormentas"] = fila.get("tormenta") is None
        decisiones.append(d)
    # Norte: "¿Ibas al norte?" hacia el lugar del sur encendido con más espacio.
    llenos = [n for n, c in (("Cancún", "cancun"), ("Riviera Maya", "riviera")) if fila.get(f"{c}_estado") == "saturado"]
    encendidos = [d["lugar"] for d in decisiones if d["accion"] == "encendido"]
    destino = max(encendidos, key=lambda l: plan.libre.get((mes, l), 0)) if (llenos and encendidos) else None
    norte = {"semana": semana, "norte_lleno": ", ".join(llenos) or None, "ibas_al_norte": destino is not None,
             "destino": destino, "cancun_pct": fila.get("cancun_ocupacion_pct"), "riviera_pct": fila.get("riviera_ocupacion_pct")}
    return decisiones, norte


def plan_desde_gold(plan: pd.DataFrame, tabla: pd.DataFrame) -> Plan:
    """Convierte las salidas de la Fase 6 en reglas por mes del año."""
    p = plan.assign(mes=pd.to_datetime(plan.periodo).dt.month).groupby(["mes", "lugar"]).pesos.sum()
    t = tabla.assign(mes=pd.to_datetime(tabla.periodo).dt.month)
    alta = {(r.mes, r.lugar) for r in t.itertuples() if r.nivel == "alta"}
    pesos = {k: float(v) for k, v in p.items() if k not in alta}
    libre = {(r.mes, r.lugar): float(r.libre) for r in t.itertuples()}
    return Plan(pesos, alta, libre)
