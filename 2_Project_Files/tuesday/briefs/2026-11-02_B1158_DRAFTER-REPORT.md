STARTABLE: YES after your stamp (11 slots; one is blocking in effect: RULING-CLOCKS must be filled or C-279 and the HPSMPOC-424/-425 texts HOLD, and with them the two Kam cards). Everything else has a safe default. Kit: `2026-11-02_B1158_SEAT-R143_hpsmpoc-records-276-277-278.md`, Sonnet (C8 row `model-routing.md:98`), pane `Datasec/HPSM-POC-R143`, 12 four-underscore lines (11 slots + last line), under 40 KB, ASCII.

## Contradictions with this commission
1. **Ruling clocks.** The B1145 stamp says 425 b at 17:59, 424 b at 18:00, sentence a at 19:14:45. The decision store (`show`, exact ids) says ruled_ts 18:00:33 (Evidence submitted card, b), 18:00:36 (register card, b), 19:15:18 (sentence card, a), all +11:00. Seconds and minutes differ. The kit types no clock; slot RULING-CLOCKS is yours, and the seat records what you stamp.
2. **Why HPSMPOC-417 stays open.** The B1147 STATUS says the ticket's breadcrumb and customer-name links in `customer/parts.tsx` are "outside this branch". True of #278's seven paths, but the breadcrumb link was already built by #272 (`parts.tsx:59` carries `min-h-11`; commit `55e6063c`). The remainder the STATUS actually measures is the header logo link, 28 to 40 px (N9, :183), plus the gate's scope question (:161, :199). The customer-name link: no pointer found (UNMEASURED). The kit's 417 text says only what the STATUS supports.
3. **DELTA 942, "HPSMPOC-432 after 409".** Not a records item: it sequences a builder. 409 item 1 is already on main (#274, `4b3cefae`), so the precondition is met. Not in the kit.
4. **A third ruled card.** The commission names two cards (424, 425). The sentence card (`hpsmpoc-425-evidence-sentence-1102`, ruled a) is also recorded in C-279 and built in #277. The kit prints `--delivered` lines for the two named only (Q-5).
5. The commission's "word-pack rule" is not a rule that applies here (C-136 was one pack's ruling). The standing rule that applies is "every word a customer will see is Kam's" (C-105); the kit writes no customer word beyond the ruled sentence.

