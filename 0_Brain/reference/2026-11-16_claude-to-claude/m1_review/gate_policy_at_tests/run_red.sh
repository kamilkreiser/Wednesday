#!/bin/bash
# QA-POLICY-AT: the crate's red controls WHOLE at the head, own empty target dir, started from the tree's root (no cd).
W=/private/tmp/claude-501/qpa
. $W/h/envx.sh
export CARGO_TARGET_DIR=$W/t_red
export RED_CONTROLS_LOG=$W/red_normal_build.log
export COAGENT_TEST_TMP=$W/testtmp_red
mkdir -p $COAGENT_TEST_TMP
echo "start $(date '+%F %T') head $(git -C $W/head rev-parse HEAD) status_lines $(git -C $W/head status --porcelain | wc -l) heavy $(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh) CARGO_TARGET_DIR=$CARGO_TARGET_DIR RED_CONTROLS_LOG=$RED_CONTROLS_LOG COAGENT_TEST_TMP=$COAGENT_TEST_TMP" > $W/red.log
python3 -B $W/h/inroot.py $W/head bash crates/coagent-policy/red-controls.sh >> $W/red.log 2>&1
echo "exit $? end $(date '+%F %T') status_lines $(git -C $W/head status --porcelain | wc -l)" >> $W/red.log
