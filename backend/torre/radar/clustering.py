# Autor: Brandon Uriel García Sánchez
# Módulo: Radar
# Qué hace:          Minería del Radar (punto del plan, Fase 4; agregado tras la auditoría del 29-sep-2026). Agrupa los
#                    centros turísticos del país que mide DataTur por su patrón de ocupación mensual (nivel y temporada)
#                    con clustering jerárquico, para ubicar a Cancún, la Riviera Maya y el resto de Quintana Roo junto a
#                    sus pares nacionales.
# Por qué así:       - Decisión de Brandon (29-sep-2026): hacer el clustering que pedía el plan y elegir el número de grupos
#                      con el coeficiente de silueta. Descartados: dejarlo para después y quitarlo del plan.
#                    - Perfil de 12 meses: la ocupación promedio de cada mes del año (Σ ocupados ÷ Σ disponibles de ese mes
#                      en 2022–2026), en porcentaje. Así el grupo depende de qué tan lleno está un centro Y de cuándo.
#                    - Ward: une en cada paso los dos grupos que menos aumentan la varianza interna; da grupos compactos y
#                      se explica con un dendrograma. Alternativa descartada: k-means (hay que fijar k antes y depende del
#                      punto de arranque).
#                    - Solo filas de tipo "centro" con los 55 meses completos: los agregados ("Total", "Centros de playa",
#                      etc.) no son lugares, y un centro con meses vacíos no se rellena (regla de oro 1); se excluye y se
#                      reporta.
#                    - Los 5 lugares de la campaña no están en DataTur: el clustering describe el norte y el país, no el sur.
# Datos de entrada:  datos/silver/datatur_ocupacion (frecuencia mensual, 2022–2026).
# Alimenta a:        Campaña (mercado emisor): a qué destinos nacionales se parece el norte de Quintana Roo por su
#                    temporada; y al planteamiento de la presión (el norte está en el grupo de playas más llenas).

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from sklearn.metrics import silhouette_score

from torre.radar.panel import GOLD, SILVER

K_CANDIDATOS = range(2, 9)
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def centros_completos() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Filas mensuales de centros (no agregados) y la lista de los que se excluyen por meses vacíos."""
    o = pd.read_parquet(SILVER / "datatur_ocupacion",
                        columns=["centro", "estado", "es_qroo", "frecuencia", "tipo_fila", "periodo",
                                 "cuartos_ocupados", "cuartos_disponibles"])
    o = o[(o.frecuencia == "mensual") & (o.tipo_fila == "centro")].copy()
    o["periodo"] = pd.to_datetime(o.periodo.astype(str))
    total = o.periodo.nunique()
    resumen = o.groupby("centro").agg(meses=("periodo", "nunique"),
                                      vacios=("cuartos_ocupados", lambda s: int(s.isna().sum())))
    resumen["vacios"] += (o.groupby("centro").cuartos_disponibles.apply(lambda s: int((s.fillna(0) <= 0).sum()))
                          - o.groupby("centro").cuartos_disponibles.apply(lambda s: int(s.isna().sum())))
    ok = resumen[(resumen.meses == total) & (resumen.vacios == 0)].index
    excluidos = resumen[~resumen.index.isin(ok)].assign(motivo=lambda r: np.where(
        r.meses < total, "menos meses publicados", "meses sin dato"))
    return o[o.centro.isin(ok)], excluidos


def perfiles(o: pd.DataFrame) -> pd.DataFrame:
    """Una fila por centro, 12 columnas: ocupación de cada mes del año, 2022–2026 (suma de cuartos, no promedio de %)."""
    o = o.assign(mes=o.periodo.dt.month)
    s = o.groupby(["centro", "mes"])[["cuartos_ocupados", "cuartos_disponibles"]].sum()
    p = (100 * s.cuartos_ocupados / s.cuartos_disponibles).unstack("mes")
    p.columns = MESES
    return p


def agrupar(p: pd.DataFrame) -> dict:
    Z = linkage(p.to_numpy(), method="ward")
    siluetas = {k: float(silhouette_score(p, fcluster(Z, k, criterion="maxclust"))) for k in K_CANDIDATOS}
    k = max(siluetas, key=siluetas.get)
    etiquetas = pd.Series(fcluster(Z, k, criterion="maxclust"), index=p.index, name="grupo")
    return {"Z": Z, "siluetas": siluetas, "k": k, "grupos": etiquetas}


def describir(p: pd.DataFrame, grupos: pd.Series) -> pd.DataFrame:
    d = p.assign(grupo=grupos, nivel=p.mean(axis=1), amplitud=p.max(axis=1) - p.min(axis=1),
                 mes_pico=p.idxmax(axis=1))
    return d.groupby("grupo").agg(centros=("nivel", "size"), nivel_medio=("nivel", "mean"),
                                  amplitud_media=("amplitud", "mean"),
                                  mes_pico_mas_comun=("mes_pico", lambda s: s.mode().iloc[0]),
                                  ejemplos=("nivel", lambda s: ", ".join(s.sort_values(ascending=False).index[:5]))).round(1)


def correr() -> dict:
    o, excluidos = centros_completos()
    p = perfiles(o)
    r = agrupar(p)
    qroo = o.drop_duplicates("centro").set_index("centro").es_qroo
    salida = p.assign(grupo=r["grupos"], es_qroo=qroo.reindex(p.index), nivel=p.mean(axis=1).round(1))
    GOLD.mkdir(parents=True, exist_ok=True)
    salida.reset_index(names="centro").to_parquet(GOLD / "radar_clusters_centros.parquet", index=False)
    return {**r, "perfiles": p, "excluidos": excluidos, "tabla": describir(p, r["grupos"]), "salida": salida}


if __name__ == "__main__":
    pd.set_option("display.width", 220, "display.max_colwidth", 90)
    r = correr()
    print(f"Centros con 55 meses completos: {len(r['perfiles'])} · excluidos: {len(r['excluidos'])}")
    print(r["excluidos"].to_string())
    print("\nSilueta por número de grupos:", {k: round(v, 3) for k, v in r["siluetas"].items()}, "→ k =", r["k"])
    print(r["tabla"].to_string())
    q = r["salida"][r["salida"].es_qroo == True][["grupo", "nivel"]]  # noqa: E712
    print("\nCentros de Quintana Roo:"); print(q.sort_values("nivel", ascending=False).to_string())
