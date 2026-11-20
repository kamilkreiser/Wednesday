# FOR RECORDS: the logging lane (WP1.10), delta check B1814 of one commit, head afc4e19 on main 7bf3752

Only what THIS round adds. Everything else stands as the second check's `2026-11-20_B1804_verify/FOR-RECORDS.md` wrote it
(the master-list items, the cost numbers, the scanner's open points, the missing controls, the process notes). The gate wrote
none of this anywhere: no ticket, no backlog line, no runbook line. State: **GO WITH FINDINGS; nothing blocks; the hosted code
scan has not run and is the authority.**

## 1. Ticket state (changing a ticket is the coordinator's)

- `OXPD2-15` ([WP1.10] Logging deny-list): the third commit exists and is checked (`afc4e1946458ef26c99fa917a5c32acc32f70578`:
  two lines of one test file). The lane lands when the pull request's checks and its code scan are green. After the merge the
  ticket still stays open for the scan of logs from a real sign-in (exit test E1.8), which needs a printer.
- Replaces the second bullet of section 1 of the second check's file ("the fix of finding 1 ... the product owner's card"): done.
- Still owed, unchanged: wire the host to the library; one README pass after the wave.

## 2. The local C# scan: how to read it (for the gate standard and the kits)

- Measured at this head: 53 calls on the logger in the three test files have no resolved target in the local database
  (`Information` 42, `ForContext` 8, `Verbose`, `Warning`, `Error` 1 each), although the extractor reports 0 unresolved
  references. Their arguments are therefore not counted locally as places a value is written to. The hosted analysis may
  resolve them. So a local "0 results" does not by itself prove "0 hosted".
- What does carry: the scanner's own list of sources. The query `/private/tmp/b1814-gate/ql/sources.ql` (16 lines; it selects
  every `SensitiveExpr` of the library's own class with its line and type) printed 19 rows at the head before and 17 at this
  head. A source that returns nothing, or whose value nothing reads, cannot reach any sink, resolved or not. **Rule for a gate
  or a kit that scans C# locally: print that list; every source whose value is read by something is a risk, whatever the
  result count says.**
- The correction of the gate standard from the second check stands as written (the launcher of the C# extractor cannot run on
  this machine; its managed program can).

## 3. The rule for the kits of the lanes that log (replaces the last bullet of section 6 of the second check's file)

- **CodeQL, C#, test code included: no method call that has an argument with a CONSTANT VALUE holding `password` or `passwd`
  (also `account...id`, `account...key`, `licen[cs]e...key`, `voucher...code`, `trusted`), when the call's RESULT is read by
  anything that can reach a logger, a file write or a trace call.** Measured this round, each a widening of the earlier
  wording:
  - a NAMED constant counts as well as a literal: its value is what is read (`DenyListTests.cs:336` is a source by its
    argument `Synthetic.Class6Value`); a search for quoted text does not see it;
  - an entry of a collection initialiser (`{ { "Password", s } }`) is a call for the scanner (`KeyValueShapeTests.cs:78`);
  - a constant joined to a variable is NOT a constant value (`KeyValueShapeTests.cs:95`); an indexer, a constructor, an object
    or property initialiser is not a method call;
  - a variable, parameter or field NAMED with one of the words, read anywhere on the way to a logger, is a source too (0 such
    at this head).
- The safe word used here: `Passphrase` (a listed name of the class `password`; the scanner's word list does not hold it).
- The drafter's sibling search (`siblings.py`) lists 16 calls at this head; the scanner's class 17: it misses lines 336 and 78
  above and lists line 95. Later kits use the query.

## 4. `KeyValueShapeTests.cs:95` (maker 20): not a risk as written, one edit away from one

`JsonDocument.Parse("{\"Password\":\"" + s + ...)`: no constant value, so no source. The gate's probe (a scratch copy with the
argument made one whole constant) gives 1 result: the same rule at line 126, path 95, 96, 125, 126. Whoever next edits that
maker keeps the value joined in, or uses another key word. Not changed in this round, by the round's rule.

## 5. Process

- The wave's lock was waited for twice by this gate (10 and 13 tries of 5 seconds): build seats now share it in earnest.
  40 jobs, highest load at a start 6.5, 0 processes of the gate alive at the end.
- The commit message of the third commit says "the two rows"; the two makers are four test rows (each with and without `@`).
  It is not false and it does not reach `main`: the squash uses `squash-subject.txt` and `squash-body.txt`. It stays readable
  on the lane branch for as long as that branch is on the origin.
- `landing.txt` of this folder replaces the one of the second check's folder; the four texts are byte-equal copies.

## 6. What was not tested (carry forward, added to section 8 of the second check's file)

The hosted code-scanning check (no pull request exists); Python again; the 62 other C# rules one by one (run: 0 results at both
trees); whether the hosted analysis resolves the 53 logger calls.
