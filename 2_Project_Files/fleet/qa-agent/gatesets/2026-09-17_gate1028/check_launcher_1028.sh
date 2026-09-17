#!/bin/zsh
# check_launcher_1028.sh — runs the #1028 launcher with --check ONLY (never a launch), stdin /dev/null, rc printed on its own line; then fixture/override
# controls that MUST refuse with the named exit (and ones that must pass). Every control passes --check. Never a launch.
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks744_1028.sh
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1028
echo "check start $(date '+%Y-%m-%d %H:%M:%S %Z') launcher sha256 $(shasum -a 256 "$L" | cut -c1-16) mode $(stat -f '%Lp' "$L")"
"$L" --check < /dev/null
rc=$?
echo "check end $(date '+%H:%M:%S %Z')"
echo "launcher --check rc=$rc"
echo "--- controls (each: want rc, got rc)"
ctl() { want=$1; shift; env "$@" "$L" --check < /dev/null > "$G/out/controls_last.out" 2> "$G/out/controls_last.err"; got=$?; echo "want $want got $got $([ "$want" = "$got" ] && echo PASS || echo MISMATCH) :: $* :: $(head -c 200 "$G/out/controls_last.err" | tr '\n' ' ') $(/usr/bin/grep -o 'origin develop [A-Z]*[^;]*GUARDED hits [0-9]*, content-cleared [^—]*' "$G/out/controls_last.out" | head -c 200)"; }
ctl 0  QA1028_AUTH_FILE=$G/pos_auth_develop_b8fce678a.ts
ctl 19 QA1028_AUTH_FILE=$G/pos_auth_landed_6e1668362.ts
ctl 18 QA1028_AUTH_FILE=$G/neg_auth_unpinned_c673f9c9e.ts
ctl 18 QA1028_LOCK_ALLOW_OFF=1
ctl 0  QA1028_CUR_DEV=e02515f8f4635822120e1cd90380b015ab5ddf00
ctl 0  QA1028_CUR_DEV=19f1e54750ce2b65312a687add2db4f5628edb7d
ctl 6  QA1028_HEAD=6252f06ac7c913619888cb20e07cc5a0c846043d
ctl 23 QA1028_PROMPT=$G/neg_prompt_nosubject.txt
ctl 22 QA1028_PROMPT=$G/neg_prompt_nofarm.txt
ctl 24 QA1028_PROMPT=$G/neg_prompt_noprior.txt
ctl 24 QA1028_PROMPT=$G/neg_prompt_nottestedfirst.txt
ctl 25 QA1028_BRIEF=$G/neg_brief_noaddendum.md
ctl 20 QA1028_BRIEF=$G/neg_brief_nosha.md
ctl 15 QA1028_BRIEF=$G/neg_brief_round2.md
echo "controls end $(date '+%H:%M:%S %Z')"
