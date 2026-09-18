# READY — KS-1248 (Ornith, briefed, vitest code_patch) — PASS 7/7 on the harness RETRY — HELD for QA

**Held 2026-09-18 12:1x by the 10:0x Wednesday seat after a source read.** Run `runs/2026-09-18_ks1248-ornith35b-night` (**the pass is `retry/`**; the first attempt failed A2b with a placeholder test file). Tip `207716440`.
Product `services/api-gateway/src/routes/system-status.ts`. It's a follow-up to #1037's N-1: `/system/status` troubleshooting called a DEGRADED required service **critical** and told operators to **restart** it.

## Source read
- Hunk 1 takes `degraded` out of the critical filter at `:528`.
- Hunk 2 gives a degraded required service **its own `warning`**. Its only command is a **read-only** `curl` of the service's health path; there's **no restart**. The comment states why: restarting a service that is up but has a sick dependency can turn a partial outage into a full one.
- **The control holds the other half:** a DOWN required service must still get `critical` and a restart command (from the brief), so the fix couldn't pass by dropping restart everywhere.
- `service.healthPath` is a real property (A7 strict `tsc` passed), so the command can't come out as `undefined`.
- Degraded OPTIONAL services still go through the existing optional branch, unchanged and out of scope.
**HELD. Not raised.**

---
## The diff, verbatim

```diff
--- a/services/api-gateway/src/routes/system-status.ts
+++ b/services/api-gateway/src/routes/system-status.ts
@@ -526,4 +526,4 @@ function generateTroubleshooting(
   // Check for unhealthy required services
   services
-    .filter(s => s.required && s.status !== 'healthy')
+    .filter(s => s.required && s.status !== 'healthy' && s.status !== 'degraded')
     .forEach(service => {
@@ -564,3 +564,20 @@ function generateTroubleshooting(
+  // KS-1248: a DEGRADED required service is up and serving with a sick dependency. Restarting it
+  // can turn a partial outage into a full one, so it gets its own advice: read what it reports
+  // and fix that dependency. Critical and restart stay reserved for a service that is down.
+  services
+    .filter(s => s.required && s.status === 'degraded')
+    .forEach(service => {
+      items.push({
+        issue: service.name + ' service is degraded',
+        severity: 'warning',
+        component: service.name,
+        resolution: service.name + ' is up but reports a failing dependency: read its degradedReasons and fix that dependency. Do not restart it.',
+        commands: [
+          '# Read what the service reports as degraded',
+          'curl -s ' + service.url + service.healthPath,
+        ],
+      });
+    });
   // Check for unhealthy optional services
   services
     .filter(s => !s.required && s.status !== 'healthy')
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1248-n-1-system-status-troubleshooting-marks.test.ts
+/**
+ * =============================================================================
+ * KS-1248 - /system/status troubleshooting never tells an operator to restart a
+ * DEGRADED required service
+ * =============================================================================
+ * After #1037 (KS-1101) a required service that answers 200 {status:'degraded'}
+ * reaches generateTroubleshooting, which classified every required service that
+ * was not 'healthy' as critical and printed restart commands for it. Degraded
+ * means up and serving with a sick dependency; a restart can turn a partial
+ * outage into a full one. Harness: the ks864a pattern - the system-status
+ * router mounted alone, fetch stubbed per host, the redis health read mocked.
+ * =============================================================================
+ */
+import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
+import http from 'node:http';
+import express from 'express';
+
+const savedEnv = { ...process.env };
+process.env.ANCHORING_SERVICE_URL = 'http://anchoring.ks1248:1';
+process.env.ORIGINATE_SERVICE_URL = 'http://originate.ks1248:1';
+
+/** What each probed host answers in the current cell. A host not listed answers healthy. */
+const answers: Record<string, 'up' | 'degraded' | 'down'> = {};
+
+vi.mock('../services/redis', () => ({ getRedisHealth: vi.fn(async () => ({ status: 'healthy' })) }));
+vi.stubGlobal('fetch', vi.fn(async (url: string) => {
+  const kind = answers[new URL(String(url)).hostname] ?? 'up';
+  if (kind === 'down') return new Response(JSON.stringify({ status: 'unhealthy' }), { status: 503 });
+  if (kind === 'degraded') return new Response(JSON.stringify({ status: 'degraded', degradedReasons: ['ks1248: dependency unreachable'] }), { status: 200 });
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
+const restarts = (item: any): boolean => (item?.commands ?? []).some((c: string) => /restart/i.test(c));
+
+describe('KS-1248: /system/status troubleshooting for a degraded required service', () => {
+  it('control: with every service up there is no advice for anchoring or originate', async () => {
+    answers['anchoring.ks1248'] = 'up';
+    answers['originate.ks1248'] = 'up';
+    const a = await adviceFor('anchoring');
+    const o = await adviceFor('originate');
+    expect([a.length, o.length]).toEqual([0, 0]);
+  });
+
+  it('control: a DOWN required service (originate answers 503) is still critical and still told to restart', async () => {
+    answers['anchoring.ks1248'] = 'up';
+    answers['originate.ks1248'] = 'down';
+    const o = await adviceFor('originate');
+    expect([o.length, o[0]?.severity, restarts(o[0])]).toEqual([1, 'critical', true]);
+  });
+
+  it('\ud83d\udd34 a DEGRADED required service (anchoring answers 200 degraded) gets one warning and no restart command', async () => {
+    answers['anchoring.ks1248'] = 'degraded';
+    answers['originate.ks1248'] = 'up';
+    const a = await adviceFor('anchoring');
+    expect([a.length, a[0]?.severity, restarts(a[0])]).toEqual([1, 'warning', false]);
+  });
+});
```
