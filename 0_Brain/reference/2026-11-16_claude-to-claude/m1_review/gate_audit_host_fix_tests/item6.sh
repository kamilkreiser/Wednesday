#!/bin/bash
# QA-AUDIT-HOST-FIX item 6, in the CLEAN worktree at the head (no file of mine in it), own target.
W=/private/tmp/claude-501/qahf
export QA_CLONE=$W/clean CARGO_TARGET_DIR=$W/target/clean COAGENT_AUDIT_HOST_SCRATCH=$W/scr6
mkdir -p $W/scr6
python3 -B $W/bin/run.py cargo test --locked -p coagent-audit-host > $W/logs/item6_host.log 2>&1; echo "host rc=$?" >> $W/logs/item6_rc.txt
python3 -B $W/bin/run.py cargo test --locked -p coagent-audit > $W/logs/item6_audit.log 2>&1; echo "audit rc=$?" >> $W/logs/item6_rc.txt
