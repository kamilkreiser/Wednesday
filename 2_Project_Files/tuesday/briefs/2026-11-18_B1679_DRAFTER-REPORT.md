STARTABLE: YES, after Tuesday's stamp (no NexusAI pane is live; code main is still the merge commit 751285aa; the kit has TEN Stamp slots, not nine: STAMP, LAUNCH WINDOW, BASE, JIRA, CREATE, MOVE, L1NOTE, RECORDS, HISTORY, Hard stop, plus the last line = 11 four-underscore lines; stamp_check 91 claims, 91 measured, rc 0). ONE CONDITION: the hosted Build of the merge commit (run 44088904188, job 134058565187) was still `in_progress` at 00:18; the kit WAITS for it (Step 3b, one background poller, no write before it exits 0), so Tuesday may launch now or after the Build reads success (expected about 00:52 to 01:05 AEDT from the 48 to 61 minute Builds of the earlier merges).

# B1679 drafter report (SEAT-R263, NexusAI records: pull request 216 / RD-995), drafted Wed 18 Nov 2026 (`date` first read 00:04:00, last read 00:18:54 AEDT)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1679_SEAT-R263_nexusai-records-216.md` (175 lines, 0 non-printable bytes, 11 four-underscore lines; lines 12, 35, 38, 59, 72, 96 exceed 1990 chars). Sidecar `...md.measured` (107 lines: 91 claim lines, 14 TM- text-to-source lines, SCAN-1, SHA-1, plus the 30 pointers' print in the build log). Work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s287/d1679/` (`texts1679.py`, `kit_body.md`, `build1679.py` (prints "pointers ok 30 bad 0"), `gen_sidecar1679.py`, `scan1679.py`, `chk_texts1679.py`, GET-only `gh1679.sh` and `jget1679.py`, `src/` copies of the files at the merge commit).

