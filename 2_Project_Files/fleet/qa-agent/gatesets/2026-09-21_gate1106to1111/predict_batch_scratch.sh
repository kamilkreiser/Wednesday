#!/bin/bash
# predict_batch_scratch.sh — re-derive the six per-PR merged trees and the all-six tree over BOTH develops (778e6cfe2 = the heads' parent,
# cbae988db = origin develop now, the #1105 squash) by REAL 3-way merges (merge-tree --write-tree, chained through scratch commit-trees) in a
# --shared --no-checkout scratch clone under the drafter's scratchpad; git write verbs THERE only — the Secuura checkout is only READ.
# Controls: each head alone over 778e6cfe2 = its head tree (fast-forward); each head alone over cbae988db in BOTH orders; the all-six chain in
# forward, reverse and four other orders over each develop; read-tree back to each develop (GIT_INDEX_FILE in scratch) returns its tree; a
# numstat outside the clone's object dir fails; the all-six tree carries every PR blob and the #1105 blobs.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
S="$1"
BASE=778e6cfe2b6061d60ffcf3a57a951c84dc152b67
DEV=cbae988dbe90ebe556459ada2cb437eaf80e2402
H1=2abc82d11014f00567b75a6b8fab5ec5e78f9df2; H2=7e7da2f88f9ef8dcf571a5720bb7bffcd700aa30; H3=4904c081c4f9be776acef78349bc10384f10de35
H4=f592268af36b282029e50ff2fa1ebe2614304b81; H5=a2a7d7845e75dac2df5c6ad0c4109d5f63394d4c; H6=3d1ea289a0c367af5cd0d060322e46fc900a1c76
C="$(mktemp -d "$S/predict1106.XXXXXX")"
date -u +%Y-%m-%dT%H:%M:%SZ
git clone --quiet --shared --no-checkout "$REPO" "$C/clone"; echo "clone rc=$?"
g() { git -C "$C/clone" "$@"; }
for h in $H1 $H2 $H3 $H4 $H5 $H6; do
  echo "${h:0:9} alone over BASE 778e6cfe2: merge-tree=$(g merge-tree --write-tree $BASE $h) head^{tree}=$(g rev-parse $h^{tree})"
done
for h in $H1 $H2 $H3 $H4 $H5 $H6; do
  a=$(g merge-tree --write-tree $DEV $h); rca=$?; b=$(g merge-tree --write-tree $h $DEV); rcb=$?
  echo "${h:0:9} alone over DEV cbae988db: fwd=$a rc=$rca rev=$b rc=$rcb same=$([ "$a" = "$b" ] && echo True || echo False)"
done
mk() { g commit-tree "$1" -p "$2" -m scratch; }
chain() { # $1 = base commit, $2.. = heads in order
  local base=$1; shift; local cur=$base; local t=''
  for h in "$@"; do t=$(g merge-tree --write-tree $cur $h) || { echo "CONFLICT at $h"; return 1; }; cur=$(mk $t $base); done
  echo "$t"
}
for b in $BASE $DEV; do
  echo "--- all six over ${b:0:9}"
  echo "forward 1..6: $(chain $b $H1 $H2 $H3 $H4 $H5 $H6)"
  echo "reverse 6..1: $(chain $b $H6 $H5 $H4 $H3 $H2 $H1)"
  echo "order 3 6 5 1 4 2: $(chain $b $H3 $H6 $H5 $H1 $H4 $H2)"
  echo "order 2 4 1 6 3 5: $(chain $b $H2 $H4 $H1 $H6 $H3 $H5)"
  echo "order 5 3 4 2 6 1: $(chain $b $H5 $H3 $H4 $H2 $H6 $H1)"
  echo "order 4 1 6 5 2 3: $(chain $b $H4 $H1 $H6 $H5 $H2 $H3)"
  export GIT_INDEX_FILE="$C/idx-${b:0:9}"; g read-tree $b; echo "control read-tree back to ${b:0:9} -> $(g write-tree) == $(g rev-parse $b^{tree})"; unset GIT_INDEX_FILE
done
ALL=$(chain $DEV $H1 $H2 $H3 $H4 $H5 $H6)
echo "--- all-six tree over DEV $ALL vs DEV: numstat (want the 8 PR paths)"; g diff-tree -r --numstat $DEV^{tree} $ALL
echo "count $(g diff-tree -r --name-only $DEV^{tree} $ALL | wc -l | tr -d ' ')"
ok=1
for h in $H1 $H2 $H3 $H4 $H5 $H6; do
  g diff --name-only $BASE $h | while IFS= read -r p; do a=$(g rev-parse "$ALL:$p"); c=$(g rev-parse "$h:$p"); [ "$a" = "$c" ] || echo "MISMATCH $p"; done
done
echo "every PR path in the all-six tree carries its head blob: (no MISMATCH line above = True)"
g diff --name-only $BASE $DEV | while IFS= read -r p; do a=$(g rev-parse "$ALL:$p"); c=$(g rev-parse "$DEV:$p"); [ "$a" = "$c" ] || echo "MISMATCH1105 $p"; done
echo "the 12 #1105 paths in the all-six tree carry develop's blobs: (no MISMATCH1105 line above = True)"
ALLB=$(chain $BASE $H1 $H2 $H3 $H4 $H5 $H6)
echo "--- all-six over BASE $ALLB vs BASE: numstat"; g diff-tree -r --numstat $BASE^{tree} $ALLB
E="$(mktemp -d "$S/empty1106.XXXXXX")"; git -C "$E" init --quiet; git -C "$E" diff-tree -r --numstat $BASE^{tree} $ALLB > /dev/null 2>&1; echo "control: numstat from an empty repo rc=$? (want 128)"
echo "checkout porcelain (read): $(git -C "$REPO" status --porcelain | wc -l | tr -d ' ') | .git/worktrees: $(ls "$REPO/.git/worktrees" | wc -l | tr -d ' ')"
echo "scratch clone at $C (left in the scratchpad, never deleted)"
date -u +%Y-%m-%dT%H:%M:%SZ
