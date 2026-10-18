# READY — KS-1626-MOCKBATCH-ORIGINATE-1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_originate/out.md.checker/patch.diff`** (from `ls` at 04:26 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_originate/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_originate/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_originate/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_originate/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_originate-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 04:26 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_originate/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `5d1be7b06279950e3bfe176c237e5d640eb04581`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/services/anchorHonesty.ts , Blockchain/Dev/services/originate/src/routes/verification.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/anchorHonesty.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/originate/src/services/anchorHonesty.ts
2	2	Blockchain/Dev/services/originate/src/routes/verification.ts
103	0	Blockchain/Dev/services/originate/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (2 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: anchorHonesty.ts verification.ts`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/services/anchorHonesty.ts`, `Blockchain/Dev/services/originate/src/routes/verification.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/services/anchorHonesty.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/routes/verification.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts 103 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/anchorHonesty.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/routes/verification.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1626 - the batch mock placeholder is read as a placeholder in originate RED KS-1626 O1 anchorHonesty reads a mock_batch_tx_ hash as a placeholder', 'KS-1626 - the batch mock placeholder is read as a placeholder in originate RED KS-1626 O2 presentBlockchainHonestly reads a mock_batch_tx_ txHash as a placeholder']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1400 failed=0 | after: total=1405 failed=0` · `NEW reds: []` [baseline_suite.json total=1400 failed=0; after_suite.json total=1405 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/anchorHonesty.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts` (+103/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/originate/src/services/anchorHonesty.ts, Blockchain/Dev/services/originate/src/routes/verification.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `5d1be7b06279950e3bfe176c237e5d640eb04581` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_originate/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1626_originate/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/services/anchorHonesty.ts b/Blockchain/Dev/services/originate/src/services/anchorHonesty.ts
index 29f5574d1..3a2339d90 100644
--- a/Blockchain/Dev/services/originate/src/services/anchorHonesty.ts
+++ b/Blockchain/Dev/services/originate/src/services/anchorHonesty.ts
@@ -27,5 +27,5 @@
 /** Placeholder tx prefixes. Mirrors services/anchoring/src/honestAnchor.ts. */
-export const FABRICATED_TX_PREFIX = /^(tx_sim_|mock_tx_|tx_)/;
-
+export const FABRICATED_TX_PREFIX = /^(tx_sim_|mock_tx_|mock_batch_tx_|tx_)/;
+
 /**
  * A row/payload counts as simulated when its flag says so OR its hash carries
diff --git a/Blockchain/Dev/services/originate/src/routes/verification.ts b/Blockchain/Dev/services/originate/src/routes/verification.ts
index 980d71e2d..94773b51e 100644
--- a/Blockchain/Dev/services/originate/src/routes/verification.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verification.ts
@@ -49,8 +49,8 @@
 // nulled (the placeholder moves to `simulatedTxRef`), `anchored` flips false,
 // and a machine-readable `simulated: true` marker is set (also surfaced
 // top-level by the response builders).
-const FABRICATED_TXHASH_RE = /^(tx_sim_|mock_tx_|tx_)/;
-
+const FABRICATED_TXHASH_RE = /^(tx_sim_|mock_tx_|mock_batch_tx_|tx_)/;
+
 export function presentBlockchainHonestly(blob: unknown): unknown {
   if (!blob || typeof blob !== 'object') return blob;
   const b = blob as Record<string, unknown>;
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts
new file mode 100644
index 000000000..538adc2a4
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1626-batch-mock-placeholder-is-read-as-a-placeholder.test.ts
@@ -0,0 +1,103 @@
+/**
+ * KS-1626 - originate's two placeholder tests must read the batch mock's hash as a placeholder.
+ *
+ * The non-production batch mock in the anchoring service writes `mock_batch_tx_<64 hex>` as a confirmed anchor's
+ * transaction hash. Originate's two placeholder tests matched `/^(tx_sim_|mock_tx_|tx_)/`, which does not match it
+ * (`mock_b`, not `mock_t`): `FABRICATED_TX_PREFIX` (services/anchorHonesty.ts, used by isSimulatedAnchor,
+ * simulatedFieldsFromAnchor and composeHonestBlockchainBlob) and `FABRICATED_TXHASH_RE` (routes/verification.ts, used
+ * by presentBlockchainHonestly). The hash was therefore served as an on-chain transaction (the KS-522 / KS-587
+ * honest-labelling family). A real Cardano hash is 64 hex digits and can never contain `_`.
+ *
+ * Every function called here is pure; the module mocks below are the neighbouring KS-563 test's, so loading
+ * routes/verification touches no database.
+ */
+
+process.env.NODE_ENV = 'development';
+// routes/verification imports ../db (via the logger), whose config demands
+// DATABASE_URL at module load - same shim the other unit suites here use.
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw },
+  getTenantManager: () => null,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
+    queryWithTenantGuc: jest.fn(),
+  }),
+);
+
+// The lineage walks are not under test here.
+jest.mock('../repositories/documentRepo', () => ({
+  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
+  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
+  MAX_LINEAGE_DEPTH: 10,
+}));
+
+import {
+  FABRICATED_TX_PREFIX,
+  composeHonestBlockchainBlob,
+  isSimulatedAnchor,
+  simulatedFieldsFromAnchor,
+} from '../services/anchorHonesty';
+import { presentBlockchainHonestly } from '../routes/verification';
+
+const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';
+const BATCH_MOCK_TX = 'mock_batch_tx_' + 'c'.repeat(64);
+const OLDER_PLACEHOLDERS = ['tx_sim_' + 'c'.repeat(64), 'mock_tx_' + 'c'.repeat(64), 'tx_' + 'c'.repeat(40)];
+
+describe('KS-1626 - the batch mock placeholder is read as a placeholder in originate', () => {
+  it('RED KS-1626 O1 anchorHonesty reads a mock_batch_tx_ hash as a placeholder', () => {
+    expect(FABRICATED_TX_PREFIX.test(BATCH_MOCK_TX)).toBe(true);
+    expect(isSimulatedAnchor(BATCH_MOCK_TX, false)).toBe(true);
+    expect(simulatedFieldsFromAnchor({ transactionHash: BATCH_MOCK_TX })).toEqual({
+      simulated: true,
+      simulatedTxRef: BATCH_MOCK_TX,
+    });
+    const blob = composeHonestBlockchainBlob({ txHash: BATCH_MOCK_TX, status: 'confirmed' }) as Record<string, unknown>;
+    expect(blob.txHash).toBeNull();
+    expect(blob.simulated).toBe(true);
+    expect(blob.simulatedTxRef).toBe(BATCH_MOCK_TX);
+  });
+
+  it('RED KS-1626 O2 presentBlockchainHonestly reads a mock_batch_tx_ txHash as a placeholder', () => {
+    const out = presentBlockchainHonestly({ txHash: BATCH_MOCK_TX, anchored: true, status: 'confirmed', blockHeight: 4242 }) as Record<string, unknown>;
+    expect(out.simulated).toBe(true);
+    expect(out.anchored).toBe(false);
+    expect(out.txHash).toBeNull();
+    expect(out.simulatedTxRef).toBe(BATCH_MOCK_TX);
+  });
+
+  it('CONTROL KS-1626 O3 a real 64-hex hash is still read as real by both', () => {
+    expect(FABRICATED_TX_PREFIX.test(REAL_TX)).toBe(false);
+    expect(isSimulatedAnchor(REAL_TX, false)).toBe(false);
+    expect(simulatedFieldsFromAnchor({ transactionHash: REAL_TX })).toEqual({});
+    const blob = { txHash: REAL_TX, anchored: true, status: 'confirmed', blockHeight: 4242 };
+    expect(composeHonestBlockchainBlob(blob)).toBe(blob);
+    expect(presentBlockchainHonestly(blob)).toBe(blob);
+  });
+
+  it('CONTROL KS-1626 O4 the three older placeholder prefixes are still read as placeholders by both', () => {
+    for (const placeholder of OLDER_PLACEHOLDERS) {
+      expect(isSimulatedAnchor(placeholder, false)).toBe(true);
+      const out = presentBlockchainHonestly({ txHash: placeholder, anchored: true }) as Record<string, unknown>;
+      expect(out.simulated).toBe(true);
+      expect(out.txHash).toBeNull();
+    }
+  });
+
+  it('CONTROL KS-1626 O5 it is a prefix test: the text later in a value does not make it a placeholder', () => {
+    expect(FABRICATED_TX_PREFIX.test('abc_mock_batch_tx_def')).toBe(false);
+    const blob = { txHash: 'abc_mock_batch_tx_def', anchored: true };
+    expect(presentBlockchainHonestly(blob)).toBe(blob);
+  });
+});
```
