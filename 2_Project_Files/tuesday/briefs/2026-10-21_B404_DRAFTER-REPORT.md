# B404 drafter report (2026-10-21 14:15-14:19 AEDT, clock from `date`)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B404_SEAT-G25_hpsmpoc-pr171-gate-tier2.md` (40 lines, long paragraphs; slots `@STAMP_TIME@`, `@STAMP_HEADS@`, `@LAUNCH_AUTH@` counted 1 each by `/usr/bin/grep -o -E '@[A-Z_]+@' | sort | uniq -c`, so the stamped copy must read 0 and the `.pre-stamp` copy 3; last line `READ-WHOLE-BY-TUESDAY: PENDING`). Shape copied from B395 (read whole, 40 lines).
Read whole: B395 brief, B383 brief (112 lines), B383 ADDENDUM-1 (14), B383 STATUS (315). Read in part: B402 brief `:50` (R5), B402 STATUS (`:54`), B403 STATUS (`:17,:26,:66`), `model-routing.md:105-112`, B395 drafter report.

## Measurements (read verbs only; instrument named; none of dotnet, merge-tree, fetch, Jira, az, HTTP to app hosts)
- `git --no-optional-locks -C '.../2_Project_Files' ls-remote origin refs/heads/main refs/pull/171/head refs/heads/b383/... 'refs/heads/b404*'` at 14:15:28: main `ec0a62a1ac107e26d859b5eebd220153a0cf691c`; PR head and branch `cc3eae47a995652700e26fca00a6f3023f87530d`; no `b404*`. `rev-parse refs/remotes/origin/main` = `ec0a62a1…`; `cat-file -t` of both = commit (local checkout holds both objects; its `refs/pull/*` are not fetched, so `log refs/pull/171/head` fails there).
- `gh api pulls/171`: open, draft false, mergeable true, `mergeable_state` blocked, commits 1, changed_files 1, base `54fbceac` (old main), body = BLUF only (no closing keyword). `pulls/171/files`: one `added` file, +413/-0. `pulls` (open list): only #171.
- `gh api compare 54fbceac...ec0a62a1`: ahead 6, behind 0, 45 files, **none under `Assessment/Persistence/`**; includes `web/package-lock.json` and `web/package.json`. `compare ec0a62a1...cc3eae47`: ahead 1, behind 6, merge-base `54fbceac`.
- `branches/main/protection/required_status_checks`: strict false; 5 required contexts (listed in the brief).
- `commits/cc3eae47/check-runs` (14:16): `web build (...)` failure (job 118921269860, failing step = the all-dependencies `npm audit`), `web (Next.js)` failure (REQUIRED, job 118923322443), `api on SQL Server (api-other-and-feedback)` failure (job 118921270075, step `dotnet test on SQL Server, this shard`), `api on SQL Server` failure (aggregate, 118927571647); the rest success, e2e skipped. Run times 2026-10-20 22:2x-22:40Z, i.e. before main's 6 commits. `commits/ec0a62a1/check-runs`: 19, all success (`dependency review` skipped). `commits/cc3eae47/status`: pending, 0 statuses.
- `code-scanning/analyses?ref=refs/pull/171/head`: 4 analyses at `cc3eae47` (actions, python, javascript-typescript, csharp), 0 results each; open alerts on the PR ref 0, on main 0 (control returns 0 too, so non-discriminating; noted in the brief).
- `uptime` 14:15: `1.42 1.33 1.40`. `lsof -nP -iTCP -sTCP:LISTEN`: 11 lines unfiltered (control), 0 on `7620-7629`, `7630-7639`, ... `7920-7929`.
- NOT measured by me: the 413-line test file's contents (not read), whether main's `ci.yml` runs `Assessment.Tests` in `api (ASP.NET Core)` (the only `dotnet test HpsmPoc.slnx` line I saw is at `ci.yml:35` in the stale local working checkout; the brief says so), the failing test names of job 118921270075 (log not fetched), whether `web/package-lock.json` change is the cause of the old head's red audit step (inferred from the step name and B395's subject; the brief makes the gate prove it).

## Slots
- `@STAMP_TIME@`: stamp time line ("stamped by Tuesday at <time> AEDT (brief read whole by Tuesday, N lines + drafter report; drafter questions at their recommended answers: ...)").
- `@STAMP_HEADS@`: main and PR head re-read at stamp (`ec0a62a1…` and `cc3eae47…`; if main has moved, say so, the REFUSE check tolerates a move that does not touch `Persistence/`). End with a full stop.
- `@LAUNCH_AUTH@`: the authority sentence. The brief already appends the 2026-10-16 grant and the 2026-09-01/09-05 gate rule after the slot in brackets; if you prefer the slot to carry all of it, delete my bracket.

## Corrections to your instruction
- You said the non-required shard's tracked reds are "listed in B402_STATUS R5": R5 is defined in B402's **brief** `:50` (four names: `RequestTimingLogTests`, `AutomationRouteTests`, `Hpsmpoc214Tests.N1`, `FeedbackAttachmentDeliveryTests.Route_B_with_no_files_makes_no_attachment_call`); B402's STATUS `:54` only says R5 was not needed (all 15 jobs green at `ec0a62a1`). HPSMPOC-308 is in B403's STATUS (`:17,:26,:66`), not B402's. The brief cites both where they are.
- The head's CI **is red on a REQUIRED context** (`web (Next.js)`, from `web build`'s audit step), which is why `mergeable_state` is blocked; that is almost certainly the stale base (PR #172's lockfile is in main now), so the brief makes the gate say `update-branch needed` and name the consequence (new head sha, `--match-head-commit`, CI again).

## Questions (recommended answers)
1. Do `update-branch` BEFORE the gate (so it tests a head whose CI is current) rather than after? Recommend after: the gate predicts the merged tree locally (`-merged` worktree and legacy merge-tree) and you update once on GO; but if you want a single round with live CI, update first and restamp `@STAMP_HEADS@` with the new head (the brief then needs its `cc3eae47` strings replaced).
2. Tier 2 for a test that pins tier-1 migration behaviour? Recommend yes (B383 STATUS `:268` and the stamp rule allow it; the brief escalates to tier 1 on any non-test path).
3. Whole `HpsmPoc.Api.Tests` run? Recommend no (not required; the PR compiles into `Assessment.Tests` only); the load is 1.4 so the gate may do it last at its option.
4. The gate designs its own mutants (not the builder's 8)? Recommend yes (as written); costs about 12-15 `dotnet test` runs of one class.
5. Ports `7920-7929`: free by `lsof` and absent from every file in `tuesday/briefs/`; older blocks up to 7919 and 7970-7979 (B357) are taken. OK?

## Not done
No file other than the two named was written. No Jira read or write, no `.tools` tree opened, no dotnet.
