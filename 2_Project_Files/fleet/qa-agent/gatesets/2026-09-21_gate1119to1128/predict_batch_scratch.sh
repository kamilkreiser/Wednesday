#!/bin/bash
# predict_batch_scratch.sh — re-derive the ten per-PR merged trees over develop 7be81d5c9 (each head's parent IS develop: FAST-FORWARD, merge-tree
# = head tree) and the all-ten tree by REAL 3-way merges (merge-tree --write-tree chained through scratch commit-trees) in a --shared --no-checkout
# scratch clone under the drafter's scratchpad; git write verbs THERE only — the Secuura checkout is only READ. Controls: each head alone over
# develop = its head tree; the all-ten chain in the push order (B E G F H A D I J C), exact reverse and four other orders; the gateway-lane four
# (D I J C) and the first-eleven-READY seven (B E G F A D C) as sub-trees against the brief's 4ed70356… / 84ef0304…; read-tree back to develop;
# numstat from an empty repo rc 128; the all-ten tree carries every PR blob (13). Derived from gatesets/2026-09-21_gate1112to1118/predict_batch_scratch.sh.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
S="$1"
DEV=7be81d5c9b109959b559e03652fb092c12de58e8
HB=e9e20196f2a91ca57ec6bc6d24087843e2611a08; HE=2a66cd17ec3bd5d91e2fc72c7e3f9102ce1eb839; HG=939de1ba519629cacd22031cbc42dbbb765b4040
HF=9aa5442aeef4d07a3d39e3c3e73e65ef9a42a350; HH=c346999ad3956c02e56fca61f9ad30396ceee2ff; HA=bd907c5538286ee9333e2182d7b388c1007b7163
HD=c50c0a8d402cb6fc585b889c528802fba74c0e40; HI=b23ad259a880ecb207b2ab3cf7e9a1b0b8368dad; HJ=f0cc0aadc1a7856f76cbb69e925e23b94dd05a40
HC=e35b5ddc27dffca5ad1a7cea17b4433484d460ac
SEAT_ALL=23d60cace7c37bc329ccc425e58659e950089a4d
BRIEF_GW4=4ed70356937b5cafb0a6b92decd4209ab7682628
BRIEF_FIRST11=84ef030470037ea14749365c6dbaf7895afc8624
C="$(mktemp -d "$S/predict1119.XXXXXX")"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "checkout count-objects before: $(git -C "$REPO" count-objects -v | tr '\n' ' ')"
git clone --quiet --shared --no-checkout "$REPO" "$C/clone"; echo "clone rc=$?"
g() { git -C "$C/clone" "$@"; }
echo "develop tree: $(g rev-parse $DEV^{tree})"
for pair in "B $HB" "E $HE" "G $HG" "F $HF" "H $HH" "A $HA" "D $HD" "I $HI" "J $HJ" "C $HC"; do set -- $pair
  a=$(g merge-tree --write-tree $DEV $2); rca=$?; b=$(g merge-tree --write-tree $2 $DEV); rcb=$?; ht=$(g rev-parse $2^{tree})
  echo "PR $1 ${2:0:9} alone over DEV 7be81d5c9: fwd=$a rc=$rca rev=$b rc=$rcb head^{tree}=$ht fast-forward(fwd==head tree)=$([ "$a" = "$ht" ] && echo True || echo False) same-both-orders=$([ "$a" = "$b" ] && echo True || echo False)"
done
mk() { g commit-tree "$1" -p "$2" -m scratch; }
chain() { local base=$1; shift; local cur=$base; local t=''
  for h in "$@"; do t=$(g merge-tree --write-tree $cur $h) || { echo "CONFLICT at $h"; return 1; }; cur=$(mk $t $base); done
  echo "$t"; }
