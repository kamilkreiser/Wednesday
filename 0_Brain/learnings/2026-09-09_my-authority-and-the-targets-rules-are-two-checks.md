---
date: 2026-09-09
type: correction
source: s157 refusing a merge Wednesday ruled; verified in Secuura/Blockchain/CLAUDE.md
status: live
tier: W
---

# "Am I allowed to?" and "does this project allow it?" are two different checks, and I have only ever run the first

**The operative case, so the headline matches it:** Wednesday is about to rule an action
**inside a client project** — a merge, a branch policy, a file move, a process change.
**Before ruling it, open THAT PROJECT'S OWN `CLAUDE.md` and read what it says about the
action.** Wednesday's authority answers whether *Wednesday* may direct the thing. It says
nothing about whether the project permits the thing **at all**, by anyone.

## The case

The tier-1 gate passed #914 `GO WITH FINDINGS`. Wednesday validated three things and ruled
the merge:

1. **the gate's verdict** — read in full, 19 KB, findings weighed;
2. **the branch topology** — measured, and the reason the one-line F-2 fix could not go on
   that branch;
3. **its own authority** — Kam's week-scoped merge grant, live through 2026-09-13.

**All three were right. The merge was still wrong.** `Blockchain/CLAUDE.md` carries a flow
Kam adopted on 2026-08-25:

> line 225 — **"The ticket and the review must not sit with the same person."**
> line 226 — **"No approval → no merge. Never push straight to `develop`."**
> line 246 — **"'no approval → no merge' is a rule we keep, not one GitHub enforces —
> nothing technical stopped #731 being self-merged unapproved."**

#914 and #915 carried **zero reviews**. The seat refused, and its framing is the lesson:
*"that is a question about what Kam's grant covers, and it is not mine to answer by
merging."* It is not Wednesday's to answer by ruling, either.

## Why the existing lessons did not fire

**[[2026-08-16_a-recorded-blocker-is-not-a-boundary]] rule 2 already distinguishes two
questions** — *"Can I?"* (a permission API) and *"should this be me?"* (enumerate the
consumers). **This is a THIRD, and neither of those two reaches it: "does the thing I am
acting on have its own rules about this action?"** A permission check and a consumer
enumeration can both come back clean while the target's own constitution forbids it.

**And the retrieval handle missed because the artefact is one Wednesday reads at BOOT.**
The workspace `CLAUDE.md` and Wednesday's own are loaded every session; a *client
project's* `CLAUDE.md` is not, and nothing in the ruling moment points at it. **It is
read when working IN a project and forgotten when ruling ABOUT one.**

## How to apply

1. **Before ruling any action inside a client project, open that project's `CLAUDE.md`
   and grep it for the verb** — merge, push, deploy, delete, branch, release.
   `grep -niE 'merge|approval|push|deploy' <project>/CLAUDE.md` is one command and it is
   the one that was not run.
2. **Two independent checks, both required, neither sufficient:** *my authority permits me
   to direct this* **AND** *the project permits this to be done at all*. **They fail
   independently** — here the first passed cleanly and the second forbade it outright.
3. **A grant from the principal about MY authority does not silently amend a convention
   the same principal adopted for a project.** Reading it that way is arguing an action
   into scope ([[2026-08-07_protocol-v1.3-signed-delegation]] — *"if it needs a clever
   reading of the grant, it is outside it"*), and it makes me **the sole author of the
   authority**, which v1.3 excludes by name.
4. **A rule that nothing technical enforces binds harder, not softer.** Line 246 says so
   explicitly and names the PR that was self-merged because nothing stopped it. **Where a
   convention survives only because people decline to do the easy thing, doing the easy
   thing destroys it** — and the coordinator doing it destroys it fastest, because every
   agent takes the precedent.
5. **When two of the principal's own rulings are in tension, that tension is HIS to
   resolve, and it goes to him as a card with the tension named** — not resolved by
   picking the one that unblocks the work. **The one that unblocks the work is exactly the
   one to distrust** ([[2026-08-16_classification-is-the-field-that-grants-authority]]
   rule 4).

## The uncomfortable part, kept

**Nothing technical would have refused that merge.** Branch protection enforces nothing on
this repo — measured and recorded in the same file. The only thing between a ruled merge
and a broken convention was **an agent willing to tell its coordinator no**, and it is the
fifth time in one day a Secuura seat has done exactly that. **The system's own instruments
were all green: gate passed, topology measured, authority live.** They were pointed at
three real questions and none of them was the one that mattered.

## Related

[[2026-08-16_a-recorded-blocker-is-not-a-boundary]] (the two questions this adds a third to) ·
[[2026-09-07_a-rule-for-creation-is-not-a-mandate-to-retrofit]] (read the verb in his rule —
here, read the rule at all) · [[2026-08-07_protocol-v1.3-signed-delegation]] (never argue an
action into scope) · [[2026-08-21_challenge-me-when-you-think-im-wrong]] (symmetric — the
argument that survives wins, and here it was the agent's) ·
[[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (its inverse: an enforcement that
exists only as a convention).
