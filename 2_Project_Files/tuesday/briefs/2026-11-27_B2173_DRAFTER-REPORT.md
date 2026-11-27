STARTABLE: YES

# B2173 DRAFTER REPORT: re-freeze of the OXPd records kit (seat R342; supersedes B2161, which superseded B2146)

I was the in-session, read-only drafter for Tuesday s335. `date` printed my first clock as `Fri 27 Nov 2026 20:50:53 AEDT`. My last check before this report printed `21:12:11`. No Stamp slot holds a typed clock.

**Precondition for YES.** At 21:12:09 the board's newest OXPd row was still 18:31:56. `main` was still 760e1a64, with 0 open pull requests. The three record files still matched B2140's manifest.

The kit stops by itself if any of these changes before the stamp:
- **A new row from him:** for example a tap on the open licence-steps card or the open mock-environment spend card. Slot RULINGS-NEW and REFUSE 6 stop it, and the kit is re-drafted.
- **A new landing:** if X89's pull request merges, P-L stops it.
- **A new CLARIFICATIONS entry:** P-7 and REFUSE 6 stop it.

## Files written (nothing else outside my scratch)
- **The kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2173_SEAT-R342_oxpd2-records-pr58-and-1127-rulings-r2.md`
  - sha256 `63ce30d3...`; 200950 bytes; 733 lines; 0 bytes above 126.
  - 11 underscore slot lines.
  - Line 1 says it SUPERSEDES B2161, which itself superseded B2146.
- **Sidecar:** `.measured` beside the kit, sha256 `41e1525f...`.
  - 169 claims, 0 TODO.
  - `stamp_check.py <kit>` exits rc 0.
- **This report.**
- **Scratch:** only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s335/d2173/`.
- **How the kit was built:** it is generated, as B2161's was. `edit.py` applies `new.md` to B2161's kit source (copied unchanged from s334/d2161), then `dry.py`, `quotes.py` and `fillkit.py` run, and `side.py` writes the sidecar.
- **Disclosure:** the kit and the sidecar were put in place by `cp`, not with the Write tool, because of their size (200 KB). The copies are `cmp`-equal to the generated files, and both target paths are my permitted outputs.

## BLUF of the kit
Everything B2161 does is kept, unchanged where nothing moved:
- the landing of pull request 58;
- ticks on owed items 54, 55 and 75;
- new owed items 161 and 162;
- C-93 to C-99.

Added or changed:
- **C-100, his live-board rows of 18:10 to 18:21:**
  - **Second factor:** tap a, "Agents do it via our own admin app".
  - **18:11 licence approval:** quoted.
  - **18:13:30 printer-path brief:** quoted.
  - **18:13:40 phone question:** quoted.
  - **18:15:39 Fleet Activity remark:** quoted.
  - **Status card:** tapped "Noted".
  - **"thanks":** quoted.
  - **18:18:56 and 18:21:22 sign-in/billing messages:** recorded as holding no decision. They are not quoted and their attachments are not recorded. No account name, temporary credential or secret appears anywhere.
- **C-101, his rows of 18:30 to 18:31:**
  - **P-4 confirm:** a, the first phase's server runs in the client's Azure.
  - **Printer path:** a, "Connector, VPN as an equal option".
  - **18:31:56:** "going to dinner now.  I will buy the license tomorrow".
- **Readings rewritten where his later rows made them false:**
  - C-96: the licence is his purchase, approved by him.
  - C-97: the tenant pieces were made by agents; the licence; two tickets.
  - C-99: P-4 as confirmed at 18:30, and the connector setting the lab path.
  - C-93's range is now C-94 to C-101.
- **X85's findings:**
  - BL-EV-103: one evidence line under owed item 103. The CA store accepted a self-signed development root and gave it back; trust of a server signed by it is UNMEASURED. Item 103 is not ticked.
  - Owed item 163: the lab's `oxpd1 echo` opens the credentials file twice. Six new pointers were re-read in the tree: `Oxpd1EchoVerb.cs:288/:296/:304`, `LabFiles.cs:57/:34` and `README.md:319`.
  - Owed item 118 gets no line (Q16).
  - No X88 result is recorded. P-9 and the PARTITION forbid reading X88's STATUS for a record line.
