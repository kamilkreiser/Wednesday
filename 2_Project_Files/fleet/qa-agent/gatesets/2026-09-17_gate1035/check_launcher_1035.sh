#!/bin/zsh
# check_launcher_1035.sh — runs the #1035 launcher with --check ONLY (never a launch), stdin /dev/null, rc printed on its own line; then fixture/override
# controls that MUST refuse with the named exit (and ones that must pass). Every control passes --check. Never a launch. (Derived from check_launcher_1034.sh.)
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1204_1035.sh
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1035
echo "check start $(date '+%Y-%m-%d %H:%M:%S %Z') launcher sha256 $(shasum -a 256 "$L" | cut -c1-16) mode $(stat -f '%Lp' "$L")"
"$L" --check < /dev/null
rc=$?
echo "check end $(date '+%H:%M:%S %Z')"
echo "launcher --check rc=$rc"
echo "--- controls (each: want rc, got rc)"
n=0; pass=0
ctl() { want=$1; shift; env "$@" "$L" --check < /dev/null > "$G/out/r2/controls_last.out" 2> "$G/out/r2/controls_last.err"; got=$?; n=$((n+1)); [ "$want" = "$got" ] && pass=$((pass+1)); echo "want $want got $got $([ "$want" = "$got" ] && echo PASS || echo MISMATCH) :: $* :: $(head -c 240 "$G/out/r2/controls_last.err" | tr '\n' ' ')"; }
ctl 0  QA1035_VER_FILE=$G/fixtures/pos_ver_develop_28fb58343.ts
ctl 19 QA1035_VER_FILE=$G/fixtures/pos_ver_landed_f888e8cd0.ts
ctl 18 QA1035_VER_FILE=$G/fixtures/neg_ver_unpinned_edit.ts
ctl 0  QA1035_CUR_DEV=732c13459d76f5b05ade94bb91de7e47585b0e7d
ctl 0  QA1035_CUR_DEV=3961c2add8e1637b32e638f8f0952c328c00833e
ctl 18 QA1035_CUR_DEV=27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d
ctl 18 QA1035_CUR_DEV=fd81a75f0688f6cbe1e5f79b061bb1369c88f477
ctl 19 QA1035_CUR_DEV=4b1fb0621e58ff00bba096751130bc6e53df4714
ctl 6  QA1035_HEAD=732c13459d76f5b05ade94bb91de7e47585b0e7d
ctl 23 QA1035_PROMPT=$G/fixtures/neg_prompt_nosubject.txt
ctl 22 QA1035_PROMPT=$G/fixtures/neg_prompt_nofarm.txt
ctl 24 QA1035_PROMPT=$G/fixtures/neg_prompt_noprior.txt
ctl 24 QA1035_PROMPT=$G/fixtures/neg_prompt_nottestedfirst.txt
ctl 25 QA1035_PROMPT=$G/fixtures/neg_prompt_nocsn.txt
ctl 25 QA1035_BRIEF=$G/fixtures/neg_brief_noaddendum.md
ctl 20 QA1035_BRIEF=$G/fixtures/neg_brief_nosha.md
ctl 15 QA1035_BRIEF=$G/fixtures/neg_brief_round2.md
ctl 7  QA1035_BRIEF=$G/fixtures/neg_brief_tier2.md
echo "controls end $(date '+%H:%M:%S %Z') | controls PASS $pass / $n"
