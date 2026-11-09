# READY — KS-2015-KS-2015-O130-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2015_o130_p1_audit_export_route_accepts_only_real_yyyy_mm_dd_dates/out.md.checker/patch.diff`** (from `ls` at 09:31 2026-11-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2015_o130_p1_audit_export_route_accepts_only_real_yyyy_mm_dd_dates/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2015_o130_p1_audit_export_route_accepts_only_real_yyyy_mm_dd_dates/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2015_o130_p1_audit_export_route_accepts_only_real_yyyy_mm_dd_dates/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2015_o130_p1_audit_export_route_accepts_only_real_yyyy_mm_dd_dates-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:31 2026-11-10 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2015_o130_p1_audit_export_route_accepts_only_real_yyyy_mm_dd_dates/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `07d4218e9776a5eced016f16330983c900e94fb3`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks2015-audit-export-accepts-only-real-yyyy-mm-dd-dates.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks2015-audit-export-accepts-only-real-yyyy-mm-dd-dates.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	2	Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
92	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks2015-audit-export-accepts-only-real-yyyy-mm-dd-dates.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (5 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: audit-export.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks2015-audit-export-accepts-only-real-yyyy-mm-dd-dates.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks2015-audit-export-accepts-only-real-yyyy-mm-dd-dates.test.ts 92 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks2015-audit-export-accepts-only-real-yyyy-mm-dd-dates.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (8 failed / 11 run; controls green; assertion reds)` [red_first.json: failed=8 of total=11; red cell(s): ['KS-2015 the audit export accepts only plain YYYY-MM-DD dates that exist RED ks2015 R1 from=0 answers 400 BAD_REQUEST and never asks the security service', 'KS-2015 the audit export accepts only plain YYYY-MM-DD dates that exist RED ks2015 R1 from=1 answers 400 BAD_REQUEST and never asks the security service', 'KS-2015 the audit export accepts only plain YYYY-MM-DD dates that exist RED ks2015 R1 from=-1 answers 400 BAD_REQUEST and never asks the security service', 'KS-2015 the audit export accepts only plain YYYY-MM-DD dates that exist RED ks2015 R1 from=2026-9-1 answers 400 BAD_REQUEST and never asks the security service', 'KS-2015 the audit export accepts only plain YYYY-MM-DD dates that exist RED ks2015 R1 from=Sep 1 2026 answers 400 BAD_REQUEST and never asks the security service', 'KS-2015 the audit export accepts only plain YYYY-MM-DD dates that exist RED ks2015 R1 from=2026-09-01T00:00:00Z answers 400 BAD_REQUEST and never asks the security service', 'KS-2015 the audit export accepts only plain YYYY-MM-DD dates that exist RED ks2015 R2 to=Sep 1 2026 answers 400 BAD_REQUEST and never asks the security service', 'KS-2015 the audit export accepts only plain YYYY-MM-DD dates that exist RED ks2015 R3 2026-02-30 (matches the pattern, is not a day) answers 400 on either side']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (11 passed / 11 run)` [green_after.json: failed=0 of total=11, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1882 failed=0 | after: total=1893 failed=0` · `NEW reds: []` [baseline_suite.json total=1882 failed=0; after_suite.json total=1893 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (+5/-2 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks2015-audit-export-accepts-only-real-yyyy-mm-dd-dates.test.ts` (+92/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `07d4218e9776a5eced016f16330983c900e94fb3` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2015_o130_p1_audit_export_route_accepts_only_real_yyyy_mm_dd_dates/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2015_o130_p1_audit_export_route_accepts_only_real_yyyy_mm_dd_dates/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts b/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
@@ -100,5 +100,8 @@ function escapeCSVField(value: string | undefined | null): string {
 function formatDate(dateStr: string): string {
-  // Validate and normalize date input
+  // KS-2015: the spec declares plain YYYY-MM-DD; accept exactly that shape and only a day that exists (2026-02-30 matches the shape and would roll over to March).
+  if (!/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
+    throw new Error(`Invalid date: ${dateStr}`);
+  }
   const date = new Date(dateStr);
-  if (isNaN(date.getTime())) {
+  if (isNaN(date.getTime()) || date.toISOString().split('T')[0] !== dateStr) {
     throw new Error(`Invalid date: ${dateStr}`);
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks2015-audit-export-accepts-only-real-yyyy-mm-dd-dates.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks2015-audit-export-accepts-only-real-yyyy-mm-dd-dates.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks2015-audit-export-accepts-only-real-yyyy-mm-dd-dates.test.ts
@@ -0,0 +1,92 @@
+import { describe, it, expect, vi, beforeAll, afterAll, beforeEach } from 'vitest';
+import http from 'node:http';
+import type { AddressInfo } from 'node:net';
+import express from 'express';
+
+// KS-2015 (gate 202 G202-N3): the spec declares `from` and `to` of GET /api/admin/audit/export as plain YYYY-MM-DD dates, but the route only
+// asked `new Date(x)` and rejected NaN, so `0`, `1`, `-1`, `2026-9-1`, `Sep 1 2026`, a full ISO timestamp and the calendar-impossible `2026-02-30`
+// (which matches the pattern and rolls over to March) all answered 200. The route now accepts exactly YYYY-MM-DD naming a real calendar day.
+// Harness: the real router behind a stub admin user, the security service replaced by a stubbed global fetch (the shape of ks745's test).
+const savedEnv = { ...process.env };
+process.env.SECURITY_SERVICE_URL = 'http://security.test:1';
+
+const ENTRY = { id: 'audit-ks2015-1', tenantId: 'a0000000-0000-4000-8000-000000000001', userId: 'u1', action: 'login', resourceType: 'user', details: {}, success: true, createdAt: '2026-09-01T10:00:00.000Z' };
+const fetchMock = vi.fn(async (_input: unknown) => ({ ok: true, status: 200, json: async () => ({ success: true, data: { logs: [ENTRY], total: 1, limit: 1000, offset: 0 } }) }) as unknown as Response);
+vi.stubGlobal('fetch', fetchMock);
+
+let server: ReturnType<ReturnType<typeof express>['listen']> | undefined;
+let port = 0;
+beforeAll(async () => {
+  const { default: router } = await import('../routes/audit-export');
+  const app = express();
+  app.use((req, _res, next) => { (req as any).user = { id: 'admin-ks2015', role: 'super_admin' }; next(); });
+  app.use('/api/admin/audit', router);
+  await new Promise<void>((r) => {
+    const s = app.listen(0, '127.0.0.1', () => { port = (s.address() as AddressInfo).port; r(); });
+    server = s;
+  });
+}, 10_000);
+afterAll(async () => {
+  const s = server;
+  if (s) await new Promise<void>((r) => s.close(() => r()));
+  for (const k of Object.keys(process.env)) if (!(k in savedEnv)) delete process.env[k];
+  Object.assign(process.env, savedEnv);
+  vi.unstubAllGlobals();
+});
+beforeEach(() => { fetchMock.mockClear(); });
+
+function getText(path: string): Promise<{ status: number; text: string }> {
+  return new Promise((resolve, reject) => {
+    http.get({ hostname: '127.0.0.1', port, path }, (res) => {
+      let data = '';
+      res.on('data', (c) => (data += c));
+      res.on('end', () => resolve({ status: res.statusCode ?? 0, text: data }));
+    }).on('error', reject);
+  });
+}
+
+const exportUrl = (from: string, to: string) => `/api/admin/audit/export?format=json&from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}`;
+
+describe('KS-2015 the audit export accepts only plain YYYY-MM-DD dates that exist', () => {
+  it.each(['0', '1', '-1', '2026-9-1', 'Sep 1 2026', '2026-09-01T00:00:00Z'])('RED ks2015 R1 from=%s answers 400 BAD_REQUEST and never asks the security service', async (bad) => {
+    const res = await getText(exportUrl(bad, '2026-09-02'));
+    expect(res.status).toBe(400);
+    expect(res.text).toContain('BAD_REQUEST');
+    expect(fetchMock).not.toHaveBeenCalled();
+  });
+
+  it('RED ks2015 R2 to=Sep 1 2026 answers 400 BAD_REQUEST and never asks the security service', async () => {
+    const res = await getText(exportUrl('2026-09-01', 'Sep 1 2026'));
+    expect(res.status).toBe(400);
+    expect(res.text).toContain('BAD_REQUEST');
+    expect(fetchMock).not.toHaveBeenCalled();
+  });
+
+  it('RED ks2015 R3 2026-02-30 (matches the pattern, is not a day) answers 400 on either side', async () => {
+    const asFrom = await getText(exportUrl('2026-02-30', '2026-03-05'));
+    const asTo = await getText(exportUrl('2026-02-01', '2026-02-30'));
+    expect(asFrom.status).toBe(400);
+    expect(asTo.status).toBe(400);
+    expect(fetchMock).not.toHaveBeenCalled();
+  });
+
+  it('control ks2015 C1 20260901 and x still answer 400', async () => {
+    expect((await getText(exportUrl('20260901', '2026-09-02'))).status).toBe(400);
+    expect((await getText(exportUrl('x', '2026-09-02'))).status).toBe(400);
+  });
+
+  it('control ks2015 C2 a plain YYYY-MM-DD range still answers 200 with the entry and asks the security service', async () => {
+    const res = await getText(exportUrl('2026-09-01', '2026-09-02'));
+    expect(res.status).toBe(200);
+    const body = JSON.parse(res.text) as { meta: { from: string; to: string }; data: Array<{ id: string }> };
+    expect(body.meta.from).toBe('2026-09-01');
+    expect(body.meta.to).toBe('2026-09-02');
+    expect(body.data.map((e) => e.id)).toEqual(['audit-ks2015-1']);
+    expect(fetchMock).toHaveBeenCalledTimes(1);
+  });
+
+  it('control ks2015 C3 a real leap day, 2024-02-29, is accepted', async () => {
+    const res = await getText(exportUrl('2024-02-29', '2024-03-01'));
+    expect(res.status).toBe(200);
+  });
+});
```
