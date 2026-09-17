# READY — KS-1185 F1 (api-gateway routes/verification.ts:431: the approve forward-timeout override is only defaulted when absent — 0 waits forever, -1/NaN/null/'800' reach setTimeout — default FB: fall back to 15000 unless a finite positive integer; + a new vitest file) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, strict, 2026-09-17 16:01
# Source read by Wednesday (scratchpad cmp_brief.py): product `-` 1/1 and `+` 3/3 IDENTICAL incl. indent (A3i byte-exact); test 109/109 IDENTICAL (a mutated copy unequal); A6 no new red; A7 tsc rc 0.
# PR NOTES: `Refs KS-1185 (F1)` (F2, F3, the F1 listener-order half and F4 are separate; F4 is held as its own READY, different test file). TIER 2. No shipped caller passes the override today. Report local-model/night/briefs/DEFAULTS2_2026-09-17.REPORT.md; brief night/briefs/split_1185F1/KS-1185.md.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
@@ -429,6 +429,8 @@ export function createVerificationRoutes(deps: VerificationRouteDeps): Router {
     createWorkflowInstanceIfRequired,
     meetsVerificationLevel,
-    originateForwardTimeoutMs = ORIGINATE_FORWARD_TIMEOUT_MS,
+    originateForwardTimeoutMs: requestedForwardTimeoutMs = ORIGINATE_FORWARD_TIMEOUT_MS,
   } = deps;
+  // KS-1185 F1: an override that is not a whole number of ms above 0 falls back to the default bound.
+  const originateForwardTimeoutMs = Number.isInteger(requestedForwardTimeoutMs) && requestedForwardTimeoutMs > 0 ? requestedForwardTimeoutMs : ORIGINATE_FORWARD_TIMEOUT_MS;
 
   // ==========================================================================
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-ks-1183-gate-follow-ups-validate.test.ts
@@ -0,0 +1,109 @@
+/**
+ * KS-1185 F1: createVerificationRoutes took originateForwardTimeoutMs unvalidated.
+ * A destructure default covers only an absent value, so 0 meant never, and a
+ * negative, NaN, null or string override threw inside the forward promise.
+ *
+ * The fix: an override that is not a whole number of ms above 0 falls back to
+ * ORIGINATE_FORWARD_TIMEOUT_MS. These cells build the REAL approve route, stub
+ * the request setTimeout to record the bound it is armed with, and fire that
+ * bound by hand, so no cell waits for a real timer.
+ */
+import { describe, it, expect, afterEach, vi } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+import * as verification from '../routes/verification';
+
+const EXPECTED_CELLS = 3;
+let CELLS_RUN = 0;
+const DOC_ID = 'doc-ks1185-f1';
+const WFI_ID = 'wfi-ks1185-f1';
+const DEFAULT_ROW = [[15000], 502, ['originate did not answer within 15000 ms']];
+
+type Log = (level: 'info' | 'warn' | 'error', message: string, meta?: object) => void;
+
+const servers: http.Server[] = [];
+
+afterEach(async () => {
+  vi.restoreAllMocks();
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
+async function drive(override: unknown): Promise<unknown[]> {
+  const pendingDocs = new Map([[DOC_ID, { title: 't', contentHash: 'h', createdBy: 'u' }]]);
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
+      deletePendingDocument: vi.fn(async (id: string) => { pendingDocs.delete(id); }),
+    } as never,
+    services: { originate: { url: 'http://127.0.0.1:' + originatePort }, anchoring: { url: '' } } as never,
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
+  app.use(verification.createVerificationRoutes({ ...deps, originateForwardTimeoutMs: override as never }));
+  const gatewayPort = await listen(http.createServer(app));
+  const spy = vi.spyOn(http.ClientRequest.prototype, 'setTimeout').mockImplementation(function (this: http.ClientRequest) {
+    return this;
+  });
+  const url = 'http://127.0.0.1:' + gatewayPort + '/api/workflow-instances/' + WFI_ID + '/approve';
+  const reply = fetch(url, { method: 'POST', signal: AbortSignal.timeout(3000) }).then((res) => res.status, () => 0);
+  for (let waited = 0; (spy.mock.calls.length === 0 || hits === 0) && waited < 2000; waited += 10) await sleep(10);
+  const bounds = spy.mock.calls.map((call) => call[0]);
+  const onTimeout = spy.mock.calls[0]?.[1];
+  if (typeof onTimeout === 'function') onTimeout();
+  const status = await reply;
+  spy.mockRestore();
+  const errors = log.mock.calls.filter(([level]) => level === 'error').map(([, , meta]) => (meta as { error?: unknown } | undefined)?.error);
+  return [bounds, status, errors];
+}
+
+describe('KS-1185 F1 - an invalid forward timeout override falls back to the default bound', () => {
+  it('KS-1185 F1 R1 - an override of 0, -1 or NaN arms the forward with the 15000 ms default', async () => {
+    CELLS_RUN += 1;
+    const rows = [await drive(0), await drive(-1), await drive(Number.NaN)];
+    expect(rows).toEqual([DEFAULT_ROW, DEFAULT_ROW, DEFAULT_ROW]);
+  });
+  it('KS-1185 F1 R2 - an override of null or the string 800 arms the forward with the 15000 ms default', async () => {
+    CELLS_RUN += 1;
+    const rows = [await drive(null), await drive('800')];
+    expect(rows).toEqual([DEFAULT_ROW, DEFAULT_ROW]);
+  });
+  it('KS-1185 F1 CONTROL - a valid override of 300 ms is kept, and firing it answers 502', async () => {
+    CELLS_RUN += 1;
+    expect(await drive(300)).toEqual([[300], 502, ['originate did not answer within 300 ms']]);
+    expect(verification.ORIGINATE_FORWARD_TIMEOUT_MS).toBe(15000);
+  });
+  it('KS-1185 F1 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
