STARTABLE: YES

# B2124 DRAFTER REPORT: the OXPd records pass for the landing of PR 55 (lane OX-B kit 1, the lab tool oxpd1), a kit for seat R334

I am the in-session, read-only drafter for Tuesday s330. `date` printed my first clock as `Thu 26 Nov 2026 13:59:05 AEDT` and my last as `14:16:37`. No slot in the kit holds a typed clock. Every MEASURED-BY-DRAFTER clock in it is either a `date` print or a GitHub timestamp, and GitHub timestamps are converted to AEDT by `zoneinfo`.

Files written (nothing else outside my scratch):
- **The kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2124_SEAT-R334_oxpd2-records-pr55.md`
  - sha256 `a1537d50...`; 108431 bytes; 359 lines.
  - 11 slot lines left unfilled; 0 bytes above 126.
- **Its sidecar `.measured`:** 133 claims, 0 TODO. `stamp_check.py <kit>` returns rc 0.
- **This report.**
- **My scratch:** only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s330/d2124/`. The kit's source with placeholders is `kit.src.md`, filled by `fillkit.py`.

## BLUF
- **Seat id R334 is free.**
  - R334 is named in 0 of the 33 SEAT kits of 11-25 and 11-26, and in no file name.
  - Controls: R333 is named in 5 kits and R330 in 5.
  - The panes at 14:06:09 and again at 14:16:37 were `%0 tuesday`, `%548 Datasec/NexusAI-N179` and four unnamed panes. None holds `OXPd2`.
- **What the kit writes.** The form is B2115: six ticks, no part line, and three new items.
  - **C-90**, a Tuesday's note. It records two coordinator choices, so that nobody later reads them as his:
    - the kit's limit H9: a run folder that can be listed but not entered. The review measured it as a false `nothing is owed`, and the README's wording is wider than the code there;
    - the certificate bound is on the bytes read, rather than refusing every path that is not a regular file.
  - **Six ticks in place**, each with a `Closed:` line: 108, 111, 127, 142, 145 and 150. Each one's own closing words are met at 504ca043, checked by its pointer and by the review's measurement.
  - **New owed items:**
    - 152 is FOUND 1 (listed but not entered);
    - 153 is FOUND 2 (the bound of 40 links is pinned by no test);
    - 154 holds the landing facts; Info 3 to 8; the FOR-RECORDS Info items; H12, H13a and H13b; and the seat's eight deviations, including its `rm -f`.
  - **One history entry and one comment on OXPD2-1.** No ticket is created.
