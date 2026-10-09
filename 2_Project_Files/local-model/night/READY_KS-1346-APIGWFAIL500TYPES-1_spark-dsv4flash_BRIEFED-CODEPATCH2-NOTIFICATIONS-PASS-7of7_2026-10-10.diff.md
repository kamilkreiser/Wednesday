# READY — KS-1346-APIGWFAIL500TYPES-1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names/out.md.checker/patch.diff`** (from `ls` at 00:30 2026-10-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names/out.md.checker/section_3.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names/out.md.checker/section_4.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 00:30 2026-10-10 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ae9bf6828f88131dfcc0b410f14c2f436903eb49`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/notifications.ts , Blockchain/Dev/services/api-gateway/src/routes/batch.ts , Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1346-apigw-fail500-logs-type-and-field-names.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/notifications.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1346-apigw-fail500-logs-type-and-field-names.test.ts` (test) — equal to numstat.out's set (4 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/api-gateway/src/routes/notifications.ts
1	1	Blockchain/Dev/services/api-gateway/src/routes/batch.ts
1	1	Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
132	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1346-apigw-fail500-logs-type-and-field-names.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: notifications.ts batch.ts audit-export.ts`
- CODE_PATCH2 (rung 3, 3 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/notifications.ts`, `Blockchain/Dev/services/api-gateway/src/routes/batch.ts`, `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1346-apigw-fail500-logs-type-and-field-names.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/notifications.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/routes/batch.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1346-apigw-fail500-logs-type-and-field-names.test.ts 132 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=4 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/notifications.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/routes/batch.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- section 4 `section_4.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1346-apigw-fail500-logs-type-and-field-names.test.ts` (hunks=1, miscount=0; applied file per `section_4.opts`: `section_4.diff`, git-apply options: `(none — strict)`; `apply_check_strict_4.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (9 failed / 15 run; controls green; assertion reds)` [red_first.json: failed=9 of total=15; red cell(s): ["KS-1346 api-gateway fail500: a non-Error throw logs its type and field names, never its values RED KS-1346 G1 'notifications GET /': a thrown plain object is logged as its type and field names", "KS-1346 api-gateway fail500: a non-Error throw logs its type and field names, never its values RED KS-1346 G1 'batch POST /certifications': a thrown plain object is logged as its type and field names", "KS-1346 api-gateway fail500: a non-Error throw logs its type and field names, never its values RED KS-1346 G1 'audit GET /export': a thrown plain object is logged as its type and field names", "KS-1346 api-gateway fail500: a non-Error throw logs its type and field names, never its values RED KS-1346 G2 'notifications GET /': a thrown class instance is logged with its class name", "KS-1346 api-gateway fail500: a non-Error throw logs its type and field names, never its values RED KS-1346 G2 'batch POST /certifications': a thrown class instance is logged with its class name", "KS-1346 api-gateway fail500: a non-Error throw logs its type and field names, never its values RED KS-1346 G2 'audit GET /export': a thrown class instance is logged with its class name", "KS-1346 api-gateway fail500: a non-Error throw logs its type and field names, never its values RED KS-1346 G3 'notifications GET /': a thrown number is logged as its type", "KS-1346 api-gateway fail500: a non-Error throw logs its type and field names, never its values RED KS-1346 G3 'batch POST /certifications': a thrown number is logged as its type", "KS-1346 api-gateway fail500: a non-Error throw logs its type and field names, never its values RED KS-1346 G3 'audit GET /export': a thrown number is logged as its type"]]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 3 product section(s) (15 passed / 15 run)` [green_after.json: failed=0 of total=15, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=845 failed=0 | after: total=860 failed=0` · `NEW reds: []` [baseline_suite.json total=845 failed=0; after_suite.json total=860 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=4 products=3 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/notifications.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1346-apigw-fail500-logs-type-and-field-names.test.ts` (+132/-0); 4 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/notifications.ts, Blockchain/Dev/services/api-gateway/src/routes/batch.ts, Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict); section 4 `section_4.diff`: `git apply -p1` (strict) — at the tip `ae9bf6828f88131dfcc0b410f14c2f436903eb49` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/notifications.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/notifications.ts
@@ -24,6 +24,6 @@
  * the route named, answer the constant body.
  */
 function fail500(res: Response, context: string, err: unknown): void {
-  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+  logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });
   res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
 }
--- a/Blockchain/Dev/services/api-gateway/src/routes/batch.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/batch.ts
@@ -22,6 +22,6 @@
  * the route named, answer the constant body.
  */
 function fail500(res: Response, context: string, err: unknown): void {
-  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+  logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });
   res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
 }
