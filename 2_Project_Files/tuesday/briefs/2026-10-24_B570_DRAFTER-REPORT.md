# B570 DRAFTER REPORT (2026-10-24, ~09:40 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B570_SEAT-G75_hpsmpoc-205-gate-tier2.md` (75 long lines, shape cloned from B559: stamp slots, REFUSE block, verdict first/last lines, round 1 of 2, heavy-run and lock rules). Unchanged copy: same path + `.pre-stamp` (`cmp` equal).
**`.pre-stamp` slot count: 9 lines match the four-underscore pattern (8 slot lines at :24-:31 + the last line :75); control: the stamped-form rule is the same as B559's. Non-ASCII 0, at-sign-caps-at-sign 0, person name 0.**
Seat Datasec/HPSM-POC-G75, tier 2 (`BRIEF_SEAT_LEVEL=sonnet`), ports 9190-9199.

## Measured by me (read-only, 09:34-09:36)
- PR #205 open, head `91cb99a5`, base `08af828b`, 2 commits, 2 files (+212 -0 test, +2 -1 launcher), mergeable true / state blocked. Open PR list = [205] only. `refs/pull/205/merge` = `f24d0cf8` (the kit tells the gate to record it).
- Check-runs at 09:34:56: 14 listed, 6 completed, 8 pending (SQL Server api-assessment, api-other-and-feedback, api ASP.NET Core, infra Bicep, web unit tests, Analyze python / javascript-typescript / csharp). **`web build (audit, lint, typecheck, build, deploy package)` is already completed FAILURE (09:34:13, run 120690275703, no output text); main's own web build is success.** Cause UNMEASURED; the kit makes it a standing Blocker until the gate reads the log and shows green or a base fact. Tuesday may want to look before launch. `CodeQL` = neutral "1 configuration not found" (interim). `web e2e (${{ matrix.shard }})` skipped (unexpanded matrix name).
- Ports: `lsof 9190-9199` empty (rc 1). Word-boundary scan of the 253 files `2026-10-23_*` / `2026-10-24_*`: one file matches `919x`, `B565_DRAFTER-REPORT.md` line 21, where `9199` only ends the wide sweep `9100-9199`; no brief allots 9190-9199 (highest allotted block read 9180-9189). Control on `ports 9120-9129` = 1.
- E6: read `edge-trim.ts` at main (`strippable = unit.trim() === "" && !KEPT.has(unit)`); node v24.21.0 over all 65536 UTF-16 units: 25 trim to empty, 200d absent. So the builder's equivalence holds by reading; the kit still makes the gate prove it (spec lists) and run plants E6b (NBSP into KEPT) and E6c (strip the joiner) that must die.

## Findings about the builder's claim set (kit carries them)
- The builder's DESIGN table has no row for the 120-char cap (must-check 5): the kit makes the gate measure it with its own scratch row and report the gap as a Note.
- Builder STATUS says CodeQL/no workflow ran: now stale; CI is running (kit Check 7).

## Not done / UNMEASURED
No npm, vitest, worktree, mutant, Jira read. Kit length 75 lines (under 95), but lines are long like B559's.
