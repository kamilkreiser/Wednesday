#!/bin/zsh
# check_and_controls.sh — #1007 drafter: run the generated launcher with --check ONLY (never without it), rc read on its own line; then three
# NEGATIVE controls, each ALSO under --check with a test override pointing at a scratch copy, each must refuse with its own exit code.
Q=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent; GS=$Q/gatesets/2026-09-17_gate1007; L=$Q/launchers/launch_qa_secuura_ks864_1007.sh
B=$Q/briefs/2026-09-17_secuura-1007-ks864-tier2.md; PR=$Q/briefs/2026-09-17_secuura-1007-ks864-tier2.prompt.txt
echo "check $(date '+%Y-%m-%d %H:%M:%S %Z')" > "$GS/check.out"
bash "$L" --check >> "$GS/check.out" 2>&1
rc=$?
echo "rc $rc" >> "$GS/check.out"
echo "controls_check $(date '+%Y-%m-%d %H:%M:%S %Z') — negative controls under --check, each must REFUSE with its own exit" > "$GS/controls_check.out"
echo "## N1 head override = develop SHA (expect exit 6)" >> "$GS/controls_check.out"
QA1007_HEAD=93629700c3d219c1d8ca61d69150bb9b623fc1be bash "$L" --check >> "$GS/controls_check.out" 2>&1
rc=$?
echo "rc $rc" >> "$GS/controls_check.out"
/usr/bin/grep -v -i 'MAIL YOUR VERDICT' "$PR" > "$GS/neg_prompt_nomail.txt"
echo "## N2 prompt copy without 'MAIL YOUR VERDICT' (expect exit 12)" >> "$GS/controls_check.out"
QA1007_PROMPT="$GS/neg_prompt_nomail.txt" bash "$L" --check >> "$GS/controls_check.out" 2>&1
rc=$?
echo "rc $rc" >> "$GS/controls_check.out"
sed 's/b28ed490ada70df2056763f4512c98443285a694/HEADSHA-REMOVED/g' "$B" > "$GS/neg_brief_nosha.md"
echo "## N3 brief copy with the head SHA removed (expect exit 20)" >> "$GS/controls_check.out"
QA1007_BRIEF="$GS/neg_brief_nosha.md" bash "$L" --check >> "$GS/controls_check.out" 2>&1
rc=$?
echo "rc $rc" >> "$GS/controls_check.out"
sed 's/TIER 2/TIER-TWO/g' "$B" > "$GS/neg_brief_notier2.md"
echo "## N4 brief copy without 'TIER 2' (expect exit 7)" >> "$GS/controls_check.out"
QA1007_BRIEF="$GS/neg_brief_notier2.md" bash "$L" --check >> "$GS/controls_check.out" 2>&1
rc=$?
echo "rc $rc" >> "$GS/controls_check.out"
