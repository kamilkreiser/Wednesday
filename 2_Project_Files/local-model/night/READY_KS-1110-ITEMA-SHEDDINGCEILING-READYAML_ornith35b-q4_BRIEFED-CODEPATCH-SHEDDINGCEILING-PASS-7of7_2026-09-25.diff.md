# READY — KS-1110-ITEMA-SHEDDINGCEILING-READYAML (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1110-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 13:23 2026-09-25; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1110-ornith35b-night/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 13:23 2026-09-25 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1110-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (self-testing) touched-file set == { systemTest/performance/tests/unit/config/sheddingCeiling.test.ts } — one file that is both the product and its test (under systemTest/performance/tests/unit)`
- Declared set [input.json product_file + suggested_test_file]: `systemTest/performance/tests/unit/config/sheddingCeiling.test.ts` (product) and `systemTest/performance/tests/unit/config/sheddingCeiling.test.ts` (test) — equal to numstat.out's set (1 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	3	systemTest/performance/tests/unit/config/sheddingCeiling.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (14 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 14 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied systemTest/performance/tests/unit/config/sheddingCeiling.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 14 line(s) byte-exact incl. leading whitespace (of 14; 14 line(s) added by the apply)` [a3i_indent.out: `OK 14 line(s) byte-exact incl. leading whitespace (of 14; 14 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `systemTest/performance/tests/unit/config/sheddingCeiling.test.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: tests/unit/config/sheddingCeiling.test.ts fails at the untouched tip (1 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=1 of total=6; red cell(s): ['load-shedding scenarios KS-1110 red-first: this suite reads scenarios.yml through readYaml, never a direct parser import']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: tests/unit/config/sheddingCeiling.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1085 failed=1 | after: total=1087 failed=1` · `NEW reds: []` [baseline_suite.json total=1085 failed=1; after_suite.json total=1087 failed=1]
- A6 [verbatim]: `PASS A6 whole . suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for .: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +14/-3 test=tests/unit/config/sheddingCeiling.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `systemTest/performance/tests/unit/config/sheddingCeiling.test.ts` (+14/-3 per numstat.out) — ONE file: it is both the product and its test (self-testing mode; red-first is by HUNK, not by file). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1110-ornith35b-night/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1110-ornith35b-night/checker.out`.

```diff
--- a/systemTest/performance/tests/unit/config/sheddingCeiling.test.ts
+++ b/systemTest/performance/tests/unit/config/sheddingCeiling.test.ts
@@ -28,4 +28,3 @@
 import { describe, expect, it } from 'vitest';
-import * as yaml from 'js-yaml';
-
+import { readYaml } from '../../../utils/yaml.ts';
 const perfRoot = join(dirname(fileURLToPath(import.meta.url)), '..', '..', '..');
@@ -43,6 +42,6 @@
  * @returns {Record<string, ScenarioConfig>} Every scenario from `config/scenarios.yml`.
  */
 function loadScenarios(): Record<string, ScenarioConfig> {
-    const raw = yaml.load(readFileSync(join(perfRoot, 'config', 'scenarios.yml'), 'utf8')) as Record<string, unknown>;
+    const raw = readYaml(join(perfRoot, 'config', 'scenarios.yml')) as Record<string, unknown>;
     return (raw['scenarios'] ?? raw) as Record<string, ScenarioConfig>;
 }
@@ -126,4 +125,16 @@
             expect(scenarios[name]?.thresholds?.['http_rate_limited']).toBeUndefined();
         }
     });
+    it('KS-1110 red-first: this suite reads scenarios.yml through readYaml, never a direct parser import', () => {
+        // KS-1110 (QA-960-2): readYaml() is the one door that keeps a malformed file out of the test output.
+        const needle = ['js', 'yaml'].join('-');
+        const own = readFileSync(fileURLToPath(import.meta.url), 'utf8').split(String.fromCharCode(10));
+        const direct = own.filter((line) => line.startsWith('import') && line.includes(needle));
+        expect(direct).toEqual([]);
+    });
+    it('KS-1110 CONTROL: loadScenarios still reads the spike and spike-short scenarios', () => {
+        const names = Object.keys(loadScenarios());
+        expect(names).toContain('spike');
+        expect(names).toContain('spike-short');
+    });
 });
```
