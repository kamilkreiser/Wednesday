```diff
--- a/Blockchain/Dev/scripts/check-no-latest-tags.sh
+++ b/Blockchain/Dev/scripts/check-no-latest-tags.sh
@@ -28,18 +28,24 @@ ROOT="$(cd "$(dirname "$0")/.." && pwd)"
 cd "$ROOT"
 
 EXIT=0
+SCANNED=0
 
 CHECK_FILES=(
   "docker-compose.production.yml"
   "deployment/azure/services.bicep"
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
@@ -53,7 +59,7 @@ for f in "${CHECK_FILES[@]}"; do
 done
 
 if [ $EXIT -eq 0 ]; then
-  echo "OK — no :latest tags found in production-bound configs."
+  echo "OK — no :latest tags found in production-bound configs ($SCANNED of ${#CHECK_FILES[@]} advertised files examined)."
 fi
 
 exit $EXIT
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_no_latest_tags_inputs.test.sh
@@ -0,0 +1,51 @@
+#!/usr/bin/env bash
+# Unit tests for check-no-latest-tags.sh inputs (KS-865): a listed input that is missing is an ERROR, not a
+# silent skip, and the OK line reports how many of the advertised files were examined.
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
+d=$(make_case case1 docker-compose.production.yml deployment/azure/services.bicep deployment/azure/services.parameters.json deployment/azure/main.parameters.json)
+run_case "$d"
+check "🔴 KS-865 — a listed input that is missing is an error" 1 "does not exist"
+
+d=$(make_case case2 $ALL)
+run_case "$d"
+check "🔴 KS-865 — the OK line reports how many advertised files were examined" 0 "5 of 5 advertised files examined"
+
+d=$(make_case case3 $ALL)
+printf 'image: foo:latest\n' > "$d/docker-compose.production.yml"
+run_case "$d"
+check "KS-865 control — a :latest tag in a listed file is still refused" 1 "::error::"
+
+d=$(make_case case4 $ALL)
+printf '# image: foo:latest\n' > "$d/docker-compose.production.yml"
+run_case "$d"
+check "KS-865 control — a comment-only :latest is ignored" 0 "OK"
+
+echo
+echo "check_no_latest_tags_inputs: $PASS passed, $FAIL failed"
+if [ "$FAIL" -ne 0 ]; then exit 1; fi
+exit 0
```
