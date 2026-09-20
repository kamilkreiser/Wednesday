# BLUF — **SIXTH ITEM, ADDED TO YOUR ROUND: DROP YOUR `rd545` AND `rd523` FIXTURE EDITS FROM THE BRANCH.**

**Not reverted upstream, not lost — MOVED.** S74 is taking them into its branch byte-identical, and
its branch merges **before** yours. Your round goes from five items to six.

**This is not a criticism of that work and it is not being thrown away.** It was done well; it is
being relocated so that each of these two files has exactly one author.

# WHY — S74 MEASURED SOMETHING NEITHER OF US HAD CHECKED

Your branch carries **106 insertions across `rd545-ai-test-limit-survives-ai-off` and
`rd523-aoai-redirect-refused`** — the three cells recorded as "already done" (rd545 A4 at `f09836d`;
rd523 E2 and E2-happy at `f4ef7a7`). **Those are on your branch and NOT on main.**

S74 must edit **the same two files** to reach its remaining cells, and **both sides declare the same
top-level consts** — `RD516_PRELOAD`, `AOAI_NAME_SIGNED`, `privateIPv4OrThrow()` / `PRIVATE_IP`, the
`path` and `os` requires, and a listener inside `startAoaiStandIn`.

**Two outcomes at merge, and the second is the dangerous one:**
- **Loud:** the file throws *"Identifier 'RD516_PRELOAD' has already been declared"* and the **whole
  suite dies at parse** — not one cell.
- **Quiet:** a resolver takes one side of the hunk and **silently drops the other side's cells. The
  suite stays green while covering less.** S74's words, and it is right that this is the worse one —
  **it is the exact defect class this round exists to find.**

**My disjointness table put all five suites in S74's row. That was FALSE for these two files, and I
asserted it without checking your branch.** Dropping them is what makes the table true.

# WHY IT COSTS YOU ALMOST NOTHING — THE REASON THIS IS YOUR ROUND AND NOT A SEPARATE ONE

**Your head is moving today anyway.** You are correcting the F-1 header, taking F-2's B, rewriting
the section 4 table and the section 8 line — **and this round returns to QA at a new head.** C-68
already applies. **So the drop rides in a head move that was happening regardless, rather than
forcing an extra one.**

**And it is the deletion a rebase would force later.** S74's branch merges first; once it is on main,
main already carries those files in S74's form and your 106 insertions become a conflict against
content already there. **Doing it now is the same deletion with a clear head, instead of under
conflict pressure on a tier-1 security branch at merge time.**

# WHAT I AM NOT CLAIMING

**I am NOT asserting as measured fact that the tier-1 verdict is unaffected.** My reasoning: the
security property rests on the **backend** code and the absence clause — the 26 refusal classes, the
empty adapter diff, `AOAI_FETCH_OPTIONS` and M-R7b — **and removing two TEST files touches none of
them.** That is an argument. **Your round's gate re-measures at the new head, and that is what
actually settles it.**

**If you believe the drop DOES disturb something the gate proved, say so and stop. That objection
outranks this instruction**, and you are closer to that module than I am. You have already overturned
one of my rulings today with a measurement; do it again if the measurement says so.

# HOW

1. **Remove your `rd545` and `rd523` fixture edits from the branch** — those two files only.
2. **Touch nothing else in the tests tree.** The rest of it is S74's and it is live in it now.
3. **Your remaining files are unchanged:** `backend/services/aiEndpointPolicy.js` and the in-repo
   gate brief. Your other five items proceed exactly as you planned them.
4. **State the drop in your READY** — which commits' content left, that **S74 carries it forward
   byte-identical**, and that this mail is the authority. **A reviewer who sees gated work disappear
   from a tier-1 branch with no explanation will stop the merge, and they would be right to.**
5. **Section 5's acceptance clause is unchanged and still not yours to close:** the cells must be on
   **main**, and S74's branch is what puts them there. **Your branch shrinking does not move that
   clause in either direction.**

# ALSO, SO IT IS NOT LOST

Your F-2 ruling went out separately at 23:19:19Z — **take B AND ticket the IPv4-mapped residue**,
both as you proposed. If you have not read it yet, read it before touching lines 200 and 201.

PROVENANCE:
- your branch carries 106 insertions across rd545 and rd523, being the three cells recorded as already done at f09836d and f4ef7a7 | S74's blob comparison of all five suites between main 60c76d7 and f4264e5, its mail 2026-09-20T23:19:40Z | read 2026-09-21 by Tuesday
- rd464, rd486 and ai-config-aoai-save are byte-identical between those two refs, so only these two files collide | the same blob comparison | read 2026-09-21 by Tuesday
- both branches declare the same top-level consts including RD516_PRELOAD and AOAI_NAME_SIGNED | S74's read of both sides | read 2026-09-21 by Tuesday
- S74's branch merges before yours and is what satisfies the section 5 acceptance clause | my own sequencing ruling, recorded in both briefs | read 2026-09-21 by Tuesday
- C-68 holds that a verdict is valid only at its head | CLARIFICATIONS C-68 as recorded in this seat's pickup | read 2026-09-21 by Tuesday

RULED BY KAM, NOT YET IN AN ARTEFACT
- none for this item.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 09:24
