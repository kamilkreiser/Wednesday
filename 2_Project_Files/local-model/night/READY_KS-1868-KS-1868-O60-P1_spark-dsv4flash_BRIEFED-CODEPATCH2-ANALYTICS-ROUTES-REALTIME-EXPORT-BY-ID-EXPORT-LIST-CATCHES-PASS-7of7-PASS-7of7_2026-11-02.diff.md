# READY — KS-1868-KS-1868-O60-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o60_p1_analytics_routes_realtime_export_by_id_export_list_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 08:00 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o60_p1_analytics_routes_realtime_export_by_id_export_list_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o60_p1_analytics_routes_realtime_export_by_id_export_list_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o60_p1_analytics_routes_realtime_export_by_id_export_list_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o60_p1_analytics_routes_realtime_export_by_id_export_list_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:00 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o60_p1_analytics_routes_realtime_export_by_id_export_list_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/analytics/src/routes/analytics.ts } + { Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/analytics/src/routes/analytics.ts` (product) and `Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/analytics/src/routes/analytics.ts
139	0	Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: analytics.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/analytics/src/routes/analytics.ts`; test(s): `Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/analytics/src/routes/analytics.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts 139 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/analytics/src/routes/analytics.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=6 of total=12; red cell(s): ["KS-1868 analytics 'GET /realtime' catch reads the thrown value safely RED ks1868 R1 GET /realtime: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 analytics 'GET /realtime' catch reads the thrown value safely RED ks1868 R2 GET /realtime: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 analytics 'GET /exports/:id' catch reads the thrown value safely RED ks1868 R1 GET /exports/:id: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 analytics 'GET /exports/:id' catch reads the thrown value safely RED ks1868 R2 GET /exports/:id: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 analytics 'GET /exports' catch reads the thrown value safely RED ks1868 R1 GET /exports: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 analytics 'GET /exports' catch reads the thrown value safely RED ks1868 R2 GET /exports: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500"]]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=56 failed=0 | after: total=68 failed=0` · `NEW reds: []` [baseline_suite.json total=56 failed=0; after_suite.json total=68 failed=0]
- A6 [verbatim]: `PASS A6 whole services/analytics suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/analytics: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/analytics/src/routes/analytics.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts` (+139/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/analytics/src/routes/analytics.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o60_p1_analytics_routes_realtime_export_by_id_export_list_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o60_p1_analytics_routes_realtime_export_by_id_export_list_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o60_p1_analytics_routes_realtime_export_by_id_export_list_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/analytics/src/routes/analytics.ts b/Blockchain/Dev/services/analytics/src/routes/analytics.ts
--- a/Blockchain/Dev/services/analytics/src/routes/analytics.ts
+++ b/Blockchain/Dev/services/analytics/src/routes/analytics.ts
@@ -242,7 +242,13 @@
       data: metrics,
     });
   } catch (error) {
-    logger.error('Error fetching real-time metrics', { error: error instanceof Error ? error.message : String(error) });
+    let reason: string;
+    try {
+      reason = error instanceof Error ? error.message : String(error);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('Error fetching real-time metrics', { error: reason });
     res.status(500).json({
       success: false,
       error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch real-time metrics' },
@@ -347,7 +353,13 @@
       data: exportResult,
     });
   } catch (error) {
-    logger.error('Error fetching export', { error: error instanceof Error ? error.message : String(error) });
+    let reason: string;
+    try {
+      reason = error instanceof Error ? error.message : String(error);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('Error fetching export', { error: reason });
     res.status(500).json({
       success: false,
       error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch export' },
@@ -369,7 +381,13 @@
       data: exports,
     });
   } catch (error) {
-    logger.error('Error listing exports', { error: error instanceof Error ? error.message : String(error) });
+    let reason: string;
+    try {
+      reason = error instanceof Error ? error.message : String(error);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('Error listing exports', { error: reason });
     res.status(500).json({
       success: false,
       error: { code: 'INTERNAL_ERROR', message: 'Failed to list exports' },
diff --git a/Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts b/Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/analytics/src/__tests__/ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts
@@ -0,0 +1,139 @@
+/**
+ * KS-1868: the three analytics route catches below read the caught value with `error instanceof Error ? error.message : String(error)` only to
+ * put it in a `logger.error` line. That read can itself throw (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws
+ * throws on `.message`), and inside an async Express 4 handler the rejection is not caught: the request gets no response and Node sees an
+ * unhandled rejection. Each catch now reads the value inside its own try and logs the constant `unreadable thrown value` when the read throws,
+ * and answers the same constant 500 as before.
+ *
+ * Routes covered here: GET /realtime, GET /exports/:id, GET /exports (mounted under /api/analytics).
+ *
+ * `express`, the two services and the logger are replaced and the route handlers are captured and called directly with a fake request and
+ * response: no port is bound, no database is touched. The stand-ins that reject with the thrown value are plain functions, not vi.fn(): a spy
+ * inspects what it rejects with and could itself fail on a revoked Proxy before the code under test saw it.
+ */
+import { describe, it, expect, vi, beforeAll, beforeEach } from 'vitest';
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
+vi.mock('../services/analyticsService', () => ({
+  analyticsService: { getRealTimeMetrics: () => Promise.reject(ks.toThrow) },
+}));
+vi.mock('../services/exportService', () => ({
+  exportService: {
+    getExport: () => Promise.reject(ks.toThrow),
+    listExports: () => Promise.reject(ks.toThrow),
+  },
+}));
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), debug: vi.fn(), error: ks.error },
+}));
+
+type Res60 = {
+  statusCode: number;
+  body: unknown;
+  status(c: number): Res60;
+  json(b: unknown): Res60;
+};
+
+function mkRes(): Res60 {
+  const r: Res60 = {
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
+type Case60 = { route: string; req: unknown; logMsg: string; answer: string };
+
+const CASES60: Case60[] = [
+  { route: 'GET /realtime', req: { params: {}, query: {} }, logMsg: 'Error fetching real-time metrics', answer: 'Failed to fetch real-time metrics' },
+  { route: 'GET /exports/:id', req: { params: { id: 'ks1868-export' }, query: {} }, logMsg: 'Error fetching export', answer: 'Failed to fetch export' },
+  { route: 'GET /exports', req: { params: {}, query: {} }, logMsg: 'Error listing exports', answer: 'Failed to list exports' },
+];
+
+const ERRS60 = (msg: string) => ks.error.mock.calls.filter((c) => c[0] === msg);
+
+/** Run one route handler with the service call rejecting with `value`. A handler that rejects (the defect) leaves the response untouched at 200. */
+async function invoke(c: Case60, value: unknown): Promise<Res60> {
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
+describe.each(CASES60)('KS-1868 analytics $route catch reads the thrown value safely', (c) => {
+  const body500 = (m: string) => ({ success: false, error: { code: 'INTERNAL_ERROR', message: m } });
+
+  it(`RED ks1868 R1 ${c.route}: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500`, async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    const res = await invoke(c, proxy);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(body500(c.answer));
+    expect(ERRS60(c.logMsg)).toHaveLength(1);
+    expect(ERRS60(c.logMsg)[0][1]).toEqual({ error: 'unreadable thrown value' });
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
+    expect(ERRS60(c.logMsg)).toHaveLength(1);
+    expect(ERRS60(c.logMsg)[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it(`control ks1868 C1 ${c.route}: an ordinary Error logs its message and the answer is the constant 500 without it`, async () => {
+    const res = await invoke(c, new Error('ordinary boom 10.0.0.7'));
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(body500(c.answer));
+    expect(JSON.stringify(res.body)).not.toContain('ordinary boom');
+    expect(ERRS60(c.logMsg)).toHaveLength(1);
+    expect(ERRS60(c.logMsg)[0][1]).toEqual({ error: 'ordinary boom 10.0.0.7' });
+  });
+
+  it(`control ks1868 C2 ${c.route}: a thrown string is logged as itself, as before`, async () => {
+    const res = await invoke(c, 'plain-string-marker');
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(body500(c.answer));
+    expect(ERRS60(c.logMsg)[0][1]).toEqual({ error: 'plain-string-marker' });
+  });
+});
```
