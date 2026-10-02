# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña
# Qué hace:          Arma, para cada uno de los 5 lugares, qué hacer de día, por la tarde y de noche, dónde comer y dónde
#                    dormir, con negocios REALES del Directorio Estadístico Nacional de Unidades Económicas (DENUE,
#                    INEGI). Un clasificador de texto (NLP por léxico) lee el nombre y el giro oficial de cada negocio y
#                    decide qué es (tipo de comida, bar, museo, hotel…) y en qué momento del día conviene. Cada lugar
#                    lleva un enlace oficial de Google Maps con sus coordenadas.
# Por qué así:       - Decisión de Brandon (01-oct-2026, "DENUE + botón Google Maps"): no se hace scraping de Google Maps
#                      ni de TripAdvisor (lo prohíben sus términos y la regla 4 de CLAUDE.md). El botón usa la dirección
#                      pública de Google Maps (https://www.google.com/maps/search/?api=1&query=lat,lon): no descarga
#                      nada, no usa llave y solo pide internet cuando la persona da clic.
#                    - Decisión de Brandon ("Clasificar giros y nombres"): las reseñas de Rest-Mex no cubren ninguno
#                      de los 5 lugares (solo Tulum, Isla Mujeres y Bacalar), así que el NLP se aplica a lo que sí
#                      existe: el nombre y el giro de cada negocio. Es un clasificador por léxico (diccionario de
#                      palabras clave → categoría), explicable regla por regla; no hay etiquetas para entrenar un modelo.
#                    - Se excluye lo que no le sirve a un visitante: negocios "SIN NOMBRE" (no se pueden encontrar),
#                      cooperativas escolares, clubes de nutrición, gimnasios, venta de lotería y moteles.
#                    - DENUE no publica horarios: el momento del día es una SUGERENCIA por tipo de lugar y así se dice
#                      en la página. Tampoco trae calificaciones: el orden es por cercanía al centro del lugar, no por
#                      calidad.
#                    - Regla de oro 9: solo se recomiendan negocios de las localidades de los 5 lugares. Si un lugar no
#                      tiene de algo (la Ruta no tiene hoteles), se toma el más cercano de los otros 4 lugares; nunca
#                      de Bacalar, Mahahual ni el norte.
# Datos de entrada:  datos/silver/denue (Q. Roo), datos/silver/iter (centro de cada lugar), torre.base.silver_iter.
# Alimenta a:        La sección "Qué hacer" de la página (campaña: qué ofrece cada lugar, en lenguaje de viajero) y la
#                    oferta por lugar que usará la Fase 8 para los mensajes.

import math
import re
import unicodedata
from pathlib import Path

import pandas as pd

from torre.base.silver_huracanes import km_haversine
from torre.base.silver_iter import REGION_LOCALIDADES

RAIZ = Path(__file__).resolve().parents[3]
SILVER = RAIZ / "datos" / "silver"
GOLD = RAIZ / "datos" / "gold"

LUGARES = [r for r in REGION_LOCALIDADES if "referencia" not in r]
KOHUNLICH = (18.4197, -88.7903)  # punto de la Ruta (mismo que el mapa y el clima)
POR_MOMENTO = 6                  # negocios que se muestran por momento del día
ZONAS_INAH = {"Bahía Calderitas–Oxtankah": ["Zona Arqueológica de Oxtankah"],
              "Ruta arqueológica del sur": ["Zona Arqueológica de Kohunlich", "Zona Arqueológica de Dzibanché",
                                            "Zona Arqueológica de Ichkabal"]}


def normalizar(texto: str) -> str:
    """Mayúsculas sin acentos ni signos: 'Marisquería El Güero' → 'MARISQUERIA EL GUERO'."""
    t = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9 ]+", " ", t.upper()).strip()


