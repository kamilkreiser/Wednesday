--- comment 5836170365 by linear[bot] at 2026-09-25T16:54:41Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1311/originate-run-the-rollback-integration-cells-as-the-app-role-inside">KS-1311 originate: run the rollback integration cells as the app role, inside the tenant scope</a></summary>
<p>

Residue from the tier-1 review of PR #1239 (merged as `6e2a00bfed57`), filed on the reviewer's instruction.

**What it is.** The integration file **seeds, writes and counts as a superuser**, so row-level security is never in the loop — the cells prove the transaction, not the tenant scope. Its route harness also omits the tenant-scope middleware, and as the app role the develop side **cannot write at all**.

**Measured.** Adding that middleware and running as the app role **reproduces red at develop and green at head**, so the rollback claim survives the stricter setup — but the committed cells do not exercise it.

**Two smaller things in the same file.** The NUL-byte fault is refused in production **before** the route, so the header should name it as a test vehicle rather than a production shape. The platform guard should assert the tenant configs actually loaded.

**Evidence:** `evidence/runs/LEADA-*`, `LEADA2-*`, `LEADC-EMPTYPLAT`, `evidence/52`.

Refs KS-1263
</p>
</details>
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1310/originate-pin-transfer-custodys-route-level-rollback-with-a-committed">KS-1310 originate: pin /transfer-custody's route-level rollback with a committed integration cell</a></summary>
<p>

Residue from the tier-1 review of PR #1239 (merged as `6e2a00bfed57`), filed on the reviewer's instruction.

**What is missing.** `/transfer-custody`'s rollback is pinned **structurally** (one `withTenant` per request, both writes on the client it hands out) and by a direct `withTenant` cell. **No committed cell drives the real route.** `/share` now has one; `/transfer-custody` does not.

**It has been shown to work.** A gate scratch cell drove it: an injected owner-flip failure left **one custody row at develop and none at the PR head**. So the cell is known to discriminate — it simply is not committed.

**What to commit.** The real `documentsRouter` over the real `db`, a seeded document and holder, and a **DB-side flip fault**. Assert **zero custody rows and an unflipped owner**. It must go **red at develop**.

**Evidence:** `reports/2026-09-25-batch1239-t1-r2/evidence/runs/CC-DEVT`, `CC-HEAD`, `quarantine/scratch_cells/`.

Refs KS-1263
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1310-pin-transfer-custodys-route-level-rollback-ks-1311-app-role-df77cdeca669">Review in Linear</a></p>

