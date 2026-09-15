# READY — KS-1101 PART C of three (api-gateway `routes/health-dashboard.ts:60`: `/api/system/health/dashboard` reads the probed body and maps `status: 'degraded'` to `down` with the reasons in `error`) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (run night4 20:55; whole api-gateway suite green). **KS-1101 COMPLETE: A (health.ts) + B (system-status.ts) + C (health-dashboard.ts) → ONE PR; the ticket's regression cell is Part A's 🔴.**
# Source read by me (Wednesday): E1 as briefed (json read with a null fallback; down-with-reasons on degraded; the up return kept); the test pins ANCHORING/ORIGINATE urls in env BEFORE the dynamic import (config/services reads env at import), stubs global fetch per url, mounts the router on listen(0), http.get for its own request; 🔴 red at the tip (up), green after; control (originate ok → up) green both.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts
@@ -57,7 +57,12 @@ async function checkService(
     clearTimeout(timeout);
     const latencyMs = Date.now() - start;
 
-      return [key, { status: 'up', latencyMs, url: config.url }];
+      // KS-1101: a 200 whose body says `status: 'degraded'` (anchoring since #728 — up, chain unreachable) is not `up`.
+      const body = (await response.json().catch(() => null)) as { status?: unknown; degradedReasons?: unknown } | null;
+      if (body?.status === 'degraded') {
+        return [key, { status: 'down', latencyMs, url: config.url, error: `degraded: ${Array.isArray(body.degradedReasons) ? body.degradedReasons.join(', ') : 'no reason given'}` }];
+      }
+      return [key, { status: 'up', latencyMs, url: config.url }];
     }
 
     return [
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1101-health-dashboard-reads-degraded-body.test.ts
@@ -0,0 +1,62 @@
+import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
+import http from 'node:http';
+import express from 'express';
+
+const savedEnv = { ...process.env };
+process.env.ANCHORING_SERVICE_URL = 'http://anchoring.test:1';
+process.env.ORIGINATE_SERVICE_URL = 'http://originate.test:1';
+
+/** Every deployed probe answers 200; anchoring's body says degraded, every other body says ok. Other services default to localhost and are not probed. */
+const fetchMock = vi.fn(async (input: unknown) => {
+  const url = String(input);
+  const body = url.startsWith('http://anchoring.test') ? { status: 'degraded', degradedReasons: ['chain unreachable'] } : { status: 'ok' };
+  return { ok: true, status: 200, json: async () => body } as unknown as Response;
+});
+vi.stubGlobal('fetch', fetchMock);
+
+const router = (await import('../routes/health-dashboard')).default;
+
+let server: http.Server; let port = 0;
+beforeAll(async () => {
+  const app = express(); app.use('/api/system/health', router);
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
+
+describe('KS-1101 C - the health dashboard reads the degraded body', () => {
+  it('🔴 KS-1101 C - anchoring answering 200 with status degraded is reported down on the dashboard, with the reason', async () => {
+    const body = await getJson('/api/system/health/dashboard');
+    expect(body.services.anchoring.status).toBe('down');
+    expect(body.services.anchoring.error).toContain('chain unreachable');
+  });
+
+  it('KS-1101 C control - a deployed downstream answering 200 with status ok is up', async () => {
+    const body = await getJson('/api/system/health/dashboard');
+    expect(body.services.originate.status).toBe('up');
+  });
+});
```
