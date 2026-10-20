## BLUF
Gate BN1 returned NO GO on #1654 (head db9bca740df0; tier 1, round 1 of 2; 1 blocker, 5 notes). The CODE fix is sound and stays as is; the blocker is migration 055. Round 2 (of 2, the cap: a second NO GO ships nothing and goes to Kam) fixes 055 and commits its proof. Same PR.

## Provenance
Verdict /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-20_gate-BN1-pr1654-ks1557/verdict.md; `sed '1d;$d' | shasum -a 256` = f8b531a439db... (= its trailer); whole-file control 9a39fb577179 differs; refs/pull/1654/head db9bca740df0 (Wednesday ls-remote). Read it whole.

## Round 2
1. **B1 (blocker): 055 can credit a minted document to the WRONG connector.** It reads only the parent's `version:*` rows; a /version sent without onBehalfOf writes no row and /sign-cert and /sign-wallet write no provenance, so a parent with several children and one row credits every child to that one connector (gate on real PG 15: K8b minted by C2, K9b minted by a human via /sign-wallet, both credited to C1). **Fix: attribute each child from ITS OWN record.** The gate measured that each child's `metadata.versionedById` names its real minter. Insert a row only when the child's own minter is known AND is a connector principal AND (where a parent `version:*` row exists) it agrees with it; skip and report every other child (the skip report must cover children with NO parent row, which the current inner join hides). Fail closed: an unattributable child stays as it is.
2. **N4:** never write `create:connector` for a human principal (role check against the same source the predicate uses); a cell proves it.
3. **N2:** a run under a role without RLS bypass must not silently finish "inserted 0, skipped 0" and be marked applied: set the bypass the way migration 044 does, or refuse loudly; prove it with a run under a non-bypass role.
4. **N3:** COMMIT the migration proof cell (forward, idempotent, reverse removing exactly 055's rows, the wrong-connector case of B1 now skipped, a human-minted child skipped, a multi-child parent) in the PR, on real PG (PGlite only if it reproduces the RLS behaviour; say which).
5. **N5 (sign-cert / sign-wallet minted docs get no create:connector):** NOT in this PR: one ticket, related KS-1557, facts only.
6. **N1 (KS-1688 interaction, measured):** org B versioning A's document now gains certify / GET / legacy-certify on the minted child (not on A's original). Policy is not yours to judge here; put the measurement as a comment on KS-1688 (it is the reason KS-1688's fix must follow this one) and one line in #1654's Known residue.
7. Re-run the whole originate suite; re-take the landing on live develop (6229a92f2480 at the gate's end; gate measured 932c1e56fc41). READY FOR DELTA GATE with the five artefacts.
