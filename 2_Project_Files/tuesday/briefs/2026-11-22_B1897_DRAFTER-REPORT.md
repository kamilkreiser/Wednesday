STARTABLE: YES - the kit is complete in the form of B1884 and waits for Tuesday's stamp and slots; `stamp_check.py` exits 0 (152 claims, 152 measured; about 100 are source measurements, the rest are counts over the kit's own instruction text, said so in the sidecar), the four comments, the optional ticket and the four record texts scan clean with the project's scanner copy (14 controls fire), and main, root records and Jira were re-read at 17:07 and are unchanged.

# B1897 DRAFTER REPORT (Sonnet) - MPS records kit R295: PR 226 (MPSCALC-430, 431, 432, 433)
Clock: first read Sun 22 Nov 2026 16:50:49 AEDT, last re-read 17:07:36 AEDT. Read-only except the kit, sidecar, this report and scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s308/d1897/`.

## Files
- Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1897_SEAT-R295_mps-records-226.md` (385 lines, 124199 bytes, ASCII, sha256 `b6b8fe416e544b356d8b88ed11273e0348861fff3aa5b602aaac9ef661fe75b4`, seat Datasec/MPS-R295, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, 11 lines carry four underscores: the 10 Stamp slots and the last line).
- Sidecar `...md.measured` (154 lines). Scratch: texts.py, texts2.py, build.py, kit_template.md, scan_drv.py, scan_rec.py, fill_sidecar.py, jget.py, jsearch.py, raw/ (four files of main plus showcase.bicep and ci.yml), base/, tar_main/ (extracted tarball of main, nothing run from it), pyjob.log.
- Read load by program: 133180 bytes of sources + 124199 kit + 13327 tickets = 270706 bytes (under 300 kB).

