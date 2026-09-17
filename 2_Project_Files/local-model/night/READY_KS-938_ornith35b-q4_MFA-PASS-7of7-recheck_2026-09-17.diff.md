# READY — KS-938 (routes/mfa.ts half: POST /disable and the setup-failure revert write mfa_secret + mfa_backup_codes as NULL instead of undefined, which updateUser skipped; + NEW auth test R1/R2 + CONTROL + COMPLETENESS) — Ornith ornith:35b q4, first sample; night run 19:05 FAIL A2 (model omitted the new-file @@ header); RE-CHECK of the SAME out.md under the NEWFILE-HEADER accommodation = PASS 7/7 (no second model round); READY written 19:23 2026-09-17 on tip 81ee4b729
# Source read by Wednesday: the model's 8 product -/+ lines and 141 test lines IDENTICAL to the brief's fences (python compare; a mutated copy unequal); apply STRICT after the synthesized `@@ -0,0 +1,141 @@` (inserted in THIS file; the model's out.md is unchanged); A3b REMOVED_LINES 241,242,376,377; A4 BOTH declared reds R1 + R2 in failed_names (2 failed / 4 run); A5 4/4; A6 751 -> 755, NEW reds []; A7 tsc rc 0. Wednesday re-ran `local-model/tests/newfile_header_arms.sh` itself: ALL PASS.
# PR NOTES: `Refs KS-938`, NEVER Closes — a SPLIT: the third site routes/users.ts:1111 (POST /api/users/me/mfa/disable, also missing the mfaBackupCodes key) is a two-line follow-up AFTER #1018 merges. TIER 1 (credential-lifecycle write). RENAME the test file at raise. KS-938 stays In Progress on merge (§5f). A6 note: ks949-platform-admin-seed-identity is a known ~1-in-7 flake (KS-1053) — re-run once before scoring. Brief night/briefs/KS-938.md; search report night/briefs/NEXT_SEARCH_2026-09-17n.REPORT.md.

