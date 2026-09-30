# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Limpia HURDAT2 (NOAA, todas las tormentas del Atlántico 1851–2025) y la guarda en Silver con una fila
#                    por punto de trayectoria (cada 6 horas). A cada punto le calcula su distancia a Chetumal y le pone
#                    las banderas que definen "una tormenta que afecta al sur de Quintana Roo".
# Por qué así:       - Definición elegida por Brandon (30-sep-2026, docs/decisiones/10-silver-fase5.md): un evento es una
#                      tormenta con al menos un punto a ≤ 200 km de Chetumal y viento ≥ 34 nudos (tormenta tropical o
#                      huracán), contada desde 1966 (inicio de la vigilancia por satélite): 31 eventos en 60 años.
#                      Alternativas descartadas: 100 km (13 eventos desde 1966: muy pocos para una tasa por mes),
#                      300 km (59 eventos: incluye tormentas que pasan por el norte de Yucatán y por Honduras) y contar
#                      desde 1851 (0.469 por año contra 0.517: antes de los satélites se perdían tormentas en el mar).
#                    - Se guardan TODOS los puntos (no solo los del sur) para que el radio o el umbral se puedan
#                      cambiar sin volver a leer el texto crudo (análisis de sensibilidad en la Fase 5).
#                    - Parser con expresión regular sobre la posición, el viento y la presión: 2 de 55,524 líneas
#                      vienen mal formadas en el archivo oficial. 1969-09-29 06Z trae "63.3N    7.5E" sin coma (se lee
#                      completa) y 1975-12-07 00Z trae "38.83" sin hemisferio (la latitud queda nula; no se adivina).
#                      Ambas se marcan con formato_irregular_flag. Las dos están en el Atlántico norte, a más de
#                      3,000 km de Chetumal: no cambian el conteo.
#                    - Faltantes oficiales de HURDAT2: viento -99 y presión -999 se guardan como nulos, no como números.
#                    - Texto → pandas (el formato alterna encabezados y filas) y Spark escribe el Parquet por año.
# Datos de entrada:  datos/bronze/huracanes/<fecha>/hurdat2-1851-2025-*.txt (D9).
# Alimenta a:        A3 Pronóstico: probabilidad mensual de tormenta (Poisson) y choques del Monte Carlo, que deciden en
#                    qué meses la campaña reserva presupuesto de contingencia.

import math
import re

import pandas as pd

from torre.base.entorno import RAIZ, crear_spark

BRONZE = RAIZ / "datos" / "bronze"
SILVER_HURACANES = RAIZ / "datos" / "silver" / "huracanes"

CHETUMAL = (18.50, -88.30)     # centro del sur de Quintana Roo (bahía de Chetumal)
RADIO_KM = 200                 # decisión de Brandon, 30-sep-2026
VIENTO_MIN_KT = 34             # 34 nudos ≈ 63 km/h: umbral oficial de tormenta tropical
ANIO_SATELITAL = 1966          # primer año con vigilancia por satélite continua

# Posición + viento + presión. Tolera "18.5N, 88.3W" (normal) y "63.3N    7.5E" (sin coma entre las dos).
POS = re.compile(r"(\d+\.\d)([NS])[\s,]*(\d+\.\d)([EW])\s*,\s*(-?\d+)\s*,\s*(-?\d+)")
# Latitud sin hemisferio ("38.83,  51.0W", tormenta de 1975): la latitud no se adivina, queda nula.
POS_SIN_HEMISFERIO = re.compile(r"(\d+\.\d+)\s*,\s*(\d+\.\d)([EW])\s*,\s*(-?\d+)\s*,\s*(-?\d+)")
LAT_BIEN = re.compile(r"\d+\.\d[NS]")


def km_haversine(lat1, lon1, lat2, lon2) -> float:
    """Distancia sobre la esfera terrestre (radio 6,371 km). Ecuación en ECUACIONES.md §3.1."""
    p = math.pi / 180
    a = (math.sin((lat2 - lat1) * p / 2) ** 2
         + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2)
    return 2 * 6371 * math.asin(math.sqrt(a))


