# READY — KS-1360 WALLET-SESSION-DELETE-SUCCESS-TRUE (spark-dsv4flash, briefed, first round) — PASS 7/7 — HELD for QA

> **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-29_KS-1360-R1/out.md.checker/patch.diff`**. **BYTE-IDENTICAL to the brief-writer's golden** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1360/KS-1360.golden.diff` (`cmp` rc 0; a control against a different ticket's golden rc 1), measured by Wednesday.

**Held BY HAND at 09:31 2026-09-29 by Wednesday morning seat 407373b1** (hold_ready.py's owed defect). Source develop **0de108577e61** (the round's source clone has a GitHub origin).

- **What:** wallet-connector server.ts DELETE /api/wallets/session/:id: the 200 reply gains success: true (additive).
- **Authority:** Kam ruled card `secuura-ks1360-wallet-session-delete-reply-shape` = (a) on the live board 2026-09-29 09:05 AEST.
- **Brief + golden + README:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1360/` (the README states the red/green and suite counts and what the brief-writer could not measure; the raise seat reads it and carries its NOT COVERED into the PR body).
- Checker verdict [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`
  - `PASS A3 touched-file set == { Blockchain/Dev/services/wallet-connector/src/server.ts , Blockchain/Dev/services/wallet-connector/src/__tests__/ks1360-session-delete-carries-success.test.ts }`
  - `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)`
  - `PASS A4 RED-FIRST: src/__tests__/ks1360-session-delete-carries-success.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)`
  - `PASS A5 GREEN-AFTER: src/__tests__/ks1360-session-delete-carries-success.test.ts passes with the product hunk (3 passed / 3 run)`
  - `PASS A6 whole services/wallet-connector suite: no NEW red vs the untouched tip`
  - `PASS A7 tsc --noEmit for services/wallet-connector: rc 0 after the patch (baseline rc=0)`
  - `SUMMARY files=2 +76/-1 test=src/__tests__/ks1360-session-delete-carries-success.test.ts red_first=yes apply_mode=strict`
  - `RESULT: PASS (7/7)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=1)`
  - `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`

```diff
--- a/Blockchain/Dev/services/wallet-connector/src/server.ts
+++ b/Blockchain/Dev/services/wallet-connector/src/server.ts
@@ -219,2 +219,2 @@
-  res.json({ message: 'Session disconnected' });
+  res.json({ success: true, message: 'Session disconnected' });
 });
--- /dev/null
+++ b/Blockchain/Dev/services/wallet-connector/src/__tests__/ks1360-session-delete-carries-success.test.ts
@@ -0,0 +1,75 @@
+/**
+ * KS-1360 - DELETE /api/wallets/session/:sessionId answers the declared 200
+ * body: WalletSuccessSchema requires a boolean success, and the handler sent
+ * only message. Drives the REAL server.ts app on 127.0.0.1. server.ts boots
+ * at import, so the boot is held off: initDb never settles (no listen), the DB
+ * reads as unavailable (the in-memory path), the user.erased subscriber is a
+ * no-op, and the shared JWT check is a pass-through (auth is not under test).
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import http from 'http';
+import type { AddressInfo } from 'net';
+import type { RequestHandler } from 'express';
+
+vi.mock('../db', () => ({
+  initDb: () => new Promise<boolean>(() => {}),
+  isDbAvailable: () => false,
+  query: async () => ({ rows: [], rowCount: 0 }),
+}));
+vi.mock('../userErasedSubscriber', () => ({
+  startUserErasedSubscriber: async () => {},
+}));
+vi.mock('@secuura/shared', async (importOriginal) => ({
+  ...(await importOriginal<Record<string, unknown>>()),
+  authenticate: () => ((_req, _res, next) => next()) as RequestHandler,
+}));
+
+import app from '../server';
+
+let base = '';
+let server: http.Server;
+
+beforeAll(async () => {
+  server = http.createServer(app);
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  await new Promise<void>((resolve) => server?.close(() => resolve()));
+});
+
+async function call(method: string, path: string, body?: object): Promise<[number, unknown]> {
+  const r = await fetch(base + path, {
+    method,
+    headers: body ? { 'content-type': 'application/json' } : {},
+    body: body ? JSON.stringify(body) : undefined,
+  });
+  return [r.status, await r.json()];
+}
+
+async function newSession(): Promise<string> {
+  const [status, body] = await call('POST', '/api/wallets/session', { walletType: 'nami', address: 'addr_ks1360' });
+  expect(status).toBe(201);
+  return (body as { sessionId: string }).sessionId;
+}
+
+describe('KS-1360 DELETE /api/wallets/session/:sessionId', () => {
+  it('RED KS-1360 D1: a live session disconnects 200 with success true and the message', async () => {
+    const id = await newSession();
+    expect(await call('DELETE', '/api/wallets/session/' + id)).toEqual([200, { success: true, message: 'Session disconnected' }]);
+  });
+
+  it('control KS-1360: an unknown session is still 404 NOT_FOUND', async () => {
+    expect(await call('DELETE', '/api/wallets/session/ks1360-unknown')).toEqual([
+      404,
+      { success: false, error: { code: 'NOT_FOUND', message: 'Session not found' } },
+    ]);
+  });
+
+  it('control KS-1360: the session is gone after the disconnect, a second DELETE is 404', async () => {
+    const id = await newSession();
+    expect((await call('DELETE', '/api/wallets/session/' + id))[0]).toBe(200);
+    expect((await call('DELETE', '/api/wallets/session/' + id))[0]).toBe(404);
+  });
+});
```
