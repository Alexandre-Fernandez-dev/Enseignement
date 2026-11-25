"""Génère les sujets A et B et le corrigé du contrôle mixte du 27/11 (Seconde, Ch2 + Ch3).

Les deux sujets ont la même structure : les énoncés sont écrits une seule fois
(fonction corps) et les valeurs propres à chaque sujet sont dans le dictionnaire S.
Modifier ce script plutôt que les .tex, puis relancer :

    python3 genere_sujets.py            # écrit les .tex dans ce dossier
    ../../../../../compile.sh "$PWD/2nde_Ch3_Sommatif_SujetA.tex"   # puis SujetB, Corrige

Fichiers produits : 2nde_Ch3_Sommatif_SujetA.tex, 2nde_Ch3_Sommatif_SujetB.tex,
2nde_Ch3_Sommatif_Corrige.tex.
"""
import sys, os

# Dossier de sortie : celui du script, ou celui donné en argument
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

# ---------- Courbe monotone par morceaux (interpolation de Fritsch-Carlson) ----------
def pchip(pts, step=0.05):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    n = len(pts)
    h = [xs[i+1]-xs[i] for i in range(n-1)]
    d = [(ys[i+1]-ys[i])/h[i] for i in range(n-1)]
    m = [0.0]*n
    for i in range(1, n-1):
        if d[i-1]*d[i] <= 0:
            m[i] = 0.0
        else:
            w1 = 2*h[i]+h[i-1]; w2 = h[i]+2*h[i-1]
            m[i] = (w1+w2)/(w1/d[i-1]+w2/d[i])
    m[0] = d[0]; m[-1] = d[-1]
    out = []
    for i in range(n-1):
        x0, x1, y0, y1 = xs[i], xs[i+1], ys[i], ys[i+1]
        k = int(round((x1-x0)/step))
        for j in range(k + (1 if i == n-2 else 0)):
            t = j/k; hh = x1-x0
            h00 = 2*t**3-3*t**2+1; h10 = t**3-2*t**2+t; h01 = -2*t**3+3*t**2; h11 = t**3-t**2
            y = h00*y0 + h10*hh*m[i] + h01*y1 + h11*hh*m[i+1]
            out.append(f"({x0+t*hh:.2f},{y:.3f})")
    return " ".join(out)

