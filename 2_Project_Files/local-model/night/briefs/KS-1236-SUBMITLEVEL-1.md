# KS-1236 SUBMITLEVEL-1 PIN THAT POST /me/verification REFUSES A TARGET LEVEL AT OR BELOW THE SUBJECT'S CURRENT LEVEL (400 BAD_REQUEST, no request row, no store read) — the submit-side ordering check that the ticket says is RIGHT today and the review side lacks — the real userRoutes driven in process over the KS-1194 harness — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, two cells added, no product file** (written 02:50 on 2026-09-21, board widening round 23)

File: `Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`
Tip: `cbae988dbe90ebe556459ada2cb437eaf80e2402`
Runner: `vitest`

Written from develop `cbae988dbe90ebe556459ada2cb437eaf80e2402` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 02:50 on 2026-09-21, read verbs only; the #1105 squash-merge). The test file at that tip is **220 lines**, read whole; its full content is in `files[...]` of your input. The product the cells pin is `Blockchain/Dev/services/auth/src/routes/users.ts` (blob `3bfa47dcde01`, **1436 lines**, read whole): `verificationRequestSchema` at `:158-161` (`targetLevel: z.enum(['STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT'])`), `POST /me/verification` at `:1257-1320`, the subject read at `:1260`, `LEVEL_ORDER` at `:1263`, the two `indexOf` reads at `:1264-1265`, **the ordering guard `    if (targetIndex <= currentIndex) {` at `:1267`** (throws `BadRequestError` — `middleware/errorHandler.ts:30-33`, status 400, code `BAD_REQUEST` — with the message `Cannot request <target> — current level is already <current>`), the pending-request read at `:1273` (the FIRST `dbQuery` of the handler) and the save after it. This service runs **VITEST** (`package.json` `"test": "vitest"`, `vitest ^4.1.9`, no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `routes/users.ts` or any other product file: the behaviour is already what it is at the tip, and these cells PIN it.

## What the cells pin (one paragraph)

KS-1236 reports that approving a stale PENDING request after the subject's level has already risen stores the LOWER level: "Submit refuses a target at or below the current level, but review re-checks nothing." The fix it recommends is on the REVIEW side (re-check the ordering at approve, or make the level UPDATE conditional) — and both shapes keep the submit-side guard as it is. That guard, `users.ts:1267`, is the half that is RIGHT today, and nothing in the auth suite asserts it: `git grep` over `src/__tests__` at the tip for `Cannot request`, `current level is already`, `targetLevel: 'STANDARD'` and `targetIndex`: 0 lines each (positive control `targetLevel: 'ENHANCED'`: 8 lines, all valid upgrades from BASIC). So the guard could silently loosen two ways — the EQUAL case admitted (a subject at ENHANCED requesting ENHANCED gets a PENDING row that approve then "raises" to the same level) or the guard reduced to nothing (a subject at HIGH requesting ENHANCED gets a PENDING row that approve stores as a DOWNGRADE, the very hole KS-1236 describes, now reachable from submit without any race). This change adds TWO cells to the `describe('KS-1194 — POST /me/verification never acknowledges a request that did not persist', ...)` block, using the file's own `user()`, `state`, `call()`, `code()` and `dbQuery`: the subject's stored `verificationLevel` is set to ENHANCED (cell 1) or HIGH (cell 2) and `POST /me/verification` is called with `targetLevel: 'ENHANCED'`; each asserts `[status, code, rows.size, dbQuery calls]` equals `[400, 'BAD_REQUEST', 0, 0]` — refused at the guard, before the pending-request read and before any INSERT. Every existing cell is unchanged. **It pins TODAY's submit-side ordering check and decides nothing about KS-1236's review-side fix.**

## The exact change — ONE hunk in the test file

