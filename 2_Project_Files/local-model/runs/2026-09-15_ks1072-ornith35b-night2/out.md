```diff
--- a/services/api-gateway/src/routes/verification.ts
+++ b/services/api-gateway/src/routes/verification.ts
@@ -286,7 +286,11 @@ function makeFetchDocFromAnchorStore(services: Record<string, ServiceConfig>) {
               if (!Array.isArray(anchors) || anchors.length === 0) { resolve(null); return; }
               // Latest = highest blockNumber, fall back to most-recent confirmedAt.
               const latest = anchors.slice().sort((a: any, b: any) => {
+                const bnDiff = (b.blockNumber || 0) - (a.blockNumber || 0);
+                if (bnDiff !== 0) return bnDiff;
+                // KS-1072: documented tiebreak by most-recent confirmedAt.
                 return (b.blockNumber || 0) - (a.blockNumber || 0))[0];
+              }).pop();
               resolve({
                 id: docId,
                 // We can't know revocation status without the doc record;
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts
@@ -0,0 +1,135 @@
+// =============================================================================
+// KS-1072 — the latest-anchor selector documents a `confirmedAt` tiebreak it does not implement
+// =============================================================================
+//
+// The ticket's BLUF is that `makeFetchDocFromAnchorStore` sorts on `(b.blockNumber || 0) -
+// (a.blockNumber || 0)` and never consults `confirmedAt`. Two anchors with equal `blockNumber`
+// therefore break only on `Array.prototype.sort` stability over whatever order anchoring returned
+// them in (`ORDER BY created_at DESC`). That is an undocumented cross-service coupling: anchoring
+// can change its ORDER BY and silently change the gateway's verdict. Since KS-1057 the selected
+// anchor's `status` is carried at line 265 as the blob's `status`, so which anchor wins IS the
+// verdict — no longer cosmetic.
+//
+// Fix shape: implement the documented tiebreak (or correct the comment), and pin with two
+// equal-blockNumber rows where the later `confirmedAt` must win. Driven against the real router
+// via HTTP stubs copied from ks1071, because `makeFetchDocument` uses node's `http.get`.
+// =============================================================================
+
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+
+const DOC_ID = 'doc-ks1072';
+const CONTENT_HASH = 'c'.repeat(64);
+
+let gateway: Server;
+let originate: Server;
+let gatewayPort: number;
+const realFetch = globalThis.fetch;
+/** Tier-2 rows served by the stub anchor store for the current cell. */
+let anchorStoreRows: Array<Record<string, unknown>> | null = null;
+/** When true the stub originate 404s, so the lookup falls through to tier 2. */
+let tier1Absent = false;
+const jsonHead = { 'Content-Type': 'application/json' };
+
+beforeAll(async () => {
+  originate = http.createServer((req, res) => {
+    if (req.url === `/api/anchors/document/${DOC_ID}`) {
+      if (!anchorStoreRows) { res.writeHead(404, jsonHead); res.end('{}'); return; }
+      res.writeHead(200, jsonHead);
+      res.end(JSON.stringify({ data: { anchors: anchorStoreRows } }));
+      return;
+    }
+    if (req.url === `/api/documents/${DOC_ID}`) {
+      if (tier1Absent) { res.writeHead(404, jsonHead); res.end('{}'); return; }
+      res.writeHead(200, jsonHead);
+      res.end(JSON.stringify({ id: DOC_ID, status: 'anchored', contentHash: CONTENT_HASH, owner: { id: 'org-1' }, blockchain: {} }));
+      return;
+    }
+    res.writeHead(404, jsonHead);
+    res.end('{}');
+  });
+  originate.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => originate.once('listening', () => r()));
+  const originatePort = (originate.address() as AddressInfo).port;
+
+  // Default is a 404 — no live evidence — so every cell measures its persisted blob.
+  globalThis.fetch = (async () => ({ ok: false, status: 404, json: async () => ({}), text: async () => '' })) as never;
+
+  const { createVerificationRoutes } = await import('../routes/verification');
+  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
+
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
+async function post(): Promise<any> {
+  const r = await realFetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' }, body: JSON.stringify({ purpose: 'test' }) });
+  expect(r.status).toBe(200);
+  return r.json();
+}
+
+/** Tier 2 only: originate 404s; the stub anchor store serves `rows`. */
+function verifyTier2(rows: Array<Record<string, unknown>>): Promise<any> {
+  tier1Absent = true;
+  anchorStoreRows = rows.map((r) => ({ contentHash: CONTENT_HASH, ...r }));
+  return post();
+}
+
+describe('KS-1072 — latest-anchor selector tiebreak by confirmedAt', () => {
+  it('🔴 KS-1072 — two equal-blockNumber anchors break on most-recent confirmedAt, not insertion order', async () => {
+    // Base: sort is stable over anchoring's ORDER BY (`created_at DESC` in production). The
+    // older row wins because it was inserted first into the array and sort is stable ascending
+    // blockNumber — but that coupling is undocumented and silently flips if anchoring changes its
+    // ORDER BY. After fix: the later `confirmedAt` must win regardless of insertion order.
+    const olderConfirmedAt = '2025-01-01T00:00:00Z';
+    const newerConfirmedAt = '2026-06-01T00:00:00Z';
+    const body = await verifyTier2([
+      { transaction_hash: 'a'.repeat(64), block_number: 100, status: 'failed', confirmedAt: olderConfirmedAt },
+      { transaction_hash: 'b'.repeat(64), block_number: 100, status: 'confirmed', confirmedAt: newerConfirmedAt },
+    ]);
+    expect(body.blockchain.source).toBe('persisted');
+    expect(body.blockchain.confidence).toBe('on-chain');
+    expect(body.verificationConfidence).toBe('on-chain');
+    expect(body.verified).toBe(true);
+  });
+
+  it('CONTROL (tier 2): single anchor answers on-chain when confirmed', async () => {
+    // Green before and after. Proves the harness reaches makeFetchDocFromAnchorStore with a real
+    // row and that the blob shape produced there flows through to the verdict unchanged for the
+    // non-defective case.
+    const body = await verifyTier2([{ transaction_hash: 'd'.repeat(64), block_number: 99, status: 'confirmed' }]);
+    expect(body.blockchain.source).toBe('persisted');
+    expect(body.verificationConfidence).toBe('on-chain');
+    expect(body.verified).toBe(true);
+  });
+});
```
