# READY — KS-1868-KS-1868-O63-P1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o63_p1_originate_system_errors_ingest_client_errors_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 08:36 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o63_p1_originate_system_errors_ingest_client_errors_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o63_p1_originate_system_errors_ingest_client_errors_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o63_p1_originate_system_errors_ingest_client_errors_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o63_p1_originate_system_errors_ingest_client_errors_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:36 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o63_p1_originate_system_errors_ingest_client_errors_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/systemErrors.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/systemErrors.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	4	Blockchain/Dev/services/originate/src/routes/systemErrors.ts
107	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (2 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: systemErrors.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/systemErrors.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/systemErrors.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts 107 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/systemErrors.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=4 of total=8; red cell(s): ['KS-1868 POST /ingest catch reads the thrown value safely RED ks1868 R1 POST /ingest: a revoked Proxy thrown by the service is logged as a constant reason and answered with the constant 500', 'KS-1868 POST /ingest catch reads the thrown value safely RED ks1868 R2 POST /ingest: an Error whose message getter throws is logged as a constant reason and answered with the constant 500', 'KS-1868 POST /client-errors catch reads the thrown value safely RED ks1868 R1 POST /client-errors: a revoked Proxy thrown by the service is logged as a constant reason and answered with the constant 500', 'KS-1868 POST /client-errors catch reads the thrown value safely RED ks1868 R2 POST /client-errors: an Error whose message getter throws is logged as a constant reason and answered with the constant 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1999 failed=0 | after: total=2007 failed=0` · `NEW reds: []` [baseline_suite.json total=1999 failed=0; after_suite.json total=2007 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/systemErrors.ts` (+2/-4 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts` (+107/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/systemErrors.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o63_p1_originate_system_errors_ingest_client_errors_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o63_p1_originate_system_errors_ingest_client_errors_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o63_p1_originate_system_errors_ingest_client_errors_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/systemErrors.ts b/Blockchain/Dev/services/originate/src/routes/systemErrors.ts
--- a/Blockchain/Dev/services/originate/src/routes/systemErrors.ts
+++ b/Blockchain/Dev/services/originate/src/routes/systemErrors.ts
@@ -132,6 +132,5 @@
     res.status(201).json({ success: true });
   } catch (err: any) {
-    logger.error('System error ingest failed', { error: err instanceof Error ? err.message : String(err) });
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
+    fail500(res, 'System error ingest failed', err);
   }
 });
@@ -163,6 +162,5 @@
     res.status(201).json({ success: true });
   } catch (err: any) {
-    logger.error('Client error ingest failed', { error: err instanceof Error ? err.message : String(err) });
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
+    fail500(res, 'Client error ingest failed', err);
   }
 });
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts
@@ -0,0 +1,107 @@
+// KS-1868 (originate routes/systemErrors.ts, POST /api/system-errors/ingest and POST /api/system-errors/client-errors): both catch blocks logged `err instanceof Error ? err.message : String(err)`
+// themselves and then answered the constant 500. When the thrown value cannot be read (a revoked Proxy makes `instanceof` throw; an Error whose `message` getter throws), that read threw INSIDE the
+// catch: the handler's promise rejected and the request got NO answer. Both catches now go through the file's own `fail500` helper (KS-730 / KS-1772), which describes the value in its own try and
+// always sends the constant 500. The service call is made to reject on a real loopback listener, as the KS-730 part A and KS-1780 cells do; a request that gets no answer within the window is
+// reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
+const mockTrackError = jest.fn();
+const mockLoggerError = jest.fn();
+
+jest.mock('../services/errorTrackingService', () => ({
+  trackError: mockTrackError,
+  resolveErrorsByService: jest.fn(),
+  getErrorStats: jest.fn(),
+  getRecentErrors: jest.fn(),
+  resolveError: jest.fn(),
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { systemErrorsRouter } from '../routes/systemErrors';
+
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const UNDESCRIBABLE = 'thrown value that could not be described';
+
+const ROUTES = [
+  { route: 'POST /ingest', path: '/ingest', body: { service: 'ks1868-svc', message: 'ks1868 reported error' }, context: 'System error ingest failed' },
+  { route: 'POST /client-errors', path: '/client-errors', body: { error: 'ks1868 render error', source: 'ks1868-frontend' }, context: 'Client error ingest failed' },
+];
+
+const app = express();
+app.use('/api/system-errors', express.json(), systemErrorsRouter);
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
+async function postWithThrow(path: string, body: object, thrown: unknown): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
+  mockTrackError.mockRejectedValueOnce(thrown);
+  try {
+    const res = await fetch(baseUrl + '/api/system-errors' + path, {
+      method: 'POST',
+      headers: { 'content-type': 'application/json' },
+      body: JSON.stringify(body),
+      signal: AbortSignal.timeout(1500),
+    });
+    return { status: res.status, body: await res.json() };
+  } catch {
+    return { status: 'NO ANSWER', body: null };
+  }
+}
+
+function revokedProxy(): object {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+}
+
+function throwingMessageError(): Error {
+  const e = new Error('ks1868 hidden');
+  Object.defineProperty(e, 'message', {
+    get() {
+      throw new Error('ks1868 message getter');
+    },
+  });
+  return e;
+}
+
+describe.each(ROUTES)('KS-1868 $route catch reads the thrown value safely', (c) => {
+  it(`RED ks1868 R1 ${c.route}: a revoked Proxy thrown by the service is logged as a constant reason and answered with the constant 500`, async () => {
+    const reply = await postWithThrow(c.path, c.body, revokedProxy());
+    expect(reply).toEqual({ status: 500, body: CONSTANT_BODY });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: UNDESCRIBABLE }]]);
+  });
+
+  it(`RED ks1868 R2 ${c.route}: an Error whose message getter throws is logged as a constant reason and answered with the constant 500`, async () => {
+    const reply = await postWithThrow(c.path, c.body, throwingMessageError());
+    expect(reply).toEqual({ status: 500, body: CONSTANT_BODY });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: UNDESCRIBABLE }]]);
+  });
+
+  it(`control ks1868 C1 ${c.route}: an ordinary Error logs its own message and the answer is the constant 500 without it`, async () => {
+    const reply = await postWithThrow(c.path, c.body, new Error('ks1868 ordinary'));
+    expect(reply).toEqual({ status: 500, body: CONSTANT_BODY });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'ks1868 ordinary' }]]);
+  });
+
+  it(`control ks1868 C2 ${c.route}: a thrown string is logged as itself, as before`, async () => {
+    const reply = await postWithThrow(c.path, c.body, 'ks1868 plain string');
+    expect(reply).toEqual({ status: 500, body: CONSTANT_BODY });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'ks1868 plain string' }]]);
+  });
+});
```
