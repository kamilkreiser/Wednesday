## What a customer now sees

When staff choose "Show SKUs and quantities only", the unpriced full proposal and the unpriced short form now print the part code the server sent in front of each line item's description, with one space between them. That covers six places:

- the stream cards and the fleet detail cell of the full proposal;
- its office table, its optional items and its software rows;
- the short form's detail cell and software table.

For example, in the full proposal's stream cards:

- before: `7 x Synthetic A3 colour MFP, 45 ppm`
- after: `7 x SYN-MFP-A3C Synthetic A3 colour MFP, 45 ppm`

(The document prints a multiplication sign where this text shows `x`.)

`(included)` and `(credit)` stay at the end of their line. The cap of four lines in a stream card, the cap of three in the short form and the "+n more" count are unchanged: they count lines, not characters.

A code prints as staff typed it, trimmed of spaces at either end. A manual item's code is free text, so a code that looks like a price (for example `4521.10` or `$1,234.56`) prints as it is in the customer's unpriced document.

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

The no-price test reads the printed text, each text node on its own line, and the value of every attribute. It reads whole-dollar forms (`57,940` and `57940`) as whole tokens. A part code is removed before the scan only where the documents print one: at the start of a text, at the start of a text node, or right after a quantity and the multiplication sign. Anything before that place, and every attribute value, stays in the scanned text. There is no list of allowed codes. The no-new-word test is exact, with one named sentence of the short form as its only exception.

Limits:

- A part code printed in its own place is read as data, whatever it holds: a code that equals an amount, or contains one, prints and reads clean there. The same text printed anywhere else is still found.
- A figure with cents printed rounded, re-grouped or abbreviated (57,941 for 57940.50, 57 940, 57.9k) is not read by the price check; the no-new-word check flags the new text instead.
- A figure staff type into a free-text narrative field is their own text and is not scrubbed.

A known gap, to be closed in a follow-up: the first limit's last sentence does not hold in two cases. Both need unusual text from the server:

- a description that begins with another line's code and description, where that code equals an amount;
- sent text that holds a control character.

In both cases the no-new-word test flags the text.

A long unbroken code (about 20 characters or more) in the first stream card of a proposal with many packages makes Chrome scale the whole printed PDF down. In the review's seven-package proposal, a 60-character code gave a scale of about 0.67, and 14 pages became 12. Letting a code break inside the stream cards is a separate follow-up. How long real catalogue codes are is not measured.

## What is not built

- The rental documents (they stay priced).
- A durable record of the choice: it is still page state plus one attribute on the printed document.

MPSCALC-278 stays open on its third clause, "the choice is recorded".

## Not on the hosted site

This change is not on the hosted site. It waits for a deploy card of its own. Before that, the way the printed line reads goes to the product owner.

## Proof

- The whole web suite is green on node 24 (149 files, 1723 tests).
- Both browser steps are green (260 passed and 17 skipped; 161 passed).
- The dependency audit, lint, the type build, the production build and the bundle check are green.
- Local CodeQL: 0 results.
- An independent review printed both documents to PDF in Chrome and read them back as text:
  - unpriced documents: no figure, the codes present;
  - priced documents: no code;
  - page counts unchanged for the repository's fixtures (12 and 3 pages; 13 and 3 pages). The review's seven-package proposal with long lines went from 13 to 14 pages.
- A second review planted an amount in the code slot of each of the six places, with codes that are the tail of that amount. The test found the amount every time.

The review's limits: synthetic data only, Chrome only, and the hosted checks on this pull request remain the authority.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
