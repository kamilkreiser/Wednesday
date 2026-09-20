# KS-1006 MFANOTENABLED-1 PIN THE TWO GUARDS THAT RUN BEFORE THE TICKET'S DEFECT IN POST /me/mfa/disable - a subject WITHOUT MFA is refused 400 'MFA is not enabled' (the exact body), and an enrolled subject whose code is missing, not a string, five or seven characters is refused 400 'Valid 6-digit verification code required' (the exact body) before any TOTP check - the real userRoutes driven in process over the KS-1194 harness - Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, two cells added, no product file** (written 09:50 on 2026-09-21, the #1118 siblings round)

File: `Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`
Tip: `7be81d5c9b109959b559e03652fb092c12de58e8`
Runner: `vitest`

Written from develop `7be81d5c9b109959b559e03652fb092c12de58e8` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 09:30 on 2026-09-21, read verbs only; the #1118 squash-merge, which carried the sibling briefs `KS-1006-WRONGCODE-1` and `KS-1236-SUBMITLEVEL-1` into this file). The test file at that tip is **244 lines** (blob `bfa8b1d3fc36`), read whole; its full content is in `files[...]` of your input. The product the cells pin is `Blockchain/Dev/services/auth/src/routes/users.ts` (blob `3bfa47dcde01`, **1436 lines**, read whole — the SAME blob the sibling briefs measured): `verifyTOTP` at `:1023-1028` (three 30-second 6-DIGIT codes, string-compared), `POST /me/mfa/disable` at `:1094-1122`: the body read `:1096`, the subject read `:1097`, **the enabled guard `    if (!user.mfaEnabled) throw new BadRequestError('MFA is not enabled');` at `:1099`**, **the shape guard `    if (!code || typeof code !== 'string' || code.length !== 6) {` / `      throw new BadRequestError('Valid 6-digit verification code required');` at `:1101-1102`**, the presence-guarded verification at `:1105` (pinned by the sibling's `wrongcode` cell at `:122` of the test file — and the ticket's defect), the disabling write `:1111-1115`, the 200 `{ success: true, message: 'MFA disabled successfully' }` at `:1118`. `BadRequestError` (`middleware/errorHandler.ts:30-33`) is status 400, code `BAD_REQUEST`; the AppError branch at `:290-304` answers exactly `{ success: false, error: { code, message } }`. This service runs **VITEST** (`package.json:11` `"test": "vitest"`, `:48` `vitest ^4.1.9`, no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `routes/users.ts` or any other product file: the behaviour is already what it is at the tip, and these cells PIN it.

## What the cells pin (one paragraph)

