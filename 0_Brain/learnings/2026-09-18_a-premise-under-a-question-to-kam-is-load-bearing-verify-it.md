---
date: 2026-09-18
type: correction
source: "I told Kam four Tested-Not-Deployed tickets were 'sitting merged and waiting on one firewall rule' and used it as the urgency under a start-now-vs-schedule question. Seat A then measured it two ways with a control: all four were ALREADY deployed on kintsugi and had been for days. The premise under the question was false."
status: live
supersedes: ""
tier: W
---

# A premise under a question to Kam is load-bearing — verify it like a fact in a brief

**The lesson:** `send_brief.sh` refuses a brief whose facts have no provenance. **The same standard
applies to anything I put under a question to Kam** — arguably more, because a brief goes to an agent
who will check it, and a question goes to a principal who will *act on it*. **Never pass a receiving
agent's summary into a decision for Kam without validating it at the source first.**

**Context:** Seat A's first mail said the four TND tickets were *"merged on develop and await a
deploy."* I compressed that into *"four owed deploys are sitting behind one firewall rule"* and made
it the urgency in a question asking Kam whether to take Stuart's box down for 2.5 hours **now** rather
than schedule it. It was false: the four fixes are **ancestors of the commit kintsugi is already
running**. Nothing was waiting on anything.

Two things about how it was caught:
- **My own condition caught it, not my diligence.** I had told seat A to *"report the RANGE, not just
  the endpoint — say which merges this deploy actually lands."* I set that so "deployed" would mean
  something specific. Measuring the range is what exposed that the four fixes were not in it. **A
  guard I set for rigour caught an error I had made for haste** — but one step too late to keep a
  false premise out of Kam's hands.
- **"Merged on develop and awaiting a deploy" and "not yet on kintsugi" are two different claims**,
  and I read the first as the second. A deploy target is a *fact about a box*, and facts about boxes
  are measured on the box.

**How to apply:**
1. **Before any question to Kam, list its load-bearing premises and name the source of each.** If a
   premise came from an agent's prose rather than a measurement, either verify it or state it as
   "reported, unverified" — never as the reason he should decide one way.
2. **Urgency is itself a claim and the most dangerous one**, because it is what makes him decide
   quickly. "X is blocked on Y" gets measured before it is said.
3. **Correct it the moment it is known, before he rules** — and say plainly where it came from, that a
   guard caught it rather than my judgement, and what the true framing now is. A corrected premise
   often reverses the answer: here it turns "do it now" into "schedule it".
4. This is [[2026-08-03_mental-model-not-source-of-truth]] failing to fire on an *inbound agent
   report*. The rule's order — read the model, **validate against the source**, then act — applies to
   what an agent tells me, not only to what I have stored.

**Related:** [[2026-08-03_mental-model-not-source-of-truth]], [[2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour]], [[../people/kam]]
