STARTABLE: YES

# B2132 DRAFTER REPORT: the OXPd records pass for the landing of PR 56 (lane OX-B kit 2, the lab tool oxpd1), a kit for seat R337

I am the in-session, read-only drafter for Tuesday s331. `date` printed my first clock as `Thu 26 Nov 2026 23:51:56 AEDT` and my last as `Fri 27 Nov 2026 00:10:25 AEDT`. No slot in the kit holds a typed clock. Every MEASURED-BY-DRAFTER clock in it is either a `date` print or a GitHub timestamp, and GitHub timestamps are converted to AEDT by `zoneinfo`.

Files written (nothing else outside my scratch):
- **The kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2132_SEAT-R337_oxpd2-records-pr56.md`
  - sha256 `2cc5b298...`; 121224 bytes; 386 lines; 7 lines over 2000 characters (1, 17, 174, 175, 234, 321 and 333).
  - 11 slot lines left unfilled; 0 bytes above 126.
- **Its sidecar `.measured`:** 139 claims, 0 TODO. `stamp_check.py <kit>` returns rc 0.
- **This report.**
- **My scratch:** only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s331/d2132/`. The kit's source with placeholders is `kit.src.md`, filled by `fillkit.py`.

## BLUF
- **Seat id R337 is free.**
  - R337 is named in 0 of the 38 SEAT kits of 11-25 and 11-26, and in no file name.
  - Controls: R336 (B2131, NexusAI) is named in 1 kit, R335 in 4 and R334 in 4.
  - The panes at 23:56:22 and again at 00:10:25 were `%0 tuesday`, `%375` and `%376` (unnamed). None holds `OXPd2`.
- **What the kit writes.** The form is B2124: six ticks, no part line, and four new items.
  - **C-91**, a Tuesday's note. It records two coordinator choices, so that nobody later reads them as his or HP's:
    - the three address options take printable ASCII only, which is stricter than HP's own address type. The device host and the callback host are outside that rule.
    - the read before a register refuses more than the reviewer proposed. The README's "at any depth" is wider than the code for a masked element.
  - **Six ticks in place**, each with a `Closed:` line: 106, 107, 109, 110, 135 and 136.
  - **New owed items:**
    - 155 is FOUND 1 (the masked second id);
    - 156 is FOUND 2 together with H9 (the callback host with a lone surrogate throws; hosts outside ASCII; the device host);
    - 157 is FOUND 3 (the XML white-space test is pinned by no cell);
    - 158 holds the landing facts, FOUND 4 to 7, the answers to Tuesday's points, H6 and H14 to H17, and the seat's ten deviations.
  - **One history entry and one comment on OXPD2-1.** No ticket is created.
