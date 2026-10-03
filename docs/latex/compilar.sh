#!/usr/bin/env bash
# Autor: Brandon Uriel García Sánchez
# Compila las guías LaTeX con XeLaTeX (MiKTeX). Uso, desde docs/latex/:  bash compilar.sh [archivo.tex ...]
# Por qué el PATH limpio: MiKTeX revisa cada carpeta del PATH y se detiene si una entrada apunta a un archivo
# (en esta computadora, C:\Users\Uriel\.local\bin\claude.exe). Solo se limpia para estos comandos.
set -e
cd "$(dirname "$0")"
B="$LOCALAPPDATA/Programs/MiKTeX/miktex/bin/x64"
[ -x "$B/xelatex.exe" ] || B="/c/Program Files/MiKTeX/miktex/bin/x64"
archivos=("$@")
[ ${#archivos[@]} -eq 0 ] && archivos=(1_guia_tecnica.tex 2_guia_sencilla.tex 3_decisiones.tex)
for f in "${archivos[@]}"; do
  for pasada in 1 2 3; do  # tres pasadas: índice, referencias cruzadas y números de página
    env PATH="$B:/c/Windows/System32:/c/Windows" "$B/xelatex.exe" -interaction=nonstopmode -halt-on-error \
      -output-directory=build "$f" > "build/${f%.tex}.salida.txt" 2>&1 || {
        echo "ERROR en $f (pasada $pasada); ver docs/latex/build/${f%.tex}.log"; exit 1; }
  done
  echo "OK  $f → build/${f%.tex}.pdf"
done
