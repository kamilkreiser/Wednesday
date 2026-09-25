#!/bin/bash
# controls_gate21T2b.sh <launcher> <scratchpad> — controls for launch_qa_secuura_batch1225-t2.sh (--check with test overrides / a doctored prompt or
# capture copy, one non-TTY launch, one moved copy) and for repin_and_launch_gate21T2b.sh (all --dry-run, except R4 which is a REAL run that must stop
# at step 0 because the routing line is absent — SKIPPED if the line is present, so this script can never launch). Every doctored copy lives under the
# scratchpad only. Nothing is launched, sent or written outside it. Derived from the sibling tier-2 kit's controls_gate21T2.sh, re-keyed to five rows,
# plus arms for the new exits (3, 4, 10, 20, 31, 37, 38-fakepg, 40, 41, 42). Each doctored phrase is chosen OUTSIDE the by-name ladder and the BOTH
# list, so the control reaches the rule it names (the ladder, exit 33, and the BOTH list, exit 30, run first); `doctor` asserts its anchor is present.
set -u
L="$1"; SP="$2"
case "$SP" in /private/tmp/claude-501/*/scratchpad*) ;; *) echo "REFUSING: not a scratchpad"; exit 9;; esac
GS="$(dirname "$(/bin/realpath "$L")")"
R="$GS/repin_and_launch_gate21T2b.sh"; PF="$GS/2026-09-25_secuura-batch1225-t2.prompt.txt"; BF="$GS/mail_gate21T2b_ready.md"
D="$(mktemp -d "$SP/g21T2b_ctrl.XXXXXX")"; ok=0; bad=0
run() { name="$1"; want="$2"; shift 2; "$@" > "$D/$name.out" 2>&1 < /dev/null; rc=$?; [ "$rc" = "$want" ] && { echo "OK   $name rc $rc (want $want)"; ok=$((ok+1)); } || { echo "MISMATCH $name rc $rc (want $want) — $D/$name.out"; bad=$((bad+1)); }; tail -2 "$D/$name.out" | sed 's/^/     /'; }
doctor() { # doctor <name> <old> <new> : a prompt copy with <old> replaced by <new>, asserting the replacement happened
  python3 - "$PF" "$D/p_$1.txt" "$2" "$3" <<'PY'
import sys; s = open(sys.argv[1], encoding='utf-8').read(); n = s.count(sys.argv[3]); assert n >= 1, ('anchor absent', sys.argv[3])
open(sys.argv[2], 'w', encoding='utf-8').write(s.replace(sys.argv[3], sys.argv[4])); print('  (copy %s: %d occurrence(s) of %r replaced)' % (sys.argv[2].split('/')[-1], n, sys.argv[3]))
PY
}
echo "controls start $(date -u +%Y-%m-%dT%H:%M:%SZ) dir $D"
H32="$(sed -n 's/^  "1232|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|[0-9]*|[0-9]*"$/\1/p' "$L")"; STALE="${H32%?}$( [ "${H32: -1}" = 0 ] && echo 1 || echo 0 )"
H25="$(sed -n 's/^  "1225|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|[0-9]*|[0-9]*"$/\1/p' "$L")"
ET="$(sed -n "s/^END_TREE='\([0-9a-f]\{40\}\)'$/\1/p" "$L")"
DEV="$(sed -n "s/^DEVELOP_SHA='\([0-9a-f]\{40\}\)'$/\1/p" "$L")"; PIN="QAB1225_CUR_DEV=$DEV"   # arms below pin develop so a live develop move cannot mask the rule they name
[ -n "$DEV" ] && [ -n "$H32" ] && [ -n "$H25" ] && [ -n "$ET" ] || { echo "REFUSING: could not read the #1232 / #1225 rows or the END_TREE"; exit 9; }
echo "== launcher (--check)"
run P_positive_check 0 "$L" --check
run P2_positive_check_pinned_develop 0 env "$PIN" "$L" --check
run F3_capture_missing 3 env "$PIN" QAB1225_BRIEF="$D/nonexistent.md" "$L" --check
run F4_prompt_missing 4 env "$PIN" QAB1225_PROMPT="$D/nonexistent.txt" "$L" --check
run C_stale_head_1232 6 env "$PIN" QAB1225_HEAD_1232="$STALE" "$L" --check
run D_develop_moved 17 env "$PIN" QAB1225_CUR_DEV="$H25" "$L" --check
run Q_compare_behind 10 env "$PIN" QAB1225_BEHIND=5 "$L" --check
tail -n +2 "$PF" > "$D/p_noultra.txt"; run G_no_thinking_directive 8 env "$PIN" QAB1225_PROMPT="$D/p_noultra.txt" "$L" --check
{ cat "$PF"; echo '{{UNFILLED}}'; } > "$D/p_unfilled.txt"; run U_unfilled_token 8 env "$PIN" QAB1225_PROMPT="$D/p_unfilled.txt" "$L" --check
/usr/bin/grep -v -F "$H32" "$BF" > "$D/b_nohead.md"; echo "  (W copy: capture lines naming #1232's head removed: $(/usr/bin/grep -c -F "$H32" "$BF") -> $(/usr/bin/grep -c -F "$H32" "$D/b_nohead.md"))"
run W_capture_missing_head 20 env "$PIN" QAB1225_BRIEF="$D/b_nohead.md" "$L" --check
/usr/bin/grep -v -F 'red-first 2-of-4' "$BF" > "$D/b_no24.md"; echo "  (O copy: capture lines naming 'red-first 2-of-4' removed: $(/usr/bin/grep -c -F 'red-first 2-of-4' "$BF") -> $(/usr/bin/grep -c -F 'red-first 2-of-4' "$D/b_no24.md"))"
run O_capture_missing_seat_item 30 env "$PIN" QAB1225_BRIEF="$D/b_no24.md" "$L" --check
doctor ticket 'PR #1231 is KS-1281.' 'PR #1231 is KS-12810.'; run T_ticket_statement 32 env "$PIN" QAB1225_PROMPT="$D/p_ticket.txt" "$L" --check
doctor tier '#1227 T2' '#1227 T1'; run I_tier_line 7 env "$PIN" QAB1225_PROMPT="$D/p_tier.txt" "$L" --check
doctor kw 'SAY WHOSE ORIGINATE ANSWERED' 'SAY SOMETHING'; run L_prompt_missing_keyword 33 env "$PIN" QAB1225_PROMPT="$D/p_kw.txt" "$L" --check
doctor legs 'NEVER send it to a stack you do not own' 'send it anywhere'; run K_legs_rule 35 env "$PIN" QAB1225_PROMPT="$D/p_legs.txt" "$L" --check
doctor legs2 'A SKIP or an rc 2 is NOT RUN, never a pass' 'A SKIP is fine'; run K2_skip_is_not_a_pass 35 env "$PIN" QAB1225_PROMPT="$D/p_legs2.txt" "$L" --check
doctor legs3 'legs 3/4/8 for #1225 are OWED' 'legs 3/4/8 for #1225 are green'; run K3_owed_not_green 35 env "$PIN" QAB1225_PROMPT="$D/p_legs3.txt" "$L" --check
doctor legs4 'you NEVER start Docker' 'you may start Docker'; run K4_never_start_docker 35 env "$PIN" QAB1225_PROMPT="$D/p_legs4.txt" "$L" --check
doctor red 'restore by bytes' 'restore somehow'; run B_redproof_rule 36 env "$PIN" QAB1225_PROMPT="$D/p_red.txt" "$L" --check
doctor rem 'FALSIFY the unreachability' 'ACCEPT the unreachability'; run B2_removal_proof 36 env "$PIN" QAB1225_PROMPT="$D/p_rem.txt" "$L" --check
doctor sub 'never as a green, never inferred' 'a green if it looks fine'; run X_substrate_unmeasured 37 env "$PIN" QAB1225_PROMPT="$D/p_sub.txt" "$L" --check
doctor sub2 'a DB NOT built by migration 001 now falls back to memory' 'a DB now works'; run X2_substrate_fallback 37 env "$PIN" QAB1225_PROMPT="$D/p_sub2.txt" "$L" --check
doctor memfb 'is a BLOCKING finding for a tier-2 GO' 'is a note'; run X3_memory_fallback_blocks 37 env "$PIN" QAB1225_PROMPT="$D/p_memfb.txt" "$L" --check
doctor memfb2 'memory fallback: <LOUD|SILENT>' 'memory: fine'; run X4_memory_fallback_verdict_clause 37 env "$PIN" QAB1225_PROMPT="$D/p_memfb2.txt" "$L" --check
doctor load 'KNOWN FALSE-RED (ticket KS-1155)' 'KNOWN FLAKE (ticket KS-1155)'; run Y_load_rule 38 env "$PIN" QAB1225_PROMPT="$D/p_load.txt" "$L" --check
doctor fpg 'the WARN is proven through a fake pg only' 'the WARN is proven'; run Y2_fake_pg_only 38 env "$PIN" QAB1225_PROMPT="$D/p_fpg.txt" "$L" --check
doctor c1142 'the `:1142` inner catch' 'the inner catch'; run Y3_inner_catch_1142 38 env "$PIN" QAB1225_PROMPT="$D/p_c1142.txt" "$L" --check
doctor holds 'NO Docker start and NO container action' 'Docker as needed'; run H_holds 39 env "$PIN" QAB1225_PROMPT="$D/p_holds.txt" "$L" --check
doctor narrow 'the ks256 `len12` and `credit` rows stay green' 'the ks256 rows are whatever'; run N_narrowing_len12_credit 40 env "$PIN" QAB1225_PROMPT="$D/p_narrow.txt" "$L" --check
doctor narrow2 'KS-1253 STAYS OPEN' 'KS-1253 may close'; run N2_ks1253_stays_open 40 env "$PIN" QAB1225_PROMPT="$D/p_narrow2.txt" "$L" --check
doctor stub 'never by name, never pid 1' 'by name is fine'; run S1_login_stub_cwd_ppid 41 env "$PIN" QAB1225_PROMPT="$D/p_stub.txt" "$L" --check
doctor stub2 'Report before/after counts' 'Report something'; run S2_login_stub_counts 41 env "$PIN" QAB1225_PROMPT="$D/p_stub2.txt" "$L" --check
doctor legit '#1229 (check-no-latest-tags.sh): (a)' '#1229: (a)'; run V_legitimate_shapes 42 env "$PIN" QAB1225_PROMPT="$D/p_legit.txt" "$L" --check
doctor go '`GO: merge #1225, #1227, #1229, #1231, #1232 batch`' '`GO: merge batch`'; run A_GO_string 26 env "$PIN" QAB1225_PROMPT="$D/p_go.txt" "$L" --check
doctor add '(1/2/3/2/2 = 10 over 10 paths)' '(as you like)'; run E_addendum 25 env "$PIN" QAB1225_PROMPT="$D/p_add.txt" "$L" --check
doctor subj '[QA -> Wednesday] TIER-2 BATCH GATE #1225-#1232 round 21' '[QA] gate'; run SJ_subject 23 env "$PIN" QAB1225_PROMPT="$D/p_subj.txt" "$L" --check
doctor et "$ET" "${ET%?}x"; run Z_end_tree_in_full 31 env "$PIN" QAB1225_PROMPT="$D/p_et.txt" "$L" --check
run NT_launch_non_tty 21 env "$PIN" "$L"
mkdir -p "$D/moved"; cp -p "$L" "$D/moved/"; run M_moved_launcher 2 "$D/moved/$(basename "$L")" --check
echo "== repin (--dry-run unless stated)"
run R1_positive_dry_run 0 bash "$R" "$L" "$SP" --dry-run
sed "s/|$H32|2|1\"$/|$STALE|2|1\"/" "$L" > "$D/L_stale.sh"; chmod 755 "$D/L_stale.sh"; echo "  (R2 copy: rows carrying the stale #1232 head: $(/usr/bin/grep -c -F "|$STALE|" "$D/L_stale.sh") — must be 1)"
run R2_stale_head 11 bash "$R" "$D/L_stale.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='[0-9a-f]*'$/DEVELOP_SHA='$H25'/" "$L" > "$D/L_devstale.sh"; chmod 755 "$D/L_devstale.sh"
run R3_pinned_develop_stale 10 bash "$R" "$D/L_devstale.sh" "$SP" --dry-run
if [ "$(/usr/bin/grep -c -F 'QA/Secuura-batch1225|coagent@agentmail.to|yes' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf)" = 0 ]; then
  run R4_real_run_unrouted 1 bash "$R" "$L" "$SP"
else echo "SKIP R4_real_run_unrouted — the routing line is present, a real run would launch"; fi
run R5_bad_scratchpad 9 bash "$R" "$L" /tmp --dry-run
run R7_no_launcher 9 bash "$R" "$D/nonexistent.sh" "$SP" --dry-run
mkdir -p "$D/kitcopy"; cp -p "$GS"/*.py "$GS"/*.sh "$GS"/*.txt "$GS"/*.md "$D/kitcopy/"; run R6_moved_kit_dry_run 0 bash "$D/kitcopy/repin_and_launch_gate21T2b.sh" "$D/kitcopy/$(basename "$L")" "$SP" --dry-run
/usr/bin/grep -c -F 'MOVED KIT' "$D/R6_moved_kit_dry_run.out" | sed 's/^/  (R6: MOVED KIT lines reported: /; s/$/ — must be 1)/'
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH"
[ "$bad" -eq 0 ]
