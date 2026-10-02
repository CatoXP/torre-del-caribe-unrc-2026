# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña
# Qué hace:          La "vitrina" de la página: lo que convence de viajar, armado SOLO con datos que existen, para los 5
#                    lugares de la parte del viajero (Chetumal, Calderitas–Oxtankah, Ruta de las pirámides y, como
#                    referencia, Cancún y Riviera Maya). Cada pieza dice a qué lugar pertenece: la página muestra la del
#                    lugar elegido arriba.
#                    1. Postales: las fotos comprobadas de cada lugar.
#                    2. Experiencias: cada una con un dato real (INAH, DENUE, SITUR-Q, DataTur) y los negocios reales que
#                       la ofrecen, con su enlace a Google Maps.
#                    3. Rutas: paradas reales, distancia EN LÍNEA RECTA (no hay datos abiertos por carretera) y mejor mes.
# Por qué así:       - Brandon (02-oct-2026) pidió "secciones para vender más cosas" (decisión 16) y después cambiar Maya
#                      Ka'an y la Laguna Milagros, sin datos, por Cancún y Riviera Maya en toda la parte del viajero, y que
#                      "Vive el sur", rutas y postales cambien con el lugar elegido (decisión 17).
#                    - Cancún y Riviera Maya son REFERENCIA: sus experiencias llevan esa etiqueta y la ruta "Del Caribe al
#                      sur" les propone bajar en el Tren Maya. Sin precios: ninguna fuente oficial los publica.
#                    - Descartado: paquetes con precio, "lo más vendido" o reseñas copiadas (reglas de oro 1 y 4).
# Datos de entrada:  datos/silver/inah, datos/silver/siturq, datos/gold/lugares_clasificados, datos/gold/pronostico_*,
#                    datos/silver/clima_diario, frontend/fotos/lugares/creditos.json, Compendio DataTur (estrellas.py).
# Alimenta a:        Campaña (Fase 8): qué se ofrece en cada lugar, con qué mensaje y en qué mes.

import json
from pathlib import Path

import pandas as pd

from torre.base.silver_huracanes import km_haversine
from torre.campana.lugares import centros, enlace_maps, nombre_bonito

RAIZ = Path(__file__).resolve().parents[3]
SILVER = RAIZ / "datos" / "silver"
GOLD = RAIZ / "datos" / "gold"
FOTOS = RAIZ / "frontend" / "fotos" / "lugares"
VIAJERO = ["Chetumal", "Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur", "Cancún", "Riviera Maya"]
ZONAS_RUTA = ["Z.A. de Kohunlich", "Z.A. de Dzibanché-Kinichná", "Z.A de Ichkabal"]
ZONAS_CANCUN = ["Z.A. de El Meco", "Z.A. de El Rey", "Museo Maya de Cancún con Z. A"]


def _fotos() -> list[dict]:
    return json.loads((FOTOS / "creditos.json").read_text(encoding="utf-8"))


def _foto(lugar: str, orden: int, tipo: str = "lugar") -> dict:
    return next(f for f in _fotos() if f["lugar"] == lugar and f["orden"] == orden and f.get("tipo", "lugar") == tipo)


def postales() -> list[dict]:
    """Las fotos comprobadas de los 5 lugares del viajero; la página muestra las del lugar elegido."""
    c = [f for f in _fotos() if f["lugar"] in VIAJERO and f.get("tipo", "lugar") == "lugar"]
    c.sort(key=lambda f: (VIAJERO.index(f["lugar"]), f["orden"]))
    return [{k: f[k] for k in ("archivo", "muestra", "lugar", "autor", "licencia", "url_licencia", "url_original")}
            for f in c]


def _negocios(x: pd.DataFrame) -> list[dict]:
    return [{"n": nombre_bonito(f.nom_estab), "loc": nombre_bonito(f.localidad), "maps": enlace_maps(f.latitud, f.longitud),
             "resenas": enlace_maps(texto=f"{nombre_bonito(f.nom_estab)}, {nombre_bonito(f.localidad)}, Quintana Roo")}
            for f in x.itertuples()]


