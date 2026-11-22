STARTABLE: YES - kit B1947 (seat SEAT-R301, NexusAI records pass for pull request 240) is drafted, `stamp_check.py` exits 0 (229 claims, 229 measured, 0 not), every Jira text and the entry scan clean with controls fired; it waits only for Tuesday's stamp (13 slots). The hosted Build of the merge commit was still running at drafting: the kit's Step 3b waits for it and no RD-349 or RD-175 write precedes it.

# B1947 drafter report (Sonnet drafter, 2026-11-23, first read 03:18:39 AEDT, all clocks from `date`)

## Files
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1947_SEAT-R301_nexusai-records-240.md` (135174 bytes, 225 lines, ASCII, 13 four-underscore lines: 12 slots and the last line `READ-WHOLE-BY-TUESDAY: ____`).
- Sidecar: `...SEAT-R301_nexusai-records-240.md.measured` (229 lines; `python3 -I -B stamp_check.py <kit>` printed `229 claims, 229 measured, 0 not measured`, rc 0, run alone). Most lines are automated line counts over the pinned sources (the sidecar's own header says so); 2 lines (date, VERDICT: PASS) are real-instrument overrides.
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s313/d1947/` (raw reads, `texts.py`, `scan1947.py`, `pointers.py`, `captable.py`, `build.py`, `load.py`, `sidecar2.py`, searches).
- Seat id: `SEAT-R301` is free (`ls` of the briefs folder and the project's `Briefs/` folder piped to `/usr/bin/grep -c -i -E 'SEAT-R301'` read 0 before the kit existed; control `SEAT-R288` reads 5; it reads 2 now: the kit and its sidecar).

## THE KIT'S LOAD (by program, `load.py`)
Kit 135174 bytes + READ list 160900 bytes = 296074 bytes (about 296 kB, under 400 kB). READ list: the two VERDICT files whole (23307 and 18685), round 2's landing.txt, pr-body.md, merge-body.txt, pr-title.txt (4513, 5618, 1080, 141), B1911 STATUS lines 1-13 and 119-156 (11304), B1931 STATUS lines 1-12 and 179-207 (7896), B1807 STATUS lines 148-171 (7529), CLAUDE.md 267-281 and 296-310 (4001), JIRA.md 189-236 and 552-575 (3822), CLARIFICATIONS 3136-3154, 2751-2757 and 2067 (21649), HISTORY 10328-10344 (3285), capabilities.js 84-112 and 151-164 (3802), rd1011 test 198-250 (2925), census test 60-69 (650), inventory json 111-112 (862), five tickets as the reader prints them (39831).

## BLUF of the facts (each re-measured; instruments in brackets)
1. Pull request 240 merged 2026-11-22T16:15:33Z (03:15:33 AEDT Mon) as a head-pinned merge commit `50b7c40cf1a682baffdd3827b77166ec65e746cd`, parents `8858e5d1...` and head `6a8bdc0d...` [`gh api -X GET pulls/240`, `git/commits/<sha>`]. 8 files, 433/20, 5 commits [`pulls/240/files`, `/commits`]. **Merge tree `000957e3...` equals the head tree** (unlike 238): `compare head...merge` ahead 1, 0 files; `compare 8858e5d1...merge` lists exactly the 8 paths. Main = the merge commit, 0 open pulls.
2. Head checks before merge: 7 names, 8 runs all success; head Build job log line 25525 reads `VERDICT: PASS - 6235/6235 tests passed across 394 suites (jest exit 0)` [saved log, `/usr/bin/grep -n -a`]. **The commission's "hosted Build run 45038753721" is the pull request HEAD's Build (event pull_request); the merge commit's own Build is run `45042817290`, job `137270806378`, in_progress at 03:2x** (the kit names both and waits on the second).
3. Merge commit at drafting: 8 check-runs: 4 success, 2 skipped (Deploy demo build and deploy, run `45042817352`: nothing deployed), 2 in progress (Build, Analyze javascript-typescript). Code scanning on main: 22 open (the same 22 numbers B1807 read), 222 fixed, 7 dismissed; the analyses of the merge commit for python and actions are listed (0 results), javascript-typescript is NOT yet; no open alert is newer than 2026-11-08T21:39:52Z; alert lines equal B1807's (the change touches no backend file).
4. Reviews: round 1 `GATE B1925: NO GO @ 081f422` (Blocker 0, Major 1, Minor 3, Info 7; count "NO GO 1 of 2 on the class off-guide colour"); round 2 `GATE B1942: GO WITH FINDINGS @ 6a8bdc0` (0/0/0/Info 8), all four round-1 findings closed (its table lines 23-28). It has no FOR-RECORDS.md (confirmed): its Info items are in VERDICT.md.
5. Tickets: RD-349 and RD-175 both Bug, Medium, To Do, label `operations`, 1 comment each (41047, 41048), transition id 31 `In Review` -> `Testing` offered on each. Neither ticket's scope reaches beyond the change (both read whole). 1025 issues, highest RD-1029, nothing created since B1807.
6. Records: `CLARIFICATIONS.md` 874164 bytes, 3154 lines, sha256 `7d72052c28a83705...`, section 107 at line 3136, C-311 at 3148, 1361 non-ASCII bytes; so section 108 / C-312 expected at lines 3156 / 3158. `HISTORY.md` at the merge 10344 lines, 1128640 bytes, sha256 prefix `f1e12fd8b6455395`, 7563 non-ASCII bytes, last heading line 10328; new heading expected at line 10346. `pull request 240` reads 0 lines of both (control `C-311` reads 1).
7. The owed ticket: the permission table is `ROUTE_CAPABILITY` in `backend/services/capabilities.js`; the two rows are lines 155 and 156 (`GET /api/data-sources/:id/describe-table` and `.../discover-tables`) in the `config.read` block (opens line 151); `config.read` is in `READS_TODAY` (107) which the viewer role holds (111). The committed inventory (`docs/role-capabilities.json` lines 111-112, `docs/ROLE-CAPABILITIES.md` lines 125-126) already reads viewer 403. **A program over both files (`captable.py`): 203 table rows = 203 inventory rows, equal sets; exactly 2 rows sit under a viewer-held capability while the inventory says viewer 403** (control: 15 rows under `admin.read`). The cell that pins the old state is P2 of `__tests__/rd1011-four-routes-administrator-only.test.js` (lines 225-227). Board search first (Jira GET, phrase form): `permission table` -> RD-1011, RD-1021, RD-1022; `describe-table` -> RD-118, RD-793, RD-1011; `discover-tables` -> 8 tickets; `config.read` -> RD-1011, RD-1021, RD-1022; `ROUTE_CAPABILITY` and `admin.read` -> none; I read RD-1011 (its comment says the table is unchanged and the change "has no ticket yet"), RD-1021, RD-1022 (other rows), RD-929, RD-793 by program: **none asks for these two rows to move, so the kit creates NEW-C and comments on nothing**. The card (read once by `decision_queue.sh show <exact id>` into scratch): ruled `a`, ruled_ts 2026-11-20T16:58:19+11:00, the option detail reads verbatim as the commission quotes it, delivered note says "has no ticket yet". No card id is in any kit text.

## D-decisions (mine, each a default of the coordinator's, none the product owner's)
- D-1 Both tickets propose Testing (the project rule, `CLAUDE.md` lines 302-303), comment first, move only after read-back equal and the move check printed.
- D-2 THE DISPOSITION (kit section, item by item, never both): round 1 F-1 to F-4 closed (record line); I-1, I-2, I-3, I-4, I-6, I-7 record lines; **I-5 -> NEW-A (Task, Low)**. Round 2 I-1, I-2, I-3, I-5, I-6, I-7, I-8 record lines; **I-4 -> NEW-B (Bug, Low)**. Owed by the ruling: **NEW-C (Task, Medium)**. Total 3 creates, 0 duplicates found.
- D-3 RD-349's second finding (the baseline asymmetry) is answered in the comment and the entry from the fixture's own history text: the drop-text spans are the signature `span x3`, which left the baseline with `p.file-description x3` (69 -> 63). Marked DERIVED, not run.
- D-4 RD-175's comment says the text-shadow was removed ON PURPOSE (its description asked that a fix not delete it silently); the kit's HOLDS forbid saying the shadow was kept or the light fills pass.
- D-5 Ratios in Jira texts are written with the word `point` (the Jira scan refuses digit-dot-digit except three-part versions); the entry may use decimals.
- D-6 Labels: `records-pass-<MMDD>` plus `operations` (NEW-A, NEW-B: the contrast family's label) and `security` (NEW-C). Priority/type reasoned in the kit.
- D-7 REFUSE 8 holds the RD-349 and RD-175 texts and the landing entry only; the three creates quote no hosted fact and are not held by it.
- D-8 Round 2 Correction 3 (the kit called the copied test file "untracked") is recorded as the coordinator's kit fault, in the entry.
- D-9 B1807's lessons folded by name: Deviations 1, 2, 3/4, 5, 6, 7, 8, 9, 12 and Correction 3 (the doubled phrase "code scanning on main reads" is written once); Deviation 6's late controls now run at Step 0 before any write.

## Q-questions for Tuesday (each with its default)
- Q-1 Move RD-349 and RD-175 to Testing? Default: yes both (slots MOVE-349 and MOVE-175 = their numbers).
- Q-2 The builders' own lists (other grey text on the KPI tiles `.metric-card .text-muted`, the tile value colour `#0096d6`) are not review findings: record line only, or tickets? Default: record line only, no ticket.
- Q-3 NEW-C priority Medium (a stated promise to the product owner, no behaviour today) or Low? Default: Medium.
- Q-4 Fold NEW-A and NEW-B? Default: three separate creates.
- Q-5 Round 2 I-1 (dark track equals the striped row's ground): left as a record line, "a palette question for the product owner", not filed and no card. Default: record line.
- Q-6 Labels `operations` on NEW-A and NEW-B: default yes.
- Q-7 The stamp may find the Build already concluded; the first poll then exits 0. If it has not, the creates may run before the wait ends (kit D-7); default as written.

## Checks run once on my prototype output (DRAFTER_RULES last line): PASS, control FIRED
- Jira scan (`scan1947.py`): 24 texts (9 landing/comment, 15 ticket paragraphs) scanned alone and after sample fill-ins: 0 hits; controls fired for every class including `8f4b7166`, `undeployed`, `a seat`, `1.5`; quiet strings (`6a8bdc0d`, `1.4.11`, `R5`, `R8`, hex colours) stayed quiet. The first run HIT twice (`gate` inside `handler gate` and `PENDING_GATE`): reworded, re-run 0.
- Entry scan over the section heading, the entry (filled) and the history entry: 0 hits; controls (name, Tuesday, B1947, R301, at-sign, URL, `8f4b7166`) fired. The seat's own program is NOT this one: the kit says so.
- `pointers.py`: 43 rows, 0 fail; controls `#212529` on index-styles.css line 306 reads False, row 157 of capabilities.js reads False. Counts: 19 indented `test(` lines in the new test file, 0 at column 1; 36 `metric-label` lines in `light-baselines.json` (27 to 242).
- REFUSE 1 count: 13 four-underscore lines in the unstamped kit (planted line control: 14).
- Marker searches (phrase form): 5 kit markers read 0; controls `LAND-238-1008-20NOV`, `RULING-1011-20NOV`, `REC-REG-349-11NOV` read 1 each.
- Never run on a real output (named in the kit's HOLDS 3): the seat's helpers, the wait program, the move check, the check over added lines on a real fill, the FOR TUESDAY lister.

## Chain step inputs (DRAFTER_RULES MEASURED LITERALS 4)
| Step | Inputs | Produced by / exists at |
|---|---|---|
| 0 | kit copy, STATUS path, `.tools/b1947/` | stamped kit; created in Step 0 |
| 1 | repo config, remote main | BASE (existing) |
| 2 | this kit's lists | the kit |
| 3 | CLARIFICATIONS, Jira, GitHub reads, POINTERS | BASE (existing) |
| 3b | Build run `45042817290`, check-runs, analyses | GitHub (finishes by itself) |
| 4 | Step 3 reads, Step 3b fills, texts | Steps 3, 3b |
| 5 | Step 4 payloads, Step 3 prechecks | Steps 3, 4 |
| 6 | Step 5 results (keys, ids), Step 3b fills | Steps 3b, 5 |
| 7 | `entry-numbers.txt`, Step 1 identity | Steps 6, 1 |
| 8 | all of the above | Steps 0-7 |
The one forward dependency is the wait: Step 5 comments on RD-349 and RD-175 and Step 6 need Step 3b's exit 0; the creates and RD-1011-free work do not.

## UNMEASURED
The merge commit's Build conclusion and its javascript-typescript analysis; the repo-local `user.email` prefix (`git config` is not a drafter read verb; RELAYED from the B1807 STATUS); the end-to-end suite itself and the 72 `tab-button` lines of `light-baselines.json`; whether a backend file requires `capabilities.js` beyond GitHub code search (6 files, all tests; the index can lag); the seat's re-run of every P4 search phrase; the page as rendered on a hosted instance; `status_watch.sh` arming; line pointers after any later merge.

## Corrections to the commission
1. "Build run 45038753721" is the head's pull_request Build, not the merge commit's (that is `45042817290`).
2. "22 open on main before it; none may be new": 22 open, 222 fixed, 7 dismissed at drafting, but the javascript-typescript analysis of the merge commit was not yet listed (the kit's REFUSE 8 and Step 3b cover it).
3. The merge tree equals the head tree here (B1807's did not); the move check was re-written accordingly.

## Outside-the-fences disclosure
- Read the decision card once with `decision_queue.sh show nexusai-rd1011-read-routes-viewer-1120` into scratch `raw/card-show.txt` (the commission allows the exact id for my check) and read it through an inclusion grep; never `list`; no card id is in the kit.
- One Bash call ran a `for` loop of four Jira issue GETs (the "one simple command per call" instruction), and one Python loop listed `/briefs/` file names to find the origin of a scan rule: that print showed file names of other projects' kits (I read no content); none is used.
- `tmux list-panes -a -F` (read-only); GitHub `search/code` GET calls (read-only API); `cp` of the saved head Build log from the tool-results folder into scratch; `os.replace` of my own first-pass `.measured` into scratch before re-initialising it.
- I read B1807's drafter helpers under `fleet/state/s301/d1807/` (read-only) and copied three of them into my scratch.
- No Jira write, no GitHub write, no ref write, no demo or hosted request, no `cd`, no other drafter's file or lock touched; the OXPd names appeared only in `tmux list-panes` output and are not in the kit.
