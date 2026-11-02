#!/bin/bash
# usage: probe.sh <name> <base|head>  -- copies scripts/g131_probe_<name>.test.ts into the clone, swaps product, runs, moves it out
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate131-ks1868-pr1949
T=$G/repo/Blockchain/Dev/services/auth/src/__tests__/g131_probe_$1.test.ts
cp $G/scripts/g131_probe_$1.test.ts $T
$G/scripts/swap.sh $2 > $G/logs/probe_$1_$2_swap.log
G131_OUT=$G/logs/probe_$1_$2.json $G/scripts/vt.sh $G/logs/probe_$1_$2_vitest.log src/__tests__/g131_probe_$1.test.ts; RC=$?
mkdir -p $G/logs/_quarantine; mv $T $G/logs/_quarantine/g131_probe_$1.test.ts.$2
$G/scripts/swap.sh head > $G/logs/probe_$1_restore.log
echo "probe $1 $2 rc=$RC"
