#!/bin/bash
# launcher_controls_gate18B_rerun.sh <launcher> <prompt> — re-runs control U with the CORRECT expected code (31 — the drafter's S5) and the POSITIVE
# check (the first run's POSITIVE refused at 18 on a transient GitHub RemoteDisconnected on ONE contents GET — UNJUDGEABLE is fail-closed by design),
# against the FINAL prompt (fill run 3). Appends to launcher_check_controls.out; writes only into the controls dir of the first run.
set -u
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate18B_seatB'
L="${1:?launcher}"; P="${2:?prompt}"; C="$(cat "$G/controls_dir_gate18B.txt")"; OUT="$G/launcher_check_controls.out"
ok=0; bad=0
run() { local name="$1" want="$2"; shift 2; local t0; t0=$(date -u +%H:%M:%SZ); env "$@" "$L" --check > "$C/$name.out" 2>&1; local rc=$?; local v; [ "$rc" = "$want" ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "$name rc=$rc want=$want $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/$name.out" | cut -c1-160)" | tee -a "$OUT"; }
echo "rerun start $(date -u +%Y-%m-%dT%H:%M:%SZ) against prompt sha256 $(shasum -a 256 "$P" | cut -c1-16)" | tee -a "$OUT"
sed 's/76a88d9ddfa4f50098aa639a1056c5c9387aeb18/0000000000000000000000000000000000000000/g' "$P" > "$C/prompt_U2.txt"; run U2_end_tree_zeroed_want31 31 QAB1170_PROMPT="$C/prompt_U2.txt"
run POSITIVE2_real_check 0
echo "rerun end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH" | tee -a "$OUT"
