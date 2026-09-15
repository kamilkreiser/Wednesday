```diff
--- a/services/demo-service/src/app.ts
+++ b/services/demo-service/src/app.ts
@@ -10,7 +10,7 @@ import { createLogger } from './utils/logger';
 import { requireDemoKey } from './middleware/demoGuard';
 import { healthRouter } from './routes/health';
 import { personaRouter } from './routes/persona';
-import express, { Request, Response } from 'express';
+import express, { NextFunction, Request, Response } from 'express';
 
 const logger = createLogger('demo-service');
@@ -82,6 +82,17 @@ export function createApp() {
       error: { code: 'NOT_FOUND', message: `Cannot ${_req.method} ${_req.path}` },
     });
   });
+
+  // KS-844: a mounted error handler — never express's default HTML page (stack trace + absolute paths).
+  app.use((err: Error & { status?: number; statusCode?: number }, _req: Request, res: Response, _next: NextFunction) => {
+    const status = err.status ?? err.statusCode ?? 500;
+    const code = status === 400 ? 'BAD_REQUEST' : status === 413 ? 'PAYLOAD_TOO_LARGE' : status >= 500 ? 'INTERNAL_ERROR' : 'REQUEST_ERROR';
+    res.status(status).json({
+      success: false,
+      error: { code, message: status >= 500 ? 'Internal server error' : err.message },
+    });
+  });
+
   return app;
 }
--- /dev/null
+++ b/services/demo-service/src/__tests__/ks844-demo-service-mounts-no-error-handler.test.ts
@@ -0,0 +1,75 @@
+vi.mock('../utils/logger', () => ({
+  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() },
+  createLogger: () => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }),
+}));
+
+vi.mock('../services/authClient', () => ({
+  authenticatePersona: vi.fn(),
+}));
+
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+
+import { createApp } from '../app';
+
+async function startServer(app: ReturnType<typeof createApp>): Promise<{ url: string; close: () => void }> {
+  return new Promise((resolve_) => {
+    const server = app.listen(0, '127.0.0.1', () => {
+      const addr = server.address();
+      const port = typeof addr === 'object' && addr ? addr.port : 0;
+      resolve_({ url: `http://127.0.0.1:${port}`, close: () => server.close() });
+    });
+  });
+}
+
+const ORIGINAL_ENV = { ...process.env };
+
+beforeEach(() => {
+  process.env.NODE_ENV = 'development';
+  process.env.DEMO_SERVICE_ENABLED = 'true';
+});
+
+afterEach(() => {
+  process.env = { ...ORIGINAL_ENV };
+});
+
+describe('KS-844: demo-service mounts an error handler that answers JSON', () => {
+  it('🔴 KS-844 — an unparseable JSON body answers JSON 400, not an HTML page', async () => {
+    const { url, close } = await startServer(createApp());
+
+    try {
+      const response = await fetch(`${url}/demo-api/health`, {
+        method: 'POST',
+        headers: { 'content-type': 'application/json' },
+        body: '{not json',
+      });
+
+      expect(response.status).toBe(400);
+      expect(response.headers.get('content-type')).toContain('application/json');
+      const body = await response.json();
+      expect(body.success).toBe(false);
+      expect(body.error.code).toBe('BAD_REQUEST');
+      expect(typeof body.error.message).toBe('string');
+    } finally {
+      close();
+    }
+  });
+
+  it('🔴 KS-844 — the response never carries a stack trace or an absolute path', async () => {
+    const { url, close } = await startServer(createApp());
+
+    try {
+      const response = await fetch(`${url}/demo-api/health`, {
+        method: 'POST',
+        headers: { 'content-type': 'application/json' },
+        body: '{not json',
+      });
+
+      const text = await response.text();
+      expect(text).not.toContain('<html');
+      expect(text).not.toContain('    at ');
+      expect(text).not.toContain('/Volumes/');
+      expect(text).not.toContain('/app/');
+    } finally {
+      close();
+    }
+  });
+
+  it('KS-844 control — a well-formed request to /demo-api/health still answers 200 JSON', async () => {
+    const { url, close } = await startServer(createApp());
+
+    try {
+      const response = await fetch(`${url}/demo-api/health`);
+      expect(response.status).toBe(200);
+      const body = await response.json();
+      expect(body).toBeDefined();
+    } finally {
+      close();
+    }
+  });
+});
```
