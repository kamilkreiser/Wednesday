GO WITH NOTES

# Gate 208: Secuura / Blockchain, PR 2017 (KS-692), tier 1, round 1

Covers SHA 536bca3aa4754b46639ffc4df2e55ed368633dd8 only (PR head, read in clone `repo/` at start and end: 536bca3aa475, branch feature/ks-692-security-apistatus-revokeunrevoke-has-no-tenant-ownership). Base = 5fc5569ed96a (worktree `base/`). Dependencies: symlinks to gate 204's install. Its lockfiles and packages/shared are byte-identical to this PR's (shared tree d94503e3 at base, head and the gate 204 commit). Node v26 (not LTS).

**BLUF:** The change does what the rulings require. On the real router over real HTTP, with only storage doubled, the head admits only the creator on her own credential, plus the KS-1906 own-tenant platform administrator on an owner-less credential that has a tenant. That second admit is unchanged from base, and Q-B (i) requires it. Every other signed-in refusal is the byte-identical 404, with no write and no state change. Anonymous callers still get 401. The gate exemption admits exactly a signed-in POST /<id>/revoke or /<id>/unrevoke. All six mutants were killed, both by my table and by the seat's own test file. Suites, tsc, eslint and docs pass, and the planted defects fail. The merge onto develop 1b1b65c7415f is clean with 0 shared paths. One note corrects the seat's systemTest prediction: that test reads 400, not 404.

## Answers
1. **Scope: confirmed.** c9cb07738cf6..head has exactly the 8 seat-listed paths (+649/-24). The status.ts diff contains only the ownership import, the `CREATOR_BOUND_WRITE` exemption in the gate, `refuseUnlessCallerMayChange`, and one call to it each in revoke and unrevoke, plus comments. The merge commit brought exactly develop's 12 paths from 5fc5569..c9cb (identical name list, content identical to c9cb, 0 shared with the change). Evidence: evidence/q1_scope.txt, evidence/status_diff.txt.
2. **Authorization table: 88 cells** (11 callers x 4 credential states x 2 operations). Callers: anonymous; the creator; same-tenant OWNER, ISSUER_ADMIN and ORG_ADMIN; other-tenant OWNER and ISSUER_ADMIN; SYSTEM_ADMIN of the own tenant and of another tenant; SUPER_ADMIN and legacy super_admin of the own tenant. My own harness: express plus the real statusRoutes and errorHandler, real HTTP on 127.0.0.1, the db module mocked unavailable so credentialRepo uses its memory store and owner map.
   - The head admits 8 of 88: the creator x 2, and platform own-tenant on owner-less-with-tenant x 6.
   - Gains over base: 2 of 88, exactly the creator's revoke and unrevoke.
   - Narrowed: 26 of 88, all platform roles. The seat's 14 SYSTEM_ADMIN cells are an exact subset; the other 12 are the SUPER_ADMIN and legacy super_admin cells under the same rule. That is what Q-B (i) requires, since KS-1851 has no platform bypass.
   - Anonymous: 8 of 8 get 401 on both base and head.
   - Signed-in refusals: 72 of 72 are a 404 whose body and headers (etag included) are byte-identical to a not-in-list control in the same list. 0 writes, 0 state changes. Base refused these with 403.
   - Evidence: evidence/decision_table.txt, evidence/authz_repo.jsonl, evidence/authz_base.jsonl, gate208-authz.test.ts.
3. **Gate exemption: 25 path tricks x {creator, other-tenant OWNER, anonymous}.** The exemption reaches a handler only for /<id>/revoke or /<id>/unrevoke:
   - Plain, trailing slash, any letter case, `//LIST/revoke`, `/./` and the x-http-method-override header all still go through the creator check.
   - An encoded slash in the id gives 404 "Status list not found" with no write.
   - These all stay on the role gate (403 for the signed-in callers, 401 anonymous): query smuggling (`allocate?x=/a/revoke`), `%2Frevoke`, `LIST//revoke`, a trailing extra segment, two segments, root /revoke, `../allocate`, `revokeX`, `%72evoke`, `;x`, allocate, create, and PUT/DELETE/PATCH.
   - My widen mutant G2 (`/^\/[^/]+\/[^/]+\/?$/`) was killed: a signed-in OWNER got 200 on allocate. The seat's M10 was also killed (create gave 201).
