```diff
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1130-tier2-e1-twin.test.ts
@@ -0,0 +1,200 @@
+// =============================================================================
+// KS-1130 — tier-2 twin cells for E1 (the placeholder-hash guard)
+// =============================================================================
+//
+// Tier 2 (`POST /api/documents/:id/verify`, anchoring's `/api/anchors/document/:id`)
+// synthesises its blockchain blob from the latest anchor row:
+//   `{ contentHash, txHash: latest.transactionHash, blockHeight: latest.blockNumber,
+//     simulated: latest.simulated, status: latest.status }`.
+// The verify handler then runs the same three shape guards as tier 1:
+//   * `persistedTxHashIsReal`        (:614–617) — string, non-empty, NOT prefixed
+//                                    by `tx_sim_`/`mock_tx_`/`tx_`;
+//   * `persistedBlockHeightIsHeight` (:622)       — positive integer;
+//   * `persistedDeclaredSimulated`   (:627)       — Boolean(persistedSimulated);
+// and only if all three hold does it consult `status === 'confirmed' || null`.
+//
+// This file pins that tier-2 path with a twin of the E1 cell in
+// ks1057-verify-confidence-is-status-aware.test.ts. It is TEST-ONLY MODE: no
+// product changes. The checker plants a tamper on line 617 below to prove the
+// 🔴 cell can go red at the untouched tip.
+//
+// Driven against the REAL router with stub originate over HTTP, because
+// `makeFetchDocument` uses node's `http.get` and not `globalThis.fetch`.
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
+/** Tier-2 rows served by the stub anchor store (tier 1 absent). */
+let anchorStoreRows: Array<Record<string, unknown>> | null = null;
+/** When true the stub originate 404s for /api/documents/:id. */
+let tier1Absent = false;
+
+beforeAll(async () => {
+  // Stub originate: covers BOTH tiers so one server stands in for both services.
+  originate = http.createServer((req, res) => {
+    const jsonHead = { 'Content-Type': 'application/json' };
+    // Tier 2 (KS-1130): anchoring's `/api/anchors/document/:id`, AUTHENTICATED
+    // BUT NOT OWNERSHIP-GATED — the third-party verifier path (BACKLOG #G6).
+    if (req.url === `/api/anchors/document/${DOC_ID}`) {
+      if (!anchorStoreRows) { res.writeHead(404, jsonHead); res.end('{}'); return; }
+      res.writeHead(200, jsonHead);
+      res.end(JSON.stringify({ data: { anchors: anchorStoreRows } }));
+      return;
+    }
+    // Tier 1: ownership-gated document record. Forced off by `tier1Absent`.
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
+  // No live chain evidence — every cell measures its persisted blob only.
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
+/** Drive the tier-2 path and return the parsed body. */
+async function verifyViaAnchorStore(row: Record<string, unknown>): Promise<any> {
+  anchorStoreRows = [{ contentHash: CONTENT_HASH, ...row }];
+  tier1Absent = true;                       // tier 1 misses -> fall through to tier 2
+  const r = await realFetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' },
+    body: JSON.stringify({ purpose: 'test' }),
+  });
+  expect(r.status).toBe(200);
+  const body = await r.json();
+  // Guard the whole family: if tier 2 were not the tier that answered, every
+  // assertion below would be about the wrong code path.
+  expect(body.blockchain.source).toBe('persisted');
+  return body;
+}
+
+describe('KS-1130 — tier-2 E1 twin cells for the placeholder-hash guard', () => {
+  it('🔴 KS-1130 E1 twin — a tier-2 row whose transactionHash is a tx_sim_ placeholder is off-chain-only', async () => {
+    const body = await verifyViaAnchorStore({ transactionHash: 'tx_sim_' + 'a'.repeat(57), blockNumber: 4242, status: 'confirmed' });
+    expect(body.verified).toBe(false);
+    expect(body.verificationConfidence).toBe('off-chain-only');
+  });
+
+  it('🔴 KS-1130 E1 twin — the same placeholder row reports blockchain.anchored false', async () => {
+    const body = await verifyViaAnchorStore({ transactionHash: 'tx_sim_' + 'a'.repeat(57), blockNumber: 4242, status: 'confirmed' });
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
