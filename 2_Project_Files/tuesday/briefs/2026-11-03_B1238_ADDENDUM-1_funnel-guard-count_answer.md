# B1238 ADDENDUM-1 (answer to STOPPED: NEEDS TUESDAY, the funnel guard count) — from Tuesday s238

**Answer: (A).** Change the guard's exact count from 8 to 9 in `__tests__/rd436-r3-admin-gate-funnel.test.js`, in the SAME single commit as the RD-902 change.

**Why (read at source by Tuesday in your worktree, `rd436-r3-admin-gate-funnel.test.js:104-110`):** the guard's own text says the count is written down "so a ninth route cannot be added without this cell being read", and its message says "If a route was added or removed, that is a deliberate change and this number is updated with it". The twin `riskConditionAdminPasses(req)` IS a new gate site, added on purpose by RD-902 and reviewed by a tier-1 gate after you. Updating the number is the guard working as designed. Option (B), calling `requireAdminFor` with a silent stub `res`, would hide a gate site from the guard that exists to count them: NOT taken.

**Exactly what changes (closed list, property first: the guard keeps all three of its checks and only its count and the words that state it move):**
1. `:107` `if (gateCalls.length !== 8)` becomes `!== 9`; the message text at `:108` that says "the 8 this guard was written against" becomes 9; the comment at `:104-106` and the test title at `:99` ("all eight adminGateRefuses call sites") say nine, and the comment names RD-902's read-path check as the ninth site (developer text, no ticket text beyond the key `RD-902`).
2. Nothing else in that file. The per-call-site spread check (`...adminGateEntraInputs(`) and the funnel-count equality must still pass UNCHANGED: your twin spreads `adminGateEntraInputs(...)` inside `adminGateRefuses({...})` exactly as the kit's design step 1 says. If it does not pass them, STOP.
3. Before the edit, run the guard at your Step-4 head and print its red message (the 9 vs 8); after the edit, green. Also plant: remove the spread from your twin in the clone only and show the guard's second check goes red (then restore by sha256). This is a red-proof that the edited guard still bites on the defect it exists for.

**What this widens, said plainly:** the kit's partition grows from three paths to FOUR (`backend/server.js`, the new rd902 test, `scripts/verify-expected-counts.json`, and `__tests__/rd436-r3-admin-gate-funnel.test.js`). The counts pair does not change for this (no `test(` added or removed in rd436; assert it). The 25-added-line bound applies to `backend/server.js` only. Step 7's "exactly the THREE PARTITION paths" reads FOUR. Record this addendum under Corrections and in the READY line ("guard count 8 -> 9 per ADDENDUM-1"). Everything else in the kit stands; resume at Step 6 (the verify with `--update-counts`, then the plain verify).

READ BY THE SEAT: say so on your next STATUS line.
