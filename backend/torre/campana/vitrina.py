# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña
# Qué hace:          La "vitrina" de la página: lo que convence de viajar al sur, armado SOLO con datos que existen.
#                    1. Postales: tira horizontal con las 28 fotos comprobadas de los 5 lugares (nunca del norte).
#                    2. Experiencias: 6 cosas que hacer en el sur, cada una con un dato real (INAH, DENUE, SITUR-Q) y
#                       los negocios reales que la ofrecen, con su enlace a Google Maps.
#                    3. Rutas de 2 y 3 días: paradas reales, distancia EN LÍNEA RECTA entre ellas (no hay datos
#                       abiertos de distancias por carretera) y el mejor mes según el planeador.
# Por qué así:       - Brandon (02-oct-2026) pidió "más cosas para convencer a las personas de viajar… secciones para
#                      vender más cosas" y eligió "Experiencias reales", "Rutas de 2–3 días" y "Llamados de campaña".
#                      No hay precios oficiales de nada: no se muestra ningún precio (regla de oro 1).
#                    - Descartado: paquetes con precio o "más vendido" (inventaría datos) y reseñas copiadas de Google o
#                      TripAdvisor (regla de oro 4). Cada negocio lleva "Reseñas en Google": se leen allá, al dar clic.
#                    - Los textos de cada experiencia son descripciones cortas del lugar; las cifras salen de las tablas.
# Datos de entrada:  datos/silver/inah, datos/gold/lugares_clasificados, datos/gold/pronostico_calendario,
#                    datos/silver/clima_diario, datos/silver/iter, frontend/fotos/lugares/creditos.json.
# Alimenta a:        Campaña (Fase 8): qué se ofrece del sur, con qué mensaje y en qué mes; la página lo muestra ya.

import json
from pathlib import Path

import pandas as pd

from torre.base.silver_huracanes import km_haversine
from torre.base.silver_iter import REGION_LOCALIDADES
from torre.campana.lugares import NORTE, centros, enlace_maps, nombre_bonito

RAIZ = Path(__file__).resolve().parents[3]
SILVER = RAIZ / "datos" / "silver"
GOLD = RAIZ / "datos" / "gold"
FOTOS = RAIZ / "frontend" / "fotos" / "lugares"
ZONAS_RUTA = ["Z.A. de Kohunlich", "Z.A. de Dzibanché-Kinichná", "Z.A de Ichkabal"]


def postales() -> list[dict]:
    """Las fotos comprobadas de los 5 lugares, intercaladas por lugar para que la tira no repita el mismo sitio."""
    c = json.loads((FOTOS / "creditos.json").read_text(encoding="utf-8"))
    sur = [f for f in c if f["lugar"] not in NORTE]
    sur.sort(key=lambda f: (f["orden"], f["lugar"]))
    return [{k: f[k] for k in ("archivo", "muestra", "lugar", "autor", "licencia", "url_licencia", "url_original")}
            for f in sur]


def _negocios(d: pd.DataFrame, filtro) -> list[dict]:
    x = d[filtro(d)]
    return [{"n": nombre_bonito(f.nom_estab), "loc": nombre_bonito(f.localidad), "maps": enlace_maps(f.latitud, f.longitud),
             "resenas": enlace_maps(texto=f"{nombre_bonito(f.nom_estab)}, {nombre_bonito(f.localidad)}, Quintana Roo")}
            for f in x.itertuples()]


