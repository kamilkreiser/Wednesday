# READY — KS-871 PART B of two (`deriveAction` :108 reads `req.originalUrl.split('?')[0]`) — Ornith ornith:35b-q8_0 PASS 7/7, 2026-09-15 15:45 — tip develop M55 48e65c435. Run `2026-09-15_ks871-ornith35b-q8_0-night5`. The q4 sample (15:43, `…-night10`) replaced the COMMENT on :107 and left :108 untouched — A3b refused it by name (the neighbour-slip class, fourth time on this file); this q8 run is a RETRY (not a twin — Kam 13:08). 2 🔴 red at the tip (action 'unknown.create' → 'gdpr.create', resourceType 'unknown' → 'gdpr'; the trailing-slash POST too) / control green / 3 green after / suite Δ 0 / tsc 0. With Part A held, **KS-871 is COMPLETE** — a Secuura seat raises A + B as ONE PR.
# Source read by Wednesday: the product hunk is the brief's one-line replace at :108 exactly (signature :95, call :230, :274, :280 untouched); the cells are the brief's, reading INSERT params [3]/[4] from the query mock through the 09-14 driver (KS-843 door, FLAG on, ROLE_ONLY → 403; WITH_SCOPE → 200 control).

```diff
--- a/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
@@ -105,7 +105,7 @@ function deriveAction(req: Request): {
   : method === 'DELETE' ? 'delete'
     : method.toLowerCase();
 
-  const segments = req.path.replace(/\/+$/, '').split('/').filter(Boolean);
+  const segments = req.originalUrl.split('?')[0].replace(/\/+$/, '').split('/').filter(Boolean); // KS-871: req.path is trimmed by the time 'finish' fires
 
 --- /dev/null
 +++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts
@@ -0,0 +1,135 @@
+/**
+ * KS-871 — audit path must be captured at entry, not after response
+ */
+
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+import { createAuditMiddleware } from '../middleware/audit';
+import { createProxyRoutes } from '../routes/proxy';
+
+const FLAG = 'SUBJECTS_ERASE_SCOPE_ENFORCED';
+
+let upstream: http.Server;
+let upstreamPort = 0;
+let received: string[] = [];
+
+beforeAll(async () => {
+  upstream = http.createServer((req, res) => {
+    received.push(`${req.method} ${req.url}`);
+    res.writeHead(200, { 'content-type': 'application/json' });
+    res.end('{"ok":true}');
+  });
+  await new Promise<void>((r) => upstream.listen(0, '127.0.0.1', () => r()));
+  upstreamPort = (upstream.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  await new Promise<void>((r) => upstream.close(() => r()));
+});
+
+beforeEach(() => {
+  received = [];
+});
+
+const ROLE_ONLY = {
+  userId: 'connector:test', role: 'connector', authMethod: 'api_key',
+  scopes: ['documents:read'], connectorId: 'conn-1', organizationId: 'org-1',
+};
+
+const WITH_SCOPE = { ...ROLE_ONLY, scopes: ['documents:read', 'subjects:erase'] };
+
+function buildApp(user: object, query: ReturnType<typeof vi.fn>) {
+  const authenticateToken = ((_required?: boolean) =>
+    ((req, _res, next) => {
+      (req as unknown as { user: object }).user = { ...user };
+      next();
+    }) as RequestHandler) as (required?: boolean) => RequestHandler;
+
+  const app = express();
+  app.use(express.json());
+  app.use(createAuditMiddleware({ query, isDbAvailable: () => true, log: () => {} }));
+  app.use(
+    createProxyRoutes({
+      services: { originate: { url: `http://127.0.0.1:${upstreamPort}`, name: 'originate' } },
+      authenticateToken,
+      log: () => {},
+    } as unknown as Parameters<typeof createProxyRoutes>[0]),
+  );
+  return app;
+}
+
+async function drive(user: object, method: 'POST' | 'GET', path: string, query: ReturnType<typeof vi.fn>): Promise<number> {
+  const server = buildApp(user, query).listen(0, '127.0.0.1');
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  const port = (server.address() as AddressInfo).port;
+  const status = await new Promise<number>((resolve) => {
+    const req = http.request(
+      { host: '127.0.0.1', port, path, method, headers: { 'content-type': 'application/json' } },
+      (res) => { res.resume(); resolve(res.statusCode ?? 0); },
+    );
+    req.on('error', () => resolve(-1));
+    req.end(method === 'POST' ? '{}' : undefined);
+  });
+  await new Promise<void>((r) => server.close(() => r()));
+  return status;
+}
+
+async function pollQueryCalls(query: ReturnType<typeof vi.fn>, timeout = 2000): Promise<void> {
+  const start = Date.now();
+  while (Date.now() - start < timeout) {
+    if (query.mock.calls.length > 0) return;
+    await new Promise((r) => setTimeout(r, 50));
+  }
+  throw new Error('query was never called within timeout');
+}
+
+describe('KS-871 — audit action derived from original URL', () => {
+  it('🔴 KS-871 B — a refused erasure is audited as gdpr.create, not unknown.create', async () => {
+    process.env[FLAG] = 'true';
+    try {
+      const query = vi.fn(async () => ({ rows: [] }));
+      const status = await drive(ROLE_ONLY, 'POST', '/api/gdpr/erasures', query);
+      expect(status).toBe(403);
+      await pollQueryCalls(query);
+      const params = query.mock.calls[0][1] as unknown[];
+      expect(params[3]).toBe('gdpr.create');
+      expect(params[4]).toBe('gdpr');
+    } finally {
+      delete process.env[FLAG];
+    }
+  });
+
+  it('🔴 KS-871 B — a refused erasure with a trailing slash derives its section too', async () => {
+    process.env[FLAG] = 'true';
+    try {
+      const query = vi.fn(async () => ({ rows: [] }));
+      const status = await drive(ROLE_ONLY, 'POST', '/api/gdpr/erasures/', query);
+      expect(status).toBe(403);
+      await pollQueryCalls(query);
+      const params = query.mock.calls[0][1] as unknown[];
+      expect(params[3]).toBe('gdpr.create');
+      expect(params[4]).toBe('gdpr');
+    } finally {
+      delete process.env[FLAG];
+    }
+  });
+
+  it('KS-871 B control — an admitted erasure is gdpr.create before and after', async () => {
+    process.env[FLAG] = 'true';
+    try {
+      const query = vi.fn(async () => ({ rows: [] }));
+      const status = await drive(WITH_SCOPE, 'POST', '/api/gdpr/erasures', query);
+      expect(status).toBe(200);
+      await pollQueryCalls(query);
+      const params = query.mock.calls[0][1] as unknown[];
+      expect(params[3]).toBe('gdpr.create');
+      expect(params[4]).toBe('gdpr');
+    } finally {
+      delete process.env[FLAG];
+    }
+  });
+});
```
