#!/bin/bash
# usage: probe.sh base|head  (swaps both product files for base, restores). Probe file moved to quarantine, never deleted.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate130-ks1868-pr1948
S=$W/repo/Blockchain/Dev/services/security/src
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $S/index.ts); H2=$(sha $S/db.ts); Q=$W/logs/_quarantine; mkdir -p $Q
if [ "$1" = base ]; then cp $W/logs/base_index.ts $S/index.ts; cp $W/logs/base_db.ts $S/db.ts; fi
echo "product sha for $1: $(sha $S/index.ts) $(sha $S/db.ts)"
for fmt in test production; do
  cp $W/scripts/probe_validate.test.ts $S/__tests__/zz-gate130-probe.test.ts
  : > $W/logs/probe_${1}_${fmt}.jsonl
  PROBE_FMT=$fmt PROBE_OUT=$W/logs/probe_${1}_${fmt}.jsonl bash $W/scripts/vt.sh $W/logs/probe_${1}_${fmt}_vitest.log zz-gate130-probe; echo "probe $1 $fmt rc=$?"
  mv $S/__tests__/zz-gate130-probe.test.ts $Q/probe_${1}_${fmt}.test.ts
done
cp $W/logs/head_index.ts $S/index.ts; cp $W/logs/head_db.ts $S/db.ts
[ "$(sha $S/index.ts)" = "$H1" ] && [ "$(sha $S/db.ts)" = "$H2" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate130-ks1868-pr1948/repo status --short
