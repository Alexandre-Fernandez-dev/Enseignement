#!/usr/bin/env python3
"""Versions texte allégées des documents de l'année, pour le Projet Claude.

Produit : <année>/Textes/, une copie allégée de chaque .tex des chapitres et des
fiches calcul, plus les *_Sequence.md et progression.md. Le Projet Claude
« Cours » lit ce dossier via GitHub : il tient dans la taille limite,
contrairement aux .tex complets.

Allègement : on garde le corps du document et les figures TikZ, qui permettent
d'expliquer les graphiques. Les figures définies par une macro du préambule
(\\newcommand contenant un tikzpicture) sont recopiées en tête du fichier, avec
leur commentaire. Les longues listes « plot coordinates {...} » sont réduites
aux points d'abscisse entière et aux extremums. On retire le reste du préambule,
les commentaires du corps et les commandes de mise en page.

Relancer (depuis la racine du dépôt), après un nouveau document :
    python3 scripts/textes_projet.py                # année 2026-2027
    python3 scripts/textes_projet.py --avec-ap      # ajoute les fiches d'AP
    python3 scripts/textes_projet.py --sans-figures # figures remplacées par [figure]
Puis committer 2026-2027/Textes/ et cliquer « Synchroniser » dans le projet.
"""
import re
import shutil
import sys
from pathlib import Path

ANNEE = "2026-2027"
RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / ANNEE
CIBLE = SOURCE / "Textes"

FIGURES = ("tikzpicture", "axis", "pspicture")
NOMBRE = r"-?\d+(?:\.\d+)?"


def accolade_fermante(texte: str, i: int) -> int:
    """Indice juste après l'accolade qui ferme celle ouverte en texte[i]."""
    prof = 0
    while i < len(texte):
        c = texte[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            prof += 1
        elif c == "}":
            prof -= 1
            if prof == 0:
                return i + 1
        i += 1
    return len(texte)


def points_cles(liste: str) -> str:
    """Réduit une liste de points aux abscisses entières et aux extremums."""
    pts = [(float(x), float(y)) for x, y in
           re.findall(rf"\(\s*({NOMBRE})\s*,\s*({NOMBRE})\s*\)", liste)]
    if len(pts) <= 15:
        return liste
    garde = []
    for k, (x, y) in enumerate(pts):
        extremum = 0 < k < len(pts) - 1 and (
            (y - pts[k - 1][1]) * (pts[k + 1][1] - y) < 0)
        if k in (0, len(pts) - 1) or abs(x - round(x)) < 1e-9 or extremum:
            garde.append(f"({x:g},{y:g})")
    return " ".join(garde) + "  [points clés]"


def compacter_figure(fig: str) -> str:
    fig = re.sub(r"(?m)(?<!\\)%.*$", "", fig)
    fig = re.sub(r"plot coordinates\s*\{([^{}]*)\}",
                 lambda m: "plot coordinates {" + points_cles(m.group(1)) + "}", fig)
    fig = re.sub(r"(?m)^[ \t]+", "", fig)
    return re.sub(r"\n\s*\n", "\n", fig).strip()


def macros_figures(preambule: str) -> str:
    """Macros du préambule qui dessinent une figure, avec leur commentaire."""
    blocs = []
    for m in re.finditer(r"\\(?:re)?newcommand\*?\s*\{?\\\w+\}?(?:\[\d\])?\s*(?=\{)",
                         preambule):
        fin = accolade_fermante(preambule, m.end())
        corps = preambule[m.start():fin]
        if not any(f"\\begin{{{env}}}" in corps for env in FIGURES) \
                and "\\draw" not in corps:
            continue
        avant = preambule[:m.start()].rstrip("\n").split("\n")
        commentaire = []
        while avant and avant[-1].lstrip().startswith("%"):
            commentaire.insert(0, avant.pop().strip())
        blocs.append("\n".join(commentaire + [compacter_figure(corps)]))
    if not blocs:
        return ""
    return ("% --- Figures définies dans le préambule ---\n"
            + "\n\n".join(blocs) + "\n% --- Fin des figures ---\n\n")


def alleger(texte: str, figures: bool) -> str:
    debut = texte.find("\\begin{document}")
    preambule = texte[:debut] if debut >= 0 else ""
    if debut >= 0:
        texte = texte[debut + len("\\begin{document}"):]
    texte = texte.replace("\\end{document}", "")
    for env in FIGURES:
        texte = re.sub(rf"\\begin\{{{env}\}}.*?\\end\{{{env}\}}",
                       (lambda m: compacter_figure(m.group(0))) if figures
                       else (lambda m: "[figure]"),
                       texte, flags=re.S)
    texte = re.sub(r"\\includegraphics(\[[^\]]*\])?\{[^}]*\}", "[image]", texte)
    texte = re.sub(r"(?m)(?<!\\)%.*$", "", texte)          # commentaires
    # définitions des macros prof/élève et mise en page : inutiles à la lecture
    texte = re.sub(r"\\ifdefined\\ELEVE.*?\\fi\b", "", texte, flags=re.S)
    texte = re.sub(r"(?m)^\s*\\(maketitle|thispagestyle|pagestyle|tableofcontents"
                   r"|newsavebox|newpage|clearpage|vfill|medskip|bigskip|smallskip"
                   r"|noindent|centering)\b.*$", "", texte)
    texte = re.sub(r"\\[vh]space\*?\{[^}]*\}", "", texte)
    texte = re.sub(r"(?m)^[ \t]+$", "", texte)
    texte = re.sub(r"\n{3,}", "\n\n", texte)
    entete = macros_figures(preambule) if figures else ""
    return entete + texte.strip() + "\n"


def a_inclure(chemin: Path, avec_ap: bool) -> bool:
    parties = chemin.relative_to(SOURCE).parts
    if "Textes" in parties or ".build" in parties or chemin.name == "def.tex":
        return False
    if not avec_ap and "AP" in parties:
        return False
    return any(p.startswith("Ch ") or p == "Fiches calcul" or p == "AP"
               for p in parties)


def main() -> None:
    avec_ap = "--avec-ap" in sys.argv
    figures = "--sans-figures" not in sys.argv
    if CIBLE.exists():
        shutil.rmtree(CIBLE)
    total = nb = 0
    for tex in sorted(SOURCE.rglob("*.tex")):
        if not a_inclure(tex, avec_ap):
            continue
        sortie = CIBLE / tex.relative_to(SOURCE).with_suffix(".txt")
        sortie.parent.mkdir(parents=True, exist_ok=True)
        contenu = f"% Source : {tex.relative_to(RACINE)}\n" + alleger(
            tex.read_text(encoding="utf-8", errors="replace"), figures)
        sortie.write_text(contenu, encoding="utf-8")
        total += len(contenu.encode())
        nb += 1
    for md in sorted(SOURCE.rglob("*.md")):
        rel = md.relative_to(SOURCE)
        if "Textes" in rel.parts or not (md.name.endswith("_Sequence.md")
                                          or md.name == "progression.md"):
            continue
        sortie = CIBLE / rel
        sortie.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(md, sortie)
        total += md.stat().st_size
        nb += 1
    print(f"{nb} fichiers dans {CIBLE.relative_to(RACINE)}, {total // 1024} Ko.")


if __name__ == "__main__":
    main()
