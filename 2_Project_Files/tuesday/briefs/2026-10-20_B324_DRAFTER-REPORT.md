# B324 drafter report (Tuesday's read-only brief drafter), 2026-10-20 ~13:20 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B324_SEAT-G17_mps-gate-pr87-tier1.md` (about 50 KB; the stamped B318 template is 51 KB; the ~45 KB target was missed by about 5 KB, cut from restated claims, not from checks).

## What I read
- Whole: the B318 tier-1 template (stamped), the builder STATUS `B312_STATUS.md` (307 lines), the builder brief `…_B312_SEAT-V3_….md` (159 lines).
- At the head `61d81f4` with `git show` (read verbs only): `QuoteReconciler.cs`, `OwnArithmetic.cs`, `ReconciliationTypes.cs`, `RentalRecomputation.cs`, `PurchaseRecomputation.cs`, `ReadinessEvaluator.cs`, `ReadinessCheck.cs`, `ReadinessPanel.tsx`, `web/src/qa/{errorProbe.ts,routes.ts,zeroErrors.test.tsx}`, parts of `ReconciliationTests.cs` (the source-scan test and the replica loops), `docs/RECONCILIATION.md` (grep only). At `acfcf5d`: `feedback/csv.ts`, `QuoteEndpoints.IsEmpty`, `WorkbookRules.AllowedTerms`, `ci.yml` (grep), `check-bundle.mjs` (head). Project docs: `BACKLOG.md:1585-1589`, `CLARIFICATIONS.md:441-452, :654-660, :678-681`.
- Not opened (by rule): `.env`, `3_Access_Keys`, `.local/`, `Source_Documents/`, `.tools/**`. So Jira was not read.

## Measurements (13:12-13:15 AEDT, read verbs / gh GETs under the project's `.gh-config`, `kamilDatasec`)
- `ls-remote`: main `acfcf5de…`, `b312/v3-readiness-reconciliation` and `refs/pull/87/head` both `61d81f4e…` (`cat-file -t` commit); `b324*` 0 (control `b312*` 1); #85 `b451239…`, #86 `925caf8…`.
- PR #87: open, draft false, 5 commits, 20 files, +2682/-0, mergeable true, state blocked. `git diff --name-status` = `20 A`. Path overlap with #85 (28 files) 0 and #86 (18 files) 0 (`comm -12`).
- Ports 7470-7479: 0 listeners (control: 12 listeners overall). B318 7450, B319 7460, B320 7480: this block sits between B319 and B320 and no brief names it. Load 8.34 9.82 9.38 (swings); `heavy-slot-1` existed at 13:12, absent at 13:15.
- `brief_seat.sh:24` `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"` confirmed: launch without the variable.
- Check-runs on the head: `CodeQL` neutral; dotnet, web, python, and the four `Analyze` legs in_progress. Code-scanning analyses: ONE (`/language:actions`, 0 results); csharp and js not present. Open alerts 0 on the PR ref and 0 on main (so the count cannot discriminate; the brief says use the analyses list as the control).
- Ruleset (not classic protection, which is 404): `deletion`, `non_fast_forward`, `code_scanning` (CodeQL), `required_status_checks` with an EMPTY list. So the `blocked` state is the CodeQL requirement, not a named check. B318's brief assumed "required checks pending"; it differs here.
- `merge-tree --write-tree acfcf5d 61d81f4` printed a tree (base = main, a fast-forward).
- 0 invisible/control characters in 2682 added lines (`python3 -I`, planted U+202E control fires); 0 skip/only/sleep/timeout tokens in added lines.
- `git grep -c 'Reconcil|Readiness' 61d81f4 -- src/MpsCalc.Api`: Dtos 3, Mapping 3, Proposal 10 (the existing `Readiness` word and `SoftwareReconciliation`).
- `C-45` now exists at `CLARIFICATIONS.md:654` (D-10/-11/-13 at `:678-681`), so "RULED BY KAM, NOT YET IN AN ARTEFACT" is partly overtaken; the brief keeps the paragraph and says so.
- Builder arithmetic checks out: 23+6+27 = 56 Engine tests, 33+26 = 59 web tests, 2140 -> 2196, 16+7+4+7+7 = 41 mutants.

