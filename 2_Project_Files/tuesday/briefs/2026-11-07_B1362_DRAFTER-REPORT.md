STARTABLE: YES, after Tuesday fills the slots. Re-read main, the file's blob, open PRs and the pane list at the stamp (a moved file refuses the seat).

# Drafter report: B1362 SEAT-H134, HPSMPOC-446 vacuous SQLite assertion (drafted 06:08 to 06:15 AEDT 2026-11-07)

## BLUF
1. Kit `2026-11-07_B1362_SEAT-H134_hpsmpoc-446-vacuous-assert.md` (81 lines, ASCII 0 non-ASCII lines, 12 four-underscore runs: eleven slots and the last line), its `.pre-stamp` (cmp rc 0), `2026-11-07_B1362_slots.json` (12 keys, every S-key matches a slot line in the kit; not run through the stamp tool, which I did not find at `tuesday/stamp_brief.py`). Sonnet, C2 (`model-routing.md:92`), `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes. Tier 3, one test file, new branch from main `eaf77b3c`.
2. **My measurement favours removal, but the kit leaves the choice to the seat's printed event search.** `KillsTheLockHolder` (`ApiFactoryHostStartRetryTests.cs:512`) is SQL Server only (`TestDatabase.SqlServer!`, `sys.dm_tran_locks`, `KILL`); the row's own summary says SQLite has no session to end (`:615`-`:616`). A counter on the SQLite hosts that only a plant can raise would be the same vacuous assertion, so the kit makes Form A (preferred) conditional on a real SQLite start-path event, else Form B (delete `:640`, drop "nothing killed and" from `:617`, keep `:641`). I did not read the SQLite migrations-lock code, so "no such event exists" is DERIVED from the summary, not measured.
3. Gate row after the READY: G2 (`model-routing.md:109`), Sonnet first, one-file diff; cap row `:111`.

## Facts re-measured (instrument; control)
- Ticket read whole by `python3 -I -B .tools/b1343/jira_get.py HPSMPOC-446` at 06:11:48 (9 lines, Backlog). It names lines 624, 626, 627, 634, 635, 640; my `grep -n -w kills` over the raw file at `eaf77b3c` printed exactly those six.
- Main `eaf77b3c0623d4b5904abfa6770e81e88380c9ae`; open PRs 0; `matching-refs/heads/b1362` 0 (control: `heads/b1326` 1 row). File 713 lines, blob `5364c3b583dc07d0060fd1412581ca382944d70b` (contents API `.sha`; control: `git hash-object` of my copy printed the same).
- Pointers by `awk NR==n`: `:512`, `:582`, `:618`-`:620`, `:624`, `:626`-`:628`, `:630`-`:631`, `:634`-`:635`, `:637`, `:640`, `:641`, `:614`-`:617` (summary).
- CI at main: `ci.yml` 682 lines; job `api` `:86`-`:87`; Hosting runs on SQL Server in shard `api-assessment` (`:250`-`:252`); named-tests step `:274`; floor `:314` = 100 for `api-assessment`.
- Landing rule read at source: analysis main `CLARIFICATIONS.md:3617` (5742 lines, `awk NR==3617`), project `CLARIFICATIONS.md:138`: head-pinned squash. (The project root's local `CLARIFICATIONS.md` is 192 lines, a stale working copy; the kit cites it only as the older precedent.)
- Ports 9570-9579: `lsof -nP -iTCP:9570-9579 -sTCP:LISTEN` 0 (control: 11 listeners overall). Word-boundary scan `957[0-9]` over non-`.pre-` SEAT kits of 6-7 Nov: 0 files (control `956[0-9]`: 1). Hits to report: none.
- Panes (`tmux list-panes -a`, 06:0x): 7; `Datasec/NexusAI-N110` (another repository); HPSM count 0 (control: the list does print N110). `df -k` 113962564 free. load1 3.56 at 06:13.
- Model: `model-routing.md:92` (C2), `:109` (G2), `:111` (cap); `models_latest.json:23` `"model_id": "claude-sonnet-5-5"`.

## D-decisions
- D-1 Branch is new `b1362/hpsmpoc-446-vacuous-assert` from main (no existing branch for this row).
- D-2 Form A/B chosen by the seat by measurement, decision rule written as a property (a counter raisable only by the plant fails it).
- D-3 Time: READY +60, HARD STOP +90 (small lane; one test row, dotnet build and a Hosting-namespace run).
- D-4 No SQLite-plant with `kills` passed to the hosts is expected to be a valid proof (DERIVED: null SQL Server string); the kit has the seat print it rather than assume.
- D-5 Slots carry only my reads and `PENDING`; no attestation of a Tuesday read.

## Q-questions for Tuesday (each with a default)
- **Q-1** Row C2 is the nearest not an exact fit (one file, test only; L6 is local-model only and Studio-only). Default: C2 Sonnet.
- **Q-2** Form B's third done-when ("accepted or declined") is yours, not the seat's. Default: seat delivers A or B; you mark the ticket on the gate's verdict.
- **Q-3** HPSMPOC-447 option (a) edits the same test file: serial after this. Default: launch 447 only after 446's gate.
- **Q-4** Ticket close needs the SQL Server leg on hosted CI (seat has no docker grant). Default: landing condition as written.
- **Q-5** Port block 9570-9579 reserved, none typed. Default: keep.

## UNMEASURED
- Whether a real SQLite start-path event exists (decides Form A); the SQLite code was not read.
- The kit's Plant two (`a.Retries.Add("planted")` after `:628`, expected `:641` red, `:640` green) is DERIVED, not run.
- Whether a warning count at main differs after the edit; whether the SQLite Hosting namespace passes as a whole today; the dotnet build and test baseline (RELAYED only from the earlier gate: 2161/0/13 at another head).
- `.tools/b1343/hv.sh`, `lock.sh`, `jira_get.py` were read by header only (hv.sh lines 1-14) or listed, not run. `stamp_brief.py` not located. HPSMPOC-447 not read.
- Whether any seat holds an unpushed local branch on this file (only pushed refs, kits and panes were read).

## Outside the fences
Read-only everywhere except my four files. One Jira GET (HPSMPOC-446) through the project's reader; `gh api -X GET` under the project's `GH_CONFIG_DIR` (main, open PRs, refs, contents of the test file, `ci.yml`, the analysis repo's `CLARIFICATIONS.md`, commit list for the file) into the scratchpad. One `find /Volumes/Laptop-DEV -name jira_read.py` ran long and was stopped (TaskStop) before finishing; no output used. `git hash-object` ran read-only inside `.tools/b1343/repo`. No card store, no ledger, no mail, no hosted host, no project file edited. The sweep file was read whole; the B1339 kit and slots were read whole as the template.
