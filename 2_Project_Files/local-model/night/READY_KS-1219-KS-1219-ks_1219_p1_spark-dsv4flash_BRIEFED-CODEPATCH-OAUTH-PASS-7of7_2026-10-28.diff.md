# READY — KS-1219-KS-1219-ks_1219_p1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1219_p1/out.md.checker/patch.diff`** (from `ls` at 13:50 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1219_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1219_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1219_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1219_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:50 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1219_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8894c7486f82f6eb682fecb879791f53312537b1`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/routes/oauth.ts , Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/oauth.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
10	0	Blockchain/Dev/services/auth/src/routes/oauth.ts
126	0	Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (10 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 10 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/routes/oauth.ts byte-exact incl. leading whitespace (apply mode strict): OK 10 line(s) byte-exact incl. leading whitespace (of 10; 10 line(s) added by the apply)` [a3i_indent.out: `OK 10 line(s) byte-exact incl. leading whitespace (of 10; 10 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/oauth.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1219: /api/oauth/authorize refuses an array-valued scope RED KS-1219 R1 GET with a repeated scope parameter is 400 invalid_request, not 500', 'KS-1219: /api/oauth/authorize refuses an array-valued scope RED KS-1219 R2 POST deny with a JSON array scope is 400 invalid_request, not 500', 'KS-1219: /api/oauth/authorize refuses an array-valued scope RED KS-1219 R3 POST approve with a JSON array scope is 400 invalid_request and mints no code']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1200 failed=0 | after: total=1206 failed=0` · `NEW reds: []` [baseline_suite.json total=1200 failed=0; after_suite.json total=1206 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +136/-0 test=src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/oauth.ts` (+10/-0 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts` (+126/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8894c7486f82f6eb682fecb879791f53312537b1` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1219_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1219_p1/KS-1219.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1219_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/oauth.ts b/Blockchain/Dev/services/auth/src/routes/oauth.ts
--- a/Blockchain/Dev/services/auth/src/routes/oauth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/oauth.ts
@@ -390,6 +390,16 @@
   // the all-unpermitted contrast. Removing the `?:` below reds exactly the two
   // no-scope cases. Narrowing this default is a decision to be made in those
   // cases first, not here.
+  // KS-1219: a repeated query parameter (?scope=a&scope=b) or a JSON array body reaches this resolver as an ARRAY whatever the compile-time cast at the handler says, and
+  // parseScopeString below would throw on it (an array has no split) and the handler would answer 500 server_error. A malformed request is a 400 invalid_request, the same
+  // existing message RULE 3 uses, so no published message changes.
+  if (scope !== undefined && typeof scope !== 'string') {
+    return {
+      ok: false,
+      message: 'invalid_request',
+      description: 'scope must be a single space- or comma-separated string',
+    };
+  }
   const requestedScopes = parseScopeString(scope);
   const grantedScopes = validateScopes(
     requestedScopes.length > 0 ? requestedScopes : app.allowedScopes,
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts
@@ -0,0 +1,126 @@
+// KS-1219: /api/oauth/authorize answered 500 server_error for an ARRAY-valued scope (a repeated query parameter, or a JSON array in the POST body): the compile-time
+// `as Record<string, string>` cast does nothing at run time, and parseScopeString calls `.split` on its argument. A malformed request is a 400 invalid_request. Each carrier is
+// driven through the real router on a loopback listener, with the same mocks as ks804-authorize-get-post-agree-per-rule.test.ts; a single string scope is the control.
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
+const CB = encodeURIComponent('https://app.example.com/cb');
+const GET_BASE = `client_id=client-1&redirect_uri=${CB}&response_type=code&state=xyz`;
+
+async function get(extraQuery: string): Promise<{ status: number; message: string | undefined }> {
+  const res = await fetch(`${base}/api/oauth/authorize?${GET_BASE}${extraQuery}`, { redirect: 'manual' });
+  const text = await res.text();
+  let message: string | undefined;
+  try { message = JSON.parse(text)?.error?.message; } catch { /* html consent page */ }
+  return { status: res.status, message };
+}
+
+async function post(body: Record<string, unknown>): Promise<{ status: number; message: string | undefined }> {
+  const res = await fetch(`${base}/api/oauth/authorize`, {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    redirect: 'manual',
+    body: JSON.stringify({ client_id: 'client-1', redirect_uri: 'https://app.example.com/cb', ...body }),
+  });
+  const text = await res.text();
+  let message: string | undefined;
+  try { message = JSON.parse(text)?.error?.message; } catch { /* redirect */ }
+  return { status: res.status, message };
+}
+
+describe('KS-1219: /api/oauth/authorize refuses an array-valued scope', () => {
+  it('RED KS-1219 R1 GET with a repeated scope parameter is 400 invalid_request, not 500', async () => {
+    expect(await get('&scope=openid&scope=profile')).toEqual({ status: 400, message: 'invalid_request' });
+  });
+
+  it('RED KS-1219 R2 POST deny with a JSON array scope is 400 invalid_request, not 500', async () => {
+    expect(await post({ action: 'deny', scope: ['openid', 'profile'] })).toEqual({ status: 400, message: 'invalid_request' });
+  });
+
+  it('RED KS-1219 R3 POST approve with a JSON array scope is 400 invalid_request and mints no code', async () => {
+    const reply = await post({ email: 'u@secuura.local', password: 'correct-horse', action: 'approve', scope: ['openid'] });
+    expect(reply).toEqual({ status: 400, message: 'invalid_request' });
+    expect(createAuthorizationCode).not.toHaveBeenCalled();
+  });
+
+  it('CONTROL KS-1219 C1 GET with one string scope still serves the consent page', async () => {
+    expect((await get('&scope=openid')).status).toBe(200);
+  });
+
+  it('CONTROL KS-1219 C2 GET with no scope still serves the consent page', async () => {
+    expect((await get('')).status).toBe(200);
+  });
+
+  it('CONTROL KS-1219 C3 POST deny with one string scope still redirects with access_denied', async () => {
+    expect((await post({ action: 'deny', scope: 'openid' })).status).toBe(302);
+  });
+});
```

## DECISION NOTE (source-read, Spark operator for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION (small): the guard is `typeof scope !== 'string'`, which also refuses JSON null/0/false
- The ticket's Recommendation: refuse a non-string scope with 400 `invalid_request`. The patch does that in `resolveAuthorizeClient` (services/auth/src/routes/oauth.ts, immediately before `parseScopeString(scope)`), reusing the existing `invalid_request` message (no new published message).
- Edge the raise seat should state to the owner: `parseScopeString` is `if (!scope) return []`, so before this patch a falsy non-string scope (JSON `null`, `0`, `false`) was treated like an absent scope (default = whole allow-list, KS-822 F-4). The new guard is `scope !== undefined && typeof scope !== 'string'`, so JSON `null`/`0`/`false` now answer 400 instead. Query-string and form values are always strings or arrays, so only a JSON body can hit that edge (POST). Arrays (the ticket's case) are the intended refusal; the falsy-scalar tightening is a side effect and is probably fine, but it is a behaviour change.
- Source-read: 10 lines inserted at the right place (after the RULE 4 comment block, before `parseScopeString`), nothing else touched; 3 RED cells (GET repeated param, POST deny array, POST approve array which mints no code) and 3 controls.
- Verdict: HOLD-WITH-DECISION (minor).
