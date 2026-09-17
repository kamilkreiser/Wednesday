# READY — KS-1090 R2-3 (NEW api-gateway test: the x-gateway-vouch header reaches originate and none of the other 17 proxied service keys; tamper routes/proxy.ts:275; 2 red cells + control + completeness) — Ornith ornith:35b q4, first sample, PASS 7/7 at 18:03 2026-09-17 on tip 581c9db0d (READY written 18:06)
# Source read by Wednesday: the model's 96 `+` lines IDENTICAL to the brief's test fence (python compare; a mutated copy unequal); one new file, no product change; apply STRICT; A4 under the tamper: BOTH declared reds (R1, R2) in failed_names (2 failed / 4 run), passed by the all-declared-reds checker.
# PR NOTES: `Refs KS-1090 (R2-3)`, NEVER Closes (R2-2 tsconfig half and R2-4 record stay open). TIER 2. RENAME the test file at raise — the builder name ks1090-api-gateway-originate-tsc-never-type.test.ts describes the ticket's OTHER half (e.g. ks1090-vouch-reaches-only-originate.test.ts). Brief night/briefs/KS-1090.md; search report night/briefs/NEXT_SEARCH_2026-09-17m.REPORT.md; run local-model/runs/2026-09-17_ks1090-ornith35b-night.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1090-api-gateway-originate-tsc-never-type.test.ts
@@ -0,0 +1,96 @@
+/**
+ * KS-1090 R2-3: the vouch mint-scope test pins two of the seventeen service
+ * keys that must never receive x-gateway-vouch. It checks analytics and auth
+ * only, so an allow-list widening that spares those two keys stays green.
+ * These cells drive the REAL createProxyRoutes with every service pointed at
+ * one local recorder, and pin for each non-originate key that no vouch
+ * arrives. The control proves originate does receive it, and that the
+ * factory reads exactly the eighteen service keys listed here.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+
+const EXPECTED_CELLS = 3;
+let CELLS_RUN = 0;
+const SECRET = 'ks1090-synthetic-vouch'.padEnd(64, '0');
+const NAMES = ['analytics', 'anchoring', 'auth', 'billing', 'dashboard', 'governance', 'kyc', 'm365', 'nft', 'originate', 'prism', 'referral', 'security', 'staking', 'timestamping', 'transfer', 'vcIssuer', 'wallet'];
+const keysRead = new Set<string>();
+const seen: Array<[string, boolean]> = [];
+
+let recorder: Server;
+let gateway: Server;
+let gatewayPort = 0;
+
+beforeAll(async () => {
+  recorder = http.createServer((req, res) => {
+    seen.push([req.url || '', req.headers['x-gateway-vouch'] === SECRET]);
+    res.writeHead(200, { 'Content-Type': 'application/json' });
+    res.end('{}');
+  });
+  recorder.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => recorder.once('listening', () => r()));
+  const url = 'http://127.0.0.1:' + (recorder.address() as AddressInfo).port;
+  const table: Record<string, unknown> = {};
+  for (const name of NAMES) table[name] = { name, url, healthPath: '/health', requiresAuth: false };
+  const services = new Proxy(table, {
+    get: (t, k) => {
+      if (typeof k === 'string') keysRead.add(k);
+      return t[k as string];
+    },
+  });
+  vi.stubEnv('GATEWAY_VOUCH_SECRET', SECRET);
+  vi.resetModules();
+  const { createProxyRoutes } = await import('../routes/proxy');
+  const caller: RequestHandler = (req, _res, next) => {
+    (req as { user?: unknown }).user = { userId: 'u-ks1090', role: 'user', tenantId: 't-ks1090' };
+    next();
+  };
+  const app = express();
+  app.use(createProxyRoutes({ services: services as never, authenticateToken: () => caller, log: () => undefined }));
+  gateway = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => gateway.once('listening', () => r()));
+  gatewayPort = (gateway.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  vi.unstubAllEnvs();
+  gateway.closeAllConnections();
+  recorder.closeAllConnections();
+  await new Promise<void>((r) => gateway.close(() => r()));
+  await new Promise<void>((r) => recorder.close(() => r()));
+});
+
+// send one GET per path through the gateway and answer what the recorder saw
+async function vouchedAt(paths: string[]): Promise<Array<[string, boolean]>> {
+  seen.length = 0;
+  for (const path of paths) {
+    const r = await fetch('http://127.0.0.1:' + gatewayPort + path);
+    await r.text();
+  }
+  return seen.slice();
+}
+
+describe('KS-1090 R2-3 - the vouch reaches originate and no other service key', () => {
+  it('KS-1090 R1 - anchoring, wallet, prism, timestamping, vcIssuer, kyc, nft and security receive no vouch', async () => {
+    CELLS_RUN += 1;
+    const rows = await vouchedAt(['/api/anchoring/p1', '/api/wallets/p1', '/api/did/p1', '/api/timestamps/p1', '/api/credentials/p1', '/api/kyc/p1', '/api/nft/p1', '/api/security/p1']);
+    expect(rows).toEqual([['/api/anchoring/p1', false], ['/api/wallets/p1', false], ['/api/did/p1', false], ['/api/timestamps/p1', false], ['/api/credentials/p1', false], ['/api/kyc/p1', false], ['/api/nft/p1', false], ['/api/p1', false]]);
+  });
+  it('KS-1090 R2 - m365, staking, referral, transfer, governance, dashboard and billing receive no vouch', async () => {
+    CELLS_RUN += 1;
+    const rows = await vouchedAt(['/api/teams/p2', '/api/stake/p2', '/api/milestones/p2', '/api/transfers/p2', '/api/governance/p2', '/api/dashboard/p2', '/api/billing/p2']);
+    expect(rows).toEqual([['/api/teams/p2', false], ['/api/stake/p2', false], ['/api/milestones/p2', false], ['/api/transfers/p2', false], ['/api/governance/p2', false], ['/api/dashboard/p2', false], ['/billing/p2', false]]);
+  });
+  it('KS-1090 CONTROL - originate receives the vouch, analytics and auth do not, and the factory reads these keys', async () => {
+    CELLS_RUN += 1;
+    const rows = await vouchedAt(['/originate/p3', '/api/analytics/p3', '/api/sessions/p3']);
+    expect([rows, [...keysRead].sort()]).toEqual([[['/p3', true], ['/api/analytics/p3', false], ['/api/sessions/p3', false]], NAMES]);
+  });
+  it('KS-1090 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});```
