# B373 drafter report (MPS clone-reference surrogate split, MPSCALC-289 only), 2026-10-21 06:01-06:2x AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B373_SEAT-W23_mps-289-292.md` (128 lines; two stamp slots `@MAIN@`, `@STAMP@`; `grep -o -E '@[A-Z_]+@' | wc -l` reads 2). Shape copied from B361 (read whole). Own measurements, read verbs only: `ls-remote` (main `1eccbc8b`, `b373*` none, 116 refs), Jira GET of MPSCALC-289 and -292 (whole), `gh api` raw reads at `1eccbc8b` of `QuoteEndpoints.cs`, `QuoteApiTests.V0Duplicate.cs`, `QuoteApiTests.Duplicate.cs`, `Proposal.cs`, `ReconciliationTests.cs`, `docs/RECONCILIATION.md`, grep of `docs/API.md` and `openapi.json` and `MpsCalc.Api.csproj`, the tree listing, `compare` of two branches, open-PR list (0). No dotnet, no fetch, no HTTP to any hosted site. Wrote only these two files (plus scratch in the session scratchpad).

## Scope decision: 289 only, 292 NOT combined
- 289 is a one-method product fix (`CopyRef`, `QuoteEndpoints.cs:566-574`) with an exact repro and acceptance. Red-first, Api test project.
- 292 is test-only in a different project (`MpsCalc.Engine.Tests`), a different proof discipline (mutant plants), and its Recommendation is design-shaped (IL/reflection token walk versus augmenting the regex; what counts as a "reference"). It wants a ruling before a Sonnet seat builds it. Suggest it as its own brief (B374) once Tuesday picks the approach.
- Tier mix too: a product edit and a test-only edit in one lane would force one gate tier on both.

## Questions for Tuesday, each with a recommended answer
1. **Tier.** Tickets carry `tier-1`; I proposed tier 2 (G2) for a six-line, one-method, no-auth, no-money fix. Recommend: tier 2, rule it in the stamp paragraph.
2. **Model row.** C2 Sonnet is enough for 289 (stated repro, stated fix shape). No escalation needed. If you later launch 292, I would put it on a higher row only if you choose the IL-walk option. Recommend: C2 for 289.
3. **Fix shape.** Pair rule (step back one unit) rather than the Recommendation's alternative text-element cut. Copy is then 99 units in the pair case, still "at most 100". Recommend: keep.
4. **docs/API.md:413** says "cut ... so the whole is 100 characters"; that becomes untrue in the pair case, so I put that one sentence in "Yours" (openapi.json:350 says "within 100", stays true, NOT yours). Recommend: keep the one-sentence edit.
5. **Stale branch overlap.** `b37/gate-b36-fix-round` (`f48edf02`, 6 ahead / 67 behind main, no PR) touches `QuoteEndpoints.cs` (also Proposal, QuoteEvents, docs, web-generated). Not a REFUSE (no open PR); I put a scratch-merge check in the MERGE CHECK. Recommend: keep, and ask whether that branch is dead.
6. **Red proof method.** One commit (as B361), with the RED shown by running the head's tests against the base `src` in the detached base worktree, not a red commit on the branch. Recommend: keep.
7. **B361 pane note.** I named B361 (pane W21) and B368 (pane R13, records for PR #92) as other seats from the briefs listing only; I did not read tmux. B361's branch `b361/import-test-rows-304-305` is on origin (`3f1ebd13`, 2 ahead / 1 behind, Import files only, no overlap). Recommend: confirm the panes are as you know them before launch.
8. **Pane name.** `Datasec/MPS-W23` as asked. Check it is free.

## Things I could not verify (all marked UNMEASURED in the brief)
- Dotnet baselines (the 394 / 151 / 1799 are RELAYED from the PR #91 tree; PR #92 may have moved them).
- That create accepts a 96-unit emoji reference and that the JSON layer yields U+FFFD (ticket and gate say so; the brief makes the 201 the test's own premise and has direct-call rows that do not depend on JSON).
- Test helper names beyond `RefOf`, `OtherSeller`, `Create`, `Assumptions`; whether a test compares `docs/API.md`; whether `:413` is the only prose with the "whole is 100" claim.
- The `Proposal.cs:67` citation in the ticket: at `1eccbc8b` the drafter saw `:67` as a field-map entry and the `QuoteRef = draft.QuoteRef` copies at `:430` and `:565`; `Proposal.cs` needs no edit and is outside "Yours".
- The project checkout does not hold `1eccbc8b` (stale), so all source reads were `gh api` raw reads; the builder's one `fetch` fixes that.
- Whether tmux panes of other seats are open; `AGENTMAIL_API_KEY`; load at launch (6.98 at 06:01).
- One drift note: the 292 ticket cites `ReconciliationTests.cs:457-476`; at `1eccbc8b` the test is `:458-476` and `FindModuleDirectory` starts at `:478`, so it matches within a line.
