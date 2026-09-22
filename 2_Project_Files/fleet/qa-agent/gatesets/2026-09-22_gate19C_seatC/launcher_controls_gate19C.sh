#!/bin/bash
# launcher_controls_gate19C.sh <launcher> <prompt> — the negative controls, each on a COPY of the prompt or an override (never the real files):
# C wrong head (last PR) -> 6 · D develop at the 18th's pre-tip 581ed7fa1 (a stale sha; content judged) -> 17/18/19 · E develop at #1180's head
# (LANDED) -> 19 · S PARTIAL (PENDING-PR- planted) -> 34 · G no thinking directive -> 8 · L a by-name keyword reworded -> 33 · I #1190 demoted to
# tier 2 -> 7 · U --pair-blob reworded -> 35 · O a BOTH token reworded -> 30 · N non-TTY launch -> 21 · POSITIVE --check -> 0.
set -u
L="$1"; P="$2"; D="$(mktemp -d /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f6fac5b6-1670-49a8-8c75-27176731d099/scratchpad/controls_gate19C.XXXXXX)"
echo "controls start $(date -u +%Y-%m-%dT%H:%M:%SZ) dir $D"
ok=0; bad=0
run() { name="$1"; want="$2"; shift 2; "$@" > "$D/$name.out" 2>&1; rc=$?; if [ "$rc" = "$want" ]; then echo "OK   $name rc $rc (want $want)"; ok=$((ok+1)); else echo "MISMATCH $name rc $rc (want $want)"; bad=$((bad+1)); fi; }
run C_wrong_head_last 6 env QAB1180_HEAD_1197=661da6c23e233c682f30c3de83b71ef46c8a5bb0 bash "$L" --check
run D_curdev_stale_581ed7fa1 18 env QAB1180_CUR_DEV=581ed7fa1 bash "$L" --check
run E_curdev_is_1180_head_LANDED 19 env QAB1180_CUR_DEV=ad86ffdbf504c250c1144f7d59ddcdba4966568d bash "$L" --check
sed 's/^ultrathink$/think/' "$P" > "$D/G.txt"; run G_no_thinking_directive 8 env QAB1180_PROMPT="$D/G.txt" bash "$L" --check
sed '3s/^/PENDING-PR-1197 /' "$P" > "$D/S.txt"; run S_partial_ladder 34 env QAB1180_PROMPT="$D/S.txt" bash "$L" --check
sed 's/RULE WHETHER IT BLOCKS/decide if it blocks/g' "$P" > "$D/O.txt"; run O_both_rule_reworded 30 env QAB1180_PROMPT="$D/O.txt" bash "$L" --check
sed 's/READ THE WHOLE TEST FILE/read the test file/g' "$P" > "$D/Lx.txt"; run L_byname_reworded 33 env QAB1180_PROMPT="$D/Lx.txt" bash "$L" --check
sed 's/#1190 T1/#1190 T2/' "$P" > "$D/I.txt"; run I_1190_demoted 7 env QAB1180_PROMPT="$D/I.txt" bash "$L" --check
sed 's/--pair-blob/--pairblob/g' "$P" > "$D/U.txt"; run U_pairblob_reworded 30 env QAB1180_PROMPT="$D/U.txt" bash "$L" --check
sed 's/5772145479/5772145470/g' "$P" > "$D/T.txt"; run T_both_token_altered 30 env QAB1180_PROMPT="$D/T.txt" bash "$L" --check
run N_nontty_launch 21 bash "$L" < /dev/null
run POSITIVE_check 0 bash "$L" --check
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH (dir $D)"
