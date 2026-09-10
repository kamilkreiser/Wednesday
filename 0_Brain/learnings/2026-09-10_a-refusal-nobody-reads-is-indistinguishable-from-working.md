---
date: 2026-09-10
type: principle
source: named by the Datasec coordinator after three instances in one morning; adopted verbatim
status: live
tier: W
---

# A guard that is correct in isolation and open-ended in practice — and whose refusal is logged where nobody reads it — is indistinguishable from working

**Her sentence, adopted as written:**
> *"A refusal that no one is looking at is indistinguishable from working."*

**Three instances on 2026-09-10, in one morning, in three different mechanisms.** That is why
this is a principle and not a bug report.

| # | Guard | Correct in isolation | Open-ended in practice | Where the refusal went |
|---|---|---|---|---|
| 1 | `panel_sync` skips if a rebase is in progress | never pull into a half-finished rebase | it *left* the rebase in progress, so it skipped **forever** | `SKIP rebase/merge in progress`, every minute, for **13 hours** |
| 2 | `panel_sync` skips if the tree is dirty outside `dashboard/data` | never pull over someone's working files | an **actively working** coordinator is the normal state, so it skipped indefinitely | `SKIP dirty outside dashboard/data`, every minute, for **42 minutes**, costing ten of the other seat's messages to Kam |
| 3 | `cockpit.html` suppresses repaint while Kam has a draft | do not repaint under someone mid-sentence | he **dictates**, so a part-finished line is his normal state | nowhere at all — the panel simply froze, and he chased it three times |

## The shape

Each guard was written by someone thinking about the *exception* it prevents. **None was written
by someone asking what happens when its condition becomes the NORMAL state.** And in each case
the condition did:

- a rebase left in progress is permanent, not transient;
- a coordinator with uncommitted work is the default, not an anomaly;
- a dictation user always has a part-finished line in the box.

**The second failure is the one that makes it expensive: the refusal was logged, honestly and
repeatedly, somewhere nobody was looking.** Instance 1 wrote its reason 780 times. Instance 2
wrote it 42 times. **Both were found by a human noticing an ABSENCE — Kam chasing a message
that never came — not by anyone reading the log.**

## The rule

1. **For every guard, ask what its condition looks like when it is TRUE for a long time.** Not
   "is this the right condition" — that part is usually fine — but *"what does this do when it
   stops being an exception?"* A guard that is correct per-cycle can be catastrophic per-hour.
2. **A refusal must end somewhere a human or a successor actually lands** — a visible banner, a
   panel row, an escalation after N consecutive refusals. **A log line is not a channel.** If the
   only record is a file nobody opens, treat the guard as silent.
3. **Prefer a guard that DEGRADES over one that BLOCKS.** The dirty-tree fix does not refuse the
   whole cycle any more; it does the part that is safe (advance the other seat's stream) and skips
   only the part that is not (the rebase). The freeze fix still suppresses the repaint but *says
   so*. **In both cases the guard kept its intent and lost its open-endedness.**
4. **When a guard fires repeatedly, that is a finding about the guard, not noise.** Repetition is
   the signal that its condition has become normal.

## How this was found, which is part of the lesson

**Not by me reading my own code.** Instance 1 was found by the other coordinator measuring row
counts; instance 3 by her reading Kam's screenshot after I had given him a confident wrong answer;
instance 2 only because **she refused my closure of her question** and I then measured local
against origin instead of reasoning about it.

**Three guards, three instances, and the common instrument was someone else looking.**

**Family:** [[2026-08-11_a-check-that-cannot-fail-is-not-a-check]] ·
[[2026-09-08_the-check-ran-and-was-not-checking-the-thing]] ·
[[2026-08-25_a-promise-is-not-a-mechanism]] ·
[[2026-09-10_a-detector-keyed-on-remedy-text-matches-the-hint]] ·
[[2026-09-10_a-single-file-bind-mount-binds-the-inode]] (five green signals, same morning: a
control that reports honestly about the wrong property).
