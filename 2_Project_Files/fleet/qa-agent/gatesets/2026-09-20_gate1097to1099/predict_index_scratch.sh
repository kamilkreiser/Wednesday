#!/bin/bash
# predict_index_scratch.sh — an independent prediction of the ALL-THREE tree for #1097-#1099: scratch-INDEX composition in a fresh
# `git clone --shared --no-checkout` under the session scratchpad (the Secuura checkout is only the clone SOURCE, a read). A temp GIT_INDEX_FILE
# inside the scratch dir: read-tree develop, then update-index --cacheinfo of each PR path at its head blob/mode (read from `git diff --raw`),
# then write-tree. No merge machinery at all. Control: each head alone composed the same way = its head tree. Nothing is deleted.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SCRATCH='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fd1ce61d-09bc-4b11-b5ed-43cb67420198/scratchpad'
DEV=c87458bdd8a9dd5ae3a082612e467cda5539aebc
WANT=706de83052728ddfe4c581e378f708fec2338b80
HEADS=(f5364217952c1cb4d3755fbf8604b3edde124c42 efce14bed4a8adda15bca124fa60ae7d894fa6a6 b68aaf9b4581e67369be33d8ebcf4d61886c039b)
echo "predict_index_scratch $(date '+%Y-%m-%d %H:%M:%S %Z') | git $(git --version | cut -d' ' -f3)"
W="$(mktemp -d "${SCRATCH:?}/idx1097-XXXXXX")"; C="$W/clone"
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
echo "ALL THREE by scratch-index composition: $T | READY ${WANT:0:12}: $([ "$T" = "$WANT" ] && echo True || echo False)"
[ "$ok" -eq 1 ] && [ "$T" = "$WANT" ] || { echo "PREDICTION DISAGREES"; exit 7; }
echo "PREDICTION OK (scratch dir left in place, never deleted: $W)"
