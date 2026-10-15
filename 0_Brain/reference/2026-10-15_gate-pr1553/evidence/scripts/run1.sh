#!/bin/bash
# run1.sh <arm-label> <repo-root> <logfile> [extra env assignments...]
arm=$1; root=$2; log=$3; shift 3
t0=$(date +%s)
( cd "$root" && env TMPDIR=/tmp/g1553 "$@" /bin/bash Blockchain/Dev/scripts/__tests__/ks884_pre_push_tag_named_develop.test.sh </dev/null ) >"$log" 2>&1
rc=$?
t1=$(date +%s)
tally=$(grep -E '^ +[0-9]+ passed, [0-9]+ failed$' "$log" | tail -1 | sed 's/^ *//')
[ -n "$tally" ] || tally=DEAD
s4=ok; grep -q 'FAIL S4 a stale' "$log" && s4=FAIL
s10=ok; grep -q 'FAIL S10 a tag' "$log" && s10=FAIL
fails=$(grep -c '^  FAIL ' "$log")
echo "$arm rc=$rc tally=[$tally] S4=$s4 S10=$s10 failcells=$fails secs=$((t1-t0)) log=$(basename "$log")"
