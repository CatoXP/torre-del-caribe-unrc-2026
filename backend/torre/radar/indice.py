# Autor: Brandon Uriel García Sánchez
# Módulo: Radar
# Qué hace:          Pieza 2 de la Fase 4. Con el panel mensual calcula el índice de presión turística (IPT) de cada
#                    lugar y mes, lo traduce a tranquilo / concurrido / saturado y mide qué tanto cambia el resultado si
#                    se mueven los pesos (sensibilidad).
# Por qué así:       Tres decisiones de Brandon (docs/decisiones/08-radar.md):
#                    1) Pesos iguales, con sensibilidad ±50 % (descartados: componentes principales, criterio del equipo).
#                    2) Cortes por percentiles comunes a todo el estado: p50 y p90 del IPT de todos los lugares y meses
#                       juntos (descartados: terciles de cada lugar, k-means).
#                    3) Escala mín–máx (29-sep-2026; descartados: percentil común y mín–máx sobre logaritmo). Riesgo
#                       declarado: con colas largas, la mediana de visitantes INAH por mil habitantes queda en 0.02 de la
#                       escala y la de ocupación en 0.70, así que un lugar puede salir más alto solo por tener ocupación.
#                       Por eso cada fila guarda con qué componentes se calculó y la sensibilidad lo mide.
#                    Las llegadas se dividen entre la población (por mil habitantes) para que un pueblo y una ciudad se
#                    comparen en la misma escala: 1,000 visitantes pesan más en Nicolás Bravo que en Chetumal.
# Datos de entrada:  datos/gold/radar_panel_mensual.parquet (panel.py).
# Alimenta a:        Campaña: un lugar "saturado" no se promueve ese mes; uno "tranquilo" es candidato a anuncio. Y a la
#                    predicción del estado del mes siguiente (pieza 3).

from pathlib import Path

import numpy as np
import pandas as pd

from torre.radar.panel import GOLD, LUGARES_5, panel_mensual

# Componentes del índice: todas miden presión (demanda que llega). Las llegadas van por mil habitantes.
# Regla (opción D de Brandon, 29-sep-2026): un componente entra a la escala común solo si lo tienen al menos
# MIN_LUGARES lugares; si lo tiene uno solo, su mín–máx lo compara contra sí mismo. Así sale "cruces_belice" (solo
# Chetumal): con él, Chetumal quedaba en 0.44 en 2025, arriba de Cancún (0.28), porque la mediana de Belice cae en 0.74
# de su propia escala. Belice sigue en el panel y en la página; solo no entra al índice.
LLEGADAS = ["llegadas_tren", "cruceristas", "cruces_belice", "visitantes_inah"]
# Llegadas por cuarto de hotel (auditoría del 29-sep-2026, decisión de Brandon): el plan pedía medir la presión contra la
# capacidad de hospedaje. Se calcula como (Tren Maya + cruceristas) ÷ cuartos del lugar ese mes. La "densidad de oferta"
# (negocios DENUE por mil habitantes) NO entra: es un solo corte en el tiempo y no puede señalar un mes más lleno que otro.
CANDIDATOS = [f"{v}_x1000hab" for v in LLEGADAS] + ["llegadas_x_cuarto", "ocupacion_pct"]
MIN_LUGARES = 2
CORTES = (0.50, 0.90)  # percentiles comunes: debajo de p50 tranquilo; de p50 a p90 concurrido; arriba de p90 saturado


def componentes(panel: pd.DataFrame) -> pd.DataFrame:
    """x_k de cada lugar y mes: llegadas por mil habitantes y ocupación (%). Sin dato → nulo (no se rellena)."""
    c = panel[["lugar", "es_de_los_5", "periodo"]].copy()
    for v in LLEGADAS:
        c[f"{v}_x1000hab"] = panel[v] / panel.poblacion * 1000
    # min_count=1: si el lugar no tiene ni tren ni crucero ese mes, queda nulo (no 0); si tiene uno, cuenta ese.
    llegadas = panel[["llegadas_tren", "cruceristas"]].astype(float).sum(axis=1, min_count=1)
    c["llegadas_x_cuarto"] = llegadas / panel.cuartos.astype(float)
    c["ocupacion_pct"] = panel.ocupacion_pct
    return c


def elegir_componentes(c: pd.DataFrame) -> list[str]:
    """Los candidatos que tienen dato en al menos MIN_LUGARES lugares (los demás no se pueden comparar contra nadie)."""
    return [k for k in CANDIDATOS if c.loc[c[k].notna(), "lugar"].nunique() >= MIN_LUGARES]


