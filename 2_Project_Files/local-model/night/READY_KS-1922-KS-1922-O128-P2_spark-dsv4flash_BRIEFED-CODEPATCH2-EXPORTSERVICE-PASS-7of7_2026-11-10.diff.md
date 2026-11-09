# READY — KS-1922-KS-1922-O128-P2 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1922_o128_p2_analytics_failed_export_stores_a_constant_reason-r2/out.md.checker/patch.diff`** (from `ls` at 07:22 2026-11-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1922_o128_p2_analytics_failed_export_stores_a_constant_reason-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1922_o128_p2_analytics_failed_export_stores_a_constant_reason-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1922_o128_p2_analytics_failed_export_stores_a_constant_reason-r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1922_o128_p2_analytics_failed_export_stores_a_constant_reason-control/out.md.checker/patch.diff` rc 0, Spark operator o128).

**Held 07:22 2026-11-10 by Spark operator o128 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1922_o128_p2_analytics_failed_export_stores_a_constant_reason-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/analytics/src/services/exportService.ts } + { Blockchain/Dev/services/analytics/src/__tests__/ks1922-failed-export-stores-a-constant-reason.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/analytics/src/services/exportService.ts` (product) and `Blockchain/Dev/services/analytics/src/__tests__/ks1922-failed-export-stores-a-constant-reason.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	1	Blockchain/Dev/services/analytics/src/services/exportService.ts
93	0	Blockchain/Dev/services/analytics/src/__tests__/ks1922-failed-export-stores-a-constant-reason.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: exportService.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/analytics/src/services/exportService.ts`; test(s): `Blockchain/Dev/services/analytics/src/__tests__/ks1922-failed-export-stores-a-constant-reason.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/analytics/src/services/exportService.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/analytics/src/__tests__/ks1922-failed-export-stores-a-constant-reason.test.ts 93 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/analytics/src/services/exportService.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/analytics/src/__tests__/ks1922-failed-export-stores-a-constant-reason.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1922 a failed export stores a constant reason, not the thrown text RED ks1922 R1 an Error thrown by the metrics service leaves only the constant reason on the record', 'KS-1922 a failed export stores a constant reason, not the thrown text RED ks1922 R2 the row written to the database carries the constant reason too', 'KS-1922 a failed export stores a constant reason, not the thrown text RED ks1922 R3 the real text is logged on the server, and only there', 'KS-1922 a failed export stores a constant reason, not the thrown text RED ks1922 R4 an unknown export type no longer echoes its name into the record']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=117 failed=1 | after: total=123 failed=0` · `NEW reds: []` [baseline_suite.json total=117 failed=1; after_suite.json total=123 failed=0]
- A6 [verbatim]: `PASS A6 whole services/analytics suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/analytics: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/analytics/src/services/exportService.ts` (+3/-1 per numstat.out) and the test file `Blockchain/Dev/services/analytics/src/__tests__/ks1922-failed-export-stores-a-constant-reason.test.ts` (+93/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/analytics/src/services/exportService.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d0b4825cc24493213f82b609670a4a0fa521a4b9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1922_o128_p2_analytics_failed_export_stores_a_constant_reason-r2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1922_o128_p2_analytics_failed_export_stores_a_constant_reason-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/analytics/src/services/exportService.ts b/Blockchain/Dev/services/analytics/src/services/exportService.ts
--- a/Blockchain/Dev/services/analytics/src/services/exportService.ts
+++ b/Blockchain/Dev/services/analytics/src/services/exportService.ts
@@ -165,3 +165,5 @@
       exportResult.status = 'failed';
-      exportResult.error = error instanceof Error ? error.message : 'Unknown error';
+      // KS-1922: the thrown text (a database, filesystem or library message) must not reach the API answer; it goes to the server log only.
+      logger.warn('Export failed', { error: error instanceof Error ? error.message : 'Unknown error' });
+      exportResult.error = 'Export failed';
       await this.dbSaveExport(exportResult);
diff --git a/Blockchain/Dev/services/analytics/src/__tests__/ks1922-failed-export-stores-a-constant-reason.test.ts b/Blockchain/Dev/services/analytics/src/__tests__/ks1922-failed-export-stores-a-constant-reason.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/analytics/src/__tests__/ks1922-failed-export-stores-a-constant-reason.test.ts
@@ -0,0 +1,93 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1922: ExportService.processExport stored the thrown error's message on the export record, and GET /api/analytics/exports/:id
+// returns that record, so a failed export put internal text (a database, filesystem or library message) into the API answer.
+// The record now carries a constant reason; the real text goes to the server log only.
+// Harness: the real ExportService; the database, the logger and the metrics service are stand-ins.
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
+const LEAK = 'connect ECONNREFUSED 10.1.2.3:5432 password authentication failed for user svc_analytics';
+
+async function settle(type: string, svc = new ExportService()) {
+  const created = await svc.createExport({ type, period: 'day', format: 'json' });
+  await vi.waitFor(async () => {
+    const got = await svc.getExport(created.id);
+    expect(['completed', 'failed']).toContain(got?.status);
+  });
+  return (await svc.getExport(created.id))!;
+}
+
+describe('KS-1922 a failed export stores a constant reason, not the thrown text', () => {
+  beforeEach(() => {
+    h.thrown = undefined;
+    h.warn.mockReset();
+    h.inserts.length = 0;
+  });
+
+  it('RED ks1922 R1 an Error thrown by the metrics service leaves only the constant reason on the record', async () => {
+    h.thrown = new Error(LEAK);
+    const got = await settle('certifications');
+    expect(got.status).toBe('failed');
+    expect(got.error).toBe('Export failed');
+  });
+
+  it('RED ks1922 R2 the row written to the database carries the constant reason too', async () => {
+    h.thrown = new Error(LEAK);
+    await settle('certifications');
+    const failedWrites = h.inserts.filter((p) => p[1] === 'failed');
+    expect(failedWrites).toHaveLength(1);
+    expect(failedWrites[0][8]).toBe('Export failed');
+  });
+
+  it('RED ks1922 R3 the real text is logged on the server, and only there', async () => {
+    h.thrown = new Error(LEAK);
+    await settle('certifications');
+    const logged = h.warn.mock.calls.filter((c) => String(c[0]) === 'Export failed');
+    expect(logged).toHaveLength(1);
+    expect(logged[0][1]).toMatchObject({ error: LEAK });
+  });
+
+  it('RED ks1922 R4 an unknown export type no longer echoes its name into the record', async () => {
+    const got = await settle('secret-internal-type');
+    expect(got.status).toBe('failed');
+    expect(got.error).toBe('Export failed');
+  });
+
+  it('control ks1922 C1 a successful export has status completed and no error', async () => {
+    const got = await settle('certifications');
+    expect(got.status).toBe('completed');
+    expect(got.error).toBeUndefined();
+  });
+
+  it('control ks1922 C2 a successful export logs no Export failed line', async () => {
+    await settle('certifications');
+    expect(h.warn.mock.calls.filter((c) => String(c[0]) === 'Export failed')).toHaveLength(0);
+  });
+});
```
