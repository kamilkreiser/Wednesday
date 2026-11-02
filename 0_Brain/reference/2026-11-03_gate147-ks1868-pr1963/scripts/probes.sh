#!/bin/bash
# Probe at head and base (product file swapped from the merge-base, sha-restored). Probe files copied in, quarantined after.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate147-ks1868-pr1963
R=$W/repo; D=$R/Blockchain/Dev; MB=4d1ab2cb6574e2b221353ac3a1de56d515711aaf
TAG=${1:-run1}; P=$W/logs/probe_$TAG; Q=$W/logs/_quarantine/$TAG
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
mkdir -p $P $Q
K=$D/services/kyc/src/userErasedSubscriber.ts; WC=$D/services/wallet-connector/src/userErasedSubscriber.ts
HK=$(sha $K); HW=$(sha $WC)
cp $W/scripts/zz_g147_kyc_probe.test.ts $D/services/kyc/src/__tests__/; cp $W/scripts/zz_g147_wc_probe.test.ts $D/services/wallet-connector/src/__tests__/
for ver in head base; do
  if [ $ver = base ]; then git -C $R show $MB:Blockchain/Dev/services/kyc/src/userErasedSubscriber.ts > $K; git -C $R show $MB:Blockchain/Dev/services/wallet-connector/src/userErasedSubscriber.ts > $WC; fi
  echo "$ver kyc sha $(sha $K) wc sha $(sha $WC)" >> $P/shas.log
  PROBE_VER=$ver PROBE_OUT=$P/kyc_$ver.jsonl node $W/scripts/vt.js kyc src/__tests__/zz_g147_kyc_probe.test.ts > $P/kyc_$ver.log 2>&1; echo "rc=$?" >> $P/kyc_$ver.log
  for fmt in dev prod; do
    PROBE_FMT=$fmt PROBE_VER=$ver PROBE_OUT=$P/wc_${ver}_$fmt.jsonl node $W/scripts/vt.js wallet-connector src/__tests__/zz_g147_wc_probe.test.ts > $P/wc_${ver}_$fmt.log 2>&1; echo "rc=$?" >> $P/wc_${ver}_$fmt.log
  done
done
git -C $R show pr1963:Blockchain/Dev/services/kyc/src/userErasedSubscriber.ts > $K; git -C $R show pr1963:Blockchain/Dev/services/wallet-connector/src/userErasedSubscriber.ts > $WC
mv $D/services/kyc/src/__tests__/zz_g147_kyc_probe.test.ts $Q/; mv $D/services/wallet-connector/src/__tests__/zz_g147_wc_probe.test.ts $Q/
{ [ "$(sha $K)" = "$HK" ] && [ "$(sha $WC)" = "$HW" ] && echo "restore OK" || echo "RESTORE FAIL"; git -C $R status --short; } > $P/restore.log
echo done > $P/probes.done
