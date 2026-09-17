#!/bin/zsh
# check_launcher_1032.sh — runs the #1032 launcher with --check ONLY (never a launch), stdin /dev/null, rc printed on its own line; then fixture/override
# controls that MUST refuse with the named exit (and ones that must pass). Every control passes --check. Never a launch.
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1194_1032.sh
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1032
echo "check start $(date '+%Y-%m-%d %H:%M:%S %Z') launcher sha256 $(shasum -a 256 "$L" | cut -c1-16) mode $(stat -f '%Lp' "$L")"
"$L" --check < /dev/null
rc=$?
echo "check end $(date '+%H:%M:%S %Z')"
echo "launcher --check rc=$rc"
echo "--- controls (each: want rc, got rc)"
ctl() { want=$1; shift; env "$@" "$L" --check < /dev/null > "$G/out/controls_last.out" 2> "$G/out/controls_last.err"; got=$?; echo "want $want got $got $([ "$want" = "$got" ] && echo PASS || echo MISMATCH) :: $* :: $(head -c 260 "$G/out/controls_last.err" | tr '\n' ' ') $(grep -m1 'develop' "$G/out/controls_last.out" | head -c 200)"; }
ctl 0  QA1032_USERS_FILE=$G/fixtures/pos_users_develop_c723a68af.ts
ctl 19 QA1032_USERS_FILE=$G/fixtures/pos_users_landed_8299a2558.ts
ctl 18 QA1032_USERS_FILE=$G/fixtures/neg_users_unpinned_edit.ts
ctl 0  QA1032_CUR_DEV=0a2b1603fe52f0f3b8152588af78bbeab0237be7
ctl 0  QA1032_CUR_DEV=bb848b8283eb5ee6a6180067315b76f1321e7b6b
ctl 18 QA1032_CUR_DEV=684bddb01b24ef1b4d0d263f9b5c614f59f3fe9f
ctl 18 QA1032_CUR_DEV=75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e
ctl 19 QA1032_CUR_DEV=70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039
ctl 6  QA1032_HEAD=00236c10bc9c237e64e008f6bb927c816a8bb29c
ctl 23 QA1032_PROMPT=$G/fixtures/neg_prompt_nosubject.txt
ctl 22 QA1032_PROMPT=$G/fixtures/neg_prompt_nofarm.txt
ctl 24 QA1032_PROMPT=$G/fixtures/neg_prompt_noprior.txt
ctl 24 QA1032_PROMPT=$G/fixtures/neg_prompt_nottestedfirst.txt
ctl 25 QA1032_PROMPT=$G/fixtures/neg_prompt_nocsn.txt
ctl 25 QA1032_BRIEF=$G/fixtures/neg_brief_noaddendum.md
ctl 20 QA1032_BRIEF=$G/fixtures/neg_brief_nosha.md
ctl 15 QA1032_BRIEF=$G/fixtures/neg_brief_round2.md
ctl 7  QA1032_BRIEF=$G/fixtures/neg_brief_tier2.md
echo "controls end $(date '+%H:%M:%S %Z')"
