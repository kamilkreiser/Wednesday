#!/bin/bash
S="/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/0bad48b2-2056-45a8-9019-8cc0029c12d3/scratchpad/gate_m3_roster_r2"
export COAGENT_TOOLS="$S/tools"
for n in daemon audit; do
  export CARGO_TARGET_DIR="$S/target_merge_$n"
  ( . "$S/merge_$n/scripts/env.sh"; cargo check --locked --manifest-path "$S/merge_$n/Cargo.toml" --workspace --all-targets > "$S/logs/merge_${n}_check.log" 2>&1; echo "$n check exit $? mounted=$(test -d /Volumes/Laptop-DEV/FRIDAY && echo yes || echo NO) $(date +%T)" >> "$S/logs/merges_summary.txt" )
done
# roster-touching tests
export CARGO_TARGET_DIR="$S/target_merge_audit"
( . "$S/merge_audit/scripts/env.sh"; cargo test --locked --manifest-path "$S/merge_audit/Cargo.toml" -p coagent-roster -p coagent-audit --no-fail-fast > "$S/logs/merge_audit_test.log" 2>&1; echo "audit test exit $? mounted=$(test -d /Volumes/Laptop-DEV/FRIDAY && echo yes || echo NO) $(date +%T)" >> "$S/logs/merges_summary.txt" )
export CARGO_TARGET_DIR="$S/target_merge_daemon"
( . "$S/merge_daemon/scripts/env.sh"; cargo test --locked --manifest-path "$S/merge_daemon/Cargo.toml" -p coagent-roster --no-fail-fast > "$S/logs/merge_daemon_roster_test.log" 2>&1; echo "daemon-tree roster test exit $? $(date +%T)" >> "$S/logs/merges_summary.txt"
  cargo test --locked --manifest-path "$S/merge_daemon/Cargo.toml" -p coagent-daemon --lib --no-fail-fast > "$S/logs/merge_daemon_lib_test.log" 2>&1; echo "daemon lib test exit $? mounted=$(test -d /Volumes/Laptop-DEV/FRIDAY && echo yes || echo NO) $(date +%T)" >> "$S/logs/merges_summary.txt" )
# main merge (fast-forward) check.sh once
export CARGO_TARGET_DIR="$S/target_merge_main"
"$S/merge_main/scripts/check.sh" > "$S/logs/merge_main_check.log" 2>&1; echo "main check.sh exit $? mounted=$(test -d /Volumes/Laptop-DEV/FRIDAY && echo yes || echo NO) $(date +%T)" >> "$S/logs/merges_summary.txt"
echo DONE >> "$S/logs/merges_summary.txt"
