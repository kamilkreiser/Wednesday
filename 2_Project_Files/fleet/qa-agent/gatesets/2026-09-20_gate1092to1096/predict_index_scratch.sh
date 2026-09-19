#!/bin/bash
# predict_index_scratch.sh — a THIRD independent prediction of the ALL-FIVE tree for #1092-#1096: scratch-INDEX composition in a fresh
# `git clone --shared --no-checkout` under the session scratchpad (the Secuura checkout is only the clone SOURCE, a read). A temp GIT_INDEX_FILE
# inside the scratch dir: read-tree develop, then update-index --cacheinfo of each PR path at its head blob/mode (read from `git diff --raw`),
# then write-tree. No merge machinery at all. Control: each head alone composed the same way = its head tree. Nothing is deleted.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SCRATCH='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/e756a2de-6a98-48d1-a280-ca95596a3651/scratchpad'
DEV=4273adfac57ab1a65b4a9983c566cc115faefc01
WANT=458cff7174a2c9090a14c9d5ed71e3a17c3792e4
HEADS=(d1c35a0c3b29383411c5f697f535293a99482de6 b6c29f87b8c2d3956ac1b89bfe338940e109a805 655b83efd6f4948b5e973afdbcd21456dc7f1661
       b62df66454c2f4a73c77a2168fabf7e16b3290d2 789e6b984c1540785c8249cb2b269e5ab63c6909)
echo "predict_index_scratch $(date '+%Y-%m-%d %H:%M:%S %Z') | git $(git --version | cut -d' ' -f3)"
W="$(mktemp -d "${SCRATCH:?}/idx1092-XXXXXX")"; C="$W/clone"
git clone -q --shared --no-checkout "$REPO" "$C" || exit 3
compose() {  # $1 index file, then heads
  local ix=$1; shift
  GIT_INDEX_FILE="$ix" git -C "$C" read-tree "$DEV" || return 1
  for h in "$@"; do
    while IFS=$'\t' read -r meta path; do
      set -- $meta; mode=${2}; blob=${4}; st=${5}
      [ "$st" = "M" ] || { echo "unexpected status $st for $path" >&2; return 1; }
      GIT_INDEX_FILE="$ix" git -C "$C" update-index --cacheinfo "$mode,$blob,$path" || return 1
    done < <(git -C "$C" diff --raw --no-abbrev "$DEV" "$h")
  done
  GIT_INDEX_FILE="$ix" git -C "$C" write-tree
}
i=0; ok=1
for h in "${HEADS[@]}"; do
  i=$((i+1)); t="$(compose "$W/index.single$i" "$h")"; ht="$(git -C "$C" rev-parse "$h^{tree}")"
  echo "  control ${h:0:9}: develop index + its delta -> ${t:0:9} == head tree ${ht:0:9}: $([ "$t" = "$ht" ] && echo True || echo False)"
  [ "$t" = "$ht" ] || ok=0
done
T="$(compose "$W/index.all" "${HEADS[@]}")"
echo "ALL FIVE by scratch-index composition: $T | READY ${WANT:0:12}: $([ "$T" = "$WANT" ] && echo True || echo False)"
[ "$ok" -eq 1 ] && [ "$T" = "$WANT" ] || { echo "PREDICTION DISAGREES"; exit 7; }
echo "PREDICTION OK (scratch dir left in place, never deleted: $W)"
