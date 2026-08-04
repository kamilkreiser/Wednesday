---
date: 2026-08-04
type: correction
source: "Self-caught: Vision's plan-confirmation QUESTION (05:57Z) swallowed by a manual mark-seen racing its arrival; surfaced only because their wrap mentioned the unanswered mail"
status: live
---

# Never blanket mark-seen mid-monitoring — acknowledge only what you processed

**The failure:** during live monitoring I ran `inbox_digest.sh mark-seen` as
post-send hygiene (to stop my own outbound copies false-firing the monitor).
`mark-seen` marks *everything currently new* — including a QUESTION that had
arrived seconds earlier and was never displayed. It vanished silently; the
asking agent burned its 15-minute fallback window waiting.

**The principle (bigger than the script):** in any at-least-once message
pipeline, **acknowledgment must cover exactly the messages you processed** —
never "everything as of now". A blanket ack races every concurrent arrival.
The same applies to marking Linear notifications, clearing task inboxes,
deleting "handled" files.

**How to apply:**
1. `mark-seen` is for **session baseline only** (first boot, known-quiet
   inbox). Never during active monitoring.
2. Outbound sender-copies need no manual handling: the monitor's own digest
   cycle absorbs them (displays+marks atomically) and its fire condition
   ignores `[OUTBOUND]` batches.
3. The failure is invisible from the inside — it surfaces only if the
   counterparty mentions the unanswered mail. So treat any "no ANSWER by
   fallback" line in a wrap as a trigger to audit the seen-state, not as
   the agent's problem.
4. If a future need for mid-flight acking appears, extend the script to ack
   explicit message IDs (ack-what-you-processed), don't reach for mark-seen.

**Related:** [[_ledger]], [[../skills/delegation-monitoring]]
