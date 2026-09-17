# READY — KS-1219 (auth routes/oauth.ts: a `scope` that arrives as an ARRAY — repeated query param, repeated form field, JSON array — answers 400 invalid_request instead of 500 server_error; two 5-line guards after the GET :478 and POST :632 destructuring + the new ks1219 test, 5 cells)
# Source read by Wednesday 23:00: product + lines 10/10 IDENTICAL to the brief's two fences, and the new test body 147/147 lines IDENTICAL to the brief's ts fence (python, per part; a mutated copy unequal — a whole-diff compare reads DIFFERENT only because the brief carries the test as a plain ts body). Checker RESULT PASS (7/7) first sample; A4 R1-R3 red by assertion at the tip; A6 whole auth suite no new red; A7 tsc rc 0. Tip = develop bb848b828.
# PR NOTES: `Refs KS-1219`, TIER 1 (auth/OAuth product edit; the auth tier, briefed last). Only `scope` is guarded (the ticket names other non-string params — not probed). Behaviour change for any client that sends a repeated scope: 500 -> 400 invalid_request (RFC 6749 §3.1 forbids repeated parameters). Re-derive hunk headers at raise. Run: runs/2026-09-17_ks1219-ornith35b-night/out.md.

```diff
--- a/Blockchain/Dev/services/auth/src/routes/oauth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/oauth.ts
@@ -476,4 +476,9 @@ oauthRouter.get('/authorize', async (req: Request, res: Response) => {
       client_id, redirect_uri, response_type, scope, state,
       code_challenge, code_challenge_method,
     } = req.query as Record<string, string>;
+    // KS-1219: a repeated query parameter arrives as an ARRAY, and parseScopeString
+    // cannot split one - refuse it as a malformed request, not a server error.
+    if (scope !== undefined && typeof scope !== 'string') {
+      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'scope must be a single string' } });
+    }
 
@@ -630,4 +635,9 @@ oauthRouter.post('/authorize', async (req: Request, res: Response) => {
       // client that can log in can authorize without learning a second dialect.
       mfaCode,
     } = req.body;
+    // KS-1219: a repeated form field or a JSON array arrives as an ARRAY, and the
+    // resolver cannot split one - refuse it before the deny branch and the resolver.
+    if (scope !== undefined && typeof scope !== 'string') {
+      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'scope must be a single string' } });
+    }
 
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1219-oauth-authorize-answers-500-server-error.test.ts
@@ -0,0 +1,147 @@
+/**
+ * KS-1219: an array-valued scope on /api/oauth/authorize is a malformed request.
+ * A repeated query parameter, a repeated form field or a JSON array hands the
+ * handler an ARRAY for scope. The resolver passes it to parseScopeString, which
+ * calls split on it, so the TypeError reached the catch and answered 500
+ * server_error. These cells drive the REAL oauthRouter on 127.0.0.1 port 0 and
+ * expect 400 invalid_request for each carrier, with no code minted.
+ */
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import express from 'express';
+
+const EXPECTED_CELLS = 4;
+let CELLS_RUN = 0;
+const CLIENT = 'sec_ks1219client';
+const REGISTERED = 'https://app.example.com/cb';
+
+const mintSpy = vi.hoisted(() => ({ calls: 0 }));
+
+const silentLogger = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
+vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: vi.fn() }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));
+
+vi.mock('../services/accountLockout', () => ({
+  isLockedOut: vi.fn(async () => false),
+  recordFailure: vi.fn(async () => 1),
+  recordSuccess: vi.fn(async () => undefined),
+}));
+vi.mock('../services/session', () => ({
+  createSession: vi.fn(async () => ({ id: 's' })),
+  getRedisClient: vi.fn(() => null),
+}));
+vi.mock('../services/password', () => ({ verifyPassword: vi.fn(async () => true) }));
+vi.mock('../services/totp', () => ({
+  verifyTotpCode: vi.fn(() => true),
+  verifyBackupCode: vi.fn(async () => ({ valid: false, index: -1 })),
+}));
+
+vi.mock('../services/oauth', () => ({
+  createAuthorizationCode: vi.fn(async () => { mintSpy.calls++; return 'MINTED_CODE_1219'; }),
+  getAppByClientId: vi.fn(async (id: string) =>
+    id === CLIENT
+      ? { id: 'app-1219', name: 'KS-1219 App', clientId: CLIENT, appType: 'confidential',
+          redirectUris: [REGISTERED], allowedScopes: ['openid', 'profile'] }
+      : null),
+  createApp: vi.fn(), getAppById: vi.fn(), listApps: vi.fn(), updateApp: vi.fn(),
+  rotateSecret: vi.fn(), exchangeCode: vi.fn(),
+  validateScopes: vi.fn((r: string[], allowed: string[]) => (r ?? []).filter((s) => allowed.includes(s))),
+  parseScopeString: vi.fn((s: string) => (s ? s.split(' ') : [])),
+  AVAILABLE_SCOPES: {},
+}));
+
+vi.mock('../repositories/userRepo', () => ({
+  getUserByEmail: vi.fn(async () => ({
+    id: 'u1219', email: 'ks1219@example.test', passwordHash: 'ks1219-stub-hash',
+    status: 'ACTIVE', mfaEnabled: false, mfaSecret: null, mfaBackupCodes: null,
+  })),
+  updateUser: vi.fn(async () => null),
+  reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
+  getPlatformAdmin: vi.fn(async () => null),
+}));
+
+vi.mock('../services/jwt', () => ({ generateTokenPair: vi.fn(() => ({ accessToken: 'a', refreshToken: 'r', expiresIn: 900 })) }));
+vi.mock('../services/refreshDenylist', () => ({ isRefreshJtiDenylisted: vi.fn(async () => false) }));
+vi.mock('../middleware/authenticate', () => ({ authenticate: () => (_r: unknown, _s: unknown, n: () => void) => n() }));
+vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [] })) }));
+vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
+
+let server: Server;
+let base = '';
+
+beforeAll(async () => {
+  const { oauthRouter } = await import('../routes/oauth');
+  const app = express();
+  app.use(express.json());
+  app.use(express.urlencoded({ extended: true }));
+  app.use('/api/oauth', oauthRouter);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  await new Promise<void>((r) => server.close(() => r()));
+});
+
+beforeEach(() => {
+  mintSpy.calls = 0;
+});
+
+// answer [status, error message or null] for a response
+async function verdict(res: Response): Promise<[number, string | null]> {
+  const text = await res.text();
+  let message: string | null = null;
+  try {
+    message = JSON.parse(text).error.message;
+  } catch {
+    message = null;
+  }
+  return [res.status, message];
+}
+
+const QUERY = '/api/oauth/authorize?response_type=code&client_id=' + CLIENT + '&redirect_uri=' + encodeURIComponent(REGISTERED);
+
+describe('KS-1219 - an array-valued scope on /api/oauth/authorize is 400 invalid_request', () => {
+  it('KS-1219 R1 - GET with a repeated scope query parameter answers 400 invalid_request', async () => {
+    CELLS_RUN += 1;
+    const res = await fetch(base + QUERY + '&scope=openid&scope=profile', { redirect: 'manual' });
+    expect(await verdict(res)).toEqual([400, 'invalid_request']);
+  });
+
+  it('KS-1219 R2 - POST approve with a repeated scope form field answers 400 invalid_request and mints no code', async () => {
+    CELLS_RUN += 1;
+    const form = 'email=ks1219%40example.test&password=correct-horse&client_id=' + CLIENT
+      + '&redirect_uri=' + encodeURIComponent(REGISTERED) + '&action=approve&scope=openid&scope=profile';
+    const res = await fetch(base + '/api/oauth/authorize', {
+      method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: form, redirect: 'manual',
+    });
+    expect([...(await verdict(res)), mintSpy.calls]).toEqual([400, 'invalid_request', 0]);
+  });
+
+  it('KS-1219 R3 - POST deny with a JSON array scope answers 400 invalid_request', async () => {
+    CELLS_RUN += 1;
+    const res = await fetch(base + '/api/oauth/authorize', {
+      method: 'POST', headers: { 'Content-Type': 'application/json' }, redirect: 'manual',
+      body: JSON.stringify({ action: 'deny', client_id: CLIENT, redirect_uri: REGISTERED, scope: ['openid', 'profile'], state: 'xyz' }),
+    });
+    expect(await verdict(res)).toEqual([400, 'invalid_request']);
+  });
+
+  it('KS-1219 CONTROL - a single string scope still renders the consent page and still mints a code', async () => {
+    CELLS_RUN += 1;
+    const page = await fetch(base + QUERY + '&scope=openid', { redirect: 'manual' });
+    const pageText = await page.text();
+    const approve = await fetch(base + '/api/oauth/authorize', {
+      method: 'POST', headers: { 'Content-Type': 'application/json' }, redirect: 'manual',
+      body: JSON.stringify({ email: 'ks1219@example.test', password: 'correct-horse', client_id: CLIENT, redirect_uri: REGISTERED, action: 'approve', scope: 'openid' }),
+    });
+    await approve.text();
+    expect([page.status, pageText.includes('name=' + String.fromCharCode(34) + 'password'), approve.status, mintSpy.calls]).toEqual([200, true, 302, 1]);
+  });
+
+  it('KS-1219 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
