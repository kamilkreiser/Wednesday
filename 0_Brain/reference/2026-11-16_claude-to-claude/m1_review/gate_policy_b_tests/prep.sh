#!/bin/bash
# QA-POLICY-B: make a tree (git worktree of the check's clone) at a SHA, optionally with one plant, optionally with
# the harness (zz_qpb.rs + adapter). usage: prep.sh <name> <base|head> <plant id or -> <harness 0|1>
W=/private/tmp/claude-501/qpb; N=$1; WHICH=$2; PL=$3; HAR=$4
SHA=$([ "$WHICH" = base ] && echo 5cab5e42df6cb3db05f3d38c7ba973beafd044b2 || echo cd7b6fdd1a4b2de5937795b052a68d793146eb6d)
[ -e $W/$N ] || git -C $W/repo worktree add -q --detach $W/$N $SHA
[ "$PL" != "-" ] && python3 -B $W/h/plant.py $W/$N $PL
if [ "$HAR" = 1 ]; then
  cp $W/h/zz_qpb.rs $W/$N/crates/coagent-policy/tests/zz_qpb.rs
  mkdir -p $W/$N/crates/coagent-policy/tests/qpb_adapter
  cp $W/h/adapter_$WHICH/mod.rs $W/$N/crates/coagent-policy/tests/qpb_adapter/mod.rs
  cmp $W/h/zz_qpb.rs $W/$N/crates/coagent-policy/tests/zz_qpb.rs && echo "harness cmp-silent in $N"
fi
git -C $W/$N diff --stat | tail -1; git -C $W/$N diff > $W/logs/diff_$N.txt
