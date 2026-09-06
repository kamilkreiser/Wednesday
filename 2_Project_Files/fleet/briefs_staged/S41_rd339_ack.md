## BLUF
**ACK — RD-339 + RD-347 @ `7eac4ff` is under its tier-2 gate (pane `QA/NexusAI-s41-rd339`, launched 11:18:47 AEST, ~25 min; the verdict comes to you by mail from Wednesday). HELD until then. Two rulings on your flags, then RD-180 + RD-251 as one branch.**

## Rulings
1. **`python3` as an undeclared CI dependency — no CI change this round, as you judged.** The wrapper fails CLOSED with a named assertion if it vanishes, so the failure mode is safe. Record it: one comment on RD-339 naming the dependency and the runner image that ships it today (`ubuntu-latest`), and ONE follow-up ticket (Low, category 1): "declare `python3` in the CI workflow (a `setup-python` step or an explicit assertion at the top of `verify`)" — Kam's word is not needed for a CI declaration, but it is a workflow-file change and gets its own gated round, not a ride on this one.
2. **The predicate's 8-of-10 uncovered surface — RD-347's scope, as you recorded.** Not this round; not lost.

## Received, with credit
The growth FAIL reported as RD-291 firing in anger on the day it was ruled — and the expectation updated WITH the change, never ahead of it. The old-suite-green control named as the ticket. The pipe-status incoherence caught a second time.

PROVENANCE:
- Your READY (7eac4ff; 2123/2123 × 111; +13/+1 with its arithmetic; the three-row red-proof; the three wrapper tampers; the five pieces; the two flags; RD-339/RD-347 in Testing) | `[Datasec/NexusAI -> Wednesday] READY FOR QA: RD-339 + RD-347 @ 7eac4ff …` 2026-09-06T01:15:33Z, read whole | read 2026-09-06 11:16
- The gate | `cockpit.sh add` receipt for pane `QA/NexusAI-s41-rd339` (wrapper `--check` rc 0; refusal paths rc 6 / rc 7 read bare); brief `2026-09-06_nexusai-s41-rd339-347-7eac4ff-throughcode.md` | read 2026-09-06 11:18
- `refs/heads/rd-339-python-gate-s41` = `7eac4ff5736f7d80c8dcf2ff9e8ba62b48217b8c`; the campaign tip `9c8e63a` unmoved | `git ls-remote origin` from Wednesday's seat | read 2026-09-06 11:16

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-06 11:19
(checked: nothing re-sequenced from the 10:57 ANSWER; the gate is reported from its receipt; the CI ruling deploys nothing and changes no file this round; the queue after (RD-180 + RD-251 one branch → RD-334 → RD-341) is as you stated.)
