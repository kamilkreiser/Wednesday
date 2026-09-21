#!/bin/bash
# launcher_controls_gate15.sh <launcher> <prompt> — refusing controls for the gate15 launcher: each control edits a COPY of the prompt / capture
# (never the real files), or sets a QAB1136_* override, runs `--check`, and records the rc on its own line against the expected exit. Controls that
# pass the API phases cost ~60-90 s each (10 compare GETs + 41 contents GETs). Writes only into $G/controls_gate15.XXXXXX/ and
# launcher_check_controls.out. Never launches (every call is --check or a non-TTY LAUNCH that must refuse at exit 21 after every guard passed).
# Derived from gatesets/2026-09-21_gate1130to1135/launcher_controls_1130.sh (its control F was mis-designed — the sed anchored a line that begins
# `WANT_COMPARE="`; here control F edits the SECOND PR's compare line, which begins at column 1).
set -u
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate15_docs_comments'
L="${1:?launcher}"; P="${2:?prompt}"
B="$G/mail_gate15_ready.md"
LAST="$(sed -n "s/^# QAB1136_CUR_DEV .*QAB1136_HEAD_\([0-9]*\) .*/\1/p" "$L" | head -1)"
C="$(mktemp -d "$G/controls_gate15.XXXXXX")"; echo "$C" > "$G/controls_dir_gate15.txt"
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
run A_missing_prompt 4 QAB1136_PROMPT="$C/absent.txt"
run B_brief_absent 3 QAB1136_BRIEF="$C/absent.md"
run C_wrong_head_last 6 "QAB1136_HEAD_$LAST=0000000000000000000000000000000000000001"
run D_curdev_old_parent_581ed7fa1 18 QAB1136_CUR_DEV=581ed7fa124b85c7c2da89ac05d52f99c2502911
run E_curdev_is_1136_head 19 QAB1136_CUR_DEV=6f5c31c455df5f75d2cc4db93dd5bdfb85cb0dfb
sed 's/^1137 \$MERGE_BASE ahead=1 behind=3 files=1$/1137 $MERGE_BASE ahead=1 behind=4 files=1/' "$L" > "$C/launcher_F.sh"; chmod 755 "$C/launcher_F.sh"
echo "F: launcher copy expecting behind=4 for #1137 (sed hit: $(/usr/bin/grep -c 'behind=4 files=1' "$C/launcher_F.sh"), real: $(/usr/bin/grep -c 'behind=4 files=1' "$L"))" | tee -a "$OUT"
t0=$(date -u +%H:%M:%SZ); "$C/launcher_F.sh" --check > "$C/F_behind4.out" 2>&1; rc=$?; [ "$rc" = 10 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "F_behind4 rc=$rc want=10 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/F_behind4.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy G '1s/ultrathink/think/'; run G_no_thinking_directive 8 QAB1136_PROMPT="$C/prompt_G.txt"
sedcopy H 's/PR #1136 is KS-1035 + KS-1036\./PR #1136 is KS-1035 and KS-1036./'; echo "H count after: $(/usr/bin/grep -c -F 'PR #1136 is KS-1035 + KS-1036.' "$C/prompt_H.txt") (real $(/usr/bin/grep -c -F 'PR #1136 is KS-1035 + KS-1036.' "$P"))" | tee -a "$OUT"; run H_namespace_sentence_reworded 32 QAB1136_PROMPT="$C/prompt_H.txt"
sedcopy I 's/#1140 KS-1097: TIER 2/#1140 KS-1097: TIER 1/'; run I_1140_promoted_to_tier1 7 QAB1136_PROMPT="$C/prompt_I.txt"
sedcopy J 's/TWO comma-separated = MG-2/two comma separated = MG-2/g'; run J_mg2_phrase_reworded 25 QAB1136_PROMPT="$C/prompt_J.txt"
sedcopy K 's/RULE WHETHER IT BLOCKS/rule if it blocks/g'; run K_rule_whether_it_blocks_reworded 30 QAB1136_PROMPT="$C/prompt_K.txt"
sedcopy L2 's/THE STALE-CLAIM FINDINGS/THE OLD-CLAIM FINDINGS/'; run L_byname_item6_reworded 33 QAB1136_PROMPT="$C/prompt_L2.txt"
sedcopy M 's/(ten PRs; tier 2 floor: five docs + five test-file comments)/(ten PRs)/'; run M_subject_prefix_shortened 23 QAB1136_PROMPT="$C/prompt_M.txt"
t0=$(date -u +%H:%M:%SZ); "$L" < /dev/null > "$C/N_nontty_launch.out" 2>&1; rc=$?; [ "$rc" = 21 ] && { v=OK; ok=$((ok+1)); } || { v=MISMATCH; bad=$((bad+1)); }; echo "N_nontty_launch rc=$rc want=21 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/N_nontty_launch.out" | cut -c1-160)" | tee -a "$OUT"
sedcopy O 's/secuura02-kintsugi-vm/secuura02-kintsugi-VM/g'; echo "O count after: $(/usr/bin/grep -c -F 'secuura02-kintsugi-vm' "$C/prompt_O.txt") (real $(/usr/bin/grep -c -F 'secuura02-kintsugi-vm' "$P"))" | tee -a "$OUT"; run O_both_token_recased 30 QAB1136_PROMPT="$C/prompt_O.txt"
sedcopy P2 's#GATEWAY_URL=http://127.0.0.1:#GATEWAY_URL=http://localhost:#g'; run P_gateway_url_loopback_reworded 31 QAB1136_PROMPT="$C/prompt_P2.txt"
sedcopy Q 's/s-b15-batch/s-b15-octopus/g'; run Q_seat_worktree_reworded 28 QAB1136_PROMPT="$C/prompt_Q.txt"
sedcopy R 's/lsof -nP -iTCP:4003 -sTCP:LISTEN/lsof -nP -i TCP:4003 -s TCP:LISTEN/g'; run R_4003_lsof_reworded 29 QAB1136_PROMPT="$C/prompt_R.txt"
sedcopy S 's/PENDING-PR-X//; 1a\
PENDING-PR-X planted'; run S_partial_marker_planted 34 QAB1136_PROMPT="$C/prompt_S.txt"
run POSITIVE_real_check 0
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH" | tee -a "$OUT"
