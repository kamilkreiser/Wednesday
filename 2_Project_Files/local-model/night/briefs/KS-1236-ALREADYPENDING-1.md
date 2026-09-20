# KS-1236 ALREADYPENDING-1 PIN THAT POST /me/verification REFUSES A SECOND REQUEST WHILE ONE IS ALREADY PENDING (400 BAD_REQUEST, exact body 'A verification request is already pending', one store read, no INSERT) - for the SAME target and for a DIFFERENT target alike - the pending-request guard the SUBMITLEVEL-1 brief named as "right today, a separate pin if wanted" - the real userRoutes driven in process over the KS-1194 harness - Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, two cells added, no product file** (written 09:35 on 2026-09-21, the #1118 siblings round)

File: `Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`
Tip: `7be81d5c9b109959b559e03652fb092c12de58e8`
Runner: `vitest`

Written from develop `7be81d5c9b109959b559e03652fb092c12de58e8` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 09:30 on 2026-09-21, read verbs only; the #1118 squash-merge, which carried the sibling briefs `KS-1236-SUBMITLEVEL-1` and `KS-1006-WRONGCODE-1` into this file). The test file at that tip is **244 lines** (blob `bfa8b1d3fc36`), read whole; its full content is in `files[...]` of your input. The product the cells pin is `Blockchain/Dev/services/auth/src/routes/users.ts` (blob `3bfa47dcde01`, **1436 lines**, read whole — the SAME blob the sibling briefs measured): `POST /me/verification` at `:1257-1307`, the subject read at `:1260`, the ordering guard at `:1267` (pinned by the sibling's two cells at `:175-:188` of the test file), the pending-request read `    const existingRequest = await findPendingVerificationRequest(user.id);` at `:1273` (the FIRST `dbQuery` of the handler — `findPendingVerificationRequest` at `:1205-1229` runs `SELECT … WHERE user_id = $1 AND status = 'PENDING' LIMIT 1` when the db is available), **the guard `    if (existingRequest) throw new BadRequestError('A verification request is already pending');` at `:1274`** (`middleware/errorHandler.ts:30-33`: status 400, code `BAD_REQUEST`; the AppError branch at `:290-304` answers `{ success: false, error: { code, message } }` and nothing else), the STANDARD auto-approve at `:1276`, and the INSERT through `saveVerificationRequest` at `:1296`. This service runs **VITEST** (`package.json:11` `"test": "vitest"`, `:48` `vitest ^4.1.9`, no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `routes/users.ts` or any other product file: the behaviour is already what it is at the tip, and these cells PIN it.

## What the cells pin (one paragraph)

KS-1236 reports that approving a STALE pending request after the subject's level rose stores the lower level; its fix is on the REVIEW side. The submit side has TWO guards that are right today and that every fix shape keeps: the ordering guard at `:1267` (pinned by `KS-1236-SUBMITLEVEL-1`, merged in #1118) and the pending-request guard at `:1274` — one request in flight per user, whatever its target. The SUBMITLEVEL-1 brief said of `:1274`: "right today, but its one-line loosening reds nothing these cells assert — a separate pin if wanted". This is that pin. Nothing in the auth suite asserts the refusal: `git grep -i 'already pending'` over `src/__tests__` at the tip is ONE line, a COMMENT in `ks467-user-admin-isolation.test.ts:174` ("the "request already pending" guard tripping on a prior test's request" — the file gives each review test its own user to AVOID the guard); `ks1018-…store-reads.test.ts` drives the pending READ's failure modes, never a hit. So the guard could loosen two ways with 782 cells green: reduced to a log line (a second, third, fourth PENDING row per user — the review side then approves whichever is stale, the very hole KS-1236 describes, widened), or narrowed to "a duplicate of the same target" (a pending ENHANCED plus a pending HIGH for one user). This change adds TWO cells to the `describe('KS-1194 — POST /me/verification never acknowledges a request that did not persist', ...)` block, using the file's own `user()`, `pendingRow()`, `state`, `call()` and `dbQuery`: a BASIC subject with a PENDING BASIC→ENHANCED row already in the db mock posts `{ targetLevel: 'ENHANCED' }` (cell 1, the duplicate) or `{ targetLevel: 'HIGH' }` (cell 2, a different target); each asserts `[status, whole body, rows.size, dbQuery calls]` equals `[400, { success: false, error: { code: 'BAD_REQUEST', message: 'A verification request is already pending' } }, 1, 1]` — refused at `:1274` after exactly ONE store read (the pending SELECT) and before any INSERT (the seeded row is still the only row). Every existing cell is unchanged. **It pins TODAY's pending-request guard and decides nothing about KS-1236's review-side fix.**

