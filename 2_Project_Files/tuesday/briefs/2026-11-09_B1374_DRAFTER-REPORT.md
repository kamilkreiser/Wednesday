STARTABLE: YES (after the stamp; the safe-default slots HOLD everything, so Tuesday must set JIRA and RECORDS)

# B1374 drafter report (seat Datasec/HPSM-POC-R194, Sonnet records)

## BLUF
Kit written, 99 lines (long paragraphs, B1367 form, shortened to one C-entry, three Jira keys). R194 and b1374 are unused (word-boundary scan of non-`.pre-` kits in `briefs/`: R194, b1374, B1374, 9640 all 0; `ls | grep -c B1374` 0 before I wrote; `matching-refs/heads/records/b1374` 0 rows, control `records/b136` 2 rows). Every commissioned fact held at source. **The census reads 3 of 3 at 07:39:39** (42514097403 at 2075486b, 42296681684 at b14b6f29, 42187059450 at eaf77b3c, all completed/success), so 319 and 308 are expected to reach Done if their other clauses read met; nothing contradicted the commission.

## Facts re-measured (instrument; clocks 07:39 to 07:42 AEDT by `date`)
- Code main `2075486b011057ea496b9ea1b6ae2974e3e2307b` (`branches/main`); open code PRs 0 (`pulls?state=open` length 0; `pulls/99999` 404); open code-scanning alerts 0.
- #295 (`pulls/295`): closed, merged true, merged_at 2026-11-08T19:15:15Z (= 2026-11-09 06:15:15 AEDT, derived +11 h), merge_commit_sha `2075486b...`, 1 commit, 2 files, +12 -0; head `59a136dcd01453c83ff46dca554c7dd816b02834`. Commit: one parent `b14b6f29fe34568472e1c6e87178b0244ec32415`, files exactly the two `HostStartRetry.cs` copies (+6 -0 each), verification true. `compare b14b6f29...2075486b`: ahead, 1, 2 files.
- Run 42514097403: name ci, event push, branch main, head_sha 2075486b, completed/success; 18 jobs; both `api on SQL Server (api-assessment)` and `(api-other-and-feedback)` and the roll-up `api on SQL Server` success; 1 skipped (dependency review). Control: run id 1 404.
- Census: `actions/runs?branch=main&event=push&created>=2026-11-06T08:21:10Z` total_count 3, the three runs above; control: from 2026-11-01 total_count 26. I read the shard jobs of the newest run only; the other two I took from the run conclusion (see UNMEASURED).
- Header block at 2075486b (raw `contents?ref=`): Api copy 70 lines, block `:6` to `:10`; Feedback 69 lines, `:5` to `:9`; `diff` prints `1d0`, `4c3`. "Found by an independent review" is at Api `:9` / Feedback `:8`. `IsMigrationsLockLost` Api `:36`, `LockNotHeld` `:31`.
- At 2075486b: row `Two_hosts_starting_...` at `ApiFactoryHostStartRetryTests.cs:620`; `Assert.Empty(kills.Killed)` count 0; `Slack = 1200` at `RequestTimingLogTests.cs:329`; the 1223 retry test at Feedback `HostStartRetryTests.cs:325`; ci.yml `:268` `grep -c ''`; `wc -l` only at `:330`.
- Jira (project `read.py`, `search.py`): 447 Backlog, 0 comments, transition 41 Done; 319 Backlog, 5 comments newest 40860 (B1367's); 308 Backlog, 3 comments newest 40806; 446 and 445 Done; `key >= HPSMPOC-445` lists 445, 446, 447; `text ~ "zzqq-no-such-string-9d41"` 0 hits. Done-when sentences printed from the descriptions (paragraph 7 of 447 and 319; 308's from `Done-when:` to ` Relates`).
- Records main `e7986dc0e3320e03cc1b4f70c93d7d89c6e20728`; open records PRs 0 (`pulls/99999` 404); CLARIFICATIONS.md 5760 lines, C-308 `:5734`, C-309 `:5744`, C-310 `:5753`, no C-311, so next free C-311; BACKLOG.md (repository root, not under 1_Project_Definition: the first fetch from that path returned 404, the root path worked) 3660 lines, B1367 section `:3645`, B1367-C1 `:3656`; history.md 2789 lines. Mentions of B1373, B1374, B1372, 2075486b in the three files 0/0/0; HPSMPOC-447 -w: clarifications 1, backlog 3.
- Review B1373: 46 lines, verdict `:1` GO WITH FINDINGS, F1 Minor `:37`, F2 `:38`, F3 `:39`.
- Panes (`tmux list-panes -a`): `%0 tuesday`, `%1 fleet-monitor` at 07:40. REFUSE 7 terms over kits B1371 (0,0,0,0), B1372 (1,0,0,10), control B1367 (5,3,0,2). `lsof -iTCP:9500-9999 -sTCP:LISTEN` 0 lines. `df -g` 103 free; load1 1.83.
- `stamp_brief.py` dry run on a scratchpad copy with the slots file: 10 slots stamped, 0 four-underscore lines left.

