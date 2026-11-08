STARTABLE: YES

# Drafter report B1367 (seat Datasec/HPSM-POC-R192, Sonnet records seat), drafted Sun 8 Nov 2026 20:37 to 20:45 AEDT

## BLUF
The kit is startable. It records the product owner's option (a) ruling on HPSMPOC-319's B469-5 (met under the ruling, three limits, ticket NOT moved, still waits on three main pushes; drafter's count 2 of 3), and moves HPSMPOC-446 to Done under the project's own Done rule C-263 ("Done means merged to main ... nothing deploys") if all three clauses of its done-when read met (the drafter read all three met). Two Jira comments, at most one transition, no ticket created, two C-entries (expected C-309 and C-310), one BACKLOG section (B1367-1, B1367-2, B1367-C1), one history entry. Kit 136 lines (`wc -l`), 12 four-underscore lines (11 slots plus the last line), 0 non-ASCII, 0 tabs, 0 `@...@` tokens, 0 angle placeholders.

## Facts re-measured (instrument; a control where a count is a zero)
- Clock: `date` 20:37:11 start, 20:44:52 last. Panes (`tmux list-panes -a`, empty names filtered) at 20:37:27: %0 tuesday, %177 Datasec/NexusAI-G366, %1 fleet-monitor. No HPSM-POC pane.
- Model: `model-routing.md` NR=98 is row C8 (table rows C1..C10 at NR 91..100, listed by grep -n); `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`; `tools/launch_when_cool.sh` exists (ls).
- Code repo (`gh api -X GET`, project `.gh-config`): main `b14b6f29fe34568472e1c6e87178b0244ec32415`, committed 2026-11-06T21:25:59Z, 1 parent, verified true. PR #294 merged_at 2026-11-06T21:26:00Z (= 2026-11-07 08:26:00 AEDT, derived), squash, parent `eaf77b3c`, head `56489340`, 1 commit, 1 file, +1 -2, merged by a User. Check-runs on the squash: 21 success, 1 skipped. Code-scanning open 0 (control: fixed 1). Open code PRs 0 (control `pulls/99999` 404).
- CI census for 319's last clause: `ci` push runs on main created >= 2026-11-06T08:21:10Z: exactly 2 (42187059450 at eaf77b3c, 42296681684 at b14b6f29), each with both `api on SQL Server` shard jobs and the roll-up completed/success. Control: same query from 2026-11-01 returned 25; job list for run 1 answered 404. So 2 of 3 at 20:38.
- Code files: `tests` file 713 lines at eaf77b3c with `Assert.Empty(kills.Killed)` once (:640), 712 lines at b14b6f29 with 0; `diff` prints exactly `617c617` and `640d639`; `grep -n -w kills` at b14b6f29 prints 624, 626, 627, 634, 635; `Assert.Empty(retries)` :641 then :640. Api `HostStartRetry.cs` 64 lines, filter :33; Feedback twin 63 lines, filter :32, `LockNotHeld = 1223` :24; `diff` of the two prints 3 differing lines (header comment, two namespace lines).
- Squash message of #294 (9 lines): `anywhere` 0 lines (control `-i killed` 2 lines). This closes B1364-1 (the gate's fix shape was "none on the branch, the squash replaces the message").
- B1364 STATUS (142 lines, sha256 prefix 9808c36a36a9cedb): :1 verdict, :84 words, :119 B1364-1 Minor, :120 to :125 Notes -2..-7, :126 no Blocker/Major, :131 FOR TUESDAY (awk/grep -n). B1362 STATUS 120 lines; its first line reads `PROGRESS B1362 ... HOLD` (stale; the kit says do not copy it). B1326 :118/:119, B1343 :101 to :104 printed.
- Jira (read helpers, GET): HPSMPOC-319 Backlog, resolution none, 4 comments (39971, 40121, 40150, 40807); 40807 reads B469-5 OPEN and "1 of 3" on the last clause. HPSMPOC-446 Backlog, 0 comments, label b1349-2026-11-06, Done transition id 41; done-when printed. Max key 447 (`key >= HPSMPOC-444` lists 444 to 447); `text ~ "B1364"` 0, `"B1367"` 0, control `zzqq-no-such-string-9d41` 0.
- Records (raw by gh api): main `84eb4106...` (PR #184 merged 2026-11-06T09:10:30Z); CLARIFICATIONS 5742 lines (966b1eb8a53c8f56), highest heading C-308 (:5734), `-i -E '^### C-(309|31[0-9])'` 0 hits; C-263 heading :5114; BACKLOG 3643 lines, newest section :3603; history 2782 lines, newest entry :3. Mentions of B1364, B1362, b14b6f29, "pull request 294", B1367: 0/0/0; control HPSMPOC-446: 1/3/0. Open records PRs 0 (control 404); `records/b1367` 0 refs, control `records/b1349` 1.
- Done rule: C-263 heading :5114 and option text :5116 quoted in S6 of the kit. Local project CLAUDE.md (51 lines): `grep -n -i Done` only line 34 (SETUP_RUNBOOK row), so no other Done rule there. Deployment is NOT a condition under C-263.
- REFUSE 7 terms against the one non-HPSM live kit (NexusAI-G366, B1365): 0, 0, 0, 0, 0; control (B1349 records kit): 5, 3, 10, 0, 12.
- df: 106 GiB free at 20:39. load1 2.93 at 20:41.

## D-decisions the kit makes
- D-1 B469-5 is "met under the product owner's ruling" and nowhere "met" without that phrase; the closing check bans a claim that a CI run/log shows the line.
- D-2 HPSMPOC-319 is never moved (NEVER set); at 3 of 3 the comment says so and the move is Tuesday's.
- D-3 No ticket for the B1364 findings: the project convention (row B1349-1 "a test-only Minor, not ticketed"; B1349-3 one accounting row for a gate's Notes) gives two rows. B1364-1 is closed by the landing text.
- D-4 HPSMPOC-446 moves only if all three clauses MET by the seat's own program; marker REC-DONE-446-08NOV-B1367.
- D-5 HPSMPOC-308 is not commented (outside the commission); its clause 3 shares the same count, flagged in the hand-off.
- D-6 Two C-entries (C-309 ruling and 319; C-310 PR #294, 446 and findings) so the STATUS last line carries both numbers.

## Q-questions for Tuesday (each with a default)
- Q-1 Sonnet on C8 for a records seat (row names no records job; precedent B1330 and B1349). Default: yes.
- Q-2 Move 446 under CLOSE-IF-MET. Default: yes (all clauses read met; C-263).
- Q-3 Hard stop 45/90/130 minutes, outer limit 23:30 AEDT 2026-11-08 (my proposal). Default: as written.
- Q-4 Should HPSMPOC-308 get a refreshed clause-3 comment (2 of 3 now)? Default: no, outside this commission.
- Q-5 The ruling's quoted fragments come only from the commissioning message; the seat cannot re-read the board. Default: kit marks them RELAYED and uses the label "Count it" only (the commission's em dash avoided to keep the records ASCII).

## UNMEASURED
Any write path (none run); the helper re-point edits; the 319 count after 20:38; whether a third main push has landed; empty-name pane count; the exact board text of the ruling; closing-check class behaviour on the long ruling quote; `scan1367.py`; post-20:41 changes anywhere.

## Outside the fences disclosure
Only the three files named were written (kit, slots, this report). Read-only: `gh api -X GET` (code and analysis repos) and the HPSM-POC `.tools/b1349` read helpers `read.py` and `search.py` (Jira GET; no token printed) plus a one-off reader in the session scratchpad (`rd.py`, GET only); raw copies of the three records files and the code files saved under the session scratchpad. No decision_queue, no briefs_staged, scoreboard, `_ledger.md`, WEDNESDAY, FRIDAY or non-Datasec tree read. No git write, fetch or checkout in any project repo; no cd typed; no az, ssh, docker, hosted HTTP. The tmux pane list was read once (names only).
