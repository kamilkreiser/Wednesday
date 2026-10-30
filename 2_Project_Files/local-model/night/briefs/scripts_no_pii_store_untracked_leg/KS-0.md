# KS-0 check-no-pii-store.sh: the untracked-file leg never fires (invalid git option) and, once it does, would end the script early on a warning (found by operator 25, no ticket; RUNG 3, bash_patch: two product lines spelled in two hunks, plus a new real-git suite given whole)

DRAFT by Spark operator 25 for Wednesday, 2026-10-30 AEDT. Secuura (Blockchain/Dev/scripts) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: operator 25's screen of the sibling check-*.sh guards (plant a real violation in a scratch tree, run the script; method of operator 24). No Linear ticket exists; the raise seat files one on the board account or links the filing.

File: `Blockchain/Dev/scripts/check-no-pii-store.sh`  (product, modified in place: 2 hunks)
Test file: `Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh`  (NEW, 84 lines)
Tip: `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558` (develop, read with `git show`-equivalent in a clone at exactly this sha on 2026-10-30)
Runner: `bash` (bash 3.2, `bash Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh` from the repo root)
Tier: `bash_patch`
Rung: **3** (2 product hunks given byte-exact; the test is copied whole)

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, in this order:
1. `Blockchain/Dev/scripts/check-no-pii-store.sh` - modified in place, EXACTLY the 2 hunks under "The exact change", byte for byte.
2. `Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh` - a NEW file: `--- /dev/null` then `+++ b/Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh`, ONE hunk `@@ -0,0 +1,84 @@`, every line `+`.

You never touch any other file. The sibling `check_no_latest_tags.test.sh` is shape reference only - do NOT touch it.

## What is wrong (one paragraph)

Two faults in the second leg. (1) `:56` runs `git ls-files --others --exclude-standard=false ...`; `--exclude-standard` takes no value, so git exits 129 with `option exclude-standard takes no value`, `|| true` hides it, and `UNTRACKED` is always empty: an untracked, not-ignored `pii-data.local.json` (a variant the header names) is never reported. The fix is `--exclude-standard`. (2) `:64` is `{ [ -n "$UNTRACKED" ] && echo ...; [ -n "$FOUND" ] && echo ...; } | sed ...`: when only UNTRACKED is set the group ends on a failing test, `pipefail` + `set -e` exit the script with 1 in the middle of a block that says `(Warning, not a failure.)`. The fix is a final `true;` in the group. Both edits are needed; either alone leaves a visible fault.

## Where

- :56 - **must change** (`--exclude-standard=false` becomes `--exclude-standard`). :64 - **must change** (a `true;` is added before the closing brace). Everything else stays.

## The exact change

2 hunks.

```diff
@@ -53,7 +53,7 @@
 # Second leg: the store must not sit inside the working tree even UNTRACKED —
 # an untracked store is one `git add -f`, or one .gitignore edit, from exposure,
 # and `git clean -fdx` will silently destroy it.
-UNTRACKED=$(git ls-files --others --exclude-standard=false \
+UNTRACKED=$(git ls-files --others --exclude-standard \
               '*pii*.json' '*ks256-pii-data*' 2>/dev/null || true)
 # --exclude-standard=false still honours .gitignore for `--others`, so also scan
 # the filesystem directly: an ignored file is exactly the case we want to warn on.
@@ -62,6 +62,6 @@
 if [ -n "$UNTRACKED" ] || [ -n "$FOUND" ]; then
   echo "WARNING (KS-256): a PII store file exists inside the working tree:" >&2
-  { [ -n "$UNTRACKED" ] && echo "$UNTRACKED"; [ -n "$FOUND" ] && echo "$FOUND"; } | sed 's/^/  /' >&2
+  { [ -n "$UNTRACKED" ] && echo "$UNTRACKED"; [ -n "$FOUND" ] && echo "$FOUND"; true; } | sed 's/^/  /' >&2
   echo "" >&2
   echo "  It is ignored today, but an in-repo store is one .gitignore slip from" >&2
   # NOTE: single-quoted deliberately. This line previously used double quotes with
```

**Do NOT touch** any other line of the script.

## The test

File: `Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh`
The shape is the sibling suite `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` (a fixture root with `scripts/<subject>`, the subject resolving its own root).

Emit this text as the new-file hunk `@@ -0,0 +1,84 @@`, every line prefixed `+`, nothing added or dropped (blank lines in it are `+` lines with nothing after the `+`):

