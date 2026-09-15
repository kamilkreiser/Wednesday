# READY — KS-1123 (the F2 pin only; F3 held separately; F1 = KS-1073's held cell) — Ornith ornith:35b-q8_0 PASS 7/7 FIRST RUN, TEST-ONLY mode, 2026-09-15 15:38 — tip develop M55 48e65c435. NO product change. Run `2026-09-15_ks1123-ornith35b-q8_0-night2` (55 s, 2,383 tokens). Tamper :709 (the `persistedStatus == null &&` guard dropped from the confidence chain): 2 🔴 red under it / control green / 3 green at the tip / suite Δ 0 / tsc 0. The tamper sits mid-statement; the brief carries `statement_ok:` (the new gate) with the arms of the :704–711 ternary read at M55.
# Source read by Wednesday: the three tier-1 cells are the brief's exactly (anchor_failed + stale confidence → off-chain-only; confirmed-status with no hash + stale confidence → off-chain-only; pending-status control → pending-onchain), driven through the ks1057 `verify(blob)` helper with all twelve file-scope declarations copied. KS-1123 is now fully pinned (F1 via KS-1073, F2, F3) — one PR for a Secuura seat can carry F2 + F3 (+ the P1–P3 comment items if the seat chooses).

```diff
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1123-api-gateway-verify-an-empty-string.test.ts
@@ -0,0 +1,215 @@
+// =============================================================================
+// KS-1123 F2 — TEST ONLY MODE (no product hunk)
+//
+// The guard at verification.ts:709 (`persistedStatus == null &&`) stops a
+// stale confidence field from upgrading any non-statusless blob to pending-onchain.
+// This file pins that behaviour with two tier-1 cells that only the guard keeps honest.
+//
+// The checker reddens these 🔴 cells by replacing line 709 with:
+//   : persistedConfidence === 'pending-onchain' // TAMPER: ...
+// and expects them GREEN at the untouched tip.
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
+const DOC_ID = 'doc-ks1123-f2';
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
+describe('KS-1123 F2 — stale confidence cannot upgrade a status', () => {
+  it('🔴 KS-1123 F2 — a failed anchor with a stale confidence field stays off-chain-only', async () => {
+    // Under the tamper :709 becomes `persistedConfidence === 'pending-onchain'`
+    // which is TRUE here → `'pending-onchain'`. At the tip line 709 requires
+    // `persistedStatus == null &&` so this cell measures OFF-CHAIN-ONLY.
+    const body = await verify({ txHash: null, blockHeight: 0, status: 'anchor_failed', confidence: 'pending-onchain' });
+    expect(body.verificationConfidence).toBe('off-chain-only');
+    expect(body.blockchain.confidence).toBe('off-chain-only');
+    expect(body.verified).toBe(false);
+  });
+
+  it('🔴 KS-1123 F2 — a confirmed-status blob with no hash and a stale confidence field stays off-chain-only', async () => {
+    // No hash → not anchored (line 705 false). `'confirmed'` maps to on-chain via
+    // confidenceForAnchorStatus (line 707 checks for pending-onchain only), so
+    // line 707 is false. Line 709 at the tip refuses because persistedStatus !== null.
+    // Under the tamper → `'pending-onchain'` — the red.
+    const body = await verify({ txHash: null, blockHeight: null, status: 'confirmed', confidence: 'pending-onchain' });
+    expect(body.verificationConfidence).toBe('off-chain-only');
+    expect(body.verified).toBe(false);
+  });
+
+  it('KS-1123 control — a pending-status blob is pending-onchain, before and after', async () => {
+    // Decided by line 707 (`confidenceForAnchorStatus('pending') === 'pending-onchain'`)
+    // and never reaches line 709. Green both sides of the change.
+    const body = await verify({ txHash: null, blockHeight: null, status: 'pending', confidence: 'pending-onchain' });
+    expect(body.verificationConfidence).toBe('pending-onchain');
+    expect(body.verified).toBe(false);
+  });
+});
```
