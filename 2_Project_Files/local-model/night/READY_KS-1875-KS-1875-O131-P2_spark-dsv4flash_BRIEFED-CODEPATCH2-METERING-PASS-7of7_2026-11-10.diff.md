# READY — KS-1875-KS-1875-O131-P2 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1875_o131_p2_originate_metering_usage_refuses_a_repeated_from_or_to/out.md.checker/patch.diff`** (from `ls` at 13:50 2026-11-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1875_o131_p2_originate_metering_usage_refuses_a_repeated_from_or_to/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1875_o131_p2_originate_metering_usage_refuses_a_repeated_from_or_to/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1875_o131_p2_originate_metering_usage_refuses_a_repeated_from_or_to/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1875_o131_p2_originate_metering_usage_refuses_a_repeated_from_or_to-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:50 2026-11-10 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1875_o131_p2_originate_metering_usage_refuses_a_repeated_from_or_to/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d3e663692a8f414f16610236259cab14b27ff0f7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/metering.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1875-a-repeated-from-or-to-on-metering-usage-is-refused.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/metering.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1875-a-repeated-from-or-to-on-metering-usage-is-refused.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	0	Blockchain/Dev/services/originate/src/routes/metering.ts
101	0	Blockchain/Dev/services/originate/src/__tests__/ks1875-a-repeated-from-or-to-on-metering-usage-is-refused.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: metering.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/metering.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1875-a-repeated-from-or-to-on-metering-usage-is-refused.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/metering.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1875-a-repeated-from-or-to-on-metering-usage-is-refused.test.ts 101 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/metering.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1875-a-repeated-from-or-to-on-metering-usage-is-refused.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1875 GET /api/metering/usage refuses a repeated from or to RED ks1875 R1 a repeated from answers 400 BAD_REQUEST and the usage query is never made', 'KS-1875 GET /api/metering/usage refuses a repeated from or to RED ks1875 R2 a repeated to answers 400 BAD_REQUEST and the usage query is never made', 'KS-1875 GET /api/metering/usage refuses a repeated from or to RED ks1875 R3 a repeated from next to a single valid to is still refused, not read as an open lower bound']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2592 failed=11 | after: total=2598 failed=11` · `NEW reds: []` [baseline_suite.json total=2592 failed=11; after_suite.json total=2598 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/metering.ts` (+7/-0 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1875-a-repeated-from-or-to-on-metering-usage-is-refused.test.ts` (+101/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/metering.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d3e663692a8f414f16610236259cab14b27ff0f7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1875_o131_p2_originate_metering_usage_refuses_a_repeated_from_or_to/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1875_o131_p2_originate_metering_usage_refuses_a_repeated_from_or_to/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/metering.ts b/Blockchain/Dev/services/originate/src/routes/metering.ts
--- a/Blockchain/Dev/services/originate/src/routes/metering.ts
+++ b/Blockchain/Dev/services/originate/src/routes/metering.ts
@@ -117,3 +117,10 @@
     const from = typeof req.query.from === 'string' ? req.query.from : undefined;
     const to = typeof req.query.to === 'string' ? req.query.to : undefined;
