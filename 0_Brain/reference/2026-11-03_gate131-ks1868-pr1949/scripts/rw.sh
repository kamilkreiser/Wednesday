#!/bin/bash
# usage: rw.sh <base|head> : runs the 4 PR test files with the logger mock wrapping the REAL winston logger
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate131-ks1868-pr1949
A=$G/repo/Blockchain/Dev/services/auth/src/__tests__
for k in internal issuer oauth authrd; do cp $G/scripts/realwinston/g131_rw_$k.test.ts $A/; done
$G/scripts/swap.sh $1 > $G/logs/rw_$1_swap.log
$G/scripts/vt.sh $G/logs/rw_$1_vitest.log src/__tests__/g131_rw_internal.test.ts src/__tests__/g131_rw_issuer.test.ts src/__tests__/g131_rw_oauth.test.ts src/__tests__/g131_rw_authrd.test.ts --hookTimeout=60000 --testTimeout=30000; RC=$?
mkdir -p $G/logs/_quarantine/rw_$1; for k in internal issuer oauth authrd; do mv $A/g131_rw_$k.test.ts $G/logs/_quarantine/rw_$1/; done
$G/scripts/swap.sh head > $G/logs/rw_restore.log
echo "rw $1 rc=$RC"