KS-1006 quotes the route's shape whole — the enabled guard, the 6-character guard, then the presence-guarded verification — and names the THIRD line as the defect (with `mfaEnabled` true and no secret, any six characters disable the factor). Its fix is to fail closed on the no-secret row; every shape of that fix KEEPS the two guards above it, and the merged `KS-1006-WRONGCODE-1` brief listed them as "right today; separate pins if wanted". These are those pins. Nothing in the auth suite asserts either refusal: `git grep -i -c` over `src/__tests__` at the tip for `MFA is not enabled` → 0 files, for `6-digit verification code` → 0 files (positive control: `me/mfa/disable` → this file, 2 lines, the sibling's cell; `mfaEnabled: true` → 6 files). So either guard could loosen with 782 cells green: the enabled guard turned into an idempotent 200 (a subject with NO factor is told "MFA disabled successfully" — a lie that also hides a mis-targeted call), or the length check dropped (a five- or seven-character string reaches the TOTP compare and comes back as a different refusal — the contract text a client matches on changes, and the shape check no longer states what a code is). This change adds TWO cells to the `describe('KS-1006 - POST /me/mfa/disable verifies the code …', ...)` block, using the file's own `user()`, `state`, `call()` and the exact-body idiom: `mfaoff` — a BASIC user (`mfaEnabled: false`, `user()`'s default) posts a well-formed six-character code and is refused `[400, { success: false, error: { code: 'BAD_REQUEST', message: 'MFA is not enabled' } }]`; `shape` — an enrolled user (`mfaEnabled: true`, the suite's base32 secret) posts FOUR bodies in turn (`{}`, `{ code: 123456 }`, `{ code: '12345' }`, `{ code: '1234567' }`) and every outcome equals `[400, { success: false, error: { code: 'BAD_REQUEST', message: 'Valid 6-digit verification code required' } }]`. Every existing cell is unchanged. **It pins TODAY's two pre-checks and decides nothing about the no-secret row (the defect).**

## The exact change — ONE hunk in the test file

The new cells go at the END of the KS-1006 `describe` block (opened at `:121`), directly below the sibling's `wrongcode` cell (its closer `  });` is `:128`) and directly above the line that closes the describe (`:129`, `});` at column 0 — the ONE trailing context line). THREE leading context lines, `:126-:128`, copied byte for byte (the three together occur exactly once in the file; `:126` and `:127` are each unique). Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` then `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`.**

```
@@ -126,4 +126,22 @@
     const r = await call('POST', '/me/mfa/disable', { code: 'abcdef' });
     expect([r.status, code(r.json), (r.json.error as Row | undefined)?.message]).toEqual([400, 'BAD_REQUEST', 'Invalid verification code']);
   });
+  it('RED KS-1006: with MFA NOT enabled, a well-formed six-character code is refused 400 with the exact body MFA is not enabled - the code is never looked at', async () => {
+    user('u-1006-off');
+    state.caller = { userId: 'u-1006-off', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/mfa/disable', { code: 'abcdef' });
+    expect([r.status, r.json]).toEqual([400, { success: false, error: { code: 'BAD_REQUEST', message: 'MFA is not enabled' } }]);
+  });
+  it('RED KS-1006: with MFA enabled and a secret stored, a code that is missing, not a string, five characters or seven characters is refused 400 with the exact body Valid 6-digit verification code required - before any TOTP check', async () => {
+    user('u-1006-shape');
+    Object.assign(state.users.get('u-1006-shape') as Record<string, unknown>, { mfaEnabled: true, mfaSecret: 'JBSWY3DPEHPK3PXP' });
+    state.caller = { userId: 'u-1006-shape', role: 'USER', tenantId: 'tenant-default' };
+    const outcomes: unknown[] = [];
+    for (const body of [{}, { code: 123456 }, { code: '12345' }, { code: '1234567' }]) {
+      const r = await call('POST', '/me/mfa/disable', body);
+      outcomes.push([r.status, r.json]);
+    }
+    const refused = [400, { success: false, error: { code: 'BAD_REQUEST', message: 'Valid 6-digit verification code required' } }];
+    expect(outcomes).toEqual([refused, refused, refused, refused]);
+  });
 });
```

`describe`, `it`, `expect` and `vi` are already imported by the file at `:15`; `Row` is the file's type at `:20`; `state` (`:21-30`), `user()` (`:109-111`, seeds a BASIC, `mfaEnabled: false` user into `state.users`), `call()` (`:115-118`, a real HTTP call to the file's own loopback server on an ephemeral port — its `body` parameter is `unknown`, so each of the four bodies is passed as is) are the file's own helpers — you add NO import and NO helper. `Object.assign` on the object `user()` stored is what the mocked `getUserById` (`:53`) hands the route — the sibling's idiom at `:124`, reused. `JBSWY3DPEHPK3PXP` is the base32 secret the suite already uses (`:124` here; `ks1052-backup-code-burn-cause-a.test.ts`, `ks737-platform-admin-mfa-bypass.test.ts`); no cell here ever reaches `verifyTOTP` with it. The `beforeEach` at `:130-139` clears `state.users` and every mock before every cell; vitest applies a file-level hook to every test whatever the declaration order (the sibling's cell at `:122` already runs green ahead of it).

## Cells

- `mfaoff` = `RED KS-1006: with MFA NOT enabled, a well-formed six-character code is refused 400 with the exact body MFA is not enabled - the code is never looked at`
- `shape` = `RED KS-1006: with MFA enabled and a secret stored, a code that is missing, not a string, five characters or seven characters is refused 400 with the exact body Valid 6-digit verification code required - before any TOTP check`

## Red cells

The two cells below are GENUINE assertion-reds: each fails under the tamper named for it and passes at the tip. They are declared here rather than with a red glyph in their titles because every `+` line in this diff must be ASCII only.

- RED KS-1006: with MFA NOT enabled, a well-formed six-character code is refused 400 with the exact body MFA is not enabled - the code is never looked at
- RED KS-1006: with MFA enabled and a secret stored, a code that is missing, not a string, five characters or seven characters is refused 400 with the exact body Valid 6-digit verification code required - before any TOTP check

## Tampers

One tamper per guard, both in `routes/users.ts`. **MFAOFFIDEMPOTENT** is a single-line tamper on `:1099` (the enabled guard; it occurs EXACTLY ONCE in the file — whole-line scan, hits `[1099]`; positive control `mfaEnabled` matches 7 lines). **LENGTHDROPPED** is a two-line BLOCK tamper on `:1101-1102`: the guard line `:1101` alone is NOT unique — the same text is the `/me/mfa/verify` route's shape check at `:1062` — so the block that includes the unique message line `:1102` (hits `[1102]`) is the locator; the block occurs exactly once (block scan, starts `[1101]`), and only its first line changes. They are the two shapes a loosening can take: the enabled guard made an idempotent success (a subject without MFA is answered the route's own 200 body, `res.json` as `:1279` and `:1118` already do in this file), or the length check dropped from the shape guard (the `!code` and `typeof` halves stay). Each `From` is the tip's text byte for byte, and each `To` is valid TypeScript, so nothing fails to load and no cell reds for the wrong reason. The checker plants them ONE AT A TIME and restores the file by bytes between them.