# ---------- El léxico (NLP por diccionario) ----------
# Cada categoría tiene raíces de palabra; gana la primera categoría cuya raíz aparece en el nombre. El orden importa:
# "MARISCOS Y ANTOJITOS" es primero mariscos. Si el nombre no dice nada, decide el giro oficial (código SCIAN).
EXCLUIR = ["SIN NOMBRE", "ESCOLAR", "ESCUELA", "PRIMARIA", "SECUNDARIA", "NUTRICION", "HERBALIFE", "COOPERATIVA",
           "ESTACIONAMIENTO", "OFICINA",
           # Centros para adultos: no se recomiendan en una página familiar de turismo.
           "MENS CLUB", "MEN S CLUB", "TABLE DANCE", "TEIBOL", "GENTLEMEN", "CABARET"]
# Puestos callejeros de juegos (canicas, brincolines) y canchas: no son una salida para un visitante.
EXCLUIR_HACER = ["PUESTO", "CANICAS", "BRINCOLIN", "CAMPO DEPORTIVO", "CANCHA"]
LEXICO_COMIDA = [
    ("Mariscos y pescado", ["MARISC", "PESCAD", "COCTEL", "CEVICH", "CAMARON", "OSTION", "PULPO"]),
    ("Cocina yucateca", ["COCHINITA", "PANUCH", "SALBUT", "POC CHUC", "RELLENO NEGRO", "YUCATEC", "CODZITO",
                         "PAPADZUL", "LECHON", "MUCBIPOLLO", "PIBIPOLLO", "PIBIL"]),
    ("Antojitos", ["ANTOJIT", "EMPANAD", "TAMAL", "QUESADILL", "GARNACH", "SOPE", "GORDITA", "TLAYUD"]),
    ("Tacos y tortas", ["TAQUER", "TACO", "TORTA", "CARNITAS", "PASTOR", "BARBACOA"]),
    ("Café, desayunos y postres", ["CAFE", "DESAYUN", "POSTRE", "PANADER", "PASTEL", "JUGO", "LICUAD", "MACHACAD", "NEVERI",
                                 "PALETER", "HELAD", "CREPA", "MARQUESITA", "RASPAD", "AGUAS FRESCAS"]),
    ("Asados y pollos", ["ASAD", "POLLO", "POLLER", "ROSTIZ", "GRILL", "PARRILL", "ALITAS", "CHICKEN", "CARNE"]),
    ("Pizzas y hamburguesas", ["PIZZ", "HAMBURGUES", "BURGER", "HOT DOG", "DOGS"]),
    # Internacional va antes que casera: "COCINA JAPONESA" no es comida casera (error hallado en la muestra 2).
    ("Cocina internacional", ["CHINA", "CHINO", "SUSHI", "ITALIAN", "PASTA", "ARGENTIN", "JAPONES", "THAI"]),
    ("Comida casera", ["COCINA ECONOMICA", "COMIDA CORRIDA", "COMIDA CASERA", "LONCHER", "FONDA", "COCINA DE"]),
]
NOCHE_NOMBRE = ["BAR", "CANTINA", "BOTANER", "MICHELAD", "CERVECER", "MEZCALER", "PUB", "LOUNGE", "CENADUR"]
GIRO_COMIDA = {"722512": "Mariscos y pescado", "722513": "Antojitos", "722514": "Tacos y tortas",
               "722515": "Café, desayunos y postres", "722517": "Pizzas y hamburguesas", "722511": "Restaurante a la carta",
               "722516": "Restaurante a la carta", "722518": "Comida para llevar", "722519": "Comida para llevar",
               "722320": "Comida para llevar", "722330": "Comida para llevar"}
GIRO_HOSPEDAJE = {"721111": "Hotel", "721112": "Hotel", "721190": "Cabañas y villas",
                  "721311": "Casa de huéspedes", "721210": "Campamento"}
GIRO_DIA = {"712111": "Museo", "712112": "Museo", "712131": "Jardín botánico o zoológico",
            "712132": "Jardín botánico o zoológico", "487210": "Paseo en lancha", "561510": "Agencia de viajes y tours",
            "561520": "Agencia de viajes y tours"}
GIRO_TARDE = {"713113": "Balneario", "713114": "Balneario", "713111": "Parque", "713112": "Parque",
              "713998": "Recreación"}
