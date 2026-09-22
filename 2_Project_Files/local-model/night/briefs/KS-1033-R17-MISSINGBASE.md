# KS-1033 R17-MISSINGBASE - bash_patch at develop 2bc5ccf63: `scripts/check-no-demo-mutation.sh` REFUSES a diff base it cannot resolve (exit 2, a line naming it) instead of printing "nothing to compare" and exiting 0 - gate 19C's NOT-PINNED row DEMOBASE-MISSINGBASE-FAILOPEN on #1185 (written 2026-09-22 19:49:00 AEST by Wednesday's feed17 drafter; every context line below is read from the tip file, never typed)

File: `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh`
Tip: 2bc5ccf63b8c40911afb568b03cace066238ffcf
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
#1185 (KS-1033) made `origin/develop` the guard's default diff base. Gate 19C then measured the pre-existing fail-open at `:66-:70` on that name: in a clone whose origin has NO `develop` (a `--single-branch main` clone, a fresh fork) `git rev-parse --verify origin/develop` fails, the guard prints `[demo-guard] base origin/develop not found; nothing to compare` and exits 0 - so a commit that touches a demo-shaping path on that tree reads as CLEAN. A guard whose whole purpose is "false positives are cheaper than shipping to live customers" (`:26-:27`) must not read an unmeasurable tree as clean. The change is the smallest fail-closed one: the same `if` block now prints WHY on stderr and exits 2 (2, not 1: 1 already means "mutation detected", `:144`). Nothing else changes: `GITHUB_BASE_REF`, the explicit `$1` base, the three-dot diff, the override token and the banner are untouched. The guard is run by hand today (it is in `run-code-guards.sh`'s DEFERRED bucket, `:116`, and `.github/workflows/ci.yml` does not name it), so the exit-code change reaches no pipeline. NOT in this task: wiring the guard anywhere, the stale DEFERRED reason text, the script header's stale "wired into ci.yml" claim.

## The exact change - 1 hunk(s) in `Blockchain/Dev/scripts/check-no-demo-mutation.sh` (3 '-' line(s), 3 '+' line(s))
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, the `@@` header, every context line (a leading space, copied from `files[product_file]`), every `-` line and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a dollar sign on a `+` line is copied as written, never escaped; there is no backslash on any `+` line.
```
--- a/Blockchain/Dev/scripts/check-no-demo-mutation.sh
+++ b/Blockchain/Dev/scripts/check-no-demo-mutation.sh
@@ -66,5 +66,5 @@
-# Skip if we can't resolve the base (first commit on a fresh clone).
+# KS-1033: a base that cannot be resolved is REFUSED (exit 2), never read as clean.
 if ! git rev-parse --verify "$BASE" >/dev/null 2>&1; then
-  echo "[demo-guard] base $BASE not found; nothing to compare"
-  exit 0
+  echo "[demo-guard] base $BASE cannot be resolved; refusing to read the tree as clean" >&2
+  exit 2
 fi
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)

* `:66` - **must change** - `# Skip if we can't resolve the base (first commit on a fresh clone).` - becomes the KS-1033 comment line
* `:67` - (correct) `if ! git rev-parse --verify "$BASE" >/dev/null 2>&1; then` - stays (the resolve check; context)
* `:68` - **must change** - `  echo "[demo-guard] base $BASE not found; nothing to compare"` - becomes the stderr line naming the base
* `:69` - **must change** - `  exit 0` - becomes `exit 2`
* `:70` - (correct) `fi` - stays (context)

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh`

File: `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh` (full content in `files[...]`; the suite #1185 added) and copies its shape: throwaway repos under `mktemp -d` pushing to a LOCAL BARE REMOTE, `GIT_CONFIG_GLOBAL=/dev/null`, a `build` that seeds `main` (and optionally `develop`) and cuts a `feature` branch that touches a demo path, a `run_guard` that runs the REAL script with `GITHUB_BASE_REF` unset, `PASS:`/`FAIL:` lines, `PASS`/`FAIL` counters, the completeness cell and the totals line. It locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d`, never edits the repo's real files and never touches a network.

