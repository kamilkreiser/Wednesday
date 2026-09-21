# KS-1246 R16-SERVICESBODY - Wednesday's task for Ornith: /health/services reads a 2xx body the way the deep check does - a service that says degraded reads degraded, never healthy (code_patch, vitest, ONE product hunk + ONE NEW test file) at develop 64ab10513 (written 05:51 on 2026-09-22 by Wednesday's feed5 drafter from services/api-gateway/src/services/health.ts:96-237 read at the tip and ks1101-health-aggregates-surface-degraded.test.ts:1-120 read for its stub shape)
Tip: `64ab105132eada0621622acf4d6053bc59926780`
Runner: `vitest`

## Premises (measured by the feed5 drafter at 05:51 on 2026-09-22 AEST, in a `--shared` scratchpad clone detached at 64ab10513; Wednesday re-derives before queueing)
- Ticket KS-1246 (P4, Backlog, unassigned, no PR attachment; the #1037 / KS-1101 tier-1 gate's F-2, graded SHIPS-WITH): "/health/services is the one aggregate #1037 didn't change. It still decides health from response.ok alone, so a 200 {status:'degraded'} reads healthy. ... Either route it through the same body-aware reading services/health.ts now uses, or remove the endpoint if nothing is meant to opt in." THE DRAFTER'S READING (one line; Wednesday may veto): shape 1 - route it through the body-aware reading. Shape 2 (remove the endpoint) is a product decision and a two-file change (the route, its listing at `index.ts:809` and the boot banner at `:1236`), outside this contract. The HTTP status rule is NOT changed: the endpoint already answers 503 `degraded` for anything that is not `healthy` (`:226-229`), and the O-SURFACE ruling on KS-1101 (readiness counts only `down`) named `/health/ready` and `/status/simple` as the readiness pair - `/health/services` is the opt-in monitoring map, not a readiness probe, so a degraded service makes it 503 `degraded` exactly as an unhealthy one does today. The vocabulary question (a 2xx body saying `unhealthy`, KS-1249) is NOT this ticket: only `status === 'degraded'` reads degraded, the deep check's own rule (`:139-140`).
- The site at 64ab10513: `health.ts:213` is `            status: response.ok ? 'healthy' : 'unhealthy',` inside the `/health/services` handler's per-service `try` (`:202-215`). The hunk is ONE edit with non-blank context on both sides (`:212` above, `:214-215` below); the blank lines `:209` and `:211` are outside it. Strict `git apply --check` rc 0 measured.
- The abort timer (`:204`, cleared at `:210`) is NOT re-armed for the body read - the same order the tip has for the response itself; a 2xx service whose body never arrives is a class the tip never read at all, and is not this ticket. A non-JSON 2xx body reads `healthy` (the `.catch(() => null)` arm), as it does at the tip.
- The test file is ABSENT at 64ab10513 - ONE NEW FILE (`ls src/__tests__ | grep -c -i ks1246` = 0). Its name IS the input's `suggested_test_file` (the builder's slug from the ticket title, measured at the 05:51 build) - the `File:` line under `## The test` and the input agree. Harness: the real `createHealthRoutes` on a bare express app over a redis-like object, three loopback stubs (200 healthy / 200 degraded / 503 unhealthy) and a refused loopback port (`127.0.0.1:2`, a real ECONNREFUSED - never port 1, the Fetch bad-port list); `../db` is mocked so importing health.ts opens no pool.
- Typecheck (the 16th round's per-file method, test file + product AFTER the patch; `runs/2026-09-22_feed5-drafter-precheck/typecheck/typecheck_feed5.log`, 05:50:18 AEST): 0 errors IN THE TEST FILE and none at the patched lines; the per-file program reports the same 4 out-of-file `req.user` errors (`auth.ts:321/362/400`, `health.ts:40`) that feed4 reproduced on the tip's untouched ks480 file through the same program - the instrument's incomplete program, not the change; a planted TS2322 CAUGHT. The golden's A7 (whole-service `tsc --noEmit`) is the authority.
- Every `+` line of both fences is ASCII-only, backslash-free and carries NO double-quote character (measured: 136 test lines, 2 product lines, 0 / 0 / 0; odd-quote lines []).
- Collision check: no PR of the 16th round touches health.ts (Seat C 16th's api-gateway files are ks864c/ks1123/ks1073/ks1185/ks1199/ks1204 test files, system-status.ts and verification.ts). ONE held READY touches health.ts: `READY_KS-1231-B_*` (the info reader, `:45-52`, a different hunk 160 lines above); both apply orders are measured in the proposal (`runs/.../orders_1231B_1246.log`). No held READY names KS-1246.

## What is wrong (one paragraph)
`GET /health/services` (`services/api-gateway/src/services/health.ts:193-234`, opt-in through `ENABLE_PUBLIC_HEALTH_SERVICES=true`, 404 otherwise) probes every configured service's health path and classifies each by `response.ok` alone (`:213`), so anchoring, auth or originate answering HTTP 200 with `status: 'degraded'` (the KS-1101 class: chain unreachable, in-memory fallbacks) reads `healthy` there while `/health/deep` reads `degraded` for the same answer. The fix reads the 2xx body the way the deep check's `probeService` does (`:139-140`): a body whose `status` is `'degraded'` reads `degraded`; the aggregate then says `degraded` (503) by the rule it already applies. NOT in this task: the deep check, `/system/status`, the endpoint's opt-in gate, the HTTP status rule, the `unhealthy`-body vocabulary (KS-1249), removing the endpoint (shape 2).

## The exact change - ONE EDIT in the product file (one hunk: context :212, the ONE `-` line :213 replaced by 2 `+` lines, then context :214-215)
E1 - `services/api-gateway/src/services/health.ts`: line 213 (the `-` line) is REPLACED by a comment line and the body-aware status line. The hunk header is `@@ -212,4 +212,5 @@` - copy it. Twelve-space indent on both `+` lines (the same as the `-` line).
```
@@ -212,4 +212,5 @@
           serviceHealth[key] = {
-            status: response.ok ? 'healthy' : 'unhealthy',
+            // KS-1246 (#1037 / KS-1101 gate F-2): a 2xx body that says degraded reads degraded, never healthy - the reading the deep check uses.
+            status: response.ok ? (((await response.json().catch(() => null)) as { status?: unknown } | null)?.status === 'degraded' ? 'degraded' : 'healthy') : 'unhealthy',
             latency: Date.now() - start,
           };
```
Copy every `+` line byte for byte; the one `-` line is the tip's :213 exactly; the three context lines are the tip's :212, :214, :215 with their leading space.

## The test - ONE NEW vitest file, in-process (the ks1101 stub shape over the real createHealthRoutes, no app boot)
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1246-f-2-health-services-still-reads.test.ts`
NEW file: `--- /dev/null` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1246-f-2-health-services-still-reads.test.ts` then ONE hunk `@@ -0,0 +1,136 @@`, every line `+`. Do NOT modify the reference test; copy its shape from this fence only. Every file-scope declaration the cells use is in the fence (stubs, listen, closeServer, stubService, healthServices, healthyUrl, degradedUrl, downUrl).
```
+// =============================================================================
+// KS-1246 (#1037 / KS-1101 gate F-2) - /health/services still read response.ok
+//          alone, so a service answering 200 {status: 'degraded'} read healthy
+// =============================================================================
+//
+// /health/services is the one aggregate #1037 did not change. It decided a
+// service health from response.ok, so a probed service that reports itself
+// degraded on a 2xx read `healthy` there while /health/deep read `degraded`.
+// Now it reads the body the way the deep check does: a 2xx whose body carries
+// status 'degraded' reads degraded, and the aggregate says degraded (503, the
+// rule the endpoint already applies to anything that is not healthy).
+//
+// Harness: the real createHealthRoutes mounted on a bare express app over a
+// redis-like object, every probed service pointed at one of two loopback stubs
+// (200 healthy / 200 degraded / 503 unhealthy) or at a refused loopback port;
+// ENABLE_PUBLIC_HEALTH_SERVICES=true because the endpoint is opt-in, 404 by
+// default. No gateway boot, no Redis, no database (`../db` is mocked).
+// =============================================================================
+
+import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
+import express from 'express';
+import http from 'http';
+import type { AddressInfo } from 'net';
+
+vi.mock('../db', async (orig) => {
+  const real = (await orig()) as Record<string, unknown>;
+  return { ...real, isDbAvailable: () => false, query: async () => ({ rows: [], rowCount: 0 }) };
+});
+
+type Kind = 'healthy' | 'degraded' | 'down';
+type Got = { status: number; body: any };
+
+const stubs: http.Server[] = [];
+
+async function listen(server: http.Server): Promise<string> {
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  return `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+}
+
+async function closeServer(server: http.Server | undefined): Promise<void> {
+  if (!server) return;
+  server.closeAllConnections();
+  await new Promise<void>((r) => server.close(() => r()));
+}
+
+/** A probed service: 200 {status: healthy}, 200 {status: degraded, degradedReasons}, or 503 {status: unhealthy}. */
+async function stubService(kind: Kind): Promise<string> {
+  const server = http.createServer((_req, res) => {
+    const [code, body] = kind === 'down'
+      ? [503, { status: 'unhealthy' }]
+      : kind === 'degraded'
+        ? [200, { status: 'degraded', degradedReasons: ['ks1246: chain unreachable'] }]
+        : [200, { status: 'healthy' }];
+    res.writeHead(code, { 'content-type': 'application/json' });
+    res.end(JSON.stringify(body));
+  });
+  stubs.push(server);
+  return listen(server);
+}
+
+/** Mount the real health routes over the given services and answer GET /health/services. */
+async function healthServices(urls: Record<string, string>): Promise<Got> {
+  const { createHealthRoutes } = await import('../services/health');
+  const services: Record<string, any> = {};
+  for (const [name, url] of Object.entries(urls)) services[name] = { name, url, healthPath: '/health', requiresAuth: false };
+  const app = express();
+  app.use(createHealthRoutes(services, { getNotificationSettings: async () => null, getRedisClient: () => null } as any));
+  const gateway = http.createServer(app as http.RequestListener);
+  const base = await listen(gateway);
+  try {
+    return await new Promise<Got>((resolve, reject) => {
+      const target = new URL(base);
+      const req = http.request({ hostname: target.hostname, port: target.port, path: '/health/services', method: 'GET', agent: false }, (res) => {
+        const chunks: Buffer[] = [];
+        res.on('data', (c: Buffer) => chunks.push(c));
+        res.on('end', () => {
+          let body: any = null;
+          try { body = JSON.parse(Buffer.concat(chunks).toString()); } catch { body = null; }
+          resolve({ status: res.statusCode ?? 0, body });
+        });
+      });
+      req.setTimeout(30000, () => req.destroy(new Error('no answer from /health/services within 30 s')));
+      req.on('error', reject);
+      req.end();
+    });
+  } finally {
+    await closeServer(gateway);
+  }
+}
+
+let healthyUrl = '';
+let degradedUrl = '';
+let downUrl = '';
+
+beforeAll(async () => {
+  vi.stubEnv('ENABLE_PUBLIC_HEALTH_SERVICES', 'true');
+  healthyUrl = await stubService('healthy');
+  degradedUrl = await stubService('degraded');
+  downUrl = await stubService('down');
+});
+
+afterAll(async () => {
+  vi.unstubAllEnvs();
+  for (const s of stubs) await closeServer(s);
+});
+
+describe('KS-1246 - /health/services reads a 2xx body the way the deep check does', () => {
+  it('RED KS-1246 - a service answering 200 with status degraded reads degraded in /health/services, and the aggregate says degraded', async () => {
+    const got = await healthServices({ auth: healthyUrl, anchoring: degradedUrl });
+    expect([got.status, got.body?.services?.anchoring?.status, got.body?.services?.auth?.status, got.body?.status])
+      .toEqual([503, 'degraded', 'healthy', 'degraded']);
+  });
+
+  it('control: every service answering 200 with status healthy reads healthy, and the aggregate is 200 healthy', async () => {
+    const got = await healthServices({ auth: healthyUrl, originate: healthyUrl });
+    expect([got.status, got.body?.services?.auth?.status, got.body?.services?.originate?.status, got.body?.status, got.body?.gateway])
+      .toEqual([200, 'healthy', 'healthy', 'healthy', 'healthy']);
+  });
+
+  it('control: a 503 answer reads unhealthy and a refused port reads unreachable, and the aggregate is 503 degraded', async () => {
+    const got = await healthServices({ auth: downUrl, billing: 'http://127.0.0.1:2' });
+    expect([got.status, got.body?.services?.auth?.status, got.body?.services?.billing?.status, got.body?.status])
+      .toEqual([503, 'unhealthy', 'unreachable', 'degraded']);
+    expect(typeof got.body?.services?.billing?.error).toBe('string');
+  });
+
+  it('control: with ENABLE_PUBLIC_HEALTH_SERVICES unset the endpoint stays opt-in and answers 404', async () => {
+    vi.stubEnv('ENABLE_PUBLIC_HEALTH_SERVICES', '');
+    try {
+      const got = await healthServices({ auth: degradedUrl });
+      expect([got.status, got.body?.error?.code]).toEqual([404, 'NOT_FOUND']);
+    } finally {
+      vi.stubEnv('ENABLE_PUBLIC_HEALTH_SERVICES', 'true');
+    }
+  });
+});
```
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('RED KS-1246 - a service answering 200 with status degraded reads degraded in /health/services, and the aggregate says degraded')` - two services, one healthy and one degraded. At the tip: `[200, 'healthy', 'healthy', 'healthy']` (the red, by assertion); after E1: `[503, 'degraded', 'healthy', 'degraded']`.
- CONTROL `it('control: every service answering 200 with status healthy reads healthy, and the aggregate is 200 healthy')` - `[200, 'healthy', 'healthy', 'healthy', 'healthy']` on both trees.
- CONTROL `it('control: a 503 answer reads unhealthy and a refused port reads unreachable, and the aggregate is 503 degraded')` - `[503, 'unhealthy', 'unreachable', 'degraded']` and a string `error` on both trees.
- CONTROL `it('control: with ENABLE_PUBLIC_HEALTH_SERVICES unset the endpoint stays opt-in and answers 404')` - `[404, 'NOT_FOUND']` on both trees.

## Red cells
- RED KS-1246 - a service answering 200 with status degraded reads degraded in /health/services, and the aggregate says degraded

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:213` - **must change**: `            status: response.ok ? 'healthy' : 'unhealthy',`
* `:212` - (correct) `          serviceHealth[key] = {` - stays (the leading context)
* `:214` - (correct) `            latency: Date.now() - start,` - stays (trailing context)
* `:215` - (correct) `          };` - stays (trailing context)
* `:226` - (correct) `    const allHealthy = Object.values(serviceHealth).every(s => s.status === 'healthy');` - stays; a degraded service falls out of it exactly as an unhealthy one does

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/api-gateway/src/services/health.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/services/health.ts` with the E1 hunk (header `@@ -212,4 +212,5 @@`), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1246-f-2-health-services-still-reads.test.ts` with the one new-file hunk (header `@@ -0,0 +1,136 @@` - 136 is the count of `+` lines); no double quote, no `\$` / `\u` / backslash of any kind in a `+` line; every context line of the product hunk keeps its leading space.
