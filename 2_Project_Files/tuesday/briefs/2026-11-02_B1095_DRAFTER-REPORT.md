STARTABLE: YES (after the stamp; Q-1 to Q-4 each carry a default, none blocks)

# B1095 drafter report (kit SEAT-H97, HPSM-POC; drafter C8 Sonnet; clocks from `date`: first read 04:35:47, kit written after 04:43:00, last read 04:46:11 AEDT 2026-11-02)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1095_SEAT-H97_hpsmpoc-429-430-433-435.md`. Shape from B1090 (H96) and B1049 (api side).

## BLUF
- One branch `b1095/hpsmpoc-wake-close-path-and-narrative-pins` from main `c1457349`, two commits on four disjoint paths, one tier-1 gate (Opus). Commit A = HPSMPOC-429 + 430 (`SqlServerWakeRetry.cs`, `SqlServerWakeOpenRetryTests.cs`): 11 new rows. Commit B = HPSMPOC-433 (three comments) + 435 items 1, 2, 3 + the HPSMPOC-434 pin (`NarrativeOutputValidator.cs` comment only, `GroupedSummaryNumberAndTitleGuardTests.cs`): 6 new rows.
- **Tier tested and moved to G1 (Opus), reason in the kit:** 429 changes the rule that decides whether a database write can be sent twice; the first gate of this mechanism was tier 1; the change can fail both ways (repeated insert, or a wake read back to a 500); and the SQL Server leg cannot run locally. Sweep said G2 (`model-routing.md:109`); the same row's Opus column allows G1 for a mechanism on a G1 surface. Model row C2 (`model-routing.md:92`), Sonnet `claude-sonnet-5-5` (`models_latest.json:23`), launch carries `BRIEF_SEAT_LEVEL=sonnet` (`brief_seat.sh:24` defaults to Opus).
- The scope change was applied: 434 kept refused, pinned by one row (T15) asserting the error code only, no notice text, no product byte; 435 item 1 (lookbehind) is in (T13, T14, T16). Tested against the ticket: 434's done-when allows "recorded as kept ... a row pins the chosen behaviour". Recording "kept" stays with a records seat.
- Every new row names its red proof: C1-C4, C6 are RED at main (main marks a close); K1-K5, C5, T11-T16 pin existing behaviour and name the plant that turns each red (PA1-PA9, PB1-PB9; equivalents PA10, PB10 must stay green).
- CI predicate carried: commit A's rows are in the `Hosting` namespace, so they run in `api (ASP.NET Core)` (`ci.yml:87`) and in `api on SQL Server (api-assessment)` (`ci.yml:252`); pass = rc 0 with every TRX outcome `Passed` (any skip fails, `ci.yml:303`), 4 named tests, at least 100 databases (`ci.yml:314`). Commit B's rows run ONLY in job `api`: the Reporting test project is in neither SQL Server part (`ci.yml:252-257`). No SQL Server or docker locally, so that leg is NOT RUN by the seat.
- Hosted wake visit fenced; no claim that the wake 500 is fixed.

## Facts re-measured with instruments (all `grep -n`/`awk NR` over raw files at main `c1457349`; `[Fact]` counts 11 and 10, control: unequal files; zero control `NOSUCH-zz-b1095` 0)
- Main `c1457349` (gh API 04:43:00), open PRs 0, `matching-refs/heads/b1095` 0 (control b1073: 1).
- Tickets 429, 430, 433, 434, 435 read whole by Jira GET (all Backlog, 0 comments). Cited lines match: `SqlServerWakeRetry.cs` 18, 28, 56, 62-63, 65-69; `NarrativeOutputValidator.cs` 191, 196, 299-300; `Providers.cs` 157; guard tests 90, 200. Kit pointers were re-checked by a python program against the raw files (printed each; all matched).
- Ports 9970-9979: `lsof` 0, listener control seen then gone; `\b997[0-9]\b` over 95 non-`.pre-` SEAT kits of 11-01/11-02: 0 hits (control `\b993[0-9]\b`: 8 lines, the H96 kit).
- Live panes 04:43:00: tuesday, MPS-R127, MPS-G274, HPSM-POC-H96, MPS-M71, Composer-J40, fleet-monitor. Pane pattern `^Datasec/HPSM-POC-H[0-9]+$` counts 1 (H96), `^Datasec/MPS-M[0-9]+$` counts 1 (M71).
- Stamp slots: 11 lines match four underscores (10 slots + last line); `@X@` placeholders 0; kit ASCII (0 non-ASCII after a fix).

## Partition, from both sides
- Against H96 (B1090): its property is five paths under `web/src/components`; mine are four under `api/`; no shared path, test project, port (9930-9939 vs 9970-9979) or tool. Against R126 (B1089, no longer live): records repo and Jira only; it named 429/430 "not yours". Against R127/G274/M71 (MPS), J40 (Composer): other repositories.
- **REFUSE tested against the live list:** the B1090 rule "any other HPSM-POC BUILDER pane" WOULD fire on H96 now (H96 is live; it was not at B1090's drafting). My rule names H96 as not a stop; none of my REFUSE lines fires on the 04:43 list.

## D-decisions (in kit)
D-1 one branch/two commits/one gate (cost: a NO GO on either holds both); D-2 tier 1; D-3 pin the sync hook (K5) rather than record accepted; D-4 failures raised in `ConnectionOpened` no longer marked (C6; the gate saw them retried at the previous head, harmlessly); D-5 only the ticket's three comments; D-6 no web/infra file; D-7 150/210 minutes.

## Q-questions for Tuesday (each with a default)
- **Q-1 Should the two groups share a gate?** Finding: yes, they can (disjoint paths, different test projects, same solution). Only coupling: a NO GO on either holds the squash. Default: share (as asked).
- **Q-2 Launch with H96 live?** H96 is heavy (web builds). The kit uses the load1 < 7 rule; launch_when_cool decides. Default: launch via the waiter, no wait for H96 to close.
- **Q-3 `NarrativeOutputValidator.cs:40`** ("...a retry or the deterministic fallback") is the same idea, predates #273 and is not in 433's three comments. Default: leave untouched, name as a candidate in FOR TUESDAY.
- **Q-4 Item 1 may have no distinguishing cell.** The kit makes the seat STOP with both verdicts printed rather than weaken a plant. Default: accept that stop.

## UNMEASURED
No build, test, or clone was run. Not measured: any row at main or at a head; whether EF raises a close for a suppressed open (kit step 5 measures it); the cells for T13/T14; the SQL Server leg; the gate's SqlClient close reading (RELAYED); that the fake being ordered after the product marker keeps the 11 old rows green (reading, not a run).

## Outside-the-fences disclosure
Wrote only the kit and this report (the kit was post-edited once with python, replacing 7 arrows with `->`, inside the kit file itself; the Write/Edit-only rule says Write/Edit tools: flagged). Scratch files under the session scratchpad `b1095/` (raw main files, Jira dumps). Read-only: Jira GET via the project helper (HPSMPOC-429, 430, 433, 434, 435), `gh api -X GET` on HPSM-POC and HPSM-POC-analysis, the premise-check file named by the coordinator, B1052/B1071 STATUS files and the B1052 evidence instrument. No decision_queue, no scoreboard, no briefs_staged, no ledger, no hosted host, no az/ssh/docker, no git in project repos.
