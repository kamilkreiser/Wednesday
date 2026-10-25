# B559 drafter report (SEAT-G71, HPSM-POC gate of PR #204, tier 2, Sonnet, round 1 of 2)

Drafted 2026-10-24 about 06:34-06:45 AEDT, read-only. Brief: `2026-10-24_B559_SEAT-G71_hpsmpoc-204-gate-tier2.md` (84 lines), copy `...md.pre-stamp` (cmp equal). Model line `claude-sonnet-5-5`, routing row G2 (tier-2 gate).

## Facts measured (by `date`, read-only; all in the brief's Fact marks)
- MEASURED (`gh api GET pulls/204`): open, merged false, mergeable true, mergeable_state blocked, 3 files, +136 -0, 4 commits, head 97dc11a4a077fd620e5752e69dbb53d109df2400, base main 31dabc8d3012d28b0dbf510ea90760a42e319730. `ls-remote`: main = 31dabc8d; b558 branch = refs/pull/204/head = 97dc11a4. `compare`: ahead 4 behind 0. Open PRs = [204].
- MEASURED (`pulls/204/files`): ApiFactoryHostStartRetryTests.cs +93, client.describeFailure.test.ts +4, attribution-preview.test.ts +39. 4 commit first lines recorded in the brief.
- MEASURED (check-runs at 06:34): 13 listed, 2 completed success (gitleaks, dependency review), CodeQL and `api on SQL Server (api-assessment)` queued, 9 in_progress. Main head lists 19. Open alerts on the PR ref 0, analyses 1. Required contexts read (5).
- MEASURED (`ci.yml` at the head, by GET): shards are `api-assessment` and `api-other-and-feedback`; the filter `!~HpsmPoc.Api.Tests.Assessment.` (:251-253) puts `Hosting.ApiFactoryHostStartRetryTests` in `api-other-and-feedback`; a proof step fails the leg on a skipped test; green runtime of that shard at most about 18.3 min (comment :166). This is the shard that gives the 12 new Api cases their first SQL Server run.
- MEASURED: no `.tools/b559`, no `.tools/wt-b559-*`, no `refs/heads/b559*`; `.tools/b558` and `wt-b558-*` exist (builder kit, declared read-forbidden and never-run in the brief); panes tuesday / MPS-M2R / fleet-monitor only; ports 8950-8959 and 8960-8969 empty (rc 1); load1 1.45; Sonnet model id claude-sonnet-5-5.
- MEASURED (brief self-checks): slot count 9 lines with the split pattern; at-sign check 0; non-ASCII 0; no person name.

## Builder discrepancy found while drafting (put into Check 1)
STATUS :139 prints per-file added lines +35 (attribution-preview) and +83 (Api class) "over the whole range"; its own stat line (:136) and `pulls/204/files` give +39 and +93 (sum 136). The brief tells the gate to reconcile; it is a Note unless a removed line or lost name hides behind it.

## Judgement calls for Tuesday at the stamp
1. Hard stop: I suggested target verdict 2 h, hard stop 3 h (as B554). The mutant matrix is bigger (91 web mutants + Api builds) and CI's SQL Server shard may queue; the gate is told to cut to named survivors + one per side + own mutants if time forces it (it must say what was cut). Raise the hard stop if you want the full 84-mutant families.
2. Check 6 waits up to 40 min polling every 60 s for both SQL Server shards; verdict at most GO WITH FINDINGS if still pending. Your call whether to launch now (shards queued/in progress) or later when CI is done.
3. Tier: kept tier 2 (Sonnet) per your commission and the routing row, but the delta has one `api/tests/**` file. The escalation list hands to tier 1 on any `api/src`, `Support/**` or helper byte. A failing SQL Server shard is made a Blocker for the leg.
4. Q-1 slot: scratch copies (mutants, cw-weak, the shrunk-set control) in `-mutb`/`-mutw` only. No screen-level scratch render was needed (tests-only PR), so no `-scr` tree.
5. Gate runs `dotnet test` (class filter on SQLite + scratch helper mutants) and `dotnet build`; the B554 "no dotnet test" line was replaced accordingly. Whole Api project not required (builder's 1958/1945/13 read as a claim).
6. Ports: 8950-8959 (free, outside the forbidden ranges). Pane name `Datasec/HPSM-POC-G71`; re-check the name at the stamp.
7. Builder decisions flagged for the gate to judge, not fixed: 4 commits (the fourth removes a ticket key from two assertions, so those rows no longer pin the retry-line prefix); the 4th Item-3 cell `firstname` (allowed only if Mfe survived the first three).

## UNMEASURED
Anything inside the head's test code (no file at the head was read, only the diff stats and ci.yml); whether the 12 Api cases Pass on SQL Server; whether the builder's mutant/row counts hold; the CI outcomes (all pending at 06:34); whether CI sets the Azurite variable (the 13 local skips); load at launch; the per-row names in the SQL Server shard log (the gate may find the log carries counts only, and the brief says to report that as UNMEASURED per row).

## Files written (only these three)
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B559_SEAT-G71_hpsmpoc-204-gate-tier2.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B559_SEAT-G71_hpsmpoc-204-gate-tier2.md.pre-stamp`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B559_DRAFTER-REPORT.md`
(Scratch: `ci.yml` copy in the session scratchpad only.)

Forbidden items not used: no decision_queue, Jira, Artifact/Docs, mail, chat, publish; no cd; no HPSM-POC git writes (only `ls-remote`); gh GET only; no 4_Credentials read; no HTTP to a hosted site.