# ---------- Données des sujets ----------
S = {
 'A': dict(
  frac='\\dfrac{42}{56}', frac_c='\\dfrac{42}{56} = \\dfrac{3 \\times 14}{4 \\times 14} = \\dfrac{3}{4}',
  prod='\\dfrac{4}{9}\\times\\dfrac{15}{8}', prod_c='\\dfrac{4}{9}\\times\\dfrac{15}{8} = \\dfrac{4 \\times 3 \\times 5}{3 \\times 3 \\times 4 \\times 2} = \\dfrac{5}{6}',
  pb="Le matin, Léa a bu $\\dfrac{1}{3}$ d'une bouteille d'eau. À midi, elle a bu $\\dfrac{1}{4}$ du reste. Quelle fraction de la bouteille a-t-elle bue à midi~?",
  pb_c="Il reste $1 - \\dfrac{1}{3} = \\dfrac{2}{3}$ de la bouteille. À midi : $\\dfrac{1}{4} \\times \\dfrac{2}{3} = \\dfrac{2}{12} = \\dfrac{1}{6}$ de la bouteille.",
  fa='x^2-49', fa_c='x^2-49 = x^2-7^2 = (x-7)(x+7)',
  fi='9x^2-12x+4', fi_c='9x^2-12x+4 = (3x)^2 - 2\\times 3x \\times 2 + 2^2 = (3x-2)^2',
  ineq='-3x+12\\geqslant 0', ineq_c='-3x \\geqslant -12 \\iff x \\leqslant \\dfrac{-12}{-3} \\iff x \\leqslant 4', ineq_s='S = \\left]-\\infty\\,;\\,4\\right]',
  ineq_rem='on divise par $-3 < 0$ : le sens de l\'inégalité change',
  pct='75\\,\\%$ de $120', pct_c='$120 \\div 4 = 30$, donc $75\\,\\% = 3 \\times 30 = 90$.',
  rac='\\sqrt{3-7}', rac_c='$3 - 7 = -4 < 0$ : un nombre négatif n\'a pas de racine carrée, donc $\\sqrt{3-7}$ n\'existe pas.',
  vec='\\overrightarrow{AB}+\\overrightarrow{CA}', vec_c='\\overrightarrow{AB}+\\overrightarrow{CA} = \\overrightarrow{CA}+\\overrightarrow{AB} = \\overrightarrow{CB}',
  ens=['\\dfrac{-18}{6}\\in\\mathbb{Z}', '\\dfrac{7}{4}\\in\\mathbb{D}', '-2{,}35\\in\\mathbb{Q}', '\\sqrt{49}\\in\\mathbb{N}'],
  ens_c=['$\\dfrac{-18}{6} = -3$, entier relatif.', '$\\dfrac{7}{4} = \\dfrac{175}{100} = \\dfrac{175}{10^2}$.', '$-2{,}35 = \\dfrac{-235}{100}$, quotient d\'entiers.', '$\\sqrt{49} = 7$, entier naturel.'],
  pts=[(-4,-3),(-3,1),(-2,3),(0,1),(2,-2),(4,1),(5,2)], xmin=-4, xmax=5, ymin=-3, ymax=3, lab=(-3.2,2.6),
  q3=['Donner $f(2)$ et l\'image de $-4$ par $f$.', 'Déterminer les antécédents de $1$ par $f$.', 'Résoudre l\'équation $f(x) = 3$.', 'Résoudre l\'inéquation $f(x) \\geqslant 1$.', 'Combien l\'équation $f(x) = 0$ a-t-elle de solutions~?'],
  q3c=['$f(2) = -2$ \\quad et \\quad $f(-4) = -3$.', 'Les antécédents de $1$ sont $-3$, $0$ et $4$.', '$S = \\{-2\\}$.', '$S = [-3\\,;\\,0] \\cup [4\\,;\\,5]$.', '$3$ solutions (la courbe coupe l\'axe des abscisses trois fois).'],
  df='[-4\\,;\\,5]',
  ctx="Une salle d'escalade propose deux formules :\n\\begin{itemize}[label=\\textbullet, itemsep=1pt, topsep=2pt]\n  \\item \\textbf{Formule A} : $4$~€ par séance ;\n  \\item \\textbf{Formule B} : un abonnement de $20$~€, puis $2$~€ par séance.\n\\end{itemize}",
  var="On note $x$ le nombre de séances, avec $0 \\leqslant x \\leqslant 15$. Le prix payé est $f(x) = 4x$ avec la formule A, et $g(x) = 20 + 2x$ avec la formule B.",
  q41='Calculer $f(5)$ et $g(5)$. Quelle formule est la moins chère pour $5$ séances~?',
  c41='$f(5) = 4 \\times 5 = 20$ et $g(5) = 20 + 2 \\times 5 = 30$. Pour $5$ séances, la formule A est la moins chère.',
  M='M(12\\,;\\,44)', c42='$g(12) = 20 + 2 \\times 12 = 44$ : c\'est l\'ordonnée de $M$, donc $M \\in \\mathcal{C}_g$.',
  c43='Les droites se coupent au point d\'abscisse $10$ : $S = \\{10\\}$. Pour $10$ séances, les deux formules coûtent le même prix ($40$~€).',
  c44='$\\mathcal{C}_f$ est en dessous de $\\mathcal{C}_g$ pour $x \\in [0\\,;\\,10[$. La formule A est moins chère pour moins de $10$ séances.',
  F='4*\\x', G='20+2*\\x', X=15, unit='séances', fpos=(13.4,57), gpos=(13.8,41.5),
  c=6, gex='18-3x', gfun='18-3*\\x', f2='f(2) = 2^2 = 4', g2='g(2) = 18 - 3 \\times 2 = 12',
  g2i="Pour $x = 2$, le carré a une aire de $4$~cm$^2$ et le triangle une aire de $12$~cm$^2$.",
  gk='6', gkc='18 - 3x = 6 \\iff -3x = -12 \\iff x = 4', gki="L'aire du triangle vaut $6$~cm$^2$ pour $AM = 4$~cm.",
  r_ex='6x', r_2='f(2) = 6 \\times 2 = 12', r_2v='12', r_k='24', r_kc='6x = 24 \\iff x = \\dfrac{24}{6} = 4', r_kr='4',
  sq_ex='36 - x^2', sq_ix='2', sq_ic='f(2) = 36 - 2^2 = 36 - 4 = 32', sq_iv='32', sq_ax='4', sq_ay='20', sq_ac='f(4) = 36 - 4^2 = 36 - 16 = 20', sq_k='27', sq_kc='36 - x^2 = 27 \\iff x^2 = 9', sq_ksq='9', sq_kx='3',
  xi=3, yi=9, Y=36, ystep=2, ylab=6, ysc2=0.2, xsc2=1.15, flab2=(5.4,33), glab2=(1.1,17.5),
  gv='36', gc='20 + 2x = 36 \\iff 2x = 16 \\iff x = 8', gi="Avec $36$~€, on peut faire $8$ séances avec la formule B.",
  vf='« $20$ est un antécédent de $5$ par $f$. »', vfc="Faux : $f(5) = 20$, donc $20$ est l'image de $5$ par $f$, et $5$ est un antécédent de $20$.",
  h='x^2-2x-3', hx='-1', hc='h(-1) = (-1)^2 - 2 \\times (-1) - 3 = 1 + 2 - 3 = 0',
  kf='3x-5', kv='7', kc='3x - 5 = 7 \\iff 3x = 12 \\iff x = 4', kr='4',
  hz='3', hzc='h(3) = 9 - 6 - 3 = 0', autre='-1',
  P=12, demi=6, aire='x(6-x)', a2='f(2) = 2 \\times (6-2) = 8', a2i="Un rectangle de côté $2$~cm a une aire de $8$~cm$^2$.",
  k=8, sk="x = 2 \\text{ ou } x = 4", ski="L'aire vaut $8$~cm$^2$ quand un côté mesure $2$~cm ou $4$~cm.",
  m=5, sm="[1\\,;\\,5]", smi="L'aire est au moins $5$~cm$^2$ quand $x$ est entre $1$ et $5$~cm.",
  amax=9, xmax_=3, ymaxA=10, ystepA=1, ysc=0.55, xsc=1.2, hfun='\\x*(6-\\x)', hlab=(4.9,7.6)),
 'B': dict(
  frac='\\dfrac{35}{49}', frac_c='\\dfrac{35}{49} = \\dfrac{5 \\times 7}{7 \\times 7} = \\dfrac{5}{7}',
  prod='\\dfrac{6}{25}\\times\\dfrac{10}{9}', prod_c='\\dfrac{6}{25}\\times\\dfrac{10}{9} = \\dfrac{2 \\times 3 \\times 2 \\times 5}{5 \\times 5 \\times 3 \\times 3} = \\dfrac{4}{15}',
  pb="Tom a mangé $\\dfrac{2}{5}$ d'une tarte. Ensuite, sa sœur a mangé $\\dfrac{1}{3}$ du reste. Quelle fraction de la tarte sa sœur a-t-elle mangée~?",
  pb_c="Il reste $1 - \\dfrac{2}{5} = \\dfrac{3}{5}$ de la tarte. Sa sœur a mangé $\\dfrac{1}{3} \\times \\dfrac{3}{5} = \\dfrac{3}{15} = \\dfrac{1}{5}$ de la tarte.",
  fa='x^2-64', fa_c='x^2-64 = x^2-8^2 = (x-8)(x+8)',
  fi='4x^2-20x+25', fi_c='4x^2-20x+25 = (2x)^2 - 2\\times 2x \\times 5 + 5^2 = (2x-5)^2',
  ineq='-2x+10<0', ineq_c='-2x < -10 \\iff x > \\dfrac{-10}{-2} \\iff x > 5', ineq_s='S = \\left]5\\,;\\,+\\infty\\right[',
  ineq_rem='on divise par $-2 < 0$ : le sens de l\'inégalité change',
  pct='75\\,\\%$ de $160', pct_c='$160 \\div 4 = 40$, donc $75\\,\\% = 3 \\times 40 = 120$.',
  rac='\\sqrt{2-5}', rac_c='$2 - 5 = -3 < 0$ : un nombre négatif n\'a pas de racine carrée, donc $\\sqrt{2-5}$ n\'existe pas.',
  vec='\\overrightarrow{BC}+\\overrightarrow{AB}', vec_c='\\overrightarrow{BC}+\\overrightarrow{AB} = \\overrightarrow{AB}+\\overrightarrow{BC} = \\overrightarrow{AC}',
  ens=['\\dfrac{-21}{7}\\in\\mathbb{Z}', '\\dfrac{9}{20}\\in\\mathbb{D}', '-1{,}8\\in\\mathbb{Q}', '\\sqrt{64}\\in\\mathbb{N}'],
  ens_c=['$\\dfrac{-21}{7} = -3$, entier relatif.', '$\\dfrac{9}{20} = \\dfrac{45}{100} = \\dfrac{45}{10^2}$.', '$-1{,}8 = \\dfrac{-18}{10}$, quotient d\'entiers.', '$\\sqrt{64} = 8$, entier naturel.'],
  pts=[(-4,1),(-3,0),(-1,-3),(1,0),(3,2),(4,0),(5,-4)], xmin=-4, xmax=5, ymin=-4, ymax=2, lab=(2.2,2.6),
  q3=['Donner $f(-1)$ et l\'image de $5$ par $f$.', 'Déterminer les antécédents de $0$ par $f$.', 'Résoudre l\'équation $f(x) = 2$.', 'Résoudre l\'inéquation $f(x) \\geqslant 0$.', 'Combien l\'équation $f(x) = -1$ a-t-elle de solutions~?'],
  q3c=['$f(-1) = -3$ \\quad et \\quad $f(5) = -4$.', 'Les antécédents de $0$ sont $-3$, $1$ et $4$.', '$S = \\{3\\}$.', '$S = [-4\\,;\\,-3] \\cup [1\\,;\\,4]$.', '$3$ solutions (la courbe coupe la droite d\'équation $y = -1$ trois fois).'],
  df='[-4\\,;\\,5]',
  ctx="Un loueur de trottinettes propose deux formules :\n\\begin{itemize}[label=\\textbullet, itemsep=1pt, topsep=2pt]\n  \\item \\textbf{Formule A} : $5$~€ par heure ;\n  \\item \\textbf{Formule B} : $12$~€ de frais de dossier, puis $3$~€ par heure.\n\\end{itemize}",
  var="On note $x$ la durée de location en heures, avec $0 \\leqslant x \\leqslant 12$. Le prix payé est $f(x) = 5x$ avec la formule A, et $g(x) = 12 + 3x$ avec la formule B.",
  q41='Calculer $f(4)$ et $g(4)$. Quelle formule est la moins chère pour $4$ heures~?',
  c41='$f(4) = 5 \\times 4 = 20$ et $g(4) = 12 + 3 \\times 4 = 24$. Pour $4$ heures, la formule A est la moins chère.',
  M='M(10\\,;\\,40)', c42='$g(10) = 12 + 3 \\times 10 = 42 \\neq 40$, donc $M \\notin \\mathcal{C}_g$.',
  c43='Les droites se coupent au point d\'abscisse $6$ : $S = \\{6\\}$. Pour $6$ heures, les deux formules coûtent le même prix ($30$~€).',
  c44='$\\mathcal{C}_f$ est en dessous de $\\mathcal{C}_g$ pour $x \\in [0\\,;\\,6[$. La formule A est moins chère pour moins de $6$ heures.',
  F='5*\\x', G='12+3*\\x', X=12, unit='heures', fpos=(10.6,57), gpos=(11.5,39.5),
  c=8, gex='32-4x', gfun='32-4*\\x', f2='f(2) = 2^2 = 4', g2='g(2) = 32 - 4 \\times 2 = 24',
  g2i="Pour $x = 2$, le carré a une aire de $4$~cm$^2$ et le triangle une aire de $24$~cm$^2$.",
  gk='8', gkc='32 - 4x = 8 \\iff -4x = -24 \\iff x = 6', gki="L'aire du triangle vaut $8$~cm$^2$ pour $AM = 6$~cm.",
  r_ex='8x', r_2='f(2) = 8 \\times 2 = 16', r_2v='16', r_k='40', r_kc='8x = 40 \\iff x = \\dfrac{40}{8} = 5', r_kr='5',
  sq_ex='64 - x^2', sq_ix='3', sq_ic='f(3) = 64 - 3^2 = 64 - 9 = 55', sq_iv='55', sq_ax='6', sq_ay='28', sq_ac='f(6) = 64 - 6^2 = 64 - 36 = 28', sq_k='39', sq_kc='64 - x^2 = 39 \\iff x^2 = 25', sq_ksq='25', sq_kx='5',
  xi=4, yi=16, Y=64, ystep=4, ylab=8, ysc2=0.112, xsc2=0.86, flab2=(7.3,58), glab2=(1.3,30),
  gv='33', gc='12 + 3x = 33 \\iff 3x = 21 \\iff x = 7', gi="Avec $33$~€, on peut louer $7$ heures avec la formule B.",
  vf='« $20$ est un antécédent de $4$ par $f$. »', vfc="Faux : $f(4) = 20$, donc $20$ est l'image de $4$ par $f$, et $4$ est un antécédent de $20$.",
  h='x^2+2x-8', hx='-4', hc='h(-4) = (-4)^2 + 2 \\times (-4) - 8 = 16 - 8 - 8 = 0',
  kf='2x+7', kv='1', kc='2x + 7 = 1 \\iff 2x = -6 \\iff x = -3', kr='-3',
  hz='2', hzc='h(2) = 4 + 4 - 8 = 0', autre='-4',
  P=16, demi=8, aire='x(8-x)', a2='f(2) = 2 \\times (8-2) = 12', a2i="Un rectangle de côté $2$~cm a une aire de $12$~cm$^2$.",
  k=12, sk="x = 2 \\text{ ou } x = 6", ski="L'aire vaut $12$~cm$^2$ quand un côté mesure $2$~cm ou $6$~cm.",
  m=7, sm="[1\\,;\\,7]", smi="L'aire est au moins $7$~cm$^2$ quand $x$ est entre $1$ et $7$~cm.",
  amax=16, xmax_=4, ymaxA=16, ystepA=2, ysc=0.34, xsc=0.9, hfun='\\x*(8-\\x)', hlab=(6.6,12.8)),
}