**Reproduce the file below EXACTLY as written - every line, in order (133 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh`, ONE hunk header `@@ -0,0 +1,133 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-no-demo-mutation.sh - a diff BASE that
# cannot be resolved is REFUSED (exit 2), never read as "nothing to compare"
# (KS-1033; gate 19C finding DEMOBASE-MISSINGBASE-FAILOPEN on #1185)
# =============================================================================
# The default base is origin/develop (KS-1033 item 1). In a clone whose origin
# has NO develop (a --single-branch main clone, a fresh fork) the guard printed
# "base origin/develop not found; nothing to compare" and exited 0, so a demo
# mutation on that tree read as clean. Every fixture is a throwaway repo under
# mktemp -d pushing to a LOCAL BARE REMOTE, in the shape of
# check_no_demo_mutation_base.test.sh.
# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh
# =============================================================================

set -uo pipefail

export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${DEMO_GUARD_SH:-$HERE/../check-no-demo-mutation.sh}"
[ -r "$SUBJ" ] || { echo "FATAL: check-no-demo-mutation.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1033b.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0
EXPECTED_CELLS=4
DEMO_FILE="Blockchain/Dev/deployment/azure/migrate/init.sql"
PLAIN_FILE="Blockchain/Dev/README.md"

# build DIR LAST: a bare origin holding main only (LAST=main) or main AND develop
# (LAST=develop), then a clone whose feature branch is cut from origin/LAST and
# touches a demo path - a real demo mutation on every fixture.
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
    git remote add origin "$1/origin.git"
    if [ "$2" = develop ]; then
      git checkout -q -b develop
      echo "develop moved ahead" > "$PLAIN_FILE"
      git add -A
      git commit -qm "develop moves ahead on a plain path"
      git push -q origin main develop
    else
      git push -q origin main
    fi
    cd "$1" || exit 9
    git clone -q "$1/origin.git" work
    cd "$1/work" || exit 9
    git config user.email t@t.t
    git config user.name t
    git checkout -q -b feature "origin/$2"
    echo "feature touches a demo path" > "$DEMO_FILE"
    git add -A
    git commit -qm "feature work"
  ) > "$1/build.log" 2>&1
}

# run_guard DIR BASE-ARG TAG: the real guard with GITHUB_BASE_REF unset, with an
# explicit base argument when BASE-ARG is non-empty. Prints its exit code; the
# combined output lands in DIR/out-TAG.txt.
run_guard() {
  (
    unset GITHUB_BASE_REF
    cd "$1/work" || exit 9
    if [ -n "$2" ]; then bash "$SUBJ" "$2"; else bash "$SUBJ"; fi
  ) > "$1/out-$3.txt" 2>&1
  echo $?
}

build "$WORK/nodev" main
RC_NODEV="$(run_guard "$WORK/nodev" "" default)"
OUT_NODEV="$WORK/nodev/out-default.txt"
RC_ARGBASE="$(run_guard "$WORK/nodev" origin/main explicit)"
OUT_ARGBASE="$WORK/nodev/out-explicit.txt"
build "$WORK/withdev" develop
RC_WITHDEV="$(run_guard "$WORK/withdev" "" default)"
OUT_WITHDEV="$WORK/withdev/out-default.txt"

# CELL 1 (RED at the tip) - a demo mutation on a clone whose origin has NO
# develop must NOT read as clean: the guard exits 2 (1 means mutation detected).
if [ "$RC_NODEV" = "2" ]; then
  echo "PASS: an unresolvable default base exits 2 - refused, not read as clean"; PASS=$((PASS+1))
else
  echo "FAIL: an unresolvable default base exited $RC_NODEV, not 2 - a demo mutation on this tree read as clean: $(head -1 "$OUT_NODEV")"; FAIL=$((FAIL+1))
fi

# CELL 2 (RED at the tip) - and it says why, never "nothing to compare".
if grep -qF 'cannot be resolved' "$OUT_NODEV" && ! grep -qF 'nothing to compare' "$OUT_NODEV"; then
  echo "PASS: the guard names the unresolvable base and prints no nothing-to-compare line"; PASS=$((PASS+1))
else
  echo "FAIL: cannot-be-resolved present=$(grep -qF 'cannot be resolved' "$OUT_NODEV" && echo yes || echo NO), nothing-to-compare present=$(grep -qF 'nothing to compare' "$OUT_NODEV" && echo YES || echo no)"; FAIL=$((FAIL+1))
fi

# CELL 3 (GREEN CONTROL, tip AND after) - the SAME tree with an explicit base
# that resolves (origin/main as the argument) is a real demo mutation: blocked.
if [ "$RC_ARGBASE" = "1" ] && grep -qF 'DEMO MUTATION DETECTED' "$OUT_ARGBASE"; then
  echo "PASS: CONTROL the same tree with an explicit resolvable base is blocked with exit 1"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL explicit base origin/main exited $RC_ARGBASE (want 1), banner present=$(grep -qF 'DEMO MUTATION DETECTED' "$OUT_ARGBASE" && echo yes || echo NO)"; FAIL=$((FAIL+1))
fi

