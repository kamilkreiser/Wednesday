TASK: test_only_bash

The INPUT is a JSON object. `brief` is the whole brief (Wednesday's instructions, authoritative). The product code is
ALREADY CORRECT: do not change it. The defect is a MISSING or WEAK check in a BASH TEST SUITE (a `*.test.sh`). You add or
change checks in the suite only.

- `test_files` - the bash suite file(s) you may change, and the ONLY files your diff may touch. Their FULL current content is
  in `files[<path>]` (null = the file does not exist at the tip: create it with `--- /dev/null`).
- `product_files` - read-only context (the script under test, or files the suite reads). Content in `files[...]`. A diff that
  touches any of them is refused.
- `mode` - `plant` or `expect`:
  - `plant`: `red_cells` are substrings of check labels (the text after `ok`/`PASS`/`FAIL` on the suite's own output line). Each
    must (a) print an `ok`/`PASS` line on the code as it is, and (b) print the suite's own `FAIL` line, with the suite exiting
    non-zero, when the brief's `## Plant` mutation is applied. The checker applies the plant in a scratch clone; you never write it.
  - `expect`: `expect` lists texts that must be ABSENT from / PRESENT in the suite's printed output. They all fail on the suite
    as it is and all hold on the suite after your change. Copy the labels the brief names exactly.
- Follow the suite's own idiom: reuse its `check`/`ok`/`FAIL` helper and its fixtures; print one `ok`/`PASS` or `FAIL` line per
  check. Do not leave a check that asserts nothing the plant (or the defect) can change. A bash syntax error, an unbound
  variable or a `command not found` is not a failing check; it is refused.

Produce ONE unified diff, and nothing else.

1. Output exactly ONE fenced code block opened with ```diff and closed with ```. No prose before or after it.
2. `git apply -p1`-applicable from the repo root at the tip: `--- a/<path>` / `+++ b/<path>` headers, correct `@@`
   hunk counts AND start lines, context copied byte-for-byte from `files[<path>]`. The `-` side of every hunk sits at
   exactly the line its header names.
3. Touch EXACTLY the files in `test_files` (every one of them), nothing else. Do not delete or weaken an existing check, and do
   not change the label of one (a count inside a label may change when the brief says so).
4. Every `red_cells` name appears as a check label in the result.
5. Follow the brief's `## The test` text where it gives check bodies; copy it verbatim.
