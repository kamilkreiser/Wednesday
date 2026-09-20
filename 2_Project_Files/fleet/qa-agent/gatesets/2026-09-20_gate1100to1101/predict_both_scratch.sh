#!/bin/bash
# predict_both_scratch.sh — predict the BOTH-PRs tree for #1100 + #1101 over develop e47019878, IN A SCRATCH CLONE ONLY.
# The Secuura checkout is READ-ONLY: it is only the SOURCE of `git clone --shared --no-checkout` (a read). Every git write verb below
# (merge-tree --write-tree, commit-tree, read-tree, update-index, write-tree) runs with -C "$C" / GIT_INDEX_FILE inside the fresh scratch
# clone under the session scratchpad. Nothing is deleted.
# BOTH merge orders (1230-then-1282 and 1282-then-1230), each a chain of 3-way merge-tree --write-tree steps committed with commit-tree, PLUS an
# independent scratch-INDEX composition (no merge machinery). All must equal the seat's claimed 1ccb80e0d.
# Derived from gatesets/2026-09-20_gate1097to1099/predict_all_three_scratch.sh + predict_index_scratch.sh (data changed).
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SCRATCH='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8db19eb7-a2f7-4e99-92e8-a56e13cd7e9c/scratchpad'
DEV=e470198783bcb1ef0eac94780f87579974051423
WANT=1ccb80e0d66ab0ff12d5dbb61753b8c0c274e923
HEADS=(99ce89e741e6c3cad7457af7c91fb6fea86acdff dc40087e756c598ca8b2957da7fbf1ec01945df8)
NUMS=(1100 1101)
echo "predict_both_scratch $(date '+%Y-%m-%d %H:%M:%S %Z') | git $(git --version | cut -d' ' -f3)"
[ -d "${SCRATCH:?}" ] || { echo "scratchpad missing" >&2; exit 2; }
W="$(mktemp -d "${SCRATCH:?}/predict1100-XXXXXX")"; C="$W/clone"
git clone -q --shared --no-checkout "$REPO" "$C"
rc=$?
echo "clone --shared --no-checkout rc $rc -> $C"
[ "$rc" -eq 0 ] || exit 3
for h in "$DEV" "${HEADS[@]}"; do git -C "$C" cat-file -e "$h^{commit}" || { echo "MISSING object $h in the clone" >&2; exit 4; }; done
# control: each head over develop alone is a fast-forward — its merge-tree result IS its own head tree
for i in "${!HEADS[@]}"; do
  h=${HEADS[$i]}
  t="$(git -C "$C" merge-tree --write-tree --merge-base="$DEV" "$DEV" "$h")"; rc=$?
  ht="$(git -C "$C" rev-parse "$h^{tree}")"
  echo "  control #${NUMS[$i]} ${h:0:9}: develop (+) head -> ${t:0:9} == head tree ${ht:0:9}: $([ "$t" = "$ht" ] && echo True || echo False) rc $rc"
  [ "$rc" -eq 0 ] && [ "$t" = "$ht" ] || exit 5
done
chain() {   # $1 label, then the heads in merge order
  local label=$1; shift
  local cur=$DEV t
  for h in "$@"; do
    t="$(git -C "$C" merge-tree --write-tree --merge-base="$DEV" "$cur" "$h")" || { echo "  $label: CONFLICT at ${h:0:9}" >&2; return 1; }
    cur="$(git -C "$C" commit-tree "$t" -p "$cur" -p "$h" -m "scratch predict $label ${h:0:9}")" || return 1
  done
  t="$(git -C "$C" rev-parse "$cur^{tree}")"
  echo "  $label: $# merges -> commit ${cur:0:9} tree $t"
  printf '%s\n' "$t" > "$W/tree_$label"
}
chain 1230then1282 "${HEADS[0]}" "${HEADS[1]}" || exit 6
chain 1282then1230 "${HEADS[1]}" "${HEADS[0]}" || exit 6
F="$(cat "$W/tree_1230then1282")"; B="$(cat "$W/tree_1282then1230")"
compose() {  # $1 index file, then heads — no merge machinery at all
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
  echo "  index control ${h:0:9}: develop index + its delta -> ${t:0:9} == head tree ${ht:0:9}: $([ "$t" = "$ht" ] && echo True || echo False)"
  [ "$t" = "$ht" ] || ok=0
done
T="$(compose "$W/index.both" "${HEADS[@]}")"
# control: read-tree back to develop in the same index context returns develop's tree
GIT_INDEX_FILE="$W/index.back" git -C "$C" read-tree "$DEV" && BACK="$(GIT_INDEX_FILE="$W/index.back" git -C "$C" write-tree)"
DT="$(git -C "$C" rev-parse "$DEV^{tree}")"
echo "BOTH over develop: 1230then1282 $F | 1282then1230 $B | scratch-index $T | READY ${WANT:0:12}"
echo "  1230then1282 == 1282then1230 == index composition: $([ "$F" = "$B" ] && [ "$F" = "$T" ] && echo True || echo False)"
echo "  == the READY's both-PRs tree $WANT: $([ "$F" = "$WANT" ] && echo True || echo False)"
echo "  control: read-tree back to develop -> $BACK == develop tree $DT: $([ "$BACK" = "$DT" ] && echo True || echo False)"
echo "  control: PR1-alone tree $(git -C "$C" rev-parse "${HEADS[0]}^{tree}") differs from the both-PRs tree: $([ "$(git -C "$C" rev-parse "${HEADS[0]}^{tree}")" != "$F" ] && echo True || echo False)"
n=0; bad=0
while IFS= read -r p; do
  n=$((n+1)); want=""
  for h in "${HEADS[@]}"; do git -C "$C" diff --quiet "$DEV" "$h" -- "$p" || want="$(git -C "$C" rev-parse "$h:$p")"; done
  got="$(git -C "$C" rev-parse "$F:$p")"
  echo "    $got ${p##*/}"
  [ "$got" = "$want" ] || { bad=$((bad+1)); echo "  BLOB MISMATCH $p"; }
done < <(git -C "$C" diff --name-only "$DEV" "$F")
echo "  paths changed over develop: $n, each equal to its own head's blob: $([ "$bad" -eq 0 ] && echo True || echo False)"
[ "$F" = "$B" ] && [ "$F" = "$T" ] && [ "$F" = "$WANT" ] && [ "$ok" -eq 1 ] && [ "$BACK" = "$DT" ] && [ "$n" -eq 2 ] && [ "$bad" -eq 0 ] || { echo "PREDICTION DISAGREES"; exit 7; }
echo "PREDICTION OK (scratch clone left in place, never deleted: $C)"
