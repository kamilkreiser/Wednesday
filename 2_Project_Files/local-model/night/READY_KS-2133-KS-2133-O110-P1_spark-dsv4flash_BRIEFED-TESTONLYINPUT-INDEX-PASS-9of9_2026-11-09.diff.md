# READY - KS-2133-KS-2133-O110-P1 (spark-dsv4flash, briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2133_o110_p1_spec_reload_same_length_and_whitespace_only_changed_spec/out.md.checker/patch.diff` (from `ls` at 06:51 2026-11-09; sha256[:16] 7c214f728232190a, 1233 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 06:51 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2133_o110_p1_spec_reload_same_length_and_whitespace_only_changed_spec/out.md.checker`; product bytes were RE-MEASURED here.** Tip `5d6a95c552fd131a166776076d951666b6de7329`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/api-gateway/src/__tests__/ks1505-spec-reload-warns-when-it-re-read-the-same-bytes.test.ts']; `+` lines 13 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/api-gateway/src/index.ts` blob 98376c5c14e4; plant file(s) also unchanged.
- Red cells [input.json]:
  - `RED KS-2133 - a changed spec of the SAME LENGTH`
  - `RED KS-2133 - a whitespace-only change`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/api-gateway/src/__tests__/ks1505-spec-reload-warns-when-it-re-read-the-same-bytes.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 2 red cell(s) exist and pass on the unmodified product; declared files 7 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1880 -> 1882, red 0 -> 0`
  - `PASS A5 RED WITH PLANT: 2 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/api-gateway/src/index.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1505-spec-reload-warns-when-it-re-read-the-same-bytes.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1505-spec-reload-warns-when-it-re-read-the-same-bytes.test.ts
@@ -90,6 +90,19 @@
     expect(g.lines()[0][1]).toBe(SUCCESS);
   }, 60_000);
 
+  it('RED KS-2133 - a changed spec of the SAME LENGTH as the one last loaded is a reload, not the same-bytes warning (the comparison is of the text, not its length)', async () => {
+    const g = await boot();
+    g.fire(g.bootRaw + '\n# ks1505: aa\n');
+    g.fire(g.bootRaw + '\n# ks1505: bb\n');
+    expect(g.lines()).toEqual([['info', SUCCESS], ['info', SUCCESS]]);
+  }, 60_000);
+
+  it('RED KS-2133 - a whitespace-only change (one added trailing newline) is a reload, not the same-bytes warning (the comparison is not made after trim)', async () => {
+    const g = await boot();
+    g.fire(g.bootRaw + '\n');
+    expect(g.lines()).toEqual([['info', SUCCESS]]);
+  }, 60_000);
+
   it('a reload that FAILS to parse keeps the previous text, logs the failure line, and the next same-bytes read of the previous text still warns', async () => {
     const g = await boot();
     g.fire('key: [unclosed');
```
