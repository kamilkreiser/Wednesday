#!/bin/zsh
# check_launcher_1029.sh — runs the #1029 launcher with --check ONLY (never a launch), stdin /dev/null, rc printed on its own line; then fixture/override
# controls that MUST refuse with the named exit (and ones that must pass). Every control passes --check. Never a launch. Fixtures: make_fixtures_1029.py.
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1180p1_1029.sh
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1029
F=$G/controls
echo "check start $(date '+%Y-%m-%d %H:%M:%S %Z') launcher sha256 $(shasum -a 256 "$L" | cut -c1-16) mode $(stat -f '%Lp' "$L")"
"$L" --check < /dev/null
rc=$?
echo "check end $(date '+%H:%M:%S %Z')"
echo "launcher --check rc=$rc"
echo "--- controls (each: want rc, got rc)"
ctl() { want=$1; shift; env "$@" "$L" --check < /dev/null > "$G/out/controls_last.out" 2> "$G/out/controls_last.err"; got=$?; echo "want $want got $got $([ "$want" = "$got" ] && echo PASS || echo MISMATCH) :: ${*##*/} :: $(head -c 220 "$G/out/controls_last.err" | tr '\n' ' ') $(/usr/bin/grep -o 'origin develop [^;]*' "$G/out/controls_last.out" | head -c 160)"; }
ctl 0  QA1029_TEST_FILE=$F/pos_test_develop_4ad1cdcd1.ts
ctl 19 QA1029_TEST_FILE=$F/neg_test_landed_d9c98320e.ts
ctl 18 QA1029_TEST_FILE=$F/neg_test_unpinned.ts
ctl 0  QA1029_CUR_DEV=20ab16f9a80c5c3c75e613d8c670efefd8f5cafb
ctl 0  QA1029_CUR_DEV=e02515f8f4635822120e1cd90380b015ab5ddf00
ctl 18 QA1029_CUR_DEV=eb1051fd39fe3edab4e0b1d1967515b758d4ba3f
ctl 6  QA1029_HEAD=a4dc0d8ee2527501cac4c3d7305a60cc22355c70
ctl 7  QA1029_BRIEF=$F/neg_brief_notier2.md
ctl 15 QA1029_PROMPT=$F/neg_prompt_round2.txt
ctl 20 QA1029_BRIEF=$F/neg_brief_nosha.md
ctl 12 QA1029_PROMPT=$F/neg_prompt_nomail.txt
ctl 22 QA1029_PROMPT=$F/neg_prompt_nofarm.txt
ctl 23 QA1029_PROMPT=$F/neg_prompt_nosubject.txt
ctl 23 QA1029_BRIEF=$F/neg_brief_nosubject.md
ctl 24 QA1029_PROMPT=$F/neg_prompt_nottestedfirst.txt
ctl 25 QA1029_BRIEF=$F/neg_brief_noaddendum.md
ctl 26 QA1029_PROMPT=$F/neg_prompt_noprobe.txt
echo "controls end $(date '+%H:%M:%S %Z')"
