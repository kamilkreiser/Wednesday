#!/bin/bash
# Gate driver: run scripts/check.sh N times on a given checkout, summarise test totals per run.
# usage: check5.sh <checkout> <logprefix> <runs>
CO="$1"; LP="$2"; N="${3:-5}"
export COAGENT_TOOLS="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"
export CARGO_TARGET_DIR="/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/0bad48b2-2056-45a8-9019-8cc0029c12d3/scratchpad/gate_m1_relay_identity/target/ws"
export CARGO_NET_OFFLINE=true
for i in $(seq 1 "$N"); do
  start=$(date +%s)
  "$CO/scripts/check.sh" > "$LP.run$i.log" 2>&1
  rc=$?
  end=$(date +%s)
  p=0; f=0; ig=0
  while read -r a b c; do p=$((p+a)); f=$((f+b)); ig=$((ig+c)); done < <(/usr/bin/grep -E '^test result:' "$LP.run$i.log" | sed -E 's/.* ([0-9]+) passed; ([0-9]+) failed; ([0-9]+) ignored.*/\1 \2 \3/')
  echo "run $i exit=$rc passed=$p failed=$f ignored=$ig secs=$((end-start))" | tee -a "$LP.summary"
done
