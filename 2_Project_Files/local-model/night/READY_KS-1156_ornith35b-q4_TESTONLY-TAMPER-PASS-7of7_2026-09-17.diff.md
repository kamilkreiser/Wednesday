# READY — KS-1156 (B, record R-C2: NEW services/auth test pinning the refresh guard's `authMethod === 'oauth'` arm at routes/auth.ts:677 — 1 red cell under the T6 tamper + 2 controls) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, strict, 2026-09-17 12:27
# Source read by Wednesday: the model's 111 `+` lines IDENTICAL to the brief's test fence (python compare; a mutated copy unequal); one new file, no product change; apply STRICT; A6 whole services/auth 754/754 (baseline 751); A7 tsc rc 0. Run: local-model/runs/2026-09-17_ks1156-ornith35b-night
# PR NOTES: `Refs KS-1156 (B, R-C2)`, NEVER Closes — A.1 (label-set decision), A.2/A.3 (comment edits), R-C1, R-C3 and C stay open. New file rather than the ks1151 file (the ticket's DoD names ks1151; same deviation as KS-1199 — state it in the PR). Test-only on an auth surface: inside the week grant (auth PRODUCT edits are not). Brief premise P5: the file also reds when the whole guard moves below getSession (R-C1's ordering) — premeasured, not graded by the checker. Brief: night/briefs/KS-1156.md; search report: night/briefs/NEXT_SEARCH_2026-09-17f.REPORT.md.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1156-auth4-gate-records-983-r2-984.test.ts
@@ -0,0 +1,111 @@
+// KS-1156 B, R-C2 (the AUTH4 gate on #986, KS-1151): every OAuth fixture in the ks1151 file carries client_id, so the
+// authMethod === 'oauth' arm of the refresh guard has no earning cell. This file pins a LABEL-ONLY token: refused, untouched.
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import express from 'express';
+import jwt from 'jsonwebtoken';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+
+const silent = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
+vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent, validateEnv: vi.fn() }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silent, createLogger: () => silent }));
+
+const USER = {
+  id: 'user-1156', email: 'u1156@secuura.local', status: 'ACTIVE', role: 'OWNER',
+  verificationLevel: 'BASIC', mfaEnabled: false, tenantId: 'ten-1', organizationId: 'org-1',
+};
+
+/** What the route did to persistence, so a cell can assert what was NOT done. */
+const world = vi.hoisted(() => ({ rotated: [] as string[], denylisted: [] as string[], sessionLookups: [] as string[] }));
+
+vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [], rowCount: 0 })) }));
+vi.mock('../repositories/userRepo', () => ({
+  getUserById: vi.fn(async () => null), getUserByIdPreAuth: vi.fn(async () => ({ ...USER })), getUserByEmail: vi.fn(async () => null),
+  updateUser: vi.fn(async () => undefined), getPlatformAdmin: vi.fn(async () => null), updatePlatformAdminPassword: vi.fn(async () => undefined),
+  reencryptMfaSecretIfLegacy: vi.fn(async () => undefined), reencryptPlatformAdminMfaSecretIfLegacy: vi.fn(async () => undefined),
+}));
+vi.mock('../services/session', () => ({
+  createSession: vi.fn(async () => ({ id: 'sess-new' })),
+  getSession: vi.fn(async (id: string) => {
+    world.sessionLookups.push(id);
+    return { id, userId: USER.id, isActive: true, expiresAt: new Date(Date.now() + 3_600_000), refreshToken: 'opaque', createdAt: new Date(), lastActivityAt: new Date() };
+  }),
+  rotateSessionRefreshToken: vi.fn(async (id: string) => { world.rotated.push(id); }),
+  revokeSession: vi.fn(async () => undefined), getRedisClient: vi.fn(() => null),
+  validateSession: vi.fn(async () => true), updateSessionActivity: vi.fn(async () => undefined),
+}));
+vi.mock('../services/refreshDenylist', () => ({
+  isRefreshJtiDenylisted: vi.fn(async () => false),
+  denylistRefreshJti: vi.fn(async (jti: string) => { world.denylisted.push(jti); }),
+}));
+vi.mock('../services/accountLockout', () => ({
+  isLockedOut: vi.fn(async () => false), recordFailure: vi.fn(async () => 1),
+  recordSuccess: vi.fn(async () => undefined), clearFailures: vi.fn(async () => undefined),
+}));
+vi.mock('../services/password', () => ({
+  verifyPassword: vi.fn(async () => false), hashPassword: vi.fn(async () => 'argon2id-stub'),
+  checkPasswordStrength: vi.fn(() => ({ ok: true })), generateResetToken: vi.fn(() => 'tok'), shouldRehashAfterVerify: vi.fn(() => false),
+}));
+vi.mock('../services/email', () => ({ sendVerificationEmail: vi.fn(async () => undefined), sendPasswordResetEmail: vi.fn(async () => undefined) }));
+vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
+
+let server: Server;
+let port = 0;
+let mint: (user: unknown, sessionId: string, opts?: { clientId: string; scopes: readonly string[] }) => { accessToken: string; refreshToken: string };
+
+beforeAll(async () => {
+  const jwtMod = await import('../services/jwt');
+  await jwtMod.initJwtKeys();
+  mint = jwtMod.generateTokenPair as unknown as typeof mint;
+  const { authRoutes } = await import('../routes/auth');
+  const { errorHandler } = await import('../middleware/errorHandler');
+  const app = express();
+  app.use(express.json({ limit: '10mb' }));
+  app.use('/api/auth', authRoutes);
+  app.use(errorHandler);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  port = (server.address() as AddressInfo).port;
+});
+afterAll(async () => { await new Promise<void>((r) => server.close(() => r())); });
+beforeEach(() => { world.rotated = []; world.denylisted = []; world.sessionLookups = []; vi.clearAllMocks(); });
+
+const claims = (tok: unknown) => (jwt.decode(String(tok)) as Record<string, unknown> | null) ?? {};
+
+/** A real OAuth mint with client_id dropped and the authMethod label kept, re-signed RS256 with the setup file key. */
+function labelOnlyToken(): string {
+  const { refreshToken } = mint(USER, 'sess-x', { clientId: 'client-1', scopes: ['openid'] });
+  const { client_id: _bound, iat: _iat, exp: _exp, ...rest } = claims(refreshToken) as Record<string, unknown>;
+  const privatePem = Buffer.from(String(process.env.JWT_PRIVATE_KEY), 'base64').toString('utf8');
+  return jwt.sign(rest, privatePem, { algorithm: 'RS256', expiresIn: 600, ...(process.env.JWT_KEY_ID ? { keyid: process.env.JWT_KEY_ID } : {}) });
+}
+
+/** POSTs the token in the body; answers [status, access token issued, rotated, denylisted count, session lookups]. */
+async function refreshOutcome(token: string): Promise<unknown[]> {
+  const url = 'http://127.0.0.1:' + String(port) + '/api/auth/refresh';
+  const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ refreshToken: token }) });
+  const body = (await res.json()) as { data?: { accessToken?: unknown } };
+  return [res.status, typeof body.data?.accessToken === 'string', world.rotated, world.denylisted.length, world.sessionLookups];
+}
+
+describe('KS-1156 R-C2 - POST /api/auth/refresh refuses a label-only OAuth refresh token', () => {
+  it('KS-1156 R1 - authMethod oauth with NO client_id: 401, no token, nothing rotated, denylisted or looked up', async () => {
+    const token = labelOnlyToken();
+    expect(claims(token).authMethod, 'the fixture keeps the label').toBe('oauth');
+    expect(claims(token).client_id, 'the fixture drops the binding').toBeUndefined();
+    const answer = await refreshOutcome(token);
+    expect(answer, 'the label arm alone refuses it before the session lookup').toEqual([401, false, [], 0, []]);
+  });
+
+  it('KS-1156 control - a bound and labelled OAuth mint is still refused: 401, nothing looked up', async () => {
+    const { refreshToken } = mint(USER, 'sess-x', { clientId: 'client-1', scopes: ['openid'] });
+    const answer = await refreshOutcome(refreshToken);
+    expect(answer, 'a token carrying both claims stays refused').toEqual([401, false, [], 0, []]);
+  });
+
+  it('KS-1156 control - a login-minted pair still refreshes: 200, token issued, session looked up and rotated', async () => {
+    const { refreshToken } = mint(USER, 'sess-x');
+    const answer = await refreshOutcome(refreshToken);
+    expect(answer, 'the harness reaches getSession, so an empty lookup list above is the guard').toEqual([200, true, ['sess-x'], 1, ['sess-x']]);
+  });
+});
```
