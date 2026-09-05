---
date: 2026-09-05
type: grant
source: Kam, panel 20:19 ("That's great to hear. Thank you. Let's go ahead with your recommendation.") on Wednesday's 20:1x assessment of the QA gate
status: live — refines 2026-09-01_qa-gate-before-my-verification (the gate stays; its WEIGHT is now tiered and its ROUNDS are capped)
tier: W
---

# The QA gate is TIERED by what the change touches, and CAPPED at two NO GO rounds on one class — full weight for security, data destruction, deploys and human handovers; through-code only for tests, docs, config and already-gated follow-ups; none for hygiene

**The operative case, so the headline matches it:** a builder's READY or wrap lands and Wednesday is about to commission a QA pass. **Ask two questions before writing the brief: (1) which TIER does this change fall in — what does it touch? (2) how many NO GO rounds has this CLASS already had?** The answer to (1) sets the pass's weight; the answer to (2), if it is two, means the residue is ticketed and the closed instances ship — no third round without Kam's word.

**The grant (recorded per go-slow rule 5).** Kam's 2026-09-01 rule — every change goes agent → Wednesday → testing agent → Wednesday — stands as the SHAPE. On 2026-09-05 at 20:17 he asked whether the gate was yielding and whether everything should go through it; Wednesday answered with the scoreboard (56 passes in five days; today 9 passes with 5 NO GO; builders 0.85 mean with 13 introduced-defect rounds; one NexusAI class at its eighth gate; ~30 min per pass; the 7-day budget at 34%) and recommended tiers plus a cap rather than sparing use. He ruled at 20:19: *"Let's go ahead with your recommendation."*

## The tiers
1. **Full gate (through-code + a real browser wherever there is a rendered surface), mandatory:** security surfaces (auth doors, tokens, MFA, key revocation, session minting), data destruction and erasure, anything deploying to dev or demo, anything handed to Peter or Stuart as a test block.
2. **Through-code only (no stood-up surface):** tests-only PRs, docs, config/CI, follow-up PRs whose MECHANISM the prior gate already measured (the #820 shape), style changes where the guide governs.
3. **No gate — the builder's own extraction red-proof stands:** BACKLOG/citation fixes, ticket hygiene, comment corrections, record-only changes.

## The cap
**Two NO GO rounds on one class → STOP.** Ship the closed instances (merge or deploy-eligible as the tier allows), ticket the residue WITH the tester's cells attached, and re-open the class as its own commission later. A third round on the same class needs Kam's word on a card. **The price, stated when the cap was recommended:** the NexusAI erasure campaign would have stopped at round 5, and rounds 6–8 found real defects (the living-process wedge, the audit-trail lie, the ledger contamination). The cap trades late catches for bounded cost; Kam took the trade knowing it.

## The KPI (weekly consolidation)
**First-time pass rate per project** — a builder's round passing its gate on the first pass means the gate has taught that class. Also: introduced-defect count per round; cost per pass. If first-time passes rise, tier 2 widens; if they fall, the gate tightens. The catch rate MIGRATING from tester to builder (extraction red-proofs, predicted sets and counts, self-caught draft defects — all seen on 09-05) is the design working.

## How to apply
1. Every QA brief's header names its TIER and the reason ("tier 1: auth door" / "tier 2: follow-up, mechanism gated at `2ddca095d`").
2. Every fix-round mail names the ROUND COUNT for the class ("round 2 of 2 under the cap — the next NO GO ships the closed instances and tickets the rest").
3. In flight on 09-05 at the grant: NexusAI re-gate (8) is the class's eighth round — the cap is forward-looking; a NO GO at (8) ships the closed instances and tickets the residue rather than opening round 9. s131's follow-up PR (S130-F1…F6) = tier 2. #817 (KS-800, the NUL-byte guard class) = tier 1 (a security guard's mount surface).
4. Unchanged: Wednesday's completion check (delivered-vs-commissioned) on every round; the signature classes; a deploy needs Kam's word.

**Family:** [[2026-09-01_qa-gate-before-my-verification]] (the rule this tiers — its three hops stand) · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: a relaxation is recorded, never assumed) · [[2026-08-07_a-check-that-cannot-fail]] (what the gate catches) · [[2026-08-21_challenge-me-when-you-think-im-wrong]] (the recommendation went to him with its price, not as a courtesy answer) · [[2026-09-04_decisions-held-narration-drifted]] (the measurement in the same breath as the characterisation).
