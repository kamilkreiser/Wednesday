# READY — KS-865 (check-no-latest-tags.sh: a listed input that is missing is an ERROR, the dead .github/workflows/deploy-staging.yml entry dropped with a comment, the OK line reports N of M advertised files examined) — Ornith ornith:35b (Q4_K_M) r1 PASS 7/7 on RE-CHECK under bash_patch B2 REANCHORED (the run's own verdict was FAIL B2: four `@@ -N,1 +N,1 @@` micro-hunks, line numbers off by three — every -/+ line byte-exact; reanchor.py rebuilt them at 31/38/42/56), THE FIRST BASH_PATCH TICKET, tip develop M55 48e65c435 (G6 override verified against origin 0b25f823f), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks865-ornith35b-night (recheck in /recheck)
# Source read by me (Wednesday): the APPLIED SCRIPT (recheck/out.md.checker/after.sh) is BYTE-IDENTICAL to the golden diff Wednesday wrote by hand for the checker's arms (tests/fixtures/bash_patch_golden_ks865_out.md) — E1 SCANNED=0 after :30, E2 the dead entry → the KS-865 comment at :38, E3 the six-line refuse+count block at :42, E4 the count on the OK line at :56. The model's test carries the brief's four cells with the helpers verbatim (case names its own; one extra echo header line — harmless). B4 at the tip: both 🔴 cells red for the predicted reason (the missing file → exit 0 not 1; the OK line carries no count), both controls green; B5 after: 4/4; B5a bash -n clean; B6: no sibling suite names the script (stated); B7 shellcheck not installed here.
# PR NOTES for the Sunday raising seat: (1) TWO files: the script (four edits, two hunks once applied) + the NEW suite `scripts/__tests__/check_no_latest_tags_inputs.test.sh` — run-shell-suites.sh globs scripts/__tests__/*.test.sh, so it is reached (verify with `--list`). (2) The CHECK_FILES change REMOVES a listed input (.github/workflows/deploy-staging.yml — exists nowhere at the tip; retired per KS-1162): state it in the PR body as the ticket's 'or the path is corrected' branch resolved by measurement (the file is gone, not moved) — a reviewer may prefer to keep a pointer; the comment line names why. (3) The caller run-code-guards.sh:82 is unchanged; with the fix the guard now FAILS if any of the five listed files is absent in a checkout — the five exist at the tip (ls-tree). (4) shellcheck was not available in the checker; run it in the PR's tool-mode clone if the repo's preflight has it. (5) Apply the REANCHORED section_1 below (the as-written micro-hunks are kept beside it in the run dir as section_1.diff.as-written).

