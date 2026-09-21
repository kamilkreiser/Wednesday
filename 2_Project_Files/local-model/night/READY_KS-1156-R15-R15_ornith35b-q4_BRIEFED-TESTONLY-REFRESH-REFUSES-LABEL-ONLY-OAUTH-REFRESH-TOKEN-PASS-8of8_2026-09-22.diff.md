# READY — KS-1156-R15-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1156-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 00:14 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1156-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/1156R15-R15/out.md.checker/patch.diff` rc 0, Wednesday 00:05 seat, source-read: expected_plus 111/111 in the diff, titles = R1 red + 2 controls; golden cmp IDENTICAL).

**Held 00:14 2026-09-22 by Wednesday 00:05 seat, source-read: expected_plus 111/111 in the diff, titles = R1 red + 2 controls; golden cmp IDENTICAL after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1156-ornith35b-night/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/auth/src/__tests__/ks1156-auth4-gate-records-983-r2-984.test.ts` (new). `+` lines 111 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 3/3 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `R15` → red exactly ['KS-1156 R1 - authMethod oauth with NO client_id: 401, no tok']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1156-ornith35b-night/input.json`. Brief: `night/briefs/KS-1156-R15-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1156-ornith35b-night/checker.out`.

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
