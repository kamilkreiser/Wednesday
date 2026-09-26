# READY — KS-1334-ADMINCONFIG500-B (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1334-B/out.md.checker/patch.diff`** (from `ls` at 02:09 2026-09-27; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1334-B/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1334-B/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 02:09 2026-09-27 by Wednesday evening seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1334-B/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/adminConfig.ts , Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/originate/src/routes/adminConfig.ts
51	4	Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/adminConfig.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (hunks=3, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts fails at the untouched tip (4 failed / 23 run; controls green; assertion reds)` [red_first.json: failed=4 of total=23; red cell(s): ['KS-730 part C: the 46 converted admin-config sites never answer a 500 with err.message KS-730 C3 SOURCE: all forty-six sites are routed through the helper, each with a DISTINCT context', 'KS-730 part C: the 46 converted admin-config sites never answer a 500 with err.message KS-730 C4 SOURCE: the four UNCONDITIONAL err.message sites are named, not silently left', 'KS-1334 part B: seed-demo-users and migrate-tenant-data never answer a 500 with err.message RED KS-1334 B1 POST /seed-demo-users: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it', 'KS-1334 part B: seed-demo-users and migrate-tenant-data never answer a 500 with err.message RED KS-1334 B1 POST /migrate-tenant-data: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts passes with the product hunk (23 passed / 23 run)` [green_after.json: failed=0 of total=23, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=979 failed=0 | after: total=983 failed=0` · `NEW reds: []` [baseline_suite.json total=979 failed=0; after_suite.json total=983 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +53/-6 test=src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (+51/-4); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1334-B/input.json`. Brief (given by --brief; its `# ` heading names KS-1334): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1334-B/KS-1334.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1334-B/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
+++ b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
@@ -2028,5 +2028,5 @@
       failed,
     });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Admin config request failed (POST /api/admin/seed-demo-users)', err);
   }
@@ -2156,4 +2156,4 @@
     res.json({ success: true, results });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Admin config request failed (POST /api/admin/migrate-tenant-data)', err);
   }
--- a/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
@@ -141,3 +141,3 @@
     expect({ liveTernaries: liveTernaries.length, helperCalls: helperCalls.length, distinctContexts: new Set(contexts).size })
-      .toEqual({ liveTernaries: 0, helperCalls: 48, distinctContexts: 48 });
+      .toEqual({ liveTernaries: 0, helperCalls: 50, distinctContexts: 50 });
     expect(contexts.filter((c) => !c)).toEqual([]);
@@ -171,4 +171,2 @@
-    const KNOWN = [
-      'POST /seed-demo-users', 'POST /migrate-tenant-data',
-    ];
+    const KNOWN: string[] = [];
     let route = '';
@@ -255,2 +253,51 @@
   });
+});
+
+// KS-1334 part B: the last two UNCONDITIONAL sites (seed-demo-users, migrate-tenant-data) now go through
+// fail500, so the KNOWN list in C4 is empty and C3 counts 50. Neither handler reaches its outer catch
+// through the prisma mock the cells above use, so each is driven through the first call its try block
+// makes outside any inner catch: seed-demo-users through the refusal warning of its demo-seed gate
+// (the gate is closed here), migrate-tenant-data through the platform pool of its tenant manager.
+const mockLoggerWarn = (jest.requireMock('../utils/logger') as { logger: { warn: jest.Mock } }).logger.warn;
+const mockDb = jest.requireMock('../db') as { getTenantManager: () => unknown };
+const KS1334B_ROUTES = [
+  { label: 'POST /seed-demo-users', path: '/seed-demo-users', calmStatus: 403, context: 'Admin config request failed (POST /api/admin/seed-demo-users)' },
+  { label: 'POST /migrate-tenant-data', path: '/migrate-tenant-data', calmStatus: 400, context: 'Admin config request failed (POST /api/admin/migrate-tenant-data)' },
+] as const;
+
+async function post1334b(route: (typeof KS1334B_ROUTES)[number], nodeEnv: string | undefined, throwIt: boolean): Promise<{ status: number; text: string }> {
+  setNodeEnv(nodeEnv);
+  delete process.env.ENABLE_DEMO_SEED;
+  mockLoggerWarn.mockReset();
+  mockDb.getTenantManager = () => null;
+  if (throwIt && route.path === '/seed-demo-users') {
+    mockLoggerWarn.mockImplementationOnce(() => { throw new Error(KS1334_LEAK); });
+  }
+  if (throwIt && route.path === '/migrate-tenant-data') {
+    mockDb.getTenantManager = () => ({ getPlatformPool: () => { throw new Error(KS1334_LEAK); } });
+  }
+  const res = await fetch(baseUrl + '/api/admin' + route.path, {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    body: JSON.stringify({}),
+  });
+  return { status: res.status, text: await res.text() };
+}
+
+describe('KS-1334 part B: seed-demo-users and migrate-tenant-data never answer a 500 with err.message', () => {
+  it.each(KS1334B_ROUTES)('RED KS-1334 B1 $label: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it', async (route) => {
+    for (const nodeEnv of KS1334_NODE_ENVS) {
+      mockLoggerError.mockClear();
+      const reply = await post1334b(route, nodeEnv, true);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(KS1334_LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+      expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: KS1334_LEAK }]] });
+    }
+  });
+
+  it.each(KS1334B_ROUTES)('control KS-1334 B0 $label: with nothing thrown the route answers its own refusal and logs no error', async (route) => {
+    const reply = await post1334b(route, 'production', false);
+    expect({ status: reply.status, success: JSON.parse(reply.text).success }).toEqual({ status: route.calmStatus, success: false });
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
 });
```
