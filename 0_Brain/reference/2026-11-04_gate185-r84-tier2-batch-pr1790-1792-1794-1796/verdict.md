GO WITH NOTES — PR 1790 / KS-1340 (MERGE, no HOLD-FOR-KAM)
GO WITH NOTES — PR 1792 / KS-1499 (MERGE, no HOLD-FOR-KAM; DB suite NOT RUN by this gate)
GO WITH NOTES — PR 1794 / KS-1600 (MERGE, no HOLD-FOR-KAM; DB suite NOT RUN by this gate)
GO WITH NOTES — PR 1796 / KS-1458 (MERGE, no HOLD-FOR-KAM; suites NOT RUN by this gate)
Merge trees onto develop c7abf98e5103 (each rc 0): 1790 25d601363ec1ff21b2dc985baa5b13c9155b25de · 1792 3b2c352a5efd2b34be461d68379137749e0cf590 · 1794 dfe01075c37e98340d78374f44e036e887bfbcad · 1796 c316ecfd5296c40c1f61f39b0b25dde61ea3adcb
Sequential 1790 -> 1792 -> 1794 -> 1796 (each rc 0): after 1790 25d601363ec1ff21b2dc985baa5b13c9155b25de · after 1792 856c2d00a5584d35effd3dce820a66c8f1d9329a · after 1794 e46256ce9327a94cea8f1bdf06db402aaf0161e5 · after 1796 21a13d4e0dd94512b5ee6bef15e7d5bf85d596a3

# QA Gate 185 (Tier 2, round 1): PRs 1790 (KS-1340), 1792 (KS-1499), 1794 (KS-1600), 1796 (KS-1458)

