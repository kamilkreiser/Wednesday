#!/bin/bash
# QA-POLICY-NOTES: the crate's whole suite at the head, debug, own empty target dir, started from the tree's root.
W=/private/tmp/claude-501/qpn
. $W/h/envq.sh
export CARGO_TARGET_DIR=$W/t_head_dbg
echo "start $(date '+%F %T')" > $W/suite.log
python3 -B $W/h/inroot.py $W/head cargo test --locked -p coagent-policy >> $W/suite.log 2>&1
echo "exit $? end $(date '+%F %T')" >> $W/suite.log
