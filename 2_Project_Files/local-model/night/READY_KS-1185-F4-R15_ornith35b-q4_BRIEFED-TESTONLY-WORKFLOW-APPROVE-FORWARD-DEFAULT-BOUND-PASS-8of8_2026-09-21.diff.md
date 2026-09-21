# READY — KS-1185-F4-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1185-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 21:43 2026-09-21). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip — with an accommodation: --recount (miscounted header: hunk @@ -0,0 +1,97 @@ declared old=0 new=97 actual old=0 new=108 ); every line byte-exact`; golden not located — no byte-identity claim is made.

**Held 21:43 2026-09-21 by Wednesday (the 20:1x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1185-ornith35b-night/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-workflow-approve-forward-default-bound.test.ts` (new). `+` lines 108 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 2/2 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `F4` → red exactly ['RED KS-1185 F4 - no override: the forward is armed with 1500']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1185-ornith35b-night/input.json`. Brief: `night/briefs/KS-1185-F4-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1185-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-workflow-approve-forward-default-bound.test.ts
@@ -0,0 +1,97 @@
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
+describe('KS-1185 F4 - workflow approve built without an override arms the production default bound', () => {
+  it('RED KS-1185 F4 - no override: the forward is armed with 15000 ms, and that bound answers 502 and keeps the document', async () => {
+    const out = await drive(undefined, true);
+    expect(out.bounds, 'the bound the forward request was armed with, override absent').toEqual([PRODUCTION_DEFAULT_MS]);
+    expect(out.bounds).toEqual([verification.ORIGINATE_FORWARD_TIMEOUT_MS]);
+    expect(out.status, `answered after ${out.ms} ms`).toBe(502);
+    expect(out.errors).toEqual(['originate did not answer within 15000 ms']);
+    expect(out.hits).toBe(1);
+    expect(out.deletes).toBe(0);
+  });
+
+  it('GREEN KS-1185 control - with a 300 ms override the real timer fires on its own, through the same setTimeout call', async () => {
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