## BLUF
One records seat, five entries (C-279 rulings, C-280/281/282 the three landings, C-283 the 407 decision under a slot), ten Jira comments at most and seven moves at most (424, 425, 429, 430, 433, 434, 435), 11 BACKLOG rows plus a pointer row, one history entry. Not moved by design: 417 (header logo link under 44 px, scope), 431 (met only on the product owner's reading), 407 (comment only). HPSMPOC-434 now has its pin: row T15 at `GroupedSummaryNumberAndTitleGuardTests.cs:392`, assertion :398, on code main; the K3 grep of B1134 that read 0 hits then now reads 1, so the kit carries `<KEPT-434>` and the move. All three squashes carry exactly the gates' reviewed blobs (4 of 4, 3 of 3, 7 of 7) and equal the gates' landing files byte for byte.

## Facts re-measured (instrument, time; controls in the kit)
- Records main `5ee23ad0` (gh api, 22:21:42); open records PRs 0; `records/b1158` 404, control `records/b1134` exists; CLARIFICATIONS 5371 lines, `### C-279` 0, `### C-278` 1 (raw GET at 5ee23ad0, grep).
- Code main `2a770988`, chain 5f128fb8 -> 491348ed -> e30eb113 -> 2a770988 (parents by API), 0 open PRs, `pulls/99999` 404. Merge clocks 20:00:53, 21:53:09, 21:59:06 AEDT (python, plus 11 h; plus 10 h planted differs).
- Squash blobs vs head blobs 4/4, 3/3, 7/7 (python over `contents` API; control differs). Squash message == gate subject + ` (#n)` + body: True x3, mutant False x3 (python). Head check-runs 20 success x3. Open code-scanning alerts 0, control `state=fixed` returns a row.
- Jira (project helpers, 22:11 to 22:15): 436 issues, Done 292, Backlog 141, In Progress 3; ten keys Backlog, unassigned, comments as in the kit; full markers 0, control marker 1.
- Hosted state: 56 STATUS first lines, 0 DEPLOYED/PARTIAL/ROLLED BACK, control lists B1031 and B1048. `compare a3a06b9a...2a770988` ahead 8 behind 0.
- 407 census at 2a770988: 10 tracked `.bicep` files, `uniqueString(` 2 times in 2 files (`infra/main.bicep:56`, `infra/showcase-ai.bicep:43`), both the pinned form; planted line matches 1.
- Disk 262 GiB; root `.git` 647940 KB; panes `%0`, `%102`, `%101`, `%1`, no HPSM-POC pane; no port assigned (`lsof` 9900-9999 empty).

## D-decisions (mine, overridable)
- D1 five entries (rulings separate from landings, as C-277 / C-278 did); order by merge time after the rulings.
- D2 the four #276 tickets share one slot; each still HOLDS to comment-only on its own failed check.
- D3 417 and 431 never move; 407 never moves.
- D4 no ticket creates: the three Minors (B1131-1, B1156-1, B1147-2) become BACKLOG rows (the commission said "ticket or record").
- D5 REFUSE 9 added: a failed squash check HOLDS that PR's Jira writes.

## Q-questions for Tuesday (each with a default)
- Q-1 HPSMPOC-431: move on the gate's "MET-ON-A-READING"? Default no: comment only (at 360/375 the button is below, not beside, the sentence).
- Q-2 HPSMPOC-407: the decision is yours (SCREEN-1745 recommendation, accepted in the daily note); item 4's reason is thin ("no real template uses these shapes" fits item 2 better). Default COMMENT-ONLY, no move (the infra suite state is not read). Set DECL-407 HOLD to drop C-283.
- Q-3 Seven moves are a lot for a records seat. Default as drafted (each gate STATUS says the done-whens are met; Done rule C-263). Set the two MOVE slots to COMMENT-ONLY to cut to comments.
- Q-4 Tell Kam about the left-out entries (B1156 N1) at the landing: already decided by you per DELTA 952; the seat tells no one. Default: unchanged.
- Q-5 Add the sentence card to the `--delivered` lines? Default no (commission names two).
- Q-6 Launch window and hard stop: default outer bound 02:00 AEDT 2026-11-03.

## UNMEASURED
The ruling clocks as the board shows them; whether #278's post-merge push checks end success (in progress when read); a real SqlClient close (HPSMPOC-429); the customer-name link of HPSMPOC-417; the review-copy and demo shas after today; whether the five HPSMPOC-430 rows match the B1095 kit rows K1 to K5 beyond their names (kit says the seat confirms).

## Outside-the-fences disclosure
- Wrote only the two files, plus session-scratchpad copies (`.../scratchpad/d/`: raw GET copies of records files and code files, three card dumps, command outputs). No write in any project, repo, Jira, the card store or any host.
- Read the card store with `decision_queue.sh show <exact id>` three times (ids above; the full output of two cards was printed to my terminal, the third through a filter). No `list`.
- Jira: GET only, through `.tools/b1134/{desc1014,read,jcount1134}.py`, plus two inline `python3 -I -B` snippets importing the project's `jira.py` `api` for GET (two comment bodies, assignee fields); no token printed.
- Read `.tools/b1134/*` file contents (headers and `move1134.py`) and listed `.tools/` directory contents (no `du` over it). Read my own seat's files (`NEXT-PICKUP-TUESDAY.md`, today's daily note, the SCREEN-1745 brief, the B1095/B1145 kits) and the local project STATUS and evidence files. Did not read `fleet/briefs_staged/`, scoreboard, `_ledger.md`, any WEDNESDAY/FRIDAY tree or non-Datasec project.
- `tmux list-panes`, `lsof`, `df`, `uptime`, `du -sk` of the root `.git`. No `cd` typed. Hook advisories on case-sensitive greps fired several times; the counts that matter carry controls (K3 grep, markers, headings).
- One kit line (the 18 and 27 red-row counts for 424/425) rests on STATUS lines I printed by awk and re-verified by program; the pointers into the B1107/B1131/B1147/B1156 STATUS files were each re-printed by program after one off-by-one (B1107 :104-108, B1156 :129-135) was found and fixed.
