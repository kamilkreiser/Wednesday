#!/bin/bash
# launcher_controls_gate18C.sh <launcher> <prompt> — refusing controls for the gate18C launcher: each control edits a COPY of the prompt (never the
# real files), or sets a QAB1167_* override, runs `--check`, and records the rc on its own line against the expected exit. Controls that pass the
# API phases cost ~60-90 s each (6 compare GETs + 42 contents GETs). Writes only into $G/controls_gate18C.XXXXXX/ and launcher_check_controls.out.
# Never launches (every call is --check or a non-TTY LAUNCH that must refuse at exit 21 after every guard passed). Derived from
# gatesets/2026-09-22_gate16C_seatC/launcher_controls_gate16C.sh (its control F edits the SECOND PR's compare line, which begins at column 1).
set -u
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate18C_seatC'
L="${1:?launcher}"; P="${2:?prompt}"
LAST="$(sed -n "s/^# QAB1167_CUR_DEV .*QAB1167_HEAD_\([0-9]*\) .*/\1/p" "$L" | head -1)"
C="$(mktemp -d "$G/controls_gate18C.XXXXXX")"; echo "$C" > "$G/controls_dir_gate18C.txt"
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
run A_missing_prompt 4 QAB1167_PROMPT="$C/absent.txt"
run B_brief_absent 3 QAB1167_BRIEF="$C/absent.md"
run C_wrong_head_last 6 "QAB1167_HEAD_$LAST=0000000000000000000000000000000000000001"
run D_curdev_old_parent_3916eacd1 18 QAB1167_CUR_DEV=3916eacd12af23bfd464440b4c770f7da0f2dd96
run E_curdev_is_1167_head 19 QAB1167_CUR_DEV=4f2b87547d8060646763a5f15ef4a165a1e436bd
run E2_curdev_is_1173_head_pair_second 19 QAB1167_CUR_DEV=611c9d504463eacd12c37e0be8af11ba67e65c82
sed 's/^1168 \$MERGE_BASE ahead=1 behind=0 files=1$/1168 $MERGE_BASE ahead=1 behind=1 files=1/' "$L" > "$C/launcher_F.sh"; chmod 755 "$C/launcher_F.sh"
echo "F: launcher copy expecting behind=1 for #1168 (sed hit: $(/usr/bin/grep -c 'behind=1 files=1' "$C/launcher_F.sh"), real: $(/usr/bin/grep -c 'behind=1 files=1' "$L"))" | tee -a "$OUT"
t0=$(date -u +%H:%M:%SZ); "$C/launcher_F.sh" --check > "$C/F_behind1.out" 2>&1; rc=$?; [ "$rc" = 10 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "F_behind1 rc=$rc want=10 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/F_behind1.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy G '1s/ultrathink/think/'; run G_no_thinking_directive 8 QAB1167_PROMPT="$C/prompt_G.txt"
sedcopy H 's/PR #1167 is KS-947\./PR #1167 is ticket KS-947./'; echo "H count after: $(/usr/bin/grep -c -F 'PR #1167 is KS-947.' "$C/prompt_H.txt") (real $(/usr/bin/grep -c -F 'PR #1167 is KS-947.' "$P"))" | tee -a "$OUT"; run H_namespace_sentence_reworded 32 QAB1167_PROMPT="$C/prompt_H.txt"
sedcopy I 's/#1171 KS-1231: TIER 1/#1171 KS-1231: TIER 2/'; run I_1171_demoted_to_tier2 7 QAB1167_PROMPT="$C/prompt_I.txt"
sedcopy J 's/COMMA-separated/comma separated/g'; run J_mg2_phrase_reworded 25 QAB1167_PROMPT="$C/prompt_J.txt"
sedcopy K 's/RULE WHETHER IT BLOCKS/rule if it blocks/g'; run K_rule_whether_it_blocks_reworded 30 QAB1167_PROMPT="$C/prompt_K.txt"
sedcopy L2 's/THE TWO-SEAT ARTEFACTS/THE 2-SEAT ARTEFACTS/'; run L_byname_item9_reworded 33 QAB1167_PROMPT="$C/prompt_L2.txt"
sedcopy M 's/(six PRs; tier 1 = #1167, #1171, #1173, #1175: Seat C 18th — KS-947 auth-surface pin + three code_patch product PRs; tier 2 = #1168, #1169)/(six PRs)/'; run M_subject_prefix_shortened 23 QAB1167_PROMPT="$C/prompt_M.txt"
t0=$(date -u +%H:%M:%SZ); "$L" < /dev/null > "$C/N_nontty_launch.out" 2>&1; rc=$?; [ "$rc" = 21 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "N_nontty_launch rc=$rc want=21 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/N_nontty_launch.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy O 's/anchor-ambiguity/anchor ambiguity/g'; echo "O count after: $(/usr/bin/grep -c -F 'anchor-ambiguity' "$C/prompt_O.txt") (real $(/usr/bin/grep -c -F 'anchor-ambiguity' "$P"))" | tee -a "$OUT"; run O_both_token_reworded 30 QAB1167_PROMPT="$C/prompt_O.txt"
sedcopy P2 's#GATEWAY_URL=http://127.0.0.1:#GATEWAY_URL=http://localhost:#g'; run P_gateway_url_loopback_reworded 31 QAB1167_PROMPT="$C/prompt_P2.txt"
sedcopy Q 's/s-c18-batch/s-c18-octopus/g'; run Q_seat_worktree_reworded 28 QAB1167_PROMPT="$C/prompt_Q.txt"
sedcopy R 's/lsof -nP -iTCP:6000 -sTCP:LISTEN/lsof -nP -i TCP:6000 -s TCP:LISTEN/g'; run R_6000_lsof_reworded 29 QAB1167_PROMPT="$C/prompt_R.txt"
sedcopy S 's/PENDING-PR-X//; 1a\
PENDING-PR-X planted'; run S_partial_marker_planted 34 QAB1167_PROMPT="$C/prompt_S.txt"
sedcopy T 's/4f2b87547d8060646763a5f15ef4a165a1e436bd/4f2b87547d8060646763a5f15ef4a165a1e436be/g'; run T_head_altered_in_prompt 20 QAB1167_PROMPT="$C/prompt_T.txt"
sedcopy U 's/--pair-blob/--pair blob/g'; echo "U count after: $(/usr/bin/grep -c -F -- '--pair-blob' "$C/prompt_U.txt") (real $(/usr/bin/grep -c -F -- '--pair-blob' "$P"))" | tee -a "$OUT"; run U_pair_blob_reworded 35 QAB1167_PROMPT="$C/prompt_U.txt"
run POSITIVE_real_check 0
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH" | tee -a "$OUT"
