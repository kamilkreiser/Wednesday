## What a seller now sees

On the proposal page of a purchase quote, beside the two print buttons, there is a small group with two choices:

- the first choice keeps today's documents, with unit and extended prices. It is selected every time the page opens.
- the second choice prints the full proposal and the short form with no figure at all.

The group never prints. It is not shown on a rental quote, on a purchase proposal without packages, or while the proposal loads.

## What the unpriced documents leave out

Every amount the server sends: the purchase total tile on both covers, the package price and class columns and the total rows, the class split table, the credit callout, the large-format ink sentence, the reconciliation callout, the customer rate columns, the usage formula callout, the software amount columns, the optional item unit price column, the optional enhancement callout, the price, class, inc-GST and rate rows of the summary table, and on the short form the class list and the rate sentence. Every other part of the documents is unchanged and keeps its existing words; no word is added to either document. Some existing sentences still speak of price without a figure (for example the schedule section title and a sentence that points to the reconciliation); they are listed in the word pack for the product owner and are not edited here.

## Priced output is unchanged

With the option absent, and with the priced choice, both documents render byte for byte as on main (checked on captures of the rendered markup at main and at this head).

## The three new words: PENDING the product owner's word pack

- `Customer PDF option` (the group's visible legend)
- `Show customer unit and extended prices` (the first choice)
- `Show SKUs and quantities only` (the second choice)

They go to the product owner as a word pack before any hosted deploy and are not shown on any hosted site until then.

**The gap in the third word:** it says SKUs and quantities, but the unpriced documents show descriptions and quantities and no part codes. Adding the codes is a words decision for the product owner.

## Not built here

- the rental documents (the rental book and the rental short form stay priced);
- a part-code column, or part codes in any text;
- a durable record of the choice: the choice is page state plus one attribute on the printed document's root (`data-price-option="unpriced"`), nothing is stored with the quote. MPSCALC-278 therefore stays open on "the choice is recorded".

## Proof and its limits

- A new test file renders both documents over synthetic fixtures and checks the rendered text for the figures the server sent, the closed list of omissions, the table shapes, that no unknown text appears, and the page control (default, keyboard group, print, content save, rental).
- The independent review also checked every money and rate member of the proposal contract with its own fixtures and detector (text, every attribute and the style element), printed both unpriced documents to PDF in a real browser and read them back as text (no figure found; the priced PDFs do carry figures), and ran the full web checks on Node 24.
- Limits: the committed test reads rendered text in a test DOM, not a PDF; it would not catch an amount placed in an attribute or a figure in another format; a figure that staff type into a narrative field is the staff's own text and is not removed.

Nothing is deployed by this change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
