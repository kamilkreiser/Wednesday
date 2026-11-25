STARTABLE: YES (after Tuesday's stamp; the unstamped kit holds 11 slot lines of four underscores, `stamp_check.py` exits 0 with 158 claims and 158 measured)

# B2108 DRAFTER REPORT (Sonnet) - MPS records kit R329: PR 229 (MPSCALC-233, 316, 120; 195 not built)
Clock: first read Thu 26 Nov 2026 06:59:25 AEDT, last build 07:21:15 AEDT. Written: `2026-11-26_B2108_SEAT-R329_mps-records-229.md` (120419 bytes, 360 lines, ASCII), its `.measured` sidecar and this report, under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/`; scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s328/d2108/` (texts.py, records.py, pointers.py, revmap.py, sources.py, build_kit.py, kit_template.md, fill_sidecar.py, jira_get.py, jsearch.py, rows.py, raw files in src/, the two job logs, the squash message, two earlier sidecar fills `measured_first_fill.txt` and `measured_second_fill.txt` moved there when the kit was rebuilt).

## BLUF
- The seat id R329 is free (0 file names and 0 non-`.pre-` SEAT kits of 11-25 and 11-26 name it; control: R328 reads 3 file names and 1 kit). Panes at drafting: `%0 tuesday` and two unnamed; 0 lines hold `Datasec/MPS`.
- **The root records are NOT at C-191/C-192-open as the B1909 kit left them: B1909 ran and landed.** Root main is `17add5bd93570f52a62763c294ca89d27cb93ae8`, C-192 exists (MPS #227/#228), so this entry is **C-193**; BACKLOG 6344, JIRA.md 931, history 1609, CLARIFICATIONS 3659 lines; status exactly the three ` M ` files. Jira before: 433 issues, 267 Done, 166 not Done (B1909 moved 428 and 429).
- Kit shape = B1909's (STATUS-file channel, marks, REFUSE AT ONCE, THE WORK 0 to 7, STANDING LINES, HOLDS incl. HOLD R, Stamp slots, last line `READ-WHOLE-BY-TUESDAY: ____`), with these changes: four keys (233, 316, 120 and, only on slot ASK-195, 195), comment order 233, 316, 120, 195; at most 5 writes; the MOVE slot accepts only `120` or NONE; no create; the B1909 STATUS deviations folded in (sidecar read, land helper selftest, texts printed whole, sources comparison false DIFFERS, status_watch, statusline).
- Every sentence of the four comments and the four record texts passed the project's scanner copy (`.tools/b1909/scan.py`, sha256 d21a053d...2514 = the file the seat copies; 14 controls fire): 8 comment forms, 2 outcome sentences (their sha256 equal B1909's frozen ones), 4 record texts (69 record lines), 0 hits; the drafter's own extra refusals (double quote, URL, newline, placeholder, card id, branch) 0 hits. That extra list is the drafter's, not the project's.

## Facts re-measured (instrument, control)
- PR 229 (`gh api -X GET`, project GH_CONFIG_DIR, account kamilDatasec): closed, merged, merged_at 2026-11-25T19:40:30Z = 2026-11-26T06:40:30+11:00 (zoneinfo); squash 15bca4ec3526cf609f50915221664c0231b5cc12, ONE parent 56f508a7, tree d63fa0c4 = the tree of head b740f548 (2 commits); 8 paths +162 -15 (sums by program equal the API); the API title equals `pr-title.txt` (cmp); main = 15bca4ec at 07:02; open PRs 0. Squash author address is GitHub's noreply form (informational).
- CI of the squash: 8 of 8 check runs completed success; `ci` 45687526321 and `Push on main` 45687525635 success; 4 analyses for the commit (csharp 63 rules, javascript-typescript 103, python 50, actions 23; results 0 each); open alerts 0. Web job 139463959743 (1552 lines): 149 files, 1742 tests, stub 260 passed 17 skipped, API-off 162 passed, 0 vulnerabilities, markers 0/57. Dotnet job 139463959656: 0 warnings, 0 errors, Engine 743, Import 198, Api 3681. (At 56f508a7 the API now lists 12 check runs where B1909 read 8: not used, not explained.)
- Blobs of the five hand paths and the stub equal the `git/trees` entries (cd6c5eab, c41077c0, 69d61e12, fb257452, bfb9506f, a3b29fda); 25 pointers (P01 to P26 without P20) each read once with a 0-line control; the 21 review rows RV and 13 rows RF each read once at their line with a 0-line control (kit THE REVIEW MAP).
- Contract file history (`gh api --paginate commits?path=` then the raw file at each of 37 shas, JSON parse): nine distinct `info.version` values equal to the nine docs/API.md:9 lists; the newest 19 commits all 0.9.0-b103 (the review counted 17 at 56f508a7; this landing adds one, so 18 after the first). `compare debb5e28...main`: ahead 7, behind 0, 20 files (the 12 of B1909's count plus these 8, no overlap, `comm` over the two file lists).
- Cells: V0Duplicate.cs at base 8 facts, 1 theory, 4 data rows; at main 15, 2, 6; column 1: 0 in both (rows 12 to 21 = nine per host).
- Jira (GET, in-process credentials, never printed; helper readers in scratch): all four keys Backlog; comments 233: 5, 316: 5, 120: 1, 195: 7; summary and paragraph hashes in the kit's THE ROWS; the reader reproduced the frozen figures of MPSCALC-426 and MPSCALC-433 (control ran). Marker searches REC-LAND-233/316/120-26NOV and REC-NOTE-195-26NOV: 0 (controls REC-REG-233-11NOV, REC-REG-120-11NOV, REC-LAND-195-16NOV, REC-LAND-427-22NOV each find their one key; zzqxnonexist 0). Duplicate searches (to the end): holdCopy -> MPSCALC-404 only (Done, another defect); AddIfRefFree 0; Contract version -> MPSCALC-120 only; characters each -> 316 only; the rest in the kit's THE ROWS. Records files: holdCopy 0 and AddIfRefFree 0 in all four; existing rows [B1703-OWED-4], [B1703-OWED-3], [B1758-OWED-10], [B1019-HELD-6] each 1.
- Card store: `decision_queue.sh show` of the one exact id given in the commission, into a scratch file: status open, ruling None. Used only for slot ASK-195; no card id is in the kit (0 hits for `datasec-mps`).

## D-decisions (drafter's, for Tuesday to overturn)
- D1 No ticket created; the kit has no create. The project's practice (C-191, C-192) is BACKLOG rows unless a CREATE slot names a ticket; F1 (the 100-unit -COPY shape) rides the open MPSCALC-233.
- D2 Owed lines, one destination each (kit PART 4 item list): stub clone -> row OWED-1; places the refusal does not reach -> row OWED-2; F1 -> the 233 comment (ticket stays open); the two contract-text gaps (F2 coverage of the version rule, F6 the :1036 clause) -> row OWED-3; scan cost and the helper -> row OWED-4; hosted deploy card -> row OWED-5; 195 -> its comment (row [B1703-OWED-3] stands); SOURCE.txt naming f8644cce and the moved sibling-sentence lines -> Corrections lines (rows [B1703-OWED-4], [B1758-OWED-10] stand); loose commit-1 text (F8) and the builder's process slips -> no line (moot; in its STATUS and the review). A comment states a finding as a clause reading where it must (233, 120); the owed WORK sits in one place.
- D3 MPSCALC-233 is not movable by this kit's slot (clause 1 NOT MET for one shape; C-79).
- D4 Entry number C-193; marker date 26NOV (STOP on another day); 195's marker is `REC-NOTE-195-26NOV` (not a landing).
- D5 The texts say 18 contract changes after the first 0.9.0-b103 commit (measured), not the review's 17.
- D6 CHECKS sentence includes the dotnet job (the change is C#), unlike B1909's.

## Questions for Tuesday (each with a default)
- Q-1 Model: **Sonnet** (`model-routing.md` line 97 row C7 and line 110 row G3; the drafter ran on C8 line 98; model id claude-sonnet-5-5 at `models_latest.json` line 23); `BRIEF_SEAT_LEVEL=sonnet` inside the quotes (brief_seat.sh line 31 defaults to opus). Default: Sonnet.
- Q-2 Does MPSCALC-233 move? **Default: stays open** (C-79: clause 1 NOT MET for a source of exactly 100 units ending -COPY, pre-existing; a rule is a product choice). Moving it is a different kit.
- Q-3 MPSCALC-316: comment, stays open for the product owner's reading of C-108; label needs-ruling not edited. Default: as drafted.
- Q-4 MPSCALC-120: **default MOVE=120** (fix shape met by the section at docs/API.md:8; F2 is Minor, stated in the comment, owed in a row). Alternative NONE if you read F2 as a review line standing against the move.
- Q-5 MPSCALC-195: comment only if you stamp ASK-195=OPEN after re-reading the card (open and unruled at 07:0x). Default of the kit if left: NONE; drafter recommends OPEN.
- Q-6 Tickets for the owed lines: **default none** (kit D1). Say so if you want one Low ticket for the stub clone (OWED-1) or for create/PATCH (OWED-2): that would need a CREATE slot and a new kit section.
- Q-7 Discrepancies you may want to know: (a) the commission and the gate's FOR-RECORDS attribute "not ruled" to comment 41400; the verbatim "not ruled" is in comments 40096/40472, and 41400 says the question remains (the 316 text cites 40472 and 41400 accordingly); (b) the verdict's summary says five Info findings, its list holds six (F3 to F8); the texts carry no count; (c) the review's 17 versus the measured 18; (d) the commission named the entry as the next C-number after C-191-era state, but C-192 exists.

## UNMEASURED
Hosted state of the site (relayed C-188 only; HOSTED slot is Tuesday's); the helpers' selftests and the dry run (the seat's, not run: no seat output exists; the texts' scan and the sha256/extract checks WERE run on the drafter's program, and the seat's scanner is byte-identical); that the kit's 233 comment's claims about the review's probes hold beyond the verdict's words (RELAYED from VERDICT.md, rows RV); the web job log order of the two Playwright groups (the first group's 260/17 skipped and the second's 162, matched by order in the log, same as B1909's reading).

## Chain inputs (every input exists at BASE or is made by an EARLIER step)
| Step | Inputs | Made by |
|---|---|---|
| 0 | the kit and sidecar, root files, tmux, df | BASE (Tuesday's stamp) |
| 1 | `.tools/b1909/*.py` as a shape reference, scan.py copy | BASE |
| 2 | sources, GitHub, Jira, the Step-0 copies | BASE and Step 0 |
| 3 | texts of the kit, Step 2 facts, `.tools/b2108/scan.py` | kit, Steps 1 and 2 |
| 4 | frozen texts, Step 3 payloads, `snap_before.json` | Steps 2 and 3 |
| 5 | comment ids and the move result, the Step-0 before-copies | Steps 0 and 4 |
| 6 | the records branch, `refs-before.txt`, the lock | Steps 0 and 5 |
| 7 | every log | Steps 0 to 6 |

## Outside the fences (disclosure)
- Two Bash calls hung and were stopped with TaskStop: one ran `/usr/bin/grep -rl` over the whole `tuesday/briefs/` tree for the seat id (recursive read of other kits and verify folders, nothing printed but file names, no write), one a `tmux list-panes`; redone with `ls` names and a bounded grep over today's and yesterday's SEAT kits, and `timeout 20 tmux`.
- Read with `cat` and loaded by path (python `-I -B`, no bytecode) files in other seats' trees, read-only: `.tools/b2106-m176/scratch/jira_get.py` (copied into my scratch as my read helper) and `.tools/b1909/scan.py` (the scanner), `.tools/b1909/*.py` sizes only.
- Git in the project root: besides the listed read verbs I ran `status --short --untracked-files=no`, `branch --list`, `config user.email`, `remote -v`, `diff --cached --name-only` (all read-only, `--no-optional-locks`), as the B1909 kit itself lists them as reads. No fetch, checkout or ref write.
- `decision_queue.sh show <exact id>` once, into a scratch file; the filtering was by several patterns, not by an inclusion filter on the id alone.
- `lsof -nP -iTCP -sTCP:LISTEN` and `tmux list-panes -a` (reads). No az, ssh, docker, hosted request, Jira write, mail or message. Nothing deleted: two superseded sidecar fills were moved (`mv`) into scratch.
- Not read: `fleet/briefs_staged/`, `projects_index/scoreboard.md`, `0_Brain/learnings/_ledger.md`, any WEDNESDAY or FRIDAY tree, any other project.
