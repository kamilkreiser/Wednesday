# READY — KS-1868-KS-1868-O61-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o61_p3_analytics_routes_zod_precheck_catches_activity_exports_reports_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 08:16 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o61_p3_analytics_routes_zod_precheck_catches_activity_exports_reports_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o61_p3_analytics_routes_zod_precheck_catches_activity_exports_reports_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o61_p3_analytics_routes_zod_precheck_catches_activity_exports_reports_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o61_p3_analytics_routes_zod_precheck_catches_activity_exports_reports_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:16 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o61_p3_analytics_routes_zod_precheck_catches_activity_exports_reports_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/analytics/src/routes/analytics.ts } + { Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-zod-catches-p3-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/analytics/src/routes/analytics.ts` (product) and `Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-zod-catches-p3-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
27	3	Blockchain/Dev/services/analytics/src/routes/analytics.ts
154	0	Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-zod-catches-p3-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (27 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: analytics.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/analytics/src/routes/analytics.ts`; test(s): `Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-zod-catches-p3-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/analytics/src/routes/analytics.ts 27 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-zod-catches-p3-unreadable-throw.test.ts 154 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/analytics/src/routes/analytics.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-zod-catches-p3-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=6 of total=12; red cell(s): ["KS-1868 analytics 'GET /activity' catch reads the thrown value safely RED ks1868 R1 GET /activity: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 analytics 'GET /activity' catch reads the thrown value safely RED ks1868 R2 GET /activity: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 analytics 'POST /exports' catch reads the thrown value safely RED ks1868 R1 POST /exports: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 analytics 'POST /exports' catch reads the thrown value safely RED ks1868 R2 POST /exports: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 analytics 'POST /reports' catch reads the thrown value safely RED ks1868 R1 POST /reports: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 analytics 'POST /reports' catch reads the thrown value safely RED ks1868 R2 POST /reports: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500"]]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=56 failed=0 | after: total=68 failed=0` · `NEW reds: []` [baseline_suite.json total=56 failed=0; after_suite.json total=68 failed=0]
- A6 [verbatim]: `PASS A6 whole services/analytics suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/analytics: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/analytics/src/routes/analytics.ts` (+27/-3 per numstat.out) and the test file `Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-zod-catches-p3-unreadable-throw.test.ts` (+154/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/analytics/src/routes/analytics.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o61_p3_analytics_routes_zod_precheck_catches_activity_exports_reports_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o61_p3_analytics_routes_zod_precheck_catches_activity_exports_reports_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o61_p3_analytics_routes_zod_precheck_catches_activity_exports_reports_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/analytics/src/routes/analytics.ts b/Blockchain/Dev/services/analytics/src/routes/analytics.ts
--- a/Blockchain/Dev/services/analytics/src/routes/analytics.ts
+++ b/Blockchain/Dev/services/analytics/src/routes/analytics.ts
@@ -277,7 +277,15 @@
         },
       },
     });
-  } catch (error) {
+  } catch (thrown) {
+    let error: unknown = thrown;
+    try {
+      if (!(thrown instanceof z.ZodError)) {
+        String(thrown instanceof Error ? thrown.message : thrown);
+      }
+    } catch {
+      error = new Error('unreadable thrown value');
+    }
     if (error instanceof z.ZodError) {
       res.status(400).json({
         success: false,
@@ -311,7 +319,15 @@
       success: true,
       data: exportResult,
     });
-  } catch (error) {
+  } catch (thrown) {
+    let error: unknown = thrown;
+    try {
+      if (!(thrown instanceof z.ZodError)) {
+        String(thrown instanceof Error ? thrown.message : thrown);
+      }
+    } catch {
+      error = new Error('unreadable thrown value');
+    }
     if (error instanceof z.ZodError) {
       return res.status(400).json({
         success: false,
@@ -394,7 +410,15 @@
       success: true,
       data: report,
     });
-  } catch (error) {
+  } catch (thrown) {
+    let error: unknown = thrown;
+    try {
+      if (!(thrown instanceof z.ZodError)) {
+        String(thrown instanceof Error ? thrown.message : thrown);
+      }
+    } catch {
+      error = new Error('unreadable thrown value');
+    }
     if (error instanceof z.ZodError) {
       return res.status(400).json({
         success: false,
diff --git a/Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-zod-catches-p3-unreadable-throw.test.ts b/Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-zod-catches-p3-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-zod-catches-p3-unreadable-throw.test.ts
@@ -0,0 +1,154 @@
+/**
+ * KS-1868: the three analytics route catches below (activity, POST exports and POST reports) each test `error instanceof z.ZodError` first and then read the caught value
+ * with `error instanceof Error ? error.message : String(error)` for a `logger.error` line. Both reads can themselves throw (a revoked Proxy throws
+ * on `instanceof`; an Error whose `message` getter throws throws on `.message`), and inside an async Express 4 handler the rejection is not caught:
+ * the request gets no response and Node sees an unhandled rejection. Each catch now probes both reads inside its own try: an unreadable value is
+ * replaced by an ordinary Error and so is logged as the constant `unreadable thrown value` and the route answers the same constant 500 as for any ordinary Error. An ordinary ZodError
+ * still answers 400 with `details` equal to its `errors`, and an ordinary Error still logs its own message and answers the constant 500.
+ *
+ * `express`, the request schemas, the service and the logger are replaced and the route handlers are captured and called directly with a fake
+ * request and response: no port is bound, no database is touched. The stand-ins that reject with the thrown value are plain functions, not vi.fn():
+ * a spy inspects what it rejects with and could itself fail on a revoked Proxy before the code under test saw it.
+ */
+import { describe, it, expect, vi, beforeAll, beforeEach } from 'vitest';
+import { z } from 'zod';
+
+const ks = vi.hoisted(() => ({
+  routes: {} as Record<string, (req: unknown, res: unknown) => Promise<void>>,
+  toThrow: undefined as unknown,
+  error: vi.fn(),
+}));
+
+vi.mock('express', () => {
+  const router = {
+    get: (p: string, f: (req: unknown, res: unknown) => Promise<void>) => {
+      ks.routes['GET ' + p] = f;
+    },
+    post: (p: string, f: (req: unknown, res: unknown) => Promise<void>) => {
+      ks.routes['POST ' + p] = f;
+    },
+  };
+  return { Router: () => router, default: { Router: () => router } };
+});
+vi.mock('../types/analytics.types', () => {
+  const passThrough = { parse: (v: unknown) => v };
+  return {
+    AnalyticsQuerySchema: passThrough,
+    ActivityQuerySchema: passThrough,
+    ExportRequestSchema: passThrough,
+    ReportRequestSchema: passThrough,
+  };
+});
+vi.mock('../services/analyticsService', () => ({
+  analyticsService: {
+    getActivityFeed: () => Promise.reject(ks.toThrow),
+  },
+}));
+vi.mock('../services/exportService', () => ({
+  exportService: {
+    createExport: () => Promise.reject(ks.toThrow),
+    generateReport: () => Promise.reject(ks.toThrow),
+  },
+}));
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), debug: vi.fn(), error: ks.error },
+}));
+
+type Res61 = {
+  statusCode: number;
+  body: unknown;
+  status(c: number): Res61;
+  json(b: unknown): Res61;
+};
+
+function mkRes(): Res61 {
+  const r: Res61 = {
+    statusCode: 200,
+    body: undefined,
+    status(c) {
+      r.statusCode = c;
+      return r;
+    },
+    json(b) {
+      r.body = b;
+      return r;
+    },
+  };
+  return r;
+}
+
+type Case61 = { route: string; req: unknown; logMsg: string; answer: string; bad: string };
+
+const CASES61: Case61[] = [
+  { route: 'GET /activity', req: { query: {} }, logMsg: 'Error fetching activity', answer: 'Failed to fetch activity feed', bad: 'Invalid query parameters' },
+  { route: 'POST /exports', req: { body: {} }, logMsg: 'Error creating export', answer: 'Failed to create export', bad: 'Invalid export request' },
+  { route: 'POST /reports', req: { body: {} }, logMsg: 'Error generating report', answer: 'Failed to generate report', bad: 'Invalid report request' },
+];
+
+const ERRS61 = (msg: string) => ks.error.mock.calls.filter((c) => c[0] === msg);
+
+/** Run one route handler with the service call rejecting with `value`. A handler that rejects (the defect) leaves the response untouched at 200. */
+async function invoke(c: Case61, value: unknown): Promise<Res61> {
+  ks.toThrow = value;
+  const res = mkRes();
+  await ks.routes[c.route](c.req, res).catch(() => undefined);
+  return res;
+}
+
+beforeAll(async () => {
+  await import('../routes/analytics');
+});
+
+beforeEach(() => {
+  ks.toThrow = undefined;
+  ks.error.mockReset();
+});
+
+describe.each(CASES61)('KS-1868 analytics $route catch reads the thrown value safely', (c) => {
+  const body500 = (m: string) => ({ success: false, error: { code: 'INTERNAL_ERROR', message: m } });
+
+  it(`RED ks1868 R1 ${c.route}: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500`, async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    const res = await invoke(c, proxy);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(body500(c.answer));
+    expect(ERRS61(c.logMsg)).toHaveLength(1);
+    expect(ERRS61(c.logMsg)[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it(`RED ks1868 R2 ${c.route}: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500`, async () => {
+    const getterThrows = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const res = await invoke(c, getterThrows);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(body500(c.answer));
+    expect(ERRS61(c.logMsg)).toHaveLength(1);
+    expect(ERRS61(c.logMsg)[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it(`control ks1868 C1 ${c.route}: an ordinary ZodError answers 400 with details equal to its errors and logs nothing`, async () => {
+    const zerr = new z.ZodError([{ code: 'custom', path: ['limit'], message: 'ks1868 control issue' }]);
+    const res = await invoke(c, zerr);
+    expect(res.statusCode).toBe(400);
+    expect(res.body).toEqual({
+      success: false,
+      error: { code: 'BAD_REQUEST', message: c.bad, details: zerr.errors },
+    });
+    expect(ks.error).not.toHaveBeenCalled();
+  });
+
+  it(`control ks1868 C2 ${c.route}: an ordinary Error logs its message and the answer is the constant 500 without it`, async () => {
+    const res = await invoke(c, new Error('ordinary boom 10.0.0.7'));
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(body500(c.answer));
+    expect(JSON.stringify(res.body)).not.toContain('ordinary boom');
+    expect(ERRS61(c.logMsg)).toHaveLength(1);
+    expect(ERRS61(c.logMsg)[0][1]).toEqual({ error: 'ordinary boom 10.0.0.7' });
+  });
+});
```