def _cercanos(d: pd.DataFrame, lugar: str, n: int = 4) -> pd.DataFrame:
    la, lo = centros()[lugar]
    x = d.assign(km=[km_haversine(a, b, la, lo) for a, b in zip(d.latitud, d.longitud)]).sort_values("km")
    return x.drop_duplicates(subset="nom_estab").head(n)  # sin nombres repetidos ("Antojitos Yucatecos" ×2)


def _sitio(nombre: str) -> dict:
    return {"n": nombre, "loc": "Zona arqueológica (INAH)", "maps": enlace_maps(texto=f"{nombre}, Quintana Roo"),
            "resenas": enlace_maps(texto=f"{nombre}, Quintana Roo")}


def experiencias(vacios_de_cada_10: int | None = None, hospedajes: dict | None = None) -> list[dict]:
    """hospedajes = tamaño de los hospedajes del DENUE en los municipios del sur (datos_pagina.hospedaje)."""
    from torre.campana.estrellas import estrellas

    d = pd.read_parquet(GOLD / "lugares_clasificados.parquet")
    d = d[d.clasificado]
    i = pd.read_parquet(SILVER / "inah", columns=["nombre", "periodo", "visitantes", "estado"])
    i = i[i.estado == "Quintana Roo"]
    i = i.assign(nombre=i.nombre.astype(str), anio=pd.to_datetime(i.periodo).dt.year, mes=pd.to_datetime(i.periodo).dt.month)
    completo = int(i[i.mes == 12].anio.max())  # último año con diciembre publicado
    visitas = lambda zonas: int(i[i.nombre.isin(zonas) & (i.anio == completo)].visitantes.sum())  # noqa: E731
    ruta, oxt, cancun = visitas(ZONAS_RUTA), visitas(["Z.A. de Oxtankah"]), visitas(ZONAS_CANCUN)
    est = estrellas()
    km = round(km_haversine(*centros()["Chetumal"], *centros()["Bahía Calderitas–Oxtankah"]))
    mariscos = d[(d.lugar == "Bahía Calderitas–Oxtankah") & (d.tipo == "Mariscos y pescado")]
    museos_che = d[(d.lugar == "Chetumal") & (d.tipo == "Museo")]
    antojos = d[(d.lugar == "Cancún") & d.tipo.isin(["Antojitos", "Cocina yucateca", "Tacos y tortas"])]
    comer_playa = d[(d.lugar == "Riviera Maya") & (d.grupo == "comer")]
    yucateca = d[(d.lugar == "Cancún") & (d.tipo == "Cocina yucateca")]
    carta_playa = d[(d.lugar == "Riviera Maya") & d.tipo.isin(["Restaurante a la carta", "Mariscos y pescado"])]
    pct5 = lambda l: est[l]["por_categoria"].get(5, 0)  # noqa: E731
    f = lambda l, n, t="lugar": _foto(l, n, t)["archivo"]  # noqa: E731
    return [
        {"clave": "piramides", "titulo": "Pirámides en la selva", "lugar": "Ruta arqueológica del sur",
         "texto": "Kohunlich, Dzibanché e Ichkabal: ciudades mayas entre la selva, con sus mascarones y templos.",
         "dato": f"Unas {round(ruta / 365):,} personas al día entre las tres zonas en {completo}: tienes la pirámide casi para ti.",
         "fuente": "INAH", "foto": f("Ruta arqueológica del sur", 1),
         "negocios": [_sitio(z) for z in ["Zona Arqueológica de Kohunlich", "Zona Arqueológica de Dzibanché",
                                          "Zona Arqueológica de Ichkabal"]]},
        {"clave": "mariscos", "titulo": "Mariscos frente a la bahía", "lugar": "Bahía Calderitas–Oxtankah",
         "texto": f"En Calderitas, a {km} km de Chetumal, se come viendo el agua; al lado está Oxtankah, la ciudad maya "
                  "de la bahía.",
         "dato": f"{len(mariscos)} marisquerías en Calderitas y {oxt:,} visitantes a Oxtankah en {completo}.",
         "fuente": "INEGI (DENUE) e INAH", "foto": f("Bahía Calderitas–Oxtankah", 3),
         "negocios": _negocios(_cercanos(mariscos, "Bahía Calderitas–Oxtankah"))},
        {"clave": "museos", "titulo": "Museos de la cultura maya", "lugar": "Chetumal",
         "texto": "El Museo de la Cultura Maya, el planetario y la historia de la ciudad, a pasos de la bahía.",
         "dato": f"{len(museos_che)} museos en Chetumal según el directorio del INEGI.",
         "fuente": "INEGI (DENUE)", "foto": f("Chetumal", 2),
         "negocios": sorted(_negocios(museos_che), key=lambda n: (not "Cultura Maya" in n["n"], n["n"]))[:4]},
        {"clave": "atardecer", "titulo": "Atardecer en el malecón", "lugar": "Chetumal",
         "texto": "El Boulevard Bahía de Chetumal: casas de madera, monumentos y el sol bajando sobre el agua.",
         "dato": (f"Hay lugar: {vacios_de_cada_10} de cada 10 cuartos de hotel de Chetumal se quedaron vacíos en 2024."
                  if vacios_de_cada_10 is not None else "Hay lugar: Chetumal tiene cuartos de hotel libres."),
         "fuente": "Gobierno de Quintana Roo (SITUR-Q)", "foto": f("Chetumal", 1),
         "negocios": [{"n": "Boulevard Bahía", "loc": "Chetumal", "maps": enlace_maps(texto="Boulevard Bahía, Chetumal"),
                       "resenas": enlace_maps(texto="Boulevard Bahía, Chetumal, Quintana Roo")}]},
        # Referencia: el norte (la campaña no lo promueve; si el mes está lleno, la página recomienda el sur)
        {"clave": "cancun_zonas", "titulo": "Zonas mayas dentro de Cancún", "lugar": "Cancún", "referencia": True,
         "texto": "El Meco, El Rey y el Museo Maya de Cancún: ciudades mayas entre los hoteles y la laguna.",
         "dato": f"{cancun:,} visitantes en {completo} entre las tres: unas {round(cancun / 365):,} al día.",
         "fuente": "INAH", "foto": f("Cancún", 3),
         "negocios": [_sitio(z) for z in ["Zona Arqueológica de El Meco", "Zona Arqueológica de El Rey",
                                          "Museo Maya de Cancún"]]},
        {"clave": "cancun_hoteles", "titulo": "La zona hotelera", "lugar": "Cancún", "referencia": True,
         "texto": "Playa Gaviota Azul y la punta de Cancún: arena blanca entre el mar y la laguna Nichupté.",
         # Solo la parte de 5 estrellas: la cuenta de cuartos de DataTur (hoteles que monitorea) no coincide con la de
         # SITUR-Q (registro estatal) que muestra la ficha; dos cifras distintas del "mismo" dato confundirían.
         "dato": f"{pct5('Cancún')} % de sus cuartos de hotel son de 5 estrellas, según la categoría oficial ({est['Cancún']['anio']}).",
         "fuente": "SECTUR-DataTur (Compendio 2024)", "foto": f("Cancún", 1),
         "negocios": [{"n": "Playa Gaviota Azul", "loc": "Zona hotelera", "maps": enlace_maps(texto="Playa Gaviota Azul, Cancún"),
                       "resenas": enlace_maps(texto="Playa Gaviota Azul, Cancún, Quintana Roo")}]},
        {"clave": "cancun_antojitos", "titulo": "Antojitos y Mercado 28", "lugar": "Cancún", "referencia": True,
         "texto": "Panuchos, salbutes y tacos en el centro, lejos de la zona hotelera.",
         "dato": f"{len(antojos):,} lugares de antojitos, tacos y cocina yucateca en la ciudad según el directorio del INEGI.",
         "fuente": "INEGI (DENUE)", "foto": f("Cancún", 1, "comida"),
         "negocios": _negocios(_cercanos(yucateca, "Cancún"))},
        {"clave": "playa_quinta", "titulo": "La Quinta Avenida", "lugar": "Riviera Maya", "referencia": True,
         "texto": "La calle peatonal de Playa del Carmen: restaurantes, tiendas y el mar a una cuadra.",
         "dato": f"{len(comer_playa):,} lugares para comer en Playa del Carmen según el directorio del INEGI.",
         "fuente": "INEGI (DENUE)", "foto": f("Riviera Maya", 3),
         "negocios": _negocios(_cercanos(carta_playa, "Riviera Maya"))},
        {"clave": "playa_portal", "titulo": "El Portal Maya y los Voladores", "lugar": "Riviera Maya", "referencia": True,
         "texto": "El parque Fundadores frente al mar, con el Portal Maya y la danza de los Voladores.",
         "dato": f"{pct5('Riviera Maya')} % de los cuartos de hotel de Playa del Carmen son de 5 estrellas, según la "
                 f"categoría oficial ({est['Riviera Maya']['anio']}).",
         "fuente": "SECTUR-DataTur (Compendio 2024)", "foto": f("Riviera Maya", 4),
         "negocios": [{"n": "Parque Fundadores", "loc": "Playa del Carmen",
                       "maps": enlace_maps(texto="Parque Fundadores, Playa del Carmen"),
                       "resenas": enlace_maps(texto="Parque Fundadores, Playa del Carmen, Quintana Roo")}]},
    ]


