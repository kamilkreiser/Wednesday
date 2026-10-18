# READY — KS-1628-READBACKPREFIXEXPORT-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_anchoring/out.md.checker/patch.diff`** (from `ls` at 07:16 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_anchoring/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_anchoring/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1628_anchoring/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 07:16 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_anchoring/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/anchoring/src/anchorReadback.ts , Blockchain/Dev/services/anchoring/src/__tests__/ks1628-verify-response-uses-the-exported-placeholder-prefix.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/anchorReadback.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1628-verify-response-uses-the-exported-placeholder-prefix.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	1	Blockchain/Dev/services/anchoring/src/anchorReadback.ts
52	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1628-verify-response-uses-the-exported-placeholder-prefix.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/anchoring/src/anchorReadback.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/anchorReadback.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1628-verify-response-uses-the-exported-placeholder-prefix.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1628-verify-response-uses-the-exported-placeholder-prefix.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1628 - buildVerifyResponse reads the placeholder test from the exported FABRICATED_TX_PREFIX RED KS-1628 P1 a hash the exported prefix matches is read as a placeholder', 'KS-1628 - buildVerifyResponse reads the placeholder test from the exported FABRICATED_TX_PREFIX RED KS-1628 P2 a hash the exported prefix does not match is read as real, whatever else it starts with']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1628-verify-response-uses-the-exported-placeholder-prefix.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=376 failed=1 | after: total=380 failed=1` · `NEW reds: []` [baseline_suite.json total=376 failed=1; after_suite.json total=380 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +54/-1 test=src/__tests__/ks1628-verify-response-uses-the-exported-placeholder-prefix.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/anchorReadback.ts` (+2/-1 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1628-verify-response-uses-the-exported-placeholder-prefix.test.ts` (+52/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_anchoring/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_anchoring/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/anchorReadback.ts b/Blockchain/Dev/services/anchoring/src/anchorReadback.ts
index 90a4b693b..48f46d098 100644
--- a/Blockchain/Dev/services/anchoring/src/anchorReadback.ts
+++ b/Blockchain/Dev/services/anchoring/src/anchorReadback.ts
@@ -27,2 +27,3 @@
 import { IDENTITY_FIELDS } from './anchorSchema';
+import { FABRICATED_TX_PREFIX } from './honestAnchor';
 import { deriveVerifyAcceptance } from './verifyAnchorStatus';
@@ -114,3 +115,3 @@
   // explorer URL is fabricated for a non-existent tx.
-  const simulated = typeof rawTxHash === 'string' && /^(tx_sim_|mock_tx_|mock_batch_tx_|tx_)/.test(rawTxHash);
+  const simulated = typeof rawTxHash === 'string' && FABRICATED_TX_PREFIX.test(rawTxHash);
   const txHash = simulated ? null : rawTxHash;
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1628-verify-response-uses-the-exported-placeholder-prefix.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1628-verify-response-uses-the-exported-placeholder-prefix.test.ts
new file mode 100644
index 000000000..cbf14cbfb
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1628-verify-response-uses-the-exported-placeholder-prefix.test.ts
@@ -0,0 +1,52 @@
+/**
+ * KS-1628 item 3 - buildVerifyResponse (anchorReadback.ts) must take its placeholder test from the ONE exported
+ * FABRICATED_TX_PREFIX in honestAnchor.ts, not keep its own copy of the regex.
+ *
+ * KS-1626 had to edit the same alternation in five places because this file carried an inline copy of the regex that
+ * honestAnchor.ts already exports; the next prefix would be missed again the same way. These cells replace the export
+ * with a prefix NOTHING else uses (`zz1628_`), so they pass only when buildVerifyResponse reads the export:
+ *  - a hash that starts `zz1628_` must be read as a placeholder (an inline copy does not know the prefix);
+ *  - a `tx_sim_` hash must now be read as real (an inline copy still calls it a placeholder).
+ * Controls: a real 64-hex hash is read as real, and a row with no hash carries no `simulated` marker.
+ * buildVerifyResponse is pure, so nothing is booted.
+ */
+
+import { describe, it, expect, vi } from 'vitest';
+
+vi.mock('../honestAnchor', () => ({ FABRICATED_TX_PREFIX: /^zz1628_/ }));
+
+import { buildVerifyResponse } from '../anchorReadback';
+
+const HASH = 'a1b2c3d4e5f60718293a4b5c6d7e8f901a2b3c4d5e6f70819203a4b5c6d7e8f9';
+const CTX = { hash: HASH, network: 'preview' };
+const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';
+const EXPORTED_PLACEHOLDER = 'zz1628_' + 'c'.repeat(64);
+const OLD_INLINE_PLACEHOLDER = 'tx_sim_' + 'c'.repeat(64);
+
+describe('KS-1628 - buildVerifyResponse reads the placeholder test from the exported FABRICATED_TX_PREFIX', () => {
+  it('RED KS-1628 P1 a hash the exported prefix matches is read as a placeholder', () => {
+    const body = buildVerifyResponse('db', {}, { transaction_hash: EXPORTED_PLACEHOLDER, status: 'confirmed' }, CTX);
+    expect(body.txHash).toBeNull();
+    expect(body.simulated).toBe(true);
+    expect(body.simulatedTxRef).toBe(EXPORTED_PLACEHOLDER);
+    expect(body.cardanoScanUrl).toBeNull();
+  });
+
+  it('RED KS-1628 P2 a hash the exported prefix does not match is read as real, whatever else it starts with', () => {
+    const body = buildVerifyResponse('db', {}, { transaction_hash: OLD_INLINE_PLACEHOLDER, status: 'confirmed' }, CTX);
+    expect(body.txHash).toBe(OLD_INLINE_PLACEHOLDER);
+    expect(body.simulated).toBeUndefined();
+  });
+
+  it('CONTROL KS-1628 P3 a real 64-hex hash is still read as real and gets its explorer link', () => {
+    const body = buildVerifyResponse('db', {}, { transaction_hash: REAL_TX, status: 'confirmed' }, CTX);
+    expect(body.txHash).toBe(REAL_TX);
+    expect(body.simulated).toBeUndefined();
+    expect(body.cardanoScanUrl).toBe('https://preview.cardanoscan.io/transaction/' + REAL_TX);
+  });
+
+  it('CONTROL KS-1628 P4 a row with no hash carries no simulated marker', () => {
+    const body = buildVerifyResponse('db', {}, { status: 'confirmed' }, CTX);
+    expect(body.simulated).toBeUndefined();
+  });
+});
```
