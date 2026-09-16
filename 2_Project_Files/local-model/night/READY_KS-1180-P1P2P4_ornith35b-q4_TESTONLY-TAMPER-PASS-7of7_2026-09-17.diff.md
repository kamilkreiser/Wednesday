# READY — KS-1180 PARTIAL: P-1005-1, P-1005-2, P-1005-4 (TEST-ONLY, MODIFY-IN-PLACE ks1073-tier-2-verify-has-no-statusless.test.ts: an anchor-store hit counter so the tier-2 cells witness the tier that answered; two KS-1180 cells pinning that a tier-1 statusless document whose doc-level _source is 'originate' / 'ANCHOR_STORE' still reports on-chain; the TS18046 `body` type fixed) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (03:25:42). Held by Wednesday at 03:27 AEST. Run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-17_ks1180-ornith35b-night
# Source read by me (Wednesday): the model's 28 `+` and 4 `-` lines are IDENTICAL in sequence to the brief's seven `## The exact change` hunks (python sequence compare over every fence; a one-character mutated copy compares unequal — the control); ONE file, product untouched; A2 applied STRICT (no fuzz, no recount). A4 under the #1005 gate's GL tamper (verification.ts:703 conjunct loosened to `!_source`): 2 failed / 5 run, both KS-1180 cells red by assertion, controls green. A5 5/5. A6 whole api-gateway 394 → 396, NEW reds []. A7 tsc rc 0.
# NOT MEASURED BY THE CHECKER: P-1005-4 (TS18046 at the old :157) — the checker's standalone tsc is blind to it (brief premise P10: an INCLUDING program gives rc 2 / 1 error on the old file, rc 0 on the golden). The model's lines equal the golden's, so the fix is carried; the raising seat runs an including tsc to confirm. P-1005-1's witness is a TEST-side property graded by the brief writer under GT2 (P8), not by the checker.
# PR NOTES: "Refs KS-1180 (P-1005-1, P-1005-2, P-1005-4)" — never Closes (P-1005-3 = the verification.ts:353 marker comment and R-1005-2's optional move are PRODUCT edits, still open). A tier-2 gate (test-only follow-up of an already-gated mechanism). api-gateway `__tests__` = the Secuura raise seat's partition; verification.ts is currently seat A's A9 lane — this file does not touch it.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts
@@ -10,7 +10,7 @@
 //
 // This file reuses the stub originate server, the stub anchor store, and the gateway app from
 // ks1057-verify-confidence-is-status-aware.test.ts — same shape, new cells. All original `it(...)`s
-// dropped; three cells written below.
+// dropped; three KS-1073 cells written below, then two KS-1180 cells (a doc-level _source other than 'anchor_store').
 // =============================================================================
 
 import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
@@ -37,6 +37,10 @@
 let anchorStoreRows: Array<Record<string, unknown>> | null = null;
 /** When true the stub originate 404s, so the lookup falls through to tier 2. */
 let tier1Absent = false;
+/** KS-1180 (P-1005-1): requests the stub anchor store received. Tier 2 answered only if this is 1. */
+let anchorHits = 0;
+/** KS-1180 (P-1005-2): doc-level keys the stub originate adds to the tier-1 document for the current cell. */
+let tier1DocExtra: Record<string, unknown> = {};
 const jsonHead = { 'Content-Type': 'application/json' };
 
 beforeAll(async () => {
@@ -44,6 +48,7 @@
   // blob each cell sets.
   originate = http.createServer((req, res) => {
     if (req.url === `/api/anchors/document/${DOC_ID}`) {
+      anchorHits += 1;
       if (!anchorStoreRows) { res.writeHead(404, jsonHead); res.end('{}'); return; }
       res.writeHead(200, jsonHead);
       res.end(JSON.stringify({ data: { anchors: anchorStoreRows } }));
@@ -58,6 +63,7 @@
         contentHash: CONTENT_HASH,
         owner: { id: 'org-1' },
         ...(currentBlob ? { blockchain: currentBlob } : {}),
+        ...tier1DocExtra,
       }));
       return;
     }
@@ -126,17 +132,21 @@
 });
 
 /** Drive the tier-1 route and return the parsed body. */
-async function verify(blob: Record<string, unknown> | undefined): Promise<any> {
+async function verify(blob: Record<string, unknown> | undefined, docExtra: Record<string, unknown> = {}): Promise<any> {
   currentBlob = blob;
   liveAnchorReply = null;
   anchorStoreRows = null;
   tier1Absent = false;
+  tier1DocExtra = docExtra;
+  anchorHits = 0;                           // KS-1180: a tier-1 cell, so 0 is asserted below
   const r = await realFetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' },
     body: JSON.stringify({ purpose: 'test' }),
   });
   expect(r.status).toBe(200);
+  // KS-1180 (P-1005-1): the 0-hit control. Tier 1 answered, so the stub anchor store was never asked.
+  expect(anchorHits, 'KS-1180: tier 1 answered, so tier 2 was never asked').toBe(0);
   return r.json();
 }
 
@@ -145,16 +155,18 @@
   currentBlob = undefined;
   liveAnchorReply = null;
   tier1Absent = true;                       // tier 1 misses -> fall through to tier 2
+  anchorHits = 0;                           // KS-1180: a tier-2 cell, so exactly 1 is asserted below
   anchorStoreRows = [{ contentHash: CONTENT_HASH, ...row }];
   const r = await realFetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' },
     body: JSON.stringify({ purpose: 'test' }),
   });
   expect(r.status).toBe(200);
   const body = await r.json();
-  // Guard the whole family: if tier 2 were not the tier that answered, every assertion below would be about the wrong code path.
-  expect(body.blockchain.source).toBe('persisted');
+  // KS-1180 (P-1005-1): the tier witness. blockchain.source reads 'persisted' on BOTH tiers, so it cannot say which
+  // tier answered. The anchor-store request count can: tier 2 answered only if the stub anchor store was asked once.
+  expect(anchorHits, 'KS-1180: tier 2 must be the tier that answered').toBe(1);
   return body;
 }
 
@@ -185,4 +197,16 @@
     expect(body.verified).toBe(true);
     expect(body.verificationConfidence).toBe('on-chain');
   });
+
+  it('🔴 KS-1180 — a tier-1 statusless document whose doc-level _source is originate still reports on-chain', async () => {
+    const originateBody = await verify({ txHash: REAL_TX, blockHeight: 4242 }, { _source: 'originate' });
+    expect(originateBody.verificationConfidence, 'KS-1180 originate: confidence').toBe('on-chain');
+    expect(originateBody.verified, 'KS-1180 originate: verified').toBe(true);
+  });
+
+  it('🔴 KS-1180 — a tier-1 statusless document whose doc-level _source is ANCHOR_STORE still reports on-chain', async () => {
+    const upperCaseBody = await verify({ txHash: REAL_TX, blockHeight: 4242 }, { _source: 'ANCHOR_STORE' });
+    expect(upperCaseBody.verificationConfidence, 'KS-1180 ANCHOR_STORE: confidence').toBe('on-chain');
+    expect(upperCaseBody.verified, 'KS-1180 ANCHOR_STORE: verified').toBe(true);
+  });
 });
```
