# READY — KS-745 (api-gateway `routes/audit-export.ts:138` + `:144`: the export fetches the security LIST route `/api/audit` (not the non-existent `/api/audit/logs`, which 404'd via `/api/audit/:id`) and reads `data.data.logs`) — Ornith ornith:35b (Q4_K_M) PASS 7/7 (run 21:04, round 2 — r1 was Wednesday's brief: the test lacked `req.user`, the route's admin guard answered 401; whole api-gateway suite green)
# Source read by me (Wednesday): both one-line edits as briefed with their comments; the test sets an admin `req.user` before the router, stubs global fetch with the list shape and reads back the url it was asked for; 🔴 red at the tip (url /api/audit/logs; body without the entry), green after; control (fetch throws → 502 BAD_GATEWAY) green both. The ticket's own reachability note ('UNMEASURED end to end') stands — this is the unit proof.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
@@ -135,13 +135,13 @@ router.get('/export', async (req: Request, res: Response) => {
 
     try {
       const response = await fetch(
-        `${SECURITY_SERVICE_URL}/api/audit/logs?${queryParams.toString()}`,
+        // KS-745: the security service lists at /api/audit (no /logs route — that hit /api/audit/:id with id "logs" → 404)
+        `${SECURITY_SERVICE_URL}/api/audit?${queryParams.toString()}`,
         { method: 'GET', headers },
       );
 
       if (response.ok) {
         const data = await response.json();
-        entries = (data as any)?.data || (data as any)?.logs || [];
+        // KS-745: the list answers { success, data: { logs, total, limit, offset } } — the array is data.data.logs
+        entries = (data as any)?.data?.logs ?? (data as any)?.logs ?? [];
       } else {
         const errorData = await response.json().catch(() => ({}));
         res.status(response.status).json({
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks745-audit-export-calls-the-list-route.test.ts
@@ -0,0 +1,65 @@
+import { describe, it, expect, vi, beforeAll, afterAll, beforeEach } from 'vitest';
+import http from 'node:http';
+import express from 'express';
+
+const savedEnv = { ...process.env };
+process.env.SECURITY_SERVICE_URL = 'http://security.test:1';
+
+/** The security service's LIST shape, one entry. Records every url it was asked for. */
+const ENTRY = { id: 'audit-ks745-1', timestamp: '2026-09-01T10:00:00.000Z', type: 'auth', action: 'login', userId: 'u1' };
+const fetchMock = vi.fn(async (_input: unknown) => ({ ok: true, status: 200, json: async () => ({ success: true, data: { logs: [ENTRY], total: 1, limit: 100, offset: 0 } }) }) as unknown as Response);
+vi.stubGlobal('fetch', fetchMock);
+
+const router = (await import('../routes/audit-export')).default;
+
+let server: http.Server; let port = 0;
+beforeAll(async () => {
+  const app = express();
+  // the route is admin-only (audit-export.ts:83-94): 401 without req.user, 403 without an admin role — set both before the router
+  app.use((req, _res, next) => { (req as any).user = { id: 'admin-ks745', role: 'platform_admin' }; next(); });
+  app.use('/api/admin/audit', router);
+  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => { port = (server.address() as any).port; r(); }); }, 10_000);
+}, 10_000);
+afterAll(async () => {
+  await new Promise<void>((r) => server.close(() => r()));
+  for (const k of Object.keys(process.env)) if (!(k in savedEnv)) delete process.env[k];
+  Object.assign(process.env, savedEnv);
+  vi.unstubAllGlobals();
+});
+beforeEach(() => { fetchMock.mockClear(); });
+function getText(path: string): Promise<{ status: number; text: string }> {
+  return new Promise((resolve, reject) => {
+    http.get({ hostname: '127.0.0.1', port, path }, (res) => {
+      let data = ''; res.on('data', (c) => (data += c));
+      res.on('end', () => resolve({ status: res.statusCode ?? 0, text: data }));
+    }).on('error', reject);
+  });
+}
+
+describe('KS-745 - the audit export calls the security list route', () => {
+  it('🔴 KS-745 - the export fetches /api/audit (the list), not /api/audit/logs, and returns the listed entry', async () => {
+    const res = await getText('/api/admin/audit/export?from=2026-09-01&to=2026-09-02&format=json');
+    const url = String(fetchMock.mock.calls[0]?.[0]);
+    expect(url.startsWith('http://security.test:1/api/audit?')).toBe(true);
+    expect(url).not.toContain('/api/audit/logs');
+    expect(res.status).toBe(200);
+    expect(res.text).toContain('audit-ks745-1');
+  });
+
+  it('KS-745 control - an unreachable security service still answers 502 BAD_GATEWAY', async () => {
+    fetchMock.mockImplementationOnce(async () => { throw new Error('offline in test'); });
+    const res = await getText('/api/admin/audit/export?from=2026-09-01&to=2026-09-02&format=json');
+    expect(res.status).toBe(502);
+    expect(res.text).toContain('BAD_GATEWAY');
+  });
+});
```
