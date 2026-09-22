#!/bin/bash
# launcher_controls_gate18B.sh <launcher> <prompt> — refusing controls for the gate18B launcher: each control edits a COPY of the prompt / capture
# (never the real files), or sets a QAB1170_* override, runs `--check`, and records the rc on its own line against the expected exit. Controls that
# pass the API phases cost ~100 s each (7 compare GETs + 46 contents GETs). Writes only into $G/controls_gate18B.XXXXXX/ and
# launcher_check_controls.out. Never launches (every call is --check or a non-TTY LAUNCH that must refuse at exit 21 after every guard passed).
# Derived from gatesets/2026-09-22_gate16B_seatB/launcher_controls_gate16B.sh (control F edits the SECOND PR's compare line; U zeroes the END_TREE).
set -u
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate18B_seatB'
L="${1:?launcher}"; P="${2:?prompt}"
B="$G/mail_gate18B_ready.md"
LAST="$(sed -n "s/^# QAB1170_CUR_DEV .*QAB1170_HEAD_\([0-9]*\) .*/\1/p" "$L" | head -1)"
C="$(mktemp -d "$G/controls_gate18B.XXXXXX")"; echo "$C" > "$G/controls_dir_gate18B.txt"
OUT="$G/launcher_check_controls.out"; : > "$OUT"
ok=0; bad=0
run() { # name expected-rc [env assignments...]
  local name="$1" want="$2"; shift 2
  local t0; t0=$(date -u +%H:%M:%SZ)
  env "$@" "$L" --check > "$C/$name.out" 2>&1
  local rc=$?
  local verdict; [ "$rc" = "$want" ] && { verdict=OK; ok=$((ok+1)); } || { verdict=MISMATCH; bad=$((bad+1)); }
  echo "$name rc=$rc want=$want $verdict ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/$name.out" | cut -c1-160)" | tee -a "$OUT"
}
sedcopy() { sed "$2" "$P" > "$C/prompt_$1.txt"; }
echo "controls start $(date -u +%Y-%m-%dT%H:%M:%SZ) dir $C launcher $L last PR $LAST" | tee -a "$OUT"
run A_missing_prompt 4 QAB1170_PROMPT="$C/absent.txt"
run B_brief_absent 3 QAB1170_BRIEF="$C/absent.md"
run C_wrong_head_last 6 "QAB1170_HEAD_$LAST=0000000000000000000000000000000000000001"
run D_curdev_the_parent_3916eacd1 18 QAB1170_CUR_DEV=3916eacd12af23bfd464440b4c770f7da0f2dd96
run E_curdev_is_1170_head 19 QAB1170_CUR_DEV=3e9f7d7b707da88e666ff94c769658f2ba3894b8
sed 's/^1172 \$MERGE_BASE ahead=1 behind=1 files=1$/1172 $MERGE_BASE ahead=1 behind=2 files=1/' "$L" > "$C/launcher_F.sh"; chmod 755 "$C/launcher_F.sh"
echo "F: launcher copy expecting behind=2 for #1172 (sed hit: $(/usr/bin/grep -c 'behind=2 files=1' "$C/launcher_F.sh"), real: $(/usr/bin/grep -c 'behind=2 files=1' "$L"))" | tee -a "$OUT"
t0=$(date -u +%H:%M:%SZ); "$C/launcher_F.sh" --check > "$C/F_behind2.out" 2>&1; rc=$?; [ "$rc" = 10 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "F_behind2 rc=$rc want=10 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/F_behind2.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy G '1s/ultrathink/think/'; run G_no_thinking_directive 8 QAB1170_PROMPT="$C/prompt_G.txt"
sedcopy H 's/PR #1170 is KS-1118\./PR #1170 is ticket KS-1118./'; echo "H count after: $(/usr/bin/grep -c -F 'PR #1170 is KS-1118.' "$C/prompt_H.txt") (real $(/usr/bin/grep -c -F 'PR #1170 is KS-1118.' "$P"))" | tee -a "$OUT"; run H_namespace_sentence_reworded 32 QAB1170_PROMPT="$C/prompt_H.txt"
sedcopy I 's/#1170 KS-1118: TIER 2/#1170 KS-1118: TIER 1/'; run I_1170_promoted_to_tier1 7 QAB1170_PROMPT="$C/prompt_I.txt"
sedcopy J 's/ONE equality target PER PR FILE/one equality target per PR file/g'; run J_mg1_phrase_reworded 25 QAB1170_PROMPT="$C/prompt_J.txt"
sedcopy K 's/RULE WHETHER IT BLOCKS/rule if it blocks/g'; run K_rule_whether_it_blocks_reworded 30 QAB1170_PROMPT="$C/prompt_K.txt"
sedcopy L2 's/THE TWO-SEAT ARTEFACTS/THE TWO-SEAT RECORDS/'; run L_byname_item9_reworded 33 QAB1170_PROMPT="$C/prompt_L2.txt"
sedcopy M 's/(seven PRs; tier 1 = #1174, #1177, #1178: Seat B 18th, one product change)/(seven PRs)/'; run M_subject_prefix_shortened 23 QAB1170_PROMPT="$C/prompt_M.txt"
t0=$(date -u +%H:%M:%SZ); "$L" < /dev/null > "$C/N_nontty_launch.out" 2>&1; rc=$?; [ "$rc" = 21 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "N_nontty_launch rc=$rc want=21 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/N_nontty_launch.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy O 's/threadTokenMint/threadtokenmint/g'; echo "O count after: $(/usr/bin/grep -c -F 'threadTokenMint' "$C/prompt_O.txt") (real $(/usr/bin/grep -c -F 'threadTokenMint' "$P"))" | tee -a "$OUT"; run O_both_token_recased 30 QAB1170_PROMPT="$C/prompt_O.txt"
sedcopy P2 's#GATEWAY_URL=http://127.0.0.1:#GATEWAY_URL=http://localhost:#g'; run P_gateway_url_loopback_reworded 31 QAB1170_PROMPT="$C/prompt_P2.txt"
sedcopy Q 's/s-b18-batch/s-b18-octopus/g'; run Q_seat_worktree_reworded 28 QAB1170_PROMPT="$C/prompt_Q.txt"
sedcopy R 's/lsof -nP -iTCP:4003 -sTCP:LISTEN/lsof -nP -i TCP:4003 -s TCP:LISTEN/g'; run R_4003_lsof_reworded 29 QAB1170_PROMPT="$C/prompt_R.txt"
sedcopy S 's/PENDING-PR-X//; 1a\
PENDING-PR-X planted'; run S_partial_marker_planted 34 QAB1170_PROMPT="$C/prompt_S.txt"
sedcopy T 's/^\(#1179 Blockchain\/Dev\/packages\/shared\/src\/__tests__\/ks727-errorhandler-class-guard.test.ts \)35eb27404fd615886d3f03ba7e691be97051f1ee/\1000000000000000000000000000000000000000/'; echo "T count after (the #1179 head blob line): $(/usr/bin/grep -c -F '35eb27404fd615886d3f03ba7e691be97051f1ee' "$C/prompt_T.txt") (real $(/usr/bin/grep -c -F '35eb27404fd615886d3f03ba7e691be97051f1ee' "$P"))" | tee -a "$OUT"; run T_head_blob_still_named_elsewhere 0 QAB1170_PROMPT="$C/prompt_T.txt"
sedcopy U 's/76a88d9ddfa4f50098aa639a1056c5c9387aeb18/0000000000000000000000000000000000000000/g'; echo "U count after (the END_TREE zeroed everywhere): $(/usr/bin/grep -c -F '76a88d9ddfa4f50098aa639a1056c5c9387aeb18' "$C/prompt_U.txt") (real $(/usr/bin/grep -c -F '76a88d9ddfa4f50098aa639a1056c5c9387aeb18' "$P"))" | tee -a "$OUT"; run U_end_tree_zeroed 30 QAB1170_PROMPT="$C/prompt_U.txt"
run POSITIVE_real_check 0
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH" | tee -a "$OUT"
