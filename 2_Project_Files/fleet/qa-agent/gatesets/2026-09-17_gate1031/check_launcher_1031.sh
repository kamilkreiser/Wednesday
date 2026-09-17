#!/bin/zsh
# check_launcher_1031.sh — runs the #1031 launcher with --check ONLY (never a launch), stdin /dev/null, rc printed on its own line; then fixture/override
# controls that MUST refuse with the named exit (and ones that must pass). Every control passes --check. Never a launch.
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1213_1031.sh
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1031
echo "check start $(date '+%Y-%m-%d %H:%M:%S %Z') launcher sha256 $(shasum -a 256 "$L" | cut -c1-16) mode $(stat -f '%Lp' "$L")"
"$L" --check < /dev/null
rc=$?
echo "check end $(date '+%H:%M:%S %Z')"
echo "launcher --check rc=$rc"
echo "--- controls (each: want rc, got rc)"
ctl() { want=$1; shift; env "$@" "$L" --check < /dev/null > "$G/out/controls_last.out" 2> "$G/out/controls_last.err"; got=$?; echo "want $want got $got $([ "$want" = "$got" ] && echo PASS || echo MISMATCH) :: $* :: $(head -c 220 "$G/out/controls_last.err" | tr '\n' ' ')"; }
ctl 0  QA1031_DOCS_FILE=$G/fixtures/pos_docs_develop_de9b5ae25.ts
ctl 19 QA1031_DOCS_FILE=$G/fixtures/pos_docs_landed_e3eeb5a68.ts
ctl 18 QA1031_DOCS_FILE=$G/fixtures/neg_docs_unpinned_edit.ts
ctl 0  QA1031_CUR_DEV=75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e
ctl 18 QA1031_CUR_DEV=19f1e54750ce2b65312a687add2db4f5628edb7d
ctl 6  QA1031_HEAD=450e3429ddd66a479231d259cd201fcddbe2b5a4
ctl 23 QA1031_PROMPT=$G/fixtures/neg_prompt_nosubject.txt
ctl 22 QA1031_PROMPT=$G/fixtures/neg_prompt_nofarm.txt
ctl 24 QA1031_PROMPT=$G/fixtures/neg_prompt_noprior.txt
ctl 24 QA1031_PROMPT=$G/fixtures/neg_prompt_nottestedfirst.txt
ctl 25 QA1031_PROMPT=$G/fixtures/neg_prompt_nocsn.txt
ctl 25 QA1031_BRIEF=$G/fixtures/neg_brief_noaddendum.md
ctl 20 QA1031_BRIEF=$G/fixtures/neg_brief_nosha.md
ctl 15 QA1031_BRIEF=$G/fixtures/neg_brief_round2.md
ctl 7  QA1031_BRIEF=$G/fixtures/neg_brief_tier2.md
echo "controls end $(date '+%H:%M:%S %Z')"