## Items (what the seat will do; slot in brackets)
1. Step 1 (read only): identity prefix be76c2c1baf03ec1 (re-read 00:05, equal), one-command transport for ls-remote/fetch/push (repo-local core.sshCommand still names the unmounted /Volumes/Laptop-DEV: RD-1001 still To Do), config diff empty.
2. Step 3b evidence wait: Build run 44088904188 and every check-run of 751285aa `completed`; Build `success` with a `VERDICT: PASS` line (expect 5868 of 5868 across 377), Deploy demo both jobs skipped (run 44088904160, read), a javascript-typescript analysis of the merge commit listed (id 2186180370 exists), else REFUSE 8.
3. **NEW ticket** [CREATE NEW]: Task, Medium, labels needs-decision, records-pass-<MMDD>, roles-ui-2026-11, security; summary 202 chars; five paragraphs rewritten from `finding3-ticket.txt` into the project's ticket form (BLUF / read at source / second point / recommendation / acceptance + marker `ACTIONAUTH-216-18NOV`). It is a decision question: "this ticket decides nothing and builds nothing". It folds in F2 and F3. Done first (5a) because two later texts carry its key.
4. **RD-995 comment + move to Testing** [JIRA, MOVE 995]. Done-when (the ticket's proposed acceptance, five parts) read against the gate: (1) note wording true at source; (2) pending list no longer names the route (P1 plant 3 red / 11 green, P2 plant 2 red); (3) 70/70 cells in 14 files, plain verify 5868/5868 across 377; (4) 203 rows same keys, only this row's note differs, generator reproduces it; (5) diff over server.js / routes / middleware / .github empty, `decide()` unchanged. All five read met by the independent review; hosted Build is the remaining evidence, hence the wait. Move rule: code change goes to Testing (CLAUDE.md line 302).
5. **RD-929 comment** [L1NOTE WRITE, default HOLD]: F2 (the condition for the permission-core wiring: honour OWN_CALLER_CHECK or move the route to the own-credential capability). **Form check:** the template's closed list allows a comment only on keys named in its row and forbids "any other key"; this kit names RD-929 in THE ROW (class comment only, no move, own marker `L1NOTE-216-929-18NOV`), so the form allows it. RD-929 is the L1 permission-core ticket (its landing comment 41174; capabilities.js header lines 4 to 8 name "item 1 of RD-929 (L1)"). No label, field or move on it. F2 is ALSO recorded in the entry and in the new ticket's P3/P4, so if L1NOTE is HOLD nothing is lost.
6. Records: section 98, entry **C-300** (measured: highest section 97 at line 3022, highest entry C-299 at line 3024, 733764 bytes, 3030 lines, sha256 282af7b4ac688bbc84c77607338e6ca3b5eff22590a670b70107da2249951903; none of `pull request 216`, `751285aa`, `C-300` present, control `C-299` present). It records the landing, the five review findings, the new ticket, the RD-929 comment, the builder's disclosure of the capability column, and cites C-290 (the ruling) and C-299.
7. Step 7 [HISTORY]: one HISTORY.md entry on `records/b1679-history` from origin/main (HISTORY.md at 751285aa: 10146 lines, last heading at line 10130 is the pull request 214 entry, ends with a newline; no `records/b1679*` branch on origin, control main prints 1 line).

## Facts re-measured (sidecar lines; all `gh api -X GET` under the NexusAI GH_CONFIG_DIR; Jira GET only)
- Pull request 216: merged, merge commit 751285aa138f366e44d0ef97e1464dc6bf52c436, merged_at 2026-11-17T13:03:11Z = 2026-11-18 00:03:11 AEDT, parents 530db4df + 25b19960, merge tree edec1b17 = head tree, 4 commits (3dadbfa8, 84f2acff, fe27ca00, 25b19960 merge of main), 7 paths all modified, +40 -11. Counts file 5867/377 at the base, 5868/377 at the merge. Main = merge commit, 0 open pulls, compare identical, repository variables 0.
- Check-runs at 00:16: 5 success (Analyze python, actions, javascript-typescript; scan; audit-production-deps), 2 skipped (Deploy demo deploy and build, run 44088904160 skipped), Build job `in_progress`. NOTE two check-runs are named `build` (the skipped Deploy demo one and the Build one); the kit pins job id 134058565187 for the log.
- Code scanning on main at 00:16: open 22, fixed 222, dismissed 7 (142 143 144 147 148 149 150); 0 created after the merge; 0 fixed since; all 22 open instances now on `751285aa`; the JS analysis of the merge commit exists (2186180370, 29 results, 13:07:14Z); 0 open alerts on a `__tests__` path; RD-995's text holds the word alert on 0 lines.
- Jira: RD-995 To Do, Task, Low, labels records-pass-1116 and roles-ui-2026-11, no comment, transition 31 In Review -> Testing offered; RD-929 To Do, Story, Medium, one comment 41174; RD-992 Done (untouched); 998 issues, highest RD-1002. Marker searches 0 (ACTIONAUTH-216-18NOV, LAND-216-995-18NOV, L1NOTE-216-929-18NOV), controls fire (ACTIONRULED-206-16NOV -> RD-992, ROLENOTE-206-16NOV -> RD-995, LAND-214-985-17NOV -> RD-985). Duplicate searches for the 401-before-own-check gap found none (RD-88 is the Done precedent for the state route; RD-988 and RD-992 name the route but not the gap).
- All 30 code pointers at 751285aa print "contains fragment" true (build1679.py: ok 30 bad 0).
- Texts: 15 strings, each sha256 prefix printed in its label, scan 0 hits raw and with sample fill-ins (selftest controls fire; `x b1996 y` is a new control: see D2). Summary 202 chars.

## Step input table (MEASURED LITERALS rule 4)
| Step | Inputs | Produced by / exists at |
|---|---|---|
| 0 | the kit, df, project folder | exist at BASE |
| 1 | repo identity, transport key, `.tools/b1679/logs` | BASE; logs dir by Step 0 |
| 2 | `.tools/b1679` | Step 0 |
| 3 | helpers jira1679/facts1679, `.env` names, CLARIFICATIONS.md | Step 2; BASE |
| 3b | wait1679, run id 44088904188, merge sha | Step 2; BASE (kit) |
| 4 | texts (kit), facts-final (3b), snap_before (3) | kit; 3b; 3. Key-fill-ins use stand-in `RD-9999` because the key does not exist yet |
| 5a create | dry payloads | Step 4 |
| 5b RD-995 comment | Detail re-filled with the key | Step 5a (or HELD form) |
| 5c move | RD-995 comment read-back + move check | 5b; Step 3b |
| 5d RD-929 comment | Detail re-filled with the key | 5a |
| 6 append | read-backs, snap_after, before-copy | 5; Step 3 |
| 7 branch | identity prefix, origin/main, entry facts | Step 1; Step 6 |
(I found and fixed one violation of this rule while drafting: the first version built every payload in Step 4 although two texts needed Step 5a's key.)

## D-decisions
- D1 Priority Medium and the four labels follow RD-992 (the decision ticket of the same route) and the review's candidate text ("Priority (proposed): Medium"). `records-pass-<MMDD>` computed at Step 0 (expected 1118).
- D2 **Commit-id hygiene (new, found by measurement):** the B-number rule read case-insensitively fires on a hexadecimal run: the head id `25b19960...` holds `b1996`, the head tree `edec1b1769...` holds `b1769`. The Jira texts and entries therefore name the reviewed head in words ("the reviewed head", "the second parent of the merge commit"); only the merge commit id (no such run: checked) and 8-character prefixes without one are written. The kit body (not copied into Jira) carries the full ids for the seat's own checks. The scan's control `x b1996 y` fires.
- D3 The jargon of the route (path with the substring `coordinator`, the exempt-path set, `COORDINATOR_SECRET`, `secret`, `gate`) is written in words in Jira texts (banned substrings); entries may use `coordinator` (the earlier entries do) but never the configured value's name.
- D4 The two empty directories of the earlier review are out of this kit (the gate F5 says none was left this time); the kit names neither.
- D5 Hard stop: left as a slot; the commission's 02:30 AEDT 2026-11-18 is stated only as the proposal inside the slot's description; the wait limit is slot minus 60 minutes, so with 02:30 it is 01:30, after the expected Build end.
- D6 No ticket for F3/F4; no ticket for the row's capability column (recorded in the entry only).
- D7 History branch name `records/b1679-history`; the earlier branches (#213, #215) landed as head-pinned PRs by Tuesday, so the kit leaves the PR to Tuesday.

## Questions for Tuesday (each with the default written)
- Q1 **RD-929 comment (slot L1NOTE).** The commission said "only if the form allows a comment on a named existing key"; it does (comments on RD-985/998/996 were of that form), but RD-929 is a large Story with an earlier landing comment. Default written: slot L1NOTE offered with recommendation WRITE; stamp HOLD if you want F2 in the entry and the new ticket only.
- Q2 **RD-995 move.** Default MOVE 995 (code change goes to Testing; all five acceptance parts met per the independent review). Stamp NONE if you want the hosted Build to be the only trigger after a human reads it.
- Q3 **New ticket priority/labels.** Default Medium with `needs-decision` and `security` (as RD-992). Say if you would rather have Low and no `security`.
- Q4 **Launch timing.** Default launch now; the seat waits on the Build. If you prefer launching after the Build reads success, the clock rule takes the later of each pair.
- Q5 The entry's F5 sentence says no directory was left in the project folder (gate F5: "Neither directory was created"). Default written as the review says; the two older empty directories from the previous review are untouched and still await their owner (not in this kit).

## UNMEASURED
The hosted Build verdict line of THIS merge (the previous merge's line was read from its job log: `VERDICT: PASS` with a non-ASCII dash, printed in the sidecar); whether the sibling NX-T3 pull request lands during the run (the kit reads every file at the merge commit, so it cannot change a text); the seat's push by the deploy key (ls-remote with the same transport works, rc 0); "nothing in backend/ requires the table" is RELAYED from the review (not re-run at source by me); hooks allowing the seat's worktree and commit (they ran for the previous pass).

## Outside-the-fences disclosure
- Writes: the kit, its sidecar, this report, and scratch `fleet/state/s287/d1679/` only. Nothing under `/Volumes/Datasec_DEV/!CODING/` written; no Jira write; no GitHub write (every call `gh api -X GET` via my `gh1679.sh`; one `gh auth status` and a `gh api` 404 read); no git write (reads: `config --get user.email` as a sha prefix, `config --get core.sshCommand` truncated to 70 characters, `ls-remote` with the one-command transport, `rev-parse`); no board, mail, az, ssh session or docker. Jira GET only (issue reads and about 35 searches, every JQL `project = RD AND ( ... )`).
- Reads: the DRAFTER_RULES; the B1669 kit (two pages), its report, sidecar head and `.pre-stamp` Stamp section, and its STATUS; the B1678 VERDICT whole and `finding3-ticket.txt` whole; the B1670 STATUS (BLUF, READY and OWED, Corrections); `CLARIFICATIONS.md` by grep, sed, wc, sha; C-290 whole; HISTORY.md at the merge commit (tail); project `CLAUDE.md` lines 286 to 306; model-routing lines 97 and 110; models_latest.json line 23 (`claude-sonnet-5-5`); the s286 scratch helpers `gh1669.sh`, `jget1669.py`, `scan1669.py` (copied and adapted).
- Hook events: one Bash call refused for a `git worktree list` I put in a read batch (re-issued without it), one for an unquoted `==` word, one for an `rm -f` on the old sidecar (not deleted; the sidecar was rewritten in place instead). No `cd` typed.
- Never read: `_ledger.md`, other seats' `.tools/` folders, any decision card, `briefs_staged/`, WEDNESDAY/FRIDAY trees.

DRAFTED B1679: kit 175 lines, sidecar rc 0 (91/91), questions 5
