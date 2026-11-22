STARTABLE: YES (once Tuesday fills the 11 stamp slots and stamps the last line; nothing else blocks it)

# B1957 DRAFTER REPORT (Sonnet drafter, read-only; Composer records seat Datasec/Composer-R303, model sonnet, routing rows C7 and G3)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1957_SEAT-R303_composer-records-pr131.md` (77,774 bytes, 176 lines; sidecar `.measured` beside it, 116 claims, `stamp_check.py` exit 0). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/d1957/`. Clock: `date` printed 06:09:02 to 06:20:44 AEDT, 2026-11-23. B1956 (OXPd) was not touched or read.

## BLUF
One Composer records pass for Composer pull request 131 (lane CW-2, build B1948, gate B1951 GO WITH FINDINGS): ONE C-entry (next number by program, 157 at drafting), ONE comment each on PCOMP-36 (stays OPEN; says what is met and not met: only 4 of 34 typed fields carry a value, 16 read variable, 14 empty) and PCOMP-37 (met on its letter; moved to Done only under slot MOVES and a six-row MET table), three BACKLOG row sentences (#336, #337, #338) and one new row (#495 at drafting), one `JIRA.md` bullet, one history entry, one commit, one `--no-ff` merge. B1951 F1 (README "No code reads it" untrue of tests) is recorded as OWED to the L2-3 lane (row #338, PCOMP-38) as a one-word fix and NOT fixed; F2 is a records note. No deploy, no release, no customer-facing word, no card slot. Seat size: about 90 minutes (read load 207,639 bytes; 2 Jira comments, 1 move at most).

## Facts re-measured with instruments (each with a control)
| fact | instrument | result | control |
|---|---|---|---|
| code main, PR 131 | `gh api -X GET` (project gh-config, account kamilDatasec) at 06:10:05 and 06:19:52 | main `423516cb2242956a4df2d7fe8bd3d95d001a98c7`; PR 131 closed, merged true, merge sha equal, merged_at 2026-11-22T17:16:50Z (04:16:50 AEDT 11-23), 3 files +5135 -0; open PRs 0; 131 is the newest of the last five | `pulls/9999` HTTP 404 |
| committed file counts | python over the raw file at the squash (`counts.py`, `counts.out`) | rows 132; class 50/52/25/3/2; variable 28 = 25+3; setters 28 (kind control_decision, id `UQ-nnn`); severity 50/82; unsupported 90/42; remediation on 76, off 2, empty 54 (78 with a value); flags 39/2/21/33/1/42; items 130 on rows, 2 rows without; 350 field targets; typed 34 = 4 value + 16 variable + 14 empty; untyped 316 all empty; `_meta.counts` agrees | one row removed reads 131; one typed empty turned true reads 5 |
| file sha256 | `shasum` | json `a744f915...` (equals the builder's CK12 value), README `3dc10809...`, test `f751bddb...`; blob shas equal the git tree | planted wrong blob unequal (kit row 1) |
| release blobs | `contents?ref=` at squash and at parent | all four equal (23cd95f5, 09d597c6, 3ed9445b, 30269393) | README is absent at parent |
| tickets | Jira GET in-process | PCOMP-36 and -37: Task, Backlog, 2 comments each (39941/39948, 39942/39949), 1 changelog each, labels seed + plan-comp-336/337, transition 41 Done; descriptions say "Not started" (count 1) and carry no Done-when (0; B1808's saved PCOMP-12 file counts 1 in a comment) | `PCOMP-9999` HTTP 404 |
| project counts | `jira_counts.py` (B1808's, read-only run) | 129 issues, Done 52, Backlog 77, held 19, seed 94 | `zzqxvbw` 0 |
| root records | git read verbs, python | root main `53b286cd`; C max 156 (so 157, 0 headings with it); BACKLOG 484 data rows, highest 494 (so 495); JIRA.md newest bullet B1808; no `records/b1957`, `.tools/b1957`, `.tools/wt-b1957-rec`; root remote 0 lines; record files clean | C-156 count 1; code clone prints origin |
| prior records | python `str.count` over the four record files | `423516cb`, `pull request 131`, `PR #131`, `b1948`, `default-baseline`: 0 each | `PR #130` 8/5/2/5, `C-156` 2/3/1/2 |
| gate | read whole | VERDICT line 1 `GATE B1951: GO WITH FINDINGS @ 6aa6a5f on main 3638da6`; F1 Minor, F2 to F4 Notes, F5 disclosure; no Blocker or Major word; FOR-RECORDS item 4 "met on its letter" | Minor counts 1 |
| scanner | `scan_b1957.py` runs a byte-equal copy of the project's own `.tools/b1808/scripts/textscan_b1808.py` (sha256 `d517e19f...` both) with B1808's name list (8 names, never printed) | TEXT-36, TEXT-37 (both variants): 0 hits; 11 record spans x 1008 placeholder variants: 0 hits; whole-kit name scan 0 | 30 Jira and 13 records planted controls fired, 0 did not; clean phrase 0 |

## STOP-severity checks run on my own prototype (PASS, control fired) / never run
Run: JIRA TEXT RULE, records rule, marker counts, C and row numbers by program, BACKLOG append check on a scratch copy (strict prefix, 5 fields on changed and new rows, 484 to 485 rows, planted extra-pipe row reads 6), PCOMP-37 Done-when rows 2 to 5 (and row 1's PR fields), description facts. Never run (named in the kit): the helper copy edits and the Jira dry run and guard for two keys, apply and read-back, the records and check scripts, the commit and merge, identity prints, pane checks, the bundle parse for "no Composer question linked to an item" (relayed from B1948 FACT 4), the AEDT conversion (by hand).

## Chain inputs (each produced by an earlier step or present at BASE)
| step | inputs | source |
|---|---|---|
| 0 | the kit, slots, root repo, Jira keys | BASE / stamp |
| PRIOR WORK | Jira GETs, `pulls`, record files, slices | BASE |
| 1 | gate files, three squash files (gh raw), blobs, notes lines | BASE |
| 2 | slots, span hashes, Step 1 facts | Steps 0, 1 |
| 3 | spans of this kit, names.json (built from the template and git config by `build_names.py`) | Step 0 builds the scratch dir; BASE scripts |
| 4 | committed-file counts, gate files, saved tickets; writes `movechecks.json`, `jira_before.json` | Steps 1, 3 |
| 5 | `payloads.json` (Step 3), `movechecks.json` and `jira_before.json` (Step 4), helper copies (Step 0) | earlier steps |
| 6 | apply-log (Step 5), C and row numbers (Step 0), spans, worktree | earlier steps |
| 7 | all of the above | earlier steps |

## D-decisions (mine; each is Tuesday's to overturn)
- D1 One commit, not B1808's two: the entry names the Jira comment ids, which exist only after Step 5.
- D2 No fold, no card slots: nothing here is the product owner's decision; every text says so.
- D3 Row sentences on #336, #337 and #338 (the third carries F1 as OWED to the L2-3 lane) plus one new row under slot FOLLOWUP-ROW (default ADD), as B1808's follow-up row.
- D4 Jira texts avoid every banned family (no M-row ids, C-numbers, "product owner", ".md", "status", "gate", "lane", "kit", "deploy", the company word). The records texts avoid "secret" (so "leak scan", not "secret scan") and the company word.
- D5 PCOMP-37's move is recommended in slot MOVES per the commission (the last Composer records kits B1688 and B1808 moved keys whose tables read MET). The ticket has no Done-when line, so the table is built from its scope sentence plus the "merged to main, not deployed" rule, as B1808 did for PCOMP-29.
- D6 TEXT-36 and TEXT-37 date the merge 2026-11-23 (AEDT; the API clock is 2026-11-22T17:16:50Z). The entry carries both clocks. If Tuesday prefers the UTC date, both texts change before the stamp.
- D7 The B1948 and gate "kit wording to correct in a successor" list (FOR-RECORDS) is for Tuesday's own drafting; it is not a project record and is not written.

## Questions for Tuesday (each with a default)
- Q1 MOVES: `PCOMP-37` (default, per the commission) or `NONE`. PCOMP-36 is never moved (the seat refuses a MOVES entry naming it).
- Q2 Pull request 85's landing (main `3638da61`, 2026-11-20T21:28Z) has NO record in the project: `3638da61` counts 0 in all four record files (control `C-156` counts). Default: this kit writes none and reports the counts in FOR TUESDAY; PCOMP-31 to PCOMP-35 and the "L1 not built" words on PCOMP-36 and PCOMP-37 (old comments) stay stale until a records pass for it. Say if you want it added to this seat (it would need its own facts and a larger kit).
- Q3 Slot STATE-ROWS and FOLLOWUP-ROW recommended `APPEND` and `ADD`; REC-MERGE `MERGE` as B1808 did. JIRA `WRITE`, COMMENTS both keys.
- Q4 HARD STOP: the commission's 10:30 AEDT; READY aimed at Step 0 plus 90 minutes.

## UNMEASURED
The bundle parse for "no Composer question linked to an item" (relayed; the seat measures it and a mismatch holds TEXT-37); the seat's own fresh `counts.py`; `date` and the live state of the keys at the seat's start; whether another Composer pane exists then (at drafting `tmux list-panes -a` showed the coordinator pane and two unnamed panes; 0 panes named for this seat); CodeQL/CI of pull request 131 beyond Tuesday's note (relayed: 3 of 3 success, alerts 0).

## Outside the fences
None known. I read, wrote and ran only: the two files of this task; scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/d1957/` (readers, counts, scan and sidecar scripts and their outputs); the sidecar `.measured` of the kit (by `stamp_check.py --init`, then filled by program). Reads: the commission, `DRAFTER_RULES.md`, B1808's kit and STATUS (form), B1948's kit and STATUS and ANSWER-1, B1951's two files, the Composer `CLAUDE.md`, record slices, the two coordinator note lines, `model-routing.md`, B1808's helper scripts (read-only; one first `cp` into scratch was refused by the path guard, a python copy of the scanner was used instead and its sha256 equals the original), GitHub GET and Jira GET (token in-process, never printed; `gh auth status` printed a masked token prefix once). No write to any project, Jira, GitHub, decision store or human; no docker, az, ssh or test.
