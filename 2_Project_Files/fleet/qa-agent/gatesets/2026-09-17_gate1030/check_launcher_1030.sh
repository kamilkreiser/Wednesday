#!/bin/zsh
# check_launcher_1030.sh — runs the #1030 launcher with --check ONLY (never a launch), stdin /dev/null, rc printed on its own line; then override
# and fixture controls that MUST refuse with the named exit (and ones that must pass). Every control passes --check. Never a launch.
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1211_1030.sh
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1030
echo "check start $(date '+%Y-%m-%d %H:%M:%S %Z') launcher sha256 $(shasum -a 256 "$L" | cut -c1-16) mode $(stat -f '%Lp' "$L")"
"$L" --check < /dev/null
rc=$?
echo "check end $(date '+%H:%M:%S %Z')"
echo "launcher --check rc=$rc"
echo "--- controls (each: want rc, got rc)"
ctl() { want=$1; shift; env "$@" "$L" --check < /dev/null > "$G/out/controls_last.out" 2> "$G/out/controls_last.err"; got=$?; echo "want $want got $got $([ "$want" = "$got" ] && echo PASS || echo MISMATCH) :: $* :: $(head -c 260 "$G/out/controls_last.err" | tr '\n' ' ') $(/usr/bin/grep -i -o 'develop [0-9a-f]* [^:]*: [0-9]* of [0-9]* guarded' "$G/out/controls_last.out" | head -c 160)"; }
ctl 0  QA1030_CUR_DEV=20ab16f9a80c5c3c75e613d8c670efefd8f5cafb
ctl 19 QA1030_CUR_DEV=e43af493418a1f13cfb60c994380fb74d79ad07e
ctl 18 QA1030_CUR_DEV=17cbb10919854658a40a07fc3e5fdafdd1e82e08
ctl 18 QA1030_CUR_DEV=19f1e54750ce2b65312a687add2db4f5628edb7d
ctl 6  QA1030_HEAD=566107f019e6cc05b6b4b5a7d62122a3f9772c80
ctl 22 QA1030_PROMPT=$G/neg_prompt_nofarm.txt
ctl 23 QA1030_PROMPT=$G/neg_prompt_nosubject.txt
ctl 24 QA1030_PROMPT=$G/neg_prompt_nottestedfirst.txt
ctl 26 QA1030_PROMPT=$G/neg_prompt_nodocker.txt
ctl 12 QA1030_PROMPT=$G/neg_prompt_nomail.txt
ctl 11 QA1030_PROMPT=$G/neg_prompt_nopushban.txt
ctl 25 QA1030_BRIEF=$G/neg_brief_noaddendum.md
ctl 27 QA1030_BRIEF=$G/neg_brief_notier1.md
ctl 20 QA1030_BRIEF=$G/neg_brief_nosha.md
echo "controls end $(date '+%H:%M:%S %Z')"
