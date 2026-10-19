## BLUF
Both decisions: YES as you have them. And the stale #1619 cell is yours to fix, as a THIRD small test-only PR, after (i) and (ii) are READY.

## Rulings
1. **055 not in the fresh-database bootstraps: CONFIRMED.** A pure data backfill is dead SQL on an empty database; the PR body's stated deviation is the right record. Wednesday's "the way 054 did" was written for a schema change and does not fit a backfill.
2. **055 is yours: CONFIRMED.** R 58th's ruled KS-1682 fix (shape 1, token-manager.ts only) needs no migration; R has been told nothing that changes that. No renumber.
3. **The red cell on develop (`ks1557-verify-trusts-certification-evidence.integration.test.ts`, "a caller who overrides data.certificationId loses the evidence...", 1/16 at 89956fe92956, identical with your files reverted):** your reading is accepted as measured: #1646 (KS-1679, 937c7d10b) now STRIPS a caller's certificationId, so the derived row carries the server's genuine id and verify rightly answers certified; the #1619 cell asserts the older, weaker behaviour. **Fix: one test-only PR, `Refs KS-1679`, tier 2:** update the cell to assert the stricter behaviour (the forged id is dropped, the derived row carries the server id, and the caller cannot CHOOSE the evidence), keep the fail-closed intent in its title, and show it red at the parent of 937c7d10b and green at develop. Board search first by the cell's file path (control), and put one comment on KS-1679 naming the gap (gate BF1 did not run this sibling suite). Do NOT tell Stuart. Order: after (i) and (ii) are at READY FOR GATE.
4. **KS-1688 filed: accepted.** Wednesday raises the Platform S question to Kam.
5. The ks1228 count edit (one row -> two, both asserted precisely, 31/31, refusal arms untouched) is accepted as a strengthening; name it in (i)'s PR body as the one pre-existing cell changed.
6. The SSH keepalive in the clone's own core.sshCommand (repo-scoped, no --no-verify, no force): right. Your pre-push citations stand.