# CELL 4 (GREEN CONTROL, tip AND after) - when origin/develop exists the default
# path is untouched: a demo mutation off develop is still blocked with exit 1.
if [ "$RC_WITHDEV" = "1" ] && grep -qF 'DEMO MUTATION DETECTED' "$OUT_WITHDEV"; then
  echo "PASS: CONTROL with origin/develop present a demo mutation is still blocked with exit 1"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL with origin/develop present exited $RC_WITHDEV (want 1), banner present=$(grep -qF 'DEMO MUTATION DETECTED' "$OUT_WITHDEV" && echo yes || echo NO)"; FAIL=$((FAIL+1))
fi

# CELL 5 - the completeness guard. A suite that exits 0 having asserted nothing
# is a check that cannot fail, so a short count is itself a FAIL.
if [ $((PASS + FAIL)) -eq "$EXPECTED_CELLS" ]; then
  echo "PASS: all $EXPECTED_CELLS cells ran"; PASS=$((PASS+1))
else
  echo "FAIL: only $((PASS + FAIL)) of $EXPECTED_CELLS cells ran - a suite that asserts nothing is not a pass"; FAIL=$((FAIL+1))
fi

echo ""
echo "check_no_demo_mutation_missing_base: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ]
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `PASS: an unresolvable default base exits 2 - refused, not read as clean` - at the tip: exit 0 (`not 2 - a demo mutation on this tree read as clean`)
- `PASS: the guard names the unresolvable base and prints no nothing-to-compare line` - at the tip: `cannot-be-resolved present=NO, nothing-to-compare present=YES`
- `PASS: CONTROL the same tree with an explicit resolvable base is blocked with exit 1`
- `PASS: CONTROL with origin/develop present a demo mutation is still blocked with exit 1`
- `PASS: all 4 cells ran`

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/scripts/check-no-demo-mutation.sh` / `+++ b/Blockchain/Dev/scripts/check-no-demo-mutation.sh` (1 hunk, copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh` (one hunk, `@@ -0,0 +1,133 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 2bc5ccf63b8c40911afb568b03cace066238ffcf by the feed17 drafter in a `git clone --shared` scratchpad clone, 2026-09-22 19:49:00 AEST)
- `Blockchain/Dev/scripts/check-no-demo-mutation.sh` at the tip (144 lines, last changed by #1185 `2d49c4bdd`) carries every `-` and context line of the hunk above BYTE FOR BYTE at `:66-:70` (generated from `git show 2bc5ccf63:Blockchain/Dev/scripts/check-no-demo-mutation.sh` by the writer script, never typed); the product section applies STRICT (`git apply --check -p1` rc 0 in the clone). `exit 1` at `:144` is the mutation-detected code, which is why the refusal is `exit 2`.
- The fail-open REPRODUCED in-process at the untouched tip with this suite's own fixture (a bare origin holding `main` only; feature cut from `origin/main` touching `deployment/azure/migrate/init.sql`): the guard printed `[demo-guard] base origin/develop not found; nothing to compare` and exited 0 (`runs/2026-09-22_feed17-drafter-precheck/probe_tip_missingbase.out`); the SAME tree with `origin/main` passed as `$1` exits 1 with the banner (the control).
- The new suite `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh` is present (126 lines, #1185's) and is the local-bare-remote exemplar this suite copies; its four cells stay green after the hunk (every one of its fixtures has `origin/develop`).
- Every `+` line of the product hunk and every line of the suite is ASCII (non-ASCII 0, asserted by the writer); no backslash and no backtick on any `+` line (0 / 0, asserted). The FEED 8 ruling WAIVES the `"` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk) and B4/B5 (RED at the tip, GREEN after).
- One sibling suite in `scripts/__tests__` names `check-no-demo-mutation.sh`: the reference itself (B6 drives it; it stays green - measured on the golden).
- The guard is NOT wired into CI at the tip: `.github/workflows/ci.yml` has 0 mentions of `demo` (control: 6 `checkout` steps); `scripts/run-code-guards.sh:116` lists it under DEFERRED with a reason that still describes the pre-#1185 `origin/main` default (stale text; not this task). The fail-closed exit therefore changes no pipeline's verdict today.
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: `runs/2026-09-22_feed17-drafter-precheck/MISSINGBASE/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1033 on the Secuura board at 2026-09-22 19:49:00 AEST: board state read at build (the builder's own gate; `fetch_tickets.log`). #1185 is MERGED at this tip (`2d49c4bdd`), so the script's `:62` default is `origin/develop` here - this brief targets the merged tree, not 3bad652d1. The `scripts/` DIRECTORY was Seat C's lane in round 19 (now merged) - Wednesday rules the lane at queue time. Gate 19C called this "a design change: fail-closed" - the diff is HELD and GATED like every Ornith output and merges on nothing but a QA gate + a signed GO.
