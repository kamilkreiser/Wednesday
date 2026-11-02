Server half of the fleet configuration template store (MPSCALC-269): create, new version, read, list and archive, behind three roles, with an audit event for each change. Archived templates are hidden from the list and kept. Applying a template to a quote is not part of this change. The generated web contract copies are regenerated.

## State of the review
- The gate ended NO GO at its round cap (round 2 of 2). By the gate, no wrong behaviour was measured.
- Two Majors. The first is a test gap: the source-scan row in tests/MpsCalc.Api.Tests/TemplateIsolationTests.cs does not read a call written inside an interpolation hole of an interpolated string, so a quote-side call placed there would not turn it red. No code in this change does that.
- The second Major is two false sentences in a builder commit message on this branch. This text replaces that message and repeats neither.
- Three Minor sentences in docs/API.md are short or false. They follow as one small change.
- The gaps are ticketed by a records seat after the merge.
- The stored-event check is well-formedness only: there is no hash chain. That was the coordinator's ruling, not the product owner's.

## Checked
- Merged tree = this branch on main 7104179f, the tree the gate judged. Main has moved since.
- Engine 623, Import 196, Api 3253 on that tree, failed 0, skipped 0.
- Web 1384 tests in 141 files on that tree, at Node 24.22.2; lint, test and the bundle check pass.
- Six operations by three roles: 66 of 66 cells on a real process. Kill -9 over 16 rounds: 543 acknowledged writes, 0 lost, 0 partial store files. Two processes: 220 of 220.
- Hosted CI and CodeQL have not run on this branch.

## Not done
- Not deployed. No default store path is configured (MpsCalc:Templates:Path is set nowhere), so a deployment as configured today would lose templates at each restart.
- Seven sentences (four new, three changed) still need the product owner's word pack before any deploy.