PREAMBULE = r"""%LTeX: language=fr-FR
\documentclass[12pt]{article}
\usepackage[fontsize=13pt]{scrextend}
\usepackage{amsmath,amssymb}
\usepackage[french]{babel}
\usepackage{enumitem}
\usepackage{currfile}
\usepackage{xcolor}
\usepackage{tasks}
\usepackage{pifont}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,patterns}
\usepackage{geometry}
\geometry{left=1.5cm, right=1.5cm, top=1cm, bottom=1cm}
\setlength{\parindent}{0cm}
\setlength{\parskip}{2pt}
\pagestyle{empty}
\input{def.tex}

\usepackage{tcolorbox}
\tcbuselibrary{skins}
\definecolor{bandeau}{HTML}{E8EEF7}
% Bandeau de titre de chaque exercice (même style que les contrôles de 1re ST2S)
\newtcbox{\exobox}{colback=bandeau, colframe=bandeau, boxrule=0pt, arc=0pt, left=4pt, right=4pt, top=3pt, bottom=3pt, fontupper=\bfseries}
\newcounter{exo}
% Espace avant chaque exercice (élastique dans les sujets, pour répartir les exercices sur la page)
\newcommand{\exoskip}{\vspace{1.4em}}
% \begin{exercice}{titre}{barème}
\newenvironment{exercice}[2]{%
  \stepcounter{exo}\par\ifnum\value{exo}=1 \vspace{0.8em}\else\exoskip\fi
  \noindent\exobox{Exercice \theexo{} --- #1 (#2 points)}\par\vspace{0.3em}
}{\par}
\setlist[enumerate]{label=\arabic*., itemsep=2pt, topsep=3pt}
\colorlet{sol}{blue!70!black}
\newcommand{\sol}[1]{\textcolor{sol}{#1}}
\newcommand{\bareme}[1]{\par\vspace{6pt}\noindent\textcolor{sol}{\small #1}}
"""

