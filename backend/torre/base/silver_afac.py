# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Limpia la base de pasajeros por aerolínea de la AFAC (DataTur, DB_AFAC) y la guarda en Silver con
#                    una fila por mes, tipo de vuelo, servicio, región de la aerolínea y aerolínea.
# Por qué así:       - Es la serie nacional de pasajeros aéreos 2016 → jul-2026: sirve de contexto para saber si el turismo
#                      aéreo del país crece o cae (2020: 48.4 millones; 2025: 122.7 millones).
#                    - Duplicados revisados el 02-oct-2026 (300 llaves repetidas):
#                        · 98 filas idénticas → se deja una.
#                        · 177 llaves con una cifra y una copia en cero → se conserva la cifra (misma regla que INAH).
#                        · 25 llaves con DOS cifras: todas de "Virgin América (Alaska Airlines)", de 2016 a ene-2018. Son
#                          dos aerolíneas que se fusionaron en 2018 bajo una sola etiqueta. Decisión de Brandon: se SUMAN
#                          y la fila lleva sumada_flag. En juego hay 369,311 pasajeros de 1,042 millones (0.035 %).
#                        · Si aparece otra llave con dos cifras, el proceso se detiene (regla de oro 5).
#                    - El texto "Fletamento " trae un espacio de más; se recorta.
#                    - 46 % de las filas valen 0: son aerolíneas del catálogo sin vuelos ese mes. Se conservan.
# Datos de entrada:  datos/bronze/datatur/<fecha>/afac/DB_AFAC.zip (D4).
# Alimenta a:        Fase 8 (contexto de mercados: qué región de aerolíneas crece) y el informe (grandes volúmenes).

import io
import zipfile

import pandas as pd

from torre.base.entorno import RAIZ, crear_spark

BRONZE = RAIZ / "datos" / "bronze"
SILVER_AFAC = RAIZ / "datos" / "silver" / "afac"

LLAVE = ["anio", "mes", "tipo_vuelo", "servicio", "region_aerolinea", "aerolinea"]
# Única etiqueta donde dos cifras en el mismo mes se suman (decisión de Brandon del 02-oct-2026).
SE_SUMAN = {"Virgin América (Alaska Airlines)"}


def leer_afac() -> pd.DataFrame:
    zipf = sorted(BRONZE.glob("datatur/*/afac/DB_AFAC.zip"))[-1]
    with zipfile.ZipFile(zipf) as z:
        nombre = next(n for n in z.namelist() if n.lower().endswith(".xlsx"))
        d = pd.read_excel(io.BytesIO(z.read(nombre)))
    d = d.rename(columns={"Año": "anio", "Id_mes": "mes", "Tipo": "tipo_vuelo", "Servicio": "servicio",
                          "Región": "region_aerolinea", "Aerolinea": "aerolinea", "Pasajeros": "pasajeros"})
    for c in ["tipo_vuelo", "servicio", "region_aerolinea", "aerolinea"]:
        d[c] = d[c].str.strip()
    d["tipo_vuelo"] = d.tipo_vuelo.str.lower()
    d["servicio"] = d.servicio.str.lower()
    d["periodo"] = d.Fecha.dt.date
    d["archivo"] = str(zipf.relative_to(RAIZ))
    return d[LLAVE + ["periodo", "pasajeros", "archivo"]]


def quitar_duplicados(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Aplica las tres reglas de duplicados. Devuelve la tabla limpia y cuántas filas tocó cada regla."""
    antes = len(d)
    d = d.drop_duplicates()
    identicas = antes - len(d)
    con_cifra = d.groupby(LLAVE).pasajeros.transform(lambda v: (v > 0).sum())
    dos = d[con_cifra > 1]
    otras = set(dos.aerolinea) - SE_SUMAN
    if otras:
        raise ValueError(f"AFAC: dos cifras en la misma llave para {sorted(otras)}; revisar a mano")
    # Se quitan las copias en cero cuando existe la cifra, y se suman las dos cifras de las etiquetas permitidas.
    d = d[~((con_cifra >= 1) & (d.pasajeros == 0))]
    n_llaves = d.groupby(LLAVE).size()
    sumadas = n_llaves[n_llaves > 1]
    d = (d.groupby(LLAVE + ["periodo", "archivo"], as_index=False, observed=True).pasajeros.sum())
    d["sumada_flag"] = d.set_index(LLAVE).index.isin(sumadas.index)
    # Llaves que solo tenían copias en cero: quedan con una sola fila en 0.
    resumen = {"identicas": identicas, "llaves_sumadas": int(len(sumadas)), "filas_finales": len(d)}
    return d.sort_values(LLAVE).reset_index(drop=True), resumen


def construir_silver_afac(spark=None) -> pd.DataFrame:
    spark = spark or crear_spark("silver-afac")
    d, r = quitar_duplicados(leer_afac())
    spark.createDataFrame(d).write.mode("overwrite").partitionBy("anio").parquet(str(SILVER_AFAC))
    print(f"AFAC Silver: {r['filas_finales']:,} filas; {r['identicas']} idénticas quitadas; "
          f"{r['llaves_sumadas']} llaves sumadas (Virgin América + Alaska)")
    print("Pasajeros por año:\n" + d.groupby("anio").pasajeros.sum().to_string())
    return d


if __name__ == "__main__":
    construir_silver_afac()
