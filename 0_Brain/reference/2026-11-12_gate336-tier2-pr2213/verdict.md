PR 2213: GO WITH NOTES (at head b119c3bd239b; tier 2; round 1)

Gate 336, tier 2 (Sonnet), one session, 2026-11-12 about 19:02 to 19:25 AEDT. Findings only: nothing fixed, pushed, commented, mailed, merged or written to Linear. All write verbs and installs were in `scratch/` of this folder (`scratch/repo` clone, push URL DISABLED; worktrees `wt-before` = develop ed5b86ea20ae, `wt-head` = PR head; `npm ci --ignore-scripts` in wt-head, then `npm run build` of packages/shared so `@secuura/shared` resolves). The project checkout was touched only by `GIT_OPTIONAL_LOCKS=0 git ls-remote`. GitHub: reads only (`gh pr view`) with the Blockchain project's own `GH_CONFIG_DIR`. Node v26.8.1.

**Pins.** Start (19:02) and end (about 19:24): develop ed5b86ea20aebcf8585838a5ed2ca7959f3fd62b, refs/pull/2213/head b119c3bd239bd5d393e4b3d4661ba3ba5682a734. NEITHER MOVED. PR: open, not draft, MERGEABLE, base develop, 1 commit on ed5b86ea20ae, 3 files +3 -3, `closingIssuesReferences` empty.

**Verdict in one paragraph.** Everything I could re-take reproduced. The product change is the one line the READY names (`{ walletAddress, error: reason }` becomes `{ error: reason }`, governanceService.ts:420) and that is the only logger call in the file or in the service that carried the wallet on this failure. The two edited cells are real red-first (4 red cells with the product reverted, 67 of 67 green with it), no assertion count changed, the whole governance suite is 367 of 367 at develop and at head, tsc with tests is clean (planted control fired), and the 2099 overlap reproduces (merge-tree rc 0 both orders, same tree; planted control conflicts both orders). One real caveat on Q1: the wallet address still reaches the logs on a failing GET by address through two OTHER log lines (G336-2213-1). The PR does not claim otherwise, so it is a note, not a blocker.

## Answers to the questions

**Q1. Is the address removed from every log path of that failure? From the line the PR names, yes; from the request as a whole, no for GET.**
- Diff base..head, the whole file greps: `logger.(error|warn|info|debug)(` calls naming address/wallet in governanceService.ts. Base: line 420 (`walletAddress`), 439 (`userId`), 450 (no address). Head: line 420 now `{ error: reason }`; the multi-line `logger.info('Vote delegated', ...)` at 1234-1238 (`delegatorAddress`, `delegateAddress`) is the only remaining address-carrying logger call, disclosed in the body as out of scope. Control: the same grep finds the old line at base (positive hit) and not at head. The five callers (lines 622, 662, 715, 750, 814) have no logger call of the address in their own bodies; none changed.
- Other layers on the same failure (not covered by the PR): `services/governance/src/index.ts:55` logs `Request received { method, path }` for every request, and `packages/shared/src/errors/error-handler.ts:260-274` logs `[Error] { requestId, statusCode, errorCode, message, stack, path, method, ip, userId }` at statusCode >= 500 (the 503 thrown here). `getParticipant(idOrAddress)` (line 750, route `GET /api/governance/participants/:id`) can reach the failing read with the wallet address IN THE URL PATH, so for that route both of those lines still write the address. For `POST /participants/register` the address is in the body, so neither line carries it. Read statically (the route, handler and logger code); I did not run the stack to capture a live log.
- Does the new log still identify the participant? The log object is `{ error: reason }` only; `reason` is `err.message` (or the constant 'unreadable thrown value'). With a parameterised query (`$1`) node-postgres messages do not embed the bound value, and I did not find a path that does. Nothing in the line names the participant. The `[Error]` line above adds `userId` and `ip` (pre-existing, caller identity, not the wallet).

**Q2. Tests: real red-first, nothing weakened.**
- Product put back to develop's file in wt-head, edited tests kept, `npm test --prefix <governance> -- ks1940 ks1942`: rc 1, 2 suites failed, 4 failed / 63 passed of 67. The four: ks1940 `RED ks1940 T2b` x2 ("a revoked Proxy thrown by the wallet lookup..." and "an Error whose message getter throws...") and ks1942 `control ks1942 NT1b` x2 (same two throw shapes). Head product restored (blob copy, worktree status clean): 2 suites, 67 of 67, rc 0. Matches the READY (2 of 24, 2 of 43). `scratch/redfirst.log`, `greenagain.log`.
- Assertion count: `expect(` occurrences ks1940 67 before / 67 after, ks1942 125 / 125; `it/test` blocks 21 / 21 and 41 / 41; numstat 1 added 1 removed in each. The only change inside each cell is removing the `walletAddress` key from the expected `toEqual` array element, which is strict (`toEqual` of the whole logged array), so the cell now fails on both an extra key and a missing `error`.
- A weakening check by shape: both cells still assert `errorLogs(...)` equals exactly one entry, `expect(r.body).toEqual(...)` (503 body), `expectNothingWritten(before)` and the planted-secret-absent assertion; none was removed.

