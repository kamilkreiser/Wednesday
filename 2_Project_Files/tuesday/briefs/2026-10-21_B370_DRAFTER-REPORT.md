# B370 DRAFTER REPORT (Sonnet drafter, row C8) for brief `2026-10-21_B370_SEAT-R15_hpsmpoc-records-deploy-6818896.md`

Drafted 2026-10-21 ~05:2x AEDT (`date` printed 05:23:57 AEDT). Marks: MEASURED = I ran it and saw the output; RELAYED = read from a file at path:line; UNMEASURED = nobody ran it. Fences kept: two files written; `gh api` GET only under the project's `GH_CONFIG_DIR` (the project's gh account, `gh auth status` MEASURED); `git --no-optional-locks ls-remote` only; no Jira, no az, no HTTP to any app host, no mail/Artifact/Docs/tmux, no `cd`. Not opened: `HP Reporting and Docs/`, `HP Docs/`, `.local/`, `Source_Documents/`, `.env`, any `.tools/b*` file (I listed `.tools/` names only), `briefs_staged/`.

## 1. What I read (whole)
B366 STATUS (342 lines) and brief (128 lines); B346 brief (110 lines, the C-124 route); B363 brief (121 lines) and B363 STATUS (154 lines, the newest route and its slips); B366 drafter report (63 lines). Records `CLARIFICATIONS.md` on main by `gh api` raw (1,986 lines): C-124 `:1892-1910` and C-127 `:1960-1986` whole; `history.md:1-14`. Parts: B367 STATUS head and verdict (the PR #166 gate, NO GO on -294, merge HELD for B366), B369 drafter report `:1-40` (the D10 partition facts), B366 evidence folder listing (`runtime-post.txt`, `runtime-final.txt` exist).

## 2. Facts (each with where)
- **Deploy outcome:** `DEPLOYED: 6818896 @ 3cBXgbJ5OOq2IZ-rmpNUZ` (`B366_STATUS.md:342`), 342 lines (MEASURED `wc -l`), sha256 `c7cac0f1c14c0f33a9f408a014b339c1a67e311e16ab58855454dc18b4e2393e` (MEASURED). Brief copy sha256 `70647c43…c7560f` equal in Tuesday's tree and the project copy (MEASURED `shasum`), = `B366_STATUS.md:13`. Live since 2026-10-20T17:58:03Z (`:1`, `:201`), 04:58 AEDT on the 21st (`:42`). One attempt, no rollback (`:2`).
- **Code main** `6818896b68090777c8edbf0e694741928c96ca3f` (MEASURED `ls-remote` ~05:2x). PR #166's branch `b364/feedback-pkcs-test-gaps-294-295` and `refs/pull/166/head` are both `4794bde3ac1fc7e0025146e37c11dfa6bd63db90` (MEASURED); not merged.
- **Records main** `e2a0d72193dd11f98a6d582cd06fb7fdffecac5e` (MEASURED `gh api commits/main`), 1,986 lines; headings C-124 `:1892`, C-125 `:1911`, C-126 `:1942`, C-127 `:1960` (MEASURED `grep -n`); no heading above C-127. `records/b370` absent: `matching-refs/heads/records/b370` length 0 (MEASURED). I did NOT scan other refs for a C-128 heading, so "C-128 is next" is main-only (UNMEASURED against all refs; the seat's C-SCAN closes it).
- **C-127's "Not deployed" bullet** is at `CLARIFICATIONS.md:1982` (MEASURED `grep -n`). Its content: hosted runs `c149a30`; it "does not supersede or edit C-124's deploy block" (read whole).
- **C-124 precedent:** "deployed" comments 39798-39806 (HPSMPOC-290, -267, -293, -275, -263, -298, -299, -300, and -268 as the runtime reading), transition 41 on -298/-299/-300 with R-R10-1 quoted verbatim (`CLARIFICATIONS.md:1903` area, read whole). HPSMPOC-303 = FOUND-3 (T-A), HPSMPOC-304 = cleanup (T-B), created by B346 (`B346_STATUS.md:26`, `:174`).
- **Mention hits for the C-SCAN pattern** `C-(12[8-9]|130)` on records main: exactly two lines, `:1907` (C-124's numbering sentence, token `C-129`) and `:1984` (C-127's numbering sentence, tokens `C-128`, `C-129`) (MEASURED `grep -n`). The brief tells the seat to expect them (B363 FOUND 1 met the first one).
- **B363 state:** its STATUS ends `RECORDS COMMITTED: caef2882f8126fc8bac0080aae63812544501a74 · 1 C-entries, 1 tickets, 2 comments, 0 Done`; comments 39842 (-301) and 39843 (-302); -301 had 39834 and 39842; -302 had 39835 and 39843; both `Backlog`; HPSMPOC-305 created; transitions listed 11/21/31/41 at B363's read (`B363_STATUS.md:59-63`). Records main `Briefs/` already holds B363's two files, none of B366/B370 (MEASURED `contents` listing).
- **B366 owed records** (`B366_STATUS.md:333-338`): C-128 free, supersession of C-127's bullet, Jira "deployed" lines, HPSMPOC-268 reading (10.0.12, Done-when NOT met), FOUND-3 non-recurrence against HPSMPOC-303. All five are in the brief.
- **HPSMPOC-268 log:** `2026-10-20T17:58:03.6574351Z Site is running with patch version DOTNETCORE-10.0.12` (`:238`); lines naming 10.0.13 or later 0, control 3 patch-version lines (`:239`); ten API starts since the 10.0.13 image appeared (`:312`). So the Done-when sentence is NOT written and Jira gets no 268 comment (your task's rule); the brief puts a record line in C-128 and STOPs if the seat's own read of `runtime-post.txt`/`runtime-final.txt` finds 10.0.13+.
- **FOUND-3 non-recurrence:** app log 17:53:52–17:58:30Z, 73 lines, `fail:` 0, `FeedbackDispatch` 0, "not a valid Type token" 0; control over B316's switch window gives 5 and 5 (`:221-223`); new process `fail:` 0 (`:8`, `:216`); `HpsmPoc.Modules.Feedback.dll` differs by commit stamp only (`:225`).
- **Partition:** B369's drafter report names the D10 seat's files: `Hpsmpoc290Tests.cs`, `PkcsInPackageTests.cs`, `.tools/b369/`, `.tools/wt-b369-*`, Jira on -294/-295 (your task says the same). `.tools/` listing (MEASURED `ls`) holds `b363 b364 b366 b367 b369` and `wt-b363 wt-b364-* wt-b367-*`; no `b370`, no `wt-b370`.
- **Newer-deploy check, drafter side:** B366 is the newest STATUS ending `DEPLOYED:` that I saw (the `Briefs/` listing shows B367 STATUS, a gate, ending `VERDICT:`; MEASURED `tail`). I did not run the full `grep -l` (UNMEASURED; the seat does with controls).

## 3. Choices I made that you may want changed
- **Comment bodies are drafted in the brief, byte for byte** (three code blocks), because row C7 says Sonnet posts only approved bytes. Stamping approves them. They carry no C-number (so a shifted C-number cannot change approved bytes), no backtick, no "Tuesday", no person's name. Source cites are B366 STATUS line numbers I checked against the file (MEASURED `sed -n`): `:1 :2 :3 :8-9 :42 :44 :220-225 :291 :342`.
- **HPSMPOC-302 gets a "deployed" comment and Done** as your task says, but its comment states plainly that the change is test rows only and no code of the ticket is in the packages (`B366_STATUS.md:44`, `:291`, `:331`). This is the one place R-R10-1's "deployed" is read as "the main that holds the PR is deployed" (see Q1).
- **No ticket, no 268 comment, no 305 touch:** 0 creates. Last line expectation `1 C-entries, 0 tickets, 3 comments, 2 Done`.
- **Two history entries** (this seat and B366, B363's two-entry shape), not one; 4 catch-up paths (B366 brief + STATUS, this brief + STATUS). B364/B367/B369 are left to PR #166's records seat.
- **Order inside the seat:** C-SCAN and all texts built first, then comments, then transitions, so a STOP on numbering cannot leave Jira half-done.
- **A moved code main is not a STOP** (hosted state is the fact; PR #166 may land), unlike B363. A newer `DEPLOYED:`/`ROLLED BACK` STATUS is a STOP.
- Helpers are copied from `.tools/b363/` (falling back to `.tools/b346/`), as B363 copied from B346; this opens a finished seat's helper files only, named in the brief. Existence is UNMEASURED beyond the directory listing.
- I avoided every person's name (the product owner's first name appears only as "the product owner's first name"); the STANDING HOLD is quoted verbatim as B363 carries it (`B363 brief :91`), minus nothing.

## 4. UNMEASURED, with the instrument that would close each
| Item | Instrument |
|---|---|
| C-128 free on every ref | seat's C-SCAN (383 refs at B363's run) |
| -301/-302 still `Backlog`, their live Done-whens, transition id for "Done" (41 expected) | seat's GETs (`GET …/transitions`) |
| -303's status, comment count, any earlier "deployed" text | seat's GET |
| Whether any `Briefs/*_STATUS.md` newer than B366 ends `DEPLOYED:`/`ROLLED BACK` | seat's `grep -l` with B316/B366 controls |
| The platform log lines in `runtime-post.txt`/`runtime-final.txt` byte-equal to `:238` | seat, by program |
| Whether `records/b370`-style PR #166 records land before this one (C-number race) | Tuesday's order of launches; the seat's C-SCAN |
| Helpers in `.tools/b363/` | seat's `ls` |

## 5. Questions for Tuesday (numbered; recommended answer first)
1. **HPSMPOC-302 is test-only: move it to Done on a "deployed" basis?** Recommend **yes** (your task says both; R-R10-1 says Done = merged, gated, deployed, and the main that holds the rows is deployed; the comment says plainly that no code of the ticket is in the packages). Alternative: comment only and leave Backlog, which would contradict B366 `:330-332`'s "records step's precondition is met".
2. **Comment bytes:** do you approve the three bodies as drafted (stamping approves them)? In particular "Closing to Done under the coordinator's rule R-R10-1" is posted before the transition: recommend keep, since the seat does comment, then transition, then read back.
3. **Two history entries or one?** Recommend two (this seat + B366) as B363 did; say "one" and the seat drops the B366 entry.
4. **Launch order vs PR #166 records (B364/B367/B369):** recommend land B370's PR first or at least launch B370 first, so the next records seat's C-SCAN sees `records/b370` and takes C-129. If PR #166's records seat runs first, B370's NEXT_C slot is wrong: re-read it at stamp.
5. **NEXT_C stamp value:** default `C-128` (main-only measurement; the seat re-derives anyway).
6. **MODEL_LINE:** default `Sonnet (BRIEF_SEAT_LEVEL=sonnet; rows C7/C8); STATUS quotes the brief_seat: model= line or says it was not visible` (B363's three seats could not see it). Model id from `models_latest.json`, not typed.
7. **HPSMPOC-268:** the brief writes no Jira comment (your rule: Done-when sentence only on 10.0.13+). C-124 did post one (39806). Recommend keep it comment-free here: the reading is unchanged and already tracked.

## 6. Slots and self-check
`/usr/bin/grep -c -E '@SLOT:[A-Z0-9_]+''@'` on the brief prints 1 (one Stamp line holding six tokens: STAMP_TIME, B_NUMBER_CONFIRM, MODEL_LINE, CODE_MAIN_PIN, RECORDS_BASE_PIN, NEXT_C; MEASURED). No `.pre-stamp` created (two-file fence): Tuesday copies it before stamping; the brief accepts a scratch-file control otherwise. The brief's sha in the title of B366 is not repeated as a slot. The word for the product owner's first name occurs 0 times in the brief (MEASURED `grep -c -i`). Last line `READ-WHOLE-BY-TUESDAY: PENDING`.
