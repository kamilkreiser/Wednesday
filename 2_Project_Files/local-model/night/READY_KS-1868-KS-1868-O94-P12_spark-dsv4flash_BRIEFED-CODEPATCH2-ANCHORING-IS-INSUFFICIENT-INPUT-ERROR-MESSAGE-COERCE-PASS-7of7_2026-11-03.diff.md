# READY — KS-1868-KS-1868-O94-P12 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p12_anchoring_transaction_is_insufficient_input_error_guard_message/out.md.checker/patch.diff`** (from `ls` at 12:56 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p12_anchoring_transaction_is_insufficient_input_error_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p12_anchoring_transaction_is_insufficient_input_error_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p12_anchoring_transaction_is_insufficient_input_error_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p12_anchoring_transaction_is_insufficient_input_error_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 12:56 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p12_anchoring_transaction_is_insufficient_input_error_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `32921f7921c2cdeb87e4361a2976a9e8cfd6beac`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/cardano/transaction.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/cardano/transaction.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/anchoring/src/cardano/transaction.ts
47	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: transaction.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/cardano/transaction.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/cardano/transaction.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts 47 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/cardano/transaction.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1868 isInsufficientInputError reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value is not recognised, and does not throw', 'KS-1868 isInsufficientInputError reads the thrown value safely RED ks1868 R2 an Error whose message getter throws is not recognised, and does not throw']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=817 failed=1 | after: total=822 failed=1` · `NEW reds: []` [baseline_suite.json total=817 failed=1; after_suite.json total=822 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/cardano/transaction.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts` (+47/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/cardano/transaction.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `32921f7921c2cdeb87e4361a2976a9e8cfd6beac` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p12_anchoring_transaction_is_insufficient_input_error_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o94_p12_anchoring_transaction_is_insufficient_input_error_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p12_anchoring_transaction_is_insufficient_input_error_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/cardano/transaction.ts b/Blockchain/Dev/services/anchoring/src/cardano/transaction.ts
--- a/Blockchain/Dev/services/anchoring/src/cardano/transaction.ts
+++ b/Blockchain/Dev/services/anchoring/src/cardano/transaction.ts
@@ -57,5 +57,11 @@
  * nothing left to select, says "Insufficient input in transaction".
  */
 export function isInsufficientInputError(err: unknown): boolean {
-  return /UTxO Balance Insufficient|Insufficient input in transaction/i.test(String((err as { message?: unknown })?.message ?? err));
+  let text: string;
+  try {
+    text = String((err as { message?: unknown })?.message ?? err);
+  } catch {
+    return false;
+  }
+  return /UTxO Balance Insufficient|Insufficient input in transaction/i.test(text);
 }
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts
@@ -0,0 +1,47 @@
+import { describe, it, expect } from 'vitest';
+
+// KS-1868: isInsufficientInputError (src/cardano/transaction.ts) recognises the two texts the transaction builder throws when the offered
+// coins cannot pay the fee. It reads `String((err as { message?: unknown })?.message ?? err)` unguarded. When the thrown value cannot be read
+// (a revoked Proxy throws on the message read and again on `String(err)`; an Error whose `message` getter throws, throws on the first read) the
+// predicate THROWS from inside the caller's catch, where an ordinary error gets true or false. An unreadable value is not that failure: false.
+import { isInsufficientInputError } from '../cardano/transaction';
+
+/** The predicate's answer, or the string 'rejected' when it throws (an assertion can then fail on it). */
+function check(value: unknown): unknown {
+  try {
+    return isInsufficientInputError(value);
+  } catch {
+    return 'rejected';
+  }
+}
+
+describe('KS-1868 isInsufficientInputError reads the thrown value safely', () => {
+  it('control ks1868 C1 an Error carrying the coin-selection text is recognised', () => {
+    expect(check(new Error('UTxO Balance Insufficient'))).toBe(true);
+  });
+
+  it('control ks1868 C2 a thrown plain string carrying the forced-outpoint text is recognised', () => {
+    expect(check('Insufficient input in transaction')).toBe(true);
+  });
+
+  it('control ks1868 C3 an unrelated Error is not recognised', () => {
+    expect(check(new Error('something else'))).toBe(false);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value is not recognised, and does not throw', () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    expect(check(proxy)).toBe(false);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is not recognised, and does not throw', () => {
+    const hostile = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    expect(check(hostile)).toBe(false);
+  });
+});
```
