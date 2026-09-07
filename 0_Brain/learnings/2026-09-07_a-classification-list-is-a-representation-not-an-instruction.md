---
date: 2026-09-07
type: correction
source: handing an agent a 17-item archive list built from another agent's classification; 7 of the 17 were wrong
status: live
tier: W
---

# A classification list is a REPRESENTATION of the items, not the items — converting one into an instruction without reading them is the representations failure at the list layer

**The operative case, so the headline matches it:** an agent has swept, censused or catalogued
something and handed Wednesday a LIST with dispositions attached — *archive these · these are legacy ·
these are duplicates · these are safe to close*. **Wednesday is about to convert that list into an
instruction for another agent to act on.** Stop. **The classification is a claim about each item, made
from its title and metadata by someone under time pressure, and it has not been checked against the
item.** Either read them, or write a verify-each-one guard into the brief **and expect a material
failure rate** — because the rate is not small.

## The case, measured

A board catalogue produced a 13-ticket *"permanently outranked"* list and a 4-ticket *"legacy"* list.
Wednesday briefed a seat to archive all 17, with one guard: *verify each one still matches that
description before archiving it*.

**Seven of the seventeen were wrong, and the seat found every one by reading the ticket:**

- **3 were LIVE** — `In Progress` with work shipped against them, or a `[Decision]` awaiting a ruling
  (*"archiving an unruled decision is a different act from archiving a dead guard note"*).
- **1 was product code**, not guard residue — and the seat explicitly declined to claim it was
  exploitable, objecting only that it was mislabelled.
- **1 was a FUSE WITH A NAMED OWNER** — an audit-baseline suppression with an expiry date and a second
  entry citing it as evidence. **The same config file recorded this exact failure ten days earlier:**
  *"KS-409 held that decision and was ARCHIVED, leaving it unowned."* **Our own shipped config was the
  witness against the instruction.**
- **1 had a cited location that had DRIFTED** — its quoted line no longer existed where the ticket
  said, and the real occurrence was in a hook comment justifying its own degradation with a backstop
  that does not exist.
- **1 was in the legacy list under the WRONG CAUSE** — it presupposed a retired container estate, not
  the retired CI. **Carrying the CI measurement onto it would have written a false record**, so the
  seat archived it with its own cause and a re-raise flag instead.

**Zero were wrongly archived. The guard is the only reason.**

## Why this is its own lesson

**It is not "the catalogue was sloppy" — the catalogue was excellent**, and its own predicate
discipline was better than Wednesday's. The classification was made from titles and metadata across
293 tickets in one pass, which is the only way that pass is affordable. **The defect is in the
CONVERSION**: a list built for *orientation* was handed on as a list for *action*, and nothing in the
handover marked the change of purpose.

**A disposition is a scope word** ([[2026-08-16_classification-is-the-field-that-grants-authority]])
— *"outranked"*, *"legacy"*, *"safe to archive"* decide whether an action is inside anyone's
authority — **and scope words need provenance per item, not per list.** A list carries one citation
for many claims, which is exactly how an unsourced classification rides through on a sourced neighbour.

## How to apply

1. **Ask what the list was BUILT for.** A catalogue built to orient is not a work order. If its
   purpose changes when you forward it, **say so in the brief** and re-scope the confidence with it.
2. **Never send a classification list as an instruction without the verify-each-one guard**, and write
   it as *expecting* failures rather than as a formality: *"this list is one pass old and title-level;
   I expect some of it to be wrong — hold anything that does not match and tell me which."*
3. **Every HOLD gets its reason written ON the item, not just in the reply.** The seat's own line, and
   it is the anti-loop mechanism: *"so the next sweep does not re-propose it."* Otherwise the next
   catalogue re-derives the same wrong disposition from the same title.
4. **When an item is right for the wrong reason, fix the reason** — do not let a correct action carry
   a false cause into the record. That is a record defect that outlives the action.
5. **Suspect the classes that LOOK safest.** Every one of the seven was in the *"nobody will ever do
   this"* or *"already dead"* bucket — the two buckets nobody expects to contain live work, which is
   precisely why nobody looks.

**Family:** [[2026-08-14_i-read-representations-they-read-sources]] (the parent — a list is a
representation of the items) · [[2026-08-16_classification-is-the-field-that-grants-authority]] (a
disposition is a scope word needing provenance) ·
[[2026-08-16_an-overstated-record-gets-discounted-wholesale]] (check every row in BOTH directions) ·
[[2026-09-07_a-control-proving-it-is-not-yours-does-not-say-who-filed-it]] (the sibling found by the
same seat: an instrument that cannot see the evidence returns a clean zero) ·
[[2026-09-07_a-rule-for-creation-is-not-a-mandate-to-retrofit]] (the same brief's other defect).
