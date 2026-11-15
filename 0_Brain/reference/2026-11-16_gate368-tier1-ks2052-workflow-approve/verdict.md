PR 2243: GO WITH NOTES (at head 40c99308b84b7aa86185e31cb6e5c2474ee59682; tier 1)

# QA GATE 368, tier 1 (G1, an authorization door), PR 2243, KS-2052: the workflow approve route takes the approver from the token. Findings only.

Pins (gh api, GH_CONFIG_DIR = Blockchain's): head 40c99308b84b7aa86185e31cb6e5c2474ee59682 read at 02:09 and again at 02:24 AEDT, unchanged, open, unmerged, 5 files +579 -2. develop 6fdba4e013b384c7d1f60d36327491ff61e6476c at both reads. PR 2170 head 52f482a83436, open. The head's parent is 0fa14b4cbd33. develop 0fa14b4..6fdba4e touches one api-gateway test file only.
My own copy: `scratch/mirror.git` is a `--mirror --no-local` clone of the builder's worktree `worktrees/s-c39-ks2052`. The remote is disabled, and develop 6fdba4e plus PR 2170's head were fetched from gate 367's mirror. The objects are content-addressed, so the SHAs prove the content. Worktrees: `scratch/wt-head` (the head) and `scratch/wt-dev` (develop 6fdba4e). Each has its own `npm ci` (rc 0, 33 node_modules trees) and its own `@secuura/shared` build. Short TMPDIR /private/tmp/g368t. load1 was read before every vitest, tsc and eslint leg. When it was above 8 I waited, and many legs did wait, logged in `scratch/mutants*.out`.

## Answers to the commission's questions

1. **The actor is the token's, always. YES.** Route diff, read whole: `signedInCaller(req.user)` gives the 401. `isNonUserPrincipal(req.user)` gives the 403. Then the zod parse runs (z.object strips unknown keys), then the mismatch check `data.approverId !== undefined && !sameId(data.approverId, caller.userId)` gives the 403. Then `processApproval(stepId, { ...data, approverId: caller.userId })`.
   - Measured with my own cells against the REAL route and service on a stateful db stand-in (`scratch/cells/g368-cells.test.ts`, 16 of 16 green at the head):
     - An upper-case copy of ANOTHER user's id, a mixed-case copy of a third user's id, and a fullwidth-digit look-alike of the assignee's id are all refused. The row stays pending, with 0 writes and 0 delegation calls.
     - Smuggled `userId`, `actualApproverId` and `assignedTo` never become the actor: the service's 400 "not authorised", 0 writes.
   - The PR's own cells cover the rest: the assignee as themself (equal id, omitted id, an ASCII-case copy of their own id) approves AND rejects (A1-A4, my G16), and the service receives the token's spelling.
2. **Ordering, and no admin override. YES.**
   - The 401 comes before the body is parsed: PR cells D1b, D1c and D2d.
   - The 403 for a non-user principal comes before the body is parsed: my G9-G11 (a connector, an api_key token and a non-GUID userId, each with an INVALID body) answer 403, not 400. See N1: no shipped cell pins this.
   - A SYSTEM_ADMIN or super_admin who is not the assignee is refused (D4a/b). My G14: an admin who omits approverId reaches the service and gets its 400, with the row untouched.
3. **delegatedFrom (D2) is not made worse. YES, and it is named.**
   - My G7: stranger Y posts `delegatedFrom: X`, and `validateDelegation` is asked about Y, the token's user. This cell is red on develop's route, where the body chose the id.
   - My G8 measures the remaining gap exactly as the PR names it: a caller holding ANY valid approve delegation approves another's step, and an arbitrary `delegatedFrom` (Z) is recorded.
   - The PR body names both facts under "What this does NOT cover".
4. **Nothing widened. YES.**
   - `git diff --name-only 0fa14b4cbd33 40c99308b84b`: 5 files. 0 of them match transferAccess, approvalWorkflowService, delegationService, api-gateway or openapi (count 0, with the 5-file list as control).
   - In routes/workflows.ts, the hunks are the import, the schema line (`approvalRequestSchema` is used only at the approve route, line 181) and the approve handler. The other six routes are byte-unchanged.
   - E3 and E4 pin `GET /pending/me` and `POST /`.
   - The issuer's `ApprovalQueue.tsx:90-98` body `{ approverId: userId, decision, walletAddress, comment }` stays valid (its own id). Its only references at the head are its own file and the `index.ts` export: no render site.
5. **Reachability statement. ACCURATE.**
   - proxy.ts at the head registers only GET and POST `/api/workflows` and GET and DELETE `/api/workflows/:id`, gateway-local through Redis (lines 1126-1153).
   - Transfer is proxied only for `/api/transfers` and `/api/delegations` (lines 1108-1116). There is no catch-all.
   - batch.ts forwards only `/api/delegations`.
   - So the issuer's relative `/api/workflows/steps/...` call has no gateway route either.
6. **The tests are honest. YES, with one ordering gap (N1).**
   - Red first: I copied the two new files onto develop 6fdba4e's route and got 25 red, every one an AssertionError (0 TypeError), and 14 green. This matches the READY, cell for cell.
   - E2E-1 and E2E-2 assert at head that the row is `pending`, `actual_approver_id` is null, `decision` is null, writes are `[]`, delegation calls are `[]` and unexpected SQL is `[]`. Each has an assignee comparator on a fresh row.
   - **My own mutants** (`scratch/mutants.py`): whole transfer suite each time, file restored with sha256 equal (6ab58a7d52e7) after every one.

| Mutant | Cells red |
|---|---|
| g1, drop the mismatch refusal | 8: B1-B4, D4a, D4b, E2E-1, E2E-2 |
| g2, body passed through | 4: A3, A4, C1, D4c |
| g3, `===` | 1: A4 |
| g4, Unicode toLowerCase fold | 0: an **equivalent survivor**. Both sides are GUID-shaped before the compare: zod `guid()` on the body, and `isNonUserPrincipal`'s GUID arm on the token. |
| g5, drop the 401 | 7 |
| g6, drop the non-user refusal | 6 |
| g7, spread order, body wins | 1: A4 |
| g8, mismatch check after the service call | 8 |
| g9, admin override via isPlatformRole | 2: D4a, D4b |
| g10, refuse an omitted approverId | 3 |
| g11, 401 after the parse | 3: D2d, D1b, D1c |
| g12, non-user test on `caller` rather than `req.user` | 2: D3a, D3c |
| g13, `data.approverId ?? caller.userId` | 1: A4 |
| g14, approverId required again | 3 |
| **g15, the non-user 403 moved AFTER the body parse** | **0 against the PR's cells and the whole suite: a SURVIVOR.** My G9-G11 kill it (3 red). |
| gC, planted control | 13 |

## Other legs
- **Whole services/transfer suite:** develop 6fdba4e: 595 of 595 in 21 files. Head: **634 of 634 in 23 files**. No pre-existing red.
- **tsc:**
  - src (the service tsconfig): 0 errors at the head and at develop.
  - src plus every test file (my `scratch/tsconfig.tests_wt-*.json`; typeRoots pinned, rootDir at Blockchain/Dev): 0 errors at both.
  - Planted TS2322 controls fired: rc 2, 1 error in src and 2 in src+tests. Restored sha256-equal.
- **eslint** (the repo's flat config through the ESLint API) on the 3 changed TS files: 0 errors, 0 warnings. A planted control fired (`no-unused-vars` error, `no-var` warning). Restored sha256-equal.
- **docs-fragments check:** OK, rc 0. A planted unclosed `<div>` in the flow fragment gave FAIL rc 1 ("tags are not balanced"). Restored sha256-equal, then OK again. The 2 cheat/flow ADVISORY lines also print on develop 6fdba4e: pre-existing.
- **Merge-tree** (`scratch/mt.sh`, `scratch/mergetree.out`):
  - head and develop 6fdba4e: clean both orders, the same tree d018a9d8591f. Its workflows.ts equals the head's. It differs from the head only by develop's own gateway test file.
  - head and PR 2170: clean both orders, tree 18cfb391b4ab. 2170 touches only the escalation sweep (`@@ -620`) and its own test: semantically disjoint from processApproval.
  - A planted same-line control on develop's `approverId` schema line conflicts both orders (rc 1).
- `git status --porcelain` is empty in both worktrees after every plant. My cell files were moved out to `scratch/hold/`.

## Findings
- **N1 (LOW, test gap, not a security gap).** The PR states, and the code does, "a key or connector principal is refused before body parsing". No shipped cell pins it: every D3 cell sends a valid body. Mutant g15 (the non-user 403 moved after the zod parse) survives all 634 cells. Under that mutant a connector with an invalid body would get 400 instead of 403, and the service is still never reached. A one-row `it.each` like D1b/D1c for the 403 would pin it. My G9-G11 are that row.
- **N2 (LOW, behaviour change, not named as such in the PR).** An assignee whose token `userId` differs only in ASCII case from the stored `assigned_to` was admitted on develop (they sent the stored spelling in the body). At the head they get the service's 400 "User is not authorised to approve this step", because processApproval's compare is exact-case and now always gets the token's spelling. My G15 measured it: develop 200 (red there), head 400. `assigned_to` comes from POST `/` participants as sent. The builder lists the exact-case compare as candidate filing 4 ("beside KS-1591"). The PR body does not say it is a change from develop. Fail-closed, so not a security regression. Fix belongs in the service (sameId there), which is PR 2170's file.
- **N3 (INFO, docs).** The cheat fragment's Figures row still says "transfer unit suite 522 of 522 across 20 files … 483 of 483 across 18 files at develop", and the host row says develop `e659170439406810`. Those are the pre-rebase figures. The PR body's 634 of 634 in 23 files at the rebased head is the measured one, and I re-measured it. The flow fragment carries no stale count.
- **N4 (INFO, D2 confirmed as named).** After the fix, the delegation path cannot be borrowed (G7). The remaining gap (G8) needs a ruling and a service change. Wednesday carries it as a board filing, with the three uncallered GET routes.
- Gate faults: F1. One `@secuura/shared` build (a `tsc` build, not a suite) started at load1 8.33. After that every leg waited for load1 8 or under. Nothing else: cd 0, rm 0, no secret read or printed, nothing posted, pushed or merged, and no write outside this folder.

## What I did NOT cover
- A live stack, a real database, the gateway at runtime, a browser, the four platform suites, Node 24 (measured on the host's Node).
- PR 2170 merged with the head was not suite-run, only merge-tree checked and read as disjoint.
- PRs 575 and 649 were not re-measured.
- Whether any environment holds step rows.

## Needs Kam
Nothing blocks this GO. Held for his word, as the PR says: the transfer-service deploy. The D2 ruling and the sibling GET routes go to the board through Wednesday.
