# READY — KS-1791-KS-1791 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1791_p1_callback_syntaxerror_neutral/out.md.checker/patch.diff`** (from `ls` at 09:51 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1791_p1_callback_syntaxerror_neutral/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1791_p1_callback_syntaxerror_neutral/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 09:51 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1791_p1_callback_syntaxerror_neutral/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `99586cd46456a3955aff48340855d10e51c979e9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/routes/auth.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/auth.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	3	Blockchain/Dev/services/auth/src/routes/auth.ts
12	1	Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (4 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: auth.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/routes/auth.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/routes/auth.ts 4 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts 12 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/auth.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts` (hunks=3, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (1 failed / 59 run; controls green; assertion reds)` [red_first.json: failed=1 of total=59; red cell(s): ["KS-1240 routes: what each entry path answers when the provider does not answer in time RED KS-1791 R1 a token answer that is 200 with a non-JSON body: the login callback answers 400 with a neutral text and none of the provider's bytes"]]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (59 passed / 59 run)` [green_after.json: failed=0 of total=59, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1326 failed=0 | after: total=1327 failed=0` · `NEW reds: []` [baseline_suite.json total=1326 failed=0; after_suite.json total=1327 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/auth.ts` (+4/-3 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts` (+12/-1); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/routes/auth.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `99586cd46456a3955aff48340855d10e51c979e9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1791_p1_callback_syntaxerror_neutral/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1791_p1_callback_syntaxerror_neutral/checker.out`.

```diff
--- a/Blockchain/Dev/services/auth/src/routes/auth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/auth.ts
@@ -1075,7 +1075,8 @@
     try {
       profile = await provider.exchangeCode(code);
     } catch (exchangeErr: any) {
-      throw new BadRequestError(
-        `OAuth authentication failed: ${exchangeErr?.message || 'invalid authorization code'}`
-      );
+      // KS-1791: a provider that answers 200 with a body that is not JSON makes the adapter's `.json()` throw a SyntaxError whose message QUOTES the first 10 characters of that body (V8). Those are the
+      // provider's bytes, so they are not echoed to the client; every other exchange failure keeps its own message, as before.
+      const detail = exchangeErr?.name === 'SyntaxError' ? 'the provider answer could not be read' : exchangeErr?.message || 'invalid authorization code';
+      throw new BadRequestError(`OAuth authentication failed: ${detail}`);
     }
--- a/Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts
@@ -141,4 +141,4 @@
-type Mode = 'ok' | 'hang' | 'stall' | 'refuse' | 'refuse5xx' | 'unauth' | 'empty200' | 'deadport';
+type Mode = 'ok' | 'hang' | 'stall' | 'refuse' | 'refuse5xx' | 'unauth' | 'empty200' | 'html200' | 'deadport';
 const PROVIDER_MARKER = 'PROVIDER_TEXT_MARKER_ks1240b';
 const mode: Record<string, Mode> = {};
 const asked: number[] = [];
@@ -193,6 +193,8 @@
       if (m === 'refuse5xx') { res.writeHead(502, { 'content-type': 'text/html' }); res.end(`<html>upstream ${PROVIDER_MARKER}</html>`); return; }
       if (m === 'unauth') { res.writeHead(401, { 'content-type': 'application/json' }); res.end(JSON.stringify({ message: 'Bad credentials' })); return; }
       if (m === 'empty200') { res.writeHead(200, { 'content-type': 'application/json' }); res.end('{}'); return; }
+      // KS-1791: HTTP 200 with a body that is not JSON; the adapter's .json() throws a SyntaxError that quotes the first 10 characters of it.
+      if (m === 'html200') { res.writeHead(200, { 'content-type': 'text/html' }); res.end(`<html>${PROVIDER_MARKER}</html>`); return; }
       res.writeHead(200, { 'content-type': 'application/json' });
       res.end(JSON.stringify(OK_BODY[key] ?? {}));
     });
@@ -418,3 +420,12 @@
+  it('RED KS-1791 R1 a token answer that is 200 with a non-JSON body: the login callback answers 400 with a neutral text and none of the provider\'s bytes', async () => {
+    const state = await freshState('github');
+    mode['github.com/login/oauth/access_token'] = 'html200';
+    const r = await call('GET', `/api/auth/social/github/callback?code=c8&state=${encodeURIComponent(state)}`);
+    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', 'OAuth authentication failed: the provider answer could not be read']);
+    expect(r.raw, 'the first bytes of the provider body are not in the response').not.toContain('<html>PROV');
+    expect(r.raw, 'the parser message is not in the response').not.toContain('is not valid JSON');
+  }, 15000);
+
   it('🔴 POST /social/link, GitHub refuses the CONNECTION: 503 SERVICE_UNAVAILABLE (was 500)', async () => {
     mode['github.com/login/oauth/access_token'] = 'deadport';
     const r = await call('POST', '/api/auth/social/link', { provider: 'github', code: 'c6' });
```
