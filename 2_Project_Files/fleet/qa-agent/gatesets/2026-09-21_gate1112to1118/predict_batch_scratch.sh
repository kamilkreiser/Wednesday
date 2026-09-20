#!/bin/bash
# predict_batch_scratch.sh — re-derive the seven per-PR merged trees over develop 362e51fe0 (each head's parent IS develop, so each is a
# FAST-FORWARD: merge-tree = head tree) and the all-seven tree by REAL 3-way merges (merge-tree --write-tree, chained through scratch
# commit-trees) in a --shared --no-checkout scratch clone under the drafter's scratchpad; git write verbs THERE only — the Secuura checkout is
# only READ. Controls: each head alone over develop = its head tree; the all-seven chain in forward (A B C D E G F = the push order), exact
# reverse and four other orders; read-tree back to develop (GIT_INDEX_FILE in scratch) returns its tree; a numstat outside the clone's object
# dir fails rc 128; the all-seven tree carries every PR blob (11) and nothing else changes vs develop. Derived from gatesets/2026-09-21_gate1106to1111/predict_batch_scratch.sh.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
S="$1"
DEV=362e51fe0db7e73d5557924902763fe3f10fd8c7
HA=3a28d2a3c4d030cb73b7775bb19c5844ce190e56; HB=abf8321a9ca426a1d623a54a41453824dce34def; HC=762a70117c6cf40545f8a4ac5f24708e7fcd91fe
HD=b008489e4fbc72bb8b68cb3bb925557978399780; HE=9a485cfe77406f47103ed6ab65c14ec01144cb68; HG=b3f94f14a0cf3e0236284481b85781417fd233f3
HF=f132c92147b5005c36e405d0116faa541d978a67
SEAT_ALL=6aa9873f974019a92574d6db52e6356734573c8c
C="$(mktemp -d "$S/predict1112.XXXXXX")"
date -u +%Y-%m-%dT%H:%M:%SZ
git clone --quiet --shared --no-checkout "$REPO" "$C/clone"; echo "clone rc=$?"
g() { git -C "$C/clone" "$@"; }
echo "develop tree: $(g rev-parse $DEV^{tree})"
for pair in "A $HA" "B $HB" "C $HC" "D $HD" "E $HE" "G $HG" "F $HF"; do set -- $pair
  a=$(g merge-tree --write-tree $DEV $2); rca=$?; b=$(g merge-tree --write-tree $2 $DEV); rcb=$?; ht=$(g rev-parse $2^{tree})
  echo "PR $1 ${2:0:9} alone over DEV 362e51fe0: fwd=$a rc=$rca rev=$b rc=$rcb head^{tree}=$ht fast-forward(fwd==head tree)=$([ "$a" = "$ht" ] && echo True || echo False) same-both-orders=$([ "$a" = "$b" ] && echo True || echo False)"
done
mk() { g commit-tree "$1" -p "$2" -m scratch; }
chain() { # $1 = base commit, $2.. = heads in order
  local base=$1; shift; local cur=$base; local t=''
  for h in "$@"; do t=$(g merge-tree --write-tree $cur $h) || { echo "CONFLICT at $h"; return 1; }; cur=$(mk $t $base); done
  echo "$t"
}
echo "--- all seven over 362e51fe0 (seat's octopus tree $SEAT_ALL)"
echo "forward A B C D E G F: $(chain $DEV $HA $HB $HC $HD $HE $HG $HF)"
echo "reverse F G E D C B A: $(chain $DEV $HF $HG $HE $HD $HC $HB $HA)"
echo "order C F A G B E D:   $(chain $DEV $HC $HF $HA $HG $HB $HE $HD)"
echo "order E A F B G D C:   $(chain $DEV $HE $HA $HF $HB $HG $HD $HC)"
echo "order B D G C E F A:   $(chain $DEV $HB $HD $HG $HC $HE $HF $HA)"
echo "order G E B F D A C:   $(chain $DEV $HG $HE $HB $HF $HD $HA $HC)"
export GIT_INDEX_FILE="$C/idx-dev"; g read-tree $DEV; echo "control read-tree back to 362e51fe0 -> $(g write-tree) == $(g rev-parse $DEV^{tree})"; unset GIT_INDEX_FILE
ALL=$(chain $DEV $HA $HB $HC $HD $HE $HG $HF)
echo "--- all-seven tree $ALL == seat $SEAT_ALL: $([ "$ALL" = "$SEAT_ALL" ] && echo True || echo False)"
echo "--- all-seven tree vs DEV: numstat (want the 11 PR paths, 0 deletions)"; g diff-tree -r --numstat $DEV^{tree} $ALL
echo "count $(g diff-tree -r --name-only $DEV^{tree} $ALL | wc -l | tr -d ' ') | name-status: $(g diff-tree -r --name-status $DEV^{tree} $ALL | cut -f1 | sort | uniq -c | tr '\n' ' ')"
echo "--- shortstat: $(g diff-tree -r --shortstat $DEV^{tree} $ALL)"
for pair in "A $HA" "B $HB" "C $HC" "D $HD" "E $HE" "G $HG" "F $HF"; do set -- $pair
  g diff --name-only $DEV $2 | while IFS= read -r p; do a=$(g rev-parse "$ALL:$p"); c=$(g rev-parse "$2:$p"); [ "$a" = "$c" ] || echo "MISMATCH PR $1 $p"; done
done
echo "every PR path in the all-seven tree carries its head blob: (no MISMATCH line above = True)"
echo "--- control: each single-PR tree differs from the all-seven tree"
for pair in "A $HA" "B $HB" "C $HC" "D $HD" "E $HE" "G $HG" "F $HF"; do set -- $pair; echo "  PR $1 head tree != ALL: $([ "$(g rev-parse $2^{tree})" != "$ALL" ] && echo True || echo False)"; done
E="$(mktemp -d "$S/empty1112.XXXXXX")"; git -C "$E" init --quiet; git -C "$E" diff-tree -r --numstat $DEV^{tree} $ALL > /dev/null 2>&1; echo "control: numstat from an empty repo rc=$? (want 128)"
echo "checkout porcelain (read): $(git -C "$REPO" status --porcelain | wc -l | tr -d ' ') | .git/worktrees: $(ls "$REPO/.git/worktrees" | wc -l | tr -d ' ') | clone refs: $(g for-each-ref | wc -l | tr -d ' ')"
echo "scratch clone at $C (left in the scratchpad, never deleted)"
date -u +%Y-%m-%dT%H:%M:%SZ
