TASK: test_only_input

The INPUT is a JSON object. `brief` is the whole brief (Wednesday's instructions, authoritative). The product code is
ALREADY CORRECT: do not change it. The defect is a MISSING or WEAK assertion in the test file(s). You add or change
test cells only.

- `test_files` — the test file(s) you may change, and the ONLY files your diff may touch. Their FULL current content is
  in `files[<path>]` (null = the file does not exist at the tip: create it with `--- /dev/null`).
- `product_files` — the code under test (content in `files[...]`). READ ONLY. A diff that touches it is refused.
- `red_cells` — substrings of the names of the cells (`it(...)` / `test(...)` titles; `describe` names count toward the
  full name) that must exist after your change. Each must (a) PASS on the code as it is, and (b) FAIL BY AN ASSERTION
  (`expect(...)` / an assertion error, not a crash and not a load error) when the brief's `## Plant` mutation is applied.
  The plant is applied by the checker in a scratch copy only; you never write it.
- `repo.test_runner` — vitest | jest | node-tap. Use that runner's idiom and the file's own existing import/mock shape.

Produce ONE unified diff, and nothing else.

1. Output exactly ONE fenced code block opened with ```diff and closed with ```. No prose before or after it.
2. `git apply -p1`-applicable from the repo root at the tip: `--- a/<path>` / `+++ b/<path>` headers, correct `@@`
   hunk counts AND start lines, context copied byte-for-byte from `files[<path>]`. The `-` side of every hunk sits at
   exactly the line its header names.
3. Touch EXACTLY the files in `test_files` (every one of them), nothing else. Do not delete or weaken an existing cell.
4. Every `red_cells` name appears as a cell in the result. A cell that asserts nothing the plant can change is refused:
   it stays green with the plant applied.
5. Follow the brief's `## The test` text where it gives cell bodies; copy it verbatim.
