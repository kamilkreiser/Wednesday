# READY — KS-1868-KS-1868-O94-P18 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p18_billing_routes_send_classified_billing_error_guard_message/out.md.checker/patch.diff`** (from `ls` at 13:21 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p18_billing_routes_send_classified_billing_error_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p18_billing_routes_send_classified_billing_error_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p18_billing_routes_send_classified_billing_error_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p18_billing_routes_send_classified_billing_error_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:21 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p18_billing_routes_send_classified_billing_error_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `32921f7921c2cdeb87e4361a2976a9e8cfd6beac`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/billing/src/routes/billing.ts } + { Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/billing/src/routes/billing.ts` (product) and `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	1	Blockchain/Dev/services/billing/src/routes/billing.ts
75	0	Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (6 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: billing.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/billing/src/routes/billing.ts`; test(s): `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/billing/src/routes/billing.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts 75 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/billing/src/routes/billing.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1868 sendClassifiedBillingError reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value is unclassified (false, nothing written)', 'KS-1868 sendClassifiedBillingError reads the thrown value safely RED ks1868 R2 an Error whose message getter throws is unclassified (false, nothing written)']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=377 failed=1 | after: total=382 failed=0` · `NEW reds: []` [baseline_suite.json total=377 failed=1; after_suite.json total=382 failed=0]
- A6 [verbatim]: `PASS A6 whole services/billing suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/billing: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/billing/src/routes/billing.ts` (+6/-1 per numstat.out) and the test file `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts` (+75/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/billing/src/routes/billing.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `32921f7921c2cdeb87e4361a2976a9e8cfd6beac` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p18_billing_routes_send_classified_billing_error_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o94_p18_billing_routes_send_classified_billing_error_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p18_billing_routes_send_classified_billing_error_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/billing/src/routes/billing.ts b/Blockchain/Dev/services/billing/src/routes/billing.ts
--- a/Blockchain/Dev/services/billing/src/routes/billing.ts
+++ b/Blockchain/Dev/services/billing/src/routes/billing.ts
@@ -54,7 +54,12 @@
   notFoundMessage: string,
   invalidRequestMessage?: string,
 ): boolean {
-  const msg = error instanceof Error ? error.message : String(error);
+  let msg: string;
+  try {
+    msg = error instanceof Error ? error.message : String(error);
+  } catch {
+    return false;
+  }
   // KS-144: Stripe-config (invalid/missing key) is a provider-unconfigured outage, not a server fault.
   // KS-445: `Neither apiKey` is stripe-node's constructor throw when the key env var is set but empty.
   if (/Invalid API Key|No API key provided|Neither apiKey|not configured/i.test(msg)) {
diff --git a/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts
@@ -0,0 +1,75 @@
+import { describe, it, expect } from 'vitest';
+import type { Response } from 'express';
+
+// KS-1868: sendClassifiedBillingError (src/routes/billing.ts) classifies a Stripe/provider error into a 503/404/400 and answers true, or answers
+// false for an unclassified error so the route's own catch sends its 500. Its first statement reads
+// `error instanceof Error ? error.message : String(error)` unguarded. When the thrown value cannot be read (a revoked Proxy throws on `instanceof`;
+// an Error whose `message` getter throws, throws on `.message`) the classifier THROWS from inside the route's catch, so the route's 500 is never
+// sent. An unreadable value is unclassified: false, nothing written. Harness: the ks431 classifier suite (the same Response double).
+import { sendClassifiedBillingError } from '../routes/billing';
+
+type Captured = Response & { statusCode?: number; body?: unknown };
+
+function mockRes(): Captured {
+  const res: Partial<Response> & { statusCode?: number; body?: unknown } = {};
+  res.status = ((code: number) => {
+    res.statusCode = code;
+    return res as Response;
+  }) as Response['status'];
+  res.json = ((payload: unknown) => {
+    res.body = payload;
+    return res as Response;
+  }) as Response['json'];
+  return res as Captured;
+}
+
+/** The classifier's answer and the response it wrote; the string 'rejected' as the answer when it throws (an assertion can then fail on it). */
+function classify(value: unknown): { answer: unknown; res: Captured } {
+  const res = mockRes();
+  try {
+    return { answer: sendClassifiedBillingError(value, res, 'Customer not found'), res };
+  } catch {
+    return { answer: 'rejected', res };
+  }
+}
+
+describe('KS-1868 sendClassifiedBillingError reads the thrown value safely', () => {
+  it('control ks1868 C1 an unconfigured-provider message is still a 503', () => {
+    const { answer, res } = classify(new Error('Invalid API Key provided'));
+    expect(answer).toBe(true);
+    expect(res.statusCode).toBe(503);
+  });
+
+  it('control ks1868 C2 a "No such" message is still a 404', () => {
+    const { answer, res } = classify(new Error('No such customer: cus_x'));
+    expect(answer).toBe(true);
+    expect(res.statusCode).toBe(404);
+  });
+
+  it('control ks1868 C3 a provider 500 is still unclassified (false, nothing written)', () => {
+    const { answer, res } = classify(Object.assign(new Error('boom'), { statusCode: 500 }));
+    expect(answer).toBe(false);
+    expect(res.statusCode).toBeUndefined();
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value is unclassified (false, nothing written)', () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    const { answer, res } = classify(proxy);
+    expect(answer).toBe(false);
+    expect(res.statusCode).toBeUndefined();
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is unclassified (false, nothing written)', () => {
+    const hostile = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const { answer, res } = classify(hostile);
+    expect(answer).toBe(false);
+    expect(res.statusCode).toBeUndefined();
+  });
+});
```
