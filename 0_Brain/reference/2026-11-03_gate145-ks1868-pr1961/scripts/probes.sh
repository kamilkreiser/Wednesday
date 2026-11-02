#!/bin/bash
# Q1 erasure probe (5 modes) and Q2/Q3 real-logger recorder (dev + production NODE_ENV), head then base products. sha-restored; probe files quarantined.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate145-ks1868-pr1961
R=$W/repo; O=$R/Blockchain/Dev/services/originate; REL=Blockchain/Dev/services/originate
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
P1=src/services/errorTrackingService.ts; P2=src/utils/lifecyclePayloadCodec.ts; H1=$(sha $O/$P1); H2=$(sha $O/$P2)
mkdir -p $W/logs/probe $W/logs/_quarantine
cp $W/scripts/probe_g145.test.ts $O/src/__tests__/zz_g145_probe.test.ts
cp $W/scripts/rec_g145.test.ts $O/src/__tests__/zz_g145_rec.test.ts
for ver in head base; do
  if [ $ver = base ]; then for p in $P1 $P2; do git -C $R show 2d3b3bb3:$REL/$p > $O/$p; done; fi
  for m in none ordinary revokedProxy getterThrows nullProto; do
    G145_MODE=$m G145_OUT=$W/logs/probe/erasure_${ver}_$m.json node $W/scripts/jest.js --runTestsByPath $O/src/__tests__/zz_g145_probe.test.ts > $W/logs/probe/erasure_${ver}_$m.log 2>&1; echo "rc=$?" >> $W/logs/probe/erasure_${ver}_$m.log
  done
  for env in development production; do
    NODE_ENV=$env G145_OUT=$W/logs/probe/rec_${ver}_$env.json node $W/scripts/jest.js --runTestsByPath $O/src/__tests__/zz_g145_rec.test.ts > $W/logs/probe/rec_${ver}_$env.log 2>&1; echo "rc=$?" >> $W/logs/probe/rec_${ver}_$env.log
  done
done
for p in $P1 $P2; do git -C $R show pr1961:$REL/$p > $O/$p; done
mv $O/src/__tests__/zz_g145_probe.test.ts $W/logs/_quarantine/zz_g145_probe.test.ts
mv $O/src/__tests__/zz_g145_rec.test.ts $W/logs/_quarantine/zz_g145_rec.test.ts
{ [ "$(sha $O/$P1)" = "$H1" ] && [ "$(sha $O/$P2)" = "$H2" ] && echo "restore OK" || echo "RESTORE FAIL"; git -C $R status --short; } > $W/logs/probes_restore.log
echo done > $W/logs/probes.done
