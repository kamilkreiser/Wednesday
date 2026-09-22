# READY — KS-1239-RAWAUTHDEAD-R16B (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `2_Project_Files/local-model/runs/2026-09-22_ks1239-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 15:30 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1239-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1239-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `2_Project_Files/local-model/runs/2026-09-22_feed13-drafter-precheck/RAWAUTHDEAD/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers differ (index.ts: golden `@@ -331,24 +331,6 @@` vs run `@@ -331,24 +331,6 @@ app.use((req, _res, next) => {`); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 15:30 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `2_Project_Files/local-model/runs/2026-09-22_ks1239-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3bad652d17cf111c1e2e1bed1ae7686894637487`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/index.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/index.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
0	18	Blockchain/Dev/services/api-gateway/src/index.ts
39	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `[no PASS A3c line in checker.out — DELETION-ONLY product hunk: numstat.out +0/-18 on Blockchain/Dev/services/api-gateway/src/index.ts; checker.out INFO A3i verbatim: `INFO A3i skipped — the input carries no expected '+' lines (a legacy or brief-less input); indentation not measured`]` — no expected_plus in the input; not re-measured here.
- A3i line absent from checker.out (not claimed)
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1239: the pre-auth rawAuthorization copy in index.ts is dead code and is gone RED KS-1239 A: index.ts takes no rawAuthorization copy of the Authorization header', 'KS-1239: the pre-auth rawAuthorization copy in index.ts is dead code and is gone RED KS-1239 B: no gateway middleware assigns req.headers.authorization onto req before auth runs']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=742 failed=0 | after: total=746 failed=0` · `NEW reds: []` [baseline_suite.json total=742 failed=0; after_suite.json total=746 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +39/-18 test=src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/index.ts` (+0/-18 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts` (+39/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3bad652d17cf111c1e2e1bed1ae7686894637487` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `2_Project_Files/local-model/runs/2026-09-22_ks1239-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1239-R16B-RAWAUTHDEAD.md`. Verdict source: `2_Project_Files/local-model/runs/2026-09-22_ks1239-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/index.ts
+++ b/Blockchain/Dev/services/api-gateway/src/index.ts
@@ -331,24 +331,6 @@ app.use((req, _res, next) => {
   stripTrustHeaders(req.headers as unknown as Record<string, unknown>);
   next();
 });
-
-// BUG-PLATFORM-AUTH-001 (2026-05-01): capture the raw Authorization header
-// at request entry, BEFORE any other middleware can mutate or consume
-// req.headers.authorization. Some downstream proxy paths (e.g.
-// routes/platform.ts → tenant-provisioning) need to forward the original
-// bearer token to internal services that JWT-verify directly. Symptom
-// before this fix: GET /api/platform/tenants returned 502 because the
-// inline proxy's `req.headers.authorization` read was empty by the time
-// the handler ran, and tenant-prov returned `Error: No token provided`,
-// which gateway's `r.json()` then failed to parse (HTML stack trace),
-// producing an unhelpful 502.
-app.use((req, _res, next) => {
-  if (req.headers.authorization) {
-    (req as any).rawAuthorization = req.headers.authorization;
-  }
-  next();
-});
-
 // AUDIT B-7 / D-2: refuse to start with wildcard origin in production-like
 // environments. With credentials:true, `*` is spec-illegal AND a CSRF
 // refresh-token exfil risk. Same rule for any wildcard-subdomain entry.
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts
@@ -0,0 +1,39 @@
+/**
+ * KS-1239: index.ts:347 copied req.headers.authorization onto req.rawAuthorization at request
+ * entry, BEFORE authentication ran. #1034 (KS-1215) made routes/platform.ts authHeaders forward
+ * req.headers.authorization instead, so the copy has 0 readers at the tip and is exactly the trap
+ * KS-1215 fell into: a pre-auth copy that delete req.headers.authorization cannot touch. This
+ * suite reads the gateway source the way ks689-users-admin-create-auth-mount.test.ts does and
+ * pins that the copy is gone and that nothing reads it.
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const GATEWAY_SRC = readFileSync(join(__dirname, '..', 'index.ts'), 'utf8');
+const PLATFORM_SRC = readFileSync(join(__dirname, '..', 'routes', 'platform.ts'), 'utf8');
+
+function occurrences(haystack: string, needle: string): number {
+  return haystack.split(needle).length - 1;
+}
+
+describe('KS-1239: the pre-auth rawAuthorization copy in index.ts is dead code and is gone', () => {
+  it('RED KS-1239 A: index.ts takes no rawAuthorization copy of the Authorization header', () => {
+    expect(occurrences(GATEWAY_SRC, 'rawAuthorization')).toBe(0);
+  });
+
+  it('RED KS-1239 B: no gateway middleware assigns req.headers.authorization onto req before auth runs', () => {
+    expect(occurrences(GATEWAY_SRC, '.rawAuthorization = req.headers.authorization')).toBe(0);
+    expect(occurrences(GATEWAY_SRC, 'BUG-PLATFORM-AUTH-001')).toBe(0);
+  });
+
+  it('control: the trust-header strip stays mounted at request entry', () => {
+    expect(occurrences(GATEWAY_SRC, 'stripTrustHeaders(req.headers as unknown as Record<string, unknown>);')).toBe(1);
+  });
+
+  it('control: routes/platform.ts authHeaders forwards req.headers.authorization and reads no rawAuthorization', () => {
+    expect(occurrences(PLATFORM_SRC, 'const auth = req.headers.authorization;')).toBe(1);
+    expect(occurrences(PLATFORM_SRC, 'req.rawAuthorization')).toBe(0);
+    expect(occurrences(PLATFORM_SRC, '(req as any).rawAuthorization')).toBe(0);
+  });
+});
```
