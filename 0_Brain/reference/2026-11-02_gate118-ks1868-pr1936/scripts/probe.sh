#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate118-ks1868-pr1936
O=$W/repo/Blockchain/Dev/services/originate
T=$O/src/__tests__/g118_probe.test.ts
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/0b6f2563-591e-4408-ab3d-78a74ca3c4e8/scratchpad
for f in signatories thirdPartyVerifiers; do
  [ "$(shasum -a 256 $O/src/routes/$f.ts | cut -d' ' -f1)" = "$(shasum -a 256 $W/evidence/src/${f}_head.ts | cut -d' ' -f1)" ] || { echo "$f not head at start"; exit 3; }
done
cp $W/scripts/g118_probe.test.ts $T
for stage in head base; do
  if [ $stage = base ]; then for f in signatories thirdPartyVerifiers; do cp $W/evidence/src/${f}_base.ts $O/src/routes/$f.ts; done; fi
  G118_OUT=$W/logs/probe_$stage.json nice -n 10 $W/repo/Blockchain/Dev/node_modules/.bin/jest --rootDir $O --config $O/jest.config.js --runInBand --forceExit --runTestsByPath $T > $W/logs/probe_${stage}_jest.log 2>&1; echo "$stage jest rc=$?"
done
for f in signatories thirdPartyVerifiers; do cp $W/evidence/src/${f}_head.ts $O/src/routes/$f.ts
  [ "$(shasum -a 256 $O/src/routes/$f.ts | cut -d' ' -f1)" = "$(shasum -a 256 $W/evidence/src/${f}_head.ts | cut -d' ' -f1)" ] && echo "RESTORE_OK $f"; done
mkdir -p $W/logs/_quarantine; mv $T $W/logs/_quarantine/
git -C $W/repo status --short
