# B1118 landing text, drafted 2026-11-02 (nothing opened, pushed or merged)

Files: pr-title.txt, pr-body.md, squash-subject.txt (59 chars, ASCII, no backticks), squash-body.txt.

## Read at source (gh api -X GET, MPS project GH_CONFIG_DIR)
- Head of b1093/mps-269-server-template-store: 531c83beaeb0c42e6db4087c5aa61b9085e2cc41 (git/ref). Equals B1118's head.
- main now: e970f7eb06fcca4ddc57510c6ce4bea579a99b2e. Open PRs for the head: 0.
- compare main...head: diverged, ahead 4, behind 5, merge base b7cf1ad0, 14 files.

## Figures and where each came from (B1118 STATUS, read whole)
- Engine 623, Import 196, Api 3253, failed 0, skipped 0, merged tree = branch on main 7104179f: Check 1.
- Web 1384 in 141 files, Node 24.22.2, same tree: Check 1.
- 66 of 66, 543 writes 0 lost 0 partial, 220 of 220: Check 3 / verdict text.
- Major = source-scan gap (B1118-1), 3 Minor docs sentences (B1118-2, -3, -4): Findings. Seven sentences (4 new + 3 altered): Check 7. No default path: Check 8(d).
- Well-formedness only / no hash chain: Check 5 and B1105-1 ruling. That it was the coordinator's ruling, not the product owner's: from the brief to me, NOT in B1118; not re-verified.
- "Ticketed by a records seat after merge", hosted CI/CodeQL not run: Check 8 records and the verdict line.

## Check 9 false sentences, avoided
Not repeated: "template code may name a quote-side type only through the static helpers", and "a second process reads the file it loaded until it restarts". Body says only that the scan misses an interpolation hole, and says nothing about second-process visibility. The body does not claim clause 4 (apply never mutates an issued quote) is proven; it says applying is not part of the change.

## Main's new commits versus the gate
Since 7104179f (gate tree): 17fc0dbc (#143), e970f7eb (#144). Paths: docs/ENGINE.md, docs/IMPORTER.md, src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs, tests/MpsCalc.Engine.Tests/PurchaseSiteAllocationTests.cs, web/src/screens/bom/QuantityAudit.severalDevices.test.tsx, web/src/screens/bom/QuantityAudit.test.tsx.
Since the merge base b7cf1ad0 (all 5 commits: 19d084fa, f8f808c4, 7104179f, 17fc0dbc, e970f7eb), 16 paths: the six above plus src/MpsCalc.Engine/Input/PurchaseInput.cs, tests/MpsCalc.Api.Tests/QuantityRuleStoreOptionsTests.cs, tests/MpsCalc.Engine.Tests/ComponentQuantityRuleTests.cs, tests/MpsCalc.Engine.Tests/PurchaseRecurringProjectionTests.cs, tests/MpsCalc.Import.Tests/PanelParityMultisetTests.cs, web/src/screens/QuoteScreen.addSectionWait.test.tsx, web/src/screens/QuoteScreen.endActions.test.tsx, web/src/screens/QuoteScreen.tsx, web/src/screens/bom/PurchaseBomEditor.addSectionWait.test.tsx, web/src/screens/bom/PurchaseBomEditor.tsx.
Branch's 14 paths: docs/API.md, docs/api/openapi.json, Program.cs, 4 files under src/MpsCalc.Api/Templates/, EntraAuthTests.cs, TemplateApiTests/IsolationTests/StoreTests.cs, 3 under web/src/api/generated/.
Overlap by path: NONE. Mergeability not stated (read at landing).
New since the gate: #144 (e970f7eb) touches PurchaseCalculator.cs, ENGINE.md and a site-allocation test and changes Engine/Api test counts. The counts in the body are therefore the gate tree's only; a landing must restate counts for the then-current main.

## Could not verify / notes
- Co-Authored-By line kept in squash body and PR body (workspace attribution rule, as B1119 form); it is a model, not a person.
- PR title is longer than the squash subject and includes the NO GO state; trim if preferred.
- Mergeability, hosted CI, CodeQL, and (#N) suffix for the squash are for landing time.