# El nombre gana al giro en hospedaje: "HOTEL COSTA AZUL" viene con giro de casa de huéspedes.
LEXICO_HOSPEDAJE = [("Hostal", ["HOSTAL", "HOSTEL", "HOSTE L"]), ("Hotel", ["HOTEL"]), ("Posada", ["POSADA"]),
                    ("Cabañas y villas", ["CABANA", "VILLA", "BUNGALOW", "GLAMPING"])]
GIRO_NOCHE = {"722412": "Bar o cantina", "722411": "Centro nocturno"}

# Momento sugerido para la comida (DENUE no publica horarios: es una regla por tipo de lugar).
MOMENTO_COMIDA = {"Café, desayunos y postres": "dia", "Mariscos y pescado": "tarde", "Comida casera": "tarde",
                  "Restaurante a la carta": "tarde", "Asados y pollos": "tarde", "Cocina internacional": "tarde",
                  "Cocina yucateca": "tarde", "Antojitos": "noche", "Tacos y tortas": "noche", "Pizzas y hamburguesas": "noche",
                  "Comida para llevar": "tarde"}


def tiene(texto: str, raices: list[str]) -> bool:
    """¿Alguna raíz aparece AL INICIO de una palabra? Evita falsos positivos de buscar dentro de la palabra:
    "MICHELADAS" contiene "HELAD" (de helados) y "BARBACOA" contiene "BAR"; con esta regla ninguno cuenta."""
    return any(re.search(r"(?<![A-Z0-9])" + re.escape(r) + (r"(?![A-Z])" if r in PALABRA_COMPLETA else ""), texto)
               for r in raices)


PALABRA_COMPLETA = {"BAR", "PUB", "CAFE", "CARNE", "PASTA", "CHINA", "CHINO", "DOGS", "VILLA"}


def clasificar(nombre: str, codigo_act: str) -> dict | None:
    """Clasificador por léxico de un negocio: devuelve tipo, grupo (comer, dormir, hacer) y momento sugerido, o None
    si no le sirve a un visitante. Primero lee el NOMBRE; si no dice nada, usa el GIRO oficial (SCIAN)."""
    n, c = f" {normalizar(nombre)} ", str(codigo_act)
    if tiene(n, EXCLUIR) or c in {"721113", "722320"}:  # sin nombre, escolar…, moteles y banquetes
        return None
    if c in GIRO_HOSPEDAJE:
        for tipo, raices in LEXICO_HOSPEDAJE:
            if tiene(n, raices):
                return {"tipo": tipo, "grupo": "dormir", "momento": "noche", "regla": "nombre"}
        return {"tipo": GIRO_HOSPEDAJE[c], "grupo": "dormir", "momento": "noche", "regla": f"giro {c}"}
    # "AGUAS FRESCAS Y RASPADOS" con giro de bar es bebida sin alcohol. Solo cuentan señales sin alcohol: "CAFE" no,
    # porque "DISCO ROCK SHOTS CAFE" es un centro nocturno.
    bebida = ["RASPAD", "AGUAS FRESCAS", "JUGO", "LICUAD", "PALETER", "HELAD", "NEVERI", "MACHACAD"]
    if c in GIRO_NOCHE and tiene(n, bebida):
        return {"tipo": "Café, desayunos y postres", "grupo": "comer", "momento": "dia", "regla": "nombre"}
    if c in GIRO_NOCHE or (c.startswith("722") and tiene(n, NOCHE_NOMBRE)):
        tipo = GIRO_NOCHE.get(c, "Bar o cantina")
        return {"tipo": tipo, "grupo": "hacer", "momento": "noche", "regla": f"giro {c}" if c in GIRO_NOCHE else "nombre"}
    if (c in GIRO_DIA or c in GIRO_TARDE) and tiene(n, EXCLUIR_HACER):
        return None
    if c in GIRO_DIA:
        return {"tipo": GIRO_DIA[c], "grupo": "hacer", "momento": "dia", "regla": f"giro {c}"}
    if c in GIRO_TARDE:
        return {"tipo": GIRO_TARDE[c], "grupo": "hacer", "momento": "tarde", "regla": f"giro {c}"}
    if c.startswith("722"):
        for tipo, raices in LEXICO_COMIDA:
            if tiene(n, raices):
                return {"tipo": tipo, "grupo": "comer", "momento": MOMENTO_COMIDA[tipo], "regla": "nombre"}
        if c == "722517" and not tiene(n, ["PIZZ", "HAMBURGUES", "BURGER", "DOG"]):
            # El giro 722517 junta pizzas, hamburguesas, hot dogs y pollos rostizados: sin pista en el nombre, se dice
            # "comida rápida" y no se adivina cuál de las cuatro.
            return {"tipo": "Comida rápida", "grupo": "comer", "momento": "noche", "regla": f"giro {c}"}
        if c in GIRO_COMIDA:
            tipo = GIRO_COMIDA[c]
            return {"tipo": tipo, "grupo": "comer", "momento": MOMENTO_COMIDA[tipo], "regla": f"giro {c}"}
    return None  # gimnasios, lotería, billares, ligas deportivas…: no se recomiendan


