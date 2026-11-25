STARTABLE: YES

# B2086 drafter report (read-only kit drafter, Sonnet 5.5; kit `2026-11-25_B2086_SEAT-R323_nexusai-records-four-landings.md`)

## BLUF
- Kit written (140417 bytes, 225 lines, ASCII, 13 `____` slot lines: 12 slots + the last line), sidecar `.measured` written (191 claims, `stamp_check.py <kit>` rc 0: 191 measured, 0 not measured), seat id `SEAT-R323` (free: `grep -c -w R323` over 208 SEAT kits read 0; control R322 read 2), model SONNET, pane `Datasec/NexusAI-R323`.
- One caveat Tuesday should weigh at the stamp: **pull request 255's Build workflow run (45540342215, check-run 138957053712) read `in_progress` at 14:52:24 AEDT** (merged 14:29:34). Everything else (the other 4 runs and 7 of 8 check-runs of its merge commit, all of 252, 253 and 254) is concluded. The kit handles it by construction (EVIDENCE poll, the three texts carrying `<<HOSTED255>>` HOLD until `success`), so launching now is safe; launching after the Build concludes is cleaner (Q-8).
- Work in the kit: 1 create (one Low Bug: GET /api/setup/status, dup-checked), 6 comments (RD-1017, RD-975, RD-577, RD-1040, RD-1039, RD-1014) and up to 5 moves to Testing (RD-1017, RD-975, RD-1040, RD-1039 by slot MOVE-LANDED; RD-577 by slot MOVE-577, default NONE), one section 113 with five entries C-327 to C-331 (the ruling; PR 253; PR 254; PR 255; PR 252), one history entry on `records/b2086-history` (Tuesday lands the PR, merge commit, C-190).
- PR 252 (commission item 4) confirmed: merged 2026-11-25 07:16:56 AEDT as `4d8713e5`, HISTORY.md only (+21/-0), 6 check-runs all success, Build log 6323/6323 across 398 suites, no Deploy demo run (control: 253 has one). It needs no Jira or ticket; the records do not yet hold it (0 lines), so the kit records it as a three-line entry C-331 (Q-2).

## Facts re-measured (instrument; every number is also in the kit and its `.measured` sidecar)
- `gh api -X GET` (facts.py, `fleet/state/s326/d2086/facts.out`): main `a3f72428241c3e41799f5c11c16b7447fdf521c4`, 0 open PRs, `compare a3f72428...main` identical; merge commits 4d8713e5 (252), 40df8493 (253), b1c2f76e (254), a3f72428 (255) with parents, trees, files and commits (landings.txt). Merge tree = head tree for 252, 254, 255; **NOT for 253** (head was behind main by 2): the kit says so and the move check uses `compare 4d8713e5...40df8493`, which lists exactly the head's 4 paths (+319/-4).
- Build logs (job ids 138747293923, 138806085739, 138894482555): 6323/398, 6341/400, 6362/401, `VERDICT: PASS` 1 and `VERDICT: FAIL` 0 each. Counts file at a3f72428: 6429/403. Deploy demo runs of 253, 254, 255: completed skipped, both jobs skipped; Actions variables total_count 0.
- Code scanning on main (paged): 22 open (same 22 numbers), 222 fixed, 7 dismissed; 0 created and 0 fixed since 2026-11-22T13:00Z; 13 at `backend/server.js` (control), 0 in the page scripts or the adapter. Because 253 and 254 edit `backend/server.js`, the texts say so and claim no alert changed.
- Jira GET (jr.py): all six comment keys To Do (RD-577 with 2 comments, RD-1014 with 1, the others 0), transition id 31 targets Testing on each, 1036 issues, highest RD-1040, `RD-99999999` 404, label records-pass-1125 holds 1 (RD-1040), records-pass-1124 holds 4, the seven markers read 0, controls DSWIRE-251-25NOV and HARDEN-248-24NOV read 1 each. RD-518 is Release Ready.
- Records: CLARIFICATIONS.md 954114 bytes, 3256 lines, sha256 prefix 76bcd9865efaa8d9, highest section 112, highest entry C-326, 1361 non-ASCII bytes; simulated append: heading 3258, C-327 at 3260, C-328 3264, C-329 3270, C-330 3276, C-331 3282, file ends 3284. HISTORY.md at a3f72428: 10448 lines, 1142290 bytes, sha256 prefix dac4ced8742114a1, 7563 non-ASCII bytes, last heading 10429; simulated append: new heading 10450, file 10471 lines, added bytes ASCII. History identity: author and committer of 96831e51 both hash to be76c2c1baf03ec1, domain users.noreply.github.com.
- RD-577 (re-checked at source as commissioned): fixed on main. `keyVaultStatus` at server.js 18607 reads the encryption state (not_configured / configured / configured_but_inactive); comment at 18602 to 18606 names RD-577 and RD-518; the RD-518 merge `aae041a` diff removes the old `process.env.KEY_VAULT_NAME ? ...` line; the two other reads (769 AzureADManager, 797 marketplace API) are deliberate. RD-518 reads Release Ready.
- Dup-check of the setup/status sibling (dupcheck.py, `dupcheck.out`): 4 phrase searches over all pages, union 113 keys (control RD-706 in the union), each read whole; 14 hold the path; 0 hold a signed-in, viewer or role reader of tenant, client or workspace ids within 600 characters (planted-text control fires). RD-706 (Done) is the anonymous open-window case, closed as intended under the product owner's 2026-09-27 ruling (option b, comment 38319); the kit cites that ruling only as context. Source: `GET /api/setup/status` (server.js 14611) has no check; its neighbour `/api/setup/managed-identity` (14709) opens with `requireAdminFor` (14712); the table lists the route under config.read (capabilities.js 160). Consumers: first-run-setup.js 1155 and 4659, index.js 277 and 1008, settings.js 2945, setup.js 12.
- The 27 unlisted rows: python over the two raw files at a3f72428: all 27 present and raw; the 10 fixed rows hold `escapeHtml(`. (Row index.js 3044 is a downloaded text file, not HTML: the comment says so.)
- Product owner's ruling: `decision_queue.sh show` of the exact id (inclusion filter) prints option [a] "Ticket it and fix", ruled 2026-11-25T06:57:58+11:00; `kam_rulings_today.sh` (read marker pointed at scratch) prints the board message "a - Ticket it and fix"; the 2026-09-27 card prints option b ruled. No card id appears in any kit text (grep 0).