```diff
--- a/Blockchain/Dev/services/auth/src/routes/mfa.ts
+++ b/Blockchain/Dev/services/auth/src/routes/mfa.ts
@@ -238,8 +238,8 @@ mfaRoutes.post('/setup/verify', authenticate(), async (req: AuthenticatedRequest
       // So the return is checked and the inconsistency is named in the log.
       const reverted = await userRepo.updateUser(userId, {
         mfaEnabled: false,
-        mfaSecret: undefined,
-        mfaBackupCodes: undefined,
+        mfaSecret: null,
+        mfaBackupCodes: null,
         verificationLevel: 'BASIC',
       } as any);
       if (!reverted) {
@@ -373,8 +373,8 @@ mfaRoutes.post('/disable', authenticate(), async (req: AuthenticatedRequest, re
     // KS-1052: a false "MFA disabled" locks the user out of their own account.
     await userRepo.updateUserOrThrow(userId, {
       mfaEnabled: false,
-      mfaSecret: undefined,
-      mfaBackupCodes: undefined,
+      mfaSecret: null,
+      mfaBackupCodes: null,
       verificationLevel: 'BASIC',
     } as any, 'MFA disable');
 
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks938-security-mfa-disabled-leaves-the-totp.test.ts
@@ -0,0 +1,141 @@
+/**
+ * KS-938: disabling MFA must clear the TOTP seed and the hashed backup codes.
+ * userRepo.updateUser skips every field whose value is undefined, so a write of
+ * mfaSecret undefined issues a PARTIAL UPDATE that leaves the column in the row.
+ * These cells drive the REAL mfaRoutes and the REAL userRepo against a stubbed
+ * db and read the UPDATE each route emits (the disable route and the setup
+ * failure revert in routes/mfa.ts).
+ */
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import express from 'express';
+
+const USER_ID = '7d1e4b2a-938c-4f1e-9a6b-2c5d8e0f9381';
+const EXPECTED_CELLS = 3;
+let CELLS_RUN = 0;
+
+const state = vi.hoisted(() => ({
+  failDelete: false,
+  queries: [] as Array<{ sql: string; params: unknown[] }>,
+}));
+
+const silentLogger = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
+vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: vi.fn() }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));
+
+function userRow() {
+  return {
+    id: USER_ID, email: 'ks938@example.test', first_name: 'K', last_name: 'S',
+    display_name: 'KS', role: 'user', status: 'active', email_verified: true,
+    password_hash: 'ks938-fake-hash', phone_number: null, phone_verified: false,
+    mfa_enabled: true, mfa_secret: 'JBSWY3DPEHPK3PXP', mfa_backup_codes: ['hashedcode1'],
+    verification_level: 'standard', organization_id: null, tenant_id: null, tenant_slug: null,
+    wallet_address: null, auth_method: 'password', metadata: null,
+    created_at: new Date(), updated_at: new Date(), last_login_at: null,
+  };
+}
+
+vi.mock('../db', () => ({
+  query: vi.fn(async (sql: string, params: unknown[] = []) => {
+    state.queries.push({ sql, params });
+    const s = sql.trim();
+    if (s.startsWith('DELETE FROM mfa_pending_setups')) {
+      if (state.failDelete) throw new Error('ks938 pending setup delete failed');
+      return { rows: [], rowCount: 1 };
+    }
+    if (s.includes('FROM mfa_pending_setups')) {
+      return { rows: [{ secret: 'JBSWY3DPEHPK3PXP', expires_at: new Date(Date.now() + 600000) }], rowCount: 1 };
+    }
+    if (s.startsWith('UPDATE users')) return { rows: [userRow()], rowCount: 1 };
+    if (s.includes('FROM users')) return { rows: [userRow()], rowCount: 1 };
+    return { rows: [], rowCount: 0 };
+  }),
+}));
+vi.mock('../services/subjectDeks', () => ({
+  subjectDeks: { getOrCreateDek: vi.fn(async () => Buffer.alloc(32, 7)), getDek: vi.fn(async () => null) },
+}));
+vi.mock('../services/password', () => ({ verifyPassword: vi.fn(async () => true) }));
+vi.mock('../services/totp', () => ({
+  verifyTotpCode: vi.fn(() => true),
+  verifyBackupCode: vi.fn(async () => ({ valid: false, index: 0 })),
+  generateBackupCodes: vi.fn(() => ['AAAAAAAA']),
+  hashBackupCode: vi.fn(async (c: string) => 'h:' + c),
+}));
+vi.mock('../middleware/authenticate', () => ({
+  authenticate: () => (req: any, _res: any, next: () => void) => {
+    req.user = { userId: USER_ID, email: 'ks938@example.test', role: 'user' };
+    next();
+  },
+}));
+vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
+
+let server: Server;
+let base = '';
+
+beforeAll(async () => {
+  const { mfaRoutes } = await import('../routes/mfa');
+  const { errorHandler } = await import('../middleware/errorHandler');
+  const app = express();
+  app.use(express.json());
+  app.use('/api/auth/mfa', mfaRoutes);
+  app.use(errorHandler);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(async () => {
+  await new Promise<void>((r) => server.close(() => r()));
+});
+
+beforeEach(() => {
+  state.failDelete = false;
+  state.queries = [];
+});
+
+// POST a JSON body and answer the status code
+async function post(path: string, body: Record<string, unknown>): Promise<number> {
+  const res = await fetch(base + '/api/auth/mfa' + path, {
+    method: 'POST',
+    headers: { Authorization: 'Bearer ks938-token', 'Content-Type': 'application/json' },
+    body: JSON.stringify(body),
+  });
+  await res.text();
+  return res.status;
+}
+
+// every UPDATE users statement that writes mfa_enabled, as [columns, params]
+function mfaWrites(): unknown[] {
+  return state.queries
+    .filter((q) => q.sql.trim().startsWith('UPDATE users SET') && q.sql.includes('mfa_enabled = '))
+    .map((q) => [q.sql.split(' SET ')[1].split(' WHERE ')[0].split(', ').map((c) => c.split(' = ')[0]), q.params]);
+}
+
+describe('KS-938 - disabling MFA clears the TOTP seed and the backup codes', () => {
+  it('KS-938 R1 - POST /disable writes mfa_secret and mfa_backup_codes as null', async () => {
+    CELLS_RUN += 1;
+    const status = await post('/disable', { password: 'correct-horse' });
+    expect([status, mfaWrites()]).toEqual([200, [[['mfa_enabled', 'mfa_secret', 'mfa_backup_codes', 'verification_level', 'updated_at'], [false, null, null, 'basic', USER_ID]]]]);
+  });
+
+  it('KS-938 R2 - the setup-failure revert writes mfa_secret and mfa_backup_codes as null', async () => {
+    CELLS_RUN += 1;
+    state.failDelete = true;
+    const status = await post('/setup/verify', { totpCode: '123456' });
+    const writes = mfaWrites();
+    expect([status, writes.length, writes[1]]).toEqual([400, 2, [['mfa_enabled', 'mfa_secret', 'mfa_backup_codes', 'verification_level', 'updated_at'], [false, null, null, 'basic', USER_ID]]]);
+  });
+
+  it('KS-938 CONTROL - a completed setup writes ONE update that enables MFA with a stored seed and the hashed codes', async () => {
+    CELLS_RUN += 1;
+    const status = await post('/setup/verify', { totpCode: '123456' });
+    const writes = mfaWrites() as Array<[string[], unknown[]]>;
+    const cols = writes.length === 1 ? writes[0][0] : [];
+    const params = writes.length === 1 ? writes[0][1] : [];
+    expect([status, writes.length, cols, params[0], typeof params[1], params[2], params[3]]).toEqual([200, 1, ['mfa_enabled', 'mfa_secret', 'mfa_backup_codes', 'verification_level', 'updated_at'], true, 'string', ['h:AAAAAAAA'], 'standard']);
+  });
+
+  it('KS-938 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
