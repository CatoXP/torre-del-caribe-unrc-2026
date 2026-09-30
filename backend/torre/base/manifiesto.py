# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Registra cada archivo crudo descargado (Bronze) en datos/bronze/MANIFIESTO.csv con su huella
#                    SHA-256, tamaño, fuente, URL, fecha de descarga y número de filas.
# Por qué así:       Regla de oro 2 (toda cifra es rastreable) y el incidente de Big Data (qué se guarda y por qué).
#                    Con la huella cualquiera puede comprobar que el archivo es el original de la fuente oficial.
#                    Alternativa descartada: guardar solo los archivos sin registro. Así no hay forma de probar
#                    de dónde vino un número ni si alguien cambió el archivo después.
# Datos de entrada:  Los archivos que escriben las funciones de ingesta.
# Alimenta a:        La trazabilidad de todas las cifras de la campaña y del informe.

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
BRONZE = RAIZ / "datos" / "bronze"
MANIFIESTO = BRONZE / "MANIFIESTO.csv"
COLUMNAS = ["fuente", "archivo", "sha256", "bytes", "filas", "url", "descargado_utc", "nota"]


def sha256_de(ruta: Path) -> str:
    """Huella SHA-256 del archivo, leída en bloques de 1 MB para no cargar archivos grandes en memoria."""
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def registrar(fuente: str, ruta: Path, url: str, filas: int | None = None, nota: str = "") -> dict:
    """Agrega (o actualiza) la fila de un archivo en el manifiesto y la devuelve.

    - fuente: código del inventario (p. ej. "D1 SITUR-Q").
    - filas:  número de registros que trae el archivo (None si no aplica, p. ej. un PDF).
    Si el archivo ya estaba registrado, se reemplaza su fila; así el manifiesto no duplica entradas.
    """
    ruta = Path(ruta)
    fila = {
        "fuente": fuente,
        "archivo": ruta.relative_to(RAIZ).as_posix(),
        "sha256": sha256_de(ruta),
        "bytes": ruta.stat().st_size,
        "filas": "" if filas is None else filas,
        "url": url,
        "descargado_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "nota": nota,
    }
    existentes = []
    if MANIFIESTO.exists():
        with open(MANIFIESTO, newline="", encoding="utf-8") as f:
            existentes = [r for r in csv.DictReader(f) if r["archivo"] != fila["archivo"]]
    MANIFIESTO.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFIESTO, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(existentes + [fila])
    return fila
