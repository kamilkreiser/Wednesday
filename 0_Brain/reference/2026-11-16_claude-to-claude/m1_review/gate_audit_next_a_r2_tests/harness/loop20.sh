#!/bin/bash
# usage: loop20.sh <tree> <target> <logdir> <n> <start>   twenty-run AW-7 loop, red variant kept on every run
W=/private/tmp/claude-501/qan2
TREE="$1"; T="$2"; L="$3"; N="${4:-20}"; S0="${5:-1}"
mkdir -p "$L"
export COAGENT_RED_AW=seal_error_ends_the_engine
if [ ! -e "$L/warm.log" ]; then
  bash $W/r.sh "$TREE" "$T" cargo test --locked -p coagent-daemon --test aw_disk --no-run > "$L/warm.log" 2>&1
  echo "warm exit $?" >> "$L/warm.log"
fi
for i in $(seq "$S0" $((S0+N-1))); do
  s=$(date +%s)
  bash $W/r.sh "$TREE" "$T" cargo test --locked -p coagent-daemon --test aw_disk -- --exact every_disk_failure_gets_a_row_and_nothing_is_recorded_twice > "$L/run$i.log" 2>&1
  rc=$?
  first=$(grep -m1 -A1 "panicked at" "$L/run$i.log" | tr '\n' ' ')
  comp=$(grep -c 'Compiling coagent-daemon' "$L/run$i.log")
  echo "run$i exit=$rc secs=$(( $(date +%s)-s )) compiling_daemon=$comp first: $first" >> "$L/summary.txt"
done
echo DONE >> "$L/summary.txt"
