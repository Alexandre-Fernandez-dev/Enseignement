#!/usr/bin/env bash
# Synchronise les PDF du dépôt vers la clé USB, puis génère les .iwb
# manquants ou périmés avec pdf2iwb.sh.
# Usage : ./sync-cle.sh            (synchronise et convertit)
#         ./sync-cle.sh --dry-run  (montre ce qui serait fait, sans rien écrire)
set -uo pipefail

# --- À adapter ---------------------------------------------------------
SRC="$HOME/chemin/vers/le/depot"                     # dossier du dépôt (ou son sous-dossier de PDF)
CLE="/run/media/$USER/AFERNANDEZ"                    # point de montage de la clé
DST="$CLE/PDF Lycée"                                 # dossier de destination sur la clé
PDF2IWB="$(dirname "$(realpath "$0")")/pdf2iwb.sh"   # pdf2iwb.sh à côté de ce script
# -----------------------------------------------------------------------

DRY=""
[[ "${1:-}" == "--dry-run" ]] && DRY="--dry-run"

if ! mountpoint -q "$CLE"; then
  echo "Clé non branchée ou non montée ($CLE)." >&2
  exit 1
fi
[[ -x "$PDF2IWB" ]] || { echo "Introuvable ou non exécutable : $PDF2IWB" >&2; exit 1; }
# Garde-fou : une source vide ou mal configurée viderait la clé.
if [[ ! -d "$SRC" ]] || [[ -z "$(find "$SRC" -type f -iname '*.pdf' -print -quit)" ]]; then
  echo "Aucun PDF trouvé dans $SRC : arrêt pour ne pas vider la clé." >&2
  exit 1
fi
mkdir -p "$DST"

echo "== Synchronisation des PDF (miroir) =="
# -rt plutôt que -a : une clé FAT/exFAT ne garde ni droits ni propriétaires.
# --modify-window=2 : les dates FAT ont une précision de 2 secondes.
# --delete --delete-excluded : supprime de DST tout ce qui n'est pas un PDF du dépôt...
# --filter='P …' : ...sauf les .iwb (traités plus bas), les .enb créés par le
#   tableau quand on édite un .iwb, et les PDF annotés *_annote.pdf (jamais supprimés).
rsync -rt --modify-window=2 $DRY --itemize-changes \
  --delete --delete-excluded \
  --filter='P *.iwb' --filter='P *.IWB' --filter='P *.enb' --filter='P *.ENB' --filter='P *_annote.pdf' \
  --include='*/' --include='*.pdf' --include='*.PDF' --exclude='*' \
  --prune-empty-dirs \
  "$SRC/" "$DST/" || { echo "Échec de rsync : arrêt." >&2; exit 1; }

echo "== Génération des .iwb manquants ou périmés =="
n_ok=0; n_err=0; n_skip=0
while IFS= read -r -d '' pdf; do
  [[ "$pdf" == *_annote.pdf ]] && continue   # PDF annoté : ni converti, ni supprimé
  iwb="${pdf%.*}.iwb"
  if [[ -f "$iwb" && ! "$pdf" -nt "$iwb" ]]; then
    n_skip=$((n_skip+1)); continue
  fi
  if [[ -n "$DRY" ]]; then
    echo "à convertir : ${pdf#$DST/}"; continue
  fi
  if "$PDF2IWB" "$pdf" >/dev/null; then
    echo "ok : ${iwb#$DST/}"; n_ok=$((n_ok+1))
  else
    echo "ÉCHEC : ${pdf#$DST/}" >&2; n_err=$((n_err+1))
  fi
done < <(find "$DST" -type f -iname '*.pdf' -print0)

echo "== Suppression des .iwb orphelins =="
n_del=0
while IFS= read -r -d '' iwb; do
  base="${iwb%.*}"
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
