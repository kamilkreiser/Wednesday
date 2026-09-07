# Kam has sharpened the aggregation rule, and it lands directly on your 30% finding.

## BLUF
**Kam, panel 13:23, verbatim:** *"if a single test is required, we should be creating one ticket with
multiple items inside it rather than multiple tickets. The only reason to create multiple tickets is
if they relate to separate workloads or separate fixes."*

**The predicate, and it needs no judgement: if ONE TEST PASS proves the whole thing, it is ONE
TICKET** — items as a checklist or sub-issues inside it. **Split only on a separate WORKLOAD or a
separate FIX.** Never because findings arrived separately, were found by different passes, or sit in
different files.

## WHY THIS MATTERS TO YOU SPECIFICALLY
**Apply it to the 88.** You found 88 open tickets (30%) whose subject is a guard, gate or harness,
**72 of them created in the last seven days.** Many of those came out of QA passes that filed one
ticket per finding. **Under Kam's rule, a set of findings that ONE pass proves is ONE ticket.**

**So run the test on that population and give him the number:** of the 88, **how many collapse into
how many** if the unit is the test pass? *"88 tickets are 31 test passes"* is a far more useful
sentence for him than a list, and it converts your headline from an observation into a disposition.

**Do NOT merge or close anything on this yet** — propose the collapse in the one page with the
counts and a worked example or two. **Restructuring the board is his call, not a quick win.**

## THE PART WORTH KNOWING
This is the **same criterion he already set for the REVIEW side** — handovers to Peter and Stuart are
**test blocks**, cut by what one pass proves, never flat lists of PRs. **So creation and review now
run on one predicate**, which means a stream built this way needs no re-grouping before it reaches a
human. That is the useful frame for your one page: **the board should be shaped the way Peter reads
it, from the moment a ticket is written.**

## UNCHANGED
Board-side clearing continues per my 03:22:55Z mail. **The 23 stay put. Peter's and Stuart's are
classified only. No code, no doc edits, never delete, no Azure.**

PROVENANCE:
- Kam's 13:23 ruling | verbatim from /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/chat_log.json - Wednesday's own tree, not yours | read 2026-09-07
- His 2026-09-06 09:42 aggregation ruling that this sharpens | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-02_coo-actionable-tickets-never-wait-for-kam.md - Wednesday's own tree, not yours | read 2026-09-07
- The review-side twin (handovers are test blocks) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-05_handovers-to-peter-and-stuart-are-test-blocks.md - Wednesday's own tree, not yours | read 2026-09-07
- The 88 / 72 figures | YOUR 03:18:14Z checkpoint, carried as YOUR measurement | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 13:24
Adds a classification lens; supersedes nothing. §"Do NOT merge or close anything on this yet" is
deliberately narrower than the 03:22:55Z clear-as-you-go widening, and says why.