- **Product owner (the commission's question): no ruling of his bears on this pass.**
  - His board read at 14:01 shows two rows on 2026-11-26, both at 09:14, and nothing later. TAPPED-BUT-OPEN is none.
  - His newest OXPd ruling is still 2026-11-25 14:30. I read no card.
- **Main's push run at 504ca043 was re-measured.** My byte copy of the review's `hosted3.py` read `HOSTED 504ca043...: PASS` (total 2384, rules 679) at 14:02:45. The control at `--total 2385` read `FAIL 4`.
- **Kit 2 of OX-B** (owed 106, 107, 109, 110, 135 and 136) is named only in item 154 and in FOR TUESDAY. Nothing is recorded for it.

## Facts re-measured (instruments)
- **GitHub** (`gh api -X GET`, the project's GH_CONFIG_DIR, account kamilDatasec):
  - **Main and the merge:** main is 504ca043, one parent c73cda4c, tree 7c987de4, the same tree as head cd2a3e13.
  - **PR 55:**
    - Merged at 02:57:55Z, which is 13:57:55 AEDT. One commit, 5 files, all modified, +335 and -41. The file list equals landing.txt lines 19 to 23.
    - pulls/56 and issues/56 both answer 404. 0 PRs are open. The newest five are 55 to 51.
  - **The landed message:**
    - The subject equals `squash-subject.txt` with #55 (True; the control with #54 is False).
    - The body equals `squash-body.txt` without its final LF (True).
  - **The PR run** 45745041466 holds `Merge cd2a3e13… into c73cda4c…` once in each of its 4 logs.
    - linux: 2384 total, 2380 succeeded, 4 skipped, GUARD 14.
    - windows: 2363 succeeded, 21 skipped, GUARD 15.
    - RULES 679; 117 unit tests against a floor of 117; secret-scan: no leaks, with its control lines.
  - **Main's push run** 45745847562 reads the same numbers. Check runs are 7 of 7 success. Code scanning at 504ca043 is 0 for each of 3 languages. Open alerts: 0.
  - **The push run at c73cda4c** has `total: 2367` on 2 lines.
  - **Blobs:**
    - The Lab README and LabFiles.cs changed between c73cda4c and 504ca043.
    - Oxpd1Command.cs, Oxpd1EchoVerb.cs and Oxpd1Echo.cs did not change.
    - `Known, not changed here` is on 1 line at c73cda4c and on 0 lines at 504ca043.
- **Tarball of 504ca043** (1770839 bytes, 679 files): `facts.py` found POINTERS 49 of 49, and the one-line-off control FIRED.
- **Project:**
  - All nine files equal `.tools/b2115/READY.manifest`, by shasum.
  - B2115 READY is 42f4d663 (C-89, comment 41510). B2122 READY is cd2a3e13, with 8 deviations, 1 line of which holds `rm -f`.
  - The P-3 counts come from `probe.py`.
  - Each of 108, 111, 127, 142, 145, 150 and 151 is a 7-line block ending in `Discovered:` (`blocks.py`). Owed items run 1 to 151: 97 open, 54 ticked.
- **Jira** (GET-only fence; POST, PUT, DELETE and PATCH were refused in-process):
  - The census is 63. Done: 33, 39, 41, 47.
  - OXPD2-1 has 16 comments; the newest is 41510. 0 comments start `Records pass after pull request 55`.
  - All 11 phrases return 0 issues. The 5 controls fire, including `Records pass after pull request 54` → OXPD2-1.
- **Dry build** (`dry.py`):
  - CLARIFICATIONS: 1212 to 1220 line feeds, C-90 at line 1214.
  - BACKLOG: 1131 to 1158. Added 27, changed 6. Removing by position and un-ticking gives back the old bytes.
    - 94 open, 60 ticked.
    - Ticked in place goes from 51 to 57.
    - The anchor heading moves from 1116 to 1143.
  - History: 386 to 394; B2115's heading moves to line 11.
  - `scan_record` finds 0 problems on 38 lines. J-1 has no `scan_jira` codes, and its ADF read-back is EQUAL.
  - Checks on the filled text: 0 doubled words and 0 doubled groups (n=1 to 5). Both controls fired.

## D-decisions (drafter's)
- **D1 (form).** The form is B2115. The `Closed:` shape is copied from its BL-CLOSE lines, and the new items use the seven-line form of items 148 to 151.
- **D2 (each frozen claim checked against its source).** Per Tuesday's lesson this morning, I checked every frozen sentence about what code, a test or the review does against its source line, and re-read each text for any claim its own limit contradicts. Three wordings were tightened before freezing:
  - 127: outside a work tree, a shape is "made where the system makes them **or refused by the system**";
  - 142: "a link to `/dev/zero`", not an ambiguous "it";
  - 154: "the enumerator's construction" opens the folder.
- **D3 (no card ids or names).** No card id appears in the kit. The only scanner `S-NAME` hits are the control string `test_by_kam_x` and the tool name `kam_rulings_today.sh`. B2115 carried both too.
- **D4 (J-1 wording).** J-1 avoids lane, gate, seat, backticks and quotes.

## Chain inputs
| Step | Inputs | Source |
|---|---|---|
| 0 | kit, sidecar, project files, df, python3 | BASE |
| 1 | the `b1785.py` copy, scratch copies | Step 0 |
| 2 | SOURCES, GitHub, tarball, job logs, Jira GETs, B2115/B2122 STATUS | BASE (origin) |
| 3 | frozen texts, C-number (P-7), BL-OLD8 (the before-copy), BL-NEW8 (the dry BACKLOG) | Steps 0, 2 |
| 4a | live CLARIFICATIONS, filled C-90 | Step 3 |
| 4b | live BACKLOG, 6 ticks, 6 Closed lines, BL-152 to BL-154 | Step 3 |
| 4c | filled J-1 (C-90 from Step 2) | Step 3 |
| 4d | live history, BL-OLD8/NEW8 (4b), CMT-1 (4c), C-90 | 4b, 4c |

## Q-questions for Tuesday (defaults as written in the kit)
- **Q1: C-90 as a Tuesday's note recording two choices.** Default: yes.
  - (a) No C-entry.
  - (b) Keep only the first choice.
- **Q2: tick 108 whole.** Its own closing words are "the reader's proposal", and that proposal landed. FOUND 1 (mode 0400/0600) is H9, a different shape, filed as 152. Default: tick. Alternative: a `Closed in part` line, which forces a re-draft.
- **Q3: tick 150.** Both sentences are gone. Default: tick.
- **Q4: FOUND 1 goes to 152, FOUND 2 to 153, and every Info item and note to 154.** Default: yes. Alternative: fold FOUND 2 into 154.
- **Q5: one comment on OXPD2-1 and no ticket.** Default: yes.
- **Q6: kit 2's items get no line.** Kit 2 is named only. Default: yes.
- **Q7: CLAUDE.md is not edited.** Default: yes.
- **Q8: owed item 138 gets no line.** Default: yes.

## UNMEASURED / NEVER RUN
- **Never run:** the seat's helper and selftest, HOLD R and R2 on the live files, the six live ticks by position, and the one POST.
- **RELAYED, not measured by me:** every probe, mutant and red/green count of the review and the seat (macOS arm64).

## Outside the fences (disclosure)
- **Board read.** `kam_rulings_today.sh` ran once, with `KAM_READ_MARKER` pointed at `d2124/kam_read_marker`. Only the first 40 characters of each row went to my session, and nothing was saved.
  - Those 40 characters showed two card-id prefixes in my session. Neither is written to any file.
  - `kam_msgs.sh` was not run, and no card was read.
- **hosted3.py.** I ran a byte copy of the review's `hosted3.py` (header read first; GET only) twice: once with `--wait`, once as the control. It wrote job logs into `d2124/hosted-main*`.
- **sed -i on my own scratch.** I ran `sed -i` once, on my own scratch `dry.py`, to fix a tokenizer.
- **Find on my side only.** `find -maxdepth 4` ran over Tuesday's `2_Project_Files`, for script paths (file names only).
- **No write anywhere else.** Nothing was written to the project, Jira, GitHub or the card store. No `cd`. Nothing deleted. No recursive read of the project folder. Nothing went to any human or device. The NexusAI pane was not touched.
