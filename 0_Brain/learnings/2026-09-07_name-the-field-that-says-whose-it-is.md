---
date: 2026-09-07
type: correction
source: Kam (ATTIO destination, 09:04) + Wednesday self-caught (KS-61 selection rule, 10:2x)
status: live
tier: W
---

# Anything Wednesday commissions names the field that says WHOSE it is — not only what will change

**The operative case, so the headline matches it:** Wednesday is about to write a card, a brief, a
GO, or **a RULE an agent will apply on its own**. The artefact says what will change. **Stop and ask
the one question none of them asked twice in one day: *and whose is it, and where does it land?***
If a reader could not answer that from the artefact, the field is missing — and the field is the one
that decides authority, so its absence is not a gap in detail, it is a gap in consent.

## The two cases, twelve hours apart, same root cause

**1 — Kam-caught, 2026-09-07 09:04.** He approved an Attio schema change on its merits at 07:07 —
one attribute, the cap lifted by exactly one. At 09:04: *"I approved ATO push, but did not realize
that this was going to the Datasec repository. This cannot happen in the future."* **Every artefact
in the chain described WHAT would change and not one named WHERE it would land** — not the card, not
the brief, not the dry-run review, not the GO. Wednesday held the destination
(`git@github.com:datasecau/attio.git`) and never surfaced it. Measured afterwards and offered as
context rather than defence: the repo had been Datasec's for 17 days and 51 commits, and every other
Datasec project uses the same org. **"It followed the existing arrangement" is not consent — it is
exactly the thing an approval exists to interrogate.**

**2 — self-caught, 2026-09-07 10:2x, hours after the fix for case 1 shipped.** Wednesday delegated
ticket SELECTION to the Secuura seat (s145) with a five-clause rule: highest priority · needs no
**input** from a client human · touches no file on a branch under gate · not already In Review ·
closable in one session. **It never named the ASSIGNEE field.** The seat applied the rule correctly
and committed to **KS-61, which is assigned to Stuart** — against Kam's ruling of 2026-09-06 10:24:
*"once something is assigned to someone it belongs to them. the ruling was only to new or unassigned
items."* Caught by reading the seat's pane minutes in; stopped before any push, comment or
reassignment; the seat's derivation work quarantined rather than reverted, because it may be usable
the moment Kam says we may take the ticket.

## Why the morning's fix did not fire on the afternoon's instance — the w=2 diagnosis

Case 1 was promoted **into the artefact** the same action, which was right. The line read: *"any
card, brief or GO whose consequence is a COMMIT states the remote and the branch in the BLUF."*

**A selection rule's consequence is not a commit. It is taking someone's ticket.** So the promoted
enforcement was scoped to the costume the incident happened to wear, and the next instance wore a
different one. This is [[2026-08-13_headline-must-match-the-operative-case]] operating **on an
enforcement line rather than on a lesson**: the handle said *commit*, the missing field was
*assignee*, and nothing in between matched.

**The general lesson about promotions, which is the more valuable half:** when a failure is promoted
into a standing line, **write the line from the CLASS, not from the incident.** The incident supplies
the evidence; it must not supply the scope. A line that names one costume will be read as covering
one costume — by an agent, and by the next Wednesday.

## How to apply

1. **Every card, brief, GO or delegated RULE states, in its BLUF, the field that decides whose the
   thing is and where it lands**, for whatever it commissions:
   - a **commit** → the remote and the branch;
   - a **deploy** → the environment and the subscription;
   - a **ticket** → the board **and the assignee**;
   - a **selection rule handed to an agent** → the **ownership predicate** ("unassigned, or on Kam's
     account; never Peter's or Stuart's");
   - a **message to a human** → who sends it (Kam) and on which channel.
2. **A rule that filters on DIFFICULTY while omitting OWNERSHIP will find the borderline item on its
   own.** Every clause of the KS-61 rule was about whether the work was *doable*; none was about
   whether it was *ours*. An agent optimising inside a rule will reach the edge of it — that is the
   agent working, not failing.
3. **When an agent follows a rule Wednesday wrote and lands somewhere wrong, the correction leads
   with whose error it is.** The STOP mail to s145 opened with *"this is WEDNESDAY'S error in the
   selection rule, not yours"* — because a seat that gets blamed for obeying will start hedging, and
   hedging is far more expensive than this mistake was.
4. **Stop, quarantine, do not revert.** Work done under a wrong instruction is not wrong work
   ([[2026-08-26_never-delete-cleanup-means-quarantine]]). It is held where it can be picked up if
   the ownership question resolves the other way.
5. **Test by its handle:** read only what the artefact says will change. If *"and whose is it?"* has
   no answer on the page, it is not ready to send.

**Family:** [[2026-08-16_classification-is-the-field-that-grants-authority]] (the parent — a scope
word is a measurement needing provenance; this is that lesson pointed at the OWNER field, which it
never named) · [[2026-08-13_headline-must-match-the-operative-case]] (why the promoted line missed) ·
[[2026-08-04_validate-brief-pointers]] (EXTENSION 2026-09-05: validate the EXTENSION of what a brief
commissions — a selection rule commissions a whole class of choices) ·
[[2026-08-03_role-beyond-code-three-priorities]] (his very-important #1: no cross-client leak — case
1 is that fear firing) · [[2026-09-02_coo-actionable-tickets-never-wait-for-kam]] (the 2026-09-06
assignment correction this violated).
