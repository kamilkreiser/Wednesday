# READY — KS-1234 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1234-ornith35b-night/out.md.checker/patch.diff`** (from `ls` of that dir at 22:50 2026-09-20). Strict `git apply --numstat` → `1 1 …/api-gateway/src/index.ts` + `94 0 …/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts`.

**Held 22:50 2026-09-20 by the 21:2x Wednesday seat after a source read.** Tip `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa`. TWO files: ONE product line in `index.ts` (`:413`, hunk `@@ -410,7 +410,7 @@`) + ONE new test file. **`Refs KS-1234`, never a closing word** — the ticket's production-boot 307 is a separate mechanism and stays open.

**What it fixes.** `POST /api/v1/documents` sent as `application/json` never answers: `shouldParseBody` (`:413`) judges `req.path` BEFORE the `/api/v1/` → `/api/` rewrite (`:561`), so `express.json` (`:416`) consumes the stream and `verification.ts:1128`'s hand parser waits for an `'end'` that never fires. The fix judges the alias by the path the rewrite gives it — one line, 1-for-1.

**Source read (Wednesday, same action):** the `+` line is byte-identical to the brief's; numstat 1/1 on the product file; **zero blank `+` lines in the product hunk** (the checker blind spot the drafter measured: an extra blank line PASSES A6 but reddens `packages/shared` ks781 — not hit here). Test 94 lines: drives the real gateway app over loopback with a fake originate; 🔴 the JSON create on `/api/v1/documents` answers 200 as `/api/documents` does (red at tip: `['no-answer', []]`), plus controls.

**Behaviour change to STATE at raise:** every `/api/v1/<proxyPath>` alias now skips express.json / urlencoded / sanitizeInput / detectSuspiciousRequests exactly like its `/api/` twin — a widening the ticket asks for, said in the PR body.

**Checker (22:47–22:49):** `RESULT: PASS (7/7)`; A2 mode per the run's log (the brief's blank-context line needed `ALLOW_BLANK_CONTEXT=1` at build). **Drafter's pre-queue measurements (scratch clone at the tip):** tip+test 1 failed/3 by assertion, fix 3/3, suite 674→677, tsc rc 0 both, **`packages/shared` ks781 231/231 both trees**; five wrong variants refused by the real checker at named gates (test_only A3, rewrite_site A3b, wrong_line A3b, regex_wrong A3c) and one blind spot recorded (newline_shift PASSes the checker, reddens shared).

