# READY — KS-1797-KS-1797 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1797_p1_authorize_get_state_challenge/out.md.checker/patch.diff`** (from `ls` at 09:51 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1797_p1_authorize_get_state_challenge/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1797_p1_authorize_get_state_challenge/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 09:51 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1797_p1_authorize_get_state_challenge/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `e3d8456ec81d0b02172dd5a3060404815e797bde`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/routes/oauth.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/oauth.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	1	Blockchain/Dev/services/auth/src/routes/oauth.ts
114	0	Blockchain/Dev/services/auth/src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (5 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: oauth.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/routes/oauth.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/routes/oauth.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts 114 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/oauth.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=2 of total=6; red cell(s): ['KS-1797: GET /api/oauth/authorize refuses a repeated state or code_challenge RED KS-1797 R1 GET with a repeated state parameter is 400 invalid_request, not 500', 'KS-1797: GET /api/oauth/authorize refuses a repeated state or code_challenge RED KS-1797 R2 GET with a repeated code_challenge parameter is 400 invalid_request, not 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1326 failed=3 | after: total=1332 failed=1` · `NEW reds: []` [baseline_suite.json total=1326 failed=3; after_suite.json total=1332 failed=1]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/oauth.ts` (+5/-1 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts` (+114/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/routes/oauth.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `e3d8456ec81d0b02172dd5a3060404815e797bde` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1797_p1_authorize_get_state_challenge/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1797_p1_authorize_get_state_challenge/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/oauth.ts b/Blockchain/Dev/services/auth/src/routes/oauth.ts
--- a/Blockchain/Dev/services/auth/src/routes/oauth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/oauth.ts
@@ -490,7 +490,11 @@
       client_id, redirect_uri, response_type, scope, state,
       code_challenge, code_challenge_method,
     } = req.query as Record<string, string>;
-
+    // KS-1797: a repeated query parameter (?state=a&state=b) reaches this handler as an ARRAY whatever the cast above says. generateConsentPage then calls escapeHtml on it, an array has no
+    // `replace`, and the catch below answered 500 server_error. A malformed request is a 400 invalid_request, the existing message the resolver's rules use, so no published message changes.
+    if ((state !== undefined && typeof state !== 'string') || (code_challenge !== undefined && typeof code_challenge !== 'string')) {
+      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'state and code_challenge must each be a single string' } });
+    }
     // KS-804: every app-derived rule lives in the resolver now — response_type,
     // client/redirect, the scheme, PKCE for public clients and scopes. This
     // handler renders the resolution; it does not re-decide any of it.
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts
@@ -0,0 +1,114 @@
+// KS-1797 (GET half): GET /api/oauth/authorize answered 500 server_error when `state` or `code_challenge` arrived as a repeated query parameter (an array at run time): generateConsentPage calls
+// escapeHtml on it and an array has no `replace`. A malformed request is a 400 invalid_request. Driven through the real router on a loopback listener with the same mocks as
+// ks1219-authorize-refuses-an-array-valued-scope.test.ts; one string value is the control. The POST half of KS-1797 (a JSON array state or code_challenge) is NOT covered here.
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { Server } from 'node:http';
+import express from 'express';
+
+const state = vi.hoisted(() => ({
+  app: null as null | {
+    id: string; name: string; clientId: string; appType: string;
+    redirectUris: string[]; allowedScopes: string[];
+  },
+}));
+
+const silent = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
+vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent, validateEnv: vi.fn() }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silent, createLogger: () => silent }));
+
+vi.mock('../services/oauth', async (importOriginal) => {
+  const real = await importOriginal<Record<string, unknown>>();
+  return {
+    ...real,
+    createAuthorizationCode: vi.fn(async () => 'MINTED_AUTHORIZATION_CODE'),
+    createApp: vi.fn(),
+    getAppByClientId: vi.fn(async () => state.app),
+    getAppById: vi.fn(),
+  };
+});
+vi.mock('../services/accountLockout', () => ({
+  isLockedOut: vi.fn(async () => false), recordFailure: vi.fn(async () => undefined),
+  recordSuccess: vi.fn(async () => undefined), clearFailures: vi.fn(async () => undefined),
+}));
+vi.mock('../services/session', () => ({
+  createSession: vi.fn(async () => ({ id: 's' })), getRedisClient: vi.fn(() => null),
+  validateSession: vi.fn(async () => true), updateSessionActivity: vi.fn(async () => undefined),
+}));
+vi.mock('../services/password', () => ({ verifyPassword: vi.fn(async () => true), hashPassword: vi.fn(async () => 'h') }));
+vi.mock('../repositories/userRepo', () => ({
+  getUserByEmail: vi.fn(async () => ({
+    id: 'user-1', email: 'u@secuura.local', status: 'ACTIVE', mfaEnabled: false,
+    passwordHash: 'h', role: 'OWNER', verificationLevel: 'BASIC',
+  })),
+  getUserById: vi.fn(async () => null), updateUser: vi.fn(async () => undefined),
+  getPlatformAdmin: vi.fn(async () => null), reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
+}));
+vi.mock('../services/jwt', () => ({ generateTokenPair: vi.fn(() => ({ accessToken: 'a', refreshToken: 'r', expiresIn: 900 })) }));
+vi.mock('../services/refreshDenylist', () => ({ isRefreshJtiDenylisted: vi.fn(async () => false) }));
+vi.mock('../middleware/authenticate', () => ({ authenticate: () => (_r: unknown, _s: unknown, n: () => void) => n() }));
+vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [] })) }));
+vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
+
+let server: Server;
+let base: string;
+let createAuthorizationCode: ReturnType<typeof vi.fn>;
+
+beforeAll(async () => {
+  const { oauthRouter } = await import('../routes/oauth');
+  ({ createAuthorizationCode } = (await import('../services/oauth')) as never);
+  const app = express();
+  app.use(express.json());
+  app.use('/api/oauth', oauthRouter);
+  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', resolve); });
+  const addr = server.address();
+  base = `http://127.0.0.1:${typeof addr === 'object' && addr ? addr.port : 0}`;
+});
+afterAll(async () => { await new Promise<void>((resolve) => server.close(() => resolve())); });
+
+beforeEach(() => {
+  state.app = {
+    id: 'app-1', name: 'Test App', clientId: 'client-1', appType: 'confidential',
+    redirectUris: ['https://app.example.com/cb'], allowedScopes: ['openid', 'profile'],
+  };
+  vi.clearAllMocks();
+});
+
+
+const CB = encodeURIComponent('https://app.example.com/cb');
+const GET_BASE = `client_id=client-1&redirect_uri=${CB}&response_type=code`;
+
+async function get(extraQuery: string): Promise<{ status: number; message: string | undefined }> {
+  const res = await fetch(`${base}/api/oauth/authorize?${GET_BASE}${extraQuery}`, { redirect: 'manual' });
+  const text = await res.text();
+  let message: string | undefined;
+  try { message = JSON.parse(text)?.error?.message; } catch { /* html consent page */ }
+  return { status: res.status, message };
+}
+
+describe('KS-1797: GET /api/oauth/authorize refuses a repeated state or code_challenge', () => {
+  it('RED KS-1797 R1 GET with a repeated state parameter is 400 invalid_request, not 500', async () => {
+    expect(await get('&state=xyz&state=second')).toEqual({ status: 400, message: 'invalid_request' });
+    expect(createAuthorizationCode).not.toHaveBeenCalled();
+  });
+
+  it('RED KS-1797 R2 GET with a repeated code_challenge parameter is 400 invalid_request, not 500', async () => {
+    expect(await get('&state=xyz&code_challenge=aaa&code_challenge=bbb')).toEqual({ status: 400, message: 'invalid_request' });
+    expect(createAuthorizationCode).not.toHaveBeenCalled();
+  });
+
+  it('CONTROL KS-1797 C1 GET with one state still serves the consent page', async () => {
+    expect((await get('&state=xyz')).status).toBe(200);
+  });
+
+  it('CONTROL KS-1797 C2 GET with no state still serves the consent page', async () => {
+    expect((await get('')).status).toBe(200);
+  });
+
+  it('CONTROL KS-1797 C3 GET with one code_challenge still serves the consent page', async () => {
+    expect((await get('&state=xyz&code_challenge=aaa')).status).toBe(200);
+  });
+
+  it('CONTROL KS-1797 C4 GET with a repeated scope is still 400 invalid_request (KS-1219)', async () => {
+    expect(await get('&state=xyz&scope=openid&scope=profile')).toEqual({ status: 400, message: 'invalid_request' });
+  });
+});
```
