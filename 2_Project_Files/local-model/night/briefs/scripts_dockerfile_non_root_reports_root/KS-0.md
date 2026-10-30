# KS-0 check-dockerfile-non-root.sh: a Dockerfile with no USER dies silently, and under BSD sed a final USER root is read as USERroot and passes (found by operator 25, no ticket; RUNG 2, bash_patch: one product line spelled, plus a new real-tools suite given whole)

DRAFT by Spark operator 25 for Wednesday, 2026-10-30 AEDT. Secuura (Blockchain/Dev/scripts) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: operator 25's screen of the sibling check-*.sh guards (plant a real violation in a scratch tree, run the script; method of operator 24). No Linear ticket exists; the raise seat files one on the board account or links the filing.

File: `Blockchain/Dev/scripts/check-dockerfile-non-root.sh`  (product, modified in place: 1 hunk)
Test file: `Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh`  (NEW, 70 lines)
Tip: `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558` (develop, read with `git show`-equivalent in a clone at exactly this sha on 2026-10-30)
Runner: `bash` (bash 3.2, `bash Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh` from the repo root)
Tier: `bash_patch`
Rung: **2** (1 product hunk given byte-exact; the test is copied whole)

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, in this order:
1. `Blockchain/Dev/scripts/check-dockerfile-non-root.sh` - modified in place, EXACTLY the 1 hunk under "The exact change", byte for byte.
2. `Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh` - a NEW file: `--- /dev/null` then `+++ b/Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh`, ONE hunk `@@ -0,0 +1,70 @@`, every line `+`.

You never touch any other file. The sibling `check_no_latest_tags.test.sh` is shape reference only - do NOT touch it.

## What is wrong (one paragraph)

`check-dockerfile-non-root.sh:27` reads the last USER with `grep -E '^\s*USER\s+' "$f" | tail -1 | sed -E 's/^\s*USER\s+//; s/[#].*$//' | tr -d '[:space:]'` inside `$( )`, under `set -euo pipefail`. Two faults. (1) A Dockerfile with NO USER makes `grep` exit 1, `pipefail` fails the substitution and `set -e` ends the script silently: exit 1, no message, so the gate's own `has NO USER directive` branch (`:30`) is unreachable. (2) `\s` is not understood by BSD `sed -E` (macOS, the evidence host per KS-666), so `USER root` becomes `USERroot`, never equals `root` or `0`, and the gate prints OK for a root container. The fix is one line: POSIX classes in the grep and the sed, and `|| true` after the last pipe stage.

## Where

- :27 - **must change** (the whole `last_user=$(...)` line). Every other line stays.

## The exact change

1 hunk.

```diff
@@ -24,5 +24,5 @@
 for f in $DOCKERFILES; do
   # Find the LAST USER directive in the file (the one that takes effect at runtime).
   # Allow `USER root` only inside the build stages — the FINAL USER must not be root.
-  last_user=$(grep -E '^\s*USER\s+' "$f" | tail -1 | sed -E 's/^\s*USER\s+//; s/[#].*$//' | tr -d '[:space:]')
+  last_user=$(grep -E '^[[:space:]]*USER[[:space:]]+' "$f" | tail -1 | sed -E 's/^[[:space:]]*USER[[:space:]]+//; s/[#].*$//' | tr -d '[:space:]' || true)
 
```

**Do NOT touch** any other line of the script.

## The test

File: `Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh`
The shape is the sibling suite `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` (a fixture root with `scripts/<subject>`, the subject resolving its own root).

Emit this text as the new-file hunk `@@ -0,0 +1,70 @@`, every line prefixed `+`, nothing added or dropped (blank lines in it are `+` lines with nothing after the `+`):

