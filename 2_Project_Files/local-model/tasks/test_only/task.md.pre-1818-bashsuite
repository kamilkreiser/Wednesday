TASK: test_only

The INPUT is a JSON object describing ONE ticket whose fix is TESTS ONLY: the product code is already right at the
tip, and the ticket asks for test cells that PIN that behaviour, so that a later change to the code goes red.

- `ticket.description` — Wednesday's brief. It names the ONE test file, gives the exact lines to add (a fenced block
  under `## The exact change`), and lists the TAMPERS that will grade your cells: each tamper replaces one line of
  product code, and the brief says exactly which cells must fail under it (`Reds:`) and which must stay green
  (`## Controls`).
- `test_file` — the ONE file your diff touches (path from the repository root). When `test_mode` is `modify`, its FULL
  current content is in `files[test_file]`: you MODIFY it in place. When `test_mode` is `new`, you create it.
- `repo.test_runner` — vitest or jest. Your cells run under it. Do not change the file's imports or its runner idiom.
- `tampers`, `controls`, `expected_plus` — the same facts as the brief, as data. You never change a tamper's file.

Produce the change as ONE unified diff, and nothing else.

1. Output exactly ONE fenced code block, opened with ```diff and closed with ```. No prose before it, none after it,
   no second block.
2. The diff touches EXACTLY ONE file: `test_file`. Never a product file, never a config, never a second test file.
   A tamper's file is the code the cells PIN — you read about it, you never edit it.
3. The diff is `git apply -p1` applicable from the repository root at the tip, STRICTLY:
   - `modify`: `--- a/<test_file>` then `+++ b/<test_file>` (the SAME path on both lines), then the brief's `@@` hunk(s)
     with the header exactly as the brief prints it.
   - `new`: `--- /dev/null` then `+++ b/<test_file>`, ONE hunk `@@ -0,0 +1,N @@` where N is the number of `+` lines.
   - A context line is ONE space followed by the file's line UNCHANGED, copied from `files[test_file]` byte for byte,
     indentation included. Never re-indent a context line, never drop one, never add one the brief does not show.
4. Copy the brief's lines BYTE FOR BYTE: every `+` line of the brief's fence is a `+` line of your diff with the same
   leading spaces and the same characters (backticks, quotes, `${...}`, commas). Do not paraphrase a comment, do not
   add a trailing comment, do not escape a character (`\u` escapes, `\'`, `\"` are all wrong). Remove only the `-`
   lines the brief removes. Add no line the brief does not add; never re-add a line that is already in the file.
5. What the cells must do (the checker measures every one of these):
   - at the UNTOUCHED tip, EVERY cell of the file passes — the new cells pin what the code ALREADY does;
   - under each tamper, EXACTLY the cells the brief lists under `Reds:` fail, by an assertion — no more, no fewer;
   - every `## Controls` cell passes under every tamper.
   If the brief's fence already achieves this (it was measured), your job is only to reproduce it exactly.

Output the ```diff block now.
