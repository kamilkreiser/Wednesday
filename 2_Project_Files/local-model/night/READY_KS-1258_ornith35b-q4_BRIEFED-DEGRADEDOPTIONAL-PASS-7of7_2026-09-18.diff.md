# READY — KS-1258 (Ornith, briefed, vitest code_patch) — PASS 7/7 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1258-ornith35b-night/out.md.checker/section_N.diff`, each applied with its `section_N.opts`.** Raise from those, not from the fence below.

**Held 2026-09-18 15:20 by the 14:4x Wednesday seat after a source read.** Run `runs/2026-09-18_ks1258-ornith35b-night`. Tip `8b9c3f022` (builder's ls-remote pin). Product `services/api-gateway/src/routes/system-status.ts`. Brief `night/briefs/KS-1258.md` (search subagent, 14:5x-15:0x).

## Source read
- A DEGRADED OPTIONAL service is told to read its degradedReasons (a read-only curl of its health path), never to start/restart it; the existing optional branch now excludes degraded. Sibling of KS-1248 (#1039, merged). Red 1/3 at tip, 3/3 after.
- The product hunk's '+' and '-' lines are IDENTICAL to the brief's edit block (Wednesday's line compare; crossed control KS-1258 brief vs KS-1230 diff = 17 of 17 missing, so the compare can fail).
- Checker: A1-A7 PASS incl. A6 (whole api-gateway suite, no NEW red) and A7 strict tsc.
**HELD. Not raised.** Refs KS-1258, linkKind contributes, no closing phrase.

---
## The model's output, verbatim

```diff
--- a/services/api-gateway/src/routes/system-status.ts
+++ b/services/api-gateway/src/routes/system-status.ts
@@ -581,4 +581,20 @@
+  // KS-1258: a DEGRADED optional service is already up, with a sick dependency, so it is not told to
+  // start or restart: it gets the same read-first advice KS-1248 gave a degraded required service.
+  services
+    .filter(s => !s.required && s.status === 'degraded')
+    .forEach(service => {
+      items.push({
+        issue: service.name + ' service is degraded (optional)',
+        severity: 'warning',
+        component: service.name,
+        resolution: service.name + ' is optional and up but reports a failing dependency: read its degradedReasons and fix that dependency. Do not start or restart it.',
+        commands: [
+          '# Read what the service reports as degraded',
+          'curl -s ' + service.url + service.healthPath,
+        ],
+      });
+    });
   // Check for unhealthy optional services
   services
-    .filter(s => !s.required && s.status !== 'healthy')
+    .filter(s => !s.required && s.status !== 'healthy' && s.status !== 'degraded')
     .forEach(service => {
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1258-degraded-optional-service-advice.test.ts
@@ -0,0 +1,84 @@
+/**
+ * =============================================================================
+ * KS-1258 - /system/status never tells an operator to START a DEGRADED optional
+ * service that is already up
+ * =============================================================================
+ * KS-1248 gave a degraded REQUIRED service its own advice. A degraded OPTIONAL
+ * service still fell into the not-healthy optional branch of
+ * generateTroubleshooting, whose advice is "Start the service locally" and
+ * "npm run dev". The service is up with a sick dependency; starting it is wrong.
+ * Harness: the ks1248 pattern - the system-status router mounted alone, fetch
+ * stubbed per host, the redis health read mocked.
+ * =============================================================================
+ */
+import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
+import http from 'node:http';
+import express from 'express';
+
+const savedEnv = { ...process.env };
+process.env.BILLING_SERVICE_URL = 'http://billing.ks1258:1';
+process.env.STAKING_SERVICE_URL = 'http://staking.ks1258:1';
+
+/** What each probed host answers in the current cell. A host not listed answers healthy. */
+const answers: Record<string, 'up' | 'degraded' | 'down'> = {};
+
+vi.mock('../services/redis', () => ({ getRedisHealth: vi.fn(async () => ({ status: 'healthy' })) }));
+vi.stubGlobal('fetch', vi.fn(async (url: string) => {
+  const kind = answers[new URL(String(url)).hostname] ?? 'up';
+  if (kind === 'down') return new Response(JSON.stringify({ status: 'unhealthy' }), { status: 503 });
+  if (kind === 'degraded') return new Response(JSON.stringify({ status: 'degraded', degradedReasons: ['ks1258: dependency unreachable'] }), { status: 200 });
+  return new Response(JSON.stringify({ status: 'healthy' }), { status: 200 });
+}));
+
+let server: ReturnType<ReturnType<typeof express>['listen']>; let port = 0;
+beforeAll(async () => {
+  const router = (await import('../routes/system-status')).default;
+  const app = express(); app.use('/system', router);
+  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => { port = (server.address() as any).port; r(); }); });
+}, 10_000);
+afterAll(async () => {
+  await new Promise<void>((r) => server.close(() => r()));
+  for (const k of Object.keys(process.env)) if (!(k in savedEnv)) delete process.env[k];
+  Object.assign(process.env, savedEnv);
+  vi.unstubAllGlobals();
+});
+
+function getJson(path: string): Promise<any> {
+  return new Promise((resolve, reject) => {
+    http.get({ hostname: '127.0.0.1', port, path }, (res) => {
+      let data = ''; res.on('data', (c) => (data += c));
+      res.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
+    }).on('error', reject);
+  });
+}
+
+/** The troubleshooting items GET /system/status emits for one component. */
+async function adviceFor(component: string): Promise<any[]> {
+  const body = await getJson('/system/status');
+  return (body.troubleshooting ?? []).filter((i: any) => i.component === component);
+}
+const startsOrRestarts = (item: any): boolean => (item?.commands ?? []).some((c: string) => /npm run dev|restart/i.test(c));
+
+describe('KS-1258: /system/status troubleshooting for a degraded optional service', () => {
+  it('control: with every service up there is no advice for billing or staking', async () => {
+    answers['billing.ks1258'] = 'up';
+    answers['staking.ks1258'] = 'up';
+    const b = await adviceFor('billing');
+    const s = await adviceFor('staking');
+    expect([b.length, s.length]).toEqual([0, 0]);
+  });
+
+  it('control: a DOWN optional service (staking answers 503) is still a warning and still told to start it', async () => {
+    answers['billing.ks1258'] = 'up';
+    answers['staking.ks1258'] = 'down';
+    const s = await adviceFor('staking');
+    expect([s.length, s[0]?.severity, startsOrRestarts(s[0])]).toEqual([1, 'warning', true]);
+  });
+
+  it('\ud83d\udd34 a DEGRADED optional service (billing answers 200 degraded) gets one warning and no start or restart command', async () => {
+    answers['billing.ks1258'] = 'degraded';
+    answers['staking.ks1258'] = 'up';
+    const b = await adviceFor('billing');
+    expect([b.length, b[0]?.severity, startsOrRestarts(b[0])]).toEqual([1, 'warning', false]);
+  });
+});
```
