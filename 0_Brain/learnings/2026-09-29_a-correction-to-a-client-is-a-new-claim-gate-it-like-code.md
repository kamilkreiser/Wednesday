---
date: 2026-09-29
type: correction
source: KS-1374, three client-facing comments in one day, each caught by a gate or drafter (ledger 2026-09-29)
status: live
tier: W
---

# A correction to a client is a NEW claim — it gets the same measurement as the thing it corrects, and it goes through the gate with the code

**The operative case, so the headline matches it:** Wednesday or a seat is about to post a correction,
clarification or follow-up comment on a ticket a client human reads (Peter, Stuart), because an earlier
comment was wrong. **Stop. The correction is not a retraction; it is a fresh set of factual claims, written
fast, under the pressure of having just been wrong, by someone who wants the matter closed.** Every
sentence in it names what it was measured against, or it says "unmeasured".

## The case (Secuura KS-1374, 2026-09-29)
1. **01:42Z, the original comment** (Wednesday-drafted, posted by B 43rd): "The harness already derives its
   pace from this value, so it speeds up on its own." False: `aktoRateLimit.ts:60` hard-coded 2000.
   Caught by the Spark brief-writer.
2. **The first correction** (Wednesday-drafted, in B 45th's brief, posted with #1347): "Demo and production
   limits are unchanged." Half true: `.env.example` (raised to 10000 in that very PR) is the documented
   seed of the production compose. Caught by gate44 (N-1347-2).
3. **The second correction** (B 45th-drafted, on Wednesday's commission): asserted "a demo scan (limit
   2000)" while also saying the demo's limit was never read, and two lines were false in the
   `OVERRIDE_APP_URL` case. Caught by gate45 (N-1347-15).

Three client-facing texts, three unmeasured claims, each written to FIX the previous one.

## Why the existing rules did not fire (the w=2 diagnosis)
- [[2026-08-14_i-read-representations-they-read-sources]] and [[2026-09-18_a-premise-under-a-question-to-kam-is-load-bearing-verify-it]]
  both fire on a claim *Wednesday is making*. A correction does not feel like making a claim; it feels
  like **removing** one. The retraction lesson ([[2026-09-06_a-retraction-inherits-the-scope-of-its-measurement]])
  says a withdrawal is the highest-risk act — but these were not withdrawals, they were REPLACEMENTS, and
  the replacement sentences were never put through the instrument the original failed.
- The code in the same PR went through a gate. **The comment did not** — it was posted by the seat at
  raise time, before the gate ran, so the gate could only find its errors afterwards, on the client's
  screen.

## How to apply
1. **A correction comment is drafted, then held, and posted only AFTER the gate that covers its PR has
   read it** (the gate checks every factual line against the head, as gate45 did). Posting with the PR,
   before the gate, is what put two wrong texts in front of Peter today.
2. **Every sentence in a correction carries its instrument or the word "unmeasured"** — especially the
   reassuring ones ("unchanged", "only local", "limit 2000"). A reassurance is a safety claim
   ([[2026-09-08_a-safety-claim-names-the-property-it-checked]]).
3. **Say less.** The minimum true correction is: what was wrong, what the PR changes, and what is not
   known. Every extra reassuring clause is a new surface to be wrong on.
4. **A third correction is not the fix — editing the wrong one is.** Where the platform allows it, edit the
   comment to be true, and say in the edit that it was edited; do not stack corrections for the client to
   reconcile.

**Family:** [[2026-08-14_i-read-representations-they-read-sources]] ·
[[2026-09-06_a-retraction-inherits-the-scope-of-its-measurement]] ·
[[2026-09-08_a-safety-claim-names-the-property-it-checked]] ·
[[2026-09-05_tickets-are-the-channel-whatsapp-via-kam-is-the-escalation]] (ticket comments are the
client channel, so they carry client-grade care) · [[2026-09-01_qa-gate-before-my-verification]].
