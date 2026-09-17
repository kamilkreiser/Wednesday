# comment_patch — change ONLY comment text in ONE source file, exactly as the brief says

You are given `input.json`:
- `ticket` — `identifier`, `title`, and `description` = **Wednesday's brief**: why, the lines, and the exact change.
- `product_file` — the ONE file you may change (path from the repo root). Its FULL current content is in `files[product_file]`.
- `comment.ranges` — the only line ranges (`[first, last]`, numbered from 1 in `files[product_file]`) your diff may change.
- `comment.must_remove` — the lines that must go, each with its line number. `comment.expected_plus` — the lines that must appear.
- `repo.tip` — the commit the content is at.

Produce the change as ONE unified diff, and nothing else.

1. Output exactly ONE fenced code block, opened with ```diff and closed with ```. No prose before or after it.
2. The diff touches EXACTLY one file, `product_file`: headers `--- a/<product_file>` and `+++ b/<product_file>`, the path
   written exactly as `product_file` gives it (it starts `Blockchain/Dev/`). `@@ -old,len +new,len @@` hunks with correct counts.
3. Change ONLY comment text, and only on the lines `comment.ranges` names. Never change code, a string or template literal,
   a test title (`it('…')`, `describe('…')`), an identifier, an import, or a JSX text. A changed test title is a code change
   and is refused. The checker compares every code token of the file before and after; one changed token fails the diff.
4. Every `-` line is the file's line at its number, copied byte for byte (leading spaces included). Every `+` line is the
   brief's line copied byte for byte, indentation included — do not re-wrap, re-word or "improve" it.
5. Context lines are the file's real neighbours, copied byte for byte from `files[product_file]` — including any non-ASCII
   character already in them (an em dash `—`, an arrow `→`): copy it, never retype it as ASCII. A blank context line is a
   single space. When the brief says a line stays, it is a context line (leading space), never a `-` line.
6. Do not add, remove or edit directive comments: `@ts-expect-error`, `@ts-ignore`, `@ts-nocheck`, `eslint-…`,
   `/// <reference …>`, `istanbul ignore`, `c8 ignore`, `@jest-environment` / `@vitest-environment`, `prettier-ignore`.
7. The brief's `## The exact change` fence IS the intended diff. Reproduce it: same `-` lines, same `+` lines, same order.
