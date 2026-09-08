---
date: 2026-09-08
type: principle
source: the Secuura/Blockchain seat (s151), measuring the KS-577 / KS-843 collision from #880's diff
status: live
tier: M
---

# A decision stays on the page while the world moves under it — the dangerous change is not the one that contradicts a ruling, it is the one that removes the precondition the ruling's TRIGGER depends on

**The operative case, so the headline matches it:** a principal has ruled, the ruling is delivered
and sitting in its artefact, and a routine change is about to merge somewhere else. **Ask what the
ruling's chosen option DEPENDS ON — not what it says.** A ruling is a sentence plus a set of
conditions that made that sentence the right answer, and only the sentence gets written down.

## The case, measured

Kam ruled the KS-843 cutover **A — logged grace** on 2026-09-06, and the reason recorded on the card
is *"Never breaks S; no synchronised window with Stuart needed."* That property was not a property of
option A. **It was a property of a DEFECT** — KS-577, "rotation mints a new key but never revokes the
old one" — which happened to leave an overlap window during which the old key still worked.

KS-577's fix (PR #880) removes the overlap. Nothing in it contradicts Kam's ruling; it never mentions
it. **But with the fix merged and its grace at the ruled default of 0, the rotation option A depends
on kills S's key instantly, which is the exact outcome option A was chosen to avoid.**

**Two second-order effects, and they are the ones that generalise:**
1. **The failure moves UP the stack.** Revocation fails at authentication (401), above the scope gate
   the cutover is about — so the blast radius is every endpoint the party calls, not the feature
   under discussion. *A precondition removed at a lower layer breaks more than the layer that used it.*
2. **The ruling's TRIGGER stops being observable.** Option A flips to scope-only *"once the log shows
   S on the new key"*. With no overlap there is no transitional state, so that evidence can never
   accrue. **A ruling whose trigger condition can no longer occur is not a ruling that still works** —
   and it fails silently, because nothing errors; the condition simply never becomes true.

## Why the existing rules did not catch it

The delivery rule ([[2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact]]) was
**satisfied** — the ruling was on Linear KS-843, verified. Delivery answers *"can the next reader find
it?"* and the question here is *"is it still true?"* **A delivered ruling and a live ruling are
different properties, and only the first has a mechanism.**

**And the dependency WAS documented.** KS-843's author wrote it in the Related section, verbatim:
*"for this cutover it happens to provide the overlap window that makes a zero-downtime swap possible.
Named so nobody mistakes the convenience for a reason to leave it open."* **So the record was right
and the reader was missing.** The paragraph was findable from KS-843; it was not findable from KS-577,
which is the ticket somebody would be holding at the moment of the merge. **A dependency written at
only one end is discoverable only by whoever is already looking at that end.**

## How to apply

1. **When a ruling is recorded, record what it DEPENDS ON in the same action** — the condition that
   made the chosen option better, especially when that condition is a current defect, a temporary
   state, or somebody else's unfinished work. The card's reason field is where it belongs.
2. **Write the dependency at BOTH ends.** On the ruling's ticket AND on the ticket that would remove
   the precondition, each naming the other. **The end that matters is the one someone is holding when
   they merge**, and it is never the end you wrote it on.
3. **A defect that is load-bearing gets said out loud.** "This bug is currently doing useful work"
   is a sentence worth writing; the KS-843 author wrote it and was right to. It converts a silent
   dependency into a findable one.
4. **Before merging any fix, ask what currently RELIES on the broken behaviour.** Not who is affected
   by the bug — who is quietly benefiting from it. Cutovers, migrations, grace periods, retry loops
   and manual workarounds are the usual answers.
5. **Check the TRIGGER, not just the outcome.** For any ruling with a condition attached ("once X
   shows Y", "when the log confirms", "after they confirm"), ask whether the change makes that
   condition unobservable. **An unobservable trigger is a ruling that can never complete**, and it
   produces no error to notice.
6. **The remedy is usually a parameter, not a revert.** Here both fixes were config paths the fix
   itself already shipped. Look for those before proposing to hold the merge or change a default the
   principal ruled.

**Family:** [[2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact]] (delivered is
not the same as still true — this is the half that rule does not cover) ·
[[2026-08-16_a-recorded-blocker-is-not-a-boundary]] (a recorded condition is a claim with a date; this
is its mirror — a recorded DECISION rests on conditions with dates) ·
[[2026-09-06_a-scoped-override-carries-its-own-expiry]] (a ruling that expires by clock; this one
expires by someone else's merge) · [[2026-08-13_establish-authority-before-reconciling]] ·
[[2026-08-07_a-check-that-cannot-fail]] (a trigger that can never fire is its decision-layer twin).
