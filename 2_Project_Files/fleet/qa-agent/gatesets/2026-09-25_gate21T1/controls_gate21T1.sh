#!/bin/bash
# controls_gate21T1.sh <launcher> <scratchpad> — controls for launch_qa_secuura_batch1213-t1.sh (--check with test overrides / a doctored prompt or
# capture copy, one non-TTY launch, one moved copy) and for repin_and_launch_gate21T1.sh (all --dry-run, except R4 which is a REAL run that must stop
# at step 0 because the routing line is absent — SKIPPED if the line is present, so this script can never launch). Every doctored copy lives under the
# scratchpad only. Nothing is launched, sent or written outside it.
set -u
L="$1"; SP="$2"
case "$SP" in /private/tmp/claude-501/*/scratchpad*) ;; *) echo "REFUSING: not a scratchpad"; exit 9;; esac
GS="$(dirname "$(/bin/realpath "$L")")"
R="$GS/repin_and_launch_gate21T1.sh"; PF="$GS/2026-09-25_secuura-batch1213-t1.prompt.txt"; BF="$GS/mail_gate21T1_ready.md"
D="$(mktemp -d "$SP/g21_ctrl.XXXXXX")"; ok=0; bad=0
run() { name="$1"; want="$2"; shift 2; "$@" > "$D/$name.out" 2>&1 < /dev/null; rc=$?; [ "$rc" = "$want" ] && { echo "OK   $name rc $rc (want $want)"; ok=$((ok+1)); } || { echo "MISMATCH $name rc $rc (want $want) — $D/$name.out"; bad=$((bad+1)); }; tail -2 "$D/$name.out" | sed 's/^/     /'; }
doctor() { # doctor <name> <old> <new> : a prompt copy with <old> replaced by <new>, asserting the replacement happened
  python3 - "$PF" "$D/p_$1.txt" "$2" "$3" <<'PY'
import sys; s = open(sys.argv[1], encoding='utf-8').read(); n = s.count(sys.argv[3]); assert n >= 1, ('anchor absent', sys.argv[3])
open(sys.argv[2], 'w', encoding='utf-8').write(s.replace(sys.argv[3], sys.argv[4])); print('  (copy %s: %d occurrence(s) of %r replaced)' % (sys.argv[2].split('/')[-1], n, sys.argv[3]))
PY
}
echo "controls start $(date -u +%Y-%m-%dT%H:%M:%SZ) dir $D"
H17="$(sed -n 's/^  "1217|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|[0-9]*"$/\1/p' "$L")"; STALE="${H17%?}$( [ "${H17: -1}" = 0 ] && echo 1 || echo 0 )"
H13="$(sed -n 's/^  "1213|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|[0-9]*"$/\1/p' "$L")"
echo "== launcher (--check)"
run P_positive_check 0 "$L" --check
run C_stale_head_1217 6 env QAB1213_HEAD_1217="$STALE" "$L" --check
run D_develop_moved 17 env QAB1213_CUR_DEV="$H13" "$L" --check
tail -n +2 "$PF" > "$D/p_noultra.txt"; run G_no_thinking_directive 8 env QAB1213_PROMPT="$D/p_noultra.txt" "$L" --check
{ cat "$PF"; echo '{{UNFILLED}}'; } > "$D/p_unfilled.txt"; run U_unfilled_token 8 env QAB1213_PROMPT="$D/p_unfilled.txt" "$L" --check
/usr/bin/grep -v -F '239/239' "$BF" > "$D/b_no239.md"; echo "  (O copy: capture lines naming 239/239 removed: $(/usr/bin/grep -c -F '239/239' "$BF") -> $(/usr/bin/grep -c -F '239/239' "$D/b_no239.md"))"
run O_capture_missing_seat_item 30 env QAB1213_BRIEF="$D/b_no239.md" "$L" --check
doctor ticket 'PR #1216 is KS-975.' 'PR #1216 is KS-9750.'; run T_ticket_statement 32 env QAB1213_PROMPT="$D/p_ticket.txt" "$L" --check
doctor tier '#1214 T1' '#1214 T2'; run I_tier_line 7 env QAB1213_PROMPT="$D/p_tier.txt" "$L" --check
doctor kw 'S8 ATTRIBUTION' 'S8 BLAME'; run L_prompt_missing_keyword 33 env QAB1213_PROMPT="$D/p_kw.txt" "$L" --check
doctor stack 'PREFLIGHT LEGS 3/4/8 ARE OWED FOR #1216 AND #1217' 'PREFLIGHT LEGS ARE OPTIONAL'; run K_stack_rule 35 env QAB1213_PROMPT="$D/p_stack.txt" "$L" --check
doctor stack2 'A SKIP or an rc 2 is NOT RUN, never a pass' 'A SKIP is fine'; run K2_skip_is_not_a_pass 35 env QAB1213_PROMPT="$D/p_stack2.txt" "$L" --check
doctor base 'PROVE IT IS EXACTLY ONE ROW AND THE GATES STILL PASS' 'LOOK AT IT'; run B_baseline_rule 36 env QAB1213_PROMPT="$D/p_base.txt" "$L" --check
doctor lock 'UNEXPECTED PACKAGE MOVEMENT' 'PACKAGES'; run X_lock_rule 37 env QAB1213_PROMPT="$D/p_lock.txt" "$L" --check
doctor load 'KNOWN FALSE-RED' 'KNOWN FLAKE'; run Y_load_rule 38 env QAB1213_PROMPT="$D/p_load.txt" "$L" --check
doctor holds 'NO deploy of any kind. Findings only.' 'deploy if green.'; run H_holds 39 env QAB1213_PROMPT="$D/p_holds.txt" "$L" --check
doctor go '`GO: merge #1213, #1214, #1216, #1217 batch`' '`GO: merge batch`'; run A_GO_string 26 env QAB1213_PROMPT="$D/p_go.txt" "$L" --check
run N_launch_non_tty 21 "$L"
mkdir -p "$D/moved"; cp -p "$L" "$D/moved/"; run M_moved_launcher 2 "$D/moved/$(basename "$L")" --check
echo "== repin (--dry-run unless stated)"
run R1_positive_dry_run 0 bash "$R" "$L" "$SP" --dry-run
sed "s/|$H17|3\"$/|$STALE|3\"/" "$L" > "$D/L_stale.sh"; chmod 755 "$D/L_stale.sh"; echo "  (R2 copy: rows carrying the stale #1217 head: $(/usr/bin/grep -c -F "|$STALE|" "$D/L_stale.sh") — must be 1)"
run R2_stale_head 11 bash "$R" "$D/L_stale.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='[0-9a-f]*'$/DEVELOP_SHA='$H13'/" "$L" > "$D/L_devstale.sh"; chmod 755 "$D/L_devstale.sh"
run R3_pinned_develop_stale 10 bash "$R" "$D/L_devstale.sh" "$SP" --dry-run
if [ "$(/usr/bin/grep -c -F 'QA/Secuura-batch1213|coagent@agentmail.to|yes' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf)" = 0 ]; then
  run R4_real_run_unrouted 1 bash "$R" "$L" "$SP"
else echo "SKIP R4_real_run_unrouted — the routing line is present, a real run would launch"; fi
run R5_bad_scratchpad 9 bash "$R" "$L" /tmp --dry-run
mkdir -p "$D/kitcopy"; cp -p "$GS"/*.py "$GS"/*.sh "$GS"/*.txt "$GS"/*.md "$D/kitcopy/"; run R6_moved_kit_dry_run 0 bash "$D/kitcopy/repin_and_launch_gate21T1.sh" "$D/kitcopy/$(basename "$L")" "$SP" --dry-run
/usr/bin/grep -c -F 'MOVED KIT' "$D/R6_moved_kit_dry_run.out" | sed 's/^/  (R6: MOVED KIT lines reported: /; s/$/ — must be 1)/'
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH"
[ "$bad" -eq 0 ]
