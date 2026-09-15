# READY — KS-1127 (`run-shell-suites.sh` tallies an exit-0 `SKIP —` suite as SKIPPED, never passed: two counters, the run loop captures each suite's output and classifies skip/pass/fail, the verdict reads `N passed, M failed, S skipped (of K)` and a `SKIPPED:` line names the suites; policy recorded in the change: a skip keeps rc 0) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on r1 RE-CHECK, BASH_PATCH, tip develop M55 48e65c435 (G6 override verified against origin 0b25f823f), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1127-ornith35b-night (recheck/)
# Source read by me (Wednesday): the applied runner is BYTE-IDENTICAL (`cmp`) to the copy Wednesday fixed by hand and measured on fixture repos before the brief; the model emitted the change as ONE whole-tail rewrite (20 `-` / 29 `+`) whose `+` side is the fix's :220–:247 byte-for-byte — the harness needed two repairs to READ that shape (an EOF clamp on the reanchor's trailing context; A3d narrowed to tip lines the hunk does not also remove), both red-proofed on this output with the old scripts as controls. The model's suite (103 lines after the header RECOUNT 101 -> 103; 8 `check` cells + the skip fixture helper): at the tip rc 1 / 3 FAIL for the predicted reasons (`2 passed, 0 failed (of 2)`, no SKIPPED line, `0 skipped` absent), after 8/8; B6 both sibling suites clean.
# PR NOTES for the Sunday raising seat: (1) TWO files: the runner (:218–:237 region: two counters, the loop body, the verdict + SKIPPED line) + the NEW suite scripts/__tests__/run_shell_suites_skip_tally.test.sh (self-hosting under a globbed ROOT); KS-1127 → Done. (2) Behaviour change to state in the PR body: each suite's stdout+stderr is now CAPTURED and printed after the suite finishes (no longer streamed live) — needed to read the SKIP line; and stderr is merged into stdout. (3) Preflight leg 14 quotes the verdict line — its prefix `shell suites:` is unchanged; KS-1046 (the preflight's own tally) is untouched. (4) The `skip` policy is rc 0 (ruled 2026-09-13 for the ks949 suite); if that changes, it is the `if [ "$skip" -ne 0 ]` block. (5) Apply the REANCHORED section_2 and the RECOUNTED section_1 as held in this READY.

