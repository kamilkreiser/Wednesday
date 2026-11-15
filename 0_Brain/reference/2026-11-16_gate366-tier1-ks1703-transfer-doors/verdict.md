PR 2241: GO WITH NOTES (at head 42fd872d49cdb4e1a0fe120d5eaf5d971dcaccac; tier 1)

# Gate 366, tier 1 (Opus, row G1). KS-1703 transfer half: the transfer and delegation read doors refuse a non-party

Gate seat: QA gate agent commissioned by Wednesday (22:3x seat). Findings only. Nothing posted, pushed, merged, mailed or written to Linear or GitHub.
Head pinned by gh api twice: 42fd872d49cd at the first measurement (00:0x AEDT) and again at 2026-11-15T13:12:31Z (PR open, not merged, updated 12:58:05Z).
Base bbb75755064e. develop at measurement: 659d17071685 (3 commits past base: KS-1415, KS-716, KS-2138; 3 files, none under services/transfer, packages/shared, the systemTest module or the fragments).

## Verdict reasoning
The product change is correct, minimal and matches the stamped rulings (W1 a, W2 keep, W3 in scope, D5 spec unchanged). Every claim I re-measured reproduced: suites 483/483 and 595/595, a one-cell name diff, tsc 0, eslint 0 errors (1 pre-existing warning), docs check OK, merge-tree clean both orders with planted controls firing. My 16 HTTP probe cells (11 transfer, 5 delegation), written independently, are all green at the head and red at develop where they should be. The notes are test-coverage gaps and a PR-body omission. None is a defect in the shipped behaviour, so none blocks.

## Findings
- **G366-2241-1 (LOW, test gap, not blocking).** I ran 16 mutants of my own over the whole suite, and the PR's cells kill 13. The other 3 survive. My probe cells kill all three, so the head is right; the PR's suite just would not notice these regressions:
  - **M2.** The list's admin arm reads the raw role (`isPlatformRole(user.role)`) in place of `isPlatformReader(user)`. A key carrying SYSTEM_ADMIN, or a SYSTEM_ADMIN token with no user id, would then list every transfer. Only the unit rows on `isPlatformReader` pin this. No HTTP cell asks the list as a key-admin. (Probes G3, G4 and G5 kill it.)
  - **M5.** Door 4 (`/api/transfers/document/:id`) goes all-or-nothing: one readable row would reveal every transfer of that document. The transfer cells open one transfer per document, so they cannot see it. The delegation side has DD-F; the transfer side has no twin. (Probe G2 kills it: two transfers of one document, where A, X and R each see only their own.)
  - **M11.** `foreignOwnerId` uses `!==` in place of `sameId`. This fails closed: an upper-cased own ownerId would get an empty page. (Probe G8 kills it.)
  - Suggested follow-up: add the G2 and G4 shapes as cells. It is not required for this merge.
- **G366-2241-2 (LOW, PR body).** The brief's "NOT touched, named in the PR" list includes `/api/workflows/*`. The PR body never mentions workflows, so it does not claim them (Q7 holds), but it does not name them either. A sibling unscoped transfer-keyed read exists there: `GET /api/workflows/transfer/:transferId/status` (routes/workflows.ts:147). It returns the approval workflow status to any signed-in caller, and 200 against 404 confirms that a transfer has a workflow. This is for the board seat, not this PR.
- **G366-2241-3 (pre-existing, NOT this PR, needs Kam or the board).** `POST /api/workflows/steps/:stepInstanceId/approve` (routes/workflows.ts, approvalWorkflowService.processApproval:467-496) takes `approverId` from the request body and never binds it to `req.user`. The authorization check is `stepInstance.assignedTo === request.approverId`. So any signed-in caller who knows a stepInstanceId can approve or reject a workflow step in the assignee's name. This is a write-side, body-supplied identity on an approval. I did not check whether a ticket already exists for it.
- Notes (cosmetic):
  - `_OPEN_DEFECT` in the systemTest module is now defined but unused.
  - The module docstring's "Which markers mean what" still calls transfers and delegations confirmed defects. The builder already flagged this as Peter's text.

## Commission questions
1. **Every read door admits only parties and platform administrators. Holds.**
   - My cells and the PR's give the route's own 404 bytes to each of these, by id and history:
     - a same-tenant non-party;
     - an other-tenant user;
     - ORG_ADMIN, ISSUER_ADMIN, ADMIN, OWNER and USER non-parties;
     - a connector or api_key token carrying a party id or SYSTEM_ADMIN/SUPER_ADMIN;
     - a token with no user id.
   - On the delegation door the same set gets the same answer.
   - On both /document doors they get an empty list byte-equal to an unknown document's.
   - Probe G9/GD5: the status, content-type, content-length and body of a refusal equal those of an unknown id, on transfer by-id, history and delegation by-id.
   - The chain is built after the check: cell R2-NC's spy holds, and the builder's m12 matches it.
2. **The list. Holds.**
   - A foreign ownerId gives an empty page, including for a caller with transfers of their own (L-O2), and for an array ownerId (G7, 200 and total 0).
   - total, limit and offset count the filtered set (L-G, G10).
   - An admin keeps today's behaviour (L-P, L-PO; mutant M14 is killed).
3. **Nothing widened. Holds.**
   - transferAccess.ts at head equals develop plus a header comment, one import and appended functions. The `decideTransferAccess` text and the `signedInCaller`..`isNonUserPrincipal` span hash the same at both (9d88d630e798, fa9af468d6ff).
   - The index.ts hunks touch only the import, the list, by-id, history and door 4. No write door and no requireCaller is touched.
   - No role besides the isPlatformRole pair is admitted. The tenant-arm mutant M16 is killed by 8 cells.