def repere_f(d, sol=False):
    xmin, xmax, ymin, ymax = d['xmin'], d['xmax'], d['ymin'], d['ymax']
    curve = pchip(d['pts'])
    return rf"""\begin{{tikzpicture}}[x=0.98cm, y=0.9cm, lab/.style={{fill=white, fill opacity=0.75, text opacity=1, inner sep=0.6pt}}]
  \draw[gray!55, thin, xstep=1, ystep=1] ({xmin},{ymin}) grid ({xmax},{ymax});
  \draw[-{{Latex[length=2mm]}}, thick] ({xmin},0) -- ({xmax}+0.5,0);
  \draw[-{{Latex[length=2mm]}}, thick] (0,{ymin}) -- (0,{ymax}+0.5);
  \draw[thick, blue!60!black] plot coordinates {{{curve}}};
  \fill[blue!60!black] {d['pts'][0]} circle (2.2pt) {d['pts'][-1]} circle (2.2pt);
  \foreach \x in {{{xmin},...,-1,1,2,...,{xmax}}} {{\draw[thick] (\x,0.08) -- (\x,-0.08); \node[below, lab, yshift=-1.5pt] at (\x,0) {{\footnotesize $\x$}};}}
  \foreach \y in {{{ymin},...,-1,1,2,...,{ymax}}} {{\draw[thick] (0.08,\y) -- (-0.08,\y); \node[left, lab, xshift=-1.5pt] at (0,\y) {{\footnotesize $\y$}};}}
  \node[below left, lab, xshift=-1pt, yshift=-1pt] at (0,0) {{\footnotesize $0$}};
  \node[lab, text=blue!60!black] at {d['lab']} {{$\mathcal{{C}}_f$}};
\end{{tikzpicture}}"""

