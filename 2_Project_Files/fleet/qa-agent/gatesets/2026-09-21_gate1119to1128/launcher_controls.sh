#!/bin/bash
# launcher_controls.sh — the refusing controls A–R for launch_qa_secuura_batch1119-1128.sh, each exercised headless (--check, or a non-TTY
# LAUNCH for N) against a COPY of the prompt / launcher in the drafter's scratchpad; every rc on its own line. Nothing is launched: every
# control either refuses before the TTY guard or IS the TTY guard. Derived from the 2026-09-21_gate1112to1118 controls (launcher_controls.sh).
set -u
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1119-1128.sh'
P='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1119-1128.prompt.txt'
S="$1"
C="$(mktemp -d "$S/ctl1119-XXXXXX")"
echo "$C" > /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1119to1128/controls_dir.txt
date -u +%Y-%m-%dT%H:%M:%SZ
run() { # $1 label, $2 want, then the command
  local label="$1" want="$2"; shift 2
  echo "== control $label (want exit $want)"
  "$@" > "$C/out.$$" 2>&1; rc=$?
  head -4 "$C/out.$$" | cut -c1-400
  echo "rc=$rc $([ "$rc" = "$want" ] && echo OK || echo MISMATCH)"
}
run "A: missing prompt (QAB1119_PROMPT=/nonexistent)" 4 env QAB1119_PROMPT=/nonexistent/prompt.txt "$L" --check
run "B: brief path absent (QAB1119_BRIEF=/nonexistent)" 3 env QAB1119_BRIEF=/nonexistent/brief.md "$L" --check
run "C: wrong #1128 head (QAB1119_HEAD_1128=0000…, a head moved)" 6 env QAB1119_HEAD_1128=0000000000000000000000000000000000000000 "$L" --check
run "D: QAB1119_CUR_DEV = the OLD develop 362e51fe0 (develop 'moved' backwards: auth.test.ts / ks978 read pre-#1114/#1115 blobs)" 18 env QAB1119_CUR_DEV=362e51fe0db7e73d5557924902763fe3f10fd8c7 "$L" --check
run "E: QAB1119_CUR_DEV = #1128's head (as if it had LANDED)" 19 env QAB1119_CUR_DEV=e35b5ddc27dffca5ad1a7cea17b4433484d460ac "$L" --check
# F: a launcher COPY whose pinned compare expects behind=1 for #1119 (the live API answers behind=0 — the shape of develop moving off the pin)
sed 's/^WANT_COMPARE="1119 \$MERGE_BASE ahead=1 behind=0 files=1$/WANT_COMPARE="1119 $MERGE_BASE ahead=1 behind=1 files=1/' "$L" > "$C/launcher_F.sh"; chmod +x "$C/launcher_F.sh"
echo "  (copy carries behind=1 x$(/usr/bin/grep -c 'behind=1' "$C/launcher_F.sh"); the real launcher x$(/usr/bin/grep -c 'behind=1' "$L") — the sed must have landed)"
run "F: launcher copy expecting behind=1 for #1119" 10 "$C/launcher_F.sh" --check
sed '1d' "$P" > "$C/prompt_G.txt"; run "G: prompt copy without the thinking directive (line 1 removed)" 8 env QAB1119_PROMPT="$C/prompt_G.txt" "$L" --check
sed 's/PR #1121 is KS-957 + KS-930\./PR #1121 is the two-key pin./' "$P" > "$C/prompt_H.txt"; diff "$P" "$C/prompt_H.txt" | head -4
run "H: namespace sentence for #1121 reworded" 32 env QAB1119_PROMPT="$C/prompt_H.txt" "$L" --check
sed 's/COMMA-separated/comma-delimited/g' "$P" > "$C/prompt_I.txt"; run "I: every 'COMMA-separated' reworded (MG-2 wording gone)" 25 env QAB1119_PROMPT="$C/prompt_I.txt" "$L" --check
sed 's/RULE WHETHER IT BLOCKS/decide if it blocks/g' "$P" > "$C/prompt_J.txt"; run "J: every 'RULE WHETHER IT BLOCKS' reworded" 30 env QAB1119_PROMPT="$C/prompt_J.txt" "$L" --check
sed 's/THE ALIAS TRIO AND THE ALLOWANCE/the alias trio and its allowance/g' "$P" > "$C/prompt_K.txt"; run "K: by-name item 9 'THE ALIAS TRIO AND THE ALLOWANCE' reworded" 33 env QAB1119_PROMPT="$C/prompt_K.txt" "$L" --check
sed 's#GATEWAY_URL=http://127.0.0.1:#GATEWAY_URL=http://localhost:#g' "$P" > "$C/prompt_L.txt"; run "L: the loopback GATEWAY_URL phrase reworded (exit-31 leg)" 31 env QAB1119_PROMPT="$C/prompt_L.txt" "$L" --check
sed 's/#1128 KS-1234: TIER 1/#1128 KS-1234: TIER 2/' "$P" > "$C/prompt_M.txt"; run "M: #1128's tier line demoted to TIER 2" 7 env QAB1119_PROMPT="$C/prompt_M.txt" "$L" --check
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
