# READY — KS-1388-ENVEXAMPLE-1 (Spark deepseek-v4-flash-0731, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> **HAND-EDITED 2026-10-05 by the Spark brief-writer sub-agent (seat 8e88f5e9), marked:** hold_ready.py (bash_patch path) wrote `Ornith` / `ornith35b-q4`; this run's backend is `spark` / `deepseek-v4-flash-0731` (`out.md.meta.json`), so the heading word and the filename tag were corrected by `mv` + this edit (as-written copy: `night/briefs/KS-1388-envexample/READY.md.pre-1005-modeltag`). The bash checker has no A2a leg; A2a was run by hand (`a2a_anchor.py` over `sections_with_n.json`): `SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0` rc 0.

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1388-envexample/out.md.checker/patch.diff`** (from `ls` at 02:29 2026-10-05; sha256[:16] e50bdc17f06010fe, 1570 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1388-envexample/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1388-envexample/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1388-envexample/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1388-envexample/precheck/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 02:29 2026-10-05 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1388-envexample/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2d85b84e1012961c880daa3de70d8491fc0a2ff9`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 2d85b84e1012961c880daa3de70d8491fc0a2ff9, observability/.env.example and Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['observability/.env.example', 'Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { observability/.env.example , Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh (MODIFIED in place — test_file pinned to an existing suite, 2026-09-16 KS-1163) }`
- Declared set [input.json product_file + suggested_test_file]: `observability/.env.example` (script) and `Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh` (MODIFIED in place) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 1 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `observability/.env.example` (+1/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh` (+9/-1 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh fails at the untouched tip (rc=1, 1 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=1 pass_lines=4 load_error=0 timeout=0` [red_first.out re-count: 1 FAIL line(s), 4 pass line(s); FAIL lines: ["FAIL observability/.env.example suggests the gateway's in-network status port"]]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive .env.example: no NEW failure after (2 suite(s))` [2 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `observability/.env.example` (+1/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the MODIFIED test `Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh` (+9/-1); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `2d85b84e1012961c880daa3de70d8491fc0a2ff9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1388-envexample/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1388-envexample/checker.out`.

```diff
--- a/observability/.env.example
+++ b/observability/.env.example
@@ -44,5 +44,5 @@
 # SECUURA_PG_DSN=postgresql://secuura:secuura_dev_password@secuura-postgres:5432/secuura?sslmode=disable
 # SECUURA_REDIS_ADDR=redis://secuura-redis:6379
 # SECUURA_REDIS_PASSWORD=secuura_redis_dev
-# SECUURA_NGINX_STATUS_URI=http://secuura-nginx-gateway:6882/stub_status
+# SECUURA_NGINX_STATUS_URI=http://secuura-nginx-gateway:80/stub_status
 # SECUURA_KAFKA_BROKER=secuura-kafka:9092
--- a/Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh
@@ -103,6 +103,14 @@
 # which nginx-exporter already scrapes and re-exports on 9113.
 expect "no scrape target uses the gateway's published host port" "0" \
     "$(grep -c "secuura-nginx-gateway:6882" <<<"$prom_live")"
-
+
+# --- the stack env example must not suggest the gateway's HOST port either (KS-1388) ---
+# observability/.env.example offers SECUURA_NGINX_STATUS_URI as a commented override. The exporter runs on
+# the container network, as Prometheus does, so the rule above holds for it too: 80, never the 6882 host
+# publish. observability/docker-compose.yml already defaults to :80; the example must agree with it.
+expect "observability/.env.example suggests the gateway's in-network status port" \
+    "# SECUURA_NGINX_STATUS_URI=http://secuura-nginx-gateway:80/stub_status" \
+    "$(grep -m1 'SECUURA_NGINX_STATUS_URI=' "$DEV_ROOT/../../observability/.env.example")"
+
 echo "prometheus_targets: ${PASS} passed, ${FAIL} failed"
 (( FAIL == 0 ))
```
