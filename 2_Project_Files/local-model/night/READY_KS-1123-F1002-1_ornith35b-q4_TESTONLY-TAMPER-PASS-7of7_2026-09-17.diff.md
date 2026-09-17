# READY — KS-1123 F-1002-1 (NEW api-gateway test pinning a 0 and a false anchor status as off-chain-only on the tier-1 verify route; tamper verification.ts:624; 2 red cells + 1 control + completeness) — Ornith ornith:35b q4, first sample, PASS 7/7 at 16:50 2026-09-17 on tip f8c7aaa39
# Source read by Wednesday: the model's 113 `+` lines IDENTICAL to the brief's test fence (python compare; a mutated copy unequal); one new file, no product change; apply STRICT; A4 tamper reds BOTH declared cells (failed=2/4: R1 and R2 by name — checked because A4 has a known any-one-red gap); A6 api-gateway 454 → 458, 0 new reds; A7 tsc rc 0.
# PR NOTES: `Refs KS-1123 (F-1002-1)`, NEVER Closes. TIER 2. RENAME the test file at raise (ks1123-api-gateway-verify-an-empty-string.test.ts reused a 09-15 READY name; those merged as #1002 under other names, so no collision at the tip). Search 17l report: night/briefs/NEXT_SEARCH_2026-09-17l.REPORT.md; brief night/briefs/split_1123F1002/KS-1123.md; run local-model/runs/2026-09-17_ks1123-ornith35b-night.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1123-api-gateway-verify-an-empty-string.test.ts
@@ -0,0 +1,113 @@
+/**
+ * KS-1123 F-1002-1: the verify route reads the persisted anchor status with a
+ * nullish default, so an empty-string, 0 or false status stays a status and a
+ * blob carrying one answers off-chain-only. Only the empty-string case was
+ * pinned. A read that keeps strings but turns 0 or false into null fires the
+ * statusless carve-out, and those blobs answer on-chain with verified true.
+ * These cells pin the 0 and false statuses on tier 1.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+
+const EXPECTED_CELLS = 3;
+let CELLS_RUN = 0;
+const REAL_TX = 'a'.repeat(64);
+const DOC_ID = 'doc-ks1123-falsy';
+const CONTENT_HASH = 'b'.repeat(64);
+const realFetch = globalThis.fetch;
+
+let gateway: Server;
+let originate: Server;
+let gatewayPort = 0;
+let currentBlob: Record<string, unknown> = {};
+
+beforeAll(async () => {
+  originate = http.createServer((req, res) => {
+    res.setHeader('Content-Type', 'application/json');
+    if (req.url !== '/api/documents/' + DOC_ID) {
+      res.writeHead(404);
+      res.end('{}');
+      return;
+    }
+    res.writeHead(200);
+    res.end(JSON.stringify({ id: DOC_ID, status: 'anchored', contentHash: CONTENT_HASH, owner: { id: 'org-1' }, blockchain: currentBlob }));
+  });
+  originate.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => originate.once('listening', () => r()));
+  const originateUrl = 'http://127.0.0.1:' + (originate.address() as AddressInfo).port;
+  globalThis.fetch = (() => ({ ok: false, status: 404, json: async () => ({}), text: async () => '' })) as never;
+  const { createVerificationRoutes } = await import('../routes/verification');
+  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
+  const app = express();
+  app.use(
+    createVerificationRoutes({
+      authenticateToken: () => (req, _res, next) => {
+        (req as { user?: unknown }).user = { userId: 'u1', email: 'u@secuura.local', role: 'ADMIN', organizationId: 'org-1', tenantId: 't1', verificationLevel: 'FULL' };
+        next();
+      },
+      mockBodyParser,
+      query: vi.fn(async () => ({ rows: [] })) as never,
+      isDbAvailable: () => false,
+      redisService: {
+        getPendingDocument: vi.fn(async () => null),
+        getAllDocumentTypes: vi.fn(async () => []),
+        getAllWorkflowInstances: vi.fn(async () => []),
+        getNotificationSettings: vi.fn(async () => ({})),
+        getRejectedDocument: vi.fn(async () => null),
+        getWorkflowDocumentMapping: vi.fn(async () => null),
+        getWorkflowInstance: vi.fn(async () => null),
+      } as never,
+      services: { originate: { url: originateUrl }, anchoring: { url: originateUrl } } as never,
+      log: () => undefined,
+      memWorkflowToDocumentMap: new Map(),
+      memRejectedDocuments: new Map(),
+      dbSaveRejection: vi.fn(async () => undefined),
+      ADMIN_ROLES: ['ADMIN', 'admin'],
+      enforceDocumentTypeRules: vi.fn(async () => ({ ok: true, docType: {} })) as never,
+      createWorkflowInstanceIfRequired: vi.fn(async () => ({ gated: false })) as never,
+      meetsVerificationLevel: () => true,
+    }),
+  );
+  gateway = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => gateway.once('listening', () => r()));
+  gatewayPort = (gateway.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  globalThis.fetch = realFetch;
+  await new Promise<void>((r) => gateway.close(() => r()));
+  await new Promise<void>((r) => originate.close(() => r()));
+});
+
+// drive the tier-1 verify route for one blob and answer verified and confidence
+async function verify(blob: Record<string, unknown>): Promise<unknown[]> {
+  currentBlob = blob;
+  const url = 'http://127.0.0.1:' + gatewayPort + '/api/documents/' + DOC_ID + '/verify';
+  const r = await realFetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' }, body: JSON.stringify({ purpose: 'test' }) });
+  const body: any = await r.json();
+  return [r.status, body.verified, body.verificationConfidence];
+}
+
+describe('KS-1123 F-1002-1 - a 0 or false anchor status stays off-chain-only on tier 1', () => {
+  it('KS-1123 R1 - a status of 0 with a real hash and height is off-chain-only', async () => {
+    CELLS_RUN += 1;
+    expect(await verify({ txHash: REAL_TX, blockHeight: 4242, status: 0 })).toEqual([200, false, 'off-chain-only']);
+  });
+  it('KS-1123 R2 - a status of false with a real hash and height is off-chain-only', async () => {
+    CELLS_RUN += 1;
+    expect(await verify({ txHash: REAL_TX, blockHeight: 4242, status: false })).toEqual([200, false, 'off-chain-only']);
+  });
+  it('KS-1123 CONTROL - confirmed is on-chain and an empty-string status is off-chain-only', async () => {
+    CELLS_RUN += 1;
+    const confirmed = await verify({ txHash: REAL_TX, blockHeight: 4242, status: 'confirmed' });
+    const empty = await verify({ txHash: REAL_TX, blockHeight: 4242, status: '' });
+    expect([confirmed, empty]).toEqual([[200, true, 'on-chain'], [200, false, 'off-chain-only']]);
+  });
+  it('KS-1123 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});```
