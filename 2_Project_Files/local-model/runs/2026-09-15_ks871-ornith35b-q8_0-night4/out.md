```diff
--- a/services/api-gateway/src/middleware/audit.ts
+++ b/services/api-gateway/src/middleware/audit.ts
@@ -94,3 +94,3 @@ function deriveAction(req: Request): {
   action: string;
   resourceType: string;
-  resourceId: string | null;
+  resourceId: string | null;
 } {
 
@@ -107,3 +107,3 @@ function deriveAction(req: Request): {
   // Trim trailing slashes and pull the first 3-4 segments after /api.
-  const segments = req.path.replace(/\/+$/, '').split('/').filter(Boolean);
+  const segments = auditPath.replace(/\/+$/, '').split('/').filter(Boolean);
   // segments[0] === 'api' for everything we audit
 
@@ -209,3 +209,4 @@ export function createAuditMiddleware(deps: AuditMiddlewareDeps): RequestHandler
     if (EXCLUDED_PREFIXES.some((p) => req.path.startsWith(p))) return next();
 
     const start = Date.now();
+    const auditPath = req.originalUrl.split('?')[0];
 
@@ -229,3 +230,3 @@ export function createAuditMiddleware(deps: AuditMiddlewareDeps): RequestHandler
           if (!deps.isDbAvailable()) return;
-          const { action, resourceType, resourceId: routeResourceId } = deriveAction(req);
+          const { action, resourceType, resourceId: routeResourceId } = deriveAction(req, auditPath);
 
@@ -279,3 +280,3 @@ export function createAuditMiddleware(deps: AuditMiddlewareDeps): RequestHandler
             method: req.method,
-            path: req.path,
+            path: auditPath,
             status: res.statusCode,
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts
@@ -0,0 +1,106 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+import { createAuditMiddleware } from '../middleware/audit';
+
+let server: http.Server;
+let port = 0;
+let capturedDetails: unknown[] = [];
+
+beforeAll(async () => {
+  server = http.createServer(() => {});
+  await new Promise<void>((r) => server.listen(0, '127.0.0.1', () => r()));
+  port = (server.address() as AddressInfo).port;
+});
+afterAll(async () => {
+  await new Promise<void>((r) => server.close(() => r()));
+});
+beforeEach(() => {
+  capturedDetails = [];
+});
+
+function buildApp() {
+  const deps = {
+    query: async (_sql: string, params: unknown[]) => {
+      const detailsParam = params[params.length - 1] as string | undefined;
+      try {
+        capturedDetails.push(JSON.parse(detailsParam ?? ''));
+      } catch {
+        capturedDetails.push(null);
+      }
+      return { rows: [] };
+    },
+    isDbAvailable: () => true,
+    log: () => {},
+  };
+  const app = express();
+  app.use(express.json());
+  app.use(createAuditMiddleware(deps));
+  app.delete('/api/gdpr/erasures/:id', ((_req, res) => {
+    res.status(403).json({ error: 'refused' });
+  }) as RequestHandler);
+  app.post('/api/documents', ((_req, res) => {
+    res.status(201).json({ ok: true });
+  }) as RequestHandler);
+  return app;
+}
+
+async function drive(method: string, path: string): Promise<number> {
+  const s = buildApp().listen(0, '127.0.0.1');
+  await new Promise<void>((r) => s.once('listening', () => r()));
+  const p = (s.address() as AddressInfo).port;
+  const status = await new Promise<number>((resolve) => {
+    const req = http.request(
+      { host: '127.0.0.1', port: p, path, method },
+      (res) => { res.resume(); resolve(res.statusCode ?? 0); },
+    );
+    req.on('error', () => resolve(-1));
+    req.end();
+  });
+  await new Promise<void>((r) => s.close(() => r()));
+  return status;
+}
+
+describe('KS-871 — audit path capture at entry', () => {
+  it('🔴 KS-871 — details.path is the original request path, not the trimmed remainder', async () => {
+    const status = await drive('DELETE', '/api/gdpr/erasures/abc');
+    expect(status).toBe(403);
+    // Wait for fire-and-forget write to flush into capturedDetails.
+    await new Promise((r) => setTimeout(r, 50));
+    expect(capturedDetails.length).toBeGreaterThanOrEqual(1);
+    const last = capturedDetails[capturedDetails.length - 1] as { path?: unknown };
+    expect(last?.path).toBe('/api/gdpr/erasures/abc');
+  });
+
+  it('🔴 KS-871 — action/resource are derived from the original path', async () => {
+    const status = await drive('DELETE', '/api/gdpr/erasures/abc');
+    expect(status).toBe(403);
+    await new Promise((r) => setTimeout(r, 50));
+    const last = capturedDetails[capturedDetails.length - 1] as { resourceType?: unknown; action?: unknown } | null;
+    expect(last?.resourceType).not.toBe('unknown');
+    expect(String(last?.action)).toMatch(/gdpr|erasure/i);
+  });
+
+  it('KS-871 control — an ordinary POST /api/documents still audits its own path', async () => {
+    const status = await drive('POST', '/api/documents');
+    expect(status).toBe(201);
+    await new Promise((r) => setTimeout(r, 50));
+    expect(capturedDetails.length).toBeGreaterThanOrEqual(1);
+    const last = capturedDetails[capturedDetails.length - 1] as { path?: unknown };
+    expect(last?.path).toBe('/api/documents');
+  });
+});
```