def _mejor_mes(lugares: list[str], punto: str) -> dict:
    """Mes del año para una ruta del sur: ningún lugar en temporada alta, sin temporada de tormentas (< 9 %) y con
    lluvia menor que la mediana; entre esos, el de menos gente (índice promedio más bajo)."""
    from torre.pronostico.calendario import ALTA_INDICE, TORMENTA_TEMPORADA, clima_normal

    forma = pd.read_parquet(GOLD / "pronostico_forma_anio.parquet")
    tormenta = pd.read_parquet(GOLD / "pronostico_poisson_tormentas.parquet").set_index("mes").prob_tormenta
    lluvia = clima_normal().set_index(["punto", "mes"]).lluvia_mm.loc[punto]
    ok = [m for m in range(1, 13) if tormenta[m] < TORMENTA_TEMPORADA and lluvia[m] < lluvia.median()]
    idx = forma[forma.lugar.isin(lugares)].groupby("mes").indice.agg(["max", "mean"])
    ok = [m for m in ok if idx.loc[m, "max"] < ALTA_INDICE]
    m = min(ok, key=lambda m: idx.loc[m, "mean"])
    return {"mes": int(m), "por_que": "menos gente, poca lluvia y sin temporada de tormentas"}


def _mejor_mes_norte(lugar: str) -> dict:
    """Norte: ningún mes es tranquilo, seco y sin tormentas a la vez (decisión 15). Se da el menos lleno de los meses
    secos y sin tormentas, con su ocupación típica, para que se vea que aun así está concurrido."""
    from torre.pronostico.calendario import NORTE, TORMENTA_TEMPORADA, clima_normal, ocupacion_tipica, tormentas_punto

    serie, punto = NORTE[lugar]
    oc, t = ocupacion_tipica(serie), tormentas_punto(punto)
    lluvia = clima_normal().set_index(["punto", "mes"]).lluvia_mm.loc[punto]
    ok = [m for m in range(1, 13) if t[m] < TORMENTA_TEMPORADA and lluvia[m] < lluvia.median()]
    m = min(ok, key=lambda m: oc[m])
    return {"mes": int(m), "por_que": f"el menos lleno de los meses secos y sin tormentas; aun así, hoteles al {round(oc[m])} %"}


