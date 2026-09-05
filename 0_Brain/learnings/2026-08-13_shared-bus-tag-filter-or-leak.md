---
date: 2026-08-13
type: correction
source: "Datasec/HPSM session 9 self-disclosed: its drain-watch script filtered coagent@ on `'ANSWER' in subject` WITHOUT requiring the `Datasec/HPSM` tag; coagent@ is the SHARED fleet bus, so the first ANSWER to arrive was SECUURA's, and the script captured its headers + ~400 chars of body into the Datasec session's scratchpad. Contained same-session (scrubbed, script deleted, grep-clean, fragment never used); disclosed unprompted."
status: live
supersedes: ""
tier: W
---

# Any agent polling the SHARED bus must filter on its own project tag — or it will read another client's mail

**The breach (hard rule 2, cross-CLIENT, in effect):** the shared
`coagent@agentmail.to` bus carries every project's traffic. An HPSM (Datasec)
automated poller filtered inbound mail on message CLASS (`'ANSWER' in subject`)
but not on RECIPIENT (`Datasec/HPSM` in subject). The first ANSWER to land after
the cap reset was Secuura's — so a Datasec session captured a Secuura message's
headers and first ~400 characters into its own scratchpad and task output.
Accidental, automated, and exactly Kam's "very important #1" (no cross-client
leak — *"it would be embarrassing or worse if Datasec had Secuura's name in
it"*, [[2026-08-03_role-beyond-code-three-priorities]]).

**Why it is worth a lesson and not just a ledger row:** it is STRUCTURAL, not a
one-agent mistake. Every project agent polls the same shared bus at boot and at
checkpoints (the fleet-comms protocol tells them to). Every one of them has this
exact exposure the moment it filters on subject-class without the project tag.
The HPSM agent's own framing was right: *"this is a fleet-protocol gap, not an
HPSM bug."* One agent fixing its own script fixes nothing fleet-wide.

**The class rule (goes into every brief's protocol section + the fleet-comms
guidance when Kam approves the shared-file edit):**
1. **Any automated read of `coagent@` (the shared bus) MUST filter on the
   project's own tag** — `[<Client>/<Project> ->` for that exact project, or
   `[Wednesday -> <Client>/<Project>]` inbound — BEFORE touching a message's
   body. Class-only filters (`QUESTION`/`ANSWER`/`wrap`) are necessary but never
   sufficient on a shared bus.
2. **Prefer the project's OWN inbox over the shared bus** where one exists.
   `wednesday-agent@` is Wednesday's; the structural end-state is each project
   reads a per-project inbox and the shared bus is retired. Until then, tag-filter.
3. **Wednesday's own automated reads are not exempt** — my drain-watcher and any
   inbox poller I write filter on the intended recipient, not just the class.
   (My own 08-13 drain script filtered outbound-vs-inbound but reads the WHOLE
   shared inbox; that is fine for MY session because I coordinate all clients,
   but it is the exact pattern that is unsafe inside a single-client agent.)

**The escalation (a promise is not a mechanism):** the durable fix is either
per-project inboxes or an explicit "filter on your project tag" line in the
workspace `CLAUDE.md` fleet-comms section — and that file is shared across
clients, so amending it is Kam's call, raised as a decision item, not a
unilateral edit from Wednesday or any project session.

**What went RIGHT and must be protected:** the agent caught it by its own
verification, contained it in the same session, disclosed it unprompted, and
correctly diagnosed it as systemic. That is why session 9 still scored 1.0 —
self-caught, contained, honestly-disclosed breaches are what the scoreboard
protects; penalising the disclosure teaches hiding
([[2026-08-07_we-each-have-strengths]] — retract without embarrassment).

**Related:** [[2026-08-03_role-beyond-code-three-priorities]] (no cross-client
leak = severity-max), [[2026-08-04_delegation-v2-observability]] (R0: client
contexts structurally unable to leak — this is R0 failing at the comms layer),
[[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (a tag-filter you must
remember to write is not one — bake it into the poller template), [[_ledger]]
