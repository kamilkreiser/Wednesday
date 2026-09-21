# READY — KS-1246-SERVICESBODY-R16 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1246-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 06:16 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1246-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1246-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed5-drafter-precheck/1246SERVICESBODY-R16/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers differ (health.ts: golden `@@ -212,4 +212,5 @@` vs run `@@ -212,4 +212,5 @@ export function createHealthRoutes(`); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 06:16 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1246-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `64ab105132eada0621622acf4d6053bc59926780`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/services/health.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1246-f-2-health-services-still-reads.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/services/health.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1246-f-2-health-services-still-reads.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	1	Blockchain/Dev/services/api-gateway/src/services/health.ts
136	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1246-f-2-health-services-still-reads.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/services/health.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/services/health.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1246-f-2-health-services-still-reads.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1246-f-2-health-services-still-reads.test.ts fails at the untouched tip (1 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=1 of total=4; red cell(s): ['KS-1246 - /health/services reads a 2xx body the way the deep check does RED KS-1246 - a service answering 200 with status degraded reads degraded in /health/services, and the aggregate says degraded']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1246-f-2-health-services-still-reads.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=697 failed=0 | after: total=701 failed=0` · `NEW reds: []` [baseline_suite.json total=697 failed=0; after_suite.json total=701 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +138/-1 test=src/__tests__/ks1246-f-2-health-services-still-reads.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/services/health.ts` (+2/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1246-f-2-health-services-still-reads.test.ts` (+136/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `64ab105132eada0621622acf4d6053bc59926780` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1246-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1246-R16-SERVICESBODY.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1246-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/services/health.ts
+++ b/Blockchain/Dev/services/api-gateway/src/services/health.ts
@@ -212,4 +212,5 @@ export function createHealthRoutes(
           serviceHealth[key] = {
-            status: response.ok ? 'healthy' : 'unhealthy',
+            // KS-1246 (#1037 / KS-1101 gate F-2): a 2xx body that says degraded reads degraded, never healthy - the reading the deep check uses.
+            status: response.ok ? (((await response.json().catch(() => null)) as { status?: unknown } | null)?.status === 'degraded' ? 'degraded' : 'healthy') : 'unhealthy',
             latency: Date.now() - start,
           };
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1246-f-2-health-services-still-reads.test.ts
@@ -0,0 +1,136 @@
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
