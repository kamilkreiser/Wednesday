#!/bin/bash
# predict_all_five_scratch.sh — predict the ALL-FIVE tree for #1092-#1096 over develop 4273adfac, IN A SCRATCH CLONE ONLY.
# The Secuura checkout is READ-ONLY: it is only the SOURCE of `git clone --shared --no-checkout` (a read). Every git write verb below
# (merge-tree --write-tree, commit-tree) runs with -C "$C", the fresh scratch clone under the session scratchpad. Nothing is deleted.
# THREE merge orders (forward, reverse, and a shuffled order with the two tier-1 heads FIRST), each a chain of 3-way merge-tree --write-tree
# steps committed with commit-tree; all must equal the seat's predicted 458cff717, and the seat's local octopus commit 4a1fa96a5's tree (read by
# rev-parse, a read) must too. Derived from gatesets/2026-09-19_gate1084to1091/predict_all_eight_scratch.sh (data changed).
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SCRATCH='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/e756a2de-6a98-48d1-a280-ca95596a3651/scratchpad'
DEV=4273adfac57ab1a65b4a9983c566cc115faefc01
WANT=458cff7174a2c9090a14c9d5ed71e3a17c3792e4
OCTO=4a1fa96a5fe9240e3f5f26b07b3382fd1eccc92b
HEADS=(d1c35a0c3b29383411c5f697f535293a99482de6 b6c29f87b8c2d3956ac1b89bfe338940e109a805 655b83efd6f4948b5e973afdbcd21456dc7f1661
       b62df66454c2f4a73c77a2168fabf7e16b3290d2 789e6b984c1540785c8249cb2b269e5ab63c6909)
NUMS=(1092 1093 1094 1095 1096)
echo "predict_all_five_scratch $(date '+%Y-%m-%d %H:%M:%S %Z') | git $(git --version | cut -d' ' -f3)"
[ -d "${SCRATCH:?}" ] || { echo "scratchpad missing" >&2; exit 2; }
C="$(mktemp -d "${SCRATCH:?}/predict1092-XXXXXX")/clone"
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
REV=(); for (( i=${#HEADS[@]}-1; i>=0; i-- )); do REV+=("${HEADS[$i]}"); done
chain reverse "${REV[@]}" || exit 6
# shuffled: #1096, #1095 (tier 1) first, then #1093, #1092, #1094
SHUF=("${HEADS[4]}" "${HEADS[3]}" "${HEADS[1]}" "${HEADS[0]}" "${HEADS[2]}")
chain shuffled "${SHUF[@]}" || exit 6
F="$(cat "$(dirname "$C")/tree_forward")"; B="$(cat "$(dirname "$C")/tree_reverse")"; X="$(cat "$(dirname "$C")/tree_shuffled")"
S="$(git -C "$REPO" rev-parse --verify -q "$OCTO^{tree}")"
NP="$(git -C "$REPO" rev-list --parents -n 1 "$OCTO" | wc -w | tr -d ' ')"
FP="$(git -C "$REPO" rev-parse --verify -q "$OCTO^1")"
echo "ALL FIVE over develop: forward $F | reverse $B | shuffled $X | seat's octopus ${OCTO:0:9} tree ${S:-UNREADABLE} (words in rev-list --parents: $NP = 1 + 6 parents; first parent ${FP:0:9}) | READY ${WANT:0:9}"
echo "  forward == reverse == shuffled: $([ "$F" = "$B" ] && [ "$F" = "$X" ] && echo True || echo False)"
echo "  == READY $WANT: $([ "$F" = "$WANT" ] && echo True || echo False)"
echo "  == seat's octopus tree: $([ "$F" = "$S" ] && echo True || echo False)"
echo "  octopus first parent == develop: $([ "$FP" = "$DEV" ] && echo True || echo False)"
# union check: the forward tree differs from develop in exactly the five paths the five heads change, each at its head blob
n=0; bad=0
while IFS= read -r p; do
  n=$((n+1)); want=""
  for h in "${HEADS[@]}"; do git -C "$C" diff --quiet "$DEV" "$h" -- "$p" || want="$(git -C "$C" rev-parse "$h:$p")"; done
  got="$(git -C "$C" rev-parse "$F:$p")"
  [ "$got" = "$want" ] || { bad=$((bad+1)); echo "  BLOB MISMATCH $p"; }
done < <(git -C "$C" diff --name-only "$DEV" "$F")
echo "  paths changed over develop: $n, each equal to its own head's blob: $([ "$bad" -eq 0 ] && echo True || echo False)"
[ "$F" = "$B" ] && [ "$F" = "$X" ] && [ "$F" = "$WANT" ] && [ "$F" = "$S" ] && [ "$FP" = "$DEV" ] && [ "$n" -eq 5 ] && [ "$bad" -eq 0 ] || { echo "PREDICTION DISAGREES"; exit 7; }
echo "PREDICTION OK (scratch clone left in place, never deleted: $C)"
