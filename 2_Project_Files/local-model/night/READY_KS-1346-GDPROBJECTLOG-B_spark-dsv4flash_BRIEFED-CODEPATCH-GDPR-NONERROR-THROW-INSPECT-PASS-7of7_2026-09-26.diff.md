# READY — KS-1346-GDPROBJECTLOG-B (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1346-B/out.md.checker/patch.diff`** (from `ls` at 22:03 2026-09-26; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1346-B/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1346-B/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 22:03 2026-09-26 by Wednesday evening seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1346-B/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3f70224a069b944334480478ad5d16a5ed33eeae`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/gdpr.ts , Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/gdpr.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	1	Blockchain/Dev/services/originate/src/routes/gdpr.ts
95	0	Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/gdpr.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/gdpr.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts fails at the untouched tip (4 failed / 11 run; controls green; assertion reds)` [red_first.json: failed=4 of total=11; red cell(s): ['KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log RED KS-1346 B1 GET /dsr/pending: a thrown plain object is logged with its content, once, under this route', 'KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log RED KS-1346 B1 GET /retention: a thrown plain object is logged with its content, once, under this route', 'KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log RED KS-1346 B1 GET /deletion-log: a thrown plain object is logged with its content, once, under this route', 'KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log RED KS-1346 B1 GET /consent/check: a thrown plain object is logged with its content, once, under this route']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts passes with the product hunk (11 passed / 11 run)` [green_after.json: failed=0 of total=11, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=962 failed=0 | after: total=973 failed=0` · `NEW reds: []` [baseline_suite.json total=962 failed=0; after_suite.json total=973 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +97/-1 test=src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/gdpr.ts` (+2/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts` (+95/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3f70224a069b944334480478ad5d16a5ed33eeae` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1346-B/input.json`. Brief (given by --brief; its `# ` heading names KS-1346): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1346-B/KS-1346.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1346-B/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/gdpr.ts
+++ b/Blockchain/Dev/services/originate/src/routes/gdpr.ts
@@ -15,2 +15,3 @@
 import { z } from 'zod';
+import { inspect } from 'util';
 import * as gdpr from '../services/gdprService';
@@ -210,3 +211,3 @@
 function fail500(res: Response, context: string, err: unknown): void {
-  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+  logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : inspect(err) });
   res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts
@@ -0,0 +1,95 @@
+// KS-1346 part B (originate routes/gdpr.ts): fail500 logged a NON-Error throw through String(), so a
+// thrown plain object reached the log as [object Object] and its content was lost. The 500 BODY was
+// already constant (KS-730); what this file pins is the LOG. Four GDPR routes that reach their service
+// with nothing to satisfy first are driven by making ITS OWN service call reject, on a real loopback
+// listener, exactly as the KS-730 part B cells do. Error and string throws must log exactly what they
+// logged before.
+const mockGetPendingDSRs = jest.fn();
+const mockGetRetentionPolicies = jest.fn();
+const mockGetDeletionLog = jest.fn();
+const mockHasValidConsent = jest.fn();
+const mockLoggerError = jest.fn();
+
+jest.mock('../services/gdprService', () => ({
+  getPendingDSRs: mockGetPendingDSRs,
+  getRetentionPolicies: mockGetRetentionPolicies,
+  getDeletionLog: mockGetDeletionLog,
+  hasValidConsent: mockHasValidConsent,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireSelfOrRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  hasAnyRole: () => true,
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { gdprRouter } from '../routes/gdpr';
+
+const DETAIL = 'ks1346b-private-detail';
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const ROUTES = [
+  { label: 'GET /dsr/pending', path: '/dsr/pending', mock: mockGetPendingDSRs, context: 'GDPR pending DSR list failed (GET /api/gdpr/dsr/pending)' },
+  { label: 'GET /retention', path: '/retention', mock: mockGetRetentionPolicies, context: 'GDPR retention policy read failed (GET /api/gdpr/retention)' },
+  { label: 'GET /deletion-log', path: '/deletion-log', mock: mockGetDeletionLog, context: 'GDPR deletion log read failed (GET /api/gdpr/deletion-log)' },
+  { label: 'GET /consent/check', path: '/consent/check?userId=u-ks1346b&purpose=MARKETING', mock: mockHasValidConsent, context: 'GDPR consent check failed (GET /api/gdpr/consent/check)' },
+] as const;
+
+const app = express();
+app.use('/api/gdpr', express.json(), gdprRouter);
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
+  route.mock.mockRejectedValueOnce(thrown);
+  const res = await fetch(baseUrl + '/api/gdpr' + route.path, { method: 'GET' });
+  return { status: res.status, text: await res.text(), calls: mockLoggerError.mock.calls };
+}
+
+describe('KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log', () => {
+  it.each(ROUTES)('RED KS-1346 B1 $label: a thrown plain object is logged with its content, once, under this route', async (route) => {
+    const reply = await callWithThrow(route, { code: 'KS1346B_OBJECT', detail: DETAIL });
+    expect(reply.status).toBe(500);
+    expect(reply.calls.length).toBe(1);
+    const [context, meta] = reply.calls[0] as [string, { error: unknown }];
+    expect(context).toBe(route.context);
+    expect(typeof meta.error).toBe('string');
+    expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346B_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
+  });
+
+  it.each(ROUTES)('control KS-1346 B2 $label: the 500 body stays the constant text for an object throw', async (route) => {
+    const reply = await callWithThrow(route, { code: 'KS1346B_OBJECT', detail: DETAIL });
+    expect({ status: reply.status, leaked: reply.text.includes(DETAIL) }).toEqual({ status: 500, leaked: false });
+    expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+  });
+
+  it('control KS-1346 B3: an Error throw still logs exactly its message', async () => {
+    const reply = await callWithThrow(ROUTES[0], new Error(DETAIL));
+    expect(reply.calls).toEqual([[ROUTES[0].context, { error: DETAIL }]]);
+  });
+
+  it('control KS-1346 B4: a string throw still logs exactly itself, not a quoted rendering', async () => {
+    const reply = await callWithThrow(ROUTES[1], DETAIL);
+    expect(reply.calls).toEqual([[ROUTES[1].context, { error: DETAIL }]]);
+  });
+
+  it('control KS-1346 B5: String() of the thrown object really is the lossy text, so B1 is not vacuous', () => {
+    expect(String({ code: 'KS1346B_OBJECT', detail: DETAIL })).toBe('[object Object]');
+  });
+});
```
