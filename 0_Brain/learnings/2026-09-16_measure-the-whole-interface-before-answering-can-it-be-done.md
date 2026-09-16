---
date: 2026-09-16
type: correction
status: live
tier: W
source: Tuesday, 2026-09-16 — told Kam the live marketplace offer was undeployable; the NexusAI agent corrected it
ledger: _ledger_laptop_datasec.md 2026-09-16
---

# "Can this be done?" is answered by the whole interface, not by the part you suspected

**The lesson:** Kam asked whether a third party could deploy the live Azure Marketplace offer. There
was an existing card pointing at the container image, so the image is what got measured — thoroughly,
and correctly. `createUiDefinition.json` line 59 defaults customers to a dev registry; line 71 names
that registry; an unauthenticated token request to it returns `UNAUTHORIZED`, with a positive control
proving the method. Every one of those facts was true, and the conclusion drawn from them —
"no third party can deploy it" — was **wrong**.

Four lines below the two that were quoted sat `acrUsername` and `acrPassword`: both **required**, both
with **no default**, labelled *"Datasec-supplied scope-map token name with pull access"*. The registry
is private **by design**, with an enabled pull-only customer token. With it, the customer-path pull
returns HTTP 200. The correct answer was *"not **unaided**"* — a commercial gap, not a broken build,
and a far smaller and more fixable thing than what was reported.

The project's own agent caught it, having read the same file without a hypothesis about what mattered
in it.

**Why the method failed, precisely:** a prior card named the image as the suspect. Measuring the
suspect answers *"is the suspect guilty"*. It does not answer *"can the customer get in"*. The
question was about an **outcome reachable through an interface**, and an outcome is decided by every
input the interface requires — not by the one input someone had already flagged.

**How to apply:**

1. **When the question is "can someone do X", enumerate the entire interface first** — every field,
   every required input, every default — and only then look at the item you suspect. For a wizard,
   a form, an API or a CLI, that is one pass over the schema and it is cheap. Enumerating the
   submitted package's fields took one command and would have prevented the whole error.
2. **Treat an inherited card or ticket as a pointer, never as a scope.** It tells you where someone
   previously looked. It is silent about everything they did not.
3. **A measurement with a positive control is still only a measurement of what it measured.** The
   control proved the registry genuinely refuses anonymous clients. It could not tell anyone that the
   wizard supplies credentials. Rigour about a fact does not extend the fact's reach, and confidence
   earned on the part transfers to the whole only if the whole was enumerated.
4. **Say the corrected shape, not just "I was wrong".** Here: the offer *is* deployable with a token
   Datasec hands over; it is *not* self-service; nothing in the listing or the wizard tells a customer
   where to get the token. The person acting on it needs the new true statement, and in this case it
   changed what would happen in a test the next morning.
5. **When another agent corrects you, take it to the principal as your own error and credit them.**
   Kam had been told something false by this seat, and he was going to act on it.

**The shape this belongs to:** the same evening produced three defects that were each *correct where
they were authored and wrong where they were read* — a log path valid on one machine, a usage cap
valid for one account, a check reading a file instead of the running system. This is that family
turned inward: a fact measured correctly in one place, then asked to carry a conclusion about a place
it never covered.
