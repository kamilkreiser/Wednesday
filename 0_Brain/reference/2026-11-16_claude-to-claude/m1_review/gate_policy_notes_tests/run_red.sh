#!/bin/bash
# QA-POLICY-NOTES: the crate's red controls WHOLE at the head, own empty target dir, started from the tree's root.
W=/private/tmp/claude-501/qpn
. $W/h/envq.sh
export CARGO_TARGET_DIR=$W/t_red
export RED_CONTROLS_LOG=$W/red_normal_build.log
echo "start $(date '+%F %T') head $(git -C $W/head rev-parse HEAD)" > $W/red.log
python3 -B $W/h/inroot.py $W/head bash crates/coagent-policy/red-controls.sh >> $W/red.log 2>&1
echo "exit $? end $(date '+%F %T')" >> $W/red.log