**Q3. Suite and tsc.**
- Whole `services/governance` suite by the package's own `jest` script: develop (all three files swapped to the base blobs in wt-head) 20 suites, 367 of 367, rc 0; head 20 suites, 367 of 367, rc 0. `scratch/suite_base.log`, `suite_head.log`.
- tsc with tests (a scratch `tsconfig.tests.json` extending the service's own, tests included, `noEmit`): rc 0, 0 error lines. Planted control (a string assigned to a number appended to `requestSchemas.test.ts`): rc 2, 1 error line, file restored. Production `tsc -p tsconfig.json`: rc 0.
- Load1: below 8 at each start (7.45 / 6.81 / 6.2), peaked at 8.45 right after one suite run (other seats' load plus the run), stayed under 8.5; flagged for the record, nothing was run above 8 at its start.
- My first suite attempt failed 19 of 20 suites with "Cannot find module '@secuura/shared'": my environment (`--ignore-scripts` leaves the workspace package unbuilt), not a PR defect; fixed by `npm run build` in packages/shared and the whole suite re-run (above). The failed run was discarded.

**Q4. Overlap with PR 2099: reproduced.**
- PR 2099 head 8967de8b17558890dc4ace2732cb8350768df601, merge-base c0e6e744b7b2. Its hunks on governanceService.ts: old-side 606-611 (`@@ -606,5 +606,7`) and 1208 (`@@ -1208,0 +1211,7`); PR 2213's: line 420 (`@@ -420 +420`). Disjoint. Develop did not change the file since 2099's merge-base (empty diff).
- `git merge-tree --write-tree` rc 0 in BOTH orders, same merged tree cd5a2f9ada58094b18df5544a1e1836eb6ab5195. Survival: in the merged file the old line is absent (control: present at base) and the new line is present (control: absent at 2099); merged vs 2099 differs only at line 420; merged vs PR 2213's head differs by 19 lines = exactly 2099's own diff size against base; the two test blobs in the merged tree equal PR 2213's (256b69dd..., 719b3f00...), 2099 does not touch them (its blobs equal base).
- Planted control: a commit on 2099's head that edits line 420 itself: merge-tree rc 1 in BOTH orders, conflict stages on governanceService.ts. `scratch/overlap.out`, `ctrl.out`.

**Q5. Body.** TIER 2 statement is the first body line after the heading; refs: only KS-2061 (title and body; my regex finds one Linear key and no other); no closing word (regex clean; `closingIssuesReferences` empty); no mention outside code spans; "Merge to develop only"; NO-PAIR paragraph present and as ruled (no fragment pair added; I confirmed the diff adds none); existing-cell sentence present and accurate (cells, expected objects, +1 -1 each, "tightening"). The numbers I re-took match the body: 3 files +3 -3, suite 367 of 367, red counts 2 of 24 and 2 of 43, tsc rc 0, hook quote. The body's phrase "the wallet address is no longer written to the error log" is true of that call only (see G336-2213-1). Not re-run: docs-fragments check, audit:gate, strict apply, pre-push hook legs.

## Findings

**G336-2213-1 (Minor): the wallet address still reaches two other logs on a failing GET by address.** `GET /api/governance/participants/:id` with an address id: `index.ts:55` logs the path on arrival and the shared `errorHandler` logs `path` (plus `ip`, `userId`, stack) on the 503. The PR's body does not claim these, and its title ("a failed by-address participant read no longer logs the wallet address") reads as the whole failure. A fix belongs in a separate row (redact or hash the id in the path, or log the route pattern). Static reading, no live log captured. Not a blocker.

**G336-2213-2 (Note): the success-path `Vote delegated` info log still writes two wallet addresses** (lines 1234-1238). Disclosed in the body and the READY, not in this PR, "board seat files it". Confirmed present at head.

**G336-2213-3 (Note): no test pins the address's absence from the OTHER log lines or from the GET route.** The two edited cells cover the register (POST) route only and the `logger.error` array only; a regression through the GET path would pass. Fits G336-2213-1; no action for this PR.

**G336-2213-4 (Info): the failure line now carries only the reason.** It no longer says which lookup (the by-id sibling keeps its `id`; the by-address one has no identifier at all). Acceptable for the stated purpose; support may want a request id (the `[Error]` line has one).

**G336-2213-5 (Info): load1 peaked at 8.45 once** straight after the head suite run (shared Mac, other seats). The commission's bound was a start condition; every run started under 8.

No Major finding.

## NOT TESTED

- A live log of the failure (no running stack, real DB or sink) so G336-2213-1 is from code, not a captured log; the shared logger's PII redaction (packages/shared/src/logger) was seen but governance uses its own winston logger and I did not run it.
- Open-PR census of the three paths (only PR 2099 re-measured; census of other PRs not repeated), merge-tree with any PR other than 2099, strict `git apply` at either base, docs-fragments check, `audit:gate`, the pre-push hook legs.
- Node 24, other packages' suites, the four platform suites, eslint (governance has no lint script), any deploy.
- The Spark shadow review was not run (the commission did not ask for it; no digest used, raw rc read directly from every run).
