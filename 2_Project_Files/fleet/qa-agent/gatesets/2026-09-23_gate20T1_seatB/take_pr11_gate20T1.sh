#!/bin/bash
# take_pr11_gate20T1.sh <a scratchpad dir under /private/tmp/claude-501/> — the RE-FINISH chain for the tier-1 set: takes PR 11 (KS-1143) from its READY,
# or re-pins everything after any head / develop move. READ verbs + the scratch clone FROM ORIGIN + writes into THIS gateset dir only. It never launches,
# sends, taps or writes under !CODING/. Every step's output goes to <step>_<HHMMSS>.out with its rc beside; the chain STOPS at the first nonzero rc (a
# refusal is the chain working — read the .out). Order: (1) capture the READYs (idempotent; never overwrites) -> (2) the round self-check (PR11_PENDING
# must be False: PR 11 is read from its READY, never typed) -> (3) predict in a scratch clone FROM ORIGIN (the seven MEASURED; develop READ in the same
# run; newdev_tree.txt written only if every hard assertion holds) -> (4) GitHub + Linear reads -> (5) fill the prompt (heads + develop re-read from
# origin in the same action) -> (6) generate the launcher -> (7) the launcher's --check. Then run launcher_controls_gate20T1.sh and read its end line.
# READY 11 landed while the drafter worked (08:31:06Z; #1212 ebb5d85ee) and this chain was run by the drafter as take_pr11_gate20T1.sh itself.
set -u
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T1_seatB'
SP="${1:-}"
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "no such dir $SP"; exit 9; } ;; *) echo "usage: take_pr11_gate20T1.sh <a Claude session scratchpad under /private/tmp/claude-501/>"; exit 9;; esac
L="$GS/launch_qa_secuura_batch1204-t1.sh"
T="$(date -u +%H%M%S)"
step() { name="$1"; shift; "$@" > "$GS/${name}_$T.out" 2>&1; rc=$?; echo "$rc" > "$GS/${name}_$T.rc"; echo "$(date -u +%H:%M:%SZ) $name rc $rc -> $GS/${name}_$T.out"; tail -3 "$GS/${name}_$T.out" | sed 's/^/    /'; [ "$rc" -eq 0 ] || { echo "STOP at $name (rc $rc)"; exit "$rc"; }; }
step capture python3 "$GS/capture_ready_mail_gate20T1.py"
step round20T1_selfcheck python3 "$GS/round20T1.py"
/usr/bin/grep -q '^PR11_PENDING False' "$GS/round20T1_selfcheck_$T.out" || { echo "STOP: PR 11 is still PENDING (no READY 11 in the inbox) — nothing to take yet; the launcher stays refused"; exit 8; }
step predict python3 "$GS/predict_batch_scratch_gate20T1.py" "$SP"
/usr/bin/grep -q '^t1sub_kind MEASURED' "$GS/newdev_tree.txt" || { echo "STOP: the tier-1 sub-tree is not MEASURED on seven real heads"; exit 4; }
step gh_pr_reads python3 "$GS/gh_pr_reads_gate20T1.py"
step linear_reads python3 "$GS/linear_reads_gate20T1.py"
step fill_prompt python3 "$GS/fill_prompt_gate20T1.py"
step gen_launcher python3 "$GS/gen_launcher_gate20T1.py" "$L" "$SP"
step launcher_check "$L" --check
echo "DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) — now: bash $GS/launcher_controls_gate20T1.sh $L $GS/2026-09-23_secuura-batch1204-t1.prompt.txt $SP ; read the prompt WHOLE; README.md."
