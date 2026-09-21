# KS-1033-item1 R16B-DEMOBASE - re-brief at develop 8c2f7b3fd of READY_KS-1033-item1_ornith35b-q4_BASHPATCH-RECOUNTED-PASS-7of7_2026-09-16.diff.md (written 2026-09-22 09:50:01 AEST by Wednesday's feed8 drafter; the product hunk and the new suite are the old READY's PASS 7/7 output re-anchored at the tip, every '+' line and every suite line made ASCII: the cell glyph is the word RED, em-dashes are hyphens; every context and '-' line asserted byte-exact at the tip at the line numbers below)

File: `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh`
Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
`Blockchain/Dev/scripts/check-no-demo-mutation.sh` refuses any change that touches a demo-shaping path
unless a commit in the range carries `[demo-mutation-allowed]`. It decides the range at `:51-60`: a
`GITHUB_BASE_REF` wins, then an explicit `$1`, and otherwise **it falls back to `BASE="origin/main"`
(`:58`)** and diffs `"$BASE...$HEAD"` (`:69`). The three-dot form takes the merge-base, which is right -
but the merge-base of `origin/main` and any develop-based branch is the point where `develop` was last
merged to `main`, **not** the branch point. Under Git Flow `develop` is permanently ahead of `main`, so
every develop-based branch is shown the whole develop-vs-main delta as if it were its own change. KS-1033
measured that on a branch that touched nothing: the guard reported four demo files as modified
(`deployment/azure/env.demo.json`, `migrate/Dockerfile`, `migrate/init.sql`, `migrate/run-platform.sh`).
This is not an abstract complaint - it is the sole reason the guard is UNWIRED. `run-code-guards.sh:116`
holds it in the `DEFERRED` bucket with exactly this reason and exactly this remedy in its own words:
*"Fix its base to the merge-base with origin/develop before wiring."* Until that is done the guard is a
check that cannot run, which is the defect KS-926 exists for; wired as-is it would demand
`[demo-mutation-allowed]` from every author on every push, which is the `--no-verify` generator KS-926
warns about. Changing the fallback to `origin/develop` makes `"$BASE...$HEAD"` resolve to the branch
point, so the diff contains the branch's own commits and nothing else.

**This is item 1 of KS-1033 and ONLY item 1.** The ticket records three unwired guards. Item 2
(`check-no-trust-header-reads.sh`, whose printed advice contradicts its own default) is explicitly
decision-class - the ticket says *"Deciding which is the point"* - and item 3
(`check-container-isolation.sh`) is a relocation to stack start-up, not an edit. Neither is touched here.
**Nothing in this task wires the guard**, either: it stays in `DEFERRED` and leg 15's census still
accounts for it, because wiring is a separate call that wants a measured push. This task removes the one
measured blocker the ticket names.

