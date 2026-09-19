#!/bin/bash
# predict_all_seven_scratch.sh — predict the ALL-SEVEN tree for #1070-#1076 over develop 51dbedd39, IN A SCRATCH CLONE ONLY.
# The Secuura checkout is READ-ONLY: it is only the SOURCE of `git clone --shared --no-checkout` (a read). Every git write verb below
# (merge-tree --write-tree, commit-tree) runs with -C "$C", the fresh scratch clone under the session scratchpad. Nothing is deleted.
# Two merge orders (forward, reverse), each a chain of 3-way merge-tree --write-tree steps committed with commit-tree; both must equal
# the seat's predicted bc4d0ed7f, and the seat's local octopus commit 29bc11a08's tree (read by rev-parse, a read) must too.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SCRATCH='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f8582263-fac0-44c3-8d2a-6ed1809e5766/scratchpad'
DEV=51dbedd39ade43cc511278502b2e1e190de641c7
WANT=bc4d0ed7fccc3bb9f594bd18565c9a5e47ab9db4
HEADS=(59af03cbab07bfcd151206d732d3aa989ac0256c dc0bf93159a981d695d4fcdff9329003e1c26d99 cb8c0b18616b29eea77ef6efac0e3fac90178671
       085205d444f6045c5ccc1c45f741aa252beae764 6be54e11b263f9881c7b410ae17613134c577fb7 3ec034083716f104eccfc50e2734ab16082e1e72
       aff1568f387b5073f31dcb99519cafeda7cc66bc)
NUMS=(1070 1071 1072 1073 1074 1075 1076)
echo "predict_all_seven_scratch $(date '+%Y-%m-%d %H:%M:%S %Z') | git $(git --version | cut -d' ' -f3)"
[ -d "${SCRATCH:?}" ] || { echo "scratchpad missing" >&2; exit 2; }
C="$(mktemp -d "${SCRATCH:?}/predict1070-XXXXXX")/clone"
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
S="$(git -C "$REPO" rev-parse --verify -q 29bc11a08^{tree})"
echo "ALL SEVEN over develop: forward $F | reverse $B | seat's octopus 29bc11a08 tree ${S:-UNREADABLE} | READY bc4d0ed7f"
echo "  forward == reverse: $([ "$F" = "$B" ] && echo True || echo False)"
echo "  == READY $WANT: $([ "$F" = "$WANT" ] && echo True || echo False)"
echo "  == seat's 29bc11a08 tree: $([ "$F" = "$S" ] && echo True || echo False)"
# union check: the forward tree differs from develop in exactly the ten paths the seven heads change, each at its head blob
n=0; bad=0
while IFS= read -r p; do
  n=$((n+1)); want=""
  for h in "${HEADS[@]}"; do git -C "$C" diff --quiet "$DEV" "$h" -- "$p" || want="$(git -C "$C" rev-parse "$h:$p")"; done
  got="$(git -C "$C" rev-parse "$F:$p")"
  [ "$got" = "$want" ] || { bad=$((bad+1)); echo "  BLOB MISMATCH $p"; }
done < <(git -C "$C" diff --name-only "$DEV" "$F")
echo "  paths changed over develop: $n, each equal to its own head's blob: $([ "$bad" -eq 0 ] && echo True || echo False)"
[ "$F" = "$B" ] && [ "$F" = "$WANT" ] && [ "$F" = "$S" ] && [ "$n" -eq 10 ] && [ "$bad" -eq 0 ] || { echo "PREDICTION DISAGREES"; exit 7; }
echo "PREDICTION OK (scratch clone left in place, never deleted: $C)"
