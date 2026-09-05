---
date: 2026-08-04
type: correction
source: "Self-caught: Vision's plan-confirmation QUESTION (05:57Z) swallowed by a manual mark-seen racing its arrival; surfaced only because their wrap mentioned the unanswered mail"
status: live
tier: M
---

# Acknowledgments cover what you PROCESSED, never "everything as of now" — in any tool, not just mark-seen

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

## Generalised at the 2026-08-10 consolidation (after the w=2 recurrence)

The rule recurred in a NEW costume on 2026-08-10: the `arm_wake_watch.sh`
runner set `baseline = now` on every cycle — a blanket acknowledgment with no
`mark-seen` call anywhere in sight — and swallowed Vision's 03:51Z QUESTION
into the fire→re-arm gap. The 08-04 lesson never fired while I wrote it,
because its retrieval handle was the SCRIPT, not the CLASS.

**The class, stated so it matches any costume:** any time a watermark, seen
flag, baseline timestamp, cursor, offset, or "handled" marker advances, it may
advance ONLY to cover events that provably reached the processor — a displayed
message, a fired wake, a written receipt. Setting it to `now`, to `latest`, or
to "everything currently visible" races every concurrent arrival, in ANY
at-least-once pipeline: mail seen-state, watcher baselines, queue offsets,
notification clears, "handled" file moves. When in doubt, err toward re-fire —
a duplicate tap costs one interruption; a swallow costs a silent fallback
window. Enforced in the runner 2026-08-10: baseline advances only to the
timestamp of the event that fired the wake.

**Related:** [[_ledger]], [[../skills/delegation-monitoring]]
