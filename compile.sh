#!/usr/bin/env bash
# Compile un document LaTeX avec XeLaTeX.
# Si le document contient le commutateur \ifdefined\ELEVE, produit aussi la version élève :
#   fichier.pdf        → version prof (trous remplis)
#   fichier_ELEVE.pdf  → version élève (trous vides)
# Les fichiers auxiliaires vont dans le sous-dossier .build/ du document.
# Usage : ./compile.sh chemin/vers/fichier.tex
set -e
cd "$(dirname "$1")"
f="$(basename "$1" .tex)"
opts=(-xelatex -synctex=1 -interaction=nonstopmode -file-line-error -auxdir=.build)

latexmk "${opts[@]}" "$f.tex"
if grep -q '^\\ifdefined\\ELEVE' "$f.tex"; then
  latexmk "${opts[@]}" -jobname="${f}_ELEVE" -usepretex='\def\ELEVE{}' "$f.tex"
fi
