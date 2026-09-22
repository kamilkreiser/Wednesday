# READY — KS-629-629LIVENESSSPEC-R16B (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 12:18 2026-09-22; it is `cat` of the section files in order: NOTE — `cat section_*.diff | cmp patch.diff` rc 1, the sections are the applied units: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed10-drafter-precheck/LIVENESSSPEC/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); file headers DIFFER (run ['+++ b/Blockchain/Dev/services/kyc/src/kyc.openapi.ts', '+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts'] vs golden ['+++ b/Blockchain/Dev/services/kyc/src/kyc.openapi.ts', '+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629b-liveness-video-removed-from-openapi-schema.test.ts']); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 12:18 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/kyc/src/kyc.openapi.ts , Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/kyc/src/kyc.openapi.ts` (product) and `Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	9	Blockchain/Dev/services/kyc/src/kyc.openapi.ts
64	0	Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (4 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 4 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 9.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/kyc/src/kyc.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)` [a3i_indent.out: `OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/kyc/src/kyc.openapi.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=1 of total=3; red cell(s): ['KS-629 Part B: the published selfie schema no longer declares livenessVideo RED KS-629 B: livenessVideo is not declared anywhere in the code of kyc.openapi.ts']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts passes with the product hunk (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=26 failed=0 | after: total=29 failed=0` · `NEW reds: []` [baseline_suite.json total=26 failed=0; after_suite.json total=29 failed=0]
- A6 [verbatim]: `PASS A6 whole services/kyc suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/kyc: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +68/-9 test=src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/kyc/src/kyc.openapi.ts` (+4/-9 per numstat.out) and the test file `Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts` (+64/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/kyc/src/kyc.openapi.ts
+++ b/Blockchain/Dev/services/kyc/src/kyc.openapi.ts
@@ -183,5 +183,6 @@
       // KS-430: runtime (submitSelfieSchema) also requires verificationId (the target
-      // session) and accepts an optional livenessVideo; the spec declared only
-      // selfieImage, so a spec-minimal body earned a 400. Reconciled to the live contract.
-      // KS-444: residual drift -- verificationId is a uuid at runtime (session ids
+      // session); the spec declared only selfieImage, so a spec-minimal body earned a
+      // 400. Reconciled to the live contract. KS-629: livenessVideo was declared here
+      // and read by nothing - removed from schema and spec (Kam, 2026-09-16).
+      // KS-444: residual drift - verificationId is a uuid at runtime (session ids
       // are uuids); published as documentation of reality.
@@ -193,10 +194,4 @@
           'Anything else is a 400 INVALID_IMAGE.',
       }),
-      livenessVideo: z.string().optional().openapi({
-        description:
-          'Accepted by the schema but NOT stored or processed by any code path ' +
-          'today -- see KS-629. Documented as inert rather than left to read as a ' +
-          'working upload.',
-      }),
     })
     .passthrough().openapi({
--- /dev/null
+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts
@@ -0,0 +1,64 @@
+// KS-629 Part B: livenessVideo is GONE from the published OpenAPI selfie schema.
+//
+// The field was declared in KycSelfieUploadRequest (kyc.openapi.ts) and by the
+// runtime schema (Part A) and read by nothing; Kam ruled 2026-09-16 that both
+// declarations go. This guard reads the file as TEXT with comments stripped (the
+// ks386 shape), so a comment that merely mentions the field cannot red it.
+// The stripper walks lines with indexOf: no regex, no escapes.
+
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const NL = String.fromCharCode(10);
+const SRC = readFileSync(join(__dirname, '..', 'kyc.openapi.ts'), 'utf8');
+
+/** Block comments and line comments removed, so the guard matches CODE, never prose (a url keeps its colon-slash-slash). */
+function codeOnly(source: string): string {
+  const kept: string[] = [];
+  let inBlock = false;
+  for (const line of source.split(NL)) {
+    let text = line;
+    if (inBlock) {
+      const close = text.indexOf('*/');
+      if (close < 0) continue;
+      inBlock = false;
+      text = text.slice(close + 2);
+    }
+    const open = text.indexOf('/*');
+    if (open >= 0) {
+      const close = text.indexOf('*/', open + 2);
+      if (close < 0) {
+        inBlock = true;
+        text = text.slice(0, open);
+      } else {
+        text = text.slice(0, open) + ' ' + text.slice(close + 2);
+      }
+    }
+    if (text.trimStart().startsWith('//')) text = '';
+    const slash = text.indexOf(' //');
+    if (slash >= 0) text = text.slice(0, slash);
+    kept.push(text);
+  }
+  return kept.join(NL);
+}
+
+const CODE = codeOnly(SRC);
+
+describe('KS-629 Part B: the published selfie schema no longer declares livenessVideo', () => {
+  it('RED KS-629 B: livenessVideo is not declared anywhere in the code of kyc.openapi.ts', () => {
+    expect(CODE).not.toContain('livenessVideo');
+  });
+
+  it('control: KycSelfieUploadRequest, selfieImage and verificationId are still declared in the selfie schema', () => {
+    expect(CODE).toContain('KycSelfieUploadRequest');
+    expect(CODE).toContain('selfieImage: z.string().openapi({');
+    expect(CODE).toContain('verificationId: z.string().uuid()');
+  });
+
+  it('control: the comment stripper eats a line comment and a block comment and keeps a url', () => {
+    expect(codeOnly('const a = 1; // livenessVideo: z.string()')).not.toContain('livenessVideo');
+    expect(codeOnly('/* livenessVideo */ const b = 2;')).not.toContain('livenessVideo');
+    expect(codeOnly('const d = https://docs.secuura.io;')).toContain('https://docs.secuura.io');
+  });
+});
```
