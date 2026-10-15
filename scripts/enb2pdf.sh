#!/usr/bin/env bash
# Transforme les annotations d'un .enb (créé par le tableau NovoTouch quand on
# édite un .iwb) en PDF annoté : les traits sont redessinés en vectoriel
# par-dessus le PDF d'origine, qui reste intact.
# Usage : enb2pdf.sh fichier.enb [fichier.pdf]
#   PDF par défaut : fichier.pdf à côté du .enb. Produit fichier_Annote.pdf.
# Les diapositives ajoutées au tableau (sans page du PDF) deviennent des pages
# supplémentaires, insérées après la page qui les précède.
# Dépendances : python-cairo, qpdf, poppler (pdfinfo).
set -euo pipefail
[[ $# -ge 1 ]] || { echo "Usage : $0 fichier.enb [fichier.pdf]" >&2; exit 1; }
enb=$(realpath "$1")
pdf=$(realpath "${2:-${enb%.*}.pdf}")
out="${pdf%.*}_Annote.pdf"
[[ -f "$enb" ]] || { echo "Introuvable : $enb" >&2; exit 1; }
[[ -f "$pdf" ]] || { echo "PDF d'origine introuvable : $pdf" >&2; exit 1; }
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT

# Tailles des pages du PDF, en points : "largeur hauteur" par ligne.
pdfinfo -f 1 -l 100000 "$pdf" | awk '/^Page +[0-9]+ size:/ {print $4, $6}' > "$tmp/sizes"

# Python dessine overlay.pdf (une page par page du PDF, puis les pages ajoutées)
# et écrit dans order.txt l'ordre final des pages : "o N" (page N du PDF
# annotée) ou "x N" (page N de overlay.pdf, diapositive ajoutée).
python3 -I - "$enb" "$tmp/sizes" "$tmp/overlay.pdf" "$tmp/order.txt" <<'EOF'
import re, sys, zipfile, cairo
import xml.etree.ElementTree as ET

enb, sizes_file, overlay, order_file = sys.argv[1:]
sizes = [tuple(map(float, l.split())) for l in open(sizes_file) if l.strip()]
n_pages = len(sizes)
EXTRA_W = 842.0                      # largeur (pt) d'une page ajoutée (A4 paysage)

z = zipfile.ZipFile(enb)
slides = {}
for name in z.namelist():
    m = re.fullmatch(r'/?Slides/Slide_(\d+)\.xml', name)
    if m:
        slides[int(m.group(1))] = ET.fromstring(z.read(name))

def matrix(s):                       # Transform WPF : M11,M12,M21,M22,OffsetX,OffsetY
    a, b, c, d, e, f = map(float, s.split(','))
    return cairo.Matrix(a, b, c, d, e, f)

def color(s):                        # #AARRGGBB
    s = s.lstrip('#')
    if len(s) == 6: s = 'FF' + s
    a, r, g, b = (int(s[i:i+2], 16) / 255 for i in (0, 2, 4, 6))
    return r, g, b, a

def strokes(slide):
    for p in slide.iter('Package'):
        if p.get('Type') != 'Ink':
            continue
        d = p.find('Data')
        pts = [tuple(map(float, q.split(',')[:2]))
               for q in d.findtext('Points', '').split(';') if q.strip()]
        r, g, b, a = color(d.findtext('ForegroundColor', '#FF000000'))
        if 'Highlight' in d.findtext('InkType', ''):
            a = min(a, 0.4)
        yield pts, float(d.findtext('Thickness', '3')), (r, g, b, a)

def draw(ctx, slide):
    n = 0
    for pts, width, rgba in strokes(slide):
        if not pts:
            continue
        ctx.set_source_rgba(*rgba)
        ctx.set_line_width(width)
        ctx.move_to(*pts[0])
        if len(pts) == 1:
            ctx.line_to(*pts[0])     # simple point : trait de longueur nulle
        for x, y in pts[1:]:
            ctx.line_to(x, y)
        ctx.stroke()
        n += 1
    return n

page_slide = {}                      # page du PDF -> diapositive
extras = {}                          # page du PDF qui précède -> [diapositives ajoutées]
last, ignored = 0, set()
for i in sorted(slides):
    s = slides[i]
    pic = None
    for p in s.iter('Package'):
        t = p.get('Type')
        if t == 'Picture' and pic is None:
            m = re.fullmatch(r'p-0*(\d+)\.png', p.find('Data').findtext('Res_SourcePath', ''))
            if m:
                pic = (int(m.group(1)), p.find('Data'))
        elif t not in ('Slide', 'Ink', 'Picture'):
            ignored.add(t)
    if pic and 1 <= pic[0] <= n_pages:
        page_slide[pic[0]] = (s, pic[1])
        last = pic[0]
    elif any(True for _ in strokes(s)):
        extras.setdefault(last, []).append(s)
if ignored:
    print("Éléments non pris en charge, ignorés :", ", ".join(sorted(ignored)), file=sys.stderr)

surf = cairo.PDFSurface(overlay, *sizes[0])
ctx = cairo.Context(surf)
total = 0
for n, (w, h) in enumerate(sizes, 1):
    surf.set_size(w, h)
    if n in page_slide:
        s, d = page_slide[n]
        # Diapositive -> pixels de l'image de la page (inverse de Transform) -> points PDF.
        m = matrix(d.findtext('Transform', '1,0,0,1,0,0'))
        m.invert()
        bw = float(d.findtext('BitmapWidth'))
        bh = float(d.findtext('BitmapHeight'))
        ctx.save()
        ctx.scale(w / bw, h / bh)
        ctx.transform(m)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        total += draw(ctx, s)
        ctx.restore()
    ctx.show_page()
order = []
k = n_pages
for n in range(0, n_pages + 1):
    if n >= 1:
        order.append(f"o {n}")
    for s in extras.get(n, []):
        d = s.find('Data')
        sw, sh = float(d.findtext('Width', '3840')), float(d.findtext('Height', '2160'))
        surf.set_size(EXTRA_W, EXTRA_W * sh / sw)
        ctx.save()
        ctx.set_source_rgb(1, 1, 1); ctx.paint()
        ctx.scale(EXTRA_W / sw, EXTRA_W / sw)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        total += draw(ctx, s)
        ctx.restore()
        ctx.show_page()
        k += 1
        order.append(f"x {k}")
surf.finish()
open(order_file, 'w').write("\n".join(order) + "\n")
print(f"Traits : {total} · pages annotées : {len(page_slide)} sur {n_pages} · "
      f"pages ajoutées : {k - n_pages}", file=sys.stderr)
EOF

# Superposition des traits, puis assemblage dans l'ordre final.
qpdf "$pdf" --overlay "$tmp/overlay.pdf" --from=1-"$(wc -l < "$tmp/sizes")" -- "$tmp/annote.pdf"
args=()
while read -r src n; do
  if [[ $src == o ]]; then args+=("$tmp/annote.pdf" "$n"); else args+=("$tmp/overlay.pdf" "$n"); fi
done < "$tmp/order.txt"
qpdf --empty --pages "${args[@]}" -- "$out"
echo "OK : $out"
