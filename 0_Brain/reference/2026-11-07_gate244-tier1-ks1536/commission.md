# Gate 244, tier 1, round 1 of 2: KS-1536, PRs 2060 then 2061

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first. Clone: /private/tmp/g244. Tier reason: who holds admin rights across the platform.

- PR 2060, KS-1536 PR 3a, head 796ea55fb8eb [H/2026-11-06_seatY-6th/pr/ks1536/ready.txt]
- PR 2061, KS-1536 PR 3b, head edcb42e7ae99 [H/2026-11-06_seatY-6th/pr/ks1536b/ready.txt]. By Wednesday's ruling 3a merges before 3b; 3b then takes develop in at the inventory doc, which moves its head: say whether that re-merge needs a re-gate or only a compare.
Card: secuura-ks-1536-platform-admin-role-one-list-1106 = a. Also: V 26th's KS-736 push holds an overlap grant against PR 2060's branch on one test file; note any interaction.

Specific asks:
1. 3b names a loss: a token carrying bare admin stops seeing every tenant and stops editing any tenant. Is that inside Kam's card, or a wider call by Wednesday's ANSWER 06:11:09Z that he should see? Say which at the top.
2. The counts behind the stop are D 57th's report for Kintsugi, read only: 3 platform_admins rows, 25 users, no bare admin. Demo is not counted. Tokens already issued are not tested. What would break for each?
3. Is anything left that still accepts platform_admin after 3a, or a list the seat left out? Enumerate every role list from the code.
