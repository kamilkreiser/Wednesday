# READY — KS-1868-KS-1868-O94-P10 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p10_anchoring_thread_mint_request_classify_thread_mint_error_guard_message/out.md.checker/patch.diff`** (from `ls` at 12:43 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p10_anchoring_thread_mint_request_classify_thread_mint_error_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p10_anchoring_thread_mint_request_classify_thread_mint_error_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [section 1: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/anchoring/src/threadMintRequest.ts b/Blockchain/Dev/services/anchoring/src/threadMintRequest.ts' vs '+++ --- a/Blockchain/Dev/services/anchoring/src/threadMintRequest.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/anchoring/src/threadMintRequest.ts: FUZZY — applies only with -C1 (one context line): ; strict rc=1 lenient rc=1] [section 2: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts' vs '+++ new file mode 100644' — the model paired the product file's --- with another file's +++ (task.md 2d)]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/anchoring/src/threadMintRequest.ts): `error: patch failed: Blockchain/Dev/services/anchoring/src/threadMintRequest.ts:74` (apply with the options recorded in section_<k>.opts; the raise seat states which); the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p10_anchoring_thread_mint_request_classify_thread_mint_error_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p10_anchoring_thread_mint_request_classify_thread_mint_error_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 12:43 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p10_anchoring_thread_mint_request_classify_thread_mint_error_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `32921f7921c2cdeb87e4361a2976a9e8cfd6beac`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/threadMintRequest.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/threadMintRequest.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	2	Blockchain/Dev/services/anchoring/src/threadMintRequest.ts
47	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: threadMintRequest.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/threadMintRequest.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/threadMintRequest.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts 47 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/threadMintRequest.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace -C1`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/anchoring/src/threadMintRequest.ts:74`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 classifyThreadMintError reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value is unclassified (null)', 'KS-1868 classifyThreadMintError reads the thrown value safely RED ks1868 R2 an Error whose message getter throws is unclassified (null)']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=817 failed=1 | after: total=821 failed=1` · `NEW reds: []` [baseline_suite.json total=817 failed=1; after_suite.json total=821 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=accommodated (see the A2 line)`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/threadMintRequest.ts` (+8/-2 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts` (+47/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/threadMintRequest.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace -C1`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `32921f7921c2cdeb87e4361a2976a9e8cfd6beac` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p10_anchoring_thread_mint_request_classify_thread_mint_error_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o94_p10_anchoring_thread_mint_request_classify_thread_mint_error_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p10_anchoring_thread_mint_request_classify_thread_mint_error_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/threadMintRequest.ts b/Blockchain/Dev/services/anchoring/src/threadMintRequest.ts
--- a/Blockchain/Dev/services/anchoring/src/threadMintRequest.ts
+++ b/Blockchain/Dev/services/anchoring/src/threadMintRequest.ts
@@ -74,5 +74,11 @@
  */
 export function classifyThreadMintError(error: unknown): ClassifiedMintError | null {
   const err = error as { message?: unknown; code?: unknown };
-  const msg = typeof err?.message === 'string' ? err.message : String(error);
-  const errCode = typeof err?.code === 'string' ? err.code : '';
+  let msg: string;
+  let errCode: string;
+  try {
+    msg = typeof err?.message === 'string' ? err.message : String(error);
+    errCode = typeof err?.code === 'string' ? err.code : '';
+  } catch {
+    return null;
+  }
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts
@@ -0,0 +1,47 @@
+import { describe, it, expect } from 'vitest';
+
+// KS-1868: classifyThreadMintError (src/threadMintRequest.ts) maps what mintAndLock threw to an honest 400/503, or null when the failure is
+// unclassified (the route then keeps its 500). It reads `err?.message` and `err?.code` unguarded. When the thrown value cannot be read (a revoked
+// Proxy throws on both reads; an Error whose `message` getter throws, throws on the first) classifyThreadMintError THROWS from inside the
+// route's catch, where an ordinary Error is classified. An unreadable value is an unclassified failure: null, the route's 500.
+import { classifyThreadMintError } from '../threadMintRequest';
+
+/** The classification, or the string 'rejected' when the function throws (an assertion can then fail on it). */
+function classify(value: unknown): unknown {
+  try {
+    return classifyThreadMintError(value);
+  } catch {
+    return 'rejected';
+  }
+}
+
+describe('KS-1868 classifyThreadMintError reads the thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error naming a refused connection is still a 503', () => {
+    expect(classify(new Error('connect ECONNREFUSED 127.0.0.1:443'))).toEqual({
+      status: 503,
+      code: 'SERVICE_UNAVAILABLE',
+      message: 'Cardano network provider unreachable',
+    });
+  });
+
+  it('control ks1868 C2 an unclassified thrown plain string is still null', () => {
+    expect(classify('something odd happened')).toBeNull();
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value is unclassified (null)', () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    expect(classify(proxy)).toBeNull();
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is unclassified (null)', () => {
+    const hostile = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    expect(classify(hostile)).toBeNull();
+  });
+});
```
