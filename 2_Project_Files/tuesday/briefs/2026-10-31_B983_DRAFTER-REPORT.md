STARTABLE: B983 SEAT-R96 (HPSM-POC records for PRs #262, #264, #263) is ready to stamp and launch; kit 77 lines, 0 non-ASCII, unstamped count of the four-underscore pattern 12 (eleven slots plus the last line).

Kit: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-31_B983_SEAT-R96_hpsmpoc-records-262-263-264.md (plus the .pre-stamp copy, cmp equal). Nothing changed in any project; nothing sent; no Jira write.

## BLUF
- Seat Datasec/HPSM-POC-R96, Sonnet (claude-sonnet-5-5), records branch records/b983, 6 Jira comments, ONE new ticket (B981-1), 3 C-entries (C-251 #262, C-252 #264, C-253 #263), BACKLOG rows for every untickted gate finding, catch-up copies, Done moves only by the DONE-SLOT.
- Default DONE-SLOT is COMMENT-ONLY. Two things need your ruling: Q-1 (the Done slot) and Q-2 (B969 and B972 HP Restricted lines, held).
- CI on the squashes is NOT settled: 68bf73cd and c364caf0 had runs in progress at 14:19. The kit writes CI as read and makes a completed-success push run a precondition of any move.

## Measured (14:19 AEDT, read-only)
- Code main c364caf0393fa1c581c1d7e5aa48c815ee509d65 (chain 8ce48527 -> 68bf73cd -> c364caf0, one parent each, verification valid, localdomain 0). Open PRs 0 on both repos.
- #262 merged 01:33:57Z (12:33:57 AEDT) head ef4a7e68, 1 path +33 -1. #264 merged 03:08:54Z (14:08:54) head 8222af61, 1 path +15 -2. #263 merged 03:16:30Z (14:16:30) head 53edc92b, 5 paths +120 -11, 4 commits. All test files only.
- CI as read: 8ce48527 19 check-runs 18 success, ci and Push on main completed success. 68bf73cd 17 check-runs (12 success, 4 incomplete), ci in_progress, Push on main success. c364caf0 12 check-runs (5 success, 6 incomplete), ci and Push on main in_progress.
- Records main 3e80c9c4daa23cfe255b53560ab4821b4971ccd7 (unchanged since B972); CLARIFICATIONS 4924 lines, highest C-250 (C-251 0); BACKLOG 2560; history 2594; records/b983 absent (control records/b972 1); 0 open records PRs. Records tree lacks STATUS of B969, B972, B973, B977, B978, B979, B981, B982 (controls B968, B970, B971 present).
- STATUS files (lines / sha256 prefix): B969 132 4b0c52224a8680f1; B972 119 263d87a756af8566; B973 66 001301a5e8a56063; B977 203 d596f94c9475f0b6; B978 133 76b0c0b979605087; B979 112 b03bde682f409940; B981 102 9c7f18e2094d453a; B982 122 66c44bf98d3558c5. Last lines: B973/B978/B979 READY FOR QA, B977/B981/B982 VERDICT, B969/B972 RECORDS COMMITTED. All mtimes older than 10 minutes except B981 (14:16) and B982 (14:07), which the seat re-checks at Step 2.
- Scan (python, controls fired): non-ASCII 0 in all eight; HP Restricted 0 in B973, B977, B978, B979, B981, B982; B969 lines 72, 76, 102; B972 lines 64, 68, 93, 107, 119 (and 2 e-mail-shape lines, 64 and 93: the attribution address and a git clone URL, as B972 reported). localdomain appears only as zero-count statements in the gate files.
- Jira (via .tools/b972 read.py and search.py): HPSMPOC-414, -407, -413, -416, -418, -419 all Backlog (new), 0 comments each; newest key HPSMPOC-421; created since 12:08: 0; controls HPSMPOC-268 1, qxv9k2zzprobe 0. text ~ "QuestionBlock" 3 hits: HPSMPOC-419 (its title names the QuestionBlock id), -375, -343. text ~ "B981-1" 0.
- Panes: %0 tuesday, %1 fleet-monitor, %93 MPS-M52, %98 MPS-G237. No R96, no HPSM-POC pane. Gate files B977, B981, B982 all end VERDICT (FINAL), no live gate pane.
- Sonnet id claude-sonnet-5-5 (models_latest.json).

## The Done precedent, with its lines (records main 3e80c9c4)
- CLARIFICATIONS.md:1904 the rule: Done means merged, gated and deployed (RULED R-R10-1).
- Line 2041 (C-129, 21 Oct): "RULED (drafter Q1): test-only tickets STAY in Backlog with the comment, 0 transitions".
- Lines 3054 (C-177), 3088 (C-178), 3142 (C-179), 3193 (C-180), 3320 (C-186): test-only keys moved to Done at merge by the stamp's RULING-DONE slot, no deploy. Line 3270 (C-183): "For a test-only landing the stamp's RULING-DONE-<key> slot replaces the deploy clause, as in C-177 to C-180." Line 3711: slot DONE plus six checks printed before the move. Lines 3307, 3395, 3466, 3635: NOT-DONE slots left keys in Backlog.
- Reading: no key moves without a stamp ruling, per key, after six checks. Hence default COMMENT-ONLY; MOVE-TEST-ONLY is allowed only for 414, 413, 416, 418, 419 (407 never).

## Q-questions with defaults
- Q-1 DONE-SLOT: COMMENT-ONLY (default) or MOVE-TEST-ONLY? If MOVE, the seat still moves a key only when its six checks pass, including a completed-success push run on the squash (currently in progress for 68bf73cd and c364caf0) and the key's Done-when met by a cited gate line. Note HPSMPOC-419 likely NOT-DONE: its title names the QuestionBlock id and B981-1 says the not-applicable variant of that id is unpinned.
- Q-2 B969 and B972 STATUS: both name HP Restricted as a scan-class name only (B969 lines 72, 76, 102; B972 lines 64, 68, 93, 107, 119). Default: HOLD both, the seat reports the lines verbatim in STATUS, you rule. The kit applies the HOLD to B972 as well; if you want B972 copied, say so at the stamp (the B925 copy with the same class of hit was accepted in B969).
- Q-3 T1 for B981-1: default one ticket, related to HPSMPOC-419, labels b981-found and b983-2026-10-31. The seat SKIPS it if its own search finds a ticket already recording the not-applicable id.
- Q-4 B972 STATUS copy: default per Q-2 (held). It is the only catch-up file whose scan is not clean.
- Q-5 Launch window: default launch now; the seat polls CI up to 15 minutes before any move and writes CI as read otherwise.

## Stamp values (what Tuesday fills)
- STAMP / LAUNCH WINDOW: the clock at launch.
- DONE-SLOT: COMMENT-ONLY (default).
- Heads at launch: records main 3e80c9c4daa23cfe255b53560ab4821b4971ccd7; code main c364caf0393fa1c581c1d7e5aa48c815ee509d65 (re-read at stamp).
- Hard stop: 90 and 180 minutes after the seat's own Step-0 date.
- Launch authority: the product owner's 2026-10-16 merge-once-tested grant (records seats land their own branch).
- Model receipt: model: claude-sonnet-5-5 -- C8 records (C7 for ticket texts and comments) -- ports none.
- GATE-CLEAR: R = {262, 263, 264}; B977, B981, B982 end VERDICT; no live gate pane (as measured 14:19).
- AUTH-RULINGS: none. Sequencing ruling: default STOP at Step 8 if the gate check fails.
- Last line: READ-WHOLE-BY-TUESDAY: DONE <time> ...

## Not done / limits
- Helpers named in the kit were read-listed in .tools/b972 (all 20 present) but not run; the seat copies and re-points them. The kit's LAND text uses the squash and gate facts above; the WHAT sentences are from the gates' squash texts (B977, B981, B982 FOR TUESDAY).
- The B973, B978, B979 builder STATUS files were read in part (header, findings, last line), not whole.
