# READY — KS-871 PART A of two (capture `auditPath = req.originalUrl.split('?')[0]` at entry + `details.path` at :280 reads it) — Ornith ornith:35b (Q4_K_M) output of 2026-09-14 (`runs/2026-09-14_ks871-ornith35b`, PASS 7/7 then at the 09-14 tip), RE-CHECKED by Wednesday 15:42 at develop M55 48e65c435 under the Part-A brief (`briefs/split_871A/KS-871.md`): PASS 7/7 — audit.ts is byte-identical between the two tips (git log empty). 1 🔴 red at the tip (details.path '/' → '/api/gdpr/erasures') / control green / 2 green after / suite Δ 0 / tsc 0. The 09-15 rounds failed this ticket ten times only because the checklist demanded :108 in the same emission — :108 is Part B, a separate READY. A Secuura seat raises A + B as ONE PR.
# Source read by Wednesday: the product hunk inserts the capture near the top of the middleware body (after the entry gates, before the res.json wrap — equivalent to the brief's E1 position) and changes exactly :280 `path: req.path,` → `path: auditPath,` with a trailing comment; :108, :206, :274 untouched. The test drives the real proxy route with the KS-843 door (FLAG on, ROLE_ONLY user → 403) and reads the INSERT's details JSON from the query mock. Re-check dir: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/79db8c58-5a83-4ef0-8864-b9fc6da6f28e/scratchpad/recheck_871A.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts b/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
index 1234567..abcdefg 100644
--- a/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
@@ -203,6 +203,8 @@
     const start = Date.now();
 
+    // KS-871: capture the path once at entry — req.path is trimmed by express after the response is sent, so we use req.originalUrl instead.
+    const auditPath = req.originalUrl.split('?')[0];
+
     // Wrap res.json so the login-success path can extract the userId from the
     // response body. Without this, /api/auth/login audit entries have a null
     // actor — defeating the whole point of the audit log for the most
@@ -277,7 +279,7 @@
           const details = JSON.stringify({
             method: req.method,
-            path: req.path,
+            path: auditPath, // KS-871: use the captured path, not req.path (which is trimmed after response)
             status: res.statusCode,
             durationMs: Date.now() - start,
             tenantId: u?.tenantId || null,
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks871-audit-path-captured-at-entry.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks871-audit-path-captured-at-entry.test.ts
new file mode 100644
index 0000000..1234567
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks871-audit-path-captured-at-entry.test.ts
@@ -0,0 +1,95 @@
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
+describe('KS-871 — audit path must be captured at entry', () => {
+  it('🔴 KS-871 — refused erasure is audited with the full path, not the trimmed remainder', async () => {
+    process.env[FLAG] = 'true';
+    const query = vi.fn(async () => ({ rows: [] }));
+    const status = await drive(ROLE_ONLY, 'POST', '/api/gdpr/erasures', query);
+    expect(status).toBe(403);
+    await pollQueryCalls(query);
+    const params = query.mock.calls[0][1] as unknown[];
+    const details = JSON.parse(params[8] as string);
+    expect(details.path).toBe('/api/gdpr/erasures');
+  });
+
+  it('CONTROL — admitted erasure is audited with the full path', async () => {
+    delete process.env[FLAG];
+    const query = vi.fn(async () => ({ rows: [] }));
+    const status = await drive(WITH_SCOPE, 'POST', '/api/gdpr/erasures', query);
+    expect(status).toBe(200);
+    expect(received.length).toBe(1);
+    await pollQueryCalls(query);
+    const params = query.mock.calls[0][1] as unknown[];
+    const details = JSON.parse(params[8] as string);
+    expect(details.path).toBe('/api/gdpr/erasures');
+  });
+});
```