## Traps found while reading (put in the brief as things to try, not findings)
1. **Independence is partial by design.** The module re-derives finance, sells at target GP, escalation, section rounding and sums, but reads rental hardware/option/software cost and cost per page, and purchase unit cost, applied percent, sell basis and catalogue sell back from the RESULT. A calculator error recorded and sold with consistently (wrong percent, wrong cost per page) is invisible. The cost-per-page value is both the cost and the basis of the sell (`RentalRecomputation.cs:85-86`).
2. **Effective tolerance is not one cent.** Purchase monthly is compared as `reportedContract / term` (a 0.60 contract error passes at 60 months); rental contract GP's reported side is built as `ContractValue - MonthlyCost * term` (a one-cent monthly cost error fails contract GP); annual GP is compared at x12 (monthly GP difference above about 0.000834 fails annual while monthly passes). A real one-cent error passes by design (inclusive 0.01), and C-30 lets shown parts move by a cent.
3. **`Agrees` is vacuously true** for an all-NotApplicable report. Matters when this later gates approve.
4. **Source-scan test** is a nine-name regex per line, skipping `//` lines: misses a fully qualified alias, `using static`, reflection, block comments.
5. **Non-empty check** counts raw lines like the API; a blank-SKU rental line counts but the calculator skips it; purchase options-only passes (the open BACKLOG.md:1587 (b)); the credit check has no `Optional` filter and targets only the first credit line.
6. **CSV neutraliser** (`csv.ts`, reused) tests the first character only for `= + - @ tab CR`: a leading LF, a leading space, a zero-width or full-width character are not covered (LF-first the usual gap).
7. **First-load test:** `settle()` is about 60 ms, so a late error is invisible; the route's own heading is asserted for the Seller only; the route-coverage regex `name: '([a-z]+)'` misses a capital or digit; the `KNOWN_BROKEN` guard compares two empty arrays and its non-empty branch never ran. 25 cases run under `fakeApi`+`withStub`, not a real server; the Playwright spec is not in CI.
8. **Nothing-wired proof by bare-word grep fails:** the Api already has `Readiness` and `SoftwareReconciliation`. The brief says grep the new type names.
9. **NEW WORDS "36"** counts table rows; row 36 holds two sentences; the nine `Rule` texts per quote mode are English sentences on every variance that the builder excludes as "register citations".
10. **Three-way merge:** #87's first-load test will render #85's and #86's screens once they land (builder's own "possible red"); the brief has the gate build a throwaway three-way tree.

## Open questions (numbered; recommended answer taken unless Tuesday overrules)
1. **Token ceiling for ruled gaps (R-V3-1 unwired, R-V3-3 held, panel unmounted, Playwright outside CI; tickets -248, -249, -251 as worded).** Recommend: ruled divergence is not a defect, ceiling GO WITH FINDINGS when the builder's comment states it plainly (as B318's 236). Taken in the brief.
2. **Jira.** Recommend READ ONLY, as B318 as stamped. Taken.
3. **Port block.** 7470-7479 is free; used. B320's brief says 7480-7489.
4. **Live Done-whens** were not read by the drafter (no `.env`); they are RELAYED from the builder's STATUS and the brief makes the gate GET them (live text wins). Recommend accept.
5. **Playwright spec re-run:** recommend OPTIONAL (browser, load, not in CI). The brief makes it optional.
6. **Three-way merge tree test:** recommend run at the gate's verdict only, after B318 and B319 have reported, so a red is attributed correctly. The brief runs it at r10 without that ordering; Tuesday may tell the gate to run it last.
7. **Builder's open rulings** (FOR TUESDAY item 6; the gate gives recommendations, Tuesday rules): (a) panel sort of passed checks: keep outstanding-first then passed, as built; (b) BACKLOG.md:1587 (b): keep "any BOM line counts" so readiness agrees with the endpoint, and raise the device-class question as its own ticket rather than let readiness contradict MPS-6; (c) Info chip shown only above 0, as built.
8. **Ceiling on the tolerance finding:** recommend Minor/Note (docs) unless a probe shows the module passing an error above one cent of a MEASURE it labels "within one cent"; Major only if a reachable calculator error above 0.01 on a total passes.
9. **Brief size:** about 50 KB vs the ~45 KB asked. Recommend accept (it matches the stamped B318 template); a further cut would drop probes.
10. **Wave/load:** five other gates/lanes are live; load1 was 8.3-8.8 at drafting. Recommend launching G17 after one of B318/B319 completes, to keep to one heavy slot at a time.

## UNMEASURED (by the drafter)
The live Jira Done-whens and comments (ids 39750-39754); `.env` presence of `AGENTMAIL_API_KEY`; whether any portfolio field in the calculator is cent-rounded (I read only the lines that assign `MonthlyCharge`/`MonthlyGrossProfit` from sums); the content of `docs/RECONCILIATION.md` beyond its tolerance lines; the whole of `ReconciliationTests.cs`, `ReadinessTests.cs`, `ReadinessPanel.test.tsx`, `V13Fixture*.cs`, and the Playwright spec; the web build and its bundle bytes; test counts (no `dotnet` or `npm` was run); the Jira search; the required-contexts list of the ruleset beyond "empty"; gitleaks; the real book, hosted site, and a real spreadsheet reading the CSV.
