STARTABLE: YES

# B2105 DRAFTER REPORT: OXPd records pass for the landing of PR 53 (first-run row 4) and the outage re-scan (kit for seat R328)

Drafter: in-session, read-only, for Tuesday s328. The first clock `Thu 26 Nov 2026 04:14:50 AEDT` and the last `04:30:33` were both printed by `date`. The kit has no typed clock in any slot. Its MEASURED-BY-DRAFTER clocks are `date` prints or GitHub timestamps.

Files written (nothing else outside scratch):
- the kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2105_SEAT-R328_oxpd2-records-pr53.md` (sha256 `10abb641...`, 100568 bytes, 328 lines, 11 unfilled slot lines, 0 bytes above 126)
- its sidecar `.measured` (114 claims, 0 TODO; `stamp_check.py <kit>` rc 0)
- this report
- scratch only, under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s328/d2105/`

## BLUF
- **What the kit writes** (the form is B2097, plus B2066's tick in place):
  - **C-88**, a Tuesday's note (the C-64 and C-87 precedent). It names C-87's sentence at line 1192, "row 4 ... is not built", as now met. It records row 4 as built, not run, and waiting for his word (C-84:1088), and says owed item 118 stays open.
  - **Two ticks**, each one byte plus one `Closed:` line:
    - **Item 96.** Its own closing line (703) reads "until steps 2 to 4 are built". All three are now built (PRs 47, 52 and 53), and the landed README:145 says so.
    - **Item 141**, which is gate B2096 FOUND 1. The landed key at `LabFiles.cs:397` is host, family and id, and the gate measured E2, E4 and E3 closed through the real verb. Its FOR-RECORDS invites this tick.
  - **Items 145 to 147:**
    - 145 is FOUND 1 (`Family`'s default arm, `:419`).
    - 146 is FOUND 2 (`OnlyElements` at `:756` to `:758`, the third reader of the class of items 133 and 143).
    - 147 holds the landing facts, Info 3 to 7, the named limits, the re-scan, and the device-run route of row 4 with the gate's four additions.
  - **One history entry** (9 lines, including H-RESCAN).
  - **One Jira comment on OXPD2-1.** No create, and no comment on OXPD2-62.
- **No ruling of the product owner bears on this pass. This holds.** `kam_rulings_today.sh` ran with `KAM_READ_MARKER` in my scratch. I printed only its `#` header lines and saved nothing. It showed 0 rows on 2026-11-26, the newest live row at 14:30:48 on 2026-11-25 (already C-86), and TAPPED-BUT-OPEN none.
- **The outage, re-measured at source:**
  - Run 45648685455 (`PR #53` dynamic, at 1c7cdbbb) is a failure. Its jobs: python success, csharp success, actions failed at the step `Perform CodeQL Analysis`.
  - That job's log holds `##[error]Server Error` on 1 line (15:48:18Z), right after `Uploading results`. That confirms the commission's "SARIF upload".
  - There is exactly 1 dynamic run at 1c7cdbbb.
  - The PR events show close at 16:39:01Z and reopen at 16:39:06Z. The only new run is `ci` pull_request 45656201864.
  - At 29cacd9b, `dynamic` 45660216367 succeeded, with analyses actions, csharp and python each 0. At 1c7cdbbb only csharp and python exist.
  - The githubstatus reading and GitHub's "cannot be retried" are RELAYED from the commission.
- **The landing, re-measured at source:**
  - 8757daa6 has one parent, 1ccf6d0c. Its tree e20eeff6 equals the trees of 1c7cdbbb and 29cacd9b.
  - The landed message equals `squash-subject.txt` (with #53) and `squash-body.txt` (True, True). `Re-run code scanning` is on 0 lines.
  - The PR run 45660235471 holds `Merge 29cacd9b into 1ccf6d0c` in all 4 logs.
  - Main push run 45661759219: 2338 tests, linux 2334 succeeded and 4 skipped, windows 2317 and 21, RULES 679, unit tests 117 of 117.
  - 7 of 7 check runs are success. Main code scanning at 8757daa6 reads 0 in each of 3 languages.
- **R328 is free.** It appears in 0 of the 20 SEAT kits of 11-25 and 11-26; the control R327 is found in 1 kit (B2102). No pane name holds OXPd2 (04:20:30 and again at 04:30:33). 0 PRs are open, and main is still 8757daa6 at 04:30:33.

## Facts re-measured (instruments)
- **GitHub** (`gh api -X GET`, project GH_CONFIG_DIR, account kamilDatasec, from 04:15:47):
  - pulls/53: 2 commits, 11 files, +1114 and -55. The whole file list is 2 added and 9 modified, equal to landing.txt rows 20 to 30.
  - pulls/54 returns 404. 0 PRs are open.
  - `matching-refs/heads/b2100` is at 29cacd9b; there are 55 heads.
- **Tarball of 8757daa6** (1765526 bytes, 679 files): `facts.py` found POINTERS 26 of 26, and the one-off control FIRED.
- **Project files:** all nine equal `.tools/b2097/READY.manifest`. The build seats B2100 and B2104 wrote no record file.
  - READY lines: B2097 `1d907789...`, B2100 `1c7cdbbb...`, B2104 `29cacd9b...`.
- **Jira** (GET-only fence; POST, PUT, DELETE and PATCH were refused in-process):
  - Census is 63. Done: 33, 39, 41, 47.
  - OXPD2-1 has 14 comments, the newest 41495 (B2097's). OXPD2-62 has 0 comments.
  - 17 phrases each return 0 issues. Controls: MASTER finds OXPD2-1, "chase HP" finds OXPD2-56, and "home screen" finds OXPD2-1 and OXPD2-62.
- **Dry build** (`dry.py`):
  - CLARIFICATIONS: 1196 to 1204 line feeds, `## C-88` at 1198.
  - BACKLOG: 1072 to 1095. Added 23, changed 2 (one byte each); removing by position and un-ticking gives back the old bytes.
    - Ticks at 700 and 1029; Closed lines at 709 and 1036; items 145, 146 and 147 at 1058, 1065 and 1072; the anchor moves 1057 to 1080.
    - 100 open and 47 ticked. "ticked in place" goes 42 to 44, and "Closed in part" stays 19.
  - History: 368 to 378, with B2097's heading moved to line 13.
  - `scan_record` found 0 problems on 36 lines. J-1's `scan_jira` codes are empty. The six scanner controls fired, and the clean line fired none.

## D-decisions (drafter's)
- D1: the form is B2097 plus B2066's tick-in-place proof (ticks put back by position).
- D2: the item-96 tick is a records gap found in passing. B2097 (row 3) did not add a `Closed in part` line under item 96. With row 4 built, the item's own closing condition is met, so the tick is the default (Q2).
- D3: the J-1 prefix is "Records pass after pull request 53". The SKIP RULE names 41495's "...52" prefix as not a near-duplicate, and the selftest plants it.
- D4: no B-numbers and no card ids in any record text, except H-FULL's STATUS path, as in B2097.
- D5: I corrected two literals after measuring:
  - B2104 STATUS holds the RESCAN READY line on 2 lines, not 1.
  - The outage log holds "Uploading code scanning results" on 2 lines and "Perform CodeQL Analysis" on 0. That step name comes from the jobs API.

## Chain inputs
| Step | Inputs | Source |
|---|---|---|
| 0 | kit, sidecar, project files, df, python3 | BASE |
| 1 | `b1785.py` copy, scratch copies | Step 0 |
| 2 | SOURCES, GitHub, tarball, job logs, Jira GETs, B2097/B2100/B2104 STATUS | BASE (origin) |
| 3 | frozen texts, C-number (P-7), BL-OLD8 (before-copy), BL-NEW8 (dry BACKLOG) | Steps 0, 2 |
| 4a | live CLARIFICATIONS, filled C-88 | Step 3 |
| 4b | live BACKLOG, two ticks, BL-CLOSE-96/141, BL-145 to 147 | Step 3 |
| 4c | filled J-1 (C-88 from Step 2) | Step 3 |
| 4d | live history, BL-OLD8/NEW8 (4b), CMT-1 (4c), C-88 | 4b, 4c |

## Q-questions for Tuesday (defaults as written in the kit)
- Q1: C-88 as a Tuesday's note. Default: yes. Alternative: no C-entry.
- Q2: tick owed item 96 (steps 2 to 4 built; steps 3 and 4 not run on a device). Default: tick. Alternative: a `Closed in part` line until the device runs.
- Q3: tick owed item 141 (B2096 FOUND 1 closed by D7). Default: tick.
- Q4: FOUND 1 goes to item 145, FOUND 2 to item 146 (naming 133 and 143), and Info 3 to 7 to item 147. Default: yes. Alternative: FOUND 2 as a line under 143.
- Q5: the outage goes in history H-RESCAN and item 147 only, not in C-88. Default: yes.
- Q6: one comment on OXPD2-1, no ticket, nothing on OXPD2-62. Default: yes.
- Q7: CLAUDE.md line 62 is not edited. Default: yes.
- Q8: no new line under items 103, 118, 133, 138 or 143. Default: yes.

## UNMEASURED / NEVER RUN
- Never run: the seat's helper and selftest, HOLD R and R2 on the live files, the live ticks by position, and the one POST.
- RELAYED, not measured: the githubstatus reading at 03:18 and GitHub's refusal of a re-run (commission). Tuesday's addendum (the head pin read as 29cacd9b) is RELAYED from the commission and Tuesday's daily note; the tree equality is MEASURED.
- The gate's probe results are RELAYED, as in B2097.

## Outside the fences (disclosure)
- `kam_rulings_today.sh` ran twice, with its read marker pointed at `d2105/kam_read_marker` (the script writes that marker). The first run printed only `awk` time/flag columns (4 header lines; no row text). The second printed only `#` header lines. Nothing else was saved, and `kam_msgs.sh` was not run.
- `find -maxdepth 4` over `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files` for the rulings script, file names only.
- I read Tuesday's own git log and commit diff (`git -C TUESDAY show`) to find the landing note. The tarball is extracted under scratch `tar/x/`.
- Two of my own sidecar drafts were moved to `d2105/_quarantine/`. Nothing was deleted.
- No write to the project, Jira, GitHub or the card store. No `decision_queue.sh`. Nothing went to any human or device. No `cd`.
