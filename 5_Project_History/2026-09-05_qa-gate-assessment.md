# QA gate assessment — answer to Kam's 20:17 question (2026-09-05)

**Kam (panel 20:17, verbatim):** "Is the QA agent yielding results? Do you think it's worthwhile having everything go through the QA agent, or should we use it sparingly?"

## BLUF
Yes, it is yielding — and the class of what it catches is the one nothing else in the fleet catches: defects INTRODUCED by a correct fix, sitting under a green suite. But "everything at full weight" is the wrong dial. Recommendation: a TIERED gate (full gate for security, data-destruction, deploys and anything handed to Peter/Stuart; through-code only for tests/docs/config/follow-ups; nothing for hygiene), plus a CAP of two NO GO rounds on one class before the residue is ticketed and the closed instances ship. Kam's 09-01 rule ("every change goes agent → Wednesday → testing agent → Wednesday") is his; the default until he rules is that it stands unchanged.

## Measured (scoreboard, read 20:18)
| Measure | Value |
|---|---|
| QA passes since the gate was installed (09-01) | 56 in 5 days |
| Today alone | 9 passes: 5 NO GO, 3 PASS, 1 PASS-with-findings |
| Builder rounds today | 38 scored, mean 0.85; 13 carry an "introduced" finding |
| NexusAI erasure class | 8 gates on one class (pass 1 + re-gates 2–8), re-gate 8 running |
| Cost per narrow pass | ~25–35 min of a tester seat, plus a builder fix round per NO GO |
| Weekly usage (statusline) | 34% of the 7-day budget at 20:18 |

## What it caught that nothing else would have (this week)
- **A BLOCKER under a green suite the tester had itself re-derived** (NexusAI RD-245, 09-04): the fix could not fire on the product's write path; the test modelled the mutation through a path the product never takes. 1504/1504 green, and the incident replayed byte-identically on the fixed and unfixed trees.
- **The headline claim of a security PR false for the door that matters most** (Secuura #819 pass 1): `POST /api/auth/login` was never converted to the allow-list gate — PENDING/INVITED still minted — and the same commit INTRODUCED an unauthenticated account takeover (`invited` admin-writable → `/api/auth/register` 201 on a real account). The builder's own suite was green.
- **Two operator-facing defects introduced by a right fix whose consumer was not read** (NexusAI re-gate 7): a failed record write rendered on the health page as customer files that could not be deleted; a refused purge landed in the audit trail as purged and ok.
- **A latent Major in a guard that had just been added** (Secuura door 2 today): the guard tests emptiness while the repository keys on the trimmed address — two identities auto-linked into one account. Provider-gated, unreachable today, and exactly the collision the guard exists to close.
- **Wednesday's own errors** (three this week): a ruled test shape that could not go red; a ratification of correctness from a wrap mail; a canary claim composed from a heading. Each falsified by the gate before it reached a merge.

## What it costs, honestly
- **Rounds on one class.** The NexusAI erasure class is at its eighth gate. Rounds 6–8 each closed everything from the round before and each found something new the round introduced. The value per round is falling but not zero — round 7 was the strongest and still NO GO. Under a two-NO-GO cap the campaign would have stopped at round 5 with N-1…NN-7's instances closed and the class ticketed; rounds 6–8's catches (the living-process wedge, the audit-trail lie, the ledger contamination) would have been found later or by an incident. That is the real price of the cap and it should be said, not hidden.
- **Wall-clock and budget.** Nine passes today at ~30 min each is ~4.5 hours of tester seats, plus the fix rounds. The 7-day budget reads 34% with two days left.
- **Coordinator load.** Every pass is a brief (read live, dated stamps, scope clause), a launch with red-proofed guards, a completion check, a SCORE, and a GO or fix round — roughly 10 points of Wednesday's context per pass. Five rotations today; the gate is a large share of why.

## The tell that it is working the way Kam wanted
The catch rate is MIGRATING from tester to builder. Today's builders red-proof by extraction (`jest --json` at both commits, diffed by name), predict SET and COUNT before every tamper, classify their own reds as defect proofs vs API-absence artefacts, and catch their own draft defects (S36's `[]`-overwrite, s130's invalid F-6 red-proof, s131's two wrong classification drafts) BEFORE the gate sees them. That is the discipline the gate exists to teach, and it is the weekly KPI to watch: when a builder's round passes its gate first time, the gate has done its job for that class.

## Recommendation — tiers, not sparing
1. **Full gate (through-code + browser where there is a surface), mandatory:** security surfaces (auth doors, tokens, MFA, key revocation), data destruction/erasure, anything deploying to dev or demo, anything handed to Peter or Stuart as a test block.
2. **Through-code only (no stood-up surface):** tests-only PRs, docs, config/CI, follow-up PRs whose mechanism the prior gate already measured (the #820 shape), style/palette-only changes where the guide governs.
3. **No gate, builder's own extraction red-proof stands:** BACKLOG/citation fixes, ticket hygiene, comment corrections.
4. **Cap: two NO GO rounds on one class → STOP.** Ship the closed instances, ticket the residue with the tester's cells attached, re-open the class as its own commission later. No round 8 without a Kam word.
5. **Weekly KPI at consolidation:** first-time-pass rate per project; introduced-defect count per round; cost per pass. If first-time passes rise, tier 2 widens; if they fall, the gate tightens.

## Default
Kam's 09-01 rule stands unchanged until he rules. If he says "tiers", Wednesday applies them from the next brief and records the grant in `learnings/` per the go-slow rule 5.
