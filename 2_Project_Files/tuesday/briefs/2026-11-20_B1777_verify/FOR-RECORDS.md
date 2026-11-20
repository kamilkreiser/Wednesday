# What a records seat files, both rounds (round 2 of 2: GO WITH FINDINGS @ b1c0e4b on main 565ba14)

Round 1 read NO GO at fa71fc8 (one Major in the no-price check). Round 2 reads GO WITH FINDINGS at b1c0e4b: the Major is closed, and no Blocker or Major is left. This file carries round 1's list forward and marks what round 2 closed.

## Round 1's list, as it stands at b1c0e4b
1. **Major, the strip had no left boundary: CLOSED.** The fix is not round 1's proposed rule but a closed list of three starts (the start of a text, the start of a text node, right after a quantity and the multiplication sign). The gate measured that the proposed rule would have been wider than the stated limit: under it, `Total 4521.10 <description>` reads clean. Round 1's rendered proof (code `0.50`, unit price `1250.50`, optional items) now finds the amount. The gate also re-ran the proof at all six code slots with tail codes, and the amount was found every time.
2. **The limits texts: CLOSED, with one residual (NEW B below).** L-A, L-B and L-C now stand verbatim in the test file, in the second commit's body and in the ADDENDUM. The squash text in this folder carries all three, with "abbreviated", and it replaces the first commit's "equal" wording.
3. **ADDENDUM additions:** (a) a code that looks like a price prints as typed: **CLOSED** (round-2 section, item 1); (b) the long-code PDF shrink: **CLOSED as text** (item 2; the fix itself is NEW A). **Still open:** the measured page counts (NEW C).
4. **STATUS count "24" should read 26:** stated in the ADDENDUM (item 4, 26 confirmed: +21 and +5). **Open for records:** the first round's STATUS file is untouched; correct it, or file a pointer to the ADDENDUM.
5. **Round-2 re-runs: DONE by this gate** (the probes, the plants, the mutants, the goldens on node 24). No PDF row was needed, because no source file changed.

## Follow-ups to file (search first; none blocks the merge)
- **NEW A, the long-code layout (carried from round 1):** let a part code break inside the stream cards (CSS), so that a long unbroken code does not shrink the printed PDF. Add a PDF check with a 60-character code in a narrow card. Measure real catalogue code lengths first, from the catalogue import, without reading any price.
- **NEW B, the check's residual (round 2, test file only):** the first limit's sentence "The same text printed anywhere else is still found" fails in two data cases:
  - a description that begins with another line's code and description, where that code equals an amount (the strip cascades);
  - sent text holding the control character U+0001, which forges a start (in a description, a narrative field or an attribute).

  The fix is two lines in `web/src/proposal/unpriced.test.tsx`: decide the starts on the text before any strip, in one pass, and remove U+0001 from text nodes and attribute values before marking. Add a cell for each. Also add the missing cell for the mark removal in `figuresIn`: a figure split across two text nodes must be found (gate mutant T5 stayed green). Proof: `/private/tmp/b1777-gate/out/cascade.jsonl`, `attack.jsonl` rows A8, A9, `split.jsonl`.
- **NEW C, ADDENDUM page counts (records text):** before the word pack goes to the product owner, add one sentence with the counts round 1 printed: `s4` 12 and 3 pages (unchanged); eight packages 13 and 3 (unchanged); the seven-package hostile proposal 13 to 14 pages, from longer lines. Section 6, bullet 2 still says the lane printed no PDF.
- **Optional:** a cell that holds the U10 exception to the short form (giving it to the full proposal stays green today).
- **Unchanged from round 1:** MPSCALC-424 (the durable record of the choice) covers clause 3.

## The ticket clauses after this change (MPSCALC-278)
1. No price anywhere in the unpriced document: MET for the two purchase documents. The product is unchanged since round 1 (its detector: 0 figures not sent as a code, 16 of 16 renders, and the real PDFs). The check is now proven at all six code slots. Open limits:
   - figures typed into narrative fields;
   - codes printed as sent, so a price-shaped code prints;
   - Chrome only;
   - the rental documents;
   - the check's residual NEW B.
2. Priced output unchanged: MET (8 committed goldens, blobs unchanged since round 1, green on node 24).
3. The choice is recorded: NOT MET in the lasting sense (page state plus one attribute). It is MPSCALC-424. **MPSCALC-278 stays open.**

## The part-code follow-up (MPSCALC-426), its acceptance check line by line
The text is round 1's reading of the records seat's frozen kit; Jira was not read by either gate.
- Both documents print the code before each description wherever the server sends one, and a test shows it: MET (sites L1 to L6, cells).
- The three words unchanged, with a test that reads them: MET (`ProposalPage.tsx` blob unchanged).
- No price in an unpriced document, with the existing checks green: MET. The check's round-1 Major is closed; a residual remains (NEW B).
- A priced document unchanged: MET.
- The pattern of the printed line goes to the product owner as a word pack before it ships: NOT YET (Tuesday's, later). The ADDENDUM is ready apart from NEW C.
- An independent review before it lands: round 1 NO GO, **round 2 GO WITH FINDINGS (this gate)**.
- Nothing put on the hosted site by this ticket: MET (nothing deployed; no deploy job on main).

## What the deploy card must tell the product owner
- What changes for a customer: the code, one space, then the description, in six places of the unpriced documents. Use one before-and-after line from the ADDENDUM.
- That the three words and the priced documents are unchanged.
- Where no code prints: lines without a code, the package name, two template sentences, and the rental documents.
- The limits:
  - a code prints exactly as staff typed it, including one that looks like a price;
  - a long unbroken code can shrink the printed PDF, and longer lines can add a page (13 to 14 in the review's seven-package proposal);
  - figures typed into narrative fields are not checked;
  - only Chrome was printed;
  - the no-price check has a narrow residual that needs unusual data (NEW B).
- That he has not been asked about, and has not approved: the six sites, the separator, the boundary rule of the check, the rental documents, or what "recorded" means. These are the coordinator's defaults. His ruling of 2026-11-20 (entry C-186) is quoted word for word, and nothing wider.
- That the hosted site still holds an older main, and that this change needs his deploy card.