4. **The by-design test changes are honest.**
   - statusOf and R5 now read as OWNER. openBody and seedRow name OWNER as currentOwnerId, so OWNER is a party to every row they make. The control R5 still sees +1 and count 1.
   - The new P7 asserts the key's refusal byte-exactly. The reason it is a strong cell (the seeded rows name the key's own id as initiatedBy) is confirmed: my M9 reddens it.
5. **AC6. Holds.** Exactly the 3 markers were replaced (test_transfer_by_id, test_transfer_history, test_delegation_by_id). The 3 _RULING_PENDING xfails remain. The fixtures are consistent with the new rule:
   - The transfer fixture's owner is initiatedBy (a party), and the peer is never named.
   - The delegation fixture's delegate is a throwaway uuid.
6. **"What this REFUSES" is accurate.**
   - I re-ran the caller search at the head with git grep over the full tree: 448 lines. The only frontend GET is issuer TransferList `?ownerId=<own>`, which still works and is case-tolerant via sameId (probe G8).
   - The e2e transfer.api.spec list cells assert only `ok()` and an array.
   - recruitment-data.ts and test-data.ts declare `get(id)`, and no spec calls it.
   - The SDK `getDelegation` has no in-repo caller. External SDK consumers are unmeasured.
7. **stats/overview, the notifications and delegations-list `?userId=` fallbacks, and workflows: not claimed.** The PR names the first three as untouched. It omits workflows (see G366-2241-2).

## Measurements (scratch/)
- **Whole services/transfer vitest** (Node v26.8.1, TMPDIR g366t, DATABASE_URL unset):
  - develop 659d1707 at load1 4.44: 483/483 in 18 files.
  - head at load1 4.44: 595/595 in 21 files.
  - Name diff: 1 gone (control P7), 113 new (112 ks1703 cells plus RED P7).
  - Files: suite_dev.json, suite_head.json.
  - The merge tree 5f857d99 differs from the head only in the 3 unrelated develop files, so the head suite stands for the merge.
- **Probes** (probe_parked/gate366-probe-{transfer,delegation}.test.ts, kept out of the trees):
  - head: 16/16 pass.
  - develop: 11 red by AssertionError, 5 pass. The 5 that pass are controls or cases develop already answered the same way: G1, G7, G10, G11 and GD4. (Transfer probes: 7 red, 4 pass. Delegation probes: 4 red, 1 pass.)
  - Files: probe_head.json, probe_dev.json, probed_*.json.
- **Mutants** (mutants.py, mut/, mutants_run1.txt): 16 mutants, whole suite each, product bytes restored and checked by sha256 every time.
  - Killed (13): M1, M3, M4, M6, M7, M8, M9, M10, M12, M13, M14, M15, M16.
  - Survived (3): M2, M5, M11, all killed once the probes are added (mutants_probes_rerun.txt).
  - LOAD GATE: my first probes run of M2/M5/M11 started at load1 10.03, which breached the >8 rule. I re-ran it at load1 6.61 and got identical results; the rerun is the one cited.
- **tsc:**
  - src: rc 0 at develop and at the head.
  - src plus tests (tsconfig.g366tests.json, rootDir ../..): rc 0 at both.
  - Planted TS2322 in the unit test file and in transferAccess.ts: rc 2, naming both lines. Restored sha-equal.
- **eslint** (API with cwd=Blockchain/Dev, root flat config; eslint_g366.cjs):
  - The head's 7 files: 0 errors, 1 warning. The warning is no-useless-assignment on `let filtered`, at develop:628 and head:630, so it is pre-existing.
  - Planted var plus debugger: 2 errors, rc 1. Restored sha-equal.
  - The CLI with absolute paths and no cwd gives false parse errors: the config's globs are cwd-relative.
- **docs-fragments check:**
  - OK at develop (255 new) and at the head (256 new).
  - A planted unclosed `<div>` in the flow fragment: rc 1, "tags are not balanced". Restored sha-equal.
  - The ADVISORY count is 2 at both, so it is pre-existing.
- **Merge-tree** (mergetree.txt):
  - head x develop 659d1707, both orders: rc 0.
  - head x PR 2170 (52f482a8), both orders: rc 0.
  - Planted same-line controls on develop and on 2170, both orders: rc 1, naming index.ts.
  - 649 and 575 were not re-measured: they are dependabot bumps of package files that this PR does not touch.
- **Platform-admin reachability.** platform_admins.id is UUID in both schemas, so a platform admin's token passes GUID_SHAPE and the admin arm is live. This assumes the token's userId is that id, which I did not trace through the mint.

## HOW
- **Clone:** scratch/clone, made by `git init` with alternates to the Blockchain object store and gate 364's clone (read only). Fetched with the gh credential helper. Push URL DISABLED.
- **Worktrees:** sparse wt-dev and wt-head. Local-only control commits d51fded4 and d30155a9 exist in my clone, with no refs.
- **node_modules:** APFS-cloned from gate 364's wt-dev. package-lock.json and the transfer and shared package.json files are sha-equal to it. There are no absolute symlinks. packages/shared was built per tree (rc 0).
- **Writes:** none outside this folder and g366t. No cd, no rm, and nothing written in any !CODING checkout.

## NOT COVERED
- A stack, the gateway path, Postgres (the list's SQL branch with isDbAvailable true is unexercised by any cell, as before).
- The systemTest module run, Schemathesis, Akto, Playwright and k6, and a second tenant end to end.
- External SDK consumers and Node 24.
- The pre-push hook and ruff.
- The token mint's userId for platform admins.
- The builder's own 16 mutants were not re-run verbatim; my 16 measure the same classes independently, plus M2, M3, M5, M11, M14 and M16 as new classes.
- Linear state of KS-1703 was not read.
