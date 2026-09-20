#!/bin/bash
# predict_batch_scratch.sh — re-derive the all-three tree in a --shared --no-checkout scratch clone (scratchpad only; the Secuura checkout is only READ):
# chained 3-way merge-tree --write-tree in ALL SIX orders; each head alone controlled = its head tree; PR1+PR2 both orders; read-tree back to develop.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
S="$1"
DEV=dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa
H1=f5a599b077667a1fdda602744092d866df03c3fa
H2=47593b77b80a295b4113da8acf850b5c8b03fd7e
H3=9b668edba63e1328ab113058b47953a11d2a3ed6
C="$(mktemp -d "$S/predict.XXXXXX")"
date -u +%Y-%m-%dT%H:%M:%SZ
git clone --quiet --shared --no-checkout "$REPO" "$C/clone"; echo "clone rc=$?"
g() { git -C "$C/clone" "$@"; }
for h in $H1 $H2 $H3; do echo "$h alone over develop: merge-tree=$(g merge-tree --write-tree $DEV $h) head^{tree}=$(g rev-parse $h^{tree})"; done
# chained: merge B onto (A merged), then C onto that; a merged TREE needs a commit to chain, so commit-tree in the scratch clone
mk() { echo "$(g commit-tree "$1" -p $DEV -m scratch)"; }
declare -a ORD=("$H1 $H2 $H3" "$H1 $H3 $H2" "$H2 $H1 $H3" "$H2 $H3 $H1" "$H3 $H1 $H2" "$H3 $H2 $H1")
for o in "${ORD[@]}"; do
  set -- $o
  t1=$(g merge-tree --write-tree $DEV $1); c1=$(mk $t1)
  t2=$(g merge-tree --write-tree $c1 $2); c2=$(mk $t2)
  t3=$(g merge-tree --write-tree $c2 $3)
  echo "order ${1:0:9} ${2:0:9} ${3:0:9}: $t3"
done
echo "PR1+PR2 1->2: $(g merge-tree --write-tree $(mk $(g merge-tree --write-tree $DEV $H1)) $H2)"
echo "PR1+PR2 2->1: $(g merge-tree --write-tree $(mk $(g merge-tree --write-tree $DEV $H2)) $H1)"
echo "control read-tree back to develop: $(g read-tree $DEV && g write-tree)"
echo "batch tree ls (4 paths expected):"; g diff-tree -r --numstat $DEV "$(g merge-tree --write-tree $(mk $(g merge-tree --write-tree $(mk $(g merge-tree --write-tree $DEV $H1)) $H2)) $H3)"
echo "scratch clone at $C (left in the scratchpad, never deleted)"