+    // KS-1875: a repeated from or to (Express parses it as an array) is refused, not read as an open bound.
+    if (Array.isArray(req.query.from) || Array.isArray(req.query.to)) {
+      return res.status(400).json({
+        success: false,
+        error: { code: 'BAD_REQUEST', message: 'from and to may each be given once' },
+      });
+    }
     if ((from && !ISO_DATE.test(from)) || (to && !ISO_DATE.test(to))) {
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1875-a-repeated-from-or-to-on-metering-usage-is-refused.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1875-a-repeated-from-or-to-on-metering-usage-is-refused.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1875-a-repeated-from-or-to-on-metering-usage-is-refused.test.ts
@@ -0,0 +1,101 @@
+// KS-1875 (originate routes/metering.ts, GET /api/metering/usage): the handler read `req.query.from` / `req.query.to` only when they are strings, so a REPEATED
+// parameter (?from=a&from=b, which Express parses as an array) was dropped as if it had not been sent, and the call answered 200 with that bound OPEN: a wider read
+// than the caller asked for. A repeated from or to is now refused with the route's own 400 BAD_REQUEST shape and the usage query is never made. The route is read-only.
+// Harness: the real router on a loopback listener; the charge-event service, the authenticator, the gateway-provenance check and the logger are stand-ins (no database).
+const mockGetUsageSummary = jest.fn();
+
+jest.mock('../services/chargeEvents', () => ({
+  getUsageSummary: mockGetUsageSummary,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user = { userId: 'user-ks1875' };
+    next();
+  },
+}));
+
+jest.mock('../utils/gatewayProvenance', () => ({
+  isGatewayVouched: () => false,
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { meteringRouter } from '../routes/metering';
+
+const DEFAULT_TENANT = 'a0000000-0000-4000-8000-000000000001';
+const SUMMARY = { tenantId: DEFAULT_TENANT, byEventType: [], totals: { count: 0, adaTotal: 0, usdTotal: 0 } };
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
+beforeEach(() => {
+  jest.clearAllMocks();
+  mockGetUsageSummary.mockResolvedValue(SUMMARY);
+});
+
+async function getUsage(query: string): Promise<{ status: number | 'NO ANSWER'; body: any }> {
+  try {
+    const res = await fetch(baseUrl + '/api/metering/usage' + query, { signal: AbortSignal.timeout(1500) });
+    return { status: res.status, body: await res.json() };
+  } catch {
+    return { status: 'NO ANSWER', body: null };
+  }
+}
+
+describe('KS-1875 GET /api/metering/usage refuses a repeated from or to', () => {
+  it('RED ks1875 R1 a repeated from answers 400 BAD_REQUEST and the usage query is never made', async () => {
+    const r = await getUsage('?from=2026-01-01&from=2026-02-01');
+    expect(r.status).toBe(400);
+    expect(r.body.success).toBe(false);
+    expect(r.body.error.code).toBe('BAD_REQUEST');
+    expect(mockGetUsageSummary).not.toHaveBeenCalled();
+  });
+
+  it('RED ks1875 R2 a repeated to answers 400 BAD_REQUEST and the usage query is never made', async () => {
+    const r = await getUsage('?to=2026-01-01&to=2026-02-01');
+    expect(r.status).toBe(400);
+    expect(r.body.error.code).toBe('BAD_REQUEST');
+    expect(mockGetUsageSummary).not.toHaveBeenCalled();
+  });
+
+  it('RED ks1875 R3 a repeated from next to a single valid to is still refused, not read as an open lower bound', async () => {
+    const r = await getUsage('?from=2026-01-01&from=2026-01-15&to=2026-03-01');
+    expect(r.status).toBe(400);
+    expect(mockGetUsageSummary).not.toHaveBeenCalled();
+  });
+
+  it('control ks1875 C1 a single from and a single to are read and passed to the usage query', async () => {
+    const r = await getUsage('?from=2026-01-01&to=2026-02-01');
+    expect(r.status).toBe(200);
+    expect(r.body.success).toBe(true);
+    expect(mockGetUsageSummary).toHaveBeenCalledTimes(1);
+    expect(mockGetUsageSummary).toHaveBeenCalledWith(DEFAULT_TENANT, '2026-01-01', '2026-02-01');
+  });
+
+  it('control ks1875 C2 no from and no to is an open window and is answered 200', async () => {
+    const r = await getUsage('');
+    expect(r.status).toBe(200);
+    expect(mockGetUsageSummary).toHaveBeenCalledWith(DEFAULT_TENANT, undefined, undefined);
+  });
+
+  it('control ks1875 C3 a single value that is not a date is still refused by the existing guard', async () => {
+    const r = await getUsage('?from=notadate');
+    expect(r.status).toBe(400);
+    expect(r.body.error.code).toBe('BAD_REQUEST');
+    expect(mockGetUsageSummary).not.toHaveBeenCalled();
+  });
+});
```