def repere_fg(d):
    X = d['X']
    return rf"""\begin{{tikzpicture}}[x=0.52cm, y=0.09cm]
  \draw[gray!35, very thin, xstep=1, ystep=5] (0,0) grid ({X},60);
  \draw[-{{Latex[length=2mm]}}] (0,0) -- ({X}+0.6,0) node[below=9pt, anchor=north east] {{\scriptsize {d['unit']}}};
  \draw[-{{Latex[length=2mm]}}] (0,0) -- (0,63) node[above] {{\scriptsize prix (€)}};
  \foreach \x in {{2,4,...,{X}}} \node[below] at (\x,0) {{\scriptsize $\x$}};
  \foreach \y in {{10,20,...,60}} \node[left] at (0,\y) {{\scriptsize $\y$}};
  \node[below left] at (0,0) {{\scriptsize $0$}};
  \begin{{scope}}
    \clip (0,0) rectangle ({X},60);
    \draw[very thick] plot[domain=0:{X}, samples=2] (\x, {{{d['F']}}});
    \draw[very thick, dashed] plot[domain=0:{X}, samples=2] (\x, {{{d['G']}}});
  \end{{scope}}
  \node at {d['fpos']} {{$\mathcal{{C}}_f$}};
  \node at {d['gpos']} {{$\mathcal{{C}}_g$}};
\end{{tikzpicture}}"""

