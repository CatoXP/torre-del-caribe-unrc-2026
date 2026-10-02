# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Limpia la base de llegadas de extranjeros por avión según su nacionalidad (DataTur, BD_Nacionalidad,
#                    con cifras de la Unidad de Política Migratoria) y la guarda en Silver con una fila por mes,
#                    aeropuerto, país y sexo. A los aeropuertos de Quintana Roo les pone su lugar y su papel en la campaña.
# Por qué así:       - Es la única fuente que dice DE DÓNDE viene el visitante extranjero en cada aeropuerto del estado:
#                      la base del buyer persona (Fase 8) y de los idiomas de la página ("Mercados que llegan").
#                    - Solo cuenta extranjeros: no hay país "México" en la base (verificado el 02-oct-2026). Por eso la
#                      columna se llama llegadas_extranjeros y no "pasajeros".
#                    - Revisado el 02-oct-2026: 0 llaves repetidas y 0 filas idénticas (521,363 filas, 2012 → jul-2026).
#                      Si un día aparecen, el proceso se detiene (regla de oro 5).
#                    - El aeropuerto de Tulum abre en feb-2024: antes no hay filas, y eso no es un cero.
#                    - Alternativa descartada: guardar solo Quintana Roo. Se conserva el país para comparar.
# Datos de entrada:  datos/bronze/datatur/<fecha>/nacionalidad/BD_Nacionalidad.zip (D3).
# Alimenta a:        Fase 8 (buyer persona: país de origen por aeropuerto y temporada) y la Fase 6 (en qué mercado se
#                    anuncia).

import io
import zipfile

import pandas as pd

from torre.base.entorno import RAIZ, crear_spark

BRONZE = RAIZ / "datos" / "bronze"
SILVER_NACIONALIDAD = RAIZ / "datos" / "silver" / "nacionalidad"

# Aeropuertos de Quintana Roo → (lugar, papel en la campaña), igual que en docs/regiones/REGIONES.md.
AEROPUERTOS_QROO = {
    "Chetumal, Q. Roo": ("Chetumal", "promovida"),
    "Cancún, Q. Roo": ("Cancún", "referencia"),
    "A.I Tulum Felipe Carrillo Puerto, Q. Roo.": ("Tulum", "referencia"),
    "Cozumel, Q. Roo": ("Cozumel", "excluida"),
}
LLAVE = ["periodo", "aeropuerto", "pais", "sexo"]


def leer_nacionalidad() -> pd.DataFrame:
    """Lee el Excel del zip más reciente y pone nombres en español y snake_case."""
    zipf = sorted(BRONZE.glob("datatur/*/nacionalidad/BD_Nacionalidad.zip"))[-1]
    with zipfile.ZipFile(zipf) as z:
        nombre = next(n for n in z.namelist() if n.lower().endswith(".xlsx"))
        d = pd.read_excel(io.BytesIO(z.read(nombre)))
    d = d.rename(columns={"Año": "anio", "MesNum": "mes", "Aeropuerto": "aeropuerto", "Pais": "pais",
                          "Región": "region_mundo", "Sexo": "sexo", "Valor": "llegadas_extranjeros"})
    d["periodo"] = d.Fecha.dt.date
    d["sexo"] = d.sexo.str.lower()
    d["archivo"] = str(zipf.relative_to(RAIZ))
    return d[["anio", "mes", "periodo", "aeropuerto", "pais", "region_mundo", "sexo", "llegadas_extranjeros", "archivo"]]


def revisar_llave(d: pd.DataFrame) -> None:
    """Regla de oro 5: si hay dos filas con la misma llave, no se elige una; se detiene."""
    repetidas = int(d.duplicated(LLAVE).sum())
    if repetidas:
        raise ValueError(f"Nacionalidad: {repetidas} llaves repetidas; revisar a mano antes de seguir")


def agregar_papel(d: pd.DataFrame) -> pd.DataFrame:
    d["es_qroo"] = d.aeropuerto.isin(AEROPUERTOS_QROO)
    d["lugar_campana"] = d.aeropuerto.map(lambda a: AEROPUERTOS_QROO.get(a, (None, None))[0])
    d["papel_campana"] = d.aeropuerto.map(lambda a: AEROPUERTOS_QROO.get(a, (None, None))[1])
    return d


def construir_silver_nacionalidad(spark=None) -> pd.DataFrame:
    spark = spark or crear_spark("silver-nacionalidad")
    d = leer_nacionalidad()
    revisar_llave(d)
    d = agregar_papel(d)
    df = spark.createDataFrame(d.astype({"lugar_campana": "object", "papel_campana": "object"}))
    df.write.mode("overwrite").partitionBy("anio").parquet(str(SILVER_NACIONALIDAD))
    q = d[d.es_qroo]
    print(f"Nacionalidad Silver: {len(d):,} filas; Quintana Roo: {len(q):,} filas")
    print("Llegadas de extranjeros por año (Quintana Roo):\n"
          + q.pivot_table(index="anio", columns="lugar_campana", values="llegadas_extranjeros", aggfunc="sum")
          .fillna(0).astype(int).to_string())
    return d


if __name__ == "__main__":
    construir_silver_nacionalidad()