def minmax(c: pd.DataFrame, comps: list[str]) -> pd.DataFrame:
    """z_k = (x_k − mín_k) / (máx_k − mín_k), con mín y máx de TODOS los lugares y meses juntos (escala común)."""
    z = c[["lugar", "es_de_los_5", "periodo"]].copy()
    for k in comps:
        x = c[k].astype(float)
        z[f"z_{k}"] = (x - x.min()) / (x.max() - x.min())
    return z


def ipt(z: pd.DataFrame, comps: list[str], pesos: dict[str, float] | None = None) -> pd.DataFrame:
    """IPT = Σ w_k z_k / Σ w_k, solo con los componentes que el lugar tiene ese mes. Pesos iguales por omisión."""
    pesos = pesos or {k: 1.0 for k in comps}
    Z = z[[f"z_{k}" for k in comps]].to_numpy(dtype=float)
    W = np.array([pesos[k] for k in comps])
    hay = ~np.isnan(Z)
    suma_w = (hay * W).sum(axis=1)
    out = z[["lugar", "es_de_los_5", "periodo"]].copy()
    with np.errstate(invalid="ignore"):
        out["ipt"] = np.where(suma_w > 0, np.nansum(np.nan_to_num(Z) * W, axis=1) / suma_w, np.nan)
    out["n_componentes"] = hay.sum(axis=1)
    out["componentes"] = [", ".join(k for k, h in zip(comps, fila) if h) for fila in hay]
    return out


def estados(t: pd.DataFrame, cortes=CORTES) -> tuple[pd.DataFrame, tuple[float, float]]:
    """Cortes comunes: percentiles p50 y p90 del IPT de todos los lugares y meses con dato."""
    u50, u90 = np.nanquantile(t.ipt, cortes)
    t = t.copy()
    t["estado"] = np.select([t.ipt.isna(), t.ipt < u50, t.ipt <= u90], ["sin dato oficial", "tranquilo", "concurrido"],
                            default="saturado")
    return t, (float(u50), float(u90))


def calcular(pesos: dict[str, float] | None = None) -> tuple[pd.DataFrame, tuple[float, float], list[str]]:
    c = componentes(panel_mensual())
    comps = elegir_componentes(c)
    z = minmax(c, comps)
    t, cortes = estados(ipt(z, comps, pesos))
    base = c.merge(z, on=["lugar", "es_de_los_5", "periodo"]).merge(t, on=["lugar", "es_de_los_5", "periodo"])
    return base, cortes, comps


def sensibilidad(base: pd.DataFrame, comps: list[str]) -> pd.DataFrame:
    """Mueve el peso de cada componente a 0.5 y a 1.5 (los demás en 1) y cuenta cuántos lugar-mes cambian de estado."""
    z = base[["lugar", "es_de_los_5", "periodo", *[f"z_{k}" for k in comps]]]
    con_dato = base.estado != "sin dato oficial"
    filas = []
    for k in comps:
        for f in (0.5, 1.5):
            t, _ = estados(ipt(z, comps, {j: (f if j == k else 1.0) for j in comps}))
            cambia = (t.estado != base.estado) & con_dato
            filas.append({"componente": k, "factor_peso": f, "cambian_pct": round(100 * cambia.sum() / con_dato.sum(), 1),
                          "cambian_5_lugares": int((cambia & base.es_de_los_5).sum())})
    return pd.DataFrame(filas)


def guardar() -> Path:
    base, cortes, _ = calcular()
    salida = GOLD / "radar_estado.parquet"
    base.assign(corte_p50=cortes[0], corte_p90=cortes[1]).to_parquet(salida, index=False)
    return salida


if __name__ == "__main__":
    pd.set_option("display.width", 200, "display.max_columns", 20, "display.max_colwidth", 70)
    base, cortes, comps = calcular()
    ruta = guardar()
    print(f"{ruta}\nComponentes del índice: {comps} (fuera por tenerlos un solo lugar: {sorted(set(CANDIDATOS) - set(comps))})")
    print(f"Cortes comunes: p50 = {cortes[0]:.3f}, p90 = {cortes[1]:.3f}")
    print(base[base.estado != "sin dato oficial"].estado.value_counts().to_string())
    ultimo = base[base.ipt.notna()].periodo.max()
    print(f"\nÚltimo mes con índice: {ultimo:%Y-%m}")
    print(base[base.periodo == ultimo][["lugar", "ipt", "estado", "componentes"]].round(3).sort_values("ipt", ascending=False).to_string(index=False))
    print("\nIPT promedio por año:")
    print(base.assign(anio=base.periodo.dt.year).pivot_table(index="lugar", columns="anio", values="ipt").round(2).to_string())
    print("\nSensibilidad (peso ×0.5 y ×1.5):")
    print(sensibilidad(base, comps).to_string(index=False))
