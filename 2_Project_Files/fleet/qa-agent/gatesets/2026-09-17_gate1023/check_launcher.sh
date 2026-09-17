#!/bin/zsh
# check_launcher.sh — runs the #1023 launcher with --check ONLY (never a launch), stdin /dev/null, rc printed on its own line; then fixture/override
# controls that MUST refuse with the named exit (and one that must pass). Never a launch.
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1207_1023.sh
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1023
echo "check start $(date '+%Y-%m-%d %H:%M:%S %Z') launcher sha256 $(shasum -a 256 "$L" | cut -c1-16) mode $(stat -f '%Lp' "$L")"
"$L" --check < /dev/null
rc=$?
echo "check end $(date '+%H:%M:%S %Z')"
echo "launcher --check rc=$rc"
echo "--- controls (each: want rc, got rc)"
ctl() { want=$1; shift; env "$@" "$L" --check < /dev/null > /dev/null 2> "$G/controls_last.err"; got=$?; echo "want $want got $got :: $* :: $(head -c 160 "$G/controls_last.err" | tr '\n' ' ')"; }
ctl 0  QA1023_AUTH_FILE=$G/pos_auth_develop_7c985bdce.ts
ctl 19 QA1023_AUTH_FILE=$G/pos_auth_landed_b8fce678a.ts
ctl 18 QA1023_AUTH_FILE=$G/neg_auth_unpinned.ts
ctl 6  QA1023_HEAD=0f8b699b41f26e1f4f688c93ba9b2ea595d6f207
ctl 23 QA1023_PROMPT=$G/neg_prompt_nosubject.txt
ctl 22 QA1023_PROMPT=$G/neg_prompt_nofarm.txt
ctl 24 QA1023_PROMPT=$G/neg_prompt_noprior.txt
ctl 24 QA1023_PROMPT=$G/neg_prompt_nottestedfirst.txt
ctl 25 QA1023_BRIEF=$G/neg_brief_noaddendum.md
ctl 20 QA1023_BRIEF=$G/neg_brief_nosha.md
ctl 15 QA1023_BRIEF=$G/neg_brief_round2.md
echo "controls end $(date '+%H:%M:%S %Z')"
