# READY — KS-1868-KS-1868-O73-P4 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p4_auth_oauth_authorize_post_and_token_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 13:10 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p4_auth_oauth_authorize_post_and_token_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p4_auth_oauth_authorize_post_and_token_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p4_auth_oauth_authorize_post_and_token_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p4_auth_oauth_authorize_post_and_token_catches_unreadable_throw-control-r3/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:10 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p4_auth_oauth_authorize_post_and_token_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `92a26320e30ad680459cdb96c5b68b91a5f175a5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/routes/oauth.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/oauth.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/auth/src/routes/oauth.ts
200	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: oauth.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/routes/oauth.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/routes/oauth.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts 200 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/oauth.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 the oauth authorize and token catches read the rejection value safely RED ks1868 R1 authorize: a revoked Proxy rejection logs a constant reason and the route answers 500 server_error', 'KS-1868 the oauth authorize and token catches read the rejection value safely RED ks1868 R2 authorize: an Error whose message getter throws logs a constant reason and the route answers 500 server_error', 'KS-1868 the oauth authorize and token catches read the rejection value safely RED ks1868 R3 token: a revoked Proxy rejection logs a constant reason and the route answers 500 server_error', 'KS-1868 the oauth authorize and token catches read the rejection value safely RED ks1868 R4 token: an Error whose message getter throws logs a constant reason and the route answers 500 server_error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1471 failed=3 | after: total=1477 failed=2` · `NEW reds: []` [baseline_suite.json total=1471 failed=3; after_suite.json total=1477 failed=2]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/oauth.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts` (+200/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/routes/oauth.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `92a26320e30ad680459cdb96c5b68b91a5f175a5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p4_auth_oauth_authorize_post_and_token_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o73_p4_auth_oauth_authorize_post_and_token_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p4_auth_oauth_authorize_post_and_token_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/oauth.ts b/Blockchain/Dev/services/auth/src/routes/oauth.ts
--- a/Blockchain/Dev/services/auth/src/routes/oauth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/oauth.ts
@@ -805,5 +805,11 @@
   } catch (error: any) {
-    logger.error('OAuth authorize POST error', { error: error.message });
+    let reason: string;
+    try {
+      reason = error.message;
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('OAuth authorize POST error', { error: reason });
     res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'server_error' } });
   }
 });
@@ -1109,5 +1115,11 @@
   } catch (error: any) {
-    logger.error('OAuth token error', { error: error.message });
+    let reason: string;
+    try {
+      reason = error.message;
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('OAuth token error', { error: reason });
     res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'server_error' } });
   }
 });
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts
@@ -0,0 +1,200 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+// KS-1868: POST /api/oauth/authorize (the deny branch) and POST /api/oauth/token look the client app up first; when
+// that lookup REJECTS, each route's outer catch must still log its line and answer the constant 500 `server_error`
+// even if the rejection value cannot be read (a revoked Proxy throws on property reads; an Error whose `message`
+// getter throws, throws on `.message`). Today such a value makes the catch itself throw inside an async Express 4
+// handler: no response is sent (the request hangs) and Node sees an UNHANDLED REJECTION. The cells count unhandled
+// rejections themselves and give the client a short timeout, so a hang shows as a failed assertion. Harness: the
+// ks781 oauth route test (real router; collaborators mocked). The app lookup stand-in rejects with a plain function,
+// not a vi.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy before the code under
+// test saw it. No code is minted and no session is created on either path.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logged: [] as unknown[][],
+  unhandled: 0,
+  minted: 0,
+}));
+
+const capture = vi.hoisted(() => ({
+  debug: () => undefined,
+  info: () => undefined,
+  warn: () => undefined,
+  error: (...args: unknown[]) => {
+    h.logged.push(args);
+  },
+  log: () => undefined,
+}));
+vi.mock('../utils/logger', () => ({ logger: capture, createLogger: () => capture, validateEnv: () => undefined }));
+
+vi.mock('../services/accountLockout', () => ({
+  isLockedOut: vi.fn(async () => false),
+  recordFailure: vi.fn(async () => 1),
+  recordSuccess: vi.fn(async () => undefined),
+}));
+vi.mock('../services/session', () => ({
+  createSession: vi.fn(async () => {
+    h.minted += 1;
+    return { id: 'sess-1' };
+  }),
+  getRedisClient: vi.fn(() => null),
+}));
+vi.mock('../services/password', () => ({ verifyPassword: vi.fn(async () => false) }));
+vi.mock('../services/oauth', () => ({
+  createAuthorizationCode: vi.fn(async () => {
+    h.minted += 1;
+    return 'MINTED_1868_CODE';
+  }),
+  createApp: vi.fn(), getAppById: vi.fn(), listApps: vi.fn(), updateApp: vi.fn(), rotateSecret: vi.fn(),
+  exchangeCode: vi.fn(), verifyClientSecret: vi.fn(),
+  getAppByClientId: (_clientId: string) => Promise.reject(h.toThrow),
+  validateScopes: vi.fn((requested: string[]) => requested ?? []),
+  parseScopeString: vi.fn(() => []), AVAILABLE_SCOPES: {},
+}));
+vi.mock('../repositories/userRepo', () => ({
+  getUserByEmail: vi.fn(async () => null),
+  getUserByIdPreAuth: vi.fn(async () => null),
+  updateUser: vi.fn(async () => null),
+  updateUserOrThrow: vi.fn(async () => null),
+  consumeBackupCode: vi.fn(async () => ({ consumed: false })),
+  reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
+  getPlatformAdmin: vi.fn(async () => null),
+}));
+vi.mock('../services/jwt', () => ({
+  generateTokenPair: vi.fn(() => ({ accessToken: 'MINTED_1868_ACCESS', refreshToken: 'r', expiresIn: 900 })),
+  verifyRefreshToken: vi.fn(() => ({})),
+}));
+vi.mock('../services/refreshDenylist', () => ({ isRefreshJtiDenylisted: vi.fn(async () => false) }));
+vi.mock('../middleware/authenticate', () => ({ authenticate: () => (_r: unknown, _s: unknown, n: () => void) => n() }));
+vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [] })) }));
+vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
+
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+
+let server: Server;
+let baseUrl = '';
+beforeAll(async () => {
+  process.removeAllListeners('unhandledRejection');
+  process.on('unhandledRejection', onUnhandled);
+  const { oauthRouter } = await import('../routes/oauth');
+  const app = express();
+  app.use(express.json());
+  app.use('/api/oauth', oauthRouter);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((resolve) => server.once('listening', () => resolve()));
+  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+});
+afterAll(async () => {
+  server.closeAllConnections();
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logged.length = 0;
+  h.unhandled = 0;
+  h.minted = 0;
+});
+
+const AUTHORIZE_LINES = () => h.logged.filter((c) => c[0] === 'OAuth authorize POST error');
+const TOKEN_LINES = () => h.logged.filter((c) => c[0] === 'OAuth token error');
+
+async function post(path: string, body: Record<string, unknown>): Promise<{ status: number; code: string | undefined; message: string | undefined; minted: number } | null> {
+  try {
+    const res = await fetch(baseUrl + path, {
+      method: 'POST',
+      headers: { 'Content-Type': 'application/json' },
+      body: JSON.stringify(body),
+      redirect: 'manual',
+      signal: AbortSignal.timeout(1500),
+    });
+    const text = await res.text();
+    let code: string | undefined;
+    let message: string | undefined;
+    try {
+      const parsed = JSON.parse(text);
+      code = parsed?.error?.code;
+      message = parsed?.error?.message;
+    } catch {
+      code = undefined;
+      message = undefined;
+    }
+    return { status: res.status, code, message, minted: h.minted };
+  } catch {
+    return null;
+  }
+}
+
+const authorizeDeny = () => post('/api/oauth/authorize', { action: 'deny', client_id: 'sec_ks1868', redirect_uri: 'https://app.test/cb' });
+const tokenExchange = () => post('/api/oauth/token', { grant_type: 'authorization_code', code: 'c-1868', client_id: 'sec_ks1868', redirect_uri: 'https://app.test/cb' });
+const SERVER_ERROR = { status: 500, code: 'INTERNAL_ERROR', message: 'server_error', minted: 0 };
+
+const getterThrows = () =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 the oauth authorize and token catches read the rejection value safely', () => {
+  it('control ks1868 C1 authorize: an ordinary Error still logs its message and the route answers 500 server_error', async () => {
+    h.toThrow = new Error('app lookup down');
+    expect(await authorizeDeny()).toEqual(SERVER_ERROR);
+    expect(h.unhandled).toBe(0);
+    expect(AUTHORIZE_LINES()).toHaveLength(1);
+    expect(AUTHORIZE_LINES()[0][1]).toEqual({ error: 'app lookup down' });
+  });
+
+  it('control ks1868 C2 token: an ordinary Error still logs its message and the route answers 500 server_error', async () => {
+    h.toThrow = new Error('app lookup down');
+    expect(await tokenExchange()).toEqual(SERVER_ERROR);
+    expect(h.unhandled).toBe(0);
+    expect(TOKEN_LINES()).toHaveLength(1);
+    expect(TOKEN_LINES()[0][1]).toEqual({ error: 'app lookup down' });
+  });
+
+  it('RED ks1868 R1 authorize: a revoked Proxy rejection logs a constant reason and the route answers 500 server_error', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    h.toThrow = proxy;
+    expect(await authorizeDeny()).toEqual(SERVER_ERROR);
+    expect(h.unhandled).toBe(0);
+    expect(AUTHORIZE_LINES()).toHaveLength(1);
+    expect(AUTHORIZE_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 authorize: an Error whose message getter throws logs a constant reason and the route answers 500 server_error', async () => {
+    h.toThrow = getterThrows();
+    expect(await authorizeDeny()).toEqual(SERVER_ERROR);
+    expect(h.unhandled).toBe(0);
+    expect(AUTHORIZE_LINES()).toHaveLength(1);
+    expect(AUTHORIZE_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 token: a revoked Proxy rejection logs a constant reason and the route answers 500 server_error', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    h.toThrow = proxy;
+    expect(await tokenExchange()).toEqual(SERVER_ERROR);
+    expect(h.unhandled).toBe(0);
+    expect(TOKEN_LINES()).toHaveLength(1);
+    expect(TOKEN_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 token: an Error whose message getter throws logs a constant reason and the route answers 500 server_error', async () => {
+    h.toThrow = getterThrows();
+    expect(await tokenExchange()).toEqual(SERVER_ERROR);
+    expect(h.unhandled).toBe(0);
+    expect(TOKEN_LINES()).toHaveLength(1);
+    expect(TOKEN_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```
