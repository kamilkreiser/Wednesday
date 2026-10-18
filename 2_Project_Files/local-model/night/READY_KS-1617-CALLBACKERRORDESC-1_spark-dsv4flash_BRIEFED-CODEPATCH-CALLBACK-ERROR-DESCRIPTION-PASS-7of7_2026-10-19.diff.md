# READY — KS-1617-CALLBACKERRORDESC-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p2/out.md.checker/patch.diff`** (from `ls` at 10:44 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p2-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:44 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `78cb3c3939e319332e387ffecb075a169edd4a39`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/routes/auth.ts , Blockchain/Dev/services/auth/src/__tests__/ks819-oauth-state-consume-order.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/auth.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks819-oauth-state-consume-order.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	0	Blockchain/Dev/services/auth/src/routes/auth.ts
37	0	Blockchain/Dev/services/auth/src/__tests__/ks819-oauth-state-consume-order.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/routes/auth.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/auth.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks819-oauth-state-consume-order.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks819-oauth-state-consume-order.test.ts fails at the untouched tip (2 failed / 16 run; controls green; assertion reds)` [red_first.json: failed=2 of total=16; red cell(s): ['KS-819 F-4 — a user who cancels at the provider gets a clean refusal RED KS-1617 A2-1 - the provider error_description reaches the server-side log, next to its error', 'KS-819 F-4 — a user who cancels at the provider gets a clean refusal RED KS-1617 A2-2 - the logged error_description is trimmed to 200 characters, like the error beside it']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks819-oauth-state-consume-order.test.ts passes with the product hunk (16 passed / 16 run)` [green_after.json: failed=0 of total=16, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1061 failed=0 | after: total=1064 failed=0` · `NEW reds: []` [baseline_suite.json total=1061 failed=0; after_suite.json total=1064 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +38/-0 test=src/__tests__/ks819-oauth-state-consume-order.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/auth.ts` (+1/-0 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks819-oauth-state-consume-order.test.ts` (+37/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `78cb3c3939e319332e387ffecb075a169edd4a39` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p2/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1617_p2/KS-1617.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/auth.ts b/Blockchain/Dev/services/auth/src/routes/auth.ts
index ded3800b1..00023447b 100644
--- a/Blockchain/Dev/services/auth/src/routes/auth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/auth.ts
@@ -1015,2 +1015,3 @@
         providerError: String(req.query.error).slice(0, 200),
+        providerErrorDescription: req.query.error_description === undefined ? undefined : String(req.query.error_description).slice(0, 200),
       });
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks819-oauth-state-consume-order.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks819-oauth-state-consume-order.test.ts
index 2d27f24b5..d7060708f 100644
--- a/Blockchain/Dev/services/auth/src/__tests__/ks819-oauth-state-consume-order.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks819-oauth-state-consume-order.test.ts
@@ -298,2 +298,39 @@
 
+  // KS-1617 A.2: the provider's explanation is LOGGED, never echoed. `error_description` is where a provider says WHICH thing is
+  // wrong (a redirect-URI mismatch, an unauthorised client); only `error` used to be logged, so a misconfigured provider and a
+  // user who pressed Cancel looked the same to an operator. The structured warning is read through the shared silent logger.
+  const providerErrorLogs = (): Array<Record<string, unknown>> =>
+    silentLogger.warn.mock.calls.map((c) => c[1] as Record<string, unknown>).filter((m) => m && m.providerError !== undefined);
+
+  it('RED KS-1617 A2-1 - the provider error_description reaches the server-side log, next to its error', async () => {
+    const { state } = await initiate('google');
+    silentLogger.warn.mockClear();
+    const r = await callback(
+      'google',
+      `?error=invalid_request&error_description=${encodeURIComponent('redirect_uri_mismatch: ks1617')}&state=${encodeURIComponent(state!)}`,
+    );
+    expect(r.code).toBe('OAUTH_PROVIDER_ERROR');
+    expect(providerErrorLogs()).toEqual([
+      { provider: 'google', providerError: 'invalid_request', providerErrorDescription: 'redirect_uri_mismatch: ks1617' },
+    ]);
+  });
+
+  it('RED KS-1617 A2-2 - the logged error_description is trimmed to 200 characters, like the error beside it', async () => {
+    const { state } = await initiate('google');
+    silentLogger.warn.mockClear();
+    await callback('google', `?error=invalid_request&error_description=${'d'.repeat(500)}&state=${encodeURIComponent(state!)}`);
+    const logged = providerErrorLogs();
+    expect(logged).toHaveLength(1);
+    expect(String(logged[0].providerErrorDescription)).toBe('d'.repeat(200));
+  });
+
+  it('CONTROL KS-1617 A2-3 - a cancel with no error_description logs the error alone, and the caller still gets the generic refusal', async () => {
+    const { state } = await initiate('google');
+    silentLogger.warn.mockClear();
+    const r = await callback('google', `?error=access_denied&state=${encodeURIComponent(state!)}`);
+    expect([r.status, r.code]).toEqual([400, 'OAUTH_PROVIDER_ERROR']);
+    expect(providerErrorLogs()).toEqual([{ provider: 'google', providerError: 'access_denied' }]);
+    expect(r.raw).not.toContain('access_denied');
+  });
+
   it('and does not burn the state on the way out', async () => {
```
