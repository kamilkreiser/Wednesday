```diff
--- a/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
@@ -148,6 +148,8 @@ export function createAuditMiddleware(deps: AuditMiddlewareDeps): RequestHandler
 
     const start = Date.now();
 
+    // <KS-871>: capture once at entry; req.path is trimmed by express routing after next() returns, so we must not re-read it inside res 'finish'.
+    const auditPath = req.originalUrl.split('?')[0];
+
     // Wrap res.json so the login-success path can extract the userId from the
     // response body. Without this, /api/auth/login audit entries have a null
     // actor — defeating the whole point of the audit log for the most
@@ -164,7 +166,7 @@ export function createAuditMiddleware(deps: AuditMiddlewareDeps): RequestHandler
       void (async () => {
         try {
           if (!deps.isDbAvailable()) return;
-          const { action, resourceType, resourceId: routeResourceId } = deriveAction(req);
+          const { action, resourceType, resourceId: routeResourceId } = deriveAction({ ...req, path: auditPath });
 
           const u = (req as Request & { user?: { userId?: string; organizationId?: string; tenantId?: string } }).user;
           let userId: string | null = u?.userId || null;
@@ -277,7 +279,7 @@ export function createAuditMiddleware(deps: AuditMiddlewareDeps): RequestHandler
           const details = JSON.stringify({
             method: req.method,
-            path: req.path,
+            path: auditPath, // <KS-871> captured above; req.path would be trimmed here
             status: res.statusCode,
             durationMs: Date.now() - start,
             tenantId: u?.tenantId || null,

--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts
@@ -0,0 +1,69 @@
+/**
+ * =============================================================================
+ * KS-871 — `req.path` IS TRIMMED BY EXPRESS ROUTING AFTER THE GATE READS IT
+ * =============================================================================
+ * The gate reads `req.path` correctly on entry (:206). Inside `res.on('finish')`
+ * (`:224`) it calls `deriveAction(req)` which re-reads `req.path` — but by then
+ * Express has left it trimmed to the mount-relative remainder. A refused erasure
+ * is therefore audited with `/erasures` instead of `/api/gdpr/erasures`.
+ *
+ * This file drives `createAuditMiddleware` directly and asserts that the
+ * recorded path matches what was typed in the request URL, not what express
+ * left behind after routing.
+ * =============================================================================
+ */
+
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { AddressInfo } from 'node:net';
+import { createAuditMiddleware } from '../middleware/audit';
+
+const queryLog: unknown[][] = [];
+
+function buildApp() {
+  const deps = {
+    query: async (_sql: string, params: unknown[]) => {
+      queryLog.push(params);
+      return { rows: [] };
+    },
+    isDbAvailable: () => true,
+    log: () => {},
+  };
+  const app = express();
+  app.use(express.json());
+  app.use(createAuditMiddleware(deps));
+  return app;
+}
+
+async function drive(method: 'POST' | 'GET', url: string): Promise<number> {
+  const server = buildApp().listen(0, '127.0.0.1');
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  const port = (server.address() as AddressInfo).port;
+  const status = await new Promise<number>((resolve) => {
+    const req = http.request({ host: '127.0.0.1', port, path: url, method }, (res) => {
+      res.resume();
+      resolve(res.statusCode ?? -1);
+    });
+    req.end(method === 'POST' ? '{}' : undefined);
+  });
+  await new Promise<void>((r) => server.close(() => r()));
+  return status;
+}
+
+describe('KS-871 — audit log records the original request path, not the routed one', () => {
+  beforeEach(() => {
+    queryLog.length = 0;
+  });
+
+  it('CONTROL — middleware reaches the finish handler for a POST /api/documents call', async () => {
+    // Without this, every assertion below would be vacuous if the middleware
+    // never made it to `res.on('finish')`. A non-/api path returns before any
+    // write happens and proves nothing about what was recorded.
+    const status = await drive('POST', '/api/documents');
+    expect(status).toBe(403);
+    expect(queryLog.length).toBeGreaterThan(0);
+  });
+
+  it('🔴 refused erasure is audited with `/api/gdpr/erasures`, NOT `/` or `/erasures`', async () => {
+    // The defect: inside `res.on('finish')` deriveAction reads `req.path` which
+    // express has trimmed by then. The fix captures `originalUrl.split('?')[0]`
+    // at entry and uses that everywhere in the finish handler.
+    void (await drive('POST', '/api/gdpr/erasures'));
+    const lastParams = queryLog[queryLog.length - 1];
+    const details = JSON.parse(String(lastParams?.[9]));
+    expect(details.path).toBe('/api/gdpr/erasures');
+  });
+
+  it('🔴 refused GET erasure preserves its full sub-path (`/api/gdpr/erasures/:ref`) rather than collapsing to `/`', async () => {
+    void (await drive('GET', '/api/gdpr/erasures/some-ref'));
+    const lastParams = queryLog[queryLog.length - 1];
+    const details = JSON.parse(String(lastParams?.[9]));
+    expect(details.path).toBe('/api/gdpr/erasures/some-ref');
+  });
+});

```
