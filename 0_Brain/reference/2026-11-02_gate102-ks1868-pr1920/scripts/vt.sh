#!/bin/bash
# usage: vt.sh <logfile> [test file...]   runs vitest in the analytics service of the clone
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate102-ks1868-pr1920
S=$G/repo/Blockchain/Dev/services/analytics
LOG=$1; shift
cd "$S" && node ../../node_modules/vitest/vitest.mjs run "$@" > "$LOG" 2>&1
echo "rc=$?" >> "$LOG"
tail -8 "$LOG"
