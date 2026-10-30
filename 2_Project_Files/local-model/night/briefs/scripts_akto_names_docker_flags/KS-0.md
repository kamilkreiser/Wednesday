# KS-0 check-akto-container-names.sh: `docker exec -it akto-mongo` and other flagged docker verbs pass the gate (found by operator 26, no ticket; RUNG 2, bash_patch: one product line spelled, plus a new real-tools suite given whole)

DRAFT by Spark operator 25 for Wednesday, 2026-10-30 AEDT. Secuura (Blockchain/Dev/scripts) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: operator 25's screen of the sibling check-*.sh guards (plant a real violation in a scratch tree, run the script; method of operator 24). No Linear ticket exists; the raise seat files one on the board account or links the filing.

File: `Blockchain/Dev/scripts/check-akto-container-names.sh`  (product, modified in place: 1 hunk)
Test file: `Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh`  (NEW, 61 lines)
Tip: `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558` (develop, read with `git show`-equivalent in a clone at exactly this sha on 2026-10-30)
Runner: `bash` (bash 3.2, `bash Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh` from the repo root)
Tier: `bash_patch`
Rung: **2** (1 product hunk given byte-exact; the test is copied whole)

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, in this order:
1. `Blockchain/Dev/scripts/check-akto-container-names.sh` - modified in place, EXACTLY the 1 hunk under "The exact change", byte for byte.
2. `Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh` - a NEW file: `--- /dev/null` then `+++ b/Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh`, ONE hunk `@@ -0,0 +1,61 @@`, every line `+`.

You never touch any other file. The sibling `check_no_latest_tags.test.sh` is shape reference only - do NOT touch it.

## What is wrong (one paragraph)

`check-akto-container-names.sh:82` builds the first alternative of the gate's pattern as `docker[[:space:]]+(exec|logs|inspect|cp|kill|stop|rm|restart)[[:space:]]+["'\`]?akto-[a-z0-9-]+`: only whitespace may sit between the verb and the container name. The everyday forms put option flags there (`docker exec -it akto-mongo mongosh`, `docker logs --tail=50 akto-testing`), and those pass the gate (exit 0, no output) although they target slot 1 whatever slot the run is aimed at, which is the exact defect the gate exists for (KS-666 / KS-687 F2). The fix is one line: allow any number of `-flag` words between the verb and the name, `([[:space:]]+-[^[:space:]]+)*`.

## Where

- :82 - **must change** (the one `PATTERN=` line). Every other line stays.

## The exact change

1 hunk.

```diff
@@ -79,7 +79,7 @@
 # One alternation, four shapes; see the header. `[a-z0-9-]+` after `akto-` is the role (mongo,
 # testing, dashboard, …). No `AKTO_PREFIX` line-exclusion: the derived forms simply do not match, and
 # a line-level exclusion would let `${X:-akto-mongo}  # cf. AKTO_PREFIX` through.
-PATTERN="(docker[[:space:]]+(exec|logs|inspect|cp|kill|stop|rm|restart)[[:space:]]+[\"'\`]?akto-[a-z0-9-]+)"
+PATTERN="(docker[[:space:]]+(exec|logs|inspect|cp|kill|stop|rm|restart)([[:space:]]+-[^[:space:]]+)*[[:space:]]+[\"'\`]?akto-[a-z0-9-]+)"
 PATTERN+="|(_CONTAINER[[:space:]]*=[[:space:]]*[\"'][a-z]*akto-[a-z0-9-]+[\"'])"
 PATTERN+="|(\\$\\{[A-Za-z_]+:-[\"']?akto-[a-z0-9-]+)"
 PATTERN+="|((\\?\\?|\\|\\|)[[:space:]]*[\"'\`]akto-[a-z0-9-]+[\"'\`])"
