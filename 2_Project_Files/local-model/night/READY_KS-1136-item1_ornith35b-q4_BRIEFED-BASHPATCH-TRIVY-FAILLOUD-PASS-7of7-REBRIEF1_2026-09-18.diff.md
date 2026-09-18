# READY — KS-1136 item 1 (Ornith, briefed, bash_patch) — PASS 7/7 on REBRIEF 1 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1136-ornith35b-night2/out.md.checker/section_N.diff`, each applied with its `section_N.opts`.**

**Held 2026-09-18 16:41 by the 14:4x Wednesday seat after a source read (46 min late: the PASS landed 15:55 while the seat launched the batch gate).** Tip `8b9c3f022`. Product `Blockchain/Testing/jobs/04-container-trivy.sh`. r1 + its retry FAILED B3b on a quote-escape dialect; rebrief 1 wrote the if-line quote-free.

## Source read
- :93 no longer turns a failed trivy into `{}`: trivy's own rc is kept (`trc`), a failed/unreadable scan is written `error: "scan-failed"` (counts {} / vulns [] kept so the artefact stays parseable), and the job exits 1 BEFORE the clean `across N image(s)` line.
- The 12 '+' lines are IDENTICAL to the brief; the 2 '-' lines are the `|| echo '{}'` line and the blank :94 the brief names. 0 escaped quotes. B4 red at tip (2 FAIL / 1 pass), B6 sibling suite no new failure.
- **Behaviour change: job 04 now exits 1 on any failed scan.** Item 2 (`09-aggregate-report.sh` reading `.error`, 7 sites) is NOT here → a Claude seat. **Refs KS-1136, NOT Closes.** Tier 2.
**HELD. Not raised.**

---
## The model's output, verbatim

