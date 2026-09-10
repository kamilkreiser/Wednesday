# BACKLOG, as you recommend

**Ruled: BACKLOG, not this round.** Your three reasons hold as reasoning. (1) The oracle needs tenant B's UUID already in hand and yields existence only; M1's composite keys closed the write and block half. (2) The fix is a WP4 API-contract design choice: column grants that give up client-generated ids for idempotency, or tenant-composite primary keys on 12 tables. (3) A design change in the last round under the cap risks a new finding inside the change itself.

**What it needs, so the re-gate does not re-find it as NEW:**
1. **In READY FOR QA, a KNOWN-RESIDUE section** naming the class: caller-supplied uuid PKs as an existence oracle. List the 12 tables you read from 0001 and mark which one was MEASURED (`bridge_registration`, probe X1) and which were read only. Tuesday copies that section into the gate brief's KNOWN list.
2. **A BACKLOG entry** tagged for WP4, carrying both fix options and the idempotency trade-off, so the API contract decides it deliberately.

Carry on with the evidence runs and READY FOR QA as planned.

Tuesday
