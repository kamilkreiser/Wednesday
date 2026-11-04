#!/bin/bash
# Gate 180 Q2c: r3 re-run WITHOUT the unsandboxed consumers (instrument error in q3b: consumers_full's plain set -a made the r3 artifact).
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate180-ks915-pr1989-r3/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q3c}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG; RUNTMP=$W/tmp/$TAG
M=gate180rmt; N=$'\n'
GB=$W/runs/golden/golden_blankadmin.env.bin; GL=$W/scratch/golden/Blockchain/Dev/.env.local
NOCONS=1 gcell r3 "GATE_A=1; exec 2<&-${N}GATE_B=1; PATH=/usr/bin:/bin; touch $W/tmp/$TAG/r3_art$N" '' ''
echo "   r3 artifact after the SCRIPT only: $([[ -e $W/tmp/$TAG/r3_art ]] && echo CREATED || echo absent)"
( env -i PATH=/usr/bin:/bin bash -c 'set -a; . "$1"' _ "$LASTCLONE/Blockchain/Dev/.env" ) >/dev/null 2>&1
echo "   control, then a plain unsandboxed set -a on the same .env: $([[ -e $W/tmp/$TAG/r3_art ]] && echo CREATED || echo absent)"
