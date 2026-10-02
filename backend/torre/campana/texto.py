# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña (minería de texto, Fase 8)
# Qué hace:          Minería de las 85,987 reseñas de Quintana Roo de Rest-Mex 2025 (Tulum, Isla Mujeres y Bacalar):
#                    1. Temas por aspecto con un léxico transparente (multitudes, precio, limpieza, ruido, calma,
#                       naturaleza, cultura, comida, servicio): cuántas reseñas tocan cada tema y qué tan seguido es una
#                       reseña MALA (1–2 estrellas) cuando lo toca (riesgo relativo).
#                    2. Reglas de asociación (Apriori, mlxtend): qué combinaciones de temas llevan a una reseña mala o a
#                       una de 5 estrellas (soporte, confianza y lift).
#                    3. El lenguaje real del turista: palabras que más distinguen a las reseñas de 5 estrellas de las de
#                       1–2 (log-odds con prior de Dirichlet informativo, Monroe et al. 2008). Con ellas se escriben los
#                       mensajes de la campaña.
# Por qué así:       - Léxico y no un modelo de temas (LDA/NMF): se puede leer, explicar y defender palabra por palabra, como
#                      el NLP de lugares.py. Un tema de LDA hay que adivinarlo; un tema del léxico se define.
#                    - Ninguna reseña es de los 5 lugares (Rest-Mex no los cubre, nota 18): el texto dice qué MOLESTA en
#                      los destinos llenos y qué valora el turista; eso sostiene la promesa del sur, no una opinión del sur.
#                    - Muchas reseñas son traducciones al español (se nota en el texto): se usan raíces cortas para tolerar
#                      variantes y se declara.
# Datos de entrada:  datos/silver/restmex (D5).
# Alimenta a:        Buyer persona, propuesta de valor y mensajes de la campaña (Fase 8).

import re
from collections import Counter

import numpy as np
import pandas as pd

from torre.base.entorno import RAIZ

SILVER = RAIZ / "datos" / "silver"
GOLD = RAIZ / "datos" / "gold"

# Raíces al inicio de palabra (\b). Cada tema se define aquí, a la vista.
ASPECTOS = {
    "multitudes": ["gente", "lleno", "llena", "multitud", "abarrot", "saturad", "concurrid", "masific", "aglomer",
                   "fila", "filas", "esperar", "espera ", "demasiados turistas", "muchos turistas"],
    "precio": ["caro", "cara", "caros", "caras", "costos", "precio", "cobr", "tarifa", "propina", "barat", "dinero"],
    "limpieza": ["sucio", "sucia", "sucied", "basura", "limpi", "sargazo", "olor", "apest", "mugr"],
    "ruido": ["ruido", "ruidos", "escándalo", "música alta", "fiesta"],
    "calma": ["tranquil", "paz", "relaj", "silencio", "calma", "sereno", "serena"],
    "naturaleza": ["naturalez", "selva", "laguna", "cenote", "manglar", "aves", "pájaro", "agua cristalina", "colores"],
    "cultura": ["ruina", "pirámide", "piramide", "maya", "historia", "arqueol", "cultura", "templo"],
    "comida": ["comida", "platillo", "delicios", "sabor", "mariscos", "tacos", "ceviche", "pescado"],
    "servicio": ["personal", "servicio", "atención", "amable", "mesero", "anfitri", "recepción"],
}
PALABRAS_VACIAS = set("""a al algo algunas algunos ante antes aquí así aun aunque bien cada casi como con contra cual cuales
cuando de del desde donde dos e el ella ellas ellos en entre era eran es esa esas ese eso esos esta estaba estaban estamos
estan están estar estas este esto estos estuvo fue fueron fuimos ha había habían han hasta hay hemos hizo hubo la las le les
lo los mas más me mi mis mucho muchos muy nada ni no nos nosotros o os otra otras otro otros para pero poco por porque que
qué quien se sea sean ser si sí sido sin sobre solo sólo son su sus también tan tanto te tenía tenían tiene tienen todo
todos tu tus tuvimos tuvo un una unas uno unos y ya él ese esa hace hacer puede pueden día días vez veces lugar lugares
cosa cosas así cuál dentro fuera luego entonces mientras ser estar haber tener ir ver dar decir mismo misma después aquí
allí allá ahí cómo dónde etc gran grande buen buena bueno buenos buenas mejor mal mala malo""".split())


def leer() -> pd.DataFrame:
    r = pd.read_parquet(SILVER / "restmex", filters=[("estado", "=", "Quintana Roo")],
                        columns=["titulo", "resena", "calificacion", "pueblo", "tipo"])
    r["texto"] = (r.titulo.fillna("") + ". " + r.resena.fillna("")).str.lower()
    return r


def marcar_aspectos(r: pd.DataFrame) -> pd.DataFrame:
    for a, raices in ASPECTOS.items():
        patron = r"\b(?:" + "|".join(re.escape(x.strip()) for x in raices) + ")"
        r[a] = r.texto.str.contains(patron, regex=True)
    r["mala"] = r.calificacion <= 2
    r["cinco"] = r.calificacion == 5
    return r


