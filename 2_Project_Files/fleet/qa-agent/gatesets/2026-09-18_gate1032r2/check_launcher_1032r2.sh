#!/bin/zsh
# check_launcher_1032r2.sh — runs the #1032 ROUND 2 launcher with --check ONLY (never a launch), stdin /dev/null, rc printed on its own line; then fixture/override
# controls that MUST refuse with the named exit (and ones that must pass). Every control passes --check. Never a launch. (From the round-1 check_launcher_1032.sh.)
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1194_1032r2.sh
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1032r2
echo "check start $(date '+%Y-%m-%d %H:%M:%S %Z') launcher sha256 $(shasum -a 256 "$L" | cut -c1-16) mode $(stat -f '%Lp' "$L")"
"$L" --check < /dev/null
rc=$?
echo "check end $(date '+%H:%M:%S %Z')"
echo "launcher --check rc=$rc"
[ "${1:-}" = "--no-controls" ] && exit $rc
echo "--- controls (each: want rc, got rc)"
ctl() { want=$1; shift; env "$@" "$L" --check < /dev/null > "$G/out/controls_last.out" 2> "$G/out/controls_last.err"; got=$?; echo "want $want got $got $([ "$want" = "$got" ] && echo PASS || echo MISMATCH) :: $* :: $(head -c 260 "$G/out/controls_last.err" | tr '\n' ' ') $(grep -m1 'develop' "$G/out/controls_last.out" | head -c 160)"; }
ctl 0  QA1032R2_USERS_FILE=$G/fixtures/pos_users_develop_c723a68af.ts
ctl 19 QA1032R2_USERS_FILE=$G/fixtures/pos_users_landed_r1_8299a2558.ts
ctl 19 QA1032R2_USERS_FILE=$G/fixtures/pos_users_landed_r2_3bfa47dcd.ts
ctl 18 QA1032R2_USERS_FILE=$G/fixtures/neg_users_unpinned_edit.ts
ctl 0  QA1032R2_CUR_DEV=3961c2add8e1637b32e638f8f0952c328c00833e
ctl 18 QA1032R2_CUR_DEV=4b251997a96034ee8a3359aac357ee17d222c3ef
ctl 18 QA1032R2_CUR_DEV=0a2b1603fe52f0f3b8152588af78bbeab0237be7
ctl 19 QA1032R2_CUR_DEV=70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039
ctl 19 QA1032R2_CUR_DEV=4306726977b55171a7c8c0eb5e42de078587a725
ctl 6  QA1032R2_HEAD=70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039
ctl 23 QA1032R2_PROMPT=$G/fixtures/neg_prompt_nosubject.txt
ctl 22 QA1032R2_PROMPT=$G/fixtures/neg_prompt_nofarm.txt
ctl 24 QA1032R2_PROMPT=$G/fixtures/neg_prompt_nor1report.txt
ctl 24 QA1032R2_PROMPT=$G/fixtures/neg_prompt_nottestedfirst.txt
ctl 25 QA1032R2_PROMPT=$G/fixtures/neg_prompt_nocsn.txt
ctl 25 QA1032R2_PROMPT=$G/fixtures/neg_prompt_nokamstap.txt
ctl 25 QA1032R2_BRIEF=$G/fixtures/neg_brief_noaddendum.md
ctl 25 QA1032R2_BRIEF=$G/fixtures/neg_brief_nokamstap.md
ctl 20 QA1032R2_BRIEF=$G/fixtures/neg_brief_nosha.md
ctl 15 QA1032R2_BRIEF=$G/fixtures/neg_brief_round1.md
ctl 7  QA1032R2_BRIEF=$G/fixtures/neg_brief_tier2.md
echo "controls end $(date '+%H:%M:%S %Z')"