def experiencias(vacios_de_cada_10: int | None = None, hospedajes: dict | None = None) -> list[dict]:
    """hospedajes = tamaño de los hospedajes del DENUE en los municipios de los 5 lugares (datos_pagina.hospedaje)."""
    d = pd.read_parquet(GOLD / "lugares_clasificados.parquet")
    d = d[d.clasificado & ~d.lugar.isin(list(NORTE))]
    i = pd.read_parquet(SILVER / "inah", columns=["nombre", "periodo", "visitantes", "estado"])
    i = i[i.estado == "Quintana Roo"]
    anio = pd.to_datetime(i.periodo).dt.year
    ultimo = int(anio[anio.groupby(anio).transform("size") > 0].max())
    completo = ultimo if (pd.to_datetime(i.periodo).dt.month[anio == ultimo].max() == 12) else ultimo - 1
    ruta = int(i[i.nombre.isin(ZONAS_RUTA) & (anio == completo)].visitantes.sum())
    oxt = int(i[(i.nombre == "Z.A. de Oxtankah") & (anio == completo)].visitantes.sum())
    cen = centros()
    km = lambda a, b: round(km_haversine(*cen[a], *cen[b]))  # noqa: E731
    mariscos = d[(d.lugar == "Bahía Calderitas–Oxtankah") & (d.tipo == "Mariscos y pescado")]
    museos = lambda x: x.tipo.eq("Museo") & x.lugar.isin(["Chetumal", "Maya Ka'an + Kantemó"])  # noqa: E731
    comunidad = lambda x: x.nom_estab.astype(str).str.contains("XYAAT|GUERRA DE CASTAS|SANTA CRUZ BALAM", regex=True)  # noqa: E731
    return [
        {"clave": "piramides", "titulo": "Pirámides en la selva", "lugar": "Ruta arqueológica del sur",
         "texto": "Kohunlich, Dzibanché e Ichkabal: ciudades mayas entre la selva, con sus mascarones y templos.",
         "dato": f"Unas {round(ruta / 365):,} personas al día entre las tres zonas en {completo}: tienes la pirámide casi para ti.",
         "fuente": "INAH", "foto": "fotos/lugares/ruta_arqueologica_del_sur_1.jpg",
         "negocios": [{"n": z, "loc": "Zona arqueológica (INAH)", "maps": enlace_maps(texto=f"{z}, Quintana Roo"),
                       "resenas": enlace_maps(texto=f"{z}, Quintana Roo")}
                      for z in ["Zona Arqueológica de Kohunlich", "Zona Arqueológica de Dzibanché",
                                "Zona Arqueológica de Ichkabal"]]},
        {"clave": "mariscos", "titulo": "Mariscos frente a la bahía", "lugar": "Bahía Calderitas–Oxtankah",
         "texto": f"En Calderitas, a {km('Chetumal', 'Bahía Calderitas–Oxtankah')} km de Chetumal, se come viendo el agua; "
                  "al lado está Oxtankah, la ciudad maya de la bahía.",
         "dato": f"{len(mariscos)} marisquerías en Calderitas y {oxt:,} visitantes a Oxtankah en {completo}.",
         "fuente": "INEGI (DENUE) e INAH", "foto": "fotos/lugares/bahia_calderitasoxtankah_3.jpg",
         "negocios": _negocios(mariscos.head(4), lambda x: x.index == x.index)},
        {"clave": "laguna", "titulo": "Una laguna dulce y un cenote", "lugar": "Laguna Milagros–Xul-Ha",
         "texto": f"La Laguna Milagros y el cenote de Xul-Ha, a {km('Chetumal', 'Laguna Milagros–Xul-Ha')} km de Chetumal. "
                  "Es frágil: se nada sin bloqueador y sin dejar nada.",
         "dato": "No hay estadística oficial de visitantes: por eso se cuida con un límite estricto de gente.",
         "fuente": "Selección de regiones del proyecto", "foto": "fotos/lugares/laguna_milagrosxul_ha_1.jpg",
         "negocios": [{"n": "Laguna Milagros", "loc": "Huay-Pix", "maps": enlace_maps(texto="Laguna Milagros, Quintana Roo"),
                       "resenas": enlace_maps(texto="Laguna Milagros, Huay-Pix, Quintana Roo")},
                      {"n": "Cenote de Xul-Ha", "loc": "Xul-Ha", "maps": enlace_maps(texto="Cenote Xul-Ha, Quintana Roo"),
                       "resenas": enlace_maps(texto="Cenote Xul-Ha, Quintana Roo")}]},
        {"clave": "museos", "titulo": "Museos de la cultura maya", "lugar": "Chetumal",
         "texto": "Del Museo de la Cultura Maya en Chetumal al de la Guerra de Castas en Tihosuco: la historia del sur "
                  "contada desde aquí.",
         "dato": f"{int(museos(d).sum())} museos en Chetumal y Maya Ka'an según el directorio del INEGI.",
         "fuente": "INEGI (DENUE)", "foto": "fotos/lugares/chetumal_2.jpg",
         # Primero los museos de historia maya; después los demás
         "negocios": sorted(_negocios(d, lambda x: museos(x) & x.nom_estab.astype(str).str.contains("MUSEO|PLANETARIO")),
                            key=lambda n: (not any(k in n["n"] for k in ("Cultura Maya", "Guerra de Castas", "Balam")),
                                           n["n"]))[:4]},
        {"clave": "comunidad", "titulo": "Turismo comunitario maya", "lugar": "Maya Ka'an + Kantemó",
         "texto": "En Felipe Carrillo Puerto, Señor y Tihosuco las comunidades mayas reciben a quien llega: selva, "
                  "historia y su forma de vivir.",
         "dato": (f"Hospedaje de la gente de aquí: en los municipios de los cinco lugares hay {hospedajes['chicos']:,} "
                  f"hospedajes chicos, {hospedajes['medianos']:,} medianos y {hospedajes['grandes']:,} grandes."
                  if hospedajes else "Hospedajes chicos, de la gente de aquí."),
         "fuente": "INEGI (DENUE)", "foto": "fotos/lugares/maya_ka_an_kantemo_2.jpg",
         "negocios": _negocios(d, comunidad)},
        {"clave": "atardecer", "titulo": "Atardecer en el malecón", "lugar": "Chetumal",
         "texto": "El Boulevard Bahía de Chetumal: casas de madera, monumentos y el sol bajando sobre el agua.",
         "dato": (f"Hay lugar: {vacios_de_cada_10} de cada 10 cuartos de hotel de Chetumal se quedaron vacíos en 2024."
                  if vacios_de_cada_10 is not None else "Hay lugar: Chetumal tiene cuartos de hotel libres."),
         "fuente": "Gobierno de Quintana Roo (SITUR-Q)", "foto": "fotos/lugares/chetumal_1.jpg",
         "negocios": [{"n": "Boulevard Bahía", "loc": "Chetumal", "maps": enlace_maps(texto="Boulevard Bahía, Chetumal"),
                       "resenas": enlace_maps(texto="Boulevard Bahía, Chetumal, Quintana Roo")}]},
    ]