```bash
#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-no-pii-store.sh - its second (untracked) leg must work
# and must stay a WARNING.
# =============================================================================
# Two faults. (1) `git ls-files --others --exclude-standard=false` is not a valid option
# (`--exclude-standard` takes no value): git exits 129, `|| true` hides it, UNTRACKED is always
# empty, and an untracked pii-data.local.json is never reported although the header promises the
# whole family. (2) Once (1) works, `{ [ -n UNTRACKED ] && echo ...; [ -n FOUND ] && echo ...; }` ends
# on a failing test when only UNTRACKED is set, so `set -e` + `pipefail` exit the script with 1
# in the middle of a "Warning, not a failure" block.
# Real git and a private fixture repo in a temp dir; nothing outside it is read.
# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${CHECK_NO_PII_STORE_SH:-$HERE/../check-no-pii-store.sh}"
[[ -r "$SUBJ" ]] || { echo "FATAL: check-no-pii-store.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/pii.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0
REAL_GREP="$(command -v grep)"

run_case() {   # $1 = name, $2 = file to plant (relative to Blockchain/Dev, "" for none), $3 = 1 to git-add it, $4 = 1 to gitignore it
  local root="$WORK/$1"
  mkdir -p "$root/Blockchain/Dev/scripts"
  cp "$SUBJ" "$root/Blockchain/Dev/scripts/check-no-pii-store.sh"
  git -C "$root" init -q
  if [[ -n "$2" ]]; then
    echo '{}' > "$root/Blockchain/Dev/$2"
    [[ "$4" == "1" ]] && echo "$2" > "$root/Blockchain/Dev/.gitignore"
    [[ "$3" == "1" ]] && git -C "$root" add "Blockchain/Dev/$2"
  fi
  ( cd "$root" && bash Blockchain/Dev/scripts/check-no-pii-store.sh ) >"$WORK/$1.out" 2>&1
  echo $?
}

RC_UNTR="$(run_case untr pii-data.local.json 0 0)"
RC_TRACKED="$(run_case tracked pii-data.json 1 0)"
RC_CLEAN="$(run_case clean "" 0 0)"
RC_IGN="$(run_case ign ks256-pii-data.json 0 1)"

# CELL 1 (RED at the tip) - an untracked, not-ignored pii variant is reported by name.
if "$REAL_GREP" -qF 'WARNING (KS-256)' "$WORK/untr.out" && "$REAL_GREP" -qF 'pii-data.local.json' "$WORK/untr.out"; then
  echo "PASS: an untracked pii-data.local.json is reported"; PASS=$((PASS+1))
else
  echo "FAIL: untracked variant not reported: out=$(head -3 "$WORK/untr.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 2 (RED at the tip) - that report is a warning: exit 0 and the closing line is printed.
if [[ "$RC_UNTR" == "0" ]] && "$REAL_GREP" -qF 'Warning, not a failure' "$WORK/untr.out"; then
  echo "PASS: the untracked-file report exits 0 and prints its full block"; PASS=$((PASS+1))
else
  echo "FAIL: untracked variant: rc=$RC_UNTR out=$(tail -2 "$WORK/untr.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 3 (GREEN CONTROL, tip AND after) - a tracked pii file exits 1 with the ERROR and the git rm hint.
if [[ "$RC_TRACKED" == "1" ]] && "$REAL_GREP" -qF 'ERROR (KS-256)' "$WORK/tracked.out" \
   && "$REAL_GREP" -qF 'git rm --cached Blockchain/Dev/pii-data.json' "$WORK/tracked.out"; then
  echo "PASS: CONTROL a tracked pii file exits 1 with the git rm hint"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL tracked: rc=$RC_TRACKED out=$(head -3 "$WORK/tracked.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 4 (GREEN CONTROL, tip AND after) - a clean repo exits 0 with the OK line and no warning.
if [[ "$RC_CLEAN" == "0" ]] && "$REAL_GREP" -qF 'no PII store file is tracked' "$WORK/clean.out" \
   && ! "$REAL_GREP" -qF 'WARNING' "$WORK/clean.out"; then
  echo "PASS: CONTROL a clean repo exits 0 with no warning"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL clean: rc=$RC_CLEAN out=$(head -3 "$WORK/clean.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 5 (GREEN CONTROL, tip AND after) - an IGNORED ks256 store is still found by the filesystem leg, exit 0.
if [[ "$RC_IGN" == "0" ]] && "$REAL_GREP" -qF 'ks256-pii-data.json' "$WORK/ign.out"; then
  echo "PASS: CONTROL an ignored ks256 store is still warned about, exit 0"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL ignored store: rc=$RC_IGN out=$(head -3 "$WORK/ign.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

echo "check_no_pii_store_untracked_leg: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 && "$PASS" -eq 5 ]]
```

## Red cells
- an untracked pii-data.local.json is reported
- the untracked-file report exits 0 and prints its full block

## Cells and controls

- RED CELL 1 `an untracked pii-data.local.json is reported` - red at the tip (the leg is dead), green with the hunks.
- RED CELL 2 `the untracked-file report exits 0 and prints its full block` - red at the tip; it is also what keeps edit 2 honest (with edit 1 alone it stays red).
- green CELL 3 `CONTROL a tracked pii file exits 1 with the git rm hint`.
- green CELL 4 `CONTROL a clean repo exits 0 with no warning`.
- green CELL 5 `CONTROL an ignored ks256 store is still warned about, exit 0` - the filesystem leg.

## The failing case (the "tamper")

Product fix, no tamper. Measured in a scratch tree (the tip's script copied out, the suite pointed at it with its `CHECK_..._SH` variable): the suite at the tip is `3 passed, 2 failed` (CELLS 1 and 2) and with the edited script `5 passed, 0 failed`; real git, bash 3.2.

## Premises (each one measured, with where)

- At `85cd24d81cb9` `git ls-files --others --exclude-standard=false '*pii*.json'` prints `error: option exclude-standard takes no value` and exits 129 (measured here); a scratch repo with an untracked `pii-data.local.json` printed only the OK line at the tip. The script is run by `run-code-guards.sh:84`.
- The suite resolves the subject through an environment variable (default: the script beside `__tests__/`); nothing in it touches the real tree.

## UNMEASURED - stated rather than glossed

- The drafter ran the suite by hand against the tip and the edited script (results above) but did NOT run `round.sh --dry-run`/`--control` before this text was written; that run is the proof.
- Whether CI runs `__tests__/*.test.sh` automatically is not measured here.

## Scope

**Refs the filing (no ticket); never a close-word.** Only the line(s) named above; nothing else in the script.

## Output

Exactly ONE fenced ```diff block, nothing outside it:
1. the product file (`--- a/Blockchain/Dev/scripts/check-no-pii-store.sh` / `+++ b/Blockchain/Dev/scripts/check-no-pii-store.sh`) with the hunks given under "The exact change";
2. the new test file (`--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh`, `@@ -0,0 +1,84 @@`), every line `+`.
Every `+` line on its own physical line. Every context line keeps its leading space.
