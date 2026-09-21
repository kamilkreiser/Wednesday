# READY — KS-1188-MFASIBLINGS-R16 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1188-ornith35b-night4/out.md.checker/patch.diff`** (from `ls` at 07:55 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1188-ornith35b-night4/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed6-drafter-precheck/1188MFASIBLINGS-R16/out.md.checker/patch.diff` rc 0, Wednesday (the 07:2x seat)).

**Held 07:55 2026-09-22 by Wednesday (the 07:2x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1188-ornith35b-night4/out.md.checker`, not typed).** Tip `3916eacd12af23bfd464440b4c770f7da0f2dd96`. Touches ONE file: `Blockchain/Dev/services/auth/src/__tests__/ks1188-mfa-sibling-sites-503.test.ts` (new). `+` lines 147 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 4/4 cells. Tampers (2), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `F1C` → red exactly ['RED KS-1188 F1c - POST /api/auth/mfa/setup/start answers 503']
- `F1D` → red exactly ['RED KS-1188 F1d - POST /api/auth/mfa/backup-codes/regenerate']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1188-ornith35b-night4/input.json`. Brief: `night/briefs/KS-1188-MFASIBLINGS-R16.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1188-ornith35b-night4/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1188-mfa-sibling-sites-503.test.ts
@@ -0,0 +1,147 @@
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