def _loc(mun: str, loc: str) -> tuple[float, float]:
    censo = pd.read_parquet(SILVER / "iter")
    f = censo[(censo.cve_mun.astype(str).str.zfill(3) == mun) & (censo.cve_loc.astype(str).str.zfill(4) == loc)]
    return float(f.latitud.iloc[0]), float(f.longitud.iloc[0])


def _mejor_mes(lugares: list[str], punto: str) -> dict:
    """Mes del año para la ruta: ningún lugar con dato en temporada alta, sin temporada de tormentas (< 9 %) y con
    lluvia menor que la mediana; entre esos, el de menos gente (índice promedio más bajo). Sin lugares con dato, solo
    clima: el mes más seco sin tormentas."""
    from torre.pronostico.calendario import ALTA_INDICE, TORMENTA_TEMPORADA, clima_normal

    forma = pd.read_parquet(GOLD / "pronostico_forma_anio.parquet")
    tormenta = pd.read_parquet(GOLD / "pronostico_poisson_tormentas.parquet").set_index("mes").prob_tormenta
    lluvia = clima_normal().set_index(["punto", "mes"]).lluvia_mm.loc[punto]
    ok = [m for m in range(1, 13) if tormenta[m] < TORMENTA_TEMPORADA and lluvia[m] < lluvia.median()]
    con_dato = forma[forma.lugar.isin(lugares)]
    if len(con_dato):
        idx = con_dato.groupby("mes").indice.agg(["max", "mean"])
        ok = [m for m in ok if idx.loc[m, "max"] < ALTA_INDICE]
        m = min(ok, key=lambda m: idx.loc[m, "mean"])
        return {"mes": int(m), "por_que": "menos gente, poca lluvia y sin temporada de tormentas"}
    m = min(ok, key=lambda m: lluvia[m])
    return {"mes": int(m), "por_que": "el mes más seco y sin tormentas (no hay estadística de visitantes)"}


