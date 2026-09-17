#!/bin/zsh
# check_launcher_1033.sh — runs the #1033 launcher with --check ONLY (never a launch), stdin /dev/null, rc printed on its own line; then override
# and fixture controls that MUST refuse with the named exit (and ones that must pass). Every control passes --check. Never a launch.
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks763_1033.sh
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1033
F=$G/fixtures
echo "check start $(date '+%Y-%m-%d %H:%M:%S %Z') launcher sha256 $(shasum -a 256 "$L" | cut -c1-16) mode $(stat -f '%Lp' "$L")"
"$L" --check < /dev/null
rc=$?
echo "check end $(date '+%H:%M:%S %Z')"
echo "launcher --check rc=$rc"
echo "--- controls (each: want rc, got rc)"
n=0; pass=0
ctl() { want=$1; shift; env "$@" "$L" --check < /dev/null > "$G/out/controls_last.out" 2> "$G/out/controls_last.err"; got=$?; n=$((n+1)); [ "$want" = "$got" ] && pass=$((pass+1)); echo "want $want got $got $([ "$want" = "$got" ] && echo PASS || echo MISMATCH) :: $* :: $(head -c 300 "$G/out/controls_last.err" | tr '\n' ' ') $(/usr/bin/grep -i -o 'develop [0-9a-f]* [^:]*: [0-9]* of [0-9]* guarded' "$G/out/controls_last.out" | head -c 160)"; }
ctl 0  QA1033_CUR_DEV=bb848b8283eb5ee6a6180067315b76f1321e7b6b
ctl 19 QA1033_CUR_DEV=2cab54988b4e7b71d403576719f5fd80e470fa92
ctl 18 QA1033_CUR_DEV=9fd3cb924e26a53a01d512462ce8b2c29f1ca6ee
ctl 18 QA1033_CUR_DEV=75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e
ctl 18 QA1033_CUR_DEV=7ee1a26e634f33b6a4ae115d559f5440a90f6fff
ctl 6  QA1033_HEAD=9fd3cb924e26a53a01d512462ce8b2c29f1ca6ee
ctl 22 QA1033_PROMPT=$F/neg_prompt_nofarm.txt
ctl 23 QA1033_PROMPT=$F/neg_prompt_nosubject.txt
ctl 24 QA1033_PROMPT=$F/neg_prompt_nottestedfirst.txt
ctl 26 QA1033_PROMPT=$F/neg_prompt_nocontainer.txt
ctl 12 QA1033_PROMPT=$F/neg_prompt_nomail.txt
ctl 11 QA1033_PROMPT=$F/neg_prompt_nopushban.txt
ctl 28 QA1033_PROMPT=$F/neg_prompt_nonpmver.txt
ctl 25 QA1033_BRIEF=$F/neg_brief_noaddendum.md
ctl 27 QA1033_BRIEF=$F/neg_brief_noreach.md
ctl 20 QA1033_BRIEF=$F/neg_brief_nosha.md
echo "controls end $(date '+%H:%M:%S %Z') :: $pass of $n PASS"
