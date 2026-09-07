## BLUF — #889 does NOT merge. F1 is merge-blocking: the PR's own integration suite is RED and its passing cells are vacuous.
**Kam's ruling is implemented CORRECTLY and the gate proved it independently — all three carried
semantics HOLD, and the org-less branch you flagged is CONFIRMED reachable and RIGHT.** The block is
the suite, not the bind. **Fix F1, then it re-gates. Do this AFTER round 3** — round 3 is already
released and #892's cap is spent, so it is the one with no slack.

## WHAT THE GATE CONFIRMED — bank it, do not re-do it
- **All three semantics HOLD**, proved by execution not reading: 403 only when both present and
  differ · case-only is not a mismatch (both sides through the shared `normaliseOrgId`) · no claim →
  unchanged and **the field did NOT become required**.
- **No third copy of `normaliseOrgId`** — the thing Peter's #795 review warned about.
- **🔴 THE ORG-LESS BRANCH: reachability CONFIRMED and the behaviour RIGHT.** You went past the literal
  wording of Kam's ruling, disclosed it, gave your reasoning, and **the gate independently confirmed
  both the reachability and the judgement.** That is the best possible outcome for a disclosed
  deviation and it is going on the scoreboard.
- **§4 PASSES** — the comment that had to change with the code did change.
- **It refuted Wednesday's `documents.ts:559` citation independently**, by opening the files rather
  than inheriting either the builder's correction or Wednesday's original. `:559` is a field in a 200
  body; nearest status is a **409 at :565**; the real precedent is `provenance.ts:131-137`, quoted
  verbatim. **Two independent refutations of the same coordinator error now exist in the record.**

## F1 — MERGE-BLOCKING, and it is the day's recurring shape
**The PR's own integration suite is RED, and its three passing cells are VACUOUS.** A red suite is
not shippable and a vacuous green is worse than a red — **it is the fourth instance today of a cell
that cannot fail**, after the `toContain` neighbour match, the inert `ONE UNIT` regex, and the
"refusal is not a warning" pin. **Fix the suite so it goes green for the right reason, and red-proof
each cell individually** — the discipline you already applied on #890 and #894.

## F2 — the FOURTH wrong comment in this project today
*"The org-less comment asserts a mechanism the code does not have."* Same class as the F3 mechanism on
#888, the `ONE UNIT` claim on #893, and `provision-actors.ts:154-156`'s *"the file simply is not
there."* **Fix it with F1, in the same commit, per your own rule: a comment that claims a behaviour is
a cell, not prose — and where it must stay prose, it must be true.**

## F3 — TOOLING, and it vindicates a workaround the fleet has been using all day
**`run-migrations.sh` reports `applied=N failed=0` for migrations it SKIPPED.** Three separate agents
today independently insisted on confirming a migration applied **by name** rather than trusting the
summary. **The gate has now established that as a real defect rather than caution.** Ticket it — it is
not #889's to fix, and it belongs with the F-1 ticket's family or its own, your call on the logical
path. **F4 and F5 are pre-existing and explicitly not this PR's.**

## SEQUENCE — unchanged except that #889 now needs a round 2
1. **Round 3 on #892** (released, cap spent, no slack).
2. **#889 F1 + F2**, then it re-gates.
3. **#893 → develop stays HELD** — it was waiting on #889's verdict and the verdict is "not yet".
4. **The F-1 ticket** from the #894 gate, and F3 above.
**Mail each leg.** **#891 is Kam's click. KS-968 is Kam's — nothing on that box.**
