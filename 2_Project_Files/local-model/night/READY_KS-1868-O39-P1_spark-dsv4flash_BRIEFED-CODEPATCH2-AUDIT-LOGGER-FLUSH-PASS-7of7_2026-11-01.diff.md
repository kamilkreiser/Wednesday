# READY — KS-1868-KS-1868-O39-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_ks_1868_o39_p1_shared_audit_logger_flush_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 10:02 2026-11-01; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_ks_1868_o39_p1_shared_audit_logger_flush_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_ks_1868_o39_p1_shared_audit_logger_flush_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o39_p1_shared_audit_logger_flush_unreadable_throw/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 10:02 2026-11-01 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_ks_1868_o39_p1_shared_audit_logger_flush_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `60e59bd2270b5ec6e0e73e7823501188f8196403`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/security/audit-logger.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/security/audit-logger.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/packages/shared/src/security/audit-logger.ts
96	0	Blockchain/Dev/packages/shared/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: audit-logger.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/security/audit-logger.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/security/audit-logger.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts 96 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/security/audit-logger.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=2 of total=3; red cell(s): ['KS-1868 AuditLogger.flush reads an onEvent failure safely RED ks1868 R1 a revoked Proxy rejection is logged as a constant and the event is retried', 'KS-1868 AuditLogger.flush reads an onEvent failure safely RED ks1868 R2 an Error whose message getter throws is logged as a constant and the event is retried']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1099 failed=1 | after: total=1102 failed=1` · `NEW reds: []` [baseline_suite.json total=1099 failed=1; after_suite.json total=1102 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/security/audit-logger.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts` (+96/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/security/audit-logger.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `60e59bd2270b5ec6e0e73e7823501188f8196403` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_ks_1868_o39_p1_shared_audit_logger_flush_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o39_p1_shared_audit_logger_flush_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_ks_1868_o39_p1_shared_audit_logger_flush_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/security/audit-logger.ts b/Blockchain/Dev/packages/shared/src/security/audit-logger.ts
--- a/Blockchain/Dev/packages/shared/src/security/audit-logger.ts
+++ b/Blockchain/Dev/packages/shared/src/security/audit-logger.ts
@@ -319,7 +319,13 @@
       try {
         await this.config.onEvent(event);
       } catch (error) {
-        logger.error('Failed to process audit event', { error: error instanceof Error ? error.message : String(error) });
+        let reason: string;
+        try {
+          reason = error instanceof Error ? error.message : String(error);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
+        logger.error('Failed to process audit event', { error: reason });
         // Re-add to buffer for retry
         this.eventBuffer.unshift(event);
       }
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts
@@ -0,0 +1,96 @@
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+
+// KS-1868: AuditLogger.flush must still log its failure and put the event back in the buffer for
+// retry when `onEvent` rejects with a value that cannot be read (a revoked Proxy throws on
+// `instanceof`; an Error whose `message` getter throws, throws on `.message`). Today the catch
+// block itself throws, so flush() rejects and the failed event is dropped instead of retried.
+// `onEvent` is a plain function, not vi.fn(): a spy inspects what it rejects with and could itself
+// fail on a revoked Proxy before the code under test saw it.
+const h = vi.hoisted(() => ({
+  error: vi.fn(),
+}));
+
+vi.mock('../logger', () => ({
+  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error },
+}));
+
+import { AuditLogger, AuditEventCategory } from '../security/audit-logger';
+
+type Outcome = { threw: boolean; delivered: number };
+
+async function run(toThrow: unknown): Promise<Outcome> {
+  let fail = true;
+  let delivered = 0;
+  const audit = new AuditLogger({
+    serviceName: 'svc',
+    version: '1',
+    environment: 'test',
+    hashIntegrity: false,
+    maxBatchSize: 1000,
+    flushIntervalMs: 3600000,
+    onEvent: () => {
+      if (fail) return Promise.reject(toThrow);
+      delivered++;
+      return Promise.resolve();
+    },
+  });
+  const out: Outcome = { threw: false, delivered: 0 };
+  try {
+    await audit.log(AuditEventCategory.SECURITY, 'KS1868_PROBE');
+    try {
+      await audit.flush();
+    } catch {
+      out.threw = true;
+    }
+    fail = false;
+    await audit.flush();
+    out.delivered = delivered;
+  } finally {
+    audit.stopFlushTimer();
+  }
+  return out;
+}
+
+const FLUSH_ERRORS = () => h.error.mock.calls.filter((c) => String(c[0]).includes('Failed to process audit event'));
+
+describe('KS-1868 AuditLogger.flush reads an onEvent failure safely', () => {
+  beforeEach(() => {
+    h.error.mockReset();
+  });
+  afterEach(() => {
+    vi.clearAllTimers();
+  });
+
+  it('control ks1868 C1 an ordinary Error is logged with its message and the event is retried', async () => {
+    const out = await run(new Error('sink down'));
+    expect(out.threw).toBe(false);
+    expect(FLUSH_ERRORS()).toHaveLength(1);
+    expect(FLUSH_ERRORS()[0][1]).toEqual({ error: 'sink down' });
+    expect(out.delivered).toBe(1);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy rejection is logged as a constant and the event is retried', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    const out = await run(proxy);
+    expect(out.threw).toBe(false);
+    expect(FLUSH_ERRORS()).toHaveLength(1);
+    expect(FLUSH_ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expect(out.delivered).toBe(1);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is logged as a constant and the event is retried', async () => {
+    const hostile = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const out = await run(hostile);
+    expect(out.threw).toBe(false);
+    expect(FLUSH_ERRORS()).toHaveLength(1);
+    expect(FLUSH_ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expect(out.delivered).toBe(1);
+  });
+});
```