## Subject
Start and end pin (identical, pin_start.txt / pin_end.txt, via ls-remote): develop c7abf98e51030f908050fede10a3546871d4f2c1; 1790 aa1f6b7739918ed76194970ed810e57f831099d0; 1792 f364327e266ce321bfeb6e3a52b045904d8d8527; 1794 06fe8557ec43be6879a854c345b3829b9417b2e0; 1796 759fd6fb19aaa22df4bd86dd61dcb6d4a9832fa8. Heads matched the commission. Host: Node v26.8.1, pg 8.20.0 / pg-connection-string 2.12.0 (read from the client checkout's node_modules by absolute path, read-only). Method: `clone --shared` into workdir/repo; heads were already present as objects in the checkout (GitHub PR refs could not be fetched through the local origin), pinned by SHA. Diffs read whole; merge-trees; docs-fragments check on each head; for 1790 the real KS-1340 predicate and the real REFUSED/ACCEPTED tables were cut out of the head blob and run under node with mutants. No PostgreSQL on this host and Docker was not touched, so no DB-gated suite ran. No node_modules in the clone, so no auth/vitest or tsc run.

## Findings
### G185-F1 — LOW (note): the DB-gated cells of 1790 (WIRING, no-TCP), 1792 (all) and 1794 (c19, c20) were not driven here
**FOUND** The R 84th counts (ks597 24/24; ks1263 12/12 both modes; ks1594 26/26 both modes; PostgreSQL 15.19) are stated here as ITS, not measured by this gate.
**TESTED** Static read of every changed line; for 1790 the pure predicate cells only (see passed).
**HOW** No Postgres without Docker. Mutants for 1792/1794 need the DB, so the "each cell fails on a deliberate break" question is UNANSWERED for 1792 (F1 RLS cell, F2 hook guards) and 1794 (c19, c20); read-only evidence: adminConfig.ts at develop lines 1004-1013 puts the typeof guard before the org decisions and treats null like absent through normaliseOrgId, which is what c19/c20 assert; in 1792 the hook calls assertProductIsTheAppRole(withTenant, tenantId) with both in scope (withTenant is assigned earlier in the same beforeAll, line 197), and the two route describes pass db.withTenant and their tenant constants, matching the signature.

### G185-F2 — INFO: commit subjects over 92 chars
**FOUND** Branch-tip subjects: 1792 "Refs KS-1499: the KS 1263 rollback suite ..." is 150 chars, 1794 127, 1796 101 (1790: 90, merge commits 56). All start "Refs KS-<ticket>: ". No "close/fix/resolve KS-" before a key in any message body (grep rc 1 on all four, control: the merge-commit bodies were printed and read).
**TESTED** Commit messages only. PR TITLES and BODIES UNMEASURED (no gh login); if the PRs are squash-merged with the commit subject as title, 1792/1794/1796 exceed 92.

### G185-F3 — INFO: docs advisory "committed page has content after its last rendered entry"
**FOUND** Printed on all four heads; none of the four PRs touches the two shared pages (name-only lists below), so it is the develop state (not compared byte-for-byte against develop beyond the file lists), exit 0 by design.

## What passed (measured)
Q1 scope (git diff --name-only develop...head): 1790 = ks597 test + 2 fragments; 1792 = ks1263 test + 2 fragments; 1794 = ks1594 test + 2 fragments; 1796 = baseline-auth.txt + ks1006 test + users.ts + 2 fragments. Matches R 84th's lists. users.ts (1796): the diff is one hunk, 2 lines removed and 3 added, ALL starting `//` after whitespace: comment-only (read in full). Control: the same diff command printed the non-comment context lines (`if (!user.mfaSecret ...`) as unchanged context, so non-comment lines would show.
Q2 mutants (1790, predicate cut from the head blob, workdir/harness): head 16/16 (11 REFUSED + 5 ACCEPTED). Mutant M1 (host/port from `new URL(dsn)`, i.e. the base behaviour): 8 FAIL / 8 pass of 16 (raw table counted). Mutant M2 (hostaddr check disabled): 1 FAIL / 15 pass of 16 (the hostaddr cell). Both caught; 0 survivors. Restored: the mutants are separate files, the head text is untouched. 1796 changes are a header comment, an import form and a baseline row (no behaviour): the baseline row removed (TS1192 on the default import) agrees with the import change `import * as userRepo`; userRepo.ts at the head has no default export (grep for `export default` returned nothing, control: grep matched decryptMfaSecret lines in the same file), and the test's mock supplies both default and named. The header's claim (decryptMfaSecret returns undefined for null/empty and from its catch) matches userRepo.ts lines 173-188.
Q3 suites: NOT RUN (see F1). R 84th's counts above are its own.
Q4 docs: docs-fragments check on each head rc 0 with "lint clean, render passes html_docs_check"; planted literal-number control (appended to the PR's own flow fragment) rc 1 on each of 4 heads, restored (git status clean). No edit to the two shared pages in any PR.
Q5 pairwise/merge: no file shared among the four (file lists above); each head onto develop c7abf98e5103 rc 0 with the trees in line 5; sequential application rc 0 four times with the trees in line 6 (built with merge-tree then commit-tree, in the workdir clone).
Q6 titles: see F2.

## NOT tested
Every DB-gated cell on a database (1790 WIRING and no-TCP cells, all of 1792, 1794 c19/c20); mutants for 1792 and 1794; jest/vitest/tsc/lint on any PR; ks1006 5/5 and ks1000 99/99; the test-inclusive ratchet count (41); the accuracy of the new users.ts comment about /api/auth/mfa/disable for passwordless accounts (not read in the route); PR titles and bodies; anything on a shared stack; the first-parent order that decides fragment numbers.

## Plain answer for Kam
All four are test-only, comment-only or documentation-only; users.ts changes in the 1796 PR are three comment lines and no code. The four can be merged together in the order 1790, 1792, 1794, 1796 with no conflicts. For 1790 I proved on the real code that the new database-safety guard refuses the sneaky connection strings it claims to, and that breaking it makes the new checks fail. For 1792 and 1794 I could only read the tests and rely on the builder's run results, because I had no database without touching Docker. Nothing here changes what users see.
