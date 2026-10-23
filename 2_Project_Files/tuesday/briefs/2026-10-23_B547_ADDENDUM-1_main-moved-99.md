From Tuesday (Kam's Datasec coordinator seat), Datasec / MPS Commercial Calculator, to SEAT-G66. ADDENDUM-1 to B547, written 20:22 AEDT. A FACT, not a change of scope.

## Main moved: PR #99 landed (Tuesday, squash, head pinned)
main c4aa4cc76e7f8e95d6bd484389a5b06019334875 -> **75d1c6e7c14422432a04b2a6d2a246e01485a10d** (one squash commit, parent c4aa4cc7, tree 5397aee0). Its 7 paths (each blob equal to the gated head 78e5bdc2, checked by Tuesday): src/MpsCalc.Api/Quotes/PricingPolicy.cs, tests/MpsCalc.Api.Tests/LeakLayerFirstLineTests.cs, LeakLayerPublicFieldTests.cs, LeakLayerRepeatedLineNumberTests.cs, LeakLayerSuppliesIssueTests.cs, PricingPolicyTests.cs, QuoteApiTests.Showcase.cs.

## What it means for you
Your REFUSE rule stops only if one of your 14 paths moved or a moved file calls SourceDocumentChecks.Run, EngineRead, IsDocumentFault or ReferenceDocumentValidator.Validate, or edits ReferenceStoreDocument.cs, ActiveSources.cs or QuoteFigures.cs: none of the 7 does (PricingPolicy.cs is the pricing gate, not the source lifecycle). NOT a refuse. Re-read main by ls-remote at your verdict as briefed; predict the merge of #100 against the NEW main 75d1c6e7 (legacy stdout merge-tree, merge-base recomputed by you) and list the overlap of the 7 paths with yours (expected 0). Everything else in your brief stands.
