# READY — KS-1868-KS-1868-O91-P9 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p9_timestamping_create_timestamp_request_exception_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 07:41 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p9_timestamping_create_timestamp_request_exception_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p9_timestamping_create_timestamp_request_exception_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p9_timestamping_create_timestamp_request_exception_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p9_timestamping_create_timestamp_request_exception_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:41 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p9_timestamping_create_timestamp_request_exception_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts } + { Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-create-timestamp-request-exception-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts` (product) and `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-create-timestamp-request-exception-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts
104	0	Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-create-timestamp-request-exception-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: qualified-tsa.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts`; test(s): `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-create-timestamp-request-exception-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-create-timestamp-request-exception-catch-unreadable-throw.test.ts 104 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-create-timestamp-request-exception-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1868 the createTimestamp request-exception catch falls back to the mock token and logs text for a hostile thrown value RED ks1868 R1: a request failure that is a revoked Proxy is logged as text and createTimestamp answers the mock token, as for an ordinary Error', 'KS-1868 the createTimestamp request-exception catch falls back to the mock token and logs text for a hostile thrown value RED ks1868 R2: a request failure that is an Error whose message getter throws is logged as text and createTimestamp answers the mock token, as for an ordinary Error', 'KS-1868 the createTimestamp request-exception catch falls back to the mock token and logs text for a hostile thrown value RED ks1868 R3: a request failure that is an Error whose message is a Symbol is logged as text and createTimestamp answers the mock token, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=100 failed=0 | after: total=106 failed=0` · `NEW reds: []` [baseline_suite.json total=100 failed=0; after_suite.json total=106 failed=0]
- A6 [verbatim]: `PASS A6 whole services/timestamping suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/timestamping: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-create-timestamp-request-exception-catch-unreadable-throw.test.ts` (+104/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p9_timestamping_create_timestamp_request_exception_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o91_p9_timestamping_create_timestamp_request_exception_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p9_timestamping_create_timestamp_request_exception_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts b/Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts
--- a/Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts
+++ b/Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts
@@ -307,3 +307,10 @@
   } catch (err: any) {
-    logger.warn('[TSA] RFC-3161 request exception', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('[TSA] RFC-3161 request exception', { error: reason });
   }
diff --git a/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-create-timestamp-request-exception-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-create-timestamp-request-exception-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-create-timestamp-request-exception-catch-unreadable-throw.test.ts
@@ -0,0 +1,104 @@
+import { describe, it, expect, beforeEach, vi } from 'vitest';
+
+// KS-1868 (operator 91 screen, timestamping qualified TSA): the request-exception catch of createTimestamp (line 308) of
+// services/timestamping/src/tsa/qualified-tsa.ts passes `err?.message` straight into the logger's meta object, unguarded. A
+// thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the catch itself throw, so
+// createTimestamp REJECTS instead of logging the failure and falling back to its documented mock token ("Falls back to a mock
+// token if no TSA is reachable"), as an ordinary Error does; an Error whose message is readable but not a string (a Symbol) is
+// handed to the logger uncoerced. The cells make the RFC-3161 request throw such a value and assert createTimestamp resolves
+// with the mock fallback and the logged value is text (the constant when the value cannot be turned into text). Harness: the
+// real module with the RFC-3161 client and verifier replaced by plain stand-ins and the logger by a plain recording object (no
+// network, no ASN.1 libraries).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logged: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('../tsa/rfc3161-client', () => ({
+  requestTimestamp: async () => {
+    throw h.toThrow;
+  },
+}));
+vi.mock('../tsa/rfc3161-verify', () => ({
+  verifyRfc3161Token: async () => ({ valid: false }),
+}));
+vi.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    h.logged.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+
+import { createTimestamp } from '../tsa/qualified-tsa';
+
+const EXC = '[TSA] RFC-3161 request exception';
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logged.length = 0;
+});
+
+async function run(value: unknown): Promise<{ ok: boolean; mock: boolean }> {
+  h.toThrow = value;
+  try {
+    const r = await createTimestamp({ hash: 'a'.repeat(64), hashAlgorithm: 'sha256' } as Parameters<typeof createTimestamp>[0]);
+    return { ok: true, mock: r.mock === true };
+  } catch {
+    return { ok: false, mock: false };
+  }
+}
+const LINES = () => h.logged.filter((l) => l.message === EXC);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: { meta: Record<string, unknown> | undefined } | undefined): string => {
+  const v = l?.meta?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+/** An Error whose `message` getter succeeds and returns the value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 the createTimestamp request-exception catch falls back to the mock token and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the RFC-3161 request is logged with its message and createTimestamp answers the mock token', async () => {
+    expect(await run(new Error('tsa down'))).toEqual({ ok: true, mock: true });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('tsa down');
+  });
+  it('control ks1868 C2: a thrown plain string is logged without a message and createTimestamp answers the mock token', async () => {
+    expect(await run('plain boom')).toEqual({ ok: true, mock: true });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('<undefined>');
+  });
+  it('control ks1868 C3: an Error with an empty message is logged with the empty text and createTimestamp answers the mock token', async () => {
+    expect(await run(new Error(''))).toEqual({ ok: true, mock: true });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('');
+  });
+  it('RED ks1868 R1: a request failure that is a revoked Proxy is logged as text and createTimestamp answers the mock token, as for an ordinary Error', async () => {
+    expect(await run(revokedProxy())).toEqual({ ok: true, mock: true });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: a request failure that is an Error whose message getter throws is logged as text and createTimestamp answers the mock token, as for an ordinary Error', async () => {
+    expect(await run(getterThrows())).toEqual({ ok: true, mock: true });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: a request failure that is an Error whose message is a Symbol is logged as text and createTimestamp answers the mock token, as for an ordinary Error', async () => {
+    expect(await run(withMessage(Symbol('ks1868')))).toEqual({ ok: true, mock: true });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('Symbol(ks1868)');
+  });
+});
```
