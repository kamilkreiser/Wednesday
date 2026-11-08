# READY - KS-2138-KS-2138-O111-P1 (spark-dsv4flash, briefed, doc_only, markdown) - PASS 10/10 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2138_o111_p1_cheat_fragment_cells_row_says_g1_to_g6_but_g6_is_red_on_develop/out.md.checker/patch.diff` (from `ls` at 08:19 2026-11-09; sha256[:16] 4a47dd3596504525, 1479 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 08:19 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2138_o111_p1_cheat_fragment_cells_row_says_g1_to_g6_but_g6_is_red_on_develop/out.md.checker`; the expectations were RE-MEASURED here.** Tip `425ea1d3df0fec9186f994d54b9da62beaf8f4e9`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Projects Documents/fragments/cheat/KS-528-react-router-v7-portals.html']; `+` lines 1 (ASCII), `-` lines 1.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Projects Documents/fragments/cheat/KS-528-react-router-v7-portals.html)`
  - `PASS A4 RED AT BASE: all 2 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (0 comment line(s) changed in 0 code file(s); 1 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 2 expectation(s) hold after the patch`
  - `PASS A6 DOC CHECK `node Blockchain/Dev/scripts/docs-fragments.mjs check` rc 0 after the patch (rc 0 at the tip)`
  - `PASS A7 REVERSION: with the patch reverse-applied, 2/2 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `and nothing for G1 to G6` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `and nothing for G1 to G5; G6 is red on develop by design` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Projects Documents/fragments/cheat/KS-528-react-router-v7-portals.html
+++ b/Projects Documents/fragments/cheat/KS-528-react-router-v7-portals.html
@@ -9,7 +9,7 @@
 <h3>Figures</h3>
 <table>
 <tr><th>Figure</th><th>Value</th></tr>
-<tr><td>cells</td><td><strong>25</strong> in 1 new file (16 in round 1, 9 added in round 2); against develop b7d433fda83c the checker reports R1 (23 files), R2 (6 lines), R3 (8 lines), R4 (2 rows) and nothing for G1 to G6</td></tr>
+<tr><td>cells</td><td><strong>25</strong> in 1 new file (16 in round 1, 9 added in round 2); against develop b7d433fda83c the checker reports R1 (23 files), R2 (6 lines), R3 (8 lines), R4 (2 rows) and nothing for G1 to G5; G6 is red on develop by design</td></tr>
 <tr><td>round 2, red first</td><td>6 new R mutants (optionalDependencies, peerDependencies, overrides flat and nested, a <code>.cjs</code> and a <code>.cts</code> file) failed against the round-1 checker and pass after it was widened; G6 failed on the real tree until the one-line change</td></tr>
 <tr><td>planted tampers</td><td><strong>32 of 32</strong> (round 1, 2026-11-06) turned their named rule red and were restored byte-identical (sha256); not replayed in round 2</td></tr>
 <tr><td>builds</td><td>round 1: 3 of 3 on Node 24.22.2 and 3 of 3 on Node 26.8.1; control (develop, 6.30.6) 3 of 3. Round 2 (2026-11-08): the issuer, three builds, <strong>Node v26.8.1 only (not an LTS line)</strong>, <code>npm ci --offline</code></td></tr>
```
