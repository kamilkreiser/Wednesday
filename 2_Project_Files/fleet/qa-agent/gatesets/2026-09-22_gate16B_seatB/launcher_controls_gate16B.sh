#!/bin/bash
# launcher_controls_gate16B.sh <launcher> <prompt> — refusing controls for the gate16B launcher: each control edits a COPY of the prompt / capture
# (never the real files), or sets a QAB1147_* override, runs `--check`, and records the rc on its own line against the expected exit. Controls that
# pass the API phases cost ~100 s each (8 compare GETs + 49 contents GETs). Writes only into $G/controls_gate16B.XXXXXX/ and
# launcher_check_controls.out. Never launches (every call is --check or a non-TTY LAUNCH that must refuse at exit 21 after every guard passed).
# Derived from gatesets/2026-09-21_gate15_docs_comments/launcher_controls_gate15.sh (control F edits the SECOND PR's compare line, column 1).
set -u
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate16B_seatB'
L="${1:?launcher}"; P="${2:?prompt}"
B="$G/mail_gate16B_ready.md"
LAST="$(sed -n "s/^# QAB1147_CUR_DEV .*QAB1147_HEAD_\([0-9]*\) .*/\1/p" "$L" | head -1)"
C="$(mktemp -d "$G/controls_gate16B.XXXXXX")"; echo "$C" > "$G/controls_dir_gate16B.txt"
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
run A_missing_prompt 4 QAB1147_PROMPT="$C/absent.txt"
run B_brief_absent 3 QAB1147_BRIEF="$C/absent.md"
run C_wrong_head_last 6 "QAB1147_HEAD_$LAST=0000000000000000000000000000000000000001"
run D_curdev_old_parent_581ed7fa1 18 QAB1147_CUR_DEV=581ed7fa124b85c7c2da89ac05d52f99c2502911
run E_curdev_is_1147_head 19 QAB1147_CUR_DEV=e456ffb5e9e1e1525f155864452c0aa2cad8752b
sed 's/^1149 \$MERGE_BASE ahead=1 behind=0 files=1$/1149 $MERGE_BASE ahead=1 behind=1 files=1/' "$L" > "$C/launcher_F.sh"; chmod 755 "$C/launcher_F.sh"
echo "F: launcher copy expecting behind=1 for #1149 (sed hit: $(/usr/bin/grep -c 'behind=1 files=1' "$C/launcher_F.sh"), real: $(/usr/bin/grep -c 'behind=1 files=1' "$L"))" | tee -a "$OUT"
t0=$(date -u +%H:%M:%SZ); "$C/launcher_F.sh" --check > "$C/F_behind1.out" 2>&1; rc=$?; [ "$rc" = 10 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "F_behind1 rc=$rc want=10 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/F_behind1.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy G '1s/ultrathink/think/'; run G_no_thinking_directive 8 QAB1147_PROMPT="$C/prompt_G.txt"
sedcopy H 's/PR #1147 is KS-928\./PR #1147 is ticket KS-928./'; echo "H count after: $(/usr/bin/grep -c -F 'PR #1147 is KS-928.' "$C/prompt_H.txt") (real $(/usr/bin/grep -c -F 'PR #1147 is KS-928.' "$P"))" | tee -a "$OUT"; run H_namespace_sentence_reworded 32 QAB1147_PROMPT="$C/prompt_H.txt"
sedcopy I 's/#1147 KS-928: TIER 2/#1147 KS-928: TIER 1/'; run I_1147_promoted_to_tier1 7 QAB1147_PROMPT="$C/prompt_I.txt"
sedcopy J 's/ONE equality target PER PR FILE/one equality target per PR file/g'; run J_mg1_phrase_reworded 25 QAB1147_PROMPT="$C/prompt_J.txt"
sedcopy K 's/RULE WHETHER IT BLOCKS/rule if it blocks/g'; run K_rule_whether_it_blocks_reworded 30 QAB1147_PROMPT="$C/prompt_K.txt"
sedcopy L2 's/THE TWO-SEAT ARTEFACTS/THE TWO-SEAT RECORDS/'; run L_byname_item9_reworded 33 QAB1147_PROMPT="$C/prompt_L2.txt"
sedcopy M 's/(eight PRs; tier 2 floor, tier 1 = #1161: Seat B 16th test-only pins)/(eight PRs)/'; run M_subject_prefix_shortened 23 QAB1147_PROMPT="$C/prompt_M.txt"
t0=$(date -u +%H:%M:%SZ); "$L" < /dev/null > "$C/N_nontty_launch.out" 2>&1; rc=$?; [ "$rc" = 21 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "N_nontty_launch rc=$rc want=21 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/N_nontty_launch.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy O 's/threadTokenMint/threadtokenmint/g'; echo "O count after: $(/usr/bin/grep -c -F 'threadTokenMint' "$C/prompt_O.txt") (real $(/usr/bin/grep -c -F 'threadTokenMint' "$P"))" | tee -a "$OUT"; run O_both_token_recased 30 QAB1147_PROMPT="$C/prompt_O.txt"
sedcopy P2 's#GATEWAY_URL=http://127.0.0.1:#GATEWAY_URL=http://localhost:#g'; run P_gateway_url_loopback_reworded 31 QAB1147_PROMPT="$C/prompt_P2.txt"
sedcopy Q 's/s-b16-batch/s-b16-octopus/g'; run Q_seat_worktree_reworded 28 QAB1147_PROMPT="$C/prompt_Q.txt"
sedcopy R 's/lsof -nP -iTCP:4003 -sTCP:LISTEN/lsof -nP -i TCP:4003 -s TCP:LISTEN/g'; run R_4003_lsof_reworded 29 QAB1147_PROMPT="$C/prompt_R.txt"
sedcopy S 's/PENDING-PR-X//; 1a\
PENDING-PR-X planted'; run S_partial_marker_planted 34 QAB1147_PROMPT="$C/prompt_S.txt"
sedcopy T 's/^\(#1161 Blockchain\/Dev\/services\/security\/src\/__tests__\/ks975-malformed-sub-is-refused.test.ts \)60015bd01b6ab9da09e223214322b38997dd94a3/\1000000000000000000000000000000000000000/'; echo "T count after (the #1161 head blob line): $(/usr/bin/grep -c -F '60015bd01b6ab9da09e223214322b38997dd94a3' "$C/prompt_T.txt") (real $(/usr/bin/grep -c -F '60015bd01b6ab9da09e223214322b38997dd94a3' "$P"))" | tee -a "$OUT"; run T_head_blob_still_named_elsewhere 0 QAB1147_PROMPT="$C/prompt_T.txt"
run POSITIVE_real_check 0
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH" | tee -a "$OUT"
