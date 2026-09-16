# READY — KS-1033 ITEM 1 ONLY (`Blockchain/Dev/scripts/check-no-demo-mutation.sh` :58 — the guard's fallback base `origin/main` → `origin/develop`, so the three-dot diff at :69 resolves to the branch point instead of dragging in the whole develop-vs-main delta; the DEFERRED reason in run-code-guards.sh:116 names exactly this remedy)
# Source read by me (Wednesday, 20:13): `diff` of the applied `after.sh` against `git show 48e65c435:…/check-no-demo-mutation.sh` = EXACTLY two changes — :50 comment (one line → five, KS-1033 named) and :58 `BASE="origin/main"` → `BASE="origin/develop"`; nothing else moved. Checker PASS 7/7 FIRST SAMPLE (20:10, q4): B3b every brief `+` line in the hunk; B4 RED at the tip rc 1 / 2 FAIL (the two develop-based-branch cells) / 3 pass (both CONTROLS + completeness); B5 GREEN rc 0 / 5 pass; B6 no sibling suite drives this guard (stated by the checker). Test read: `mktemp -d` work dir with an EXIT trap, a LOCAL bare remote only, 4 cells + the EXPECTED_CELLS=4 completeness arm. Accommodations named by the checker: section 1 `--recount --ignore-whitespace`; section 2 new-file header RECOUNTED 104 → 126 (the declared count would have dropped the tail) — the diff below is the recounted one.
# PR NOTES for the Sunday raising seat: (1) TWO files: the guard (ONE hunk pair) + the NEW suite `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh`. (2) THIS CLOSES KS-1033 ITEM 1 ONLY — item 2 (`check-no-trust-header-reads.sh`, decision-class by the ticket's own words) and item 3 (`check-container-isolation.sh`, a relocation) stay open; the ticket must NOT be closed on this PR. (3) The DEFERRED reason string at `run-code-guards.sh:116` ("defaults to BASE=origin/main (line 58)") goes STALE with this change and is deliberately NOT edited here (live bash inside an array; editing it is one step from wiring the guard) — the PR description says so, and the follow-up is "wire the guard or rewrite its DEFERRED reason", a separate call. (4) `:98`'s two-dot `git log "$BASE..$HEAD"` override-token scan is untouched (an asymmetry with :69's three dots, not KS-1033's).

