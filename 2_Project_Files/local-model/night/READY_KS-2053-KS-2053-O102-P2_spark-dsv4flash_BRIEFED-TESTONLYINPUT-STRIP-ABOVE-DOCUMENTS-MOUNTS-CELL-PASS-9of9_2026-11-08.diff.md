# READY - KS-2053-KS-2053-O102-P2 (spark-dsv4flash, briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-08_ks_2053_o102_p2_strip_above_documents_mounts/out.md.checker/patch.diff` (from `ls` at 23:05 2026-11-08; sha256[:16] a00e62174fd964eb, 1013 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 23:05 2026-11-08 by Spark operator 102 (Wednesday) after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-08_ks_2053_o102_p2_strip_above_documents_mounts/out.md.checker`; product bytes were RE-MEASURED here.** Tip `abd044f63a9dd5673f1b9ff7a2b1e42e1c26de82`. Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2053_o102_p2_strip_above_documents_mounts/KS-2053.md`
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/originate/src/__tests__/ks741-emitter-marker-strip.test.ts']; `+` lines 13 (ASCII), `-` lines 1.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/originate/src/index.ts` blob ed24308dd063; plant file(s) also unchanged.
- Red cells [input.json]:
  - `sits above BOTH /api/documents mounts`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/originate/src/__tests__/ks741-emitter-marker-strip.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 1 red cell(s) exist and pass on the unmodified product; declared files 8 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 2563 -> 2564, red 11 -> 11`
  - `PASS A5 RED WITH PLANT: 1 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/originate/src/index.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks741-emitter-marker-strip.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks741-emitter-marker-strip.test.ts
@@ -336,4 +336,16 @@
     expect(without).not.toBe(source); // the line was there to remove
     expect(mountLine(without, 'app.use(createEmitterMarkerStrip());')).toBe(-1);
   });
-});
+
+  it('the strip mount line sits above BOTH /api/documents mounts (KS-2053)', () => {
+    const source = fs.readFileSync(indexPath, 'utf8');
+    const strip = mountLine(source, 'app.use(createEmitterMarkerStrip());');
+    const publicDocuments = mountLine(source, "app.use('/api/documents', publicDocumentsRouter);");
+    const documents = mountLine(source, "app.use('/api/documents', documentsRouter);");
+    expect(strip).toBeGreaterThan(0);
+    expect(publicDocuments).toBeGreaterThan(0);
+    expect(documents).toBeGreaterThan(0);
+    expect(strip).toBeLessThan(publicDocuments);
+    expect(strip).toBeLessThan(documents);
+  });
+});
```
