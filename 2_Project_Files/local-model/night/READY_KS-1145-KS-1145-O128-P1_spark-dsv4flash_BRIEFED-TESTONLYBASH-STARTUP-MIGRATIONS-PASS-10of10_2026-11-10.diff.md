# READY - KS-1145-KS-1145-O128-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_bash/plant) - PASS 10/10 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1145_o128_p1_ks949_suite_slug_only_drift_cell/out.md.checker/patch.diff` (from `ls` at 07:16 2026-11-10; sha256[:16] 62c45d9f9cfdb484, 1507 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 07:16 2026-11-10 by Spark operator o128 after a source read (hold_ready.py, test_only_bash path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1145_o128_p1_ks949_suite_slug_only_drift_cell/out.md.checker`; product and plant-file bytes were RE-MEASURED here.** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`. Brief: not given (--brief) and not located
- Touched set [patch.diff `+++` headers == sections.json == `git apply --numstat` == input.json test_files; no product or plant file named]: ['Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh']; `+` lines 12 (ASCII), `-` lines 1.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/api-gateway/src/startup-migrations.ts` blob 9416120ef9de; plant file(s) also unchanged.
- Red cells [input.json]:
  - `ID4: slug-only drift on a second id`
- Red evidence under the plant [red_with_plant__*.out, the suite's own FAIL line per red cell, verbatim]:
  - `FAIL — ID4: slug-only drift on a second id was not repaired, command tag 'UPDATE 0', slug 'slug-only-drift'`
- Plant file(s) [input.json plant_diff / plant; applied in the checker's clone only]: ['Blockchain/Dev/services/api-gateway/src/startup-migrations.ts']
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh)`
  - `PASS A3p the plant applies at the tip (1 pinned line(s))`
  - `PASS A3s every patched suite parses (bash -n)`
  - `PASS A4 GREEN WITHOUT PLANT: 1 named cell(s) exist and pass on the unmodified product; declared suites 28 cells, 0 red, rc [0]`
  - `PASS A6 WHOLE SUITE no worse: declared cells 27 -> 28 (none lost); 0 sibling suite(s) 0 -> 0 cells, FAIL lines 0 -> 0`
  - `PASS A5 RED WITH PLANT: 1 named cell(s) print the suite's own FAIL line under the plant (Blockchain/Dev/services/api-gateway/src/startup-migrations.ts) and pass without it; rc [1]; e.g. ks949_main_seed_idempotence.test.sh: FAIL — ID4: slug-only drift on a second id was not repaired, command tag`
  - `PASS A8 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- Checker INFO lines [checker.out, verbatim]:
  - `INFO baseline at the tip: declared suites 27 cell(s), 0 FAIL line(s), rc {'Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh': 0}; 0 sibling suite(s) 0 cell(s), 0 FAIL line(s)`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_bash)`

**PR NOTES for the raise seat:** TEST_ONLY_BASH (plant shape) - bash suite bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief plant (checker clone only), not a change in the PR. DOES NOT PROVE the plant is the regression that matters, or that a cell catches a different fault; an INFO line above is the checker's own note and is not a leg. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh
@@ -81,3 +81,3 @@
 PGPORT_NAME=54329          # only ever a socket FILE name: no TCP is bound
-TOTAL_CELLS=27   # KS-962 round 2: +ID3, the IS DISTINCT FROM guard's regression cell
+TOTAL_CELLS=28   # KS-962 round 2: +ID3, the IS DISTINCT FROM guard's regression cell; KS-1145: +ID4, the slug arm
 
@@ -318,4 +318,15 @@
 fi
 
+# KS-1145 (gate item 2): AG4 plants drift on BOTH columns, so either arm of the guard alone repairs its fixture.
+# ID4 plants drift on the SLUG only of a second id (its tenant_id is untouched): only the slug arm of the guard can see it,
+# and a guard without that arm reads UPDATE 0 and leaves the slug drifted.
+PSQL ag <<<"UPDATE users SET tenant_slug='slug-only-drift' WHERE id='c1000000-0000-4000-8000-000000000001';" >/dev/null
+OUT=$(PSQL ag <<<"$STMT"); SLUGAFTER=$(PSQL ag <<<"SELECT tenant_slug FROM users WHERE id='c1000000-0000-4000-8000-000000000001';")
+if [ "$OUT" = "UPDATE 1" ] && [ "$SLUGAFTER" = "oxford-university" ]; then
+  ok "ID4: slug-only drift on a second id is repaired, UPDATE 1 and the slug restored (the slug arm of the IS DISTINCT FROM guard)"
+else
+  bad "ID4: slug-only drift on a second id was not repaired, command tag '$(printf '%s' "$OUT" | one_line 40)', slug '$SLUGAFTER'"
+fi
+
 # --- 10. Controls ------------------------------------------------------------------
 echo "  -- controls"
```
