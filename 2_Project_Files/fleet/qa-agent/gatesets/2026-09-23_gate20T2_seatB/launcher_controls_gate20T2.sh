#!/bin/bash
# launcher_controls_gate20T2.sh <launcher> <prompt> <scratch dir> — the negative controls, each on a COPY of the prompt / the launcher or an override
# (never the real files):
# C wrong head (last PR #1206) -> 6 · D develop at round 19's base 3bad652d1 (a stale sha; content judged: 17 disjoint / 18 changed / 19 landed — any
# of the three is a REFUSAL of a stale develop) · E develop at #1202's head (LANDED) -> 19 · S PARTIAL (PENDING-PR- planted in the prompt) -> 34 ·
# P5a a launcher COPY whose PR-5 row head is PENDING (not 40-hex) -> 34 · P5b a launcher COPY with the PR-5 row REMOVED (three rows) -> 34 · G no
# thinking directive -> 8 · L a by-name keyword reworded -> 33 · I #1203 demoted to tier 1 -> 7 · U `planted-comment control` reworded -> 35 (the
# token-instrument guard) · W `DIFFERENT subsets` reworded -> 36 (the bash-kind guard) · O RULE WHETHER IT BLOCKS reworded -> 30 · T a BOTH token
# altered (c4tokens.js) -> 30 · N non-TTY launch -> 21 · POSITIVE --check -> 0.
set -u
L="$1"; P="$2"; SP="$3"
case "$SP" in /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/*/scratchpad*) ;; *) echo "REFUSING: $SP is not a scratchpad"; exit 9;; esac
D="$(mktemp -d "$SP/controls_gate20T2.XXXXXX")"
echo "controls start $(date -u +%Y-%m-%dT%H:%M:%SZ) dir $D"
ok=0; bad=0
run() { name="$1"; want="$2"; shift 2; "$@" > "$D/$name.out" 2>&1; rc=$?; case " $want " in *" $rc "*) echo "OK   $name rc $rc (want $want)"; ok=$((ok+1));; *) echo "MISMATCH $name rc $rc (want $want)"; bad=$((bad+1));; esac; }
run C_wrong_head_last 6 env QAB1202_HEAD_1206=bfbaf4366897a97ec20c2f88e67448597739ce40 bash "$L" --check
run D_curdev_stale_3bad652d1 "17 18 19" env QAB1202_CUR_DEV=3bad652d17cf111c1e2e1bed1ae7686894637487 bash "$L" --check
run E_curdev_is_1202_head_LANDED 19 env QAB1202_CUR_DEV=49f419e625d7304f724b4a604f542827b7772458 bash "$L" --check
sed '3s/^/PENDING-PR-5 /' "$P" > "$D/S.txt"; run S_partial_prompt 34 env QAB1202_PROMPT="$D/S.txt" bash "$L" --check
sed -E 's/^(  "1206\|KS-1139\|[^|]*\|)[0-9a-f]{40}(\|1")$/  "PENDING|KS-1139|refs\/heads\/feature\/ks-1139-pending|PENDING-PR-5|1"/' "$L" > "$D/L_p5a.sh"
/usr/bin/grep -c 'PENDING-PR-5' "$D/L_p5a.sh" > "$D/L_p5a.count" 2>&1; echo "  (P5a copy: PENDING row count $(cat "$D/L_p5a.count") — must be 1 for the control to mean anything)"
run P5a_pr5_row_pending 34 bash "$D/L_p5a.sh" --check
/usr/bin/grep -v -E '^  "1206\|KS-1139\|' "$L" > "$D/L_p5b.sh"
echo "  (P5b copy: rows naming 1206 left: $(/usr/bin/grep -c -E '^  "1206\|' "$D/L_p5b.sh") — must be 0; the real launcher: $(/usr/bin/grep -c -E '^  "1206\|' "$L") — must be 1)"
run P5b_pr5_row_removed 34 bash "$D/L_p5b.sh" --check
sed 's/^ultrathink$/think/' "$P" > "$D/G.txt"; run G_no_thinking_directive 8 env QAB1202_PROMPT="$D/G.txt" bash "$L" --check
sed 's/RULE WHETHER IT BLOCKS/decide if it blocks/g' "$P" > "$D/O.txt"; run O_both_rule_reworded 30 env QAB1202_PROMPT="$D/O.txt" bash "$L" --check
sed 's/READ THE WHOLE TEST FILE/read the test file/g' "$P" > "$D/Lx.txt"; run L_byname_reworded 33 env QAB1202_PROMPT="$D/Lx.txt" bash "$L" --check
sed 's/#1203 T2/#1203 T1/' "$P" > "$D/I.txt"; run I_1203_regraded 7 env QAB1202_PROMPT="$D/I.txt" bash "$L" --check
sed 's/planted-comment control/comment control/g' "$P" > "$D/U.txt"; run U_token_instrument_reworded 35 env QAB1202_PROMPT="$D/U.txt" bash "$L" --check
sed 's/DIFFERENT subsets/the same subsets/g' "$P" > "$D/W.txt"; run W_bashkind_reworded 36 env QAB1202_PROMPT="$D/W.txt" bash "$L" --check
sed 's/c4tokens\.js/c5tokens.js/g' "$P" > "$D/T.txt"; run T_both_token_altered 30 env QAB1202_PROMPT="$D/T.txt" bash "$L" --check
run N_nontty_launch 21 bash "$L" < /dev/null
run POSITIVE_check 0 bash "$L" --check
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH (dir $D)"
