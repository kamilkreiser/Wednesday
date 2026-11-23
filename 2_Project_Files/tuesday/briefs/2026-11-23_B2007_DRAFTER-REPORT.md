STARTABLE: YES (once Tuesday fills the 11 stamp slots and stamps the last line; nothing else blocks it)

# B2007 DRAFTER REPORT (Sonnet drafter, read-only; Composer records seat Datasec/Composer-R307, model sonnet, routing rows C7, C8 and G3)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B2007_SEAT-R307_composer-records-pr132.md` (92,728 bytes, 191 lines; sidecar `.measured` beside it, 172 claims, `stamp_check.py` exit 0). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s318/d2007/`. Clock: `date` printed 20:44:00 to 21:01:32 AEDT, 2026-11-23. B2005 and B2006 (OXPd) and the running OXPd and NexusAI records seats were not touched or read.

## BLUF
One Composer records pass: the landing of pull request 132 (PCOMP-67, the Q-03/Q-04 scan test plants every alternative; squash `8b9ab200`, test-only, build B1959, review B1962 GO) and the landing of pull request 85 (2026-11-21 08:28 AEDT, squash `3638da61`), which is on NO record of the project (counts below). TWO C-entries (158 and 159 at drafting; the PR 85 entry first), one comment on PCOMP-67 and, under slot MOVES and a six-row MET table, its move to Done, ONE new Task (B1509's create form) for the two sibling alternations (`(True|False)` at line 88, `(png|svg|jpg)` at line 97 of the test file) after a board search that found nothing (printed counts and a control that fires), two BACKLOG state sentences (#367, #368) and one new row (#496, label `plan-comp-496`), one `JIRA.md` bullet, one history entry, one commit, one `--no-ff` merge. The product owner's standing hold binds every text: no deploy of a changed content release without his own card; a program-checked DEPLOY WORD CHECK (an allow-list of fragments, leftovers must be 0) keeps any text from saying a deploy is due, approved, scheduled or done. Main has carried a changed content release since PR 85 (demo CONTENT_HASH `05070f1d` to `5db37614`, draft `62cf4932` to `5679855b`); that is recorded as a fact with the refusal beside it. Seat size about 90 minutes (read load 232,710 bytes by program; 3 Jira writes at most).

## Facts re-measured with instruments (each with a control)
| fact | instrument | result | control |
|---|---|---|---|
| code main, PR 132 | `gh api -X GET` (project gh-config, account kamilDatasec) 20:44:05 to 20:57:27 | main `8b9ab200b09f9a859c3b25b6441813546338d3dd`; PR 132 merged true, merged_at 2026-11-22T20:08:05Z (07:08:05 AEDT 11-23), head `ceff5cf4`, base `423516cb`, 1 file +17 -4, blob `1d575680`; squash 1 parent, tree `dccab983`, 1 trailer; Analyze csharp and javascript-typescript success; alerts on main 0; open PRs 0 | `pulls/9999` HTTP 404; `commits/0000...` HTTP 422 |
| PR 85 | same | merged true, merged_at 2026-11-20T21:28:01Z (08:28:01 AEDT 11-21), squash `3638da611ce8...`, parent `b4681297`, tree `e9ded89d`, 57 files +38887 -3186, 7 under content/release-*, 15 commits, checks success | blobs at `b4681297` differ from the squash's |
| release blobs | `contents/<path>?ref=` at four shas | equal at `423516cb`, `3638da61`, `8b9ab200` (23cd95f5, 09d597c6, 3ed9445b, 30269393); CONTENT_HASH values `05070f1d`/`62cf4932` at `b4681297`, `5db37614`/`5679855b` after | the four blobs at `b4681297` read unequal |
| test file | raw at `8b9ab200` (13029 bytes, git blob equal) | `True|False` once at `:88`, `png|svg|jpg` once at `:97`, `morePlants` 6, middle pattern at `:80`; plants: one each for Constraint, PolicyControlValue, Compare | a copy without the `:Compare` plant reads 0 |
| PCOMP-67 | Jira GET | Task, Backlog, labels `composer-seed-1023` + `plan-comp-368`, 0 comments, 0 changelog, updated 2026-10-23, transition 41 Done; description holds `PR #85 is not landed` once, no Done-when | `PCOMP-9999` HTTP 404; B1957's saved PCOMP-12 comment counts Done-when 1 |
| board search | JQL `project = PCOMP AND ( ... )`, `jsearch1.out`, `jcount2.out` | `svg` 0, `morePlants` 0, `b330-sm316-qgate` 0, `labels = "plan-comp-496"` 0; `alternation` 2 (PCOMP-120 another test, PCOMP-67); `png` 7 and `True` 9 unrelated word matches | `Compare alternative` 1, `labels = "plan-comp-368"` 1, `zzqxvbw` 0 |
| project counts | paginating counter | 129 issues, Done 53, Backlog 76, held 19, seed 94, updated since 11-19: 11 | `zzqxvbw` 0 |
| root records | git read verbs, python | root main `51a1b115` (B1957's merge), C max 157 (next 158 and 159), BACKLOG highest row 495 (next 496), 485 data rows, JIRA.md newest `- B1957`, history entry at `:3`; no `.tools/b2007`, `records/b2007`, worktree | C-157 count 1; `.tools/b1957` exists |
| PR 85 already recorded? | python `str.count` over the four record files | `3638da611ce8...` 0 in all; `pull request 85 landed` 0; `3638da61` 2, 0, 0, 1 (all B1957's mention as the PARENT of PR 131); every other mention says held or not landed. **Not recorded.** | `PR #130` 8, 5, 2, 5; `C-157` 2, 6, 1, 3 |
| the project's move rule | `grep` over the Composer `CLAUDE.md` and `JIRA.md` | CLAUDE.md holds no Jira rule (jira and pcomp 0; its one "move" is the repository move); JIRA.md `:28`-`:30` say "the project records no rule for when a merged ticket moves" (3); practice from `:33` on: a move on the coordinator's instruction, Done-when met per the gate (merged, not deployed) | planted phrase 0 |
| scanner | `proto_b2007.py` runs a byte-equal copy of `.tools/b1808/scripts/textscan_b1808.py` (sha256 `d517e19f...` both; 8 name tokens read in-process, never printed) | Jira rule: 0 hits on TEXT-67 (2 variants), summary, 5 paragraphs; records rule + deploy word check: 0 hits over 312 variants; kit-wide name scan 0 | 29 of 29 project controls, 16 of 16 records controls fire; clean phrase 0 |

## STOP-severity checks run on my own prototype (PASS, control fired) / never run
Run: JIRA TEXT RULE, records rule, DEPLOY WORD CHECK, marker counts, C and row numbers by program, BACKLOG append check on a scratch copy, PCOMP-67 Done-when rows 1 to 6 on live reads (all MET), text facts (dates converted by python zoneinfo, line pointers, `morePlants` 6, blob equality), description facts. Never run (named in the kit): the helper copies and edits (one-key `jira_write.py` plus the create form ported from B1509), the Jira dry run and its guard for this list and the create controls, apply and read-back, `build_names.py` for B2007, the records and check scripts, commit and merge, identity prints, REFUSE 2's pane checks (no Composer pane exists), the slot-dependent facts, the seat's own Done-when file.

## Chain inputs (each produced by an earlier step or present at BASE)
| step | inputs | source |
|---|---|---|
| 0 | the kit, slots, root repository, `.tools/b1957` and `.tools/b1509` scripts | BASE / stamp |
| PRIOR WORK | Jira GETs, `pulls`, record files, slices | BASE |
| 1 | two gates' files, the test file (raw), release blobs at four shas, notes lines | BASE |
| 2 | slots, span hashes, Step 1 facts | Steps 0, 1 |
| 3 | spans of this kit, `names.json` built by `build_names.py` | Step 0 builds the scratch dir; BASE scripts |
| 4 | test file, gate files, saved tickets; writes `movechecks.json`, `jira_before.json`, `payloads.json`, `task-payload.json` | Steps 1, 3 |
| 5 | payloads (Step 4), `movechecks.json`, `jira_before.json`, helper copies | earlier steps |
| 6 | apply-log (Step 5: the comment id, the new key), C and row numbers (Step 0), spans, worktree | earlier steps |
| 7 | all of the above | earlier steps |

## D-decisions (mine; each is Tuesday's to overturn)
- D1 TWO C-entries (PR 85 first, 158; PR 132 second, 159): different events, different dates, one has no Jira line. The PR 85 record is unconditional (the commission: write it if absent, and it is absent); to defer it Tuesday strikes it before the stamp.
- D2 The PR 85 entry is a record, not a ruling: it cites C-155 and the product owner's 2026-11-20 ruling by date (no card id), restates the standing refusal verbatim in substance, and states nothing about what the demo runs (not measured by anyone).
- D3 No Jira write for PR 85 (PCOMP-31 to PCOMP-35 still carry C-155's comments that call it an open draft; PCOMP-66's row and PCOMP-67's description say not landed): the entry names them as stale and owed, touches none.
- D4 PCOMP-67 moves under slot MOVES only, per the review's FOR-RECORDS item 1 and the project's practice; the project has no written rule (quoted from `JIRA.md`). Its description's stale block is NOT edited (the closed list has no field edit); the comment says it is out of date.
- D5 The new ticket text names no key of itself (the comment on PCOMP-67 says "a ticket of their own"), so both frozen bodies are approvable before the key exists; the Task's description names PCOMP-67 and the row number.
- D6 Texts date the PR 132 merge 2026-11-23 (AEDT; UTC date 2026-11-22), as B1957 did for PR 131; the entries carry both clocks.
- D7 The new BACKLOG row #496 is always added (the label `plan-comp-496` needs it); under CREATE `NO` it records the follow-up alone.
- D8 Records texts write the siblings in words (no pipe character allowed in a record span); the Jira texts carry `(True|False)` and `(png|svg|jpg)` as the gate's FOR-RECORDS item 4 does.

## Questions for Tuesday (each with a default)
- Q1 MOVES: `PCOMP-67` (default: the gate's FOR-RECORDS item 1, the practice since B842) or `NONE`.
- Q2 CREATE: `YES` (default: no existing ticket covers the siblings) or `NO` (row #496 still added, ticket held).
- Q3 STATE-ROWS `APPEND`, REC-MERGE `MERGE`, JIRA `WRITE`, COMMENTS `PCOMP-67`, RECORDS `WRITE` (defaults as B1957); HARD STOP 23:59 AEDT (the commission's).
- Q4 PR 85: a Jira comment on PCOMP-31 to PCOMP-35 to correct "open draft" is NOT in this kit (default: a later pass, with its own facts); say so if wanted in this seat.
- Q5 Seat id `R307` and pane `Datasec/Composer-R307`: 0 of 58 non-`.pre-` SEAT kits of 2026-11-22 and 2026-11-23 name `R307` (control `R306` 1), but B2005 and B2006 are being drafted beside this one: re-scan at the stamp.

## UNMEASURED
What the demo runs (nobody has measured it); the mutants S2 and S3 (svg, jpg) at the base are the build's measurement, RELAYED and not re-run (TICKET-DESC-2 says so); the gate's mutant results are RELAYED (this pass runs no test); the live state of the keys, root main and code main at the seat's start; whether another Composer pane exists then (at 20:50:51 `tmux list-panes -a` showed the coordinator's pane, the OXPd and NexusAI records seats and unnamed panes).

## Outside the fences
None known. I read, wrote and ran only: the two files of this task; scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s318/d2007/` (GET readers, counters, prototype and sidecar scripts and their outputs, a raw copy of the test file at `8b9ab200`, a byte-equal copy of the project's scanner); the sidecar `.measured` of the kit (by `stamp_check.py --init`, then filled by program). Reads: the commission, `DRAFTER_RULES.md`, B1957's kit, STATUS and drafter report (form), B1956's kit and report not read (only its section of the joint commission B1956-B1957 was read), B1959's STATUS, the two gates' folders (B1962 whole; B1818 VERDICT lines 1 to 40, FOR-RECORDS and landing.txt whole), the Composer `CLAUDE.md`, record slices, coordinator note lines, `model-routing.md`, `.tools/b1957/scripts/`, `.tools/b1509/scripts/jira_write.py`, `build_payloads.py` and `jira_readback.py`, `.tools/b1808/scripts/` scanner files, GitHub GET and Jira GET (credentials in-process through the project's `jira_lib`, never printed; `gh auth status` printed no token). One slip: a first measuring command of mine contained a stray `rm -f /dev/null` that the delete hook refused before anything ran; I re-issued it without it. No write to any project, Jira, GitHub, decision store or human; no docker, az, ssh or test.
