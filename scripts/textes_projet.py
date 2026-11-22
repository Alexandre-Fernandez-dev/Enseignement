#!/usr/bin/env python3
"""Versions texte allégées des documents de l'année, pour le Projet Claude.

Produit : <année>/Textes/, une copie allégée de chaque .tex des chapitres et des
fiches calcul (corps du document seulement : sans préambule, sans figures TikZ,
sans commentaires), plus les *_Sequence.md et progression.md.
Le Projet Claude « Cours » lit ce dossier via GitHub : il tient dans la taille
limite, contrairement aux .tex complets.

Relancer (depuis la racine du dépôt), après un nouveau document :
    python3 scripts/textes_projet.py            # année 2026-2027
    python3 scripts/textes_projet.py --avec-ap  # inclut aussi les fiches d'AP
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


def alleger(texte: str) -> str:
    debut = texte.find("\\begin{document}")
    if debut >= 0:
        texte = texte[debut + len("\\begin{document}"):]
    texte = texte.replace("\\end{document}", "")
    for env in FIGURES:
        texte = re.sub(rf"\\begin\{{{env}\}}.*?\\end\{{{env}\}}", "[figure]",
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
    return texte.strip() + "\n"


def a_inclure(chemin: Path, avec_ap: bool) -> bool:
    rel = chemin.relative_to(SOURCE)
    parties = rel.parts
    if "Textes" in parties or ".build" in parties or chemin.name == "def.tex":
        return False
    if not avec_ap and "AP" in parties:
        return False
    return any(p.startswith("Ch ") or p == "Fiches calcul" for p in parties)


def main() -> None:
    avec_ap = "--avec-ap" in sys.argv
    if CIBLE.exists():
        shutil.rmtree(CIBLE)
    total = nb = 0
    for tex in sorted(SOURCE.rglob("*.tex")):
        if not a_inclure(tex, avec_ap):
            continue
        sortie = CIBLE / tex.relative_to(SOURCE).with_suffix(".txt")
        sortie.parent.mkdir(parents=True, exist_ok=True)
        contenu = f"% Source : {tex.relative_to(RACINE)}\n" + alleger(
            tex.read_text(encoding="utf-8", errors="replace"))
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
