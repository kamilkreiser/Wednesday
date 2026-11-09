# READY - KS-1415-KS-1415-O114-P3 (Spark (DeepSeek V4 Flash), briefed, test_only_bash/plant) - PASS 10/10 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1415_o114_p3_prometheus_suite_count_cells_for_the_gateway_host_port/out.md.checker/patch.diff` (from `ls` at 16:33 2026-11-09; sha256[:16] 05f8d272cf7376a2, 1051 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 16:33 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_bash path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1415_o114_p3_prometheus_suite_count_cells_for_the_gateway_host_port/out.md.checker`; product and plant-file bytes were RE-MEASURED here.** Tip `204e62acdc351e664f9a1ca49a058275e9b3e907`. Brief: not given (--brief) and not located
- Touched set [patch.diff `+++` headers == sections.json == `git apply --numstat` == input.json test_files; no product or plant file named]: ['Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh']; `+` lines 7 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `observability/.env.example` blob 6fef48d07180, `observability/config/alerting.env.example` blob 60c0973900fb; plant file(s) also unchanged.
- Red cells [input.json]:
  - `observability/.env.example names the gateway host port 6882 on no line`
  - `observability/config/alerting.env.example names the gateway host port 6882 on no line`
- Red evidence under the plant [red_with_plant__*.out, the suite's own FAIL line per red cell, verbatim]:
  - `FAIL observability/.env.example names the gateway host port 6882 on no line`
  - `FAIL observability/config/alerting.env.example names the gateway host port 6882 on no line`
- Plant file(s) [input.json plant_diff / plant; applied in the checker's clone only]: ['observability/.env.example', 'observability/config/alerting.env.example']
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh)`
  - `PASS A3p the plant applies at the tip (2 pinned line(s))`
  - `PASS A3s every patched suite parses (bash -n)`
  - `PASS A4 GREEN WITHOUT PLANT: 2 named cell(s) exist and pass on the unmodified product; declared suites 8 cells, 0 red, rc [0]`
  - `PASS A6 WHOLE SUITE no worse: declared cells 6 -> 8 (none lost); 0 sibling suite(s) 0 -> 0 cells, FAIL lines 0 -> 0`
  - `PASS A5 RED WITH PLANT: 2 named cell(s) print the suite's own FAIL line under the plant (observability/.env.example, observability/config/alerting.env.example) and pass without it; rc [1]; e.g. prometheus_targets.test.sh: FAIL observability/.env.example names the gateway host port 6882 on no line`
  - `PASS A8 RESTORE: 3 watched file(s) back at their tip sha256; tracked tree clean`
- Checker INFO lines [checker.out, verbatim]:
  - `INFO baseline at the tip: declared suites 6 cell(s), 0 FAIL line(s), rc {'Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh': 0}; 0 sibling suite(s) 0 cell(s), 0 FAIL line(s)`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_bash)`

**PR NOTES for the raise seat:** TEST_ONLY_BASH (plant shape) - bash suite bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief plant (checker clone only), not a change in the PR. DOES NOT PROVE the plant is the regression that matters, or that a cell catches a different fault; an INFO line above is the checker's own note and is not a leg. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh
@@ -120,4 +120,11 @@
     "# SECUURA_NGINX_STATUS_URI=http://secuura-nginx-gateway:80/stub_status" \
     "$(grep -m1 'SECUURA_NGINX_STATUS_URI=' "$DEV_ROOT/../../observability/.env.example")"
 
+# KS-1415 (gate62 minor 2): the two first-line pins above read only the FIRST SECUURA_NGINX_STATUS_URI line, so a later active line
+# that names the gateway's host port 6882 passes them. A count is blind to position: no line of either example may name the gateway on 6882.
+expect "observability/.env.example names the gateway host port 6882 on no line" "0" \
+    "$(grep -c 'secuura-nginx-gateway:6882' "$DEV_ROOT/../../observability/.env.example")"
+expect "observability/config/alerting.env.example names the gateway host port 6882 on no line" "0" \
+    "$(grep -c 'secuura-nginx-gateway:6882' "$DEV_ROOT/../../observability/config/alerting.env.example")"
+
 echo "prometheus_targets: ${PASS} passed, ${FAIL} failed"
```
