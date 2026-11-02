#!/bin/bash
# usage: probe_fix.sh FA|FAC  -- the probe on a gate-made candidate fix of the product (NOT the PR); head restored after
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate134-ks1950-pr1952
R=$G/repo; S=$R/Blockchain/Dev/services/governance/src; A=$R/Blockchain/Dev/services/governance; Q=$G/logs/_quarantine; mkdir -p $Q
cp $G/logs/prod/fix/$1_services_governanceService.ts $S/services/governanceService.ts
cp $G/scripts/probe.test.ts $A/src/__tests__/zz-gate134-probe.test.ts
: > $G/logs/probe_fix$1.jsonl
PROBE_OUT=$G/logs/probe_fix$1.jsonl RACE_N=${RACE_N:-300} bash $G/scripts/jt.sh $G/logs/probe_fix$1_jest.log zz-gate134-probe; echo "probe fix $1 rc=$?"
mv $A/src/__tests__/zz-gate134-probe.test.ts $Q/probe_fix$1_$(date +%H%M%S).test.ts
bash $G/scripts/swap.sh head
git -C $R status --short
