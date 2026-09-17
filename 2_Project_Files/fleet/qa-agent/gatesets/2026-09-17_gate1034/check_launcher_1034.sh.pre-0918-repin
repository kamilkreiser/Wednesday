#!/bin/zsh
# check_launcher_1034.sh — runs the #1034 launcher with --check ONLY (never a launch), stdin /dev/null, rc printed on its own line; then fixture/override
# controls that MUST refuse with the named exit (and ones that must pass). Every control passes --check. Never a launch. (Derived from check_launcher_1032.sh.)
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1215_1034.sh
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1034
echo "check start $(date '+%Y-%m-%d %H:%M:%S %Z') launcher sha256 $(shasum -a 256 "$L" | cut -c1-16) mode $(stat -f '%Lp' "$L")"
"$L" --check < /dev/null
rc=$?
echo "check end $(date '+%H:%M:%S %Z')"
echo "launcher --check rc=$rc"
echo "--- controls (each: want rc, got rc)"
n=0; pass=0
ctl() { want=$1; shift; env "$@" "$L" --check < /dev/null > "$G/out/controls_last.out" 2> "$G/out/controls_last.err"; got=$?; n=$((n+1)); [ "$want" = "$got" ] && pass=$((pass+1)); echo "want $want got $got $([ "$want" = "$got" ] && echo PASS || echo MISMATCH) :: $* :: $(head -c 260 "$G/out/controls_last.err" | tr '\n' ' ') $(grep -m1 'develop' "$G/out/controls_last.out" | head -c 200)"; }
ctl 0  QA1034_AUTH_FILE=$G/fixtures/pos_auth_develop_6e1668362.ts
ctl 19 QA1034_AUTH_FILE=$G/fixtures/pos_auth_landed_bf09d315a.ts
ctl 18 QA1034_AUTH_FILE=$G/fixtures/neg_auth_unpinned_edit.ts
ctl 0  QA1034_CUR_DEV=27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d
ctl 0  QA1034_CUR_DEV=732c13459d76f5b05ade94bb91de7e47585b0e7d
ctl 18 QA1034_CUR_DEV=0a2b1603fe52f0f3b8152588af78bbeab0237be7
ctl 18 QA1034_CUR_DEV=d127dc7d4655a4e227d4f6e511f469c456eaabb7
ctl 18 QA1034_CUR_DEV=2cab54988b4e7b71d403576719f5fd80e470fa92
ctl 19 QA1034_CUR_DEV=fd81a75f0688f6cbe1e5f79b061bb1369c88f477
ctl 19 QA1034_CUR_DEV=6c6fdc94e869c98a73e6ffaa1b66be1d3b20d7b3
ctl 6  QA1034_HEAD=6c6fdc94e869c98a73e6ffaa1b66be1d3b20d7b3
ctl 23 QA1034_PROMPT=$G/fixtures/neg_prompt_nosubject.txt
ctl 22 QA1034_PROMPT=$G/fixtures/neg_prompt_nofarm.txt
ctl 24 QA1034_PROMPT=$G/fixtures/neg_prompt_noprior.txt
ctl 24 QA1034_PROMPT=$G/fixtures/neg_prompt_nottestedfirst.txt
ctl 25 QA1034_PROMPT=$G/fixtures/neg_prompt_nocsn.txt
ctl 25 QA1034_BRIEF=$G/fixtures/neg_brief_noaddendum.md
ctl 20 QA1034_BRIEF=$G/fixtures/neg_brief_nosha.md
ctl 15 QA1034_BRIEF=$G/fixtures/neg_brief_round2.md
ctl 7  QA1034_BRIEF=$G/fixtures/neg_brief_tier2.md
echo "controls end $(date '+%H:%M:%S %Z') | controls PASS $pass / $n"
