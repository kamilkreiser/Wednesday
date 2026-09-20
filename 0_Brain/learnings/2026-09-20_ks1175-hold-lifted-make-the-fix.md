---
date: 2026-09-20
type: grant
source: Kam, dashboard panel (view=wednesday), 2026-09-20 19:42:44 +10:00
status: live
tier: W
---

# KS-1175's hold is LIFTED and the answer was "make the fix", not the test — a card answered OUTSIDE its own options

**His words, verbatim:**
> *"Decision secuura-ks1175-testonly-pin-on-a-held-ticket note: remove the rule and make the fix"*

**The operative case, so the headline matches it:** Wednesday offered Kam three options on a held ticket — write the test-only pin (`go`), hold, or raise the pin under a new ticket. **He answered with none of them.** He removed the hold *and* redirected the work from the pin to the ticket's real fix. **A card's options are Wednesday's framing of the question; they are not the boundary of his answer.**

## What is lifted, and what is NOT

**LIFTED:** KS-1175's signature-class hold. It was named individually in `tasks/WEEK-INSTRUCTION.md:26` beside KS-1250 as *"anything IRREVERSIBLE — new fields on the immutable Cardano record"*. **That naming no longer binds KS-1175. KS-1250 is untouched and still his.**

**NOT lifted, because he did not name it, and stated back to him at 19:43 as Wednesday's reading:** building the fix and gating it changes nothing on any chain. **A new field only reaches the immutable record when something is DEPLOYED and an anchor is actually made.** That step keeps its own pause until he says otherwise. *Never argue an action into scope* ([[2026-08-07_protocol-v1.3-signed-delegation]]) — the lift reaches the build and the gate, and the burden is on him to widen it, not on me to read it wide.

## The work it redirects

The parked brief `night/briefs/KS-1175-STRIP-1.md.HELD-KAM-SIGNATURE-CLASS-do-not-queue` is **superseded, not resurrected**: it was written to PIN today's stripping behaviour, and he has asked for the behaviour to CHANGE. The real fix is the ticket's own — `anchorSchema.ts` accepting and anchoring the non-PII actor and organisation identifiers instead of stripping them — which is a multi-file product change and therefore **a Claude seat's job, not the local model's** (the round-22 writer rejected it as multi-file by its own fix shape, correctly).

## How to apply

1. **Read the scope field, not the option list.** When Kam answers a card with a `note:` instead of a key, the note IS the ruling and it may be wider than anything offered. Record it verbatim before interpreting it.
2. **State the reading back in the same action** (done, 19:43 panel), with the part being treated as still-his named explicitly. He corrects in seconds; a silent wide reading corrects in incidents.
3. **A lifted hold lifts ONE ticket.** KS-1250 is still named and still pauses. Do not generalise "he lifted a hold" into "the class is open".
4. **The mechanism could not record it** — see the ledger row of the same date: `reconcile_rulings.py` parses `Decision <id>: <key>` and his `note:` form is not a key, so his ruling did not reach the card and would have evaporated. Recorded by hand into this file, the card's withdrawal reason and the pickup. **The reconciler fix is OWED.**

**Family:** [[2026-09-06_a-scoped-override-carries-its-own-expiry]] (no expiry stated here — said so rather than assumed) · [[2026-08-07_protocol-v1.3-signed-delegation]] (what a grant does and does not reach) · [[2026-09-14_kams-instruction-stands-until-he-withdraws-it]] · [[2026-08-16_an-ask-without-a-default-is-an-indefinite-hold]] (the card carried a default; he answered past it) · [[2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact]].
