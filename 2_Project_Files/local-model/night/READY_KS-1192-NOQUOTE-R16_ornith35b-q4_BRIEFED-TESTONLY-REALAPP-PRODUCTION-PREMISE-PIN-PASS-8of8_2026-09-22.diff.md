# READY — KS-1192-NOQUOTE-R16 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1192-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 04:37 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1192-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed4-drafter-precheck/1192NOQUOTE-R16/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 04:37 2026-09-22 by Wednesday after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1192-ornith35b-night/out.md.checker`, not typed).** Tip `64ab105132eada0621622acf4d6053bc59926780`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1192-real-app-production-erasure-door.test.ts` (new). `+` lines 144 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 4/4 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `R16` → red exactly ['RED KS-1192 - a connector WITHOUT subjects:erase is refused ', 'RED KS-1192 - the 307 for POST /api/gdpr/erasures carries th']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1192-ornith35b-night/input.json`. Brief: `night/briefs/KS-1192-NOQUOTE-R16.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1192-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1192-real-app-production-erasure-door.test.ts
@@ -0,0 +1,144 @@
+// KS-1192 (F-1011-6, the #1011 round-2 gate on KS-871): the ks871 real-app production cell stays green with its
+// vi.resetModules() removed (index.ts stays the test-mode module), and 0-upstream-hits cannot tell the erasure door
+// from CSRF. These cells import the REAL index.ts app under NODE_ENV=test, re-import it under NODE_ENV=production, and pin
+// the module-load witness (X-CSRF-Token from the index.ts CSRF mount, the Secure XSRF-TOKEN cookie from csrf.ts) and the
+// refusal code the door itself emits.
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import http from 'http';
+import jwt from 'jsonwebtoken';
+import type { AddressInfo } from 'net';
+
+const rec = vi.hoisted(() => ({ calls: [] as Array<{ sql: string; params: unknown[] }> }));
+vi.mock('../db', async (orig) => ({
+  ...((await orig()) as Record<string, unknown>),
+  isDbAvailable: () => true,
+  query: async (sql: string, params: unknown[] = []) => { rec.calls.push({ sql, params }); return { rows: [], rowCount: 0 }; },
+}));
+
+type Reply = { status: number; location: string | undefined; csrfHeader: boolean; secureCookie: boolean; code: unknown; required: unknown };
+type Gateway = { server: http.Server; url: string };
+
+const seen: string[] = [];
+let recorder: http.Server | undefined;
+let recorderUrl = '';
+
+async function listen(server: http.Server): Promise<string> {
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  return `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+}
+
+async function closeServer(server: http.Server | undefined): Promise<void> {
+  if (!server) return;
+  server.closeAllConnections();
+  await new Promise<void>((r) => server.close(() => r()));
+}
+
+/** POST an empty JSON body; read the two module-load witnesses and the error code of the refusal body. */
+function post(gateway: Gateway | undefined, path: string, ua: string, scopes: string[]): Promise<Reply> {
+  const token = jwt.sign(
+    { userId: 'c0000000-0000-4000-8000-00000000000c', role: 'connector', authMethod: 'api_key', email: 'connector@ks1192.test', scopes,
+      tenantId: 'a0000000-0000-4000-8000-000000000001', organizationId: 'd0000000-0000-4000-8000-00000000000d', verificationLevel: 'BASIC' },
+    process.env.__TEST_JWT_PRIVATE_PEM as string, { algorithm: 'RS256', expiresIn: '10m' });
+  const target = new URL(gateway!.url);
+  return new Promise((resolve, reject) => {
+    const req = http.request({ hostname: target.hostname, port: target.port, path, method: 'POST', agent: false,
+      headers: { 'content-type': 'application/json', 'content-length': '2', 'user-agent': ua, authorization: 'Bearer ' + token } }, (res) => {
+      const chunks: Buffer[] = [];
+      res.on('data', (c: Buffer) => chunks.push(c));
+      res.on('end', () => {
+        let error: { code?: unknown; required?: unknown } = {};
+        try { error = JSON.parse(Buffer.concat(chunks).toString())?.error ?? {}; } catch { error = {}; }
+        const cookies = res.headers['set-cookie'] ?? [];
+        resolve({ status: res.statusCode ?? 0, location: res.headers.location, csrfHeader: typeof res.headers['x-csrf-token'] === 'string',
+          secureCookie: cookies.some((c) => c.startsWith('XSRF-TOKEN=') && c.split(';').map((p) => p.trim()).includes('Secure')),
+          code: error.code, required: error.required });
+      });
+    });
+    req.on('error', reject);
+    req.end('{}');
+  });
+}
+
+/** The audit INSERT whose user_agent (param 7) is ua, read back as action / resource_type / details.path. */
+async function waitForRow(ua: string): Promise<{ action: unknown; resourceType: unknown; path: unknown } | undefined> {
+  for (let waited = 0; waited < 3000; waited += 25) {
+    const call = rec.calls.find((c) => /INSERT INTO audit_logs/.test(c.sql) && c.params[7] === ua);
+    if (call) return { action: call.params[3], resourceType: call.params[4], path: (JSON.parse(String(call.params[8])) as { path?: unknown }).path };
+    await new Promise((r) => setTimeout(r, 25));
+  }
+  return undefined;
+}
+
+/** Stub the env, reset the module registry, then import the REAL app, so index.ts and csrf.ts evaluate under the stubs. */
+async function bootApp(env: Record<string, string>): Promise<Gateway> {
+  for (const [key, value] of Object.entries(env)) vi.stubEnv(key, value);
+  vi.resetModules();
+  const app = (await import('../index')).default;
+  const server = http.createServer(app as http.RequestListener);
+  return { server, url: await listen(server) };
+}
+
+beforeAll(async () => {
+  recorder = http.createServer((req, res) => {
+    req.resume();
+    req.on('end', () => { seen.push(`${req.method} ${req.url}`); res.writeHead(200, { 'content-type': 'application/json' }); res.end('{}'); });
+  });
+  recorderUrl = await listen(recorder);
+});
+
+afterAll(async () => {
+  await closeServer(recorder);
+  vi.unstubAllEnvs();
+});
+
+describe('KS-1192 control - the real app imported under NODE_ENV=test carries no production witness', () => {
+  let gateway: Gateway | undefined;
+  beforeAll(async () => {
+    gateway = await bootApp({ NODE_ENV: 'test', ORIGINATE_SERVICE_URL: recorderUrl, GATEWAY_VOUCH_SECRET: '', SUBJECTS_ERASE_SCOPE_ENFORCED: 'true' });
+  }, 60000);
+  afterAll(async () => { await closeServer(gateway?.server); });
+
+  it('GREEN KS-1192 control - NODE_ENV=test: no X-CSRF-Token, no Secure cookie, and the connector without subjects:erase is refused 403', async () => {
+    const hitsBefore = seen.length;
+    const res = await post(gateway, '/api/gdpr/erasures', 'ks1192-test-refused', ['documents:read']);
+    expect([res.csrfHeader, res.secureCookie], 'the module-load witness under NODE_ENV=test').toEqual([false, false]);
+    expect(res.status).toBe(403);
+    expect(seen.length - hitsBefore).toBe(0);
+  });
+});
+
+describe('KS-1192 real app re-imported under NODE_ENV=production - the mode is pinned and the 403 is the erasure door', () => {
+  let gateway: Gateway | undefined;
+  beforeAll(async () => {
+    gateway = await bootApp({
+      NODE_ENV: 'production', CSRF_SECRET: 'ks1192-stub-csrf-not-a-real-secret', DATABASE_URL: 'postgres://ks1192:ks1192@127.0.0.1:1/ks1192',
+      REDIS_URL: 'redis://127.0.0.1:1', ENABLE_TEST_TOKENS: '', ENABLE_MOCK_ENDPOINTS: '', ORIGINATE_SERVICE_URL: recorderUrl,
+      GATEWAY_VOUCH_SECRET: '', SUBJECTS_ERASE_SCOPE_ENFORCED: 'true',
+    });
+  }, 60000);
+  afterAll(async () => { await closeServer(gateway?.server); });
+
+  it('RED KS-1192 - the 307 for POST /api/gdpr/erasures carries the production module-load witness: X-CSRF-Token and a Secure cookie', async () => {
+    const res = await post(gateway, '/api/gdpr/erasures', 'ks1192-prod-307', ['documents:read']);
+    expect([res.csrfHeader, res.secureCookie], 'the module-load witness: index.ts CSRF mount, csrf.ts Secure cookie').toEqual([true, true]);
+    expect(res.status, 'production redirects the unversioned path').toBe(307);
+    expect(res.location).toBe('/api/v1/gdpr/erasures');
+  });
+
+  it('RED KS-1192 - a connector WITHOUT subjects:erase is refused by the door (403 INSUFFICIENT_SCOPE) under the witness, audited gdpr.create', async () => {
+    const hitsBefore = seen.length;
+    const res = await post(gateway, '/api/v1/gdpr/erasures', 'ks1192-prod-refused', ['documents:read']);
+    expect([res.csrfHeader, res.secureCookie], 'the module-load witness on the refusal').toEqual([true, true]);
+    expect([res.status, res.code, res.required], 'the refusal is the erasure door, not CSRF').toEqual([403, 'INSUFFICIENT_SCOPE', 'subjects:erase']);
+    expect(seen.length - hitsBefore, 'nothing reached originate').toBe(0);
+    expect(await waitForRow('ks1192-prod-refused')).toEqual({ action: 'gdpr.create', resourceType: 'gdpr', path: '/api/gdpr/erasures' });
+  });
+
+  it('GREEN KS-1192 control - a connector WITH subjects:erase passes the door: 200 from originate, one upstream hit, audited gdpr.create', async () => {
+    const hitsBefore = seen.length;
+    const res = await post(gateway, '/api/v1/gdpr/erasures', 'ks1192-prod-admitted', ['documents:read', 'subjects:erase']);
+    expect(res.status, 'originate answered').toBe(200);
+    expect(seen.slice(hitsBefore), 'the upstream hit').toEqual(['POST /api/v1/gdpr/erasures']);
+    expect(await waitForRow('ks1192-prod-admitted')).toEqual({ action: 'gdpr.create', resourceType: 'gdpr', path: '/api/gdpr/erasures' });
+  });
+});
```
