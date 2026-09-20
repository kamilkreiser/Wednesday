#!/bin/bash
# launcher_controls.sh — the refusing controls A–R for launch_qa_secuura_batch1112-1118.sh, each exercised headless (--check, or a non-TTY
# LAUNCH for N) against a COPY of the prompt / launcher in the drafter's scratchpad; every rc on its own line. Nothing is launched: every
# control either refuses before the TTY guard or IS the TTY guard. Derived from the 2026-09-21_gate1106to1111 controls (launcher_check_controls.out).
set -u
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1112-1118.sh'
P='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1112-1118.prompt.txt'
S="$1"
C="$(mktemp -d "$S/ctl1112-XXXXXX")"
echo "$C" > /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1112to1118/controls_dir.txt
date -u +%Y-%m-%dT%H:%M:%SZ
run() { # $1 label, $2 want, then the command
  local label="$1" want="$2"; shift 2
  echo "== control $label (want exit $want)"
  "$@" > "$C/out.$$" 2>&1; rc=$?
  head -4 "$C/out.$$" | cut -c1-400
  echo "rc=$rc $([ "$rc" = "$want" ] && echo OK || echo MISMATCH)"
}
run "A: missing prompt (QAB1112_PROMPT=/nonexistent)" 4 env QAB1112_PROMPT=/nonexistent/prompt.txt "$L" --check
run "B: brief path absent (QAB1112_BRIEF=/nonexistent)" 3 env QAB1112_BRIEF=/nonexistent/brief.md "$L" --check
run "C: wrong #1118 head (QAB1112_HEAD_1118=0000…, a head moved)" 6 env QAB1112_HEAD_1118=0000000000000000000000000000000000000000 "$L" --check
run "D: QAB1112_CUR_DEV = the OLD develop cbae988db (develop 'moved' backwards: the #1106-#1111 test files read pre-batch blobs)" 18 env QAB1112_CUR_DEV=cbae988dbe90ebe556459ada2cb437eaf80e2402 "$L" --check
run "E: QAB1112_CUR_DEV = #1118's head (as if it had LANDED)" 19 env QAB1112_CUR_DEV=f132c92147b5005c36e405d0116faa541d978a67 "$L" --check
# F: a launcher COPY whose pinned compare expects behind=1 for #1112 (the live API answers behind=0 — the shape of develop moving off the pin)
sed 's/^WANT_COMPARE="1112 \$MERGE_BASE ahead=1 behind=0 files=1$/WANT_COMPARE="1112 $MERGE_BASE ahead=1 behind=1 files=1/' "$L" > "$C/launcher_F.sh"; chmod +x "$C/launcher_F.sh"
echo "  (copy carries behind=1 x$(/usr/bin/grep -c 'behind=1' "$C/launcher_F.sh"); the real launcher x$(/usr/bin/grep -c 'behind=1' "$L") — the sed must have landed)"
run "F: launcher copy expecting behind=1 for #1112" 10 "$C/launcher_F.sh" --check
sed '1d' "$P" > "$C/prompt_G.txt"; run "G: prompt copy without the thinking directive (line 1 removed)" 8 env QAB1112_PROMPT="$C/prompt_G.txt" "$L" --check
sed 's/PR #1114 is KS-1244 + KS-1198\./PR #1114 is the joined-key pin./' "$P" > "$C/prompt_H.txt"; diff "$P" "$C/prompt_H.txt" | head -4
run "H: namespace sentence for #1114 reworded" 32 env QAB1112_PROMPT="$C/prompt_H.txt" "$L" --check
sed 's/COMMA-separated/comma-delimited/g' "$P" > "$C/prompt_I.txt"; run "I: every 'COMMA-separated' reworded (MG-2 wording gone)" 25 env QAB1112_PROMPT="$C/prompt_I.txt" "$L" --check
sed 's/RULE WHETHER IT BLOCKS/decide if it blocks/g' "$P" > "$C/prompt_J.txt"; run "J: every 'RULE WHETHER IT BLOCKS' reworded" 30 env QAB1112_PROMPT="$C/prompt_J.txt" "$L" --check
sed 's/THE GUARD AND ITS MOUNT/the guard and the mount/g' "$P" > "$C/prompt_K.txt"; run "K: by-name item 5 'THE GUARD AND ITS MOUNT' reworded" 33 env QAB1112_PROMPT="$C/prompt_K.txt" "$L" --check
sed 's#GATEWAY_URL=http://127.0.0.1:#GATEWAY_URL=http://localhost:#g' "$P" > "$C/prompt_L.txt"; run "L: the loopback GATEWAY_URL phrase reworded (exit-31 leg)" 31 env QAB1112_PROMPT="$C/prompt_L.txt" "$L" --check
sed 's/#1113 KS-1283: TIER 1/#1113 KS-1283: TIER 2/' "$P" > "$C/prompt_M.txt"; run "M: #1113's tier line demoted to TIER 2" 7 env QAB1112_PROMPT="$C/prompt_M.txt" "$L" --check
echo "== control N: a LAUNCH (no --check) with stdin not a TTY must refuse at exit 21 BEFORE exec (all guards pass; nothing launched) (want exit 21)"
"$L" < /dev/null > "$C/out.N" 2>&1; rc=$?; tail -2 "$C/out.N" | cut -c1-300; echo "rc=$rc $([ "$rc" = 21 ] && echo OK || echo MISMATCH)"
sed 's/\[QA -> Wednesday\] BATCH GATE #1112-#1118 (seven PRs; tier 1 = #1113, #1114, #1118)/[QA -> Wednesday] BATCH GATE #1112-#1118/' "$P" > "$C/prompt_O.txt"; run "O: the verdict subject prefix shortened" 23 env QAB1112_PROMPT="$C/prompt_O.txt" "$L" --check
sed 's/MG-3 KEY-SET rule/MG-3 rule/g' "$P" > "$C/prompt_P.txt"; run "P (new): the MG-3 KEY-SET rule phrase reworded" 25 env QAB1112_PROMPT="$C/prompt_P.txt" "$L" --check
sed 's/lsof -nP -iTCP:4003 -sTCP:LISTEN/lsof -i :4003/g' "$P" > "$C/prompt_Q.txt"; run "Q (new): the :4003 lsof discipline reworded" 29 env QAB1112_PROMPT="$C/prompt_Q.txt" "$L" --check
sed 's/PR #1116 is KS-1284 + KS-1175\./PR #1116 is KS-1284./' "$P" > "$C/prompt_R.txt"; run "R (new): the two-key namespace sentence for #1116 loses its second key" 32 env QAB1112_PROMPT="$C/prompt_R.txt" "$L" --check
echo "== positive control: the real launcher --check"
"$L" --check > "$C/out.pos" 2>&1; rc=$?; echo "rc=$rc $([ "$rc" = 0 ] && echo OK || echo MISMATCH)"
echo "controls dir $C (left in the scratchpad)"
date -u +%Y-%m-%dT%H:%M:%SZ
