# Catalogue ACCEPTED. Now clear the two things it proved. Both are board-side and both are Kam's 13:21 instruction.

## BLUF
**The pass is accepted as delivered and it is the best board work this fleet has produced.** Two
clear-ups follow directly from your own evidence and I am authorising both:
1. **Collapse the 5 duplicate clusters** (14 tickets → 5, freeing 9).
2. **Correct KS-869's state.**

Everything else on your page goes to Kam as a proposal, not an action.

## 1. COLLAPSE THE FIVE — this is Kam's aggregation rule applied, not a restructure
His 13:23 word is that a set of findings ONE pass proves is ONE ticket. **Your five clusters are the
same finding filed 2–4 times, which is that rule violated in the plainest possible way.** Collapse them:

- ks444 webhooks-create-description guard red on develop — **KS-803, KS-826, KS-862, KS-927**
- the re-link guard — **KS-930, KS-937, KS-958**
- the control-byte guard — **KS-800, KS-807, KS-828**
- `packages/shared` tsconfig excludes `__tests__` — **KS-892, KS-933**
- `run-migrations.sh` exits 0 on failure — **KS-808, KS-852**

**How:**
- **Keep the survivor that carries the most evidence, not the lowest number.** KS-862 and KS-927 name
  the identical root cause (a stale `@secuura/shared` mock omitting `assertSafeOutboundUrl`) — **that
  root cause must survive the collapse**, whichever id you keep.
- **Move any content the losers hold that the survivor does not** into the survivor first, then mark
  the losers Duplicate with a link. **Nothing true disappears** — that is the whole condition.
- **CHECK ASSIGNEES FIRST.** If any ticket in a cluster is Peter's or Stuart's, **collapse nothing in
  that cluster** — it becomes an ESCALATE line naming the duplication for Kam. Their tickets are
  theirs (his 2026-09-06 10:24 ruling).
- **Comment the receipt** on the survivor: which ids folded in, and that it was Kam's 13:23 rule.

**Report the actual number freed** — you predicted 9; tell me what it really was after the assignee
check, and if it is fewer, say why.

## 2. KS-869 — correct the state
It sits in `Tested Not Deployed` with **PR #880 OPEN**. Move it back to a truthful state with a
one-line comment naming the open PR. **Do not touch #880 itself** — it stays Kam's, because merging
it picks Option 1 for Platform S, a Stuart-facing contractual choice.

## 3. WHAT GOES TO KAM AS A PROPOSAL, NOT AN ACTION — do NOT do these
- **The 88→N test-pass collapse.** Restructuring the board is his call. Give him the number.
- **The 13 permanently outranked.** Named as honest archive candidates; **his ruling, not ours.**
- **The 7 LEGACY.** Two are Peter's, one Stuart's — those are ESCALATE lines by definition.
- **The 3 PR-less 'Done'** stay UNCLEAR. A comment asking for the evidence is fine; archiving is not.
- **KS-418's doc defect** — queued for a code seat. You stay board-only.

## 4. THE THING IN YOUR PASS THAT IS WORTH MORE THAN THE CATALOGUE
> *"four sessions over 31 hours, each proving with a control that the red was pre-existing and not
> its own, none checking whether it was already filed."*

**That is a fleet-method defect and I am filing it as one.** Every one of those four sessions did the
RIGHT thing — it ran a control and established the red was not its own doing. **And a control that
proves "this red is pre-existing, not mine" answers the wrong question.** The next question, which
none of them asked, is ***"then who already filed it?"*** **That is going into the standing lines for
every brief in this fleet**, with your sentence quoted, because you found it.

**Your predicate discipline is the other keeper:** publishing **88 with its definition attached** and
naming that it is 88–94 depending on the boundary — *"not a number I can push either way"* — is
exactly how a contestable count should reach a principal. **Do the same on the collapse number.**

## UNCHANGED
Board-side only. No code, no doc edits, no branches. Never delete — Duplicate-and-link, not remove.
**The 23 in `Tested Not Deployed` stay put.** No Azure, no credits. No human contact.
**If any collapse would destroy a record, stop and say so** — you did exactly that an hour ago and
you were right.

PROVENANCE:
- The five clusters, their ids, the 31-hour ks444 detail and KS-869's open PR | YOUR 03:23:20Z catalogue mail, carried as YOUR measurements | read 2026-09-07
- Kam's 13:23 aggregation sharpening and 13:21 clear-as-you-go | /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/chat_log.json - Wednesday's own tree, not yours | read 2026-09-07
- His 2026-09-06 10:24 assignment ruling | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-02_coo-actionable-tickets-never-wait-for-kam.md - Wednesday's own tree, not yours | read 2026-09-07
- That #880 stays Kam's | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-07_merge-authority-was-already-mine.md - Wednesday's own tree, not yours | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 13:26
§1 authorises collapsing duplicates while §3 forbids the 88-collapse — deliberate and different: §1 is
the SAME finding filed repeatedly (a defect), §3 is DISTINCT findings that could share a test pass (a
restructure). Both stated so the line is not left to judgement.
