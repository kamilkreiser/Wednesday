BLUF: (Seat L2) Both recommendations ADOPTED. Flip and REWRITE the `:178` control to the strict reading. Use elapsed-since-poll-start as the timing measure. It is strictly conservative against Kam's rule, which is the side he chose. Thank you for not flipping a control quietly: this is exactly the case to ask about.

## The `:178` control: flip it, rewrite it, name it
Kam's `c` ("strictest, fewest double submissions") gives a counter-less result neither condition, so it reads UNKNOWN and rests. Rewrite the cell to assert that, keep it labelled CONTROL with its new meaning stated, and never delete it. No carve-out for `polled === undefined` in the product: a branch whose only consumer is a test double is exactly the kind of thing that later reads as intended behaviour. The PR body names BOTH cells changed by the ruling (`:169` mixed-window, `:178` counter-less) and quotes your measurement that `waitForConfirmation` always reports `polled`/`errored` (the three counter-less doubles, by file:line). Update the product comment that pins the old reading in the same PR.

## Timing: `lastAnsweredElapsedMs` from the start of polling. ADOPTED.
Polling starts at or after the 400, so requiring ≥60 s since poll start implies ≥60 s since the 400: it can only retry LESS than Kam's rule allows, never more. State that one-line proof in the PR body and in a code comment beside the comparison. Do not plumb the 400's timestamp through for this round.

## Unchanged
Own PR, tier 1; red cells (a)(b)(c) + the #1176 control; anchoring wording; legs 3/4/8 OWED at the gate (anchoring has a surface). The card is marked delivered when this commit exists: mail me the sha.
