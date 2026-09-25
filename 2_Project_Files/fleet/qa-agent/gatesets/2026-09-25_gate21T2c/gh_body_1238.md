#1238 KS-1158 R5a: re-point the ks1059 header citations and fix the two code quotes that drifted
head 0f3ffbb0947a82b7ec1c2866fd1a82ff4c94b2c1

## BLUF

Comment-only, one file: the header of
services/originate/src/__tests__/ks1059-sim-leg-must-not-resurrect-a-terminal-document.test.ts.

R3 landed with #1153 (`358bfbbcc`) and R5b with #1172 (`2f60bce16`). R5a is the remaining record: the
header still described `anchorStateSync.ts` as it was at `d4cf7e3cf`.

Two things drifted, not one. The line numbers moved - and the CODE they quote changed, because the
`!bc.txHash` term MOVED OUT of the `inFlight` definition and INTO the sim leg:
    at d4cf7e3cf  :284  const inFlight = !bc.txHash && bc.status !== 'anchor_failed' && ...
                  :325  if (inFlight && simFields.simulated) {
    at this base  :329  const inFlight = bc.status !== 'anchor_failed' && bc.status !== 'confirmed';
                  :378  if (inFlight && !bc.txHash && simFields.simulated) {
So the header's argument - "`inFlight` used to imply `!bc.txHash`, so the two halves overlapped" - had
become wrong as PROSE, not merely mis-numbered. Moving only the numbers would have left a false sentence
sitting at the right line. Both quotes are re-quoted from this base and the prose now says the term moved.

A record correction the ticket does not carry: FOUR of the header's five citations were already wrong at
`d4cf7e3cf`, the revision the header itself measured. `:283` is `if (bc.simulated) return document;` (the
inFlight line is `:284`), `:285` is the `failed` assignment (the guard is `:286`), `:296` is a blank line
(the heal-forward branch is `:297`), and `:~315` is marked approximate for what sits at `:313`. Only
`:325` was exact. Three of them are off by exactly one in the same direction, which is the shape of a list
counted off a 0-indexed listing rather than of separate typos. So this was never simply "the code moved
and the header went stale" - it was partly wrong the day it was written, and the code moving on top of it
hid that.

`d4cf7e3cf` is KEPT. It dates a past measurement ("On develop at d4cf7e3cf, with `inFlight &&` deleted...")
and is still true of that revision - the same reason KS-979's past-tense line was left alone.

Test evidence
- Touched: one test file's header comment. No executable byte: every changed line is a `*`-prefixed
  docblock line.
- Ran: originate jest --runInBand 74 suites / 863 tests, rc 0 - identical to the bare serial baseline.
  tsc --noEmit rc 0. packages/shared vitest 46 files / 918 tests rc 0 on a re-run; the first run returned
  ONE timeout (`crypto-agility.guard` at 5053 ms against the 5000 ms default) and zero assertion failures
  - the KS-1155 load class. Both runs reported.
- Residual check after the edit: the strings `:283`, `:285`, `:296`, `:~315` and `anchorStateSync.ts:325`
  each read 0 occurrences in the file; `d4cf7e3cf` still reads 2.
- NOT run: legs 3, 4, 8 (local stack not up); no product surface. Not a claim that the gate is green.
  Integration config not run. No image rebuilt.
- Migrations + config: none.


Refs KS-1158

🤖 Generated with [Claude Code](https://claude.com/claude-code)

