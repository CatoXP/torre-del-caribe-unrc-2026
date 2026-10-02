# Autor: Brandon Uriel García Sánchez
# Módulo: Torre en vivo (A5, Fase 7)
# Qué hace:          Reproduce las 239 semanas reales (ene-2022 → jul-2026) como si llegaran una por una:
#                    1. Escribe cada semana de señales como un archivo JSON en datos/gold/envivo_entrada/, en orden.
#                    2. Spark Structured Streaming lee esa carpeta con maxFilesPerTrigger = 1 (una semana por lote) y,
#                       en cada lote (foreachBatch), el motor de reglas decide qué anuncio se enciende o se pausa.
#                    3. Guarda todas las decisiones en Gold y comprueba que las semanas llegaron en orden.
# Por qué así:       - Brandon eligió "reproducción grabada" (02-oct-2026): GitHub Pages es estático y no puede transmitir.
#                      La página reproduce este resultado con la etiqueta "reproducción de datos históricos reales".
#                    - Structured Streaming y no un ciclo for: es la misma arquitectura que recibiría los datos de verdad
#                      (una carpeta a la que llega un archivo por semana) y responde al incidente de Big Data de "baja
#                      latencia para ajustar la campaña DURANTE su ejecución". Cambiar la fuente a una real no cambia el
#                      motor de reglas.
#                    - El plan de dinero es el de la Fase 6 aplicado por mes del año ("si este plan hubiera corrido en
#                      2022–2026"). Jul–sep no tienen plan (fuera del pronóstico): ahí la Torre vigila, pero no gasta.
# Datos de entrada:  datos/gold/envivo_senales.parquet (torre.envivo.senales), presupuesto_plan.parquet (Fase 6).
# Alimenta a:        La página ("La torre, semana a semana") y la Fase 8 (qué anuncio y cuándo).

import json
import os
import shutil

import pandas as pd

from torre.base.entorno import RAIZ, crear_spark
from torre.campana.presupuesto import tabla_meses
from torre.envivo.motor import Memoria, decidir, plan_desde_gold

GOLD = RAIZ / "datos" / "gold"
ENTRADA = GOLD / "envivo_entrada"
CHECKPOINT = GOLD / "envivo_checkpoint"


def escribir_entrada(s: pd.DataFrame) -> int:
    """Un archivo por semana, con hora de modificación creciente: el lector de Spark los toma del más viejo al más nuevo."""
    shutil.rmtree(ENTRADA, ignore_errors=True)
    ENTRADA.mkdir(parents=True)
    base = 1_700_000_000
    for i, fila in enumerate(s.sort_values("semana").to_dict("records")):
        limpio = {k: (None if (isinstance(v, float) and pd.isna(v)) else v) for k, v in fila.items()}
        limpio = {k: (v.isoformat() if hasattr(v, "isoformat") else v) for k, v in limpio.items()}
        ruta = ENTRADA / f"semana_{fila['semana']:%Y-%m-%d}.json"
        ruta.write_text(json.dumps(limpio, ensure_ascii=False), encoding="utf-8")
        os.utime(ruta, (base + i * 60, base + i * 60))
    return len(s)


def reproducir(spark=None) -> dict:
    spark = spark or crear_spark("torre-en-vivo")
    s = pd.read_parquet(GOLD / "envivo_senales.parquet")
    n = escribir_entrada(s)
    plan = plan_desde_gold(pd.read_parquet(GOLD / "presupuesto_plan.parquet"), tabla_meses())
    memoria, decisiones, norte, orden = Memoria(), [], [], []
    esquema = spark.read.json(str(ENTRADA)).schema  # el esquema se fija antes de empezar a escuchar

    def lote(df, id_lote):
        for fila in df.toPandas().to_dict("records"):
            fila = {k: (None if (not isinstance(v, (list, dict)) and pd.isna(v)) else v) for k, v in fila.items()}
            orden.append(pd.Timestamp(fila["semana"]))
            d, nt = decidir(fila, plan, memoria)
            for x in d:
                x["lote"] = id_lote
            decisiones.extend(d)
            norte.append(nt | {"lote": id_lote})

    shutil.rmtree(CHECKPOINT, ignore_errors=True)
    q = (spark.readStream.schema(esquema).option("maxFilesPerTrigger", 1).json(str(ENTRADA))
         .writeStream.foreachBatch(lote).option("checkpointLocation", str(CHECKPOINT))
         .trigger(availableNow=True).start())
    q.awaitTermination()
    if len(orden) != n or any(b <= a for a, b in zip(orden, orden[1:])):
        raise RuntimeError(f"La reproducción no llegó completa o en orden: {len(orden)} de {n} semanas")
    d, nt = pd.DataFrame(decisiones), pd.DataFrame(norte)
    d.to_parquet(GOLD / "envivo_decisiones.parquet", index=False)
    nt.to_parquet(GOLD / "envivo_norte.parquet", index=False)
    print(f"Reproducción: {n} semanas en {d.lote.nunique()} lotes de Spark Structured Streaming, en orden")
    print(d.pivot_table(index="lugar", columns="accion", values="semana", aggfunc="count", fill_value=0).to_string())
    print(f"Pesos gastados: ${d.pesos_gastados.sum():,.0f} de ${d.pesos_plan.sum():,.0f} planeados en semanas con plan; "
          f"arrastre final ${sum(memoria.arrastre.values()):,.0f}")
    print(f"¿Ibas al norte?: {nt.ibas_al_norte.sum()} semanas → " + nt[nt.ibas_al_norte].destino.value_counts().to_string()
          .replace("\n", " · "))
    print("Pausas por motivo:\n" + d[d.accion == "pausado"].motivo.str.replace(r" \(.*?\)", "", regex=True)
          .value_counts().to_string())
    return {"decisiones": d, "norte": nt, "arrastre_final": dict(memoria.arrastre)}


if __name__ == "__main__":
    reproducir()
