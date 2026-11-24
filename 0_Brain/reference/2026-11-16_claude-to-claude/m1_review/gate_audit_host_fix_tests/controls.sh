#!/bin/bash
# QA-AUDIT-HOST-FIX: positive controls of my own schedules: the generated run under each G01 red variant.
W=/private/tmp/claude-501/qahf
for red in reopen_hides_landed release_reopen_hides_landed; do
  COAGENT_AUDIT_HOST_RED=$red QAHF_CASES=600 COAGENT_AUDIT_HOST_SCRATCH=$W/scr5 CARGO_TARGET_DIR=$W/target/dbg_red \
    timeout 3000 python3 -B $W/bin/run.py cargo test --locked -p coagent-audit-host --lib -- --exact tests::qahf::qahf_generated --nocapture > $W/logs/control_$red.log 2>&1
  echo "$red rc=$?"
done
