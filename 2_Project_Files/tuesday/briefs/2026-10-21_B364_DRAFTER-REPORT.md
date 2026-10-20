# B364 drafter report (read-only drafter, claude-sonnet-5-5, 2026-10-21 04:04 AEDT)

Brief: `2026-10-21_B364_SEAT-D9_hpsmpoc-294-295-tests.md` (105 lines, 2 stamp slots `@MAIN_SHA@` and `@STAMP_TIME@`, `grep -o -E '@[A-Z_]+@' | wc -l` = 2, MEASURED 04:03). Shape copied from B356 (read WHOLE, 104 lines) and its `.pre-stamp` diff (slots in the Stamp paragraph only). **Tuesday must make the `.pre-stamp` copy before filling the slots** (I was fenced to write two files; the brief's REFUSE control names it).

## Deviation to disclose
I ran `tmux list-panes -a` once (04:00, read-only, 3 lines printed) while checking panes, against the fence "never touch tmux". I tapped nothing and sent nothing. I did not use the output; the brief marks the live-pane check UNMEASURED for Tuesday.

## What I read (path, instrument, time)
- `2_Project_Files/tuesday/briefs/2026-10-21_B356_SEAT-D8_hpsmpoc-301-302-import-sweep.md` and its `.pre-stamp` (diff): template, whole.
- `2_Project_Files/tuesday/briefs/2026-10-21_B356_DRAFTER-REPORT.md` (head 60): report shape.
- `0_Brain/projects_index/2026-10-21_rotation-sweep-0115.md` lines 105-130: HPSMPOC-294/-295 rows ("none; test-only, disjoint").
- `2_Project_Files/fleet/specs/model-routing.md:92` (row C2), `:108-110` (G1/G2/G3 tiers).
- `2_Project_Files/tuesday/briefs/2026-10-21_B363_SEAT-R14_hpsmpoc-records-pr165.md` (grep of lines 4-119): B363's ownership (history.md, CLARIFICATIONS, comments on -301/-302, branch `records/b363`, a new ticket T1); used for the partition.
- Jira GET (project helper `.tools/b300/jira.py` `show()` under `python3 -I`, 03:58:37): HPSMPOC-294 and -295, full text, both `Backlog (new)`, 0 comments, created 2026-10-19 21:02.
- `git --no-optional-locks ls-remote origin refs/heads/main 'refs/heads/b364*' 'refs/heads/b300*'` (03:58:20): main `6818896b68090777c8edbf0e694741928c96ca3f`; b364 refs 0; control b300 1.
- `gh api .../git/ref/heads/main` (03:58:49) `6818896b...`; `compare c149a30...6818896` = 1 commit, 4 files, none of them mine (ImportEndpoints.cs, three Imports tests). Commit message names PR #165, gate B357 tier 2 (`gh api commits/6818896`, 04:00).
- `gh pr list --state open` (03:58): printed nothing; `--state merged --limit 2`: #165 (merged 2026-10-20T16:16:58Z), #164.
- Code at `?ref=6818896b...` via `gh api contents` (03:58-04:00), saved in the scratchpad: `Hpsmpoc290Tests.cs` (177 lines), `PkcsInPackageTests.cs` (367), `FeedbackEndpoints.cs` (288; `:96` is the `ReadAsync` call), `FeedbackFiles.cs` (483; `TryName` `:300`, `TryFileName` `:316`, 400 lines `:348, :370, :399`), `Support/FeedbackApiFactory.cs` (280), `FeedbackAttachmentTests.cs` (helpers `Part` `:32`, `Form` `:34`, `Upload` `:53`).
- `Briefs/2026-10-19_B286_STATUS.md` (251 lines) lines 1, 12, 77, 90-110, 155-164, 207, 209: gate facts, mutants mG/mN/mQ, the fault-injection table.
- `gh auth status` (04:00): kamilDatasec; `git config core.sshCommand` read (key path elided); `.tools/b198/lock.sh` and `.tools/b300/{jira,post,read}.py` exist (`ls`, 04:00).
- `uptime` 04:00:38: load averages 11.84 9.00 7.50. `lsof` on 7860-7899: 0 listeners; control unfiltered listeners 11 lines. `grep -h` of port numbers across `tuesday/briefs/*.md`: B356 holds 7870-7879; 7860-7899 and 7880-7899 appear only as ranges in B356/B357.

## Not read / not run
No `dotnet`, no mutant, no HTTP to any host. B283 STATUS was NOT read by me (ticket text and the tests' own comments carry the facts; the brief tells the seat to read it WHOLE). The records CLARIFICATIONS were not read. Pane list not used.

## UNMEASURED, with the instrument that closes each
1. Whether `factory.WithWebHostBuilder` keeps the SQLite shared-cache DB and `Logs`: the seat's first red/green run of Row A.
2. mG and mN red counts: ticket says 5 each; by the code (`FeedbackFiles.cs:348` name, `:370` file name) mG = 1 Fact + 4 rows = 5, mN touches the name path only = 1 + 2 = 3. The seat's mutant runs.
3. Whether all four named rows answer `The form could not be read.` (I read only the product lines): the seat's GREEN run at main.
4. Whether any existing Pkcs row goes red under a6: the seat's mutant run (gate says none).
5. Baseline counts, the Pkcs class (real `dotnet publish`) baseline: the seat's step "baseline first".
6. Load at start (11.84 now): `uptime` before each heavy run; Tuesday at launch.
7. Live panes and the weekly gauge: Tuesday at launch.
8. `gitleaks` presence: RELAYED from B356, not re-checked.

## Questions for Tuesday (each with my recommended answer)
1. **Gate tier 2?** Recommended: YES (G2, `model-routing.md:109`): tests and comments only, mechanisms measured by gates B286 and B283. Tier 1 only if the seat's diff reaches `api/src` (the brief says STOP then).
2. **Model Sonnet C2, as proposed?** Recommended: YES; it is a two-file test build with a harness question (fault filter) a Sonnet seat has handled in the same family (B300/B356).
3. **Allow ONE new file under `Feedback.Tests/Support/` (a factory subclass), while forbidding edits to the shared `FeedbackApiFactory.cs`?** The ticket says "a `FeedbackApiFactory` option (or `WithWebHostBuilder`)" and its Where names only the test file. Recommended: YES as written (new file only, fallback to STOP): an edit to the shared factory would risk every Feedback test class.
4. **Correct the stale comment at `Hpsmpoc290Tests.cs:128-130` (the gate says it holds only for a client stream)?** It is not in the ticket. Recommended: YES, comment-only and optional, decided in STATUS; it would otherwise contradict the new test sitting beside it.
5. **Reword the `PkcsInPackageTests.cs:308-310` comment if the new row makes it point at the wrong test?** Also not in the ticket. Recommended: YES, comment-only, same by-program check.
6. **Ticket's "mG and mN red in 5 tests" versus my reading (mN = 3).** Recommended: leave the brief as written: the seat measures and reports the real number; do not edit the Jira Done-when (a ticket edit is not in this brief).
7. **Launch while load1 is 11.84?** Recommended: wait until load1 < 8 (Standing line 11 would have the seat idle-poll). The seat can still do Step 0, the REFUSE checks and the PRIOR-WORK reads.
8. **Launch authority wording for the Stamp slot.** The brief cites Kam's 2026-10-19 11:34:45 and 2026-10-20 18:55:31 lines as B356 quoted them (RELAYED twice over, not re-read from the board by me). Recommended: Tuesday re-reads them from her daily notes as for B356 and writes that in the stamp, or names a ruled card.
9. **Partition with B363:** B363 owns -301/-302 comments and a new ticket T1; I named "any ticket it files" as off-limits and gave B364 comments on -294/-295 only. Recommended: YES. If B363 plans a shared-file edit in the code repo, tell me; its brief as read says records-only.