def rutas() -> list[dict]:
    cen = centros()
    def km(a, b):  # noqa: E306
        return round(km_haversine(*a, *b))
    def coord(lugar, n):  # noqa: E306
        x = _foto(lugar, n)
        return x["lat"], x["lon"]
    r1 = ["Chetumal", "Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur"]
    sur = _mejor_mes(r1, "chetumal")
    c1, c3, c4 = coord("Cancún", 1), coord("Cancún", 3), coord("Cancún", 4)
    p3, p2, p6 = coord("Riviera Maya", 3), coord("Riviera Maya", 2), coord("Riviera Maya", 6)
    return [
        {"titulo": "Bahía y pirámides", "dias": 2, "lugares": r1, "planeador": "Ruta arqueológica del sur",
         "foto": _foto("Bahía Calderitas–Oxtankah", 1)["archivo"],
         "paradas": ["Chetumal: el malecón y el Museo de la Cultura Maya", "Calderitas: mariscos y la zona de Oxtankah",
                     "Kohunlich y Dzibanché, en la selva"],
         "km": [km(cen[a], cen[b]) for a, b in zip(r1, r1[1:])], **sur},
        {"titulo": "Del Caribe al sur en Tren Maya", "dias": 3, "lugares": ["Cancún", "Riviera Maya"], "planeador": "Chetumal",
         "foto": _foto("Chetumal", 1)["archivo"],
         "paradas": ["Cancún o Playa del Carmen: subir al Tren Maya", "Chetumal: el malecón al atardecer",
                     "Calderitas: mariscos y la zona de Oxtankah", "Kohunlich y Dzibanché, en la selva"],
         "km": [km(cen["Cancún"], cen["Chetumal"])] + [km(cen[a], cen[b]) for a, b in zip(r1, r1[1:])], **sur},
        {"titulo": "Cancún en 2 días", "dias": 2, "lugares": ["Cancún"], "planeador": "Cancún", "referencia": True,
         "foto": _foto("Cancún", 2)["archivo"],
         "paradas": ["La zona hotelera y Playa Gaviota Azul", "El Mercado 28 y los antojitos del centro",
                     "La zona arqueológica de El Meco"],
         "km": [km(c1, c4), km(c4, c3)], **_mejor_mes_norte("Cancún")},
        {"titulo": "Playa del Carmen en un día", "dias": 1, "lugares": ["Riviera Maya"], "planeador": "Riviera Maya",
         "referencia": True, "foto": _foto("Riviera Maya", 1)["archivo"],
         "paradas": ["La Quinta Avenida", "El parque Fundadores y el Portal Maya", "La playa del pueblo"],
         "km": [km(p3, p2), km(p2, p6)], **_mejor_mes_norte("Riviera Maya")},
    ]


def vitrina(vacios_de_cada_10: int | None = None, hospedajes: dict | None = None) -> dict:
    return {"postales": postales(), "experiencias": experiencias(vacios_de_cada_10, hospedajes), "rutas": rutas(),
            "nota": "Distancias en línea recta (no hay datos abiertos de distancias por carretera). Sin precios: ninguna "
                    "fuente oficial los publica. Las reseñas se leen en Google Maps."}


if __name__ == "__main__":
    v = vitrina(4)
    print(len(v["postales"]), "postales")
    for e in v["experiencias"]:
        print(e["lugar"][:10], "|", e["titulo"], "|", e["dato"], "|", [n["n"] for n in e["negocios"]])
    for r in v["rutas"]:
        print(r["titulo"], r["lugares"], r["dias"], r["km"], r["mes"], r["por_que"])
