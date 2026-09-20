# KS-1006 WRONGCODE-1 PIN THAT POST /me/mfa/disable, WITH A SECRET STORED AND MFA ENABLED, REFUSES A CODE THAT CANNOT BE A TOTP (400 'Invalid verification code', the factor stays enforced) — the verifying half of the presence-guarded check that the ticket says is RIGHT today and that every fail-closed fix keeps — the real userRoutes driven in process over the KS-1194 harness — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, TWO hunks (one mock line + one describe), one cell added, no product file** (written 03:02 on 2026-09-21, board widening round 23)

File: `Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`
Tip: `cbae988dbe90ebe556459ada2cb437eaf80e2402`
Runner: `vitest`

Written from develop `cbae988dbe90ebe556459ada2cb437eaf80e2402` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at the stamp above, read verbs only; the #1105 squash-merge). The test file at that tip is **220 lines**, read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/auth/src/routes/users.ts` (blob `3bfa47dcde01`, **1436 lines**, read whole): `verifyTOTP` at `:1023-1028` (a window of three 30-second 6-DIGIT codes, string-compared), `POST /me/mfa/disable` at `:1094-1122`, the enabled check at `:1099`, the 6-character shape check at `:1101-1103`, **the presence-guarded verification `    if (user.mfaSecret && !verifyTOTP(user.mfaSecret, code)) {` at `:1105`** (throws `BadRequestError('Invalid verification code')` — `middleware/errorHandler.ts:30-33`, status 400, code `BAD_REQUEST`), and the disabling write `userRepo.updateUserOrThrow(...)` at `:1111-1115` followed by `{ success: true, message: 'MFA disabled successfully' }` at `:1118`. This service runs **VITEST** (`package.json` `"test": "vitest"`, `vitest ^4.1.9`, no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above), in TWO hunks. You never touch `routes/users.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1006 (Peter, PR #872 note 4): the inline `POST /api/users/me/mfa/disable` "skips verification when `mfaSecret` is falsy — guarded on presence rather than on proof", a latent shape (a row with `mfa_enabled` true and no secret is not produced by enrolment). Its suggested fix is to FAIL CLOSED on the no-secret row (refuse, or require a backup code) and align with the `/api/auth/mfa/disable` handler — every shape of which KEEPS the half that is right today: with a secret stored, a code that does not verify is refused and the factor stays enforced. Nothing in the auth suite drives this route: `git grep -i 'me/mfa' src/__tests__` at the tip is 0 lines, and `Invalid verification code` is asserted only for the dedicated `/api/auth/mfa/*` flow (`ks732-mfa-disable-proof.test.ts`, a different router). So the verifying half could silently invert or vanish (the wrong code admitted, MFA disabled on any six characters plus a bearer — the very outcome the ticket's latent row would give, made live for EVERY enrolled user) with 779 cells green. This change (hunk A) gives the file's `userRepo` mock the one method the route's success path calls, `updateUserOrThrow` (so a loosening ends in the route's REAL 200, not in a mock gap), and (hunk B) adds a `describe` with ONE cell: an enrolled user (`mfaEnabled: true`, a base32 secret) posts `{ code: 'abcdef' }` — six characters, so the shape check at `:1101` passes, and letters, so no TOTP window can ever equal it (deterministic; a wrong 6-digit code would collide with probability 3 in a million) — and the cell asserts `[status, code, message]` equals `[400, 'BAD_REQUEST', 'Invalid verification code']`. Every existing cell is unchanged. **It pins TODAY's refusal of a non-verifying code when a secret is present and decides nothing about the no-secret row (the defect).**

## The exact change — TWO hunks in the test file