```diff
--- a/Blockchain/Dev/scripts/check-no-latest-tags.sh
+++ b/Blockchain/Dev/scripts/check-no-latest-tags.sh
@@ -28,6 +28,7 @@
 cd "$ROOT"
 
 EXIT=0
+SCANNED=0
 
 CHECK_FILES=(
   "docker-compose.production.yml"
@@ -35,11 +36,16 @@
   "deployment/azure/services.parameters.json"
   "deployment/azure/main.bicep"
   "deployment/azure/main.parameters.json"
-  ".github/workflows/deploy-staging.yml"
+  # KS-865: .github/workflows/deploy-staging.yml was listed here but exists nowhere at the tip (the workflow is retired); a missing listed input is now an ERROR below, so a dead entry cannot ride along.
 )
 
 for f in "${CHECK_FILES[@]}"; do
-  [ -f "$f" ] || continue
+  if [ ! -f "$f" ]; then
+    echo "::error::$f is listed in CHECK_FILES but does not exist under $ROOT (KS-865: a missing input is an error, not a skip)"
+    EXIT=1
+    continue
+  fi
+  SCANNED=$((SCANNED+1))
   # Match `image: …:latest` or `imageTag: latest` or `:latest"` in JSON.
   # Skip comment-only lines: `#` for yaml/sh, `//` for bicep.
   hits=$(grep -nE '(:latest\b|imageTag[^"]*"latest")' "$f" \
@@ -53,7 +59,7 @@
 done
 
 if [ $EXIT -eq 0 ]; then
-  echo "OK — no :latest tags found in production-bound configs."
+  echo "OK — no :latest tags found in production-bound configs ($SCANNED of ${#CHECK_FILES[@]} advertised files examined)."
 fi
 
 exit $EXIT
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_no_latest_tags_inputs.test.sh
@@ -0,0 +1,65 @@
+#!/usr/bin/env bash
+# Unit tests for check-no-latest-tags.sh (KS-865).
+# Every case builds a throwaway tree; the gate resolves ROOT from its own location.
+
+set -uo pipefail
+GATE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/check-no-latest-tags.sh"
+PASS=0; FAIL=0
+TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
+
+# make_case <name> <files to create, space-separated, relative to the case root> — copies the gate into <case>/scripts/
+# and creates each listed file (empty). Prints the case root.
+make_case() {
+  local name="$1"; shift; local d="$TMP/$name"
+  mkdir -p "$d/scripts" && cp "$GATE" "$d/scripts/check-no-latest-tags.sh" && chmod +x "$d/scripts/check-no-latest-tags.sh"
+  local f; for f in "$@"; do mkdir -p "$d/$(dirname "$f")" && : > "$d/$f"; done
+  echo "$d"
+}
+# run_case <case root> — runs the copied gate; sets OUT and RC.
+run_case() { OUT=$(bash "$1/scripts/check-no-latest-tags.sh" 2>&1); RC=$?; }
+# check <name> <want_rc> <want_substring> — one cell: exit code AND a substring of the output.
+check() {
+  local name="$1" want="$2" sub="$3"
+  if [ "$RC" -ne "$want" ]; then FAIL=$((FAIL+1)); echo "  FAIL: $name (expected exit $want, got $RC)"; return; fi
+  case "$OUT" in *"$sub"*) PASS=$((PASS+1)); echo "  PASS: $name" ;; *) FAIL=$((FAIL+1)); echo "  FAIL: $name (exit ok, output lacks '$sub')" ;; esac
+}
+ALL="docker-compose.production.yml deployment/azure/services.bicep deployment/azure/services.parameters.json deployment/azure/main.bicep deployment/azure/main.parameters.json"
+
+echo "check_no_latest_tags_inputs:"
+
+d=$(make_case case_missing_one docker-compose.production.yml deployment/azure/services.bicep deployment/azure/services.parameters.json deployment/azure/main.parameters.json)
+run_case "$d"
+check "🔴 KS-865 — a listed input that is missing is an error" 1 "does not exist"
+
+d=$(make_case case_all_five docker-compose.production.yml deployment/azure/services.bicep deployment/azure/services.parameters.json deployment/azure/main.bicep deployment/azure/main.parameters.json)
+run_case "$d"
+check "🔴 KS-865 — the OK line reports how many advertised files were examined" 0 "5 of 5 advertised files examined"
+
+d=$(make_case case_has_latest docker-compose.production.yml deployment/azure/services.bicep deployment/azure/services.parameters.json deployment/azure/main.bicep deployment/azure/main.parameters.json)
+printf 'image: foo:latest\n' > "$d/docker-compose.production.yml"
+run_case "$d"
+check "KS-865 control — a :latest tag in a listed file is still refused" 1 "::error::"
+
+d=$(make_case case_comment_only docker-compose.production.yml deployment/azure/services.bicep deployment/azure/services.parameters.json deployment/azure/main.bicep deployment/azure/main.parameters.json)
+printf '# image: foo:latest\n' > "$d/docker-compose.production.yml"
+run_case "$d"
+check "KS-865 control — a comment-only :latest is ignored" 0 "OK"
+
+echo "check_no_latest_tags_inputs: $PASS passed, $FAIL failed"
+[[ $FAIL -eq 0 ]]
```
