# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Descarga las fuentes abiertas restantes del inventario y las registra en el manifiesto:
#                    D5 Rest-Mex 2025, D6 DENUE (32 estados), D7 Censo 2020 ITER Q. Roo, D8 Open-Meteo (clima
#                    horario y diario de 8 puntos), D9 HURDAT2, D10 FRED, D11 ENDUTIH 2025 (PDF) y D12 GeoJSON.
# Por qué así:       Todas las URL se verificaron el 26–27 de septiembre de 2026 (ver docs/datos/INVENTARIO.md).
#                    Cada fuente es una función corta e independiente: si una falla, las demás siguen, y se
#                    puede volver a correr solo esa.
#                    DENUE se baja completo (32 estados, no solo Q. Roo) porque así la parte de Big Data trabaja con
#                    volumen real y da el contexto nacional de la oferta turística (criterio 2).
# Datos de entrada:  URLs oficiales de INEGI, NOAA, FRED, Open-Meteo, HuggingFace y GitHub.
# Alimenta a:        A1 (oferta y turistas por residente), A3 (clima, huracanes, tipo de cambio) y la campaña
#                    (reseñas y hábitos digitales).

import csv
import io
import json
import time
import zipfile
from datetime import date
from pathlib import Path

import requests

from torre.base.manifiesto import BRONZE, registrar

UA = {"User-Agent": "Mozilla/5.0 (proyecto escolar UNRC)"}
HOY = date.today().isoformat()

# 8 puntos de clima: los 2 destinos emisores y los destinos que se promueven (coordenadas del centro de cada lugar).
PUNTOS_CLIMA = {
    "cancun": (21.1619, -86.8515),
    "playa_del_carmen": (20.6296, -87.0739),
    "tulum": (20.2114, -87.4654),
    "coba": (20.4918, -87.7328),
    "felipe_carrillo_puerto": (19.5801, -88.0452),
    "bacalar": (18.6771, -88.3950),
    "chetumal": (18.5001, -88.2961),
    "kohunlich": (18.4197, -88.7903),
}
ESTADOS_DENUE = [f"{i:02d}" for i in range(1, 33)]


