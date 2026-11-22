## What changes

Four files. One stylesheet rule (layout only), one end-to-end spec, one name in the Playwright config, and the no-price test file. Nothing is deployed. No word of any document, no figure and no priced-document byte changes.

**MPSCALC-427** (a long part code in the stream cards of the unpriced full proposal)
- `web/src/proposal/proposal.css` (+1 -1): `.pd-card .pd-bullets li` gains `overflow-wrap: anywhere;`. Before, a part code with no break in it made the first stream card's column wider than the other, so the other column was squeezed and the page count went up. `break-word` does not fix this, because the grid's `1fr` columns still keep the longest unbreakable word as their minimum. `anywhere` does.
- `web/e2e/proposal-long-code.spec.ts` (new, 78 lines) and `web/playwright.config.ts` (+1 -1, one name in `STUB_OFF_ONLY`): the spec prints the unpriced full proposal of seven synthetic packages in Chrome twice, once with a short first code and once with a 60-character code that has no break. It then checks the page count (read from the PDF's own page objects, not with `pdftotext`), the layout overflow and the widths of the two card columns of the first row. It runs in the stub-off step only.
- Real catalogue part codes were measured before the build, by a program that prints only lengths: 1878 values, 6 to 8 characters each.

**MPSCALC-428** (`web/src/proposal/unpriced.test.tsx`, tests only, +91 -18)
- The places a part code can start are decided on the text before any strip, in one pass, so there is no cascade between two lines.
- U+0001 is removed from text nodes and attribute values before the scan writes its own marks.
- The header's first limit now says so.
- Six cells are added: N1 (cascade) and its control, N2 (U+0001 in a description), N3 (in a narrative field), N4 (in an attribute value), and N5 (a figure split across two text nodes, with no code involved). The file goes from 88 cells to 94.

## Who decides

Each ticket's own text says it changes no word and no priced document. MPSCALC-427 calls itself "a style change with its own independent review". Every design choice here is the coordinator's, not the product owner's: the `anywhere` value, a committed spec instead of a written method, the seven-package fixture, the six cells, and one commit. Nothing goes to the hosted site with this pull request. The stylesheet is part of a document customers receive, so the next MPS hosted deploy card must name this change.

## Checked

- **Independent gate (tier G1).** It re-ran everything in its own copies of the head, the base and the merge with current main.
- **Unit tests.** The test file passes 94 of 94. The whole web run has 149 files: 1740 passed at the head and 1742 on the merge, 0 failed. `eslint .` and `tsc -b` both pass.
- **End-to-end.** The stub-off step passed 162 of 162 on the merge.
- **The 428 cells are red where they should be.** Each new cell is red under the change it pins: the old strip turns N1 red, the old scan turns N2 to N4 red, and keeping the marks turns N5 red.
- **The 427 check is red where it should be.** Without the rule the long code prints 13 pages with columns of 469 px and 125 px, and the spec fails. With `break-word` it also fails. With the rule it prints 12 pages with 297 px and 297 px, the same as the short code.
- **Priced document unchanged.** The priced S4 document prints 13 pages with equal text and equal page images before and after the rule.
- **Text size.** The median word height is 9.493 pt in all four long-code and short-code PDFs.
- **Rendered pages.** The before and after renderings of the section-2 page are kept outside the repository, in the project's `.tools/b1901-m175/evidence/`: `before_no-rule_long-code-long-p3-03.png` and `after_head0_long-code-long-p3-03.png`.

## Not tested

- The browser's own print dialog (`window.print`), which the review used. The spec covers Chrome's `page.pdf` path only.
- The page count on the hosted runner's fonts. This first hosted run is its first measurement.
- The one-pager's detail cell with a long code. This is a separate follow-up.
- Hosted CI and CodeQL decide on this pull request. Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
