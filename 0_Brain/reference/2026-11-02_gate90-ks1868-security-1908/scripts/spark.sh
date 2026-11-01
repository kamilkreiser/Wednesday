#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate90-ks1868-security-1908
GD=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/gate
T=Blockchain/Dev/services/security/src/__tests__
bash $GD/spark_gate.sh $W/repo 1908 c7bcdca341465c57bb4c59e8efe480ffabb9301c develop \
  $T/ks1868-security-revoke-prior-connector-keys-unreadable-throw.test.ts \
  $T/ks1868-security-save-key-and-retire-priors-unreadable-throw.test.ts \
  --node-modules $W/repo/Blockchain/Dev/node_modules \
  --work /private/tmp/gate90_spark/work --out /private/tmp/gate90_spark/work/out > $W/logs/spark_gate.log 2>&1
echo "spark_gate rc=$?" >> $W/logs/spark_gate.log
mkdir -p $W/evidence/spark_shadow
cp -R /private/tmp/gate90_spark/work/out $W/evidence/spark_shadow/gate_out
mkdir -p /private/tmp/gate90_spark/review
SPARK_THINK=0 python3 $GD/spark_review.py --repo $W/repo --head-sha c7bcdca341465c57bb4c59e8efe480ffabb9301c \
  --facts /private/tmp/gate90_spark/work/out/facts.json --diff /private/tmp/gate90_spark/work/out/diff.patch \
  --ticket KS-1868 --pr-body-file $W/evidence/pr_body_substitute.md --out /private/tmp/gate90_spark/review > $W/logs/spark_review.log 2>&1
echo "spark_review rc=$?" >> $W/logs/spark_review.log
cp -R /private/tmp/gate90_spark/review $W/evidence/spark_shadow/review
