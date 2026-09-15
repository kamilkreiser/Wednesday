```diff
diff --git a/services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts b/services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts
new file mode 100644
index 0000000..abcdef0
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts
@@ -1,95 +0,0 @@
+/**
+ * KS-871: audit log records `req.path` AFTER the response. When an earlier
+ * router.use() gate has already answered (REFUSED erasure), Express trims
+ * req.path to `/`, so the audit row carries the wrong path. This test drives
+ * the refused-erasure code path through the real middleware and asserts on
+ * what gets written into the captured SQL params.
+ */
+import { describe, it, expect, beforeEach, vi } from 'vitest';
+import express from 'express';
+import type { RequestHandler } from 'express';
+import { createAuditMiddleware } from '../middleware/audit';
+
+describe('KS-871 — audit log captures original request path at entry', () => {
+  let queryCalls: Array<{ sql: string; params: unknown[] }> | null = null;
+
+  function buildApp(user?: object) {
+    const authenticateToken = ((_required?: boolean) =>
+      ((req, _res, next) => {
+        if (user) (req as any).user = user;
+        next();
+      }) as RequestHandler);
+
+    // Capture every call to deps.query so we can inspect details without DB.
+    const captured: Array<{ sql: string; params: unknown[] }> = [];
+    const deps = {
+      query: async (sql: string, params: unknown[]) => {
+        captured.push({ sql, params });
+        return { rows: [] };
+      },
+      isDbAvailable: () => true,
+      log: () => {},
+    };
+
+    const app = express();
+    app.use(express.json());
+    app.use(createAuditMiddleware(deps));
+
+    // Mount a router that refuses DELETE /api/gdpr/erasures/* with 403
+    // WITHOUT calling next(). This simulates the "earlier gate" shape in
+    // the ticket where res.on('finish') sees trimmed req.path === '/'.
+    const gdprRouter = express.Router();
+    gdprRouter.delete('/erasures/:id', (_req, res) => {
+      res.status(403).json({ error: 'forbidden' });
+    });
+    app.use('/api/gdpr', gdprRouter);
+
+    // Normal route for control cell.
+    const docRouter = express.Router();
+    docRouter.post('/', (_req, res) => {
+      res.status(201).json({ id: 'doc-1' });
+    });
+    app.use('/api/documents', docRouter);
+
+    queryCalls = captured;
+    return app;
+  }
+
+  beforeEach(() => {
+    queryCalls = null;
+  });
+
+  it('🔴 KS-871 — details.path is the original request path, not the trimmed remainder', async () => {
+    const app = buildApp();
+    await new Promise<void>((resolve, reject) => {
+      const server = app.listen(0, '127.0.0.1', () => resolve());
+      require('http').request(
+        { host: '127.0.0.1', port: (server.address() as any).port, path: '/api/gdpr/erasures/abc', method: 'DELETE' },
+        (res) => { res.resume(); server.close(() => {}); },
+      ).on('error', (e) => { server.close(() => {}); reject(e); }).end();
+    });
+
+    // Wait briefly for fire-and-forget write to complete.
+    await new Promise((r) => setTimeout(r, 50));
+
+    expect(queryCalls!.length).toBeGreaterThan(0);
+    const lastCall = queryCalls![queryCalls!.length - 1];
+    const params = lastCall.params as [string, string | null, string | null, string, string, string | null, string, string | null, string, boolean];
+    const detailsJson = params[8] as string;
+    const details = JSON.parse(detailsJson);
+    
+    // The defect: req.path was trimmed to '/' by Express before finish handler ran.
+    // After fix: should be the full original path.
+    expect(details.path).toBe('/api/gdpr/erasures/abc');
+  });
+
+  it('🔴 KS-871 — action/resource are derived from the original path', async () => {
+    const app = buildApp();
+    await new Promise<void>((resolve, reject) => {
+      const server = app.listen(0, '127.0.0.1', () => resolve());
+      require('http').request(
+        { host: '127.0.0.1', port: (server.address() as any).port, path: '/api/gdpr/erasures/abc', method: 'DELETE' },
+        (res) => { res.resume(); server.close(() => {}); },
+      ).on('error', (e) => { server.close(() => {}); reject(e); }).end();
+    });
+
+    await new Promise((r) => setTimeout(r, 50));
+
+    expect(queryCalls!.length).toBeGreaterThan(0);
+    const lastCall = queryCalls![queryCalls!.length - 1];
+    const params = lastCall.params as unknown[];
+    
+    // Params order: tenantId, userId, orgId, action, resourceType, resourceId, ip, userAgent, details, success
+    const action = params[3] as string;
+    const resourceType = params[4] as string;
+    
+    // Should derive gdpr + erasures from original path, not 'unknown'.
+    expect(action).toContain('gdpr');
+    expect(resourceType).not.toBe('unknown');
+  });
+
+  it('KS-871 control — an ordinary POST /api/documents still audits its own path', async () => {
+    const app = buildApp();
+    await new Promise<void>((resolve, reject) => {
+      const server = app.listen(0, '127.0.0.1', () => resolve());
+      require('http').request(
+        { host: '127.0.0.1', port: (server.address() as any).port, path: '/api/documents', method: 'POST', headers: { 'content-type': 'application/json' } },
+        (res) => { res.resume(); server.close(() => {}); },
+      ).on('error', (e) => { server.close(() => {}); reject(e); }).end('{}');
+    });
+
+    await new Promise((r) => setTimeout(r, 50));
+
+    expect(queryCalls!.length).toBeGreaterThan(0);
+    const lastCall = queryCalls![queryCalls!.length - 1];
+    const params = lastCall.params as [string, string | null, string | null, string, string, string | null, string, string | null, string, boolean];
+    const detailsJson = params[8] as string;
+    const details = JSON.parse(detailsJson);
+    
+    expect(details.path).toBe('/api/documents');
+  });
+});

```