- **Jira: four POSTs, down from five.** T-K2 is DROPPED: his tapped second-factor card says agents made the app registration, the attribute set and the test user.
  - T-K3: the card reader, due 2026-12-07.
  - T-D2: the licence, due 2026-12-07. Its description quotes his 18:11 approval and his 18:31 "tomorrow".
  - J-61 on OXPD2-61: the test user was made by an agent, the second factor is a code generator so no phone is needed, and a browser step is still owed.
  - J-1 on OXPD2-1: now also carries the device-run paragraph and the first-phase Azure and connector path.
- **Neighbours:** the kit says a records seat may run beside build seat X89 (B2170) and device seat X88 (B2171). It writes only project record files outside the repository, never their lanes. Both partitions are stated from both sides, and X89's kit partition (c) already names this records pass.
- **REFUSE 6** now also stops on any CLARIFICATIONS entry added after my read (92 headings, C-92 last at line 1230, sha256 `04f77946`). It also stops if slot RULINGS-NEW is not `no OXPd row of his newer than 2026-11-27 18:31:56`.
- **Seat:** R342 was free:
  - it appears in 0 of the 45 SEAT kits of 11-26/27 and in no file name;
  - controls: R341 on 3, R340 on 2;
  - only this commission and plan B2174 name it, both as this records pass.

## Facts re-measured (instruments, clocks)
- **Project files (shasum, 20:52:52, again 21:12:11):** all nine files equal B2140's manifest. B2161's frozen facts still hold:
  - CLARIFICATIONS `04f77946`, 1236 line feeds, C-92 last at line 1230;
  - BACKLOG `74800003`, 1212 line feeds, owed 1 to 160 (89 open, 71 ticked);
  - history `85b66031`, 410 line feeds.
- **Item positions at drafting:** item 103 at lines 761 to 767, item 118 at 877, the anchor at 1197.
- **GitHub (GET only, gh auth kamilDatasec, 20:54:50):**
  - main 760e1a64; pull requests 59 and issue 59 both 404; 0 open; 60 heads;
  - refs b2161, b2173, b2153, b2170 and b2171 have 0 rows (control: b2138 has 1);
  - tarball sha256 equals B2161's, 679 files;
  - pointers 62 of 62, with the control FIRED (21:01:03).
- **Logs and hosted run:**
  - the pull request run's logs `diff`-equal to B2161's (21:00:14);
  - hosted3 PASS at 21:00:21, control FAIL 4 at 21:00:31;
  - the 0ca8c655 push log has `total: 2429` 2 times and `total: 2431` 0 times (21:02:01);
  - `facts2.py` (blobs, message, VERDICT and FOR-RECORDS literals) equal (21:00:45).
- **Jira (GET-only fence fired on POST, PUT, DELETE and PATCH; from 20:56:20):**
  - census 63, unchanged; `oxpd-kamil-action` is OXPD2-56 to 61 and 63;
  - OXPD2-61 has 0 comments and Backlog status;
  - OXPD2-1 has 19 comments, the newest 41547, and 0 starting "Records pass after pull request 58";
  - new phrases (`Business Premium`, `code generator`, `second factor`, `credentials file twice`, `oxpd1 echo`, `self-signed`, `site connector`, `Azure Marketplace`) each find 0 issues; `named pipe` finds OXPD2-1 only.
- **Board:**
  - `kam_rulings_today.sh` (marker in my scratch) at 20:51:35 and 21:12:09: 26 rows, the newest 18:31:56, TAPPED-BUT-OPEN none.
  - `kam_msgs.sh 24` at 20:59:36: the 24 rows from 17:39:03 were saved. `passw` appears 0 times. B2161's rows file is a byte prefix of the saved file.
