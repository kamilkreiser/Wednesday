#!/bin/bash
# predict_all_three_scratch.sh — predict the ALL-THREE tree for #1097-#1099 over develop c87458bdd, IN A SCRATCH CLONE ONLY.
# The Secuura checkout is READ-ONLY: it is only the SOURCE of `git clone --shared --no-checkout` (a read). Every git write verb below
# (merge-tree --write-tree, commit-tree) runs with -C "$C", the fresh scratch clone under the session scratchpad. Nothing is deleted.
# THREE merge orders (forward, reverse, and tier-1-first: #1099, #1098, #1097), each a chain of 3-way merge-tree --write-tree steps committed
# with commit-tree; all must equal the seat's predicted 706de8305, and the seat's local octopus commit f893a92cf's tree (read by rev-parse, a
# read) must too. Derived from gatesets/2026-09-20_gate1092to1096/predict_all_five_scratch.sh (data changed).
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SCRATCH='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fd1ce61d-09bc-4b11-b5ed-43cb67420198/scratchpad'
DEV=c87458bdd8a9dd5ae3a082612e467cda5539aebc
WANT=706de83052728ddfe4c581e378f708fec2338b80
OCTO=f893a92cf105a4faaacb7c48b647efe3e8fedbec
HEADS=(f5364217952c1cb4d3755fbf8604b3edde124c42 efce14bed4a8adda15bca124fa60ae7d894fa6a6 b68aaf9b4581e67369be33d8ebcf4d61886c039b)
NUMS=(1097 1098 1099)
echo "predict_all_three_scratch $(date '+%Y-%m-%d %H:%M:%S %Z') | git $(git --version | cut -d' ' -f3)"
[ -d "${SCRATCH:?}" ] || { echo "scratchpad missing" >&2; exit 2; }
C="$(mktemp -d "${SCRATCH:?}/predict1097-XXXXXX")/clone"
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
  echo "  $label: ${#@} merges -> commit ${cur:0:9} tree $t"
  printf '%s\n' "$t" > "$(dirname "$C")/tree_$label"
}
chain forward "${HEADS[@]}" || exit 6
chain reverse "${HEADS[2]}" "${HEADS[1]}" "${HEADS[0]}" || exit 6
# the third order: #1099 (tier 1) first, then #1097, then #1098
chain tier1first "${HEADS[2]}" "${HEADS[0]}" "${HEADS[1]}" || exit 6
F="$(cat "$(dirname "$C")/tree_forward")"; B="$(cat "$(dirname "$C")/tree_reverse")"; X="$(cat "$(dirname "$C")/tree_tier1first")"
S="$(git -C "$REPO" rev-parse --verify -q "$OCTO^{tree}")"
NP="$(git -C "$REPO" rev-list --parents -n 1 "$OCTO" | wc -w | tr -d ' ')"
FP="$(git -C "$REPO" rev-parse --verify -q "$OCTO^1")"
echo "ALL THREE over develop: forward $F | reverse $B | tier1first $X | seat's octopus ${OCTO:0:9} tree ${S:-UNREADABLE} (words in rev-list --parents: $NP = 1 + 4 parents; first parent ${FP:0:9}) | READY ${WANT:0:9}"
echo "  forward == reverse == tier1first: $([ "$F" = "$B" ] && [ "$F" = "$X" ] && echo True || echo False)"
echo "  == READY $WANT: $([ "$F" = "$WANT" ] && echo True || echo False)"
echo "  == seat's octopus tree: $([ "$F" = "$S" ] && echo True || echo False)"
echo "  octopus first parent == develop: $([ "$FP" = "$DEV" ] && echo True || echo False)"
n=0; bad=0
while IFS= read -r p; do
  n=$((n+1)); want=""
  for h in "${HEADS[@]}"; do git -C "$C" diff --quiet "$DEV" "$h" -- "$p" || want="$(git -C "$C" rev-parse "$h:$p")"; done
  got="$(git -C "$C" rev-parse "$F:$p")"
  echo "    $got ${p##*/}"
  [ "$got" = "$want" ] || { bad=$((bad+1)); echo "  BLOB MISMATCH $p"; }
done < <(git -C "$C" diff --name-only "$DEV" "$F")
echo "  paths changed over develop: $n, each equal to its own head's blob: $([ "$bad" -eq 0 ] && echo True || echo False)"
[ "$F" = "$B" ] && [ "$F" = "$X" ] && [ "$F" = "$WANT" ] && [ "$F" = "$S" ] && [ "$FP" = "$DEV" ] && [ "$NP" -eq 5 ] && [ "$n" -eq 3 ] && [ "$bad" -eq 0 ] || { echo "PREDICTION DISAGREES"; exit 7; }
echo "PREDICTION OK (scratch clone left in place, never deleted: $C)"