echo "--- all ten over 7be81d5c9 (seat's octopus tree $SEAT_ALL)"
echo "forward B E G F H A D I J C: $(chain $DEV $HB $HE $HG $HF $HH $HA $HD $HI $HJ $HC)"
echo "reverse C J I D A H F G E B: $(chain $DEV $HC $HJ $HI $HD $HA $HH $HF $HG $HE $HB)"
echo "order C D I J A B E F G H:   $(chain $DEV $HC $HD $HI $HJ $HA $HB $HE $HF $HG $HH)"
echo "order F G B E H C A J I D:   $(chain $DEV $HF $HG $HB $HE $HH $HC $HA $HJ $HI $HD)"
echo "order I A C E D H J B G F:   $(chain $DEV $HI $HA $HC $HE $HD $HH $HJ $HB $HG $HF)"
echo "order H J F I B D G C E A:   $(chain $DEV $HH $HJ $HF $HI $HB $HD $HG $HC $HE $HA)"
GW=$(chain $DEV $HD $HI $HJ $HC); GW2=$(chain $DEV $HC $HJ $HI $HD)
echo "--- gateway lane four (D I J C): $GW | reverse $GW2 | == brief's six-patch tree $BRIEF_GW4: $([ "$GW" = "$BRIEF_GW4" ] && [ "$GW2" = "$BRIEF_GW4" ] && echo True || echo False)"
F11=$(chain $DEV $HB $HE $HG $HF $HA $HD $HC); F11r=$(chain $DEV $HC $HD $HA $HF $HG $HE $HB)
echo "--- first-eleven-READY seven (B E G F A D C): $F11 | reverse $F11r | == brief's $BRIEF_FIRST11: $([ "$F11" = "$BRIEF_FIRST11" ] && [ "$F11r" = "$BRIEF_FIRST11" ] && echo True || echo False)"
export GIT_INDEX_FILE="$C/idx-dev"; g read-tree $DEV; echo "control read-tree back to 7be81d5c9 -> $(g write-tree) == $(g rev-parse $DEV^{tree})"; unset GIT_INDEX_FILE
ALL=$(chain $DEV $HB $HE $HG $HF $HH $HA $HD $HI $HJ $HC)
echo "--- all-ten tree $ALL == seat $SEAT_ALL: $([ "$ALL" = "$SEAT_ALL" ] && echo True || echo False)"
echo "--- all-ten tree vs DEV: numstat (want the 13 PR paths, +508/-1)"; g diff-tree -r --numstat $DEV^{tree} $ALL
echo "count $(g diff-tree -r --name-only $DEV^{tree} $ALL | wc -l | tr -d ' ') | name-status: $(g diff-tree -r --name-status $DEV^{tree} $ALL | cut -f1 | sort | uniq -c | tr '\n' ' ')"
echo "--- shortstat: $(g diff-tree -r --shortstat $DEV^{tree} $ALL)"
for pair in "B $HB" "E $HE" "G $HG" "F $HF" "H $HH" "A $HA" "D $HD" "I $HI" "J $HJ" "C $HC"; do set -- $pair
  g diff --name-only $DEV $2 | while IFS= read -r p; do a=$(g rev-parse "$ALL:$p"); c=$(g rev-parse "$2:$p"); [ "$a" = "$c" ] || echo "MISMATCH PR $1 $p"; done
done
echo "every PR path in the all-ten tree carries its head blob: (no MISMATCH line above = True)"
echo "--- control: each single-PR tree differs from the all-ten tree"
for pair in "B $HB" "E $HE" "G $HG" "F $HF" "H $HH" "A $HA" "D $HD" "I $HI" "J $HJ" "C $HC"; do set -- $pair; echo "  PR $1 head tree != ALL: $([ "$(g rev-parse $2^{tree})" != "$ALL" ] && echo True || echo False)"; done
E="$(mktemp -d "$S/empty1119.XXXXXX")"; git -C "$E" init --quiet; git -C "$E" diff-tree -r --numstat $DEV^{tree} $ALL > /dev/null 2>&1; echo "control: numstat from an empty repo rc=$? (want 128)"
echo "checkout porcelain non-untracked (read): $(git -C "$REPO" status --porcelain | grep -c -v '^??') | porcelain total $(git -C "$REPO" status --porcelain | wc -l | tr -d ' ') | .git/worktrees: $(ls "$REPO/.git/worktrees" | wc -l | tr -d ' ') | for-each-ref: $(git -C "$REPO" for-each-ref | wc -l | tr -d ' ')"
echo "checkout count-objects after: $(git -C "$REPO" count-objects -v | tr '\n' ' ')"
echo "scratch clone at $C (left in the scratchpad, never deleted)"
date -u +%Y-%m-%dT%H:%M:%SZ