## The exact change - 2 hunk(s) in `Blockchain/Dev/scripts/check-no-demo-mutation.sh` (2 '-' line(s), 6 '+' line(s), one '+' group per hunk)
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]`), every `-` line and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a backslash on a `+` line is copied as written, never escaped.
```
--- a/Blockchain/Dev/scripts/check-no-demo-mutation.sh
+++ b/Blockchain/Dev/scripts/check-no-demo-mutation.sh
@@ -49,5 +49,9 @@ DEMO_PREFIXES=(
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
@@ -55,6 +59,6 @@ elif [ -n "${1:-}" ]; then
   BASE="$1"
   HEAD="${2:-HEAD}"
 else
-  BASE="origin/main"
+  BASE="origin/develop"
   HEAD="HEAD"
 fi
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:50` - **must change**: `# default to comparing against origin/main.`
* `:58` - **must change**: `  BASE="origin/main"`
* `:49` - (correct) `# Determine the diff range. In CI this is the PR base..head; locally` - stays
* `:51` - (correct) `if [ -n "${GITHUB_BASE_REF:-}" ]; then` - stays

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh`

File: `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` (full content in `files[...]`) and locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d` and never edits the repo's real files.

**Reproduce the file below EXACTLY as written - every line, in order (126 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. Every value a cell reads is assigned above the first cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh`, ONE hunk header `@@ -0,0 +1,126 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-no-demo-mutation.sh - the DEFAULT diff
# base must be origin/develop, not origin/main (KS-1033 item 1)
# =============================================================================
# Under Git Flow develop is permanently ahead of main, so an origin/main base
# shows the whole develop-vs-main delta as this branch's own change. Every
# fixture is a throwaway repo under mktemp -d pushing to a LOCAL BARE REMOTE.
# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh
# =============================================================================

set -uo pipefail

export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${DEMO_GUARD_SH:-$HERE/../check-no-demo-mutation.sh}"
[ -r "$SUBJ" ] || { echo "FATAL: check-no-demo-mutation.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1033.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0
EXPECTED_CELLS=4
DEMO_FILE="Blockchain/Dev/deployment/azure/migrate/init.sql"
PLAIN_FILE="Blockchain/Dev/README.md"

build() {
  rm -rf "$1"
  mkdir -p "$1"
  (
    export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
    git init -q --bare -b main "$1/origin.git"
    git init -q -b main "$1/seed"
    cd "$1/seed" || exit 9
    git config user.email t@t.t
    git config user.name t
    mkdir -p Blockchain/Dev/deployment/azure/migrate
    echo base > "$PLAIN_FILE"
    echo base > "$DEMO_FILE"
    git add -A
    git commit -qm init
    git checkout -q -b develop
    echo "develop moved ahead" > "$DEMO_FILE"
    git add -A
    git commit -qm "develop touches a demo path"
    git remote add origin "$1/origin.git"
    git push -q origin main develop
    cd "$1" || exit 9
    git clone -q "$1/origin.git" work
    cd "$1/work" || exit 9
    git config user.email t@t.t
    git config user.name t
    git checkout -q -b feature origin/develop
    if [ "$2" = demo ]; then
      echo "feature touches a demo path too" > "$DEMO_FILE"
    else
      echo "an ordinary change" > "$PLAIN_FILE"
    fi
    git add -A
    git commit -qm "feature work"
  ) > "$1/build.log" 2>&1
}

run_guard() {
  (
    unset GITHUB_BASE_REF
    if [ -n "$2" ]; then export GITHUB_BASE_REF="$2"; fi
    cd "$1/work" || exit 9
    bash "$SUBJ"
  ) > "$1/out.txt" 2>&1
  echo $?
}

build "$WORK/plain" plain
RC_PLAIN="$(run_guard "$WORK/plain" "")"
OUT_PLAIN="$WORK/plain/out.txt"
build "$WORK/demo" demo
RC_DEMO="$(run_guard "$WORK/demo" "")"
OUT_DEMO="$WORK/demo/out.txt"
build "$WORK/ciref" plain
RC_CIREF="$(run_guard "$WORK/ciref" develop)"
OUT_CIREF="$WORK/ciref/out.txt"

# CELL 1 (RED at the tip) - a develop-based branch that touched no demo path
# must be allowed. At the tip the origin/main base drags develop's own demo
# commit into the diff and the guard exits 1.
if [ "$RC_PLAIN" = "0" ]; then
  echo "PASS: a develop-based branch touching no demo path exits 0"; PASS=$((PASS+1))
else
  echo "FAIL: a develop-based branch touching no demo path exited $RC_PLAIN, not 0 - the base dragged in develop's own commits ($(grep -c 'migrate/init.sql' "$OUT_PLAIN") demo path line(s) reported)"; FAIL=$((FAIL+1))
fi

# CELL 2 (RED at the tip) - and it must say so, not print the block banner.
if grep -qF 'no demo-shaping paths touched' "$OUT_PLAIN" && ! grep -qF 'DEMO MUTATION DETECTED' "$OUT_PLAIN"; then
  echo "PASS: the guard reports no demo-shaping paths touched and prints no block banner"; PASS=$((PASS+1))
else
  echo "FAIL: clean-message present=$(grep -qF 'no demo-shaping paths touched' "$OUT_PLAIN" && echo yes || echo NO), block banner present=$(grep -qF 'DEMO MUTATION DETECTED' "$OUT_PLAIN" && echo YES || echo no)"; FAIL=$((FAIL+1))
fi

# CELL 3 (GREEN CONTROL, tip AND after) - the guard still refuses a REAL demo
# change on the branch itself. This is what stops a fix that just always passes.
if [ "$RC_DEMO" = "1" ] && grep -qF 'DEMO MUTATION DETECTED' "$OUT_DEMO"; then
  echo "PASS: CONTROL a branch that really touches a demo path is still blocked with exit 1"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL a real demo change exited $RC_DEMO (want 1), banner present=$(grep -qF 'DEMO MUTATION DETECTED' "$OUT_DEMO" && echo yes || echo NO)"; FAIL=$((FAIL+1))
fi

# CELL 4 (GREEN CONTROL, tip AND after) - GITHUB_BASE_REF still wins over the
# default, so the branch named there is what the diff is taken against.
if [ "$RC_CIREF" = "0" ] && grep -qF 'no demo-shaping paths touched' "$OUT_CIREF"; then
  echo "PASS: CONTROL GITHUB_BASE_REF=develop is still honoured ahead of the default"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL GITHUB_BASE_REF=develop exited $RC_CIREF (want 0): $(head -1 "$OUT_CIREF")"; FAIL=$((FAIL+1))
fi

# CELL 5 - the completeness guard. A suite that exits 0 having asserted nothing
# is a check that cannot fail, so a short count is itself a FAIL.
if [ $((PASS + FAIL)) -eq "$EXPECTED_CELLS" ]; then
  echo "PASS: all $EXPECTED_CELLS cells ran"; PASS=$((PASS+1))
else
  echo "FAIL: only $((PASS + FAIL)) of $EXPECTED_CELLS cells ran - a suite that asserts nothing is not a pass"; FAIL=$((FAIL+1))
fi

echo ""
echo "check_no_demo_mutation_base: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ]
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `# CELL 1 (RED at the tip) - a develop-based branch that touched no demo path`
- `echo "PASS: a develop-based branch touching no demo path exits 0"; PASS=$((PASS+1))`
- `# CELL 2 (RED at the tip) - and it must say so, not print the block banner.`
- `echo "PASS: the guard reports no demo-shaping paths touched and prints no block banner"; PASS=$((PASS+1))`
- `# CELL 3 (GREEN CONTROL, tip AND after) - the guard still refuses a REAL demo`
- `echo "PASS: CONTROL a branch that really touches a demo path is still blocked with exit 1"; PASS=$((PASS+1))`
- `# CELL 4 (GREEN CONTROL, tip AND after) - GITHUB_BASE_REF still wins over the`
- `echo "PASS: CONTROL GITHUB_BASE_REF=develop is still honoured ahead of the default"; PASS=$((PASS+1))`
- `# CELL 5 - the completeness guard. A suite that exits 0 having asserted nothing`
- `echo "PASS: all $EXPECTED_CELLS cells ran"; PASS=$((PASS+1))`

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/scripts/check-no-demo-mutation.sh` / `+++ b/Blockchain/Dev/scripts/check-no-demo-mutation.sh` (2 hunk(s), copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh` (one hunk, `@@ -0,0 +1,126 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed8 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 09:50:01 AEST)
- `Blockchain/Dev/scripts/check-no-demo-mutation.sh` at the tip carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief.py against `git show 8c2f7b3fd:Blockchain/Dev/scripts/check-no-demo-mutation.sh`); the rebuilt product section applies STRICT (`git apply --check -p1` rc 0 in the clone).
- The new suite `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` is present.
- Every `+` line of the product hunk(s) and every line of the suite is ASCII (non-ASCII 0, asserted); the FEED 8 ruling (Wednesday, 2026-09-22 09:3x) WAIVES the `"` 0 / `\` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk, whitespace-stripped) and B4/B5 (RED at the tip, GREEN after).
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: see `runs/2026-09-22_feed8-drafter-precheck/DEMOBASE/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1033 on the Secuura board at 2026-09-22 09:50:01 AEST: Backlog, not archived (`board_states.log`). The product file is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
