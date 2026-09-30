# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Descarga de DataTur (SECTUR) los archivos oficiales: ocupación hotelera semanal y mensual,
#                    llegadas por nacionalidad y aeropuerto, visitantes del INAH, tráfico aéreo (AFAC), cruceros y
#                    el Compendio Estadístico 2024. Los guarda crudos en datos/bronze/datatur/<fecha>/ y los
#                    registra en el manifiesto con su huella SHA-256 y su número de filas.
# Por qué así:       La lista de archivos se lee de las propias páginas de DataTur (no se inventan nombres), así
#                    que si SECTUR publica una semana nueva se descarga sola.
#                    Verificado el 27-sep-2026: 135 zips semanales (2024-S01 → 2026-S31) y 31 mensuales
#                    (2024-01 → 2026-07). BD_Nacionalidad trae ~521,364 filas; BdINAH incluye las zonas
#                    arqueológicas de Q. Roo.
#                    Alternativa descartada: descargar a mano desde el navegador, que no es reproducible.
# Datos de entrada:  D2, D2m, D3 y D4 del inventario (https://datatur.sectur.gob.mx).
# Alimenta a:        A1 Radar (ocupación semanal del norte, presión INAH), buyer persona (nacionalidad y sexo por
#                    aeropuerto) y A3 Pronóstico (series mensuales).

import io
import re
import zipfile
from datetime import date

import openpyxl
import requests

from torre.base.manifiesto import BRONZE, registrar

BASE = "https://datatur.sectur.gob.mx"
UA = {"User-Agent": "Mozilla/5.0 (proyecto escolar UNRC)"}

# Páginas de DataTur donde viven los enlaces a los archivos, y qué fuente del inventario es cada una.
PAGINAS = {
    "hoteleria": ("/SitePages/hoteleria.aspx", "D2 DataTur ocupación hotelera"),
    "nacionalidad": ("/SitePages/upmnacionalidad.aspx", "D3 DataTur BD_Nacionalidad"),
    "inah": ("/SitePages/museosyzonasarqueologicas.aspx", "D4 DataTur BdINAH"),
    "afac": ("/SitePages/afac.aspx", "D4 DataTur DB_AFAC"),
    "cruceros": ("/SitePages/cruceros.aspx", "D4 DataTur cruceros"),
    "compendio": ("/SitePages/compendioestadistico.aspx", "D4 DataTur Compendio 2024"),
}


def enlaces_de(pagina: str) -> list[str]:
    """Devuelve las rutas de los .zip/.xlsx publicados en una página de DataTur, sin repetir y en orden."""
    texto = requests.get(BASE + pagina, headers=UA, timeout=60).text
    rutas = re.findall(r'href="(/Documentoscompartidos/[^"]+\.(?:zip|xlsx))"', texto, flags=re.I)
    return sorted(set(rutas))


def contar_filas(contenido: bytes, nombre: str) -> int | None:
    """Cuenta las filas de todas las hojas de los Excel dentro de un zip (o de un .xlsx suelto).

    Es el conteo "crudo": incluye encabezados y notas. El conteo limpio se hace en Silver.
    Se usa read_only para no cargar libros grandes completos en memoria.
    """
    def filas_xlsx(datos: bytes) -> int:
        libro = openpyxl.load_workbook(io.BytesIO(datos), read_only=True, data_only=True)
        total = sum((hoja.max_row or 0) for hoja in libro.worksheets)
        libro.close()
        return total

    try:
        if nombre.lower().endswith(".xlsx"):
            return filas_xlsx(contenido)
        with zipfile.ZipFile(io.BytesIO(contenido)) as z:
            excels = [n for n in z.namelist() if n.lower().endswith(".xlsx")]
            return sum(filas_xlsx(z.read(n)) for n in excels) if excels else None
    except Exception:
        return None  # archivo que no es Excel legible: se registra sin conteo y se revisa en Silver


def descargar_datatur(categorias=tuple(PAGINAS), contar: bool = True) -> list[dict]:
    """Descarga todos los archivos de las categorías pedidas y los registra en el manifiesto."""
    carpeta_base = BRONZE / "datatur" / date.today().isoformat()
    registros = []
    for categoria in categorias:
        pagina, fuente = PAGINAS[categoria]
        carpeta = carpeta_base / categoria
        carpeta.mkdir(parents=True, exist_ok=True)
        rutas = enlaces_de(pagina)
        print(f"{categoria}: {len(rutas)} archivos")
        for ruta in rutas:
            url = BASE + ruta
            nombre = ruta.rsplit("/", 1)[-1]
            destino = carpeta / nombre
            if not destino.exists():  # permite reanudar si se corta la red
                r = requests.get(url, headers=UA, timeout=300)
                r.raise_for_status()
                destino.write_bytes(r.content)
            filas = contar_filas(destino.read_bytes(), nombre) if contar else None
            registros.append(registrar(fuente, destino, url, filas=filas))
    return registros


if __name__ == "__main__":
    for fila in descargar_datatur():
        pass
    print("listo")
