# READY — KS-1369 GATEWAY-PROXY-SKIP-WHEN-HEADERS-SENT (spark-dsv4flash, briefed, first round) — PASS 7/7 — HELD for QA

> **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-29_KS-1369-R1/out.md.checker/patch.diff`**. **BYTE-IDENTICAL to the brief-writer's golden** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1369/KS-1369.golden.diff` (`cmp` rc 0; a control against a different ticket's golden rc 1), measured by Wednesday.

**Held BY HAND at 09:31 2026-09-29 by Wednesday morning seat 407373b1** (hold_ready.py's owed defect). Source develop **0de108577e61** (the round's source clone has a GitHub origin).

- **What:** api-gateway routes/proxy.ts onProxyReq: return early when the outgoing request headers are already sent.
- **Authority:** Kam ruled card `secuura-ks1369-gateway-proxy-crash-guard-shape` = (a) on the live board 2026-09-29 09:05 AEST.
- **Brief + golden + README:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1369/` (the README states the red/green and suite counts and what the brief-writer could not measure; the raise seat reads it and carries its NOT COVERED into the PR body).
- Checker verdict [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`
  - `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/proxy.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1369-onproxyreq-skips-header-writes-once-sent.test.ts }`
  - `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)`
  - `PASS A4 RED-FIRST: src/__tests__/ks1369-onproxyreq-skips-header-writes-once-sent.test.ts fails at the untouched tip (2 failed / 3 run; controls green; assertion reds)`
  - `PASS A5 GREEN-AFTER: src/__tests__/ks1369-onproxyreq-skips-header-writes-once-sent.test.ts passes with the product hunk (3 passed / 3 run)`
  - `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip`
  - `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
  - `SUMMARY files=2 +65/-0 test=src/__tests__/ks1369-onproxyreq-skips-header-writes-once-sent.test.ts red_first=yes apply_mode=strict`
  - `RESULT: PASS (7/7)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=1)`
  - `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts
@@ -242,2 +242,4 @@
     onProxyReq: (proxyReq, req) => {
+      // KS-1369: once the outgoing headers are sent, every setHeader below throws; skip the writes.
+      if (proxyReq.headersSent) return;
       // Forward request ID
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1369-onproxyreq-skips-header-writes-once-sent.test.ts
@@ -0,0 +1,63 @@
+/**
+ * KS-1369 - onProxyReq must not write headers once the outgoing request's
+ * headers are already sent. Under load the hook's first setHeader threw
+ * Cannot set headers after they are sent to the client, as an uncaught
+ * exception and the gateway process exited. Drives the REAL hook: the options
+ * createServiceProxy hands to http-proxy-middleware are captured, and
+ * onProxyReq is called directly with a fake proxyReq. No network, no app boot.
+ */
+import { describe, it, expect, vi } from 'vitest';
+import type { RequestHandler } from 'express';
+
+const captured = vi.hoisted(() => [] as Array<Record<string, any>>);
+vi.mock('http-proxy-middleware', () => ({
+  createProxyMiddleware: (opts: Record<string, any>) => {
+    captured.push(opts);
+    return ((_req, _res, next) => next()) as RequestHandler;
+  },
+}));
+
+import { createProxyRoutes } from '../routes/proxy';
+
+createProxyRoutes({
+  services: { auth: { name: 'auth', url: 'http://ks1369-auth:4000', healthPath: '/health', requiresAuth: false } },
+  authenticateToken: () => ((_req, _res, next) => next()) as RequestHandler,
+  log: () => {},
+});
+const hook = captured.find((o) => o.target === 'http://ks1369-auth:4000')!.onProxyReq;
+
+function fakeProxyReq(headersSent: boolean, throwOnSet: boolean) {
+  const calls: string[] = [];
+  const setHeader = (name: string) => {
+    if (throwOnSet) throw new Error('Cannot set headers after they are sent to the client');
+    calls.push('set ' + name);
+  };
+  return { calls, headersSent, setHeader, write: () => { calls.push('write'); } };
+}
+
+const loginReq = { requestId: 'req-ks1369', method: 'POST', headers: { authorization: 'Bearer ks1369' }, body: { email: 'a@b.c' } };
+
+describe('KS-1369 onProxyReq once the outgoing headers are sent', () => {
+  it('RED KS-1369 H1: headersSent true and setHeader throwing, the hook does not throw', () => {
+    const p = fakeProxyReq(true, true);
+    expect(() => hook(p, loginReq)).not.toThrow();
+  });
+
+  it('RED KS-1369 H2: headersSent true, the hook sets no header and writes no body', () => {
+    const p = fakeProxyReq(true, false);
+    hook(p, loginReq);
+    expect(p.calls).toEqual([]);
+  });
+
+  it('control KS-1369: headersSent false, the hook still sets its headers and writes the body', () => {
+    const p = fakeProxyReq(false, false);
+    hook(p, loginReq);
+    expect(p.calls).toEqual([
+      'set X-Request-ID',
+      'set Authorization',
+      'set Content-Type',
+      'set Content-Length',
+      'write',
+    ]);
+  });
+});
```
