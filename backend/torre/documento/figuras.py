# Autor: Brandon Uriel García Sánchez
# Módulo: Documento ejecutivo
# Qué hace:          Dibuja las gráficas del documento ejecutivo con el estilo de la UNRC (guinda #9F2241,
#                    dorado #BC955C, tipografía Noto Sans, nunca texto en negro) y las guarda en
#                    docs/ejecutivo/figuras/.
# Por qué así:       Los colores y la tipografía salen de la Guía de Identidad Gráfica UNRC 2024-2030 (págs. 9,
#                    17-19 y 26), resumida en docs/ejecutivo/GUIA_ESTILO_UNRC.md. Noto Sans vive en
#                    herramientas/fuentes/ para no tener que instalarla en Windows.
#                    Cada función lee un archivo oficial de datos/bronze/: la gráfica muestra exactamente lo que
#                    publicó la fuente.
# Datos de entrada:  DataTur BdINAH (D4) y SITUR-Q (D1) en datos/bronze/.
# Alimenta a:        Capítulos del documento ejecutivo (selección de regiones, Fase 1).

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # dibuja a archivo, sin abrir ventanas
import matplotlib.pyplot as plt
from matplotlib import font_manager

RAIZ = Path(__file__).resolve().parents[3]
FIGURAS = RAIZ / "docs" / "ejecutivo" / "figuras"
BRONZE = RAIZ / "datos" / "bronze"

GUINDA, DORADO, GRIS_TEXTO, GRIS_SUAVE = "#9F2241", "#BC955C", "#3A3A3A", "#BDBDBD"
PALETA = ["#9F2241", "#BC955C", "#565393", "#58A65D", "#8CAFDD", "#F26E50", "#465973"]


def estilo_unrc():
    """Aplica el estilo UNRC a todas las gráficas: Noto Sans, textos en gris oscuro, sin marco pesado."""
    for f in (RAIZ / "herramientas" / "fuentes").glob("NotoSans-*.ttf"):
        font_manager.fontManager.addfont(str(f))
    plt.rcParams.update({
        "font.family": "Noto Sans", "font.size": 10,
        "text.color": GRIS_TEXTO, "axes.labelcolor": GRIS_TEXTO,
        "xtick.color": GRIS_TEXTO, "ytick.color": GRIS_TEXTO,
        "axes.edgecolor": GRIS_SUAVE, "axes.spines.top": False, "axes.spines.right": False,
        "axes.titleweight": "bold", "axes.titlecolor": GUINDA, "axes.titlesize": 13,
        "figure.facecolor": "white", "savefig.dpi": 200, "savefig.bbox": "tight",
    })


def _ultimo(patron: str) -> Path:
    """Devuelve el archivo más reciente de Bronze que coincide con el patrón (la última descarga)."""
    rutas = sorted(BRONZE.glob(patron))
    if not rutas:
        raise FileNotFoundError(f"No hay archivo en Bronze para {patron}; primero corre la ingesta (Fase 1).")
    return rutas[-1]


def _pie(ax, texto: str):
    """Línea de fuente al pie de la gráfica, obligatoria en el documento ejecutivo."""
    ax.figure.text(0.01, -0.02, texto, fontsize=8, color=GRIS_TEXTO, ha="left", va="top")


