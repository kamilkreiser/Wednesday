#!/bin/bash
# QA-AUDIT-HOST-NOTES item 8: the crate's tests, the audit crate's tests, the red script; one at a time,
# each started only when other seats run at most 2 heavy jobs (a job = a matching process whose parent
# is not itself a matching process).
W=/private/tmp/claude-501/qahn
count() {
  ps -axo pid=,ppid=,command= | awk '
    $3 == "bash" && /(check\.sh|red-controls[^ ]*\.sh|test-p1p\.sh|test-daemon\.sh)/ && !/qahn/ { m[$1]=$2 }
    END { n=0; for (p in m) if (!(m[p] in m)) n++; print n }'
}
waitfor() {
  while :; do c=$(count); if [ "$c" -le 2 ]; then echo "$(date '+%T') start $1; heavy jobs of others: $c"; return; fi
    echo "$(date '+%T') waiting for $1: heavy jobs of others $c"; sleep 60; done
}
export QA_CLONE=$W/clean COAGENT_AUDIT_HOST_SCRATCH=$W/scratch/clean
mkdir -p $W/scratch/clean $W/redlogs
waitfor "cargo test -p coagent-audit-host"
CARGO_TARGET_DIR=$W/target/clean-test python3 -B $W/bin/run.py cargo test --locked -p coagent-audit-host > $W/logs/test_host.log 2>&1; echo "$(date '+%T') host tests rc=$?"
waitfor "cargo test -p coagent-audit"
CARGO_TARGET_DIR=$W/target/clean-test python3 -B $W/bin/run.py cargo test --locked -p coagent-audit > $W/logs/test_audit.log 2>&1; echo "$(date '+%T') audit tests rc=$?"
waitfor "red-controls-audit-host.sh"
COAGENT_AUDIT_HOST_RED_TARGET=$W/target/red COAGENT_AUDIT_HOST_RED_LOGS=$W/redlogs CARGO_TARGET_DIR=$W/target/clean-test python3 -B $W/bin/run.py bash scripts/red-controls-audit-host.sh > $W/logs/red_script.log 2>&1; echo "$(date '+%T') red script rc=$?"
