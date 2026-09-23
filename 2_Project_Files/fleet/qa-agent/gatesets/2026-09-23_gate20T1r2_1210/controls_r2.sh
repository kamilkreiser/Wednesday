#!/bin/bash
# controls_r2.sh <launcher> <scratchpad> — controls for launch_qa_secuura_1210-t1r2.sh (--check with test overrides, and one non-TTY launch) and for
# repin_and_launch_r2.sh (all --dry-run, except R4 which is a REAL run that must stop at step 0 because the routing line is absent — it is SKIPPED if the
# line is present, so this script can never launch). Copies live under the scratchpad only. Nothing is launched, sent or written outside it.
set -u
L="$1"; SP="$2"
case "$SP" in /private/tmp/claude-501/*/scratchpad*) ;; *) echo "REFUSING: not a scratchpad"; exit 9;; esac
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T1r2_1210'
R="$GS/repin_and_launch_r2.sh"; PF="$GS/2026-09-23_secuura-1210-t1r2.prompt.txt"; BF="$GS/mail_r2_ready.md"
BASE='2bc5ccf63b8c40911afb568b03cace066238ffcf'
D="$(mktemp -d "$SP/r2_ctrl.XXXXXX")"; ok=0; bad=0
run() { name="$1"; want="$2"; shift 2; "$@" > "$D/$name.out" 2>&1 < /dev/null; rc=$?; [ "$rc" = "$want" ] && { echo "OK   $name rc $rc (want $want)"; ok=$((ok+1)); } || { echo "MISMATCH $name rc $rc (want $want) — $D/$name.out"; bad=$((bad+1)); }; tail -2 "$D/$name.out" | sed 's/^/     /'; }
echo "controls start $(date -u +%Y-%m-%dT%H:%M:%SZ) dir $D"
H="$(sed -n "s/^HEAD_SHA='\([0-9a-f]\{40\}\)'$/\1/p" "$L")"; STALE="${H%?}$( [ "${H: -1}" = 0 ] && echo 1 || echo 0 )"
echo "== launcher (--check)"
run P_positive_check 0 "$L" --check
run C_stale_head 6 env QA1210_HEAD="$STALE" "$L" --check
run D_develop_at_BASE 17 env QA1210_CUR_DEV="$BASE" "$L" --check
tail -n +2 "$PF" > "$D/p_noultra.txt"; run G_no_thinking_directive 8 env QA1210_PROMPT="$D/p_noultra.txt" "$L" --check
/usr/bin/grep -v -F '2550' "$BF" > "$D/b_no2550.md"; echo "  (O copy: capture lines naming 2550 removed: $(/usr/bin/grep -c -F '2550' "$BF") -> $(/usr/bin/grep -c -F '2550' "$D/b_no2550.md"))"
run O_capture_missing_seat_item 30 env QA1210_BRIEF="$D/b_no2550.md" "$L" --check
sed 's/THE THIRD JOB/THE LAST JOB/' "$PF" > "$D/p_nothird.txt"; run L_prompt_missing_keyword 33 env QA1210_PROMPT="$D/p_nothird.txt" "$L" --check
sed 's/GO: merge #1210 batch/GO: merge #1210/' "$PF" > "$D/p_nogo.txt"; run A_prompt_missing_GO_string 26 env QA1210_PROMPT="$D/p_nogo.txt" "$L" --check
run N_launch_non_tty 21 "$L"
echo "== repin (--dry-run unless stated)"
run R1_positive_dry_run 0 bash "$R" "$L" "$SP" --dry-run
sed "s/^HEAD_SHA='$H'$/HEAD_SHA='$STALE'/" "$L" > "$D/L_stale.sh"; chmod 755 "$D/L_stale.sh"; echo "  (R2 copy: HEAD_SHA rows carrying the stale head: $(/usr/bin/grep -c "^HEAD_SHA='$STALE'$" "$D/L_stale.sh") — must be 1)"
run R2_stale_head 11 bash "$R" "$D/L_stale.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='[0-9a-f]*'$/DEVELOP_SHA='$BASE'/" "$L" > "$D/L_devstale.sh"; chmod 755 "$D/L_devstale.sh"
run R3_pinned_develop_stale 10 bash "$R" "$D/L_devstale.sh" "$SP" --dry-run
if [ "$(/usr/bin/grep -c -F 'QA/Secuura-1210r2|coagent@agentmail.to|yes' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf)" = 0 ]; then
  run R4_real_run_unrouted 1 bash "$R" "$L" "$SP"
else echo "SKIP R4_real_run_unrouted — the routing line is present, a real run would launch"; fi
run R5_bad_scratchpad 9 bash "$R" "$L" /tmp --dry-run
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH"
[ "$bad" -eq 0 ]