## The exact change — ONE hunk in the test file

The new cells go inside the first `describe` block (opened at `:141`), directly below the `🟢 control: with no database at all …` cell (its closer `  });` is `:174`) and directly above the sibling's first cell `  it('RED KS-1236: a target level EQUAL to the current level …` at `:175` (the ONE trailing context line — it occurs exactly once in the file). THREE leading context lines, `:172-:174`, copied byte for byte (the three together occur exactly once in the file; `:173` alone is unique). Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` then `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`.**

```
@@ -172,4 +172,18 @@
     const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
     expect([r.status, (r.json.data as Row | undefined)?.status, dbQuery.mock.calls.length]).toEqual([200, 'PENDING', 0]);
   });
+  it('RED KS-1236: a second request while one is already PENDING is refused 400 with the exact body A verification request is already pending - one store read, no INSERT', async () => {
+    user('u-1236-pend');
+    pendingRow('vr-1236-pend', 'u-1236-pend');
+    state.caller = { userId: 'u-1236-pend', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
+    expect([r.status, r.json, state.rows.size, dbQuery.mock.calls.length]).toEqual([400, { success: false, error: { code: 'BAD_REQUEST', message: 'A verification request is already pending' } }, 1, 1]);
+  });
+  it('RED KS-1236: a request for a DIFFERENT target while one is already PENDING is refused the same way - the guard is on any pending request, not on a duplicate target', async () => {
+    user('u-1236-pend2');
+    pendingRow('vr-1236-pend2', 'u-1236-pend2');
+    state.caller = { userId: 'u-1236-pend2', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/verification', { targetLevel: 'HIGH' });
+    expect([r.status, r.json, state.rows.size, dbQuery.mock.calls.length]).toEqual([400, { success: false, error: { code: 'BAD_REQUEST', message: 'A verification request is already pending' } }, 1, 1]);
+  });
   it('RED KS-1236: a target level EQUAL to the current level is refused 400 BAD_REQUEST before any store read or INSERT', async () => {
```

`describe`, `it`, `expect` and `vi` are already imported by the file at `:15`; `Row` is the file's type at `:20`; `state` (`:21-30`, a `vi.hoisted` object holding `users`, `rows`, `caller`), `dbQuery` (`:34-49`, the hoisted mock the `../db` module returns — its `status = 'PENDING'` branch at `:43-46` answers the pending SELECT from `state.rows`), `user()` (`:109-111`, seeds a `BASIC` user into `state.users`), `pendingRow()` (`:112-114`, seeds a PENDING BASIC→ENHANCED row into `state.rows` — the SAME helper the review cells use at `:195`, `:202`, …), `call()` (`:115-118`, a real HTTP call to the file's own loopback server on an ephemeral port) are the file's own helpers — you add NO import and NO helper. The `beforeEach` at `:130-139` clears `state.users`, `state.rows` and every mock before every cell, so the seeding is local to each cell.

## Cells

- `duplicate` = `RED KS-1236: a second request while one is already PENDING is refused 400 with the exact body A verification request is already pending - one store read, no INSERT`
- `othertarget` = `RED KS-1236: a request for a DIFFERENT target while one is already PENDING is refused the same way - the guard is on any pending request, not on a duplicate target`

## Red cells

The two cells below are GENUINE assertion-reds: each fails under the tamper(s) named for it and passes at the tip. They are declared here rather than with a red glyph in their titles because every `+` line in this diff must be ASCII only.

- RED KS-1236: a second request while one is already PENDING is refused 400 with the exact body A verification request is already pending - one store read, no INSERT
- RED KS-1236: a request for a DIFFERENT target while one is already PENDING is refused the same way - the guard is on any pending request, not on a duplicate target

