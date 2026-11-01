#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900
GD=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/gate
T=Blockchain/Dev/services/kyc/src/__tests__
bash $GD/spark_gate.sh $W/repo 1900 a06c3441c2371a6f33bb75855e9953d55990de87 develop \
  $T/ks1868-kyc-save-verification-unreadable-throw.test.ts \
  $T/ks1868-kyc-get-verification-unreadable-throw.test.ts \
  $T/ks1868-kyc-get-verifications-by-user-unreadable-throw.test.ts \
  $T/ks1868-kyc-get-verification-stats-unreadable-throw.test.ts \
  $T/ks1868-kyc-save-consent-unreadable-throw.test.ts \
  --node-modules $W/repo/Blockchain/Dev/node_modules \
  --work /private/tmp/gate85_spark/work --out /private/tmp/gate85_spark/work/out > $W/logs/spark_gate.log 2>&1
echo "spark_gate rc=$?" >> $W/logs/spark_gate.log
cp -R /private/tmp/gate85_spark/work/out $W/evidence/spark_shadow/gate_out
cat $W/logs/spark_gate.log
