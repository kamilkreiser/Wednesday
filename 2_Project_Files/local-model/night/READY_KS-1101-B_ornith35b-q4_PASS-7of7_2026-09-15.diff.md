# READY — KS-1101 PART B of three (api-gateway `routes/system-status.ts:336-337`: `/api/system/status` reads the probed body and maps `status: 'degraded'` to `unhealthy` with the reasons in `error`) — Ornith ornith:35b (Q4_K_M) PASS 7/7 (run night3 20:50, round 3 — r1 an apostrophe in a single-quoted describe title (task.md rule 3a added), r2 an empty queue file; whole api-gateway suite green). Part C (`routes/health-dashboard.ts:59`) NOT yet briefed.
# Source read by me (Wednesday): E1 as briefed (the json read widened; early return unhealthy on degraded; :341 healthy return kept); the test = the KS-864 driver shape (env pinned, redis mocked, global fetch stubbed per url, the router on listen(0), http.get for its own request); 🔴 red at the tip (healthy), green after; control (originate ok → healthy) green both.

```diff
--- a/services/api-gateway/src/routes/system-status.ts
+++ b/services/api-gateway/src/routes/system-status.ts
@@ -333,7 +333,12 @@ async function checkServiceHealth(service: ServiceDefinition): Promise<{
     if (response.ok) {
       let version: string | undefined;
       try {
-        const data = await response.json() as { version?: string };
+        const data = await response.json() as { version?: string; status?: unknown; degradedReasons?: unknown };
         version = data.version;
+        // KS-1101: a 200 whose body says `status: 'degraded'` (anchoring since #728 — up, chain unreachable) is not healthy.
+        if (data.status === 'degraded') {
+          return { status: 'unhealthy', latency, version, error: `degraded: ${Array.isArray(data.degradedReasons) ? data.degradedReasons.join(', ') : 'no reason given'}` };
+        }
       } catch {
         // Response may not be JSON (e.g., frontend health)
       }
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1101-system-status-reads-degraded-body.test.ts
@@ -0,0 +1,62 @@
+import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
+import http from 'node:http';
+import express from 'express';
+
+const savedEnv = { ...process.env };
+process.env.NODE_ENV = 'staging';
+process.env.ANCHORING_SERVICE_URL = 'http://anchoring.test:1';
+
+vi.mock('../services/redis', () => ({ getRedisHealth: vi.fn(async () => ({ status: 'healthy' })) }));
+
+/** Every downstream probe answers 200; anchoring's body says degraded, every other body says ok. */
+const fetchMock = vi.fn(async (input: unknown) => {
+  const url = String(input);
+  const body = url.startsWith('http://anchoring.test') ? { status: 'degraded', degradedReasons: ['chain unreachable'] } : { status: 'ok' };
+  return { ok: true, status: 200, json: async () => body } as unknown as Response;
+});
+vi.stubGlobal('fetch', fetchMock);
+
+const router = (await import('../routes/system-status')).default;
+
+let server: http.Server; let port = 0;
+beforeAll(async () => {
+  const app = express(); app.use('/api/system', router);
+  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => { port = (server.address() as any).port; r(); }); }, 10_000);
+}, 10_000);
+afterAll(async () => {
+  await new Promise<void>((r) => server.close(() => r()));
+  for (const k of Object.keys(process.env)) if (!(k in savedEnv)) delete process.env[k];
+  Object.assign(process.env, savedEnv);
+  vi.unstubAllGlobals();
+});
+function getJson(path: string): Promise<any> {
+  return new Promise((resolve, reject) => {
+    http.get({ hostname: '127.0.0.1', port, path }, (res) => {
+      let data = ''; res.on('data', (c) => (data += c));
+      res.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
+    }).on('error', reject);
+  });
+}
+async function serviceNamed(name: string): Promise<{ name?: string; status?: string; error?: string } | undefined> {
+  const body = await getJson('/api/system/status');
+  return (Object.values(body.services).flat() as Array<{ name?: string; status?: string; error?: string }>).find((s) => s.name === name);
+}
+describe('KS-1101 B - system status reads the degraded body', () => {
+  it('🔴 KS-1101 B — anchoring answering 200 with status degraded is reported unhealthy on /api/system/status, with the reason', async () => {
+    const a = await serviceNamed('anchoring');
+    expect(a?.status).toBe('unhealthy');
+    expect(a?.error).toContain('chain unreachable');
+  });
+  it('KS-1101 B control — a downstream answering 200 with status ok is healthy', async () => {
+    const o = await serviceNamed('originate');
+    expect(o?.status).toBe('healthy');
+  });
+});
```
