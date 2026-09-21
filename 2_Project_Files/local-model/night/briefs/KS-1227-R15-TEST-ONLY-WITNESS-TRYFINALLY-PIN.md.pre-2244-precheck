# KS-1227 R15-TEST-ONLY-WITNESS-TRYFINALLY-PIN - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 190 lines read whole)
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `vitest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1227_ornith35b-q4_TEST-ONLY-WITNESS-TRYFINALLY-PIN-PASS-7of7_2026-09-17.diff.md` (its checker PASS was at an OLDER tip; run dir exists: `runs/2026-09-17_ks1227-ornith35b-night`); canonical patch 3399 B sha256[:16] `a83f86d50148d8ec`, +24/-8.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 1 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts` at the tip: EXISTS (190 lines) - MODIFY IN PLACE. Mode: **MODIFY**.
- Tamper source: the old brief `night/briefs/KS-1227.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-1227: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments none (all merged); briefs already on disk: KS-1227.md.
- Generator notes: reds INFERRED as every non-CONTROL/COMPLETENESS cell (2) - no RED-prefixed title in the old patch; Wednesday confirms the set against the old READY header; the run input.json is the older code_patch shape (no tampers key) - tampers taken from the old brief instead; CONTROL INFERRED: the file's first existing cell 'KS-1180 control - a document the anchor store does not have:' (green on both trees by construction; the old READY declared no control); Runner: vitest from the old brief header.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them at tip 2026-09-17; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1227 (test-only, api-gateway ks1072 test: try/finally around postTier2's witness listener + R1 env-pointed witness pin + R2 listener-leak cell)
> # Source read by Wednesday 23:40: the model's 32 +/- lines (+24/-8) IDENTICAL to the brief (python sequence compare; a mutated copy unequal); checker RESULT PASS (7/7) first sample; A4 red-first by assertion. Tip = develop 27e53ec3a. HELD LATE: PASS at 23:14, held 23:4x (the seat was on gate verdicts; ledger row).
> # PR NOTES: `Refs KS-1227: R1 pins the counting rule AS MERGED; the keep-vs-filter decision stays open on the ticket`; the :128 reword half not done. TIER 2 (test-only). Run: runs/2026-09-17_ks1227-ornith35b-night/out.md.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, MODIFY IN PLACE: your diff contains EXACTLY ONE file, the EXISTING test file above, as the hunk(s) below (context lines byte-for-byte from the tip; no blank context line; no blank + line; a pure insertion ends with a context line). No product hunk. 

## The exact change
```
@@ -115,14 +115,14 @@
   const anchorStoreUrls: string[] = []; // KS-1180 (P-1016-1): the requests the stub anchor store receives during this verify
   const onAnchorStoreRequest = (req: { url?: string }): void => { anchorStoreUrls.push(String(req.url)); };
   anchorServer.on('request', onAnchorStoreRequest);
-  const res = await fetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
-    method: 'POST',
-    headers: { 'Content-Type': 'application/json' },
-    body: JSON.stringify({ purpose: 'test' }),
-  });
-  expect(res.status).toBe(200);
-  const body = await res.json();
-  anchorServer.off('request', onAnchorStoreRequest);
+  let body: unknown;
+  try {
+    const res = await fetch('http://127.0.0.1:' + String(gatewayPort) + '/api/documents/' + DOC_ID + '/verify', { method: 'POST', headers: jsonHead, body: JSON.stringify({ purpose: 'test' }) });
+    expect(res.status).toBe(200); // KS-1227 (R-1029-3): inside the try, so a status red still reaches the finally
+    body = await res.json();
+  } finally {
+    anchorServer.off('request', onAnchorStoreRequest); // KS-1227: detached on every path, as the KS-1180 control detaches before it asserts
+  }
   // KS-1180 (P-1016-1): the tier witness. blockchain.source reads 'persisted' on BOTH tiers, so it cannot say which tier
   // answered. Tier 2 answered only if the stub anchor store served this document exactly once.
   expect(anchorStoreUrls, 'KS-1180: tier 2 answered, one anchor-store read of this document').toEqual(['/api/anchors/document/' + DOC_ID]);
@@ -187,4 +187,20 @@
     ]);
     expect(body.blockchain.txHash).toBe('e'.repeat(64));
   });
+  it('KS-1227 R1 - a second request reaching the stub anchor store reds the postTier2 witness even though tier 2 answered', async () => {
+    // KS-1227 (R-1029-2, R-1029-4): the witness counts EVERY stub request, as merged at 27e53ec3a, so a hit-only URL filter
+    // in postTier2 reds here. The live chain scan reads ANCHORING_SERVICE_URL; pointing it at the stub adds a non-hit request.
+    vi.stubEnv('ANCHORING_SERVICE_URL', 'http://127.0.0.1:' + String((anchorServer.address() as AddressInfo).port));
+    try {
+      const witness = await postTier2([{ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transaction_hash: '5'.repeat(64), status: 'confirmed' }]).then(() => 'no red', (e: Error) => e.message);
+      expect(witness).toContain('KS-1180: tier 2 answered, one anchor-store read of this document');
+    } finally {
+      vi.unstubAllEnvs();
+    }
+  }); // KS-1227 R1
+  it('KS-1227 R2 - a status red inside postTier2 still detaches its anchor-store listener', async () => {
+    // KS-1227 (R-1029-3): an empty store answers 404, so the helper reds at its status read; only the stub handler stays attached.
+    const statusRed = await postTier2([]).then(() => 'no red', (e: Error) => e.message);
+    expect([statusRed.startsWith('expected 404 to be 200'), anchorServer.listenerCount('request')]).toEqual([true, 1]);
+  }); // KS-1227 R2
 });
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `KS-1227 R1 - a second request reaching the stub anchor store reds the postTier2 witness even though tier 2 answered`
- `KS-1227 R2 - a status red inside postTier2 still detaches its anchor-store listener`
- `KS-1180 control - a document the anchor store does not have: 404, and the stub anchor store was asked once`  (CONTROL - green on both trees)

## Tampers
### TESTONLYWITNESSTRYFINALLYPIN
File: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts`
Line: 585
From:
```
    const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
```
To:
```
    const anchoringBase = 'http://anchoring:4005'; // TAMPER: KS-1227 red-proof, the live chain scan ignores ANCHORING_SERVICE_URL, so no second request reaches the stub
```
Reds: `KS-1227 R1 - a second request reaching the stub anchor store reds the postTier2 witness even though tier 2 answered`, `KS-1227 R2 - a status red inside postTier2 still detaches its anchor-store listener`
(From located at the tip: 1 match(es); the old brief/input said line 585)

## Controls
- `KS-1180 control - a document the anchor store does not have: 404, and the stub anchor store was asked once`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
