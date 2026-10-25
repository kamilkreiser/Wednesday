# B558 DRAFTER REPORT (2026-10-24 05:33-05:45 AEDT, Sonnet drafter, read-only)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B558_SEAT-H8_hpsmpoc-test-followups-329-332.md` (118 lines; sha256 `8921fe750e3c177a95246bdc6e49ef9f190b66d7f130c37a2baf9365f05cd7fc`) and its `.pre-stamp` copy (`cmp` equal). Unstamped copy reads **8** lines with the four-underscore pattern (`/usr/bin/grep -c -E '_''_''_''_'` = 8 on both files; the 7 slot lines + the last line). 0 non-ASCII lines.

## Facts measured (command -> output)
- main: `git ls-remote origin refs/heads/main` (05:33) -> `31dabc8d3012d28b0dbf510ea90760a42e319730`. `git log --oneline -1` -> "A 400 shows the API's sentence for a customer-name refusal only (#203)". `gh api pulls/203 --jq '[.merged,.merge_commit_sha]'` -> `[true,"31dabc8d..."]`. Matches the sha you gave.
- `gh pr list --state open` -> `[]` (0 open PRs). `tmux list-panes -a -F '#{@cockpit_name}'` -> `tuesday`, `Datasec/MPS-M2R`, `fleet-monitor` (no HPSM-POC seat). `gh api git/matching-refs/heads/b558 --jq length` -> 0; `find .tools -name 'b558*' / 'wt-b558-*'` -> 0 (control `b554*` -> 1). `refs/heads/b548/...` still on origin at `e5c2774c` (squashed as #203; history branch).
- Blobs at main: attribution-preview.test.ts `6aebef65...`; Api `Support/HostStartRetry.cs` `e402defe...`; client.describeFailure.test.ts `d14f764f...`; client.ts `f49adb1d...`.
- 329: `EXACT_NUMBER` at `attribution-preview.test.ts:22`; digit rows `:179-186` use digits 1 and 0 only; flagged table `:188-199` holds 8 cells (letter, underscore, dot, hyphen each side). The regex lives in the TEST file, so those mutants are scratch mutants of the test file itself. Gate text RELAYED `B549_STATUS.md:188,211`.
- 330: `HostStartRetry.cs:30-36` walk; `grep -c -F 'e = e.InnerException'` in that file -> 1 (control 0). `ApiFactoryHostStartRetryTests.cs` holds 0 `InvalidOperationException(` (no wrapped row); `Forge`, `LockLost`, `OtherLockText` already exist there; `HostStartRetry.Run` `:40`. Feedback twin pins a wrapped fault at `HostStartRetryTests.cs:47` (that copy only).
- 332: table at `client.describeFailure.test.ts:147-154`, 4 cells, matches the gate's cite (`B554_STATUS.md:334-339`).
- CI: `ci.yml:249-253` the second SQL Server shard filter is `FullyQualifiedName!~HpsmPoc.Api.Tests.Assessment.`, so `Hosting.*` rows run on SQL Server there. `HPSM_TEST_SQLSERVER` was UNSET for B549 (RELAYED). Repo dotnet: `.tools/dotnet/dotnet --version` -> `10.0.402`; `dotnet` is NOT on the drafter's PATH. Docker exists on the machine but standing line 4 forbids it.
- Ports: `lsof -nP -iTCP:8930-8949 -sTCP:LISTEN` -> nothing (rc 1); `8480-8499` nothing. Block picked **8940-8949** (grep `894[0-9]` over all briefs -> no hit; highest named: 8920-8929 and ranges 8890-8930/8910-8930).
- load: `uptime` 1.76 (05:33), 2.43 (05:34).
- Routing: the table has no row literally titled "Sonnet first: test-only pins". Nearest: L6 "Test-only pin" (Sonnet is its "1st fallback" column) and C2 (Sonnet build seat). Model line in the brief: `model: claude-sonnet-5-5 -- L6 test-only pin (Sonnet = the fallback column; build-seat rule C2) -- P1-P4 none -- gauge: ...`.

## Judgement calls for Tuesday at the stamp
1. **Api partition.** You said "one api test support file". The row cannot live in `Support/HostStartRetry.cs` (it is the subject, holds no tests, and its line 1 says it is a byte copy of the Feedback file). I put the Api row in `api/tests/HpsmPoc.Api.Tests/Hosting/ApiFactoryHostStartRetryTests.cs` and made `HostStartRetry.cs` read-only (scratch-mutant target only). Confirm or overrule.
2. **Routing row text** (above): L6/C2 chosen; edit the model line if you meant another row.
3. **Gate tier:** suggested tier 2 (tests only); your call.
4. **Ticket key in test names:** I kept B548's rule (no ticket key in test names or commit messages); the existing #198 rows already carry "HPSMPOC-325" in titles and are not touched.
5. **Mutant breadth for 329:** I asked for program-generated families (20 digit mutants, 64 punctuation mutants) beyond the two named survivors; trim if too heavy for a Sonnet seat. 332 allows 2-3 cells (up to 5 if Mfi/Mfe survive); 330 adds Q11b (depth cap) and Q11c (text check dropped) and a double-wrapped row.
6. **SQL Server:** the brief makes the Api row factory-free, DB-free, env-free (an argument, not a measurement) and requires `UNMEASURED-ON-SQLSERVER` locally; the proof is the PR's two shard TRXs. If you want it measured before the PR, a SQL Server must be provided to the seat (docker is forbidden to it).
7. Hard stop/target READY suggested 4 h / 2 h; load rule < 7 (B548 used < 8).

## UNMEASURED
No npm/dotnet/vitest/mutant run; no Jira read (all four tickets are the seat's to read, 331 reported only); the intersection program over the ~40 `b4*`/`b5*` branches (only the open-PR list and live panes were read); that the new rows kill O-M9-narrow, W-L-slash-plus, Q11, Mfs (RELAYED/reasoned, not run); the local gh/git were not used for any write; the count of rows in `ApiFactoryHostStartRetryTests` (gate says 21 tests in the set).

## Files written
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B558_SEAT-H8_hpsmpoc-test-followups-329-332.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B558_SEAT-H8_hpsmpoc-test-followups-329-332.md.pre-stamp`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B558_DRAFTER-REPORT.md`
No other file was written; no Jira, mail, chat, decision_queue, publish tool, fetch, worktree or HTTP to a hosted site was used.