## Tampers

Two single-line tampers on the SAME line of `routes/users.ts` (`:1274`, the pending-request guard; it occurs EXACTLY ONCE in the file — whole-line scan, hits `[1274]`; positive control `findPendingVerificationRequest` matches 3 lines: `:1205`, `:1222`, `:1273`). They are the two shapes a loosening can take: the guard reduced to a LOG line (a second PENDING row is admitted, saved and acknowledged 200), or the guard NARROWED to a same-target duplicate (`existingRequest && existingRequest.targetLevel === data.targetLevel` — a pending ENHANCED no longer blocks a request for HIGH). Each `From` is the tip's line at that number, byte for byte, and each `To` is valid TypeScript (`logger` is imported at `users.ts:18` and mocked by the test at `:86` with `warn: vi.fn()`; `existingRequest` is narrowed to `VerificationRequest` by the `&&`, and `targetLevel` is a field of that interface (`:1134-1145`) at `:1138`), so nothing fails to load and no cell reds for the wrong reason. The checker plants them ONE AT A TIME and restores the file by bytes between them.

### GUARDTOLOG — the refusal becomes a warning; a second PENDING row is saved and acknowledged
File: `Blockchain/Dev/services/auth/src/routes/users.ts`
Line: 1274
From:
```
    if (existingRequest) throw new BadRequestError('A verification request is already pending');
```
To:
```
    if (existingRequest) logger.warn('A verification request is already pending', { userId: user.id });
```
Reds: `duplicate`, `othertarget`

### SAMETARGETONLY — only a duplicate of the SAME target is refused; a pending ENHANCED no longer blocks a request for HIGH
File: `Blockchain/Dev/services/auth/src/routes/users.ts`
Line: 1274
From:
```
    if (existingRequest) throw new BadRequestError('A verification request is already pending');
```
To:
```
    if (existingRequest && existingRequest.targetLevel === data.targetLevel) throw new BadRequestError('A verification request is already pending');
```
Reds: `othertarget`

## Controls

- `🟢 control: with no database at all the request is still accepted in memory, as before`
- `RED KS-1236: a target level EQUAL to the current level is refused 400 BAD_REQUEST before any store read or INSERT`
- `🟢 control: a healthy reject answers 200, saves REJECTED and never touches the level`

