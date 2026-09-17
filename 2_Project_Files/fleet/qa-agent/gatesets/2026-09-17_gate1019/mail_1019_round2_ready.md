SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1019 KS-1187 @82f09c8bd1bfab28e4d23c180cbaffea251685be (ROUND 2 of 2, TIER 1)
TS: 2026-09-17T06:39:12.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
READY FOR QA: #1019 KS-1187 ROUND 2 of 2 at `82f09c8bd1bfab28e4d23c180cbaffea251685be` (tier 1). F-1019-1 is fixed, and F-1019-2 and F-1019-3 ship with it.
- **The rule:** once the path resolved so far names the door (its first segment, under the door router's own case rule), any `.` or `..` segment after it is `undetermined` → 400 `NON_CANONICAL_PATH`, whether plain, percent-encoded, carrying `;params` or produced by an encoded slash.
- **Red-proof and tampers:** the five regression cells are red at `8b8996f8b` in both modes, reading `[200, null, one hit]`. The whole red-proof reads 24/70 red, as predicted. All 8 tamper rows landed as predicted, including the Q-WFIX-shaped row (24 reds).
- **develop `f8c7aaa39` merged in** after #1020 (your 02:04:06Z approval, extended to every head at 12:53 AEST): merge commit `82f09c8bd`, tree = my read-only prediction, no file overlap. At the merge commit: ks1187 70 / 70, api-gateway 55 / 524, shared 44 / 851, 0 failed, tsc rc 0.

## Recommendation
Gate the head `82f09c8bd` (tier 1): the round-2 change is `4d551f104`, and the merge commit only brings develop in. There is no round 3. Next, per your 06:22:46Z GO: the F1 measurement (five facts comments, then a STATUS). KS-1207 pushes only after #1019 merges.

## Detail

### Head and push
- Branch `feature/ks-1187-security-an-absolute-form-request-target-bypasses-the-ks-843`, fast-forward `8b8996f8b` → `82f09c8bd1bfab28e4d23c180cbaffea251685be`, two commits: round 2 `4d551f1046b55209b9ca5e4281e2cb9a868f67c2` (parent `8b8996f8b`) and the merge `82f09c8bd` (parents `4d551f104`, develop `f8c7aaa39`). `refs/pull/1019/head` = `82f09c8bd1bfab28e4d23c180cbaffea251685be` (GitHub REST, 06:37Z: open, base sha `f8c7aaa39`, 4 commits, changed_files 3).
- The round-2 commit vs `8b8996f8b`: `routes/proxy.ts` (+13 −3) and `__tests__/ks1187-erasure-door-judges-the-canonical-path.test.ts` (+148). PR files vs develop `f8c7aaa39` are still 3 (the ks843 test is round 1's): proxy.ts +88 −5, ks1187 test +370, ks843 test +7 −1.
- Push 06:29:58Z → 06:36:23Z, rc 0 (`8b8996f8b..82f09c8bd`). EXPECT_OLD guard held; push_protocol verify **PROTOCOL-CLEAN**, shape fast-forward, origin at the head.
- In-hook preflight: **12/15 legs ran, 3 SKIPPED (3, 4, 8: no local stack), nothing failed**. Not a full pass. Leg 1 `spec is in sync`, leg 2 OK, leg 5 59 / 59, legs 6 and 7 OK.

### The rule and why no legitimate originate gdpr route is refused
- `erasureDoorVerdict` gains `namesDoor` (the one case rule, used for the dot check and the final comparison). In the segment loop, a `.` or `..` segment returns `undetermined` when `namesDoor(segments[0])`; otherwise the round-1 handling runs (skip `.`, pop on `..`, climb-out undetermined).
- **Only after the door is named.** For every non-erasure gdpr route the check reads false and the round-1 path runs. The real-app Tightening-A controls stay forwarded unchanged; GWIDE below shows what a broader rule would break.
- **The erasure routes are `POST /erasures` and `GET /erasures/:externalRef`.** A legitimate caller puts no dot segment after the door. A reference that is exactly `.` or `..` cannot be sent reliably as a segment (RFC 3986 §5.2.4 removes dot segments, and §6.2.2.2 makes an encoded dot equivalent to a dot).
- **Dotted references stay the door:** a leading-dots reference, `a.b`, a trailing dot, and W18 `erasures/%2e%2e%3bx` (a verdict control, plus a real-app control refused 403 with 0 hits).
- **One refusal changes class:** `erasures/abc/..` was the door (403 without the scope) and is now 400. It is refused either way, and originate routes no erasure handler for it.
- **Not re-run by me:** your 17-route and 26-spelling census on this exact rule.

### Cells (31 new; the file has 70)
- **Verdict:** 12 dot-after-door spellings → undetermined (`erasures/..`, `%2e%2e`, `.%2e`, `%2E%2E`, `..;x`, `%2e%2e%2fabc`, `../`, `.`, `abc/..`, `ERASURES/..`, `x/../erasures/..`, absolute-form `erasures/..`); 4 dotted-reference controls → door; the dot rule follows the case rule (`ERASURES/..` under a case-sensitive router → not-door; `erasures/..` → undetermined).
- **Real app, test mode:** GET `erasures/..`, `%2e%2e`, `.%2e`, `..;x`, `%2e%2e%2fabc` by a connector without `subjects:erase` → `[400, NON_CANONICAL_PATH, []]`. W18 → `[403, []]`.
- **Real app, production (`/api/v1/gdpr/...`):** the same 5 → `[400, NON_CANONICAL_PATH, []]`. The code is the door's, not `security.ts`'s `BAD_REQUEST`, measured by the cells; I did not read why the detector passes them.
- **F-1019-3:** a bare app mounting `createProxyRoutes` with a recording `authenticateToken`. POST `%65rasures` with the scope → `[200, ['POST /api/gdpr/%65rasures']]`; the catch-all layer sees `{baseUrl: /api/gdpr, url: /%65rasures}`. Control: the door's chain ran (baseUrl `/api/gdpr/erasures`). With the restore removed the catch-all sees `/erasures`, so the cell goes red for its stated reason.
- **F-1019-2:** the same bare app with express's `Router` doMocked to `caseSensitive: true` (a new default object; the real module is not mutated). Control: `erasures/..` → 400. Cell: `ERASURES/..` → `[200, null, ['GET /api/gdpr/ERASURES/..']]`; under a constant `false` it is 400. The cell's comment says it pins the option read, not that a case-sensitive gateway beside a case-insensitive upstream is safe.

### Red-proof at `8b8996f8b` (prediction written first: 24 red / 46 green)
`proxy.ts` written back to blob `db1534753`; the new test file run; restored (sha256 equal). 70 run: **46 green, 24 red, all `AssertionError`**. The 24 are the 12 dot verdict cells, the case-rule cell, 5 test-mode, 5 production and the F-1019-2 control. Every real-app red read `[200, null, one hit]`. W18, the dotted-reference controls, F-1019-3 and the F-1019-2 router cell stayed green, as predicted.

### Tamper table (at the round-2 commit `4d551f104`; this PR's files are byte-identical at `82f09c8bd`)
Each row: anchor count 1, `tsc --noEmit -p .`, the WHOLE api-gateway suite (54 files / 512, pending 0), restore by bytes (sha256 equal) and `git diff --quiet HEAD`. Every red is an `AssertionError`; no load failure.

| Row | Tamper | Reds (pred) | tsc |
|---|---|---|---|
| T0 | none | 0 (0) | 0 |
| QWFIX | the dot check removed | 24 (24): the red-proof set | 0 |
| GHARDFALSE | `Boolean(false && …caseSensitive)` | 1 (1): F-1019-2 router cell | 0 |
| GNORESTORE | `req.url = req.url \|\| original` | 2 (2): F-1019-3 cell + the ks843 F-7/F-9 source pin | 0 |
| GONLYDOTDOT | the check on `..` only | 1 (1): the `erasures/.` verdict cell | 0 |
| GCASEFOLD | the dot check lower-cases regardless of the router | 2 (2): verdict case-rule cell + F-1019-2 router cell | 0 |
| GWIDE | every dot segment refused, door or not | 7 (7): verdict `./erasures`, `x/../erasures`, the canonical-path cell, the case-rule cell; real-app `./erasures` and `x/../erasures`; the F-1019-2 router cell | 0 |
| TI | inert comment | 0 (0) | 0 |

### Suites at the round-2 commit `4d551f104` (your predecessor's run)
- api-gateway **54 / 512 all pass** (round 1: 481).
- packages/shared **44 / 851 all pass**.
- `tsc --noEmit -p .` rc 0.
- Test-including program (`exclude: []`): 590 files, ks1187 in the program, **31 error lines / 11 files, 0 in either touched file** (your base = head figure).
  - **Slip:** my first program inherited `exclude: src/__tests__` and read 0; the file-list control caught it.
- eslint: `proxy.ts` the same 4 `no-unused-vars` (`_e`, `_e`, `err`, `err`); ks1187 test 0.

### Develop merge-in (at `82f09c8bd`)
- **Prediction first** (read-only): merge-base `fa887f382`. #1019's files since then are `proxy.ts` and the ks1187 / ks843 tests. develop's are #1017's `index.ts`, `middleware/auth.ts`, `middleware/rateLimitEnforce.ts` and ks1195 test, shared's ks781 test, and #1020's `lock-discovery.mjs`. Overlap: none. `git merge-tree --write-tree 4d551f104 f8c7aaa39` = `99df1503e4f18ac444baed015659fecbb912bbb0`.
- **Merge:** `git merge --no-ff` with a message naming no ticket id. Tree `99df1503e` = the prediction.
- **Content re-read:** this PR's 3 files byte-identical to `4d551f104`; develop's 6 files byte-identical to `f8c7aaa39`; `git diff f8c7aaa39 HEAD` = exactly the 3 PR files.
- **Suites at `82f09c8bd`** (all predicted before the run): ks1187 solo **70 / 70**; api-gateway **55 files / 524, 0 failed, 0 pending** (= develop's 454 + this file's 70); packages/shared **44 / 851, 0 failed**; `npx tsc --noEmit -p .` rc 0 (0 lines). Porcelain 0 after.
- **Not re-run at the merge commit:** the test-including program, eslint, the red-proof and the tamper table (the PR's files are unchanged by the merge).

### PR, ticket, links
- PR body: a Round 2 section added above round 1's record (the rule, why no route is refused, cells, red-proof, tamper table, Test Evidence, the merge-time Records from your item 5). Round 1 is kept below a separator as the record, byte-identical. Closing phrases in the new body: 0 (control: a planted "Fixes KS-1" counts 1). The new section names only KS-1187 and KS-843; its one KS-744 mention was reworded, to add no new ticket id. PR body PATCH 06:37Z, read back equal. KS-1187 one line: comment `76dec71e-4759-4e37-8996-af82cfe03f7f` (06:38:07Z, "Kam ruled fix-now 2026-09-17; the fix is #1019.").
- linkKinds after the push and after the body PATCH (06:37:09Z and 06:38:28Z): [KS-843 contributes, KS-1187 contributes], both In Progress; control pull/99999 [].

### Listeners
4 `login_stub.mjs` listeners from this push stopped by verified pid (CONTROL: ps rows parsed 1097; 0 alive after; non-node controls 17 before and after). 16 other node LISTEN sockets failed the stopper's pid checks (not a login stub started in this worktree after the push); I left them alone and have not identified them.
