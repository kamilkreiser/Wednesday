# READY — KS-1089 (`run-shell-suites.sh` polish, both items: QA-8 `--list` on a tree with no suites no longer dies on bash 3.2 (`:72` uses the `${reached[@]+"${reached[@]}"}` form `:92` already uses); QA-7 the git-list refusal prints a headline PER CAUSE — `could not ask git…` when git printed nothing, `git listed its repository-local variables, but GIT_DIR is not among them` when it printed a list without GIT_DIR — the parenthetical the reference suite pins is untouched) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on r1 RE-CHECK, BASH_PATCH, tip develop M55 48e65c435 (G6 override verified against origin 0b25f823f), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1089-ornith35b-night (recheck/)
# Source read by me (Wednesday): the applied runner is BYTE-IDENTICAL (`cmp`) to the copy Wednesday fixed by hand before the brief was written (E1 at :72; the two `git_env_headline=` assignments inside their own if/else branches; :202 `echo "$git_env_headline"`); the model's product hunks were the brief's lines byte-for-byte — the r1 FAIL was Wednesday's brief (a block-replacement `+` side that repeated context lines; rewritten to the minimal shape) and then the HARNESS (the reanchor collapsed the two `+` lines onto the `-` line's position → fixed as SPLIT-GROUPS + the dropped-marker context repair, both red-proofed on this very output). The model's suite (100 lines, 7 `check` cells: two QA-8 reds, two QA-7 reds, three controls): at the tip rc 1 / 4 FAIL for the predicted reasons, after 7/7; B6 both sibling suites (the 396-line reference, whose two pins on `could not ask git which variables` and `GIT_DIR absent` still hold) clean. Accommodations named: section_1 REANCHORED (the model's headers off by three); section_2 header RECOUNTED 95 -> 100.
# PR NOTES for the Sunday raising seat: (1) TWO files: the runner (:72 + :197–:202) + the NEW suite scripts/__tests__/run_shell_suites_polish.test.sh (self-hosting: it sits under a globbed ROOT, so the runner runs it — verify with --list); KS-1089 → Done, both checklist items ticked. (2) `--list` on an empty tree now prints ONE blank line and exits 0 (the `printf '%s\n'` with no args — identical to `:92`'s behaviour); say so in the PR body. (3) Do not touch :203–:206.

```diff
--- a/Blockchain/Dev/scripts/run-shell-suites.sh
+++ b/Blockchain/Dev/scripts/run-shell-suites.sh
@@ -69,7 +69,7 @@
 done
 
 if [ "$MODE" = "list" ]; then
-  printf '%s\n' "${reached[@]}"
+  printf '%s\n' ${reached[@]+"${reached[@]}"}
   exit 0
 fi
 
@@ -193,18 +193,20 @@
   if [ "$v" = "GIT_DIR" ]; then git_env_has_dir=1; fi
 done
 git_env_total=${#git_env_names[@]}
 if [ "$git_env_total" -eq 0 ] || [ "$git_env_has_dir" -ne 1 ]; then
   if [ -z "$git_local_env" ]; then
     git_env_state="printed nothing"
+    git_env_headline="FAIL — could not ask git which variables are repository-local"
   else
     git_env_state="printed a list with $git_env_total usable name(s), GIT_DIR absent"
+    git_env_headline="FAIL — git listed its repository-local variables, but GIT_DIR is not among them"
   fi
-  echo "FAIL — could not ask git which variables are repository-local"
+  echo "$git_env_headline"
   echo "       (git rev-parse --local-env-vars $git_env_state). Refusing to run the"
   echo "       suites: an inherited GIT_DIR would aim every fixture's git calls at"
   echo "       the caller's repository (KS-1086)."
   exit 1
 fi
 git_env_cleared=""
 for v in "${git_env_names[@]}"; do
   if printenv "$v" >/dev/null 2>&1; then
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/run_shell_suites_polish.test.sh
@@ -0,0 +1,100 @@
+#!/usr/bin/env bash
+# KS-1089 QA-8: `--list` on an empty tree; QA-7: headline per cause.
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+RUNNER="${RUNNER_SH:-$HERE/../run-shell-suites.sh}"
+if [[ ! -f "$RUNNER" ]]; then
+  echo "FATAL: run-shell-suites.sh not found at $RUNNER" >&2
+  exit 2
+fi
+
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
+echo "run_shell_suites_polish: KS-1089"
+
+# --- QA-8: --list on a tree with ZERO reached suites --------------------------
+R="$(new_repo)"
+check 'QA-8: --list on an empty tree exits 0 (bash 3.2, set -u)' 0 \
+  "$(run_runner "$R" --list)"
+check 'QA-8: --list on an empty tree raises no unbound-variable error' 0 \
+  "$(runner_out "$R" --list | grep -c 'unbound variable')"
+R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/one.test.sh" 0; commit_all "$R"
+check 'CONTROL: --list with one suite still prints it' 1 \
+  "$(runner_out "$R" --list | grep -c "$PRIMARY_ROOT/one.test.sh")"
+
+# --- QA-7: the git-list refusal has a headline PER CAUSE -----------------------
+K_REALGIT="$(command -v git)"
+K_NODIRBIN="$(mktemp -d "$TMP/nodirbin.XXXXXX")"
+printf '#!/usr/bin/env bash\nif [ "${1:-}" = rev-parse ] && [ "${2:-}" = --local-env-vars ]; then "%s" rev-parse --local-env-vars | grep -vx GIT_DIR; exit 0; fi\nexec "%s" "$@"\n' "$K_REALGIT" "$K_REALGIT" > "$K_NODIRBIN/git"
+chmod +x "$K_NODIRBIN/git"
+R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/one.test.sh" 0; commit_all "$R"
+K_NODIR="$( cd "$R/Blockchain/Dev" && PATH="$K_NODIRBIN:$PATH" bash scripts/run-shell-suites.sh 2>&1 )"
+check 'QA-7: a list WITHOUT GIT_DIR gets the GIT_DIR headline' 1 \
+  "$(printf '%s\n' "$K_NODIR" | grep -c 'GIT_DIR is not among them')"
+check 'QA-7: that case no longer prints the could-not-ask headline' 0 \
+  "$(printf '%s\n' "$K_NODIR" | grep -c 'could not ask git which variables')"
+check 'CONTROL: the parenthetical still names the cause (the reference pins it)' 1 \
+  "$(printf '%s\n' "$K_NODIR" | grep -cE 'with [1-9][0-9]* usable name\(s\), GIT_DIR absent')"
+K_EMPTYBIN="$(mktemp -d "$TMP/emptybin.XXXXXX")"
+printf '#!/usr/bin/env bash\nexit 0\n' > "$K_EMPTYBIN/git"; chmod +x "$K_EMPTYBIN/git"
+K_EMPTY="$( cd "$R/Blockchain/Dev" && PATH="$K_EMPTYBIN:$PATH" bash scripts/run-shell-suites.sh 2>&1 )"
+check 'CONTROL: git printing NOTHING keeps the could-not-ask headline' 1 \
+  "$(printf '%s\n' "$K_EMPTY" | grep -c 'could not ask git which variables')"
+
+echo "run_shell_suites_polish: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 ]]
```