```

**Do NOT touch** any other line of the script.

## The test

File: `Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh`
The shape is the sibling suite `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` (a fixture root with `scripts/<subject>`, the subject resolving its own root).

Emit this text as the new-file hunk `@@ -0,0 +1,61 @@`, every line prefixed `+`, nothing added or dropped (blank lines in it are `+` lines with nothing after the `+`):

```bash
#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-akto-container-names.sh - a docker verb followed by
# option flags before the container name must still be flagged.
# =============================================================================
# The first alternative of the gate's pattern is `docker <verb> <optional quote>akto-<role>` with
# only whitespace between the verb and the name, so the everyday forms `docker exec -it akto-mongo
# mongosh` and `docker logs --tail=50 akto-testing` pass the gate although they target slot 1.
# Real grep and find, a private fixture tree; nothing outside the temp dir is read.
# Usage: bash Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${CHECK_AKTO_CONTAINER_NAMES_SH:-$HERE/../check-akto-container-names.sh}"
[[ -r "$SUBJ" ]] || { echo "FATAL: check-akto-container-names.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/akto-flags.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0

run_case() {   # $1 = case name, $2 = line planted in scripts/z.sh -> prints the gate's exit code
  local d="$WORK/$1"
  mkdir -p "$d/src" "$d/bin" "$d/scripts"
  printf 'export const a = 1;\n' > "$d/src/ok.ts"
  printf 'export const b = 1;\n' > "$d/bin/ok.ts"
  printf '#!/bin/bash\n%s\n' "$2" > "$d/scripts/z.sh"
  bash "$SUBJ" "$d" >"$WORK/$1.out" 2>&1
  echo $?
}

check() {   # $1 = label, $2 = want rc, $3 = got rc
  if [[ "$3" == "$2" ]]; then
    echo "PASS: $1"; PASS=$((PASS+1))
  else
    echo "FAIL: $1 (want rc $2, got rc $3)"; FAIL=$((FAIL+1))
  fi
}

# CELL 1 (RED at the tip) - short flags between the verb and the name.
check "docker exec -it akto-mongo is flagged" 1 "$(run_case c1 'docker exec -it akto-mongo mongosh')"

# CELL 2 (RED at the tip) - a long flag with its value attached, and a quoted name.
check "docker logs --tail=50 \"akto-testing\" is flagged" 1 "$(run_case c2 'docker logs --tail=50 "akto-testing"')"

# CELL 3 (RED at the tip) - two flags in a row.
check "docker exec -i -t akto-mongo is flagged" 1 "$(run_case c3 'docker exec -i -t akto-mongo mongosh')"

# CELL 4 (GREEN CONTROL, tip AND after) - the plain literal is still flagged.
check "CONTROL docker exec akto-mongo is still flagged" 1 "$(run_case c4 'docker exec akto-mongo mongosh')"

# CELL 5 (GREEN CONTROL, tip AND after) - the derived form with flags is the fix, not the defect.
check "CONTROL docker exec -it with the AKTO_PREFIX form is clean" 0 "$(run_case c5 'docker exec -it "${AKTO_PREFIX:-akto}-mongo" mongosh')"

# CELL 6 (GREEN CONTROL, tip AND after) - flags before a non-akto container are clean.
check "CONTROL docker exec -it other-container is clean" 0 "$(run_case c6 'docker exec -it other-mongo mongosh')"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
```

## Red cells
- docker exec -it akto-mongo is flagged
- docker logs --tail=50 "akto-testing" is flagged
- docker exec -i -t akto-mongo is flagged

## Cells and controls

- RED CELL 1 `docker exec -it akto-mongo is flagged` - red at the tip (exit 0), green with the hunk.
- RED CELL 2 `docker logs --tail=50 "akto-testing" is flagged` - red at the tip.
- RED CELL 3 `docker exec -i -t akto-mongo is flagged` - red at the tip.
- green CELL 4 `CONTROL docker exec akto-mongo is still flagged`.
- green CELL 5 `CONTROL docker exec -it with the AKTO_PREFIX form is clean` - the fix shape stays clean.
- green CELL 6 `CONTROL docker exec -it other-container is clean`.

## The failing case (the "tamper")

Product fix, no tamper. Measured in a scratch tree (the tip's script copied out, the suite pointed at it with its `CHECK_..._SH` variable): the suite at the tip is `3 passed, 3 failed` (CELLS 1-3) and with the edited script `6 passed, 0 failed`, on macOS bash 3.2; the existing sibling suite check_akto_container_names.test.sh is unchanged by the edit, and the edited script still exits 0 on the real systemTest/akto tree.

## Premises (each one measured, with where)

- At `85cd24d81cb9` line 82 is the quoted pattern line; planted in a scratch package (src/, bin/, scripts/ each with a file), `docker exec -it akto-mongo mongosh`, `docker exec -i "akto-mongo" mongosh` and `docker logs --tail 5 akto-testing` each exited 0 with empty output, while `docker exec akto-mongo mongosh` exited 1. The repo's own docs write the `-it` form (systemTest/akto/docs/quick-start.md:422, with the derived name). The sibling suite has no flagged-verb case (grep of its docker lines).
- The suite resolves the subject through an environment variable (default: the script beside `__tests__/`); nothing in it touches the real tree.

## UNMEASURED - stated rather than glossed

- The drafter ran the suite by hand against the tip and the edited script (results above) but did NOT run `round.sh --dry-run`/`--control` before this text was written; that run is the proof.
- Whether CI runs `__tests__/*.test.sh` automatically is not measured here.

## Scope

**Refs the filing (no ticket); never a close-word.** Only the line(s) named above; nothing else in the script.

## Output

Exactly ONE fenced ```diff block, nothing outside it:
1. the product file (`--- a/Blockchain/Dev/scripts/check-akto-container-names.sh` / `+++ b/Blockchain/Dev/scripts/check-akto-container-names.sh`) with the hunk given under "The exact change";
2. the new test file (`--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh`, `@@ -0,0 +1,61 @@`), every line `+`.
Every `+` line on its own physical line. Every context line keeps its leading space.
