#!/bin/bash
# take_pr5_gate20T2.sh <this session's scratchpad> — the RE-FINISH chain for the tier-2 set: takes PR 5 (KS-1139) from its READY when it lands, or
# re-pins everything after any head / develop move. READ verbs + the scratch clone FROM ORIGIN + writes into THIS gateset dir, briefs/ and launchers/
# only. It never launches, sends, taps or writes under !CODING/. Every step's output goes to <step>_<HHMMSS>.out with its rc beside; the chain STOPS at
# the first nonzero rc (a refusal is the chain working — read the .out). Order: (1) capture the READYs (idempotent; never overwrites) -> (2) the round
# self-check (PR5_PENDING must be False: PR 5 is read from its READY, never typed) -> (3) predict in a scratch clone FROM ORIGIN (the tier-2 sub-tree
# must be MEASURED on four real heads) -> (4) GitHub + Linear reads -> (5) fill the prompt (heads read from origin in the same action; == the READY ==
# round20T2) -> (6) generate the launcher -> (7) the launcher's --check. Then run launcher_controls_gate20T2.sh and read its "controls end" line.
# PR 5 landed while the drafter worked (READY 5 06:39:32Z; #1206 bfbaf4366) and this chain's steps were run by hand then; the script is the same
# chain for a cold successor (README.md section 8).
set -u
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T2_seatB'
SP="${1:-}"
case "$SP" in /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/*/scratchpad*) [ -d "$SP" ] || { echo "no such dir $SP"; exit 9; } ;; *) echo "usage: take_pr5_gate20T2.sh <this session's scratchpad under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/>"; exit 9;; esac
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1202-t2.sh'
T="$(date -u +%H%M%S)"
step() { name="$1"; shift; "$@" > "$GS/${name}_$T.out" 2>&1; rc=$?; echo "$rc" > "$GS/${name}_$T.rc"; echo "$(date -u +%H:%M:%SZ) $name rc $rc -> $GS/${name}_$T.out"; tail -3 "$GS/${name}_$T.out" | sed 's/^/    /'; [ "$rc" -eq 0 ] || { echo "STOP at $name (rc $rc)"; exit "$rc"; }; }
step capture python3 "$GS/capture_ready_mail_gate20T2.py"
step round20T2_selfcheck python3 "$GS/round20T2.py"
/usr/bin/grep -q '^PR5_PENDING False' "$GS/round20T2_selfcheck_$T.out" || { echo "STOP: PR 5 is still PENDING (no READY 5 in the inbox) — nothing to take yet; the launcher stays PARTIAL-proof"; exit 8; }
step predict python3 "$GS/predict_batch_scratch_gate20T2.py" "$SP"
CL="$(sed -n 's/^scratch clone \(.*\)$/\1/p' "$GS/predict_$T.out")"
/usr/bin/grep -q '^t2sub_kind MEASURED' "$GS/newdev_tree.txt" || { echo "STOP: the tier-2 sub-tree is not MEASURED on four real heads"; exit 4; }
step gh_pr_reads python3 "$GS/gh_pr_reads_gate20T2.py"
step linear_reads python3 "$GS/linear_reads_gate20T2.py"
step fill_prompt python3 "$GS/fill_prompt_gate20T2.py"
step gen_launcher python3 "$GS/gen_launcher_gate20T2.py" "$L" "$CL"
step launcher_check "$L" --check
echo "DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) — now: bash $GS/launcher_controls_gate20T2.sh $L <prompt> $SP ; read the prompt WHOLE; README.md sections 3-4."
