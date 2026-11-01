#!/bin/bash
# Gate 70: the remaining probe runs, strictly one at a time (each waits for load1 <= 8 inside jest_run.sh).
#   1. probe70 at the head;
#   2. the base swap (31d146678): gate 65's and gate 68's ORIGINAL probes, and probe70.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate70-ks1384-r2b-1884
P=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference
bash $G/scripts/probe_run.sh $G/evidence/probe/gate70-r2b-probe.integration.test.ts probe70_head_app.log
bash $G/scripts/swap_base_run.sh 31d1466788bea96f6175b595c8fb3078229668be base31d1 \
  "$P/2026-11-01_gate65-r1r3-1868/evidence/probe/gate65-r1r3-probe.integration.test.ts|probe65_base31d1_app.log" \
  "$P/2026-11-01_gate68-ks1384-r2a-1874/evidence/probe/gate68-r2a-probe.integration.test.ts|probe68_base31d1_app.log" \
  "$G/evidence/probe/gate70-r2b-probe.integration.test.ts|probe70_base31d1_app.log" > $G/evidence/swap_base_31d1.out 2>&1
echo "swap rc=$?"
grep -v "load1=" $G/evidence/swap_base_31d1.out
echo CHAIN_DONE
