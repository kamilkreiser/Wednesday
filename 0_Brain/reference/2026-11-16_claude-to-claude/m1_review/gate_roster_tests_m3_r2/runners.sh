#!/bin/bash
S="/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/0bad48b2-2056-45a8-9019-8cc0029c12d3/scratchpad/gate_m3_roster_r2"
export COAGENT_TOOLS="$S/tools"
export CARGO_TARGET_DIR="$S/target_head"
"$S/clone/scripts/red-controls-roster.sh" > "$S/logs/red_roster.log" 2>&1
echo "roster exit $? mounted=$(test -d /Volumes/Laptop-DEV/FRIDAY && echo yes || echo NO) $(date +%T)" >> "$S/logs/runners_summary.txt"
"$S/clone/scripts/red-controls-core.sh" > "$S/logs/red_core.log" 2>&1
echo "core exit $? mounted=$(test -d /Volumes/Laptop-DEV/FRIDAY && echo yes || echo NO) $(date +%T)" >> "$S/logs/runners_summary.txt"
