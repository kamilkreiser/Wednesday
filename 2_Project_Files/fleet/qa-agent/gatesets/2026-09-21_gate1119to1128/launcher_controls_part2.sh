#!/bin/bash
# launcher_controls_part2.sh — controls N–S + the positive control (the first run of launcher_controls.sh ended after M when the drafter's tool
# call hit its wall clock; A–M's rcs stand in launcher_check_controls.out). Appends to the same file. Same controls dir.
set -u
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1119-1128.sh'
P='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1119-1128.prompt.txt'
C="$(cat /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1119to1128/controls_dir.txt)"
echo "(part 2 resumed $(date -u +%Y-%m-%dT%H:%M:%SZ) in $C)"
run() { local label="$1" want="$2"; shift 2
  echo "== control $label (want exit $want)"
  "$@" > "$C/out.$$" 2>&1; rc=$?
  head -4 "$C/out.$$" | cut -c1-400
  echo "rc=$rc $([ "$rc" = "$want" ] && echo OK || echo MISMATCH)"; }
echo "== control N: a LAUNCH (no --check) with stdin not a TTY must refuse at exit 21 BEFORE exec (all guards pass; nothing launched) (want exit 21)"
"$L" < /dev/null > "$C/out.N" 2>&1; rc=$?; tail -2 "$C/out.N" | cut -c1-300; echo "rc=$rc $([ "$rc" = 21 ] && echo OK || echo MISMATCH)"
sed 's/\[QA -> Wednesday\] BATCH GATE #1119-#1128 (ten PRs; tier 1 = #1124, #1125, #1126, #1127, #1128)/[QA -> Wednesday] BATCH GATE #1119-#1128/' "$P" > "$C/prompt_O.txt"; run "O: the verdict subject prefix shortened" 23 env QAB1119_PROMPT="$C/prompt_O.txt" "$L" --check
sed 's/MG-3 KEY-SET rule/MG-3 rule/g' "$P" > "$C/prompt_P.txt"; run "P: the MG-3 KEY-SET rule phrase reworded" 25 env QAB1119_PROMPT="$C/prompt_P.txt" "$L" --check
sed 's/lsof -nP -iTCP:4006 -sTCP:LISTEN/lsof -i :4006/g' "$P" > "$C/prompt_Q.txt"; run "Q: the :4006 lsof discipline reworded (exit-29 leg)" 29 env QAB1119_PROMPT="$C/prompt_Q.txt" "$L" --check
sed 's/expect EXACTLY those two cells red/expect those two cells red/g' "$P" > "$C/prompt_R.txt"; run "R (new): the allowance's measuring phrase in by-name 4 reworded" 33 env QAB1119_PROMPT="$C/prompt_R.txt" "$L" --check
sed 's/ALIASNARROWED/ALIASNARROWED-X/g' "$P" > "$C/prompt_S.txt"; run "S (new): the seat's tamper id ALIASNARROWED renamed in the prompt (a BOTH token lost; exit-30 leg)" 30 env QAB1119_PROMPT="$C/prompt_S.txt" "$L" --check
echo "== positive control: the real launcher --check"
"$L" --check > "$C/out.pos" 2>&1; rc=$?; echo "rc=$rc $([ "$rc" = 0 ] && echo OK || echo MISMATCH)"
echo "controls dir $C (left in the scratchpad)"
date -u +%Y-%m-%dT%H:%M:%SZ
