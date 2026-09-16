# READY — KS-1185 F4 PARTIAL (pin the 15 s production default of the approve route's originate forward: NEW test ks1185-workflow-approve-forward-default-bound.test.ts builds the REAL route with NO override, reads the bound the forward is armed with and fires that call's own callback → 502 + document kept, no 15 s wait) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (05:04:39). Held by Wednesday at 05:07 AEST. Run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-17_ks1185-ornith35b-night
# Source read by me (Wednesday): the model's 108 `+` lines IDENTICAL in sequence to the brief's ```ts block (python compare; a one-character mutated copy compares unequal = the control); one new file, verification.ts untouched; apply STRICT; A4 under the #1010 gate's Q-DEFAULT-0 tamper (verification.ts:426 default → 0) 1 red by assertion / 2 run, control green; A5 2/2; A6 api-gateway 408 → 410, NEW reds []; A7 tsc rc 0 (the service tsconfig excludes __tests__ — the test file's own tsc rc 0, not gated).
# NOT GRADED BY THE CHECKER (brief premises): the Q-LATE-16s / Q-LATE-29999 rows and the two reach tampers (override ignored at the call; setTimeout removed) — graded in the writer's pre-measure.
# PR NOTES: "Refs KS-1185 (F4)" — F1 (validate the override), F2 (idle-not-total bound), F3 (misleading late log) stay open, product edits, not local. Test-only → tier 2; runtime unchanged, so the §5f Done rule does not apply, but KS-1185 stays open for F1–F3. New file only; verification.ts is seat A's KS-1072 lane.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-workflow-approve-forward-default-bound.test.ts
@@ -0,0 +1,108 @@
+// KS-1185 F4 (KS-1183 gate on #1010): no cell built the approve route WITHOUT originateForwardTimeoutMs, so the
+// production default was never exercised: the default set to 0 (never), 16_000 or 29_999 reddened 0 of 402 cells.
+// These cells build the REAL route and read the bound the forward request is armed with, without waiting 15 s.
+import { describe, it, expect, afterEach, vi } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+import * as verification from '../routes/verification';
+
+const DOC_ID = 'doc-ks1185';
+const WFI_ID = 'wfi-ks1185';
+/** The bound index.ts gets today, because it passes no override (ORIGINATE_FORWARD_TIMEOUT_MS, KS-1183). */
+const PRODUCTION_DEFAULT_MS = 15_000;
+/** A short override, so the control can let the real timer fire. */
+const OVERRIDE_MS = 300;
+
+type Log = (level: 'info' | 'warn' | 'error', message: string, meta?: object) => void;
+type Drive = { status: number; ms: number; bounds: unknown[]; errors: unknown[]; deletes: number; hits: number };
+
+const servers: http.Server[] = [];
+const restores: Array<() => void> = [];
+
+afterEach(async () => {
+  for (const restore of restores.splice(0)) restore();
+  for (const server of servers.splice(0)) {
+    server.closeAllConnections();
+    await new Promise<void>((r) => server.close(() => r()));
+  }
+});
+
+async function listen(server: http.Server): Promise<number> {
+  servers.push(server);
+  server.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  return (server.address() as AddressInfo).port;
+}
+
+const sleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));
+
+async function drive(override: number | undefined, fireTheBound: boolean): Promise<Drive> {
+  const pendingDocs = new Map([[DOC_ID, { title: 't', contentHash: 'h', createdBy: 'u' }]]);
+  let deletes = 0;
+  let hits = 0;
+  const instance = { status: 'pending_approval', documentId: DOC_ID, steps: [{ name: 'Approve' }], currentStepIndex: 0 };
+  const originatePort = await listen(http.createServer((req) => { hits++; req.resume(); }));
+  const log = vi.fn<Log>();
+  const deps = {
+    authenticateToken: (): RequestHandler => (_req, _res, next) => next(),
+    mockBodyParser: express.json({ limit: '1mb' }),
+    query: vi.fn(async () => ({ rows: [] })) as never,
+    isDbAvailable: () => false,
+    redisService: {
+      getWorkflowInstance: vi.fn(async (id: string) => (id === WFI_ID ? structuredClone(instance) : null)),
+      setWorkflowInstance: vi.fn(async () => undefined),
+      getPendingDocument: vi.fn(async (id: string) => pendingDocs.get(id) ?? null),
+      deletePendingDocument: vi.fn(async (id: string) => { deletes++; pendingDocs.delete(id); }),
+    } as never,
+    services: { originate: { url: `http://127.0.0.1:${originatePort}` }, anchoring: { url: '' } } as never,
+    log,
+    memWorkflowToDocumentMap: new Map(),
+    memRejectedDocuments: new Map(),
+    dbSaveRejection: vi.fn(async () => undefined),
+    ADMIN_ROLES: ['ADMIN'],
+    enforceDocumentTypeRules: vi.fn(async () => ({ ok: true, docType: {} })) as never,
+    createWorkflowInstanceIfRequired: vi.fn(async () => ({ gated: false })) as never,
+    meetsVerificationLevel: () => true,
+  };
+  const app = express();
+  app.use(verification.createVerificationRoutes(override === undefined ? deps : { ...deps, originateForwardTimeoutMs: override }));
+  const gatewayPort = await listen(http.createServer(app));
+  const spy = vi.spyOn(http.ClientRequest.prototype, 'setTimeout');
+  restores.push(() => spy.mockRestore());
+  const started = Date.now();
+  const reply = fetch(`http://127.0.0.1:${gatewayPort}/api/workflow-instances/${WFI_ID}/approve`, { method: 'POST', signal: AbortSignal.timeout(3_000) })
+    .then((res) => res.status, () => 0);
+  // Wait until the route has armed the forward AND originate holds the request, then read the bound.
+  for (let waited = 0; (spy.mock.calls.length === 0 || hits === 0) && waited < 2_000; waited += 10) await sleep(10);
+  const bounds = spy.mock.calls.map((call) => call[0]);
+  const onTimeout = spy.mock.calls[0]?.[1];
+  if (fireTheBound && typeof onTimeout === 'function') onTimeout();
+  const status = await reply;
+  const errors = log.mock.calls.filter(([level]) => level === 'error').map(([, , meta]) => (meta as { error?: unknown } | undefined)?.error);
+  return { status, ms: Date.now() - started, bounds, errors, deletes, hits };
+}
+
+describe('KS-1185 F4 — workflow approve built without an override arms the production default bound', () => {
+  it('🔴 KS-1185 F4 — no override: the forward is armed with 15000 ms, and that bound answers 502 and keeps the document', async () => {
+    const out = await drive(undefined, true);
+    expect(out.bounds, 'the bound the forward request was armed with, override absent').toEqual([PRODUCTION_DEFAULT_MS]);
+    expect(out.bounds).toEqual([verification.ORIGINATE_FORWARD_TIMEOUT_MS]);
+    expect(out.status, `answered after ${out.ms} ms`).toBe(502);
+    expect(out.errors).toEqual(['originate did not answer within 15000 ms']);
+    expect(out.hits).toBe(1);
+    expect(out.deletes).toBe(0);
+  });
+
+  it('🟢 KS-1185 control — with a 300 ms override the real timer fires on its own, through the same setTimeout call', async () => {
+    const out = await drive(OVERRIDE_MS, false);
+    expect(out.bounds).toEqual([OVERRIDE_MS]);
+    expect(out.status, `answered after ${out.ms} ms`).toBe(502);
+    expect(out.ms).toBeGreaterThanOrEqual(OVERRIDE_MS - 50);
+    expect(out.ms).toBeLessThan(OVERRIDE_MS + 1_500);
+    expect(out.errors).toEqual(['originate did not answer within 300 ms']);
+    expect(out.hits).toBe(1);
+    expect(out.deletes).toBe(0);
+  });
+});
```