**For the raise seat:** strict apply; numstat MUST read `1 1` on index.ts (STOP otherwise); run api-gateway vitest (677 expected) **AND `packages/shared` ks781 (231/231 expected — the checker's A6 does not run it)**; tsc; `Refs KS-1234`. **Partition tonight:** disjoint from Seat B 10th's three files (PR 3 is `startup-migrations.ts`, a different file in the same service) and from Seat A 15th's anchoring/**. Not added to Seat B's series (it holds "nothing beyond the three"); bank for the next raise seat or an addendum once B's READYs land.

**NOT TESTED:** the production-boot 307 (`NODE_ENV=production`; a read only); a real originate; kintsugi; the loopback listener is in-process (the checker's own A6 runs those 10 files).

---
--- a/Blockchain/Dev/services/api-gateway/src/index.ts
+++ b/Blockchain/Dev/services/api-gateway/src/index.ts
@@ -410,7 +410,7 @@ const proxyPaths = [
   '/api/onedrive', '/api/teams',
   '/api/users', '/api/sessions', '/api/issuer-certs',
 ];
-const shouldParseBody = (req: Request): boolean => !proxyPaths.some(p => req.path.startsWith(p));
+const shouldParseBody = (req: Request): boolean => !proxyPaths.some(p => req.path.replace(/^\/api\/v1\//, '/api/').startsWith(p)); // KS-1234: judge the /api/v1 alias by the path the rewrite below gives it
 
 // Default 1MB body limit; file upload routes get 10MB via their own middleware
 app.use((req, res, next) => { if (shouldParseBody(req)) express.json({ limit: '1mb' })(req, res, next); else next(); });
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts
@@ -0,0 +1,94 @@
+/**
+ * KS-1234 - POST /api/v1/documents sent as application/json never answers. index.ts decides
+ * shouldParseBody() on req.path BEFORE the /api/v1/ -> /api/ rewrite, so the alias of a proxyPaths
+ * route (/api/documents) is parsed by express.json, which consumes the request stream; the rewrite then
+ * hands the request to the hand-parsing POST /api/documents in routes/verification.ts, whose
+ * req.on('end') never fires. The real app is driven over loopback with a fake originate (the ks1238
+ * idiom): a connector key is validated and exchanged upstream, and what originate receives is recorded.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import http from 'http';
+import jwt from 'jsonwebtoken';
+import type { AddressInfo } from 'net';
+
+vi.mock('../db', async (orig) => {
+  const real = (await orig()) as Record<string, unknown>;
+  return { ...real, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }) };
+});
+
+const PRIV = process.env.__TEST_JWT_PRIVATE_PEM as string;
+const TENANT = 'a0000000-0000-4000-8000-000000000001';
+const CREATE_KEY = 'sk_ks1234_create_00000001';
+const BODY = JSON.stringify({ title: 'ks1234', contentHash: 'b'.repeat(64) });
+/** Every originate request: "<METHOD> <url> <title the JSON body carried, or ->" */
+const hits: string[] = [];
+
+function readBody(req: http.IncomingMessage): Promise<string> {
+  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
+}
+async function listen(server: http.Server): Promise<string> {
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  return 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+}
+function titleOf(body: string): string {
+  try { return String((JSON.parse(body) as Record<string, unknown>).title ?? '-'); } catch { return '-'; }
+}
+
+let upstream: http.Server | undefined;
+let gateway: http.Server | undefined;
+let gatewayUrl = '';
+beforeAll(async () => {
+  upstream = http.createServer(async (req, res) => {
+    const body = await readBody(req);
+    const json = (status: number, payload: unknown) => { res.writeHead(status, { 'content-type': 'application/json' }); res.end(JSON.stringify(payload)); };
+    const url = req.url || '';
+    if (url === '/api/keys/validate') {
+      const key = JSON.parse(body || '{}').key as string;
+      if (key === CREATE_KEY) return json(200, { data: { valid: true, connectorId: 'ks1234-create', scopes: ['documents:write'], organizationId: 'org-ks1234', tenantId: TENANT, rateLimit: 1000, rateLimitWindow: 60 } });
+      return json(200, { data: { valid: false } });
+    }
+    if (url === '/internal/connector-token') {
+      const token = jwt.sign({ userId: 'connector:ks1234-create', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector' }, PRIV, { algorithm: 'RS256', expiresIn: 600 });
+      return json(200, { success: true, data: { token, expiresIn: 600 } });
+    }
+    hits.push(String(req.method) + ' ' + url + ' ' + titleOf(body));
+    return json(200, { success: true, data: [] });
+  });
+  const upstreamUrl = await listen(upstream);
+  for (const name of ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM',
+    'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET']) vi.stubEnv(name + '_SERVICE_URL', upstreamUrl);
+  vi.stubEnv('NODE_ENV', 'test');
+  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
+  delete process.env.JWT_JWKS_URL;
+  vi.resetModules();
+  const app = (await import('../index')).default;
+  gateway = http.createServer(app as http.RequestListener);
+  gatewayUrl = await listen(gateway);
+}, 60000);
+afterAll(async () => {
+  for (const s of [gateway, upstream]) if (s) { s.closeAllConnections(); await new Promise<void>((r) => s.close(() => r())); }
+  vi.unstubAllEnvs();
+});
+
+/** Send the request through the real gateway with a 3 s bound (the gate's); returns [status or 'no-answer', originate hits]. */
+async function send(method: string, path: string, body?: string): Promise<[number | string, string[]]> {
+  const mark = hits.length;
+  let status: number | string = 'no-answer';
+  try {
+    const res = await fetch(gatewayUrl + path, { method, headers: { 'content-type': 'application/json', 'x-api-key': CREATE_KEY }, body, signal: AbortSignal.timeout(3000) });
+    await res.text();
+    status = res.status;
+  } catch { status = 'no-answer'; }
+  return [status, hits.slice(mark)];
+}
+describe('KS-1234: a JSON create on the /api/v1/documents alias must answer', () => {
+  it('control: POST /api/documents as application/json answers 200 and originate receives the body', async () => {
+    expect(await send('POST', '/api/documents', BODY)).toEqual([200, ['POST /api/documents ks1234']]);
+  }, 15000);
+  it('control: the /api/v1 alias itself is live - GET /api/v1/signatories answers 200 and reaches originate at /api/signatories', async () => {
+    expect(await send('GET', '/api/v1/signatories')).toEqual([200, ['GET /api/signatories -']]);
+  }, 15000);
+  it('🔴 KS-1234: POST /api/v1/documents as application/json answers 200 within the bound and originate receives the same body', async () => {
+    expect(await send('POST', '/api/v1/documents', BODY)).toEqual([200, ['POST /api/documents ks1234']]);
+  }, 15000);
+});
