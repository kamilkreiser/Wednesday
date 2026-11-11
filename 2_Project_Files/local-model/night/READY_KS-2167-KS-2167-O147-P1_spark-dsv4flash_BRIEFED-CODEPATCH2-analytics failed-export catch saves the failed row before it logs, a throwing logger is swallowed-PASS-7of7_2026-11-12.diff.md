# READY — KS-2167-KS-2167-O147-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2167_o147_p1_failed_export_catch_saves_before_it_logs/out.md.checker/patch.diff`** (from `ls` at 01:54 2026-11-12; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2167_o147_p1_failed_export_catch_saves_before_it_logs/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2167_o147_p1_failed_export_catch_saves_before_it_logs/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2167_o147_p1_failed_export_catch_saves_before_it_logs/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 01:54 2026-11-12 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2167_o147_p1_failed_export_catch_saves_before_it_logs/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4f85ca04c622f29099d184bc45de2faa61fb4af0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/analytics/src/services/exportService.ts } + { Blockchain/Dev/services/analytics/src/__tests__/ks2167-a-throwing-logger-in-the-failed-export-catch-still-saves-the-failed-row.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/analytics/src/services/exportService.ts` (product) and `Blockchain/Dev/services/analytics/src/__tests__/ks2167-a-throwing-logger-in-the-failed-export-catch-still-saves-the-failed-row.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	2	Blockchain/Dev/services/analytics/src/services/exportService.ts
105	0	Blockchain/Dev/services/analytics/src/__tests__/ks2167-a-throwing-logger-in-the-failed-export-catch-still-saves-the-failed-row.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: exportService.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/analytics/src/services/exportService.ts`; test(s): `Blockchain/Dev/services/analytics/src/__tests__/ks2167-a-throwing-logger-in-the-failed-export-catch-still-saves-the-failed-row.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/analytics/src/services/exportService.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/analytics/src/__tests__/ks2167-a-throwing-logger-in-the-failed-export-catch-still-saves-the-failed-row.test.ts 105 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/analytics/src/services/exportService.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/analytics/src/__tests__/ks2167-a-throwing-logger-in-the-failed-export-catch-still-saves-the-failed-row.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-2167 a throwing logger in the failed-export catch still saves the failed row RED ks2167 R1 a logger that throws still leaves one failed row written with the constant reason', 'KS-2167 a throwing logger in the failed-export catch still saves the failed row RED ks2167 R2 a logger that throws still leaves the constant reason on the stored export', 'KS-2167 a throwing logger in the failed-export catch still saves the failed row RED ks2167 R3 an Error whose message cannot be read still leaves one failed row written']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=123 failed=0 | after: total=128 failed=0` · `NEW reds: []` [baseline_suite.json total=123 failed=0; after_suite.json total=128 failed=0]
- A6 [verbatim]: `PASS A6 whole services/analytics suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/analytics: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/analytics/src/services/exportService.ts` (+8/-2 per numstat.out) and the test file `Blockchain/Dev/services/analytics/src/__tests__/ks2167-a-throwing-logger-in-the-failed-export-catch-still-saves-the-failed-row.test.ts` (+105/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/analytics/src/services/exportService.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4f85ca04c622f29099d184bc45de2faa61fb4af0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2167_o147_p1_failed_export_catch_saves_before_it_logs/input.json`. Brief (given by --brief; its `# ` heading names KS-2167): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2167_o147_p1_failed_export_catch_saves_before_it_logs/KS-2167.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2167_o147_p1_failed_export_catch_saves_before_it_logs/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/analytics/src/services/exportService.ts b/Blockchain/Dev/services/analytics/src/services/exportService.ts
--- a/Blockchain/Dev/services/analytics/src/services/exportService.ts
+++ b/Blockchain/Dev/services/analytics/src/services/exportService.ts
@@ -164,8 +164,14 @@
     } catch (error) {
       exportResult.status = 'failed';
-      // KS-1922: the thrown text (a database, filesystem or library message) must not reach the API answer; it goes to the server log only.
-      logger.warn('Export failed', { error: error instanceof Error ? error.message : 'Unknown error' });
       exportResult.error = 'Export failed';
       await this.dbSaveExport(exportResult);
+      // KS-1922 and KS-2167: the thrown text (a database, filesystem or library message) goes to the server log only, never to the API answer,
+      // and only AFTER the failed row is saved: a logger or a message read that throws must not undo the saved failure or reject the unawaited call.
+      try {
+        const reason = error instanceof Error ? error.message : 'Unknown error';
+        logger.warn('Export failed', { error: reason });
+      } catch {
+        // nothing more can be done with a log line that cannot be written or read
+      }
     }
   }
