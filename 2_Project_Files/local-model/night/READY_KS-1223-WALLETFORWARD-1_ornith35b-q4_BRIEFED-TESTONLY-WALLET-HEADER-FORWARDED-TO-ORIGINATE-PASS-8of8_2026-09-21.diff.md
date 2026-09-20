# READY — KS-1223-WALLETFORWARD-1 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1223-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 04:44 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1223-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1106rows-drafter-precheck/WALLETFORWARDUNPINNED/out.md.checker/patch.diff` rc 0, the 04:3x Wednesday seat).

**Held 04:44 2026-09-21 by the 04:3x Wednesday seat after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1223-ornith35b-night/out.md.checker`, not typed).** Tip `362e51fe0db7e73d5557924902763fe3f10fd8c7`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1223-wallet-forwarded-to-originate.test.ts` (new). `+` lines 82 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 2/2 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `WALLETNOTFORWARDED` → red exactly ['RED KS-1223: POST /api/documents with x-wallet-address: addr']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1223-ornith35b-night/input.json`. Brief: `night/briefs/KS-1223-WALLETFORWARD-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1223-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1223-wallet-forwarded-to-originate.test.ts
@@ -0,0 +1,82 @@
+/**
+ * KS-1223 - the FORWARD half of the wallet header: the gateway's hand-parsing POST /api/documents (routes/verification.ts,
+ * the "No workflow needed: forward to originate service" block) copies an inbound x-wallet-address onto the request it
+ * forwards to originate. The #1106-#1111 gate planted that line deleted and measured 0 red of 679: nothing pins the
+ * forward. The REAL gateway is driven over loopback with a fake originate that records the header it receives (the
+ * ks1234 idiom). A characterisation pin of TODAY's forward - whether the wallet should come from the caller's header
+ * at all is KS-1223's question for the owners, not this file's.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import http from 'http';
+import jwt from 'jsonwebtoken';
+import type { AddressInfo } from 'net';
+vi.mock('../db', async (orig) => {
+  const real = (await orig()) as Record<string, unknown>;
+  return { ...real, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }) };
+});
+const PRIV = process.env.__TEST_JWT_PRIVATE_PEM as string;
+const CREATE_KEY = 'sk_ks1223_create_00000001';
+const BODY = JSON.stringify({ title: 'ks1223', contentHash: 'c'.repeat(64) });
+/** Every originate document create: the x-wallet-address header it received, or '-' when none */
+const walletsSeen: string[] = [];
+function readBody(req: http.IncomingMessage): Promise<string> {
+  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
+}
+async function listen(server: http.Server): Promise<string> {
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  return 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+}
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
+      if (key === CREATE_KEY) return json(200, { data: { valid: true, connectorId: 'ks1223-create', scopes: ['documents:write'], organizationId: 'org-ks1223', tenantId: 'a0000000-0000-4000-8000-000000000001', rateLimit: 1000, rateLimitWindow: 60 } });
+      return json(200, { data: { valid: false } });
+    }
+    if (url === '/internal/connector-token') {
+      const token = jwt.sign({ userId: 'connector:ks1223-create', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector' }, PRIV, { algorithm: 'RS256', expiresIn: 600 });
+      return json(200, { success: true, data: { token, expiresIn: 600 } });
+    }
+    if (req.method === 'POST' && url === '/api/documents') walletsSeen.push(String(req.headers['x-wallet-address'] ?? '-'));
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
+/** POST /api/documents through the real gateway with the given extra headers, 3 s bound; returns [status or 'no-answer', wallets originate saw since the mark] */
+async function create(extra: Record<string, string>): Promise<[number | string, string[]]> {
+  const mark = walletsSeen.length;
+  let status: number | string = 'no-answer';
+  try {
+    const res = await fetch(gatewayUrl + '/api/documents', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': CREATE_KEY, ...extra }, body: BODY, signal: AbortSignal.timeout(3000) });
+    await res.text();
+    status = res.status;
+  } catch { status = 'no-answer'; }
+  return [status, walletsSeen.slice(mark)];
+}
+describe('KS-1223: the gateway forwards an inbound x-wallet-address to originate on POST /api/documents today', () => {
+  it('RED KS-1223: POST /api/documents with x-wallet-address: addr_client answers 200 and originate receives x-wallet-address: addr_client', async () => {
+    expect(await create({ 'x-wallet-address': 'addr_client' })).toEqual([200, ['addr_client']]);
+  }, 15000);
+  it('CONTROL: POST /api/documents without the header answers 200 and originate receives no x-wallet-address', async () => {
+    expect(await create({})).toEqual([200, ['-']]);
+  }, 15000);
+});
```
