# READY — KS-1462-OBJECTLOG-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1462_p1/out.md.checker/patch.diff`** (from `ls` at 07:04 2026-10-16; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1462_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1462_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1462_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in adminConfig.ts (run 8 vs golden 10 body lines — context, since the change lines are equal) (identical in ks730c-adminconfig-500-never-answers-err-message.test.ts); hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks730c-adminconfig-500-never-answers-err-message.test.ts/adminConfig.ts, sha256 equal).

**Held 07:04 2026-10-16 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1462_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `76698952a75717bbcbc35ace85d08d6758d8844f`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/adminConfig.ts , Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/originate/src/routes/adminConfig.ts
46	0	Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/adminConfig.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts fails at the untouched tip (1 failed / 30 run; controls green; assertion reds)` [red_first.json: failed=1 of total=30; red cell(s): ['KS-1462 item 1: migrate-tenant-data logs a thrown non-Error the way fail500 does RED KS-1462 C1 a per-tenant getPool that throws a plain object logs its type and field names, never [object Object]']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts passes with the product hunk (30 passed / 30 run)` [green_after.json: failed=0 of total=30, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1368 failed=0 | after: total=1371 failed=0` · `NEW reds: []` [baseline_suite.json total=1368 failed=0; after_suite.json total=1371 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +47/-1 test=src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (+46/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `76698952a75717bbcbc35ace85d08d6758d8844f` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1462_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1462_p1/KS-1462.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1462_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
+++ b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
@@ -2232,7 +2232,7 @@ adminConfigRouter.post('/migrate-tenant-data', async (_req: Request, res: Respon
         // thrown text. The text goes to the server log with the route and the tenant named, as fail500 does.
         logger.error('Admin config tenant step failed (POST /api/admin/migrate-tenant-data)', {
           tenant: tenant.slug,
-          error: err instanceof Error ? err.message : String(err),
+          error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err,
         });
         results.push({ tenant: tenant.slug, error: 'TENANT_COPY_FAILED' });
       }
--- a/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
@@ -373,3 +373,49 @@ describe('KS-1334 part C: migrate-tenant-data never answers a 200 carrying a ten
     expect(KS1334_LEAK.length).toBeGreaterThan(60);
   });
 });
+
+// KS-1462 (item 1 of 2; item 2, the bare-string per-tenant code, is NOT changed here): the per-tenant catch logged
+// `String(err)`, so a thrown PLAIN OBJECT reached the server log as [object Object]. It now uses the same describer as
+// fail500: an Error by its message, a string verbatim, any other object by its type and field names (never values).
+async function postMigrateThrowing(thrown: unknown): Promise<number> {
+  setNodeEnv('development');
+  mockSharedForC.queryWithTenantGuc.mockResolvedValue({ rows: [] });
+  mockDb.getTenantManager = () => ({
+    getPlatformPool: () => ({ query: jest.fn().mockResolvedValue({ rows: [KS1334C_TENANT] }) }),
+    getDefaultPool: () => ({}),
+    getPool: () => { throw thrown; },
+  });
+  const res = await fetch(baseUrl + '/api/admin/migrate-tenant-data', {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    body: JSON.stringify({}),
+  });
+  await res.text();
+  return res.status;
+}
+
+describe('KS-1462 item 1: migrate-tenant-data logs a thrown non-Error the way fail500 does', () => {
+  beforeEach(() => { mockLoggerError.mockClear(); });
+  afterEach(() => {
+    mockDb.getTenantManager = () => null;
+    mockSharedForC.queryWithTenantGuc.mockReset();
+  });
+
+  it('RED KS-1462 C1 a per-tenant getPool that throws a plain object logs its type and field names, never [object Object]', async () => {
+    const status = await postMigrateThrowing({ code: 'ECONNREFUSED', detail: 'secret-value-not-logged' });
+    expect(status).toBe(200);
+    expect(mockLoggerError.mock.calls).toEqual([[KS1334C_CONTEXT, { tenant: KS1334C_TENANT.slug, error: 'thrown Object with fields [code, detail]' }]]);
+  });
+
+  it('control KS-1462 C2 a per-tenant getPool that throws an Error still logs its message', async () => {
+    const status = await postMigrateThrowing(new Error('ks1462 error message'));
+    expect(status).toBe(200);
+    expect(mockLoggerError.mock.calls).toEqual([[KS1334C_CONTEXT, { tenant: KS1334C_TENANT.slug, error: 'ks1462 error message' }]]);
+  });
+
+  it('control KS-1462 C3 a per-tenant getPool that throws a string still logs it verbatim', async () => {
+    const status = await postMigrateThrowing('ks1462 thrown string');
+    expect(status).toBe(200);
+    expect(mockLoggerError.mock.calls).toEqual([[KS1334C_CONTEXT, { tenant: KS1334C_TENANT.slug, error: 'ks1462 thrown string' }]]);
+  });
+});
```
