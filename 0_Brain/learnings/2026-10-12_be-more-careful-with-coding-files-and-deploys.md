---
date: 2026-10-12
type: feedback
source: Kam, live board 2026-10-12 16:04:05 view=wednesday, verbatim "please be more careful, especially with coding files and deploys"
status: live
---

# Be more careful, especially with coding files and deploys

**Trigger:** minutes after I carded him a command copied from a launcher hint (the ssh-add path did not exist on this Mac, see the 2026-10-12 ledger row). His words are general, not only about that card.

**Rule:** before anything touching a coding file or a deploy leaves my hands (a brief, a card, a tap, a queue line):
1. Run the read-only precondition myself: the path exists, the sha is on the remote, the lock is free, the control passes. A launcher line, warning text or a drafter's report is a representation.
2. Deploys stay with a deploy seat under the October grant rules (kintsugi first, backup/rollback, KS-535 wallet rule); the verify seats do not deploy; nothing goes to demo unless Kintsugi is verified first.
3. Spark output is read at source (patch applied in a scratch clone, test run) before a raising seat gets it; no merge without the QA gate GO.
4. When unsure which of two actions is safer, pick the one that is reversible and say so.

**Why:** a wrong instruction to Kam costs his attention; a wrong code or deploy action costs the fleet. Same family as [[2026-08-03_mental-model-not-source-of-truth]].