```diff
--- a/Blockchain/Testing/jobs/04-container-trivy.sh
+++ b/Blockchain/Testing/jobs/04-container-trivy.sh
@@ -91,6 +91,6 @@
     --vuln-type os,library \
     --skip-db-update \
-    "$img" 2>/dev/null || echo '{}')"
-
+    "$img" 2>/dev/null)"; trc=$?
+  # KS-1136: trc is trivy's own exit code - a failed scan is no longer turned into an empty, clean-looking report.
   # extract just the high-signal subset
   norm=$(echo "$raw" | jq --arg img "$img" '{
@@ -114,3 +114,7 @@
+  # KS-1136: a trivy that exited non-zero, or output jq could not read, is a FAILED scan - never a clean image.
+  if [[ $trc -ne 0 || -z $norm ]]; then
+    norm="$(jq -n --arg img "$img" '{image: $img, error: "scan-failed", counts: {}, vulns: []}')"
+  fi
   [ "$first" -eq 1 ] || printf ',\n' >> "$OUT"
   first=0
   echo "$norm" >> "$OUT"
@@ -121,2 +125,8 @@
+# KS-1136: a run with a failed scan exits 1 and never prints the clean-run "across N image(s)" summary.
+failed=$(jq '[.images[] | select(.error)] | length' "$OUT")
+if [ "$failed" -gt 0 ]; then
+  echo "  -> FAILED: trivy could not scan $failed of ${#IMAGES[@]} image(s) - a failed scan is not a clean image"
+  exit 1
+fi
 crit=$(jq '[.images[].counts.CRITICAL // 0] | add' "$OUT")
 high=$(jq '[.images[].counts.HIGH // 0] | add' "$OUT")
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh
@@ -0,0 +1,93 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Testing/jobs/04-container-trivy.sh - a FAILED per-image
+# scan must never read as a CLEAN image (KS-1136 item 1, R-2)
+# =============================================================================
+# The defect: each image's scan was `raw="$(trivy image ... || echo '{}')"`, so a
+# trivy that exited non-zero with no output became `{}`, and the jq that follows
+# wrote `counts: {}` / `vulns: []` for that image - scanned and clean - with the
+# job exiting 0. With partial output on one of two images, the artefact itself
+# came out unparseable, still rc 0.
+#
+# docker and trivy are NEVER run here (no stack, no daemon): both are STUBS on
+# a private PATH, in the shape of container_trivy_image_filter.test.sh. The
+# trivy stub reads $root/fail.txt ("<image> empty|partial" per line) and fails
+# that image's scan the way the gate measured; every other image gets `{}`.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh
+# =============================================================================
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+JOB="$REPO_ROOT/Blockchain/Testing/jobs/04-container-trivy.sh"
+[ -f "$JOB" ] || { echo "FATAL: 04-container-trivy.sh not found at $JOB" >&2; exit 2; }
+command -v jq >/dev/null 2>&1 || { echo "FATAL: jq is not on PATH - the subject cannot run, so nothing here can be graded" >&2; exit 2; }
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1136.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+# Build a fixture around the job under test.
+#   $1 = dir   $2 = corpus text (what `docker images` prints)   $3 = fail list ("<image> empty|partial" lines)
+build_fixture() {
+  local root="$1" corpus="$2" fails="${3:-}"
+  rm -rf "$root"; mkdir -p "$root/Testing/jobs" "$root/bin" "$root/run"
+  cp "$JOB" "$root/Testing/jobs/04-container-trivy.sh"
+  printf '%s\n' "$corpus" > "$root/images.txt"
+  printf '%s\n' "$fails" > "$root/fail.txt"
+  { printf '#!/bin/bash\n'
+    printf 'case "${1:-}" in\n'
+    printf '  info) exit 0 ;;\n'
+    printf '  images) cat "%s/images.txt" ;;\n' "$root"
+    printf 'esac\nexit 0\n'
+  } > "$root/bin/docker"
+  sed "s#@ROOT@#$root#g" > "$root/bin/trivy" <<'STUB'
+#!/bin/bash
+for last; do :; done
+echo "$last" >> "@ROOT@/trivy_scanned.txt"
+mode="$(awk -v i="$last" '$1 == i { print $2 }' "@ROOT@/fail.txt")"
+case "$mode" in
+  empty) exit 1 ;;
+  partial) printf '{"Results":['; exit 1 ;;
+esac
+echo '{}'
+STUB
+  chmod +x "$root/bin/docker" "$root/bin/trivy"
+}
+
+# Run the job the way the orchestrator / audit runner do. Prints rc.
+run_job() {
+  local root="$1"
+  ( export PATH="$root/bin:/usr/bin:/bin" SELF="$root/Testing" RUN_DIR="$root/run"
+    cd "$SELF" && bash jobs/04-container-trivy.sh ) >"$root/out.txt" 2>&1
+  echo $?
+}
+art() { jq -r "$2" "$1/run/04-container-trivy.json" 2>/dev/null || echo unparseable; }
+
+# CONTROL - every scan succeeds: rc 0, two images, no image carries an error.
+build_fixture "$WORK/clean" 'dev-auth:latest
+dev-api-gateway:latest'
+rc="$(run_job "$WORK/clean")"
+got="$rc $(art "$WORK/clean" '.images | length') $(art "$WORK/clean" '[.images[] | select(.error)] | length')"
+if [ "$got" = "0 2 0" ]; then ok "CONTROL - two clean scans: rc 0, 2 images, 0 errors"; else bad "CONTROL - two clean scans: rc 0, 2 images, 0 errors" "want 0 2 0, got $got"; fi
+
+# RED - the ONLY image's trivy exits 1 with NO output.
+build_fixture "$WORK/empty" 'dev-auth:latest' 'dev-auth:latest empty'
+rc="$(run_job "$WORK/empty")"
+got="$rc $(art "$WORK/empty" '.images[0].error // "none"')"
+if [ "$got" = "1 scan-failed" ]; then ok "🔴 a trivy that exits 1 with no output is recorded as scan-failed and the job exits 1"; else bad "🔴 a trivy that exits 1 with no output is recorded as scan-failed and the job exits 1" "want 1 scan-failed, got $got"; fi
+
+# RED - one of two images fails with PARTIAL output; the other scans clean.
+build_fixture "$WORK/partial" 'dev-auth:latest
+dev-api-gateway:latest' 'dev-auth:latest partial'
+rc="$(run_job "$WORK/partial")"
+got="$rc $(art "$WORK/partial" '[.images[] | .error // "none"] | sort | join(",")')"
+if [ "$got" = "1 none,scan-failed" ]; then ok "🔴 a partial-output failure on one of two images is recorded as scan-failed, the other stays clean, and the job exits 1"; else bad "🔴 a partial-output failure on one of two images is recorded as scan-failed, the other stays clean, and the job exits 1" "want 1 none,scan-failed, got $got"; fi
+
+printf '\n  %d passed, %d failed\n' "$pass" "$fail"
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