## D-decisions
- D-1 One C-entry (C-311) covers 447, the shared 319/308 last clause, and the key outcomes; the review's F1 is a BACKLOG row (B1374-1, accounts for F1 to F3), plus a pointer row; no ticket.
- D-2 447's done-when under option (b) is read as three clauses A (accepted with reason), B (header says windows), C (no behaviour change). Clause A rests on the header's own "left narrow on purpose" reason plus the seat's comment as the record; stated openly because the comment is part of the recording (Q-2).
- D-3 The choice for 447 is the coordinator's, not the product owner's: the kit forbids calling it a ruling; the Done rule C-263 is the product owner's and is quoted.
- D-4 B469-5 stays "met under the product owner's ruling" and is quoted from comment 40860; the closing classes of B1367 are carried.
- D-5 The seat copies the review report into the project Briefs/ at Step 0 (not committed) so line pointers into it can be proved; the original stays in Tuesday's folder.
- D-6 Shorter than B1367: 1 entry, 3 comments, no history B-list; the clocks are +40/+70/+100.
- D-7 Slots default to safe: JIRA HOLD, MOVE COMMENT-ONLY, RECORDS HOLD, LAND SEAT.

## Q-questions for Tuesday (each with a default)
- Q-1 Slots. Recommend JIRA WRITE, MOVE CLOSE-IF-MET, RECORDS WRITE, LAND SEAT. Default if you decline: the file's HOLD / COMMENT-ONLY / HOLD / SEAT (nothing posted).
- Q-2 Is clause A of 447 (recording the gap as accepted) satisfied by the seat's own comment plus the header's reason, or must the acceptance exist before the move? Default: the comment is the record (kit as written); a stricter reading makes MOVE COMMENT-ONLY for 447.
- Q-3 308's clause 1 rests on the gate's 30 of 30 figures relayed in comment 40806 (never re-run by anyone this morning). Default: MET by the row's presence and the relayed figures, said so in the comment; say if you want it counted UNMEASURED.
- Q-4 Launch window ends 09:30 in the slots file; adjust to your plan.

## UNMEASURED
No write of any kind by me beyond the three files; helper re-points listed, not run; a fourth main push after 07:39:39; the shard jobs of runs 42296681684 and 42187059450 (I read their run conclusions success and B1367's STATUS names both shard jobs success; I did not re-list their jobs); number of empty-name panes; whether `closing1367.py` accepts the new sentences; the gate's 30-of-30 figures; the CI log of nothing (no hosted call).

## Outside-the-fences disclosure
Read-only reads: the project's Jira helpers (GET only, token never printed), `gh api -X GET` under the HPSM-POC `GH_CONFIG_DIR`, the project's `.tools/b1367/` helper sources, B1367's STATUS and the review report, the drafter-rules, the template kit, `model-routing.md:98`, `models_latest.json`, B1371 and B1372 kits (term counts only), `lsof`, `tmux list-panes`. No decision card, no queue listing, no staged or WEDNESDAY/FRIDAY tree, no ledger. Scratch files (raw fetches, rd.py, cm.py, trial.md) are in the session scratchpad only. One `sed -i ''` on my own kit (the drafter's file, not a project file) fixed a wording slip. No Artifact or mail.
