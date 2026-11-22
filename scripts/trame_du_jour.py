#!/usr/bin/env python3
"""Affiche les séances prévues un jour donné, pour préparer la « trame du jour ».

Pour chaque niveau (Seconde, 1re ST2S), lit la progression sur le Drive (lecture seule, voir
scripts/progressions.py) et la copie du dépôt. Quand les deux disent la même chose, le texte est
donné une fois ; sinon les deux versions sont données : le Drive est la saisie la plus récente
(cahier de textes), le dépôt contient les décisions prises avec Claude. Sans accès au Drive, seule
la copie du dépôt est lue et le script le signale.
Puis affiche les passages des fichiers <Niveau>_ChN_Sequence.md qui mentionnent cette date.

Sert de point de départ à Claude (sur l'ordinateur, le téléphone ou dans le cloud) pour rédiger
la trame des cours du jour : voir la section « Trame du jour » du CLAUDE.md.
N'utilise que la bibliothèque standard de Python, pour fonctionner aussi dans une session cloud.

Usage (depuis la racine du dépôt) :
    python3 scripts/trame_du_jour.py              # aujourd'hui (heure de Paris)
    python3 scripts/trame_du_jour.py demain
    python3 scripts/trame_du_jour.py 26/11        # année scolaire en cours
    python3 scripts/trame_du_jour.py 2026-11-26
    python3 scripts/trame_du_jour.py 26/11 --depot   # sans lire le Drive

Changement d'année ou de classeur : voir ANNEE et NIVEAUX dans scripts/progressions.py.
"""
import datetime as dt
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from progressions import JOURS, NIVEAUX, ROOT, charger, format_moment, lire_date, versions  # noqa: E402


def passages_sequence(motif, jour):
    """Sections « ### … » des fichiers de séquence dont le titre contient la date (ex. 26/11)."""
    cle = jour.strftime("%d/%m")
    sorties = []
    for chemin in sorted(glob.glob(os.path.join(ROOT, motif))):
        with open(chemin, encoding="utf-8") as f:
            lignes = f.read().splitlines()
        i = 0
        while i < len(lignes):
            if lignes[i].startswith("### ") and cle in lignes[i]:
                j = i + 1
                while j < len(lignes) and not lignes[j].startswith("#"):
                    j += 1
                sorties.append((os.path.relpath(chemin, ROOT), "\n".join(lignes[i:j]).rstrip()))
                i = j
            else:
                i += 1
    return sorties


def en_ligne(vs, lundi):
    """Versions d'une information de la semaine, sur une ligne."""
    morceaux = []
    for etiquette, texte, depuis in vs:
        suite = f" (depuis la semaine du {depuis.strftime('%d/%m')})" if depuis != lundi else ""
        texte = " / ".join(l.strip() for l in texte.splitlines() if l.strip()) or "(vide)"
        morceaux.append(f"{texte}{suite}" if len(vs) == 1 else f"[{etiquette}] {texte}{suite}")
    return " ; ".join(morceaux)


def main(args):
    lire_drive = "--depot" not in args
    args = [a for a in args if a != "--depot"]
    jour = lire_date(args[0] if args else None)
    nom_jour = JOURS[jour.weekday()]
    lundi = jour - dt.timedelta(days=jour.weekday())
    print(f"# Séances du {nom_jour} {jour.strftime('%d/%m/%Y')}\n")
    for niv in NIVEAUX:
        depot, drive, raison = charger(niv, lire_drive)
        print(f"## {niv['nom']} — semaine du {lundi.strftime('%d/%m')}")
        if drive:
            print(f"Sources : Drive (« {niv['drive']} », modifié le {format_moment(drive.modifie)}) "
                  f"et dépôt ({niv['depot']}).")
        else:
            print(f"Source : dépôt seulement ({niv['depot']}), peut-être en retard sur le Drive. "
                  f"Drive non lu : {raison}.")
        for alerte in depot.alertes + (drive.alertes if drive else []):
            print(f"Attention : {alerte}")
        if depot.ligne(lundi) is None and (drive is None or drive.ligne(lundi) is None):
            print("Semaine absente des classeurs.\n")
            continue
        chapitre = versions(depot, drive, "chapitre", lundi)
        print(f"Chapitre : {en_ligne(chapitre, lundi) if chapitre else '—'}\n")

        seances = [c for c in niv["champs"] if c.jour == nom_jour]
        if not seances:
            print(f"Pas de cours de {niv['nom']} le {nom_jour}.\n")
        for c in seances:
            vs = versions(depot, drive, c.id, lundi)
            if c.id.endswith("_detail") and not any(t for _, t, _ in vs):
                continue
            print(f"### {c.libelle}")
            for etiquette, texte, _ in vs or [("", "", None)]:
                if len(vs) > 1 or drive:
                    print(f"[{etiquette}]")
                print(texte or "(vide)")
            print()

        infos = [(c.libelle, versions(depot, drive, c.id, lundi))
                 for c in niv["champs"] if c.jour is None and c.id != "chapitre"]
        infos = [(lib, vs) for lib, vs in infos if any(t for _, t, _ in vs)]
        if infos:
            print("### Cette semaine")
            for lib, vs in infos:
                print(f"- {lib} : {en_ligne(vs, lundi)}")
            print()
        if seances:
            for fichier, texte in passages_sequence(niv["sequences"], jour):
                print(f"### Extrait de {fichier}\n{texte}\n")


if __name__ == "__main__":
    main(sys.argv[1:])
