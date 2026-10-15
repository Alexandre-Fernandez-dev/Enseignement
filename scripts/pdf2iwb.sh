#!/usr/bin/env bash
# usage : pdf2iwb.sh fichier.pdf  -> produit fichier.iwb à côté
set -euo pipefail
pdf=$(realpath "$1")
out="${pdf%.*}.iwb"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
mkdir "$tmp/images"

pdftoppm -png -scale-to-y 4320 -scale-to-x -1 "$pdf" "$tmp/images/p"

first=$(ls "$tmp"/images/*.png | head -n1)
read W H < <(identify -format '%w %h\n' "$first")

{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<iwb xmlns="http://www.imsglobal.org/xsd/iwb_v1p0" xmlns:svg="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0">'
  echo "<svg:svg version=\"1.2\" baseProfile=\"tiny\" width=\"$W\" height=\"$H\" viewBox=\"0 0 $W $H\">"
  echo '<svg:pageSet>'
  i=1
  for img in "$tmp"/images/*.png; do
    read w h < <(identify -format '%w %h\n' "$img")
    echo "<svg:page id=\"page$i\"><svg:image x=\"0\" y=\"0\" width=\"$w\" height=\"$h\" xlink:href=\"images/$(basename "$img")\"/></svg:page>"
    i=$((i+1))
  done
  echo '</svg:pageSet></svg:svg></iwb>'
} > "$tmp/content.xml"

rm -f "$out"
(cd "$tmp" && zip -qr "$out" content.xml images)
echo "OK : $out"