def visitantes_inah_2025() -> Path:
    """Barras: visitantes 2025 por zona arqueológica de Q. Roo (INAH). Guinda = regiones que se promueven."""
    import pandas as pd

    zipf = _ultimo("datatur/*/inah/BdINAH.zip")
    df = pd.read_excel(zipf, sheet_name=0) if zipf.suffix == ".xlsx" else _leer_inah(zipf)
    q = df[(df["Estado"] == "Quintana Roo") & (df["Año"] == 2025) & df["Nombre"].str.startswith("Z.A")]
    tot = q.groupby("Nombre")["Visitantes"].sum().sort_values()
    tot = tot[tot > 0]
    promovidas = ("Kohunlich", "Dzibanch", "Ichkabal", "Oxtankah")  # zonas de las 5 regiones (28-sep-2026)
    colores = [GUINDA if any(p in n for p in promovidas) else DORADO for n in tot.index]

    estilo_unrc()
    fig, ax = plt.subplots(figsize=(8, 4.6))
    etiquetas = [n.replace("Z.A. de ", "").replace("Z.A de ", "") for n in tot.index]
    ax.barh(etiquetas, tot.values, color=colores)
    for i, v in enumerate(tot.values):
        ax.text(v, i, f" {v:,.0f}", va="center", fontsize=8, color=GRIS_TEXTO)
    ax.set_title("Tulum recibe más de 1 millón de visitantes; la ruta del sur, menos de 70 mil")
    ax.set_xlabel("Visitantes en 2025 (nacionales + extranjeros)")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f} M" if x >= 1e6 else f"{x/1e3:.0f} mil"))
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=GUINDA), plt.Rectangle((0, 0), 1, 1, color=DORADO)],
              labels=["Región que promueve la campaña", "Fuera del foco (referencia, crucero o retirada)"], frameon=False, loc="lower right")
    _pie(ax, f"Fuente: SECTUR-DataTur, base de visitantes del INAH (archivo {zipf.name}, descargado el {zipf.parts[-3]}).")
    salida = FIGURAS / "f01_visitantes_inah_2025.png"
    fig.savefig(salida); plt.close(fig)
    return salida


def _leer_inah(zipf: Path):
    """Lee el Excel que viene dentro de BdINAH.zip."""
    import io
    import zipfile

    import pandas as pd

    with zipfile.ZipFile(zipf) as z:
        nombre = next(n for n in z.namelist() if n.lower().endswith(".xlsx"))
        return pd.read_excel(io.BytesIO(z.read(nombre)))


def cobertura_ocupacion_siturq() -> Path:
    """Mapa de calor: cuántos meses con dato de ocupación hotelera tiene cada destino en cada año (SITUR-Q)."""
    import numpy as np

    archivo = _ultimo("siturq/*/ocupacion_hotelera.json")
    bloque = json.loads(archivo.read_text(encoding="utf-8"))
    unidades = list(dict.fromkeys(r["unidad"] for r in bloque))
    anios = sorted({r["anio"] for r in bloque})
    matriz = np.zeros((len(unidades), len(anios)))
    for r in bloque:
        filas = (r.get("respuesta") or {}).get("data") or []
        con_dato = [f for f in filas if float(f.get("Ocupación hotelera") or 0) > 0]
        matriz[unidades.index(r["unidad"]), anios.index(r["anio"])] = len(con_dato)

    estilo_unrc()
    fig, ax = plt.subplots(figsize=(8, 5.2))
    mapa = matplotlib.colors.LinearSegmentedColormap.from_list("unrc", ["#F4ECEE", GUINDA])
    ax.imshow(matriz, cmap=mapa, vmin=0, vmax=12, aspect="auto")
    ax.set_xticks(range(len(anios)), anios)
    ax.set_yticks(range(len(unidades)), unidades)
    for i in range(len(unidades)):
        for j in range(len(anios)):
            v = int(matriz[i, j])
            ax.text(j, i, v if v else "–", ha="center", va="center", fontsize=8,
                    color="white" if v > 6 else GRIS_TEXTO)
    ax.set_title("La ocupación hotelera oficial de SITUR-Q termina en diciembre de 2024")
    ax.set_xlabel("Año (número = meses con dato publicado)")
    for s in ax.spines.values():
        s.set_visible(False)
    _pie(ax, f"Fuente: SITUR-Q, indicador «Ocupación hotelera», consulta del {archivo.parts[-2]} (archivo {archivo.name}).")
    salida = FIGURAS / "f02_cobertura_ocupacion_siturq.png"
    fig.savefig(salida); plt.close(fig)
    return salida