- **Cards:** `decision_queue.sh show` for 18 named Datasec ids at 20:52:15. The 11 B2161 printed are `cmp`-equal to its prints. 15 are SOURCES rows.
  - Open: licence steps, mock-environment spend, and the parallel-builds decision. None is a Kam ruling.
- **P-W:** QUOTES 125, BAD 0 over the written kit, each control 0.
- **P-9 (X85 STATUS, sha256 `949b9c4a`, 182 line feeds, 20:59:54):**
  - last line starts `STOPPED: NEEDS TUESDAY E01 hung`;
  - `ImportCaCertificate: Answered 200 applied Yes` 3, `RemoveCaCertificate: Answered 200 applied Yes` 2;
  - the remaining literals are as printed in the kit.
- **Dry build** (scratch only; `scan_record` 0 problems over 163 filled lines; doubled-word checks 0):
  - CLARIFICATIONS: 1236 to 1496 line feeds, C-93 to C-101;
  - BACKLOG: 1212 to 1237 line feeds, 25 lines added, 3 changed; owed 1 to 163, 89 open and 74 ticked; Evidence lines 2 to 3;
  - history: 410 to 419 line feeds;
  - Jira codes: T-K3 and T-D2 S-DQUOTE S-NAME; J-61 S-DQUOTE; J-1 none.
- **Pickup OXPd block (lines 12 to 22):** every terminal quote B2161 carries is still found there by P-W. I found no terminal word of his in that block that B2161 lacks.

## Chain inputs (MEASURED LITERALS rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | kit and sidecar, the project files | at BASE |
| 1 | the `b1785.py` copy | Step 0 |
| 2 | X85 STATUS, review files, tarball (re-GET), Jira | at BASE / origin |
| 3 | frozen texts, P-7 count, before-copies | kit / Step 2 / Step 0 |
| 4a–4d | dry texts, keys and comment ids from 4c's log, BL sha8 from 4b | Steps 3 and 4 |

## D-decisions
- **D1:** T-K2 is dropped. Agents made those pieces (his tapped card), so a ticket asking him for them would be false.
- **D2:** C-97's and C-99's taps stay verbatim. Only their readings are re-worded, and the entries say so.
- **D3:** the clock `18:18:56` trips the doubled-word check (`18 18`). It is a named exception, masked in `dry.py` the same way B2161 masked C-99.
- **D4:** X85's STATUS is SOURCES row 50. A difference HOLDS (it does not just get named). X88's STATUS is never a source.
- **D5:** I did not include the open licence-steps card's print as a source, because its text names a billing account. C-101 says only that it is open.

## Q-questions for Tuesday (defaults as written in the kit)
- Q1–Q14 are as in B2161, re-worded for the counts (Q9 now has eight entries; Q10 now has two tickets). Default: as written.
- **Q15:** 103 gets an evidence line, not a tick or a `Closed in part` line, plus new item 163. Default: as written.
- **Q16:** no line under 118. Default: as written.
- **Q17:** the billing and sign-in messages are not quoted. Default: as written.
- **Q18:** the Fleet Activity remark is recorded, read as a reporting rule. Default: as written.
- **Q19:** the licence ticket stays due 2026-12-07, not 11-28. Default: as written.

## UNMEASURED / NEVER RUN
- The seat's helper, HOLD R/R2, the live writes, and the four POSTs.
- Whether the code generator has been registered (relayed as owed).
- The licence price.

## Outside the fences (disclosure)
- **Board reads:** `kam_rulings_today.sh` with its marker in my scratch, and `kam_msgs.sh 16` and `24`.
  - The raw prints were moved to `d2173/_quarantine/`. I deleted nothing.
  - No credential appeared (`passw` 0); the one header-only block was not a row.
- **Cards:** `show` for named Datasec ids only, never `list`.
- **Coordinator files:** the pickup's first lines and DELTA 1540 to 1547, by line range. Tonight's kits B2170 and B2171 at their partition lines only. B2161's kit was read whole; its 18 lines over 2000 characters were regenerated from source rather than read through the Read tool.
- **Not touched:** no write to the project, Jira, GitHub, cards or mail; no `cd`.