- **Product owner (the commission's question): no ruling of his bears on this pass.**
  - His board read at 23:55:24 shows two rows on 2026-11-26, both at 09:14, and nothing later. TAPPED-BUT-OPEN is none.
  - His newest OXPd ruling is still 2026-11-25 14:30. I read no card.
  - It is now 27 Nov, so the stamp's RULINGS-NEW slot must also cover any row of his on 11-27.
- **Main's push run at 38a031e5 was re-measured.** My byte copy of the review's `hosted3.py` (sha256 969fe376) ran with `--wait` from 23:52:19 to 23:53:30 and read `HOSTED 38a031e5...: PASS` (total 2422, rules 679). The control at `--total 2423` read `FAIL 4`.
  - Analyze (csharp) was still running at the first read. I re-read it at 23:56:29: the check runs read 7 of 7 success, and code scanning is 0 for each of 3 languages at 38a031e5.

## Facts re-measured (instruments)
- **GitHub** (`gh api -X GET`, the project's GH_CONFIG_DIR, account kamilDatasec):
  - **Main and the merge:** main is 38a031e5, one parent 504ca043, tree 22c5f214, the same tree as head 0ae90664.
  - **PR 56:**
    - Merged at 12:49:23Z, which is 23:49:23 AEDT. One commit, 6 files, all modified, +363 and -23. The six numstat rows sum to 363 and 23 and equal landing.txt lines 20 to 25.
    - pulls/57 and issues/57 both answer 404. 0 PRs are open. The newest are 56 to 52.
  - **The landed message:**
    - The subject equals `squash-subject.txt` with #56 (True; the control with #55 is False).
    - The body equals `squash-body.txt` without its final LF (True).
  - **The PR run** 45822109786 holds `Merge 0ae90664… into 504ca043…` once in each of its 4 logs.
    - linux: 2422 total, 2418 succeeded, 4 skipped, GUARD 14.
    - windows: 2401 succeeded, 21 skipped, GUARD 15.
    - RULES 679; 117 unit tests against a floor of 117; secret-scan lines with their controls.
  - **The push run at 504ca043** has `total: 2384` on 2 lines (control `total: 2422`: 0). 2384 plus the squash body's 38 new cases is 2422.
  - **Blobs:**
    - Oxpd1Command.cs, Oxpd1EchoVerb.cs and the README changed between 504ca043 and 38a031e5.
    - LabFiles.cs, Oxpd1Soap.cs and Oxpd1Client.cs did not change.
- **Tarball of 38a031e5** (1775699 bytes, 679 files): `facts.py` found POINTERS 64 of 64, and the one-line-off control FIRED.
- **Project:**
  - All nine files equal `.tools/b2124/READY.manifest`, by shasum (BACKLOG c816826c, CLARIFICATIONS 1aed594f, history 937e71b2).
  - B2124 READY is afb5806b (C-90, comment 41518). B2128 READY is 0ae90664.
  - Each of 106, 107, 109, 110, 135, 136 and 154 is a 7-line block ending in `Discovered:` (`blocks.py`). Owed items run 1 to 154: 94 open, 60 ticked.
- **Jira** (GET-only fence; POST, PUT, DELETE and PATCH were refused in-process):
  - The census is 63. Done: 33, 39, 41, 47.
  - OXPD2-1 has 17 comments; the newest is 41518. 0 comments start `Records pass after pull request 56`.
  - All 11 phrases return 0 issues. The 5 controls fire.
- **Dry build** (`dry.py`):
  - CLARIFICATIONS: 1220 to 1228 line feeds, C-91 at line 1222.
  - BACKLOG: 1158 to 1192. Added 34, changed 6. Removing by position and un-ticking gives back the old bytes.
    - 92 open, 66 ticked.
    - Ticked in place goes from 57 to 63.
    - The anchor heading moves from 1143 to 1177.
  - History: 394 to 402; B2124's heading moves to line 11.
  - `scan_record` finds 0 problems on 45 lines. J-1 has no `scan_jira` codes, and its ADF read-back is EQUAL.
  - Checks on the filled text:
    - 0 doubled words;
    - 0 doubled groups of 1 to 8 words;
    - 0 repeated runs of 12 or more characters.
    - All three controls fired.
  - The frozen table re-parsed from the written kit is byte-equal to the one generated from the source.

## D-decisions (drafter's)
- **D1 (form).** The form is B2124. The `Closed:` shape is copied from its BL-CLOSE lines, and the new items use the seven-line form of items 152 to 154.
- **D2 (each frozen claim checked against its source).** Per today's lessons, I checked every frozen sentence about what code, a test or the review does against its source line. I re-read each filled text for a claim its own limit contradicts. Corrections made before freezing:
  - **BL-CLOSE-106.** It said the README Limits name what "the client never hands the lab". The id held as text of a record's other elements IS handed to the lab, so the line now says "what that read cannot see".
  - **BL-158.** The same error appeared in its H6 sentence, and is fixed the same way.
  - **C-91.** It said the widened read "refuses more than proposed", but the list it gave included the result's text and attributes, which the reviewer had proposed. The sentence now separates the two.
  - **Ambiguous `:315` pointers.** These pointers came after a pointer into another file. They now carry the README's full path.
  - **The C-42 range.** It is `:268` to `:274`. Line 276 is `## C-43`, although the form wrote 276.
  - **Two doubled-word hits from the dry run were reworded:**
    - "`ID`, `Id`";
    - "the commit (the commit".
- **D3 (the scanner that judges).** The record texts are judged by `scan_record` and J-1 by `scan_jira` (`b1785.py`), not by `words.py`. Even so, the texts write the XML node as `<?...?>`, so no frozen text holds the term that ANSWER-1 had to accept.
- **D4 (seat's deviations: ten, not nine).** The commission says nine. B2128's STATUS numbers eight items in `## DEVIATIONS` and adds 9 and 10 in FINAL (`p8.py`). The kit says ten, and P-1 checks 8 plus the FINAL line.
- **D5 (no card ids or names).** No card id or person's name appears in the kit text that the seat copies.
- **D6 (J-1 wording).** J-1 avoids lane, gate, seat, backticks and quotes.

## Chain inputs
| Step | Inputs | Source |
|---|---|---|
| 0 | kit, sidecar, project files, df, python3 | BASE |
| 1 | the `b1785.py` copy, scratch copies | Step 0 |
| 2 | SOURCES, GitHub, tarball, job logs, Jira GETs, B2124/B2128 STATUS | BASE (origin) |
| 3 | frozen texts, C-number (P-7), BL-OLD8 (the before-copy), BL-NEW8 (the dry BACKLOG) | Steps 0, 2 |
| 4a | live CLARIFICATIONS, filled C-91 | Step 3 |
| 4b | live BACKLOG, 6 ticks, 6 Closed lines, BL-155 to BL-158 | Step 3 |
| 4c | filled J-1 (C-91 from Step 2) | Step 3 |
| 4d | live history, BL-OLD8/NEW8 (4b), CMT-1 (4c), C-91 | 4b, 4c |

## Q-questions for Tuesday (defaults as written in the kit)
- **Q1: C-91 as a Tuesday's note recording two choices.** Default: yes.
  - (a) No C-entry.
  - (b) Keep only the ASCII rule.
- **Q2: tick 106 whole.** Its closing words name the reader's proposal, which landed in widened form. FOUND 1's masked id is not a child of the record, and the client empties it before the lab reads it (the H6 class). It is filed as 155. Default: tick. Alternative: a `Closed in part` line, which forces a re-draft.
- **Q3: tick 107.** The proposal itself did not land; a stricter rule did. Default: tick, saying "by a rule stricter than the reader's proposal". Alternative: a part line.
- **Q4: FOUND 2 goes to a new item 156 together with H9.** It does not fit 135, whose own words are met, or 109, which covers only the write options. Default: yes. Alternative: a part line under 135.
- **Q5: FOUND 3 gets its own item 157,** as FOR-RECORDS proposes. Default: yes. Alternative: a clause of 158.
- **Q6: every other note goes to 158.** "Four" corrected to "six" is a kit word, and the README already says six. Default: yes.
- **Q7: one comment on OXPD2-1 and no ticket.** Default: yes.
- **Q8: 152, 153, 154 and 138 get no line, and CLAUDE.md is not edited.** Default: yes.

## UNMEASURED / NEVER RUN
- **Never run:** the seat's helper and selftest, HOLD R and R2 on the live files, the six live ticks by position, and the one POST.
- **RELAYED, not measured by me:** every probe, mutant and red/green count of the review and the seat (macOS arm64). FOUND 1's deny-list stems are the reader's. I read only `Oxpd1Soap.cs:363-366` and `Oxpd1Client.cs:245`.

## Outside the fences (disclosure)
- **Board read.** `kam_rulings_today.sh` ran once, with `KAM_READ_MARKER` pointed at `d2132/kam_read_marker`. Only the first 40 characters of each row went to my session, and nothing was saved.
  - Two card-id prefixes showed in my session. Neither is written to any file.
  - `kam_msgs.sh` was not run, and no card was read.
- **hosted3.py.** I ran a byte copy of the review's `hosted3.py` (header read first; GET only) twice: once with `--wait` (in the background), once as the control. It wrote job logs into `d2132/hosted-main*`.
- **How the kit and sidecar were written.** I wrote them with `cat` from my scratch (the kit) and by `stamp_check.py --init`, then `cat` of `side.py`'s output (the sidecar). I did not use the Write tool. Their bytes are those of `kit.out.md` and `side.out` (`cmp` equal).
- **Find on my side only.** `find -maxdepth 4` ran over Tuesday's `2_Project_Files`, for the board reader's path (file names only).
- **Grep inside my own tarball extraction.** I ran `grep -r` inside `d2132/tar/x` (the tarball extraction) for DenyList. I never ran it over the project folder.
- **Hook refusals, each re-issued correctly.**
  - A `cd` in my first Bash call.
  - An `echo ======` separator.
- **No write anywhere else.** Nothing was written to the project, Jira, GitHub or the card store. Nothing was deleted. Nothing went to any human or device. The B2131 files and `d2131` were not touched (only `ls`, and a read of B2131's commission for R-ids).
