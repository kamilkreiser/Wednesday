# READY — KS-1188 F1a (NEW auth test: GET /api/auth/mfa/status (routes/mfa.ts) answers 503 SERVICE_UNAVAILABLE with the fixed body under a DEK infra fault — message / pg 53300 / ECONNREFUSED; a non-infra fault stays 500) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE. Held by Wednesday at 06:40 AEST. Run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-17_ks1188-ornith35b-night2
# Source read by me (Wednesday): the model's 136 lines IDENTICAL to the brief's test block (python compare; a mutated copy unequal); one new file, no product change; apply STRICT; A4 under the #1013 gate's G-CALLER-FAILOPEN at mfa.ts:143 (a 503 read as no user → 200 mfaEnabled:false): 3 red / 5 run by assertion, controls green; A6 auth NEW reds [].
# PR NOTES: "Refs KS-1188 (F1a)". Test-only → tier 2. Pinned at develop 523f283c6. F1b's tamper line moves if READY_KS-1018 / #1015 (users.ts) merges first — the test file itself does not collide.

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
+describe('KS-1188 F1a — GET /api/auth/mfa/status answers 503 on a getUserById DEK infrastructure fault', () => {
+  it('🔴 KS-1188 F1a — a message-form DEK infrastructure fault answers 503 SERVICE_UNAVAILABLE with the fixed body', async () => {
+    getDek.mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
+    const r = await getStatus();
+    expect(r.status, 'the mfa/status status under a DEK infrastructure fault').toBe(503);
+    expect(r.body).toStrictEqual(UNAVAILABLE);
+    expect(getDek).toHaveBeenCalledWith(USER_ID);
+  });
+
+  it('🔴 KS-1188 F1a — a pg 53300 DEK fault answers 503 SERVICE_UNAVAILABLE with the fixed body', async () => {
+    getDek.mockRejectedValueOnce(Object.assign(new Error('sorry, too many clients already'), { code: '53300' }));
+    const r = await getStatus();
+    expect(r.status, 'the mfa/status status under a DEK infrastructure fault').toBe(503);
+    expect(r.body).toStrictEqual(UNAVAILABLE);
+  });
+
+  it('🔴 KS-1188 F1a — an ECONNREFUSED DEK fault answers 503 SERVICE_UNAVAILABLE and never a 200 with mfaEnabled false', async () => {
+    getDek.mockRejectedValueOnce(Object.assign(new Error('connect ECONNREFUSED 127.0.0.1:5432'), { code: 'ECONNREFUSED' }));
+    const r = await getStatus();
+    expect(r.status, 'the mfa/status status under a DEK infrastructure fault').toBe(503);
+    expect(r.body.success).toBe(false);
+    expect(r.body.data).toBeUndefined();
+  });
+
+  it('🟢 KS-1188 control — a NON-infrastructure DEK failure reaches the REAL errorHandler and answers 500 INTERNAL_ERROR', async () => {
+    getDek.mockRejectedValueOnce(new Error('ks1188-not-an-infrastructure-fault'));
+    const r = await getStatus();
+    expect(r.status).toBe(500);
+    expect(r.body).toStrictEqual(INTERNAL);
+    expect(getDek).toHaveBeenCalledWith(USER_ID);
+    expect(errorLines()).toContain('DB getUserById failed');
+    expect(errorLines()).toContain('Error occurred');
+  });
+
+  it('🟢 KS-1188 control — with nothing rejecting the REAL route reads the row and answers 200 with mfaEnabled true', async () => {
+    const r = await getStatus();
+    expect(r.status).toBe(200);
+    expect(r.body).toStrictEqual({ success: true, data: { mfaEnabled: true, mfaType: 'totp', backupCodesRemaining: 2 } });
+    expect(getDek).toHaveBeenCalledWith(USER_ID);
+    expect(errorLines().length).toBe(0);
+  });
+});
```
