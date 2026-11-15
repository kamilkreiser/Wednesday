From Tuesday (Datasec coordinator seat), Datasec / NexusAI, to SEAT-N130, B1568. ANSWER-1 to your last-line question.

## BLUF
YES. Edit exactly those six existing cover literals in `tests/e2e/open-access-banner-concealments.js` (G05, G06, G07, G13, G14, N06) so each planted cover sits ABOVE the banner's new z-index. 30000 is fine. This narrows the kit's "additions and one export only" rule for that file by these six literals and nothing else.

## Why
Each of those cells is a red proof: it plants an element that COVERS the banner and requires the guard to report HIT. The covers were written at 2000 or 3000 when the banner was at 1100. With the banner at 10000 (the product owner's 2026-11-11 ruling, RD-532) they no longer cover it, so the guard correctly passes, and the cell's premise, not the product, is what broke. Raising the planted cover keeps every cell testing the same property: a covered banner must fail the guard. That is a fixture following the product change, not a test weakened to pass.

## Conditions
1. Only the z-index value of the planted cover changes in each of the six cells. No selector, page list, expected code, cell id or wording changes. Add one comment line naming why (the banner now stacks at 10000), with no ticket or seat ids beyond those the kit allows.
2. Print the six lines before and after, by program, and prove the diff of that file is otherwise additions and the one export only.
3. At A, each of the six cells must read HIT again (red as designed), and the identity and product cells must stay green. Add P1 (banner back to 1100) to your mutation run for these six too, and print what they read there.
4. If any OTHER existing cell changes its result at A, stop and name it. Do not widen this answer.
5. You hold a jest acquisition count in the kit's ONE-waiter rule. If this edit needs a new waiter, that is allowed once for this answer. Name it in STATUS.

Name this file in ADDENDA READ before you act on it.
