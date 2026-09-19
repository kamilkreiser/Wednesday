#!/bin/bash
# predict_all_seven_scratch.sh — predict the ALL-SEVEN tree for #1077-#1083 over develop f9c28a8b8, IN A SCRATCH CLONE ONLY.
# The Secuura checkout is READ-ONLY: it is only the SOURCE of `git clone --shared --no-checkout` (a read). Every git write verb below
# (merge-tree --write-tree, commit-tree) runs with -C "$C", the fresh scratch clone under the session scratchpad. Nothing is deleted.
# Two merge orders (forward, reverse), each a chain of 3-way merge-tree --write-tree steps committed with commit-tree; both must equal
# the seat's predicted 993718b84, and the seat's local octopus commit 6780f7856's tree (read by rev-parse, a read) must too.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SCRATCH='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f8582263-fac0-44c3-8d2a-6ed1809e5766/scratchpad'
DEV=f9c28a8b82874708edd9de72c40cdb9bfc6ee4cf
WANT=993718b84caa4478989a301331d53740991e6b79
HEADS=(3a549bcf821f0f2e41e6188cf8384ff16329179f c204a830848447ed6571f5c6547991fbe7b89402 de823dcdead32334444024774f6dd8dae8b9726a
       cdff7905d55756ff4d30acaf3cf14e0080d3d209 2f0dfbcbb78f8ba1d99ab2f64c81b1b0334a92b3 c72e3f594f381175c5b4f917ee8b1665517e5f0d
       5f3280e9c09a5315968a48cb57f7166d361a2161)
NUMS=(1077 1078 1079 1080 1081 1082 1083)
echo "predict_all_seven_scratch $(date '+%Y-%m-%d %H:%M:%S %Z') | git $(git --version | cut -d' ' -f3)"
[ -d "${SCRATCH:?}" ] || { echo "scratchpad missing" >&2; exit 2; }
C="$(mktemp -d "${SCRATCH:?}/predict1077-XXXXXX")/clone"
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
F="$(cat "$(dirname "$C")/tree_forward")"; B="$(cat "$(dirname "$C")/tree_reverse")"
S="$(git -C "$REPO" rev-parse --verify -q 6780f7856^{tree})"
echo "ALL SEVEN over develop: forward $F | reverse $B | seat's octopus 6780f7856 tree ${S:-UNREADABLE} | READY 993718b84"
echo "  forward == reverse: $([ "$F" = "$B" ] && echo True || echo False)"
echo "  == READY $WANT: $([ "$F" = "$WANT" ] && echo True || echo False)"
echo "  == seat's 6780f7856 tree: $([ "$F" = "$S" ] && echo True || echo False)"
# union check: the forward tree differs from develop in exactly the eight paths the seven heads change, each at its head blob
n=0; bad=0
while IFS= read -r p; do
  n=$((n+1)); want=""
  for h in "${HEADS[@]}"; do git -C "$C" diff --quiet "$DEV" "$h" -- "$p" || want="$(git -C "$C" rev-parse "$h:$p")"; done
  got="$(git -C "$C" rev-parse "$F:$p")"
  [ "$got" = "$want" ] || { bad=$((bad+1)); echo "  BLOB MISMATCH $p"; }
done < <(git -C "$C" diff --name-only "$DEV" "$F")
echo "  paths changed over develop: $n, each equal to its own head's blob: $([ "$bad" -eq 0 ] && echo True || echo False)"
[ "$F" = "$B" ] && [ "$F" = "$WANT" ] && [ "$F" = "$S" ] && [ "$n" -eq 8 ] && [ "$bad" -eq 0 ] || { echo "PREDICTION DISAGREES"; exit 7; }
echo "PREDICTION OK (scratch clone left in place, never deleted: $C)"
