# READY — KS-1485-MOCKBATCHPREFIX-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1485_p1/out.md.checker/patch.diff`** (from `ls` at 03:01 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1485_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1485_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1485_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in anchorStateSync.ts (run 6 vs golden 9 body lines — context, since the change lines are equal) (identical in ks1485-authoritative-tx-hash-rejects-the-batch-mock-prefix.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 03:01 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1485_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `385fc288fae831f2ca15b9d091c844f33285b784`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/services/anchorStateSync.ts , Blockchain/Dev/services/originate/src/__tests__/ks1485-authoritative-tx-hash-rejects-the-batch-mock-prefix.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1485-authoritative-tx-hash-rejects-the-batch-mock-prefix.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/originate/src/services/anchorStateSync.ts
61	0	Blockchain/Dev/services/originate/src/__tests__/ks1485-authoritative-tx-hash-rejects-the-batch-mock-prefix.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/services/anchorStateSync.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1485-authoritative-tx-hash-rejects-the-batch-mock-prefix.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1485-authoritative-tx-hash-rejects-the-batch-mock-prefix.test.ts fails at the untouched tip (3 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=3 of total=7; red cell(s): ['KS-1485 - authoritativeTxHash and the batch mock placeholder RED KS-1485 a mock_batch_tx_ txHash is not an authoritative hash', 'KS-1485 - authoritativeTxHash and the batch mock placeholder RED KS-1485 a mock_batch_tx_ transactionHash is not an authoritative hash', 'KS-1485 - authoritativeTxHash and the batch mock placeholder RED KS-1485 a mock_batch_tx_ transactionId is not an authoritative hash']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1485-authoritative-tx-hash-rejects-the-batch-mock-prefix.test.ts passes with the product hunk (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1393 failed=0 | after: total=1400 failed=0` · `NEW reds: []` [baseline_suite.json total=1393 failed=0; after_suite.json total=1400 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +62/-1 test=src/__tests__/ks1485-authoritative-tx-hash-rejects-the-batch-mock-prefix.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1485-authoritative-tx-hash-rejects-the-batch-mock-prefix.test.ts` (+61/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `385fc288fae831f2ca15b9d091c844f33285b784` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1485_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1485_p1/KS-1485.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1485_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/services/anchorStateSync.ts
+++ b/Blockchain/Dev/services/originate/src/services/anchorStateSync.ts
@@ -79,5 +79,5 @@ export function authoritativeTxHash(anchor: AnchorReadState): string | null {
   const raw = anchor.transactionHash || anchor.txHash || anchor.transactionId;
   if (typeof raw !== 'string' || raw.length === 0) return null;
-  if (raw.startsWith('tx_') || raw.startsWith('mock_tx_')) return null;
+  if (raw.startsWith('tx_') || raw.startsWith('mock_tx_') || raw.startsWith('mock_batch_tx_')) return null;
   return raw;
 }
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1485-authoritative-tx-hash-rejects-the-batch-mock-prefix.test.ts
@@ -0,0 +1,61 @@
+/**
+ * KS-1485 - authoritativeTxHash rejects the batch mock's placeholder prefix.
+ *
+ * `authoritativeTxHash` (anchorStateSync.ts) returns the tx hash of an anchor read, or null for a legacy dev-mode
+ * placeholder, which is not an on-chain transaction (the KS-522 honest-labelling family). It rejected `tx_` and
+ * `mock_tx_` only, so the non-production batch mock's `mock_batch_tx_...` (anchoring/src/index.ts) passed as a real hash
+ * in all three decisions that call it. A real Cardano transaction hash is hex and can never contain `_`, so the prefix
+ * cannot reject a real hash.
+ *
+ * The function is pure, so these cells call it directly. The module's own imports are mocked, as in the neighbouring
+ * KS-1158 R1 test, so loading it touches no database and writes no log.
+ */
+
+jest.mock('../repositories/documentRepo', () => ({
+  getDocument: jest.fn(),
+  updateDocument: jest.fn(),
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import { authoritativeTxHash } from '../services/anchorStateSync';
+
+const REAL_TX = '9c2e4a6b8d0f1e3a5c7b9d2f4a6c8e0b1d3f5a7c9e2b4d6f8a0c2e4b6d8f0a1c';
+const BATCH_MOCK_TX = 'mock_batch_tx_0f3a9c1d5e7b2a4c';
+
+describe('KS-1485 - authoritativeTxHash and the batch mock placeholder', () => {
+  it('RED KS-1485 a mock_batch_tx_ txHash is not an authoritative hash', () => {
+    expect(authoritativeTxHash({ txHash: BATCH_MOCK_TX })).toBeNull();
+  });
+
+  it('RED KS-1485 a mock_batch_tx_ transactionHash is not an authoritative hash', () => {
+    expect(authoritativeTxHash({ transactionHash: BATCH_MOCK_TX })).toBeNull();
+  });
+
+  it('RED KS-1485 a mock_batch_tx_ transactionId is not an authoritative hash', () => {
+    expect(authoritativeTxHash({ transactionId: BATCH_MOCK_TX })).toBeNull();
+  });
+
+  it('CONTROL a real hex hash is returned unchanged from each of the three fields', () => {
+    expect(authoritativeTxHash({ txHash: REAL_TX })).toBe(REAL_TX);
+    expect(authoritativeTxHash({ transactionHash: REAL_TX })).toBe(REAL_TX);
+    expect(authoritativeTxHash({ transactionId: REAL_TX })).toBe(REAL_TX);
+  });
+
+  it('CONTROL the two older placeholder prefixes are still rejected', () => {
+    expect(authoritativeTxHash({ txHash: 'tx_sim_0f3a9c1d5e7b2a4c' })).toBeNull();
+    expect(authoritativeTxHash({ txHash: 'mock_tx_0f3a9c1d5e7b2a4c' })).toBeNull();
+  });
+
+  it('CONTROL absent, null and empty fields give null', () => {
+    expect(authoritativeTxHash({})).toBeNull();
+    expect(authoritativeTxHash({ txHash: null, transactionHash: null, transactionId: null })).toBeNull();
+    expect(authoritativeTxHash({ txHash: '' })).toBeNull();
+  });
+
+  it('CONTROL it is a prefix test, not a substring test: the text later in a value does not reject it', () => {
+    expect(authoritativeTxHash({ txHash: 'abc_mock_batch_tx_def' })).toBe('abc_mock_batch_tx_def');
+  });
+});
```
