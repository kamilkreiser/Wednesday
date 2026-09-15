```diff
--- a/services/api-gateway/src/routes/verification.ts
+++ b/services/api-gateway/src/routes/verification.ts
@@ -285,5 +285,9 @@
               const anchors = data?.data?.anchors;
               if (!Array.isArray(anchors) || anchors.length === 0) { resolve(null); return; }
               // Latest = highest blockNumber, fall back to most-recent confirmedAt.
-              const latest = anchors.slice().sort((a: any, b: any) =>
-                (b.blockNumber || 0) - (a.blockNumber || 0))[0];
+              const latest = anchors.slice().sort((a: any, b: any) => {
+                const byBlock = (b.blockNumber || 0) - (a.blockNumber || 0);
+                if (byBlock !== 0) return byBlock;
+                return (Date.parse(b.confirmedAt) || 0) - (Date.parse(a.confirmedAt) || 0);
+              })[0];
               resolve({
--- /dev/null
+++ b/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts
@@ -0,0 +1,181 @@
+// KS-1072 — latest-anchor selector confirmsAt tiebreak.
+
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+
+const DOC_ID = 'doc-ks1072';
+let gateway: Server | undefined;
+let stubServer: Server | undefined;
+let gatewayPort!: number;
+/** Tier-2 rows served by the stub anchor store endpoint. */
+let anchorStoreRows: Array<Record<string, unknown>> | null = null;
+const jsonHead = { 'Content-Type': 'application/json' };
+
+beforeAll(async () => {
+  stubServer = http.createServer((req, res) => {
+    if (req.url === `/api/anchors/document/${DOC_ID}`) {
+      if (!anchorStoreRows || anchorStoreRows.length === 0) {
+        res.writeHead(404, jsonHead);
+        res.end('{}');
+        return;
+      }
+      res.writeHead(200, jsonHead);
+      res.end(JSON.stringify({ data: { anchors: anchorStoreRows } }));
+      return;
+    }
+    // Disable live chain-scan verifier so response reflects selected tier-2 blob directly.
+    if (typeof req.url === 'string' && req.url.startsWith('/api/anchors/verify/')) {
+      res.writeHead(500, jsonHead);
+      res.end('{}');
+      return;
+    }
+    // Force tier 2: originate returns nothing useful for this docId.
+    if (typeof req.url === 'string' && req.url.startsWith(`/api/documents/${DOC_ID}`)) {
+      res.writeHead(404, jsonHead);
+      res.end('{}');
+      return;
+    }
+    res.writeHead(404, jsonHead);
+    res.end('{}');
+  });
+  stubServer.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => stubServer.once('listening', () => r()));
+  const stubPort = (stubServer.address() as AddressInfo).port;
+
+  const { createVerificationRoutes } = await import('../routes/verification');
+  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
+
+  const app = express();
+  app.use(
+    createVerificationRoutes({
+      authenticateToken: () => (_req, _res, next) => next(),
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
+      services: {
+        originate: { url: `http://127.0.0.1:${stubPort}` },
+        anchoring: { url: `http://127.0.0.1:${stubPort}` },
+      } as never,
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
+  if (gateway) await new Promise<void>((r) => gateway.close(() => r()));
+  if (stubServer) await new Promise<void>((r) => stubServer.close(() => r()));
+});
+
+async function postVerify(): Promise<any> {
+  const r = await fetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ purpose: 'test' }),
+  });
+  expect(r.status).toBe(200);
+  return r.json();
+}
+
+/** Force tier-2 by serving only anchor store rows; originate returns 404. */
+async function verifyTier2(rows: Array<Record<string, unknown>>): Promise<any> {
+  anchorStoreRows = rows;
+  return postVerify();
+}
+
+describe('KS-1072 — latest-anchor selector confirmedAt tiebreak', () => {
+  it('🔴 KS-1072 — equal blockNumber: the most recent confirmedAt wins', async () => {
+    // Two anchors with identical blockNumber=100 but different confirmedAt.
+    // Listed OLD FIRST in the array; stable sort would keep old first without
+    // the tiebreak fix → red at base. After fix, anchor_new should win.
+    const body = await verifyTier2([
+      {
+        id: 'anchor_old',
+        contentHash: 'a'.repeat(64),
+        transactionHash: '0'.repeat(63) + '1',
+        blockNumber: 100,
+        confirmedAt: '2026-01-01T00:00:00Z',
+      },
+      {
+        id: 'anchor_new',
+        contentHash: 'b'.repeat(64),
+        transactionHash: '0'.repeat(63) + '2',
+        blockNumber: 100,
+        confirmedAt: '2026-06-01T00:00:00Z',
+      },
+    ]);
+    expect(body.blockchain.txHash).toBe('0'.repeat(63) + '2');
+    expect(body.verified).toBe(true);
+  });
+
+  it('🔴 KS-1072 — a missing confirmedAt loses the tiebreak', async () => {
+    // One anchor without confirmedAt listed first; one dated second. The dated
+    // one must still win because Date.parse(undefined) is NaN and `|| 0` makes
+    // it the oldest possible value.
+    const body = await verifyTier2([
+      {
+        id: 'anchor_nodate',
+        contentHash: 'c'.repeat(64),
+        transactionHash: '0'.repeat(63) + '3',
+        blockNumber: 50,
+      },
+      {
+        id: 'anchor_dated',
+        contentHash: 'd'.repeat(64),
+        transactionHash: '0'.repeat(63) + '4',
+        blockNumber: 50,
+        confirmedAt: '2026-03-01T00:00:00Z',
+      },
+    ]);
+    expect(body.blockchain.txHash).toBe('0'.repeat(63) + '4');
+    expect(body.verified).toBe(true);
+  });
+
+  it('KS-1072 control — a higher blockNumber still wins regardless of confirmedAt', async () => {
+    // Green before AND after the fix. Higher blockNumber dominates the tiebreak.
+    const body = await verifyTier2([
+      {
+        id: 'anchor_higher_block',
+        contentHash: 'e'.repeat(64),
+        transactionHash: '0'.repeat(63) + '5',
+        blockNumber: 101,
+        confirmedAt: '2020-01-01T00:00:00Z',
+      },
+      {
+        id: 'anchor_lower_block_newer_date',
+        contentHash: 'f'.repeat(64),
+        transactionHash: '0'.repeat(63) + '6',
+        blockNumber: 100,
+        confirmedAt: '2099-12-31T00:00:00Z',
+      },
+    ]);
+    expect(body.blockchain.txHash).toBe('0'.repeat(63) + '5');
+    expect(body.verified).toBe(true);
+  });
+});
```
