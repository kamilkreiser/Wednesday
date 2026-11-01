#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate80-ks1868-governance-1895
R=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs
H=$W/wt_head/Blockchain/Dev/services/governance/src/__tests__
P=spark_secuura_2026-11-01_ks_1868
LOG=$W/logs/q2_test_vs_canonical.log; : > $LOG
: > $W/evidence/prod_canon_all.txt
while read k rd; do
  d=$R/$rd/out.md.checker
  grep -E '^\+' $d/section_2.diff | grep -v '^+++' | sed 's/^+//' > $W/evidence/canon_$k.ts
  echo "=== $k (run dir $rd)" >> $LOG
  grep -E '^(---|\+\+\+|@@|new file)' $d/section_2.diff >> $LOG
  echo "sha256 committed: $(shasum -a 256 < $H/$k.test.ts)  canon: $(shasum -a 256 < $W/evidence/canon_$k.ts)" >> $LOG
  diff $W/evidence/canon_$k.ts $H/$k.test.ts >> $LOG 2>&1; echo "diff rc=$? (0 same, 1 differs)" >> $LOG
  echo "committed lines=$(wc -l < $H/$k.test.ts) canon lines=$(wc -l < $W/evidence/canon_$k.ts) export-lines=$(grep -c '^export {};$' $H/$k.test.ts)" >> $LOG
  grep -E '^[+-]' $d/section_1.diff | grep -vE '^(\+\+\+|---)' >> $W/evidence/prod_canon_all.txt
done <<EOL
ks1868-db-get-proposal-unreadable-throw ${P}_o43_p2_governance_dbgetproposal_unreadable_throw-r2
ks1868-get-all-proposals-unreadable-throw ${P}_o44_p1_governance_get_all_proposals_unreadable_throw
ks1868-get-all-participants-unreadable-throw ${P}_o44_p2_governance_get_all_participants_unreadable_throw
ks1868-get-active-delegations-unreadable-throw ${P}_o44_p3_governance_get_active_delegations_unreadable_throw
ks1868-get-total-vote-power-unreadable-throw ${P}_o44_p4_governance_get_total_vote_power_unreadable_throw
EOL
git -C $W/repo diff -U0 refs/gate/develop refs/gate/pr1895 -- Blockchain/Dev/services/governance/src/services/governanceService.ts | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)' > $W/evidence/prod_head.txt
echo "canon product +/- lines: $(wc -l < $W/evidence/prod_canon_all.txt) ; head product +/- lines: $(wc -l < $W/evidence/prod_head.txt)" >> $LOG
diff <(sort $W/evidence/prod_canon_all.txt) <(sort $W/evidence/prod_head.txt) >> $LOG 2>&1; echo "product multiset diff rc=$?" >> $LOG
