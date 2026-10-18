# READY — KS-1626-MOCKBATCH-APIGW-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_apigw/out.md.checker/patch.diff`** (from `ls` at 04:26 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_apigw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_apigw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_apigw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_apigw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 04:26 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_apigw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `5d1be7b06279950e3bfe176c237e5d640eb04581`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/verification.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/api-gateway/src/routes/verification.ts
189	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/routes/verification.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1626 - the batch mock placeholder is not an on-chain claim, live or persisted RED KS-1626 G1 a mock_batch_tx_ hash from the live chain-scan reply is not a hash', 'KS-1626 - the batch mock placeholder is not an on-chain claim, live or persisted RED KS-1626 G2 a mock_batch_tx_ persisted hash with a height and confirmed must not report on-chain']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1186 failed=0 | after: total=1191 failed=0` · `NEW reds: []` [baseline_suite.json total=1186 failed=0; after_suite.json total=1191 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +191/-2 test=src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts` (+189/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `5d1be7b06279950e3bfe176c237e5d640eb04581` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_apigw/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_apigw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
index 5a0531714..e55505041 100644
--- a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
@@ -652,7 +652,7 @@
           // KS-1129 O1: the live reply gets the three shape guards the persisted read got in KS-1069.
           if (j.verified === true && !j.simulated) {
             const liveHash = j.txHash || j.transactionHash || (j.anchor && j.anchor.txHash) || null;
-            liveTxHash = typeof liveHash === 'string' && !/^(tx_sim_|mock_tx_|tx_)/.test(liveHash) ? liveHash : null;
+            liveTxHash = typeof liveHash === 'string' && !/^(tx_sim_|mock_tx_|mock_batch_tx_|tx_)/.test(liveHash) ? liveHash : null;
             const blockNum = j.blockNumber ?? j.blockHeight ?? (j.anchor && j.anchor.blockHeight);
             liveBlockHeight = typeof blockNum === 'number' && Number.isInteger(blockNum) && blockNum > 0 ? blockNum : null;
             liveConfirmedAt = j.confirmedAt || j.anchoredAt || (j.anchor && j.anchor.confirmedAt) || null;
@@ -689,7 +689,7 @@
     const persistedTxHashIsReal =
       typeof persistedTxHash === 'string' &&
       persistedTxHash.length > 0 &&
-      !/^(tx_sim_|mock_tx_|tx_)/.test(persistedTxHash);
+      !/^(tx_sim_|mock_tx_|mock_batch_tx_|tx_)/.test(persistedTxHash);
     // Height: a positive integer, not merely truthy. Strict, not coerced (ruled
     // 2026-09-13): a numeric string reaching this read is a shape defect the
     // guard refuses. A string CAN reach it: originate's KS-584 heal path
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts
new file mode 100644
index 000000000..5787a18da
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts
@@ -0,0 +1,189 @@
+// =============================================================================
+// KS-1626 - the api-gateway verify route's two placeholder tests must read the batch mock's hash as a placeholder
+// =============================================================================
+//
+// The non-production batch mock in the anchoring service writes `mock_batch_tx_<64 hex>` as a confirmed anchor's
+// transaction hash. `POST /api/documents/:id/verify` (routes/verification.ts) tests a hash against
+// `/^(tx_sim_|mock_tx_|tx_)/` at two places - the LIVE chain-scan reply and the PERSISTED blob - and neither matches
+// `mock_batch_tx_` (it starts `mock_b`, not `mock_t`), so a batch-mock hash with a height reported `on-chain` with
+// `verified: true`. A real Cardano hash is 64 hex digits and can never contain `_`.
+//
+// Harness copied from the KS-1069 file rather than imported (stub originate, stub chain-scan reply, the real router).
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
+const DOC_ID = 'doc-ks1626';
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
+      res.end(JSON.stringify({
+        id: DOC_ID,
+        status: 'anchored',
+        contentHash: CONTENT_HASH,
+        owner: { id: 'org-1' },
+        ...(currentBlob ? { blockchain: currentBlob } : {}),
+      }));
+      return;
+    }
+    res.writeHead(404, jsonHead);
+    res.end('{}');
+  });
+  originate.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => originate.once('listening', () => r()));
+  const originatePort = (originate.address() as AddressInfo).port;
+
+  // The chain scan is the ONLY caller of globalThis.fetch on this path. Default
+  // is a 404 - no live evidence - so every cell measures its persisted blob.
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
+      // Passthrough auth: this file measures the confidence computation, not auth.
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
+async function post(): Promise<any> {
+  const r = await realFetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' },
+    body: JSON.stringify({ purpose: 'test' }),
+  });
+  expect(r.status).toBe(200);
+  return r.json();
+}
+
+/** Tier 1: the stub originate serves `blob` as the document's blockchain blob. */
+async function verifyTier1(blob: Record<string, unknown> | undefined): Promise<any> {
+  currentBlob = blob;
+  liveAnchorReply = null;
+  anchorStoreRows = null;
+  tier1Absent = false;
+  return post();
+}
+
+async function verifyLive(reply: Record<string, unknown>): Promise<any> {
+  currentBlob = undefined;
+  liveAnchorReply = reply;
+  anchorStoreRows = null;
+  tier1Absent = false;
+  return post();
+}
+
+const BATCH_MOCK_TX = 'mock_batch_tx_' + 'c'.repeat(64);
+const LIVE_REAL = { verified: true, txHash: REAL_TX, blockNumber: 4242 } as const;
+const OFF_CHAIN = { verified: false, confidence: 'off-chain-only' } as const;
+const ON_CHAIN = { verified: true, confidence: 'on-chain' } as const;
+const CONFIRMED_REAL = { txHash: REAL_TX, blockHeight: 4242, status: 'confirmed' } as const;
+
+function claim(body: any): { verified: unknown; confidence: unknown } {
+  return { verified: body.verified, confidence: body.verificationConfidence };
+}
+
+describe('KS-1626 - the batch mock placeholder is not an on-chain claim, live or persisted', () => {
+  it('RED KS-1626 G1 a mock_batch_tx_ hash from the live chain-scan reply is not a hash', async () => {
+    expect(claim(await verifyLive({ ...LIVE_REAL, txHash: BATCH_MOCK_TX }))).toEqual(OFF_CHAIN);
+  });
+
+  it('RED KS-1626 G2 a mock_batch_tx_ persisted hash with a height and confirmed must not report on-chain', async () => {
+    expect(claim(await verifyTier1({ ...CONFIRMED_REAL, txHash: BATCH_MOCK_TX }))).toEqual(OFF_CHAIN);
+  });
+
+  it('CONTROL KS-1626 GC1 a real 64-hex hash from the live reply still reports on-chain', async () => {
+    const body = await verifyLive({ ...LIVE_REAL });
+    expect(claim(body)).toEqual(ON_CHAIN);
+    expect(body.blockchain.txHash).toBe(REAL_TX);
+  });
+
+  it('CONTROL KS-1626 GC2 a real 64-hex persisted hash with a height and confirmed still reports on-chain', async () => {
+    const body = await verifyTier1({ ...CONFIRMED_REAL });
+    expect(claim(body)).toEqual(ON_CHAIN);
+    expect(body.blockchain.txHash).toBe(REAL_TX);
+  });
+
+  it('CONTROL KS-1626 GC3 the older tx_sim_ placeholder is still off-chain-only on both reads', async () => {
+    expect(claim(await verifyLive({ ...LIVE_REAL, txHash: 'tx_sim_' + 'c'.repeat(32) }))).toEqual(OFF_CHAIN);
+    expect(claim(await verifyTier1({ ...CONFIRMED_REAL, txHash: 'tx_sim_' + 'c'.repeat(32) }))).toEqual(OFF_CHAIN);
+  });
+});
```
