# READY - KS-2066-KS-2066-O116-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2066_o116_p1_ks1539_plain_error_message_never_logged_cell/out.md.checker/patch.diff` (from `ls` at 17:47 2026-11-09; sha256[:16] b89a3af75fe73dfe, 995 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 17:47 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2066_o116_p1_ks1539_plain_error_message_never_logged_cell/out.md.checker`; product bytes were RE-MEASURED here.** Tip `e8d23ce366e292ed6ca13f296cc2cfb2a3796496`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-create-path-logs-a-thrown-allow-list-read.test.ts']; `+` lines 11 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` blob a5e55ac8b59a; plant file(s) also unchanged.
- Red cells [input.json]:
  - `KS-2066 F3: a rejected plain Error whose message quotes stored text`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-create-path-logs-a-thrown-allow-list-read.test.ts)`
  - `PASS A3p the plant applies at the tip (1 pinned line(s))`
  - `PASS A4 GREEN WITHOUT PLANT: 1 red cell(s) exist and pass on the unmodified product; declared files 7 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1880 -> 1881, red 0 -> 0`
  - `PASS A5 RED WITH PLANT: 1 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/api-gateway/src/routes/verification.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-create-path-logs-a-thrown-allow-list-read.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-create-path-logs-a-thrown-allow-list-read.test.ts
@@ -187,4 +187,15 @@
     ]);
     expect(routeWarns()).toEqual([]);
   });
+
+  // KS-2066 F3 (gate 213): "never the message" is pinned above for a SyntaxError only. A plain Error whose message quotes stored text must not reach a log line either.
+  it('CONTROL KS-2066 F3: a rejected plain Error whose message quotes stored text logs the class Error and none of that text', async () => {
+    readSpy.mockImplementationOnce(async () => {
+      throw new Error(`redis reply [x-${QUOTED}] was refused`);
+    });
+    const r = await create();
+    expect([r.status, r.code]).toEqual([503, 'SERVICE_UNAVAILABLE']);
+    expect(routeWarns().map(([, , errorClass]) => errorClass)).toEqual(['Error']);
+    expect(JSON.stringify(logs)).not.toContain(QUOTED);
+  });
 });
```