--- a/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
@@ -22,6 +22,6 @@
  * the route named, answer the constant body.
  */
 function fail500(res: Response, context: string, err: unknown): void {
-  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+  logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });
   res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
 }
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1346-apigw-fail500-logs-type-and-field-names.test.ts
@@ -0,0 +1,132 @@
+/**
+ * KS-1346 (api-gateway routes/notifications.ts, routes/batch.ts, routes/audit-export.ts): the three fail500 copies
+ * #1432 added log `err instanceof Error ? err.message : String(err)`, so a thrown NON-Error object is logged as
+ * "[object Object]" and its content is lost (gate77 N-1432-2). The owner ruling of 2026-09-27 (option a, "type and
+ * field names only") is already the helper line in originate's four copies (adminConfig.ts:104 at develop
+ * e919265db717): an Error logs its message, a string logs itself, an object logs its TYPE and FIELD NAMES only, never
+ * a value, and any other primitive logs its typeof.
+ *
+ * Harness: the fake req/res dispatch of the KS-1410 api-gateway tests (the real routers, no server, no network), with
+ * the notifications router's router-wide authenticateToken replaced by a pass-through. Every route below reads
+ * req.user FIRST inside its try; the fake user's field getter throws the value under test, so it lands in fail500.
+ */
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+import type { Request, Response, Router } from 'express';
+
+const mockLoggerError = vi.hoisted(() => vi.fn());
+vi.mock('../utils/logger', () => ({
+  logger: { error: mockLoggerError, warn: vi.fn(), info: vi.fn(), debug: vi.fn() },
+}));
+vi.mock('../middleware/auth', () => ({
+  authenticateToken: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+import notificationsRouter from '../routes/notifications';
+import batchRouter from '../routes/batch';
+import auditExportRouter from '../routes/audit-export';
+
+// THE FIXTURE IS LOAD-BEARING: values that must never reach a log line.
+const SECRET_DSN = 'postgres://svc:ks1346-planted-secret@10.0.4.17:5432/app';
+const SECRET_EMAIL = 'ks1346.person@example.invalid';
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+
+type CapturedRes = Response & { _status: number; _json: unknown };
+
+function makeRes(onFinish: () => void): CapturedRes {
+  const res: any = {
+    _status: 200,
+    _json: null,
+    status(code: number) {
+      res._status = code;
+      return res;
+    },
+    json(body: unknown) {
+      res._json = body;
+      onFinish();
+      return res;
+    },
+    setHeader() {
+      return res;
+    },
+  };
+  return res;
+}
+
+function dispatch(router: Router, opts: { method: string; url: string; user?: unknown; body?: unknown }): Promise<CapturedRes> {
+  return new Promise((resolve, reject) => {
+    const res = makeRes(() => resolve(res));
+    const req = {
+      method: opts.method,
+      url: opts.url,
+      headers: {},
+      body: opts.body,
+      query: {},
+      user: opts.user,
+      get(name: string) {
+        return (this as any).headers[name?.toLowerCase()];
+      },
+    } as unknown as Request;
+    router(req, res as any, (err: unknown) => (err ? reject(err) : resolve(res)));
+  });
+}
+
+/** A req.user whose `field` getter throws `thrown` (any value, not only an Error). */
+function throwingUser(field: string, thrown: unknown): Record<string, unknown> {
+  return Object.defineProperty({}, field, {
+    enumerable: true,
+    get() {
+      throw thrown;
+    },
+  });
+}
+
+class DbFault {
+  code = 'ECONNREFUSED';
+  dsn = SECRET_DSN;
+}
+
+const ROUTES = [
+  { label: 'notifications GET /', router: notificationsRouter, method: 'GET', url: '/', field: 'userId', context: 'Notification list failed (GET /api/notifications)' },
+  { label: 'batch POST /certifications', router: batchRouter, method: 'POST', url: '/certifications', field: 'userId', context: 'Batch certify failed (POST /api/batch/certifications)' },
+  { label: 'audit GET /export', router: auditExportRouter, method: 'GET', url: '/export', field: 'role', context: 'Audit export failed (GET /api/admin/audit/export)' },
+];
+
+async function drive(route: (typeof ROUTES)[number], thrown: unknown): Promise<CapturedRes> {
+  return dispatch(route.router, { method: route.method, url: route.url, user: throwingUser(route.field, thrown), body: {} });
+}
+
+beforeEach(() => mockLoggerError.mockClear());
+
+describe('KS-1346 api-gateway fail500: a non-Error throw logs its type and field names, never its values', () => {
+  it.each(ROUTES)('RED KS-1346 G1 $label: a thrown plain object is logged as its type and field names', async (route) => {
+    const res = await drive(route, { dsn: SECRET_DSN, owner: SECRET_EMAIL });
+    expect(res._status).toBe(500);
+    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: 'thrown Object with fields [dsn, owner]' }]]);
+  });
+
+  it.each(ROUTES)('RED KS-1346 G2 $label: a thrown class instance is logged with its class name', async (route) => {
+    await drive(route, new DbFault());
+    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: 'thrown DbFault with fields [code, dsn]' }]]);
+  });
+
+  it.each(ROUTES)('RED KS-1346 G3 $label: a thrown number is logged as its type', async (route) => {
+    await drive(route, 42);
+    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: 'thrown number' }]]);
+  });
+
+  it.each(ROUTES)('control KS-1346 GC1 $label: no VALUE of a thrown object reaches the log, and the body stays constant', async (route) => {
+    const res = await drive(route, { dsn: SECRET_DSN, owner: SECRET_EMAIL });
+    const logged = JSON.stringify(mockLoggerError.mock.calls);
+    expect([logged.includes(SECRET_DSN), logged.includes(SECRET_EMAIL)]).toEqual([false, false]);
+    expect(res._json).toEqual(CONSTANT_BODY);
+  });
+
+  it.each(ROUTES)('control KS-1346 GC2 $label: an Error still logs its message, a string still logs itself', async (route) => {
+    await drive(route, new Error('ks1346-error-text'));
+    await drive(route, 'ks1346-string-text');
+    expect(mockLoggerError.mock.calls).toEqual([
+      [route.context, { error: 'ks1346-error-text' }],
+      [route.context, { error: 'ks1346-string-text' }],
+    ]);
+  });
+});
```