The new cells go at the END of the first `describe` block (opened at `:131`), directly above the line that closes it (`:165`, `});` at column 0 — the ONE trailing context line). There is NO leading context: the line above (`:164`, `  });`, the end of the `🟢 control` cell) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` then `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`.**

```
@@ -165,1 +165,15 @@
+  it('RED KS-1236: a target level EQUAL to the current level is refused 400 BAD_REQUEST before any store read or INSERT', async () => {
+    user('u-1236-same');
+    (state.users.get('u-1236-same') as Record<string, unknown>).verificationLevel = 'ENHANCED';
+    state.caller = { userId: 'u-1236-same', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
+    expect([r.status, code(r.json), state.rows.size, dbQuery.mock.calls.length]).toEqual([400, 'BAD_REQUEST', 0, 0]);
+  });
+  it('RED KS-1236: a target level BELOW the current level (a downgrade) is refused 400 BAD_REQUEST before any store read or INSERT', async () => {
+    user('u-1236-down');
+    (state.users.get('u-1236-down') as Record<string, unknown>).verificationLevel = 'HIGH';
+    state.caller = { userId: 'u-1236-down', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
+    expect([r.status, code(r.json), state.rows.size, dbQuery.mock.calls.length]).toEqual([400, 'BAD_REQUEST', 0, 0]);
+  });
 });
