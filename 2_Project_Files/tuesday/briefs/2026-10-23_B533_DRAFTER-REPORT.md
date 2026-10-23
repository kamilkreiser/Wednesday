# Drafter report: B533 (SEAT-G59), MPS Calculator tier-1 QA gate on PR #99 (B519 pricing-policy leak tests and fixes)

Drafted 2026-10-23 about 13:50-14:05 AEDT (clock `date`) by Tuesday's read-only gate-kit drafter (Sonnet 5.5, row C8). Wrote only: the kit, its `.pre-stamp` (made with `cp`, `cmp` equal) and this report. Nothing stamped, launched, sent, published, fetched, built or run in the project; no decision-queue tool, no Artifact/Docs/mail/chat, no HTTP to any app or hosted host, no `az`, no Jira.

## BLUF
Kit is ready for Tuesday to read and stamp. B533 was free (no other file carried it; B531 was the highest number present), so the number stands. Tier 1, Opus (`claude-opus-5-5`, read from `models_latest.json`), `BRIEF_SEAT_LEVEL=opus`, round 1 of 2, pane `Datasec/MPS-G59`, ports 8750-8759 (none needed). PR #99 head `25cb3657`, main `e027ebd0`, both re-pinned by me at 13:52 (nothing moved from the builder's STATUS). **CI on the head is NOT finished: at 13:52 five of eight check-runs were in progress (dotnet, web, python, Analyze csharp, Analyze javascript-typescript) and `package` had not appeared; 0 open alerts but only 2 of 4 analyses.** The kit makes the verdict wait for that.

## Files
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B533_SEAT-G59_mps-b519-pricing-policy-gate-tier1.md` (106 lines).
- `.pre-stamp`: same path plus `.pre-stamp`, byte-identical.
- This report.

## Slots left for Tuesday (8 slot lines plus the last line = 9 lines with the pattern)
STAMP; LAUNCH WINDOW; Stamped by; Launch authority; Hard stop and target (suggested target verdict 2 h, hard stop 3 h after launch, as asked); Head, main, PR #99 state and the PR's check-runs at launch (this is the "Main at launch" slot, widened because the PR and its CI are the moving parts); Model receipt line and load1 (drafter's line: `model: claude-opus-5-5 -- G1 -- P1-P4 none -- gauge 95% (Tuesday no-90% grant)`); Pane free and **Q-1** (may the gate use scratch xunit rows and scratch source edits in its own worktrees under `.tools/b533/`; checks C3-C6 need YES or they are NOT TESTED as behaviour); and the last line `READ-WHOLE-BY-TUESDAY: ____`.
Counts (`/usr/bin/grep -c -E` with the pattern split by quotes): kit 9, `.pre-stamp` 9, a one-line scratch control (`x` plus four underscores) 1. Other scans of the kit: non-ASCII bytes 0, `@[A-Z_]+@` pattern 0, person-name word list (Kam, Kamil, Kreiser, Paul, Friday, Wednesday) 0, decision-card shape 0.

## What I read
- Shapes, whole: `2026-10-23_B524_SEAT-G57_mps-b517-docs-gate-tier2.md.pre-stamp` (slot format, pins, load rule, verdict shape, severity floor) and `B524_DRAFTER-REPORT.md`; `B505_SEAT-G53_hpsmpoc-b501-telemetry-gate-tier1.md` (structure only: findings with severities, mutation by committed row name, attack and differential rows, CI-complete rule, hard stop, last-round wording).
- Subject: builder brief B519 (123 lines) and builder STATUS B519 (139 lines), both whole.
- Head, by `gh api -X GET ... contents?ref=25cb3657` raw: `PricingPolicy.cs` (whole, 208 lines), the three new `LeakLayer*.cs` files (whole), the test-row names of `PricingPolicyTests.cs`, `ci.yml` lines 1-45 plus greps, the Api test csproj (whole). Also `pulls`, `pulls/99`, `pulls/99/files`, `check-runs`, `code-scanning` alerts and analyses, `rules/branches/main`, `ls-remote`, `uptime`, `lsof`, `ls` and the heavy-slot holders, and greps of the briefs folder for port blocks. The project `CLAUDE.md` and `CLARIFICATIONS.md` were only grepped (the kit tells the gate to read them whole).

## Decisions where I used judgement
- **Verdict wording.** The task named `VERDICT: GO|NO GO round 1 of 2 on #99 @ <sha>`; B524's real shape is a `GATE VERDICT B...` first line and a `VERDICT: B...` last line. I kept both lines, put `round 1 of 2 on #99 @ 25cb365` into the first line, and kept the three tokens (GO / GO WITH FINDINGS / NO GO) because both templates and the severity floor use them; a NO GO line must end `majors+: B533-n, ...` listing every Major and Blocker by id.
- **Mutation list.** "Revert to first match only" is mutant (a), at all five sites and per site; "drop one leak field from the guard" is mutant (e), one field at a time across `SameLine`, `RatesChanged`, the usage comparison, the dropped-price loop and the step 1 internal-input checks; the test-side guard (the six-name allow-list) has its own mutants (i).
- **Added a differential check (C6)** the task did not name but the fix shape calls for: the new multiset rule must never allow what base refused, and for unique keys must equal base byte for byte. The gate writes its own invariant and seed (not 519197) before running.
- **Attack rows (C5, A1-A7)** cover the four you named (repeated numbers, case/whitespace variants, a supplies line priced without authorisation, mixed purchase/rental) plus: every write path to a stored draft (does each reach `Apply`), step 4 hidden-input transplant, and amplification (the policy is quadratic in places: `PricingPolicy.cs:88` and `:106-112`) with a response-size row for the `:123` echo of a request string.
- **Semantic overlap with B518** (C9): that lane edits the callers of `Apply` and validation, so file-disjointness is not enough; the kit asks the gate to read B518's diff once it is on origin.
- **Ports 8750-8759.** The 2026-10-23 briefs allot blocks up to 8740-8749 (B530); B527-B530 mention `8700-8799` only as a scanned range; no brief names an `875x` block; `lsof` empty.
- The CI pass predicate is stated in the kit: `dotnet test` exit code with no filter and warnings as errors; **a skipped test does not fail CI**, so the gate counts skipped itself.

