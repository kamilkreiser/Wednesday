```diff
--- a/services/api-gateway/src/routes/verification.ts
+++ b/services/api-gateway/src/routes/verification.ts
@@ -682,7 +682,7 @@ export function createVerificationRoutes(deps: VerificationRouteDeps): Router {
       persistedTxHashIsReal &&           // KS-1069: was `persistedTxHash &&`
       persistedBlockHeightIsHeight &&    // KS-1069: was `persistedBlockHeight &&`
       !persistedDeclaredSimulated &&     // KS-1069: was `persistedSimulated !== true`
-      (persistedStatus === 'confirmed' || persistedStatus == null),
+      (persistedStatus === 'confirmed' || (persistedStatus == null && (doc as any)._source !== 'anchor_store')),
     );
 
     // KS-1071: the in-flight decision is made HERE, once, for BOTH tiers —
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts
@@ -0,0 +1,175 @@
+// =============================================================================
+// KS-1073 — tier-2 verify has no statusless-blob cell; the carve-out must not apply to tier 2
+// =============================================================================
+//
+// The gateway's verify handler treats ANY blob with NO `status` (`persistedStatus == null`)
+// like `'confirmed'`. That carve-out exists only for TIER-1 legacy documents (originate's seeded
+// demo docs, KS-1057). Tier-2 blobs synthesised from the anchor store carry `_source: 'anchor_store'`
+// at doc-level and copy `status: latest.status`; they should NOT take the legacy carve-out.
+//
+// This file drives against the REAL router with stub originate + stub anchor store over HTTP,
+// mirroring the shape of ks1057-verify-confidence-is-status-aware.test.ts but dropping every
+// original `it(...)` and writing only the three cells named by the ticket.
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
+const DOC_ID = 'doc-ks1073';
+const CONTENT_HASH = 'b'.repeat(64);
+
+let gateway: Server;
+let originate: Server;
+let gatewayPort: number;
+const realFetch = globalThis.fetch;
+
+/** The blockchain blob the stub originate serves for the current cell. */
+let currentBlob: Record<string, unknown> | undefined;
+/** The anchoring chain-scan reply for the current cell. `null` = no live hit. */
+let liveAnchorReply: Record<string, unknown> | null = null;
+/** Tier-2 rows served by the stub anchor store. `null` = tier 2 has nothing. */
+let anchorStoreRows: Array<Record<string, unknown>> | null = null;
+/** When true the stub originate 404s, so the lookup falls through to tier 2. */
+let tier1Absent = false;
+const jsonHead = { 'Content-Type': 'application/json' };
+
+beforeAll(async () => {
+  // Stub originate: the first lookup tier. Serves the document whose blockchain
+  // blob each cell sets.
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
+      res.end(JSON.stringify({
+        id: DOC_ID,
+        status: 'anchored',
+        contentHash: CONTENT_HASH,
+        owner: { id: 'org-1' },
+        ...(currentBlob ? { blockchain: currentBlob } : {}),
+      }));
+      return;
+    }
+    res.writeHead(404, { 'Content-Type': 'application/json' });
+    res.end('{}');
+  });
+  originate.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => originate.once('listening', () => r()));
+  const originatePort = (originate.address() as AddressInfo).port;
+
+  globalThis.fetch = (async () => (
+    liveAnchorReply
+      ? { ok: true, status: 200, json: async () => liveAnchorReply, text: async () => '' }
+      : { ok: false, status: 404, json: async () => ({}), text: async () => '' }
+  )) as never;
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
+/** Drive the real route and return the parsed body. */
+async function verify(
+  blob: Record<string, unknown> | undefined,
+  live: Record<string, unknown> | null = null,
+): Promise<any> {
+  currentBlob = blob;
+  liveAnchorReply = live;
+  anchorStoreRows = null;
+  tier1Absent = false;
+  const r = await realFetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' },
+    body: JSON.stringify({ purpose: 'test' }),
+  });
+  expect(r.status).toBe(200);
+  return r.json();
+}
+
+describe('KS-1073 — statusless tier-2 blobs must not take the legacy carve-out', () => {
+  it('🔴 KS-1073 — a tier-2 anchor-store row with NO status is not anchored', async () => {
+    const body = await verifyViaAnchorStore({ transactionHash: REAL_TX, blockNumber: 4242 });
+    expect(body.verified).toBe(false);
+    expect(body.verificationConfidence).toBe('off-chain-only');
+  });
+
+  it('🔴 KS-1073 — the same statusless tier-2 row reports blockchain.anchored false', async () => {
+    const body = await verifyViaAnchorStore({ transactionHash: REAL_TX, blockNumber: 4242 });
+    expect(body.blockchain.anchored).toBe(false);
+  });
+
+  it('KS-1073 control — a tier-1 legacy statusless blob still reports on-chain, and a CONFIRMED tier-2 row still does', async () => {
+    // Tier-1 legacy (seeded demo documents): `{txHash, blockHeight}` with no `status` key.
+    const legacyBody = await verify({
+      txHash: REAL_TX,
+      blockHeight: 1024576,
+      anchoredAt: new Date().toISOString(),
+    });
+    expect(legacyBody.verified).toBe(true);
+    expect(legacyBody.verificationConfidence).toBe('on-chain');
+
+    // Tier-2 confirmed: should report on-chain via the `=== 'confirmed'` arm, NOT the carve-out.
+    const confirmedBody = await verifyViaAnchorStore({ transactionHash: REAL_TX, blockNumber: 4242, status: 'confirmed' });
+    expect(confirmedBody.verified).toBe(true);
+    expect(confirmedBody.verificationConfidence).toBe('on-chain');
+  });
+});
```
