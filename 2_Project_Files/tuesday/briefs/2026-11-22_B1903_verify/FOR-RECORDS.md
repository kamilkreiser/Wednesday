# For the records (MPSCALC-427, MPSCALC-428), gate B1903

## The tickets now
This gate read both tickets by Jira GET (2026-11-22 evening; control MPSCALC-361 reads Done; JQL `project = MPSCALC AND ( key in (MPSCALC-427, MPSCALC-428) )` returns 2 rows):
- MPSCALC-427: Backlog, 0 comments, 0 links, label `records-pass-1120c`, updated 2026-11-20 17:53.
- MPSCALC-428: Backlog, 0 comments, 0 links, label `records-pass-1120c`, updated 2026-11-20 17:54.

Neither ticket has changed since the kit. No pull request names either one. A merge does not move a ticket. The records pass moves them and comments after the pull request lands.

## Sentence for the 427 comment
This wording is the coordinator's choice, not the product owner's. The ticket says it "changes no word and no priced document".

> The card items of the full proposal gain `overflow-wrap: anywhere`. Real catalogue part codes were measured first: 1878 values of 6 to 8 characters, lengths only. A committed Chrome print check, `web/e2e/proposal-long-code.spec.ts`, prints the unpriced seven-package proposal with a short code and with a 60-character code that has no break. Both print 12 pages, with no overflow and two card columns of 297 px. Without the rule, the long code gave 13 pages and columns of 469 px and 125 px. The ticket's own example, `overflow-wrap: break-word`, does not fix it, because the grid's `1fr` minimum keeps the unbroken word; `anywhere` does. The priced S4 document prints the same text and the same page images before and after. No word changed.

## Sentence for the 428 comment
> In `unpriced.test.tsx`, the places a code can start are now decided on the text before any strip, in one pass, so there is no cascade. U+0001 is removed from text nodes and attribute values before the scan writes its marks. The first limit says so. Six cells were added, N1 and its control, N2 to N5, taking the file from 88 cells to 94. Each cell is red under the change it pins: the present function turns N1 to N4 red, the old strip turns N1 red, the old scan turns N2 to N4 red, and keeping the marks turns N5 red. No source byte of either document changed.

## Readings the 427 comment should carry (findings of this gate, all Minor)
1. **Text size.** The check pins the cause (the column widths) and the page count. Text size is evidence only: the median word height is 9.493 pt in all four PDFs, through Chrome's `page.pdf`. The review's figures came from the browser print dialog (`window.print`), and that path is UNMEASURED. This print path did not reproduce "scales the whole PDF down"; the defect showed as an extra page and a squeezed column.
2. **Hosted page count.** The equality of the page counts depends on the data. The hosted runner's fonts may give a different absolute page count, and the first hosted run is the measurement.
3. **Hyphenated codes.** These were measured in this gate's scratch copies; no committed cell covers them.
   - One hyphen followed by a 56-character segment shows the same defect without the rule (13 pages, columns of 437 px and 157 px) and is fixed by the rule (12 pages, 297 px and 297 px).
   - A hyphen every 10 characters prints 12 pages with equal columns even without the rule.
4. **Places the rule does not reach.** A long code also prints in places other than the cards:
   - The one-pager's detail cell, `OnePager.tsx:246`, is in a `table-layout: fixed` table with no wrap rule. A long code there would overflow its cell. This is DERIVED from the CSS and not measured.
   - The full proposal's tables, `ProposalDocument.tsx:360`, `:398`, `:419` and `:467`. The seven-package print put the 60-character code into the package table (`:398`) with 0 overflow and an equal page count. The other three are not measured.
   - Candidate follow-up: a long-code check for the one-pager and for those tables.
5. **Priced documents.** The priced path prints no part code (`detail(x, !priced)` and `priced ? description : partCoded(...)`), so the rule never receives a code there. It does apply to priced card text, and that text is unchanged in the measured S4 print.

## Measured in the gate
- Tarballs of e0dcea68 (head), ec281cfb (base) and d8e6d050 (main), plus a MERGE tree: main with the kit's two frozen scripts applied.
- Head equals the base with the frozen scripts applied, byte for byte. Exactly four paths differ.
- Test file: 94 passed (88 at base). Whole vitest run: 149 files, 1740 passed at head and 1742 on the merge.
- `eslint .` and `tsc -b` pass at the head and on the merge.
- `red428.py`: 6 labels, DIFF 0. `red427.py`: 5 labels, DIFF 0, on port 9983.
- The stub-off step on the merge: 162 passed.
- Nothing deployed.
