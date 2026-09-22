# READY — KS-629-629LIVENESSRT-R16B (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 12:25 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed10-drafter-precheck/LIVENESSRT/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); file headers DIFFER (run ['+++ b/Blockchain/Dev/services/kyc/src/index.ts', '+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts'] vs golden ['+++ b/Blockchain/Dev/services/kyc/src/index.ts', '+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629a-liveness-video-removed-from-runtime-schema.test.ts']); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 12:25 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/kyc/src/index.ts , Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/kyc/src/index.ts` (product) and `Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
0	1	Blockchain/Dev/services/kyc/src/index.ts
63	0	Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `[no PASS A3c line in checker.out — DELETION-ONLY product hunk: numstat.out +0/-1 on Blockchain/Dev/services/kyc/src/index.ts; checker.out INFO A3i verbatim: `INFO A3i skipped — the input carries no expected '+' lines (a legacy or brief-less input); indentation not measured`]` — no expected_plus in the input; not re-measured here.
- A3i line absent from checker.out (not claimed)
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/kyc/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=1 of total=3; red cell(s): ['KS-629 Part A: the runtime selfie schema no longer accepts livenessVideo RED KS-629 A: livenessVideo is not declared anywhere in the code of index.ts']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts passes with the product hunk (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=26 failed=0 | after: total=29 failed=0` · `NEW reds: []` [baseline_suite.json total=26 failed=0; after_suite.json total=29 failed=0]
- A6 [verbatim]: `PASS A6 whole services/kyc suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/kyc: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +63/-1 test=src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/kyc/src/index.ts` (+0/-1 per numstat.out) and the test file `Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts` (+63/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks629-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/kyc/src/index.ts
+++ b/Blockchain/Dev/services/kyc/src/index.ts
@@ -533,3 +533,2 @@
   selfieImage: z.string(), // Base64 encoded
-  livenessVideo: z.string().optional(), // Base64 encoded video
 });
--- /dev/null
+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts
@@ -0,0 +1,63 @@
+// KS-629 Part A: livenessVideo is GONE from the runtime selfie schema.
+//
+// The field was accepted by submitSelfieSchema (index.ts) and by the OpenAPI
+// schema (Part B) and read by nothing; Kam ruled 2026-09-16 that both
+// declarations go. index.ts boots a listener at module load, so this guard
+// reads it as TEXT with comments stripped (the ks386 shape) rather than
+// importing it. The stripper walks lines with indexOf: no regex, no escapes.
+
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const NL = String.fromCharCode(10);
+const SRC = readFileSync(join(__dirname, '..', 'index.ts'), 'utf8');
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
+describe('KS-629 Part A: the runtime selfie schema no longer accepts livenessVideo', () => {
+  it('RED KS-629 A: livenessVideo is not declared anywhere in the code of index.ts', () => {
+    expect(CODE).not.toContain('livenessVideo');
+  });
+
+  it('control: selfieImage and verificationId are still declared in the selfie schema', () => {
+    expect(CODE).toContain('selfieImage: z.string()');
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
