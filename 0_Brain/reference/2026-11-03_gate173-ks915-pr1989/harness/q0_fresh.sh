#!/bin/bash
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989/harness/lib.sh
mkdir -p $W/runs/q0
c=$(mkclone ${1:-fresh0}) || exit 1
rc=$(run "$c" $W/runs/q0/${1:-fresh0}.log); echo rc=$rc
cat $W/runs/q0/${1:-fresh0}.log