def leer_hurdat2() -> pd.DataFrame:
    """Recorre el archivo: una línea de encabezado (id, nombre, n puntos) seguida de n líneas de trayectoria."""
    archivo = sorted(BRONZE.glob("huracanes/*/hurdat2-1851-*.txt"))[-1]
    lineas = archivo.read_text(encoding="utf-8").splitlines()
    filas, i = [], 0
    while i < len(lineas):
        cab = [x.strip() for x in lineas[i].split(",")]
        id_tormenta, nombre, n = cab[0], cab[1], int(cab[2])
        for linea in lineas[i + 1:i + 1 + n]:
            c = [x.strip() for x in linea.split(",")]
            m = POS.search(linea)
            if m:
                lat = float(m.group(1)) * (1 if m.group(2) == "N" else -1)
                lon_txt, hemi_lon, viento, presion = m.group(3), m.group(4), int(m.group(5)), int(m.group(6))
            else:
                m = POS_SIN_HEMISFERIO.search(linea)
                if not m:  # regla de oro 5: una línea que no se entiende detiene el proceso
                    raise ValueError(f"HURDAT2: línea sin posición legible en {id_tormenta}: {linea[:60]}")
                lat = None
                lon_txt, hemi_lon, viento, presion = m.group(2), m.group(3), int(m.group(4)), int(m.group(5))
            filas.append({
                "id_tormenta": id_tormenta, "nombre": nombre,
                "fecha": c[0], "hora_utc": c[1], "marca": c[2] or None, "estado_sistema": c[3],
                "lat": lat, "lon": float(lon_txt) * (-1 if hemi_lon == "W" else 1),
                "viento_kt": None if viento == -99 else viento,
                "presion_mb": None if presion == -999 else presion,
                "formato_irregular_flag": not LAT_BIEN.fullmatch(c[4]),
            })
        i += 1 + n
    d = pd.DataFrame(filas)
    d["anio"] = d.fecha.str[:4].astype(int)
    d["mes"] = d.fecha.str[4:6].astype(int)
    d["fecha_hora_utc"] = pd.to_datetime(d.fecha + d.hora_utc.str.zfill(4), format="%Y%m%d%H%M")
    # Spark en Windows no convierte marcas de tiempo anteriores a 1970 (mktime): se guarda fecha + hora en número.
    d["fecha"] = d.fecha_hora_utc.dt.date
    d["hora_utc"] = d.hora_utc.astype(int)
    d["archivo"] = str(archivo.relative_to(RAIZ))
    return d


def agregar_banderas(d: pd.DataFrame) -> pd.DataFrame:
    d["km_chetumal"] = [None if pd.isna(a) else round(km_haversine(a, b, *CHETUMAL), 1) for a, b in zip(d.lat, d.lon)]
    d["dentro_radio_flag"] = d.km_chetumal.fillna(float("inf")) <= RADIO_KM  # sin latitud no se puede afirmar cercanía
    d["tormenta_o_huracan_flag"] = d.viento_kt.fillna(0) >= VIENTO_MIN_KT
    d["era_satelital_flag"] = d.anio >= ANIO_SATELITAL
    d["afecta_sur_flag"] = d.dentro_radio_flag & d.tormenta_o_huracan_flag & d.era_satelital_flag
    return d


def eventos_sur(d: pd.DataFrame) -> pd.DataFrame:
    """Una fila por tormenta que afecta al sur: mes del primer punto que cumple la definición, viento máximo dentro
    del radio y distancia mínima a Chetumal. Es la serie que usa el modelo de Poisson de la Fase 5."""
    x = d[d.afecta_sur_flag].sort_values(["fecha", "hora_utc"])
    return (x.groupby("id_tormenta")
             .agg(nombre=("nombre", "first"), anio=("anio", "first"), mes=("mes", "first"),
                  viento_max_kt=("viento_kt", "max"), km_min=("km_chetumal", "min"))
             .reset_index().sort_values(["anio", "mes"]).reset_index(drop=True))


def construir_silver_huracanes(spark=None):
    spark = spark or crear_spark("silver-huracanes")
    d = agregar_banderas(leer_hurdat2())
    columnas = ["id_tormenta", "nombre", "anio", "mes", "fecha", "hora_utc", "marca", "estado_sistema", "lat", "lon",
                "viento_kt", "presion_mb", "km_chetumal", "dentro_radio_flag", "tormenta_o_huracan_flag",
                "era_satelital_flag", "afecta_sur_flag", "formato_irregular_flag", "archivo"]
    d = d[columnas]
    df = spark.createDataFrame(d.astype({"viento_kt": "Int64", "presion_mb": "Int64", "marca": "object"}))
    df.write.mode("overwrite").partitionBy("anio").parquet(str(SILVER_HURACANES))
    ev = eventos_sur(d)
    anios = d.anio.max() - ANIO_SATELITAL + 1
    print(f"HURDAT2 Silver: {len(d):,} puntos de {d.id_tormenta.nunique():,} tormentas ({d.anio.min()}–{d.anio.max()}); "
          f"{int(d.formato_irregular_flag.sum())} líneas con formato irregular")
    print(f"Afectan al sur (≤{RADIO_KM} km de Chetumal, ≥{VIENTO_MIN_KT} kt, desde {ANIO_SATELITAL}): "
          f"{len(ev)} eventos en {anios} años = {len(ev) / anios:.3f} por año")
    print("Eventos por mes:", ev.mes.value_counts().sort_index().to_dict())
    return d


if __name__ == "__main__":
    construir_silver_huracanes()
