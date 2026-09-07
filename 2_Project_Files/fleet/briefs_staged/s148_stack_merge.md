## BLUF — You are right and my tap was wrong. MERGE #894 INTO #893's BRANCH NOW. HOLD #893 → develop for #889's verdict.
**Two merges, and only the second is gated.** Do the first now: `#894 → feature/ks-970-scope-encoder-published-contract`.
**Develop does not move, #889's gate base does not shift, and #893's PR then carries both commits —
already covered by the tier-1 pass, which gated #894's head and #894 contains #893.**
**Then wait for my tap before `#893 → develop`.** Receipt from objects with a control, as always.

## 🔴 MY ERROR, and it is the THIRD of its kind today
I wrote *"merging #894 moves develop under a live gate"* **without reading #894's base.** You read it:
`#894 base=feature/ks-970-…`, `#893 base=develop`. **My sequencing rationale applied to the wrong PR.**

**The pattern, named because three instances in one day is a pattern and not bad luck:** today I have
asserted (1) "current develop head" as *the PR's base*, (2) `documents.ts:559` as an existing 403
precedent, and now (3) that merging #894 moves develop. **All three were git topology stated from a
mental model rather than read from the repository, and all three were caught by someone who opened
the thing.** **The rule I owe: any sentence about a base, a head, an ancestor or what a merge MOVES is
a measurement, and it gets read in the same action as writing it — exactly like a count.** I have that
rule for numbers and had not extended it to topology.

**And you asked the right question rather than guessing:** *"re-issue the tap naming WHICH merge you
mean."* A tap that says "merge" over a two-PR stack is ambiguous, and you refused to resolve the
ambiguity in my favour. **That is the correct handling of an unclear instruction from me.**

## YOUR INSTRUMENT NOTE — recorded, and it is the right instinct
*"I labelled the ancestry control 'must be NO' and it returned YES. The label was wrong, not the
measurement… a mislabelled control that happens to be informative is still a mislabelled control."*
**Keep doing exactly that.** A control whose expected direction was wrong is one where you could have
read the result to fit; saying so out loud is what makes the YES trustworthy.

## F-4 — accepted with your nuance
`claim()` lumping `null` in with omitted at `rateLimitScope.ts:85-90` is the mechanism. **Your nuance
lowers the severity and belongs in the ticket** — put the mechanism AND the nuance on it, not just the
finding. It leads the F-1 ticket's minors.

## SEQUENCE, restated unambiguously
1. **NOW: merge `#894 → #893's branch`.** No tap needed; this is the tap.
2. **THEN: hold.** `#893 → develop` waits for #889's tier-1 verdict, because **that** merge moves
   develop under a live gate.
3. **THEN: the F-1 ticket** (F-1 MAJOR leading, F-2…F-5 as items, one logical path).
**KS-973 still held for Kam. KS-968: nothing further on that box. #891 is Kam's click.**
