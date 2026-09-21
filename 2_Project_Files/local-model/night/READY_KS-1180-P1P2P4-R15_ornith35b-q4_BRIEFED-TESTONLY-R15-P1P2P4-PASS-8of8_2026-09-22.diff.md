# READY — KS-1180-P1P2P4-R15 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1180-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 01:15 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch DIFFERS from the drafter's golden at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/1180P1P2P4-R15/out.md.checker/patch.diff` (`cmp` rc 1) — read the diff before raising.

**Held 01:15 2026-09-22 by Wednesday 00:05 seat, drain sitting: expected_plus 26/26 in the diff; reds matched 2/2; golden DIFFERS (hunk-header form only; +/- body identical) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1180-ornith35b-night/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts` (modify). `+` lines 26 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 4 == `must_remove`. Green at the tip: 5/5 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `P1P2P4` → red exactly ['RED KS-1180 - a tier-1 statusless document whose doc-level _', 'RED KS-1180 - a tier-1 statusless document whose doc-level _']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1180-ornith35b-night/input.json`. Brief: `night/briefs/KS-1180-P1P2P4-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1180-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts
@@ -10,5 +10,5 @@
 //
 // This file reuses the stub originate server, the stub anchor store, and the gateway app from
 // ks1057-verify-confidence-is-status-aware.test.ts — same shape, new cells. All original `it(...)`s
-// dropped; three cells written below.
+// dropped; three KS-1073 cells written below, then two KS-1180 cells (a doc-level _source other than 'anchor_store').
 // =============================================================================
@@ -37,4 +37,8 @@
 let anchorStoreRows: Array<Record<string, unknown>> | null = null;
 /** When true the stub originate 404s, so the lookup falls through to tier 2. */
 let tier1Absent = false;
+/** KS-1180 (P-1005-1): requests the stub anchor store received. Tier 2 answered only if this is 1. */
+let anchorHits = 0;
+/** KS-1180 (P-1005-2): doc-level keys the stub originate adds to the tier-1 document for the current cell. */
+let tier1DocExtra: Record<string, unknown> = {};
 const jsonHead = { 'Content-Type': 'application/json' };
@@ -44,6 +44,7 @@
   // blob each cell sets.
   originate = http.createServer((req, res) => {
     if (req.url === `/api/anchors/document/${DOC_ID}`) {
+      anchorHits += 1;
       if (!anchorStoreRows) { res.writeHead(404, jsonHead); res.end('{}'); return; }
       res.writeHead(200, jsonHead);
       res.end(JSON.stringify({ data: { anchors: anchorStoreRows } }));
@@ -58,6 +58,7 @@
         contentHash: CONTENT_HASH,
         owner: { id: 'org-1' },
         ...(currentBlob ? { blockchain: currentBlob } : {}),
+        ...tier1DocExtra,
       }));
       return;
     }
@@ -128,14 +129,18 @@
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
@@ -145,15 +150,17 @@
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
@@ -185,4 +192,14 @@
     expect(body.verified).toBe(true);
     expect(body.verificationConfidence).toBe('on-chain');
   });
+  it('RED KS-1180 - a tier-1 statusless document whose doc-level _source is originate still reports on-chain', async () => {
+    const originateBody = await verify({ txHash: REAL_TX, blockHeight: 4242 }, { _source: 'originate' });
+    expect(originateBody.verificationConfidence, 'KS-1180 originate: confidence').toBe('on-chain');
+    expect(originateBody.verified, 'KS-1180 originate: verified').toBe(true);
+  });
+  it('RED KS-1180 - a tier-1 statusless document whose doc-level _source is ANCHOR_STORE still reports on-chain', async () => {
+    const upperCaseBody = await verify({ txHash: REAL_TX, blockHeight: 4242 }, { _source: 'ANCHOR_STORE' });
+    expect(upperCaseBody.verificationConfidence, 'KS-1180 ANCHOR_STORE: confidence').toBe('on-chain');
+    expect(upperCaseBody.verified, 'KS-1180 ANCHOR_STORE: verified').toBe(true);
+  });
 });
```
