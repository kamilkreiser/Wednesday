# doc_patch — edit ONE documentation file exactly as the brief says

You are given `input.json`:
- `ticket` — `identifier`, `title`, and `description` = **Wednesday's brief**: what to change, the exact lines, the exact text.
- `product_file` — the ONE file you may change (path from the repo root). Its FULL current content is in `files[product_file]`.
- `repo.tip` — the commit the content is at.

Produce the change as ONE unified diff, and nothing else.

1. Output exactly ONE fenced code block, opened with ```diff and closed with ```. No prose before or after it.
2. The diff is `git apply -p1` applicable from the repo root at the tip: `--- a/<path>` / `+++ b/<path>` headers,
   `@@ -old,len +new,len @@` hunks with correct counts, context lines copied EXACTLY (byte for byte, leading
   space included) from `files[product_file]` — the line above and the line below every edit come from the
   file, never from memory. A blank context line is a single space.
3. The diff touches EXACTLY one file: `product_file`. Every edit the brief names appears; nothing the brief does
   not name changes — no reflowing of neighbouring lines, no re-wrapping, no "improvements".
4. Prose is written in the file's own register (its bullets, its `code` spans, its dates and ticket ids as the
   brief gives them). Where the brief gives text to copy, copy it verbatim.
