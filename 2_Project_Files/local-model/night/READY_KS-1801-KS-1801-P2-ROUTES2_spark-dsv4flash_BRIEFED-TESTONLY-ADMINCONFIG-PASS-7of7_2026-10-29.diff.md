# READY — KS-1801-KS-1801-P2-ROUTES2 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1801_p2/out.md.checker/patch.diff`** (from `ls` at 19:53 2026-10-29; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1801_p2/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 19:53 2026-10-29 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1801_p2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `fd84001c738a1bf9071d2d8a5cac6e953ad95789`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
53	0	Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (46 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 53 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 46 line(s) byte-exact incl. leading whitespace (of 46; 53 line(s) added by the apply)` [a3i_indent.out: `OK 46 line(s) byte-exact incl. leading whitespace (of 46; 53 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `a3bfdab5f0b87b5f` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/originate/src/routes/adminConfig.ts:134)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-29_ks_1801_p2_192302/clone/Blockchain/Dev/services/originate/src/routes/adminConfig.ts:134: '  try {' -> '  JSON.stringify(err?.message); try {'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/originate/src/routes/adminConfig.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 134. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts fails at the untouched tip (4 failed / 31 run; controls green; assertion reds)` [red_first.json: failed=4 of total=31; red cell(s): ['KS-1801: the errorMessageIncludes catches answer a hostile thrown value RED KS-1801 B1 POST /document-types: a revoked Proxy thrown by the query is answered with the constant 500', 'KS-1801: the errorMessageIncludes catches answer a hostile thrown value RED KS-1801 B1 GET /rights-holders/:id/documents: a revoked Proxy thrown by the query is answered with the constant 500', 'KS-1801: the errorMessageIncludes catches answer a hostile thrown value RED KS-1801 B2 POST /document-types: an object whose message getter throws is answered with the constant 500', 'KS-1801: the errorMessageIncludes catches answer a hostile thrown value RED KS-1801 B2 GET /rights-holders/:id/documents: an object whose message getter throws is answered with the constant 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts passes with the product hunk (31 passed / 31 run)` [green_after.json: failed=0 of total=31, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1757 failed=0 | after: total=1767 failed=0` · `NEW reds: []` [baseline_suite.json total=1757 failed=0; after_suite.json total=1767 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +53/-0 test=src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts` (+53/-0 per numstat.out); the product `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` is the tamper target and is byte-unchanged (sha256 a3bfdab5f0b87b5f, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `fd84001c738a1bf9071d2d8a5cac6e953ad95789` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1801_p2/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1801_p2/KS-1801.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1801_p2/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts
@@ -98,3 +98,56 @@
+// KS-1801: the two catches that call errorMessageIncludes (it reads the message only, never `code`) are driven too. Each row names the thrown value that the catch DOES recognise
+// (`hit`) and the answer that gives; a hostile value must fall through to the constant 500 like every other catch above.
+const DOC_ID = '00000000-0000-4000-8000-000000000001';
+const MESSAGE_ROUTES = [
+  {
+    label: 'POST /document-types', method: 'POST', path: '/document-types', body: JSON.stringify({ name: 'KS-1801 type', code: 'ks1801' }),
+    hit: new Error('duplicate key value violates unique constraint "x"'),
+    hitAnswer: { status: 409, body: { success: false, error: { code: 'CONFLICT', message: 'Document type code already exists' } } },
+  },
+  {
+    label: 'GET /rights-holders/:id/documents', method: 'GET', path: '/rights-holders/' + DOC_ID + '/documents', body: undefined,
+    hit: new Error('relation "documents" does not exist'),
+    hitAnswer: { status: 200, body: { success: true, documents: [] } },
+  },
+] as const;
+
+async function callMessageRoute(route: (typeof MESSAGE_ROUTES)[number], thrown: unknown): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
+  mockQueryRaw.mockRejectedValueOnce(thrown);
+  try {
+    const res = await fetch(baseUrl + '/api/admin' + route.path, {
+      method: route.method,
+      headers: { 'content-type': 'application/json' },
+      body: route.body,
+      signal: AbortSignal.timeout(1500),
+    });
+    return { status: res.status, body: await res.json() };
+  } catch {
+    return { status: 'NO ANSWER', body: null };
+  }
+}
+
+describe('KS-1801: the errorMessageIncludes catches answer a hostile thrown value', () => {
+  it.each(MESSAGE_ROUTES)('RED KS-1801 B1 $label: a revoked Proxy thrown by the query is answered with the constant 500', async (route) => {
+    expect(await callMessageRoute(route, revokedProxy())).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it.each(MESSAGE_ROUTES)('RED KS-1801 B2 $label: an object whose message getter throws is answered with the constant 500', async (route) => {
+    expect(await callMessageRoute(route, throwingMessageGetter())).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it.each(MESSAGE_ROUTES)('control KS-1801 D1 $label: the Error the catch recognises is still answered as before', async (route) => {
+    expect(await callMessageRoute(route, route.hit)).toEqual(route.hitAnswer);
+  });
+
+  it.each(MESSAGE_ROUTES)('control KS-1801 D2 $label: an ordinary Error is still answered with the constant 500', async (route) => {
+    expect(await callMessageRoute(route, new Error('ks1801 ordinary'))).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it.each(MESSAGE_ROUTES)('control KS-1801 D3 $label: a thrown object with only code 42P01 is NOT recognised here (this catch reads the message only) and gets the constant 500', async (route) => {
+    expect(await callMessageRoute(route, { code: '42P01' })).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+});
+
 describe('KS-1780: adminConfig catches answer a hostile thrown value', () => {
   it.each(ROUTES)('RED KS-1780 A1 $label: a revoked Proxy thrown by the query is answered with the constant 500', async (route) => {
     expect(await callWithThrow(route.path, revokedProxy())).toEqual({ status: 500, body: CONSTANT_BODY });
```
