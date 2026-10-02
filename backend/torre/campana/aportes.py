# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña
# Qué hace:          Lee las fotos y reseñas que el EQUIPO junta en los 5 lugares (docs/aportes/aportes.json + fotos),
#                    las valida y las prepara para la sección "Lo que vivimos" de la página. Si no hay ninguna, la
#                    sección no aparece.
# Por qué así:       - Brandon (02-oct-2026) pidió fotos de comida, reseñas reales y estrellas. No existen con licencia
#                      libre para los 5 lugares (Commons: 0 fotos de platillos; Rest-Mex no cubre los lugares) y copiar
#                      reseñas de Google o TripAdvisor está prohibido (regla de oro 4). Eligió "Reseñas y fotos del
#                      equipo": material propio o con permiso, con nombre y fecha (decisión 16).
#                    - Reglas (regla de oro 1 y decisión 06): cada aporte dice quién, cuándo y en qué lugar; las fotos
#                      de otra persona necesitan su permiso por escrito; si la foto trae ubicación GPS, debe caer en el
#                      municipio del lugar (municipio_de). Un aporte que no cumple se rechaza y se dice por qué.
#                    - Las estrellas (1 a 5) son la opinión de quien escribió la reseña, no una calificación oficial; la
#                      página lo dice.
# Datos de entrada:  docs/aportes/aportes.json y docs/aportes/fotos/ (los llena el equipo; ver docs/aportes/LEEME.md).
# Alimenta a:        Campaña: prueba social con material propio (Fase 8) y la sección "Lo que vivimos".

import hashlib
import io
import json
from datetime import date
from pathlib import Path

from PIL import Image, ExifTags

from torre.base.ubicaciones import municipio_de

RAIZ = Path(__file__).resolve().parents[3]
ENTRADA = RAIZ / "docs" / "aportes"
SALIDA = RAIZ / "frontend" / "fotos" / "aportes"
LUGARES = {"Chetumal": "004", "Bahía Calderitas–Oxtankah": "004", "Ruta arqueológica del sur": "004",
           "Maya Ka'an + Kantemó": ("002", "006"), "Laguna Milagros–Xul-Ha": "004",
           "Cancún": "005", "Riviera Maya": "008"}  # referencia en la parte del viajero (decisión 17)
OBLIGATORIOS = ("tipo", "lugar", "autor", "fecha", "texto", "permiso")


def _gps(im: Image.Image) -> tuple[float, float] | None:
    """Latitud y longitud del EXIF de la foto, si las trae."""
    try:
        g = im.getexif().get_ifd(ExifTags.IFD.GPSInfo)
    except Exception:  # noqa: BLE001 — una foto sin EXIF legible simplemente no tiene GPS
        return None
    if not g or 2 not in g or 4 not in g:
        return None
    conv = lambda v: float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600  # noqa: E731
    lat, lon = conv(g[2]), conv(g[4])
    return (-lat if g.get(1) == "S" else lat, -lon if g.get(3) == "W" else lon)


def validar(a: dict) -> str | None:
    """Motivo de rechazo, o None si el aporte cumple."""
    falta = [k for k in OBLIGATORIOS if not a.get(k)]
    if falta:
        return f"faltan campos: {', '.join(falta)}"
    if a["tipo"] not in ("foto", "resena"):
        return "tipo debe ser 'foto' o 'resena'"
    if a["lugar"] not in LUGARES:
        return f"lugar fuera de los 5 lugares: {a['lugar']}"
    if a["permiso"] is not True:
        return "sin permiso del autor"
    try:
        if date.fromisoformat(a["fecha"]) > date.today():
            return "fecha futura"
    except ValueError:
        return "fecha no es AAAA-MM-DD"
    if a["tipo"] == "resena" and not (isinstance(a.get("estrellas"), int) and 1 <= a["estrellas"] <= 5):
        return "una reseña lleva estrellas de 1 a 5"
    if a["tipo"] == "foto" and not (ENTRADA / "fotos" / str(a.get("archivo", ""))).is_file():
        return "no existe el archivo de la foto"
    return None


def preparar() -> dict:
    """Valida, copia las fotos a 1,200 px y devuelve {aportes, rechazados}."""
    f = ENTRADA / "aportes.json"
    lista = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
    salida, rechazados = [], []
    for a in lista:
        motivo = validar(a)
        if a.get("tipo") == "foto" and not motivo:
            im = Image.open(ENTRADA / "fotos" / a["archivo"])
            gps = _gps(im)
            esperado = LUGARES[a["lugar"]]
            if gps and municipio_de(*gps) not in (esperado if isinstance(esperado, tuple) else (esperado,)):
                motivo = "la ubicación GPS de la foto no cae en el municipio del lugar"
            else:
                im = im.convert("RGB")
                im.thumbnail((1200, 1200))
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=78, optimize=True, progressive=True)
                SALIDA.mkdir(parents=True, exist_ok=True)
                nombre = hashlib.sha256(buf.getvalue()).hexdigest()[:16] + ".jpg"
                (SALIDA / nombre).write_bytes(buf.getvalue())
                a = {**a, "archivo": f"fotos/aportes/{nombre}", "ancho": im.width, "alto": im.height,
                     "gps_comprobado": bool(gps)}
        if motivo:
            rechazados.append({"aporte": a.get("archivo") or a.get("texto", "")[:40], "motivo": motivo})
        else:
            salida.append({k: a[k] for k in ("tipo", "lugar", "autor", "fecha", "texto", "estrellas", "archivo",
                                              "ancho", "alto", "gps_comprobado") if k in a})
    return {"aportes": salida, "rechazados": rechazados}


if __name__ == "__main__":
    r = preparar()
    print(f"{len(r['aportes'])} aportes listos; {len(r['rechazados'])} rechazados")
    for x in r["rechazados"]:
        print("  rechazado:", x)