```diff
--- a/Blockchain/Dev/scripts/run-shell-suites.sh
+++ b/Blockchain/Dev/scripts/run-shell-suites.sh
@@ -217,21 +217,31 @@
 
 pass=0
 fail=0
-failed_names=()
-for rel in "${reached[@]}"; do
-  echo ""
-  echo "=== $rel ==="
-  if bash "$REPO_ROOT/$rel"; then
-    pass=$((pass + 1))
-  else
-    fail=$((fail + 1))
-    failed_names+=("$rel")
-  fi
-done
-
-echo ""
-echo "shell suites: $pass passed, $fail failed (of ${#reached[@]})"
-if [ "$fail" -ne 0 ]; then
-  printf 'FAILED: %s\n' "${failed_names[@]}"
-  exit 1
-fi
+failed_names=()
+skip=0
+skipped_names=()
+for rel in "${reached[@]}"; do
+  echo ""
+  echo "=== $rel ==="
+  if out=$(bash "$REPO_ROOT/$rel" 2>&1); then rc=0; else rc=$?; fi
+  printf '%s\n' "$out"
+  if [ "$rc" -eq 0 ] && grep -qE '^[[:space:]]*SKIP —' <<< "$out"; then
+    skip=$((skip + 1))
+    skipped_names+=("$rel")
+  elif [ "$rc" -eq 0 ]; then
+    pass=$((pass + 1))
+  else
+    fail=$((fail + 1))
+    failed_names+=("$rel")
+  fi
+done
+
+echo ""
+echo "shell suites: $pass passed, $fail failed, $skip skipped (of ${#reached[@]})"
+if [ "$skip" -ne 0 ]; then
+  printf 'SKIPPED: %s\n' "${skipped_names[@]}"
+fi
+if [ "$fail" -ne 0 ]; then
+  printf 'FAILED: %s\n' "${failed_names[@]}"
+  exit 1
+fi
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/run_shell_suites_skip_tally.test.sh
@@ -0,0 +1,103 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for run-shell-suites.sh — the SKIP tally (KS-1127)
+# A suite that exits 0 with a `SKIP —` line is tallied as skipped, not passed;
+# the verdict carries the ratio.
+# =============================================================================
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+RUNNER="${RUNNER_SH:-$HERE/../run-shell-suites.sh}"
+if [[ ! -f "$RUNNER" ]]; then
+  echo "FATAL: run-shell-suites.sh not found at $RUNNER" >&2
+  exit 2
+fi
+
+# The globbed roots, read FROM THE SCRIPT rather than retyped.
+ROOTS=()
+while IFS= read -r _root; do
+  [ -n "$_root" ] && ROOTS+=("$_root")
+done < <(sed -n '/^ROOTS=(/,/^)/p' "$RUNNER" | grep -oE '"[^"]+"' | tr -d '"')
+if [[ "${#ROOTS[@]}" -eq 0 ]]; then
+  echo "FATAL: could not read ROOTS out of $RUNNER" >&2
+  exit 2
+fi
+PRIMARY_ROOT="${ROOTS[0]}"
+SECOND_ROOT="${ROOTS[1]:-$PRIMARY_ROOT}"
+
+TMP="$(mktemp -d)"
+trap 'rm -rf "$TMP"' EXIT
+PASS=0
+FAIL=0
+
+check() {   # $1 = label, $2 = expected, $3 = actual
+  if [[ "$2" == "$3" ]]; then
+    echo "  ok   $1 (=$3)"; PASS=$((PASS + 1))
+  else
+    echo "  FAIL $1 — expected $2, got $3"; FAIL=$((FAIL + 1))
+  fi
+}
+
+new_repo() {   # -> path
+  local r; r="$(mktemp -d "$TMP/repo.XXXXXX")"
+  mkdir -p "$r/$(dirname "$PRIMARY_ROOT")" "$r/$PRIMARY_ROOT" "$r/$SECOND_ROOT"
+  mkdir -p "$r/Blockchain/Dev/scripts"
+  cp "$RUNNER" "$r/Blockchain/Dev/scripts/run-shell-suites.sh"
+  git -C "$r" init -q
+  git -C "$r" config user.email "test@secuura.local"
+  git -C "$r" config user.name  "KS-731 fixture"
+  printf '#!/usr/bin/env bash\nexit 0\n' > "$r/.keep-marker"
+  git -C "$r" add -A >/dev/null 2>&1
+  git -C "$r" commit -qm init >/dev/null 2>&1
+  printf '%s' "$r"
+}
+
+suite_at() {   # $1 = repo, $2 = path relative to repo, $3 = exit code the suite returns
+  mkdir -p "$1/$(dirname "$2")"
+  printf '#!/usr/bin/env bash\necho "fixture suite %s"\nexit %s\n' "$2" "$3" > "$1/$2"
+}
+
+commit_all() { git -C "$1" add -A >/dev/null 2>&1; git -C "$1" commit -qm t >/dev/null 2>&1; }
+
+run_runner() {   # $1 = repo, $2... = args -> "<rc>"
+  local r="$1"; shift
+  ( cd "$r/Blockchain/Dev" && bash scripts/run-shell-suites.sh "$@" >/dev/null 2>&1 )
+  printf '%s' "$?"
+}
+
+runner_out() {   # $1 = repo, $2... = args -> stdout+stderr
+  local r="$1"; shift
+  ( cd "$r/Blockchain/Dev" && bash scripts/run-shell-suites.sh "$@" 2>&1 )
+}
+
+skip_suite_at() {   # $1 = repo, $2 = path relative to repo — a suite that cannot run its cells and says so, exit 0
+  mkdir -p "$1/$(dirname "$2")"
+  printf '#!/usr/bin/env bash\necho "SKIP — no PostgreSQL binaries found; 0/26 cells run"\nexit 0\n' > "$1/$2"
+}
+
+echo "run_shell_suites_skip_tally: KS-1127"
+
+# --- a SKIP beside a green suite is tallied as skipped, never as passed --------
+R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/green.test.sh" 0; skip_suite_at "$R" "$PRIMARY_ROOT/skipper.test.sh"; commit_all "$R"
+check 'green + SKIP: the verdict reads 1 passed, 0 failed, 1 skipped (of 2)' 1 \
+  "$(runner_out "$R" | grep -c '^shell suites: 1 passed, 0 failed, 1 skipped (of 2)')"
+check 'green + SKIP: the skipped suite is NAMED on a SKIPPED: line' 1 \
+  "$(runner_out "$R" | grep -c 'SKIPPED: .*skipper.test.sh')"
+check 'CONTROL: a skip does not fail the run (policy: rc 0)' 0 "$(run_runner "$R")"
+check 'CONTROL: the SKIP suite output is still streamed' 1 \
+  "$(runner_out "$R" | grep -c 'SKIP — no PostgreSQL binaries')"
+
+# --- no skip: the tally says 0 skipped and nothing is named --------------------
+R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/green.test.sh" 0; commit_all "$R"
+check 'green only: the verdict reads 1 passed, 0 failed, 0 skipped (of 1)' 1 \
+  "$(runner_out "$R" | grep -c '^shell suites: 1 passed, 0 failed, 0 skipped (of 1)')"
+check 'CONTROL: green only, no SKIPPED: line' 0 "$(runner_out "$R" | grep -c '^SKIPPED:')"
+
+# --- a RED suite still fails the run and is named (unchanged behaviour) --------
+R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/green.test.sh" 0; suite_at "$R" "$PRIMARY_ROOT/red.test.sh" 1; commit_all "$R"
+check 'CONTROL: a red suite still propagates rc 1' 1 "$(run_runner "$R")"
+check 'CONTROL: and is still named on the FAILED: line' 1 \
+  "$(runner_out "$R" | grep -c 'FAILED: .*red.test.sh')"
+
+echo "run_shell_suites_skip_tally: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 ]]
```
