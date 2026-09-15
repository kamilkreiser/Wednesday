#!/bin/bash
# doc_d8d9_arms.sh — red-proof for the doc checker's D8 (every brief '+' line present EXACTLY) and D9 (an insert-only block
# follows its named "Insert AFTER line N" anchor), 2026-09-16 00:0x, row 99. All arms on REAL run artefacts:
#   1 KS-1049 A r1 (the false green: backticks dropped, bullet placed below the paragraph) → FAIL D8 + D9
#   2 KS-1035 D r1 (exact lines) under the CURRENT reanchor                                  → PASS 8/8 (D8 + D9 green)
#   3 the same KS-1035 output under the OLD reanchor (.pre-0915-blankoffset)                  → FAIL D9 (misplaced by a blank)
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
T=$LM/tasks/doc_patch; R=$LM/tasks/code_patch/reanchor.py; W=$(mktemp -d); fail=0
clone_of() { /usr/bin/grep -o "Cloning into '[^']*'" "$1/run.log" | head -1 | sed "s/Cloning into '//; s/'$//"; }
R49=$LM/runs/2026-09-15_ks1049-ornith35b-night; R35=$LM/runs/2026-09-15_ks1035-ornith35b-night
bash $T/build_doc_input.sh KS-1049 $W/in49.json $LM/night/briefs/split_1049A/KS-1049.md product=Blockchain/Dev/CONTRIBUTING.md ctx=32768 >/dev/null 2>&1 || { echo "ARM FAIL: build 1049"; exit 1; }
bash $T/build_doc_input.sh KS-1035 $W/in35.json $LM/night/briefs/split_1035D/KS-1035.md product=Blockchain/Dev/docs/DEV-PROCESS.md ctx=32768 >/dev/null 2>&1 || { echo "ARM FAIL: build 1035"; exit 1; }
o=$(bash $T/checker.sh $W/in49.json $R49/out.md "$(clone_of $R49)" 2>&1)
echo "$o" | /usr/bin/grep -q '^FAIL D8' && echo "$o" | /usr/bin/grep -q '^FAIL D9' && echo "ARM1 PASS (1049 r1 → FAIL D8 + D9)" || { echo "ARM1 FAIL"; echo "$o" | /usr/bin/grep -E '^(FAIL|RESULT)'; fail=1; }
o=$(bash $T/checker.sh $W/in35.json $R35/out.md "$(clone_of $R35)" 2>&1)
echo "$o" | /usr/bin/grep -q '^RESULT: PASS (8/8)' && echo "ARM2 PASS (1035 r1 → PASS 8/8)" || { echo "ARM2 FAIL"; echo "$o" | /usr/bin/grep -E '^(FAIL|RESULT)'; fail=1; }
cp $R $W/rean.keep; cp $R.pre-0915-blankoffset $W/rean.old; mv $R $W/rean.cur; cp $W/rean.old $R
o=$(bash $T/checker.sh $W/in35.json $R35/out.md "$(clone_of $R35)" 2>&1)
mv $W/rean.cur $R
echo "$o" | /usr/bin/grep -q '^FAIL D9' && echo "ARM3 PASS (old reanchor → FAIL D9)" || { echo "ARM3 FAIL"; fail=1; }
python3 -c "import filecmp,sys; sys.exit(0 if filecmp.cmp('$R','$W/rean.keep',shallow=False) else 1)" && echo "reanchor restored" || { echo "ARM FAIL: reanchor NOT restored"; fail=1; }
exit $fail
