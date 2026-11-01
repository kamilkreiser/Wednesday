STARTABLE: YES (after Tuesday fills 14 slots and the last line; Q-1 to Q-7 each have a default)

# B1040 DRAFTER REPORT | SEAT-R111 (records) | HPSM-POC | the B1031 UAT deploy of 77c3132e + keep-awake, the landing of PR #270, the wake-time 500 ticket | drafted 2026-11-01 12:2x-12:5x AEDT by an Agent-tool sub-agent (read-only)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1040_SEAT-R111_hpsmpoc-records-uat-deploy-77c3132e-270.md` (95 lines, sha256 `32812bfc5bda370af5d431f7e0ce9dc1124f2a63b04575d53daead245ea8a1ef`). Pre-stamp: same path + `.pre-stamp`, made by `cp -n`, `cmp` EQUAL, the same sha256. Slot count (`/usr/bin/grep -c -E '_''_''_''_'`) **15** = 14 slot lines + the last line (the kit's REFUSE 1 control says 15). `@[A-Z_]+@` 0. Person-name / card-id scan over the kit: 0 (the one card-shaped string is the B1031 kit's FILE NAME; the kit tells the seat never to write it into a record and to neutralise it in the scan class).

## BLUF
- One records seat (Sonnet, C8; `model-routing.md:98`, C7 `:97`; `models_latest.json` line 23 `claude-sonnet-5-5`) records: C-260, the B1031 deploy of `77c3132e` to UAT plus the one-way keep-awake DB change (cost about AUD 326/month; the cost brake printed, never run; wake test as measured; ANSWER-2's decision); C-261, the PR #270 landing (if C-COUNT = TWO); 13 deploy comments + 1 on HPSMPOC-427 = **14 comments**; 1 new ticket for the wake-time API 500; BACKLOG rows; history; up to 4 catch-up copies.
- **Moves**: only by a new `move1040.py` that selects the transition by NAME `Done` (to `Done`, category done; prints the id, expected 41; refuses on 0 or 2 or more; read-back resolution must be exactly `Done`, never Won't Do / Duplicate / Cannot Reproduce), each after a per-key ancestry check (`compare/<merge>...77c3132e` ahead/identical, behind 0) and a cited Done-when line.
- Launch: `WED_USAGE_STOP=100 bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/HPSM-POC-R111 "WED_USAGE_STOP=100 BRIEF_SEAT_LEVEL=sonnet bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1040_SEAT-R111_hpsmpoc-records-uat-deploy-77c3132e-270.md'"`

## Facts (instrument; control)
1. **B1040 / R111 free.** `ls` of tuesday/briefs and the project Briefs: `_B1040_` 0 and 0, `SEAT-R111` 0 and 0 (controls `_B1039_` 3 in tuesday/briefs, `SEAT-R110` 2); recursive `R111` over tuesday/briefs 0; `B1040` appears only in today's daily note line 151 (this commission). `.tools/b1040`, `.tools/wt-b1040` absent (`ls -d` rc 1; control `.tools/b1033` present). `.tools/.git-lock` absent.
2. **Records main `dd44bce8cc810209e2ae816ad2d0d9d48956caa6`** (`gh api git/ref/heads/main`); open records PRs 0. CLARIFICATIONS 5053 lines, 259 `### C-` headings, highest C-259 at line 5036; `C-260` boundary count 0/0/0 in CLARIFICATIONS/BACKLOG/history (control C-259 1/12/1). BACKLOG 2865 lines (B1033 section at 2810); history 2629 lines (B1033 entry at line 3). Blobs `f28c4b42`, `ed2e9b90`, `aa87e33d`. Records hold nothing of the deploy or #270 (`PR #270`, `a3a06b9a`, `B1036`, `B1034`, `cost brake` 0 each; control `77c3132e` 5/4/0).
3. **Code main `a3a06b9a...` = PR #270**; open code PRs 0. #270: merged 11:59:14 AEDT, head `1353d337`, base `1f4bf7bc`, 1 commit, 2 test files +27 -0; squash tree `3d46254d...` = head tree; message = B1036's `squash-subject.txt` + blank + `squash-body.txt` (python True; one-char mutant False); `localdomain` 0, `Co-Authored-By` 1; head check-runs 20/20 success; squash 19 (18 success, 1 skipped); `ci` 41259135668 completed success; `Push on main` 41259136132 completed success; open code-scanning alerts on main 0.
4. **Deployed range** `compare/e8ac3f29...77c3132e`: ahead 8, behind 0; subjects map to keys 399; 414; 407; 413 416 418 419; 411 415 408; (none: #266); 422 423; (none: #268). = D-10's 12 keys. **Ancestry per merge vs 77c3132e**: #261-#267 `ahead` (7..1, behind 0), #268 `identical`; **controls** #269 `behind 1`, #270 `behind 2`.
5. **Jira** (GETs via `.tools/b1033/jira.py` `api`, scratch drivers, no token printed): all 14 keys Task, Backlog (new); transitions exactly 11 Backlog / 21 Selected for Development / 31 In Progress / 41 Done (to Done, category done) on every key; comment counts 1 each for the 12 + 426 (ids in the kit), 427 has 0. Newest key HPSMPOC-427; `key = HPSMPOC-428` 0. Statuses: Backlog, Selected for Development, In Progress, Done (no Declined status); resolutions Done, Won't Do, Duplicate, Cannot Reproduce; earlier moves read back resolution Done (HPSMPOC-359, -360, -298). Controls: `key = HPSMPOC-268` 1, `qxv9k2zzprobe` 0, `REC-DEPLOY-31OCT-K357` 1. Kit markers `REC-DEPLOY-01NOV` 0, `REC-LAND270-01NOV-K427` 0; label `b1040-2026-11-01` 0.
6. **No ticket records the wake-time 500**: `B1031` 0, `"database wake"` 0, `"connect budget"` 0, `"waking database"` 1 (HPSMPOC-426, does not record the 500), `readRetry` 2 (426, 98 Done), `transient` 11 (Backlog: HPSMPOC-207 start-up login reset, related; HPSMPOC-126 unrelated).
7. **Sources**: B1031 STATUS 318 lines / `5824cfb33457c699` / 68942 B / mtime 12:16:32; first line `DEPLOY B1031: DONE, ...`; last line `DEPLOYED: UAT @ 77c3132e (WEB + API) + review database kept awake | ...`. ADDENDUM-1 sha256 `27a8e4d8...` and ANSWER-2 `78a20066...` = the hashes B1031 recorded at `:115` and `:259`. B1034 94 / `99d04b175cf0f887` / `READY FOR QA`; B1036 269 / `f79dc80fc3835fd6` / `VERDICT: ... GO WITH FINDINGS (round 1 of 2)`; B1033 127 / `77f4ac21169df606` / `RECORDS COMMITTED:`. Decision card (via `decision_queue.sh show`): ruled a, `ruled_ts` 10:05:05+11:00; your brief says live board 10:04:18. The kit records both and does not reconcile them (the C-255 form); no card id is in the kit.
8. **Catch-up scans** (python byte program; planted e-mail and high-byte controls fire): listed line by line in the CATCHUP-LIST slot. B1031 has 4 non-ASCII lines (U+2026 x3 lines, U+00B7 x1), `git@github.com`, `...@datasec-rd.com`, and the subscription and tenant ids on line 39.
9. Panes at 12:38: `%0 tuesday`, `%1 fleet-monitor` only. load1 2.39.

## D-decisions (taken by the drafter; change at stamp)
- D-1 Default **MOVE-DEPLOYED** follows your brief ("the Done rule now lets the D-10 keys + HPSMPOC-426 MOVE"). The kit makes the C-entry and `<MOVE-ON>` say plainly that this is the **first move after a UAT-only deploy** (C-250 moved nothing; the demo is still held at `c00e2828`).
- D-2 **HPSMPOC-399, -407, -408 are never moved** (open items: C-249, C-252, C-254). They get `<MOVE-OFF-ITEMS>`.
- D-3 HPSMPOC-426's comment is its own text (`<DEP-426>`), with the wake walk and the 500 (per `{F1-SENTENCE}`).
- D-4 C-numbers in time order: C-260 deploy (11:09), C-261 #270 (11:59).
- D-5 HPSMPOC-388 gets no comment, though #270's title names it. C-261 records that.
- D-6 The move helper never uses an id from the kit. `post.py ... done` is forbidden.
- D-7 Jira B-number allow-list: B1031, B1034, B1036, B1040. Azure resource names and host names are banned from Jira texts. The cost-brake command appears in the records only.

## Q-questions (one slot each; default in brackets)
- Q-1 DONE-MOVES: MOVE-DEPLOYED or COMMENT-ONLY? [MOVE-DEPLOYED]. Tension: B972's stamp ruled COMMENT-ONLY for the last UAT-only deploy. Two of its reasons were "demo held", which still holds, and "new words not reviewed", which does not apply to these 8 PRs.
- Q-2 MOVE-KEYS [414, 413, 416, 418, 411, 415, 422, 426]. 419 and 423 are HELD because the records never ruled their Done-when (C-253, C-257). Name them to move them.
- Q-3 KEY-427: COMMENT-ONLY or MOVE-TEST-ONLY? [COMMENT-ONLY]. #270 is test-only and NOT deployed. The C-177/C-186 precedent moved such keys only on an explicit stamp slot, and C-129 says they stay in Backlog.
- Q-4 FINDING-TICKET [FILE].
- Q-5 C-COUNT: TWO or ONE? [TWO]. Your brief said "one C-entry for the deploy". #270 is a landing, and precedent gives each landing its own entry.
- Q-6 CATCHUP-LIST [B1031, B1033, B1034, B1036 with the listed allowances]. B1031's non-ASCII and partial e-mail lines HOLD it unless you allow them.
- Q-7 DB-STATE: your own read-only `az sql db show` at stamp. The seat never runs `az`.

## UNMEASURED
- The scan of every origin ref for C-numbers (the drafter scanned main only).
- The PR #270 body text.
- Each gate closure line cited for a move (B977:172, B981:42-53, B989 for 411/415, B1031:148 and :162): relayed from the records, not re-opened by the drafter.
- The live DB state (Tuesday's read is relayed).
- Whether HPSMPOC-423's added ranges cover every range its Done-when names.
- The real monthly cost.

## Outside the fences (for Tuesday, not the seat)
- The B1031 STATUS (line 39) names subscription `a6b8fe11-...` / tenant `ec01829b-...` (`...@datasec-rd.com`). None of the five Datasec environments in the workspace CLAUDE.md lists it, though records C-07 covers it. Worth a line in the environment map.
- B1033's STATUS and Step-0 copy sit uncommitted in the project root. The kit offers B1033 as a catch-up copy.
- The post-merge `ci` run on `1f4bf7bc` read cancelled (B1033-10). It is still yours to re-run or wave.