```bash
#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-dockerfile-non-root.sh - a Dockerfile that
# runs as root, or has no USER at all, must be REPORTED, not swallowed.
# =============================================================================
# Two faults on the last_user line. (1) With no USER directive `grep` exits 1, `pipefail`
# makes the command substitution fail and `set -e` ends the script silently: exit 1, no
# message, so the gate fails but names no file. (2) The `sed -E` uses `\s`, which BSD sed
# (macOS) does not know, so `USER root` is read as `USERroot`, never equals `root`, and the
# gate prints OK for a root container.
# Real tools, a private fixture tree; nothing outside the temp dir is read.
# Usage: bash Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${CHECK_DOCKERFILE_NON_ROOT_SH:-$HERE/../check-dockerfile-non-root.sh}"
[[ -r "$SUBJ" ]] || { echo "FATAL: check-dockerfile-non-root.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/dfroot.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0
REAL_GREP="$(command -v grep)"

run_case() {   # $1 = name, $2 = Dockerfile text -> prints rc; output in $WORK/$1.out
  local root="$WORK/$1"
  mkdir -p "$root/scripts" "$root/services/s" "$root/frontend" "$root/docker" "$root/connectors" "$root/deployment"
  cp "$SUBJ" "$root/scripts/check-dockerfile-non-root.sh"
  printf '%s' "$2" > "$root/services/s/Dockerfile"
  ( cd "$root" && bash scripts/check-dockerfile-non-root.sh ) >"$WORK/$1.out" 2>&1
  echo $?
}

RC_NOUSER="$(run_case nouser $'FROM node:20\nRUN true\n')"
RC_ROOT="$(run_case root $'FROM node:20\nUSER root\n')"
RC_APP="$(run_case app $'FROM node:20\nUSER app\n')"
RC_MULTI="$(run_case multi $'FROM node:20 AS build\nUSER root\nFROM node:20\nUSER app\n')"

# CELL 1 (RED at the tip) - no USER directive: exit 1 AND the file is named.
if [[ "$RC_NOUSER" == "1" ]] && "$REAL_GREP" -qF 'has NO USER directive' "$WORK/nouser.out" \
   && "$REAL_GREP" -qF 'services/s/Dockerfile' "$WORK/nouser.out"; then
  echo "PASS: a Dockerfile with no USER directive exits 1 and is named"; PASS=$((PASS+1))
else
  echo "FAIL: no-USER case: rc=$RC_NOUSER out=$(head -2 "$WORK/nouser.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 2 (RED at the tip on a BSD/macOS userland) - a final USER root exits 1 and is named.
if [[ "$RC_ROOT" == "1" ]] && "$REAL_GREP" -qF "final USER is 'root'" "$WORK/root.out"; then
  echo "PASS: a final USER root exits 1 and is named"; PASS=$((PASS+1))
else
  echo "FAIL: USER root case: rc=$RC_ROOT out=$(head -2 "$WORK/root.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 3 (GREEN CONTROL, tip AND after) - a non-root USER passes.
if [[ "$RC_APP" == "0" ]] && "$REAL_GREP" -qF 'OK - all 1 Dockerfile' <(sed 's/ — / - /' "$WORK/app.out"); then
  echo "PASS: CONTROL USER app exits 0 with the OK line"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL USER app: rc=$RC_APP out=$(head -2 "$WORK/app.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 4 (GREEN CONTROL, tip AND after) - USER root in a build stage, non-root at the end, passes.
if [[ "$RC_MULTI" == "0" ]]; then
  echo "PASS: CONTROL a root build stage with a non-root final USER exits 0"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL multi-stage: rc=$RC_MULTI out=$(head -2 "$WORK/multi.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

echo "check_dockerfile_non_root_reports_root: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
```

## Red cells
- a Dockerfile with no USER directive exits 1 and is named
- a final USER root exits 1 and is named

## Cells and controls

- RED CELL 1 `a Dockerfile with no USER directive exits 1 and is named` - red at the tip (exit 1 but no output at all), green with the hunk.
- RED CELL 2 `a final USER root exits 1 and is named` - red at the tip on a BSD userland (macOS), where the script prints OK for it; on a GNU userland it is green both ways.
- green CELL 3 `CONTROL USER app exits 0 with the OK line`.
- green CELL 4 `CONTROL a root build stage with a non-root final USER exits 0` - the last USER wins, as before.

## The failing case (the "tamper")

Product fix, no tamper. Measured in a scratch tree (the tip's script copied out, the suite pointed at it with its `CHECK_..._SH` variable): the suite at the tip is `2 passed, 2 failed` (CELLS 1 and 2) and with the edited script `4 passed, 0 failed`, on macOS bash 3.2 with BSD sed.

## Premises (each one measured, with where)

- At `85cd24d81cb9` the script is 43 lines; planted in a scratch tree, a Dockerfile with no USER exited 1 with empty output, and `USER root`, `USER 0` both printed `OK - all 1 Dockerfile(s) drop root for runtime` (rc 0). `printf 'USER root\n' | sed -E 's/^\s*USER\s+//'` prints `USER root` unchanged on this Mac. The script is run by `run-code-guards.sh:79`.
- The suite resolves the subject through an environment variable (default: the script beside `__tests__/`); nothing in it touches the real tree.

## UNMEASURED - stated rather than glossed

- The drafter ran the suite by hand against the tip and the edited script (results above) but did NOT run `round.sh --dry-run`/`--control` before this text was written; that run is the proof.
- Whether CI runs `__tests__/*.test.sh` automatically is not measured here.

## Scope

**Refs the filing (no ticket); never a close-word.** Only the line(s) named above; nothing else in the script.

## Output

Exactly ONE fenced ```diff block, nothing outside it:
1. the product file (`--- a/Blockchain/Dev/scripts/check-dockerfile-non-root.sh` / `+++ b/Blockchain/Dev/scripts/check-dockerfile-non-root.sh`) with the hunk given under "The exact change";
2. the new test file (`--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh`, `@@ -0,0 +1,70 @@`), every line `+`.
Every `+` line on its own physical line. Every context line keeps its leading space.
