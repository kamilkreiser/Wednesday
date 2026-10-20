# B357 drafter report (HPSM-POC PR #165 tier-2 gate), 2026-10-21 ~02:2x AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B357_SEAT-G13_hpsmpoc-gate-pr165-tier2.md`. Shape copied from B304. Read verbs only (`gh api` GET, `ls-remote`, `lsof`, `date`); no dotnet, no git write, no other client's material, no HP Restricted path.

## Measurements (all MEASURED 02:18-02:20 AEDT unless marked)
- PR #165: open, draft false, head `b06ddfd9d913845d2d22b1688073c725a76c77cb`, base `c149a3037463d38bf7cec38c16a182c746b3b1b3`, 2 commits (`23602ab214d6af7d2bb120a75aa09cced1d71fa6`, `b06ddfd…`), 4 files, +499/-4. compare: ahead 2, behind 0, merge base = c149a30.
- Files: `ImportEndpoints.cs` +6/-3; `ImportFailGuardTests.cs` +331 (added); `ImportSweepCountTests.cs` +160; `ImportSweptUploadTests.cs` +2/-1 (`///` comment only, read in the patch).
- Product change is one condition at head `ImportEndpoints.cs:323`: `== reason` becomes `is not null`; comment lines `:317-322`. Row deletes `:308-315` precede the guard. Status read is inside the per-file loop (`:134-147`), so "first status read" and "next status read after release" differ (T-e).
- `ls-remote`: main c149a30; branch and `refs/pull/165/head` b06ddfd; `b357*` 0 refs (control `b300*` 1). Open PRs: only #165.
- Check runs at 02:20 (18 runs): 7 success, 1 neutral (`CodeQL`), 10 in progress. `CodeQL` neutral completed 15:18:08Z (02:18 AEDT) as in B304. In progress: Analyze (actions, csharp, javascript-typescript, python), api, both SQL Server shards, vitest, web build, infra. gitleaks and dependency review: success. At draft time the CodeQL legs are NOT complete, so any verdict is conditional until they are.
- Code scanning: PR ref returns 2 analyses of an earlier commit (not read further), 0 open alerts. Main: 4 analyses at c149a30, 0 open alerts (control).
- Main protection required contexts (5): api (ASP.NET Core), web (Next.js), infra (Bicep validate), secrets (gitleaks, full history), dependency review. `web (Next.js)` is not yet in the head's list.
- Main's check runs on c149a30: api 13m46s, api-assessment 14m08s, api-other-and-feedback 15m14s (check-run started/completed, queue included). B304 shard sums 889 + 625 = 1514; expected 1524 at head.
- Load 7.10 8.23 8.88 at 02:20. Ports: 7880-7899 0 listeners, 7900-7919 0 listeners, unfiltered 13 listeners (control). No brief names a port in 7900-7909 (grep 0; control 730x = 3). B356 named 7860-7899.
- Sonnet id from `models_latest.json`: `claude-sonnet-5-5`. Routing row: G2 (tier 2, Sonnet 1st; O55 1st "if the mechanism sits on a G1 surface").
- Test census read from head: `ImportFailGuardTests` has 4 facts + 1 theory (2 rows) = 6 names; `ImportSweepCountTests` +4 facts = 10 added, matching the builder.

## Things the brief tells the gate to attack that I noticed
1. Rows dropped BEFORE the guard (T-b): under the old same-reason guard B304 called "guard above the deletes" equivalent; under the wider guard it may not be. Own mutant `gd` plus r2(e).
2. R8-iii (`A_store_write_that_fails_after_the_sweep…`) has no forged counter; its inputs are the 500 `store-failed` answer and the final state. Suspected weak input assertion (T-d, r4).
3. Builder's R8-ii differs from B304's (read after release, end `StoredAt set,set,null`).
4. Builder's own disclosures: -302 mutants s1-s4 run on the first (now unreachable) commit pair, not `b06ddfd`; it read `ImportPendingSweep.cs` against its partition; it did not read `history.md` or the B300 STATUS; it rebuilt its commits after finding a `client.Timeout` token.
5. Escalation clause written as binding: a hidden-audit finding is a Blocker and the re-gate is tier 1 Opus; the verdict last line then is `STOPPED: NEEDS TUESDAY`.

## Open questions, each with a recommended answer
1. **G row: G2 (Sonnet) or G1 (Opus)?** The guard sits on the append-only audit path, arguably a security/audit surface. Recommend G2 Sonnet as instructed, with the escalation clause (already in the brief), because the mechanism was measured by B304 and the change is one condition plus tests.
2. **Round count under the cap.** Recommend counting PR #165 as round 1 of 2 (new PR; B304 returned GO WITH FINDINGS, so no NO GO has been spent). Tuesday may overrule at stamp.
3. **Launch with CI still pending?** Recommend yes (as ruled for B304); the brief makes the verdict conditional with a `(CI pending: …)` suffix unless every check and all four Analyze legs completed.
4. **Port block.** Recommend none needed (in-process host); `7900-7909` reserved, chosen because no brief names it and it is unlistened (measured).
5. **Stamp.** Tuesday fills the two slots at launch; recommend main still c149a30 at stamp (re-read `ls-remote` first). If main moved, re-draft only if it touches the four PR paths.
6. **`brief_seat: model=` line.** The builder could not see its own. Recommend Tuesday quotes the printed line in the launch tap so the gate STATUS can record it for the routing pilot.
7. **Should the gate read the B300 STATUS / `history.md`?** The brief lets it, read-only and only outside Restricted paths (neither is). Recommend leaving as written; it is optional input for question 7.
8. **Jira comment byte-equality (39834/39835).** The gate cannot read the builder's `.tools/b356/texts/` (another seat's tree), so byte-equality is NOT TESTED by design; recommend Tuesday's records seat compares them, or accept the gate's live-text checks.
