# READY — KS-1923-KS-1923-O130-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1923_o130_p1_audit_logger_flush_keeps_failed_events_in_order/out.md.checker/patch.diff`** (from `ls` at 09:42 2026-11-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1923_o130_p1_audit_logger_flush_keeps_failed_events_in_order/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1923_o130_p1_audit_logger_flush_keeps_failed_events_in_order/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1923_o130_p1_audit_logger_flush_keeps_failed_events_in_order/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1923_o130_p1_audit_logger_flush_keeps_failed_events_in_order-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:42 2026-11-10 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1923_o130_p1_audit_logger_flush_keeps_failed_events_in_order/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `07d4218e9776a5eced016f16330983c900e94fb3`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/security/audit-logger.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1923-audit-logger-flush-keeps-failed-events-in-order.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/security/audit-logger.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1923-audit-logger-flush-keeps-failed-events-in-order.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	4	Blockchain/Dev/packages/shared/src/security/audit-logger.ts
143	0	Blockchain/Dev/packages/shared/src/__tests__/ks1923-audit-logger-flush-keeps-failed-events-in-order.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: audit-logger.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/security/audit-logger.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1923-audit-logger-flush-keeps-failed-events-in-order.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/security/audit-logger.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1923-audit-logger-flush-keeps-failed-events-in-order.test.ts 143 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/security/audit-logger.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1923-audit-logger-flush-keeps-failed-events-in-order.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1923 AuditLogger.flush keeps every failed event, in delivery order RED ks1923 R1 two failures in one flush are retried in the order they were logged', 'KS-1923 AuditLogger.flush keeps every failed event, in delivery order RED ks1923 R2 a success between two failures: the two failed events come back in logged order and the success is not repeated', 'KS-1923 AuditLogger.flush keeps every failed event, in delivery order RED ks1923 R3 a logger that throws while the failure is logged does not make flush reject and does not drop the event', 'KS-1923 AuditLogger.flush keeps every failed event, in delivery order RED ks1923 R4 a logger that throws on the first of two failures still processes the second event and keeps both']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1623 failed=1 | after: total=1629 failed=1` · `NEW reds: []` [baseline_suite.json total=1623 failed=1; after_suite.json total=1629 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/security/audit-logger.ts` (+8/-4 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1923-audit-logger-flush-keeps-failed-events-in-order.test.ts` (+143/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/security/audit-logger.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `07d4218e9776a5eced016f16330983c900e94fb3` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1923_o130_p1_audit_logger_flush_keeps_failed_events_in_order/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1923_o130_p1_audit_logger_flush_keeps_failed_events_in_order/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/security/audit-logger.ts b/Blockchain/Dev/packages/shared/src/security/audit-logger.ts
--- a/Blockchain/Dev/packages/shared/src/security/audit-logger.ts
+++ b/Blockchain/Dev/packages/shared/src/security/audit-logger.ts
@@ -316,3 +316,5 @@ export class AuditLogger {
     this.eventBuffer = [];
-
+    // KS-1923 (G73-F1, G73-F3): failed events are collected in the order they were logged and put back in FRONT of the buffer once, after the loop, so a retry keeps delivery order
+    // and an event is kept before the failure is logged (a logger that throws can no longer drop it).
+    const failed: AuditEvent[] = [];
     for (const event of events) {
@@ -321,2 +323,3 @@ export class AuditLogger {
       } catch (error) {
+        failed.push(event);
         let reason: string;
@@ -327,7 +330,8 @@ export class AuditLogger {
         }
-        logger.error('Failed to process audit event', { error: reason });
-        // Re-add to buffer for retry
-        this.eventBuffer.unshift(event);
+        // The event is already kept for retry above (failed.push), so a logger that throws cannot lose it.
+        try { logger.error('Failed to process audit event', { error: reason }); } catch { /* nothing more can be said if the logger itself fails */ }
       }
     }
+    // Re-add to buffer for retry, oldest first
+    this.eventBuffer.unshift(...failed);
   }
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1923-audit-logger-flush-keeps-failed-events-in-order.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1923-audit-logger-flush-keeps-failed-events-in-order.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1923-audit-logger-flush-keeps-failed-events-in-order.test.ts
@@ -0,0 +1,143 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1923 (G73-F1 and G73-F3; G73-F4, the unbounded buffer, is NOT in this piece): AuditLogger.flush put each failed event back with
+// `unshift` AFTER logging the failure, so (F1) a logger that throws skipped the unshift and the event was dropped, and (F3) two failures
+// A then B were put back as B, A, so they were retried in reverse order and the audit hash chain did not verify in delivery order.
+// Harness: the real AuditLogger, the logger module replaced by a stand-in, onEvent a plain function that fails for chosen actions.
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
+function make(failing: Set<string>, delivered: string[]) {
+  return new AuditLogger({
+    serviceName: 'svc',
+    version: '1',
+    environment: 'test',
+    hashIntegrity: false,
+    maxBatchSize: 1000,
+    flushIntervalMs: 3600000,
+    onEvent: (event) => {
+      if (failing.has(event.action)) return Promise.reject(new Error('sink down'));
+      delivered.push(event.action);
+      return Promise.resolve();
+    },
+  });
+}
+
+describe('KS-1923 AuditLogger.flush keeps every failed event, in delivery order', () => {
+  beforeEach(() => {
+    h.error.mockReset();
+  });
+
+  it('RED ks1923 R1 two failures in one flush are retried in the order they were logged', async () => {
+    const failing = new Set(['KS1923_A', 'KS1923_B']);
+    const delivered: string[] = [];
+    const audit = make(failing, delivered);
+    try {
+      await audit.log(AuditEventCategory.SECURITY, 'KS1923_A');
+      await audit.log(AuditEventCategory.SECURITY, 'KS1923_B');
+      await audit.flush();
+      expect(delivered).toEqual([]);
+      failing.clear();
+      await audit.flush();
+      expect(delivered).toEqual(['KS1923_A', 'KS1923_B']);
+    } finally {
+      audit.stopFlushTimer();
+    }
+  });
+
+  it('RED ks1923 R2 a success between two failures: the two failed events come back in logged order and the success is not repeated', async () => {
+    const failing = new Set(['KS1923_A', 'KS1923_C']);
+    const delivered: string[] = [];
+    const audit = make(failing, delivered);
+    try {
+      await audit.log(AuditEventCategory.SECURITY, 'KS1923_A');
+      await audit.log(AuditEventCategory.SECURITY, 'KS1923_B');
+      await audit.log(AuditEventCategory.SECURITY, 'KS1923_C');
+      await audit.flush();
+      expect(delivered).toEqual(['KS1923_B']);
+      failing.clear();
+      await audit.flush();
+      expect(delivered).toEqual(['KS1923_B', 'KS1923_A', 'KS1923_C']);
+    } finally {
+      audit.stopFlushTimer();
+    }
+  });
+
+  it('RED ks1923 R3 a logger that throws while the failure is logged does not make flush reject and does not drop the event', async () => {
+    h.error.mockImplementation(() => {
+      throw new Error('logger boom');
+    });
+    const failing = new Set(['KS1923_A']);
+    const delivered: string[] = [];
+    const audit = make(failing, delivered);
+    try {
+      await audit.log(AuditEventCategory.SECURITY, 'KS1923_A');
+      const outcome = await audit.flush().then(() => 'resolved', () => 'rejected');
+      expect(outcome).toBe('resolved');
+      failing.clear();
+      await audit.flush().catch(() => undefined);
+      expect(delivered).toEqual(['KS1923_A']);
+    } finally {
+      audit.stopFlushTimer();
+    }
+  });
+
+  it('RED ks1923 R4 a logger that throws on the first of two failures still processes the second event and keeps both', async () => {
+    h.error.mockImplementation(() => {
+      throw new Error('logger boom');
+    });
+    const failing = new Set(['KS1923_A', 'KS1923_B']);
+    const delivered: string[] = [];
+    const audit = make(failing, delivered);
+    try {
+      await audit.log(AuditEventCategory.SECURITY, 'KS1923_A');
+      await audit.log(AuditEventCategory.SECURITY, 'KS1923_B');
+      await audit.flush().catch(() => undefined);
+      failing.clear();
+      await audit.flush().catch(() => undefined);
+      expect(delivered).toEqual(['KS1923_A', 'KS1923_B']);
+    } finally {
+      audit.stopFlushTimer();
+    }
+  });
+
+  it('control ks1923 C1 events that all succeed are delivered once, in order, and leave nothing to retry', async () => {
+    const delivered: string[] = [];
+    const audit = make(new Set(), delivered);
+    try {
+      await audit.log(AuditEventCategory.SECURITY, 'KS1923_A');
+      await audit.log(AuditEventCategory.SECURITY, 'KS1923_B');
+      await audit.flush();
+      await audit.flush();
+      expect(delivered).toEqual(['KS1923_A', 'KS1923_B']);
+      expect(h.error).not.toHaveBeenCalled();
+    } finally {
+      audit.stopFlushTimer();
+    }
+  });
+
+  it('control ks1923 C2 one failure is logged once with its message and retried once', async () => {
+    const failing = new Set(['KS1923_A']);
+    const delivered: string[] = [];
+    const audit = make(failing, delivered);
+    try {
+      await audit.log(AuditEventCategory.SECURITY, 'KS1923_A');
+      await audit.flush();
+      const logged = h.error.mock.calls.filter((c) => String(c[0]).includes('Failed to process audit event'));
+      expect(logged).toHaveLength(1);
+      expect(logged[0][1]).toEqual({ error: 'sink down' });
+      failing.clear();
+      await audit.flush().catch(() => undefined);
+      expect(delivered).toEqual(['KS1923_A']);
+    } finally {
+      audit.stopFlushTimer();
+    }
+  });
+});
```
