# For the records seat (after landing; nothing here is written by the gate)

Change: the priced or unpriced option on the two purchase documents (full proposal and short form), MPSCALC-278, head 42a08f9 on main 50d2a47. Not deployed.

## The ticket's three clauses (MPSCALC-278 stays OPEN)
1. "With the unpriced option no price appears anywhere in the document (test over the printed text)": met for the two purchase documents at this head. Proven by a committed vitest over rendered text (jsdom), and by the gate's own detector and a real-browser PDF read back by pdftotext. Not proven: rental documents (out of scope, stay priced, control hidden there); figures staff type into narrative fields; the committed test reads text only (see follow-up 1).
2. "With the priced option output is unchanged": met (gate: 36 of 36 rendered-markup captures equal main; builder: 8 of 8). The proof is in uncommitted captures, not in a committed test (follow-up 2).
3. "The choice is recorded": NOT met in the durable sense. The choice is page state (priced by default each time the page opens) plus `data-price-option="unpriced"` on the document root. A durable record needs a contract member and its own lane.

## Word pack (before any hosted deploy)
The lane's WORD-PACK file (in the project's `1_Project_Definition/Briefs/`, dated 2026-11-19) goes to the product owner: the three words (`Customer PDF option`, `Show customer unit and extended prices`, `Show SKUs and quantities only`), the SKU gap (the third word promises SKUs; the documents show quantities and no part codes), and the existing price words that remain in the unpriced documents. No text may say the product owner approved the words, the choice of documents, or what "recorded" means.

## Follow-ups to file
1. Harden the committed oracle (`web/src/proposal/unpriced.test.tsx`, `figuresIn`): also scan attribute values, and integer-part / whole-dollar forms of each figure. The gate planted an amount in a `data-*` attribute and a whole-dollar fragment without a dollar sign; all 29 cells stayed green.
2. Narrow the U10 "part of a priced leaf" refinement (it admitted a planted new phrase made of existing words, all cells green) and commit a priced-markup check that sees more than the column heads (a planted priced column-width change stayed green in the new file and in the existing document tests).
3. Durable record of the choice (contract member, generated client, endpoint): its own lane; closes clause 3.
4. Rental unpriced option (rental book and rental short form): its own lane, if the product owner wants it.
5. Part codes in the unpriced documents, if the product owner rules the third word should be kept as written.
6. For the product owner, information only: on the unpriced short form of a proposal with more than six packages, the packages shown are still the server's top five by package total, in that order, and credit rows keep their "(credit)" label; after a recalculating content save the staff-only notice on screen shows the old and new purchase totals (it never prints).