def aspectos(r: pd.DataFrame) -> pd.DataFrame:
    """Por pueblo y aspecto: % de reseñas que lo tocan, % malas entre ellas y riesgo relativo (vs. todas las del pueblo)."""
    filas = []
    for pueblo, g in list(r.groupby("pueblo")) + [("Quintana Roo (3 pueblos)", r)]:
        base = g.mala.mean()
        for a in ASPECTOS:
            t = g[g[a]]
            filas.append({"pueblo": pueblo, "aspecto": a, "resenas": len(t), "pct_menciona": 100 * len(t) / len(g),
                          "pct_malas": 100 * t.mala.mean() if len(t) else np.nan, "pct_malas_pueblo": 100 * base,
                          "riesgo_relativo": t.mala.mean() / base if len(t) and base else np.nan})
    return pd.DataFrame(filas)


def reglas_asociacion(r: pd.DataFrame, soporte: float = 0.001) -> pd.DataFrame:
    """Apriori sobre transacciones {temas mencionados} ∪ {reseña mala | reseña de 5}. Reglas que terminan en la
    calificación. lift = confianza / soporte(consecuente)."""
    from mlxtend.frequent_patterns import apriori, association_rules
    t = r[list(ASPECTOS)].copy()
    t["reseña mala (1–2)"] = r.mala
    t["reseña de 5"] = r.cinco
    frec = apriori(t.astype(bool), min_support=soporte, use_colnames=True, max_len=3)
    reg = association_rules(frec, metric="lift", min_threshold=1.0)
    fin = reg.consequents.apply(lambda c: len(c) == 1 and next(iter(c)) in {"reseña mala (1–2)", "reseña de 5"})
    ante = reg.antecedents.apply(lambda a: not (a & {"reseña mala (1–2)", "reseña de 5"}))
    reg = reg[fin & ante].copy()
    reg["si"] = reg.antecedents.apply(lambda a: " + ".join(sorted(a)))
    reg["entonces"] = reg.consequents.apply(lambda c: next(iter(c)))
    return reg[["si", "entonces", "support", "confidence", "lift"]].rename(
        columns={"support": "soporte", "confidence": "confianza"}).sort_values(["entonces", "lift"], ascending=[True, False])


def tokens(texto: str) -> list[str]:
    return [w for w in re.findall(r"[a-záéíóúñü]{3,}", texto) if w not in PALABRAS_VACIAS]


def palabras_que_distinguen(r: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Log-odds con prior de Dirichlet informativo (Monroe, Colaresi y Quinn, 2008):
    δ_w = ln[(y_w^A + α_w)/(n_A + α_0 − y_w^A − α_w)] − ln[(y_w^B + α_w)/(n_B + α_0 − y_w^B − α_w)],
    z_w = δ_w / √(1/(y_w^A+α_w) + 1/(y_w^B+α_w)), con α_w = 0.01·(conteo de w en todo el corpus) (prior informativo)."""
    a = Counter(w for t in r[r.cinco].texto for w in tokens(t))
    b = Counter(w for t in r[r.mala].texto for w in tokens(t))
    todo = a + b
    alfa = {w: 0.01 * c for w, c in todo.items()}
    a0 = sum(alfa.values())
    na, nb = sum(a.values()), sum(b.values())
    filas = []
    for w, c in todo.items():
        if c < 50:
            continue
        ya, yb, al = a[w], b[w], alfa[w]
        d = np.log((ya + al) / (na + a0 - ya - al)) - np.log((yb + al) / (nb + a0 - yb - al))
        z = d / np.sqrt(1 / (ya + al) + 1 / (yb + al))
        filas.append({"palabra": w, "en_cinco": ya, "en_malas": yb, "delta": d, "z": z})
    f = pd.DataFrame(filas)
    cinco = f.nlargest(n, "z").assign(lado="reseñas de 5 estrellas")
    malas = f.nsmallest(n, "z").assign(lado="reseñas de 1–2 estrellas")
    return pd.concat([cinco, malas], ignore_index=True)


def construir() -> dict:
    r = marcar_aspectos(leer())
    asp, reg, pal = aspectos(r), reglas_asociacion(r), palabras_que_distinguen(r)
    asp.to_parquet(GOLD / "campana_aspectos.parquet", index=False)
    reg.to_parquet(GOLD / "campana_reglas.parquet", index=False)
    pal.to_parquet(GOLD / "campana_palabras.parquet", index=False)
    print(f"Reseñas: {len(r):,} · malas (1–2): {r.mala.mean():.1%} · de 5: {r.cinco.mean():.1%}")
    q = asp[asp.pueblo == "Quintana Roo (3 pueblos)"].sort_values("riesgo_relativo", ascending=False)
    print(q[["aspecto", "pct_menciona", "pct_malas", "riesgo_relativo"]].round(2).to_string(index=False))
    print(asp.pivot(index="aspecto", columns="pueblo", values="riesgo_relativo").round(2).to_string())
    print(reg[reg.entonces.str.contains("mala")].head(12).round(4).to_string(index=False))
    print(reg[reg.entonces == "reseña de 5"].head(8).round(3).to_string(index=False))
    print(pal.groupby("lado").palabra.apply(lambda p: ", ".join(p)).to_string())
    return {"r": r, "aspectos": asp, "reglas": reg, "palabras": pal}


if __name__ == "__main__":
    construir()
