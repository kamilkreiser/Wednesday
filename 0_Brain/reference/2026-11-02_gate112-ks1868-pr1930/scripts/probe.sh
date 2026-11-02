#!/bin/bash
# usage: probe.sh <base|head> <test|production> [probe-name]   swaps product for base, restores head; probe file moved to quarantine after.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate112-ks1868-pr1930
A=$G/repo/Blockchain/Dev/services/security/src; L=$G/logs; Q=$L/_quarantine; mkdir -p $Q
P=${3:-g112_probe}
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
if [ "$1" = base ]; then cp $L/index_base.ts $A/index.ts; cp $L/db_base.ts $A/db.ts; fi
echo "product $1: $(sha $A/index.ts | cut -c1-12) $(sha $A/db.ts | cut -c1-12)"
cp $G/scripts/$P.test.ts $A/__tests__/zz-$P.test.ts
OUT=$L/${P}_$1_$2.jsonl; : > $OUT
PROBE_OUT=$OUT LOGFMT=$2 bash $G/scripts/vt.sh $L/${P}_$1_$2_vitest.log src/__tests__/zz-$P.test.ts; echo "probe $P $1 $2 rc=$?"
mv $A/__tests__/zz-$P.test.ts $Q/${P}_$1_$2.test.ts
cp $L/index_head.ts $A/index.ts; cp $L/db_head.ts $A/db.ts
[ "$(sha $A/index.ts)" = "$(sha $L/index_head.ts)" ] && [ "$(sha $A/db.ts)" = "$(sha $L/db_head.ts)" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate112-ks1868-pr1930/repo status --short