### MFAOFFIDEMPOTENT — a subject without MFA is answered 200 MFA disabled successfully instead of the refusal
File: `Blockchain/Dev/services/auth/src/routes/users.ts`
Line: 1099
From:
```
    if (!user.mfaEnabled) throw new BadRequestError('MFA is not enabled');
```
To:
```
    if (!user.mfaEnabled) return res.json({ success: true, message: 'MFA disabled successfully' });
```
Reds: `mfaoff`

### LENGTHDROPPED — the six-character check is dropped from the shape guard; a five- or seven-character string reaches the TOTP compare
File: `Blockchain/Dev/services/auth/src/routes/users.ts`
Line: 1101
From:
```
    if (!code || typeof code !== 'string' || code.length !== 6) {
      throw new BadRequestError('Valid 6-digit verification code required');
```
To:
```
    if (!code || typeof code !== 'string') {
      throw new BadRequestError('Valid 6-digit verification code required');
```
Reds: `shape`

## Controls

- `RED KS-1006: with MFA enabled and a secret stored, a six-character code that cannot be a TOTP is refused 400 Invalid verification code`
- `🟢 control: with no database at all the request is still accepted in memory, as before`
- `🟢 control: a healthy reject answers 200, saves REJECTED and never touches the level`

*(All three are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:122`, `:168` and `:239` before this hunk, `:122`, `:186` and `:257` after it — each occurs exactly once in the file and none is a prefix of any other title. The glyphs are the FILE's, in EXISTING titles that this diff never writes; the new cells' titles are ASCII. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix. The other 11 existing cells (the submit cells at `:142`, `:150`, `:160`; the sibling's two KS-1236 cells at `:175`, `:182`; the review cells at `:194`, `:201`, `:207`, `:214`, `:221`, `:232`) are also green under both tampers — none posts to `/me/mfa/disable` — but are left undeclared. The `:122` control is the sibling's `wrongcode` cell: under MFAOFFIDEMPOTENT its subject IS enabled, so `:1099` falls through as before; under LENGTHDROPPED its `'abcdef'` is six characters, so the dropped check never mattered to it — it proves the verification at `:1105` still refuses beside the new cells. The `:168` and `:239` controls prove the harness (loopback server, mocked repo, mocked db) still runs.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip both new cells pass. `mfaoff`: `user('u-1006-off')` stores a user with `mfaEnabled: false`; `state.caller` makes the route's `req.user.userId` that id; `call()` POSTs `{ code: 'abcdef' }`; `:1097` hands the route the seeded object, **`:1099` is true** (`!false`), `BadRequestError('MFA is not enabled')` is thrown, the file's `errorHandler` answers 400 `{ success: false, error: { code: 'BAD_REQUEST', message: 'MFA is not enabled' } }`; `:1101` and `:1105` are never reached. `shape`: `Object.assign` makes `u-1006-shape` enabled with a secret, so `:1099` passes; each of the four bodies fails `:1101` — `{}` (`code` undefined → `!code`), `{ code: 123456 }` (`typeof` is `'number'`), `{ code: '12345' }` (length 5), `{ code: '1234567' }` (length 7) — and `:1102` throws; each outcome is `[400, { success: false, error: { code: 'BAD_REQUEST', message: 'Valid 6-digit verification code required' } }]`, and `outcomes` equals four copies of `refused`. `:1105` is never reached, so the REAL `verifyTOTP` never runs in either cell. (Measured: see MEASURED.)

Under **MFAOFFIDEMPOTENT** `:1099` answers `mfaoff` with 200 `{ success: true, message: 'MFA disabled successfully' }` — the array reads `[200, { success: true, message: … }]` — assertion red; `shape`'s subject is enabled, unaffected — green (declared so). Under **LENGTHDROPPED** the first two bodies of `shape` are still refused at `:1101` (`!code`, `typeof`), but `'12345'` and `'1234567'` pass the shape guard, reach `:1105`, and the REAL `verifyTOTP` compares three 6-DIGIT strings to them — never equal — so `:1106` throws `BadRequestError('Invalid verification code')`: outcomes 3 and 4 read `[400, { success: false, error: { code: 'BAD_REQUEST', message: 'Invalid verification code' } }]` — the message differs — assertion red on `shape`; `mfaoff` is refused at `:1099` before the shape guard — green (declared so). Under BOTH every existing cell stays green: the only other cell posting to this route is the sibling's `wrongcode` (a control here).

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` lines.** `routes/users.ts` at `7be81d5c9`: `:1099` is `    if (!user.mfaEnabled) throw new BadRequestError('MFA is not enabled');`, whole-line hits `[1099]`; `:1101` is `    if (!code || typeof code !== 'string' || code.length !== 6) {`, whole-line hits `[1062, 1101]` (**not unique** — `:1062` is `/me/mfa/verify`'s shape check, whose message at `:1063` is `Invalid verification code — must be 6 digits`); `:1102` is `      throw new BadRequestError('Valid 6-digit verification code required');`, hits `[1102]`. Hence the two-line block `:1101-1102` as LENGTHDROPPED's From (the builder verifies a block occurs EXACTLY ONCE and starts at `Line:`). Positive controls: `mfaEnabled` 7 lines, `code.length` 2 lines (`:1062`, `:1101`), `BadRequestError` 16 lines. The blob is `3bfa47dcde01` — identical to the blob the sibling briefs measured at `cbae988db`. The checker plants and restores (T8 by sha256 after each; tip blob sha256 `96408a532a73ef77`).
- **Premise: the ticket's claim, re-derived.** KS-1006 (Linear, `In Progress`, read 09:33) quotes the three-guard shape and names the third (`:1105`) as the defect; its Suggested fix is "fail closed" on the no-secret row. The two guards above it are not questioned by the ticket and survive every fix shape. `KS-1006` occurs **0** times under `services/auth/src` (the sibling's test cell carries it in `src/__tests__`).
- **Premise: the anchor.** The test file is **244** lines at this tip (220 at `cbae988db`; #1118 added the KS-1006 describe at `:121-129` and the two KS-1236 cells at `:175-188`). The three leading context lines are `:126` (unique — the only `/me/mfa/disable` call), `:127` (unique — the only `'Invalid verification code'` expect), `:128` `  });` (15 hits); the THREE together occur exactly once (block scan, `[126]`). The trailing context `:129` is `});` at column 0 (7 hits in the file: `:71`, `:78`, `:106`, `:129`, `:139`, `:189`, `:244`) — `git apply` anchors the hunk by its line number and the three unique-together leading lines. The insertion is pure, so no blank line is asked of you anywhere.
- **Premise: the in-process route call.** `beforeAll` (`:95-106`) mounts the REAL `userRoutes` and `errorHandler` on an express app listening on `127.0.0.1:0` (the file's own harness; this brief names no port); `authenticate` is mocked (`:72-78`) to inject `state.caller`; `userRepo.getUserById` (`:53`) returns `state.users.get(id)`; `express.json()` (`:97`) parses each body, so `{}` arrives as an empty object and `123456` as a number.
- **Premise: the body.** `errorHandler.ts:290-304` answers an `AppError` with exactly `{ success: false, error: { code, message } }` (`details` only for `ValidationError`), so `toEqual` on the whole `r.json` is stable and pins the message.
- **Premise: the code shape under LENGTHDROPPED.** `verifyTOTP` (`:1023-1028`) returns true only when `generateTOTP` (`:1011-1021`, six DIGITS zero-padded) equals `code` for one of three time steps; a five- or seven-character string can never be equal — so the tamper's red is deterministic (a DIFFERENT 400 message), not probabilistic.
- **Premise: `+` lines that also occur at the tip.** Two, both added by this brief (so T4 accepts them): `  });` (the cell closer) and `    const r = await call('POST', '/me/mfa/disable', { code: 'abcdef' });` (`:126` — the sibling's call line, reused verbatim). No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick). The titles use `-`, `:` and `/`, no em dash, no glyph.
- **Premise: the runner.** `services/auth/package.json` at the tip has `"test": "vitest"` (`:11`) and `vitest ^4.1.9` (`:48`) in devDependencies, with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it.
- **Premise: no live-lane collision.** `routes/users.ts` is not `api-gateway/src/index.ts`, `preflight.sh`, `enforcement.ts` or under `services/anchoring/**`. The held READYs that name this test file are the two siblings (`READY_KS-1006-WRONGCODE-1`, `READY_KS-1236-SUBMITLEVEL-1`) — BOTH merged into this tip by #1118 (spent). The one un-merged READY naming `routes/users.ts` is `READY_KS-1188-F1b` (a NEW test file, tamper `users.ts:909`) — different lines, different handler. `READY_KS-938` (MFA) modifies `routes/mfa.ts`, not `users.ts`. See Collision.
- **Premise: the surface.** The cells drive one auth route in process with a mocked authenticator, a mocked repo and a mocked db; the REAL `verifyTOTP` is reached only under LENGTHDROPPED, on a throwaway base32 secret. No session, no JWT, no product bytes. MFA / AUTH surface, test-only pin (allowed under Wednesday's reading).

## Collision

**Same test file as this round's sibling brief `KS-1236-ALREADYPENDING-1` — DISJOINT hunks, same product file, DIFFERENT tamper lines.** That brief's hunk is `@@ -172,4 +172,18 @@` (inside the first KS-1194 describe), BELOW this hunk. Both orders apply with `git apply` — measured in MEASURED: **this first, then ALREADYPENDING**: its hunk lands at `:190` (offset +18); **ALREADYPENDING first, then this**: this hunk at its stated line (it sits above the other insertion). The file is byte-identical either way (276 lines, one sha256). **Order for the raise: either; if raised in one PR, put this brief's hunk first (lower line numbers first) and re-derive ALREADYPENDING's header as `@@ -190,4 +190,18 @@`.** Tamper lines: this brief plants `:1099` and the block `:1101-1102`; ALREADYPENDING plants `:1274` — no shared line; each is planted-and-restored, none moves the other. No tamper of either brief reds the other's cells (measured: MEASURED). The two MERGED siblings' READYs also name this file's `+++ b/` — spent holds, in the tip. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21, `--shared` scratch clones at `7be81d5c9`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_siblings-1236-1006-drafter/MFANOTENABLED/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md` = this brief's own hunk with the two file-header lines, fresh `--shared` clone `g_b1` at `7be81d5c9`, farmed by the harness's `prepare_clone.sh`): **RESULT: PASS (8/8)** — T1 one fenced block; T2 touched set == the test file only; T3 strict apply; T4 every `+` line byte-exact; T5 green at the tip **16/16 cells** (14 existing + 2 new, every declared cell present); T6 MFAOFFIDEMPOTENT (planted at `users.ts:1099`) red set == {mfaoff} — received `[ 200, { success: true, message: 'MFA disabled successfully' } ]` vs expected `[ 400, { success: false, error: { code: 'BAD_REQUEST', message: 'MFA is not enabled' } } ]`; LENGTHDROPPED (planted as `block 2 -> 2 lines at users.ts:1101-1102`) red set == {shape} — outcomes 3 and 4 received `message: 'Invalid verification code'` where `'Valid 6-digit verification code required'` was expected (outcomes 1 and 2 unchanged) (`MFANOTENABLED/out.md.checker/tamper_*.cells.json`, `probe_received_*.raw`); every red an assertion failure; T7 all three controls green under both; T8 `users.ts` restored to sha256 `96408a532a73` after each. Source tracked-modified count 0 before and after (`MFANOTENABLED/prepare.out.log`).
- Whole auth suite on the measurement clone `m_auth` (`measure_row.sh`, `MFANOTENABLED/measure.log`, the test file reset to the tip first so the counts are this hunk's alone): bare tip **66 files, 782/782**; with this hunk **784/784** — +2, 0 new red. File alone: 14/14 bare, 16/16 with the hunk (262 lines, sha256 `34d13320a2a19e0f`). Under MFAOFFIDEMPOTENT the WHOLE suite is **783/1 of 784** — `mfaoff` only (no other file posts to `/me/mfa/disable`); under LENGTHDROPPED **783/1 of 784** — `shape` only. Restore by checkout after each: sha256 `96408a532a73ef77` == tip blob, porcelain 0.
- Three wrong variants refused by the same checker on fresh clones (`golden_runs.log`): a `+` line altered → FAIL T4 `MISSING '+'`; a real diff that also deletes the `:239-243` healthy-reject control → FAIL T4 `REMOVED BEYOND THE BRIEF`; both assertions weakened to type/length checks (own input) → T1-T5 pass, then FAIL T6 `reds NOTHING (0 of 16 cells failed)` under BOTH tampers.
- Both apply orders with the sibling `KS-1236-ALREADYPENDING-1` hunk (`collision_orders.sh`, `collision.log`): **this then ALREADYPENDING** — this hunk at its stated line, the other `succeeded at 190 (offset 18 lines)`; **ALREADYPENDING then this** — both at their stated lines; the resulting file is **276 lines, sha256 `852cfa71f994cf5c` in BOTH orders** (`cmp` identical). With BOTH hunks and no tamper: the file **18/18**; the whole auth suite **786/786**. Cross-tampers over the combined file (each planted by bytes and restored to `96408a532a73`): MFAOFFIDEMPOTENT reds exactly {mfaoff}; LENGTHDROPPED exactly {shape}; ALREADYPENDING's GUARDTOLOG and SAMETARGETONLY red exactly its own cells — no tamper of either brief reds the other's cells.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` / `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`, then the hunk above exactly as shown (`@@ -126,4 +126,22 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (MFA / auth surface, test-only pin — allowed). Refs KS-1006** (and KS-732, whose sibling-door proof this route's cells complete). **NEVER Closes** — KS-1006 asks for a PRODUCT change on the no-secret row (fail closed); this brief pins the two pre-checks that every fix shape keeps and leaves the latent no-secret admission as the open defect it is.
- **Not from a gate cell.** Named by the merged `KS-1006-WRONGCODE-1` brief's own NOT-PINNED paragraph and by round 23's next-best list (3).
- **Not pinned here, said plainly:** the no-secret row (`mfaEnabled` true, `mfaSecret` null — a cell asserting today's admission would pin the bug; the #1118 gate's FALSYMFASECRETDOOR row, BY DESIGN); a CORRECT code disabling MFA (the success path, needs a computed TOTP); the `NotFoundError('User')` at `:1098` (a missing subject — a different status, 404); the exact text of `/me/mfa/verify`'s twin shape check at `:1062-1063` (a different route, a different message).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1006 night/inputs/test_only_1006MFANOTENABLED-1.json night/briefs/KS-1006-MFANOTENABLED-1.md ctx=65536
```
