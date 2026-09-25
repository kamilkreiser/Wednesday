#!/bin/bash
# controls_gate21T1b.sh <launcher> <scratchpad> — controls for launch_qa_secuura_batch1224-t1.sh (--check with test overrides / a doctored prompt or
# capture copy, one non-TTY launch, one moved copy) and for repin_and_launch_gate21T1b.sh (all --dry-run, except R4 which is a REAL run that must stop
# at step 0 because the routing line is absent — SKIPPED if the line is present, so this script can never launch). Every doctored copy lives under the
# scratchpad only. Nothing is launched, sent or written outside it. Derived from the sibling kits' controls_gate21T1.sh / controls_gate21T2.sh, re-keyed
# to four rows. Each doctored phrase is chosen OUTSIDE the by-name ladder, so the control reaches the rule it names (the ladder, exit 33, runs first).
# NEW here: V — the base-invariant compare asserts the PR's own paths BY NAME (a same-count wrong path must refuse, exit 10).
set -u
L="$1"; SP="$2"
case "$SP" in /private/tmp/claude-501/*/scratchpad*) ;; *) echo "REFUSING: not a scratchpad"; exit 9;; esac
GS="$(dirname "$(/bin/realpath "$L")")"
R="$GS/repin_and_launch_gate21T1b.sh"; PF="$GS/2026-09-25_secuura-batch1224-t1.prompt.txt"; BF="$GS/mail_gate21T1b_ready.md"
D="$(mktemp -d "$SP/g21b_ctrl.XXXXXX")"; ok=0; bad=0
run() { name="$1"; want="$2"; shift 2; "$@" > "$D/$name.out" 2>&1 < /dev/null; rc=$?; [ "$rc" = "$want" ] && { echo "OK   $name rc $rc (want $want)"; ok=$((ok+1)); } || { echo "MISMATCH $name rc $rc (want $want) — $D/$name.out"; bad=$((bad+1)); }; tail -2 "$D/$name.out" | cut -c1-260 | sed 's/^/     /'; }
doctor() { # doctor <name> <old> <new> : a prompt copy with <old> replaced by <new>, asserting the replacement happened
  python3 - "$PF" "$D/p_$1.txt" "$2" "$3" <<'PY'
import sys; s = open(sys.argv[1], encoding='utf-8').read(); n = s.count(sys.argv[3]); assert n >= 1, ('anchor absent', sys.argv[3])
open(sys.argv[2], 'w', encoding='utf-8').write(s.replace(sys.argv[3], sys.argv[4])); print('  (copy %s: %d occurrence(s) of %r replaced)' % (sys.argv[2].split('/')[-1], n, sys.argv[3]))
PY
}
echo "controls start $(date -u +%Y-%m-%dT%H:%M:%SZ) dir $D"
H30="$(sed -n 's/^  "1230|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|[0-9]*|[0-9]*|[^|"]*"$/\1/p' "$L")"; STALE="${H30%?}$( [ "${H30: -1}" = 0 ] && echo 1 || echo 0 )"
H24="$(sed -n 's/^  "1224|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|[0-9]*|[0-9]*|[^|"]*"$/\1/p' "$L")"
[ -n "$H30" ] && [ -n "$H24" ] || { echo "REFUSING: could not read the #1230 / #1224 rows"; exit 9; }
echo "== launcher (--check)"
run P_positive_check 0 "$L" --check
run C_stale_head_1230 6 env QAB1224_HEAD_1230="$STALE" "$L" --check
run D_develop_moved 17 env QAB1224_CUR_DEV="$H24" "$L" --check
run V_compare_paths_by_name 10 env QAB1224_PATHS_1226="Blockchain/Dev/packages/shared/src/crypto/registry.ts" "$L" --check
tail -n +2 "$PF" > "$D/p_noultra.txt"; run G_no_thinking_directive 8 env QAB1224_PROMPT="$D/p_noultra.txt" "$L" --check
{ cat "$PF"; echo '{{UNFILLED}}'; } > "$D/p_unfilled.txt"; run U_unfilled_token 8 env QAB1224_PROMPT="$D/p_unfilled.txt" "$L" --check
/usr/bin/grep -v -F '832/832' "$BF" > "$D/b_no832.md"; echo "  (O copy: capture lines naming 832/832 removed: $(/usr/bin/grep -c -F '832/832' "$BF") -> $(/usr/bin/grep -c -F '832/832' "$D/b_no832.md"))"
run O_capture_missing_seat_item 30 env QAB1224_BRIEF="$D/b_no832.md" "$L" --check
doctor ticket 'PR #1228 is KS-1171.' 'PR #1228 is KS-11710.'; run T_ticket_statement 32 env QAB1224_PROMPT="$D/p_ticket.txt" "$L" --check
doctor tier '#1226 T1' '#1226 T2'; run I_tier_line 7 env QAB1224_PROMPT="$D/p_tier.txt" "$L" --check
doctor kw 'THE EQUIVALENCE PROOF' 'THE EQUIVALENCE'; run L_prompt_missing_keyword 33 env QAB1224_PROMPT="$D/p_kw.txt" "$L" --check
doctor binv 'EVERY MERGE CHECK IS BASE-INVARIANT' 'EVERY MERGE CHECK IS AS IT WAS';   # controls_1: the first anchor WRAPS across two prompt lines, so its doctor asserted (rc 4, no copy)
 run B_base_invariant_rule 34 env QAB1224_PROMPT="$D/p_binv.txt" "$L" --check
doctor stack 'PREFLIGHT LEGS 3/4/8 ARE OWED FOR #1228' 'PREFLIGHT LEGS ARE OPTIONAL'; run K_stack_rule 35 env QAB1224_PROMPT="$D/p_stack.txt" "$L" --check
doctor stack2 'A SKIP or an rc 2 is NOT RUN, never a pass' 'A SKIP is fine'; run K2_skip_is_not_a_pass 35 env QAB1224_PROMPT="$D/p_stack2.txt" "$L" --check
doctor leg4 'mint NO credential' 'mint a credential if needed'; run K3_leg4_honesty 35 env QAB1224_PROMPT="$D/p_leg4.txt" "$L" --check
doctor rule 'IFF polled >= 2 AND elapsed >= 60_000' 'IFF polled >= 2 OR elapsed >= 60_000'; run J_ruling_both_conditions 36 env QAB1224_PROMPT="$D/p_rule.txt" "$L" --check
doctor integ 'NOT APPLICABLE — none exist' 'green — none exist'; run J2_integration_rule 37 env QAB1224_PROMPT="$D/p_integ.txt" "$L" --check
doctor anch 'pre-existing (KS-562), not caused by this change' 'known flaky'; run Y_anchoring_wording 38 env QAB1224_PROMPT="$D/p_anch.txt" "$L" --check
doctor load 'KNOWN FALSE-RED (ticket KS-1155)' 'KNOWN FLAKE (ticket KS-1155)'; run Y2_load_rule 38 env QAB1224_PROMPT="$D/p_load.txt" "$L" --check
doctor holds 'NO deploy of any kind. Findings only.' 'deploy if green.'; run H_holds 39 env QAB1224_PROMPT="$D/p_holds.txt" "$L" --check
doctor guard 'TAMPER THE GUARD' 'LOOK AT THE GUARD'; run R_guard_rule_1224 40 env QAB1224_PROMPT="$D/p_guard.txt" "$L" --check
doctor typeonly 'NO package.json / lockfile / tsconfig in this round' 'package.json changes allowed'; run W_type_only_rule_1226 41 env QAB1224_PROMPT="$D/p_typeonly.txt" "$L" --check
doctor relax 'THE F-A RELAXATION' 'THE F-A CHANGE'; run Q_fa_relaxation_1230 42 env QAB1224_PROMPT="$D/p_relax.txt" "$L" --check
doctor resid 'record it as a KS-1131 residual' 'call it green'; run Q2_residual_never_green_1230 42 env QAB1224_PROMPT="$D/p_resid.txt" "$L" --check
doctor reap 'never by name, never pid 1' 'by name is fine'; run Z_login_stub_reaper 43 env QAB1224_PROMPT="$D/p_reap.txt" "$L" --check
doctor go '`GO: merge #1224, #1226, #1228, #1230 batch`' '`GO: merge batch`'; run A_GO_string 26 env QAB1224_PROMPT="$D/p_go.txt" "$L" --check
doctor add 'ONE equality target PER PR FILE (2/1/5/1 = 9 over 9 paths)' 'targets as you like'; run E_addendum 25 env QAB1224_PROMPT="$D/p_add.txt" "$L" --check
doctor subj '[QA -> Wednesday] TIER-1 BATCH GATE #1224-#1230 round 21' '[QA] gate'; run S_subject 23 env QAB1224_PROMPT="$D/p_subj.txt" "$L" --check
run N_launch_non_tty 21 "$L"
mkdir -p "$D/moved"; cp -p "$L" "$D/moved/"; run M_moved_launcher 2 "$D/moved/$(basename "$L")" --check
echo "== repin (--dry-run unless stated)"
run R1_positive_dry_run 0 bash "$R" "$L" "$SP" --dry-run
sed "s/|$H30|1|2|/|$STALE|1|2|/" "$L" > "$D/L_stale.sh"; chmod 755 "$D/L_stale.sh"; echo "  (R2 copy: rows carrying the stale #1230 head: $(/usr/bin/grep -c -F "|$STALE|" "$D/L_stale.sh") — must be 1)"
run R2_stale_head 11 bash "$R" "$D/L_stale.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='[0-9a-f]*'$/DEVELOP_SHA='$H24'/" "$L" > "$D/L_devstale.sh"; chmod 755 "$D/L_devstale.sh"
run R3_pinned_develop_stale 10 bash "$R" "$D/L_devstale.sh" "$SP" --dry-run
if [ "$(/usr/bin/grep -c -F 'QA/Secuura-batch1224|coagent@agentmail.to|yes' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf)" = 0 ]; then
  run R4_real_run_unrouted 1 bash "$R" "$L" "$SP"
else echo "SKIP R4_real_run_unrouted — the routing line is present, a real run would launch"; fi
run R5_bad_scratchpad 9 bash "$R" "$L" /tmp --dry-run
mkdir -p "$D/kitcopy"; cp -p "$GS"/*.py "$GS"/*.sh "$GS"/*.txt "$GS"/*.md "$D/kitcopy/"; run R6_moved_kit_dry_run 0 bash "$D/kitcopy/repin_and_launch_gate21T1b.sh" "$D/kitcopy/$(basename "$L")" "$SP" --dry-run
/usr/bin/grep -c -F 'MOVED KIT' "$D/R6_moved_kit_dry_run.out" | sed 's/^/  (R6: MOVED KIT lines reported: /; s/$/ — must be 1)/'
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH"
[ "$bad" -eq 0 ]
