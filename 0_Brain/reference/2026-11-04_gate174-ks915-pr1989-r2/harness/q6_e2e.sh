#!/bin/bash
# Q6 through the whole script: a .env line the bash reader runs that reassigns PATH (bash 3.2 `set -r` does not lock it)
# and then runs an external command that creates a file outside the sandbox. Plus the suite's x1/x2 forms as controls.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q6e}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG $W/tmp/${TAG}-art; RUNTMP=$W/tmp/$TAG; A=$W/tmp/${TAG}-art
M=gate174rmt; N=$'\n'; GB=$W/runs/golden/golden_blankadmin.env.bin; GL=$W/scratch/golden/Blockchain/Dev/.env.local
NOCONS=1 gcell e1 "X=1; PATH=/usr/bin:/bin; touch $A/e1_created$N" '' ''
echo "   e1 artifact outside the sandbox: $([[ -e $A/e1_created ]] && echo CREATED || echo absent)"
NOCONS=1 gcell e2 "X=1; PATH=/usr/bin:/bin; printf 'NODE_ENV=production\\n' | tee $A/e2_created >/dev/null$N" '' ''
echo "   e2 artifact: $([[ -e $A/e2_created ]] && echo CREATED || echo absent)"
NOCONS=1 gcell e3 "history -s NODE_ENV=production; history -w $A/e3_hist$N" '' ''
echo "   e3 (suite x1 form) artifact: $([[ -e $A/e3_hist ]] && echo CREATED || echo absent)"
NOCONS=1 gcell e4 "X=1; PATH=/usr/bin:/bin; command -v openssl >/dev/null && touch $A/e4_ran_with_real_path$N" '' ''
echo "   e4 artifact: $([[ -e $A/e4_ran_with_real_path ]] && echo CREATED || echo absent)"