*(All three are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:168`, `:175` and `:239` before this hunk, `:168`, `:189` and `:253` after it — each occurs exactly once in the file and none is a prefix of any other title. The first glyph title is the FILE's, in an EXISTING title that this diff never writes; the new cells' titles are ASCII. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix. The other 11 existing cells (the KS-1006 cell at `:122`; the submit cells at `:142`, `:150`, `:160`; the sibling's `BELOW` cell at `:182`; the review cells at `:194`, `:201`, `:207`, `:214`, `:221`, `:232`) are also green under both tampers — no existing submit cell has a PENDING row for its user when it posts (the retry cell at `:150` posts twice, but its first INSERT was refused, so no row exists for the second post; `ks467` and `ks1018` are other files), and the review cells never enter this handler — but are left undeclared. The `:168` control proves a submit with NO pending row still passes `:1274` beside the new cells (under GUARDTOLOG the log line is never reached for it; under SAMETARGETONLY `existingRequest` is null); the `:175` control proves the sibling's ordering guard still fires; the `:239` control proves the review route — where KS-1236's defect actually lives, and which these cells never drive — still runs.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip both new cells pass: `user('u-1236-pend')` stores a BASIC user; `pendingRow('vr-1236-pend', 'u-1236-pend')` puts ONE row `{ user_id: 'u-1236-pend', target_level: 'ENHANCED', status: 'PENDING', … }` into `state.rows` (size 1); `state.caller` makes the route's `req.user.userId` that id; `call()` POSTs `{ targetLevel: 'ENHANCED' }` to the real `userRoutes` on the file's loopback server; `:1259` parses the body, `:1260` asks the mocked repo for the user (BASIC), `:1263-1265` compute `currentIndex` 0 and `targetIndex` 2, `:1267` is false (2 <= 0), `:1273` calls `findPendingVerificationRequest` — `isDbAvailable()` is true, so `dbQuery` runs the `status = 'PENDING'` SELECT (**call 1**), the mock at `:43-46` filters `state.rows` by `user_id` and PENDING and returns the seeded row, `:1212-1219` maps it to a `VerificationRequest` — **`:1274` is true**, `BadRequestError` is thrown, the file's `errorHandler` answers 400 `{ success: false, error: { code: 'BAD_REQUEST', message: 'A verification request is already pending' } }`; nothing reached `:1296`, so `dbQuery` was called exactly once and `state.rows` still holds exactly the seeded row. The asserted array is `[400, <that body>, 1, 1]`. The `othertarget` cell is the same with `targetLevel: 'HIGH'` (`targetIndex` 3, still above 0; the pending row's target does not enter `:1274` at the tip). (Measured: see MEASURED.)

Under **GUARDTOLOG** `:1274` logs and falls through for BOTH cells: `:1276` is false (neither target is STANDARD), `:1286-1296` build a second request and `saveVerificationRequest` runs the INSERT (`dbQuery` **call 2**, the mock records it into `state.rows` — size 2) and the route answers 200 `{ success: true, message: 'Verification request submitted for review', data: { … status: 'PENDING' } }` — each array reads `[200, <that body>, 2, 2]` — assertion red on both. Under **SAMETARGETONLY** `:1274` reads `existingRequest && 'ENHANCED' === 'ENHANCED'` for `duplicate` — true, still 400, green (declared so) — and `existingRequest && 'ENHANCED' === 'HIGH'` for `othertarget` — false, the same fall-through to the INSERT and the 200: `[200, <body>, 2, 2]` — assertion red. Under BOTH tampers every existing cell stays green (no existing submit cell has a pending row for its user; the review cells never enter this handler).

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` line.** `routes/users.ts` at `7be81d5c9`, line 1274 is `    if (existingRequest) throw new BadRequestError('A verification request is already pending');` (4-space indent), byte for byte; it occurs **exactly once** in the file (whole-line scan, `[1274]`); the positive control `findPendingVerificationRequest` matches 3 lines, `BadRequestError` 16 lines. The blob is `3bfa47dcde01` — identical to the blob the sibling briefs measured at `cbae988db`, so `git blame` and the neighbouring line numbers in `KS-1236-SUBMITLEVEL-1` hold. The checker plants and restores it (T8 by sha256 after each; tip blob sha256 `96408a532a73ef77`).
- **Premise: the ticket's claim, re-derived.** KS-1236 (Linear, `In Progress`, read 09:33): "Submit refuses a target at or below the current level, but review re-checks nothing"; its Recommendation is entirely review-side. The `:1274` guard is not mentioned by the ticket at all — it is the OTHER submit-side guard that a review-side fix leaves alone. `KS-1236` occurs **0** times under `services/auth/src` (the sibling's test cells carry it in `src/__tests__`).
- **Premise: the anchor.** The test file is **244** lines at this tip (220 at `cbae988db`; #1118 added the KS-1006 describe at `:121-129` and the two KS-1236 cells at `:175-188`). The three leading context lines are `:172` (the `call(...ENHANCED...)` idiom — 6 hits in the file), `:173` (**unique** — the only `expect` with `dbQuery.mock.calls.length]).toEqual([200, 'PENDING', 0]`), `:174` `  });` (15 hits); the THREE together occur exactly once (block scan, `[172]`). The trailing context `:175` is unique (`[175]`). The insertion is pure, so no blank line is asked of you anywhere.
- **Premise: the in-process route call.** `beforeAll` (`:95-106`) mounts the REAL `userRoutes` and `errorHandler` on an express app listening on `127.0.0.1:0` (an ephemeral port chosen by the OS — the file's own harness; nothing in this brief names a port); `call()` fetches it and returns `{ status, json }`. `authenticate` is mocked (`:72-78`) to inject `state.caller` as `req.user`; `userRepo.getUserById` (`:53`) returns `state.users.get(id)`; `../db` (`:79`) is `{ isDbAvailable: () => state.dbAvailable, query: dbQuery }` with `dbAvailable` reset to true by `beforeEach` (`:136`), so the pending read takes the db path (`:1206-1220`), never the module-level memory map at `:1226`.
- **Premise: the pending SELECT is answered by the mock.** `dbQuery` at `:43-46`: `if (sql.includes("status = 'PENDING'"))` returns `state.rows` filtered by `r.user_id === params[0] && r.status === 'PENDING'`, `.slice(0, 1)`; the product SQL at `:1209` contains `status = 'PENDING'` and passes `[userId]`. `pendingRow()` writes `user_id`, `target_level: 'ENHANCED'`, `status: 'PENDING'` — the columns `:1212-1219` read.
- **Premise: the body.** `errorHandler.ts:290-304` answers an `AppError` with exactly `{ success: false, error: { code, message } }` (`details` only for `ValidationError`), so `toEqual` on the whole `r.json` is stable and pins the message.
- **Premise: `+` lines that also occur at the tip.** Two, both added by this brief (so T4 accepts them): `  });` (the cell closer, unavoidable) and `    const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });` (`:146`, `:156`, `:164`, `:172`, `:179`, `:186` — the file's own call idiom, reused verbatim). No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick). The titles use `-`, `:` and `_`, no em dash, no glyph.
- **Premise: the runner.** `services/auth/package.json` at the tip has `"test": "vitest"` (`:11`) and `vitest ^4.1.9` (`:48`) in devDependencies, with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it.
- **Premise: no live-lane collision.** `routes/users.ts` is not `api-gateway/src/index.ts`, `preflight.sh`, `enforcement.ts` or under `services/anchoring/**`. The held READYs that name this test file are the two siblings (`READY_KS-1236-SUBMITLEVEL-1`, `READY_KS-1006-WRONGCODE-1`) — BOTH merged into this tip by #1118 (spent). The one un-merged READY naming `routes/users.ts` is `READY_KS-1188-F1b` (a NEW test file, tamper `users.ts:909`) — different line, different handler. See Collision.
- **Premise: the surface.** The cells drive one auth route in process with a mocked authenticator, a mocked repo and a mocked db. No session, no MFA state, no JWT, no product bytes. AUTH surface, test-only pin (allowed under Wednesday's reading).

## Collision

**Same test file as this round's sibling brief `KS-1006-MFANOTENABLED-1` — DISJOINT hunks, same product file, DIFFERENT tamper lines.** That brief's hunk is `@@ -126,4 +126,22 @@` (inside the KS-1006 describe, trailing context `:129` `});`), ABOVE this hunk. Both orders apply with `git apply` — measured in MEASURED: **MFANOTENABLED first, then this**: this hunk lands at `:190` (offset +18, the `:172-:175` context found eighteen lines down); **this first, then MFANOTENABLED**: its hunk at its stated line. The file is byte-identical either way (276 lines, one sha256). **Order for the raise: either; if raised in one PR, put MFANOTENABLED's hunk first (lower line numbers first) and re-derive this header as `@@ -190,4 +190,18 @@`.** Tamper lines: this brief plants `:1274`; MFANOTENABLED plants `:1099` and the block `:1101-1102` — no shared line; each is planted-and-restored, none moves the other. No tamper of either brief reds the other's cells (measured: MEASURED). The two MERGED siblings' READYs (`READY_KS-1236-SUBMITLEVEL-1`, `READY_KS-1006-WRONGCODE-1`) also name this file's `+++ b/` — spent holds, in the tip. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21, `--shared` scratch clones at `7be81d5c9`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_siblings-1236-1006-drafter/ALREADYPENDING/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md` = this brief's own hunk with the two file-header lines, fresh `--shared` clone `g_a1` at `7be81d5c9`, farmed by the harness's `prepare_clone.sh`): **RESULT: PASS (8/8)** — T1 one fenced block; T2 touched set == the test file only; T3 strict apply; T4 every `+` line byte-exact; T5 green at the tip **16/16 cells** (14 existing + 2 new, every declared cell present); T6 GUARDTOLOG red set == {duplicate, othertarget} and SAMETARGETONLY red set == {othertarget}, every red an assertion failure — received `[ 200, { success: true, message: 'Verification request submitted for review', data: { currentLevel: 'BASIC', requestId: 'vr-…', status: 'PENDING', targetLevel: … } }, 2, 2 ]` vs expected `[ 400, { success: false, error: { code: 'BAD_REQUEST', message: 'A verification request is already pending' } }, 1, 1 ]` (`ALREADYPENDING/out.md.checker/tamper_*.cells.json`, `probe_received_GUARDTOLOG.raw`): a second PENDING row saved and acknowledged; T7 all three controls green under both; T8 `users.ts` restored to sha256 `96408a532a73` after each. Source tracked-modified count 0 before and after (`ALREADYPENDING/prepare.out.log`).
- Whole auth suite on the measurement clone `m_auth` (`measure_row.sh`, `ALREADYPENDING/measure.log`): bare tip **66 files, 782/782** (`whole_bare_tip.json`); with this hunk **784/784** (`whole_applied.json`) — +2, 0 new red. File alone: 14/14 bare, 16/16 with the hunk (258 lines, sha256 `6de258ea25382fec`). Under GUARDTOLOG the WHOLE suite is **782/2 of 784** — the two reds are these two cells and nothing else (no other file asserts the guard); under SAMETARGETONLY **783/1 of 784** — `othertarget` only. Restore by checkout after each: sha256 `96408a532a73ef77` == tip blob, porcelain 0.
- Three wrong variants refused by the same checker on fresh clones (`golden_runs.log`): a `+` line altered → FAIL T4 `MISSING '+'`; a real diff that also deletes the `:168-174` nodb control → FAIL T4 `REMOVED BEYOND THE BRIEF`; both assertions weakened to shape-only checks (own input) → T1-T5 pass, then FAIL T6 `reds NOTHING (0 of 16 cells failed)` under BOTH tampers.
- Both apply orders with the sibling `KS-1006-MFANOTENABLED-1` hunk (`collision_orders.sh`, `collision.log`): **ALREADYPENDING then MFANOTENABLED** — both `Applied … cleanly` at their stated lines; **MFANOTENABLED then ALREADYPENDING** — this hunk `succeeded at 190 (offset 18 lines)`; the resulting file is **276 lines, sha256 `852cfa71f994cf5c` in BOTH orders** (`both_order1.test.ts` == `both_order2.test.ts`, `cmp` identical). With BOTH hunks and no tamper: the file **18/18** (`both_file.json`); the whole auth suite **786/786** (`whole_both.json`). Cross-tampers over the combined file (`cross_*.json`, each planted by bytes and restored to `96408a532a73`): GUARDTOLOG reds exactly {duplicate, othertarget}; SAMETARGETONLY exactly {othertarget}; MFANOTENABLED's MFAOFFIDEMPOTENT and LENGTHDROPPED red exactly its own one cell each — no tamper of either brief reds the other's cells.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` / `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`, then the hunk above exactly as shown (`@@ -172,4 +172,18 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (auth surface, test-only pin — allowed). Refs KS-1236** (and KS-1194, whose harness and file this rides). **NEVER Closes** — KS-1236 asks for a REVIEW-side change; this brief pins the second SUBMIT-side guard that every fix shape keeps, and leaves the review-side downgrade as the open defect it is.
- **Not from a gate cell.** Named by the merged `KS-1236-SUBMITLEVEL-1` brief's own NOT-PINNED paragraph and by round 23's next-best list (2).
- **Not pinned here, said plainly:** the review route's approve of a stale request (the defect); the memory-path pending read at `:1226-1228` (with `dbAvailable` false — the `:168` control takes that path with no pending row; a memory-path duplicate would need the module-level map seeded through a prior 200, a cross-cell dependency this file avoids on purpose); the STANDARD auto-approve at `:1276-1284` (it sits BELOW `:1274`, so a pending row blocks it too, but no cell here requests STANDARD).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1236 night/inputs/test_only_1236ALREADYPENDING-1.json night/briefs/KS-1236-ALREADYPENDING-1.md ctx=65536
```
