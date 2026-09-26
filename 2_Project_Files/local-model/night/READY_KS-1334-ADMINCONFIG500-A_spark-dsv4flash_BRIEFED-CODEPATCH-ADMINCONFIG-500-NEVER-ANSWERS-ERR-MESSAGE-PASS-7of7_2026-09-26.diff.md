# READY — KS-1334-ADMINCONFIG500-A (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1334-A/out.md.checker/patch.diff`** (from `ls` at 21:30 2026-09-26; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1334-A/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1334-A/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 21:30 2026-09-26 by Wednesday evening seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1334-A/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3f70224a069b944334480478ad5d16a5ed33eeae`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/adminConfig.ts , Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/originate/src/routes/adminConfig.ts
54	2	Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/adminConfig.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (hunks=3, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts fails at the untouched tip (4 failed / 19 run; controls green; assertion reds)` [red_first.json: failed=4 of total=19; red cell(s): ['KS-730 part C: the 46 converted admin-config sites never answer a 500 with err.message KS-730 C3 SOURCE: all forty-six sites are routed through the helper, each with a DISTINCT context', 'KS-730 part C: the 46 converted admin-config sites never answer a 500 with err.message KS-730 C4 SOURCE: the four UNCONDITIONAL err.message sites are named, not silently left', 'KS-1334 part A: refresh-tenants and backfill-certification-metadata never answer a 500 with err.message RED KS-1334 A1 POST /refresh-tenants: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it', 'KS-1334 part A: refresh-tenants and backfill-certification-metadata never answer a 500 with err.message RED KS-1334 A1 POST /backfill-certification-metadata: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts passes with the product hunk (19 passed / 19 run)` [green_after.json: failed=0 of total=19, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=962 failed=0 | after: total=967 failed=0` · `NEW reds: []` [baseline_suite.json total=962 failed=0; after_suite.json total=967 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +56/-4 test=src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (+54/-2); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3f70224a069b944334480478ad5d16a5ed33eeae` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1334-A/input.json`. Brief (given by --brief; its `# ` heading names KS-1334): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1334/KS-1334.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1334-A/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
+++ b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
@@ -112,3 +112,3 @@
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err?.message || 'Refresh failed' } });
+    fail500(res, 'Admin config request failed (POST /api/admin/refresh-tenants)', err);
   }
@@ -1857,4 +1857,4 @@
     res.json({ success: true, updatedCount: result });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Admin config request failed (POST /api/admin/backfill-certification-metadata)', err);
   }
--- a/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
@@ -141,3 +141,3 @@
     expect({ liveTernaries: liveTernaries.length, helperCalls: helperCalls.length, distinctContexts: new Set(contexts).size })
-      .toEqual({ liveTernaries: 0, helperCalls: 46, distinctContexts: 46 });
+      .toEqual({ liveTernaries: 0, helperCalls: 48, distinctContexts: 48 });
     expect(contexts.filter((c) => !c)).toEqual([]);
@@ -171,3 +171,2 @@
     const KNOWN = [
-      'POST /refresh-tenants', 'POST /backfill-certification-metadata',
       'POST /seed-demo-users', 'POST /migrate-tenant-data',
@@ -203,2 +202,55 @@
   });
+});
+
+// KS-1334 part A: two of the four UNCONDITIONAL sites named by C4 above now go through fail500. They
+// answered err.message in EVERY environment, production included, so unlike the KS-730 cells the
+// production row is the one that separates this class, and it is driven first. Part B covers the
+// other two (seed-demo-users, migrate-tenant-data). Its own LEAK carries no double quote: the shared
+// LEAK above does, JSON-escapes to a backslash-quote in the body, and so can never be found by includes.
+const KS1334_LEAK = 'could not serialize access due to concurrent update ks1334-private-detail';
+const KS1334_NODE_ENVS = ['production', 'development', 'demo', 'test', undefined];
+const KS1334_ROUTES = [
+  { label: 'POST /refresh-tenants', path: '/refresh-tenants', body: {}, context: 'Admin config request failed (POST /api/admin/refresh-tenants)' },
+  { label: 'POST /backfill-certification-metadata', path: '/backfill-certification-metadata', body: { issuerName: 'ks1334-issuer' }, context: 'Admin config request failed (POST /api/admin/backfill-certification-metadata)' },
+] as const;
+const mockRefreshTenantConfigs = (jest.requireMock('../db') as { refreshTenantConfigs: jest.Mock }).refreshTenantConfigs;
+
+async function post1334(route: (typeof KS1334_ROUTES)[number], nodeEnv: string | undefined, throwIt: boolean): Promise<{ status: number; text: string }> {
+  setNodeEnv(nodeEnv);
+  if (throwIt) {
+    mockRefreshTenantConfigs.mockRejectedValue(new Error(KS1334_LEAK));
+    mockExecuteRaw.mockRejectedValue(new Error(KS1334_LEAK));
+  } else {
+    mockRefreshTenantConfigs.mockResolvedValue(undefined);
+    mockExecuteRaw.mockResolvedValue(3);
+  }
+  const res = await fetch(baseUrl + '/api/admin' + route.path, {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    body: JSON.stringify(route.body),
+  });
+  return { status: res.status, text: await res.text() };
+}
+
+describe('KS-1334 part A: refresh-tenants and backfill-certification-metadata never answer a 500 with err.message', () => {
+  it.each(KS1334_ROUTES)('RED KS-1334 A1 $label: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it', async (route) => {
+    for (const nodeEnv of KS1334_NODE_ENVS) {
+      mockLoggerError.mockClear();
+      const reply = await post1334(route, nodeEnv, true);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(KS1334_LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+      expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: KS1334_LEAK }]] });
+    }
+  });
+
+  it.each(KS1334_ROUTES)('control KS-1334 A0 $label: a call that does not throw answers 200 and logs nothing', async (route) => {
+    const reply = await post1334(route, 'production', false);
+    expect({ status: reply.status, success: JSON.parse(reply.text).success }).toEqual({ status: 200, success: true });
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1334 A2: KS1334_LEAK survives JSON encoding, so leaked: false above is not vacuous', () => {
+    expect(JSON.stringify({ success: false, error: { message: KS1334_LEAK } }).includes(KS1334_LEAK)).toBe(true);
+    expect(new Error(KS1334_LEAK).message).toBe(KS1334_LEAK);
+  });
 });
```
