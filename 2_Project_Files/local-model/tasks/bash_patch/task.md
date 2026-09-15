# bash_patch — fix ONE bash script exactly as the brief says, and add ONE shell test suite that proves it

You are given `input.json`:
- `ticket` — `identifier`, `title`, and `description` = **Wednesday's brief**: what is wrong, the exact edits (line numbers and the
  line's text at the tip), and the test cells to write.
- `product_file` — the ONE script you may change (path from the repo root). Its FULL current content is in `files[product_file]`.
- `reference_test_file` — an EXISTING `*.test.sh` suite in the same directory as your new test. Its FULL content is in
  `files[reference_test_file]`. Copy its SHAPE: the `set -uo pipefail` line, the `PASS=0; FAIL=0` counters, the way it locates
  the script under test from `${BASH_SOURCE[0]}`, its `mktemp -d` + `trap` cleanup, its `expect`-style helper that prints
  `  FAIL: <name> (...)` and increments FAIL, and its last lines that print the totals and `exit 1` when FAIL is not 0.
- `suggested_test_file` — the path of the NEW test file you create (under `test_dir`, beside the reference).
- `repo.tip` — the commit the contents are at.

Produce the change as ONE unified diff, and nothing else.

1. Output exactly ONE fenced code block, opened with ```diff and closed with ```. No prose before or after it.
2. The diff is `git apply -p1` applicable from the repo root at the tip: `--- a/<path>` / `+++ b/<path>` headers for the
   script, `--- /dev/null` / `+++ b/<path>` for the new test; `@@ -old,len +new,len @@` hunks with correct counts; context
   lines copied EXACTLY (byte for byte, leading space included) from `files[product_file]`. A blank context line is a
   single space.
3. The diff touches EXACTLY two files: `product_file` and the new test at `suggested_test_file`. Nothing else.
4. The script edits are the brief's, line for line: every `-` line the brief names is removed, every `+` line the brief
   gives is added verbatim (do not paraphrase a comment, do not re-indent, do not add a trailing comment). Nothing the
   brief does not name changes. The script must still parse (`bash -n`).
5. The test suite is bash 3.2 (macOS): no `mapfile`, no `declare -A`, no `${var,,}`, no `timeout`. It never touches
   the repo's real files: every case builds a throwaway directory under `mktemp -d`, copies or points at the script as the
   brief says, runs it, and asserts on its exit code and output. Each cell's name starts with `🔴` when the brief says it
   is red at the tip, or `CONTROL` when it must pass on both trees. A `🔴` cell FAILS at the untouched tip and PASSES after
   your script edit; a CONTROL cell passes on both. Write exactly the cells the brief lists — no more, no fewer.
