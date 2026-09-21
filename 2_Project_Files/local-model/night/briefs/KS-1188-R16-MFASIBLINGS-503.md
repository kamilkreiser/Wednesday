# KS-1188 R16-MFASIBLINGS-503 - Wednesday's task for Ornith: a TEST-ONLY pin that the two SIBLING getUserById sites in routes/mfa.ts (POST /setup/start :166, POST /backup-codes/regenerate :397) answer 503 SERVICE_UNAVAILABLE on a DEK infrastructure fault - the F1c / F1d cells the #1148-#1166 gate proposed - at develop 3916eacd1 (written 07:44 on 2026-09-22 by Wednesday's feed6 drafter from routes/mfa.ts:135-190 + :386-426, repositories/userRepo.ts:165-240 + :407-419 + :796-977, services/totp.ts:1-120 and the #1163 shape file ks1188-mfa-status-503-route.test.ts read whole at the tip, and the gate report's NOT PINNED rows MFASIBLINGSITES-166 / -397)
File: `Blockchain/Dev/services/auth/src/__tests__/ks1188-mfa-sibling-sites-503.test.ts`
Tip: `3916eacd12af23bfd464440b4c770f7da0f2dd96`
Runner: `vitest`

## Premises (measured by the feed6 drafter at 07:44:39 AEST on 2026-09-22, in a `--shared` scratchpad clone detached at 3916eacd1; Wednesday re-derives before queueing)
- THE TIP: origin develop by `ls-remote` = `3916eacd12af23bfd464440b4c770f7da0f2dd96` (two reads, the stamps in `runs/2026-09-22_feed6-drafter-precheck/lsremote.txt`); `rev-list --count --first-parent a1931d2f3..3916eacd1` = 12 (Seat C 17th's twelve squashes over BASE_GO, #1148 ... #1166, the merge already landed when this drafter booted); `cat-file -e 3916eacd1:Blockchain/Dev/services/auth/src/__tests__/ks1188-mfa-status-503-route.test.ts` rc 0 - the #1163 shape file IS at this tip (its path from the gate report's #1163 equality-targets line, blob 5213553cc).
- THE ROWS (the gate's, measured by a QA gate, not a census): `mfa.ts:143`, `:166` and `:397` are THREE whole-line-identical occurrences of `    const user = await userRepo.getUserById(userId);` (`grep -c -x -F` = 3, at :143 / :166 / :397). #1163's F1a pins :143 (GET /status, scope anchor :138). The gate planted the 503-swallowing `.catch` at :166 (scope anchor :161 `mfaRoutes.post('/setup/start', authenticate(), ...)`) and separately at :397 (scope anchor :391 `mfaRoutes.post('/backup-codes/regenerate', authenticate(), ...)`) and the WHOLE auth lane stayed 801/801 GREEN both times (`evidence/tamper16C.head-1163-site166.out` / `-site397.out`). Nothing pins those two routes. This brief is F1c + F1d as ONE file.
- THE PRODUCT IS RIGHT at the tip: `userRepo.getUserById` (:407-419) awaits `fromRow` inside its try, `fromRow` (:218-221) calls `subjectDeks.getDek(row.id)` whenever a column is subject-DEK ciphertext (the row's email is `sdek:ciphertext`), and the catch maps an infrastructure fault (`dbErrors.ts:44` - `/connection terminated/i`) to `ServiceUnavailableError('Authentication service temporarily unavailable, please retry')`; each route's `catch (error) { next(error); }` hands it to the REAL errorHandler -> 503 with the fixed body. The test file's mocks are the shape file's (`@secuura/shared` spread over the actual so `currentTenantId` / `runWithPlatformScope` stay REAL; `../services/subjectDeks`, `../utils/logger`, `../db`, `../middleware/authenticate` replaced) with ONE addition each: a `vi.hoisted` row state (`mfaEnabled`, a real base32 `secret`) because /setup/start needs MFA OFF (else :168 throws 409 ConflictError) and /backup-codes/regenerate needs MFA ON with a seed the test can mint a code for; and the `../db` mock answers `UPDATE users` with `rowCount: 1` so `updateUserOrThrow` (:960-977, KS-1052) confirms the regenerate write. `isEncryptedPii: () => false` makes `decryptMfaSecret` (:173-175) hand the seed back as legacy plaintext, so `generateTotpCode(state.secret)` from the REAL `../services/totp` is the code `verifyTotpCode` (:402) accepts. `getUserByIdPreAuth` (:511, `FROM auth_find_user_by_id`) falls to the mock's empty answer -> tenantForRls undefined, harmless.
- The test file is ABSENT at 3916eacd1 - ONE NEW FILE (`ls src/__tests__ | grep -c -i sibling` = 0). Mode NEW. Boots the REAL router on 127.0.0.1:0 (the shape file's idiom); no Redis, no PostgreSQL, no network beyond loopback. The regenerate good path hashes ten backup codes with the REAL argon2id (`totp.ts:93-107`, 32 MiB / t=2) - that cell carries a 30 s timeout.
- TAMPERS are BLOCK tampers (the 2026-09-19 contract): a one-line From matches 3 times (:143 / :166 / :397): the builder would plant it by its `Line:` number without asserting uniqueness, and the gate's own instrument flagged exactly that ambiguity on F1a (F1AANCHORAMBIGUITY), so each From is the site line PLUS its neighbour, whole consecutive lines, and each block occurs EXACTLY ONCE at the tip (measured: block :166-:167 hits [166]; block :396-:397 hits [396]). The `Line:` is the block's start (the builder cross-checks it). The To keeps the neighbour line byte for byte and rewrites the site line into the gate's mutation `.catch((e: any) => { if (e?.statusCode === 503) return null; throw e; })` - the F1a tamper's exact text (`night/briefs/KS-1188-R15-F1a.md`).
- Every `+` line is ASCII-only, backslash-free, carries NO double-quote character, and every single-quoted string is balanced (measured on the 147 lines: 0 / 0 / 0, odd-quote lines []). JSON bodies are built by `JSON.stringify` at run time, never as literals.
- Typecheck (the 16th round's per-file method, `runs/2026-09-22_feed6-drafter-precheck/typecheck/typecheck_feed6.log`, run 1188r1 after the golden had farmed the clone): a temp tsconfig extending auth's (`strict`, `noUnusedLocals`, `noUnusedParameters`) with `files=[the test]`, `include []`, `exclude []`, `types [node, vitest/globals]`, `npx tsc -p` -> 0 errors in the file (0 total, rc 0); a planted TS2322 on a copy of the fence was CAUGHT (1 error, rc 2). Golden precheck (this fence as the model output through the REAL `tasks/test_only/checker.sh` in the clone): `RESULT: PASS (8/8)` - T5 4/4 at the tip; T6[F1C] red == declared exactly, the red an assertion `expected 401 to be 503`; T6[F1D] `expected 400 to be 503`; the checker's planted mfa.ts blobs sha256 128f88bb0b1b (:166-167) and b0c3617e3a2c (:396-397) are BYTE-IDENTICAL to the gate's own site166 / site397 plants (`plant_sha` in its `tamper16C-head-1163-site166.json` / `-site397.json`). (Premise line rewritten at 07:46:52 AEST after the measurements; the input was rebuilt and the golden re-run from this text.)
- AUTH TEST-ONLY PIN (allowed under the week instruction: test-only pins on auth surfaces are IN, auth PRODUCT edits are OUT): the diff has ZERO product hunks; `routes/mfa.ts` is named only as the checker's tamper target. Collision check: no held READY and no open PR creates a `ks1188-mfa-sibling` file (`ls night/READY_* | grep -c -i sibling` = 0); #1163 is MERGED at this tip.

## What is wrong (one paragraph)
#1163 (KS-1188 F1a) pinned that GET /api/auth/mfa/status answers 503 when `getUserById` hits a DEK-read infrastructure fault - at ONE of the three identical `getUserById` sites in `routes/mfa.ts`. The gate then planted the same fail-open mutation (a `.catch` that turns a 503 into a null user) at the other two sites, :166 inside POST /setup/start and :397 inside POST /backup-codes/regenerate, and 801 auth cells stayed green: at :166 the null user becomes a 401 (`if (!user) throw new InvalidCredentialsError()`, :167), at :397 a 400 (`BadRequestError('MFA is not enabled')`, :398-400) - the database being down would be reported to the caller as THEIR credential or THEIR MFA state. The code is RIGHT at the tip; this task is the PIN (test-only): one new vitest file whose two RED cells red under those two tampers and whose two GREEN controls (the good path of each route, 200) stay green under both. NOT in this task: any product file, GET /status (#1163 holds it), GET /users/me (#1163 F1b), the ticket's scope question (rows, not BY DESIGN - the gate's words).

## THE MODE - read this twice
TEST-ONLY, ONE NEW FILE: your diff contains EXACTLY ONE file, the NEW test file above: `--- /dev/null` then `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1188-mfa-sibling-sites-503.test.ts` then ONE `@@ -0,0 +1,147 @@` hunk, every line `+`, no context, no `-`. No product hunk. Copy the 147 lines below byte for byte, in order: no double quote anywhere, no backslash anywhere - the fence is written so that none is needed. Every declaration below is USED (`noUnusedLocals` is on): keep `state`, `USER_ID`, `UNAVAILABLE`, `server`, `base`, `getDek`, `logError`, `post`, `errorLines` and every import exactly as written.

## The exact change
```
+// KS-1188 F1c / F1d - the #1148-#1166 gate (2026-09-22, NOT PINNED rows MFASIBLINGSITES-166 and -397): routes/mfa.ts
+// holds THREE identical `const user = await userRepo.getUserById(userId);` sites - :143 in GET /status, :166 in
+// POST /setup/start, :397 in POST /backup-codes/regenerate. #1163 (F1a) pinned the 503 at :143 only; the gate planted
+// the same 503-swallowing .catch at :166 and again at :397 and the whole auth lane stayed 801/801 GREEN - nothing
+// pinned those two routes. These cells mount the REAL mfa routes, the REAL userRepo and the REAL errorHandler on
+// 127.0.0.1:0 exactly as ks1188-mfa-status-503-route.test.ts does, aim a getDek rejection at the row read inside
+// getUserById, POST each route through the mocked authenticate (the bearer identity), and pin the 503 and its body.
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+import { generateTotpCode } from '../services/totp';
+
+/** Row state the ../db mock reads per cell: setup/start needs MFA OFF (else 409), regenerate needs it ON with a real seed. */
+const state = vi.hoisted(() => ({ mfaEnabled: false, secret: 'JBSWY3DPEHPK3PXP' }));
+
+vi.mock('@secuura/shared', async (importOriginal) => {
+  const actual = await importOriginal<Record<string, unknown>>();
+  return {
+    ...actual,
+    encryptField: (v: string) => v,
+    decryptField: (v: string) => v,
+    encryptFieldWithDek: (v: string) => v,
+    decryptFieldWithDek: (v: string) => v,
+    isSubjectDekCiphertext: (v: unknown) => typeof v === 'string' && v.startsWith('sdek:'),
+    isEncryptedPii: () => false,
+    lookupHash: (v: string) => 'hash:' + v,
+  };
+});
+
+vi.mock('../services/subjectDeks', () => ({
+  subjectDeks: {
+    getDek: vi.fn(async () => Buffer.from('ks1188-throwaway-dek')),
+    getOrCreateDek: vi.fn(async () => Buffer.from('ks1188-throwaway-dek')),
+  },
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+vi.mock('../db', () => ({
+  query: vi.fn(async (sql: string) => {
+    const text = String(sql);
+    if (text.includes('SELECT') && text.includes('FROM users')) {
+      return { rows: [{ id: 'ks1188-mfa-sibling-user', email: 'sdek:ciphertext', status: 'active', role: 'user', mfa_enabled: state.mfaEnabled, mfa_secret: state.secret, mfa_backup_codes: ['h1', 'h2'], created_at: '2026-01-01T00:00:00.000Z', updated_at: '2026-01-01T00:00:00.000Z' }], rowCount: 1 };
+    }
+    if (text.startsWith('UPDATE users')) {
+      return { rows: [], rowCount: 1 };
+    }
+    return { rows: [], rowCount: 0 };
+  }),
+}));
+
+vi.mock('../middleware/authenticate', () => {
+  const inject = () => (req: any, _res: any, next: () => void) => {
+    req.user = { userId: 'ks1188-mfa-sibling-user', role: 'user' };
+    next();
+  };
+  return { authenticate: inject, authenticateAccessOrConnector: inject };
+});
+
+const USER_ID = 'ks1188-mfa-sibling-user';
+const UNAVAILABLE = { success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Authentication service temporarily unavailable, please retry' } };
+
+let server: Server;
+let base = '';
+let getDek: any;
+let logError: any;
+
+beforeAll(async () => {
+  const { mfaRoutes } = await import('../routes/mfa');
+  const { errorHandler } = await import('../middleware/errorHandler');
+  getDek = (await import('../services/subjectDeks')).subjectDeks.getDek;
+  logError = (await import('../utils/logger')).logger.error;
+  const app = express();
+  app.use(express.json());
+  app.use('/api/auth/mfa', mfaRoutes);
+  app.use(errorHandler);
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => {
+      base = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+      resolve();
+    });
+  });
+});
+
+afterAll(async () => {
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+
+beforeEach(() => { vi.clearAllMocks(); });
+
+/** POST a JSON body to an mfa route over loopback (the mocked authenticate injects the bearer identity): status + parsed body. */
+async function post(path: string, body: Record<string, unknown>): Promise<{ status: number; body: any }> {
+  const res = await fetch(base + path, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) });
+  return { status: res.status, body: await res.json() };
+}
+
+/** The messages the logger received at error level, in call order. */
+function errorLines(): unknown[] {
+  return logError.mock.calls.map((call: unknown[]) => call[0]);
+}
+
+describe('KS-1188 F1c / F1d - the two sibling getUserById sites in mfa.ts answer 503 on a DEK infrastructure fault', () => {
+  it('RED KS-1188 F1c - POST /api/auth/mfa/setup/start answers 503 SERVICE_UNAVAILABLE on a getUserById DEK infrastructure fault', async () => {
+    state.mfaEnabled = false;
+    getDek.mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
+    const r = await post('/api/auth/mfa/setup/start', {});
+    expect(r.status, 'the setup/start status under a DEK infrastructure fault').toBe(503);
+    expect(r.body.error.code).toBe('SERVICE_UNAVAILABLE');
+    expect(r.body).toStrictEqual(UNAVAILABLE);
+    expect(getDek).toHaveBeenCalledWith(USER_ID);
+  });
+
+  it('RED KS-1188 F1d - POST /api/auth/mfa/backup-codes/regenerate answers 503 SERVICE_UNAVAILABLE on a getUserById DEK infrastructure fault', async () => {
+    state.mfaEnabled = true;
+    getDek.mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
+    const r = await post('/api/auth/mfa/backup-codes/regenerate', { totpCode: generateTotpCode(state.secret) });
+    expect(r.status, 'the backup-codes/regenerate status under a DEK infrastructure fault').toBe(503);
+    expect(r.body.error.code).toBe('SERVICE_UNAVAILABLE');
+    expect(r.body).toStrictEqual(UNAVAILABLE);
+    expect(getDek).toHaveBeenCalledWith(USER_ID);
+  });
+
+  it('GREEN KS-1188 F1c control - with nothing rejecting POST /api/auth/mfa/setup/start answers 200 with a secret and an otpauth URI', async () => {
+    state.mfaEnabled = false;
+    const r = await post('/api/auth/mfa/setup/start', {});
+    expect(r.status).toBe(200);
+    expect(r.body.success).toBe(true);
+    expect(typeof r.body.data.secret).toBe('string');
+    expect(String(r.body.data.otpAuthUri).startsWith('otpauth://totp/')).toBe(true);
+    expect(getDek).toHaveBeenCalledWith(USER_ID);
+    expect(errorLines().length).toBe(0);
+  });
+
+  it('GREEN KS-1188 F1d control - with nothing rejecting and a valid TOTP code POST /api/auth/mfa/backup-codes/regenerate answers 200 with ten new codes', async () => {
+    state.mfaEnabled = true;
+    const r = await post('/api/auth/mfa/backup-codes/regenerate', { totpCode: generateTotpCode(state.secret) });
+    expect(r.status).toBe(200);
+    expect(r.body.success).toBe(true);
+    expect(r.body.data.backupCodes.length).toBe(10);
+    expect(r.body.data.message).toBe('New backup codes generated. Previous codes are now invalid.');
+    expect(getDek).toHaveBeenCalledWith(USER_ID);
+    expect(errorLines().length).toBe(0);
+  }, 30_000);
+});
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `RED KS-1188 F1c - POST /api/auth/mfa/setup/start answers 503 SERVICE_UNAVAILABLE on a getUserById DEK infrastructure fault`
- `RED KS-1188 F1d - POST /api/auth/mfa/backup-codes/regenerate answers 503 SERVICE_UNAVAILABLE on a getUserById DEK infrastructure fault`
- `GREEN KS-1188 F1c control - with nothing rejecting POST /api/auth/mfa/setup/start answers 200 with a secret and an otpauth URI`  (CONTROL - green on both trees)
- `GREEN KS-1188 F1d control - with nothing rejecting and a valid TOTP code POST /api/auth/mfa/backup-codes/regenerate answers 200 with ten new codes`  (CONTROL - green on both trees)

## Tampers
### F1C
File: `Blockchain/Dev/services/auth/src/routes/mfa.ts`
Line: 166
From:
```
    const user = await userRepo.getUserById(userId);
    if (!user) throw new InvalidCredentialsError();
```
To:
```
    const user = await userRepo.getUserById(userId).catch((e: any) => { if (e?.statusCode === 503) return null; throw e; });
    if (!user) throw new InvalidCredentialsError();
```
Reds: `RED KS-1188 F1c - POST /api/auth/mfa/setup/start answers 503 SERVICE_UNAVAILABLE on a getUserById DEK infrastructure fault`
(Scope anchor :161 `mfaRoutes.post('/setup/start', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {` - the gate's MFASIBLINGSITES-166 row. The 2-line From block occurs EXACTLY ONCE at 3916eacd1, starting at :166 (the site line alone occurs 3 times: :143 / :166 / :397). Reachability: the F1c cell rejects getDek once with the message-form fault; getUserById maps it to ServiceUnavailableError (statusCode 503); the tamper's .catch swallows exactly that into a null user, :167 throws InvalidCredentialsError -> 401 - `expect(r.status).toBe(503)` fails by assertion. The F1d cell and both controls never enter this route's rejection path: green.)

### F1D
File: `Blockchain/Dev/services/auth/src/routes/mfa.ts`
Line: 396
From:
```
    const { totpCode } = req.body;
    const user = await userRepo.getUserById(userId);
```
To:
```
    const { totpCode } = req.body;
    const user = await userRepo.getUserById(userId).catch((e: any) => { if (e?.statusCode === 503) return null; throw e; });
```
Reds: `RED KS-1188 F1d - POST /api/auth/mfa/backup-codes/regenerate answers 503 SERVICE_UNAVAILABLE on a getUserById DEK infrastructure fault`
(Scope anchor :391 `mfaRoutes.post('/backup-codes/regenerate', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {` - the gate's MFASIBLINGSITES-397 row. The 2-line From block occurs EXACTLY ONCE at 3916eacd1, starting at :396 (the site line is :397). Reachability: the F1d cell rejects getDek once; under the tamper the 503 becomes a null user and :398-400 throws BadRequestError('MFA is not enabled') -> 400 - `expect(r.status).toBe(503)` fails by assertion. The F1c cell and both controls: green.)

## Controls
- `GREEN KS-1188 F1c control - with nothing rejecting POST /api/auth/mfa/setup/start answers 200 with a secret and an otpauth URI`
- `GREEN KS-1188 F1d control - with nothing rejecting and a valid TOTP code POST /api/auth/mfa/backup-codes/regenerate answers 200 with ten new codes`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/auth/src/__tests__/ks1188-mfa-sibling-sites-503.test.ts`); the header `@@ -0,0 +1,147 @@` (147 is the count of `+` lines - count them); no double quote, no `\$` / `\u` / backslash of any kind in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
