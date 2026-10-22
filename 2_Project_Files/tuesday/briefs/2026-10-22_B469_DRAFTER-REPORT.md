# B469 drafter report (read-only, 2026-10-22 16:55-17:15 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B469_SEAT-G39_hpsmpoc-b462-308-gate-tier1.md` (47 lines, unstamped: 5 four-underscore slots, control 1; `@[A-Z_]+@` count 0, control 1; no READ-WHOLE line; no person's name). Pane `Datasec/HPSM-POC-G39`, ports 8220-8229 (0 listeners; unfiltered lsof listed 12), `.tools/b469` absent, no `b469*` ref. `BRIEF_SEAT_LEVEL=opus` is valid (`brief_seat.sh:25`, default opus). Row G1 quoted in the kit from `model-routing.md:108`; the kit says honestly that G2 (:109) lists config/CI as tier 2 and the tier-1 ruling comes from the B462 brief item 8.

## Workflow-PR rule
None found in the project `CLAUDE.md` (`/usr/bin/grep -c -i -E 'workflow|\.github|ci\.yml|codeowners|merge|pull request|branch protection|github actions'` = 0; control `External communication` = 1). No `CODEOWNERS` (ls-tree of main lists only `.github/workflows/ci.yml` and `.github/workflows/security/gitleaks.ignore`). Rules that do apply, quoted in the kit as check 10: B462 brief item 8, "**Workflow edits are tier 1.** Any byte in `.github/workflows/ci.yml` makes this tier 1 (a CI gate)"; `1_Project_Definition/CLARIFICATIONS.md:55` "branch protection on `main` (3 checks, admins enforced, 0 approvals, no force-push/delete)" (now 5 required contexts by `gh api`; the SQL Server shard is not one of them); the 2026-10-16 merge-once-tested grant.

## Measured by the drafter (all read-only)
- ls-remote 17:02:45: main `a93b926a`, b462 `e8ecb8ae` (= READY), b460 `b9fd28ed`, b461 `52bd6e7c`, b429 `473bfaca`, b459 `26460869`; no b465-b469 ref. 1 commit, 6 paths, api/src, web, infra diffs 0 bytes. Trailer is `Claude Opus 5.5` (the builder is Opus, so gate and builder share a model; the kit says so).
- `ci.yml` diff read whole: 4 hunks, all in `api-sqlserver-shard` (timeout 20 -> 30; env `HPSM_TEST_HOST_RETRIES`; new `if: always()` count step that warns but never fails; the new test name in the `api-other-and-feedback` named set). `permissions:` at :20 not in the diff; one `-` line only.
- The real fault text in CI job 118913548649 contains the quotes `'__EFMigrationsLock'`, so the retry's substring matches (control: 23 `SqlException` hits). The log does NOT print the error number; no repo file pins 1223. `Number == 1223` is therefore unproven at runtime, and a wrong number would make the retry a silent no-op with the counter at 0. The kit carries this as a check-3 item.
- Jira: HPSMPOC-308 Backlog, one comment; 0 issues created since 2026-10-22 (control `key = HPSMPOC-308` = 1), so none of the builder's four Deferred items is filed.
- Overlap by `gh api compare`: b429 (40 files), b459 (2), b460 (`Hpsmpoc290Tests.cs`), b461 (14 web paths): 0 shared with the 6. b465 compare is 404; B466 will add a Feedback test file in the same project (drafter report B465-467 lines 109-112: project shared, no file).
- Arithmetic of the two red timing values checked: 1384 - 900 = 484 and 1543 - 704 = 839.

## Things the kit adds beyond the prompt
- Check 4 (iii): added-time mutants (X = 400..2000 ms inserted after each measured wait) to show that the detection floor for product-added time in a stage moved from about 350 to about 1200 ms; this is the honest cost of Slack 1200 and the builder's comment does not state it. Misattribution (>= 1300 ms off) is the part the builder's claim covers.
- The `(slow)` suffix: the staged request now crosses the product's 5 s Slow mark and logs at Warning; the kit asks whether any log-level filter depends on it, and what +5 s costs in the REQUIRED SQLite `api` job.
- Check 3 F6 runs the CI counter step's `run:` body verbatim (absent file, empty file, 2 lines, and a final line without a newline where `wc -l` and `[ -s ]` disagree); the step never fails the job by design.
- Check 7: the `named` test name must equal the method's real full name, else the proof step reddens every PR.
- Check 9: an overlay worktree `-ov` (head plus ONLY B460's `Hpsmpoc290Tests.cs`) to run the `WithWebHostBuilder` interaction.
- R8 (`_started` guard off) and R9 (`Logs.Entries.Clear()` off) are probes whose outcome the drafter does not know.

## UNMEASURED
- Nothing was built or run (no dotnet on this shell, load1 7.9-9.8): every red/green prediction in the kit (R1-R9, S1-S2, X ladder, F1-F6, `-ov`) is unmeasured.
- Whether `Number == 1223` is the code SQL Server raises for the lock release (the CI log shows only the message), and what the first command on SQL Server is when the forged fault attaches.
- The builder's 60-run spread, 14-job classification, 49-job duration table and the 0.6 min/day trend are RELAYED; the drafter fetched only one job log (118913548649).
- Whether any `Feedback` test other than `Hpsmpoc290Tests` reaches a host by a path that bypasses `StartServer` (counts only: 2 `CreateClient(` lines, one the factory's own; 2 `WithWebHostBuilder` lines, both in B460's file).
- Whether b465/b466/b467 branches will exist by the gate's start (absent at 17:02), so the kit falls back to their briefs' Yours lists.