def _bajar(url: str, destino: Path, timeout: int = 300) -> bytes:
    """Descarga una URL a un archivo (salvo que ya exista, para poder reanudar) y devuelve su contenido."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not destino.exists():
        r = requests.get(url, headers=UA, timeout=timeout)
        r.raise_for_status()
        destino.write_bytes(r.content)
    return destino.read_bytes()


def _filas_csv_en_zip(contenido: bytes) -> int:
    """Cuenta las filas de datos (sin encabezado) de los CSV de la carpeta "conjunto_de_datos" dentro de un zip.

    Corrección del 28-sep-2026: la primera versión contaba TODOS los CSV del zip, incluido el diccionario de datos
    (58 líneas en cada zip del DENUE). Eso inflaba el DENUE en 33 × 58 = 1,914 registros (6,139,989 en lugar de
    6,138,075). Se detectó al comparar contra Spark y contra un lector CSV independiente en la Fase 2.
    Segunda corrección (28-sep-2026, Fase 3): la versión anterior solo excluía el diccionario y seguía sumando el
    catálogo "catalogos/tam_loc.csv.csv" del Censo ITER (14 filas): 2,257 en lugar de 2,243 localidades. Ahora se
    cuenta exclusivamente la carpeta conjunto_de_datos, como promete esta descripción.
    """
    total = 0
    with zipfile.ZipFile(io.BytesIO(contenido)) as z:
        for n in z.namelist():
            if n.lower().endswith(".csv") and "conjunto_de_datos" in n.lower():
                with z.open(n) as f:
                    total += max(sum(1 for _ in f) - 1, 0)
    return total


def restmex():
    url = "https://huggingface.co/datasets/vg055/Rest-Mex2025/resolve/main/Rest-Mex_2025_train.csv"
    ruta = BRONZE / "restmex" / HOY / "Rest-Mex_2025_train.csv"
    datos = _bajar(url, ruta)
    # Las reseñas tienen saltos de línea dentro del texto: se cuentan registros con el lector de CSV, no líneas.
    filas = sum(1 for _ in csv.reader(io.StringIO(datos.decode("utf-8", errors="replace")))) - 1
    return [registrar("D5 Rest-Mex 2025", ruta, url, filas=filas, nota="licencia CC-BY-4.0")]


def _es_zip(url: str) -> bool:
    """Pregunta al servidor el tipo de archivo sin descargarlo. INEGI responde una página HTML cuando no existe."""
    r = requests.head(url, headers=UA, timeout=60, allow_redirects=True)
    return r.ok and "zip" in r.headers.get("Content-Type", "")


def denue():
    """DENUE de los 32 estados. Los estados más grandes vienen divididos en partes.

    Verificado el 28-sep-2026: el Estado de México (15) no existe como denue_15_csv.zip, sino como denue_15_1_csv.zip
    (50.6 MB) y denue_15_2_csv.zip (30.2 MB). Por eso, si el archivo único no existe, se buscan las partes _1, _2, …
    """
    base = "https://www.inegi.org.mx/contenidos/masiva/denue/denue_{}_csv.zip"
    salida = []
    for e in ESTADOS_DENUE:
        if _es_zip(base.format(e)):
            nombres = [e]                       # el estado viene en un solo archivo
        else:
            nombres: list[str] = []             # el estado viene en partes: _1, _2, ... hasta que ya no exista
            parte = 1
            while _es_zip(base.format(f"{e}_{parte}")):
                nombres.append(f"{e}_{parte}")
                parte += 1
            if not nombres:
                raise RuntimeError(f"DENUE: no se encontró el estado {e} ni sus partes")
        for n in nombres:
            url = base.format(n)
            ruta = BRONZE / "denue" / HOY / f"denue_{n}_csv.zip"
            datos = _bajar(url, ruta)
            if datos[:2] != b"PK":  # los zip siempre empiezan con "PK"; si no, es una página de error
                ruta.unlink()
                raise RuntimeError(f"DENUE {n}: la descarga no es un zip")
            salida.append(registrar("D6 DENUE INEGI", ruta, url, filas=_filas_csv_en_zip(datos), nota=f"estado {n}"))
    return salida


def iter_qroo():
    url = "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_23_cpv2020_csv.zip"
    ruta = BRONZE / "iter" / HOY / "iter_23_cpv2020_csv.zip"
    datos = _bajar(url, ruta)
    return [registrar("D7 Censo 2020 ITER", ruta, url, filas=_filas_csv_en_zip(datos))]


def _bajar_con_espera(url: str, ruta: Path, intentos: int = 6) -> bytes:
    """Como _bajar, pero si Open-Meteo responde 429 (demasiadas peticiones) espera y reintenta.

    El 28-sep-2026 la primera versión, que pedía 7.7 años horarios de un golpe, recibió 429 en el segundo punto.
    El servicio gratuito limita cuántos datos se piden por minuto y por hora.
    """
    for i in range(intentos):
        try:
            return _bajar(url, ruta, timeout=600)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 429 and i < intentos - 1:
                time.sleep(60 * (i + 1))  # 1, 2, 3... minutos
                continue
            raise
    raise RuntimeError(f"Open-Meteo no respondió después de {intentos} intentos: {url}")


def clima():
    """Clima de 8 puntos (reanálisis ERA5 vía Open-Meteo), en partes pequeñas para respetar el límite gratuito:

    - horario (temperatura, lluvia, viento): un archivo por punto y por año, de 2019 a hoy;
    - diario (máximas y acumulados): un archivo por punto y por década, de 1950 a hoy.
    """
    salida, ayer = [], date.fromordinal(date.today().toordinal() - 1)
    tramos = [("horario", f"{a}-01-01", min(date(a, 12, 31), ayer).isoformat(),
               "hourly=temperature_2m,precipitation,wind_speed_10m", str(a)) for a in range(2019, ayer.year + 1)]
    tramos += [("diario", f"{d}-01-01", min(date(d + 9, 12, 31), ayer).isoformat(),
                "daily=temperature_2m_max,precipitation_sum,wind_speed_10m_max&timezone=America%2FCancun", f"{d}s")
               for d in range(1950, ayer.year + 1, 10)]
    for punto, (lat, lon) in PUNTOS_CLIMA.items():
        for tipo, inicio, fin, variables, etiqueta in tramos:
            url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
                   f"&start_date={inicio}&end_date={fin}&{variables}")
            ruta = BRONZE / "clima" / HOY / tipo / f"{punto}_{etiqueta}.json"
            ya_estaba = ruta.exists()
            datos = json.loads(_bajar_con_espera(url, ruta))
            serie = datos.get("hourly") or datos.get("daily") or {}
            salida.append(registrar("D8 Open-Meteo", ruta, url, filas=len(serie.get("time", [])), nota=f"{punto} {tipo} {etiqueta}"))
            if not ya_estaba:
                time.sleep(3)  # pausa entre peticiones reales al servidor
    return salida


def huracanes():
    """HURDAT2: se toma el archivo más reciente publicado en el índice de la NOAA."""
    import re
    indice = requests.get("https://www.nhc.noaa.gov/data/hurdat/", headers=UA, timeout=60).text
    nombre = sorted(set(re.findall(r"hurdat2-1851-\d{4}-\d{6}\.txt", indice)))[-1]
    url = f"https://www.nhc.noaa.gov/data/hurdat/{nombre}"
    ruta = BRONZE / "huracanes" / HOY / nombre
    datos = _bajar(url, ruta).decode("utf-8", errors="replace").splitlines()
    tormentas = sum(1 for l in datos if l.startswith("AL"))
    return [registrar("D9 HURDAT2 NOAA", ruta, url, filas=len(datos), nota=f"{tormentas} tormentas")]


def fred():
    salida = []
    for serie in ("DEXMXUS", "CPIAUCSL"):
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={serie}"
        ruta = BRONZE / "fred" / HOY / f"{serie}.csv"
        filas = len(_bajar(url, ruta).decode().splitlines()) - 1
        salida.append(registrar("D10 FRED", ruta, url, filas=filas))
    return salida


def endutih():
    url = "https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/endutih/ENDUTIH_25_RR.pdf"
    ruta = BRONZE / "endutih" / HOY / "ENDUTIH_25_RR.pdf"
    _bajar(url, ruta)
    return [registrar("D11 ENDUTIH 2025", ruta, url, nota="reporte de resultados (agregados)")]


def geojson():
    url = "https://raw.githubusercontent.com/PhantomInsights/mexico-geojson/main/2020/states/Quintana%20Roo.json"
    ruta = BRONZE / "geo" / HOY / "quintana_roo.json"
    datos = json.loads(_bajar(url, ruta))
    return [registrar("D12 GeoJSON Q. Roo", ruta, url, filas=len(datos.get("features", [])), nota="polígonos")]


FUENTES = {"restmex": restmex, "denue": denue, "iter": iter_qroo, "clima": clima,
           "huracanes": huracanes, "fred": fred, "endutih": endutih, "geo": geojson}


def descargar_abiertas(fuentes=tuple(FUENTES)):
    """Corre cada fuente por separado; si una falla, se reporta y se sigue con las demás (no se inventa nada)."""
    fallas = {}
    for nombre in fuentes:
        try:
            filas = FUENTES[nombre]()
            print(f"{nombre:10s} OK  {len(filas)} archivo(s), {sum(int(f['filas'] or 0) for f in filas):,} filas")
        except Exception as e:  # se declara el hueco, no se rellena
            fallas[nombre] = repr(e)
            print(f"{nombre:10s} FALLÓ: {e!r}")
    return fallas


if __name__ == "__main__":
    descargar_abiertas()
