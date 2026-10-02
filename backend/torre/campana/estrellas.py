# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña
# Qué hace:          Lee del Compendio Estadístico del Turismo en México 2024 (DataTur, tabla 5_2) los cuartos de hotel
#                    por categoría oficial (1 a 5 estrellas) de Cancún y de Playa del Carmen (Riviera Maya), y calcula
#                    qué parte de los cuartos es de cada categoría.
# Por qué así:       - Brandon (02-oct-2026) pidió "las estrellas del lugar" y eligió "Estrellas oficiales" (decisión 16).
#                      La categoría oficial solo se publica para los 70 centros que monitorea DataTur: Cancún y Playa del
#                      Carmen están; ninguno de los lugares del sur (hueco declarado).
#                    - La tabla trae, por centro y categoría, los cuartos-noche disponibles del año. La parte de cada
#                      categoría se calcula con cuartos-noche (no se promedian porcentajes) y los cuartos promedio se
#                      obtienen dividiendo entre los 366 días de 2024.
#                    - Descartado: estrellas de Google o TripAdvisor (términos de uso, regla de oro 4).
# Datos de entrada:  datos/bronze/datatur/<fecha>/compendio/CETM2024.zip (5_2.xlsx, hoja Vista01).
# Alimenta a:        Las fichas de Cancún y Riviera Maya en "Los lugares" (referencia: qué tipo de hotel domina allá).

import io
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
DIAS_2024 = 366
CENTROS = {"Cancún": "Cancún", "Riviera Maya": "Playa del Carmen"}  # lugar de la página → centro de DataTur


def tabla() -> pd.DataFrame:
    """Una fila por centro y categoría, con cuartos-noche disponibles en 2024."""
    zipf = sorted((RAIZ / "datos" / "bronze" / "datatur").glob("*/compendio/CETM2024.zip"))[-1]
    with zipfile.ZipFile(zipf) as z:
        v = pd.read_excel(io.BytesIO(z.read("CETM2024/5_2.xlsx")), sheet_name="Vista01", header=None)
    v = v.iloc[8:, 1:10]
    v.columns = ["clasificacion", "tipo", "subtipo", "centro", "categoria", "corredor", "pueblo_magico",
                 "cuartos_noche", "cuartos_promedio"]
    # La tabla dinámica solo escribe el nombre del centro en su primera fila: se rellena hacia abajo.
    # Si una fila trae el centro en otra columna (por las celdas combinadas), se reacomoda por el texto "Estrella".
    filas = []
    centro = None
    for _, f in v.iterrows():
        valores = [x for x in f.tolist() if pd.notna(x)]
        if not valores:
            continue
        i = next((k for k, x in enumerate(valores) if isinstance(x, str) and "Estrella" in x), None)
        if i is None:
            continue
        if i >= 1 and isinstance(valores[i - 1], str):
            centro = valores[i - 1]
        numeros = [x for x in valores[i + 1:] if isinstance(x, (int, float))]
        if centro and numeros:
            filas.append({"centro": centro, "categoria": valores[i], "estrellas": int(valores[i][0]),
                          "cuartos_noche": float(numeros[0])})
    return pd.DataFrame(filas)


def estrellas() -> dict:
    t = tabla()
    salida = {}
    for lugar, centro in CENTROS.items():
        x = t[t.centro == centro].groupby("estrellas").cuartos_noche.sum()
        if x.empty:
            raise ValueError(f"No está {centro} en la tabla 5_2 (regla de oro 5)")
        total = x.sum()
        salida[lugar] = {"centro": centro, "cuartos": round(total / DIAS_2024),
                         "por_categoria": {int(k): round(v / total * 100, 1) for k, v in x.sort_index(ascending=False).items()},
                         "fuente": "SECTUR-DataTur, Compendio Estadístico del Turismo en México 2024 (tabla 5_2)",
                         "anio": 2024}
    return salida


if __name__ == "__main__":
    import json
    print(json.dumps(estrellas(), ensure_ascii=False, indent=1))