def volumen_bronze() -> Path:
    """Barras: cuántos registros aportó cada fuente oficial a Bronze (escala logarítmica, del manifiesto)."""
    import pandas as pd

    m = pd.read_csv(BRONZE / "MANIFIESTO.csv")
    m = m[m.fuente != "Evidencia sargazo"]  # capturas de noticias: evidencia, no datos
    m["filas"] = pd.to_numeric(m["filas"], errors="coerce").fillna(0)
    r = m.groupby("fuente")["filas"].sum()
    r = r[r > 0].sort_values()
    etiquetas = [f.split(" ", 1)[1] for f in r.index]  # quita el código D1, D2...

    estilo_unrc()
    fig, ax = plt.subplots(figsize=(8, 5))
    colores = [GUINDA if v >= 100_000 else DORADO for v in r.values]
    ax.barh(etiquetas, r.values, color=colores)
    ax.set_xscale("log")
    for i, v in enumerate(r.values):
        ax.text(v, i, f" {v:,.0f}", va="center", fontsize=8, color=GRIS_TEXTO)
    ax.set_title(f"{m['filas'].sum():,.0f} registros oficiales reunidos de {len(r)} fuentes")
    ax.set_xlabel("Registros por fuente (escala logarítmica: cada marca multiplica por 10)")
    _pie(ax, f"Fuente: manifiesto de datos crudos del proyecto (datos/bronze/MANIFIESTO.csv), {len(m)} archivos, "
             f"{m['bytes'].sum() / 1e6:,.0f} MB.")
    salida = FIGURAS / "f03_volumen_bronze.png"
    fig.savefig(salida); plt.close(fig)
    return salida


def costos_publicitarios_travel() -> Path:
    """Barras: costo por clic (USD) y tasa de clics (%) de la categoría Travel por canal y editor (D13)."""
    import pandas as pd

    archivo = _ultimo("benchmarks/*/benchmarks_tablas.csv")
    d = pd.read_csv(archivo)
    t = d[(d.categoria == "Travel") & d.metrica.isin(["Average CPC", "Average CTR"])].copy()
    # Etiqueta en tres líneas (editor / canal / año) para que no se encimen en el eje
    canal = t["canal"].str.replace(" (Google/Microsoft)", "", regex=False).str.replace(" Ads", "", regex=False)
    t["serie"] = t["editor"] + "\n" + canal + "\n" + t["anio"].astype(str)
    cpc = t[t.metrica == "Average CPC"].set_index("serie")["valor"]
    ctr = t[t.metrica == "Average CTR"].set_index("serie")["valor"].reindex(cpc.index)

    estilo_unrc()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.2))
    a1.bar(cpc.index, cpc.values, color=[GUINDA if "Facebook" not in s else DORADO for s in cpc.index])
    a1.set_title("Costo por clic (USD)", fontsize=11)
    a2.bar(ctr.index, ctr.values, color=[GUINDA if "Facebook" not in s else DORADO for s in ctr.index])
    a2.set_title("Personas que dan clic de cada 100 (CTR, %)", fontsize=11)
    for ax, serie, fmt in ((a1, cpc, "${:.2f}"), (a2, ctr, "{:.2f} %")):
        ax.tick_params(axis="x", labelsize=7)
        for i, v in enumerate(serie.values):
            ax.text(i, v, fmt.format(v), ha="center", va="bottom", fontsize=8, color=GRIS_TEXTO)
    fig.suptitle("Un clic en Facebook cuesta 4 a 5 veces menos que en buscadores (turismo)",
                 color=GUINDA, fontweight="bold", fontsize=13)
    _pie(a1, f"Fuente: WordStream 2025 y LocaliQ 2026, categoría «Travel» (promedios de anunciantes de EE. UU.), "
             f"extraído el {archivo.parts[-2]}.")
    salida = FIGURAS / "f04_costos_publicitarios_travel.png"
    fig.savefig(salida); plt.close(fig)
    return salida


