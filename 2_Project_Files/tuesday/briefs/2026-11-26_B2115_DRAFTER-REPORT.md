STARTABLE: YES

# B2115 DRAFTER REPORT: OXPd records pass for the landing of PR 54 (lane OX-A, the OXPd 1.x client readers), kit for seat R330

Drafter: in-session, read-only, for Tuesday s329. The first clock `Thu 26 Nov 2026 09:56:56 AEDT` and the last `10:14:56` were both printed by `date`. The kit has no typed clock in any slot; its MEASURED-BY-DRAFTER clocks are `date` prints or GitHub timestamps.

Files written (nothing else outside scratch):
- the kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2115_SEAT-R330_oxpd2-records-pr54.md` (sha256 `612a1a7b...`, 112545 bytes, 386 lines, 11 unfilled slot lines, 0 bytes above 126)
- its sidecar `.measured` (143 claims, 0 TODO; `stamp_check.py <kit>` rc=0)
- this report
- scratch only, under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s329/d2115/`

## BLUF
- **Seat id R330 is free.** It is in 0 of the 27 SEAT kits of 11-25 and 11-26 and in no file name. Controls: R329 is in 3 kits (B2108, MPS), R328 in 1.
- **What the kit writes** (form: B2105, with more ticks and B2105's own `Closed in part` shape):
  - **C-89**, a Tuesday's note. It says no new OXPd word of his bears on this pass, and records two coordinator choices so nobody later reads them as his or HP's:
    - the `@` rule is stricter than HP's `LimitedUri` pattern;
    - the adapter README:146-149 sentence is wider than the code at the envelope level (FOUND 1).
  - **Seven ticks in place**, each with a `Closed:` line:
    - 133, 143, 146, 126, 134 and 93 each meet their own closing words.
    - 94 is ticked by evidence: its README limit landed now, and the lab read before a register (`Oxpd1Command.cs:925`/`:1011`/`:1047-1050`) has been on main since before the landing, with the same blob at 8757daa6 and c73cda4c.
  - **One `Closed in part` line under 85**: the summary is narrowed, the attribute cap is still owed.
  - **Four new owed items:**
    - 148 is FOUND 1.
    - 149 is FOUND 2.
    - 150 is the two Lab README sentences (`:220`, `:308-311`) for lane OX-B.
    - 151 is the landing facts, Info 3 to 7, and the kit and seat notes.
  - **One history entry** (7 texts).
  - **One comment on OXPD2-1.** No create.
- **Product owner (commission's question).** There is no OXPd ruling after 2026-11-25 14:30. On 2026-11-26 he tapped twice, both at 09:14:
  - **The Datasec day's plan, option a 'Carry on'.** Its text names 'OXPd lanes A and B'. I read it with `decision_queue.sh show` into scratch.
  - **An MPS card.**
  - The day's-plan tap agrees with the work but decides none of its choices. The kit says so in C-89 and in H-OWNER (Q1).
- **The equivalent mutant (commission item 3).** The form does record such things: B2105's item 147 carried the kit's limits and the review's Info. So it is a clause of item 151, not a line of its own (Q5).

## Facts re-measured (instruments)
- **GitHub** (`gh api -X GET`, project GH_CONFIG_DIR, kamilDatasec, from 09:58:26; re-read at 10:14:56):
  - main is c73cda4c, with one parent 8757daa6 and tree dd15534f, the same as head 8ce4a86c's.
  - PR 54: merged 22:46:22Z; 1 commit, 10 files (all modified), +227 and -53. The file list equals landing.txt rows 18 to 27.
  - pulls/55 returns 404. 0 PRs are open.
  - The landed subject equals `squash-subject.txt` with #54 (True; the control with #53 is False).
  - The landed body equals `squash-body.txt` without its final LF (True; with it, False; the same as B2105's D7).
  - The PR run 45715406005 holds `Merge 8ce4a86c... into 8757daa6...` in all 4 logs.
  - Main push run 45716051253:
    - linux: total 2367 (on 2 lines), succeeded 2363, skipped 4, GUARD 14.
    - windows: succeeded 2346, skipped 21, GUARD 15.
    - RULES 679; 117 unit tests against a floor of 117; secret-scan reads `no leaks found` on 3 lines.
  - Check runs: 7 of 7 success. Code scanning at c73cda4c reads 0 for each of 3 languages; open alerts 0.
  - The Lab README and `Oxpd1Command.cs` blobs are the same at both shas.
- **Tarball of c73cda4c** (1767857 bytes, 679 files): `facts.py` found POINTERS 55 of 55, and the one-line-off control FIRED.
- **Project:**
  - All nine files equal `.tools/b2105/READY.manifest`.
  - B2105's READY line is `52af9637...` (C-88). B2109's READY line is `8ce4a86c`, and it has 7 DEVIATIONS.
  - All P-3 counts were measured by `counts.py`.
  - Each of the nine edited items' blocks is 7 lines ending in `Discovered:` (`blocks.py`).
- **Jira** (GET-only fence; POST, PUT, DELETE and PATCH were refused in-process):
  - Census is 63. Done: 33, 39, 41, 47.
  - OXPD2-1 has 15 comments, the newest 41499 (B2105's). 0 comments start 'Records pass after pull request 54'.
  - 15 phrases each return 0 issues. The controls fire.
- **Dry build** (`dry.py`):
  - CLARIFICATIONS: 1204 to 1212 line feeds, `## C-89` at 1206.
  - BACKLOG: 1095 to 1131. Added 36, changed 7 (one byte each); removing by position and un-ticking gives back the old bytes.
    - 97 open and 54 ticked. "ticked in place" goes 44 to 51, and "Closed in part" goes 19 to 20.
  - History: 378 to 386, with B2105's heading moved to line 11.
  - `scan_record` found 0 problems on 47 lines. J-1's `scan_jira` codes are empty. The six scanner controls fired.
- **Panes:** none named OXPd2 (10:02:29 and 10:14:56). Composer-C110 was live at 10:02 and gone by 10:14.

## D-decisions (drafter's)
- D1: the form is B2105. The `Closed in part` shape is taken from item 96's lines (BACKLOG 707 and 708).
- D2: the new items are ordered FOUNDs first (148, 149), then the OX-B README item (150), then the landing item (151).
- D3: no card ids appear in the kit. The day's-plan tap is cited by its option label and detail only.
- D4: J-1 avoids the scanner's words (lane, gate, seat), backticks, double quotes and the `@` character ("at sign").
- D5: on 93, the cells are W10 and B07, which are new cells, not the W07 row the item asked for. The kit's Q9 was the coordinator's, and the text says so.

## Chain inputs
| Step | Inputs | Source |
|---|---|---|
| 0 | kit, sidecar, project files, df, python3 | BASE |
| 1 | `b1785.py` copy, scratch copies | Step 0 |
| 2 | SOURCES, GitHub, tarball, job logs, Jira GETs, B2105/B2109 STATUS | BASE (origin) |
| 3 | frozen texts, C-number (P-7), BL-OLD8 (before-copy), BL-NEW8 (dry BACKLOG) | Steps 0, 2 |
| 4a | live CLARIFICATIONS, filled C-89 | Step 3 |
| 4b | live BACKLOG, 7 ticks, 7 Closed lines, BL-PART-85, BL-148 to 151 | Step 3 |
| 4c | filled J-1 (C-89 from Step 2) | Step 3 |
| 4d | live history, BL-OLD8/NEW8 (4b), CMT-1 (4c), C-89 | 4b, 4c |

## Q-questions for Tuesday (defaults as written in the kit)
- **Q1: C-89 as a Tuesday's note naming the day's-plan tap.** Default: yes.
  - Alternative (a): no C-entry.
  - Alternative (b): drop the quoted tap. Line 3 of the file says entries are copied from the board export, and this quote comes from my card-store print.
- **Q2: tick 126 and 134.** Each one's first option landed whole; the stale Lab README sentences go to item 150. Default: tick. Alternative: a `Closed in part` line under each.
- **Q3: tick 94 by evidence.** Both halves are now on main, and 106 stays open. Default: tick. Alternative: `Closed in part`, keeping the kit and commission framing that "94's lab half is 106".
- **Q4: one `Closed in part` line under 85.** Default: yes. Alternative: no line.
- **Q5: the findings go to 148, 149, 150 and 151, with the equivalent mutant as a clause of 151.** Default: yes. Alternative: FOUND 2 folded into 151.
- **Q6: one comment on OXPD2-1 and no ticket.** Default: yes.
- **Q7: CLAUDE.md is not edited.** Default: yes.
- **Q8: no line under 106, 127 or 138.** Default: yes.

## UNMEASURED / NEVER RUN
- **Never run:** the seat's helper and selftest, HOLD R and R2 on the live files, the seven live ticks by position, and the one POST.
- **RELAYED, not measured by me:**
  - main's `hosted3.py` PASS at c73cda4c (from the commission; `g2112/logs-main-c73cda4c` holds only job logs, and I found no PASS line in a file);
  - every probe, mutant and red/green count of the review.
- **What the stamp re-checks:**
  - RULINGS-NEW is now worded `no OXPd ruling newer than 2026-11-25 14:30`, not B2105's `none newer than`, because there are rows on 11-26 that are not OXPd.
  - Panes and main at the stamp.

## Outside the fences (disclosure)
- `kam_rulings_today.sh` ran twice with `KAM_READ_MARKER` at `d2115/kam_read_marker`:
  - the first run printed only the time and source columns;
  - the second printed the two 11-26 rows whole to my session, to judge them.
  - Nothing was saved, and `kam_msgs.sh` was not run.
- `decision_queue.sh show <the day's-plan id>` wrote `d2115/card-morning.txt`, read through an id count of 1.
- I ran `find -maxdepth 4` over Tuesday's `2_Project_Files` for two script paths (file names only).
- I ran `jget.py sums`, which made GETs of OXPD2-1 to OXPD2-64. 64 returned 404 and ended the loop with a KeyError traceback; no write.
- No write to the project, Jira, GitHub or the card store; no `cd`; nothing deleted; nothing to any human or device.