Hunk A adds ONE line to the hoisted `userRepo` mock, directly below `    updateUser: vi.fn(async () => null),` (`:55`) and above `    updateUserPlatformScope: vi.fn(async (id: string) => {` (`:56`, the ONE trailing context line, occurs exactly once). Hunk B adds a `describe` block directly above the file-level `beforeEach(() => {` (`:120`, the ONE trailing context line, occurs exactly once) — vitest applies a file-level hook to every test in the file whatever the declaration order, so the new cell gets the same `beforeEach` reset as the others. Neither hunk has leading context. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in either fence. Keep both headers exactly as shown. **Your diff MUST begin with the two file-header lines, above the first `@@` line: `--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` then `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`; the two hunks follow in this order, A then B.**

```
@@ -56,1 +56,2 @@
+    updateUserOrThrow: vi.fn(async () => null),
     updateUserPlatformScope: vi.fn(async (id: string) => {
```

```
@@ -120,1 +121,10 @@
+describe('KS-1006 - POST /me/mfa/disable verifies the code against a stored secret before disabling the factor', () => {
+  it('RED KS-1006: with MFA enabled and a secret stored, a six-character code that cannot be a TOTP is refused 400 Invalid verification code', async () => {
+    user('u-1006-wrong');
+    Object.assign(state.users.get('u-1006-wrong') as Record<string, unknown>, { mfaEnabled: true, mfaSecret: 'JBSWY3DPEHPK3PXP' });
+    state.caller = { userId: 'u-1006-wrong', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/mfa/disable', { code: 'abcdef' });
+    expect([r.status, code(r.json), (r.json.error as Row | undefined)?.message]).toEqual([400, 'BAD_REQUEST', 'Invalid verification code']);
+  });
+});
 beforeEach(() => {
```

`describe`, `it`, `expect` and `vi` are already imported at `:15`; `Row` is the file's type at `:20`; `state` (`:21-30`), `user()` (`:108-110`, seeds a BASIC, `mfaEnabled: false` user into `state.users`), `call()` (`:114-117`, a real HTTP call to the file's own loopback server on an ephemeral port) and `code()` (`:118`) are the file's own helpers — you add NO import and NO helper beyond the one mock line. `Object.assign` on the object `user()` stored is what the mocked `getUserById` (`:53`) hands the route. `JBSWY3DPEHPK3PXP` is the base32 secret the suite already uses elsewhere (`ks1052-backup-code-burn-cause-a.test.ts:104`, `ks737-platform-admin-mfa-bypass.test.ts:45`); the REAL `verifyTOTP` runs on it. The mock line is inert at the tip: no existing cell reaches `updateUserOrThrow`.

## Cells

- `wrongcode` = `RED KS-1006: with MFA enabled and a secret stored, a six-character code that cannot be a TOTP is refused 400 Invalid verification code`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1006: with MFA enabled and a secret stored, a six-character code that cannot be a TOTP is refused 400 Invalid verification code

## Tampers

Two single-line tampers on the SAME line of `routes/users.ts` (`:1105`, the presence-guarded verification; it occurs EXACTLY ONCE in the file — counted with `grep -c -F -x`, 1; positive control `grep -c -i verifyTOTP` over the same file is 3: `:1023` the definition, `:1069` the enable route's call, `:1105`). They are the two shapes a loosening can take: the verdict INVERTED (`!verifyTOTP` becomes `verifyTOTP` — a wrong code passes, a right one is refused), or the presence guard INVERTED (`user.mfaSecret &&` becomes `!user.mfaSecret &&` — verification runs only when there is NO secret, so an enrolled user is never verified: the ticket's latent hole opened for everyone). Each `From` is the tip's line at that number, byte for byte, and each `To` is valid TypeScript, so nothing fails to load and no cell reds for the wrong reason. The checker plants them ONE AT A TIME and restores the file by bytes between them.

### VERIFYINVERTED — a code that does NOT verify is the one admitted
File: `Blockchain/Dev/services/auth/src/routes/users.ts`
Line: 1105
From:
```
    if (user.mfaSecret && !verifyTOTP(user.mfaSecret, code)) {
```
To:
```
    if (user.mfaSecret && verifyTOTP(user.mfaSecret, code)) {
```
Reds: `wrongcode`