## Instruments for the texts
- Scanner: `fleet/state/s326/d2086/scan1947.py`, sha256 prefix 3707dc37c4795fbf, byte-equal to `.tools/b2055/scan1947.py`'s copy used by the previous drafter (selftest 67 ok, 0 FAIL). `scan2086.py` over 61 texts (25 Jira, 22 entry, 14 history) alone, with sample fill-ins and with HELD fill-ins: 0 problems after fixes (first run: 9 problems, all re-worded: doubled parentheses, `deployed`, `gate`, decimals, a repeated 7-word run between HELD clauses). Controls fire (Tuesday, _by_Kam_, secret, B2086, R323, card shape, doubled paren, repeated run). This is the project's scanner copy (the file the seat will use), not a drafter list.
- Pointers: `pointers2086.py`, 53 rows, fail 0, controls fire (`loadViewerDataSources` absent; SETTINGS_CHANGE on 3 lines).
- Marker/phrase form of every JQL: `project = RD AND ( ... )`.

## Model row
`fleet/specs/model-routing.md` line 97 (C7, client-board comments: Sonnet posts a body the coordinator approved byte for byte; Opus drafts security-finding comments; these texts are the approved bodies), line 98 (C8), line 110 (G3); `models_latest.json` line 23 `claude-sonnet-5-5`; `brief_seat.sh` line 31 defaults to Opus, so the launch line carries `BRIEF_SEAT_LEVEL=sonnet`. The previous NexusAI records kit B2073 ran Sonnet (its model line).

## Chain inputs (each produced by an earlier step or present at BASE)
| Step | Inputs | Source |
|---|---|---|
| 0 | kit file, scanner copy, `date +%m%d` | BASE (kit copy `cp -n`; `.tools/b2055/scan1947.py` exists) |
| 1 | the text bank in the kit, `.env` by name, CLARIFICATIONS.md, scanner | BASE + Step 0 |
| 2 | local repo config reads, one-command transport key `3_Access_Keys/github_deploy_rw` | BASE |
| 3 | GitHub GETs, Jira GETs, Step 1 helpers, Step 2 identity prefix | BASE + steps 1, 2 |
| 4 | Step 3 facts, text bank, fill-ins, placeholder keys | steps 1, 3 |
| 5 | Step 4 payloads, the created key (5a read-back) for the RD-1040 text, each comment's read-back for its move | steps 3, 4, 5a |
| 6 | Step 5 comment ids, created key and moves (PER clauses), Step 3 facts, before-copy | steps 3, 5 |
| 7 | `entry-numbers.txt` from Step 6, Step 5 clauses, Step 2 identity | steps 2, 5, 6 |
| 8 | all logs and raw files | steps 0-7 |

