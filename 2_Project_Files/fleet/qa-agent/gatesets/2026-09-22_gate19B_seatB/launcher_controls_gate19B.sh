#!/bin/bash
# launcher_controls_gate19B.sh <launcher> <prompt> — the negative controls, each on a COPY of the prompt or an override (never the real files):
# C wrong head (last PR #1201) -> 6 · D develop at the 18th's pre-tip 581ed7fa1 (a stale sha; content judged: 17 disjoint / 18 changed / 19 landed —
# any of the three is a REFUSAL of a stale develop) · E develop at #1182's head (LANDED) -> 19 · S PARTIAL (PENDING-PR- planted) -> 34 · G no thinking
# directive -> 8 · L a by-name keyword reworded -> 33 · I #1198 demoted to tier 2 -> 7 · U `alone blob` reworded -> 35 (the PAIR guard) · W the
# KS-1164 instrument line reworded -> 36 · O RULE WHETHER IT BLOCKS reworded -> 30 · T a BOTH token altered -> 30 · N non-TTY launch -> 21 ·
# POSITIVE --check -> 0. (19C's U control wanted 35 and got 30: `--pair-blob` is ALSO a BOTH token, so the BOTH ladder fires first — here U rewords
# `alone blob`, which only the PAIR guard reads.)
set -u
L="$1"; P="$2"; D="$(mktemp -d /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f6fac5b6-1670-49a8-8c75-27176731d099/scratchpad/controls_gate19B.XXXXXX)"
echo "controls start $(date -u +%Y-%m-%dT%H:%M:%SZ) dir $D"
ok=0; bad=0
run() { name="$1"; want="$2"; shift 2; "$@" > "$D/$name.out" 2>&1; rc=$?; case " $want " in *" $rc "*) echo "OK   $name rc $rc (want $want)"; ok=$((ok+1));; *) echo "MISMATCH $name rc $rc (want $want)"; bad=$((bad+1));; esac; }
run C_wrong_head_last 6 env QAB1182_HEAD_1201=6e675cb815e984f9fa013f54ec4f214b552e56a0 bash "$L" --check
run D_curdev_stale_581ed7fa1 "17 18 19" env QAB1182_CUR_DEV=581ed7fa1 bash "$L" --check
run E_curdev_is_1182_head_LANDED 19 env QAB1182_CUR_DEV=8c413d78243a47d144f4049e6cd720a473d4dceb bash "$L" --check
sed 's/^ultrathink$/think/' "$P" > "$D/G.txt"; run G_no_thinking_directive 8 env QAB1182_PROMPT="$D/G.txt" bash "$L" --check
sed '3s/^/PENDING-PR-1201 /' "$P" > "$D/S.txt"; run S_partial_ladder 34 env QAB1182_PROMPT="$D/S.txt" bash "$L" --check
sed 's/RULE WHETHER IT BLOCKS/decide if it blocks/g' "$P" > "$D/O.txt"; run O_both_rule_reworded 30 env QAB1182_PROMPT="$D/O.txt" bash "$L" --check
sed 's/READ THE WHOLE TEST FILE/read the test file/g' "$P" > "$D/Lx.txt"; run L_byname_reworded 33 env QAB1182_PROMPT="$D/Lx.txt" bash "$L" --check
sed 's/#1198 T1/#1198 T2/' "$P" > "$D/I.txt"; run I_1198_demoted 7 env QAB1182_PROMPT="$D/I.txt" bash "$L" --check
sed 's/alone blob/lone blob/g' "$P" > "$D/U.txt"; run U_aloneblob_reworded 35 env QAB1182_PROMPT="$D/U.txt" bash "$L" --check
sed 's/NOT the instrument/not an instrument/g' "$P" > "$D/W.txt"; run W_instrument_reworded 36 env QAB1182_PROMPT="$D/W.txt" bash "$L" --check
sed 's/amend1164_19/amend1164_20/g' "$P" > "$D/T.txt"; run T_both_token_altered 30 env QAB1182_PROMPT="$D/T.txt" bash "$L" --check
run N_nontty_launch 21 bash "$L" < /dev/null
run POSITIVE_check 0 bash "$L" --check
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH (dir $D)"
