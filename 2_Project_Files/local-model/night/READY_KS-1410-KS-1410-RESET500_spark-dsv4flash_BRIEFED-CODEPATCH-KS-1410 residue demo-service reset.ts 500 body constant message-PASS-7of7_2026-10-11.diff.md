# READY — KS-1410-KS-1410-RESET500 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-11_T2-reset-500-body/out.md.checker/patch.diff`** (from `ls` at 06:58 2026-10-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-11_T2-reset-500-body/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-11_T2-reset-500-body/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-11_T2-reset-500-body/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-11_T2-reset-500-body-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 06:58 2026-10-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-11_T2-reset-500-body/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `f8c86f859fe0c016a20fe413f5a53806f3592a50`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/demo-service/src/routes/reset.ts , Blockchain/Dev/services/demo-service/src/__tests__/reset.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/demo-service/src/routes/reset.ts` (product) and `Blockchain/Dev/services/demo-service/src/__tests__/reset.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/demo-service/src/routes/reset.ts
58	0	Blockchain/Dev/services/demo-service/src/__tests__/reset.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/demo-service/src/routes/reset.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/demo-service/src/routes/reset.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/demo-service/src/__tests__/reset.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/reset.test.ts fails at the untouched tip (1 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=1 of total=12; red cell(s): ['POST /demo-api/reset RED KS-1410 R1: the 500 body never carries the thrown error text']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/reset.test.ts passes with the product hunk (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=86 failed=0 | after: total=89 failed=0` · `NEW reds: []` [baseline_suite.json total=86 failed=0; after_suite.json total=89 failed=0]
- A6 [verbatim]: `PASS A6 whole services/demo-service suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/demo-service: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +59/-1 test=src/__tests__/reset.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/demo-service/src/routes/reset.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/demo-service/src/__tests__/reset.test.ts` (+58/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `f8c86f859fe0c016a20fe413f5a53806f3592a50` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-11_T2-reset-500-body/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-11_T2-reset-500-body/checker.out`.

```diff
--- a/Blockchain/Dev/services/demo-service/src/routes/reset.ts
+++ b/Blockchain/Dev/services/demo-service/src/routes/reset.ts
@@ -69,6 +69,6 @@
     return res.status(500).json({
       success: false,
-      error: { code: 'INTERNAL_ERROR', message: message, failedStep },
+      error: { code: 'INTERNAL_ERROR', message: 'Internal server error', failedStep },
     });
   }
 });
--- a/Blockchain/Dev/services/demo-service/src/__tests__/reset.test.ts
+++ b/Blockchain/Dev/services/demo-service/src/__tests__/reset.test.ts
@@ -237,4 +237,62 @@ describe('POST /demo-api/reset', () => {
     // KS-150: envelope shape — the human-readable text is `error.message`.
     expect(body.error.message).toContain('X-Demo-Reset');
   });
+
+  // KS-1410: the 500 catch answered the thrown error's own text (`message: message`) with no NODE_ENV guard,
+  // so a driver message or an internal host:port reached the client. The fix answers a constant message and
+  // keeps the log (`logger.error`) and `failedStep`. The marker below is one no other code path could produce.
+  const KS1410_LEAK = 'connect ECONNREFUSED 10.0.4.17:5432 ks1410-demo-private-detail';
+
+  function failPgRestoreWithLeak() {
+    vi.spyOn(fs, 'accessSync').mockReturnValue(undefined);
+    const mockExecFile = vi.mocked(execFile);
+    mockExecFile.mockImplementation((_cmd: any, _args: any, callback: any) => {
+      callback(new Error(KS1410_LEAK), { stdout: '', stderr: '' });
+      return undefined as any;
+    });
+  }
+
+  it('RED KS-1410 R1: the 500 body never carries the thrown error text', async () => {
+    failPgRestoreWithLeak();
+
+    const app = createApp();
+    const res = await startServer(app, 'POST', '/demo-api/reset', {
+      'X-Demo-Reset': 'true',
+    });
+
+    expect(res.status).toBe(500);
+
+    const body = await res.json();
+    expect(JSON.stringify(body)).not.toContain('ks1410-demo-private-detail');
+    expect(body.error.message).toBe('Internal server error');
+  });
+
+  it('control KS-1410 RC1: the 500 body keeps success false, the INTERNAL_ERROR code and failedStep', async () => {
+    failPgRestoreWithLeak();
+
+    const app = createApp();
+    const res = await startServer(app, 'POST', '/demo-api/reset', {
+      'X-Demo-Reset': 'true',
+    });
+
+    expect(res.status).toBe(500);
+
+    const body = await res.json();
+    expect([body.success, body.error.code, body.error.failedStep]).toEqual([false, 'INTERNAL_ERROR', 'database']);
+  });
+
+  it('control KS-1410 RC2: the thrown error text is still logged server-side', async () => {
+    failPgRestoreWithLeak();
+    const { logger } = await import('../utils/logger');
+
+    const app = createApp();
+    await startServer(app, 'POST', '/demo-api/reset', {
+      'X-Demo-Reset': 'true',
+    });
+
+    expect(logger.error).toHaveBeenCalledWith(
+      'Demo reset failed',
+      expect.objectContaining({ failedStep: 'database', error: expect.stringContaining('ks1410-demo-private-detail') }),
+    );
+  });
 });
```
