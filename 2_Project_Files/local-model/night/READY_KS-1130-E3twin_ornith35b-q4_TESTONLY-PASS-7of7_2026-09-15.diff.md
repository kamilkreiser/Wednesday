# READY — KS-1130 (the E3 tier-2 twin pin only; E1 and E7 held separately) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST RUN, TEST-ONLY mode, 2026-09-15 15:25 — tip develop M55 48e65c435. NO product change. Run `runs/2026-09-15_ks1130-ornith35b-night4` (47 s, 2,148 tokens, think=0). Tamper :627 `Boolean(persistedSimulated)` → `persistedSimulated === true` (the pre-KS-1069 strict form): 2 🔴 red under the tamper / control green / 3 green at the tip / suite Δ 0 / tsc 0. Applied with --recount only (one miscounted new-file header).
# Source read by Wednesday: the three cells are the brief's exactly (simulated 'true' → verified false + off-chain-only; simulated 1 → blockchain.anchored false; simulated false control → verified true + on-chain); the driver is the ks1057 shape with ALL twelve file-scope declarations copied (the brief listed them by name after the E7 prune — none needed splicing). With E1 + E7 + E3 held, KS-1130's three tier-2 twins are all pinned; the three files can go up as ONE PR.

```diff
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1130-tier2-e3-twin.test.ts
@@ -0,0 +1,175 @@
+// =============================================================================
+// KS-1130 — E3 tier-2 twin cells (test-only mode)
+// =============================================================================
+//
+// Proves that under the pre-KS-1069 strict form (`=== true`) the tier-2 read of
+// `simulated` rejects string `'true'` and number `1`, while boolean `false`
+// stays green at both tip and tamper.
+//
+// Driven against the real router with stub originate over HTTP, mirroring the
+// ks1057 harness shape for reachability.
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
+async function verifyViaAnchorStore(row: Record<string, unknown>): Promise<any> {
+  currentBlob = undefined;
+  liveAnchorReply = null;
+  tier1Absent = true;
+  anchorStoreRows = [{ contentHash: CONTENT_HASH, ...row }];
+  const r = await realFetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' },
+    body: JSON.stringify({ purpose: 'test' }),
+  });
+  expect(r.status).toBe(200);
+  const body = await r.json();
+  expect(body.blockchain.source).toBe('persisted');
+  return body;
+}
+
+describe('KS-1130 — E3 tier-2 twin cells for simulated shape guards', () => {
+  it('🔴 KS-1130 E3 twin — a tier-2 row whose simulated is the STRING "true" is off-chain-only', async () => {
+    const body = await verifyViaAnchorStore({ transactionHash: REAL_TX, blockNumber: 4242, status: 'confirmed', simulated: 'true' });
+    expect(body.verified).toBe(false);
+    expect(body.verificationConfidence).toBe('off-chain-only');
+  });
+
+  it('🔴 KS-1130 E3 twin — a tier-2 row whose simulated is the NUMBER 1 reports blockchain.anchored false', async () => {
+    const body = await verifyViaAnchorStore({ transactionHash: REAL_TX, blockNumber: 4242, status: 'confirmed', simulated: 1 });
+    expect(body.blockchain.anchored).toBe(false);
+  });
+
+  it('KS-1130 control — a confirmed tier-2 row with simulated false still reports on-chain', async () => {
+    const body = await verifyViaAnchorStore({ transactionHash: REAL_TX, blockNumber: 4242, status: 'confirmed', simulated: false });
+    expect(body.verified).toBe(true);
+    expect(body.verificationConfidence).toBe('on-chain');
+  });
+});
```
