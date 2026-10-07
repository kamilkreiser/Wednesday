# READY — KS-1274 (Spark DeepSeek V4 Flash, briefed, bash_patch2 multi-file, rung 3) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1274-trivy-bare-object/out.md.checker/patch.diff`** (4 sections, 8 hunks). BYTE-IDENTICAL to the drafter's golden `2_Project_Files/local-model/night/briefs/KS-1274-trivy-bare-object/golden.diff` (`cmp -s` rc 0, Wednesday afternoon seat; control: same patch vs the KS-1355-stack-guard golden rc 1).

**Held BY HAND 15:15 2026-10-07 by Wednesday afternoon seat** (`hold_ready.py` has no bash_patch2 path yet: OWED). Every clause below is COPIED from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1274-trivy-bare-object/checker.out`, not typed. Tip `147ae442074c7f3b5be9ce7ccc4452c8dae34b4f`. **First round, round 1 of 2 (counter untouched).** Wednesday read the whole diff at source (security-scan job → personal read, not the 1-in-5 sample): the guard reads `$raw` (trivy's stdout, assigned at `04-container-trivy.sh:87` in the same loop, read at develop 147ae442074c), so the `jq -e 'has("Results") or has("ArtifactName")'` test reads the scan's own output; empty output also fails `jq -e`, so it stays a failed scan.

## Checker verdict lines (verbatim)
- PASS B0 subject: clone at 147ae442074c7f3b5be9ce7ccc4452c8dae34b4f, Blockchain/Testing/jobs/04-container-trivy.sh and Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh present
- PASS B1 output is exactly one fenced ```diff block
- PASS B2 every section applies at the tip (strict)
- PASS B3 (bash_patch2) touched-file set == the declared set: { Blockchain/Testing/jobs/04-container-trivy.sh } + { Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh , Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh , Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh }
- PASS B3b 1 must_change site(s) of 04-container-trivy.sh are '-' lines, no stays-site removed; all 2 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)
- PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0)
- PASS B4 RED-FIRST: with every test section and no product section — container_trivy_failed_scan_is_loud.test.sh=RED(rc 1, 1 FAIL) container_trivy_exit_code_env_keeps_findings.test.sh=green-support container_trivy_image_filter.test.sh=green-support
- PASS B5a every .sh product parses after the patch (bash -n)
- PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): container_trivy_failed_scan_is_loud.test.sh(5 pass) container_trivy_exit_code_env_keeps_findings.test.sh(6 pass) container_trivy_image_filter.test.sh(5 pass)
- PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (3 suite(s): aggregate_report_trivy_artefact.test.sh 5p/0f->5p/0f; ks1136_aggregate_report_unreadable_artefacts.test.sh 6p/0f->6p/0f; orchestrate_jobs.test.sh 18p/0f->18p/0f;)
- SUMMARY files=4 products=1 tests=3 red=1 support=2 red_first=yes apply_mode=strict
- PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=8 ok=8 bad=0 skipped_newfile=0)

## PR NOTES for the raise seat
- BASH_PATCH2 — PRODUCT `Blockchain/Testing/jobs/04-container-trivy.sh` (1 hunk); RED suite `container_trivy_failed_scan_is_loud.test.sh` (new bare-`{}` red cell + a CONTROL cell for trivy 0.71's clean report with `ArtifactName` and no `Results`, two stub modes, clean stub `{"Results":[]}`); SUPPORT suites `container_trivy_exit_code_env_keeps_findings.test.sh` and `container_trivy_image_filter.test.sh` (clean stub + its comment). The stub edits MUST land with the guard (product-alone reds both SUPPORT suites).
- **The ticket's own suggested fix ("no Results key → failed") is WRONG as written:** it would flag real clean trivy 0.71 scans. Say so in the PR body; the CONTROL cell proves it.
- Apply per section, strict, at the tip; re-check `ls-remote origin develop` first. Tier: the gate decides — a security-scan job's failure mode (a failed scan read as clean): recommend TIER 1. `Refs KS-1274`. Open PRs touching these four files at hold time: 0 of 22 (Wednesday's GitHub read).
- Input `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1274-trivy-bare-object/input.json`; brief `2_Project_Files/local-model/night/briefs/KS-1274-trivy-bare-object/KS-1274.md`.