def repere_aire(d):
    L = d['demi']; Y = d['ymaxA']; st = d['ystepA']
    return rf"""\begin{{tikzpicture}}[x={d['xsc']}cm, y={d['ysc']}cm]
  \draw[gray!35, very thin, xstep=1, ystep={st}] (0,0) grid ({L},{Y});
  \draw[gray!20, very thin, xstep=0.5, ystep={st}] (0,0) grid ({L},{Y});
  \draw[-{{Latex[length=2mm]}}] (0,0) -- ({L}+0.5,0) node[below=9pt, anchor=north east] {{\scriptsize $x$ (cm)}};
  \draw[-{{Latex[length=2mm]}}] (0,0) -- (0,{Y}+0.8) node[above] {{\scriptsize aire (cm$^2$)}};
  \foreach \x in {{1,...,{L}}} \node[below] at (\x,0) {{\scriptsize $\x$}};
  \foreach \y in {{{st},{2*st},...,{Y}}} \node[left] at (0,\y) {{\scriptsize $\y$}};
  \node[below left] at (0,0) {{\scriptsize $0$}};
  \draw[very thick, domain=0:{L}, samples=60, smooth] plot (\x, {{{d['hfun']}}});
  \node at {d['hlab']} {{$\mathcal{{C}}$}};
\end{{tikzpicture}}"""

def figure_carre(d):
    c = d['c']; m = 2 if c == 6 else 3
    return rf"""\begin{{tikzpicture}}[scale={0.62 if c == 6 else 0.47}]
  \fill[pattern=north east lines] (0,0) rectangle ({c},{c});
  \fill[white] (0,0) rectangle ({m},{m});
  \draw[very thick] (0,0) -- ({c},0) -- ({c},{c}) -- (0,{c}) -- cycle;
  \draw[thick] ({m},0) -- ({m},{m}) -- (0,{m});
  \node[below left] at (0,0) {{$A$}};
  \node[below right] at ({c},0) {{$B$}};
  \node[above right] at ({c},{c}) {{$C$}};
  \node[above left] at (0,{c}) {{$D$}};
  \node[below right] at ({m},0) {{$M$}};
  \node[left] at (0,{m}) {{$P$}};
  \node[fill=white, inner sep=1pt, above right] at ({m},{m}) {{$N$}};
  \draw[densely dashed, gray] (0,-0.2) -- (0,-1.7) ({m},-0.2) -- ({m},-1.7);
  \draw[{{Bar[width=2.5mm]Latex[length=2mm]}}-{{Latex[length=2mm]Bar[width=2.5mm]}}, thick] (0,-1.5) -- node[below=1pt] {{$x$}} ({m},-1.5);
\end{{tikzpicture}}"""

def repere_geo(d):
    c = d['c']; Y = d['Y']; st = d['ystep']; yl = d['ylab']
    return rf"""\begin{{tikzpicture}}[x={d['xsc2']}cm, y={d['ysc2']}cm]
  \draw[gray!35, very thin, xstep=1, ystep={st}] (0,0) grid ({c},{Y});
  \draw[-{{Latex[length=2mm]}}] (0,0) -- ({c}+0.5,0) node[right] {{\scriptsize $x$}};
  \draw[-{{Latex[length=2mm]}}] (0,0) -- (0,{Y}+3) node[above] {{\scriptsize aire (cm$^2$)}};
  \foreach \x in {{1,...,{c}}} \node[below] at (\x,0) {{\scriptsize $\x$}};
  \foreach \y in {{{yl},{2*yl},...,{Y}}} \node[left] at (0,\y) {{\scriptsize $\y$}};
  \node[below left] at (0,0) {{\scriptsize $0$}};
  \draw[very thick, domain=0:{c}, samples=60, smooth] plot (\x, {{\x*\x}});
  \draw[very thick, dashed, domain=0:{c}, samples=2] plot (\x, {{{d['gfun']}}});
  \node at {d['flab2']} {{$\mathcal{{C}}_f$}};
  \node at {d['glab2']} {{$\mathcal{{C}}_g$}};
\end{{tikzpicture}}"""