### PRESENCEINVERTED — an enrolled user with a secret is never verified at all
File: `Blockchain/Dev/services/auth/src/routes/users.ts`
Line: 1105
From:
```
    if (user.mfaSecret && !verifyTOTP(user.mfaSecret, code)) {
```
To:
```
    if (!user.mfaSecret && !verifyTOTP(user.mfaSecret, code)) {
```
Reds: `wrongcode`

## Controls

- `🟢 control: with no database at all the request is still accepted in memory, as before`
- `🟢 control: a healthy reject answers 200, saves REJECTED and never touches the level`
- `🔴 approve: the row is saved APPROVED BEFORE the level is raised`

*(All three are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:158`, `:215` and `:177` before these hunks, `:168`, `:225` and `:187` after them — each occurs exactly once in the file and none is a prefix of any other title. The glyphs are the FILE's, in EXISTING titles that this diff never writes; the new cell's title is ASCII. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix. The other 8 existing cells are also green under both tampers — none of them posts to `/me/mfa/disable`, so `:1105` is never reached by them — but are left undeclared. The three controls prove the harness (loopback server, mocked repo, mocked db) still runs beside the new mock line and the new describe.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: `user('u-1006-wrong')` stores a BASIC user, `Object.assign` makes it `mfaEnabled: true` with the base32 secret, `state.caller` makes the route's `req.user.userId` that id; `call()` POSTs `{ code: 'abcdef' }` to the real `userRoutes`; `:1097` asks the mocked repo for the user (the seeded object), `:1099` passes (enabled), `:1101` passes (`'abcdef'` is a 6-character string), **`:1105` is true** (a secret is present and `verifyTOTP` compares three 6-DIGIT strings to `'abcdef'`, all unequal, so it returns false), `:1106` throws `BadRequestError('Invalid verification code')`, the file's `errorHandler` answers 400 `{ error: { code: 'BAD_REQUEST', message: 'Invalid verification code' } }`; `:1111` is never reached. The asserted array is `[400, 'BAD_REQUEST', 'Invalid verification code']`. (Measured: see MEASURED.)

Under **VERIFYINVERTED** `:1105` reads `secret && false` — false — so the handler goes on to `:1111`, calls the mock's `updateUserOrThrow` (hunk A; resolves null, the route does not read the answer), logs, and answers 200 `{ success: true, message: 'MFA disabled successfully' }`: the array reads `[200, undefined, undefined]` — assertion red. Under **PRESENCEINVERTED** `:1105` reads `!secret && ...` — false because a secret IS present — the same 200: `[200, undefined, undefined]` — assertion red. Under BOTH every existing cell stays green: none posts to this route.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` line.** `routes/users.ts` at `cbae988db`, line 1105 is `    if (user.mfaSecret && !verifyTOTP(user.mfaSecret, code)) {` (4-space indent), byte for byte; it occurs **exactly once** in the file (`grep -c -F -x`, 1); the positive control `verifyTOTP` (case-insensitive) matches 3 lines. `git blame` at the tip: `:1105` last touched by `e50dbde98` (2026-02-18); the file's last change is `f6669623c` (KS-1194). The checker plants and restores it (T8 by sha256 after each; tip blob sha256 `96408a532a73ef77`).
- **Premise: the ticket's claim, re-derived.** KS-1006 quotes the shape at `users.ts:1064` (its base); at this tip the route is `:1094` and the line `:1105`, byte-identical to the ticket's quote. KS-732 (#872, `a45204ac9`, in this tip) changed the SIBLING door `/api/auth/mfa/disable` (`routes/mfa.ts`), not this route. `KS-1006` occurs **0** times under `services/auth/src`. The held `READY_KS-938` (MFA) modifies `routes/mfa.ts` `:238` / `:373`, not `users.ts`.
- **Premise: the anchors.** The test file is **220** lines. Hunk A's trailing context `:56` `    updateUserPlatformScope: vi.fn(async (id: string) => {` occurs exactly once; `:55` `    updateUser: vi.fn(async () => null),` (not written) is directly above it, and `updateUserOrThrow` occurs 0 times at the tip. Hunk B's trailing context `:120` `beforeEach(() => {` occurs exactly once; `:119` (blank) is not written. Both insertions are pure; no blank line is asked of you anywhere. After hunk A, every later line is +1: hunk B's header therefore reads `+121` on the new side (`@@ -120,1 +121,10 @@`).
- **Premise: the in-process route call.** `beforeAll` (`:94-105`) mounts the REAL `userRoutes` and `errorHandler` on an express app listening on `127.0.0.1:0` (the file's own harness; this brief names no port); `authenticate` is mocked (`:71-77`) to inject `state.caller`; `userRepo.getUserById` (`:53`) returns `state.users.get(id)`. `beforeEach` (`:120-129`) clears `state.users` and every mock before every cell — file-level hooks apply to every test in the file regardless of where the `describe` sits (measured below: the cell runs green with the hook declared after it).
- **Premise: the code shape.** `verifyTOTP` (`:1023-1028`) returns true only when `generateTOTP` (`:1011-1021`, six DIGITS zero-padded) equals `code` for one of three time steps; `'abcdef'` contains letters, so it can never be equal — the refusal is deterministic, not probabilistic.
- **Premise: `+` lines that also occur at the tip.** Two, both added by this brief (so T4 accepts them): `  });` and `});` (closers). No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick). The titles use `-`, `:` and `/`, no em dash, no glyph.
- **Premise: the runner.** `services/auth/package.json` at the tip has `"test": "vitest"` and `vitest ^4.1.9` in devDependencies, with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it.
- **Premise: no live-lane collision.** `routes/users.ts` is not `api-gateway/src/index.ts`, `preflight.sh`, `enforcement.ts` or under `services/anchoring/**`; the test file is none of Seat B 11th's six. The ONE brief that names this test file is this round's sibling `KS-1236-SUBMITLEVEL-1.md` (see Collision); no held `READY_*` names it (0). The held READYs that name `routes/users.ts` are KS-1050 and KS-1018 (merged into this tip — spent), KS-692 and KS-938 (mentions), and KS-1188-F1b (a NEW test file, tamper `users.ts:909`, unmerged): none modifies `users.ts` and none plants `:1105`.
- **Premise: the surface.** The cell drives one auth route in process with a mocked authenticator, a mocked repo and a mocked db; the REAL TOTP verifier runs on a throwaway base32 secret. No session, no JWT, no product bytes. MFA / AUTH surface, test-only pin (allowed under Wednesday's reading).

## Collision

**Same test file as this round's sibling brief `KS-1236-SUBMITLEVEL-1` (queued or not yet — check `night/READY_*`) — DISJOINT hunks, same product file, DIFFERENT tamper lines.** KS-1236's hunk is `@@ -165,1 +165,15 @@` (inside the first `describe`, trailing context `:165` `});`); this brief's hunks are `@@ -56,1 +56,2 @@` and `@@ -120,1 +121,10 @@` (above the file-level `beforeEach`). Both orders apply with `git apply` — measured below: **this first, then KS-1236** applies KS-1236's hunk at `:175` (offset +10, the one-line `});` context found ten lines down); **KS-1236 first, then this** applies both of this brief's hunks at their stated lines (both sit above KS-1236's insertion). The resulting file is byte-identical in both orders (sha256 compared), and the file with BOTH briefs' cells runs green at the tip. **Order for the raise: either; if raised in one PR, put this brief's two hunks first (lower line numbers first) and re-derive KS-1236's header as `@@ -175,1 +175,15 @@` — or raise KS-1236 first and re-derive this brief's hunk B as-is (its lines are above KS-1236's).** Tamper lines: KS-1236 plants `users.ts:1267`, this plants `:1105` — no shared line; each is planted-and-restored, none moves the other. Neither tamper of this brief reds KS-1236's cells (they never post to `/me/mfa/disable`) and neither of KS-1236's reds this cell (it never posts to `/me/verification`). Seat B 11th's six files include neither. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21, `--shared` scratch clone at `cbae988db`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_round23-drafter-precheck/KS-1006/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md` = this brief's own two hunks with the two file-header lines, fresh `--shared` clone `r23_clone_3` at `cbae988db`, farmed by the harness's `prepare_clone.sh`): **RESULT: PASS (8/8)** — T1 one fenced block; T2 touched set == the test file only; T3 strict apply (both hunks at their stated lines); T4 every `+` line byte-exact; T5 green at the tip **12/12 cells** (11 existing + 1 new, every declared cell present); T6 VERIFYINVERTED red set == {wrongcode} and PRESENCEINVERTED red set == {wrongcode}, each an assertion failure — received `[ 200, undefined, undefined ]` vs expected `[ 400, 'BAD_REQUEST', 'Invalid verification code' ]` (`KS-1006/out.md.checker/tamper_*.cells.json`): the route's REAL 200 through the mock's `updateUserOrThrow`, not a mock gap; T7 all three controls green under both; T8 `users.ts` restored to sha256 `96408a532a73` after each. Source tracked-modified count 0 before and after (`KS-1006/prepare.log`).
- Both apply orders with the sibling `KS-1236-SUBMITLEVEL-1` hunk (`KS-1006/patch_1006.diff` + `patch_1236.diff` on the bare tip file): **1006 then 1236** — 1236's hunk applies at `:175` (offset +10); **1236 then 1006** — both of 1006's hunks at their stated lines; the resulting file is **244 lines, sha256 `f9f0b7fce6009962` in BOTH orders** (`both_orderA.test.ts` == `both_orderB.test.ts`, `cmp` identical).
- With BOTH briefs' cells applied and no tamper: the file **14/14** (`both_file.out`); the whole auth suite **66 files, 782/782** (`full_suite_both.out`; bare tip 779/779 — +3, 0 new red). Cross-tampers over the combined file (`cross_*.out`, each planted by bytes and restored to `96408a532a73`): EQUALADMITTED reds exactly KS-1236's `samelevel`; GUARDNEVERFIRES exactly KS-1236's two; VERIFYINVERTED and PRESENCEINVERTED exactly this brief's `wrongcode` — no tamper of either brief reds the other's cell.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` / `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts`, then the TWO hunks above exactly as shown, A (`@@ -56,1 +56,2 @@`) then B (`@@ -120,1 +121,10 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (MFA / auth surface, test-only pin — allowed). Refs KS-1006** (and KS-732, whose sibling-door proof this cell is the users-route half of). **NEVER Closes** — KS-1006 asks for a PRODUCT change on the no-secret row (fail closed); this brief pins the with-secret refusal that every fix shape keeps and leaves the latent no-secret admission as the open defect it is.
- **Not from a gate cell.** Found by the 2026-09-21 board widening (round 23): the ticket's own quoted shape names a verifying half no cell asserts.
- **Not pinned here, said plainly:** the no-secret row (`mfaEnabled` true, `mfaSecret` null — a cell asserting today's admission would pin the bug); the `MFA is not enabled` and `Valid 6-digit verification code required` refusals at `:1099` / `:1102` (right today; separate pins if wanted); a CORRECT code disabling MFA (it would need the file's clock or a computed TOTP — the `ks732` file's idiom — and is the success path the ticket does not question).
- **Collision: same test file as this round's KS-1236 brief, disjoint hunks, both orders measured, same product file, no shared tamper line** (measured above and in the MEASURED section).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1006 night/inputs/test_only_1006WRONGCODE-1.json night/briefs/KS-1006-WRONGCODE-1.md ctx=65536
```
