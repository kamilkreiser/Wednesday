---
date: 2026-08-04
type: correction
source: "w=2 ledger promotion: (1) Peter to-do type mis-asserted in the consent micro-brief; (2) Tokenomics brief pointed tenant verification at the stale client CLAUDE.md — a file that was itself under repair"
status: live
tier: W
---

# Validate what a brief points AT, not just what it asserts

**The failure class (two occurrences, same day):** the delegation-protocol
rule "validate every fact in a brief against the live source" fired for facts
I *asserted* — but not for **pointers**: places I sent the agent to verify
things for themselves. Occurrence 2 was the sharp one: the Tokenomics
stale-tenant brief said "verify the current tenant from the client
CLAUDE.md's tenant section" — but that file was one of the two artifacts
being repaired *because its tenant section is stale*. Circular ground truth;
the agent had nowhere authoritative to stand.

**Why the existing rule didn't fire (w=2 diagnosis):** paths-over-content
(a good rule — paths stay fresh) made pointing feel inherently safe. It
isn't: a pointer is an implicit assertion that *the target is fit to answer
the question*.

**How to apply:**
1. For every "verify X from Y" in a brief: open Y first (read-only) and
   confirm Y actually answers X correctly TODAY. If I can't check Y, say so
   in the brief honestly ("Y may itself be stale — cross-check against Z").
2. **Repair-object rule:** if Y is part of what the brief asks the agent to
   fix, Y is disqualified as ground truth for that fix. Name an independent
   source (a sibling project's fixed artifact, live `az account show`,
   4_Credentials state).
3. Withholding facts from a brief (as I did with tenant IDs, rightly wary of
   asserting unverified ones) obliges me to ensure the verification path I
   name instead is sound — otherwise I've swapped a checkable wrong fact for
   an unfalsifiable dead end, which is worse.

**Related:** [[_ledger]], [[../skills/delegation-protocol]],
[[2026-08-03_mental-model-not-source-of-truth]]

## EXTENSION 2026-09-05 (w=2): validate the EXTENSION of what a brief commissions, not only the existence of what it points at

**The case.** Two briefs on one morning, both caught by the receiving agent: the s125 brief queued two Platform S merges for a Platform K seat (the seat's scope — the client CLAUDE.md isolates Platform S), and it queued "fix the MFA bypass on `POST /api/oauth/authorize`" for KS-781, whose own BLUF names THREE token-issuing doors kept as one ticket. Both facts were validated the way this lesson and the send_brief gate demand — the ticket exists, it is open, its last comment is dated — and both were wrong about *how much* was being commissioned and *whose* it was to do.

**The rule, extended:**
1. **A QUEUE item on a ticket carries the ticket's SCOPE sentence** (its BLUF, quoted) in the provenance line — not only its state. If the brief commissions less than the ticket (one door of three, one leg of a migration), it says so as narrowing: "door 1 of 3 this round; doors 2–3 tracked as sub-issues before door 1 merges." A brief that is narrower than its ticket without saying so produces a ticket that closes on a fraction.
2. **A QUEUE item carries the receiving seat's AUTHORITY over it** — read from the client's own CLAUDE.md (coupled pairs, isolated projects) before the item is written. "Author to merge" on a reviewer's board says who is expected to merge, not which seat may.
3. **Enforcement candidate (w=3 would promote it):** send_brief refuses a queued ticket id whose provenance line lacks a `scope:` clause; and refuses a repo/PR reference outside the `<Client>/<Project>` the brief is addressed to unless the client CLAUDE.md declares the pair.

**Family:** [[2026-08-13_headline-must-match-the-operative-case]] (a ticket's title said one route; its operative case said three) · [[2026-08-13_shared-bus-tag-filter-or-leak]] (client isolation is a property of the seat, not of the task's size).

## EXTENSION 2026-09-05 21:3x (w=2): a mail that changes an earlier instruction NAMES it and says SUPERSEDES — the self-check reads the PREVIOUS mail to the same agent, not only the mail in hand
**The case.** Wednesday's 11:18Z GO told s131 to rebase #822 after #821 and mail the head; the 11:22Z ANSWER, four minutes later, said #822 rebases after its tier-2 verdict lands. Neither mail named the other. s131 had already acted on the first, finished the push rather than stop mid-flight, and flagged the conflict — the 18:5x seat's w=1 (two brief items colliding) in a new costume: the two items were in two mails.
**The rule, extended:**
1. **Before sending anything to an agent that sequences, holds or releases a thing already sequenced (a PR, a ticket, a deploy), re-read the previous outbound to that agent for the same id.** If the new sentence changes it, the new mail says so by name: *"supersedes item 3 of the 11:18Z GO"*. A silent change is a contradiction the agent has to adjudicate mid-turn.
2. The SELF-CHECK line's scope is now: Kam's rulings · the mail against itself · **the previous mail to this agent on every id this mail names.**
3. **Enforcement candidate (w=3 promotes it):** `send_brief.sh` keeps the last outbound per project; when a new body carries a sequencing verb (rebase / merge / after / before / hold / release) on a PR or ticket id that the previous body also sequenced, it refuses unless the body contains `SUPERSEDES`.

