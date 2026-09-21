# READY — KS-1199-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1199-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 22:00 2026-09-21). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; golden not located — no byte-identity claim is made.

**Held 22:00 2026-09-21 by Wednesday (the 20:1x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1199-ornith35b-night/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1199-status-differing-anchor-tie-verdict.test.ts` (new). `+` lines 113 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 4/4 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `R15` → red exactly ['RED KS-1199 - confirmed January listed first, failed June se', 'RED KS-1199 - confirmed January listed first, submitted June', 'RED KS-1199 - failed June listed first, confirmed January se']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1199-ornith35b-night/input.json`. Brief: `night/briefs/KS-1199-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1199-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1199-status-differing-anchor-tie-verdict.test.ts
@@ -0,0 +1,113 @@
+// KS-1199 (the #1016 gate P-1016-3 on KS-1072): every ks1072 cell ties two CONFIRMED anchors and asserts txHash only, so a
+// tiebreak that preferred the confirmed row passed 424 of 424 cells. These cells pin the VERDICT on a status-differing tie.
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+
+const DOC_ID = 'doc-ks1199';
+const CONTENT_HASH = 'c'.repeat(64);
+const JAN = '2026-01-01T00:00:00Z';
+const JUN = '2026-06-01T00:00:00Z';
+const OLD_TX = 'a'.repeat(64);
+const NEW_TX = 'b'.repeat(64);
+const jsonHead = { 'Content-Type': 'application/json' };
+const priorAnchoringUrl = process.env.ANCHORING_SERVICE_URL;
+
+let gateway: Server;
+let anchorServer: Server;
+let originate: Server;
+let gatewayPort = 0;
+let anchorStoreRows: Array<Record<string, unknown>> = []; // the tier-2 rows the stub anchor store serves, in the order listed
+let anchorStoreHits = 0; // reads of this document from the stub anchor store in the current cell: the tier-2 witness
+
+/** One anchor row at the SAME blockNumber as every other row in this file, so only the tiebreak separates them. */
+function row(status: string, confirmedAt: string, txHash: string): Record<string, unknown> {
+  return { blockNumber: 100, confirmedAt, transaction_hash: txHash, status, contentHash: CONTENT_HASH };
+}
+
+/** Verifies the document over the real router with these rows; answers [status, anchor-store hits, verified, confidence, txHash]. */
+async function verdictFor(rows: Array<Record<string, unknown>>): Promise<unknown[]> {
+  anchorStoreRows = rows;
+  anchorStoreHits = 0;
+  const url = 'http://127.0.0.1:' + String(gatewayPort) + '/api/documents/' + DOC_ID + '/verify';
+  const res = await fetch(url, { method: 'POST', headers: jsonHead, body: JSON.stringify({ contentHash: CONTENT_HASH, purpose: 'test' }) });
+  const body = (await res.json()) as { verified?: unknown; verificationConfidence?: unknown; blockchain?: { txHash?: unknown } };
+  return [res.status, anchorStoreHits, body.verified, body.verificationConfidence, body.blockchain?.txHash];
+}
+
+beforeAll(async () => {
+  anchorServer = http.createServer((req, res) => {
+    if (req.url === '/api/anchors/document/' + DOC_ID) {
+      anchorStoreHits += 1;
+      res.writeHead(200, jsonHead);
+      res.end(JSON.stringify({ data: { anchors: anchorStoreRows } }));
+      return;
+    }
+    res.writeHead(404, jsonHead); res.end('{}');
+  });
+  anchorServer.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => anchorServer.once('listening', () => r()));
+  const anchorUrl = 'http://127.0.0.1:' + String((anchorServer.address() as AddressInfo).port);
+  process.env.ANCHORING_SERVICE_URL = anchorUrl; // the live scan answers 404 on loopback, never off-host
+
+  originate = http.createServer((_req, res) => { res.writeHead(404, jsonHead); res.end('{}'); }); // tier 1 never answers
+  originate.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => originate.once('listening', () => r()));
+  const originateUrl = 'http://127.0.0.1:' + String((originate.address() as AddressInfo).port);
+
+  const { createVerificationRoutes } = await import('../routes/verification');
+  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
+  const app = express();
+  app.use(createVerificationRoutes({
+    authenticateToken: () => (_req, _res, next) => next(), mockBodyParser,
+    query: vi.fn(async () => ({ rows: [] })) as never,
+    isDbAvailable: () => false, log: () => undefined,
+    redisService: {
+      getPendingDocument: vi.fn(async () => null), deletePendingDocument: vi.fn(async () => undefined), getAllDocumentTypes: vi.fn(async () => []),
+      getAllWorkflowInstances: vi.fn(async () => []), getNotificationSettings: vi.fn(async () => ({})), getRejectedDocument: vi.fn(async () => null),
+      setRejectedDocument: vi.fn(async () => undefined), getWorkflowDocumentMapping: vi.fn(async () => null),
+      getWorkflowInstance: vi.fn(async () => null), setWorkflowInstance: vi.fn(async () => undefined),
+    } as never,
+    services: { originate: { url: originateUrl }, anchoring: { url: anchorUrl } } as never,
+    memWorkflowToDocumentMap: new Map(), memRejectedDocuments: new Map(),
+    dbSaveRejection: vi.fn(async () => undefined), ADMIN_ROLES: ['ADMIN', 'admin'],
+    enforceDocumentTypeRules: vi.fn(async () => ({ ok: true, docType: {} })) as never,
+    createWorkflowInstanceIfRequired: vi.fn(async () => ({ gated: false })) as never,
+    meetsVerificationLevel: () => true,
+  }));
+  gateway = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => gateway.once('listening', () => r()));
+  gatewayPort = (gateway.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  if (priorAnchoringUrl === undefined) delete process.env.ANCHORING_SERVICE_URL; else process.env.ANCHORING_SERVICE_URL = priorAnchoringUrl;
+  await new Promise<void>((r) => gateway.close(() => r()));
+  await new Promise<void>((r) => anchorServer.close(() => r()));
+  await new Promise<void>((r) => originate.close(() => r()));
+});
+
+describe('KS-1199 - an equal-blockNumber tie whose rows differ in status: the newer row decides the verdict', () => {
+  it('RED KS-1199 - confirmed January listed first, failed June second: not verified, off-chain-only', async () => {
+    const answer = await verdictFor([row('confirmed', JAN, OLD_TX), row('failed', JUN, NEW_TX)]);
+    expect(answer, 'the newer failed anchor decides').toEqual([200, 1, false, 'off-chain-only', NEW_TX]);
+  });
+
+  it('RED KS-1199 - failed June listed first, confirmed January second: still not verified', async () => {
+    const answer = await verdictFor([row('failed', JUN, NEW_TX), row('confirmed', JAN, OLD_TX)]);
+    expect(answer, 'the newer failed anchor decides whatever the order').toEqual([200, 1, false, 'off-chain-only', NEW_TX]);
+  });
+
+  it('RED KS-1199 - confirmed January listed first, submitted June second: pending, not verified', async () => {
+    const answer = await verdictFor([row('confirmed', JAN, OLD_TX), row('submitted', JUN, NEW_TX)]);
+    expect(answer, 'the newer in-flight anchor decides').toEqual([200, 1, false, 'pending-onchain', NEW_TX]);
+  });
+
+  it('GREEN KS-1199 control - failed January listed first, confirmed June second: verified on-chain', async () => {
+    const answer = await verdictFor([row('failed', JAN, OLD_TX), row('confirmed', JUN, NEW_TX)]);
+    expect(answer, 'the newer confirmed anchor decides').toEqual([200, 1, true, 'on-chain', NEW_TX]);
+  });
+});
```