## D-decisions (drafter, each the coordinator's to change)
- D-1 Texts are frozen with hosted facts in fill-in clauses (`<<HOSTED253..255>>`, `<<SCANMAIN>>`, `<<PUSHRUNS*>>`), as the previous kit did, so a seat cannot post a stale figure; the 255 clause HOLDS while its Build runs.
- D-2 RD-1040's comment states two items of that ticket's own proposed acceptance are NOT met by the change by choice (the dashboard's region filter for excluded roles; the inventory not regenerated), and the owed stale header and inventory text; no ticket for them (the commission allows one).
- D-3 RD-975's comment records the review's two minor limits and the zone dependence, and names RD-974 without writing it; RD-974's partition note (rd798 cells C-BODY-HOURS LIVE, IN 190, OUT 190) is in C-328 only (those cell names verified in the file at main).
- D-4 Marker rule written into Folded in (B2073's Deviation 3 would otherwise recur), plus the other B2073 deviations (group file-name table, tuple/list compare, empty fill-in, absolute worktree path, CLAUDE.md line numbers by content).
- D-5 RD-1014 gets a comment-only note listing the 27 rows (the kit's phrase for commission item 3); no move, no label.
- D-6 The product owner's ruling is cited only by the option label and the option text as the store prints them; nothing says he approved fields, defaults or the audit tag (HOLD 2).

## Questions for Tuesday (each with a default)
- Q-1 Model: Sonnet (as B2073). Default: Sonnet.
- Q-2 PR 252: commission says "needs nothing new: confirm". Confirmed (above). Default: keep the three-line entry C-331 (like C-326 for PR 250) so the records hold it; drop it by deleting `E-C5-*` and the C5 references if you read "nothing new" as "write nothing".
- Q-3 New ticket: Bug, priority Low, labels records-pass-1125 + security (commission says Low; RD-706, the anonymous sibling, was Bug Low). Default: as written.
- Q-4 RD-577: comment now, move to Testing only if you stamp MOVE-577 `577`. Default: NONE (comment only), because the readout was verified at source on main, not on a running server (RD-518's own comment 38191 says it was not yet measured as a signed-in administrator).
- Q-5 Move the four landed tickets to Testing (project rule line 302). Default: MOVE-LANDED `YES`; RD-1039 moves only after its Build concludes success.
- Q-6 The stale `capabilities.js` header and the stale `docs/role-capabilities.json` text are owed record lines, not tickets (commission: at most one ticket). Default: not ticketed.
- Q-7 RD-974: named in C-328 and in the RD-975 comment, never written. Default: no comment on RD-974.
- Q-8 Launch while PR 255's Build is in progress. Default: launch now (STAMP the slots as usual); the EVIDENCE poll (25 minutes) and HOLD of the three 255 texts cover it. Alternative: stamp after the Build concludes and the kit is unchanged.

## UNMEASURED
- Build result of PR 255's merge commit (in_progress); the 6429/403 figures are the counts file and the review's own verify (RELAYED).
- Any running server, hosted instance or browser; the field content of GET /api/setup/status (source reading; the review's probe seeded data sources only); whether the new ticket's search guard behaves on a real run (never run: stated in HOLDS 3).
- The seat's append, ADF, post, history and EVIDENCE helpers have never run on a real output (stated in the kit); I ran the scan, the pointers, the repeated-text and doubled-parenthesis checks, the simulated appends and the dup-check on prototype output (each STOP-severity check fired its control).
- Kit load: kit 140 kB + reading list about 215 kB = about 355 kB against the 400 kB Sonnet budget: tight; the kit tells the seat to read the three build STATUS files by READY and NOT TESTED only if it nears the budget.

## Outside-the-fences disclosure
- Read-only throughout. Wrote only the three briefs files (kit, `.measured`, this report) and scratch under `fleet/state/s326/d2086/` (nothing deleted).
- Ran `decision_queue.sh show` for exactly two ids (the ruling card of 2026-11-25 and the 2026-09-27 setup-window card, both named by the commission), and `kam_rulings_today.sh` with `KAM_READ_MARKER` in scratch. No `list`.
- Ran one `git -C <NexusAI 2_Project_Files> ls-remote origin` (a read verb) without the one-command transport: it failed (`Permission denied (publickey)`, the repo's stored sshCommand names an unmounted drive); recorded in the kit as RD-1001's subject. No fetch, no config read of user values.
- One Bash call was refused by the no-delete hook (a stray `rm -f` of a sed backup); nothing in it ran. A few scratch scripts ran as `python3 -B` instead of `-I` because they import the scratch Jira reader; they read only Jira/GitHub GETs.
- Read: the three review folders, the three build seats' STATUS sizes, B2073's STATUS Deviations section, CLARIFICATIONS.md, `CLAUDE.md` lines 273, 302, 303, model-routing rows, raw GitHub files at a3f72428. No staged briefs, scoreboard, ledger, WEDNESDAY or FRIDAY tree, no other client. No message to anyone.
