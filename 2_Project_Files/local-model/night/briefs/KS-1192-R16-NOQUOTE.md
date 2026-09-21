# KS-1192 R16-NOQUOTE - the ONE rebrief (round 2 of 2, Kam's 2026-09-16 counter) of the KS-1192 test-only pin, re-derived at develop 64ab10513 (written 04:14 on 2026-09-22 by Wednesday's feed4 drafter from index.ts:380-395 read at the tip and the R15 brief KS-1192-R15-R15.md read whole)
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1192-real-app-production-erasure-door.test.ts`
Tip: `64ab105132eada0621622acf4d6053bc59926780`
Runner: `vitest`

## Premises (measured by the feed4 drafter at 04:14:50 AEST, in a `--shared` scratchpad clone detached at 64ab10513; Wednesday re-derives before queueing)
- Why a rebrief: round 1 (run `runs/2026-09-17_ks1192-ornith35b-night`, PASS 7/7 at 523f283c6) reproduced 143 of 144 lines; the one miss was line 84, where the brief carried `res.end('{"recorder":true}')` and the model emitted a backslash-escaped copy - the backslash-in-expected_plus class (IMPROVEMENTS 2026-09-22 02:28 / 02:35). The R15 re-brief (`KS-1192-R15-R15.md`) carried that escaped line itself and was HELD OUT on 09-21 for the same reason; it was never queued. This is the one rebrief the file gets: a FAIL here goes to a Claude seat, not a third brief.
- What changed in the fence vs round 1 (SAME cells, SAME tamper, SAME controls): line 84 now ends `res.end('{}'); });` (the recorder answers 200 with an empty JSON object - the control cell asserts the 200 and the upstream hit, never the body); the header comment line 2 reads `0-upstream-hits` instead of a double-quoted phrase; three comment lines (4, 5, 36) lose an apostrophe. Measured over the 144 `+` lines: double-quote characters 0, backslashes 0, non-ASCII 0, every single-quoted string balanced.
- The test file is ABSENT at 64ab10513 - ONE NEW FILE (`ls __tests__ | grep -c ks1192` = 0). Mode NEW.
- Tamper line `index.ts:387` at 64ab10513 is `if (NODE_ENV !== 'test') {` and is whole-line unique in the file (count 1 by `grep -c -x -F`). Same line and text as round 1 and R15.
- Typecheck (the 16th round's per-file method: a temp tsconfig extending `services/api-gateway/tsconfig.json`, files=[this file], noEmit, types node + vitest/globals, `npx tsc -p`): 0 errors in the file, 0 total; a planted TS2322 on a copy of the file was CAUGHT. Log: `runs/2026-09-22_feed4-drafter-precheck/typecheck/typecheck_feed4.log`.

## What is wrong (one paragraph)
The ks871 real-app production cell (`ks871-real-app-canonical-audit-rows.test.ts`) does not pin its own production premise: with `vi.resetModules()` removed it stays 3/3 green while `index.ts` stays the test-mode module, and its 0-upstream-hits assertion cannot tell the erasure door from a CSRF 403. The product is right at the tip. These cells import the REAL `index.ts` app under NODE_ENV=test (control), re-import it under NODE_ENV=production, and pin the module-load witness (X-CSRF-Token from the index.ts CSRF mount at :387-389, the Secure XSRF-TOKEN cookie from csrf.ts) and the refusal code the door emits (403 INSUFFICIENT_SCOPE, required subjects:erase, 0 upstream hits, audited gdpr.create). NOT in this task: the ks871 file (untouched), any product file.

## THE MODE - read this twice
TEST-ONLY, ONE NEW FILE: your diff contains EXACTLY ONE file, the NEW test file above: `--- /dev/null` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1192-real-app-production-erasure-door.test.ts` then ONE `@@ -0,0 +1,144 @@` hunk, every line `+`, no context, no `-`. No product hunk. Copy every `+` line byte for byte: no double quote anywhere, no backslash anywhere - the fence is written so that none is needed.

## The exact change
```
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

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `RED KS-1192 - the 307 for POST /api/gdpr/erasures carries the production module-load witness: X-CSRF-Token and a Secure cookie`
- `RED KS-1192 - a connector WITHOUT subjects:erase is refused by the door (403 INSUFFICIENT_SCOPE) under the witness, audited gdpr.create`
- `GREEN KS-1192 control - NODE_ENV=test: no X-CSRF-Token, no Secure cookie, and the connector without subjects:erase is refused 403`  (CONTROL - green on both trees)
- `GREEN KS-1192 control - a connector WITH subjects:erase passes the door: 200 from originate, one upstream hit, audited gdpr.create`  (CONTROL - green on both trees)

## Tampers
### R16
File: `Blockchain/Dev/services/api-gateway/src/index.ts`
Line: 387
From:
```
if (NODE_ENV !== 'test') {
```
To:
```
if (NODE_ENV !== 'test' && NODE_ENV !== 'production') {
```
Reds: `RED KS-1192 - the 307 for POST /api/gdpr/erasures carries the production module-load witness: X-CSRF-Token and a Secure cookie`, `RED KS-1192 - a connector WITHOUT subjects:erase is refused by the door (403 INSUFFICIENT_SCOPE) under the witness, audited gdpr.create`
(Under the tamper the production import mounts no CSRF: both RED cells fail on their FIRST assertion, the `[csrfHeader, secureCookie]` witness `[false, false]` vs `[true, true]` - an assertion red. The two controls never read the witness as true - the test-mode control asserts `[false, false]`, which the tamper does not change, and the with-scope control asserts the 200 and the upstream hit only.)

## Controls
- `GREEN KS-1192 control - NODE_ENV=test: no X-CSRF-Token, no Secure cookie, and the connector without subjects:erase is refused 403`
- `GREEN KS-1192 control - a connector WITH subjects:erase passes the door: 200 from originate, one upstream hit, audited gdpr.create`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/api-gateway/src/__tests__/ks1192-real-app-production-erasure-door.test.ts`); the header `@@ -0,0 +1,144 @@` (144 is the count of `+` lines - count them); no double quote, no `\$` / `\u` / backslash of any kind in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
