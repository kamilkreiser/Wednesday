# Spark shadow verdict PR #1712 (findings only, no scoring)
Verdict: **GO WITH NOTES**
HEAD {'files': 1, 'files_ok': 1, 'files_failed': 0, 'passed': 113, 'failed': 0, 'count_unparsed_files': []}  BASE {'files': 1, 'files_ok': 0, 'files_failed': 1, 'passed': 99, 'failed': 14, 'count_unparsed_files': []}
tokens: 20726 prompt / 604 completion, 35.7s, 1 attempt

1. [Note] The new test Q3 asserts the SQL text only, not the actual behavior against a real database, so it does not prove the fix works in production.
   evidence: Blockchain/Dev/services/vc-issuer/src/__tests__/ks1683-credential-list-and-by-hash-bound-to-the-creator.test.ts:530-531 `It asserts the SQL TEXT only. No database runs in this file, so it does not prove that real pages stop repeating — the gate's PGlite walk is that evidence, and it is not reproduced here.`
   The test only checks the regex match on the SQL string; the PGlite evidence is not part of the test suite.
2. [Note] The fix does not address NULLS LAST for NULL created_at values; PostgreSQL sorts NULLs first under DESC, so rows with NULL created_at may still be ordered before non-NULL rows, potentially causing page instability if NULLs exist.
   evidence: Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts:365 `ORDER BY created_at DESC, id DESC LIMIT $${idx++} OFFSET $${idx++}`
   The ticket itself notes 'Whether NULLs should sort last (`NULLS LAST`; PostgreSQL puts NULLs first under `DESC`) is a choice for whoever fixes it.' The PR does not add NULLS LAST, so the fix is incomplete for NULL timestamps.
3. [Note] The test Q3 does not verify that the id tie-breaker is actually applied to the data returned; it only checks the SQL text, so a regression in the model's sorting logic would not be caught.
   evidence: Blockchain/Dev/services/vc-issuer/src/__tests__/ks1683-credential-list-and-by-hash-bound-to-the-creator.test.ts:533-537 `it('Q3 the list page SELECT orders on a total order: created_at DESC, id DESC (KS-1731)', async () => { await list(mods, ALICE); const page = statements().find(([s]) => /OFFSET/.test(s)); expect(page).toBeTruthy(); expect(page![0]).toMatch(/ORDER BY created_at DESC, id DESC LIMIT \$\d+ OFFSET \$\d+$/); });`
   The test only checks the SQL string, not the actual ordering of returned rows.
