# READY — KS-1543-IGNOREDCATCHES-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-15_ks_1543_p1/out.md.checker/patch.diff`** (from `ls` at 12:47 2026-10-15; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-15_ks_1543_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-15_ks_1543_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-15_ks_1543_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in verification.ts (run 16 vs golden 19 body lines — context, since the change lines are equal) (identical in ks1543-five-pre-existing-eslint-warnings-in.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 12:47 2026-10-15 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-15_ks_1543_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `e67e0dc1916b954a53c40db68ea81f0f905de641`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/verification.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-five-pre-existing-eslint-warnings-in.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-five-pre-existing-eslint-warnings-in.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/api-gateway/src/routes/verification.ts
47	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-five-pre-existing-eslint-warnings-in.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/routes/verification.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-five-pre-existing-eslint-warnings-in.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1543-five-pre-existing-eslint-warnings-in.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1543 part 1 - the two deliberately ignored catches in verification.ts lint clean RED KS-1543 C1 - the live-anchor fall-through catch is a bare catch with no lint message', 'KS-1543 part 1 - the two deliberately ignored catches in verification.ts lint clean RED KS-1543 C2 - the rejected-document DB fallback catch is a bare catch with no lint message']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1543-five-pre-existing-eslint-warnings-in.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1146 failed=0 | after: total=1150 failed=0` · `NEW reds: []` [baseline_suite.json total=1146 failed=0; after_suite.json total=1150 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +49/-2 test=src/__tests__/ks1543-five-pre-existing-eslint-warnings-in.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-five-pre-existing-eslint-warnings-in.test.ts` (+47/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `e67e0dc1916b954a53c40db68ea81f0f905de641` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-15_ks_1543_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1543_p1/KS-1543.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-15_ks_1543_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
@@ -649,7 +649,7 @@ export function createVerificationRoutes(deps: VerificationRouteDeps): Router {
             liveConfirmedAt = j.confirmedAt || j.anchoredAt || (j.anchor && j.anchor.confirmedAt) || null;
           }
         }
-      } catch (_err) {
+      } catch {
         // Network/timeout — fall through to persisted state. Verification
         // remains honest because we still report 'pending-onchain' rather
         // than fabricating.
@@ -1491,7 +1491,7 @@ export function createVerificationRoutes(deps: VerificationRouteDeps): Router {
           // Back-fill Redis from DB result (fire-and-forget)
           redisService.setRejectedDocument(id, rejection).catch(() => {});
         }
-      } catch (err: any) {
+      } catch {
         // Ignore DB errors - fallback to in-memory only
       }
     }
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-five-pre-existing-eslint-warnings-in.test.ts
@@ -0,0 +1,47 @@
+// KS-1543 (part 1 of 2) - two catches in routes/verification.ts drop their error ON PURPOSE (the live-anchor read falls
+// through to the persisted state; the rejected-document DB read falls back to memory), but they named the binding
+// (`_err`, `err: any`), and the shared flat config's no-unused-vars sets no caughtErrorsIgnorePattern, so even the
+// underscore name warned. Both are now a bare `catch {`, the form this file already uses elsewhere. These cells lint the
+// REAL file with the repo's own eslint.config.mjs through ESLint's Node API. Part 2 (the other three warnings) is not here.
+import { describe, it, expect } from 'vitest';
+import fs from 'fs';
+import path from 'path';
+import { ESLint } from 'eslint';
+
+const DEV = path.resolve(__dirname, '../../../..');
+const FILE = path.resolve(__dirname, '../routes/verification.ts');
+const eslint = new ESLint({ cwd: DEV });
+
+/** The line just above an anchor comment (1-based), its text, and every lint message ESLint reports on it. */
+async function catchAbove(anchor: string): Promise<{ text: string; messages: string[] }> {
+  const lines = fs.readFileSync(FILE, 'utf8').split('\n');
+  const at = lines.findIndex((line) => line.includes(anchor));
+  expect(at).toBeGreaterThan(0);
+  const [result] = await eslint.lintFiles([FILE]);
+  const messages = result.messages.filter((m) => m.line === at).map((m) => `${m.ruleId}: ${m.message}`);
+  return { text: lines[at - 1].trim(), messages };
+}
+
+describe('KS-1543 part 1 - the two deliberately ignored catches in verification.ts lint clean', () => {
+  it('RED KS-1543 C1 - the live-anchor fall-through catch is a bare catch with no lint message', async () => {
+    const { text, messages } = await catchAbove('// Network/timeout — fall through to persisted state.');
+    expect(text).toBe('} catch {');
+    expect(messages).toEqual([]);
+  }, 60_000);
+
+  it('RED KS-1543 C2 - the rejected-document DB fallback catch is a bare catch with no lint message', async () => {
+    const { text, messages } = await catchAbove('// Ignore DB errors - fallback to in-memory only');
+    expect(text).toBe('} catch {');
+    expect(messages).toEqual([]);
+  }, 60_000);
+
+  it('GREEN KS-1543 control - the instrument reports an unused caught binding, even one named with a leading underscore', async () => {
+    const [result] = await eslint.lintText('export function f(): void {\n  try {\n    f();\n  } catch (_e) {\n    // planted\n  }\n}\n', { filePath: FILE });
+    expect(result.messages.map((m) => m.ruleId)).toContain('@typescript-eslint/no-unused-vars');
+  }, 60_000);
+
+  it('GREEN KS-1543 control - verification.ts lints with 0 errors', async () => {
+    const [result] = await eslint.lintFiles([FILE]);
+    expect(result.errorCount).toBe(0);
+  }, 60_000);
+});
```