```

`describe`, `it`, `expect` and `vi` are already imported by the file at `:15`; `state` (`:21-30`, a `vi.hoisted` object holding `users`, `rows`, `caller`), `dbQuery` (`:34-49`, the hoisted mock the `../db` module returns), `user()` (`:108-110`, seeds a `BASIC` user into `state.users`), `call()` (`:114-117`, a real HTTP call to the file's own loopback server on an ephemeral port) and `code()` (`:118`) are the file's own helpers — you add NO import and NO helper. The `beforeEach` at `:120-129` clears `state.users`, `state.rows` and every mock before every cell, so the seeding is local to each cell. `state.users.get(id)` returns the object `user()` stored, so assigning `verificationLevel` on it is what `userRepo.getUserById` (mocked at `:51-53`) hands the route.

## Cells

- `samelevel` = `RED KS-1236: a target level EQUAL to the current level is refused 400 BAD_REQUEST before any store read or INSERT`
- `downgrade` = `RED KS-1236: a target level BELOW the current level (a downgrade) is refused 400 BAD_REQUEST before any store read or INSERT`

## Red cells

The two cells below are GENUINE assertion-reds: each fails under the tamper(s) named for it and passes at the tip. They are declared here rather than with a red glyph in their titles because every `+` line in this diff must be ASCII only.

- RED KS-1236: a target level EQUAL to the current level is refused 400 BAD_REQUEST before any store read or INSERT
- RED KS-1236: a target level BELOW the current level (a downgrade) is refused 400 BAD_REQUEST before any store read or INSERT

## Tampers

Two single-line tampers on the SAME line of `routes/users.ts` (`:1267`, the ordering guard; it occurs EXACTLY ONCE in the file — counted with `grep -c -F -x`, 1; positive control `grep -c -i LEVEL_ORDER` over the same file is 3: `:1263`, `:1264`, `:1265`). They are the two shapes a loosening can take: the EQUAL case admitted (`<=` becomes `<`), or the guard reduced to an unknown-level check that can never fire (`<= currentIndex` becomes `< 0` — `targetIndex` is never negative because the zod enum at `:159` only admits the four listed levels). Each `From` is the tip's line at that number, byte for byte, and each `To` is valid TypeScript (both compare two numbers), so nothing fails to load and no cell reds for the wrong reason. The checker plants them ONE AT A TIME and restores the file by bytes between them.

### EQUALADMITTED — a request for the subject's CURRENT level is admitted
File: `Blockchain/Dev/services/auth/src/routes/users.ts`
Line: 1267
From:
```
    if (targetIndex <= currentIndex) {
```
To:
```
    if (targetIndex < currentIndex) {
```
Reds: `samelevel`

### GUARDNEVERFIRES — the ordering guard is reduced to an unknown-level check, so a downgrade is admitted too
File: `Blockchain/Dev/services/auth/src/routes/users.ts`
Line: 1267
From:
```
    if (targetIndex <= currentIndex) {
```
To:
```
    if (targetIndex < 0) {
```
Reds: `samelevel`, `downgrade`

## Controls

- `🟢 control: with no database at all the request is still accepted in memory, as before`
- `🟢 control: a healthy reject answers 200, saves REJECTED and never touches the level`
- `🔴 approve: the row is saved APPROVED BEFORE the level is raised`

*(All three are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:158`, `:215` and `:177` before this hunk, `:158`, `:229` and `:191` after it — each occurs exactly once in the file and none is a prefix of any other title. The glyphs are the FILE's, in EXISTING titles that this diff never writes; the new cells' titles are ASCII. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix. The other 9 existing cells (three submit cells at `:132`, `:140`, `:150`; five review cells at `:170`, `:183`, `:190`, `:197`, `:208`) are also green under both tampers — every one requests ENHANCED from a BASIC subject, so `targetIndex` (2) is above `currentIndex` (0) under `<=`, `<` and `< 0` alike, or never reaches the guard at all (the review route) — but are left undeclared. The `:158` control proves a VALID upgrade from BASIC still passes the guard beside the new cells; the `:215` and `:177` controls prove the review route — where KS-1236's defect actually lives, and which these cells never drive — still runs.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip both new cells pass: `user('u-1236-same')` stores a BASIC user, the next line sets its `verificationLevel` to `'ENHANCED'`, `state.caller` makes the route's `req.user.userId` that id; `call()` POSTs `{ targetLevel: 'ENHANCED' }` to the real `userRoutes` on the file's loopback server; `:1259` parses the body (ENHANCED is in the enum), `:1260` asks the mocked repo for the user (the seeded object, level ENHANCED), `:1263-1265` compute `currentIndex` 2 and `targetIndex` 2, **`:1267` is true** (2 <= 2), `:1268` throws `BadRequestError`, the file's `errorHandler` answers 400 `{ error: { code: 'BAD_REQUEST', ... } }`; nothing reached `:1273`, so `dbQuery` was never called and `state.rows` is empty. The asserted array is `[400, 'BAD_REQUEST', 0, 0]`. The `downgrade` cell is the same with the subject at HIGH: `currentIndex` 3, `targetIndex` 2, 2 <= 3 true, the same 400. (Measured: see MEASURED.)

Under **EQUALADMITTED** `:1267` reads `2 < 2`, false, for `samelevel`: the handler goes on to `:1273` (`dbQuery` call 1, the pending read: no row), then saves the request (`dbQuery` call 2, the INSERT the mock records into `state.rows`) and answers 200 — the array reads `[200, undefined, 1, 2]` — assertion red. `downgrade` under it reads `2 < 3`, true, still 400 — green (declared so). Under **GUARDNEVERFIRES** `:1267` reads `2 < 0`, false, for BOTH cells: both proceed to the pending read and the INSERT and answer 200 — both arrays read `[200, undefined, 1, 2]` — assertion red on both. Under BOTH tampers every existing cell stays green: the submit cells request ENHANCED from a BASIC subject (`2 <= 0`, `2 < 0`, `2 < 0` are all false — the guard never fired for them at the tip either), and the review cells never enter this handler.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` line.** `routes/users.ts` at `cbae988db`, line 1267 is `    if (targetIndex <= currentIndex) {` (4-space indent), byte for byte; it occurs **exactly once** in the file (`grep -c -F -x`, 1); the positive control `LEVEL_ORDER` (case-insensitive) matches 3 lines. `git blame` at the tip: `:1267` last touched by `e50dbde98` (2026-02-18); the file's last change is `f6669623c` (KS-1194, the same PR that wrote this test file). The checker plants and restores it (T8 by sha256 after each; tip blob sha256 `96408a532a73ef77`).
- **Premise: the ticket's claim, re-derived.** KS-1236: "Submit's check (read at develop `34cdcfb26`): `services/auth/src/routes/users.ts:1252-1254` compares `LEVEL_ORDER` indexes for the current and target levels" — at this tip those are `:1263-1267` (KS-1018's rethrow blocks and KS-1194's save ordering moved the handler down). "Review: the approve writes the target level through `updateUser` with no comparison" — the review handler at `:1323` onwards is NOT driven by these cells; its fix is the ticket's. `KS-1236` occurs **0** times under `services/auth/src`.
- **Premise: the anchor.** The test file is **220** lines; `:165` is `});` (column 0), the closing line of the first `describe` (opened `:131`); it is the trailing context line. `});` at column 0 occurs 6 times in the file (`:70`, `:77`, `:105`, `:129`, `:165`, `:220` — `grep -n -x`), so it is NOT unique; `git apply` anchors this hunk by its line number and the one-line context, exactly as the KS-1244 hunk on `auth.test.ts:211` did with a repeated `  });`. The insertion is pure, so no blank line is asked of you anywhere; the line above the insertion (`:164`, `  });`) is not written.
- **Premise: the in-process route call.** `beforeAll` (`:94-105`) mounts the REAL `userRoutes` and `errorHandler` on an express app listening on `127.0.0.1:0` (an ephemeral port chosen by the OS — the file's own harness; nothing in this brief names a port); `call()` fetches it and returns `{ status, json }`. `authenticate` is mocked (`:71-77`) to inject `state.caller` as `req.user`; `userRepo.getUserById` (`:53`) returns `state.users.get(id)`; `../db` (`:78`) is `{ isDbAvailable: () => state.dbAvailable, query: dbQuery }` with `dbAvailable` reset to true by `beforeEach`.
- **Premise: the enum.** `targetLevel` must be one of `STANDARD | ENHANCED | HIGH | GOVERNMENT` (`:159`), so the EQUAL case is driven with the subject AT ENHANCED requesting ENHANCED, and the downgrade with the subject at HIGH requesting ENHANCED — `BASIC` cannot be requested (zod refuses it before the guard, a different 400).
- **Premise: `+` lines that also occur at the tip.** Two, both added by this brief (so T4 accepts them): `  });` (the cell closer, unavoidable) and `    const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });` (`:136`, `:146`, `:154`, `:162` — the file's own call idiom, reused verbatim). No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick). The titles use `-`, `:` and `_`, no em dash, no glyph.
- **Premise: the runner.** `services/auth/package.json` at the tip has `"test": "vitest"` and `vitest ^4.1.9` in devDependencies, with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it.
- **Premise: no live-lane collision.** `routes/users.ts` is not `api-gateway/src/index.ts`, `preflight.sh`, `enforcement.ts` or under `services/anchoring/**`; the test file is none of Seat B 11th's six. No held `READY_*` and no brief in `night/briefs/` names this test file (`grep -il`, 0 and 0). The held READYs that name `routes/users.ts` are KS-1050 (merged as `e02515f8f`, spent), KS-1018 (merged as `eb1051fd3`, spent), KS-692 (vc-issuer — a mention only), KS-938 (mfa.ts — a mention only) and KS-1188-F1b (a NEW test file `ks1188-users-me-503-route.test.ts`, tamper at `users.ts:909`, unmerged): none modifies `users.ts` and none plants `:1267` — see Collision.
- **Premise: the surface.** The cells drive one auth route in process with a mocked authenticator, a mocked repo and a mocked db. No session, no MFA state, no JWT, no product bytes. AUTH surface, test-only pin (allowed under Wednesday's reading).

## Collision

**No held READY touches this test file** (`grep -il ks1194-a-failed night/READY_*`: 0). **The ONE brief that does is this round's sibling `KS-1006-WRONGCODE-1` (same file, DISJOINT hunks: `@@ -56,1 +56,2 @@` and `@@ -120,1 +121,10 @@`, both ABOVE this hunk; tamper `users.ts:1105`, not `:1267`).** Both orders apply with `git apply` — measured in the MEASURED section: KS-1006 first, then this: this hunk lands at `:175` (offset +10, the `});` context found ten lines down); this first, then KS-1006: both of its hunks at their stated lines; the file is byte-identical either way (244 lines, one sha256), the file with both runs 14/14, and no tamper of either brief reds the other's cells. **Order for the raise: either; if raised in one PR, put KS-1006's two hunks first (lower line numbers first) and re-derive this header as `@@ -175,1 +175,15 @@`.** Product file `routes/users.ts`: the only unmerged held READY naming it is `READY_KS-1188-F1b` (a new test file of its own; its tamper is `users.ts:909`, the GET /me 503 rewrite) — different line, different handler, planted-and-restored, neither moves the other; KS-1050 and KS-1018 are merged into this tip (their comments are at `:1246` and `:935`), spent holds. Seat B 11th's six files include neither this test file nor `users.ts`. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21, `--shared` scratch clone at `cbae988db`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_round23-drafter-precheck/KS-1236/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md` = this brief's own hunk with the two file-header lines, fresh `--shared` clone `r23_clone_1` at `cbae988db`, farmed by the harness's `prepare_clone.sh`): **RESULT: PASS (8/8)** — T1 one fenced block; T2 touched set == the test file only; T3 strict apply; T4 every `+` line byte-exact; T5 green at the tip **13/13 cells** (11 existing + 2 new, every declared cell present); T6 EQUALADMITTED red set == {samelevel} and GUARDNEVERFIRES red set == {samelevel, downgrade}, every red an assertion failure — received `[ 200, undefined, 1, 2 ]` vs expected `[ 400, 'BAD_REQUEST', 0, 0 ]` in all three reds (`KS-1236/out.md.checker/tamper_*.cells.json`); T7 all three controls green under both; T8 `users.ts` restored to sha256 `96408a532a73` after each. Source tracked-modified count 0 before and after (`KS-1236/prepare.log`).
- Whole auth suite in the same clone: bare tip **66 files, 779/779** (`full_suite_before.out`); with this hunk applied **66 files, 781/781** (`full_suite_after.out`) — +2, 0 new red. The applied file is kept as `KS-1236/ks1194_with_cells.test.ts` (sha256 `aadf1202d29b595a`).
- With the sibling KS-1006 brief's hunks as well (measured in `KS-1006/`): both apply orders give the same 244-line file (sha256 `f9f0b7fce6009962`); the file runs **14/14**; the whole auth suite **782/782**; EQUALADMITTED / GUARDNEVERFIRES red exactly this brief's cells and KS-1006's two tampers red exactly its one cell (`KS-1006/cross_*.out`).

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` / `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`, then the hunk above exactly as shown (`@@ -165,1 +165,15 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (auth surface, test-only pin — allowed). Refs KS-1236** (and KS-1194, whose harness and file this rides). **NEVER Closes** — KS-1236 asks for a REVIEW-side change (re-check the ordering at approve, or a conditional level UPDATE); this brief pins the SUBMIT-side guard that both shapes keep, and leaves the review-side downgrade as the open defect it is.
- **Not from a gate cell.** Found by the 2026-09-21 board widening (round 23): the ticket's own sentence "Submit refuses a target at or below the current level" names a behaviour no cell asserts.
- **Not pinned here, said plainly:** the review route's approve of a stale request (the defect — a cell asserting today's 200 + stored `enhanced` would pin the bug); the `already pending` refusal at `:1274` (right today, but its one-line loosening reds nothing these cells assert — a separate pin if wanted); the exact error message text (the code `BAD_REQUEST` is asserted, the message is not, so a reword does not red this).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1236 night/inputs/test_only_1236SUBMITLEVEL-1.json night/briefs/KS-1236-SUBMITLEVEL-1.md ctx=65536
```
