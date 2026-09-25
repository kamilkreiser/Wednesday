KS-1311 originate: run the rollback integration cells as the app role, inside the tenant scope
state In Progress

Residue from the tier-1 review of PR #1239 (merged as `6e2a00bfed57`), filed on the reviewer's instruction.

**What it is.** The integration file **seeds, writes and counts as a superuser**, so row-level security is never in the loop — the cells prove the transaction, not the tenant scope. Its route harness also omits the tenant-scope middleware, and as the app role the develop side **cannot write at all**.

**Measured.** Adding that middleware and running as the app role **reproduces red at develop and green at head**, so the rollback claim survives the stricter setup — but the committed cells do not exercise it.

**Two smaller things in the same file.** The NUL-byte fault is refused in production **before** the route, so the header should name it as a test vehicle rather than a production shape. The platform guard should assert the tenant configs actually loaded.

**Evidence:** `evidence/runs/LEADA-*`, `LEADA2-*`, `LEADC-EMPTYPLAT`, `evidence/52`.

Refs KS-1263
