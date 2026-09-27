# READY — KS-1346-KS-1346-C-ADMINCONFIG-TYPEFIELDS (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1346-C-adminconfig/out.md.checker/patch.diff`** (from `ls` at 05:06 2026-09-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1346-C-adminconfig/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1346-C-adminconfig/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1346-C-adminconfig/out.md.checker/patch.diff /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/golden_C-adminconfig/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 05:06 2026-09-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1346-C-adminconfig/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ec32c40e2b1e2698d2e855a916f390d48dad1b45`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/adminConfig.ts , Blockchain/Dev/services/originate/src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/originate/src/routes/adminConfig.ts
117	0	Blockchain/Dev/services/originate/src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/adminConfig.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts fails at the untouched tip (4 failed / 15 run; controls green; assertion reds)` [red_first.json: failed=4 of total=15; red cell(s): ['KS-1346 part C: adminConfig fail500 keeps a non-Error throw readable in the log RED KS-1346 C1 GET /settings: a thrown plain object is logged as its type and field names, once, under this route', 'KS-1346 part C: adminConfig fail500 keeps a non-Error throw readable in the log RED KS-1346 C1 GET /document-types: a thrown plain object is logged as its type and field names, once, under this route', 'KS-1346 part C: adminConfig fail500 keeps a non-Error throw readable in the log RED KS-1346 C1 GET /workflows: a thrown plain object is logged as its type and field names, once, under this route', 'KS-1346 part C: adminConfig fail500 keeps a non-Error throw readable in the log RED KS-1346 C1 GET /organizations: a thrown plain object is logged as its type and field names, once, under this route']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts passes with the product hunk (15 passed / 15 run)` [green_after.json: failed=0 of total=15, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1013 failed=0 | after: total=1028 failed=0` · `NEW reds: []` [baseline_suite.json total=1013 failed=0; after_suite.json total=1028 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +118/-1 test=src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts` (+117/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ec32c40e2b1e2698d2e855a916f390d48dad1b45` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1346-C-adminconfig/input.json`. Brief (given by --brief; its `# ` heading names KS-1346): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1346-C-adminconfig/KS-1346.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1346-C-adminconfig/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
+++ b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
@@ -101,6 +101,6 @@
  * strings is 46 chances to mislabel one, and a cell asserts the count and the distinctness.
  */
 function fail500(res: Response, context: string, err: unknown): void {
-  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+  logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });
   res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
 }
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts
@@ -0,0 +1,117 @@
+// KS-1346 part C (originate routes/adminConfig.ts): fail500 logged a NON-Error throw through String(),
+// so a thrown plain object reached the log as [object Object] and its content was lost. The 500 BODY was
+// already constant (KS-730); what this file pins is the LOG. Fifty admin-config sites go through the one
+// fail500 helper; four GET routes are driven end to end, each by making its own prisma.$queryRaw reject,
+// on a real loopback listener, exactly as the KS-730 part C cells do. Error and string throws must log
+// exactly what they logged before.
+// Kam ruled 2026-09-27 (card secuura-ks1346-logging-thrown-objects-leaks-secrets, option a): a non-Error,
+// non-string throw is logged as its TYPE and FIELD NAMES only, never its values, so no secret reaches the log.
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+const mockLoggerError = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw, $executeRaw: jest.fn() },
+  refreshTenantConfigs: jest.fn(),
+  withTenant: (_t: unknown, fn: () => unknown) => fn(),
+  getTenantManager: () => null,
+}));
+
+jest.mock('../middleware/auth', () => {
+  const actual = jest.requireActual('../middleware/auth');
+  return {
+    ...actual,
+    authenticate: () => (req: any, _res: unknown, next: () => void) => {
+      const principal = { id: 'u-ks1346c', role: 'SYSTEM_ADMIN', tenantId: 't-ks1346c' };
+      req._secuuraUser = principal; req.user = principal; req.tenantId = principal.tenantId;
+      next();
+    },
+    requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  };
+});
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    ...(jest.requireActual('@secuura/shared') as Record<string, unknown>),
+    runWithPlatformScope: (fn: () => unknown) => fn(),
+    queryWithTenantGuc: jest.fn(),
+  }),
+);
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { adminConfigRouter } from '../routes/adminConfig';
+
+const DETAIL = 'ks1346c-private-detail';
+const SECRET = 'ks1346c-secret-value';
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const ROUTES = [
+  { label: 'GET /settings', path: '/settings', context: 'Admin config request failed (GET /api/admin/settings)' },
+  { label: 'GET /document-types', path: '/document-types', context: 'Admin config request failed (GET /api/admin/document-types)' },
+  { label: 'GET /workflows', path: '/workflows', context: 'Admin config request failed (GET /api/admin/workflows)' },
+  { label: 'GET /organizations', path: '/organizations', context: 'Admin config request failed (GET /api/admin/organizations)' },
+] as const;
+
+const app = express();
+app.use('/api/admin', express.json(), adminConfigRouter);
+let server: ReturnType<typeof app.listen>;
+let baseUrl = '';
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(() => server?.close());
+beforeEach(() => jest.clearAllMocks());
+
+async function callWithThrow(route: (typeof ROUTES)[number], thrown: unknown): Promise<{ status: number; text: string; calls: unknown[][] }> {
+  mockLoggerError.mockClear();
+  mockQueryRaw.mockRejectedValueOnce(thrown);
+  const res = await fetch(baseUrl + '/api/admin' + route.path);
+  return { status: res.status, text: await res.text(), calls: mockLoggerError.mock.calls };
+}
+
+describe('KS-1346 part C: adminConfig fail500 keeps a non-Error throw readable in the log', () => {
+  it.each(ROUTES)('RED KS-1346 C1 $label: a thrown plain object is logged as its type and field names, once, under this route', async (route) => {
+    const reply = await callWithThrow(route, { code: 'KS1346C_OBJECT', detail: DETAIL, password: SECRET });
+    expect(reply.status).toBe(500);
+    expect(reply.calls.length).toBe(1);
+    const [context, meta] = reply.calls[0] as [string, { error: unknown }];
+    expect(context).toBe(route.context);
+    expect(meta.error).toBe('thrown Object with fields [code, detail, password]');
+  });
+
+  it.each(ROUTES)('control KS-1346 C6 $label: no VALUE of a thrown object reaches the log', async (route) => {
+    const reply = await callWithThrow(route, { code: 'KS1346C_OBJECT', detail: DETAIL, password: SECRET });
+    const logged = JSON.stringify(reply.calls);
+    expect({ secret: logged.includes(SECRET), detail: logged.includes(DETAIL), code: logged.includes('KS1346C_OBJECT') }).toEqual({ secret: false, detail: false, code: false });
+  });
+
+  it.each(ROUTES)('control KS-1346 C2 $label: the 500 body stays the constant text for an object throw', async (route) => {
+    const reply = await callWithThrow(route, { code: 'KS1346C_OBJECT', detail: DETAIL });
+    expect({ status: reply.status, leaked: reply.text.includes(DETAIL) }).toEqual({ status: 500, leaked: false });
+    expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+  });
+
+  it('control KS-1346 C3: an Error throw still logs exactly its message', async () => {
+    const reply = await callWithThrow(ROUTES[0], new Error(DETAIL));
+    expect(reply.calls).toEqual([[ROUTES[0].context, { error: DETAIL }]]);
+  });
+
+  it('control KS-1346 C4: a string throw still logs exactly itself, not a quoted rendering', async () => {
+    const reply = await callWithThrow(ROUTES[1], DETAIL);
+    expect(reply.calls).toEqual([[ROUTES[1].context, { error: DETAIL }]]);
+  });
+
+  it('control KS-1346 C5: String() of the thrown object really is the lossy text, so C1 is not vacuous', () => {
+    expect(String({ code: 'KS1346C_OBJECT', detail: DETAIL })).toBe('[object Object]');
+  });
+});
```
