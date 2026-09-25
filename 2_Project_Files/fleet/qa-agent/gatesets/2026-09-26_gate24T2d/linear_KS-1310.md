KS-1310 originate: pin /transfer-custody's route-level rollback with a committed integration cell
state In Progress

Residue from the tier-1 review of PR #1239 (merged as `6e2a00bfed57`), filed on the reviewer's instruction.

**What is missing.** `/transfer-custody`'s rollback is pinned **structurally** (one `withTenant` per request, both writes on the client it hands out) and by a direct `withTenant` cell. **No committed cell drives the real route.** `/share` now has one; `/transfer-custody` does not.

**It has been shown to work.** A gate scratch cell drove it: an injected owner-flip failure left **one custody row at develop and none at the PR head**. So the cell is known to discriminate — it simply is not committed.

**What to commit.** The real `documentsRouter` over the real `db`, a seeded document and holder, and a **DB-side flip fault**. Assert **zero custody rows and an unflipped owner**. It must go **red at develop**.

**Evidence:** `reports/2026-09-25-batch1239-t1-r2/evidence/runs/CC-DEVT`, `CC-HEAD`, `quarantine/scratch_cells/`.

Refs KS-1263