def rutas() -> list[dict]:
    cen = centros()
    def tramos(puntos):  # noqa: E306
        return [round(km_haversine(*a, *b)) for a, b in zip(puntos, puntos[1:])]
    r1 = ["Chetumal", "Bahía Calderitas–Oxtankah", "Ruta arqueológica del sur"]
    r2 = ["Chetumal", "Laguna Milagros–Xul-Ha", "Ruta arqueológica del sur"]
    maya = [("002", "0001", "Felipe Carrillo Puerto"), ("002", "0239", "Señor"), ("002", "0250", "Tihosuco"),
            ("006", "0076", "Kantemó")]
    assert all(m in REGION_LOCALIDADES["Maya Ka'an + Kantemó"] for m in maya)
    pm = [_loc(m, l) for m, l, _ in maya]
    return [
        {"titulo": "Bahía y pirámides", "dias": 2, "planeador": "Ruta arqueológica del sur", "foto": "fotos/lugares/bahia_calderitasoxtankah_1.jpg",
         "paradas": ["Chetumal: el malecón y el Museo de la Cultura Maya", "Calderitas: mariscos y la zona de Oxtankah",
                     "Kohunlich y Dzibanché, en la selva"],
         "km": tramos([cen[x] for x in r1]), **_mejor_mes(r1, "chetumal")},
        {"titulo": "Laguna y selva", "dias": 3, "planeador": "Ruta arqueológica del sur", "foto": "fotos/lugares/laguna_milagrosxul_ha_2.jpg",
         "paradas": ["Chetumal: la bahía al atardecer", "Laguna Milagros y el cenote de Xul-Ha",
                     "Kohunlich, Dzibanché e Ichkabal"],
         "km": tramos([cen[x] for x in r2]), **_mejor_mes(r2, "chetumal")},
        {"titulo": "Pueblos de Maya Ka'an", "dias": 2, "planeador": None, "foto": "fotos/lugares/maya_ka_an_kantemo_1.jpg",  # sin serie: no está en el planeador
         "paradas": ["Felipe Carrillo Puerto (estación del Tren Maya)", "Señor: ecoturismo comunitario",
                     "Tihosuco: el Museo de la Guerra de Castas", "Kantemó: la cueva"],
         "km": tramos(pm), **_mejor_mes(["Maya Ka'an + Kantemó"], "felipe_carrillo_puerto")},
    ]


def vitrina(vacios_de_cada_10: int | None = None, hospedajes: dict | None = None) -> dict:
    return {"postales": postales(), "experiencias": experiencias(vacios_de_cada_10, hospedajes), "rutas": rutas(),
            "nota": "Distancias en línea recta entre los centros de cada lugar (no hay datos abiertos de distancias por "
                    "carretera). Sin precios: ninguna fuente oficial los publica. Las reseñas se leen en Google Maps."}


if __name__ == "__main__":
    v = vitrina(6)
    print(len(v["postales"]), "postales")
    for e in v["experiencias"]:
        print(e["titulo"], "|", e["dato"], "|", [n["n"] for n in e["negocios"]])
    for r in v["rutas"]:
        print(r["titulo"], r["dias"], r["km"], r["mes"], r["por_que"])
