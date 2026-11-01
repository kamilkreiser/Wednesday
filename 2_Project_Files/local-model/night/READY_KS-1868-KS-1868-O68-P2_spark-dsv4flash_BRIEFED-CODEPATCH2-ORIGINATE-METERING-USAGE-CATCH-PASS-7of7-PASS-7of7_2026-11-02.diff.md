# READY — KS-1868-KS-1868-O68-P2 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p2_originate_metering_usage_catch_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 09:43 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p2_originate_metering_usage_catch_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p2_originate_metering_usage_catch_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p2_originate_metering_usage_catch_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p2_originate_metering_usage_catch_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:43 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p2_originate_metering_usage_catch_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `cde2dee4dffba6a61228c40d641ff567660c32b2`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/metering.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-metering-usage-catch-p2-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/metering.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-metering-usage-catch-p2-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/originate/src/routes/metering.ts
105	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-metering-usage-catch-p2-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: metering.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/metering.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-metering-usage-catch-p2-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/metering.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-metering-usage-catch-p2-unreadable-throw.test.ts 105 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/metering.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-metering-usage-catch-p2-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1868 GET /api/metering/usage reads the thrown value safely RED ks1868 R1 usage: a revoked Proxy thrown by the query is logged as a constant reason and the constant 500 is answered', 'KS-1868 GET /api/metering/usage reads the thrown value safely RED ks1868 R2 usage: an Error whose message getter throws is logged as a constant reason and the constant 500 is answered']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1999 failed=0 | after: total=2004 failed=0` · `NEW reds: []` [baseline_suite.json total=1999 failed=0; after_suite.json total=2004 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/metering.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-metering-usage-catch-p2-unreadable-throw.test.ts` (+105/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/metering.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `cde2dee4dffba6a61228c40d641ff567660c32b2` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p2_originate_metering_usage_catch_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o68_p2_originate_metering_usage_catch_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p2_originate_metering_usage_catch_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/metering.ts b/Blockchain/Dev/services/originate/src/routes/metering.ts
--- a/Blockchain/Dev/services/originate/src/routes/metering.ts
+++ b/Blockchain/Dev/services/originate/src/routes/metering.ts
@@ -126,7 +126,13 @@
     const summary = await getUsageSummary(reqTenantId(req), from, to);
     return res.json({ success: true, data: summary });
   } catch (error) {
-    logger.error('Failed to read metering usage', { error: error instanceof Error ? error.message : String(error) });
+    let reason: string;
+    try {
+      reason = error instanceof Error ? error.message : String(error);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('Failed to read metering usage', { error: reason });
     return res
       .status(500)
       .json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to read usage' } });
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-metering-usage-catch-p2-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-metering-usage-catch-p2-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-metering-usage-catch-p2-unreadable-throw.test.ts
@@ -0,0 +1,105 @@
+// KS-1868 (originate routes/metering.ts, GET /api/metering/usage): the catch of the usage route logged the thrown value as `error instanceof Error ? error.message : String(error)` and then answered the
+// constant 500 `Failed to read usage`. When the usage query rejects with a value that cannot be read (a revoked Proxy makes `instanceof` throw; an Error whose `message` getter throws), the read threw INSIDE
+// the catch: the handler's promise rejected, Express 4 does not catch that, and the request got NO answer. The catch now reads the same expression into a local inside its own try and logs the constant
+// reason `unreadable thrown value`; the answer is the same constant 500 an ordinary Error already gets. The route is read-only (it only reads recorded usage); nothing is written. The service call is made to
+// reject on a real loopback listener; a request that gets no answer within the window is reported as NO ANSWER so a hang is a red assertion and not a stuck run.
+const mockGetUsageSummary = jest.fn();
+const mockLoggerError = jest.fn();
+
+jest.mock('../services/chargeEvents', () => ({
+  getUsageSummary: mockGetUsageSummary,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user = { userId: 'user-ks1868' };
+    next();
+  },
+}));
+
+jest.mock('../utils/gatewayProvenance', () => ({
+  isGatewayVouched: () => false,
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { meteringRouter } from '../routes/metering';
+
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to read usage' } };
+
+const app = express();
+app.use('/api/metering', meteringRouter);
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
+async function getUsage(): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
+  try {
+    const res = await fetch(baseUrl + '/api/metering/usage', { signal: AbortSignal.timeout(1500) });
+    return { status: res.status, body: await res.json() };
+  } catch {
+    return { status: 'NO ANSWER', body: null };
+  }
+}
+
+async function usageWithThrow(thrown: unknown): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
+  mockGetUsageSummary.mockRejectedValueOnce(thrown);
+  return getUsage();
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
+describe('KS-1868 GET /api/metering/usage reads the thrown value safely', () => {
+  it('RED ks1868 R1 usage: a revoked Proxy thrown by the query is logged as a constant reason and the constant 500 is answered', async () => {
+    expect(await usageWithThrow(revokedProxy())).toEqual({ status: 500, body: CONSTANT_BODY });
+    expect(mockLoggerError.mock.calls).toEqual([['Failed to read metering usage', { error: 'unreadable thrown value' }]]);
+  });
+
+  it('RED ks1868 R2 usage: an Error whose message getter throws is logged as a constant reason and the constant 500 is answered', async () => {
+    expect(await usageWithThrow(throwingMessageError())).toEqual({ status: 500, body: CONSTANT_BODY });
+    expect(mockLoggerError.mock.calls).toEqual([['Failed to read metering usage', { error: 'unreadable thrown value' }]]);
+  });
+
+  it('control ks1868 C1 usage: an ordinary Error logs its own message and the constant 500 is answered', async () => {
+    expect(await usageWithThrow(new Error('ks1868 ordinary'))).toEqual({ status: 500, body: CONSTANT_BODY });
+    expect(mockLoggerError.mock.calls).toEqual([['Failed to read metering usage', { error: 'ks1868 ordinary' }]]);
+  });
+
+  it('control ks1868 C2 usage: a thrown string is logged as itself, as before', async () => {
+    expect(await usageWithThrow('ks1868 plain string')).toEqual({ status: 500, body: CONSTANT_BODY });
+    expect(mockLoggerError.mock.calls).toEqual([['Failed to read metering usage', { error: 'ks1868 plain string' }]]);
+  });
+
+  it('control ks1868 C3 usage: a successful read answers 200 with the summary and logs no error', async () => {
+    const summary = { tenantId: 't', from: null, to: null, byEventType: [], totals: { count: 0, adaTotal: 0, usdTotal: 0 } };
+    mockGetUsageSummary.mockResolvedValueOnce(summary);
+    expect(await getUsage()).toEqual({ status: 200, body: { success: true, data: summary } });
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+});
```
