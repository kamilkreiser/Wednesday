# READY — KS-1188-F1a-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1188-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 01:15 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1188-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/1188F1a-R15/out.md.checker/patch.diff` rc 0, Wednesday 00:05 seat, drain sitting: expected_plus 136/136 in the diff; reds matched 3/3; golden IDENTICAL).

**Held 01:15 2026-09-22 by Wednesday 00:05 seat, drain sitting: expected_plus 136/136 in the diff; reds matched 3/3; golden IDENTICAL after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1188-ornith35b-night/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/auth/src/__tests__/ks1188-mfa-status-503-route.test.ts` (new). `+` lines 136 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 5/5 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `F1A` → red exactly ['RED KS-1188 F1a - a message-form DEK infrastructure fault an', 'RED KS-1188 F1a - a pg 53300 DEK fault answers 503 SERVICE_U', 'RED KS-1188 F1a - an ECONNREFUSED DEK fault answers 503 SERV']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1188-ornith35b-night/input.json`. Brief: `night/briefs/KS-1188-F1a-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1188-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1188-mfa-status-503-route.test.ts
@@ -0,0 +1,136 @@
+// KS-1188 F1a (the #1013 gate on KS-999): GET /api/auth/mfa/status answers 503 when getUserById hits a DEK-read
+// infrastructure fault, but no cell pinned it. The gate's G-CALLER-FAILOPEN (mfa.ts maps that 503 to a null user, so the
+// route answers 200 mfaEnabled:false) reddened 0 of 745 cells. These cells mount the REAL mfa routes, the REAL userRepo and
+// the REAL errorHandler on 127.0.0.1:0, aim a getDek rejection at the row, and pin the status and the body.
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
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
+    if (String(sql).includes('SELECT') && String(sql).includes('FROM users')) {
+      return { rows: [{ id: 'ks1188-mfa-status-user', email: 'sdek:ciphertext', status: 'active', role: 'user', mfa_enabled: true, mfa_secret: 'sdek:seed', mfa_backup_codes: ['h1', 'h2'], created_at: '2026-01-01T00:00:00.000Z', updated_at: '2026-01-01T00:00:00.000Z' }], rowCount: 1 };
+    }
+    return { rows: [], rowCount: 0 };
+  }),
+}));
+
+vi.mock('../middleware/authenticate', () => {
+  const inject = () => (req: any, _res: any, next: () => void) => {
+    req.user = { userId: 'ks1188-mfa-status-user', role: 'user' };
+    next();
+  };
+  return { authenticate: inject, authenticateAccessOrConnector: inject };
+});
+
+const USER_ID = 'ks1188-mfa-status-user';
+const UNAVAILABLE = { success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Authentication service temporarily unavailable, please retry' } };
+const INTERNAL = { success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } };
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
+/** GET /api/auth/mfa/status over loopback: the status and the parsed JSON body. */
+async function getStatus(): Promise<{ status: number; body: any }> {
+  const res = await fetch(base + '/api/auth/mfa/status');
+  return { status: res.status, body: await res.json() };
+}
+
+/** The messages the logger received at error level, in call order. */
+function errorLines(): unknown[] {
+  return logError.mock.calls.map((call: unknown[]) => call[0]);
+}
+
+describe('KS-1188 F1a - GET /api/auth/mfa/status answers 503 on a getUserById DEK infrastructure fault', () => {
+  it('RED KS-1188 F1a - a message-form DEK infrastructure fault answers 503 SERVICE_UNAVAILABLE with the fixed body', async () => {
+    getDek.mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
+    const r = await getStatus();
+    expect(r.status, 'the mfa/status status under a DEK infrastructure fault').toBe(503);
+    expect(r.body).toStrictEqual(UNAVAILABLE);
+    expect(getDek).toHaveBeenCalledWith(USER_ID);
+  });
+
+  it('RED KS-1188 F1a - a pg 53300 DEK fault answers 503 SERVICE_UNAVAILABLE with the fixed body', async () => {
+    getDek.mockRejectedValueOnce(Object.assign(new Error('sorry, too many clients already'), { code: '53300' }));
+    const r = await getStatus();
+    expect(r.status, 'the mfa/status status under a DEK infrastructure fault').toBe(503);
+    expect(r.body).toStrictEqual(UNAVAILABLE);
+  });
+
+  it('RED KS-1188 F1a - an ECONNREFUSED DEK fault answers 503 SERVICE_UNAVAILABLE and never a 200 with mfaEnabled false', async () => {
+    getDek.mockRejectedValueOnce(Object.assign(new Error('connect ECONNREFUSED 127.0.0.1:5432'), { code: 'ECONNREFUSED' }));
+    const r = await getStatus();
+    expect(r.status, 'the mfa/status status under a DEK infrastructure fault').toBe(503);
+    expect(r.body.success).toBe(false);
+    expect(r.body.data).toBeUndefined();
+  });
+
+  it('GREEN KS-1188 control - a NON-infrastructure DEK failure reaches the REAL errorHandler and answers 500 INTERNAL_ERROR', async () => {
+    getDek.mockRejectedValueOnce(new Error('ks1188-not-an-infrastructure-fault'));
+    const r = await getStatus();
+    expect(r.status).toBe(500);
+    expect(r.body).toStrictEqual(INTERNAL);
+    expect(getDek).toHaveBeenCalledWith(USER_ID);
+    expect(errorLines()).toContain('DB getUserById failed');
+    expect(errorLines()).toContain('Error occurred');
+  });
+
+  it('GREEN KS-1188 control - with nothing rejecting the REAL route reads the row and answers 200 with mfaEnabled true', async () => {
+    const r = await getStatus();
+    expect(r.status).toBe(200);
+    expect(r.body).toStrictEqual({ success: true, data: { mfaEnabled: true, mfaType: 'totp', backupCodesRemaining: 2 } });
+    expect(getDek).toHaveBeenCalledWith(USER_ID);
+    expect(errorLines().length).toBe(0);
+  });
+});
```
