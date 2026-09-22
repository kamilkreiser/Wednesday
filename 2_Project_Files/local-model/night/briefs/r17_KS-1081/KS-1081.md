# KS-1081 R17-NEITHERTEMPLATE ADD ONE CELL TO THE bootstrap-env canonical-template SUITE - a scratch tree carrying NEITHER `env.example` nor `.env.example` is refused by the pre-flight guard with its named message and rc 1 - gate 19C's NOT-PINNED row CANONENV-NEITHER on #1191 ("the No env template found exit 1 is unpinned") - Wednesday's task for Ornith, TEST_ONLY, **ONE existing bash suite, ONE pure-insertion hunk, no product file** (written 2026-09-22 20:02:11 AEST by the feed17 drafter)

File: `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh`
Tip: `2bc5ccf63b8c40911afb568b03cace066238ffcf`

Written from develop `2bc5ccf63b8c40911afb568b03cace066238ffcf` (`git ls-remote` against GitHub at boot, read verbs only; #1191 `225e63100` is MERGED at this tip). The suite at that tip is **90 lines** (last change `225e63100`, #1191), read whole; its full content is in `files[...]` of your input. The product it judges is `Blockchain/Dev/scripts/bootstrap-env.sh` (334 lines, last change `225e63100`, `set -e` at `:18`): the template resolution at `:36-:39` (canonical first, legacy fallback) and the pre-flight guard at **`:68-:71`** - `if [[ ! -f "$ENV_EXAMPLE" ]]; then` / `print_error "No env template found: neither ... nor ..."` / `exit 1` / `fi`. The suite builds a BOTH tree (`:31-:38`) and a LEGACY-only tree (`:40-:46`); no tree exercises the guard, so its named refusal is unpinned (gate 19C: CANONENV-MISSINGEXAMPLE is already cell 6; CANONENV-NEITHER is not).

## THE MODE - read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the suite above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `bootstrap-env.sh` or any other file: no product behaviour changes; ONE cell is ADDED (with the scratch tree it needs), between the tally's blank-line `echo ""` (`:88`) and the tally line (`:89`).

## What the change does (one paragraph)

The block builds a third scratch tree under the suite's own `$SCRATCH_ROOT` (`:29`, removed on EXIT by `:30`) with the script and `stack_env.sh` copied in and NO template of either name, runs the script exactly as `:37` and `:45` do (the same `env -u ...` line), records `NEITHER_RC`, and asserts rc 1 AND the guard's own wording `No env template found` in the log. Without the guard the script would still exit 1 - `set -e` on the failed `cp` at `:79` - but with `cp`'s error instead of a named refusal, which is what the message half of the cell pins. The block sits after `:88` (`echo ""`) so it stays one contiguous insertion between two non-blank lines; the cell's PASS/FAIL line therefore prints after the blank line and before the tally. Nothing else in the suite changes.

## The exact change - ONE hunk in the suite

A PURE INSERTION of 14 `+` lines between `:88` (`echo ""`, leading context) and `:89` (the tally `echo`, trailing context) - both unique in the file, both ASCII. Copy every line byte for byte. Every `+` line is ASCII only, carries NO backslash, NO backtick, no `printf`, no bash-4 idiom; `$SCRATCH_ROOT`, `$BOOTSTRAP`, `$ENV_SH`, `$HOME`, `$PATH`, `$NEITHER`, `$NEITHER_RC` are plain expansions the suite already uses. There is no blank line anywhere in the hunk.

```
@@ -88,2 +88,16 @@
 echo ""
+# KS-1081 (gate 19C CANONENV-NEITHER, #1191): a tree carrying NEITHER template must be
+# refused by the pre-flight guard (bootstrap-env.sh:68-71) with its named message and
+# rc 1 - not die later on a failed cp. Built and run here so the block stays contiguous.
+NEITHER="$SCRATCH_ROOT/neither/Blockchain/Dev"
+mkdir -p "$NEITHER/scripts"
+cp "$BOOTSTRAP" "$NEITHER/scripts/bootstrap-env.sh"
+cp "$ENV_SH" "$NEITHER/scripts/stack_env.sh"
+env -u SECUURA_STACK_SLOT -u STACK_SLOT -u POSTGRES_EXTERNAL_PORT -u REDIS_EXTERNAL_PORT HOME="$HOME" PATH="$PATH" bash "$NEITHER/scripts/bootstrap-env.sh" >"$NEITHER/bootstrap.log" 2>&1
+NEITHER_RC=$?
+if [[ "$NEITHER_RC" -eq 1 ]] && grep -qF 'No env template found' "$NEITHER/bootstrap.log"; then
+  echo "PASS: a tree carrying NEITHER template is refused by name (rc 1, No env template found)"; PASS=$((PASS+1))
+else
+  echo "FAIL: a tree carrying NEITHER template: rc=$NEITHER_RC, named refusal present=$(grep -qF 'No env template found' "$NEITHER/bootstrap.log" && echo yes || echo NO) (want rc 1 and the message)"; FAIL=$((FAIL+1))
+fi
 echo "bootstrap_env_canonical_template: $PASS passed, $FAIL failed"
```

Do NOT touch the BOTH or LEGACY trees (`:31-:46`), cells 1-6 (`:52-:86`), the tally (`:89`) or the exit (`:90`). Do NOT rename the cell: the checker names it by the literal prefix `a tree carrying NEITHER template`.

## Cells

- `neither` = `a tree carrying NEITHER template`
- `c1` = `every variable in env.example reached the generated .env`
- `c3` = `the script reports the canonical template by name`
- `c4` = `the script resolves the canonical template path under DEV_DIR`
- `c5` = `CONTROL bootstrap exits 0 and DATABASE_URL still carries the slot-1 port 6432`
- `c6` = `CONTROL a tree carrying only .env.example still bootstraps (the fallback)`

## Red cells

- a tree carrying NEITHER template (the ONE cell this diff adds - GREEN at the tip with the hunk applied, RED under GUARDGONE)

## Tampers

ONE tamper, a ONE-line edit of the product's pre-flight guard at `bootstrap-env.sh:68` (the `From` is the line at `:68` byte for byte; the builder locates a one-line tamper by `Line:`). The suite copies the script FROM `$BOOTSTRAP` (`:12`, `:33`, `:42`, and the new block), so the tampered script is what every tree runs. The checker plants it and restores the file by bytes (T8).

### GUARDGONE - the pre-flight guard never fires (`if false; then`): a tree with no template runs on to the failed `cp` at `:79` and dies under `set -e` with cp's error, not the named refusal - the new cell reds on its message half; every tree that HAS a template is unaffected
File: `Blockchain/Dev/scripts/bootstrap-env.sh`
Line: 68
From:
```
if [[ ! -f "$ENV_EXAMPLE" ]]; then
```
To:
```
if false; then
```
Reds: `neither`

## Controls

- `c1`
- `c3`
- `c4`
- `c5`
- `c6`

*(All are literal prefixes of the descriptions the suite prints - `c1` `:53`, `c3` `:65`, `c4` `:71`, `c5` `:77`, `c6` `:83`, `neither` the new block's `PASS:`/`FAIL:` lines; each prefix names exactly one cell. Cell 2 (`:59`/`:61`) is NOT declared: its PASS and FAIL lines share no prefix (`the canonical-only variable $CANON_ONLY ...` vs `$CANON_ONLY is declared ...`) - it stays green under the tamper regardless (the BOTH tree has both templates) and is simply not named.)*

## THE CHANGE - state it to yourself before you write a line

At the untouched tip the suite is `6 passed, 0 failed`, rc 0. With this hunk: `7 passed, 0 failed`, rc 0 - the new cell green (rc 1, message present). Under **GUARDGONE** with the hunk: the new cell red (`rc=1, named refusal present=NO`), every other cell green, `6 passed, 1 failed`, rc 1.

## Premises (measured by reading the tip)

- **Premise: the anchors.** `:88` (`echo ""`) and `:89` are non-blank ASCII and each occurs once in the suite; `:87` is blank and is NOT in the fence.
- **Premise: the From line.** `bootstrap-env.sh` at `2bc5ccf63`, line 68, byte for byte; `set -e` at `:18` is why the tamper cannot turn rc 1 into rc 0 (the `cp` at `:79` fails) - the cell's message half is the discriminating assertion.
- **Premise: the cell names.** `NEITHER template` occurs 0 times in the suite at the tip (control: `only .env.example` 2); no declared prefix is a prefix of another.
- **No backslash** in any `+` line (0, counted by the writer); **no backtick** (0); **no non-ASCII** (0); the suite after the hunk parses (the checker's T5 run).
- **Premise: the surface.** A shell suite that builds scratch trees under `mktemp -d` and removes them on EXIT; `openssl` is required by the suite's own pre-flight (`:20`); nothing outside `$TMPDIR` is written. Not an auth surface.

## Collision

Both files were changed by #1191, MERGED at this tip (`225e63100`); no held READY names either file. The `scripts/` directory was Seat C's round-19 lane (now merged) - Wednesday rules the lane at queue time.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh` / `+++ b/Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh`, then the ONE hunk above exactly as shown (`@@ -88,2 +88,16 @@`). Every `+` line is its OWN physical line (the INPUT JSON shows this brief's line breaks as the two characters backslash and n inside a JSON string - DECODE them; a `+` line that carries a backslash is a FAIL).

## Notes for the raise (not for the model)

- Test-only, zero product bytes, one new cell + its scratch tree. **Raise tier: TIER 2 (a scripts/__tests__ shell suite).** **Refs KS-1081** (gate 19C's CANONENV-NEITHER). Does not close it.
- Placement: the block sits after the tally's `echo ""` because every other insertion point in this suite borders a blank line, which the harness's modify-in-place fence refuses; the raiser may move the block up beside the LEGACY tree (`:46`) in the same PR - the cell text and the tamper do not change.
