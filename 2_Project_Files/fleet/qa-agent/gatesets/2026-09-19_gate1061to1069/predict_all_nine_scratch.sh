#!/bin/bash
# predict_all_nine_scratch.sh — predict the ALL-NINE tree for #1061-#1069 over develop 3c447abc7, IN A SCRATCH CLONE ONLY.
# The Secuura checkout is READ-ONLY: it is only the SOURCE of `git clone --shared --no-checkout` (a read). Every git write verb below
# (merge-tree --write-tree, commit-tree) runs with -C "$C", the fresh scratch clone under the session scratchpad. Nothing is deleted.
# Two merge orders (forward, reverse), each a chain of 3-way merge-tree --write-tree steps committed with commit-tree; both must equal
# the seat's predicted 275cff9ff, and the seat's local octopus commit 77b7af584's tree (read by rev-parse, a read) must too.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SCRATCH='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f8582263-fac0-44c3-8d2a-6ed1809e5766/scratchpad'
DEV=3c447abc7714e98fbba596aa1045b7bb47a6d215
WANT=275cff9ffcb1a8204db499506f08db54ee39f4eb
HEADS=(413cc5e80c8aab94c9b3058fbe0d49fbcfdaa540 b9497c69837d33d3c56562abfb9f9ac5c0dafa2b cd0a88e41ada8ddd927c3dc85f8270b52142f834
       7fd0f7d1e560d85c789872eac96067b428215ed5 3b46e2e14a2783bfe03df8919ca79d2dea21c043 0c649c09bca81ccb41ba791bb2a85ba29476c052
       48a8e12bbb6b01d34bea55ab29936b033f8304b3 9af88d99dbc0203a69cb765c67dee10df900e737 34406a29babe355a7ea8ecd916062da5b2fa8f85)
NUMS=(1061 1062 1063 1064 1065 1066 1067 1068 1069)
echo "predict_all_nine_scratch $(date '+%Y-%m-%d %H:%M:%S %Z') | git $(git --version | cut -d' ' -f3)"
[ -d "${SCRATCH:?}" ] || { echo "scratchpad missing" >&2; exit 2; }
C="$(mktemp -d "${SCRATCH:?}/predict1061-XXXXXX")/clone"
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
S="$(git -C "$REPO" rev-parse --verify -q 77b7af584^{tree})"
echo "ALL NINE over develop: forward $F | reverse $B | seat's octopus 77b7af584 tree ${S:-UNREADABLE} | READY 275cff9ff"
echo "  forward == reverse: $([ "$F" = "$B" ] && echo True || echo False)"
echo "  == READY $WANT: $([ "$F" = "$WANT" ] && echo True || echo False)"
echo "  == seat's 77b7af584 tree: $([ "$F" = "$S" ] && echo True || echo False)"
# union check: the forward tree differs from develop in exactly the eleven paths the nine heads change, each at its head blob
n=0; bad=0
while IFS= read -r p; do
  n=$((n+1)); want=""
  for h in "${HEADS[@]}"; do git -C "$C" diff --quiet "$DEV" "$h" -- "$p" || want="$(git -C "$C" rev-parse "$h:$p")"; done
  got="$(git -C "$C" rev-parse "$F:$p")"
  [ "$got" = "$want" ] || { bad=$((bad+1)); echo "  BLOB MISMATCH $p"; }
done < <(git -C "$C" diff --name-only "$DEV" "$F")
echo "  paths changed over develop: $n, each equal to its own head's blob: $([ "$bad" -eq 0 ] && echo True || echo False)"
[ "$F" = "$B" ] && [ "$F" = "$WANT" ] && [ "$F" = "$S" ] && [ "$n" -eq 11 ] && [ "$bad" -eq 0 ] || { echo "PREDICTION DISAGREES"; exit 7; }
echo "PREDICTION OK (scratch clone left in place, never deleted: $C)"
