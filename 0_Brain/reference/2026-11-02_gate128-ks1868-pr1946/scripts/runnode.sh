#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
O=$W/repo/Blockchain/Dev/services/originate
git -C $W/repo show e2a2426d221d:Blockchain/Dev/services/originate/src/services/retentionScheduler.ts > $W/scratch_base_retentionScheduler.ts
for v in base head; do
 if [ $v = base ]; then F=$W/scratch_base_retentionScheduler.ts; else F=$O/src/services/retentionScheduler.ts; fi
 for k in ordinary string revokedProxy throwingGetter getterRevokedProxy getterThrowingToJSON; do
  echo "== $v $k"; node $W/scripts/nodeprobe.js $O $F $k 2>&1 | cut -c1-300 | head -6
 done
done
