# READY (hand-written note: hold_ready.py REFUSES a loose code_patch2 PASS, A3x unmeasured) - O30-P1 (KS-1544 class, staking rewards.ts)

Spark operator 30, 2026-10-30. Rung 5 LOOSE (one product, 2 hunks, product lines written by the model, hunk headers dictated, per-hunk skeleton, explicit new-file header skeleton in the ORIGINAL brief). **A PASS is a candidate, never a merge.** The two sites are NOT named in KS-1544 (it names tenant-provisioning); same class (paged ORDER BY with no unique last key), found by op 29, re-read by op 30 at the tip. Wednesday decides: raise as `Refs KS-1544` or file a new ticket.

- What: staking src/routes/rewards.ts :315 `ORDER BY claimed_at` -> `claimed_at, id` (svc_reward_claims) and :362 `ORDER BY distributed_at` -> `distributed_at, id` (svc_revenue_distributions). Tie-break column from the tables' actual key: both `id TEXT PRIMARY KEY` (migrations/002_verification-tiers.sql:693, :703). Plus 1 new vitest source-text file (6 cells, 3 red).
- NOT touched: services/staking/src/routes/stake.ts (:458, `ORDER BY stake_date`, same class) - Seat E 22nd is editing it; hand that site to them.
- Tip: 85cd24d81cb97e30e08fdc054d1ba4b65ea8b558 (ls-remote 2026-10-30 equals).
- Result: PASS 7/7 on the ORIGINAL (no rebrief used); 72 s round, model 34.8 s, 14185+1322 tokens; A4 3 red of 6 (3 control green); A5 6/6; whole staking suite no new red; tsc rc 0; strict apply; A2a 2/2. Golden BYTE-IDENTICAL (model never saw the golden product lines); control PASS beforehand.
- Why no hold_ready READY: loose code_patch2 excluded (A3x unmeasured=1).
- I read both -/+ pairs: each only inserts `, id` after the sort column; placeholders, quotes, WHERE untouched.
- Brief: night/briefs/ks_1544s_staking_rewards_paged_lists_total_order/KS-1544.md  Run dir: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1544s_staking_rewards_paged_lists_total_order
- Raise-seat notes: query plans unmeasured; defect reasoned from SQL; open PRs on rewards.ts not enumerated (the coordinator named only stake.ts as live; op 29 had listed all of staking as live-seat owned - check before raising).

```diff
diff --git a/Blockchain/Dev/services/staking/src/routes/rewards.ts b/Blockchain/Dev/services/staking/src/routes/rewards.ts
--- a/Blockchain/Dev/services/staking/src/routes/rewards.ts
+++ b/Blockchain/Dev/services/staking/src/routes/rewards.ts
@@ -314,5 +314,5 @@
     const claimsResult = await query(
-      'SELECT * FROM svc_reward_claims WHERE address = $1 ORDER BY claimed_at LIMIT $2 OFFSET $3',
+      'SELECT * FROM svc_reward_claims WHERE address = $1 ORDER BY claimed_at, id LIMIT $2 OFFSET $3',
       [address, limitNum, offsetNum]
     );
     const claims = claimsResult.rows.map(rowToRewardClaim);
@@ -361,5 +361,5 @@
     const distResult = await query(
-      'SELECT * FROM svc_revenue_distributions ORDER BY distributed_at LIMIT $1 OFFSET $2',
+      'SELECT * FROM svc_revenue_distributions ORDER BY distributed_at, id LIMIT $1 OFFSET $2',
       [limitNum, offsetNum]
     );
     const distributions = distResult.rows.map(rowToRevenueDistribution);
diff --git a/Blockchain/Dev/services/staking/src/__tests__/ks1544-class-staking-rewards-paged-lists-order-in-a-total-order.test.ts b/Blockchain/Dev/services/staking/src/__tests__/ks1544-class-staking-rewards-paged-lists-order-in-a-total-order.test.ts
... (new test file section: see golden.diff in the brief dir / run dir patch.diff)
```
