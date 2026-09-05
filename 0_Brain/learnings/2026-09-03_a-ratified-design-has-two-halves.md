---
date: 2026-09-03
type: correction
source: Kam, terminal ~21:00 AEST, with two screenshots — the ratified mock and the built page
status: live
tier: W
---

# A ratified mock is a spec with TWO halves — a brief that carries its figures and not its layout ships half the design, and only the principal will notice

**The operative case, so the headline matches it:** Kam has approved a MOCK — a rendered design document — and Wednesday is now writing the brief that turns it into code. **Ask which half of that mock the brief is carrying.** A mock states two things at once: WHAT the page says (the figures, the groups, the captions, what is deliberately absent) and WHAT THE PAGE IS (the columns, the chrome, the tiles, the chips, the popover, the type scale). The figures are easy to carry because they are prose. **The layout is a picture, and a picture does not survive into a brief unless someone measures it into words.**

## The case

The Sustainability relayout was mocked by the NexusAI agent (S25) as a full-page HTML design and ratified by Kam on 2026-09-03 at 13:18 (*"That's fantastic. I agree with the approach. Please go ahead."*). Two sessions built from it. Both briefs carried the figures — water first, CO2e hidden, wood/tree held, the /1000 trap red-proved, every figure derived on the seat with an eye. Neither brief carried one sentence about the layout.

S26 delivered exactly what it was asked for and delivered it well: every figure on the page reproduces from the raw rows to the last digit, the gate is green across 78 suites, the guards are red-proved with sha-verified mutants. Then Kam looked at the rendered page at ~21:00 and said: *"For Nexus sustainability tab, use this layout. this is much better. the current one up on screen is not good."*

Measured by Wednesday from the objects, after his message:

| the mock (`d18d4e8:docs/sustainability/mocks/s25-relayout-mock.html`) | the built page (`caf1fe7`) |
|---|---|
| `.grid{grid-template-columns:minmax(300px,1fr) 2fr}` — metrics left, improvements right | two full-width Bootstrap cards stacked; **`grep grid-template-columns` over the served CSS returns nothing** |
| `.topbar` in `--nx-brand-chrome` with the window as a white pill | no header bar; the page's own `<h1>` |
| `.fig` tiles, `min-width:150px`, value over caption, eye at the corner | each figure an inline run of text — a group reads as one long line |
| the `What these figures rest on` box REPLACED by the pill + the eyes | the old box still on the page |
| `.cls` bordered uppercase chip | Bootstrap `badge bg-primary` — `#0d6efd`, off BRAND.md |

**The tester did not catch it either, and that is the instructive part.** Pass 15 compared the figures against the mock — that is how it found the doubled nouns — and reported *"structure as commissioned"*, because the structure it checked was **the brief's** four groups, not **the mock's** page. Every instrument in the chain was pointed at the half that had been written down.

## Why the existing lessons did not fire

- [[2026-09-01_qa-gate-before-my-verification]] put a render in the loop, and the render was checked against the commission. **The commission was the incomplete artefact**, so the gate confirmed a faithful build of half a design.
- [[2026-09-02_style-guides-never-mixed]] made Wednesday ask *which document says what this project looks like* — and here that document EXISTED and was ratified. The rule got as far as naming the guide in the brief and never asked whether the built page CONFORMS to its shape.
- [[2026-08-10_own-the-spec-not-just-the-escalation]] says spec alignment is Wednesday's verification step. It was run item by item against the brief's items. **A completion check against a brief cannot find what the brief left out.**

## How to apply

1. **When a mock is ratified, MEASURE IT INTO THE BRIEF in the same action.** Open the file, read its CSS, and write the layout down as numbered, checkable properties — the grid, the chrome, the tile shape, the chip, the popover, the table rules. "Build it like the mock" is not a brief; a reader who has the mock still needs to know which of its properties are load-bearing.
2. **A design ratified once stays the spec for every later round.** Each subsequent brief carries a pointer to the mock BY REF (`git show <sha>:<path>`, ancestry verified) and one line naming which of its halves this round is closing.
3. **The completion check gets a second question.** Not only *does the delivery match the brief?* but ***does the delivery match the artefact Kam approved?*** Those are different documents, and when they differ, the ratified one wins — because that is the thing the principal said yes to.
4. **The QA brief gets the mock as an EXPECTED artefact**, so a pass can report "the page does not have the mock's shape" without being told to look for it. A tester given the figures will check the figures.
5. **The screenshots close the loop.** Any round that changes what a page IS ends with rendered screenshots to Kam, both modes, before the deploy — his eye is the only instrument that has ever caught this class, twice now (the navy palette on 2026-09-02, this layout tonight).

**The uncomfortable part, kept:** the agents did not fail here. Wednesday commissioned half a design twice, scored the second half 0.90, and would have deployed it to the dev app if Kam had not looked at the screen. **The system's own instruments were all green because they were all pointed at the same incomplete sentence.**

**Related:** [[2026-09-02_style-guides-never-mixed]] · [[2026-09-01_qa-gate-before-my-verification]] · [[2026-08-10_own-the-spec-not-just-the-escalation]] · [[2026-08-07_a-check-that-cannot-fail]] (every instrument agreed because every instrument shared one blind spot) · [[2026-08-13_headline-must-match-the-operative-case]] (a brief's items are its retrieval handles — what is not an item does not exist)
