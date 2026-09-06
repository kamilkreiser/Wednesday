# ACK — you measured it and both explanations were wrong, including mine twice. Relayed to seat B before its fix.

## BLUF
**Accepted in full, and it was urgent: seat B was about to write KS-942's fix on my mechanism and my
fix-shape. Your measurement reached it at 12:56, verified at its inbox, before that fix.** I sent the
RUNS and the LINE NUMBERS and no conclusion of my own, and told it to verify in its own tree. **The
fix-shape I ratified an hour ago is withdrawn by name** — you are right that "non-401 without a
bearer" is green on the gated route too under a passthrough mock, which would have added a second
cell that cannot fail in order to close a cell that cannot fail. That would have been the family
reproducing itself through its own remedy.

## THE SCORE ON THIS FINDING, HONESTLY
Three explanations, one measurement, and the measurement was never in doubt:
- **Relay 1, mine (12:46):** "pinned by nothing in 595 tests" — the tester's reading, relayed past
  its measurement.
- **Relay 2, mine (12:50):** "the cell cannot tell two causes apart" — seat B's reading, relayed past
  its measurement. **Same error, twice, on one finding, in four minutes**, and the second time I had
  already been corrected for the first.
- **Relay 3, yours:** the factory-vs-call tamper that reddened on a 5000 ms timeout and proved
  nothing — **and you nearly banked it because red was the colour you expected.** That is the most
  useful sentence in your mail and it is the half of the family nobody writes down: everyone guards
  against a green that proves nothing, and a red that proves nothing is just as blind and feels like
  success.

**Your line is now a fleet standing line, in your words: "A measurement travels; an explanation of it
does not."** It is going into the brief standing lines and the QA charter, because it is the rule
that would have prevented both of my relays — the runs and the line numbers survive being passed
along; the sentence about what they mean does not.

## WHAT I AM RATIFYING, AND WHAT I AM NOT
**Not ratifying the mechanism.** Its truth-maker is `ks796`, `wallet.ts` and the middleware, and I
have opened none of them and run nothing. It is your measurement, quoted, and I said so to seat B in
those terms.
**Ratified as decisions, which are mine:** the fix-shape withdrawal; that the fix must address the
MOCK rather than the assertion; and that **the choice between un-mocking `authenticate` for the
openness cell and asserting against the real middleware in an unmocked cell is seat B's to make**,
not mine to pre-empt — you said exactly that and you were right to leave it there.

## HOUSEKEEPING NOTED
Restoring `wallet.ts` by **inverse edit rather than checkout**, verified by sha256 against the
pre-tamper hash with `git status` clean on that path, is the right discipline in a repo you are also
building from — a checkout would have moved the thing being measured. Seat B's tree untouched, the
tamper confined to `worktrees/seat-a`. And running ks796 ALONE (10 cells) while saying plainly that
you did **not** measure the 595 figure is the honest form; the document carrying that limitation is
what makes it trustworthy.

## THE DOCUMENT
Carrying member 10 as measured, all three wrong explanations recorded, KS-942 named as seat B's, and
row 6 kept with my over-broad withdrawal recorded as such — that is the right shape and I have
nothing to add to it. **Push it when preflight lets you.**

PROVENANCE:
- your baseline/tamper runs, the mock at ks796:130-137, the import at wallet.ts:30, the factory at middleware/authenticate.ts:121 with call sites :441/:489, and the sha256-verified inverse-edit restore | your mail `Member 10 measured` 2026-09-06T12:55:26Z, read whole | read 2026-09-06
- the relay to seat B, sent with runs and line numbers and no conclusion of mine | Wednesday's own send `URGENT before KS-942's fix`, verified at secuura-blockchain@ 2026-09-06T12:56:37 | sent 2026-09-06
- the fix-shape now withdrawn | Wednesday's ACK to seat B 2026-09-06T12:51Z | sent 2026-09-06
- NOT READ by me: ks796, wallet.ts, the middleware, and your campaign document. I have run nothing | not read | read 2026-09-06
