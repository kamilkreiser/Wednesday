TASK: doc_only

The INPUT is a JSON object. `brief` is the whole brief (authoritative). You edit documentation and code COMMENTS only.

- `doc_files` — the files you may change, and the ONLY files your diff may touch. FULL current content in
  `files[<path>]` (null = does not exist at the tip: create it with `--- /dev/null`).
- `expect` — checks run on your result: every `absent` text must be gone from the files it names, every `present` text
  must be there. They are applied to the file text exactly as written.
- In a code file (ts/js/sh/py/yml) you may change ONLY whole-line comments (`//`, `/* ... */`, `#`). Any changed line
  that is not entirely comment is refused, as are blank-line edits outside a block comment and trailing comments on a
  code line.

Produce ONE unified diff, and nothing else.

1. Output exactly ONE fenced code block opened with ```diff and closed with ```. No prose before or after it.
2. `git apply -p1`-applicable from the repo root at the tip: `--- a/<path>` / `+++ b/<path>` headers, correct `@@`
   hunk counts AND start lines, context copied byte-for-byte from `files[<path>]`.
3. Touch EXACTLY the files in `doc_files` (every one of them), nothing else. Every edit the brief names appears; nothing
   it does not name changes — no reflowing or re-wrapping of neighbouring lines.
4. Where the brief gives text to copy, copy it verbatim; keep the file's own register (bullets, `code` spans, dates, ids).