```diff
--- a/Blockchain/Dev/scripts/check-no-demo-mutation.sh
+++ b/Blockchain/Dev/scripts/check-no-demo-mutation.sh
@@ -47,7 +47,11 @@ DEMO_PREFIXES=(
 
 # Determine the diff range. In CI this is the PR base..head; locally
-# default to comparing against origin/main.
+# default to comparing against origin/develop (KS-1033). The three-dot diff
+# below takes the merge-base, and under Git Flow develop is permanently ahead
+# of main, so an origin/main base shows the whole develop-vs-main delta as
+# this branch's own change - measured: 4 demo files on a branch that touched
+# nothing.
 if [ -n "${GITHUB_BASE_REF:-}" ]; then
   BASE="origin/${GITHUB_BASE_REF}"
   HEAD="HEAD"
@@ -55,7 +59,7 @@ elif [ -n "${1:-}" ]; then
   BASE="$1"
   HEAD="${2:-HEAD}"
 else
-  BASE="origin/main"
+  BASE="origin/develop"
   HEAD="HEAD"
 fi
 
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh
@@ -0,0 +1,126 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-no-demo-mutation.sh - the DEFAULT diff
+# base must be origin/develop, not origin/main (KS-1033 item 1)
+# =============================================================================
+# Under Git Flow develop is permanently ahead of main, so an origin/main base
+# shows the whole develop-vs-main delta as this branch's own change. Every
+# fixture is a throwaway repo under mktemp -d pushing to a LOCAL BARE REMOTE.
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${DEMO_GUARD_SH:-$HERE/../check-no-demo-mutation.sh}"
+[ -r "$SUBJ" ] || { echo "FATAL: check-no-demo-mutation.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1033.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+EXPECTED_CELLS=4
+DEMO_FILE="Blockchain/Dev/deployment/azure/migrate/init.sql"
+PLAIN_FILE="Blockchain/Dev/README.md"
+
+build() {
+  rm -rf "$1"
+  mkdir -p "$1"
+  (
+    export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
+    git init -q --bare -b main "$1/origin.git"
+    git init -q -b main "$1/seed"
+    cd "$1/seed" || exit 9
+    git config user.email t@t.t
+    git config user.name t
+    mkdir -p Blockchain/Dev/deployment/azure/migrate
+    echo base > "$PLAIN_FILE"
+    echo base > "$DEMO_FILE"
+    git add -A
+    git commit -qm init
+    git checkout -q -b develop
+    echo "develop moved ahead" > "$DEMO_FILE"
+    git add -A
+    git commit -qm "develop touches a demo path"
+    git remote add origin "$1/origin.git"
+    git push -q origin main develop
+    cd "$1" || exit 9
+    git clone -q "$1/origin.git" work
+    cd "$1/work" || exit 9
+    git config user.email t@t.t
+    git config user.name t
+    git checkout -q -b feature origin/develop
+    if [ "$2" = demo ]; then
+      echo "feature touches a demo path too" > "$DEMO_FILE"
+    else
+      echo "an ordinary change" > "$PLAIN_FILE"
+    fi
+    git add -A
+    git commit -qm "feature work"
+  ) > "$1/build.log" 2>&1
+}
+
+run_guard() {
+  (
+    unset GITHUB_BASE_REF
+    if [ -n "$2" ]; then export GITHUB_BASE_REF="$2"; fi
+    cd "$1/work" || exit 9
+    bash "$SUBJ"
+  ) > "$1/out.txt" 2>&1
+  echo $?
+}
+
+build "$WORK/plain" plain
+RC_PLAIN="$(run_guard "$WORK/plain" "")"
+OUT_PLAIN="$WORK/plain/out.txt"
+build "$WORK/demo" demo
+RC_DEMO="$(run_guard "$WORK/demo" "")"
+OUT_DEMO="$WORK/demo/out.txt"
+build "$WORK/ciref" plain
+RC_CIREF="$(run_guard "$WORK/ciref" develop)"
+OUT_CIREF="$WORK/ciref/out.txt"
+
+# CELL 1 (RED at the tip) - a develop-based branch that touched no demo path
+# must be allowed. At the tip the origin/main base drags develop's own demo
+# commit into the diff and the guard exits 1.
+if [ "$RC_PLAIN" = "0" ]; then
+  echo "PASS: a develop-based branch touching no demo path exits 0"; PASS=$((PASS+1))
+else
+  echo "FAIL: a develop-based branch touching no demo path exited $RC_PLAIN, not 0 - the base dragged in develop's own commits ($(grep -c 'migrate/init.sql' "$OUT_PLAIN") demo path line(s) reported)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip) - and it must say so, not print the block banner.
+if grep -qF 'no demo-shaping paths touched' "$OUT_PLAIN" && ! grep -qF 'DEMO MUTATION DETECTED' "$OUT_PLAIN"; then
+  echo "PASS: the guard reports no demo-shaping paths touched and prints no block banner"; PASS=$((PASS+1))
+else
+  echo "FAIL: clean-message present=$(grep -qF 'no demo-shaping paths touched' "$OUT_PLAIN" && echo yes || echo NO), block banner present=$(grep -qF 'DEMO MUTATION DETECTED' "$OUT_PLAIN" && echo YES || echo no)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - the guard still refuses a REAL demo
+# change on the branch itself. This is what stops a fix that just always passes.
+if [ "$RC_DEMO" = "1" ] && grep -qF 'DEMO MUTATION DETECTED' "$OUT_DEMO"; then
+  echo "PASS: CONTROL a branch that really touches a demo path is still blocked with exit 1"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL a real demo change exited $RC_DEMO (want 1), banner present=$(grep -qF 'DEMO MUTATION DETECTED' "$OUT_DEMO" && echo yes || echo NO)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - GITHUB_BASE_REF still wins over the
+# default, so the branch named there is what the diff is taken against.
+if [ "$RC_CIREF" = "0" ] && grep -qF 'no demo-shaping paths touched' "$OUT_CIREF"; then
+  echo "PASS: CONTROL GITHUB_BASE_REF=develop is still honoured ahead of the default"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL GITHUB_BASE_REF=develop exited $RC_CIREF (want 0): $(head -1 "$OUT_CIREF")"; FAIL=$((FAIL+1))
+fi
+
+# CELL 5 - the completeness guard. A suite that exits 0 having asserted nothing
+# is a check that cannot fail, so a short count is itself a FAIL.
+if [ $((PASS + FAIL)) -eq "$EXPECTED_CELLS" ]; then
+  echo "PASS: all $EXPECTED_CELLS cells ran"; PASS=$((PASS+1))
+else
+  echo "FAIL: only $((PASS + FAIL)) of $EXPECTED_CELLS cells ran - a suite that asserts nothing is not a pass"; FAIL=$((FAIL+1))
+fi
+
+echo ""
+echo "check_no_demo_mutation_base: $PASS passed, $FAIL failed"
+[ $FAIL -eq 0 ]
```