def nombre_bonito(nombre: str) -> str:
    """'MARISQUERIA EL GUERO' → 'Marisquería El Guero' (solo mayúsculas iniciales; las palabras cortas, en minúscula)."""
    chicas = {"de", "del", "la", "las", "el", "los", "y", "e", "en", "a", "con"}
    palabras = re.sub(r"^\d{4,}\s+", "", str(nombre).strip()).lower().split()  # "38989 STARBUCKS…" → "Starbucks…"
    return " ".join(p if (i and p in chicas) else p[:1].upper() + p[1:] for i, p in enumerate(palabras))


def centros() -> dict:
    """Centro de cada lugar: su localidad principal del Censo 2020 (la Ruta, en Kohunlich), igual que el mapa."""
    censo = pd.read_parquet(SILVER / "iter")
    censo = censo[censo.tipo_fila == "localidad"] if "tipo_fila" in censo else censo
    salida = {}
    for lugar in LUGARES:
        mun, loc, _ = REGION_LOCALIDADES[lugar][0]
        fila = censo[(censo.cve_mun.astype(str).str.zfill(3) == mun) & (censo.cve_loc.astype(str).str.zfill(4) == loc)]
        salida[lugar] = (float(fila.latitud.iloc[0]), float(fila.longitud.iloc[0]))
    salida["Ruta arqueológica del sur"] = KOHUNLICH
    return salida


def negocios() -> pd.DataFrame:
    """Negocios de las localidades de los 5 lugares, clasificados. Una fila por negocio que le sirve a un visitante."""
    d = pd.read_parquet(SILVER / "denue", filters=[("es_qroo", "==", True)],
                        columns=["id", "nom_estab", "codigo_act", "nombre_act", "cve_mun", "cve_loc", "localidad",
                                 "latitud", "longitud", "per_ocu"])
    d["cve_mun"], d["cve_loc"] = d.cve_mun.astype(str).str.zfill(3), d.cve_loc.astype(str).str.zfill(4)
    de_lugar = {(m, l): lugar for lugar in LUGARES for m, l, _ in REGION_LOCALIDADES[lugar]}
    d["lugar"] = [de_lugar.get(k) for k in zip(d.cve_mun, d.cve_loc)]
    d = d[d.lugar.notna()].copy()
    clase = [clasificar(n, c) for n, c in zip(d.nom_estab, d.codigo_act)]
    d["clasificado"] = [c is not None for c in clase]
    for campo in ("tipo", "grupo", "momento", "regla"):
        d[campo] = [c[campo] if c else None for c in clase]
    return d


