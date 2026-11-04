#!/bin/bash
# Gate 180 Q2b: E 33rd's declared residual (an earlier line shuts/redirects the reader's stderr), written so compose and dotenv parse every line.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate180-ks915-pr1989-r3/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q3b}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG; RUNTMP=$W/tmp/$TAG
M=gate180rmt; N=$'\n'
GB=$W/runs/golden/golden_blankadmin.env.bin; GL=$W/scratch/golden/Blockchain/Dev/.env.local
gcell r1 "GATE_A=1; exec 2<&-${N}GATE_B=1; PATH=/usr/bin:/bin; declare -x POSTGRES_\"\"HOST=$M.host$N" '' ''
gcell r2 "GATE_A=1; exec 2<&1${N}GATE_B=1; PATH=/usr/bin:/bin; declare -x POSTGRES_\"\"HOST=$M.host$N" '' ''
gcell r3 "GATE_A=1; exec 2<&-${N}GATE_B=1; PATH=/usr/bin:/bin; touch $W/tmp/$TAG/r3_art$N" '' ''
echo "   r3 artifact: $([[ -e $W/tmp/$TAG/r3_art ]] && echo CREATED || echo absent)"
gcell r0 "GATE_B=1; PATH=/usr/bin:/bin; declare -x POSTGRES_\"\"HOST=$M.host$N" '' ''
