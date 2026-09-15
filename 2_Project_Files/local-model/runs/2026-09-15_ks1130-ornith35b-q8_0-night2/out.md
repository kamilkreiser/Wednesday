```diff
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1130-tier2-e7-twin.test.ts
@@ -0,0 +1,200 @@
+// =============================================================================
+// KS-1130 — E7 twin for tier-2 (blockNumber as string)
+// =============================================================================
+//
+// Tier-2 rows come from anchoring's `/api/anchors/document/:id`. The synthesised
+// blob reads `latest.transactionHash`, `latest.blockNumber`, `latest.simulated`
+// at lines 301–302 of verification.ts. Under PR #969 (KS-1069), line 623 guards
+// with `typeof persistedBlockHeight === 'number' && Number.isInteger(...) && ... > 0`.
+// If a row arrives whose `blockNumber` is the STRING `'4242'`, the guard rejects it
+// → off-chain-only. A tamper that widens to accept strings would flip this cell red.
+//
+// This file is TEST-ONLY. No product changes. The checker plants the tamper in a
+// clone and expects these cells RED; on the untouched tip they are GREEN.
+//
+// Driven against the real router with stub originate + anchor store over HTTP,
+// following ks1057's shape verbatim.
+// =============================================================================
+
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+
+const REAL_TX = 'a'.repeat(64);
+const DOC_ID = 'doc-ks1130';
+const CONTENT_HASH = 'b'.repeat(64);
+
+let gateway: Server;
+let originate: Server;
+let gatewayPort: number;
+const realFetch = globalThis.fetch;
+
+/** When true the stub originate 404s, so the lookup falls through to tier 2. */
+let tier1Absent = false;
+/** Tier-2 rows served by the stub anchor store. `null` = tier 2 has nothing. */
+let anchorStoreRows: Array<Record<string, unknown>> | null = null;
+const jsonHead = { 'Content-Type': 'application/json' };
+
+beforeAll(async () => {
+  // Stub originate: serves both tiers for this test.
+  originate = http.createServer((req, res) => {
+    if (req.url === `/api/anchors/document/${DOC_ID}`) {
+      if (!anchorStoreRows) { res.writeHead(404, jsonHead); res.end('{}'); return; }
+      res.writeHead(200, jsonHead);
+      res.end(JSON.stringify({ data: { anchors: anchorStoreRows } }));
+      return;
+    }
+    if (req.url === `/api/documents/${DOC_ID}`) {
+      if (tier1Absent) { res.writeHead(404, jsonHead); res.end('{}'); return; }
+      res.writeHead(200, { 'Content-Type': 'application/json' });
+      res.end(JSON.stringify({ id: DOC_ID, status: 'anchored', contentHash: CONTENT_HASH, owner: { id: 'org-1' }, blockchain: {} }));
+      return;
+    }
+    res.writeHead(404, { 'Content-Type': 'application/json' });
+    res.end('{}');
+  });
+  originate.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => originate.once('listening', () => r()));
+  const originatePort = (originate.address() as AddressInfo).port;
+
+  // No live chain evidence — cells measure persisted blob only.
+  globalThis.fetch = (async () => ({ ok: false, status: 404, json: async () => ({}), text: async () => '' })) as never;
+
+  const { createVerificationRoutes } = await import('../routes/verification');
+  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
+
+  const app = express();
+  app.use(
+    createVerificationRoutes({
+      authenticateToken: () => (req, _res, next) => {
+        (req as { user?: unknown }).user = {
+          userId: 'u1', email: 'u@secuura.local', role: 'ADMIN',
+          organizationId: 'org-1', tenantId: 't1', verificationLevel: 'FULL',
+        };
+        next();
+      },
+      mockBodyParser,
+      query: vi.fn(async () => ({ rows: [] })) as never,
+      isDbAvailable: () => false,
+      redisService: {
+        getPendingDocument: vi.fn(async () => null),
+        deletePendingDocument: vi.fn(async () => undefined),
+        getAllDocumentTypes: vi.fn(async () => []),
+        getAllWorkflowInstances: vi.fn(async () => []),
+        getNotificationSettings: vi.fn(async () => ({})),
+        getRejectedDocument: vi.fn(async () => null),
+        setRejectedDocument: vi.fn(async () => undefined),
+        getWorkflowDocumentMapping: vi.fn(async () => null),
+        getWorkflowInstance: vi.fn(async () => null),
+        setWorkflowInstance: vi.fn(async () => undefined),
+      } as never,
+      services: { originate: { url: `http://127.0.0.1:${originatePort}` }, anchoring: { url: `http://127.0.0.1:${originatePort}` } } as never,
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
+
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
+/** Drive the tier-2 path and return parsed body. */
+async function verifyViaAnchorStore(row: Record<string, unknown>): Promise<any> {
+  currentBlob = undefined;
+  liveAnchorReply = null;
+  tier1Absent = true;                       // tier 1 misses -> fall through to tier 2
+  anchorStoreRows = [{ contentHash: CONTENT_HASH, ...row }];
+  const r = await realFetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' },
+    body: JSON.stringify({ purpose: 'test' }),
+  });
+  expect(r.status).toBe(200);
+  const body = await r.json();
+  // Guard: if tier 2 were not the tier that answered, every assertion is wrong.
+  expect(body.blockchain.source).toBe('persisted');
+  return body;
+}
+
+describe('KS-1130 — E7 twin for tier-2 blockNumber-as-string guard', () => {
+  it('🔴 KS-1130 E7 twin — a tier-2 row whose blockNumber is the STRING "4242" is off-chain-only', async () => {
+    const body = await verifyViaAnchorStore({ transactionHash: REAL_TX, blockNumber: '4242', status: 'confirmed' });
+    expect(body.verified).toBe(false);
+    expect(body.verificationConfidence).toBe('off-chain-only');
+  });
+
+  it('🔴 KS-1130 E7 twin — the same string-height row reports blockchain.anchored false', async () => {
+    const body = await verifyViaAnchorStore({ transactionHash: REAL_TX, blockNumber: '4242', status: 'confirmed' });
+    expect(body.blockchain.anchored).toBe(false);
+  });
+
+  it('KS-1130 control — a well-shaped confirmed tier-2 row still reports on-chain', async () => {
+    const body = await verifyViaAnchorStore({ transactionHash: REAL_TX, blockNumber: 4242, status: 'confirmed' });
+    expect(body.verified).toBe(true);
+    expect(body.verificationConfidence).toBe('on-chain');
+  });
+});
```
