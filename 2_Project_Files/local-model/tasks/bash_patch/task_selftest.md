# bash_patch SELF-TESTING — change ONE bash script that carries its own `--self-test`, exactly as the brief says

You are given `input.json`:
- `ticket` — `identifier`, `title`, and `description` = **Wednesday's brief**: what is wrong, the exact edits (line numbers,
  the line's text at the tip, and the whole diff), and the self-test checks to add.
- `product_file` — the ONE script you may change (path from the repo root). Its FULL current content is in `files[product_file]`.
  The script is BOTH the product and its own test suite: `self_testing.runner` runs it (e.g. `bash <path> --self-test`).
- `self_testing.test_hunks` — which hunk(s) of your diff (1-based, counting from the top) are the NEW self-test checks. The
  checker applies those hunk(s) ALONE and the self-test must exit `self_testing.red_rc`; it then applies every other hunk on
  top and the self-test must exit `self_testing.green_rc` with no FAIL line and no fewer PASS lines than before.
- `repo.tip` — the commit the contents are at.

Produce the change as ONE unified diff, and nothing else.

1. Output exactly ONE fenced code block, opened with ```diff and closed with ```. No prose before or after it.
2. The diff is `git apply -p1` applicable from the repo root at the tip: ONE `--- a/<path>` / `+++ b/<path>` header pair for
   `product_file`, then its hunks in FILE order, each `@@ -old,len +new,len @@` with correct counts AND a correct start
   line (the checker verifies the old side sits at exactly that line). Context lines are copied EXACTLY (byte for byte,
   leading space included) from `files[product_file]`. Copy every `-` line from the file; never retype it from memory.
3. The diff touches EXACTLY one file: `product_file`. No new file, no second file.
4. The edits are the brief's, line for line: every `-` line the brief names is removed, every `+` line the brief gives is
   added verbatim (do not paraphrase a comment, do not re-indent, do not add a trailing comment, keep non-ASCII characters
   and backslashes exactly). Nothing the brief does not name changes. The script must still parse (`bash -n`).
5. Keep the hunks in the brief's order; the test hunk(s) must sit at the ordinal(s) in `self_testing.test_hunks`.
