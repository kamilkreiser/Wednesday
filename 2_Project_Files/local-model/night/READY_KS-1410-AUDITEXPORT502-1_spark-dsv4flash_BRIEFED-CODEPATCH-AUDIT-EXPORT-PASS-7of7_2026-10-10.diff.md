# READY — KS-1410-AUDITEXPORT502-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-apigw-audit-export-502-loose/out.md.checker/patch.diff`** (from `ls` at 00:30 2026-10-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-apigw-audit-export-502-loose/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-apigw-audit-export-502-loose/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts: --recount --ignore-whitespace needed; miscounted hunks=1; strict rc=128]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts): `error: corrupt patch at line 15` (apply with the options recorded in section_<k>.opts; the raise seat states which); CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-apigw-audit-export-502-loose-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in audit-export.ts (run 11 vs golden 13 body lines — context, since the change lines are equal) (identical in ks1410-audit-export-502-never-answers-err-message.test.ts); hunk headers differ (audit-export.ts: golden `@@ -168,11 +168,12 @@` vs run `@@ -170,10 +170,11 @@`); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 00:30 2026-10-10 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-apigw-audit-export-502-loose/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ae9bf6828f88131dfcc0b410f14c2f436903eb49`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-audit-export-502-never-answers-err-message.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-audit-export-502-never-answers-err-message.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	1	Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
132	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-audit-export-502-never-answers-err-message.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `[no PASS A3c line in checker.out — LOOSE BRIEF declared by `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1410-apigw-audit-export-502-loose/KS-1410.md` (`Rung: **4** (a LOOSER brief`); checker.out INFO A3i verbatim: `INFO A3i skipped — the input carries no expected '+' lines (a legacy or brief-less input); indentation not measured`]` — no expected_plus in the input; not re-measured here.
- A3i line absent from checker.out (not claimed)
- **LOOSE BRIEF: product lines written by the model, not byte-checked against the brief; reviewer reads the hunk.** Declared by `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1410-apigw-audit-export-502-loose/KS-1410.md` (`Rung: **4** (a LOOSER brief`); checker.out has `INFO A3i skipped` (no expected '+' lines) and no PASS A3c; A4-A7 passed (below). Golden comparison, as reported: CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-apigw-audit-export-502-loose-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in audit-export.ts (run 11 vs golden 13 body lines — context, since the change lines are equal) (identical in ks1410-audit-export-502-never-answers-err-message.test.ts); hunk headers differ (audit-export.ts: golden `@@ -168,11 +168,12 @@` vs run `@@ -170,10 +170,11 @@`); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content). Run's own golden_cmp.out [verbatim]: `golden tree d8c4f1e620e75e57cefca3675a06cec8fe79d858 · patch tree not-built -> DIFFERS (logs /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-10_KS-1410-apigw-audit-export-502-loose_002021/*_cmp.index.out)`. A DIFFERS verdict is expected and acceptable for a loose brief — the verdict is A4-A7 plus the reviewer's read of the product hunk.
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `section 1 Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts: hunk 1 (@@ -170,10 +170,11 @@) declared old=10 new=11 but actual old=9 new=10`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (hunks=1, miscount=1; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace`; `apply_check_strict_1.out`: NON-EMPTY: `error: corrupt patch at line 15`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-audit-export-502-never-answers-err-message.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1410-audit-export-502-never-answers-err-message.test.ts fails at the untouched tip (5 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=5 of total=8; red cell(s): ['KS-1410 N-1432-1 audit export: an unreachable security service answers 502 without the thrown text RED KS-1410 X1 NODE_ENV=production: the 502 body does not carry the thrown text', 'KS-1410 N-1432-1 audit export: an unreachable security service answers 502 without the thrown text RED KS-1410 X1 NODE_ENV=development: the 502 body does not carry the thrown text', 'KS-1410 N-1432-1 audit export: an unreachable security service answers 502 without the thrown text RED KS-1410 X1 NODE_ENV=test: the 502 body does not carry the thrown text', 'KS-1410 N-1432-1 audit export: an unreachable security service answers 502 without the thrown text RED KS-1410 X2: the thrown text is logged server-side', 'KS-1410 N-1432-1 audit export: an unreachable security service answers 502 without the thrown text RED KS-1410 X3: the 502 body is the same constant for two different thrown texts']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1410-audit-export-502-never-answers-err-message.test.ts passes with the product hunk (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=845 failed=0 | after: total=853 failed=0` · `NEW reds: []` [baseline_suite.json total=845 failed=0; after_suite.json total=853 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +134/-1 test=src/__tests__/ks1410-audit-export-502-never-answers-err-message.test.ts red_first=yes apply_mode=lenient`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (+2/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-audit-export-502-never-answers-err-message.test.ts` (+132/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ae9bf6828f88131dfcc0b410f14c2f436903eb49` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-apigw-audit-export-502-loose/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-apigw-audit-export-502-loose/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
@@ -170,10 +170,11 @@
     } catch (err: any) {
+      logger.error('Audit export could not reach the security service (GET /api/admin/audit/export)', { error: err instanceof Error ? err.message : String(err) });
       res.status(502).json({
         success: false,
         error: {
           code: 'BAD_GATEWAY',
-          message: `Failed to reach security service: ${err.message}`,
+          message: 'Failed to reach security service',
         },
       });
       return;
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-audit-export-502-never-answers-err-message.test.ts
@@ -0,0 +1,132 @@
+/**
+ * KS-1410 gate77 N-1432-1 (api-gateway routes/audit-export.ts): when the fetch to the security service THROWS, the
+ * catch answered a 502 whose message interpolated the thrown error's own text
+ * (`Failed to reach security service: ${err.message}`), so a driver message or an internal host:port reached the
+ * client in every environment. Fix shape named by the gate: a constant body plus a server-side log.
+ *
+ * These cells are deliberately LOOSE about the exact wording: any constant 502 message passes, and any logger.error
+ * call that carries the thrown text passes. What they pin is the contract: 502 + BAD_GATEWAY, the thrown text absent
+ * from the body, present in the server log.
+ *
+ * Harness: the fake req/res dispatch of the KS-1410 api-gateway tests (the real router, no server); global fetch is
+ * stubbed per cell, so no network.
+ */
+import { describe, it, expect, vi, afterEach, beforeEach } from 'vitest';
+import type { Request, Response, Router } from 'express';
+
+const mockLoggerError = vi.hoisted(() => vi.fn());
+vi.mock('../utils/logger', () => ({
+  logger: { error: mockLoggerError, warn: vi.fn(), info: vi.fn(), debug: vi.fn() },
+}));
+
+import auditExportRouter from '../routes/audit-export';
+
+// THE FIXTURE IS LOAD-BEARING: a private host:port and a marker no other code path could produce.
+const LEAK = 'connect ECONNREFUSED 10.0.4.17:4008 ks1410-n1432-private-detail';
+const ADMIN = { userId: 'u-ks1410', role: 'super_admin' };
+const QUERY = { format: 'json', from: '2026-01-01', to: '2026-01-02' };
+
+type CapturedRes = Response & { _status: number; _json: unknown; _headers: Record<string, string> };
+
+function makeRes(onFinish: () => void): CapturedRes {
+  const res: any = {
+    _status: 200,
+    _json: null,
+    _headers: {},
+    status(code: number) {
+      res._status = code;
+      return res;
+    },
+    json(body: unknown) {
+      res._json = body;
+      onFinish();
+      return res;
+    },
+    send(body: unknown) {
+      res._json = body;
+      onFinish();
+      return res;
+    },
+    setHeader(name: string, value: string) {
+      res._headers[name] = value;
+      return res;
+    },
+  };
+  return res;
+}
+
+function dispatch(router: Router, opts: { user?: unknown; query?: Record<string, string> }): Promise<CapturedRes> {
+  return new Promise((resolve, reject) => {
+    const res = makeRes(() => resolve(res));
+    const req = {
+      method: 'GET',
+      url: '/export',
+      headers: {},
+      body: {},
+      query: opts.query ?? {},
+      user: opts.user,
+      get(name: string) {
+        return (this as any).headers[name?.toLowerCase()];
+      },
+    } as unknown as Request;
+    router(req, res as any, (err: unknown) => (err ? reject(err) : resolve(res)));
+  });
+}
+
+beforeEach(() => mockLoggerError.mockClear());
+afterEach(() => {
+  vi.unstubAllGlobals();
+  vi.unstubAllEnvs();
+});
+
+describe('KS-1410 N-1432-1 audit export: an unreachable security service answers 502 without the thrown text', () => {
+  it.each(['production', 'development', 'test'])('RED KS-1410 X1 NODE_ENV=%s: the 502 body does not carry the thrown text', async (nodeEnv) => {
+    vi.stubEnv('NODE_ENV', nodeEnv);
+    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error(LEAK)));
+    const res = await dispatch(auditExportRouter, { user: ADMIN, query: QUERY });
+    const body = res._json as any;
+    expect({ status: res._status, success: body.success, code: body.error.code, leaked: JSON.stringify(body).includes(LEAK) }).toEqual({
+      status: 502,
+      success: false,
+      code: 'BAD_GATEWAY',
+      leaked: false,
+    });
+    expect(typeof body.error.message === 'string' && body.error.message.length > 0).toBe(true);
+  });
+
+  it('RED KS-1410 X2: the thrown text is logged server-side', async () => {
+    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error(LEAK)));
+    const res = await dispatch(auditExportRouter, { user: ADMIN, query: QUERY });
+    expect(res._status).toBe(502);
+    expect(JSON.stringify(mockLoggerError.mock.calls).includes(LEAK)).toBe(true);
+  });
+
+  it('RED KS-1410 X3: the 502 body is the same constant for two different thrown texts', async () => {
+    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error(LEAK)));
+    const first = await dispatch(auditExportRouter, { user: ADMIN, query: QUERY });
+    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('getaddrinfo ENOTFOUND security.internal')));
+    const second = await dispatch(auditExportRouter, { user: ADMIN, query: QUERY });
+    expect(second._json).toEqual(first._json);
+  });
+
+  it('control KS-1410 XC1: an upstream non-ok answer still passes its status and error through', async () => {
+    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 503, json: async () => ({ error: 'upstream says no' }) }));
+    const res = await dispatch(auditExportRouter, { user: ADMIN, query: QUERY });
+    expect([res._status, res._json]).toEqual([503, { success: false, error: { code: 'BAD_GATEWAY', message: 'upstream says no' } }]);
+  });
+
+  it('control KS-1410 XC2: a reachable security service still exports its rows as JSON and logs nothing', async () => {
+    const logs = [{ id: 'a1', timestamp: '2026-01-01T00:00:00Z', type: 'auth', action: 'login', userId: 'u1', outcome: 'success' }];
+    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => ({ success: true, data: { logs } }) }));
+    const res = await dispatch(auditExportRouter, { user: ADMIN, query: QUERY });
+    expect([res._status, (res._json as any).meta.totalEntries, (res._json as any).data]).toEqual([200, 1, logs]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1410 XC3: no req.user still answers 401 and never calls the security service', async () => {
+    const fetchSpy = vi.fn();
+    vi.stubGlobal('fetch', fetchSpy);
+    const res = await dispatch(auditExportRouter, { query: QUERY });
+    expect([res._status, (res._json as any).error.code, fetchSpy.mock.calls.length]).toEqual([401, 'UNAUTHORIZED', 0]);
+  });
+});
```
