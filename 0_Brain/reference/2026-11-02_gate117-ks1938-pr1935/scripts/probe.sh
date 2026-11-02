#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate117-ks1938-pr1935
O=$W/repo/Blockchain/Dev/services/originate
P=$O/src/services/gdprService.ts
T=$O/src/__tests__/g117_probe.test.ts
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/0b6f2563-591e-4408-ab3d-78a74ca3c4e8/scratchpad
HEADSHA=$(shasum -a 256 $W/evidence/src/gdpr_head.ts | cut -d' ' -f1)
[ "$(shasum -a 256 $P | cut -d' ' -f1)" = "$HEADSHA" ] || { echo "product not head at start"; exit 3; }
cp $W/scripts/g117_probe.test.ts $T
for stage in head base; do
  if [ $stage = base ]; then cp $W/evidence/src/gdpr_base.ts $P; fi
  (cd $O && G117_OUT=$W/logs/probe_$stage.json npx jest --runInBand src/__tests__/g117_probe.test.ts > $W/logs/probe_${stage}_jest.log 2>&1); echo "$stage jest rc=$?"
done
cp $W/evidence/src/gdpr_head.ts $P
[ "$(shasum -a 256 $P | cut -d' ' -f1)" = "$HEADSHA" ] && echo RESTORE_OK
mkdir -p $W/logs/_quarantine; mv $T $W/logs/_quarantine/
git -C $W/repo status --short
