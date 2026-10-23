# B538 ADDENDUM-1, from Tuesday (s151), 2026-10-23, to seat G63 (gate on MPS PR #102). Binding, same rules as B538.

## BLUF
MPS main MOVED after your stamp: Tuesday landed PR #101 by squash at about 16:2x, main 4c593517 -> c4aa4cc76e7f8e95d6bd484389a5b06019334875 (one parent 4c593517). The moved set is src/MpsCalc.Api/Quotes/Proposal.cs plus three test files (B103DealUsageCountedLineTests.cs, B103DealUsageProposalTests.cs, DealUsageColourRowTests.cs). Proposal.cs names PurchaseCalculator once and uses QuoteDraftDto (read by Tuesday from main), so your REFUSE rule on a moved main would fire. TUESDAY RULING: this move is NOT a refuse for this gate. Continue.

## What changes
1. Use main = c4aa4cc7 everywhere B538 says 4c593517: the PR's merge ref (re-read refs/pull/102/merge and its parents: expect c4aa4cc7 and c7365aee), wt-merge, and the C10 merge prediction. If you already built wt-merge on the old merge ref, rebuild it on the new one before the whole CI line, and say which tree each figure came from.
2. C10 (2c) is now a read of LANDED code: B518's -230 counted-device check (NoCountedDevice) and #101's counted-line definition in Proposal.cs at c4aa4cc7 must agree. Read both and say whether they agree; a disagreement is a finding graded by your GRADING table.
3. Everything else in B538 stands, including your hard stop.

Say in STATUS that you read this addendum and when.
