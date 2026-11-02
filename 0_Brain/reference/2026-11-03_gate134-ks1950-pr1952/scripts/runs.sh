#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate134-ks1950-pr1952
R=$G/repo; T=$R/Blockchain/Dev/services/governance/src/__tests__; MB=8150eeb3802bd9cfe5242ffbc49278c1a3739a84; Q=$G/logs/_quarantine; mkdir -p $Q $G/logs/tests_head
NEW=ks1950-an-admin-change-made-mid-request-is-not-reverted-by-a-stale-row-write.test.ts
K40=ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts
K42=ks1942-register-binds-the-linked-wallet-and-stake-is-admin-set.test.ts
for f in $NEW $K40 $K42; do cp $T/$f $G/logs/tests_head/$f; done
sh(){ shasum -a 256 "$1" | cut -c1-16; }
echo "head test shas: $(sh $T/$NEW) $(sh $T/$K40) $(sh $T/$K42)"
bash $G/scripts/jt.sh $G/logs/head_changed_tests.log --json --outputFile=$G/logs/head_changed_tests.json "ks1950-an-admin|ks1940-failed|ks1942-register"; echo "head changed tests rc=$?"
bash $G/scripts/swap.sh base
bash $G/scripts/jt.sh $G/logs/red_base_changed_tests.log --json --outputFile=$G/logs/red_base_changed_tests.json "ks1950-an-admin|ks1940-failed|ks1942-register"; echo "red rc=$?"
mv $T/$NEW $Q/$NEW.during_base_suite
git -C $R show $MB:Blockchain/Dev/services/governance/src/__tests__/$K40 > $T/$K40
git -C $R show $MB:Blockchain/Dev/services/governance/src/__tests__/$K42 > $T/$K42
bash $G/scripts/jt.sh $G/logs/base_whole.log --json --outputFile=$G/logs/base_whole.json; echo "base whole rc=$?"
cp $G/logs/tests_head/$NEW $T/$NEW; cp $G/logs/tests_head/$K40 $T/$K40; cp $G/logs/tests_head/$K42 $T/$K42
bash $G/scripts/swap.sh head
echo "restored test shas: $(sh $T/$NEW) $(sh $T/$K40) $(sh $T/$K42)"
git -C $R status --short
bash $G/scripts/jt.sh $G/logs/head_whole.log --json --outputFile=$G/logs/head_whole.json; echo "head whole rc=$?"
