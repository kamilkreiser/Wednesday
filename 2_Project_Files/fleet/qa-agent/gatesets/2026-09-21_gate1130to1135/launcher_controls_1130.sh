#!/bin/bash
# launcher_controls_1130.sh — refusing controls for launch_qa_secuura_batch1130-1135.sh: each control edits a COPY of the prompt / capture (never
# the real files), or sets a QAB1130_* override, runs `--check`, and records the rc on its own line against the expected exit. Controls that pass
# the API phases cost ~90 s each. Writes only into $G/controls_1130/ and launcher_check_controls.out. Never launches (every call is --check or a
# non-TTY LAUNCH that must refuse at exit 21 after every guard passed).
set -u
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135'
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1130-1135.sh'
P='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1130-1135.prompt.txt'
B="$G/mail_batch1130_ready.md"
C="$(mktemp -d "$G/controls_1130.XXXXXX")"; echo "$C" > "$G/controls_dir_1130.txt"
OUT="$G/launcher_check_controls.out"; : > "$OUT"
ok=0; bad=0
run() { # name expected-rc [env assignments...] -- description
  local name="$1" want="$2"; shift 2
  local t0; t0=$(date -u +%H:%M:%SZ)
  env "$@" "$L" --check > "$C/$name.out" 2>&1
  local rc=$?
  local verdict; [ "$rc" = "$want" ] && { verdict=OK; ok=$((ok+1)); } || { verdict=MISMATCH; bad=$((bad+1)); }
  echo "$name rc=$rc want=$want $verdict ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/$name.out" | cut -c1-160)" | tee -a "$OUT"
}
sedcopy() { # name sed-expr -> $C/prompt_<name>.txt ; prints the count of the needle after the edit
  sed "$2" "$P" > "$C/prompt_$1.txt"
}
echo "controls start $(date -u +%Y-%m-%dT%H:%M:%SZ) dir $C" | tee -a "$OUT"
run A_missing_prompt 4 QAB1130_PROMPT="$C/absent.txt"
run B_brief_absent 3 QAB1130_BRIEF="$C/absent.md"
run C_wrong_head_1135 6 QAB1130_HEAD_1135=0000000000000000000000000000000000000001
run D_curdev_old_7be81d5c9 18 QAB1130_CUR_DEV=7be81d5c9b109959b559e03652fb092c12de58e8
run E_curdev_is_1132_head 19 QAB1130_CUR_DEV=39bbf29a564fcc6b68ffe50607e29df251b8b180
sed 's/^1130 \$MERGE_BASE ahead=1 behind=0 files=1$/1130 $MERGE_BASE ahead=1 behind=1 files=1/' "$L" > "$C/launcher_F.sh"; chmod 755 "$C/launcher_F.sh"
echo "F: launcher copy expecting behind=1 for #1130 (sed hit: $(/usr/bin/grep -c 'behind=1 files=1' "$C/launcher_F.sh"), real: $(/usr/bin/grep -c 'behind=1 files=1' "$L"))" | tee -a "$OUT"
t0=$(date -u +%H:%M:%SZ); "$C/launcher_F.sh" --check > "$C/F_behind1.out" 2>&1; rc=$?; [ "$rc" = 10 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "F_behind1 rc=$rc want=10 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/F_behind1.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy G '1s/ultrathink/think/'; run G_no_thinking_directive 8 QAB1130_PROMPT="$C/prompt_G.txt"
sedcopy H 's/PR #1135 is KS-1236 + KS-1006\./PR #1135 is KS-1236 and KS-1006./'; echo "H count after: $(/usr/bin/grep -c -F 'PR #1135 is KS-1236 + KS-1006.' "$C/prompt_H.txt") (real $(/usr/bin/grep -c -F 'PR #1135 is KS-1236 + KS-1006.' "$P"))" | tee -a "$OUT"; run H_namespace_sentence_reworded 32 QAB1130_PROMPT="$C/prompt_H.txt"
sedcopy I 's/#1132 KS-958: TIER 1/#1132 KS-958: TIER 2/'; run I_1132_demoted_to_tier2 7 QAB1130_PROMPT="$C/prompt_I.txt"
sedcopy J 's/COMMA-separated/comma separated/g'; run J_comma_separated_reworded 25 QAB1130_PROMPT="$C/prompt_J.txt"
sedcopy K 's/RULE WHETHER IT BLOCKS/rule if it blocks/g'; run K_rule_whether_it_blocks_reworded 30 QAB1130_PROMPT="$C/prompt_K.txt"
sedcopy L2 's/THE OTHER MAPPER/THE SECOND MAPPER/'; run L_byname_item6_reworded 33 QAB1130_PROMPT="$C/prompt_L2.txt"
sedcopy M 's/\[QA -> Wednesday\] BATCH GATE #1130-#1135 (six PRs; tier 1 = #1132, #1133, #1134, #1135)/[QA -> Wednesday] BATCH GATE #1130-#1135 (six PRs)/'; run M_subject_prefix_shortened 23 QAB1130_PROMPT="$C/prompt_M.txt"
t0=$(date -u +%H:%M:%SZ); "$L" < /dev/null > "$C/N_nontty_launch.out" 2>&1; rc=$?; [ "$rc" = 21 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "N_nontty_launch rc=$rc want=21 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/N_nontty_launch.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy O 's/CONNECTORIDDROPPED/CONNECTORID-DROPPED/g'; echo "O count after: $(/usr/bin/grep -c -F 'CONNECTORIDDROPPED' "$C/prompt_O.txt") (real $(/usr/bin/grep -c -F 'CONNECTORIDDROPPED' "$P"))" | tee -a "$OUT"; run O_both_token_split 30 QAB1130_PROMPT="$C/prompt_O.txt"
sedcopy P2 's#GATEWAY_URL=http://127.0.0.1:#GATEWAY_URL=http://localhost:#g'; run P_gateway_url_loopback_reworded 31 QAB1130_PROMPT="$C/prompt_P2.txt"
sedcopy Q 's/s-b14-batch/s-b14-octopus/g'; run Q_seat_worktree_reworded 28 QAB1130_PROMPT="$C/prompt_Q.txt"
sedcopy R 's/lsof -nP -iTCP:4003 -sTCP:LISTEN/lsof -nP -i TCP:4003 -s TCP:LISTEN/g'; run R_4003_lsof_reworded 29 QAB1130_PROMPT="$C/prompt_R.txt"
sedcopy S 's/#1132 TWO/#1132 two/g'; run S_1132_TWO_reworded 25 QAB1130_PROMPT="$C/prompt_S.txt"
run POSITIVE_real_check 0
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH" | tee -a "$OUT"