def recomendaciones(d: pd.DataFrame | None = None) -> pd.DataFrame:
    """Para cada lugar y cada (grupo, momento): los más cercanos a su centro, alternando tipos para que no salgan seis
    taquerías seguidas. Si el lugar no tiene de algo, se completa con los más cercanos de los otros 4 lugares."""
    d = negocios() if d is None else d
    d = d[d.clasificado]
    cen = centros()
    filas = []
    for lugar, (la, lo) in cen.items():
        todos = d.assign(km=[km_haversine(a, b, la, lo) for a, b in zip(d.latitud, d.longitud)])
        for grupo, momento in [("hacer", "dia"), ("comer", "dia"), ("hacer", "tarde"), ("comer", "tarde"),
                               ("hacer", "noche"), ("comer", "noche"), ("dormir", "noche")]:
            cand = todos[(todos.grupo == grupo) & (todos.momento == momento)]
            propios = cand[cand.lugar == lugar].sort_values("km")
            otros = cand[cand.lugar != lugar].sort_values("km")
            elegidos = _alternar(propios, POR_MOMENTO)
            if len(elegidos) < POR_MOMENTO:
                elegidos = pd.concat([elegidos, _alternar(otros, POR_MOMENTO - len(elegidos))])
            for _, f in elegidos.iterrows():
                filas.append({"lugar": lugar, "grupo": grupo, "momento": momento, "nombre": nombre_bonito(f.nom_estab),
                              "tipo": f.tipo, "localidad": nombre_bonito(f.localidad), "km": round(f.km, 1),
                              "de_otro_lugar_flag": f.lugar != lugar, "lat": round(f.latitud, 5),
                              "lon": round(f.longitud, 5), "regla": f.regla, "denue_id": int(f["id"])})
    return pd.DataFrame(filas)


def _alternar(x: pd.DataFrame, n: int) -> pd.DataFrame:
    """Toma n filas ya ordenadas por distancia, pero rotando por tipo (la más cercana de cada tipo, luego la segunda…)."""
    if x.empty or n <= 0:
        return x.head(0)
    x = x.assign(_rango=x.groupby("tipo").cumcount())
    return x.sort_values(["_rango", "km"]).head(n).drop(columns="_rango")


def resumen_nlp(d: pd.DataFrame) -> pd.DataFrame:
    """Cuántos negocios turísticos (giros 721, 722, 712, 713, 487, 561) quedaron clasificados y por qué regla."""
    turisticos = d[d.codigo_act.astype(str).str[:3].isin(["721", "722", "712", "713", "487", "561"])]
    return pd.DataFrame({
        "negocios_turisticos": [len(turisticos)],
        "clasificados": [int(turisticos.clasificado.sum())],
        "por_nombre": [int((turisticos.regla == "nombre").sum())],
        "por_giro": [int(turisticos.regla.fillna("").str.startswith("giro").sum())],
        "excluidos": [int((~turisticos.clasificado).sum())],
    })


def guardar():
    d = negocios()
    r = recomendaciones(d)
    GOLD.mkdir(parents=True, exist_ok=True)
    r.to_parquet(GOLD / "lugares_recomendados.parquet", index=False)
    d.drop(columns=["per_ocu"]).to_parquet(GOLD / "lugares_clasificados.parquet", index=False)
    return d, r


def enlace_maps(lat: float | None = None, lon: float | None = None, texto: str | None = None) -> str:
    """Dirección pública de Google Maps (sin llave, sin descarga): por coordenadas o, si no hay, por nombre."""
    from urllib.parse import quote

    q = f"{lat},{lon}" if lat is not None and not (isinstance(lat, float) and math.isnan(lat)) else texto
    return f"https://www.google.com/maps/search/?api=1&query={quote(str(q))}"


if __name__ == "__main__":
    d, r = guardar()
    pd.set_option("display.width", 200)
    print(resumen_nlp(d).to_string(index=False))
    print(d[d.clasificado].groupby(["lugar", "grupo"]).size().unstack(fill_value=0).to_string())
    print(r.groupby(["lugar", "grupo", "momento"]).size().unstack(fill_value=0).to_string())
    print(r[r.lugar == "Chetumal"][["momento", "grupo", "nombre", "tipo", "km"]].to_string(index=False))
