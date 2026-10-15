#!/usr/bin/env bash
# Synchronise les PDF du dépôt vers la clé USB, puis génère les .iwb
# manquants ou périmés avec pdf2iwb.sh.
# Usage : scripts/sync-cle.sh            (synchronise et convertit)
#         scripts/sync-cle.sh --dry-run  (montre ce qui serait fait, sans rien écrire)
set -uo pipefail

# --- Configuration -----------------------------------------------------
# Sous-dossiers identiques à ceux de la synchro Drive (.git/hooks/post-commit).
SCRIPTS="$(dirname "$(realpath "$0")")"
ROOT="$(realpath "$SCRIPTS/..")"                     # racine du dépôt
ANNEE="2026-2027"                                    # année en cours
SRC="$ROOT/$ANNEE"                                   # PDF de l'année en cours
CLE="/run/media/$USER/AFERNANDEZ"                    # point de montage de la clé
DST="$CLE/PDF Lycée"                                 # dossier de destination sur la clé
PDF2IWB="$SCRIPTS/pdf2iwb.sh"                        # pdf2iwb.sh à côté de ce script
# Les documents personnels (plans de classe, listes) vont dans $CLE/Documents,
# hors de DST : le miroir n'y touche pas.
# -----------------------------------------------------------------------

DRY=""
[[ "${1:-}" == "--dry-run" ]] && DRY="--dry-run"

if ! mountpoint -q "$CLE"; then
  echo "Clé non branchée ou non montée ($CLE)." >&2
  exit 1
fi
[[ -x "$PDF2IWB" ]] || { echo "Introuvable ou non exécutable : $PDF2IWB" >&2; exit 1; }
git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1 \
  || { echo "$ROOT n'est pas un dépôt git : arrêt." >&2; exit 1; }
# Garde-fou : une source vide ou mal configurée viderait la clé.
if [[ ! -d "$SRC" ]] || [[ -z "$(find "$SRC" -type f -iname '*.pdf' -print -quit)" ]]; then
  echo "Aucun PDF trouvé dans $SRC : arrêt pour ne pas vider la clé." >&2
  exit 1
fi
# Seul DST est accessible en écriture sur la clé : on ne le crée pas.
[[ -d "$DST" && -w "$DST" ]] || { echo "Dossier absent ou protégé en écriture : $DST" >&2; exit 1; }

echo "== Synchronisation des PDF (miroir) =="
# -rt plutôt que -a : une clé FAT/exFAT ne garde ni droits ni propriétaires.
# --modify-window=2 : les dates FAT ont une précision de 2 secondes.
# --delete --delete-excluded : supprime de DST tout ce qui n'est pas un PDF du dépôt...
# --filter='P …' : ...sauf les .iwb (traités plus bas), les .enb créés par le
#   tableau quand on édite un .iwb, et les PDF annotés *_Annote.pdf (jamais supprimés).
rsync -rt --modify-window=2 $DRY --itemize-changes \
  --delete --delete-excluded \
  --filter='P *.iwb' --filter='P *.IWB' --filter='P *.enb' --filter='P *.ENB' \
  --filter='P *_[Aa]nnote.pdf' --filter='P *_[Aa]nnote.PDF' \
  --include='*/' --include='*.pdf' --include='*.PDF' --exclude='*' \
  --prune-empty-dirs \
  "$SRC/" "$DST/" || { echo "Échec de rsync : arrêt." >&2; exit 1; }

# Les deux boucles suivantes partent des PDF du dépôt (SRC) et non de ceux de la clé :
# après le miroir c'est équivalent, et en --dry-run cela compte aussi les PDF pas
# encore copiés. rsync -t conserve les dates, d'où la comparaison avec le PDF source.
# Chaque .iwb reçoit la date de son PDF : il est à jour si les deux dates sont égales
# (à 2 s près, précision FAT), que le PDF ait changé pour une date plus récente ou plus
# ancienne.
echo "== Génération des .iwb manquants ou périmés =="
n_ok=0; n_err=0; n_skip=0
while IFS= read -r -d '' src; do
  rel="${src#$SRC/}"
  [[ "$rel" == *_[Aa]nnote.[Pp][Dd][Ff] ]] && continue   # PDF annoté : ni converti, ni supprimé
  pdf="$DST/$rel"
  iwb="${pdf%.*}.iwb"
  if [[ -f "$iwb" ]]; then
    ecart=$(( $(stat -c %Y "$src") - $(stat -c %Y "$iwb") ))
    if (( ecart >= -2 && ecart <= 2 )); then
      n_skip=$((n_skip+1)); continue
    fi
  fi
  if [[ -n "$DRY" ]]; then
    echo "à convertir : $rel"; continue
  fi
  if "$PDF2IWB" "$pdf" >/dev/null && touch -r "$pdf" "$iwb"; then
    echo "ok : ${iwb#$DST/}"; n_ok=$((n_ok+1))
  else
    echo "ÉCHEC : $rel" >&2; n_err=$((n_err+1))
  fi
done < <(find "$SRC" -type f -iname '*.pdf' -print0)

echo "== Suppression des .iwb orphelins =="
n_del=0
while IFS= read -r -d '' iwb; do
  base="$SRC/${iwb#$DST/}"; base="${base%.*}"
  [[ -f "$base.pdf" || -f "$base.PDF" ]] && continue
  if [[ -n "$DRY" ]]; then
    echo "à supprimer : ${iwb#$DST/}"
  else
    rm -f -- "$iwb" && echo "supprimé : ${iwb#$DST/}"
  fi
  n_del=$((n_del+1))
done < <(find "$DST" -type f -iname '*.iwb' -print0)
[[ -z "$DRY" ]] && find "$DST" -mindepth 1 -type d -empty -delete

echo "== Écriture sur la clé =="
sync
echo "Convertis : $n_ok · déjà à jour : $n_skip · échecs : $n_err · iwb orphelins : $n_del"
echo "Vous pouvez retirer la clé."
