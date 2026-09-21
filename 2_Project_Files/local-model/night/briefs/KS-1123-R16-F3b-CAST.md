# KS-1123 R16-F3b-CAST - REBRIEF 1 of 1 (Kam's 2026-09-16 counter: round 2 of 2) - the R15-F3b READY (checker PASS 8/8, run `runs/2026-09-21_ks1123-ornith35b-night3`; it SUPERSEDED F2-R15) re-issued with its ONE TypeScript error fixed, at develop 64ab10513 (written 03:50 on 2026-09-22 by Wednesday's rebrief3 drafter from the R15-F3b brief + READY fence read whole, api-gateway/src/routes/verification.ts:624 + :746 re-located at the tip, api-gateway/tsconfig.json and the seat's tsc output)
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1123-api-gateway-verify-an-empty-string.test.ts`
Tip: `64ab105132eada0621622acf4d6053bc59926780`
Runner: `vitest`

## Premises (measured by the rebrief3 drafter at 03:52:33 AEST on 2026-09-22, in a `--shared` scratchpad clone detached at 64ab10513; Wednesday re-derives before queueing)
- THE DEFECT of round 1 (`READY_KS-1123-F3b-R15_..._PASS-8of8_2026-09-22.diff.md`, HELD 00:14 09-22): vitest green and checker PASS 8/8, the run's patch byte-identical to the drafter's golden, but Seat C 16th's targeted type-check (a temp tsconfig extending api-gateway's `tsconfig.json` - `strict`, `noUnusedLocals`, `noUnusedParameters` - with `files=[the test]`, `exclude []`, planted TS2322 control CAUGHT) reports ONE error in the NEW file (delta +1), verbatim from `5_Project_History/2026-09-22_seatC-16th/raise/typecheck17.out`:
  - `src/__tests__/ks1123-api-gateway-verify-an-empty-string.test.ts(158,10): error TS18046: 'body' is of type 'unknown'.`
- THE CAUSE: in `verifyViaAnchorStore` the parsed body is `const body = await r.json();` - `Response.json()` is typed `Promise<unknown>` under `strict`, and three lines later `expect(body.blockchain.source)` reads a property of `unknown`. The sibling helper `verify()` never hit this because it RETURNS `r.json()` straight into its declared `Promise<any>`.
- THE FIX (ONE line differs from the round-1 fence; every cell, tamper and control is the SAME): `const body: any = await r.json();` - the same explicit `any` the file already uses for both helpers' return types (`Promise<any>`), so the guard `expect(body.blockchain.source).toBe('persisted')` and `return body;` type-check. Nothing else in the 215 lines moves; the '+' count is unchanged at 215.
- VERIFIED by the drafter in the clone at 64ab10513: the fence written to its path and type-checked with the SAME instrument shape (`tsconfig.rebrief3-*.json` extending `./tsconfig.json`, `files=[src/__tests__/ks1123-api-gateway-verify-an-empty-string.test.ts]`, `include []`, `exclude []`, `types ["node","vitest/globals"]`, `npx tsc -p`): 0 errors in the file (the round-1 fence under the same instrument: 1, the TS18046 above - the positive control). Golden precheck (this fence as the model output through `tasks/test_only/checker.sh`): see the proposal.
- QUOTE RULE (IMPROVEMENTS 2026-09-22 02:35): `grep -c` for `"` over the '+' lines = 0, for a backslash = 0, non-ASCII = 0 (round 1 was already clean; unchanged).
- TAMPERS re-located at 64ab10513 (develop moved 581ed7fa1 -> 64ab10513 since the R15-F3b brief): F2 `verification.ts:746` = `        : persistedStatus == null && persistedConfidence === 'pending-onchain'` (exact whole-line match count 1); F3 `verification.ts:624` = `    const persistedStatus = (doc as any).blockchain?.status ?? null;` (exact whole-line match count 1). Same line numbers as R15-F3b - the file did not move between the two tips.
- THE R15-F3b PREMISES STAND (read them in `night/briefs/KS-1123-R15-F3b.md`): reachability of the tier-1 F3 red via :624 -> :722 -> :741-748; why the old tier-2 red is a CONTROL since KS-1073 (#1005) added `_source !== 'anchor_store'` to the :722 carve-out; the fold of the F2 cells into this one NEW file (a PASS here SUPERSEDES both the held F2-R15 and F3b-R15 READYs as the PR unit).
- Ticket KS-1123: Backlog (as at the census15 read); PR attachments #1002 (merged). Nothing in the product changes.

## What is wrong (one paragraph)
`services/api-gateway/src/routes/verification.ts` decides `verificationConfidence` from the persisted anchor status. Two guards keep it honest and nothing in the suite pins either: (F2) the third arm of the chained ternary at :746 upgrades to `pending-onchain` on a stale `confidence` field ONLY for a statusless blob (`persistedStatus == null &&`); (F3) the read at :624 uses `??`, so an EMPTY-STRING status (a value `anchor_store.status TEXT` can hold) stays a real non-confirmed status instead of collapsing to null and firing the tier-1 statusless carve-out at :722 (a real hash and height would then report on-chain / verified: true). The code is RIGHT at the tip. This task is the PIN: one new test file whose F2 cells red when the :746 guard is dropped and whose F3 cell reds when `??` becomes `||`. Round 1 wrote exactly these cells and PASSed; it is re-issued ONLY because one line does not type-check under api-gateway's tsconfig. Reproduce the fence below byte for byte.

## THE MODE - read this twice
TEST-ONLY, ONE NEW FILE: your diff contains EXACTLY ONE file, the NEW test file above: `--- /dev/null` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1123-api-gateway-verify-an-empty-string.test.ts` then ONE `@@ -0,0 +1,215 @@` hunk, every line `+`, no context, no `-`. No product hunk. Copy the 215 lines below byte for byte, in order. Every string in this file is single-quoted; there is NO double-quote character and NO backslash anywhere in the file - never add, escape or change a quote.

## The exact change
```
+// =============================================================================
+// KS-1123 F2 - TEST ONLY MODE (no product hunk)
+//
+// The guard at verification.ts:709 (`persistedStatus == null &&`) stops a
+// stale confidence field from upgrading any non-statusless blob to pending-onchain.
+// This file pins that behaviour with two tier-1 cells that only the guard keeps honest.
+//
+// The checker reddens these RED cells by replacing line 709 with:
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
+/** Drive the tier-2 verify path via the stub anchor store and return the parsed body. */
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
+  const body: any = await r.json();
+  // Guard the whole family: if tier 2 were not the tier that answered, every
+  // assertion below would be about the wrong code path.
+  expect(body.blockchain.source).toBe('persisted');
+  return body;
+}
+
+describe('KS-1123 F2 - stale confidence cannot upgrade a status', () => {
+  it('RED KS-1123 F2 - a failed anchor with a stale confidence field stays off-chain-only', async () => {
+    // Under the tamper :709 becomes `persistedConfidence === 'pending-onchain'`
+    // which is TRUE here -> `'pending-onchain'`. At the tip line 709 requires
+    // `persistedStatus == null &&` so this cell measures OFF-CHAIN-ONLY.
+    const body = await verify({ txHash: null, blockHeight: 0, status: 'anchor_failed', confidence: 'pending-onchain' });
+    expect(body.verificationConfidence).toBe('off-chain-only');
+    expect(body.blockchain.confidence).toBe('off-chain-only');
+    expect(body.verified).toBe(false);
+  });
+
+  it('RED KS-1123 F2 - a confirmed-status blob with no hash and a stale confidence field stays off-chain-only', async () => {
+    // No hash -> not anchored (line 705 false). `'confirmed'` maps to on-chain via
+    // confidenceForAnchorStatus (line 707 checks for pending-onchain only), so
+    // line 707 is false. Line 709 at the tip refuses because persistedStatus !== null.
+    // Under the tamper -> `'pending-onchain'` - the red.
+    const body = await verify({ txHash: null, blockHeight: null, status: 'confirmed', confidence: 'pending-onchain' });
+    expect(body.verificationConfidence).toBe('off-chain-only');
+    expect(body.verified).toBe(false);
+  });
+
+  it('KS-1123 control - a pending-status blob is pending-onchain, before and after', async () => {
+    // Decided by line 707 (`confidenceForAnchorStatus('pending') === 'pending-onchain'`)
+    // and never reaches line 709. Green both sides of the change.
+    const body = await verify({ txHash: null, blockHeight: null, status: 'pending', confidence: 'pending-onchain' });
+    expect(body.verificationConfidence).toBe('pending-onchain');
+    expect(body.verified).toBe(false);
+  });
+});
+
+describe('KS-1123 F3 - an empty-string status must stay off-chain-only (not collapse to null)', () => {
+  it('RED KS-1123 F3 - tier 1: an EMPTY-STRING status with a real hash and height is off-chain-only', async () => {
+    // Under the tamper `??` -> `||` at verification.ts:624 the '' collapses to null, the tier-1
+    // statusless carve-out at :722 fires, and a real hash + height report on-chain / verified: true.
+    const body = await verify({ txHash: REAL_TX, blockHeight: 4242, status: '' });
+    expect(body.verified).toBe(false);
+    expect(body.verificationConfidence).toBe('off-chain-only');
+  });
+
+  it('KS-1123 F3 control - tier 2: the empty-string twin stays off-chain-only even when tier 1 collapses', async () => {
+    // Green on both trees since KS-1073 (#1005): the carve-out at :722 excludes `_source: 'anchor_store'`,
+    // so a null status on this tier never earns the claim - the F3 tamper cannot reach it.
+    const body = await verifyViaAnchorStore({ transactionHash: REAL_TX, blockNumber: 4242, status: '' });
+    expect(body.verified).toBe(false);
+    expect(body.verificationConfidence).toBe('off-chain-only');
+  });
+
+  it('KS-1123 F3 control - a confirmed tier-1 blob still reports on-chain', async () => {
+    // Green at the tip AND under both tampers (a 'confirmed' status is neither falsy nor stale).
+    const body = await verify({ txHash: REAL_TX, blockHeight: 4242, status: 'confirmed' });
+    expect(body.verified).toBe(true);
+    expect(body.verificationConfidence).toBe('on-chain');
+  });
+});
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles - literal rendered strings)
- `RED KS-1123 F2 - a failed anchor with a stale confidence field stays off-chain-only`
- `RED KS-1123 F2 - a confirmed-status blob with no hash and a stale confidence field stays off-chain-only`
- `KS-1123 control - a pending-status blob is pending-onchain, before and after`  (CONTROL - green on both trees)
- `RED KS-1123 F3 - tier 1: an EMPTY-STRING status with a real hash and height is off-chain-only`
- `KS-1123 F3 control - tier 2: the empty-string twin stays off-chain-only even when tier 1 collapses`  (CONTROL - green on both trees; KS-1073 keeps tier 2 out of the carve-out)
- `KS-1123 F3 control - a confirmed tier-1 blob still reports on-chain`  (CONTROL - green on both trees)

