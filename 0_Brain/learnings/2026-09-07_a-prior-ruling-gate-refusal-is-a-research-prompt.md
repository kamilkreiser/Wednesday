---
date: 2026-09-07
type: correction
source: the decision-queue prior-ruling gate refusing the vault `add -A` card, 21:1x, laptop/Datasec seat
status: live
tier: W
---

# A gate saying "Kam already ruled this" is telling you to go read the SHIPPED DIFF — what a fix CHANGED is not what its card was ABOUT

**The operative case, so the headline matches it:** Wednesday is filing a card and
`decision_queue.sh add` REFUSES it, naming a card Kam has already ruled on the same subject
words. **There are two lazy exits and both are wrong.** Re-running with
`--override-prior-rulings` because the finding *feels* different is the expensive one; dropping
the card because he *seems* to have ruled it is the quiet one, and it is worse, because nobody
ever learns the finding existed. **The correct move is a measurement: open the artefact the
prior ruling was shipped into, and read what the fix actually CHANGED.**

## The case

The NexusAI seat (S45) reported that `Notes (MASTER)/skills/Current/end-of-session.md` tells
every session to run `git add -A` in the vault, and that the vault held four Secuura files — so
a Datasec seat following the documented ritual would commit another client's content. Wednesday
verified it and went to card it.

**The gate refused**, naming `fleet-vault-note-attribution` — ruled `adopt` by Kam on
2026-09-04, **shipped the same day** as vault commit `b830104`, with a `ruling_note` reading
*"Step 1b of the shared end-of-session skill now derives attribution from `git diff --cached`."*

On the card's face this was the same subject: the same file, the same step, the same ritual,
ruled and shipped three days earlier. **Wednesday was one keystroke from recording a live
cross-client trap as already-handled.**

**What settled it was reading `git show origin/main:<the skill>`.** Kam's fix is present, at
line 56. It derives *who the commit names*. **Lines 23 and 50 still say `git add -A`.** His
ruling changed the **attribution**; it never touched the **staging scope**. Two different
changes to one step of one file — and the card, the title and the ruling note were all accurate
about the first while being silent about the second.

**A second finding fell out of the same command,** and it could not have been reached any other
way: `b830104` is an ancestor of `origin/main` and **is not** an ancestor of this drive's HEAD.
The vault here is 1 ahead / 450 behind and cannot pull. **So every agent booting from this drive
reads a wrap ritual that lacks even the fix Kam already paid for.**

## Why the existing lessons did not fire

[[2026-08-14_i-read-representations-they-read-sources]] says go to the source. It fired for the
FINDING — Wednesday measured the file list and the staging verb first-hand. It did not fire for
the **prior ruling**, because a ruling felt like a settled fact rather than a claim, and its
`ruling_note` was written by Wednesday, which makes it feel like a memory rather than a
representation. **It is a representation.** A note saying "SHIPPED" is a claim about a diff.

[[2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact]] is the neighbour and
it points the other way: it asks whether a ruling REACHED an artefact. **This asks the next
question — once it reached one, what did it change there?** Delivered and sufficient are
different properties, and only the second one closes a subject.

## How to apply

1. **On any prior-ruling refusal, open the artefact before deciding anything.** `git show
   <ref>:<path>` on the file the ruling shipped into, and read the lines the new finding is
   about. Cheap, decisive, and it is the only thing that discriminates.
2. **Read the ruling's SCOPE, not its subject.** "He ruled on the vault staging step" and "he
   ruled on attribution within the vault staging step" are different facts that share every
   keyword. **The gate matches on words; only the diff matches on scope.**
3. **A `ruling_note` is a representation of a diff, including one Wednesday wrote.** Own
   authorship makes it feel like memory. It is a claim with a date on it.
4. **State the override's reason as the MEASUREMENT, in the BLUF.** Not "this is different" but
   *"his fix added attribution at line 56 and left `add -A` at line 50 — I read origin's copy."*
   That sentence is what lets Kam check the override in one read instead of trusting it.
5. **The refusal is a dividend, not a cost.** It bought a sharper finding and a second one
   nobody was looking for. **Treat a gate that stops you as a question it is asking**, and
   answer the question rather than routing around it
   ([[2026-08-09_an-enforcement-you-must-arm-is-not-one]] — in-path enforcement works, and this
   is what "working" looks like from the inside).

**Family:** [[2026-08-14_i-read-representations-they-read-sources]] (the parent — a ruling note
is a representation) · [[2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact]]
(delivered ≠ sufficient) · [[2026-08-16_a-recorded-blocker-is-not-a-boundary]] (clearing the
stated blocker is the start of the check) · [[2026-09-07_a-rule-for-creation-is-not-a-mandate-to-retrofit]]
(read the verb in his rule — this is: read the diff of his fix) ·
[[2026-09-07_a-census-complete-over-a-frame-that-is-not]] (the ruling was complete over
attribution and silent about staging — the same shape, in a card).