def ocupacion_semanal_qroo() -> Path:
    """Líneas: ocupación hotelera semanal 2022–2026 de los centros de Q. Roo (DataTur, ya limpia en Silver).

    Se muestra el promedio móvil de 4 semanas para que se lea la tendencia y no el ruido semana a semana.
    """
    import pandas as pd

    d = pd.read_parquet(RAIZ / "datos" / "silver" / "datatur_ocupacion")
    s = d[(d.frecuencia == "semanal") & d.es_qroo & (d.tipo_fila == "centro")].copy()
    s["periodo"] = pd.to_datetime(s["periodo"])
    series = {"Cancun": ("Cancún", GUINDA), "Riviera Maya": ("Riviera Maya", DORADO),
              "Cozumel": ("Cozumel", PALETA[2]), "Isla Mujeres": ("Isla Mujeres", PALETA[3])}

    estilo_unrc()
    fig, ax = plt.subplots(figsize=(9, 4.4))
    for centro, (etiqueta, color) in series.items():
        c = s[s.centro == centro].sort_values("periodo").set_index("periodo")["ocupacion_pct"]
        ax.plot(c.rolling(4, min_periods=1).mean(), color=color, lw=1.8, label=etiqueta)
    ax.axvline(pd.Timestamp("2025-09-01"), color=GRIS_SUAVE, ls="--", lw=1)
    ax.text(pd.Timestamp("2025-09-08"), 97, "Sep-2025: DataTur actualiza\nla oferta de Isla Mujeres", fontsize=7.5,
            color=GRIS_TEXTO, va="top")
    ax.set_ylim(10, 100)
    ax.set_ylabel("Ocupación hotelera (%)")
    ax.set_title("Cancún y Riviera Maya rondan el 74 %; Cozumel e Isla Mujeres, el 52 %")
    ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    _pie(ax, "Fuente: SECTUR-DataTur, monitoreo semanal de ocupación hotelera 2022–2026 (promedio móvil de 4 semanas), "
             "datos limpios del proyecto.")
    fig.subplots_adjust(bottom=0.2)
    salida = FIGURAS / "f05_ocupacion_semanal_qroo.png"
    fig.savefig(salida); plt.close(fig)
    return salida


def oferta_turistica_municipios() -> Path:
    """Barras apiladas: negocios turísticos por municipio de Q. Roo y por giro (DENUE, ya limpio en Silver)."""
    import pandas as pd

    d = pd.read_parquet(RAIZ / "datos" / "silver" / "denue", columns=["cve_ent", "municipio", "categoria_turistica", "es_turistico"])
    q = d[(d.cve_ent.astype(str) == "23") & d.es_turistico]
    tabla = q.pivot_table(index="municipio", columns="categoria_turistica", aggfunc="size", fill_value=0)
    tabla = tabla.loc[tabla.sum(axis=1).sort_values().index]
    orden = ["Alimentos y bebidas", "Alojamiento", "Esparcimiento", "Agencias de viajes", "Museos y sitios históricos", "Transporte turístico"]
    tabla = tabla[[c for c in orden if c in tabla.columns]]

    estilo_unrc()
    fig, ax = plt.subplots(figsize=(9, 4.8))
    izquierda = None
    for i, col in enumerate(tabla.columns):
        ax.barh(tabla.index, tabla[col], left=izquierda, color=PALETA[i % len(PALETA)], label=col)
        izquierda = tabla[col] if izquierda is None else izquierda + tabla[col]
    for i, total in enumerate(tabla.sum(axis=1)):
        ax.text(total, i, f" {total:,}", va="center", fontsize=8, color=GRIS_TEXTO)
    ax.set_xlabel("Negocios turísticos registrados")
    ax.set_title(f"{len(q):,} negocios turísticos en Quintana Roo; 4 de cada 10 están en Benito Juárez (Cancún)")
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper center", bbox_to_anchor=(0.45, -0.14))
    _pie(ax, "Fuente: INEGI, Directorio Estadístico Nacional de Unidades Económicas (DENUE), giros característicos del "
             "turismo (SCIAN 721, 722, 5615, 487, 712, 713); datos limpios del proyecto.")
    fig.subplots_adjust(bottom=0.25)
    salida = FIGURAS / "f06_oferta_turistica_municipios.png"
    fig.savefig(salida); plt.close(fig)
    return salida


if __name__ == "__main__":
    FIGURAS.mkdir(parents=True, exist_ok=True)
    for f in (visitantes_inah_2025, cobertura_ocupacion_siturq, volumen_bronze, costos_publicitarios_travel,
              ocupacion_semanal_qroo, oferta_turistica_municipios):
        print("✓", f().relative_to(RAIZ))
