# READY — KS-1868-KS-1868-O94-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p3_timestamping_tsa_submit_request_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 12:00 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p3_timestamping_tsa_submit_request_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p3_timestamping_tsa_submit_request_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p3_timestamping_tsa_submit_request_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p3_timestamping_tsa_submit_request_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 12:00 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p3_timestamping_tsa_submit_request_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `c6f4cc2f17a3999bd568b91ec6b55eebe58aa603`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts } + { Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts` (product) and `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
12	2	Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts
67	0	Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (12 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: rfc3161-client.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts`; test(s): `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts 12 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts 67 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1868 submitTimestampRequest reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value gives a failed result with a constant reason', 'KS-1868 submitTimestampRequest reads the thrown value safely RED ks1868 R2 an Error whose message getter throws gives a failed result with a constant reason', 'KS-1868 submitTimestampRequest reads the thrown value safely RED ks1868 R3 an Error whose message is a Symbol gives a failed result carrying its text']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=105 failed=3 | after: total=110 failed=0` · `NEW reds: []` [baseline_suite.json total=105 failed=3; after_suite.json total=110 failed=0]
- A6 [verbatim]: `PASS A6 whole services/timestamping suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/timestamping: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts` (+12/-2 per numstat.out) and the test file `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts` (+67/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `c6f4cc2f17a3999bd568b91ec6b55eebe58aa603` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p3_timestamping_tsa_submit_request_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o94_p3_timestamping_tsa_submit_request_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p3_timestamping_tsa_submit_request_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts b/Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts
--- a/Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts
+++ b/Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts
@@ -167,7 +167,17 @@
     // A timeout arrives here as a TimeoutError/AbortError. Naming it explicitly
     // matters operationally: "TSA request failed: The operation was aborted"
     // reads like a bug in our code, when it is the deadline doing its job.
-    if (err?.name === 'TimeoutError' || err?.name === 'AbortError') {
+    let timedOut = false;
+    let reason: string | null | undefined;
+    try {
+      timedOut = err?.name === 'TimeoutError' || err?.name === 'AbortError';
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      timedOut = false;
+      reason = 'unreadable thrown value';
+    }
+    if (timedOut) {
       return {
         success: false,
         error: `TSA request timed out after ${TSA_REQUEST_TIMEOUT_MS}ms (${tsaUrl})`,
@@ -175,7 +185,7 @@
     }
     return {
       success: false,
-      error: `TSA request failed: ${err?.message}`,
+      error: `TSA request failed: ${reason}`,
     };
   }
 }
diff --git a/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts
@@ -0,0 +1,67 @@
+import { describe, it, expect, vi, afterEach } from 'vitest';
+
+// KS-1868: submitTimestampRequest (src/tsa/rfc3161-client.ts) must still answer { success: false } when the value the TSA call threw
+// cannot be read. Its catch reads `err?.name` and then `${err?.message}` unguarded: a revoked Proxy throws on both reads, an Error whose
+// `message` getter throws throws on the second, and an Error whose `message` is a Symbol makes the template literal throw a TypeError.
+// In each case the function REJECTS (and with it the batch route's per-item result) where an ordinary Error gives a failed result.
+// The fetch stand-in is a plain function, not vi.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy first.
+import { submitTimestampRequest } from '../tsa/rfc3161-client';
+
+function failFetchWith(value: unknown): void {
+  vi.stubGlobal('fetch', () => Promise.reject(value));
+}
+
+async function run(): Promise<{ success: boolean; error?: string } | undefined> {
+  return submitTimestampRequest('http://tsa.test/tsr', Buffer.from('request')).catch(() => undefined);
+}
+
+describe('KS-1868 submitTimestampRequest reads the thrown value safely', () => {
+  afterEach(() => {
+    vi.unstubAllGlobals();
+  });
+
+  it('control ks1868 C1 an ordinary Error still gives a failed result with its message', async () => {
+    failFetchWith(new Error('connection reset'));
+    const r = await run();
+    expect(r).toEqual({ success: false, error: 'TSA request failed: connection reset' });
+  });
+
+  it('control ks1868 C2 a TimeoutError still gives the timed-out result', async () => {
+    const e = new Error('slow');
+    e.name = 'TimeoutError';
+    failFetchWith(e);
+    const r = await run();
+    expect(r?.success).toBe(false);
+    expect(r?.error).toMatch(/^TSA request timed out after \d+ms \(http:\/\/tsa\.test\/tsr\)$/);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value gives a failed result with a constant reason', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    failFetchWith(proxy);
+    const r = await run();
+    expect(r).toEqual({ success: false, error: 'TSA request failed: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws gives a failed result with a constant reason', async () => {
+    failFetchWith(
+      Object.create(Error.prototype, {
+        message: {
+          get() {
+            throw new Error('getter boom');
+          },
+        },
+      }),
+    );
+    const r = await run();
+    expect(r).toEqual({ success: false, error: 'TSA request failed: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 an Error whose message is a Symbol gives a failed result carrying its text', async () => {
+    const e = new Error('x');
+    Object.defineProperty(e, 'message', { value: Symbol('sym') });
+    failFetchWith(e);
+    const r = await run();
+    expect(r).toEqual({ success: false, error: 'TSA request failed: Symbol(sym)' });
+  });
+});
```
