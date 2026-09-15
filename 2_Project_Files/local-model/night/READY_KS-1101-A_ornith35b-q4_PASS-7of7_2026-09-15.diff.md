# READY — KS-1101 PART A of three (api-gateway `services/health.ts:132`: `/health/deep` + `/health/ready` now read the probed body and treat `status: 'degraded'` as down, with the reasons in `error`) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (run 20:39; A2 --recount on the product hunk; whole api-gateway suite green). Parts B (`routes/system-status.ts:333`) and C (`routes/health-dashboard.ts:59`) NOT yet briefed — same shape.
# Source read by me (Wednesday): E1 as briefed (json read with a null fallback, throw on degraded naming the reasons); the test mounts createHealthRoutes on listen(0) with db/auth/logger mocked and a stubbed global fetch with a realFetch passthrough for its own request; 🔴 red at the tip (anchoring 200-degraded read as up), green after; control (all ok → healthy 200) green both.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/services/health.ts
+++ b/Blockchain/Dev/services/api-gateway/src/services/health.ts
@@ -129,7 +129,10 @@ export function createHealthRoutes(
         const timeout = setTimeout(() => controller.abort(), CHECK_TIMEOUT);
         try {
           const resp = await fetch(`${url}/health`, { signal: controller.signal });
-          if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
+          if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
+          // KS-1101: a downstream may answer 200 with `status: 'degraded'` (anchoring since #728 — the chain is
+          // unreachable but the service is up). HTTP status alone hid it; a degraded body is not `up`.
+          const body = (await resp.json().catch(() => null)) as { status?: unknown; degradedReasons?: unknown } | null;
+          if (body?.status === 'degraded') throw new Error(`degraded: ${Array.isArray(body.degradedReasons) ? body.degradedReasons.join(', ') : 'no reason given'}`);
         } finally {
           clearTimeout(timeout);
         }
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1101-gateway-health-aggregates-read-anchoring-s.test.ts
@@ -0,0 +1,75 @@
+import { describe, it, expect, vi, beforeAll, afterAll, beforeEach } from 'vitest';
+import express from 'express';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+
+vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [{ '?column?': 1 }] })) }));
+vi.mock('../middleware/auth', () => ({ authenticateToken: () => (_req: unknown, _res: unknown, next: () => void) => next() }));
+vi.mock('../utils/logger', () => ({ logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() } }));
+
+import { createHealthRoutes } from '../services/health';
+
+const realFetch = globalThis.fetch;
+const fetchMock = vi.fn();
+vi.stubGlobal('fetch', fetchMock);
+
+/** A 200 whose body is `body`, the shape `fetch` returns. */
+function okJson(body: unknown): Promise<{ ok: true; status: 200; json: () => Promise<unknown> }> {
+  return Promise.resolve({ ok: true as const, status: 200 as const, json: async () => body });
+}
+
+const services = {
+  auth: { url: 'http://auth.test' },
+  originate: { url: 'http://originate.test' },
+  anchoring: { url: 'http://anchoring.test' },
+} as never;
+const redisService = { getNotificationSettings: async () => null, getRedisClient: () => ({ ping: async () => 'PONG' }) } as never;
+
+let server: Server;
+let baseUrl: string;
+
+beforeAll(async () => {
+  const app = express();
+  app.use(createHealthRoutes(services, redisService));
+  await new Promise<void>((resolve) => { server = app.listen(0, resolve); });
+  baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+});
+afterAll(async () => { await new Promise<void>((resolve) => server.close(() => resolve())); });
+beforeEach(() => { fetchMock.mockReset(); });
+
+describe('KS-1101 — deep health degraded-body handling', () => {
+  it('🔴 KS-1101 — anchoring answering 200 {status: degraded} is NOT reported up on /health/deep', async () => {
+    fetchMock.mockImplementation(async (input: unknown) => {
+      if (String(input).startsWith(baseUrl)) return realFetch(input as string);
+      if (String(input).startsWith('http://anchoring.test')) return okJson({ status: 'degraded', degradedReasons: ['chain unreachable'] });
+      return okJson({ status: 'ok' });
+    });
+    const res = await fetch(`${baseUrl}/health/deep`);
+    const body = (await res.json()) as { status: string; checks: Record<string, { status: string; error?: string }> };
+    expect(body.checks.anchoring.status).toBe('down');
+    expect(body.checks.anchoring.error).toContain('degraded');
+    expect(res.status).toBe(503);
+    expect(body.status).toBe('degraded');
+  });
+
+  it('KS-1101 control — every downstream 200 {status: ok} reads up and the aggregate is healthy', async () => {
+    fetchMock.mockImplementation(async (input: unknown) => {
+      if (String(input).startsWith(baseUrl)) return realFetch(input as string);
+      return okJson({ status: 'ok' });
+    });
+    const res = await fetch(`${baseUrl}/health/deep`);
+    const body = (await res.json()) as { status: string; checks: Record<string, { status: string; error?: string }> };
+    expect(res.status).toBe(200);
+    expect(body.status).toBe('healthy');
+    expect(body.checks.anchoring.status).toBe('up');
+  });
+});
```
