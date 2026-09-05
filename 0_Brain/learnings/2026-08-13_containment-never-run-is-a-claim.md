---
date: 2026-08-13
type: principle
source: "Datasec/HPSM agent, session 16, self-caught while building the Monday deck: `INCLUDE_ANNEX = False` stripped the annex SLIDES and shipped the internal reasoning anyway in the SPEAKER NOTES — including a payment-schedule defect in a document HP holds. It had already written a slide asserting that route 'produces a file that never contained the annex'. Their formulation."
status: live
supersedes: ""
tier: M
---

# A containment control that has never been run is a claim, not a control — and the quiet channel is where it leaks

**The case.** A deck was built in two parts: a client-facing narrative and an
internal annex holding everything a client must never see — defects in the
client's own contract, past-due obligations, commercial exposure. The build had
a switch, `INCLUDE_ANNEX = False`, whose entire purpose was to produce a
client-safe file. It removed the annex *slides*. It left the internal reasoning
in the **speaker notes**, which travel inside the same file. Three client-facing
notes referenced the annex; one carried an arithmetic defect in the client's own
payment schedule.

The agent found it by **running the switch** while writing the slide that
described it. The slide already claimed the route produced a clean file. That
claim was false at the moment it was written.

**Why this is its own lesson and not just another instance of
[[2026-08-06_exercise-mechanisms-before-arming]].** That lesson says: run a new
mechanism before arming it. This adds the specific reason containment mechanisms
fail differently from other mechanisms:

1. **A containment control is judged on what it REMOVES, and absence is the
   hardest thing to see.** A watcher that fails is noisy. A redaction that fails
   looks exactly like a redaction that worked — until it reaches the wrong
   reader, when the cost has already been paid.
2. **The leak is never in the loud channel.** The annex divider here was
   deliberately unmistakable, and it worked perfectly. What leaked was the
   channel nobody looks at: speaker notes, document metadata, alt-text, comments,
   revision history, embedded objects, filenames, the summary field of an
   attachment. **Whenever content is split into "shown" and "hidden", enumerate
   every carrier the file has, not just the visible surface.** (Same family as
   [[2026-08-07_enumerate-every-surface-before-done]], pointed at a single
   artefact rather than a codebase.)
3. **Documenting a control is how you convince yourself it exists.** Writing the
   sentence "this produces a clean file" is subjectively identical to having
   verified it. The agent was one keystroke from shipping the assertion instead
   of the test.

**How to apply:**
1. **Exercise every containment mode before claiming it** — build the redacted
   artefact, then inspect the OUTPUT for the content that should be gone,
   searching every carrier the format supports. Never inspect the source and
   infer the output.
2. **Fix the mechanism, not the wording.** The right response here was a
   build-time marker plus a verifier that FAILS when a client-safe note matches
   an internal pattern — so the claim cannot be quietly wrong again. Correcting
   the sentence would have left the next build to chance.
3. **Assume the check runs on the artefact a stranger receives**, not on the one
   you built. Attachments, exports and "safe copies" all carry more than their
   visible content.
4. **Applies well beyond decks:** redacted documents, sanitised logs, demo
   datasets, screenshots (window titles, notification banners), exported CSVs,
   anonymised tickets, and any "internal vs external" split in a single file.

**The meta-note worth keeping.** This is the third protocol improvement a
delegated agent has handed the fleet — after the local-proof rule and the DKIM
authorship check. All three arrived unprompted, from an agent doing its own work
carefully, and all three were better than what the coordinator would have
written. Noticing and propagating them is the job
([[2026-08-11_coordinator-not-carrier]]).

**Related:** [[2026-08-06_exercise-mechanisms-before-arming]] (parent),
[[2026-08-07_a-check-that-cannot-fail]], [[2026-08-07_enumerate-every-surface-before-done]],
[[2026-08-06_local-proof-is-not-target-evidence]], [[_ledger]]
