# Autor: Brandon Uriel García Sánchez
# Módulo: Campaña
# Qué hace:          Arma los diccionarios de la página en 10 idiomas (frontend/idiomas/<código>.js) a partir de las
#                    traducciones fuente en docs/idiomas/<código>.tsv, y COMPRUEBA que cada traducción conserve sus
#                    marcas: cifras {n0}, meses {m0}, lugares {p0}, nombres propios {x0} y etiquetas <b>, <em>, <small>.
# Por qué así:       - Brandon (02-oct-2026) pidió la página en 10 idiomas y eligió "Mercados que llegan" (decisión 16).
#                    - Las frases salen de la página misma (frontend/idiomas.js → Idiomas.claves()) y se guardan en
#                      docs/idiomas/claves.json. Muchas siguen un patrón (pie de foto + crédito, "tipo de negocio ·
#                      distancia"): esas se arman con la traducción de la parte base y las reglas del idioma, en vez de
#                      traducir cada combinación a mano.
#                    - Si una traducción pierde o inventa una marca, el programa se detiene: una cifra no puede
#                      desaparecer ni cambiar al traducir (regla de oro 1).
#                    - El maya yucateco (yua) se deja como plantilla vacía hasta que lo traduzca y revise una persona que
#                      lo hable; mientras, no aparece en el menú.
# Datos de entrada:  docs/idiomas/claves.json y docs/idiomas/<código>.tsv.
# Alimenta a:        La campaña para visitantes extranjeros (la página en su idioma).

import json
import re
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
FUENTE = RAIZ / "docs" / "idiomas"
SALIDA = RAIZ / "frontend" / "idiomas"
IDIOMAS = ["en", "fr", "de", "it", "pt", "zh", "ja", "ko"]
MARCA = re.compile(r"\{[nmpx]\d+\}|</?[a-z]+>")
FOTO_SMALL = re.compile(r"^(.*)<small>Foto: \{x0\}, \{x1\}</small>$")
FOTO_LARGO = re.compile(r"^(.*)\. Foto: \{x0\}, \{x1\}, vía Wikimedia Commons\.$")
CON_LUGAR = re.compile(r"^(.*), \{p0\}$")
TIPO = re.compile(r"^(.+) · (en el centro|a \{n0\} km del centro|en \{p0\}, a \{n0\} km|en Calderitas, a \{n0\} km"
                  r"|en Xul-ha, a \{n0\} km)$")


def leer_tsv(lang: str) -> dict:
    """Secciones #lugares, #tipos, #sufijos, #foto y #frases (id ⇥ traducción)."""
    sec, d = None, {"lugares": {}, "tipos": {}, "sufijos": {}, "foto": {}, "frases": {}}
    for linea in (FUENTE / f"{lang}.tsv").read_text(encoding="utf-8").splitlines():
        if not linea.strip():
            continue
        if linea.startswith("#"):
            sec = linea[1:].strip()
            continue
        a, b = linea.split("\t", 1)
        d[sec][a.strip()] = b.strip()
    return d


def marcas(s: str) -> Counter:
    return Counter(MARCA.findall(s))


def armar(lang: str, claves: list[str]) -> tuple[dict, list[str]]:
    t = leer_tsv(lang)
    directas = {claves[int(i)]: v for i, v in t["frases"].items()}

    def una(k: str) -> str | None:
        if k in directas:
            return directas[k]
        if m := FOTO_SMALL.match(k):
            b = una(m.group(1))
            return None if b is None else f"{b}<small>{t['foto']['Foto']}: {{x0}}, {{x1}}</small>"
        if m := FOTO_LARGO.match(k):
            b = una(m.group(1))
            return None if b is None else f"{b}. {t['foto']['Foto']}: {{x0}}, {{x1}}, {t['foto']['vía']} Wikimedia Commons."
        if (m := TIPO.match(k)) and m.group(1) in t["tipos"]:
            return f"{t['tipos'][m.group(1)]} · {t['sufijos'][m.group(2)]}"
        if (m := CON_LUGAR.match(k)) and (b := una(m.group(1))) is not None:
            return f"{b}, {{p0}}"
        return None

    frases, faltan = {}, []
    for k in claves:
        v = una(k)
        if v is None:
            faltan.append(k)
            continue
        if marcas(v) != marcas(k):
            raise ValueError(f"[{lang}] las marcas no coinciden:\n  es: {k}\n  {lang}: {v}")
        frases[k] = v
    return {"frases": frases, "lugares": t["lugares"]}, faltan


def guardar(lang: str, d: dict):
    SALIDA.mkdir(parents=True, exist_ok=True)
    js = (f"/* Traducción al idioma «{lang}» de la parte del viajero. Generado por backend/torre/campana/idiomas.py desde "
          f"docs/idiomas/{lang}.tsv: no editar a mano. */\n"
          f"window.IDIOMAS_TRAD = window.IDIOMAS_TRAD || {{}};\nwindow.IDIOMAS_TRAD[{json.dumps(lang)}] = "
          f"{json.dumps(d, ensure_ascii=False, indent=0)};\n")
    (SALIDA / f"{lang}.js").write_text(js, encoding="utf-8")


def plantilla_maya(claves: list[str]):
    """Plantilla para quien traduzca al maya yucateco: la frase en español y un espacio vacío."""
    f = FUENTE / "yua.tsv"
    if not f.exists():
        f.write_text("#frases\n" + "\n".join(f"{i}\t" for i in range(len(claves))) + "\n", encoding="utf-8")


def correr() -> dict:
    claves = json.loads((FUENTE / "claves.json").read_text(encoding="utf-8"))
    resumen = {}
    for lang in IDIOMAS:
        if not (FUENTE / f"{lang}.tsv").exists():
            resumen[lang] = "sin archivo"
            continue
        d, faltan = armar(lang, claves)
        guardar(lang, d)
        resumen[lang] = {"traducidas": len(d["frases"]), "faltan": faltan}
    plantilla_maya(claves)
    return resumen


if __name__ == "__main__":
    for lang, r in correr().items():
        if isinstance(r, str):
            print(lang, r)
            continue
        print(f"{lang}: {r['traducidas']} frases, faltan {len(r['faltan'])}")
        for k in r["faltan"][:400]:
            print("   falta:", k)