## Leads for the gate recorded in the kit (drafter reading of the code at the head; none is a finding)
- D-1 lets a restricted caller move a price between lines of one number; whether that can move a customer total is for C5 A1 to measure.
- `PricingPolicy.cs:123` (and `:50`, `:57`, `:64`) echoes a request string into the 403 detail; compare with base.
- Quadratic shapes at `:88` and `:106-112` with no cap in this file (the input cap is another lane's).
- The class header comment (`:6-10`) names two people; the kit tells the gate never to quote it and to check whether it is in the base blob.
- Rental credits and the `Credit` flag belong to a sibling lane; the kit classes anything equal at base as a FACT for Tuesday.

## UNMEASURED (and the instrument that closes each)
- The three tickets' Done-when text (I did not read Jira): the gate reads MPSCALC-197, -211, -104 by Jira GET in C2. Until then the Done-when list rests on the builder brief's restatement.
- Every runtime figure (Api 1994, 27 names, 22 ran / 13 red at base, mutants 7 of 7, the 600-case property): builder's, RELAYED; closes by the gate's own C3, C4, C6, C7 runs.
- Final CI result and the other two analyses (csharp, javascript-typescript): closes by re-reading `check-runs` and `analyses` at the verdict (C8) or Tuesday's read at launch.
- Whether the header-comment names are in the base blob: closes by `git show e027ebd:src/MpsCalc.Api/Quotes/PricingPolicy.cs` in C1.
- The port-block listener control (I ran no bind): the gate runs it in REFUSE.
- Whether a stale heavy-slot holder still exists: at 13:52 slot 1 was absent, slot 2 held by B520 and slot 3 by B518; holders change by the minute.
- `AGENTMAIL_API_KEY` presence in the project `.env` (not opened): the kit's mail line is conditional on it, copied from B524.
- Directory.Build.props `TreatWarningsAsErrors` is taken from the workflow comment, not read.
