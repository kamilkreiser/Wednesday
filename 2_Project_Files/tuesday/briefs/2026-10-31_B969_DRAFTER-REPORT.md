STARTABLE
# B969 drafter report | SEAT-R93 records kit for PR #244 to #257 (drafted 2026-10-31 about 09:25 to 10:00 AEDT, Sonnet 5.5, read-only)

## BLUF
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-31_B969_SEAT-R93_hpsmpoc-records-244-257.md` (251 lines, unstamped; `.pre-stamp` copy beside it). Unstamped copy reads 13 four-underscore lines (12 slots + last line), 0 non-ASCII lines, 0 `@X@` tokens.
- None of the thirteen PRs has a record: #244 #245 #246 #247 #248 #249 #250 #251 #252 #254 #255 #256 #257 each read 0 in records CLARIFICATIONS, history, BACKLOG and JIRA.md (control: #243 reads 4 / 3 / 3 / 0). #249 is merged (2026-10-30 16:05:20 AEDT, squash `37bc6323`) and unrecorded, so it is in. All thirteen are merged; #259 and #260 are open.
- Scope: 19 landing comments (one per ticket key), 9 residual tickets (T1 to T9), 13 C-entries (default C-232 to C-244 in merge order), BACKLOG section, 1 history entry, 32 catch-up STATUS copies. Jira caps: 9 creates, 14 label adds (12 planned), exactly 19 comments, 0 transitions unless DONE-251-SLOT = MOVE-DONE (then 2).
- **Launch gate: the Step-8 gate check does NOT clear right now.** B964 to B967 are `GATE VERDICT: PENDING` (last line `WORKING:`) and gate panes G231 to G234 are live. The seat would do everything, push `records/b969`, open no PR and STOP at Step 8. Launch after the four gates end, or accept the push-and-stop (Q-1).
- **Main moved:** code main is `32fc17507a20d9dc6421ebdd7a7ee0061ae6214a` (PR #253, merged 09:51:25 AEDT 31 Oct, 10 check-runs in progress). Your list ended at `edf36342`. #253 is not in the kit (its second gate B965 is still PENDING, yet it merged); named in the kit as not recorded (Q-2).

## Measured (read-only)
- `gh -X GET` under the project GH_CONFIG_DIR: pulls and squash commits of all 13 (merged_at, squash, head, commits, paths, lines, 1 parent, verification valid, subject length 82 to 100, `localdomain` 0 each, control `94274a75` = 1); code main `32fc1750`; open code PRs 258, 259, 260.
- Records repo: main `303324d5` (PR #155 = B925's merge); 0 open PRs; `records/b969` absent (control `records/b925` present); highest C-number C-231; BACKLOG.md and JIRA.md sit at the repo ROOT (not under 1_Project_Definition); the working copy in the project is STALE (C-numbers stop at 192 there).
- tmux: no R93, no records pane. Live: tuesday %0, fleet-monitor %1, builders H68 H74 H76 H77, gates G231 to G234. `lsof` 9980-9999: nothing listening.
- Sonnet id from models_latest.json levels.sonnet.model_id: `claude-sonnet-5-5`.
- All 32 catch-up STATUS files: sha256 prefix, lines, last-line family, mtime age (all older than 700 minutes), counts of `HP Restricted` / e-mail-shape / non-ASCII / account-handle lines (program with a firing control). Absent from records main: 0 hits each; B914 B916 B919 B920 B922 B924 present.
- COPY anchors (23 spans from the gate STATUS files): each FROM and TO occurs exactly once in its line, 23 of 23, 0 non-ASCII, 0 hits on the banned-term scan (control fires 3 of 3). The Jira text lines of the kit also scan clean (59 lines, banned words and builder numbers 0).

## Which PRs already had records
None of the thirteen (see BLUF). Jira landing comments were NOT read (the kit forbids the drafter Jira); Step 3 reads every key and SKIPs any key already carrying its marker.

## D-decisions (mine)
- D-1 One comment per ticket key (19), not per PR: a ticket with no comment has no landing record. Per-key marker `REC-LAND<PR>-31OCT-K<key>`.
- D-2 One C-entry per PR (13), as B914 did, in merge order, numbers reserved consecutively; the seat's all-refs scan decides the first free number.
- D-3 Residue batched into 9 tickets: T1 B959-2; T2 B962-1, B962-5, B947-11, B947-12, B947-15; T3 B961-1 plus B943-2, B943-3, B943-5 (the gate's own "residue with cells" list for #251); T4 B963-1, -2, -3; T5 the two axe items; T6 Demo-name; T7 B953-3; T8 Home tile and next-actions sentence; T9 step-previous rows. Everything else is rows only.
- D-4 Fix-shapes are COPIED by program from the gate lines (FROM/TO anchors, backticks and `**` stripped, nothing else edited); a span that trips the banned-term scan is HELD, never edited.
- D-5 Jira ban list kept from B925, so the word "phase" cannot appear: T8 is hand-written ("the new label"), the #256 WHAT is overridden, T2-5 is hand-written (the route name contains the word). B954 is allowed in T5 and T9 only, as the builder STATUS file name they cite.
- D-6 CI is read per squash at Step 2 and written as read; no "green" by inference. Main's head currently has runs in progress.
- D-7 Catch-up copies widened to 32 files (all builder and gate STATUS files of the 13 PRs, plus B925, B953, B954 which tickets cite). RECORDS-COPY-SLOT SKIP keeps the 10 files the tickets cite as provenance so no ticket cites a missing file.

## Q-questions (defaults)
- Q-1 Launch now (push-and-stop at Step 8, PR later) or wait until B964 to B967 end? Default: wait; launch when the gate check is clear, so one seat lands it.
- Q-2 Add #253 (HPSMPOC-387, B953 NO GO round 1, B965 round 2 PENDING) to a later records kit? Default: yes, a separate kit after B965 ends.
- Q-3 Your list said the axe `region` / `scrollable-region` Notes came from B953 and B959. I found NO such text in B953 or B959; the two axe items are in B958 (B958-1, scrollable-region-focusable on the one-customer wrapper, #254) and in the #260 builder STATUS (B954 line 125, moderate `region`, identical on base). T5 uses those. Default: keep T5 as written.
- Q-4 DONE-251-SLOT: HPSMPOC-403 and -404 are test-only (precedent C-177 to C-180, C-186). Default COMMENT-ONLY (B925 kept 398 open the same way).
- Q-5 T3 also carries B943-2, B943-3, B943-5 (the gate's residue list), beyond your "falsy-only neighbour". Default: keep them in T3 (one ticket for one PR's residue).
- Q-6 T2 item 1 copies the gate's words list ("the product owner approves or rewords each"). Default: keep (it is the gate's text, no ruling made).
- Q-7 T6 (Demo name on main's Home and /customers/quollridge) and T7 (B953-3, now on main with #253) have no gate fix-shape for T6; T7's fix-shape comes from the builder's round-2 report lines 193 and 200 (Step 2 asserts it, else HELD). Default: keep.

## Stamp values (Tuesday fills; suggested)
- STAMP / Stamped by: Tuesday, read whole with this report; answers to Q-1 to Q-7 above.
- LAUNCH WINDOW: after B964 to B967 end (gate-check clear); through launch_when_cool, one waiter; live beside: HPSM-POC builders H68 H74 H76 H77 until they end.
- DONE-251-SLOT: COMMENT-ONLY. RECORDS-COPY-SLOT: COPY.
- Hard stop: target 120 and hard stop 240 minutes after the seat's own Step-0 date.
- Heads at launch: records main `303324d5b1b8cdfee89305443184ffdf956e8f20`; code main `32fc17507a20d9dc6421ebdd7a7ee0061ae6214a` (re-read at the stamp).
- Launch authority: the product owner's 2026-10-16 merge-once-tested grant; Kam's 2026-10-24 standing order; records seats land their own branch (B871 B880 B884 B907 B914 B924 B925).
- Model receipt: `model: claude-sonnet-5-5 -- C8 records (C7 for ticket texts and the comments) -- ports none: confirmed by Tuesday`. Launch must carry `BRIEF_SEAT_LEVEL=sonnet`.
- GATE-CLEAR: NOT CLEAR at drafting (B964 to B967 PENDING; panes G231 to G234 live); Tuesday re-reads at the stamp. AUTH-RULINGS: none beyond the launch authority. Sequencing: default STOP to Tuesday at Step 8 if the gate check fails (branch pushed, no PR).

## Not done / unmeasured
No Jira read, no write, no record file touched. Not measured: CI state of the 13 squashes, existing Jira comments, the Jira search tokenisation of the new markers, anything after about 09:55. Scratch mirrors of records files are in the session scratchpad `b969/` (not part of any project).
