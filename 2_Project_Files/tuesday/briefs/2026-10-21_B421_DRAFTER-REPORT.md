# B421 DRAFTER REPORT (HPSM-POC PR #178 tier-2 gate kit, SEAT-G29)

Drafted 2026-10-21 20:26-20:45 AEDT by a Sonnet drafter. Kit: `2_Project_Files/tuesday/briefs/2026-10-21_B421_SEAT-G29_hpsmpoc-pr178-gate-tier2.md` (unstamped).

## Slots (2 unfilled, on purpose)
- `@STAMP_TIME@` (Stamp paragraph) and `@LAUNCH_AUTH@` (Stamp paragraph). `grep -o -E '@[A-Z_]+@' | wc -l` on the kit = **2** (measured). Also fill the last line `READ-WHOLE-BY-TUESDAY: (added at stamping)`. Same slot set as B413 (its `.pre-stamp` differs from the stamped file in exactly those 3 places). I wrote no `.pre-stamp` sibling (two files only), so keep a copy before stamping if you want the slot-count control to be the file itself.
- The Stamp names hard stop 23:30 AEDT, target verdict 22:45, pane `Datasec/HPSM-POC-G29`, ports 8010-8019, B421, Sonnet, round 1 of 2, row G2 (`model-routing.md:109` read and quoted).

## What I measured (read verbs only; no fetch, no npm/dotnet/bicep/az/HTTP)
- `ls-remote`: main `ae7a2c86…`, `refs/pull/178/head` = `b418/uat-template-drift` = `6340699e…`. `gh api` agrees. No `b421*` ref. Both shas are present in the local object store.
- `gh api pulls/178`: open, not draft, mergeable true, state blocked, base `ae7a2c86`, 3 commits, 6 files, +156/-7, only open PR.
- `compare`: ahead 3, behind 0, merge-base = main (not diverged). 6 files with per-file +/-. The 7 deleted lines are enumerated in the kit: 1 in the C#, 2 in `appservice.bicep`, 4 in the infra test file (comment, table entry, `assertNotIn`, `assertEqual` tuple).
- CI at the head at 20:26: 4 complete (gitleaks success, dependency review success, Analyze(actions) success, CodeQL neutral); 9 in progress (api, infra, web build, web unit tests, two SQL Server shards, three Analyze legs); `web (Next.js)` not yet listed. Code-scanning: 1 analysis (actions, head sha, 0 results); open alerts on `refs/pull/178/head` 0. Required contexts: 5, `strict` false.
- CI commands read from `ci.yml` at main: api job `:49/:71/:86-87`, shard filters `:247/:250`, infra job `:560-612` (Bicep v0.47.16, `validate.sh`, which runs `test_security_baseline.py` at `validate.sh:21`).
- Head `Read` code, head README insertions (step 7 paragraph at `:164`, one UAT sentence at `:235`) and the 8-line `uat.bicepparam` comment read through `git show/diff`. Not read: the new test bodies in `UatOpenTests.cs`, the test-file `+` lines (the gate does).
- Environment: load `1.88 2.63 3.27`; ports 8010-8019 0 listeners (11 unfiltered); `.tools/b421` and `wt-b421-*` absent; `.tools/b198` present.
- Builder STATUS and brief read whole. I did not open any `.tools/b4*` tree or evidence file.

## Design choices in the kit
- Every builder number is marked RELAYED and every control is the gate's own: its own Bicep evaluator over the compiled template (not `value_in`/`inert.py`), its own probe class `G29Probe` for D3 (base first, then head), its own 3 mutants plus the builder's m3-a..d rebuilt from the STATUS text, its own infra mutants (banner restore, address list tampers) so the four edited expectations are shown to still bite.
- Escalation rule written into the Stamp: any cell that did not open at base but opens at head, exact `true` not opening, or any file outside the 6 means hand to G1 (Opus) and STOP.
- Two traps I put in the kit: (1) the new refusal message contains the constant `'true'`, so a naive "message does not contain the value" check is wrong; the gate checks the full padded/case string and proves the instrument with an own mutant that interpolates the value. (2) Do not run `dotnet build-server shutdown` (the builder did; it stops other seats' servers); build with node-reuse and shared compilation off instead.
- Slots sized to B413: REFUSE, Stamp, Step 0, launch line, HOLD, 8 checks (EQ/partition, D1, D2, D3, D4, suites, CI+CodeQL, secrets+merge), severity, verdict line, NOT TESTED BY DESIGN.

## Findings about the builder's claims (for the gate to settle, flagged in the kit)
1. **"1 of 156 cells differ" looks short by one (UNMEASURED prediction).** uat's `ForwardedHeaders__KnownProxies` also changes from `''` to the 25-entry list when evaluated with each tree's own parameters, so I expect 2. The kit asks the gate to reconcile and treat it as a correction to the builder's instrument, not a defect, if it reads 2.
2. The builder kept `GetValue<bool>` on the non-exact path (DESIGN D3). That keeps the binder's start-up failure for `""`/`on`/`1` and its value-printing message (B417-5). It differs from the brief's "replace" wording but is the only way to keep those cells unchanged; the kit makes B417-5 a Note.
3. The README edit also has a second hunk (one sentence in the UAT paragraph). The brief's partition allowed it ("if true after your change"); the gate checks each claim in it.
4. D1b/D1c are rule-sensitivity rows that are red only against the OLD table (the builder labels them so). The kit makes the gate judge the label (Minor if unlabelled).

## Questions, with recommendations
1. **Tier.** D3 touches the sign-in surface. Recommend keep tier 2 as ruled: the edit only adds a refusal, B417 (G1) measured the mechanism, and the kit carries a hard hand-to-G1 rule. Alternative is tier 1 for check 4 only; I do not recommend it.
2. **Launch timing.** CI is still running (9 jobs, `web (Next.js)` not listed). Recommend launch as B413 did (re-read CI at start, mid, verdict) as soon as load allows (load1 is 1.9), so the verdict can land well before 22:45. The kit's wait is on the SQL Server shards; they are the longest legs.
3. **Dependabot.** The builder saw "1 high on the default branch" on push. I made it a GET-only Note (count, package, whether it is on main) and the kit says do not dismiss. Recommend ledger it for you, not the gate.
4. **Freeze.** I carried the "Wednesday 23:59 AEDT freeze" from the B413 kit as RELAYED and did not re-measure it. Confirm it still applies before the hard stop of 23:30 stands as the gate's deadline.
5. **Live prerequisites for the deploy seat (not the gate's).** The new C# refuses to start unless the live `Auth__UatOpen__Enabled` is exactly `true`; the live address list was read at 18:47 and cannot be re-read without `az`. The kit puts both in FOR TUESDAY; recommend the deploy seat does them before the next UAT template deploy.
