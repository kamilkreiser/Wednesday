# READY — KS-1626-MOCKBATCH-ANCHORING-1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_anchoring/out.md.checker/patch.diff`** (from `ls` at 04:26 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_anchoring/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_anchoring/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_anchoring/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_anchoring-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in honestAnchor.ts (run 12 vs golden 13 body lines — context, since the change lines are equal), anchorReadback.ts (run 10 vs golden 11 body lines — context, since the change lines are equal) (identical in ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 04:26 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_anchoring/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `5d1be7b06279950e3bfe176c237e5d640eb04581`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/honestAnchor.ts , Blockchain/Dev/services/anchoring/src/anchorReadback.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/honestAnchor.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/services/anchoring/src/honestAnchor.ts
1	1	Blockchain/Dev/services/anchoring/src/anchorReadback.ts
63	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (2 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: honestAnchor.ts anchorReadback.ts`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/honestAnchor.ts`, `Blockchain/Dev/services/anchoring/src/anchorReadback.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/honestAnchor.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/anchorReadback.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts 63 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/honestAnchor.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/anchorReadback.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1626 - the batch mock placeholder is read as a placeholder on the anchoring read paths RED KS-1626 A1 honestTxView reads a mock_batch_tx_ hash as a placeholder', 'KS-1626 - the batch mock placeholder is read as a placeholder on the anchoring read paths RED KS-1626 A2 buildVerifyResponse reads a mock_batch_tx_ hash as a placeholder']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=371 failed=1 | after: total=376 failed=1` · `NEW reds: []` [baseline_suite.json total=371 failed=1; after_suite.json total=376 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/honestAnchor.ts` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts` (+63/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/honestAnchor.ts, Blockchain/Dev/services/anchoring/src/anchorReadback.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `5d1be7b06279950e3bfe176c237e5d640eb04581` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_anchoring/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_anchoring/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/honestAnchor.ts b/Blockchain/Dev/services/anchoring/src/honestAnchor.ts
--- a/Blockchain/Dev/services/anchoring/src/honestAnchor.ts
+++ b/Blockchain/Dev/services/anchoring/src/honestAnchor.ts
@@ -14,8 +14,8 @@
  * the flag can lie (they were written `simulated = false`).
  */
-
-export const FABRICATED_TX_PREFIX = /^(tx_sim_|mock_tx_|tx_)/;
-
+
+export const FABRICATED_TX_PREFIX = /^(tx_sim_|mock_tx_|mock_batch_tx_|tx_)/;
+
 export interface HonestTxView {
   /** Real on-chain hash, or null when the stored hash is a placeholder. */
   txHash: string | null;
diff --git a/Blockchain/Dev/services/anchoring/src/anchorReadback.ts b/Blockchain/Dev/services/anchoring/src/anchorReadback.ts
--- a/Blockchain/Dev/services/anchoring/src/anchorReadback.ts
+++ b/Blockchain/Dev/services/anchoring/src/anchorReadback.ts
@@ -112,7 +112,7 @@
   // dev mock). Never present it as an on-chain claim: the placeholder moves
   // to `simulatedTxRef`, `simulated: true` is machine-readable, and no
   // explorer URL is fabricated for a non-existent tx.
-  const simulated = typeof rawTxHash === 'string' && /^(tx_sim_|mock_tx_|tx_)/.test(rawTxHash);
+  const simulated = typeof rawTxHash === 'string' && /^(tx_sim_|mock_tx_|mock_batch_tx_|tx_)/.test(rawTxHash);
   const txHash = simulated ? null : rawTxHash;
   // KS-726 (#805 review F1): the DB query admits 'submitting' rows, whose
   // transaction the node has NOT acknowledged. `verified: true` alone cannot
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts
@@ -0,0 +1,63 @@
+/**
+ * KS-1626 - the anchoring service's two placeholder tests must read the batch mock's hash as a placeholder.
+ *
+ * The non-production batch mock (index.ts, the batch anchor mock branch) writes `mock_batch_tx_<64 hex>` as a confirmed
+ * anchor's transaction hash. Both placeholder tests on the READ paths - `honestTxView` (honestAnchor.ts, the
+ * anchor-by-id and by-document reads) and `buildVerifyResponse` (anchorReadback.ts, the verify read) - matched
+ * `/^(tx_sim_|mock_tx_|tx_)/`, which does not match `mock_batch_tx_` (it starts `mock_b`, not `mock_t`), so the hash
+ * was presented as an on-chain transaction: `txHash` set, no `simulated` marker, a cardanoscan URL for a transaction
+ * that does not exist (the KS-522 / KS-587 honest-labelling family). A real Cardano hash is 64 hex digits and can
+ * never contain `_`, so the prefix cannot reject a real hash.
+ *
+ * Both functions are pure, so these cells call them directly and boot nothing.
+ */
+
+import { describe, it, expect } from 'vitest';
+
+import { honestTxView, FABRICATED_TX_PREFIX } from '../honestAnchor';
+import { buildVerifyResponse } from '../anchorReadback';
+
+const HASH = 'a1b2c3d4e5f60718293a4b5c6d7e8f901a2b3c4d5e6f70819203a4b5c6d7e8f9';
+const CTX = { hash: HASH, network: 'preview' };
+const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';
+const BATCH_MOCK_TX = 'mock_batch_tx_' + 'c'.repeat(64);
+const OLDER_PLACEHOLDERS = ['tx_sim_' + 'c'.repeat(64), 'mock_tx_' + 'c'.repeat(64), 'tx_' + 'c'.repeat(40)];
+
+describe('KS-1626 - the batch mock placeholder is read as a placeholder on the anchoring read paths', () => {
+  it('RED KS-1626 A1 honestTxView reads a mock_batch_tx_ hash as a placeholder', () => {
+    const view = honestTxView(BATCH_MOCK_TX, false);
+    expect(view.txHash).toBeNull();
+    expect(view.simulated).toBe(true);
+    expect(view.simulatedTxRef).toBe(BATCH_MOCK_TX);
+  });
+
+  it('RED KS-1626 A2 buildVerifyResponse reads a mock_batch_tx_ hash as a placeholder', () => {
+    const body = buildVerifyResponse('db', {}, { transaction_hash: BATCH_MOCK_TX, status: 'confirmed' }, CTX);
+    expect(body.txHash).toBeNull();
+    expect(body.simulated).toBe(true);
+    expect(body.simulatedTxRef).toBe(BATCH_MOCK_TX);
+    expect(body.cardanoScanUrl).toBeNull();
+  });
+
+  it('CONTROL KS-1626 A3 a real 64-hex hash is still read as real by both', () => {
+    expect(honestTxView(REAL_TX, false)).toEqual({ txHash: REAL_TX, simulated: false });
+    const body = buildVerifyResponse('db', {}, { transaction_hash: REAL_TX, status: 'confirmed' }, CTX);
+    expect(body.txHash).toBe(REAL_TX);
+    expect(body.simulated).toBeUndefined();
+    expect(body.cardanoScanUrl).toBe('https://preview.cardanoscan.io/transaction/' + REAL_TX);
+  });
+
+  it('CONTROL KS-1626 A4 the three older placeholder prefixes are still read as placeholders by both', () => {
+    for (const placeholder of OLDER_PLACEHOLDERS) {
+      expect(honestTxView(placeholder, false).simulated).toBe(true);
+      const body = buildVerifyResponse('db', {}, { transaction_hash: placeholder, status: 'confirmed' }, CTX);
+      expect(body.txHash).toBeNull();
+      expect(body.simulated).toBe(true);
+    }
+  });
+
+  it('CONTROL KS-1626 A5 it is a prefix test: the text later in a value does not make it a placeholder', () => {
+    expect(FABRICATED_TX_PREFIX.test('abc_mock_batch_tx_def')).toBe(false);
+    expect(honestTxView('abc_mock_batch_tx_def', false)).toEqual({ txHash: 'abc_mock_batch_tx_def', simulated: false });
+  });
+});
```
