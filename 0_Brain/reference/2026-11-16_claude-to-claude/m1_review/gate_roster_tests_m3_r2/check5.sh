#!/bin/bash
S="/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/0bad48b2-2056-45a8-9019-8cc0029c12d3/scratchpad/gate_m3_roster_r2"
export COAGENT_TOOLS="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"
export CARGO_TARGET_DIR="$S/target_head"
for i in 1 2 3 4 5; do
  "$S/clone/scripts/check.sh" > "$S/logs/check_$i.log" 2>&1
  echo "run $i exit $? mounted=$(test -d /Volumes/Laptop-DEV/FRIDAY && echo yes || echo NO) $(date +%T)" >> "$S/logs/check_summary.txt"
done