## BLUF
Records ONE entry (expected C-191), FOUR comments (430, 431, 432, 433), up to FOUR moves to Done by id 41 (slot MOVE), up to ONE new ticket (slot CREATE, default NONE), plus BACKLOG, JIRA.md and history rows; at most 9 Jira writes.
- **Default MOVE is `430,432,433`; MPSCALC-431 stays open.** Its line "the first failure printed names the key of the defect" is met by the sub-test label only (gate F1; the plant tests' message is still the bare `unique anchor`, on 3 lines: test_infra.py:586, :620, :676 at main). Its comment says so in its first sentence and in the line-3 reading. The alternative (MOVE with 431) is offered with its own frozen move-431 sentence and REFUSE 9 (431 may move only with CREATE `1` and the create read back).
- F2 (9449 secret-scan history findings) is a BACKLOG row [B1897-OWED-2] naming locations and counts only (9426 + 17 + 2 + 2 + 2, arithmetic checked); no value, no scan run by the seat. F3 (three zero-byte strays) is a records sentence in the entry and a row [B1897-OWED-3]; the seat is forbidden to touch them.
- The follow-up for the 431 line is BACKLOG row [B1897-OWED-1] by default; the ticket text (summary 253 characters, six paragraphs, marker LAND-NEW-ANCHORMSG-22NOV, label records-pass-1122b) is frozen in PART 2 for CREATE `1`.

## Facts re-measured (instruments in the kit tables and the sidecar)
- Code main by `gh api -X GET git/ref/heads/main`: `ec281cfb35a1356d59e23e1c69e8eab1e1852f2e` at 16:51 and 17:07 (unchanged); open PRs 0; open code-scanning alerts 0. PR 226 merged 2026-11-22T05:32:14Z = 16:32:14 AEDT (checked with zoneinfo), one parent 9c9a7219, squash tree a534af44 = head 48134ee0 tree, 2 files +107 -10; blobs test_infra.py 6486350d and validate.sh 22322327 re-hashed over the raw files (equal to the tree and to the commission).
- CI of the squash: 8 of 8 check runs success, `Push on main` and `ci` success, 4 analyses with 0 results. Python job log (id 137108247637, ANSI stripped, 641 lines): 15 groups, 15 `Ran`, 15 `OK`, 0 `FAILED (`; test_infra.py Ran 49, test_validate_script.py Ran 6; the five new-class tests and the one site-plant test listed ok. The web job log was NOT read (not relevant to a test-and-comment change).
- Tests 43 to 49 by the indented pattern (column-1 pattern 0 both); classes 8 to 10; diff 106/9 and `4c4`; `README.md step 3` 0 lines in infra/scripts at main (tarball of main, 734 files), 1 at base; compare 9c9a7219...main ahead 1, 2 files; debb5e28...ec281cfb ahead 4, 8 files.
- Jira (GET only): 433 issues, 262 Done, 171 not Done (equals B1884's after-census, re-read three times, identical); MPSCALC-430/431/432/433 Backlog, 0 comments, 0 links; MPSCALC-434 404; transitions list `41 Done` on each; my reader reproduces B1884's frozen figures for MPSCALC-426 and the MPSCALC-433 summary hash. Markers REC-LAND-430..433 and LAND-NEW-ANCHORMSG read 0; label records-pass-1122b reads 0 (controls fire).
- Root records: main c205d1c1 (the B1884 commit), `### C-190` once, `### C-191` 0, status exactly the three files, no remote, no records/b1897, no .tools/b1897, no lock, 0 `Datasec/MPS` panes, 995 GiB free.
- Scanner: copy of `.tools/b1800/scan.py` (sha256 d21a053d..., equal), over 22 jira texts and 4 record texts: 0 hits; 14 controls fire; extra refusals fire. The five frozen comment sentences hash as printed, and the four comments extracted back out of the written kit hash equal to their printed figures (4 of 4, mutant unequal, marker once at the end).

## D-decisions (mine, Tuesday overrules)
- D1 The clause "no other byte of infra changes" (430, 431, 432) and "no template, test or code behaviour changes" (433) is written as the coordinator's reading that it binds the change built for that ticket, because the one squash also carries the other tickets' paths (the review graded each MET without remarking it). Stated plainly in each comment and in THE BASIS.
- D2 MPSCALC-431's comment carries the label-only gap in its BLUF and line 3, "graded Minor" for the review's finding, and never says the message names the key (a HOLD).
- D3 The move-431 sentence is mine (four of five lines met, the fifth by label only, a follow-up carries the message); the stock move sentence says "every clause reads met", which would be untrue for 431.
- D4 CREATE default NONE (431 itself carries the line; a second ticket would duplicate it).
- D5 The CHECKS fill-in reads the python job log by `##[group]` file name, not the web log.
- D6 New entry row ids B1897-DONE-1 and OWED-1..4; a fifth row for the deploy card names main ec281cfb (ahead of the site by 4 commits and 8 paths, of which this PR adds none under src, web or contract).
- D7 F2 row cites MPSCALC-221 (Done, secret-scan false positive of the synthetic care key) as the earlier case; found by a Jira search for "gitleaks" and "generic-api-key".

## Q-questions for Tuesday (defaults in the kit)
- Q1 MOVE: `430,432,433` (default recommended, 431 open) or `430,431,432,433` with CREATE `1`.
- Q2 Do you hold reading D1 for the "no other byte" clauses? Default yes; if not, leave 430, 431, 432 out of MOVE (and 433).
- Q3 CREATE `NONE` (default) or `1`.
- Q4 Keep "graded Minor" for the review's finding in the 431 comment? Default yes (the VERDICT grades it Minor, R16).
- Q5 The entry and comments say the plant-message gap is "the coordinator's own choice before the build" (Stamp S5 of the builder kit). Default as written.

## UNMEASURED / not done
- No `gitleaks` run, no test run, no `dotnet`/`npm`, nothing from the extracted tarball executed. The 9449 counts, the five sampled locations, "generated fixture identifiers", the planted-run figures (34 to 2, 5/7/12/1/1, seven plants, 31 labels) are RELAYED or DERIVED from VERDICT, FOR-RECORDS and the builder STATUS, not re-run.
- Whether any scan of main's history exists beyond the builder's local run is measured only as: no scan-named path in the tree (0) and 0 lines of ci.yml naming it.
- The seat's checks (REFUSE items, E-move, the helpers, the dry run, the fake transport, the lock) were never run on a real output (they are the seat's work); a failure the seat can trace to the kit's own wording is a `STOPPED: NEEDS TUESDAY` question, not the seat's to amend. The kit's `<<CHECKS>>` parse of the log was prototyped by my group parser (15 of 15) only.
- Hosted site state (debb5e28) is relayed from C-188; ticket `updated` stamps not re-checked at the end.
- 84-odd sidecar lines are counts over the kit's instruction text, not source measurements.

## Outside the fences
Extracted the GET tarball of main into scratch (820 entries, 734 files, nothing skipped, no script run from inside, `-I` for every python); ran `lsof` as a count and `tmux list-panes`; Jira reads by my own scratch reader (credentials by name in-process, never printed); `gh api -X GET` only under the project GH_CONFIG_DIR; `stat` on the three stray files (no write). Hook advisories received (case-sensitive grep, `cut`, pipe rc), not blocks. No write to any project, Jira, GitHub, mail or Artifact; no deletion; no `cd`. HPSM-POC and every other client untouched.
