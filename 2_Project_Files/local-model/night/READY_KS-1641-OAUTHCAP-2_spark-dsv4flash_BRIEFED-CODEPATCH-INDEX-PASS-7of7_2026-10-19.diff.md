# READY — KS-1641-OAUTHCAP-2 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1641_p1b/out.md.checker/patch.diff`** (from `ls` at 19:25 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1641_p1b/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1641_p1b/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1641_p1b/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1641_p1b-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 19:25 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1641_p1b/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `80868551e67934cb951d28eec44ce3bdf835944c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/m365-integration/src/index.ts , Blockchain/Dev/services/m365-integration/src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/m365-integration/src/index.ts` (product) and `Blockchain/Dev/services/m365-integration/src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/m365-integration/src/index.ts
75	0	Blockchain/Dev/services/m365-integration/src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/m365-integration/src/index.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/m365-integration/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/m365-integration/src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1641 - the OAuth callback does not reflect unbounded provider text into the redirect RED KS-1641 E1: a 5000-character error_description reaches the redirect as at most 200 characters', 'KS-1641 - the OAuth callback does not reflect unbounded provider text into the redirect RED KS-1641 E2: the 200 characters kept are the FIRST 200 of the description']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=64 failed=0 | after: total=68 failed=0` · `NEW reds: []` [baseline_suite.json total=64 failed=0; after_suite.json total=68 failed=0]
- A6 [verbatim]: `PASS A6 whole services/m365-integration suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/m365-integration: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +76/-1 test=src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/m365-integration/src/index.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/m365-integration/src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts` (+75/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `80868551e67934cb951d28eec44ce3bdf835944c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1641_p1b/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1641_p1/KS-1641.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1641_p1b/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/m365-integration/src/index.ts b/Blockchain/Dev/services/m365-integration/src/index.ts
index 1d9ea9df2..d119bdef4 100644
--- a/Blockchain/Dev/services/m365-integration/src/index.ts
+++ b/Blockchain/Dev/services/m365-integration/src/index.ts
@@ -464,3 +464,3 @@
     log('error', 'OAuth callback error', { error: oauthError, description: error_description });
-    return res.redirect(`${process.env.FRONTEND_URL || 'http://localhost:6882'}/admin/integrations?m365=error&message=${encodeURIComponent(String(error_description || oauthError))}`);
+    return res.redirect(`${process.env.FRONTEND_URL || 'http://localhost:6882'}/admin/integrations?m365=error&message=${encodeURIComponent(String(error_description || oauthError).slice(0, 200))}`);
   }
diff --git a/Blockchain/Dev/services/m365-integration/src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts
new file mode 100644
index 000000000..729134390
--- /dev/null
+++ b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts
@@ -0,0 +1,75 @@
+/**
+ * KS-1641 (finding 2 only) - GET /api/callback is the unauthenticated OAuth redirect target, and on a provider error it
+ * put the provider's `error_description` into the admin redirect URL with NO length cap (services/auth caps the same
+ * field at 200 characters). After the fix the reflected text is at most 200 characters; a short description and the
+ * `error` code fallback are reflected exactly as before. The redirect PATH is not touched by this file.
+ * Harness: the ks934 pattern - the real app from ../index, `../db` and express's `listen` mocked (index.ts listens at
+ * import), driven over an HTTP listener on 127.0.0.1 with redirects NOT followed.
+ */
+import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
+import http from 'http';
+
+process.env.NODE_ENV = 'test';
+process.env.FRONTEND_URL = 'http://frontend.test';
+
+const rows: any[] = [];
+
+vi.mock('../db', () => ({
+  initDb: async () => undefined,
+  isDbAvailable: () => true,
+  query: async () => ({ rows }),
+}));
+
+vi.mock('express', async (importOriginal) => {
+  const actual: any = (await importOriginal<any>()).default ?? (await importOriginal<any>());
+  const factory: any = (...args: any[]) => {
+    const app = actual(...args);
+    app.listen = () => ({ close: (cb?: () => void) => cb?.(), address: () => ({ port: 0 }), on() { return this; } });
+    return app;
+  };
+  Object.assign(factory, actual);
+  return { ...actual, default: factory };
+});
+
+let server: http.Server;
+let base = '';
+beforeAll(async () => {
+  const app = (await import('../index')).default as any;
+  server = http.createServer(app);
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  base = `http://127.0.0.1:${(server.address() as any).port}`;
+}, 20_000);
+afterAll(async () => {
+  if (server) await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+
+/** GET /api/callback with a provider error; returns the redirect target's `m365` and decoded `message`. */
+async function callback(query: string): Promise<{ status: number; m365: string | null; message: string | null }> {
+  const res = await fetch(`${base}/api/callback?${query}`, { redirect: 'manual' });
+  const loc = new URL(res.headers.get('location') || 'http://none.invalid/');
+  return { status: res.status, m365: loc.searchParams.get('m365'), message: loc.searchParams.get('message') };
+}
+
+describe('KS-1641 - the OAuth callback does not reflect unbounded provider text into the redirect', () => {
+  it('RED KS-1641 E1: a 5000-character error_description reaches the redirect as at most 200 characters', async () => {
+    const r = await callback(`error=access_denied&error_description=${encodeURIComponent('A'.repeat(5000))}`);
+    expect([r.status, r.m365]).toEqual([302, 'error']);
+    expect((r.message ?? '').length).toBeLessThanOrEqual(200);
+  });
+
+  it('RED KS-1641 E2: the 200 characters kept are the FIRST 200 of the description', async () => {
+    const text = 'B'.repeat(200) + 'TAIL-MARKER-' + 'C'.repeat(300);
+    const r = await callback(`error=access_denied&error_description=${encodeURIComponent(text)}`);
+    expect(r.message).toBe('B'.repeat(200));
+  });
+
+  it('CONTROL KS-1641 E3: a short error_description is reflected exactly as the provider sent it', async () => {
+    const r = await callback(`error=access_denied&error_description=${encodeURIComponent('The user cancelled the request')}`);
+    expect([r.status, r.m365, r.message]).toEqual([302, 'error', 'The user cancelled the request']);
+  });
+
+  it('CONTROL KS-1641 E4: with no error_description the error code is the message', async () => {
+    const r = await callback('error=access_denied');
+    expect([r.status, r.m365, r.message]).toEqual([302, 'error', 'access_denied']);
+  });
+});
```
