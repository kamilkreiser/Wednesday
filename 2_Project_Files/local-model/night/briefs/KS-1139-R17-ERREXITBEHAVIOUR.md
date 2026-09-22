# KS-1139 R17-ERREXITBEHAVIOUR ADD ONE BEHAVIOURAL CELL TO THE validate-lint errexit SUITE - cell 4: `run_check`, extracted from the subject and run under `bash -e` with both counters at 0, survives to the second check (`survived=2`) - gate 19C's NOT-PINNED row ERREXIT-ZEROCOUNT on #1192 ("the pin is static-only") - Wednesday's task for Ornith, TEST_ONLY, **ONE existing bash suite, ONE pure-insertion hunk, no product file** (written 2026-09-22 19:55:50 AEST by the feed17 drafter)

File: `Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh`
Tip: `2bc5ccf63b8c40911afb568b03cace066238ffcf`

Written from develop `2bc5ccf63b8c40911afb568b03cace066238ffcf` (`git ls-remote` against GitHub at boot, read verbs only; #1192 `4ff8247fe` is MERGED at this tip). The suite at that tip is **81 lines** (last change `4ff8247fe`, #1192), read whole; its full content is in `files[...]` of your input. The product it judges is `systemTest/schemathesis/validate-lint.sh` (75 lines, last change `4ff8247fe`): `run_check()` at `:26-:40` advances `PASS_COUNT` at **`:33`** and `FAIL_COUNT` at **`:38`** by the assignment form `X=$((X + 1))`; before #1192 they were bare `((X++))`, which exits 1 when the counter is 0, and the script runs under `set -e` (`:6`). Gate 19C MEASURED on /bin/bash 3.2.57 that the pre-#1192 script DIES after its first PASS under `set -e` (the suite header's "bash 3.2 does not" at `:5-:6` is refuted on this box) - and that the suite pins the fix STATICALLY only (cells 1-2 grep the source). This brief adds the behavioural cell the gate proposed.

## THE MODE - read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the suite above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `validate-lint.sh` or any other file: no product behaviour changes; ONE cell (cell 4) is ADDED; its block bumps `TOTAL_CELLS` by one at runtime so the suite's own completeness guard (`:76-:79`) still adds up (the constant at `:12` is NOT edited - see the raise note).

## What the change does (one paragraph)

Cells 1-2 (`:37-:61`) grep the subject's SOURCE for the bare `((X++))` idiom and for the two assignment lines; cell 3 is `bash -n`. None of them RUNS `run_check`. Cell 4 extracts `run_check()` from the subject with `sed -n "/^run_check()/,/^}/p"`, `eval`s it inside a fresh `bash -e` with `PASS_COUNT=0` and `FAIL_COUNT=0`, calls it twice with `true` as the command, and prints `survived=$PASS_COUNT`. On the fixed script this prints `survived=2`. If either counter line goes back to `((PASS_COUNT++))`, the first call exits 1 inside `run_check` at counter 0, `-e` kills the shell, nothing is printed and the cell reads `got '<nothing>'`. The block bumps `TOTAL_CELLS` by one (`TOTAL_CELLS=$((TOTAL_CELLS + 1))`) so `:76` still equals `pass + fail` and the tally prints `of 4 cells`. Nothing else in the suite changes; `:12` stays `TOTAL_CELLS=3`.

## The exact change - ONE hunk in the suite

A PURE INSERTION of 13 `+` lines between `:63` (the rule line that opens the CONTROL CELL 3 comment block; leading context) and `:64` (`# CONTROL CELL 3 - The subject parses cleanly ...`; trailing context) - so cell 4's block sits between cell 2 and cell 3, with its own closing rule line so cell 3's comment block keeps an opener. Copy every line byte for byte. Every `+` line is ASCII only, carries NO backslash, NO backtick, no `printf`, no bash-4 idiom; `$SUBJ`, `$PASS_COUNT`, `$survived` are plain expansions. There is no blank line anywhere in the hunk.

```
@@ -63,2 +63,15 @@
 # ---------------------------------------------------------------------------
+# CELL 4 - KS-1139 (gate 19C ERREXIT-ZEROCOUNT, #1192): cells 1-2 pin the fix
+# STATICALLY. This one RUNS it: run_check is extracted from the subject and run
+# under bash -e with both counters at 0; a bare ((PASS_COUNT++)) at 0 exits 1
+# and errexit kills the shell before the second check (measured on /bin/bash
+# 3.2.57 at the pre-#1192 script: rc 1, no survived line). Fixed: survived=2.
+TOTAL_CELLS=$((TOTAL_CELLS + 1))
+survived="$(bash -e -c 'eval "$(sed -n "/^run_check()/,/^}/p" "$1")"; PASS_COUNT=0; FAIL_COUNT=0; run_check a true >/dev/null; run_check b true >/dev/null; echo "survived=$PASS_COUNT"' _ "$SUBJ" 2>/dev/null | tail -1 || true)"
+if [ "$survived" = "survived=2" ]; then
+  ok "run_check survives bash -e from PASS_COUNT=0 to the second check (survived=2)"
+else
+  bad "run_check survives bash -e from PASS_COUNT=0 to the second check (survived=2)" "got '${survived:-<nothing>}' - errexit killed the extracted run_check at the first counter"
+fi
+# ---------------------------------------------------------------------------
 # CONTROL CELL 3 - The subject parses cleanly under any bash version we run this
```

Do NOT touch `:12` (`TOTAL_CELLS=3` stays), cells 1-3, the `SUBJECT` line, the tally at `:74`, or the completeness guard at `:76-:79`. Do NOT rename the cell: the checker names it by the literal prefix `run_check survives bash -e from PASS_COUNT=0 to the second check`.

## Cells

- `c1` = `validate-lint.sh has NO bare arithmetic-command post-increment/decrement`
- `c2` = `both counters advance by assignment`
- `c3` = `validate-lint.sh parses (bash -n)`
- `c4` = `run_check survives bash -e from PASS_COUNT=0 to the second check`

## Red cells

- run_check survives bash -e from PASS_COUNT=0 to the second check (the ONE cell this diff adds - GREEN at the tip with the hunks applied, RED under PASSPLUSPLUS; green under FAILPLUSPLUS, which never reaches the fail branch)

## Tampers

Both tampers are ONE-line edits of the product's counters in `run_check` (`validate-lint.sh:33` and `:38`; each `From` occurs EXACTLY ONCE in the file as a whole line). The suite reads the subject FROM `$SUBJ` (`:20`), so the tampered script is what every cell sees. The checker plants each and restores the file by bytes (T8).

### PASSPLUSPLUS - the PASS counter goes back to the bare arithmetic command (#1192 reverted on one line): cells 1 and 2 red statically, cell 4 red behaviourally (errexit kills run_check at PASS_COUNT=0)
File: `systemTest/schemathesis/validate-lint.sh`
Line: 33
From:
```
        PASS_COUNT=$((PASS_COUNT + 1))
```
To:
```
        ((PASS_COUNT++))
```
Reds: `c1`, `c2`, `c4`

### FAILPLUSPLUS - the FAIL counter goes back to the bare arithmetic command: cells 1 and 2 red statically; cell 4 stays GREEN because both calls pass and the fail branch never runs - the cell is specific to the counter that fires
File: `systemTest/schemathesis/validate-lint.sh`
Line: 38
From:
```
        FAIL_COUNT=$((FAIL_COUNT + 1))
```
To:
```
        ((FAIL_COUNT++))
```
Reds: `c1`, `c2`

## Controls

- `c3`

*(All are literal prefixes of the descriptions the suite prints - `c1` `:45`/`:47`, `c2` `:58`/`:60`, `c3` `:69`/`:71`, `c4` the `ok`/`bad` lines of the new cell; each prefix names exactly one cell. `c3` (`bash -n`) is green under both tampers: `((X++))` parses.)*

## THE CHANGE - state it to yourself before you write a line

At the untouched tip the suite is `3 passed, 0 failed (of 3 cells)`, rc 0. With this hunk: `4 passed, 0 failed (of 4 cells)`, rc 0 - cell 4 green (`survived=2`). Under **PASSPLUSPLUS** with the hunk: cells 1, 2 and 4 red (`got '<nothing>'`), cell 3 green, `1 passed, 3 failed`, rc 1. Under **FAILPLUSPLUS**: cells 1 and 2 red, cells 3 and 4 green, `2 passed, 2 failed`, rc 1.

## Premises (measured by reading the tip)

- **Premise: the anchors.** `:64` is non-blank ASCII and occurs once in the suite; `:63` is the rule line `# ---...` (occurs 6 times in the file - hunk 2 is anchored by its header line number, and strict `git apply` reads the header). `:62` is blank and is NOT in any fence.
- **Premise: the From lines.** `validate-lint.sh` at `2bc5ccf63`, lines 33 and 38, byte for byte (8 leading spaces), each occurs once as a whole line.
- **Premise: the cell names.** `run_check survives` occurs 0 times in the suite at the tip (control: `both counters advance` 2); no declared prefix is a prefix of another.
- **No backslash** in any `+` line (0, counted by the writer); **no backtick** (0); **no non-ASCII** (0); the suite after the hunk parses (`bash -n` rc 0 - the checker's T5 run).
- **Premise: the surface.** A shell suite that reads one script and runs an extracted function under a throwaway `bash -e`; nothing is written anywhere. Not an auth surface.

## Collision

`Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh` and `systemTest/schemathesis/validate-lint.sh` were both ADDED/CHANGED by #1192, which is MERGED at this tip (`4ff8247fe`); no held READY names either file. The `scripts/` directory was Seat C's round-19 lane (now merged) - Wednesday rules the lane at queue time.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh` / `+++ b/Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh`, then the ONE hunk above exactly as shown (`@@ -63,2 +63,15 @@`). Every `+` line is its OWN physical line (the INPUT JSON shows this brief's line breaks as the two characters backslash and n inside a JSON string - DECODE them; a `+` line that carries a backslash is a FAIL).

## Notes for the raise (not for the model)

- Test-only, zero product bytes, one new cell. **`TOTAL_CELLS` at `:12` is bumped at RUNTIME inside the cell block, not edited in place:** the constant's only neighbours are `:11` and the blank `:13`, the harness refuses a blank context line in a modify-in-place fence (builder rule 1, 2026-09-18), and `git apply` refuses a one-sided-context hunk that is not at EOF (measured: `probe_blankctx.log`). The raiser may fold `TOTAL_CELLS=4` into `:12` and drop the runtime line in the same PR. **Raise tier: TIER 2 (a scripts/__tests__ shell suite; systemTest tooling subject).** **Refs KS-1139** (gate 19C's ERREXIT-ZEROCOUNT). Does not close it.
- Gate 19C measured bash >= 4.1 NOT at all (no interpreter on the box); cell 4 is graded under whatever `bash` is first on PATH (/bin/bash 3.2.57 here), where the pre-#1192 script also died - the premise the suite header states (`:5-:6`) is wrong on this box either way, a comment for the raiser.
