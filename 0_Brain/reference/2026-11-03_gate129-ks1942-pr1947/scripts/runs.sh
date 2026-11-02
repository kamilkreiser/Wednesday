#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947
R=$G/repo; T=$R/Blockchain/Dev/services/governance/src/__tests__; MB=1584c0f0ff808fddf35245bee41b6b5f9231054c; Q=$G/logs/_quarantine; mkdir -p $Q $G/logs/tests_head
NEW=ks1942-register-binds-the-linked-wallet-and-stake-is-admin-set.test.ts
K40=ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts
GOV=governance.test.ts
for f in $NEW $K40 $GOV; do cp $T/$f $G/logs/tests_head/$f; done
sh(){ shasum -a 256 "$1" | cut -c1-16; }
echo "head test shas: $(sh $T/$NEW) $(sh $T/$K40) $(sh $T/$GOV)"
# 1 green at head: the three changed test files
bash $G/scripts/jt.sh $G/logs/head_changed_tests.log --json --outputFile=$G/logs/head_changed_tests.json "ks1942-register|ks1940-failed|/governance.test"; echo "head changed tests rc=$?"
# 2 red-first: base product + head tests
bash $G/scripts/swap.sh base
bash $G/scripts/jt.sh $G/logs/red_base_changed_tests.log --json --outputFile=$G/logs/red_base_changed_tests.json "ks1942-register|ks1940-failed|/governance.test"; echo "red rc=$?"
# 3 base whole suite: base product + base tests (new file moved out)
mv $T/$NEW $Q/$NEW.during_base_suite
git -C $R show $MB:Blockchain/Dev/services/governance/src/__tests__/$K40 > $T/$K40
git -C $R show $MB:Blockchain/Dev/services/governance/src/__tests__/$GOV > $T/$GOV
bash $G/scripts/jt.sh $G/logs/base_whole.log --json --outputFile=$G/logs/base_whole.json; echo "base whole rc=$?"
# restore
cp $G/logs/tests_head/$NEW $T/$NEW; cp $G/logs/tests_head/$K40 $T/$K40; cp $G/logs/tests_head/$GOV $T/$GOV
bash $G/scripts/swap.sh head
echo "restored test shas: $(sh $T/$NEW) $(sh $T/$K40) $(sh $T/$GOV)"
git -C $R status --short
# 4 head whole suite
bash $G/scripts/jt.sh $G/logs/head_whole.log --json --outputFile=$G/logs/head_whole.json; echo "head whole rc=$?"