diff --git a/Blockchain/Dev/services/analytics/src/__tests__/ks2167-a-throwing-logger-in-the-failed-export-catch-still-saves-the-failed-row.test.ts b/Blockchain/Dev/services/analytics/src/__tests__/ks2167-a-throwing-logger-in-the-failed-export-catch-still-saves-the-failed-row.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/analytics/src/__tests__/ks2167-a-throwing-logger-in-the-failed-export-catch-still-saves-the-failed-row.test.ts
@@ -0,0 +1,105 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-2167: ExportService.processExport logged before it set the constant reason and saved the failed row, and createExport calls it
+// without await or catch, so a logger that throws left the stored export 'processing' and rejected the call with nobody to handle it.
+// The failed row is now saved first, and the log line is written inside its own try.
+// Harness: the real ExportService; the database, the logger and the metrics service are stand-ins (the shape of ks1922's suite).
+const h = vi.hoisted(() => ({
+  thrown: undefined as unknown,
+  warn: vi.fn(),
+  inserts: [] as unknown[][],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: async (_sql: string, params?: unknown[]) => {
+    h.inserts.push(params || []);
+    return { rows: [], rowCount: 1 };
+  },
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: h.warn, error: vi.fn(), debug: vi.fn() },
+}));
+
+vi.mock('../services/analyticsService', () => ({
+  analyticsService: {
+    getCertificationMetrics: async () => {
+      if (h.thrown !== undefined) throw h.thrown;
+      return { total: 3 };
+    },
+  },
+}));
+
+import { ExportService } from '../services/exportService';
+
+async function settle(type: string, svc = new ExportService()) {
+  const created = await svc.createExport({ type, period: 'day', format: 'json' });
+  await vi.waitFor(async () => {
+    const got = await svc.getExport(created.id);
+    expect(['completed', 'failed']).toContain(got?.status);
+  });
+  await new Promise((resolve) => setTimeout(resolve, 20));
+  return (await svc.getExport(created.id))!;
+}
+
+function failedWrites() {
+  return h.inserts.filter((p) => p[1] === 'failed');
+}
+
+describe('KS-2167 a throwing logger in the failed-export catch still saves the failed row', () => {
+  beforeEach(() => {
+    h.thrown = undefined;
+    h.warn.mockReset();
+    h.inserts.length = 0;
+  });
+
+  it('RED ks2167 R1 a logger that throws still leaves one failed row written with the constant reason', async () => {
+    h.thrown = new Error('boom');
+    h.warn.mockImplementation(() => {
+      throw new Error('logger down');
+    });
+    await settle('certifications');
+    expect(failedWrites()).toHaveLength(1);
+    expect(failedWrites()[0][8]).toBe('Export failed');
+  });
+
+  it('RED ks2167 R2 a logger that throws still leaves the constant reason on the stored export', async () => {
+    h.thrown = new Error('boom');
+    h.warn.mockImplementation(() => {
+      throw new Error('logger down');
+    });
+    const got = await settle('certifications');
+    expect(got.status).toBe('failed');
+    expect(got.error).toBe('Export failed');
+  });
+
+  it('RED ks2167 R3 an Error whose message cannot be read still leaves one failed row written', async () => {
+    const hostile = new Error('hidden');
+    Object.defineProperty(hostile, 'message', {
+      get() {
+        throw new Error('message getter down');
+      },
+    });
+    h.thrown = hostile;
+    const got = await settle('certifications');
+    expect(got.error).toBe('Export failed');
+    expect(failedWrites()).toHaveLength(1);
+  });
+
+  it('control ks2167 C1 a logger that throws does nothing to a successful export', async () => {
+    h.warn.mockImplementation(() => {
+      throw new Error('logger down');
+    });
+    const got = await settle('certifications');
+    expect(got.status).toBe('completed');
+    expect(got.error).toBeUndefined();
+  });
+
+  it('control ks2167 C2 with a working logger a failed export writes one failed row and one Export failed log line', async () => {
+    h.thrown = new Error('boom');
+    await settle('certifications');
+    expect(failedWrites()).toHaveLength(1);
+    expect(h.warn.mock.calls.filter((c) => String(c[0]) === 'Export failed')).toHaveLength(1);
+  });
+});
```
