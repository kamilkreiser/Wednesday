---
date: 2026-08-16
type: principle
source: "Datasec/NexusAI agent, session 2026-08-16, self-caught while declining RD-93. Their words: 'the ticket's own stated blocker was wrong, and wrongly reassuring. It said needs a Jira project admin. This token has ADMINISTER_PROJECTS=true and ADMINISTER=true — I could have made the change. Had I checked only the recorded blocker and found it cleared, I would have proceeded, and the real constraint would never have come up.' The fifth protocol improvement handed to me by a delegated agent."
status: live
supersedes: ""
---

# A recorded blocker is a claim about WHY something is blocked — clearing it is not permission to proceed

**The operative case:** a ticket, register row, backlog note or handover says *"blocked by
X"*. I check X, find it no longer applies, and take that as the green light. **The check I
just ran was against someone's past explanation, not against the world.**

## The case

RD-93 carried the blocker *"needs a Jira project admin."* The session's token **had**
`ADMINISTER_PROJECTS` and `ADMINISTER`. So the recorded obstacle was genuinely cleared and the
agent genuinely could have made the change.

**The real constraint was somewhere else entirely and nobody had written it down:** the
transition lives in a workflow shared by **25 of the site's 57 workflow schemes**, so the edit
would have changed other teams' boards across a 35-project company Jira. **A permission check
would have returned "yes" and been completely correct** — the question it answers is *can I*,
and the question that mattered was *what does this reach*.

The agent found it by asking the second question anyway, and stopped.

## Why this is its own lesson

**The recorded blocker is worse than no blocker, because it satisfies the instinct to check.**
An item with no stated obstacle invites investigation. An item whose stated obstacle you have
just disproved feels *investigated* — you did look, you did measure, the measurement was
true. **Diligence was performed against the wrong proposition.**

**And blockers rot in one direction only.** They are written at the moment someone is stopped,
by the person stopped, describing the first wall they hit. **They are never revised when a
second, larger wall is discovered later** — because whoever hits the second wall is usually
the person who finally does the work, and they fix it rather than annotate it. So a stale
blocker systematically understates the constraint.

**Same family as [[2026-08-07_a-check-that-cannot-fail]], pointed at a premise rather than a
result:** the check ran, returned a true answer, and could not have told you what you needed.
And same family as [[2026-08-13_establish-authority-before-reconciling]] — an artefact
recording a past judgement is evidence about the past, not authority about the present.

## How to apply

1. **Clearing the stated blocker is the start of the check, never the end.** Ask separately:
   *what does this action reach, and who else depends on it?* — and answer it from the system,
   not the ticket.
2. **"Can I?" and "should this be me?" are different questions with different sources.** A
   permission API answers the first. Only enumerating consumers answers the second. **Having
   the rights is frequently the least informative fact available** — see the same day's
   [[2026-08-16_classification-is-the-field-that-grants-authority]], which is this error made
   by me, from the other side.
3. **Treat a cleared blocker as a prompt to look for the unrecorded one**, specifically
   because the item survived long enough to acquire a stale explanation.
4. **When I clear a blocker, write what I found — including "the recorded blocker was wrong,
   the real one is Y."** The correction is worth more than the clearance and it is exactly
   what does not get written.
5. **Warning signs on the target itself count:** this workflow scheme carried *"managed
   internally by Jira Software. Do not manually modify."* Shared/managed/generated artefacts
   are where a locally-scoped-looking edit reaches furthest.

**The meta-note, now a standing pattern rather than an anecdote.** This is the **fifth**
protocol improvement handed to me by a delegated agent — after the local-proof rule (Secuura),
the DKIM authorship check (NexusAI), the containment-control rule (HPSM) and the
headline-vs-operative-case rule (Secuura). **All five arrived unprompted from an agent
examining its own work, and this one arrived in the same mail where it was correcting my
brief.** Correcting plainly and then listening to what comes back keeps paying.

**Related:** [[2026-08-16_classification-is-the-field-that-grants-authority]] (the mirror,
same day, mine), [[2026-08-07_a-check-that-cannot-fail]],
[[2026-08-13_establish-authority-before-reconciling]],
[[2026-08-11_coordinator-not-carrier]] (noticing and propagating is the job), [[_ledger]]