## Tampers
### F2
File: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts`
Line: 746
From:
```
        : persistedStatus == null && persistedConfidence === 'pending-onchain'
```
To:
```
        : persistedConfidence === 'pending-onchain' // TAMPER: the statusless-only guard dropped - a stale confidence now upgrades any status
```
Reds: `RED KS-1123 F2 - a failed anchor with a stale confidence field stays off-chain-only`, `RED KS-1123 F2 - a confirmed-status blob with no hash and a stale confidence field stays off-chain-only`
(From located at 64ab10513 by exact whole-line match: 1 match, at :746. Reachability: both F2 cells send no hash, so :722 is false and :744 is false ('anchor_failed' and 'confirmed' do not map to pending-onchain); :746 alone decides them and the tampered :746 is true for both (`confidence: 'pending-onchain'` present). The F3 cells never reach :746: the tier-1 red is decided at :722 under its own tamper and at :744/:748 at the tip; the controls are decided at :722 ('confirmed' -> on-chain) and :744 ('pending' -> pending-onchain).)

### F3
File: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts`
Line: 624
From:
```
    const persistedStatus = (doc as any).blockchain?.status ?? null;
```
To:
```
    const persistedStatus = (doc as any).blockchain?.status || null; // TAMPER: KS-1123 F3, an empty-string status collapses to null and fires the statusless carve-out
```
Reds: `RED KS-1123 F3 - tier 1: an EMPTY-STRING status with a real hash and height is off-chain-only`
(From located at 64ab10513 by exact whole-line match: 1 match, at :624. Reachability: the tier-1 F3 cell sends `status: ''` with a real 64-hex hash and height 4242; :624 tampered gives null; :722 `persistedStatus == null && _source !== 'anchor_store'` is true on tier 1 -> on-chain, verified true -> the red. The F2 cells under this tamper: their statuses 'anchor_failed' / 'confirmed' / 'pending' are truthy strings, `||` and `??` agree -> unchanged -> green. The tier-2 control: null status on `_source: 'anchor_store'` -> :722 false -> off-chain-only -> green.)

## Controls
- `KS-1123 control - a pending-status blob is pending-onchain, before and after`
- `KS-1123 F3 control - tier 2: the empty-string twin stays off-chain-only even when tier 1 collapses`
- `KS-1123 F3 control - a confirmed tier-1 blob still reports on-chain`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/api-gateway/src/__tests__/ks1123-api-gateway-verify-an-empty-string.test.ts`); the header `@@ -0,0 +1,215 @@` (215 '+' lines - count them; the R15 batch over-declared new-file headers by 2-20 lines); single quotes only, no `"`, no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
