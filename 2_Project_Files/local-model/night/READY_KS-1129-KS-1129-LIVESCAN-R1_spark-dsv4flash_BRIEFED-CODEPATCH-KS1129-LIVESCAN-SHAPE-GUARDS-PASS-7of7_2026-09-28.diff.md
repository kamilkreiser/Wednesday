# READY — KS-1129-KS-1129-LIVESCAN-R1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1129-LIVESCAN-R1/out.md.checker/patch.diff`** (from `ls` at 16:27 2026-09-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1129-LIVESCAN-R1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1129-LIVESCAN-R1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1129-LIVESCAN-R1/out.md.checker/patch.diff /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/golden_KS-1129-LIVESCAN-R1/out.md.checker/patch.diff` rc 0, Wednesday morning 4901153c).

**Held 16:27 2026-09-28 by Wednesday morning 4901153c after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1129-LIVESCAN-R1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/verification.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	3	Blockchain/Dev/services/api-gateway/src/routes/verification.ts
49	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (5 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 5 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/routes/verification.ts byte-exact incl. leading whitespace (apply mode strict): OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)` [a3i_indent.out: `OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1069-persisted-anchored-input-shape.test.ts fails at the untouched tip (6 failed / 20 run; controls green; assertion reds)` [red_first.json: failed=6 of total=20; red cell(s): ['KS-1129 O1: the live chain-scan reply is shape-checked before it can claim on-chain RED KS-1129 L1: a STRING verified value is not a verified reply', 'KS-1129 O1: the live chain-scan reply is shape-checked before it can claim on-chain RED KS-1129 L2: a tx_sim_ placeholder hash from the live reply is not a hash', 'KS-1129 O1: the live chain-scan reply is shape-checked before it can claim on-chain RED KS-1129 L3: a live height of -1 is not a height', 'KS-1129 O1: the live chain-scan reply is shape-checked before it can claim on-chain RED KS-1129 L4: a live height of 4242.5 is not a height', 'KS-1129 O1: the live chain-scan reply is shape-checked before it can claim on-chain RED KS-1129 L5: a numeric STRING live height is refused, strict as the persisted read (E7)', 'KS-1129 O1: the live chain-scan reply is shape-checked before it can claim on-chain RED KS-1129 L6: a live reply that declares simulated is not on-chain']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1069-persisted-anchored-input-shape.test.ts passes with the product hunk (20 passed / 20 run)` [green_after.json: failed=0 of total=20, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=773 failed=0 | after: total=781 failed=0` · `NEW reds: []` [baseline_suite.json total=773 failed=0; after_suite.json total=781 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +54/-3 test=src/__tests__/ks1069-persisted-anchored-input-shape.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (+5/-3 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts` (+49/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1129-LIVESCAN-R1/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1129-LIVESCAN-R1/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
@@ -603,10 +603,12 @@
           // confirmedAt, ... }. Older code expected j.anchor.* (nested) which
           // never matched, so liveTxHash stayed null and the response always
           // fell through to the persisted document.blockchain stub.
-          if (j.verified) {
-            liveTxHash = j.txHash || j.transactionHash || (j.anchor && j.anchor.txHash) || null;
+          // KS-1129 O1: the live reply gets the three shape guards the persisted read got in KS-1069.
+          if (j.verified === true && !j.simulated) {
+            const liveHash = j.txHash || j.transactionHash || (j.anchor && j.anchor.txHash) || null;
+            liveTxHash = typeof liveHash === 'string' && !/^(tx_sim_|mock_tx_|tx_)/.test(liveHash) ? liveHash : null;
             const blockNum = j.blockNumber ?? j.blockHeight ?? (j.anchor && j.anchor.blockHeight);
-            liveBlockHeight = blockNum != null ? Number(blockNum) : null;
+            liveBlockHeight = typeof blockNum === 'number' && Number.isInteger(blockNum) && blockNum > 0 ? blockNum : null;
             liveConfirmedAt = j.confirmedAt || j.anchoredAt || (j.anchor && j.anchor.confirmedAt) || null;
           }
         }
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts
@@ -258,2 +258,51 @@
   });
+});
+
+// KS-1129 O1: the LIVE chain-scan read (anchoring's reply to GET /api/anchors/verify/:hash) had no shape
+// rule. A truthy verified, any truthy hash and a Number()-coerced height reported on-chain. It now applies
+// the three guards the persisted read above got in KS-1069. Every cell below serves NO persisted blob, so
+// the live reply alone decides the claim.
+async function verifyLive(reply: Record<string, unknown>): Promise<any> {
+  currentBlob = undefined;
+  liveAnchorReply = reply;
+  anchorStoreRows = null;
+  tier1Absent = false;
+  return post();
+}
+
+const LIVE_REAL = { verified: true, txHash: REAL_TX, blockNumber: 4242 } as const;
+const OFF_CHAIN = { verified: false, confidence: 'off-chain-only' } as const;
+
+function claim(body: any): { verified: unknown; confidence: unknown } {
+  return { verified: body.verified, confidence: body.verificationConfidence };
+}
+
+describe('KS-1129 O1: the live chain-scan reply is shape-checked before it can claim on-chain', () => {
+  it('RED KS-1129 L1: a STRING verified value is not a verified reply', async () => {
+    expect(claim(await verifyLive({ ...LIVE_REAL, verified: 'false' }))).toEqual(OFF_CHAIN);
+  });
+  it('RED KS-1129 L2: a tx_sim_ placeholder hash from the live reply is not a hash', async () => {
+    expect(claim(await verifyLive({ ...LIVE_REAL, txHash: 'tx_sim_' + 'c'.repeat(32) }))).toEqual(OFF_CHAIN);
+  });
+  it('RED KS-1129 L3: a live height of -1 is not a height', async () => {
+    expect(claim(await verifyLive({ ...LIVE_REAL, blockNumber: -1 }))).toEqual(OFF_CHAIN);
+  });
+  it('RED KS-1129 L4: a live height of 4242.5 is not a height', async () => {
+    expect(claim(await verifyLive({ ...LIVE_REAL, blockNumber: 4242.5 }))).toEqual(OFF_CHAIN);
+  });
+  it('RED KS-1129 L5: a numeric STRING live height is refused, strict as the persisted read (E7)', async () => {
+    expect(claim(await verifyLive({ ...LIVE_REAL, blockNumber: '4242' }))).toEqual(OFF_CHAIN);
+  });
+  it('RED KS-1129 L6: a live reply that declares simulated is not on-chain', async () => {
+    expect(claim(await verifyLive({ ...LIVE_REAL, simulated: true }))).toEqual(OFF_CHAIN);
+  });
+  it('control KS-1129 C1: a real hash, a positive integer height and verified true still report on-chain, from the live read', async () => {
+    const body = await verifyLive({ ...LIVE_REAL });
+    expect(claim(body)).toEqual({ verified: true, confidence: 'on-chain' });
+    expect({ source: body.blockchain.source, txHash: body.blockchain.txHash, blockHeight: body.blockchain.blockHeight })
+      .toEqual({ source: 'cardano-live', txHash: REAL_TX, blockHeight: 4242 });
+  });
+  it('control KS-1129 C2: simulated false on a real live reply still reports on-chain', async () => {
+    expect(claim(await verifyLive({ ...LIVE_REAL, simulated: false }))).toEqual({ verified: true, confidence: 'on-chain' });
+  });
 });
```
