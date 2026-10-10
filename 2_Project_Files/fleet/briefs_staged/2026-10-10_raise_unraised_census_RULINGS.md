# Wednesday's rulings on 2026-10-10_raise_unraised_census_PROPOSAL.md (18:56 AEDT)

Census control spot-checked by Wednesday at source: 1fba82ddb ("KS-1449: mark six nft request bodies required…") IS an ancestor of develop 785cb671557a (merge-base --is-ancestor rc 0, drafter's scratch clone).

- Q1 collision: raise branches are cut from develop AFTER #1448 lands (R 36th in flight; it moves the yaml and both docs). The yaml and doc collisions with #1450 are the routine keep-both merge-in at merge time; not a reason to wait for #1450.
- Q2: KS-1426 is #1450's; not raised again either way.
- Q3 tiers: A2 billing = TIER 1 (money surface); A3 tenant-provisioning = TIER 1; B1 document-share = TIER 1. A1, B2, C2 tier 2; C1 tier 1.
- Q4: C3, C4 and platform-tenant-id-uuid need a source review before raising; they are OUT of the first raise seat. A3 is out with them (it carries the unreviewed uuid pass).
- Q5: KS-723 anchors-get EXCLUDED (REVIEW = REJECT).
- Q6: yes, landed READY files get marked; OWED, a Wednesday-tree edit at a quiet boundary, never a delete.
- Q7: yes. The raise seat re-runs each pass's red-first then green at its base before opening each PR, and records both.

FIRST RAISE SEAT (lane F, Seat F 12th, Sonnet per today's grant): A1, B2, C1, C2 (4 PRs), then A2 and B1 only if ctx allows (tier 1, named). Gate batching per the 09-18 rule: tier-2 PRs in one gate, tier-1 in another.
