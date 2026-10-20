# B372 drafter report (2026-10-21 ~06:10 AEDT)

Brief: `2026-10-21_B372_SEAT-D11_hpsmpoc-305-guard-tests.md`. Shape copied from B364.

## Stamp slots
Two slots, `@MAIN@` (main sha at launch) and `@STAMP@` (stamp time, launch authority, answered drafter questions). Fill both; a `.pre-stamp` copy should read 2, the stamped copy 0. The drafter did not make the `.pre-stamp` copy.

## Questions for Tuesday (each with a recommended answer)
1. Q1. Tier 2 (G2) with an `api/src` STOP, as B364? Recommend YES: test-only, mechanism and both mutants measured by gate B357.
2. Q2. Sonnet row C2? Recommend YES, same as B364.
3. Q3. Allow at most one new `Support/` file? Recommend YES but unlikely to be needed (the existing factories and `RowsOf`/`StateOf`/`PastTheBound` helpers cover both rows).
4. Q4. Include the optional comment-only fix for B357-3 (comment at `ImportFailGuardTests.cs:234`)? Recommend YES, only if it stays a few lines. B357-1 (product check-then-act) and B357-4 (mutant `ge`) are excluded; consider filing B357-1 as its own ticket (it is a product change, tier 1).
5. Q5. Mutant application: the brief has the seat mutate `ImportEndpoints.cs` in its worktree with the new rows present, and restore it. Recommend YES (same as B364's "mutants live in the worktree only").
6. Q6. Is a single commit right? Recommend YES (one test file, two rows).
7. Q7. `dotnet build-server shutdown` is forbidden in this brief because B371 is live. B364 required it at release. Recommend keeping it forbidden until B371 ends.

## Could not verify (all marked UNMEASURED in the brief)
- No `gh` run (fenced), so open PRs touching `api/tests/HpsmPoc.Api.Tests/Imports/` are unread. Tuesday must check before launch. Only the B371 PR #166 file list (from the task) is known.
- No dotnet run: baseline counts, whether the two new rows are GREEN at main, which test goes red under gd and gr, and whether either mutant also turns an existing row red.
- The FK needs of planted rows: whether an `import_file` row exists for a refused run, and how to cheaply make a `partial` run. I read neither `ImportRobustnessTests` nor `ImportFailurePathResidualTests`.
- The gate's own R2g/R2h probe code (under `Briefs/2026-10-21_B357_evidence/` and `.tools/b357/`) was not read. The brief points the seat at it.
- Which `lock.sh` to use (`.tools/b198/` per B364, `.tools/b300/lock.sh` is present), and whether `post.py` and `read.py` exist in `.tools/b300/` (my `ls | head` listed only `jira.py`, `lock.sh` and others).
- Whether 7380-7389 is free (no `lsof`). Panes live: not listed. `AGENTMAIL_API_KEY` absence is relayed from B364.
- Machine load at 06:01:03 was 7.54 / 6.55 / 6.67, under 8 with a thin margin.

## Measured, for Tuesday
- Main is `6818896b68090777c8edbf0e694741928c96ca3f` (ls-remote 06:01). No `b372*` ref on origin. `b364/feedback-pkcs-test-gaps-294-295` is on origin (`777f29c3`).
- HPSMPOC-305 is Backlog, created 2026-10-21T04:09:31+11:00, 0 comments, 0 links.
- `FailOnceAsync` is `ImportEndpoints.cs:304-332`. The five row deletes are `:310-314` inside `if (dropRowsOf is not null)` `:308-315`. The guard is `:323`. `FailAsync` is `:290-302`.
- `ImportFailGuardTests.cs` is 331 lines. Helpers: `RowsOf` `:105`, `StateOf` `:114`, `PastTheBound` `:127`. The nearest model for a new row is the null-reason row `:265-286`. The B357-3 comment is `:234`.
- Stale-ticket check: the ticket's line cites match main. The ticket's Done-when is the two rows only; B357-1, -3 and -4 are Notes.
- gd and gr are defined in the brief from the ticket and B357 (`:72-73`): gd moves the `:323` guard above the deletes, gr drops `run.Status == "failed" &&`. B357 describes the gr mutant as "status clause dropped", which I read as dropping the `run.Status == "failed" &&` clause. Please confirm if you want the exact mutant text pinned.
- The brief says "Row gd" with a first `FailAsync` call to make the run failed-with-reason. B357's R2g plants rows after the sweep. The brief lets the seat choose how to reach the failed-with-reason state.
