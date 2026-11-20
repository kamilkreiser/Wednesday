# B1770 gate: what a records seat files (round 1 of 2, NO GO @ fa71fc8 on main 565ba14)

## Before landing (the round-2 lane, for Tuesday to brief)
1. **Major, fix in the test file only:** `stripCodes` in `web/src/proposal/unpriced.test.tsx` strips a `<code> <description>` match only when the character before the code is not a digit, `.` or `,` (the same rule as `hasToken`). Add one control cell: a line with code `0.50`, the amount `1250.50` printed in its code slot, which oracle P must find. The source files, the goldens and the ADDENDUM's before-and-after lines do not change.
2. **Fix the texts of the limits, everywhere they appear:** the test file comment, the commit or squash body, the PR body and ADDENDUM section 6. They should say: a code printed in its own place is read as data whatever it holds (not only "equal" to an amount); and rounded or regrouped forms of a figure with cents are not read by the no-price check (U10 flags them as new text). The PR and squash texts in this folder are already written that way.
3. **ADDENDUM additions before it goes to the product owner:** (a) a code that looks like a price prints as typed in the unpriced document, because staff type manual codes as free text of 1 to 60 characters; (b) a long unbroken code (about 20 characters or more) in the first stream card of a proposal with many packages makes Chrome scale the whole printed PDF down. The gate measured scale 0.99 at 20 characters, 0.93 at 25, 0.88 at 30, 0.79 at 40 and about 0.67 at 60, with the full proposal moving from 14 to 13 or 12 pages.
4. **STATUS correction:** "added source lines: 24" reads 26 by `git diff --numstat` (+21 and +5).
5. Round 2 re-runs: the gate probes (`/private/tmp/b1770-gate/quar/head-proposal/zzprobe*.test.tsx`, `zzoracle.ts`, re-extracted from the new test file), the four plants and the mutant set, the 16-render base/head compare, and the goldens on node 24. The PDF row need not repeat unless a source file changes.

## Follow-ups to file (each searched first)
- **NEW A, the long-code layout:** let a part code break inside the stream cards (CSS, outside this lane), so that a long unbroken code does not shrink the printed PDF. Add a PDF check with a 60-character code in a narrow card. How long real catalogue SKUs are is UNMEASURED; measure it first from the catalogue import, without reading any price.
- **Optional tidy (Info):** scope the one U10 exception to the short form, the only document that needs it.

## The ticket clauses after this change (MPSCALC-278)
1. No price anywhere in the unpriced document: MET for the two purchase documents. Measured: the gate's detector found 0 figures that the server did not send as a code (16 of 16 renders, and the real PDFs). The open limits are figures typed into narrative fields; codes printed as sent (a code that looks like a price prints); Chrome only; the rental documents.
2. Priced output unchanged: MET, by committed goldens (8 files, 16 of 16 gate captures equal at base and head, node 24, TZ=UTC too).
3. The choice is recorded: NOT MET in the lasting sense (page state plus one attribute). It is not built by this lane; it is MPSCALC-424. **MPSCALC-278 stays open.**

## The part-code follow-up ticket (MPSCALC-426), its acceptance check line by line
The text was read from the records seat's frozen kit (`2026-11-20_B1766_SEAT-R283_mps-records-221.md:267`); Jira itself was not read by this gate.
- Both documents print the code before each description wherever the server sends one, shown by a test over the printed text of both: MET at fa71fc8 (sites L1 to L6, all six with cells).
- The three words unchanged, a test reads them: MET (U11; the `ProposalPage.tsx` blob is unchanged).
- No price in an unpriced document, the existing checks green: MET for the product. The check itself has the Major above.
- A priced document unchanged: MET (goldens).
- The pattern of the printed line has gone to the product owner as a word pack before it ships: NOT YET. That is Tuesday's, later; the ADDENDUM exists and needs the two additions above.
- An independent review before it lands: this gate, round 1 NO GO. Round 2 is owed.
- Nothing put on the hosted site by this ticket: MET (nothing deployed; no deploy job on main).

## What the deploy card must tell the product owner
- What changes for a customer: the code, one space, then the description, in six places of the unpriced documents. Use one before-and-after line from the ADDENDUM.
- That the three words and the priced documents are unchanged.
- Where no code prints: lines without a code, the package name, two template sentences, and the rental documents.
- The limits:
  - a code prints exactly as staff typed it, including one that looks like a price;
  - a long unbroken code can shrink the printed PDF;
  - figures typed into narrative fields are not checked;
  - only Chrome was printed.
- That he has not been asked about, and has not approved: the six sites, the separator, the rental documents, or what "recorded" means. These are the coordinator's defaults. His ruling of 2026-11-20 is quoted word for word, and nothing wider.
- That the hosted site still holds an older main, and that this change needs his deploy card.
