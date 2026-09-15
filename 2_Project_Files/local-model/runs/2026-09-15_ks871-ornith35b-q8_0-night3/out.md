```diff
--- a/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
@@ -92,7 +92,7 @@ const EXCLUDED_PREFIXES = [
  * tail without needing to enumerate every route.
  */
-function deriveAction(req: Request): {
+function deriveAction(req: Request, auditPath: string): {   // KS-871: capture original URL so refused mounts don't trim req.path
   action: string;
   resourceType: string;
   resourceId: string | null;
@@ -105,7 +105,7 @@ function deriveAction(req: Request): {
     : method === 'DELETE' ? 'delete'
     : method.toLowerCase();
 
   // Trim trailing slashes and pull the first 3-4 segments after /api.
-  const segments = req.path.replace(/\/+$/, '').split('/').filter(Boolean);
+  const segments = auditPath.replace(/\/+$/, '').split('/').filter(Boolean);   // KS-871: use captured entry path, not trimmed mount-relative remainder
   // segments[0] === 'api' for everything we audit
   const section = segments[1] || 'unknown';
   const subResource = segments[2];
@@ -227,7 +227,7 @@ export function createAuditMiddleware(deps: AuditMiddlewareDeps): RequestHandler
 
       void (async () => {
         try {
           if (!deps.isDbAvailable()) return;
-          const { action, resourceType, resourceId: routeResourceId } = deriveAction(req);
+          const { action, resourceType, resourceId: routeResourceId } = deriveAction(req, auditPath);   // KS-871: pass captured entry path
           
           const u = (req as Request & { user?: { userId?: string; organizationId?: string; tenantId?: string } }).user;
           let userId: string | null = u?.userId || null;
@@ -277,7 +277,7 @@ export function createAuditMiddleware(deps: AuditMiddlewareDeps): RequestHandler
           }
           const details = JSON.stringify({
             method: req.method,
-            path: req.path,
+            path: auditPath,   // KS-871: record original request path, not Express-trimmed remainder after router.use() gate
             status: res.statusCode,
             durationMs: Date.now() - start,
             tenantId: u?.tenantId || null,

--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts
@@ -0,0 +1,96 @@
+/**
+ * =============================================================================
+ * KS-871 — AUDIT LOG MUST RECORD THE ORIGINAL REQUEST PATH AT ENTRY TIME
+ * =============================================================================
+ * When an earlier `router.use(prefix, handler)` gate has already answered
+ * (a REFUSED GDPR erasure is the case), Express trims `req.path` to the
+ * mount-relative remainder by the time `res.on('finish')` fires. The audit
+ * middleware was reading that trimmed value AFTER the response, so refused
+ * requests were logged with `path: '/'` instead of `/api/gdpr/erasures`.
+ *
+ * This file drives the REAL `createAuditMiddleware` in-process against a stub
+ * upstream and asserts on what gets written into the SQL params — no server,
+ * no HTTP round trip needed for the assertion itself.
+ * =============================================================================
+ */
+
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import express from 'express';
+import type { AddressInfo } from 'node:net';
+import http from 'node:http';
+import { createAuditMiddleware } from '../middleware/audit';
+
+let capturedRows: Array<{ sql: string; params: unknown[] }> = [];
+const queryStub = vi.fn(async (_sql: string, params: unknown[]) => {
+  capturedRows.push({ sql: _sql, params });
+  return { rows: [] };
+});
+
+function buildApp() {
+  const app = express();
+  app.use(express.json());
+
+  // Mount the audit middleware at /api — this is where the defect lives.
+  // A `router.use('/api/gdpr', …)` mounted BELOW will answer some paths
+  // without calling next(), which is exactly when req.path gets trimmed.
+  app.use(createAuditMiddleware({
+    query: queryStub as any,
+    isDbAvailable: () => true,
+    log: () => {},
+  }));
+
+  // Refused-erasure router: answers 403 WITHOUT calling next(). On the
+  // untouched code, by the time res.on('finish') runs, req.path === '/'.
+  const gdprRouter = express.Router();
+  gdprRouter.delete('/erasures/:id?', (_req, res) => {
+    res.status(403).json({ error: 'scope denied' });
+  });
+  app.use('/api/gdpr', gdprRouter);
+
+  // Ordinary route that answers normally — used as control cell.
+  const docRouter = express.Router();
+  docRouter.post('/', (_req, res) => {
+    res.status(201).json({ id: 'doc-1' });
+  });
+  app.use('/api/documents', docRouter);
+
+  return app;
+}
+
+async function drive(path: string, method: string): Promise<number> {
+  const server = buildApp().listen(0, '127.0.0.1');
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  const port = (server.address() as AddressInfo).port;
+  try {
+    capturedRows = [];
+    const status = await new Promise<number>((resolve) => {
+      const req = http.request(
+        { host: '127.0.0.1', port, path, method },
+        (res) => { res.resume(); resolve(res.statusCode ?? 0); },
+      );
+      req.on('error', () => resolve(-1));
+      if (method !== 'GET') req.write('{}');
+      req.end();
+    });
+    return status;
+  } finally {
+    await new Promise<void>((r) => server.close(() => r()));
+  }
+}
+
+describe('KS-871 — audit logs must capture original request path at entry', () => {
+  beforeEach(() => {
+    vi.clearAllMocks();
+  });
+
+  it('🔴 KS-871 — details.path is the original request path, not the trimmed remainder', async () => {
+    // Refused erasure: router answers without calling next(), so Express
+    // trims req.path to '/' before finish fires. The fix captures the
+    // original URL at entry time and uses that everywhere.
+    const status = await drive('/api/gdpr/erasures/abc', 'DELETE');
+    expect(status).toBe(403);
+    expect(capturedRows.length).toBeGreaterThan(0);
+    const lastRow = capturedRows[capturedRows.length - 1];
+    const params = lastRow.params as unknown[];
+    const detailsJson = params[8] as string;   // index 8 in INSERT param list → details column
+    const details = JSON.parse(detailsJson);
+    expect(details.path).toBe('/api/gdpr/erasures/abc');
+  });
+
+  it('🔴 KS-871 — action/resource are derived from the original path', async () => {
+    // deriveAction now reads the captured auditPath instead of req.path,
+    // so resourceType reflects 'gdpr' + 'erasures', not 'unknown'.
+    const status = await drive('/api/gdpr/erasures/abc', 'DELETE');
+    expect(status).toBe(403);
+    const lastRow = capturedRows[capturedRows.length - 1];
+    const params = lastRow.params as unknown[];
+    expect(params[3]).toBe('gdpr.delete');     // action
+    expect(params[4]).toBe('gdpr');            // resource_type
+  });
+
+  it('KS-871 control — an ordinary POST /api/documents still audits its own path', async () => {
+    // A route that answers normally (calls next() implicitly via res.json)
+    // should see no trimming at all — this proves the harness reaches the
+    // code under test regardless of the defect shape.
+    const status = await drive('/api/documents', 'POST');
+    expect(status).toBe(201);
+    expect(capturedRows.length).toBeGreaterThan(0);
+    const lastRow = capturedRows[capturedRows.length - 1];
+    const params = lastRow.params as unknown[];
+    const detailsJson = params[8] as string;
+    const details = JSON.parse(detailsJson);
+    expect(details.path).toBe('/api/documents');
+  });
+});
```
