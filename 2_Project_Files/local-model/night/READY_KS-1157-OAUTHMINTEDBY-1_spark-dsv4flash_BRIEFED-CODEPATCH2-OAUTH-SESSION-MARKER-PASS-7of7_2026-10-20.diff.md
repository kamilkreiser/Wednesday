# READY — KS-1157-OAUTHMINTEDBY-1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1157_p1/out.md.checker/patch.diff`** (from `ls` at 09:55 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1157_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1157_p1/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1157_p1/out.md.checker/section_3.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1157_p1/out.md.checker/section_4.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1157_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1157_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:55 2026-10-20 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1157_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `89956fe92956a810f6821fdee09915f087feea7b`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/types/index.ts , Blockchain/Dev/services/auth/src/services/session.ts , Blockchain/Dev/services/auth/src/routes/oauth.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1157-a-session-minted-by-an-oauth-grant-carries-a-marker.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/types/index.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1157-a-session-minted-by-an-oauth-grant-carries-a-marker.test.ts` (test) — equal to numstat.out's set (4 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	0	Blockchain/Dev/services/auth/src/types/index.ts
2	0	Blockchain/Dev/services/auth/src/services/session.ts
2	2	Blockchain/Dev/services/auth/src/routes/oauth.ts
244	0	Blockchain/Dev/services/auth/src/__tests__/ks1157-a-session-minted-by-an-oauth-grant-carries-a-marker.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `[no PASS A3c line in checker.out — CODE_PATCH2: the checker skips A3c/A3i and asserts per-file A3x instead; checker.out PASS A3x verbatim: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0)`]` — no expected_plus in the input; not re-measured here.
- A3i line absent from checker.out (not claimed)
- CODE_PATCH2 (rung 3, 3 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/types/index.ts`, `Blockchain/Dev/services/auth/src/services/session.ts`, `Blockchain/Dev/services/auth/src/routes/oauth.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1157-a-session-minted-by-an-oauth-grant-carries-a-marker.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/types/index.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/services/session.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/routes/oauth.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1157-a-session-minted-by-an-oauth-grant-carries-a-marker.test.ts 244 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=4 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/types/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/services/session.ts` (hunks=2, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/auth/src/routes/oauth.ts` (hunks=2, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- section 4 `section_4.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1157-a-session-minted-by-an-oauth-grant-carries-a-marker.test.ts` (hunks=1, miscount=0; applied file per `section_4.opts`: `section_4.diff`, git-apply options: `(none — strict)`; `apply_check_strict_4.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=4 of total=7; red cell(s): ['KS-1157 route cells - both OAuth grants mark the session they create RED KS-1157 R1: the authorization_code grant creates its session with the browser clientType and the oauth marker', 'KS-1157 route cells - both OAuth grants mark the session they create RED KS-1157 R2: the refresh_token grant creates its session with the browser clientType and the oauth marker', 'KS-1157 service cells - the marker is stored and read back RED KS-1157 R3: a session created with the oauth marker is stored with it and getSession returns it', 'KS-1157 service cells - the marker is stored and read back RED KS-1157 R4: the marker is a field of its own: the oauth session keeps clientType browser, so the KS-43 cohorts are untouched']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 3 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1096 failed=0 | after: total=1103 failed=0` · `NEW reds: []` [baseline_suite.json total=1096 failed=0; after_suite.json total=1103 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=4 products=3 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/types/index.ts` (+2/-0 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1157-a-session-minted-by-an-oauth-grant-carries-a-marker.test.ts` (+244/-0); 4 files in all (code_patch2: products Blockchain/Dev/services/auth/src/types/index.ts, Blockchain/Dev/services/auth/src/services/session.ts, Blockchain/Dev/services/auth/src/routes/oauth.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict); section 4 `section_4.diff`: `git apply -p1` (strict) — at the tip `89956fe92956a810f6821fdee09915f087feea7b` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1157_p1/input.json`. Brief (given by --brief; its `# ` heading names KS-1157): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1157_p1/KS-1157.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1157_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/types/index.ts b/Blockchain/Dev/services/auth/src/types/index.ts
index 9b0b4f08a..8b9e82723 100644
--- a/Blockchain/Dev/services/auth/src/types/index.ts
+++ b/Blockchain/Dev/services/auth/src/types/index.ts
@@ -220,2 +220,4 @@
   clientType?: 'browser' | 'native' | 'api';
+  // KS-1157: set only on a session minted by an OAuth grant, so a future deploy-step denylist can select those sessions. Orthogonal to clientType.
+  mintedBy?: 'oauth';
   expiresAt: Date;
diff --git a/Blockchain/Dev/services/auth/src/services/session.ts b/Blockchain/Dev/services/auth/src/services/session.ts
index 16848a319..6df9ef629 100644
--- a/Blockchain/Dev/services/auth/src/services/session.ts
+++ b/Blockchain/Dev/services/auth/src/services/session.ts
@@ -133,2 +133,3 @@
   clientType: ClientType = 'browser',
+  mintedBy?: 'oauth',
 ): Promise<Session> {
@@ -147,2 +148,3 @@
     clientType,
+    ...(mintedBy ? { mintedBy } : {}),
     expiresAt,
diff --git a/Blockchain/Dev/services/auth/src/routes/oauth.ts b/Blockchain/Dev/services/auth/src/routes/oauth.ts
index 87f2103ef..ee5a62f49 100644
--- a/Blockchain/Dev/services/auth/src/routes/oauth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/oauth.ts
@@ -968,3 +968,3 @@
       // clients can re-issue under 'api' if they want single-session.
-      const session = await createSession(user, req.ip, req.get('user-agent'), undefined, 'browser');
+      const session = await createSession(user, req.ip, req.get('user-agent'), undefined, 'browser', 'oauth');
       // KS-823: the pair is bound to the client that redeemed the code — the
@@ -1077,3 +1077,3 @@
       // Default to 'browser' to match the original session's policy.
-      const session = await createSession(user, req.ip, req.get('user-agent'), undefined, 'browser');
+      const session = await createSession(user, req.ip, req.get('user-agent'), undefined, 'browser', 'oauth');
       // KS-823: the re-issued pair stays bound to the same client.
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1157-a-session-minted-by-an-oauth-grant-carries-a-marker.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1157-a-session-minted-by-an-oauth-grant-carries-a-marker.test.ts
new file mode 100644
index 000000000..a8c779722
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1157-a-session-minted-by-an-oauth-grant-carries-a-marker.test.ts
@@ -0,0 +1,244 @@
+// =============================================================================
+// KS-1157 - a session minted by an OAuth grant carries a marker (`mintedBy: 'oauth'`).
+// =============================================================================
+//
+// Before: both OAuth grants (authorization_code and refresh_token) called
+// createSession(user, ip, ua, undefined, 'browser') and nothing on the stored session said "an OAuth grant minted this", so a
+// deploy-step denylist that must be selective (OAuth sessions only, interactive logins untouched) had no enumerable target set.
+// After: createSession takes an optional sixth argument `mintedBy` and stores it on the session ONLY when given; both OAuth grants
+// pass 'oauth'. The marker is a field of its own: clientType stays 'browser' for those sessions, so the KS-43 eviction cohorts are
+// not touched. No cutoff is added (Kam's 2026-09-14 ruling: the forward-only window is accepted).
+//
+// Two layers in one file: the ROUTE cells drive POST /api/oauth/token over a raw socket (the ks1150 harness) and read what the
+// grant handed to createSession; the SERVICE cells run the real createSession over an in-memory Redis stand-in and read the
+// session back through the real getSession.
+// =============================================================================
+
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import express from 'express';
+import net from 'node:net';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+
+const silent = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
+vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent, validateEnv: vi.fn() }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silent, createLogger: () => silent }));
+
+const ACTIVE_USER = {
+  id: 'user-1157', email: 'u1157@secuura.local', status: 'ACTIVE', role: 'OWNER',
+  verificationLevel: 'BASIC', mfaEnabled: false, tenantId: 'ten-1', organizationId: 'org-1',
+};
+
+const world = vi.hoisted(() => ({
+  appRow: null as null | Record<string, unknown>,
+  codeRow: null as null | Record<string, unknown>,
+}));
+
+vi.mock('../db', () => ({
+  query: vi.fn(async (sql: string, params?: unknown[]) => {
+    if (sql.includes('auth_find_oauth_app_by_client_id')) {
+      const want = params?.[0];
+      return { rows: world.appRow && world.appRow.client_id === want ? [world.appRow] : [] };
+    }
+    if (sql.includes('FROM oauth_authorization_codes') && sql.includes('used = false')) {
+      const [code, clientId] = (params ?? []) as string[];
+      const r = world.codeRow;
+      const hit = r && r.code === code && r.client_id === clientId && r.used === false;
+      return { rows: hit ? [r] : [] };
+    }
+    if (sql.includes('UPDATE oauth_authorization_codes SET used = true')) {
+      if (world.codeRow) world.codeRow.used = true;
+      return { rows: [], rowCount: 1 };
+    }
+    return { rows: [], rowCount: 0 };
+  }),
+}));
+
+vi.mock('../services/oauth', async (importOriginal) => {
+  const real = await importOriginal<Record<string, unknown>>();
+  return { ...real, verifyClientSecret: vi.fn(async (_id: string, presented: string) => presented === 'the-secret') };
+});
+
+vi.mock('../repositories/userRepo', () => ({
+  getUserById: vi.fn(async () => null),
+  getUserByIdPreAuth: vi.fn(async () => ({ ...ACTIVE_USER })),
+  getUserByEmail: vi.fn(async () => null),
+  updateUser: vi.fn(async () => undefined),
+  getPlatformAdmin: vi.fn(async () => null),
+  reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
+  reencryptPlatformAdminMfaSecretIfLegacy: vi.fn(async () => undefined),
+}));
+
+// The route cells see a recording createSession; the service cells reach the real module through importActual.
+vi.mock('../services/session', () => ({
+  createSession: vi.fn(async () => ({ id: 'sess-1157' })),
+  getRedisClient: vi.fn(() => null),
+  validateSession: vi.fn(async () => true),
+  updateSessionActivity: vi.fn(async () => undefined),
+}));
+vi.mock('../services/jwt', () => ({
+  generateTokenPair: vi.fn(() => ({ accessToken: 'MINTED_1157', refreshToken: 'MINTED_1157_R', expiresIn: 900 })),
+  verifyRefreshToken: vi.fn((token: string) => {
+    if (token !== 'VALID_REFRESH_1157') throw new Error('invalid');
+    return { userId: ACTIVE_USER.id, sessionId: 'sess-old', jti: 'jti-1157', type: 'refresh', client_id: 'client-1' };
+  }),
+}));
+vi.mock('../services/refreshDenylist', () => ({ isRefreshJtiDenylisted: vi.fn(async () => false) }));
+vi.mock('../services/accountLockout', () => ({
+  isLockedOut: vi.fn(async () => false), recordFailure: vi.fn(async () => undefined),
+  recordSuccess: vi.fn(async () => undefined), clearFailures: vi.fn(async () => undefined),
+}));
+vi.mock('../middleware/authenticate', () => ({
+  authenticate: () => (req: Record<string, unknown>, _s: unknown, n: () => void) => {
+    (req as { user?: unknown }).user = { userId: 'user-1157', organizationId: 'org-1', tenantId: 'ten-1' };
+    n();
+  },
+}));
+vi.mock('../middleware/tenantGuc', () => ({ seedTenantGuc: (_r: unknown, _s: unknown, n: () => void) => n() }));
+vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
+
+let server: Server;
+let port: number;
+
+beforeAll(async () => {
+  const { oauthRouter } = await import('../routes/oauth');
+  const app = express();
+  app.use(express.json());
+  app.use('/api/oauth', oauthRouter);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  port = (server.address() as AddressInfo).port;
+});
+afterAll(async () => { await new Promise<void>((r) => server.close(() => r())); });
+
+function raw(method: string, path: string, body: unknown): Promise<{ status: number; body: string }> {
+  return new Promise((resolve, reject) => {
+    const payload = JSON.stringify(body);
+    const lines = [
+      `${method} ${path} HTTP/1.1`, 'Host: 127.0.0.1', 'Connection: close',
+      'Content-Type: application/json', `Content-Length: ${Buffer.byteLength(payload)}`, '', '',
+    ].join('\r\n');
+    const sock = net.connect(port, '127.0.0.1', () => sock.write(lines + payload));
+    const chunks: Buffer[] = [];
+    sock.on('data', (d: Buffer) => chunks.push(d));
+    sock.on('error', reject);
+    sock.on('end', () => {
+      const text = Buffer.concat(chunks).toString('utf8');
+      resolve({ status: Number(text.slice(9, 12)), body: text.slice(text.indexOf('\r\n\r\n') + 4) });
+    });
+  });
+}
+
+function appRow() {
+  return {
+    id: 'app-1', name: 'App', description: null, client_id: 'client-1',
+    client_secret_hash: '$argon2id$stub', redirect_uris: ['https://app.example.com/cb'],
+    allowed_scopes: ['openid', 'profile'], app_type: 'confidential',
+    organization_id: 'org-1', tenant_id: 'ten-1', is_active: true,
+    created_by: 'user-1157', created_at: new Date().toISOString(),
+  };
+}
+function codeRow() {
+  return {
+    code: 'THE_CODE', client_id: 'client-1', user_id: ACTIVE_USER.id,
+    redirect_uri: 'https://app.example.com/cb', scope: 'openid',
+    code_challenge: null, code_challenge_method: 'S256',
+    expires_at: new Date(Date.now() + 300_000).toISOString(), used: false,
+  };
+}
+const redeemCode = () => raw('POST', '/api/oauth/token', {
+  grant_type: 'authorization_code', code: 'THE_CODE', client_id: 'client-1',
+  redirect_uri: 'https://app.example.com/cb', client_secret: 'the-secret',
+});
+const refresh = () => raw('POST', '/api/oauth/token', {
+  grant_type: 'refresh_token', refresh_token: 'VALID_REFRESH_1157', client_id: 'client-1', client_secret: 'the-secret',
+});
+
+beforeEach(() => {
+  world.appRow = appRow(); world.codeRow = codeRow();
+  vi.clearAllMocks();
+});
+
+/** What the grant handed to createSession, as the trailing arguments after the user: (ip, userAgent, deviceId, clientType, mintedBy). */
+async function lastCreateSessionTail(): Promise<unknown[]> {
+  const { createSession } = await import('../services/session');
+  const calls = (createSession as unknown as { mock: { calls: unknown[][] } }).mock.calls;
+  return calls.length > 0 ? calls[calls.length - 1].slice(3) : ['NO createSession CALL'];
+}
+
+describe('KS-1157 route cells - both OAuth grants mark the session they create', () => {
+  it('RED KS-1157 R1: the authorization_code grant creates its session with the browser clientType and the oauth marker', async () => {
+    const r = await redeemCode();
+    expect(r.status, `body: ${r.body.slice(0, 200)}`).toBe(200);
+    expect(await lastCreateSessionTail()).toEqual([undefined, 'browser', 'oauth']);
+  });
+
+  it('RED KS-1157 R2: the refresh_token grant creates its session with the browser clientType and the oauth marker', async () => {
+    const r = await refresh();
+    expect(r.status, `body: ${r.body.slice(0, 200)}`).toBe(200);
+    expect(await lastCreateSessionTail()).toEqual([undefined, 'browser', 'oauth']);
+  });
+
+  it('CONTROL KS-1157 C1: both grants still mint a pair and the ACTIVE user path is unchanged', async () => {
+    const a = await redeemCode();
+    expect([a.status, a.body.includes('MINTED_1157')]).toEqual([200, true]);
+    world.codeRow = codeRow();
+    const b = await refresh();
+    expect([b.status, b.body.includes('MINTED_1157')]).toEqual([200, true]);
+  });
+});
+
+// The real session service over an in-memory Redis stand-in (only the commands createSession / getSession / revokeSession use).
+function fakeRedis() {
+  const kv = new Map<string, string>();
+  const sets = new Map<string, Set<string>>();
+  const setOf = (k: string) => { if (!sets.has(k)) sets.set(k, new Set()); return sets.get(k) as Set<string>; };
+  return {
+    kv,
+    smembers: async (k: string) => [...setOf(k)],
+    get: async (k: string) => kv.get(k) ?? null,
+    setex: async (k: string, _ttl: number, v: string) => { kv.set(k, v); return 'OK'; },
+    sadd: async (k: string, v: string) => { setOf(k).add(v); return 1; },
+    srem: async (k: string, v: string) => { setOf(k).delete(v); return 1; },
+    expire: async () => 1,
+    del: async (k: string) => { kv.delete(k); sets.delete(k); return 1; },
+  };
+}
+
+describe('KS-1157 service cells - the marker is stored and read back', () => {
+  let svc: typeof import('../services/session');
+  let redis: ReturnType<typeof fakeRedis>;
+
+  beforeEach(async () => {
+    svc = await vi.importActual<typeof import('../services/session')>('../services/session');
+    redis = fakeRedis();
+    svc.__setRedisForTesting(redis);
+  });
+
+  const user = ACTIVE_USER as unknown as Parameters<typeof import('../services/session')['createSession']>[0];
+
+  it('RED KS-1157 R3: a session created with the oauth marker is stored with it and getSession returns it', async () => {
+    const made = await svc.createSession(user, '127.0.0.1', 'ua', undefined, 'browser', 'oauth');
+    const back = await svc.getSession(made.id);
+    expect((back as unknown as Record<string, unknown>).mintedBy).toBe('oauth');
+    expect(JSON.parse(redis.kv.get(`sess:${made.id}`) as string).mintedBy).toBe('oauth');
+  });
+
+  it('RED KS-1157 R4: the marker is a field of its own: the oauth session keeps clientType browser, so the KS-43 cohorts are untouched', async () => {
+    const made = await svc.createSession(user, '127.0.0.1', 'ua', undefined, 'browser', 'oauth');
+    const back = await svc.getSession(made.id);
+    expect([back?.clientType, (back as unknown as Record<string, unknown>).mintedBy]).toEqual(['browser', 'oauth']);
+  });
+
+  it('CONTROL KS-1157 C2: an interactive session (no sixth argument) carries NO marker key at all', async () => {
+    const made = await svc.createSession(user, '127.0.0.1', 'ua', undefined, 'browser');
+    expect('mintedBy' in made).toBe(false);
+    expect('mintedBy' in JSON.parse(redis.kv.get(`sess:${made.id}`) as string)).toBe(false);
+  });
+
+  it('CONTROL KS-1157 C3: a native interactive session is unmarked and keeps its clientType', async () => {
+    const made = await svc.createSession(user, '127.0.0.1', 'ua', 'device-1', 'native');
+    const back = await svc.getSession(made.id);
+    expect([back?.clientType, 'mintedBy' in (back as object)]).toEqual(['native', false]);
+  });
+});
```
