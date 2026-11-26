## BLUF
A policy document with a long company, product or policy name lost its `manifest <hash>` footer line from every page of the PDF: the first footer line had no length limit, so it took more rendered lines than the footer band holds and the hash line, the last one, was dropped. The first footer line is now held to what fits above the hash line, with the fitting the change report already uses. Customer PDF and DOCX footers change only for a first line that does not fit; for every name that fits, the footer text and the document bytes are unchanged. No content release, nothing deploys.

## What changes (three files, 160 lines added, 2 removed)
- `packages/renderers/src/change-report.ts`: `footerFirstLine` is exported (one word). Its behaviour is unchanged; the change report's own tests pass as before.
- `packages/renderers/src/policy-document.ts`: imports it and wraps the first line of the policy footer in it. The hash line is never clipped. Title, subject, cover and body keep the full name.
- `packages/renderers/test/policy-footer-budget.test.ts` (new, five tests): every page of the policy PDF keeps the hash line inside the page for a 250-character name with a 200-character company, released and draft, in three shapes; the PDF and DOCX footer ends in exactly the hash line, with the first line within 122 code points and two rendered lines; the DOCX footer keeps the hash line; a short name gives the old footer text byte for byte; a first line exactly at the budget is not clipped and one character over is clipped with three dots.
- Not changed: the PDF writer (`document-pdf.ts`), any content or release file, any config.

## Choices
The shape of the fix (reuse the change report's fitting at the footer text, not in the PDF writer), the export in place, the tests and the mutants are the coordinator's choices. The clipped line ends in three ASCII dots, the same as the change report's footer.

## Test results (CI image, no network)
- New file over the unfixed product: 3 failed, 2 passed (the three footer tests red, the two control tests green). With the fix: 5 passed.
- Mutants of the fix: footer not fitted, budget moved to 123, fitting returns every line whole: each turns the new file red; the unmutated head is green.
- Renderers project: 296 passed, 1 skipped (base 291 passed, 1 skipped); test names lost 0, the 5 added all in the new file. Format check, typecheck, prettier and eslint on the three files pass.
- A seeded probe of 192 policy PDFs with long or unusual names (wide letters, line breaks, tabs, non-breaking spaces): the hash line was missing in 96 at base and in 0 with the fix. Names in CJK, combining marks, emoji and right-to-left scripts keep the hash line too.
- A short name: the policy PDF and DOCX, released and draft, are byte for byte the same before and after.
- Both `CONTENT_HASH` files are byte-identical to main. No secret found in the diff or the message.
- Hosted checks: read at landing.

## Limits
- The DOCX footer is clipped the same way although Word lays out its footer by its own rules; Word's own layout was not measured.
- Line fitting uses the bundled body font's widths; a brand with another body font was not measured.
- Clipping is by code point: a cut can drop a combining mark or split an emoji sequence just before the dots.
- A name that is one unbroken run of wide letters is clipped to fewer than 122 code points, and the page label then wraps over the footer's three lines (it did not print at all before).
- Policy PDFs with a four-digit page count were not rendered.

## Status
Product fix in the renderer; not a content release. No release, no deploy.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