```diff
--- a/Blockchain/Testing/jobs/04-container-trivy.sh
+++ b/Blockchain/Testing/jobs/04-container-trivy.sh
@@ -115,5 +115,6 @@
   # KS-1136: a trivy that exited non-zero, or output jq could not read, is a FAILED scan - never a clean image.
-  if [[ $trc -ne 0 || -z $norm ]]; then
+  # KS-1274: so is a report with neither Results nor ArtifactName - a bare `{}` exits 0 with no scan in it.
+  if [[ $trc -ne 0 || -z $norm ]] || ! printf '%s' "$raw" | jq -e 'has("Results") or has("ArtifactName")' >/dev/null 2>&1; then
     norm="$(jq -n --arg img "$img" '{image: $img, error: "scan-failed", counts: {}, vulns: []}')"
   fi
   [ "$first" -eq 1 ] || printf ',\n' >> "$OUT"
--- a/Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh
@@ -12,6 +12,6 @@
 # docker and trivy are NEVER run here (no stack, no daemon): both are STUBS on
 # a private PATH, in the shape of container_trivy_image_filter.test.sh. The
-# trivy stub reads $root/fail.txt ("<image> empty|partial" per line) and fails
-# that image's scan the way the gate measured; every other image gets `{}`.
+# trivy stub reads $root/fail.txt ("<image> empty|partial|bare|nores" per line) and fails
+# that image's scan the way the gate measured (nores: a clean report with no Results); every other image gets a clean `{"Results":[]}`.
 #
 # Usage: bash Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh
@@ -53,8 +53,10 @@
 case "$mode" in
   empty) exit 1 ;;
   partial) printf '{"Results":['; exit 1 ;;
+  bare) echo '{}'; exit 0 ;;
+  nores) echo '{"SchemaVersion":2,"ArtifactName":"dev-auth:latest"}'; exit 0 ;;
 esac
-echo '{}'
+echo '{"Results":[]}'
 STUB
   chmod +x "$root/bin/docker" "$root/bin/trivy"
 }
@@ -88,6 +90,18 @@
 got="$rc $(art "$WORK/partial" '[.images[] | .error // "none"] | sort | join(",")')"
 if [ "$got" = "1 none,scan-failed" ]; then ok "🔴 a partial-output failure on one of two images is recorded as scan-failed, the other stays clean, and the job exits 1"; else bad "🔴 a partial-output failure on one of two images is recorded as scan-failed, the other stays clean, and the job exits 1" "want 1 none,scan-failed, got $got"; fi
-
+
+# RED - KS-1274: the ONLY image's trivy exits 0 with a bare `{}` (no Results, no ArtifactName).
+build_fixture "$WORK/bare" 'dev-auth:latest' 'dev-auth:latest bare'
+rc="$(run_job "$WORK/bare")"
+got="$rc $(art "$WORK/bare" '.images[0].error // "none"')"
+if [ "$got" = "1 scan-failed" ]; then ok "🔴 KS-1274 a trivy that exits 0 with a bare {} is recorded as scan-failed and the job exits 1"; else bad "🔴 KS-1274 a trivy that exits 0 with a bare {} is recorded as scan-failed and the job exits 1" "want 1 scan-failed, got $got"; fi
+
+# CONTROL - KS-1274: trivy 0.71 OMITS Results from a clean report but keeps ArtifactName - that is still a clean scan.
+build_fixture "$WORK/nores" 'dev-auth:latest' 'dev-auth:latest nores'
+rc="$(run_job "$WORK/nores")"
+got="$rc $(art "$WORK/nores" '.images[0].error // "none"')"
+if [ "$got" = "0 none" ]; then ok "CONTROL KS-1274 a clean report with ArtifactName and no Results stays clean: rc 0, no error"; else bad "CONTROL KS-1274 a clean report with ArtifactName and no Results stays clean: rc 0, no error" "want 0 none, got $got"; fi
+
 printf '\n  %d passed, %d failed\n' "$pass" "$fail"
 [ "$fail" -eq 0 ] || exit 1
 exit 0
--- a/Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh
@@ -19,6 +19,6 @@
 # findings image prints a report with 1 CRITICAL + 1 HIGH and, like the real
 # trivy, exits TRIVY_EXIT_CODE when that is set UNLESS --exit-code 0 is on its
 # command line; an empty image exits 1 with no output; every other image gets
-# `{}` and exits 0.
+# a clean `{"Results":[]}` and exits 0.
 #
 # Usage: bash Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh
@@ -65,5 +65,5 @@
   exit "${TRIVY_EXIT_CODE:-${cfg:-0}}"
 fi
-echo '{}'
+echo '{"Results":[]}'
 STUB
   chmod +x "$root/bin/docker" "$root/bin/trivy"
--- a/Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh
@@ -13,4 +13,4 @@
 # a private PATH that RECORD what they were asked. `docker images` prints a
 # fixture list; `trivy image …` appends its last argument (the image) to a
-# file and prints `{}`. Which images were scanned is read from that record —
+# file and prints a clean `{"Results":[]}`. Which images were scanned is read from that record —
 # the one observable the job's own exit code and artefact cannot forge.
@@ -74,5 +74,5 @@
     printf 'for last; do :; done\n'
     printf 'echo "$last" >> "%s/trivy_scanned.txt"\n' "$root"
-    printf "echo '{}'\n"
+    printf "echo '{\"Results\":[]}'\n"
   } > "$root/bin/trivy"
   chmod +x "$root/bin/docker" "$root/bin/trivy"
```
