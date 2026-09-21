#!/bin/bash
# launcher_controls_gate16C.sh <launcher> <prompt> — refusing controls for the gate16C launcher: each control edits a COPY of the prompt (never the
# real files), or sets a QAB1148_* override, runs `--check`, and records the rc on its own line against the expected exit. Controls that pass the
# API phases cost ~60-80 s each (12 compare GETs + 54 contents GETs). Writes only into $G/controls_gate16C.XXXXXX/ and launcher_check_controls.out.
# Never launches (every call is --check or a non-TTY LAUNCH that must refuse at exit 21 after every guard passed). Derived from
# gatesets/2026-09-21_gate15_docs_comments/launcher_controls_gate15.sh (its control F edits the SECOND PR's compare line, which begins at column 1).
set -u
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate16C_seatC'
L="${1:?launcher}"; P="${2:?prompt}"
LAST="$(sed -n "s/^# QAB1148_CUR_DEV .*QAB1148_HEAD_\([0-9]*\) .*/\1/p" "$L" | head -1)"
C="$(mktemp -d "$G/controls_gate16C.XXXXXX")"; echo "$C" > "$G/controls_dir_gate16C.txt"
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
run A_missing_prompt 4 QAB1148_PROMPT="$C/absent.txt"
run B_brief_absent 3 QAB1148_BRIEF="$C/absent.md"
run C_wrong_head_last 6 "QAB1148_HEAD_$LAST=0000000000000000000000000000000000000001"
run D_curdev_old_parent_581ed7fa1 18 QAB1148_CUR_DEV=581ed7fa124b85c7c2da89ac05d52f99c2502911
run E_curdev_is_1148_head 19 QAB1148_CUR_DEV=c4a96cfe012196aa56765b6b26bd63b123980087
sed 's/^1150 \$MERGE_BASE ahead=1 behind=0 files=1$/1150 $MERGE_BASE ahead=1 behind=1 files=1/' "$L" > "$C/launcher_F.sh"; chmod 755 "$C/launcher_F.sh"
echo "F: launcher copy expecting behind=1 for #1150 (sed hit: $(/usr/bin/grep -c 'behind=1 files=1' "$C/launcher_F.sh"), real: $(/usr/bin/grep -c 'behind=1 files=1' "$L"))" | tee -a "$OUT"
t0=$(date -u +%H:%M:%SZ); "$C/launcher_F.sh" --check > "$C/F_behind1.out" 2>&1; rc=$?; [ "$rc" = 10 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "F_behind1 rc=$rc want=10 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/F_behind1.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy G '1s/ultrathink/think/'; run G_no_thinking_directive 8 QAB1148_PROMPT="$C/prompt_G.txt"
sedcopy H 's/PR #1148 is KS-864\./PR #1148 is ticket KS-864./'; echo "H count after: $(/usr/bin/grep -c -F 'PR #1148 is KS-864.' "$C/prompt_H.txt") (real $(/usr/bin/grep -c -F 'PR #1148 is KS-864.' "$P"))" | tee -a "$OUT"; run H_namespace_sentence_reworded 32 QAB1148_PROMPT="$C/prompt_H.txt"
sedcopy I 's/#1158 KS-855: TIER 1/#1158 KS-855: TIER 2/'; run I_1158_demoted_to_tier2 7 QAB1148_PROMPT="$C/prompt_I.txt"
sedcopy J 's/COMMA-separated/comma separated/g'; run J_mg2_phrase_reworded 25 QAB1148_PROMPT="$C/prompt_J.txt"
sedcopy K 's/RULE WHETHER IT BLOCKS/rule if it blocks/g'; run K_rule_whether_it_blocks_reworded 30 QAB1148_PROMPT="$C/prompt_K.txt"
sedcopy L2 's/THE TWO-SEAT ARTEFACTS/THE 2-SEAT ARTEFACTS/'; run L_byname_item9_reworded 33 QAB1148_PROMPT="$C/prompt_L2.txt"
sedcopy M 's/(twelve PRs; tier 2 floor, tier 1 = #1158, #1160, #1162, #1163, #1164, #1165: Seat C 16th test-only pins)/(twelve PRs)/'; run M_subject_prefix_shortened 23 QAB1148_PROMPT="$C/prompt_M.txt"
t0=$(date -u +%H:%M:%SZ); "$L" < /dev/null > "$C/N_nontty_launch.out" 2>&1; rc=$?; [ "$rc" = 21 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "N_nontty_launch rc=$rc want=21 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/N_nontty_launch.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy O 's/anchor-ambiguity/anchor ambiguity/g'; echo "O count after: $(/usr/bin/grep -c -F 'anchor-ambiguity' "$C/prompt_O.txt") (real $(/usr/bin/grep -c -F 'anchor-ambiguity' "$P"))" | tee -a "$OUT"; run O_both_token_reworded 30 QAB1148_PROMPT="$C/prompt_O.txt"
sedcopy P2 's#GATEWAY_URL=http://127.0.0.1:#GATEWAY_URL=http://localhost:#g'; run P_gateway_url_loopback_reworded 31 QAB1148_PROMPT="$C/prompt_P2.txt"
sedcopy Q 's/s-c16-batch/s-c16-octopus/g'; run Q_seat_worktree_reworded 28 QAB1148_PROMPT="$C/prompt_Q.txt"
sedcopy R 's/lsof -nP -iTCP:6000 -sTCP:LISTEN/lsof -nP -i TCP:6000 -s TCP:LISTEN/g'; run R_6000_lsof_reworded 29 QAB1148_PROMPT="$C/prompt_R.txt"
sedcopy S 's/PENDING-PR-X//; 1a\
PENDING-PR-X planted'; run S_partial_marker_planted 34 QAB1148_PROMPT="$C/prompt_S.txt"
sedcopy T 's/c4a96cfe012196aa56765b6b26bd63b123980087/c4a96cfe012196aa56765b6b26bd63b123980088/g'; run T_head_altered_in_prompt 20 QAB1148_PROMPT="$C/prompt_T.txt"
run POSITIVE_real_check 0
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH" | tee -a "$OUT"
