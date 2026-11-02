#!/bin/bash
# usage: vt.sh <log> [files...]  (vitest anchored at the m365 service in this workdir)
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate154-ks1868-pr1971
L=$1; shift
ND=$W/repo/Blockchain/Dev/node_modules/.bin/vitest
$ND run --root $W/repo/Blockchain/Dev/services/m365-integration --maxWorkers=2 "$@" > $L 2>&1
echo rc=$? >> $L
tail -8 $L