4. **Ordering and side effects: confirmed.** In the code, the owner check sits after shape and list and before the entry check (status.ts:324, :376). The KS-1371 lines are unchanged. Spies on StatusListManager.prototype.revoke and unrevoke record 0 calls on every refusal, and the revoked-index list is unchanged. Not-owned and not-stored refusals are byte-identical to not-in-list. The latency difference between refusal and control is at most 2 ms. Both paths do the same getRecordById lookup first, so timing is equal by construction.
5. **Mutants: 6 of 6 killed**, each with an anchor count of 1 and the file restored sha256-equal (55556469…).
   - Seat mutants, with seat-file kill counts: M1 42, M6 55 and M8 12, all equal to the seat's figures. M10 read 8, where the seat reported 12; the seat used a different mutant form.
   - My own: G1 (mayRead instead of mayReadCredential, i.e. not KS-1906) killed 3, and G2 killed 5.
   - Evidence: evidence/mutants.txt, evidence/mut_*.
6. **Suites:**
   - vitest on the merged head 536bca: 28 files, 842 of 842, rc 0. Base: 27 files, 766 of 766, rc 0. The ks1868 C1 timeout did not occur here.
   - tsc: service config rc 0, test config rc 0. check:test-types reports 42 files, 28 under tests, 0 errors. A planted TS2322 gave rc 1.
   - eslint (API with cwd Blockchain/Dev): 6 files, 0/0. A planted `debugger` gave rc 1.
   - docs-fragments: OK. A planted unbalanced div plus a second h2 gave rc 1 with 2 findings, and the file was restored. The 2 ADVISORY lines also appear on base.
   - Evidence: evidence/suite_*.log, evidence/tsc_head.txt, evidence/lint_docs_tsc_planted.txt, evidence/eslint.txt.
   - On test_status_list_authz.py:136: yes, it will fail after merge. The PR names it in its own fragments. The PR body was not read (no network). The code it will read is wrong in the seat's claim; see N1.
7. **Merge onto develop 1b1b65c7415f:** merge-tree rc 0, tree a69a94b6. The merged tree differs from develop in exactly the 8 PR paths. Develop since c9cb: 34 paths, 0 shared with the PR. A planted control (status.ts added to the list) reads 1. Evidence: evidence/q6_q7.txt.

## Findings
- **N1 (Low): the seat's systemTest prediction is wrong.** The seat and the PR's fragments say systemTest `test_tenant_admin_cannot_write_status_lists` (systemTest/schemathesis/tests/test_status_list_authz.py:136) will read **404**. It will read **400** "credentialId is required and must be a string" on its revoke and unrevoke rows. The reason is that `sla.STATUS_WRITES` (tests/support/status_list_authz.py:50-51) sends bodies with no credentialId. At head, a signed-in ISSUER_ADMIN passes the gate and the shape check refuses it first; base gave 403. The test stays red either way, because `is_role_refusal` accepts only 403. The text to correct is in fragments/flow/KS-692-…html:27 and fragments/cheat/KS-692-…html:5, and in KS-1429's successor test. Evidence class: MEASURED AT RUNTIME at the vc-issuer router, not through the gateway. Evidence: evidence/q6_repo.jsonl, evidence/q6_base.jsonl.
- **N2 (Info): the commission's Q2 wording does not match the rule it cites.** Q2 says "nobody on owner-less". Under KS-1851 exactly (Q-B (i), KS-1906), the head admits a platform administrator (SYSTEM_ADMIN, SUPER_ADMIN or super_admin) of the credential's own tenant on an owner-less credential that has a tenant: 6 cells. Base admitted the same 6, so this is neither a gain nor a defect. It matches credentials.ts:309-310 and ownership.ts:150-155. READ plus MEASURED. Evidence: evidence/decision_table.txt.
- **N3 (Info): the seat's narrowed count leaves out two platform roles.** The seat's direction table counts 14 narrowed cells (SYSTEM_ADMIN only). The full count is 26, adding SUPER_ADMIN and legacy super_admin under the same rule. No direction discrepancy. Evidence: evidence/decision_table.txt.
- **N4 (Info): develop 1b1b65c7415f is not merged into the PR, and the suites were not run on that merged tree.** The merge is clean and file-disjoint (answer 7). A GO is about SHA 536bca only.

## Not covered
- A real PostgreSQL: the getRecordById database path and its fallback-on-throw.
- The gateway and jwtAuthenticate. The router was driven with a stand-in principal header.
- Node 24, the four platform suites, any box or deploy, a second replica.
- The PR body on GitHub (no network).

My test copies are moved into `_quarantine_2026-11-05/`. Nothing was deleted, and the clone tree is clean against HEAD apart from the node_modules/dist symlinks. No process is left running. Nothing was posted.
