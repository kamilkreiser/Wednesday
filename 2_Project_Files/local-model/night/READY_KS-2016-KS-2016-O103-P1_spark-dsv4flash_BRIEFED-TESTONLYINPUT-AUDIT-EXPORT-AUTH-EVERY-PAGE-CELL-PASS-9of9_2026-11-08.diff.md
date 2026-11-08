# READY - KS-2016-KS-2016-O103-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-08_ks_2016_o103_p1_audit_export_auth_every_page/out.md.checker/patch.diff` (from `ls` at 23:25 2026-11-08; sha256[:16] 003af42d382779ee, 1318 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 23:25 2026-11-08 by Spark operator 103 after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-08_ks_2016_o103_p1_audit_export_auth_every_page/out.md.checker`; product bytes were RE-MEASURED here.** Tip `abd044f63a9dd5673f1b9ff7a2b1e42e1c26de82`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-pages-its-rows-and-claims-no-type-filter.test.ts']; `+` lines 15 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` blob f221421c97d6; plant file(s) also unchanged.
- Red cells [input.json]:
  - `three upstream pages (2,300 rows) each carry`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-pages-its-rows-and-claims-no-type-filter.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 1 red cell(s) exist and pass on the unmodified product; declared files 13 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1840 -> 1841, red 0 -> 0`
  - `PASS A5 RED WITH PLANT: 1 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-pages-its-rows-and-claims-no-type-filter.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-pages-its-rows-and-claims-no-type-filter.test.ts
@@ -181,3 +181,18 @@
     expect([noTo.status, badFormat.status, fetchMock.mock.calls.length]).toEqual([400, 400, 0]);
   });
 });
+
+describe('KS-2016 - the caller\'s Authorization header goes upstream on every page, not only the first', () => {
+  it('RED KS-2016 A1: three upstream pages (2,300 rows) each carry the caller\'s Authorization header', async () => {
+    upstreamRows = manyRows(2300);
+    const status = await new Promise<number>((resolve, reject) => {
+      http.get({ hostname: '127.0.0.1', port, path: `/api/admin/audit/export?${RANGE}&format=json`, headers: { authorization: 'Bearer ks2016-caller' } }, (res) => {
+        res.resume();
+        res.on('end', () => resolve(res.statusCode ?? 0));
+      }).on('error', reject);
+    });
+    const sent = fetchMock.mock.calls.map((call) => ((call as unknown[])[1] as { headers?: Record<string, string> } | undefined)?.headers?.Authorization);
+    expect(status).toBe(200);
+    expect(sent).toEqual(['Bearer ks2016-caller', 'Bearer ks2016-caller', 'Bearer ks2016-caller']);
+  });
+});
```
