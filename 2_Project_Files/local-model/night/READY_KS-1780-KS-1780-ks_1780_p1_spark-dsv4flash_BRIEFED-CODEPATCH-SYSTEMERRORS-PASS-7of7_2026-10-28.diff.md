# READY — KS-1780-KS-1780-ks_1780_p1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p1/out.md.checker/patch.diff`** (from `ls` at 13:50 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:50 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8894c7486f82f6eb682fecb879791f53312537b1`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/systemErrors.ts , Blockchain/Dev/services/originate/src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/systemErrors.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
13	1	Blockchain/Dev/services/originate/src/routes/systemErrors.ts
83	0	Blockchain/Dev/services/originate/src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (12 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 13 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/systemErrors.ts byte-exact incl. leading whitespace (apply mode strict): OK 12 line(s) byte-exact incl. leading whitespace (of 12; 13 line(s) added by the apply)` [a3i_indent.out: `OK 12 line(s) byte-exact incl. leading whitespace (of 12; 13 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/systemErrors.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1780: GET /api/system-errors answers a hostile thrown value RED KS-1780 R1 a revoked Proxy thrown by the service is answered with the constant 500', 'KS-1780: GET /api/system-errors answers a hostile thrown value RED KS-1780 R2 a Proxy whose getPrototypeOf trap throws is answered with the constant 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1690 failed=0 | after: total=1694 failed=0` · `NEW reds: []` [baseline_suite.json total=1690 failed=0; after_suite.json total=1694 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +96/-1 test=src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/systemErrors.ts` (+13/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts` (+83/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8894c7486f82f6eb682fecb879791f53312537b1` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1780_p1/KS-1780.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/systemErrors.ts b/Blockchain/Dev/services/originate/src/routes/systemErrors.ts
--- a/Blockchain/Dev/services/originate/src/routes/systemErrors.ts
+++ b/Blockchain/Dev/services/originate/src/routes/systemErrors.ts
@@ -181,3 +181,15 @@
+/**
+ * KS-1780: `err instanceof z.ZodError` reads the thrown value's prototype. A revoked Proxy, or a Proxy whose getPrototypeOf trap throws, makes THAT check throw from inside the catch, before
+ * fail500 is reached, so the handler's promise rejects and the request gets no response at all (the KS-1772 shape, one step earlier). A value that cannot be inspected is not a ZodError.
+ */
+function isZodError(err: unknown): err is z.ZodError {
+  try {
+    return err instanceof z.ZodError;
+  } catch {
+    return false;
+  }
+}
+
 /** List errors with optional filters — admin only (dev: open) */
 systemErrorsRouter.get('/', authenticate(), requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'), async (req: Request, res: Response) => {
   try {
@@ -194,6 +206,6 @@
     res.json({ success: true, ...result });
   } catch (err: any) {
-    if (err instanceof z.ZodError) {
+    if (isZodError(err)) {
       return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid query parameters', details: err.errors } });
     }
     fail500(res, 'Error list read failed (GET /api/system-errors)', err);
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts
@@ -0,0 +1,83 @@
+// KS-1780 (originate routes/systemErrors.ts, GET /api/system-errors): the catch of the list route tested `err instanceof z.ZodError` BEFORE it reached fail500. That check reads the thrown
+// value's prototype, so a revoked Proxy, or a Proxy whose getPrototypeOf trap throws, made the check itself throw inside the catch: the handler's promise rejected and the request got NO
+// answer. fail500 already survives such a value (KS-1772); this file pins that the list route's own check does too. The service call is made to reject on a real loopback listener, as the
+// KS-1346 part A cells do; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
+const mockGetRecentErrors = jest.fn();
+
+jest.mock('../services/errorTrackingService', () => ({
+  trackError: jest.fn(),
+  resolveErrorsByService: jest.fn(),
+  getErrorStats: jest.fn(),
+  getRecentErrors: mockGetRecentErrors,
+  resolveError: jest.fn(),
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { systemErrorsRouter } from '../routes/systemErrors';
+
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
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
+async function listWithThrow(thrown: unknown, query = ''): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
+  mockGetRecentErrors.mockRejectedValueOnce(thrown);
+  try {
+    const res = await fetch(baseUrl + '/api/system-errors/' + query, { signal: AbortSignal.timeout(1500) });
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
+function throwingPrototypeTrap(): object {
+  return new Proxy({}, { getPrototypeOf() { throw new Error('ks1780 trap'); } });
+}
+
+describe('KS-1780: GET /api/system-errors answers a hostile thrown value', () => {
+  it('RED KS-1780 R1 a revoked Proxy thrown by the service is answered with the constant 500', async () => {
+    expect(await listWithThrow(revokedProxy())).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it('RED KS-1780 R2 a Proxy whose getPrototypeOf trap throws is answered with the constant 500', async () => {
+    expect(await listWithThrow(throwingPrototypeTrap())).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it('CONTROL KS-1780 C1 a plain Error is still answered with the constant 500', async () => {
+    expect(await listWithThrow(new Error('ks1780 ordinary'))).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it('CONTROL KS-1780 C2 a bad query is still a 400 BAD_REQUEST from the ZodError arm, and the service is not called', async () => {
+    const reply = await listWithThrow(new Error('unused'), '?limit=abc');
+    expect(reply.status).toBe(400);
+    expect((reply.body as { error: { code: string } }).error.code).toBe('BAD_REQUEST');
+    expect(mockGetRecentErrors).not.toHaveBeenCalled();
+  });
+});
```
