## What a customer now sees

When staff choose "Show SKUs and quantities only", the unpriced full proposal and the unpriced short form now print the part code the server sent in front of each line item's description, with one space between them. That covers six places: the stream cards and the fleet detail cell of the full proposal, its office table, its optional items and its software rows, and the short form's detail cell and software table. For example, in the full proposal's stream cards:

- before: `7 x Synthetic A3 colour MFP, 45 ppm`
- after: `7 x SYN-MFP-A3C Synthetic A3 colour MFP, 45 ppm`

(The document prints a multiplication sign where this text shows `x`.)

`(included)` and `(credit)` stay at the end of their line. The cap of four lines in a stream card, the cap of three in the short form and the "+n more" count are unchanged: they count lines, not characters.

## What does not change

- The three option words are unchanged: "Customer PDF option", "Show customer unit and extended prices", "Show SKUs and quantities only". The screen file that holds them is not touched.
- The priced documents are unchanged to the byte. Eight captures of the priced render from the base are committed and compared byte for byte, for the default render and for `priced={true}`.
- No word is added. The new text is the server's code, one space, and the existing description.

## Where no code prints

- A line the server sent no usable code for (absent, null, empty, spaces only, or the same text as its description) prints exactly as before, with no placeholder.
- The package name prints no code, because the contract gives a package no code.
- The sentence that names the software bundle in the office section prints no code.
- The short form's sentence about optional items prints no code.
- The rental documents print no code and stay priced.

## The check, and its limits

The no-price test now reads the printed text, each text node on its own line, and the value of every attribute. It also reads whole-dollar forms (`57,940` and `57940`) as whole tokens. A part code printed in its own place is read as data, so a code made of digits is not mistaken for an amount, while the same text printed anywhere else is still found. There is no list of allowed codes. The no-new-word test is exact, with one named sentence of the short form as its only exception.

Limits:

- A figure staff type into a free-text narrative field is their own text and is not checked.
- A code in its own place is read as data whatever it holds. A code that looks like a price, typed by staff as a manual item code, prints as typed in the customer's unpriced document.
- A figure with cents printed rounded or regrouped is not read by the no-price test, though the no-new-word test would flag the new text.
- A very long unbroken code (about 20 characters or more) in the first stream card of a proposal with many packages makes the printed PDF scale down slightly.

## What is not built

- The rental documents (they stay priced).
- A durable record of the choice: it is still page state plus one attribute on the printed document.

The ticket stays open on its third clause, "the choice is recorded".

## Not on the hosted site

This change is not on the hosted site. It waits for a deploy card of its own. Before that, the way the printed line reads goes to the product owner.

## Proof

- Proposal family and whole web suite green on node 24.
- Both browser steps green.
- Production build and bundle check green.
- Local CodeQL: 0 results.
- An independent review printed both documents to PDF in Chrome and read them back as text:
  - unpriced documents: no figure, the codes present;
  - priced documents: no code;
  - page counts unchanged for the repository's fixtures.

The review's limits: synthetic data only, Chrome only, and the hosted checks on this pull request remain the authority.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