def corps(k, corrige=False):
    d = S[k]
    C = corrige
    def s(txt):  # solution affichée seulement dans le corrigé
        return (r" \sol{" + txt + "}") if C else ""
    def b(txt):
        return (r"\bareme{" + txt + "}") if C else ""
    out = []
    if C:
        out.append(rf"""\begin{{center}}
  {{\large\bfseries Corrigé du contrôle ({k}) --- Nombres et fonctions}}\\[0.3em]
  {{\itshape Seconde \quad $\bullet$ \quad Barème sur 20 points}}
\end{{center}}""")
    else:
        out.append(rf"""\begin{{center}}
  {{\large\bfseries Contrôle ({k}) --- Nombres et fonctions}}\\[0.3em]
  {{\itshape Seconde \quad $\bullet$ \quad Durée~: 55 minutes}}
\end{{center}}
\noindent\textit{{Toutes les réponses doivent être justifiées.}}""")
    # Exercice 1 : automatismes et ensembles de nombres
    out.append(r"""\begin{exercice}{Automatismes}{5}
Les questions sont indépendantes. Détailler les calculs.
\begin{enumerate}""")
    out.append(rf"""  \item Calculer ${d['prod']}$. Donner le résultat sous forme irréductible.{s('$' + d['prod_c'] + '$')}
  \item Résoudre l'inéquation ${d['ineq']}$. Donner les solutions sous forme d'intervalle.{s('$' + d['ineq_c'] + '$ (' + d['ineq_rem'] + '), donc $' + d['ineq_s'] + '$.')}
  \item Calculer ${d['pct']}$.{s(d['pct_c'])}
  \item Justifier chaque appartenance.
  \begin{{tasks}}[label=\alph*), label-width=1.4em, item-indent=1.8em](4)""")
    for i in range(4):
        out.append(rf"""    \task ${d['ens'][i]}$""" + ((r"\\[2pt]" + r"\sol{\small " + d['ens_c'][i] + "}") if C else ""))
    out.append(r"""  \end{tasks}
\end{enumerate}""")
    out.append(b("Questions 1 à 3 : 1 point chacune (question 2 : $0{,}5$ pour la résolution avec le changement de sens, $0{,}5$ pour l'intervalle). Question 4 : $0{,}5$ par nombre, l'écriture qui justifie (entier, $\\dfrac{a}{10^n}$, $\\dfrac{a}{b}$) est attendue."))
    out.append(r"""\end{exercice}
""")
    # Exercice 2 : lecture graphique
    out.append(rf"""\begin{{exercice}}{{Lecture graphique}}{{5}}
La courbe $\mathcal{{C}}_f$ ci-contre représente une fonction $f$. Répondre par lecture graphique.
\par\smallskip
\begin{{minipage}}[t]{{0.46\linewidth}}\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000
\begin{{enumerate}}
  \item Quel est l'ensemble de définition de $f$~?{s('$' + d['df'] + '$')}""")
    for i in (0, 1, 3):
        out.append(rf"""  \item {d['q3'][i]}{s(d['q3c'][i])}""")
    out.append(rf"""\end{{enumerate}}
\end{{minipage}}\hfill
\begin{{minipage}}[t]{{0.52\linewidth}}
\vspace{{0pt}}\centering
{repere_f(d)}
\end{{minipage}}""")
    out.append(b("1. $1$ ; 2. $1$ ($0{,}5 + 0{,}5$) ; 3. $1{,}5$ (tous les antécédents) ; 4. $1{,}5$ (crochets et réunion)."))
    out.append(r"""\end{exercice}
""")
    # Exercice 3 : problème (formules de prix)
    if not C:
        out.append(r"""\vfill
\noindent\hfill\textbf{Tournez la page}\enspace{\Large\ding{228}}
\newpage""")
    out.append(rf"""\begin{{exercice}}{{Problème}}{{6}}
{d['ctx']}
{d['var']}

\begin{{minipage}}[t]{{0.5\linewidth}}\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000
\begin{{enumerate}}
  \item {d['q41']}{s(d['c41'])}
  \item Le point ${d['M']}$ appartient-il à la courbe $\mathcal{{C}}_g$~? Justifier par un calcul.{s(d['c42'])}
  \item Les courbes de $f$ et $g$ sont tracées ci-contre. Résoudre graphiquement $f(x) = g(x)$. Interpréter le résultat.{s(d['c43'])}
  \item Résoudre graphiquement $f(x) < g(x)$. Interpréter le résultat.{s(d['c44'])}
\end{{enumerate}}
\end{{minipage}}\hfill
\begin{{minipage}}[t]{{0.48\linewidth}}
\vspace{{0pt}}\centering
{repere_fg(d)}
\end{{minipage}}""")
    out.append(b("$1{,}5$ point par question. Question 1 : $0{,}5 + 0{,}5$ pour les calculs, $0{,}5$ pour la conclusion. Questions 3 et 4 : lecture $1$, interprétation $0{,}5$."))
    out.append(r"""\end{exercice}
""")
    # Exercice 4 : aire hachurée = carré ABCD privé du carré AMNP
    c = d['c']
    out.append(rf"""\begin{{exercice}}{{Fonction et géométrie}}{{4}}
\begin{{minipage}}[t]{{0.6\linewidth}}
\vspace{{0pt}}\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000
$ABCD$ est un carré de côté ${c}$~cm.

$M$ est un point du segment $[AB]$.

On note $x$ la longueur $AM$, en cm.

$AMNP$ est un carré, avec $P$ sur le segment $[AD]$.

On note $f(x)$ l'aire de la partie hachurée, en cm$^2$.
\begin{{enumerate}}
  \item Dans quel intervalle le nombre $x$ peut-il varier~?{s('$M$ est sur $[AB]$ et $AB = ' + str(c) + '$, donc $x \\in [0\\,;\\,' + str(c) + ']$.')}
  \item Justifier que $f(x) = {d['sq_ex']}$.{s('L\'aire du carré $ABCD$ est $' + str(c) + '^2 = ' + str(c*c) + '$ et celle du carré $AMNP$ est $x^2$. La partie hachurée est le carré $ABCD$ privé du carré $AMNP$, donc $f(x) = ' + d['sq_ex'] + '$.')}
  \item Calculer $f({d['sq_ix']})$. Interpréter le résultat.{s('$' + d['sq_ic'] + '$. Pour $AM = ' + d['sq_ix'] + '$~cm, l\'aire hachurée est $' + d['sq_iv'] + '$~cm$^2$.')}
  \item Montrer que ${d['sq_kx']}$ est un antécédent de ${d['sq_k']}$ par $f$. Interpréter le résultat.{s('$f(' + d['sq_kx'] + ') = ' + str(d['c']*d['c']) + ' - ' + d['sq_kx'] + '^2 = ' + str(d['c']*d['c']) + ' - ' + d['sq_ksq'] + ' = ' + d['sq_k'] + '$ : l\'image de $' + d['sq_kx'] + '$ est $' + d['sq_k'] + '$, donc $' + d['sq_kx'] + '$ est un antécédent de $' + d['sq_k'] + '$. Pour $AM = ' + d['sq_kx'] + '$~cm, l\'aire hachurée est $' + d['sq_k'] + '$~cm$^2$.')}
\end{{enumerate}}
\end{{minipage}}\hfill
\begin{{minipage}}[t]{{0.36\linewidth}}
\vspace{{0pt}}\centering
{figure_carre(d)}
\end{{minipage}}""")
    out.append(b("1 point par question. Question 2 : $0{,}5$ pour les deux aires, $0{,}5$ pour la différence. Question 3 : calcul $0{,}5$ (le carré se calcule avant la soustraction), interprétation $0{,}5$. Question 4 : calcul de l'image $0{,}5$ ; conclusion avec le mot « antécédent » et interprétation $0{,}5$."))
    out.append(r"""\end{exercice}""")
    return "\n".join(out)

# Sujets
AERE = r"""\renewcommand{\exoskip}{\vspace{1.4em plus 1fill}}
\setlist[enumerate]{label=\arabic*., itemsep=9pt, topsep=6pt}
"""
for k in 'AB':
    with open(os.path.join(OUT, f"2nde_Ch3_Sommatif_Sujet{k}.tex"), "w") as f:
        f.write(PREAMBULE + "\n\\begin{document}\n" + AERE + corps(k) + "\n\\vfill\n\\end{document}\n")
# Corrigé
with open(os.path.join(OUT, "2nde_Ch3_Sommatif_Corrige.tex"), "w") as f:
    f.write(PREAMBULE.replace("fontsize=13pt", "fontsize=12pt") + "\n\\begin{document}\n" + corps('A', True) + "\n\n\\newpage\n\\setcounter{exo}{0}\n" + corps('B', True) + "\n\\end{document}\n")
print("ok")
